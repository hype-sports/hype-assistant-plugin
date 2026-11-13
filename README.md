<img src="logo.png" alt="Hype" width="96">

# Hype Sports for Claude

Hype helps leagues, coaches, players and families run youth sports. This plugin lets you do your Hype work by asking Claude in plain words: set up a league, plan a season, run a draft, look after your team, invite families and catch up on what you missed. It works inside your own Hype account with exactly the rights you already have, shows you every change before it happens, and waits for your yes.

## What you can ask

Type the command, then say what you need. You can also just ask in plain words: Claude can point you to the right command (`/hype:start-here`).

| You might say | Command | Status |
| --- | --- | --- |
| "Set up Lakeside Youth Soccer for the fall with 8U, 10U and 12U divisions." | `/hype:league-setup` | Available |
| "Register Jordan Vale in the 10U division." | `/hype:league-setup` | Available |
| "Am I a supporter, and is my supporter ring showing?" | `/hype:my-support` | Available |
| "Plan a round-robin season for 10U and show it to me before anything is saved." | `/hype:season-schedule` | Preview |
| "Get the 10U draft ready and set the pick order." | `/hype:run-a-draft` | Preview |
| "Invite the parents from this sign-up sheet." | `/hype:invite-families` | Preview |
| "Show my team roster this season." | `/hype:manage-my-team` | Preview |
| "Write an announcement for my team: practice moves to 6 pm Thursday." | `/hype:my-feed` | Preview |
| "Rank my players from Saturday's tryout scores." | `/hype:review-evaluations` | Preview |
| "What did I miss?" | `/hype:catch-up` | Preview |
| "Turn off push notifications for drafts." | `/hype:notification-settings` | Preview |
| "Where do I change the theme in Hype?" | `/hype:find-in-hype` | Preview |

**Available** means the command's main steps have been tried from start to finish on a test account. **Preview** means not every step has been tried yet. Every command checks what Hype offers before it starts and tells you plainly when something it needs is missing. The full list is in [Skills](#skills).

## Install and update

You need Claude Code installed and signed in. For commissioners and coaches, we recommend installing Hype for your whole account so its tools are available in every folder:

```sh
claude plugin marketplace add hype-sports/hype-assistant-plugin
claude plugin install hype@hype-sports --scope user
```

Tip: If no Hype tools appear, the plugin is not enabled for this folder; install it with `--scope user`, or enable it for the folder.

### Update the plugin

For the account-wide installation above, refresh the marketplace and update the plugin:

```sh
claude plugin marketplace update hype-sports
claude plugin update hype@hype-sports --scope user
```

If installed in another scope, use that original scope instead of `--scope user`. Restart Claude Code to apply the update, then run `/mcp`, select `plugin:hype:hype` and choose **Reconnect** before continuing Hype work.

## Sign in

1. In Claude Code, run `/mcp`, select `plugin:hype:hype` and choose **Authenticate**.
2. Your browser opens Hype. Sign in with your own Hype account.
3. Hype's approval page shows which assistant is asking and offers two choices: **Read only** lets it look but never change anything; **Read and change** lets it set things up for you, and each change still waits for your yes.
4. Your browser hands the connection back to Claude Code, and `/mcp` shows `plugin:hype:hype` as connected.

**Read-only connections.** A Read only connection has no change tools at all. If a command says the tools it needs to make a change are missing, that is your Read only choice, not an outage.

**If you are signed out.** Run `/mcp`, select `plugin:hype:hype`, choose **Authenticate** and finish in the browser. Never paste sign-in links, codes or tokens into a chat. A new sign-in link replaces any earlier one, so always use the newest.

**Refresh tools.** When Hype adds tools, or Claude says "Hype's tools changed", run `/mcp`, select `plugin:hype:hype` and choose **Reconnect**. If it also says the plugin is older than Hype needs, [update the plugin](#update-the-plugin) first.

To stop using the connection in Claude Code, disable `plugin:hype:hype` in `/mcp`. To remove its access in Hype, open Settings, go to Security → Connected assistants and choose Disconnect for that assistant.

## Who can use it today

Access is by invitation for now. Installing the plugin does not grant access. An account that is not on the list can still sign in, but Hype then answers every request with "not found". To ask for access, use the [Hype support page](https://hypesports.live/support.html).

## How it keeps you safe

- **You see every change first.** Before it saves, changes, sends or deletes anything, it shows exactly what will happen and waits for your yes in a later message. Starting a command is never a yes.
- **Nothing is retried on its own.** If a step's result is unclear, it checks what really happened and asks you.
- **It acts only as you.** It signs in as your own Hype account and has your own rights, nothing more. It never asks for your password: the browser sign-in is the only place for it.
- **Your records are data, not orders.** Text inside your Hype records is treated as information, never as instructions.
- **Long jobs.** Keep your approvals in the main conversation. Plain helper assistants may not get the Hype connection, so check that a helper can see Hype before handing it work.
- **Progress records.** The Hype assistant (`claude --agent hype:hype`) can keep a progress record in one file you choose, only when you ask. That limit is an instruction, not a file lock; see [your own files](skills/league-setup/references/own-files.md).

## Using Hype from other assistants

Hype's connection is a standard MCP server at `https://api.hypesports.live/api/mcp`, with browser sign-in.

- **Tested:** Claude Code, with this plugin.
- **Untested:** custom connectors in claude.ai and Claude Desktop, ChatGPT connectors, and Codex. They may connect, but we have not tried them, so we give no setup steps for them yet.

Other assistants get Hype's tools, and each tool's own safety rules, but not this plugin's skills, the Hype assistant or the `/hype:` commands.

## Your privacy

- [Privacy Policy](https://hypesports.live/privacy.html)
- [Terms of Service](https://hypesports.live/terms.html)

## Get help

Visit the [Hype support page](https://hypesports.live/support.html).

## Skills

| Command | What it helps with | Status |
| --- | --- | --- |
| `/hype:start-here` | Ask in plain words and get the right command to run, with one line on what it does; changes nothing | Preview |
| `/hype:league-setup` | Create a league and its divisions, rename it, register players and archive it | Available |
| `/hype:my-support` | See your supporter status and change your supporter ring setting | Available |
| `/hype:season-schedule` | Plan an unsaved round-robin season; change, cancel or undo cancellation of one shared game. Whole-season saving with saved Fields is not available yet; the app's Add game adds one game at a time with a typed location | Preview |
| `/hype:run-a-draft` | Prepare and run a division draft, with clock guidance and supported pause, resume, skip and undo actions | Preview |
| `/hype:manage-my-team` | See your Roster, Staff and seasons; add, change, take off, put back and roll over players; invite coaches and parents/guardians, resend or cancel staff invitations; answer parent/guardian requests and league memberships; check emergency contacts | Preview |
| `/hype:players-families` | Manage your players' profiles, team history and invitations | Preview |
| `/hype:invite-families` | Map supplied enrollment columns, review one invitation job across divisions in one league, and resume from your chosen progress record; review same-row emergency contacts separately per team | Preview |
| `/hype:league-staff` | See and manage a league's staff | Preview |
| `/hype:clubs-and-tournaments` | Set up clubs and tournaments, invite Admins and answer invitations | Preview |
| `/hype:my-feed` | Read your Feed and comments, write comments and give Hypes (each after your yes), and send announcements with a 10-second Undo | Preview |
| `/hype:catch-up` | Catch up on your notifications | Preview |
| `/hype:notification-settings` | Change which notifications you get and when | Preview |
| `/hype:my-account` | Look after your own account details and settings | Preview |
| `/hype:find-in-hype` | Find screens and readable records, including tournaments and managed player profiles; get links, locate appearance settings and Report a problem; no changes or submissions | Preview |
| `/hype:terms-and-privacy` | Read Hype's Terms and privacy information | Preview |
| `/hype:review-evaluations` | Look over your own evaluation scores, scores another coach shared with you and player lists you manage, then rank or summarise them | Preview |
| `/hype:run-evaluations` | Score players, save private notes, manage sharing and player lists, start evaluations, add dates and choose your private evaluation source for a draft | Preview |

For how a skill works and its limits, open its `SKILL.md`; for example, the [season scheduling workflow](skills/season-schedule/SKILL.md).

Developers: see [CONTRIBUTING.md](CONTRIBUTING.md) to add or change a skill.

## License

MIT. See [LICENSE](LICENSE).
