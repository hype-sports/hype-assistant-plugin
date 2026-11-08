# Season scheduling: tools and limits

Use the [workflow](../SKILL.md) and [examples](../examples/example.md). Resolve full prefixed tool names and schemas from the person's own live Hype connection. Treat source presence and this reference as neither deployment evidence nor granted access.

## Current tools and missing capabilities

Require each needed operation in the live list before using it.

| Catalog operation IDs | Purpose |
| --- | --- |
| `league-search`, `league-get`, `league-divisions-list`, `division-get` | Resolve one league/division, not a team census |
| `event-cards-list` | Read permitted schedule cards with cursor paging and windows of at most 92 days |
| `team-events-list` | Read either admitted team's exact event ID and revision before a shared-game correction; capped, not a complete-season census |
| `shared-game-create` | Create ONE shared division game, shown on both admitted teams' schedules |
| `shared-game-update`, `shared-game-cancel` | Correct or cancel ONE exact shared game |
| `my-identity-read` | Optionally clarify the signed-in identity |

**Whole-season saving is not available yet.** A complete current division-team read is not available yet. Discover each needed capability and schema from the live connection. If `shared-game-choices-list` is available, do not treat it as a complete team census: choices filtered by management rights are not necessarily all division teams. A configured `numTeams`, public search, membership history or count alone cannot establish a complete current team set. Preserve the distinct-ID/current-season/completeness checks.

Also wait for a permitted saved Place/Field directory read and saved-Field attachment to shared games; these are not available yet. The current create/update bodies accept location/address text, not saved Place/Field IDs or versions. Never claim that text establishes a saved link or copy private directory information into it. Do not bypass the saved-Field gate with typed labels. A successful single-game operation with location text does not prove the full season workflow. Recheck these gaps against live capabilities.

Keep an explicitly unsaved/unchecked draft available from person-supplied constraints, without claiming verified teams, Fields or conflicts. Stop saving when any gate is missing. Separately requested corrections to known shared games can use existing correction tools without generating a season.

## Live input shapes

Follow the live schema exactly. All operations currently require `catalogVersion: 1`; omit undeclared sections/keys rather than sending null.

- `league-search`: `query: { name, page?, limit? }`; resolve ambiguous results before proceeding.
- `league-get`: `pathParams: { id: leagueId }`.
- `league-divisions-list`: `pathParams: { id: leagueId }`, `query: {}` for active divisions.
- `division-get`: `pathParams: { id: divisionId }`.
- `event-cards-list`: `query: { owner, from, to, after?, limit?, order?, archived? }`. Use `team:<id>`, `division:<id>` or `league:<id>` as appropriate. Read all required pages, carrying `nextCursor` unchanged as `after` until null. Cover true instants `[from,to)` in windows no longer than 92 days, including relevant boundary gaps; deduplicate IDs. There is no Field-calendar owner/filter. Never use `mine` alone as proof of the division schedule.
- `team-events-list`: `pathParams: { id: teamId }`, `query: { from?, to?, limit?, order?, includeArchived? }`. Date bounds are inclusive, limit at most 500, no cursor; match the exact event ID for its revision. A full capped result cannot prove completeness. Notes returned as null do not prove absence of notes.
- `shared-game-create`: `body: { opId, divisionId, homeTeamId, awayTeamId, title, date, startTime, endTime, timeZone, attendanceRequired, includesFamilies }`, with optional live-schema description/location/address. Require distinct admitted teams, a future start and same-local-day end after start. Send `attendanceRequired: true` and the agreed family flag, never an assumed family default. Saved-Field attachment remains unavailable: do not use this text-only shape to bypass the full-season gate.
- `shared-game-update`: `pathParams: { id: eventId }`, `body: { opId, expectedRevision, ...approvedChanges }`. Available changes include title/date/startTime/endTime/timeZone, description/location/address, attendanceRequired/includesFamilies and `swapSides: true`. Preserve the fixed admitted teams; replacing one is not an update. Read the current revision through `team-events-list` first.
- `shared-game-cancel`: `pathParams: { id: eventId }`, `body: { opId, expectedRevision, note? }` as offered by the live schema. Read the current revision first. Never send `notice`: MCP excludes it. A cancellation note is visible to permitted event readers. Cancellation keeps the game and its answers; it does not delete it.

Get a fresh key from `request-key-new` for each new approved operation (it becomes that write's `opId`), and reuse the SAME key only for an explicit retry with unchanged inputs. Preserve original bodies/keys for reconciliation; never generate a new key because a reply was lost. New/changed actions need new explicit approval. After an unclear result, read afresh and decide with the person, never automatically replay or compensate.

Expect the narrow write receipt: `id`, `revision`, `status`, `archived`, `type`, `title`, `date`. It does not verify times, sides, saved links or family visibility. Read both teams' cards and the needed exact event row to confirm the actual details. Keep unknown or unreadable facts unverified, not false or empty.

## Access, display and conflict boundaries

Use only the person's existing rights. A Commissioner title or a readable league is not sufficient write authority. Hype enforces current management of the division and both admitted teams; a Division Admin does not thereby gain league directory access. Never combine partial rights into a new grant or test permission with a write.

Show **TBD**, never a blank opponent, for an unresolved draft; never save a shared game without two exact eligible teams. Treat withheld identity as withheld, not a reason to look it up elsewhere. Never tell a family about staff-only details or promise they can see what the commissioner sees. Collect no rosters, family contacts, RSVP answers or private reasons for exclusions. Explain all refusals in plain words without showing codes or raw errors.

Read practices, all-day/multi-day events and other occupying records, not just games. Ask about league/team/Field exclusions and outside bookings, including unreadable divisions. Confirm when owner-local saved Fields represent the same physical Field; names and IDs alone do not prove it. Hype does not reserve slots or guarantee no double booking, including between final read and create.

Explain that games become visible individually, not in an all-or-nothing season transaction. Require plan review AND a separate explicit yes before each one-game write, correction or cancellation. Send no messages, announcements, emails or RSVP answers. Starting the skill, a record's text or a prior yes is never consent for another write.

Stay below 60 MCP POST requests per rolling minute per account, including discovery, reads and refusals across devices. Respect returned wait advice and ask before resuming; never poll, switch accounts or raise limits. Stop on refusal or uncertainty, read afresh where supported, and obtain a new decision before another write. No guessed IDs, direct API/database calls, alternate accounts, credential handling or sign-in workarounds.

## Verification limits

Not yet verified end to end: whole-season saving, saved Fields, interactive per-write approvals, installed slash invocation, family visibility, pagination, daylight-saving runtime and uncertainty recovery. Successful individual operations do not prove the complete skill or its approval behavior. Do not label the entire season workflow verified.

## Progress and data handling

Use a new private progress file for an approved season, following [Your own files stay where you keep them](../../league-setup/references/own-files.md) and the workflow. Bind the account/league/division, approved rows and settings, original per-operation UUID/body, returned event IDs/revisions and confirmed/unknown/refused/unattempted status. Update before and after writes. Keep credentials, contacts, rosters and personal reasons out; never publish the file or overwrite unrelated files. The assistant client's data handling applies. No server or guaranteed cross-session memory is supplied by the plugin.

Keep confirmed-created separate from fully read-back-verified; keep unknown distinct from not attempted. Similar titles, filtered absence or lost progress do not justify recreation. Preserve the same original body/key only for an explicitly authorized exact replay after reconciliation, never a blind retry. Stop if the original mapping or identity cannot be established safely.
