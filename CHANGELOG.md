# Changelog

All notable changes to this plugin are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 0.1.113 - 2026-11-25

- Season scheduling: hide one cancelled event from only your own schedule or return an event by clearing your personal hide. Read the exact event first, review and confirm the personal-only effect, preserve the original request key and receipt for requested repeats, and stop on refusals or uncertain answers without automatic retries. Hiding never cancels, archives or deletes the event for anyone else.

## 0.1.112 - 2026-11-24

- Messaging: read whether people can be added to one exact custom group and prepare a confirmed addition only when Hype permits it. Additions remain switched off pending safety verification. Keep exact returned person IDs, the original request key and body, acceptance-only receipts and no automatic retries or polling; options never prove permission or recover a lost write.

## 0.1.111 - 2026-11-22

- Personal team and league creation: prepare the original request key before the first confirmed send, keep the exact body and key for a person-confirmed repeat, and recognize replayed answers as the same saved record. Explain key reuse refusals and read current state after an unknown result without automatic resends or replacement keys.

## 0.1.110 - 2026-11-22

- Manage my team: add a team event and tell the team with one review and next-message yes. Report event, Feed post and notification results separately; check the original request after an unknown result and retry only its announcement, never create a duplicate event or post. Keep shared division games in season scheduling.

## 0.1.109 - 2026-11-22

- Manage my team: read league uniform requests and missing teams, export the route's complete file without invented links or truncation, and review league request creation, locking and default-list changes before one yes. Keep division and parent scope private, personal Skip caller-only and unkeyed, and uncertain changes stopped without automatic retries.

## 0.1.108 - 2026-11-21

- Manage my team: preview everyone's jersey changes with clashes and league warnings, then save the exact reviewed table once after one yes. Start and read uniform requests, manage default size lists and lock the whole order; parents can review and save only their own player's answer until locked. Keep sent lists unchanged, respect read-only history and stop without automatic retries or follow-up reads after uncertain writes.
## 0.1.107 - 2026-11-21

- Season scheduling: read a game's live score, record one requested scoring tap, hand scoring to a selected eligible scorer, or turn off the streaming overlay link. Review and confirm changes, keep the original scoring keys after uncertain answers, and leave overlay-link creation and copying in the app.

## 0.1.106 - 2026-11-21

- Players & Families: invite family or friends to follow a player, read and answer your invitations, withdraw or remind a known offer, and read Followers to remove an exact family/friend follow. Keep parent/guardian and staff powers separate, review every change before one yes, keep contacts private, and stop without retries or follow-up reads after uncertain changes.

## 0.1.105 - 2026-11-21

- Messaging: use a returned message author's Hype person ID for requested current role and member-name reads. Missing or null author IDs stay unavailable, never inferred from names or provider identifiers. Navigation-only requests hand off these chat reads and decorative supporter rings to Messaging.

## 0.1.104 - 2026-11-21

- Messaging: read current chat author role labels, a current member's chat name and decorative supporter rings only when requested and offered by the live connection. Keep app access checks, hidden identities and unavailable roles; omit guardian names and profile-picture URLs, never infer support status from a missing ring, and never poll or retry automatically. These reads do not mark chats read or change unread counts, presence or typing.

## 0.1.103 - 2026-11-21

- Messaging: start a custom group from permitted league choices and bounded name searches, or leave only your own custom-group membership, when those live tools are available. Keep exact shared confirmation, the original creation key, pending-only acceptance receipts and no automatic retries; adding people to existing groups remains unavailable.

## 0.1.102 - 2026-11-21

- Messaging: find related adults by name, check current direct-message eligibility, open the exact approved person's chat, and read or change your own chat mute when those live tools are available. Keep bounded discovery, one shared review and next-message yes, server permission checks and no automatic retries after uncertain changes.

## 0.1.101 - 2026-11-21

- Messaging: edit or delete your own chat message within the app's 15-minute window, or mark your own chat read or unread, when the live connection offers those tools. Keep the shared exact review and next-message yes, caller-owned unread state checks, plain refusals and no automatic retry after an uncertain result.

## 0.1.100 - 2026-11-21

- Players & Families: read a player's visible Overview sections and let current managing parents/guardians review and save exact section changes, audiences, order, archive, restore and permanent deletion. Keep the two audience choices, one next-message yes and one save; an unknown save never triggers an automatic retry or follow-up read, even when the server suggests loading the Overview. Clarify first-save limits, missing long text and the editor's archive/delete choices; shared recovery rules honor workflow-specific read-back exceptions.

## 0.1.99 - 2026-11-21

- My support: stop naming four old payment tools (start a payment, recover a payment, read a payment step, open the manage-support page) that Hype's server no longer offers. The skill still sends paying and managing support to the Hype app, and the plugin's tool-catalog check passes again.

## 0.1.98 - 2026-11-20

- The skills and shared invitation rules now describe the request limit as the shared per-account allowance Hype sets, instead of a fixed 60 requests a minute, because that allowance is becoming a setting that can change. Pacing (at least 1.1 seconds between request starts) and the stop-on-rate-limit rules are unchanged.

## 0.1.97 - 2026-11-17

- Clubs and Tournaments: correct the skill to say Tournament Admin invitations attempt email through the shared staff invitation sender. Explain confirmed sends, unconfirmed results and the per-recipient daily cap without promising inbox delivery or retrying automatically.

## 0.1.96 - 2026-11-17

- Run evaluations: the assistant no longer says a typed-in player can't get a Hand-set score or private note; it saves them with that player's own ID, and registered players work as before.

## 0.1.95 - 2026-11-17

- Explain expired sign-in, read-only access, account access and purchase requirements without asking for sign-in links or repeated attempts. Add privacy guidance and private security-report links.
- Update an older plugin when Hype's tool catalog is newer, even if the minimum plugin version did not change.
- Shorten the Hype assistant's instructions, use only the plugin's own connection, and update chosen progress entries without rewriting the whole file. Keep one complete review, one yes and safe handling of uncertain results.
- Check skill routing, heading links and plain-request selection; parse skill and agent files explicitly; add directory validation and an optional offline comparison with server tool names.
- Keep common file, invitation and version rules in shared references; move detailed team Staff workflows out of the main skill without changing their safeguards.

## 0.1.94 - 2026-11-16

- Messaging: ask who reacted to a message and get the names and reaction types, as in the app; a removed message now says it was removed, and photos show their name and size.

## 0.1.93 - 2026-11-16

- Invite families: clarified which progress details can be empty; only the person who started a job can check or stop it; the question about keeping a progress record is asked before the review, never after your yes; the whole reviewed list always starts as one background job.

## 0.1.92 - 2026-11-16

- Invite families: after one complete review and one yes, start the whole ordered parent list as one background job instead of sending small parts or checking every parent separately. Saved-import invitations use the same job.
- Report address-free progress only when asked, explain waiting, sent, refused and uncertain results, and offer to stop future work without promising to recall mail or remove access.
- Keep the chosen progress record and original request key/full input for deliberate lost-answer recovery; never automatically poll, retry, resend or start a replacement job. Align the mixed announcement example and shared invitation guidance.

## 0.1.91 - 2026-11-16

- Add Messaging: find your chats, including current-season Team and Staff chats by team, check unread snapshots and read recent messages with paging, attachment details and reaction counts. Keep personal details out of summaries and reports.
- Send exact approved text as yourself under the shared one-review, one-yes rule, preserving Hype's access, consent and rate checks and the original message identifier. Unknown sends stop without automatic retries or replacement keys.
- Route conversation reads and text sends from catch-up, find-in-hype, manage-my-team and my-feed to Messaging instead of saying they must happen in the app; chat photos stay in the app. Explain first-message restrictions, the 30-send hourly limit, older-page cursor expiry and omitted closed direct chats.

## 0.1.90 - 2026-11-16

- Season scheduling: save a complete reviewed season to saved league Fields through the existing shared-game tools, with one next-message yes for the whole plan. Use the league directory's current references and verify each saved link; preserve sequential calls, original request keys and honest partial results. Keep progress only at the person's chosen path. Plan-only requests remain unsaved.

## 0.1.89 - 2026-11-15

- My account: set your own profile photo to Hype's approved drawn picture (one review, one yes); profile reads now say whether a photo is set. Personal photos stay in the app. League setup reads the saved Private choice back from `league-get` when it is returned (League Admins), instead of always saying it was sent but not confirmed.

## 0.1.88 - 2026-11-15

- The four spreadsheet skills' descriptions now open with the attached-file rule, so it is in view before a skill is chosen.

## 0.1.87 - 2026-11-15

- Spreadsheets: when the named file is not there, the converter lists the `.xlsx` files in that folder (full paths, at most 20), so the assistant runs the converter straight away instead of listing or searching folders itself, and retries once only with a name that is clearly the same file. League setup now says plainly never to claim Hype confirmed a league's Private choice, since the league read does not return it. League setup also triggers on "set up the league from this registration spreadsheet".

## 0.1.86 - 2026-11-15

- Spreadsheet skills: the attached-file rule (current folder, straight to the converter, never list or search) now opens each skill, so it is read before the first step.

## 0.1.85 - 2026-11-15

- Spreadsheets: a file attached or named without a folder is taken from the current working folder and converted directly, with no listing or searching; if it is not there, the converter now says it cannot find the file and the assistant asks for the exact path. The spreadsheet skills also read the plugin's own reference files with the file-reading tool, never through the shell.

## 0.1.84 - 2026-11-15

- run-evaluations: starting a division evaluation or a personal sheet sends no player IDs; Hype includes the current players itself and reports how many. The assistant no longer offers to pick players at creation (the player list can be changed afterwards).

## 0.1.83 - 2026-11-15

- Workbooks: the assistant runs only the bundled converter command, never listing, searching or opening other folders or files.
- league-setup: division names the person wrote (for example U10, U12) are used as their names; the usual 8U Boys form is proposed only when none was given.

## 0.1.82 - 2026-11-15

- Read a chosen Excel workbook with a bundled read-only converter when a shell is available; otherwise ask once for a CSV export with Excel, Google Sheets and Numbers steps. Never guess workbook contents or substitute another file. The converter names the sheet it read, and the assistant uses only the rows and columns the request needs.
- players-families: route “add my kids” and family sheets to managed Hype profiles, check existing profiles first, and review every new child and requested emergency contact together before one yes. Keep existing profiles instead of creating duplicates, and point to Players in the app afterward.
- players-families and invite-families: receipts after yes never repeat email addresses or phone numbers.

## 0.1.81 - 2026-11-14

- clubs-and-tournaments: explain which Club actions are refused while archived and that declines, expiry and account erasure still finish. Restore also removes every Admin's archived lifecycle note for that Club.

## 0.1.80 - 2026-11-14

- run-evaluations: adding another date to an evaluation says when to send `ownerType: 'team'` (only when the event card shows a team as the owner) and to leave it out for a division evaluation, matching what Hype accepts. If it is unclear, the assistant asks.

## 0.1.79 - 2026-11-14

- clubs-and-tournaments: archive or restore a Club, or permanently delete a new, unused mistake only when the server says it is eligible. Show its lifecycle counts and use the shared review and your yes in the next message. Offer Archive after a Delete refusal only for the 30-day limit or an in-use Club; an already archived Club points to Restore, and other refusals stop.
- Read your Club archive/deletion notes, including deleted-Club notes for former Admins, and dismiss only your own copy after the shared review and yes; dismissal never restores or deletes the Club.

## 0.1.78 - 2026-11-14

- my-account: list your connected assistants and disconnect one of them, including this one, after naming it back and getting your yes in your next message. A read-only connection is pointed to the app instead.

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
- Use one complete review and one next-message yes for all requested changes, including mixed roster changes, child profiles with contacts and sports, and invitation lists. Preserve server access checks, request keys, receipts and safe recovery; change confirmation has no separate time limit.
- Include requested same-row emergency contacts in the invitation review instead of asking again per team or page. The historical sending implementation was replaced by the whole-list background job in 0.1.92.
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
- Add invitation allowance snapshots and safe recovery of unfinished attempts; this initial invitation implementation was replaced by whole-list jobs in 0.1.92.
- Add missing Parent 1 and Parent 2 emergency contacts from the same invitation-sheet rows to exactly paired team roster entries, with separate per-team table approval, existing contacts preserved, skipped and missing-phone rows explained, and a readback after each add-only save.
- Pair a league registration with its team roster entry only through `team-roster-contact-status` (`registrationId` to `entryId`), never by player name; an unpaired row is left out and explained.
- Map parent columns from any readable spreadsheet layout and review one complete invitation list across divisions in one league, with first parents before second parents under one yes. The historical sending implementation was replaced by the whole-list job in 0.1.92.
- Add requested invitation recovery from the chosen progress record with retained keys and exact inputs; follow 0.1.92's whole-job recovery rules for the current flow.
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
- Clubs and Tournaments: your own invitation lists are plain reads that leave expired offers out (no cleanup step or extra yes), and a Club Admin offer now emails the address once. At this release, Tournament offers did not send email; see 0.1.97 for the current guidance.

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
