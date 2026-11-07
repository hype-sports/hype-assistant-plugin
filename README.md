# Hype Sports for Claude

Use Hype from Claude Code. The Hype Sports plugin connects Claude to your own Hype account, so you can ask about your leagues, teams, players, events and settings in plain words, and have Claude help with the work: setting up a league, scheduling a season, running a draft, managing a team, catching up on notifications and more.

The plugin gives Claude a Hype assistant and one skill per area. It never gives you a separate account or extra rights: Hype checks your own access on every request, exactly as it does in the app.

## Access

**Access is invite-only for now: signing in works only for invited Hype accounts.** Installing the plugin does not grant access. If your account has not been invited, sign-in is refused.

## Install in Claude Code

You need Claude Code installed and signed in. Then run:

```sh
claude plugin marketplace add hype-sports/hype-assistant-plugin
claude plugin install hype@hype-sports
```

Start a new Claude Code session and pick a command from the Skills table below. Skills that can change anything only start when you run their command, and starting one is never approval to save anything.

To try a local copy instead, load its folder for one session:

```sh
claude --plugin-dir /absolute/path/to/hype-assistant-plugin
```

Do not load both copies together.

## The Hype assistant

Select `hype:hype` in `/agents`, or start a session with `claude --agent hype:hype`, and ask the Hype assistant for help with your leagues, teams, players or events.

The assistant uses only Hype's own tools, through your own sign-in. Before any save, change, send or deletion it explains exactly what will happen and waits for your yes. With look-only access it cannot change anything. It never retries a change by itself: after an unclear result it reads the current state and asks you. Text inside your Hype records is treated as information, never as instructions. When an area skill fits, it points you to the matching `/hype:<skill>` command.

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
| `/hype:league-staff` | See and manage a league's staff | Preview |
| `/hype:clubs-and-tournaments` | Set up clubs and tournaments, invite Admins and answer invitations | Preview |
| `/hype:catch-up` | Catch up on your notifications | Preview |
| `/hype:notification-settings` | Change which notifications you get and when | Preview |
| `/hype:my-account` | Look after your own account details and settings | Preview |
| `/hype:terms-and-privacy` | Read Hype's Terms and privacy information | Preview |
| `/hype:review-evaluations` | Look over your own evaluation scores, scores another coach shared with you and player lists you manage, then rank or summarise them | Preview |

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
