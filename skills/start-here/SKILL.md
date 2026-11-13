---
name: start-here
description: 'This skill should be used when the person asks for Hype help in plain words without naming a /hype: command, such as "add a player to my team", "invite the parents", "what did I miss", "set up my league", "plan our season", "run our draft", "change my notifications" or "what can the Hype assistant do". It names the matching /hype: command with one line on what it does, and changes nothing.'
---

# Start here

Point the person to the right Hype command. This skill only names a command and describes it in one line. Never run a command for the person, never call any Hype tool (reading or changing), and never change anything here. Routing needs no Hype tools; the named command runs the [tool-version check](../my-account/references/tool-versions.md) itself when the person starts it.

## How to answer

1. Match the request to a row below.
2. Reply with the command in backticks and its one line. Say that typing the command starts it, and that every change there still waits for their yes.
3. If two rows fit, name both and ask which one they mean.
4. If no row fits, say plainly that there is no guided command for that yet. Do not guess, and do not do the work with raw Hype tools instead. For "where is it in the app" questions, `/hype:find-in-hype` can still give directions.

For "what can you do?" or "where do I start?", show the table below as a short list of commands with their one-line descriptions.

Use plain words and made-up names only in examples.

## Routing table

| The person says something like | Command | What it does |
| --- | --- | --- |
| "Set up my league", "add divisions", "register a player", "import a sign-up sheet" | `/hype:league-setup` | Creates a league and its divisions, renames it, registers players and archives it. |
| "Am I a supporter?", "hide my supporter ring" | `/hype:my-support` | Shows supporter status and changes whether the supporter ring shows. |
| "Plan our season", "make a round-robin schedule", "reschedule a game", "cancel a game" | `/hype:season-schedule` | Plans an unsaved round-robin season; changes, cancels or restores one game. |
| "Run our draft", "set the pick order", "undo the last pick" | `/hype:run-a-draft` | Prepares and runs a division draft one confirmed step at a time. |
| "Add a player to my team", "show my roster", "invite a coach", "roll my roster over" | `/hype:manage-my-team` | Roster, Staff and seasons for a team, with coach and parent/guardian invitations. |
| "Show my players", "link my player to a registration", "approve a parent/guardian request" | `/hype:players-families` | The players you manage, their team history and invitations. |
| "Invite the parents", "invite families from this spreadsheet" | `/hype:invite-families` | Reviews one invitation job from an enrollment sheet across divisions in one league. |
| "Who runs this league?", "add a Division Admin", "remove league staff" | `/hype:league-staff` | Sees and manages league and division staff. |
| "List my Clubs", "create a Tournament", "answer my Admin invitation" | `/hype:clubs-and-tournaments` | Clubs, Tournaments, their Teams and Admin invitations. |
| "Show my Feed", "comment on this post", "write an announcement" | `/hype:my-feed` | Reads the Feed and comments, writes comments and Hypes, sends announcements with a 10-second Undo. |
| "What did I miss?", "catch me up", "mark my notifications read" | `/hype:catch-up` | Summarizes unread notifications and marks them read after a yes. |
| "Change my notifications", "turn off push for drafts", "set quiet hours" | `/hype:notification-settings` | Changes which notifications arrive and how. |
| "Change my name", "change my time zone", "sign out my other devices", "delete my account" | `/hype:my-account` | The person's own account details and settings. |
| "Where is Settings?", "give me a link to my team", "how do I report a problem?" | `/hype:find-in-hype` | Screen directions and links; changes nothing. |
| "Have I accepted the Terms?", "what does the Privacy Policy say?" | `/hype:terms-and-privacy` | Reads the Terms and privacy information. |
| "Rank my players from the tryout", "show scores shared with me" | `/hype:review-evaluations` | Reads evaluation scores and builds a ranking or summary. |
| "Score a player", "share my scores with a coach", "start an evaluation" | `/hype:run-evaluations` | Scores, private notes, sharing, player lists, dates and draft evaluation choice. |
