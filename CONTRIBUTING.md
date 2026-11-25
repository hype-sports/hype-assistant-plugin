## Contributing

- Put each skill in `skills/<name>/SKILL.md`, with optional `references/` and `examples/` folders inside that skill. Keep the workflow focused and link supporting files where needed.
- Start `SKILL.md` with YAML front matter. The checker requires `name` to match the folder name and `description` to be a nonempty, quoted, single-line value. Describe concrete requests the skill helps with.
- Use made-up names only in examples, never real people's data.
- Let plain requests select every skill; do not disable model invocation. Give descriptions concrete everyday trigger phrases and state which neighboring skill owns overlapping requests.
- Follow [One review, one yes, all changes](agents/hype.md#one-review-one-yes-all-changes) for all changes and side effects; link to it from the skill instead of adding per-item approval rules. Keep tool limits, access checks, request keys, receipts and safe recovery.
- Every skill that changes things must carry the identical four-bullet **How changes are confirmed** block used by the existing changing skills, as well as the link to the full shared rule.
- Add a new skill to the area list in `agents/hype.md`; its `/hype:` command is an optional shortcut.
- Add a README Skills row with the command, what it helps with, and **Available** or **Preview**. Use Available only after the main journey has run end to end on a test account; otherwise use Preview.
- Raise `version` in `.claude-plugin/plugin.json` and add an entry for that version in `CHANGELOG.md`. Also update the `Plugin release:` line in `agents/hype.md` and `shared/tool-versions.md` to match; `check.sh` enforces both pins.
- Run `bash scripts/check.sh` and `python3 -I scripts/check-selftest.py` and paste their output in the pull request. The checker covers JSON, skill header conventions, skill routing, relative Markdown file links, new commit messages, the version increase and changelog entry. It checks this agent's reviewed header fields and scoped tool list (not general YAML). With Claude Code available it also parses skill components and runs agent-directory, strict manifest and directory-profile validation; the CLI's agent-directory check alone does not validate agent fields; if skipped, a reviewer must run them before merge. The self-test uses a stub validator, not a real component parse.
- When server source is available, run `bash scripts/check.sh --tool-catalog /path/to/tool-required-inputs.json` with its current required-input catalog. This offline comparison checks explicit tool names with known tool prefixes/endings, not wildcard families, every possible typo, input schemas or workflow completeness. Review those against server source too; never commit a private source path or catalog. Without the option, tool drift is explicitly skipped.
- Tag each merged release as `vMAJOR.MINOR.PATCH`; do not tag an unmerged feature branch. Never rewrite old public commit messages.
- Directory submission needs a reviewer test account arranged privately through the submission form, never credentials in this repository. These local checks do not prove live sign-in, tool behavior or support for other assistant clients.
- Keep internal tracker references out of all public files and commit messages; `check.sh` rejects them and reports only the file and line, or the commit.
- Get one independent review before merge.

## Reporting problems

Open a GitHub issue describing the problem and how to reproduce it. Never include passwords, tokens or personal data.

For security problems, do not open a public issue: report them privately with GitHub's **Report a vulnerability** button on this repository's Security tab.
