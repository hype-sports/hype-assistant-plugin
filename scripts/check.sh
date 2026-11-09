#!/usr/bin/env bash
# Offline only: refresh origin/main separately before running the pre-merge check.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -I - <<'PY'
import json
import re
import runpy
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

errors = []
files = [p for p in Path('.').rglob('*') if p.is_file() and '.git' not in p.parts]
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

# shortcut: check file targets, not heading fragments; add heading checks if docs start linking to local headings.
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
        if url.scheme or url.netloc or not url.path:
            continue
        link_count += 1
        if not (path.parent / unquote(url.path)).exists():
            errors.append(f'{path}: missing relative link target {target}')
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
    pin = f'Plugin release: {current}. Expected operation catalog version: {compatibility["EXPECTED_CATALOG_VERSION"]}.'
    for path in (Path('agents/hype.md'), Path('skills/my-account/references/tool-versions.md')):
        text = path.read_text()
        if pin not in text or compatibility['NOTICE'] not in text:
            errors.append(f'{path}: tool-version release/catalog pin or reconnect notice differs')
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
else
  printf '%s\n' 'SKIPPED: Claude strict validation (claude is not on PATH)'
fi
printf '%s\n' 'PASS: all available plugin checks passed'
