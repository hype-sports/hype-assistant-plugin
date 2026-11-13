## Contributing

- Put each skill in `skills/<name>/SKILL.md`, with optional `references/` and `examples/` folders inside that skill. Keep the workflow focused and link supporting files where needed.
- Start `SKILL.md` with YAML front matter. The checker requires `name` to match the folder name and `description` to be a nonempty, quoted, single-line value. Describe concrete requests the skill helps with.
- Use made-up names only in examples, never real people's data.
- Any skill that can save, change or send anything must set `disable-model-invocation: true`. Show exactly what will happen and ask for explicit approval before every change; starting a skill is not approval. Never retry a change automatically.
- Add a new skill to the `start-here` routing table and the command list in `agents/hype.md`.
- Add a README Skills row with the command, what it helps with, and **Available** or **Preview**. Use Available only after the main journey has run end to end on a test account; otherwise use Preview.
- Raise `version` in `.claude-plugin/plugin.json` and add an entry for that version in `CHANGELOG.md`. Also update the `Plugin release:` line in `agents/hype.md` and `skills/my-account/references/tool-versions.md` to match; `check.sh` enforces both pins.
- Run `bash scripts/check.sh` and paste its output in the pull request. It checks JSON, skill front matter, relative Markdown file links, the commit messages since `origin/main`, the version increase over `origin/main`, and the matching changelog entry. It also runs strict plugin and marketplace validation when Claude Code is available; if those checks are skipped, have a reviewer run them before merge.
- Keep internal tracker references out of all public files and commit messages; `check.sh` rejects them and reports only the file and line, or the commit.
- Get one independent review before merge.

## Reporting problems

Open a GitHub issue describing the problem and how to reproduce it. Never include passwords, tokens or personal data.

For security problems, do not open a public issue: report them privately with GitHub's **Report a vulnerability** button on this repository's Security tab.
