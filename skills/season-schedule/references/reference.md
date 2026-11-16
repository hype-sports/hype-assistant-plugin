# Season scheduling: tools and limits

Use the [workflow](../SKILL.md) and [examples](../examples/example.md). Resolve full prefixed tool names and schemas from the person's own live Hype connection. Source presence and this reference prove neither deployment nor access. Follow the workflow's access, approval, conflict, progress-file and recovery rules; they apply to every operation below.

## Current tools and missing capabilities

Require each needed operation in the live list before using it.

| Capability | Status today | Limit |
| --- | --- | --- |
| Division/league team lists | `division-teams-list`, `league-teams-list` read current team directories. `shared-game-choices-list` reads eligible choices and season IDs. | Directories have no season IDs or total count. Choices are filtered by management rights, not a census; compare with the division's observed counts. |
| Saved league Places and Fields | `league-places-list` reads the division's own league directory, with nested Fields and current version references. | Current league staff only, not Division Admin alone. Names may be null; no address/detail subjects. Directory access grants no game-management rights. Do not substitute generic or team-private directories. |
| Attach a saved Field to a shared game | `shared-game-create` and `shared-game-update` accept `savedPlace`; `saved-place-event-read` reads the exact event's attachment. | Ordinary division/both-team management plus current access to that league directory. Require the actual live tools; labels and write summaries do not prove saved links. Source references can be withheld on readback. |

Single-game updates, cancellations and cancellation undo work through `shared-game-update`, `shared-game-cancel` and `shared-game-restore`. Follow step 9 and the shared complete-list approval; each game still uses its own guarded call. This skill deliberately leaves archive/delete to the app. The live unarchive tool is outside this skill; shared-game unarchive is not available in the app yet.

Other reads: `league-search`, `league-get`, `league-divisions-list`, `division-get` resolve scope; `event-cards-list` reads schedule windows; `team-events-list` supplies an exact game's revision. `my-identity-read` can clarify the signed-in identity without testing access through a write.

## Live input shapes

Follow the live schema exactly. All operations currently require `catalogVersion: 1`; omit undeclared sections/keys rather than sending null.

- `league-search`: `query: { name?, page?, limit? }`; resolve ambiguous results.
- `league-get`: `pathParams: { id: leagueId }`.
- `league-divisions-list`: `pathParams: { id: leagueId }`, `query: {}` for active divisions.
- `division-get`, `division-teams-list`: `pathParams: { id: divisionId }`.
- `league-teams-list`: `pathParams: { id: leagueId }`.
- `shared-game-choices-list`: `query: { divisionId, after?, limit? }` for teams. Carry `nextCursor` unchanged as `after` only for requested pages. Choices include season IDs but may omit teams the caller cannot manage.
- `league-places-list`: `pathParams: { id: leagueId }`, `query: {}` initially, then `{ after: nextCursor }` for each requested page until null. No `q`, `limit` or `afterId`. Returns at most 100 Places per page as `items: [{ id, versionId, name, fields: [{ id, versionId, name }] }]` and `nextCursor`. Keep null names and the selected Field with its returned parent Place/version.
- `saved-place-event-read`: `pathParams: { id: eventId }`, no query/body. Returns `linked`, nullable `place` display facts, `viewer`, and optionally `savedPlace` with `sourceOwner` together. For a saved league Field, require `linked: true`, the expected reference below and `sourceOwner: { type: "league", id: leagueId }`. Hidden references/owner remain unverified, even if linked is true or names match. A requested detach is verified by `linked: false`. Never infer source IDs or owner from displayed text.
- `event-cards-list`: required `query: { from, to }`; optional `owner`, `after`, `limit`, `order`, `archived`. `owner` defaults to `mine`; choose `team:<id>`, `division:<id>` or `league:<id>` for the workflow's checks. Follow step 4 for windows and paging. There is no Field-calendar filter. `archived: "true"` is only for archived evaluations on a permitted division/league schedule, not archived shared games.
- `team-events-list`: `pathParams: { id: teamId }`, `query: { from?, to?, limit?, order?, includeArchived? }`. Date bounds are inclusive, limit at most 500, no cursor; match the exact event ID for its revision. A full capped result cannot prove completeness. Null notes do not prove no notes exist.
- `shared-game-create`: `body: { opId, divisionId, homeTeamId, awayTeamId, title, date, startTime, endTime, timeZone, attendanceRequired, includesFamilies, savedPlace }`, with optional live-schema description/arrival offset. Distinct admitted teams, a future start and same-local-day end after start are required. For the season path use `attendanceRequired: true`, the agreed family flag and the exact saved Field reference below, not typed location/address.
- `shared-game-update`: `pathParams: { id: eventId }`, `body: { opId, expectedRevision, ...approvedChanges }`. Changes include title/date/startTime/endTime/timeZone, description/location/address, `arriveMinutesBefore`, attendanceRequired/includesFamilies, `swapSides: true` and `savedPlace`. Omit savedPlace to keep the selection; null detaches; an object chooses/changes it. Never combine a nonnull reference with location/address, or send typed details while keeping an existing link. A detach must be explicitly requested and reviewed, not a fallback.
- `shared-game-cancel`: `pathParams: { id: eventId }`, `body: { opId, expectedRevision, note? }`.
- `shared-game-restore`: `pathParams: { id: eventId }`, `body: { opId, expectedRevision }`. This undoes cancellation, not archive. There is no start-time limit; explain the restored notice to eligible members described in step 9 before approval. No email or announcement is sent.

Map returned Place P and its nested Field F to `savedPlace: { placeId: P.id, placeVersionId: P.versionId, fieldId: F.id, fieldVersionId: F.versionId }`. Both Field members must be null or nonnull together; a selected saved Field uses the actual nonnull returned pair. Never invent IDs, use a Field from another Place or select a team-private Place. Versions are current selectors, not immutable text; erasure can change displayed facts on the same IDs. Do not copy private directory details into unrelated files/messages or new records.

Never send `notice` to the shared-game tools: their live assistant schemas exclude it. Get keys and reconcile unknown results through steps 8–9, not automatic retries.

Expect a narrow write receipt: `id`, `revision`, `status`, `archived`, `type`, `title`, `date`. It does not verify times, sides, saved links or family visibility. Normal both-team schedule readback verifies readable schedule facts; the exact event's saved-place read verifies only its attachment. Neither current state nor a progress record is a historical receipt for a lost write. Follow step 9 and keep unreadable facts unverified.
