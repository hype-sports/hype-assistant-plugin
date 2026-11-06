# Changelog

All notable changes to this plugin are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 0.1.29 - 2026-11-06

### Changed
- Clubs and Tournaments: get each new create or Admin-offer key from the shared `request-key-new` tool and reuse it only for an exact retry, instead of generating one yourself; the app remains the fallback when that tool is unavailable.

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
