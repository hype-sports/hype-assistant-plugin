# Changelog

All notable changes to this plugin are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 0.1.45 - 2026-11-08

### Fixed
- League setup: get a fresh `idempotencyKey` from `request-key-new` for each new parent/guardian invitation, including each approved table row; reuse it unchanged only for an explicitly requested retry after an unclear outcome. Emergency-contact tools still take no key.

## 0.1.44 - 2026-11-08

### Changed
- Let people keep requested contact details in their chosen files and progress records, replacing the blanket file ban; publishing, sharing and credentials remain prohibited (HYPE-5468, decision 900).

## 0.1.43 - 2026-11-08

### Fixed
- Keep a person's own files and requested progress records where they choose, with one shared rule for storage and minimal resume details (HYPE-5468). Contact details still never go into files; publishing, sharing and credentials remain prohibited. Draft progress may record picks made, but private player lists, evaluation scores and coaches' private pick lists stay out of files.

## 0.1.42 - 2026-11-07

### Changed
- Use the add-only emergency-contact tool for reviewed additions, preserving existing contacts; keep whole-list replacement for edits/removals and explain the existing update fallback when the add tool is not live yet (HYPE-5328). Approval, privacy, family takeover and unknown-outcome stops remain unchanged.

## 0.1.41 - 2026-11-07

### Changed
- Allow one later-turn yes for one exact reviewed table of parent/guardian invitation sends and team-player emergency-contact replacements, limited to one team or division, with paged approvals, fresh reads, sequential pacing and stop-on-change/refusal/unknown recovery (HYPE-5180). All other writes keep individual approval.

## 0.1.40

### Added
- `find-in-hype` Preview skill for read-only screen directions and links to readable Home records, with app-only appearance and Report a problem handoffs.

## 0.1.39 - 2026-11-06

### Changed
- Season scheduling: tell the commissioner that the assistant checks its plan for team and Field clashes, but Hype won't stop a double-booking and games added outside the plan or edited later aren't checked (HYPE-4726).

## 0.1.38 - 2026-11-06

### Changed
- Recommend account-wide installation for commissioners and coaches with `--scope user`, and explain how to enable Hype when its tools are missing in another folder (HYPE-5176).

## 0.1.37 - 2026-11-06

### Fixed
- Team emergency contacts use the requested player's `team-roster-list` row `id` as `entryId`, never `playerProfileId` or a person's ID; `NOT_FOUND` means not found or not visible, without retrying another kind of ID (HYPE-5131).

## 0.1.36 - 2026-11-06

### Changed
- League staff and League setup: each new `league-staff-invite` gets a fresh `idempotencyKey` from `request-key-new` (HYPE-4855, HYPE-4892); the same key is reused, unchanged, only when the person explicitly asks to retry that same invite after an unclear outcome, and a different email or roles needs a new key.

## 0.1.35 - 2026-11-06

### Added
- `review-evaluations` for reading your own evaluation scores, scores shared with you and player lists you manage, and building a ranking, summary or file from them.

## 0.1.34 - 2026-11-06

### Changed
- My account: deleting your account now checks Club and Tournament ownership too, as well as League and Team. The skill no longer says Club and Tournament checks are missing, and still treats a missing or unreadable list as unknown, never as clearance.

## 0.1.33 - 2026-11-06

### Changed
- Clubs and Tournaments: get each new create or Admin-offer key from the shared `request-key-new` tool (HYPE-4892), never asking for a new key on a retry and reusing it only for an exact retry after the re-check and a fresh yes, instead of generating one yourself; the app remains the fallback when that tool is unavailable or fails.

## 0.1.32 - 2026-11-06

### Changed
- Team management explains staff-only reading and whole-list editing of one player's emergency contacts (HYPE-5081): read first, review the exact replacement, get explicit yes in a later turn, respect family takeover and keep contacts out of summaries and files. Requires the two tools to be present in the live connection; source changes alone do not make them live.

## 0.1.31 - 2026-11-06

### Added
- The plugin now carries the Hype connection (`.mcp.json`, server `hype` at `https://api.hypesports.live/api/mcp`). Sign in from `/mcp` (`plugin:hype:hype`, Authenticate): Hype's page in the browser lets you Allow it to read and change things as you in Hype, or Deny. Only invited accounts can connect.

## 0.1.30 - 2026-11-06

### Changed
- League setup: a league's logo can now change through `league-update` (HYPE-4839), but only to a picture the person uploaded with `demo-logo-upload`; never a web address from the chat, never fetched. The assistant cannot see the picture, so it asks the person to check the logo in the app; removing a logo needs their explicit yes, and leaving it out keeps it. Live after the next API deploy.

## 0.1.29 - 2026-11-06

### Changed
- Season scheduling: each new game's key now comes from `request-key-new` (HYPE-4892), reused only for an explicit retry with unchanged inputs, instead of a UUID the assistant makes itself.

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
