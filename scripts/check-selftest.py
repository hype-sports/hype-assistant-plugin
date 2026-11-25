#!/usr/bin/env python3
"""Exercise the offline checker in an isolated repository with no Hype data."""
import os
import json
import runpy
from pathlib import Path
import shutil
import subprocess
import tempfile

source = Path(__file__).with_name('check.sh')
runpy.run_path(str(source.with_name('xlsx-to-csv-selftest.py')), run_name='__main__')
runpy.run_path(str(source.with_name('put-chat-photo-selftest.py')), run_name='__main__')
compatibility = runpy.run_path(str(source.with_name('tool-versions.py')))
for label, catalog, minimum, installed, expected in (
    ('older plugin needs update and reconnect notice', 1, '0.1.48', '0.1.47', compatibility['NOTICE'] + '\n' + compatibility['UPDATE_NOTICE']),
    ('older plugin and different catalog need update and reconnect', 2, '0.1.48', '0.1.47', compatibility['NOTICE'] + '\n' + compatibility['UPDATE_NOTICE']),
    ('current plugin has no notice', 1, '0.1.48', '0.1.48', ''),
    ('newer plugin has no notice', 1, '0.1.48', '0.1.49', ''),
    ('newer catalog needs update even when minimum is unchanged', 2, '0.1.48', '0.1.48', compatibility['NOTICE'] + '\n' + compatibility['UPDATE_NOTICE']),
    ('numeric version order', 1, '0.1.10', '0.1.9', compatibility['NOTICE'] + '\n' + compatibility['UPDATE_NOTICE']),
):
    assert compatibility['reconnect_notice'](catalog, minimum, installed) == expected, label
    print(f'PASS: {label}')
version_globals = compatibility['reconnect_notice'].__globals__
original_catalog = version_globals['EXPECTED_CATALOG_VERSION']
try:
    version_globals['EXPECTED_CATALOG_VERSION'] = 2
    assert compatibility['reconnect_notice'](1, '0.1.48', '0.1.48') == compatibility['NOTICE']
finally:
    version_globals['EXPECTED_CATALOG_VERSION'] = original_catalog
print('PASS: older server catalog needs reconnect without a plugin update')
for catalog, minimum in ((True, '0.1.48'), (0, '0.1.48'), (None, '0.1.48'), (1, None), (1, 'bad')):
    try:
        compatibility['reconnect_notice'](catalog, minimum, '0.1.48')
    except ValueError:
        pass
    else:
        raise AssertionError('Missing/malformed versions must be unavailable, not compatible or stale')
print('PASS: missing or malformed version facts are unavailable')
with tempfile.TemporaryDirectory(prefix='hype-plugin-check-') as temp:
    root = Path(temp)
    for folder in ('scripts', '.claude-plugin', 'skills/example', 'skills/my-account/references', 'shared', 'agents', 'tools'):
        (root / folder).mkdir(parents=True)
    shutil.copyfile(source, root / 'scripts/check.sh')
    shutil.copyfile(source.with_name('tool-versions.py'), root / 'scripts/tool-versions.py')
    version_paths = (root / 'agents/hype.md', root / 'shared/tool-versions.md')
    for command in ('bash', 'dirname', 'git', 'python3'):
        (root / 'tools' / command).symlink_to(shutil.which(command))
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['PATH'] = str(root / 'tools')
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args], env=env, stderr=subprocess.STDOUT)
    manifest = root / '.claude-plugin/plugin.json'
    manifest.write_text('{"name":"hype","version":"0.1.0"}\n')
    (root / '.claude-plugin/marketplace.json').write_text('{}\n')
    skill = root / 'skills/example/SKILL.md'
    good_skill = '---\nname: example\ndescription: "A sample: quoted description."\n---\n'
    good_skill += '\n[tool-version check](../../shared/tool-versions.md)\n'
    skill.write_text(good_skill)
    readme = root / 'README.md'
    good_links = '/hype:example /hype:my-account\n[Skill](skills/example/SKILL.md)\n[Again][skill]\n[skill]: skills/example/SKILL.md\n`[code](missing.md)`\n```md\n[code](missing.md)\n```\n'
    readme.write_text(good_links)
    git('init', '-q')
    git('add', '.claude-plugin', 'skills', 'README.md')
    git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Fixture baseline')
    git('update-ref', 'refs/remotes/origin/main', 'HEAD')
    manifest.write_text('{"name":"hype","version":"0.1.1"}\n')
    changelog = root / 'CHANGELOG.md'
    good_changelog = '# Changelog\n\n## [0.1.10] - 2026-01-01\n\n## 0.1.1 - 2026-01-01\n'
    changelog.write_text(good_changelog)
    claude = root / 'tools/claude'
    claude.write_text('#!/bin/bash\nprintf "STUB validator: %s\\n" "$*"\n')
    claude.chmod(0o755)
    def check(label, expected, needle, sync_versions=True, args=()):
        if sync_versions:
            version = json.loads(manifest.read_text())['version']
            for path in version_paths:
                header = "---\nname: hype\ndescription: 'Fixture agent.'\nmodel: inherit\ncolor: cyan\ntools:\n  - Read\n  - Write\n  - Edit\n  - mcp__plugin_hype_hype__*\n---\n" if path == version_paths[0] else ''
                path.write_text(header + f'Plugin release: {version}. Expected operation catalog version: {compatibility["EXPECTED_CATALOG_VERSION"]}.\n\n{compatibility["NOTICE"]}\n{compatibility["UPDATE_NOTICE"]}\n/hype:example /hype:my-account\n')
        result = subprocess.run([str(root / 'tools/bash'), str(root / 'scripts/check.sh'), *args], env=env, text=True, capture_output=True)
        output = result.stdout + result.stderr
        assert (result.returncode == 0) == expected, (label, output)
        assert needle in output, (label, output)
        print(f'PASS: {label}')
        return output
    public_file = root / 'public.txt'
    for label, value in (
        ('ticket reference rejected', 'HYPE-' + '1234'),
        ('singular decision reference rejected', 'decision ' + '12'),
        ('mixed-case plural decision reference rejected', 'DeCiSiOnS ' + '1234'),
        ('lowercase ticket reference rejected', 'hype-' + '42'),
        ('numbered decision with a hash rejected', 'decision #' + '7'),
    ):
        public_file.write_text('Public notes\n' + value + '\n')
        git('add', 'public.txt')
        output = check(label, False, 'FAIL: public.txt:2\n')
        assert [line for line in output.splitlines() if line.startswith('FAIL:')] == ['FAIL: public.txt:2'], output
        assert value not in output, 'Private reference appeared in checker output'
    public_file.write_text('Public release notes describe a scheduling change.\nVersion 0.1.50 shipped in 2026; a decision was made.\n')
    check('clean public file passes', True, 'Public references:')
    public_file.unlink()
    git('rm', '-q', '--cached', 'public.txt')
    git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-q', '--allow-empty', '-m', 'Fix\n\nPart of ' + 'HYPE-' + '77')
    output = check('private reference in a commit message rejected', False, 'FAIL: commit ')
    assert 'HYPE-' + '77' not in output, 'Private reference appeared in checker output'
    git('update-ref', 'refs/remotes/origin/main', 'HEAD')
    check('commit messages already on origin/main are not rescanned', True, 'Commit messages: checked 0 commits')
    check('valid files and validator invocation', True, 'STUB validator: plugin validate --strict .\n')
    check('plugin manifest validation', True, 'STUB validator: plugin validate --strict .claude-plugin/plugin.json')
    check('marketplace validation', True, 'STUB validator: plugin validate --strict .claude-plugin/marketplace.json')
    check('directory profile validation', True, 'STUB validator: plugin validate --profile directory --strict .claude-plugin/plugin.json')
    check('skill component parsing', True, 'STUB validator: plugin validate --strict skills')
    check('agent component parsing', True, 'STUB validator: plugin validate --strict agents')
    readme.write_text(good_links.replace('/hype:example', 'missing shortcut'))
    check('missing skill routing rejected', False, 'command missing from agent or README')
    readme.write_text(good_links)
    skill.write_text(good_skill.replace('---\n\n', 'disable-model-invocation: true\n---\n\n'))
    check('manual-only skill rejected', False, 'plain requests must be able to select')
    skill.write_text(good_skill)
    catalog = root / 'catalog.json'
    catalog.write_text('{"catalogVersion":1,"required":{"team-roster-read":[]}}')
    skill.write_text(good_skill + '\n`team-roster-read`\n')
    check('known documented tool passes', True, 'Tool drift: checked 1', args=('--tool-catalog', str(catalog)))
    skill.write_text(good_skill + '\n`team-invented-read`\n')
    check('unknown documented tool rejected', False, 'unknown documented tool team-invented-read', args=('--tool-catalog', str(catalog)))
    skill.write_text(good_skill)
    shared_tools = root / 'shared/tools.md'
    shared_tools.write_text('`team-invented-read`\n')
    check('unknown shared-reference tool rejected', False, 'unknown documented tool team-invented-read', args=('--tool-catalog', str(catalog)))
    shared_tools.unlink()
    catalog.write_text('{"catalogVersion":2,"required":{"team-roster-read":[]}}')
    check('different catalog version rejected', False, 'version differs from the plugin expected catalog', args=('--tool-catalog', str(catalog)))
    for malformed_catalog in ('{}', '{"catalogVersion":1,"required":{}}', '{"catalogVersion":1,"required":[]}', '{'):
        catalog.write_text(malformed_catalog)
        check('malformed or empty tool catalog rejected', False, 'cannot read a valid server', args=('--tool-catalog', str(catalog)))
    catalog.unlink()
    skill.write_text(good_skill)
    version_paths[0].write_text('Plugin release: 0.0.0. Expected operation catalog version: 1.\n' + compatibility['NOTICE'])
    check('stale embedded plugin version rejected', False, 'tool-version release/catalog pin', sync_versions=False)
    check('restored version pins pass', True, 'Tool versions:')
    version_paths[0].write_text(version_paths[0].read_text().replace(compatibility['UPDATE_NOTICE'], 'Missing update instructions'))
    check('missing update notice rejected', False, 'tool-version release/catalog pin', sync_versions=False)
    check('restored update notice passes', True, 'Tool versions:')
    for old, new in (('model: inherit', 'model: bogus'), ('color: cyan', 'color: banana'), ('mcp__plugin_hype_hype__*', 'mcp__hype__*'), ('tools:', 'tools: 123')):
        check('prepare valid agent fixture', True, 'Agent header:')
        version_paths[0].write_text(version_paths[0].read_text().replace(old, new))
        check('invalid agent header rejected', False, 'agent header must keep', sync_versions=False)
    check('restored agent header passes', True, 'Agent header:')
    version_paths[1].write_text('Plugin release: 0.1.1. Expected operation catalog version: 2.\n' + compatibility['NOTICE'])
    check('stale catalog expectation rejected', False, 'tool-version release/catalog pin', sync_versions=False)
    check('restored catalog pin passes', True, 'Tool versions:')
    claude.unlink()
    check('missing Claude explicitly skipped', True, 'SKIPPED:')
    malformed = root / 'broken.json'
    malformed.write_text('{')
    check('malformed JSON rejected', False, 'invalid JSON')
    malformed.unlink()
    skill.write_text(good_skill.replace('name: example', 'name: wrong'))
    check('wrong skill name rejected', False, 'name must equal folder')
    skill.write_text(good_skill.replace('"A sample: quoted description."', 'Unquoted: description'))
    check('unquoted description rejected', False, 'description must be')
    skill.write_text('name: example\n')
    check('missing header rejected', False, 'missing front matter')
    skill.write_text(good_skill)
    for bad in ('[Broken](missing.md)', '[Broken][no-definition]', '[Broken][b]\n[b]: missing.md', '[Wrapped\nlink](missing.md)', '[Wrapped\nlink][missing]'):
        readme.write_text(bad)
        check('broken Markdown link rejected', False, 'FAIL: README.md:')
    readme.write_text(good_links + '\n[Broken heading](skills/example/SKILL.md#missing)\n')
    check('broken Markdown heading rejected', False, 'missing Markdown heading')
    readme.write_text(good_links + '\n# Same heading\n# Same heading\n[Here](#same-heading)\n[Second](#same-heading-1)\n')
    check('same-file and duplicate headings pass', True, 'Markdown links:')
    readme.write_text(good_links)
    changelog.write_text('# Changelog\n\n## 0.1.10 - 2026-01-01\n')
    check('missing changelog entry rejected (0.1.10 is not 0.1.1)', False, 'has no "## 0.1.1" entry')
    changelog.unlink()
    check('missing changelog file rejected', False, 'has no "## 0.1.1" entry')
    for bad_heading in ('## [0.1.1 - 2026-01-01', '## 0.1.1] - 2026-01-01'):
        changelog.write_text('# Changelog\n\n' + bad_heading + '\n')
        check('half-bracketed changelog heading rejected: ' + bad_heading, False, 'has no "## 0.1.1" entry')
    for version in ('0.1.0', '0.0.9', '00.2.0'):
        manifest.write_text('{"version":"' + version + '"}')
        changelog.write_text('# Changelog\n\n## ' + version + ' - 2026-01-01\n')
        check('invalid version change rejected: ' + version, False, 'must be greater than' if version != '00.2.0' else 'cannot compare plugin versions')
    changelog.write_text(good_changelog)
    manifest.write_text('{"version":"0.1.9"}')
    git('add', '.claude-plugin/plugin.json')
    git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Numeric comparison baseline')
    git('update-ref', 'refs/remotes/origin/main', 'HEAD')
    manifest.write_text('{"version":"0.1.10"}')
    check('numeric version comparison', True, 'Version: 0.1.10 >')
    git('update-ref', '-d', 'refs/remotes/origin/main')
    check('missing origin/main rejected', False, 'cannot compare')
    git('update-ref', 'refs/remotes/origin/main', 'HEAD')
    claude.write_text('#!/bin/bash\nexit 7\n')
    claude.chmod(0o755)
    check('validator failure propagates', False, 'Version:')
print('PASS: offline checker self-checks (stub validator; no product calls)')
