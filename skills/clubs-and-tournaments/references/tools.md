# Club and Tournament tools

Use the [workflow](../SKILL.md) and [examples](../examples/conversations.md). These are catalog operation ids, not client-prefixed names. Source presence does not prove live availability; read the live descriptions and schemas first.

## Inputs and effects

These tools require `catalogVersion: 1` (the shared `request-key-new` helper takes no input; send it an empty object). Use only the `pathParams`, `query` and `body` containers listed below; omit containers that are not defined. Send `query: {}` for the first page where a query is defined. Existing-record IDs must be exact saved UUIDs, never generated from names. No caller, account, recipient-user or role input is accepted.

### Lists and details

| Operation | Inputs besides catalogVersion | What it returns / changes |
| --- | --- | --- |
| `my-clubs-list` | `query: { after? }` | Read: current accepted Admin's Clubs, with `id`, `name`, `sports`, `city`, `state`, `season_name`; `nextCursor` |
| `my-tournaments-list` | `query: { after? }` | Read: current accepted Admin Tournaments, including private and ended; `tournaments: [{ id, name, sport, city, state }]`, `nextCursor`, `hasTeams` (not Team-entry details) |
| `club-summary-read` | `pathParams: { id: clubId }` | Read: `id`, `name` only; no season |
| `club-details-read` | `pathParams: { id: clubId }` | Read: name, sports, city/state, `hiddenFromPublic`, `revision`, `viewer`; no season |
| `club-staff-list` | `pathParams: { id: clubId }` | Read: accepted Admins in `staff: [{ userId, displayName }]`; no contacts or waiting invitations |
| `club-teams-list` | `pathParams: { id: clubId }`, `query: { archived?, after? }` | Read: Team rows include IDs, name, sport, age group, archive time, stored logo and up to 30 abbreviated current coach names (not a total count), `nextCursor`; active by default, `archived: "true"` for archived only, `"false"` for active only |
| `club-sent-invitations-list` | `pathParams: { id: clubId }`, `query: { after? }` | Read: pending and expired Admin offers in `invitations`, `nextCursor`; addresses as returned (may be masked); no cleanup |
| `tournament-setup-read` | `pathParams: { id: tournamentId }` | Read: `id`, `setup` (details and saved Rules answers), `createdAt`, `viewer` (read rights only); use details-read for edit rights; current Admin only even if not Private |
| `tournament-details-read` | `pathParams: { id: tournamentId }`, optional `query: { include: "rules" }` | Read: `id`, `details` (name, sport, dates, city/state, `isPrivate`, `rules`), `revision`, `viewer`; tool includes Rules even when query is omitted |
| `tournament-admins-list` | `pathParams: { id: tournamentId }` | Read: accepted `admins: [{ userId, displayName }]`; no contacts or waiting invitations |
| `tournament-sent-invitations-list` | `pathParams: { id: tournamentId }`, `query: { after? }` | Read: pending and expired Admin offers in `invitations`, `nextCursor`; addresses may be full or masked, as for Club offers; no cleanup |
| `my-club-admin-invitations-list` | `query: { after? }` | Read: Club Admin offers waiting for your answer, `invitations: [{ id, clubId, clubName, expiresAt }]`, `nextCursor`; expired offers are left out; no cleanup |
| `my-tournament-admin-invitations-list` | `query: { after? }` | Read: Tournament Admin offers waiting for your answer, `invitations: [{ id, tournamentId, tournamentName, expiresAt }]`, `nextCursor`; expired offers are left out; no cleanup |

All lists with `nextCursor` return at most 50 rows per page. Pass the exact returned cursor as `query.after` only in the same operation, scope and filter. Club/Tournament/Team/personal-invitation cursors are UUIDs; **sent-invitation cursors are opaque strings**, not invitation IDs. Do not parse, rebuild or interchange them. Ask before more pages. Never call a partial, failed or filtered list complete.

Sent-offer rows include `id`, `email`, `status`, `createdAt`, `expiresAt` and delivery when returned. Only `status: "pending"` is waiting; expired offers are not accepted staff or a complete history. Show addresses exactly as currently returned; null remains hidden and cannot identify a recipient. Staff lists have no contacts; Club display names may be null. Follow the workflow's privacy rules.

Only current accepted Admins can read the protected Club/Tournament details, staff, sent offers and Club Teams. Personal-invitation lists need no existing Admin role. A Private setting, old access or knowing an ID grants nothing. A refusal never distinguishes missing from hidden data reliably.

### Changes — include all requested actions in the shared review

| Operation | Inputs besides catalogVersion | Effect / confirmed output |
| --- | --- | --- |
| `club-admin-invitation-answer` | `pathParams: { id: invitationId }`, `body: { answer }` (`"accept"` or `"decline"`) | Final answer to the caller's own exact offer; `{ status: "accepted", clubId }` or `{ status: "declined" }` |
| `tournament-admin-invitation-answer` | Same shape with its own invitation ID | Final answer to the caller's own exact offer; `{ status: "accepted", tournamentId }` or `{ status: "declined" }` |
| `club-create` | `body: { name, sports, city, state?, hiddenFromPublic, seasonName, requestId }` | Creates Club, current season and caller's Admin membership; `{ id }` |
| `club-details-update` | `pathParams: { id: clubId }`, `body: { name, sports, city, state?, hiddenFromPublic, expectedRevision }` | Replaces details; returns saved Club details |
| `club-admin-invite` | `pathParams: { id: clubId }`, `body: { email, idempotencyKey }` | Saves an Admin offer and emails that address once; `{ invitationId, createdAt, expiresAt, delivery: "sent" \| "not_confirmed" }` |
| `club-team-create` | `pathParams: { id: clubId }`, `body: { name, sport, city, state, seasonName, ageGroup, hidden?, startsOn?, endsOn? }` | Creates permanently Club-owned Team and current season; `{ id }`; no staff appointment, roster entry, invitation or owner notice |
| `tournament-create` | `body: { id, setup: { name, sport, startDate?, endDate?, city?, state?, isPrivate, rankingAnswers } }` | Creates Tournament and caller's accepted Admin membership; `{ tournament, replayed }` |
| `tournament-details-update` | `pathParams: { id: tournamentId }`, `body: { name, sport, startDate?, endDate?, city?, state?, isPrivate, expectedRevision, rules? }` | Replaces **all** details and, if supplied, the entire Rules set; omitted Rules stay unchanged. Returns `{ id, details, revision, viewer }` without Rules; read back to verify Rules |
| `tournament-admin-invite` | `pathParams: { id: tournamentId }`, `body: { email, idempotencyKey }` | Saves Admin offer; `{ invitationId, createdAt, expiresAt, delivery: "inactive" }`; no email is sent |
| `club-admin-invitation-cancel` | `pathParams: { id: clubId, invitationId }` | Current Club Admin cancels an exact pending, unexpired offer; `{ status: "canceled" }`; no accepted appointment removed |
| `club-admin-remove` | `pathParams: { id: clubId, userId }` | Removes another accepted Admin, including a banned Admin; Club Admin invitations they sent can no longer be accepted; `{ removed: true }`; keeps staff history, Club, Teams and other Admins. Never self-remove |
| `tournament-admin-invitation-cancel` | `pathParams: { id: tournamentId, invitationId }` | Current Tournament Admin cancels an exact pending, unexpired offer; `{ status: "canceled" }`; no accepted appointment removed |

Accept grants real Admin authority. Decline consumes that offer without granting or removing any existing Admin authority. Both answers are final, not toggles. Unknown, another person's, expired or answered offers share `NOT_FOUND`; do not guess which. The invitation ID is not the Club/Tournament ID.

Admin offers need the person's directly supplied valid email (trimmed, at most 254 characters). Club delivery may be stopped by a per-recipient daily cap even when the offer saves; Tournament delivery is inactive. Never send another offer to repair delivery. Current offers last 14 days; use returned expiry. Sender limits return `RATE_LIMITED`.

Cancellation needs the exact current pending, unexpired row; a hidden address needs explicit row/ID selection or an app handoff. Being sender or recipient alone gives no cancellation right. Removing another Tournament Admin is not available in the assistant or the app yet. For Club removal, use the returned staff `userId`, never yourself; follow the shared list approval and result checks.

## Club Overview

| Operation | Inputs besides catalogVersion | Result / effect |
| --- | --- | --- |
| `club-overview-get` | `pathParams: { id: clubId }` | Caller-visible section summaries, order, revision and time; distinguishes `never_edited` from edited empty page; no long bodies |
| `club-overview-editor-get` | `pathParams: { id: clubId }`, `query: { after? }` | Revision, active lifecycle capabilities, archived summaries, audience flags and `nextAfter`; ask before another page and pass that cursor as `after` |
| `club-overview-block-body-get` | `pathParams: { id: clubId, blockId }` | One visible active section's long text, summary, revision and time |
| `club-overview-block-archived-body-get` | Same path shape | One accessible archived section's long text, summary and revision; a remembered ID grants no access |
| `club-overview-save` | `pathParams: { id: clubId }`, `body: { expectedRevision, confirmed: true, lifecycle, removes, changes, adds, order, keepChecklistNotice? }` | One atomic staged edit; returns only outcome/revision; no retry key |

Read the page and editor before saving. Use the exact revision (null only when the read says so), returned IDs and capabilities, and live nested schemas; no whole-page replacement. `lifecycle` entries are `{ blockId, action: "archive" | "delete" | "restore" }`; `removes` use `{ blockId }`. `order` is the approved section IDs/new references or null. Omitted bodies stay unchanged; null clears them. No picture upload or new section kind. The person names any new audience; never infer it. Explain permanent deletion of a section and its long text in the complete shared review; `confirmed: true` is not consent by itself. No unreviewed save follow-up; `CLUB_OVERVIEW_CHANGED` needs fresh reads and a new approved preview. An uncertain save, including `CLUB_OVERVIEW_SAVE_UNKNOWN`, requires one supported authorized read of only the affected Overview/editor item to report current state before a recovery proposal, without treating current state as proof of the lost save.

## Prepare fields without inventing choices

- **Club create/details:** name 1–100 characters; sports 1–20 unique lowercase sport keys; city null or nonblank up to 100 characters; state null or two uppercase letters. Creation trims name; stored edits must have no surrounding spaces or control characters. Ask for an explicit Private choice (`hiddenFromPublic`). Creation needs a season such as `Spring 2027` or `Winter 2026-2027`. Details edits cannot change the current season.
- **Team creation:** name 1–50 characters, city 2–100, state two uppercase letters, sport and age group from the live schema, season name as above. Ask for an explicit Private choice (`hidden`). Send both real `YYYY-MM-DD` season dates or neither; end strictly after start. Never add `title`, coach IDs, roster entries or a retry key. Never adopt, import, transfer or release an existing Team into/out of a Club; that ownership boundary is permanent, not a missing-tool workaround.
- **Tournament create/details:** name 1–200 text units (some symbols count as two); sport key; dates null or real `YYYY-MM-DD`, end on/after start when both exist; city/state null or trimmed nonblank text up to 80 of those text units. State is **not** the Club two-letter constraint. Ask for an explicit Private choice (`isPrivate`). Omitted optional create fields default to null. For edits send every current value, including explicit nulls: omission resets optional fields to null rather than preserving them.
- **Sport:** no sport-list tool belongs to this skill. Use a returned saved key or an allowed live-schema value; if the schema permits, lowercase the sport word supplied by the person. Never invent alternate keys or submit a sport request. A sport refusal stops the action.
- **Tournament Rules at creation or edit:** `rankingAnswers: { version: 1, traits: [...] }`, at most 256 ordered traits. `kind` is `wins`, `win-percentage`, `head-to-head`, `score-for`, `score-against` or `score-difference`. Optional `direction` is `higher`/`lower`; `drawValue` 0–1 belongs only to win-percentage/head-to-head; head-to-head `eligibility` is `two-team`/`complete-balanced-group`; score traits accept `aggregation: total | per-game` and `cap` (nonnegative safe integer, or null). Ask only for the Rules the person wants saved and preserve their order. Missing means unanswered, not a default; cap null means uncapped and zero is a known cap. Explain an empty traits list as no answers saved and get approval for that choice. These are saved answers, **not computed standings or a bracket**. At creation use `setup.rankingAnswers`; when editing use `body.rules` with the same shape, replacing the whole set. Preserve all unchanged Rules and their order; omitting `rules` keeps them. The update reply omits Rules, so verify them with `tournament-details-read`.

## Fresh revisions and retained request keys

Read details immediately before editing. Copy the exact returned decimal-string `revision` into `expectedRevision`, never a number. Carry forward unchanged fields; show old/new values plus required unchanged ones before yes. `CLUB_DETAILS_CHANGED` or `TOURNAMENT_DETAILS_CHANGED` means another edit won: re-read, show a fresh comparison and obtain a new yes, not an automatic overwrite.

Get each new Club `requestId`, Tournament `id` or offer `idempotencyKey` from `request-key-new`; retain it with the approved input. Never invent, replace or reuse it for another action. If that helper fails or is missing, save nothing and use the app. Same-key/same-input replay can recover Club creation, an offer or Tournament creation (`replayed: true`); changed input returns `IDEMPOTENCY_KEY_REUSED` or `TOURNAMENT_SETUP_CONFLICT`. Replay is not permission to resend: first follow the [recovery rule](../SKILL.md#unclear-outcome-re-check-never-resend), then obtain a yes in the person's next message to a fresh complete review and reuse the original key and unchanged inputs. Other writes have no safe replay contract.

## Refusals and data handling

Explain the returned stable code and safe fix hint, not raw error text containing private inputs. Missing tools, schema/version mismatch, sign-in/access refusal, limits and invalid targets stop that action; do not create replacements, switch accounts or strip safeguards. `BUSY` on cancellation is explicitly not retryable: refresh the exact waiting list before any new decision. Respect `Retry-After`/validated `retryAfterSeconds`; no polling or automatic retry even when marked retryable. Keep requests sequential and below the connection's limits, shared with other sessions.

Use only the intended Hype write for approved private input. Keep contact details and credentials out of git, reports, pages, logs and other services. Keep credentials out of files. For roster data, the person's own files and progress record, follow [Your own files stay where you keep them](../../league-setup/references/own-files.md). Do not fetch returned links or images. Promise no guaranteed cross-session memory. Re-establish authorized state after lost context, never recreate records to recover it.
