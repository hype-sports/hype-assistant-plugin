#!/usr/bin/env bash
# Offline only: refresh origin/main separately before running the pre-merge check.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -I - "$@" <<'PY'
import argparse
import json
import re
import runpy
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

errors = []
files = [p for p in Path('.').rglob('*') if p.is_file() and '.git' not in p.parts]
private_reference = re.compile(r'(?i:\bHYPE-[0-9]+\b|\bdecisions?\s+#?[0-9]+\b)')
text_count = 0
for path in sorted(files):
    try:
        lines = path.read_text().splitlines()
    except UnicodeDecodeError:
        continue
    text_count += 1
    for number, line in enumerate(lines, 1):
        if private_reference.search(line):
            errors.append(f'{path}:{number}')
print(f'Public references: checked {text_count} text files')
try:
    commits = subprocess.check_output(['git', 'rev-list', 'origin/main..HEAD'], text=True, stderr=subprocess.DEVNULL).split()
    for commit in commits:
        if private_reference.search(subprocess.check_output(['git', 'log', '-1', '--format=%B', commit], text=True)):
            errors.append(f'commit {commit[:12]} message')
    print(f'Commit messages: checked {len(commits)} commits since origin/main')
except subprocess.CalledProcessError:
    errors.append('commit messages: cannot list origin/main..HEAD')

json_files = sorted(p for p in files if p.suffix == '.json')
for path in json_files:
    try:
        json.loads(path.read_text())
    except (ValueError, OSError) as exc:
        errors.append(f'{path}: invalid JSON ({type(exc).__name__})')
print(f'JSON: checked {len(json_files)} files')

skills = sorted(Path('skills').glob('*/SKILL.md'))
if not skills:
    errors.append('skills: no SKILL.md files found')
for path in skills:
    text = path.read_text()
    header = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.S)
    if not header:
        errors.append(f'{path}: missing front matter')
        continue
    names = re.findall(r'^name:\s*([^\n]+)$', header[1], re.M)
    descriptions = re.findall(r'^description:[ \t]*(.+)$', header[1], re.M)
    if len(names) != 1 or names[0].strip().strip('\"\'') != path.parent.name:
        errors.append(f'{path}: name must equal folder name')
    if len(descriptions) != 1 or not re.fullmatch(r'"(?:[^"\\]|\\.)+"|\'(?:[^\']|\'\')+\'', descriptions[0].strip()):
        errors.append(f'{path}: description must be a nonempty quoted single-line value')
print(f'Skill headers: checked {len(skills)} files')
agent = Path('agents/hype.md').read_text()
agent_header = re.match(r'\A---\n(.*?)\n---(?:\n|\Z)', agent, re.S)
if not agent_header:
    errors.append('agents/hype.md: missing agent front matter')
else:
    header = agent_header[1]
    keys = re.findall(r'^([a-z-]+):', header, re.M)
    expected = ['name', 'description', 'model', 'color', 'tools']
    description = re.findall(r'^description:\s*(.+)$', header, re.M)
    tools = re.findall(r'^  - (.+)$', header, re.M)
    if (sorted(keys) != sorted(expected)
        or not all(line in header.splitlines() for line in ('name: hype', 'model: inherit', 'color: cyan', 'tools:'))
        or len(description) != 1
        or not re.fullmatch(r'\'(?:[^\']|\'\')+\'|"(?:[^"\\\\]|\\\\.)+"', description[0])
        or tools != ['Read', 'Write', 'Edit', 'mcp__plugin_hype_hype__*']):
        errors.append('agents/hype.md: agent header must keep the reviewed name, model, color, quoted description and scoped tools')
print('Agent header: checked reviewed fields and tool namespace (not a general YAML parser)')
readme = Path('README.md').read_text()
for path in skills:
    command = f'/hype:{path.parent.name}'
    if command not in agent or command not in readme:
        errors.append(f'{path}: command missing from agent or README')
    if re.search(r'^disable-model-invocation:\s*true\s*$', path.read_text(), re.M):
        errors.append(f'{path}: plain requests must be able to select this skill')
print('Skill routing: agent, README and plain-request selection checked')

parser = argparse.ArgumentParser(description='Offline plugin checks; optionally compare documented tool names to a supplied server catalog.')
parser.add_argument('--tool-catalog', type=Path)
args = parser.parse_args()
catalog_version = None
if args.tool_catalog:
    try:
        catalog = json.loads(args.tool_catalog.read_text())
        required = catalog['required']
        if (not isinstance(required, dict) or not required
            or not all(isinstance(name, str) and isinstance(inputs, list) for name, inputs in required.items())
            or type(catalog['catalogVersion']) is not int or catalog['catalogVersion'] < 1):
            raise ValueError('invalid tool catalog')
        catalog_version = catalog['catalogVersion']
        names = set(required) | {'request-key-new'}
        roots = {name.split('-')[0] for name in names}
        endings = {name.split('-')[-1] for name in names}
        skill_names = {path.parent.name for path in skills}
        checked = set()
        for path in [Path('agents/hype.md'), *Path('skills').rglob('*.md'), *Path('shared').rglob('*.md')]:
            for match in re.finditer(r'`(?:mcp__plugin_hype_hype__)?([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`', path.read_text()):
                name = match[1]
                if name in skill_names or name.split('-')[0] not in roots or name.split('-')[-1] not in endings:
                    continue
                checked.add(name)
                if name not in names:
                    errors.append(f'{path}: unknown documented tool {name}')
        print(f'Tool drift: checked {len(checked)} explicit tool names against supplied catalog (not workflow completeness or live behavior)')
    except (OSError, ValueError, KeyError, TypeError):
        errors.append('tool catalog: cannot read a valid server required-input catalog')
else:
    print('SKIPPED: tool drift (supply --tool-catalog with the current server required-input catalog)')

def heading_ids(path):
    counts = {}
    ids = set()
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$', path.read_text(), re.M):
        slug = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        ids.add(f'{slug}-{count}' if count else slug)
    return ids

markdown = sorted(p for p in files if p.suffix == '.md')
link_count = 0
for path in markdown:
    text = re.sub(r'^(`{3,}|~{3,}).*?^\1[^\n]*$', '', path.read_text(), flags=re.M | re.S)
    text = re.sub(r'`[^`\n]*`', '', text)
    definitions = dict((m[0].strip().lower(), m[1]) for m in re.findall(r'^\s*\[([^\]]+)\]:\s*(<[^>]+>|\S+)', text, re.M))
    targets = re.findall(r'!?\[[^\]]*\]\(\s*(<[^>]*>|[^\s()]*(?:\([^()]*\)[^\s()]*)*)(?:\s+[^\n]*?)?\)', text)
    targets += list(definitions.values())
    for label, ref in re.findall(r'!?\[([^\]]+)\]\[([^\]]*)\]', text):
        if (ref or label).strip().lower() not in definitions:
            errors.append(f'{path}: undefined Markdown link reference [{ref or label}]')
    for target in targets:
        target = target.strip('<>')
        url = urlsplit(target)
        if url.scheme or url.netloc:
            continue
        destination = path.parent / unquote(url.path) if url.path else path
        link_count += 1
        if not destination.exists():
            errors.append(f'{path}: missing relative link target {target}')
        elif url.fragment and destination.suffix == '.md' and unquote(url.fragment) not in heading_ids(destination):
            errors.append(f'{path}: missing Markdown heading {target}')
print(f'Markdown links: checked {link_count} relative file targets in {len(markdown)} files')

try:
    try:
        base = json.loads(subprocess.check_output(['git', 'show', 'origin/main:.claude-plugin/plugin.json'], text=True, stderr=subprocess.DEVNULL))['version']
    except subprocess.CalledProcessError:
        # First release: origin/main has no manifest yet, so there is no earlier version to beat.
        base = None if subprocess.run(['git', 'rev-parse', '--verify', '-q', 'origin/main'], capture_output=True).returncode == 0 else ''
        if base == '':
            raise
    current = json.loads(Path('.claude-plugin/plugin.json').read_text())['version']
    def release(value):
        # This repository publishes stable releases only (MAJOR.MINOR.PATCH).
        if not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', value):
            raise ValueError('expected stable MAJOR.MINOR.PATCH')
        return tuple(map(int, value.split('.')))
    if base is None:
        release(current)
        print(f'Version: {current} (first release; origin/main has no manifest)')
    elif release(current) <= release(base):
        errors.append(f'plugin version {current} must be greater than origin/main {base}')
    else:
        print(f'Version: {current} > origin/main {base}')
    compatibility = runpy.run_path('scripts/tool-versions.py')
    if catalog_version is not None and catalog_version != compatibility['EXPECTED_CATALOG_VERSION']:
        errors.append('tool catalog: version differs from the plugin expected catalog')
    pin = f'Plugin release: {current}. Expected operation catalog version: {compatibility["EXPECTED_CATALOG_VERSION"]}.'
    for path in (Path('agents/hype.md'), Path('shared/tool-versions.md')):
        text = path.read_text()
        if pin not in text or compatibility['NOTICE'] not in text or compatibility['UPDATE_NOTICE'] not in text:
            errors.append(f"{path}: tool-version release/catalog pin or reconnect notice differs; write '{pin}' to match plugin.json in agents/hype.md and shared/tool-versions.md, and keep the reconnect notice")
    for path in skills:
        if '[tool-version check](' not in path.read_text():
            errors.append(f'{path}: missing tool-version check')
    print('Tool versions: instruction release/catalog pins and workflow checks verified')
    changelog = Path('CHANGELOG.md').read_text() if Path('CHANGELOG.md').exists() else ''
    if not re.search(rf'^## (?:{re.escape(current)}|\[{re.escape(current)}\])(?:\s|$)', changelog, re.M):
        errors.append(f'CHANGELOG.md has no "## {current}" entry for the plugin.json version')
    else:
        print(f'Changelog: entry for {current} found')
except (subprocess.CalledProcessError, ValueError, KeyError, TypeError, OSError) as exc:
    errors.append(f'cannot compare plugin versions ({type(exc).__name__}); ensure origin/main exists and versions are stable semver')

for error in errors:
    print(f'FAIL: {error}', file=sys.stderr)
if errors:
    sys.exit(1)
PY

if command -v claude >/dev/null 2>&1; then
  claude plugin validate --strict .
  # A folder containing both manifests can select the marketplace, so check each explicitly too.
  claude plugin validate --strict .claude-plugin/plugin.json
  claude plugin validate --strict .claude-plugin/marketplace.json
  claude plugin validate --profile directory --strict .claude-plugin/plugin.json
  # Skills need explicit component parsing; our Python check above guards the agent fields.
  claude plugin validate --strict skills
  claude plugin validate --strict agents
else
  printf '%s\n' 'SKIPPED: Claude strict validation (claude is not on PATH)'
fi
printf '%s\n' 'PASS: all available plugin checks passed'
