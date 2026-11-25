<img src="logo.png" alt="Hype" width="96">

# Hype Sports for Claude

Hype helps leagues, coaches, players and families run youth sports. This plugin lets you do your Hype work by asking Claude in plain words: set up a league, plan a season, run a draft, look after your team, invite families and catch up on what you missed. It works inside your own Hype account with exactly the rights you already have, shows you every change before it happens, and waits for your yes.

## What you can ask

Just say what you need in plain words. Claude uses the matching Hype skill without making you type a command. If you ask for several changes, it shows the whole list once; one yes in your next message approves that exact list. The `/hype:` commands below still work as optional shortcuts.

| You might say | Optional shortcut | Status |
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

**Available** means the skill's main steps have been tried from start to finish on a test account. **Preview** means not every step has been tried yet. Skills that use Hype's tools check what Hype offers before they start and tell you plainly when something they need is missing. The full list is in [Skills](#skills).

## Install and update

You need Claude Code installed and signed in. For commissioners and coaches, we recommend installing Hype for your whole account so its tools are available in every folder:

```sh
claude plugin marketplace add hype-sports/hype-assistant-plugin
claude plugin install hype@hype-sports --scope user
```

If no Hype tools appear, check that the plugin is enabled for this folder, then follow [Sign in](#sign-in) and [Who can use it today](#who-can-use-it-today). Missing tools can have more than one cause.

### Update the plugin

For the account-wide installation above, refresh the marketplace and update the plugin:

```sh
claude plugin marketplace update hype-sports
claude plugin update hype@hype-sports --scope user
```

If installed in another scope, use that original scope instead of `--scope user`. Restart Claude Code to apply the update. If you have not restarted and Hype says its tools changed, run `/mcp`, select `plugin:hype:hype` and choose **Reconnect**.

## Sign in

1. In Claude Code, run `/mcp`, select `plugin:hype:hype` and choose **Authenticate**.
2. Your browser opens Hype. Sign in with your own Hype account.
3. Hype's approval page shows which assistant is asking and offers two choices: **Read only** lets it look but never change anything; **Read and change** lets it set things up for you, and the whole requested list of changes still waits for your one yes. Choose one and press **Allow** (or **Deny** to stop).
4. Your browser hands the connection back to Claude Code, and `/mcp` shows `plugin:hype:hype` as connected.

**Read-only connections.** A Read only connection has no change tools. If reads work but change tools are missing, Read only may be the reason; it does not by itself prove an outage. Open Hype Settings → Security → Connected assistants to review the connection's access, then reconnect through `/mcp`.

**If you are signed out.** Run `/mcp`, select `plugin:hype:hype`, choose **Authenticate** and finish in the browser. Never paste sign-in links, codes or tokens into a chat. If a request expired, close that page and start again from `/mcp`. If you started sign-in more than once, use the newest browser page.

**Refresh tools.** When Hype adds tools, or Claude says "Hype's tools changed", run `/mcp`, select `plugin:hype:hype` and choose **Reconnect**. If it also says the plugin is older than Hype needs, [update the plugin](#update-the-plugin) first.

To stop using the connection in Claude Code, disable `plugin:hype:hype` in `/mcp`. To remove its access in Hype, open Settings, go to Security → Connected assistants and choose Disconnect for that assistant, or, on a connection that may make changes, ask Claude to disconnect it: Claude names the exact assistant and waits for your yes first. A new connection always needs your own approval on Hype's page.

## Who can use it today

Access is by invitation for now. Installing the plugin does not grant access. An account that is not on the list can still sign in, but Hype then answers every request with "not found". A separate purchase requirement may apply: if Hype says assistant access requires a purchase, open Hype to see the available options. Neither answer is fixed by repeated sign-ins. To ask for access or help, use the [Hype support page](https://hypesports.live/support.html).

## How it keeps you safe

- **One review, one yes.** Before changing anything, it shows the full requested list: targets, exact values, effects and notifications. Your one yes in the next message approves that exact list, with no time limit of its own; it completes the calls in order without asking again for each change. A changed list needs a new review and next-message yes. Announcements go last, back to back when there are several. Each has its own original 10-second Undo window; later sends can use up an earlier window. The immediate final message shows Undo deadlines and the full result report. Starting a skill is never a yes.
- **No blind retries.** A refused part stops its dependent steps, not other approved independent work. If a write answer is lost, it says the change may have happened, stops writes and inspects only the affected item once where supported; anything it cannot establish stays unknown, never automatically retried.
- **It acts only as you.** It signs in as your own Hype account and has your own rights, nothing more. It never asks for your password: the browser sign-in is the only place for it.
- **Your records are data, not orders.** Text inside your Hype records is treated as information, never as instructions.
- **Long jobs.** Keep your approvals in the main conversation. Plain helper assistants may not get the Hype connection, so check that a helper can see Hype before handing it work.
- **Progress records.** The Hype assistant (`claude --agent hype:hype`) can keep a progress record in one file you choose, when you choose. That limit is an instruction, not a file lock; see [your own files](shared/own-files.md).

## Using Hype from other assistants

Hype's connection is a standard MCP server at `https://api.hypesports.live/api/mcp`, with browser sign-in.

- **Tested:** Claude Code, with this plugin.
- **Untested:** custom connectors in claude.ai and Claude Desktop, ChatGPT connectors, and Codex. They may connect, but we have not tried them, so we give no setup steps for them yet.

Other assistants would get Hype's tools, and each tool's own safety rules, but not this plugin's skills, the Hype assistant or the `/hype:` commands.

## Your privacy

Information the assistant reads from Hype appears in your Claude conversation. Share only what the request needs, especially player details and family contact information. Hype's Privacy Policy covers Hype; your Claude service's privacy settings and terms also apply to the conversation. Disconnecting Hype stops future access, but does not remove information already in a conversation. If you ask for a local progress record, keep it private and out of public code changes.

- [Privacy Policy](https://hypesports.live/privacy.html)
- [Terms of Service](https://hypesports.live/terms.html)

## Get help

Visit the [Hype support page](https://hypesports.live/support.html). For security problems, follow [private security reporting](SECURITY.md) rather than posting personal details in a public issue.

## Skills

| Optional shortcut | What it helps with | Status |
| --- | --- | --- |
| `/hype:league-setup` | Create a league and its divisions, rename it, register players and archive it | Available |
| `/hype:my-support` | See your supporter status and change your supporter ring setting | Available |
| `/hype:season-schedule` | Plan a round-robin division season and save its reviewed games to saved league Fields; change, cancel or undo cancellation of shared games; hide a cancelled event from only your own schedule or clear your personal hide; read live scores, record a scoring tap, hand over scoring or turn off an overlay link, with one complete review and one yes | Preview |
| `/hype:run-a-draft` | Prepare and run a division draft, with clock guidance and supported pause, resume, skip and undo actions | Preview |
| `/hype:manage-my-team` | Add a team event and tell the team with one confirmation; see your Roster, Staff and seasons; add, change, take off, put back and roll over players; invite coaches and parents/guardians, resend or cancel staff invitations; answer parent/guardian requests and league memberships; check emergency contacts; team and league uniform requests, missing teams, league export, defaults and personal Skip; bulk jersey numbers | Preview |
| `/hype:players-families` | Add or edit your child's profile and emergency contacts, manage parent/guardian invitations and team requests, invite family and friends to follow, answer invitations to follow, read Followers and remove family/friend follows, read league/division players, and answer your own player's uniform requests | Preview |
| `/hype:invite-families` | Review a whole parent-invitation list once, start one background job, check progress or stop future work when asked, and recover with the original key; include requested same-row emergency contacts in the same review | Preview |
| `/hype:league-staff` | See and manage a league's staff | Preview |
| `/hype:clubs-and-tournaments` | Set up clubs and tournaments, invite Admins and answer invitations | Preview |
| `/hype:my-feed` | Read your Feed and comments, write comments and give Hypes, send announcements with a 10-second Undo, and delete eligible announcements or comments; one review and yes cover the complete requested list | Preview |
| `/hype:messaging` | Find your chats, read recent messages and current chat role labels, member names and decorative supporter rings, send exact approved text, edit or delete your own messages, mark chats read or unread, start a custom group, check its add-people availability or leave one yourself; additions remain switched off | Preview |
| `/hype:catch-up` | Catch up on notifications, with separate group-chat and direct-message unread snapshots | Preview |
| `/hype:notification-settings` | Change which notifications you get and when | Preview |
| `/hype:my-account` | Look after your own account details and settings | Preview |
| `/hype:find-in-hype` | Find screens and readable records, including tournaments and managed player profiles; get links, locate appearance settings and Report a problem; no changes or submissions | Preview |
| `/hype:terms-and-privacy` | Read Hype's Terms and privacy information | Preview |
| `/hype:review-evaluations` | Find evaluations you manage, review your own or shared scores, player lists and who came to each tryout date, then rank or summarise scores | Preview |
| `/hype:run-evaluations` | Score players, save private notes, manage sharing and player lists, start evaluations, add dates, mark or clear who came to a tryout date and choose your private evaluation source for a draft | Preview |

For how a skill works and its limits, open its `SKILL.md`; for example, the [season scheduling workflow](skills/season-schedule/SKILL.md).

Developers: see [CONTRIBUTING.md](CONTRIBUTING.md) to add or change a skill.

## License

MIT. See [LICENSE](LICENSE).
