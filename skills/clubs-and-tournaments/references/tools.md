# Club and Tournament tools

Use the [workflow](../SKILL.md) and [examples](../examples/conversations.md). These are catalog operation ids, not client-prefixed names. Source presence does not prove live availability; read the live descriptions and schemas first.

## Inputs and effects

All 22 tools currently require `catalogVersion: 1` (the shared `request-key-new` helper takes no input; send it an empty object). Use only the `pathParams`, `query` and `body` containers listed below; omit containers that are not defined. Send `query: {}` for the first page where a query is defined. Existing-record IDs must be exact saved UUIDs, never generated from names. No caller, account, recipient-user or role input is accepted.

### Lists and details

| Operation | Inputs besides catalogVersion | What it returns / changes |
| --- | --- | --- |
| `my-clubs-list` | `query: { after? }` | Read: current accepted Admin's Clubs, with `id`, `name`, `sports`, `city`, `state`, `season_name`; `nextCursor` |
| `club-summary-read` | `pathParams: { id: clubId }` | Read: `id`, `name` only; no season |
| `club-details-read` | `pathParams: { id: clubId }` | Read: name, sports, city/state, `hiddenFromPublic`, `revision`, `viewer`; no season |
| `club-staff-list` | `pathParams: { id: clubId }` | Read: accepted Admins in `staff: [{ userId, displayName }]`; no contacts or waiting invitations |
| `club-teams-list` | `pathParams: { id: clubId }`, `query: { archived?, after? }` | Read: `teams: [{ id, name, sport, ageGroup, archivedAt }]`, `nextCursor`; active by default, `archived: "true"` for archived only, `"false"` for active only |
| `club-sent-invitations-list` | `pathParams: { id: clubId }`, `query: { after? }` | Read: pending and expired Admin offers in `invitations`, `nextCursor`; addresses as returned (may be masked); no cleanup |
| `tournament-setup-read` | `pathParams: { id: tournamentId }` | Read: `id`, `setup` (details and saved Rules answers), `createdAt`, `viewer` (read rights only); use details-read for edit rights; current Admin only even if not Private |
| `tournament-details-read` | `pathParams: { id: tournamentId }` | Read: `id`, `details` (name, sport, dates, city/state, `isPrivate`), `revision`, `viewer` |
| `tournament-admins-list` | `pathParams: { id: tournamentId }` | Read: accepted `admins: [{ userId, displayName }]`; no contacts or waiting invitations |
| `tournament-sent-invitations-list` | `pathParams: { id: tournamentId }`, `query: { after? }` | Read: pending and expired Admin offers in `invitations`, `nextCursor`; addresses may be full or masked, as for Club offers; no cleanup |
| `my-club-admin-invitations-list` | `query: { after? }` | Read: Club Admin offers waiting for your answer, `invitations: [{ id, clubId, clubName, expiresAt }]`, `nextCursor`; expired offers are left out; no cleanup |
| `my-tournament-admin-invitations-list` | `query: { after? }` | Read: Tournament Admin offers waiting for your answer, `invitations: [{ id, tournamentId, tournamentName, expiresAt }]`, `nextCursor`; expired offers are left out; no cleanup |

All lists with `nextCursor` return at most 50 rows per page. Pass the exact returned cursor as `query.after` only in the same operation, scope and filter. Club/Team/personal-invitation cursors are UUIDs; **sent-invitation cursors are opaque strings**, not invitation IDs. Do not parse, rebuild or interchange them. Ask before more pages. Never call a partial, failed or filtered list complete.

Sent-offer rows are `{ id, email, status, createdAt, expiresAt }`, with `status: "pending" | "expired"`. **Show a pending address in full to the inviter when the current tool returns it in full.** Masking applies only where the tool masks: keep `email: null` hidden and never reconstruct it from supplied inputs, history, another tool or a prior receipt. These lists include pending and expired offers; report only `status: "pending"` as waiting, never expired rows. They are not accepted staff or a full invitation history. Display only contacts actually returned by this list in the current conversation; do not save them in files, notes or other services. A null address cannot identify a recipient. Staff lists have no contacts; Club display names may be null.

Only current accepted Admins can read the protected Club/Tournament details, staff, sent offers and Club Teams. Personal-invitation lists need no existing Admin role. A Private setting, old access or knowing an ID grants nothing. A refusal never distinguishes missing from hidden data reliably.

### Changes — preview and explicit yes every time

| Operation | Inputs besides catalogVersion | Effect / confirmed output |
| --- | --- | --- |
| `club-admin-invitation-answer` | `pathParams: { id: invitationId }`, `body: { answer }` (`"accept"` or `"decline"`) | Final answer to the caller's own exact offer; `{ status: "accepted", clubId }` or `{ status: "declined" }` |
| `tournament-admin-invitation-answer` | Same shape with its own invitation ID | Final answer to the caller's own exact offer; `{ status: "accepted", tournamentId }` or `{ status: "declined" }` |
| `club-create` | `body: { name, sports, city, state?, hiddenFromPublic, seasonName, requestId }` | Creates Club, current season and caller's Admin membership; `{ id }` |
| `club-details-update` | `pathParams: { id: clubId }`, `body: { name, sports, city, state?, hiddenFromPublic, expectedRevision }` | Replaces details; returns saved Club details |
| `club-admin-invite` | `pathParams: { id: clubId }`, `body: { email, idempotencyKey }` | Saves an Admin offer and emails that address once; `{ invitationId, createdAt, expiresAt, delivery: "sent" \| "not_confirmed" }` |
| `club-team-create` | `pathParams: { id: clubId }`, `body: { name, sport, city, state, seasonName, ageGroup, hidden?, startsOn?, endsOn? }` | Creates permanently Club-owned Team and current season; `{ id }`; no staff appointment, roster entry, invitation or owner notice |
| `tournament-create` | `body: { id, setup: { name, sport, startDate?, endDate?, city?, state?, isPrivate, rankingAnswers } }` | Creates Tournament and caller's accepted Admin membership; `{ tournament, replayed }` |
| `tournament-details-update` | `pathParams: { id: tournamentId }`, `body: { name, sport, startDate?, endDate?, city?, state?, isPrivate, expectedRevision }` | Replaces **all** details; returns `{ id, details, revision, viewer }`; cannot edit Rules answers |
| `tournament-admin-invite` | `pathParams: { id: tournamentId }`, `body: { email, idempotencyKey }` | Saves Admin offer; `{ invitationId, createdAt, expiresAt, delivery: "inactive" }`; no email is sent |
| `tournament-admin-invitation-cancel` | `pathParams: { id: tournamentId, invitationId }` | Current Tournament Admin cancels an exact pending, unexpired offer; `{ status: "canceled" }`; no accepted appointment removed |

Accept grants real Admin authority. Decline consumes that offer without granting or removing any existing Admin authority. Both answers are final, not toggles. Unknown, another person's, expired or answered offers share `NOT_FOUND`; do not guess which. The invitation ID is not the Club/Tournament ID.

For sending an Admin offer, ask for the exact email directly from the person; never infer an address or probe whether it has an account. Email is trimmed, valid and at most 254 characters. For a Club offer, explain that a new offer emails that address once: `delivery: "sent"` means the email service took it (not proof it reached the inbox), and `not_confirmed` means it was not sent, was refused or its outcome is unknown. A per-recipient daily limit can silently stop the email and in-app notice while the offer still saves. Replaying the same `idempotencyKey` and email returns the saved answer and never emails again. For a Tournament offer, explain **delivery is inactive: no email is sent**. Either way, Admin access starts only after the recipient accepts through their own connection or the app. Do not promise a notification beyond the returned `delivery`, send a separate message, or send another offer to repair delivery. Current offers last 14 days unanswered; use the actual returned expiry. Sender limits return `RATE_LIMITED`.

For cancellation, use an exact ID from the current authorized sent-offer list. Confirm scope, pending status and expiry; show the ID and the recipient only if that list currently reveals it. Do not cancel by guessed email match, row order or name. A hidden address requires the person's explicit selection of the exact row/ID, or an app handoff. Being sender/recipient alone does not grant cancellation rights. There is **no Club cancellation tool** and no remove/leave-Admin tool for either kind.

## Prepare fields without inventing choices

- **Club create/details:** name 1–100 characters; sports 1–20 unique lowercase sport keys; city null or nonblank up to 100 characters; state null or two uppercase letters. Creation trims name; stored edits must have no surrounding spaces or control characters. Ask for an explicit Private choice (`hiddenFromPublic`). Creation needs a season such as `Spring 2027` or `Winter 2026-2027`. Details edits cannot change the current season.
- **Team creation:** name 1–50 characters, city 2–100, state two uppercase letters, sport and age group from the live schema, season name as above. Ask for an explicit Private choice (`hidden`). Send both real `YYYY-MM-DD` season dates or neither; end strictly after start. Never add `title`, coach IDs, roster entries or a retry key. Never adopt, import, transfer or release an existing Team into/out of a Club; that ownership boundary is permanent, not a missing-tool workaround.
- **Tournament create/details:** name 1–200 text units (some symbols count as two); sport key; dates null or real `YYYY-MM-DD`, end on/after start when both exist; city/state null or trimmed nonblank text up to 80 of those text units. State is **not** the Club two-letter constraint. Ask for an explicit Private choice (`isPrivate`). Omitted optional create fields default to null. For edits send every current value, including explicit nulls: omission resets optional fields to null rather than preserving them.
- **Sport:** no sport-list tool belongs to this skill. Use a returned saved key or an allowed live-schema value; if the schema permits, lowercase the sport word supplied by the person. Never invent alternate keys or submit a sport request. A sport refusal stops the action.
- **Rules answers at Tournament creation:** `rankingAnswers: { version: 1, traits: [...] }`, at most 256 ordered traits. `kind` is `wins`, `win-percentage`, `head-to-head`, `score-for`, `score-against` or `score-difference`. Optional `direction` is `higher`/`lower`; `drawValue` 0–1 belongs only to win-percentage/head-to-head; head-to-head `eligibility` is `two-team`/`complete-balanced-group`; score traits accept `aggregation: total | per-game` and `cap` (nonnegative safe integer, or null). Ask only for the Rules the person wants saved and preserve their order. Missing means unanswered, not a default; cap null means uncapped and zero is a known cap. Explain an empty traits list as no answers saved and get approval for that choice. These are saved answers, **not computed standings or a bracket**. No tool edits them after creation.

## Fresh revisions and retained request keys

Read details immediately before editing. Copy the exact returned decimal-string `revision` into `expectedRevision`, never a number. Carry forward unchanged fields; show old/new values plus required unchanged ones before yes. `CLUB_DETAILS_CHANGED` or `TOURNAMENT_DETAILS_CHANGED` means another edit won: re-read, show a fresh comparison and obtain a new yes, not an automatic overwrite.

Follow the live schema: Club `requestId`, new Tournament `id` and offer `idempotencyKey` are required UUIDs. For each new action, get one from the shared `request-key-new` tool; never hand-type or invent one. Never call `request-key-new` again for a retry or after a lost reply. A retry reuses that SAME key with unchanged inputs, and only after the [recovery rule](../SKILL.md#unclear-outcome-re-check-never-resend)'s re-check and a fresh yes from the person. If `request-key-new` is missing, refused, errors or times out, say so, save nothing, and use the Hype app's existing create/invite flow. Never reuse a key for another action or omit a required key. Retain it with the exact approved fields for this action; do not put addresses in a progress file. A same-key/same-input replay can recover Club creation or an offer; the same Tournament ID/setup can replay creation (`replayed: true`). Changed input with that key returns `IDEMPOTENCY_KEY_REUSED` or `TOURNAMENT_SETUP_CONFLICT`. **This is not permission to resend.** Follow the workflow's [recovery rule](../SKILL.md#unclear-outcome-re-check-never-resend) first. Never mint a replacement key to bypass a conflict. Club Team creation, detail replacements, answers and cancellation have no safe replay contract.

## Refusals and data handling

Explain the returned stable code and safe fix hint, not raw error text containing private inputs. Missing tools, schema/version mismatch, sign-in/access refusal, limits and invalid targets stop that action; do not create replacements, switch accounts or strip safeguards. `BUSY` on cancellation is explicitly not retryable: refresh the exact waiting list before any new decision. Respect `Retry-After`/validated `retryAfterSeconds`; no polling or automatic retry even when marked retryable. Keep requests sequential and below the connection's limits, shared with other sessions.

Use only the intended Hype write for approved private input. Keep contact details and credentials out of files, git, reports, pages, logs and other services. For roster data, the person's own files and progress record, follow [Your own files stay where you keep them](../../league-setup/references/own-files.md). Do not fetch returned links or images. Promise no guaranteed cross-session memory. Re-establish authorized state after lost context, never recreate records to recover it.
