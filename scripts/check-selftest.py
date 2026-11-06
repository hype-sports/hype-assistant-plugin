#!/usr/bin/env python3
"""Exercise the offline checker in an isolated repository with no Hype data."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

source = Path(__file__).with_name('check.sh')
with tempfile.TemporaryDirectory(prefix='hype-plugin-check-') as temp:
    root = Path(temp)
    for folder in ('scripts', '.claude-plugin', 'skills/example', 'tools'):
        (root / folder).mkdir(parents=True)
    shutil.copyfile(source, root / 'scripts/check.sh')
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
    def check(label, expected, needle):
        result = subprocess.run([str(root / 'tools/bash'), str(root / 'scripts/check.sh')], env=env, text=True, capture_output=True)
        output = result.stdout + result.stderr
        assert (result.returncode == 0) == expected, (label, output)
        assert needle in output, (label, output)
        print(f'PASS: {label}')
    check('valid files and validator invocation', True, 'STUB validator: plugin validate --strict .\n')
    check('plugin manifest validation', True, 'STUB validator: plugin validate --strict .claude-plugin/plugin.json')
    check('marketplace validation', True, 'STUB validator: plugin validate --strict .claude-plugin/marketplace.json')
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
