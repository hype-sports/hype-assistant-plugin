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
compatibility = runpy.run_path(str(source.with_name('tool-versions.py')))
for label, catalog, minimum, installed, expected in (
    ('older plugin needs update and reconnect notice', 1, '0.1.48', '0.1.47', compatibility['NOTICE'] + '\n' + compatibility['UPDATE_NOTICE']),
    ('older plugin and different catalog need update and reconnect', 2, '0.1.48', '0.1.47', compatibility['NOTICE'] + '\n' + compatibility['UPDATE_NOTICE']),
    ('current plugin has no notice', 1, '0.1.48', '0.1.48', ''),
    ('newer plugin has no notice', 1, '0.1.48', '0.1.49', ''),
    ('different catalog needs notice', 2, '0.1.48', '0.1.48', compatibility['NOTICE']),
    ('numeric version order', 1, '0.1.10', '0.1.9', compatibility['NOTICE'] + '\n' + compatibility['UPDATE_NOTICE']),
):
    assert compatibility['reconnect_notice'](catalog, minimum, installed) == expected, label
    print(f'PASS: {label}')
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
    for folder in ('scripts', '.claude-plugin', 'skills/example', 'skills/my-account/references', 'agents', 'tools'):
        (root / folder).mkdir(parents=True)
    shutil.copyfile(source, root / 'scripts/check.sh')
    shutil.copyfile(source.with_name('tool-versions.py'), root / 'scripts/tool-versions.py')
    version_paths = (root / 'agents/hype.md', root / 'skills/my-account/references/tool-versions.md')
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
    good_skill += '\n[tool-version check](../my-account/references/tool-versions.md)\n'
    skill.write_text(good_skill)
    readme = root / 'README.md'
    good_links = '[Skill](skills/example/SKILL.md)\n[Again][skill]\n[skill]: skills/example/SKILL.md\n`[code](missing.md)`\n```md\n[code](missing.md)\n```\n'
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
    def check(label, expected, needle, sync_versions=True):
        if sync_versions:
            version = json.loads(manifest.read_text())['version']
            for path in version_paths:
                path.write_text(f'Plugin release: {version}. Expected operation catalog version: {compatibility["EXPECTED_CATALOG_VERSION"]}.\n\n{compatibility["NOTICE"]}\n')
        result = subprocess.run([str(root / 'tools/bash'), str(root / 'scripts/check.sh')], env=env, text=True, capture_output=True)
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
    ):
        public_file.write_text('Public notes\n' + value + '\n')
        git('add', 'public.txt')
        output = check(label, False, 'FAIL: public.txt:2\n')
        assert [line for line in output.splitlines() if line.startswith('FAIL:')] == ['FAIL: public.txt:2'], output
        assert value not in output, 'Private reference appeared in checker output'
    public_file.write_text('Public release notes describe a scheduling change.\n')
    check('clean public file passes', True, 'Public references:')
    public_file.unlink()
    check('valid files and validator invocation', True, 'STUB validator: plugin validate --strict .\n')
    check('plugin manifest validation', True, 'STUB validator: plugin validate --strict .claude-plugin/plugin.json')
    check('marketplace validation', True, 'STUB validator: plugin validate --strict .claude-plugin/marketplace.json')
    version_paths[0].write_text('Plugin release: 0.0.0. Expected operation catalog version: 1.\n' + compatibility['NOTICE'])
    check('stale embedded plugin version rejected', False, 'tool-version release/catalog pin', sync_versions=False)
    check('restored version pins pass', True, 'Tool versions:')
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
