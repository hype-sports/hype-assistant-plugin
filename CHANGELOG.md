# Changelog

All notable changes to this plugin are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 0.1.77 - 2026-11-14

- my-account: when roles block account deletion, the assistant says archived or paused leagues and teams count too, so a shorter list seen elsewhere does not confuse the person.

## 0.1.76 - 2026-11-14

- my-account: when account deletion is refused because roles remain, the assistant now receives and shows the list of roles to leave or hand over first.
- players-families: delete one emergency contact after showing its name and relationship in the shared review and getting one yes, without replacing or wiping the contact list.

## 0.1.75 - 2026-11-14

- league-setup: every imported row now tells the server what the preview showed for it, so a player added or changed by someone else after the preview stops the import and is reported, instead of being quietly left as it was.

## 0.1.74 - 2026-11-14

- league-setup: two or more players (typed, pasted or from a file), or one player with two parents' details, now always go through the import (one preview, both parents kept as contacts, then one import), never one-at-a-time registration.

## 0.1.73 - 2026-11-14

- players-families: current league staff, or the adult themselves, can remove a parent/guardian from a league player. The review says who gets an in-app notice, that the link ends but its history is kept, and that an older invitation cannot bring them back.

## 0.1.72 - 2026-11-14

- league-setup: a phone number that needs correcting stops the plan; Claude asks for it and never offers leaving it out as a default.
- league-setup and invite-families: invitation reviews show each address being invited, exactly as it will be sent, so you can catch a typo before your yes.
- league-setup: the invitation allowance is read after the import is saved (it grows with the league's registered players), and the plan never reads another league for defaults.

## 0.1.71 - 2026-11-14

- league-setup: for a league in a US state, parent phone numbers written US-style (202-555-0123) are converted to the full international form (+12025550123) and shown as "was → becomes" before your yes; anything else is listed for you to correct, never dropped. Any preview refusal or difference stops for a new yes; no row value is changed to get past it.
- league-setup: the plan lists the exact invitations, the allowance is read only for the league being acted on, and a changed count or recipient list stops for a new yes. Never more invitations than the plan listed.

## 0.1.70 - 2026-11-14

- league-setup: when one plan creates a league or divisions and imports a sign-up sheet, the plan now shows each row's division before your yes, and rows it cannot place are left out. After the divisions exist, the server preview runs; the import goes ahead under that yes only if every row is a plain new addition in its planned division. Any match, update, contact change, exception or skip is shown for a new yes.

## 0.1.69 - 2026-11-14

- manage-my-team: the review for a parent/guardian Roster-spot invitation or a coach invitation now shows the email address exactly as you typed it, so you can catch a typo before your yes. Addresses still come only from you, never from a roster or contact read.

## 0.1.68 - 2026-11-14

- manage-my-team settles the team before reading any Roster: the team you named, or the only team you run (named in the review); otherwise it asks which team. It no longer reads every team's Roster to find a player.
- Inviting a parent/guardian for a Roster spot: when you have not given their email, Claude asks for it in one question (or points you to the Roster spot in Hype), then shows the full review before anything is sent. It never takes an address from a roster or contact list.

## 0.1.67 - 2026-11-13

- manage-my-team: plain roster requests such as "On <team>, add two players and change a jersey number" now start the team skill, so its one review and one yes apply.

## 0.1.66 - 2026-11-13

- Send announcements last, back to back when several are approved, with each original Undo window explained before yes and the full result report in the immediate final message.
- After a lost write answer, inspect only the affected item once; report current state and keep unsupported or unresolved outcomes unknown rather than retry or scan wider lists.

- Delete requested announcements and comments under the shared complete-list review and one next-message yes, with no Undo and removal confirmed only by a validated answer.
- Keep notification bell counts separate from group-chat and direct-message unread snapshots, and explain where to act in the app.
- Read notification settings without a separate approval prompt, retaining one review and yes for changes. Use the app's labels, distinguish saved Email choices from actual sends, and do not offer daily summary controls: neither the assistant nor the app has them today.

- Plain requests now select the matching Hype skill; commands remain optional shortcuts. Remove the command-only start-here guide and clarify skill ownership.
- Use one complete review and one next-message yes for all requested changes, including mixed roster changes, child profiles with contacts and sports, and multi-part invitations. Preserve server access checks, request keys, receipts and safe recovery; change confirmation has no separate time limit.
- Include requested same-row emergency contacts in the invitation review instead of asking again per team or page. Use the current live send limits without making the person manage parts; whole-list server-paced sending is not available yet.
- Keep player erasure in the app and preserve the warning that saved child birth dates and contacts must be checked there.

- players-families: after adding a child, say that the saved birth date and emergency contacts can't be read back here and should be checked in the app.

## 0.1.65 - 2026-11-13

### Changed
- Clubs and Tournaments: list your administered Tournaments, cancel waiting Club Admin offers, remove another Club Admin and edit saved Tournament Rules after your separate yes. Removing another Tournament Admin is not available yet.
- Read and edit Club Overview sections with current permissions, exact previews and separate approval, including clear permanent-deletion effects and no automatic retries or follow-up reads after saving.
- Align the tool reference and examples with current tools, remove stale tool counts and shorten repeated guidance.

## 0.1.64 - 2026-11-13

### Added
- `start-here`: ask in plain words and get the right `/hype:` command to run, with one line on what it does. It never runs a command and changes nothing.
- `check.sh` also checks the commit messages since `origin/main` for internal tracker references.

### Changed
- The README now reads as a product page: what it is, what you can ask, install and update, sign in (including Read only connections and what to do if you are signed out), who can use it today, how it keeps you safe, other assistants, privacy links and where to get help.
- Removed maintainer-only material from the README and testing-status notes from skill text; the Skills table's Preview label covers it.
- Removed the repository's `.claude/settings.json`, which turned on authoring plugins for anyone who opened the repository.

## 0.1.63 - 2026-11-13

### Changed
- Shorten league setup, route staff work and larger family invitations to their dedicated skills, use the division readiness checklist and explain which registration actions stay in the app.
- Offer approved demo artwork only when requested, never as an upload of a person's own picture; custom logos stay in the app.
- Align league staff with separate Admin/title choices, title-only edits, own Division Admin self-leave and recipient accept/decline.
- Show a parent contact back only to the person who typed it, in that person's immediate approval.
- Show the current family-invitation allowance, check one supplied sign-up contact when asked, and keep same-sheet contact imports add-only without a replacement fallback.

## 0.1.62 - 2026-11-13

### Added
- Add or edit a child's profile and emergency contacts, see who manages the profile, leave it, or ask to join a team as a parent/guardian, with confirmation before every change.
- Answer, resend or cancel supported parent/guardian invitations, review team requests, and read league or division players within the person's own access.
- Add parent, coach and league-admin examples, including what to say when an earlier invitation email's result is unknown.

### Changed
- Organize Players & Families by who is asking and link to the existing league invitation skills instead of repeating their sends.
- Show names instead of record numbers, find the team before a join request, and explain that one coach approval answers one player's request.
- Keep irreversible player erasure and withdrawing mistaken team requests in the app; explain possible duplicate emails before asking to resend.

## 0.1.61 - 2026-11-13

### Changed
- Match account-deletion guidance to every staff and Admin role that must be left first, and keep the status waiting list separate from those blockers.
- Cover login history, assistant activity, personal Blocks and managed-player erase requests, with separate approval before each change and later-turn confirmation before scheduling player erasure.
- Read Terms state from its returned fields without assuming publication history, and point account/player erasure requests to `my-account`.

## 0.1.60 - 2026-11-13

### Changed
- Align evaluation creation with Division Admin management rights without promising a private scoring sheet or scoring access.
- Find manageable evaluations without a saved sheet, read who came to each tryout date, and mark or clear one player's attendance after a separate preview and yes.
- State attendance's current player-list editor and date-start requirements without claiming a draft effect; clarify accepted page-size forms and include attendance in command summaries.
- Clarify manual evaluation-review invocation, tryout request phrases and distinct paging inputs; keep archiving and restoring deliberately in the app.
- Move detailed evaluation actions and ranking/file rules into linked references with worked examples, preserving approval, privacy and uncertain-outcome safeguards.

## 0.1.59 - 2026-11-13

### Changed
- Run a draft with today's tools: draw and reveal pick order, assign who picks for a team, refresh teams, manage Saves and player links, change settings, and manage a private pick list or the team's own turn, one yes per change.
- Explain paced Hat draws for marked players at the app's current pace and separately approved assistant draws, with limited Undo rather than calling each group final; never start an automatic timer or substitute all-at-once placement.
- Add clear Cancel, Delete and Archive warnings, private cutoff-age reading and the person's own Division Skip preference; read current settings and keep clock recovery and unchanged-request retries in one reference.
- Stop if the request-key tool is missing or fails instead of generating a replacement key; use one shared missing-tool rule.
- Match Cancel and Delete explanations to the app's confirmation wording, and distinguish the draft's scheduled time and clock expiry settings from calendar entries and a team's own auto-pick switch.

## 0.1.58 - 2026-11-13

### Added
- Add tournament and managed player-profile links with read-only record selection, explicit page requests and no guessed IDs.

### Fixed
- Correct `find-in-hype` directions: Home, Feed, Messages and Events are the main tabs; Settings and Notifications open from the header.
- Keep followed players out of profile-link lookups, direct team player requests to Members (Players filter), and describe the notification arrow under the list.
- Name the existing workflow commands, keep app-only actions in the app, and describe Report a problem as a permanent prepared-email handoff rather than a pre-launch option. Suggest updating the app if the control is missing, and keep the signed-in Preview warning.

## 0.1.57 - 2026-11-13

### Changed
- Season scheduling now names the live team lists and saved Place/Field readers. Keep whole-season plans unsaved because shared games accept location text, not saved Fields; never send saved IDs to those tools.
- Add plain request phrases and cancellation undo for one shared game after a fresh read and explicit yes. Explain its restored notice to eligible members, with no email or announcement. Leave archive and permanent delete to the app; shared-game unarchive has a live tool but no app action yet.
- Clarify that the app's Add game also accepts only a typed location, not saved Fields. Restore write-access and data-collection safeguards, distinguish saved directories from team lists, and give short numbered steps for one-game changes and unclear results.
- Remove repeated season guidance, clarify optional schedule-card filters and keep technical error codes out of replies. Update the examples to match.

## 0.1.56 - 2026-11-13

### Changed
- `my-support`: a shorter, plainer description, and no hard-coded "paying is not open yet" line, so the skill stays right once support payments open. It now names the four checkout and portal tools the connection may list and says they are left to the Hype app on purpose, and explains an Apple or Google subscription in the status: managed in the phone's settings, and a date that is still being retried is never called paid up.
- `my-account` points supporter questions to `/hype:my-support`.

## 0.1.55 - 2026-11-13

### Changed
- Manage my team: add, change, take off and put back Roster entries, invite a parent/guardian for a roster spot and roll a Roster over to the next season, each after your yes in a later turn. A lost answer is treated as unknown: the lists are read again, never retried blindly.
- Staff invitations now get a request key from `request-key-new`, so a repeated send cannot cancel the first offer and email again; resend and cancel a waiting staff invitation.
- Answer parent/guardian requests one at a time (approve, decline or block) and request, answer, leave, place or remove league memberships within each tool's own limits.
- Emergency-contact guidance moved to its own reference page; the skill description now covers emergency contacts and "who coaches my team". Team chat is left to the Messaging skill once it is released.
- The assistant's command list now includes Manage my team, Clubs and Tournaments, My support and Terms and privacy.
- The plugin listing now links Hype's existing Privacy Policy and Terms of Service, and its support page.

## 0.1.53 - 2026-11-13

### Added
- `my-feed` Preview skill: read your Feed and comments, write comments and give Hypes (each after your yes), and send announcements with a 10-second Undo. Say Undo right after saving to cancel at once, without another confirmation.
- Choose announcement groups and roles and check reach before sending. A queued announcement is lined up to go out after its Undo window unless held or refused; an unavailable one is saved but not lined up to go out. Neither proves it reached anyone's phone; failed-send history is not available yet.
- Feed tool reference and worked evaluation scenarios; tell the person to run the existing skills for notification reading and settings.

## 0.1.52 - 2026-11-13

### Changed
- Clarify the team emergency-contact read, add-only save and whole-list replacement tools, including optional relationships and preserving unchanged coach contacts.
- Keep sign-up contact values hidden and linked-parent details limited to what the requested read returns. Explain that team contact counts exclude sign-up contacts and cannot prove that nothing is on file.

## 0.1.51 - 2026-11-13

### Added
- Players & Families: approve or decline a known whole Team parent/guardian request with current Team permission and a separate explicit yes; before approval, show who is asking, the Team and every waiting player exactly as in the app, and report each player's result.
- Show your own Team spots waiting for a player profile without linking them or showing another family's spots; finding incoming requests and resending invitations remain outside this workflow.

## 0.1.50 - 2026-11-12

### Fixed
- Remove private reference numbers from release notes and reject them in future public-file checks.

## 0.1.49 - 2026-11-11

Combined feedback release for progress records, version checks, reconnect guidance, two-parent imports and reviewed invitation/contact jobs.

### Changed
- Show the invitation preview's remaining allowance, limiting budget, availability time and proposed usage as a snapshot, and read back unfinished attempts before any approved resume without sending twice.
- Add missing Parent 1 and Parent 2 emergency contacts from the same invitation-sheet rows to exactly paired team roster entries, with separate per-team table approval, existing contacts preserved, skipped and missing-phone rows explained, and a readback after each add-only save.
- Pair a league registration with its team roster entry only through `team-roster-contact-status` (`registrationId` to `entryId`), never by player name; an unpaired row is left out and explained.
- Map parent columns from any readable spreadsheet layout and review one complete invitation job across divisions in one league, previewing batches of up to 200 rows and sending first parents before second parents in ordered parts of at most 25 rows under one yes.
- Resume requested invitation jobs from the chosen progress record, reconciling unfinished batches with the same key and exact ordered rows without another email attempt; show possible-parent hints without automatically skipping them.
- Check the server's catalog and minimum plugin versions at session start and after a whole-call refusal suggesting stale tools, not an ordinary business refusal; say how to reconnect when tools changed and how to update first when the plugin is too old, without retrying writes or clearing sign-in. Pin the instruction versions to this release and exercise older/current comparisons offline.
- Guide league roster imports through a read-only preview and separately approved save, retaining both supplied parents and explaining skipped contacts instead of falling back to one-parent registration.
- Review saved-import invitations separately, send first parents before second parents, preserve pending offers, and report skipped, refused, unknown and not-attempted parents without automatic retries or claims of mailbox delivery.
- Direct sign-up sheets from Players & Families to the two-parent league import workflow without granting personal-profile management rights.
- Give the `hype` agent Read and Write for the person's chosen progress record by instruction, not a hard path lock; preserve own-files privacy, direct approval, attempting/outcome logging and safe lost-answer recovery. No Bash or Edit access.
- Document which helpers received the Hype connection in the reported run, live-tool checks and the main-conversation approval pattern for long jobs.
- Explain `/mcp` → `plugin:hype:hype` → Reconnect to refresh Hype's tool list after new tools or a plugin update, without clearing authentication or starting a new sign-in just to refresh tools; point to the existing Connected assistants screen in Hype to remove access.

## 0.1.48 - 2026-11-10

### Fixed
- Team emergency contacts require first and last names (each 1–100 trimmed characters; together with their separating space, at most 100) and a valid phone Hype accepts (7–25 trimmed characters); email and relationship are optional. Ask for missing phones instead of guessing or saving without one.
- Build whole-list updates from the fresh read, keeping every existing contact unless a change or removal was requested. If a contact being kept lacks a phone, ask for it or use add-only for additions; never silently drop it.

## 0.1.47 - 2026-11-08

### Added
- `run-evaluations` for approved scoring, private notes, sharing, player-list changes, evaluation setup, extra dates and choosing your private evaluation source for a draft.

### Changed
- Link evaluation reading to the new evaluation actions, checking live tools before offering a change. Draft commissioner instructions remain unchanged.

## 0.1.46 - 2026-11-08

### Added
- `invite-families` Preview skill for supplied enrollment rows: column mapping, exact registrations in one division, pending-address checks, reviewed invitation pages, keyed sends, conversation-only progress and final checks. Requires the live pending-match and keyed-invitation tools; emergency contacts come in a later version.

### Changed
- Reviewed invitation tables may continue only on the confirmed exact already-a-guardian refusal from the league invitation-create tool, counting that row as skipped rather than done. Other refusal and unknown-outcome stops remain unchanged.
- Warn before approval when an address will receive invitations for several player registrations in the same league, counting all supplied send rows across tables/pages while preserving one invitation and email per player.
- Clarify already-a-parent/guardian skips and the exact-code exception, skip the caller's own addresses, stop on unexpected replacement, and distinguish already-sent emails from unchecked planned rows when counting a supplied whole-league sheet.

### Fixed
- Require a server-issued request key for every new league parent/guardian invitation; reuse it only for a deliberate retry with unchanged inputs. Describe replacement, replay and uncertain email results without sending again to repair delivery.

## 0.1.45 - 2026-11-08

### Fixed
- League setup: get a fresh `idempotencyKey` from `request-key-new` for each new parent/guardian invitation, including each approved table row; keep the same key for an explicitly requested unchanged retry or a confirmed-429 table resubmission. Document guardian reply fields, uncertain email delivery, replay without new sends and safe stops on League staff/guardian key-reuse refusals. Emergency-contact tools still take no key.

## 0.1.44 - 2026-11-08

### Changed
- Let people keep requested contact details in their chosen files and progress records, replacing the blanket file ban; publishing, sharing and credentials remain prohibited.

## 0.1.43 - 2026-11-08

### Fixed
- Keep a person's own files and requested progress records where they choose, with one shared rule for storage and minimal resume details. Contact details still never go into files; publishing, sharing and credentials remain prohibited. Draft progress may record picks made, but private player lists, evaluation scores and coaches' private pick lists stay out of files.

## 0.1.42 - 2026-11-07

### Changed
- Use the add-only emergency-contact tool for reviewed additions, preserving existing contacts; keep whole-list replacement for edits/removals and explain the existing update fallback when the add tool is not live yet. Approval, privacy, family takeover and unknown-outcome stops remain unchanged.

## 0.1.41 - 2026-11-07

### Changed
- Allow one later-turn yes for one exact reviewed table of parent/guardian invitation sends and team-player emergency-contact replacements, limited to one team or division, with paged approvals, fresh reads, sequential pacing and stop-on-change/refusal/unknown recovery. All other writes keep individual approval.

## 0.1.40

### Added
- `find-in-hype` Preview skill for read-only screen directions and links to readable Home records, with app-only appearance and Report a problem handoffs.

## 0.1.39 - 2026-11-06

### Changed
- Season scheduling: tell the commissioner that the assistant checks its plan for team and Field clashes, but Hype won't stop a double-booking and games added outside the plan or edited later aren't checked.

## 0.1.38 - 2026-11-06

### Changed
- Recommend account-wide installation for commissioners and coaches with `--scope user`, and explain how to enable Hype when its tools are missing in another folder.

## 0.1.37 - 2026-11-06

### Fixed
- Team emergency contacts use the requested player's `team-roster-list` row `id` as `entryId`, never `playerProfileId` or a person's ID; `NOT_FOUND` means not found or not visible, without retrying another kind of ID.

## 0.1.36 - 2026-11-06

### Changed
- League staff and League setup: each new `league-staff-invite` gets a fresh `idempotencyKey` from `request-key-new`; the same key is reused, unchanged, only when the person explicitly asks to retry that same invite after an unclear outcome, and a different email or roles needs a new key.

## 0.1.35 - 2026-11-06

### Added
- `review-evaluations` for reading your own evaluation scores, scores shared with you and player lists you manage, and building a ranking, summary or file from them.

## 0.1.34 - 2026-11-06

### Changed
- My account: deleting your account now checks Club and Tournament ownership too, as well as League and Team. The skill no longer says Club and Tournament checks are missing, and still treats a missing or unreadable list as unknown, never as clearance.

## 0.1.33 - 2026-11-06

### Changed
- Clubs and Tournaments: get each new create or Admin-offer key from the shared `request-key-new` tool, never asking for a new key on a retry and reusing it only for an exact retry after the re-check and a fresh yes, instead of generating one yourself; the app remains the fallback when that tool is unavailable or fails.

## 0.1.32 - 2026-11-06

### Changed
- Team management explains staff-only reading and whole-list editing of one player's emergency contacts: read first, review the exact replacement, get explicit yes in a later turn, respect family takeover and keep contacts out of summaries and files. Requires the two tools to be present in the live connection; source changes alone do not make them live.

## 0.1.31 - 2026-11-06

### Added
- The plugin now carries the Hype connection (`.mcp.json`, server `hype` at `https://api.hypesports.live/api/mcp`). Sign in from `/mcp` (`plugin:hype:hype`, Authenticate): Hype's page in the browser lets you Allow it to read and change things as you in Hype, or Deny. Only invited accounts can connect.

## 0.1.30 - 2026-11-06

### Changed
- League setup: a league's logo can now change through `league-update`, but only to a picture the person uploaded with `demo-logo-upload`; never a web address from the chat, never fetched. The assistant cannot see the picture, so it asks the person to check the logo in the app; removing a logo needs their explicit yes, and leaving it out keeps it. Live after the next API deploy.

## 0.1.29 - 2026-11-06

### Changed
- Season scheduling: each new game's key now comes from `request-key-new`, reused only for an explicit retry with unchanged inputs, instead of a UUID the assistant makes itself.

## 0.1.28 - 2026-11-06

### Fixed
- Clubs and Tournaments: your own invitation lists are plain reads that leave expired offers out (no cleanup step or extra yes), and a Club Admin offer now emails the address once while a Tournament offer still sends no email.

## 0.1.27 - 2026-11-05

### Changed
- Add draft tool input guidance and a worked conversation, explain default pick clocks, and offer approved pause, resume, skip, undo and timeout recovery only when the corresponding tools are live.

## 0.1.26 - 2026-11-05

### Changed
- Tailor `manage-my-team` offers to the selected team's Home role: offer pending invitations, follow requests, league memberships and coach invitations only for Admin or Staff, while keeping Hype's permission checks authoritative.

## 0.1.24 - 2026-11-05

### Added
- Hype assistant agent for accessible league and team information, workflow guidance, and approval-controlled changes.
- `league-setup` for league and division setup, invitations, player registration, and season-end archiving.
- `my-support` for supporter status and approval-controlled supporter ring settings.
- `season-schedule` for unsaved season planning and approved changes or cancellations to existing shared games; whole-season saving is not available yet.
- `run-a-draft` for commissioner draft setup and running picks one approved step at a time.
- `manage-my-team` for Roster, Staff, seasons, coach invitations, and staff invitation answers.
- `players-families` for managed player profiles, sports, team history, and parent/guardian workflows.
- `league-staff` for viewing staff and approving invitations, cancellations, removals, or leaving a role.
- `clubs-and-tournaments` for supported Club and Tournament setup, details, Admin offers, and Club Teams.
- `catch-up` for notification summaries and approved read-status changes.
- `notification-settings` for reviewing notification channels, quiet hours, and approved preference changes.
- `my-account` for own-account details, settings, deletion requests, and device sign-outs.
- `terms-and-privacy` for read-only Terms and privacy guidance with app-only acceptance and erasure handoffs.
