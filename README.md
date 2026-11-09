# Hype Sports for Claude

Use Hype from Claude Code. The Hype Sports plugin connects Claude to your own Hype account, so you can ask about your leagues, teams, players, events and settings in plain words, and have Claude help with the work: setting up a league, scheduling a season, running a draft, managing a team, catching up on notifications and more.

The plugin gives Claude a Hype assistant and one skill per area. It never gives you a separate account or extra rights: Hype checks your own access on every request, exactly as it does in the app.

## Access

**Access is invite-only for now: signing in works only for invited Hype accounts.** Installing the plugin does not grant access. If your account has not been invited, sign-in is refused.

## Install in Claude Code

You need Claude Code installed and signed in. For commissioners and coaches, we recommend installing Hype for your whole account so its tools are available in every folder:

```sh
claude plugin marketplace add hype-sports/hype-assistant-plugin
claude plugin install hype@hype-sports --scope user
```

Tip: If no Hype tools appear, the plugin is not enabled for this folder; install it with `--scope user`, or enable it for the folder.

Start a new Claude Code session and pick a command from the Skills table below. Skills that can change anything only start when you run their command, and starting one is never approval to save anything.

To try a local copy instead, load its folder for one session:

```sh
claude --plugin-dir /absolute/path/to/hype-assistant-plugin
```

Do not load both copies together.

## The Hype assistant

Select `hype:hype` in `/agents`, or start a session with `claude --agent hype:hype`, and ask the Hype assistant for help with your leagues, teams, players or events.

The assistant uses Hype's own tools through your own sign-in. If you ask it to maintain a progress record, it also has Read and Write for the one exact file you choose; it is instructed never to access any other file. **This is an instruction, not a hard file-access lock:** Claude Code's plugin-agent tool list cannot restrict Read and Write to a single path. It has no Bash or Edit tool. With no chosen progress path, it must not access files. Your record stays where you choose, is not published or kept by the plugin, and must stay out of git commits unless you say otherwise. It follows the [own-files rules](skills/league-setup/references/own-files.md), including the limits on contact details and sensitive information. When keeping progress, it saves “attempting” before each approved Hype write and the confirmed, refused or unknown outcome afterward; a failed progress save stops the next Hype write. Before any save, change, send or deletion it explains exactly what will happen and waits for your yes. With look-only access it cannot change anything. It never retries a change by itself: after an unclear result it reads the current state and asks you. Text inside your Hype records is treated as information, never as instructions. When an area skill fits, it points you to the matching `/hype:<skill>` command.

### Helpers and long jobs

Connection availability depends on how Claude Code starts the helper:

- **Forks of the connected conversation** inherit its Hype tools and conversation context.
- **The plugin's `hype` agent** allows the Hype tools through the person's existing connection. It does not sign in separately or gain extra rights.
- **Plain helper assistants** (such as general-purpose helpers) did not receive the plugin connection in the reported long-job run. Do not assume a plain helper has it, or send it work before checking.

Every helper must check that the needed live Hype tools are actually available before starting. A missing connection is a stop, not permission to authenticate another account or invent tool results. Claude Code versions may differ; this is the working pattern from the reported run, not a promise that every helper has a connection.

For a long job, keep the main conversation in charge of your approvals and Hype changes. Use connected forks or the `hype` agent for reads and proposals; background helpers cannot make Hype changes on relayed approval. Run any matching `/hype:<skill>` command in the main conversation. Process approved writes one at a time, not in parallel. If you request a progress file, choose its exact path and use only one writer for that file; never let helpers overwrite each other's progress. A progress record is not permission to resume changes automatically: after a lost answer, read the current Hype state, explain what is confirmed or unknown, and ask before another write. Never recreate or resend an action just because its answer was lost.

## The Hype connection

The plugin works through Hype's assistant connection at `https://api.hypesports.live/api/mcp`, signed in as your own Hype account; Hype's own rules decide what you can see and change.

Installing the plugin adds that connection; Claude Code lists it as `plugin:hype:hype`. To sign in, run `/mcp` in Claude Code, select `plugin:hype:hype` and choose Authenticate. Your browser opens Hype's sign-in page:

1. Sign in to Hype with your own account. Only invited accounts can connect.
2. Hype shows which assistant is asking, the Hype account it will act as, and the website its answer goes to. Allow lets it read and change things as you in Hype; Deny or closing the page gives it nothing.
3. Your browser hands the connection back to Claude Code, and `/mcp` shows `plugin:hype:hype` as connected.

The connection has your own rights in Hype and nothing more. To stop using it, disable `plugin:hype:hype` in Claude Code's `/mcp`; a way to disconnect assistants from inside Hype is coming. Never paste passwords, access tokens or other credentials into a conversation, this repository or a connection setting: the browser sign-in is the only place for your password.

## Skills

**Available** means the skill's main journey has been run end to end on a test account. **Preview** means the skill is not fully verified yet: some paths have not been run end to end, and some steps may still wait for Hype tools that are not live. Each skill checks which tools are live before it starts and stops plainly when something it needs is missing.

| Command | What it helps with | Status |
| --- | --- | --- |
| `/hype:league-setup` | Create a league and its divisions, rename it, register players and archive it | Available |
| `/hype:my-support` | See your supporter status and change your supporter ring setting | Available |
| `/hype:season-schedule` | Plan a division's round-robin season as an unsaved draft, and change or cancel existing shared games; saving a whole season is not available yet | Preview |
| `/hype:run-a-draft` | Prepare and run a division draft, with clock guidance and supported pause, resume, skip and undo actions | Preview |
| `/hype:manage-my-team` | See your Roster, Staff and seasons, invite a coach and answer staff invitations | Preview |
| `/hype:players-families` | Manage your players' profiles, team history and invitations | Preview |
| `/hype:invite-families` | Review supplied enrollment rows and invite parents/guardians per division; emergency contacts come later | Preview |
| `/hype:league-staff` | See and manage a league's staff | Preview |
| `/hype:clubs-and-tournaments` | Set up clubs and tournaments, invite Admins and answer invitations | Preview |
| `/hype:catch-up` | Catch up on your notifications | Preview |
| `/hype:notification-settings` | Change which notifications you get and when | Preview |
| `/hype:my-account` | Look after your own account details and settings | Preview |
| `/hype:find-in-hype` | Find screens and readable Home records, get links, locate appearance settings, and check where Report a problem is offered; no changes or submissions | Preview |
| `/hype:terms-and-privacy` | Read Hype's Terms and privacy information | Preview |
| `/hype:review-evaluations` | Look over your own evaluation scores, scores another coach shared with you and player lists you manage, then rank or summarise them | Preview |
| `/hype:run-evaluations` | Score players, save private notes, manage sharing and player lists, start evaluations, add dates and choose your private evaluation source for a draft | Preview |

For how a skill works and its limits, open its `SKILL.md`; for example, the [season scheduling workflow](skills/season-schedule/SKILL.md) and its [tools and data handling](skills/season-schedule/references/reference.md).

Adding a skill: see [CONTRIBUTING.md](CONTRIBUTING.md).

## Other Claude apps and Codex

Claude Code only for now.

## Maintainer checks

```sh
bash scripts/check.sh
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

File checks do not prove a signed-in workflow: before calling a skill Available, run its main journey end to end on a test account. Raise `plugin.json`'s version and add a `CHANGELOG.md` entry for each release.

Plugin format references:

- [Create a Claude Code plugin](https://code.claude.com/docs/en/plugins/create)
- [Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference)
- [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference)

## License

MIT. See [LICENSE](LICENSE).
