# Season scheduling: tools and limits

Use the [workflow](../SKILL.md) and [examples](../examples/example.md). Resolve full prefixed tool names and schemas from the person's own live Hype connection. Source presence and this reference prove neither deployment nor access. Follow the workflow's access, approval, conflict, progress-file and recovery rules; they apply to every operation below.

## Current tools and missing capabilities

Require each needed operation in the live list before using it.

| Capability | Status today | Limit |
| --- | --- | --- |
| Division/league team lists | `division-teams-list`, `league-teams-list` read current team directories. `shared-game-choices-list` reads eligible choices and season IDs. | Directories have no season IDs or total count. Choices are filtered by management rights, not a census; compare with the division's observed counts. |
| Saved Places and Fields | `saved-places-list`, `saved-place-fields-list` read permitted directories and current version references. | Use the division's league directory and selectable records. Directory access grants no game-management rights; preserve redacted facts. |
| Attach a saved Field to a shared game | Missing from `shared-game-create` and `shared-game-update`; these accept location/address text only. | Keep whole-season plans unsaved. To save with saved Fields, do this in the app; never substitute typed labels or send saved IDs to these tools. |

Single-game updates, cancellations and cancellation undo work through `shared-game-update`, `shared-game-cancel` and `shared-game-restore`. Follow step 9 for one game and one explicit yes. Archive/unarchive/delete tools also exist; this skill deliberately leaves them to the app, as explained there.

Other reads: `league-search`, `league-get`, `league-divisions-list`, `division-get` resolve scope; `event-cards-list` reads schedule windows; `team-events-list` supplies an exact game's revision. `my-identity-read` can clarify the signed-in identity without testing access through a write.

## Live input shapes

Follow the live schema exactly. All operations currently require `catalogVersion: 1`; omit undeclared sections/keys rather than sending null.

- `league-search`: `query: { name?, page?, limit? }`; resolve ambiguous results.
- `league-get`: `pathParams: { id: leagueId }`.
- `league-divisions-list`: `pathParams: { id: leagueId }`, `query: {}` for active divisions.
- `division-get`, `division-teams-list`: `pathParams: { id: divisionId }`.
- `league-teams-list`: `pathParams: { id: leagueId }`.
- `shared-game-choices-list`: `query: { divisionId, after?, limit? }` for teams. Carry `nextCursor` unchanged as `after` only for requested pages. Choices include season IDs but may omit teams the caller cannot manage.
- `saved-places-list`: `query: { leagueId, q?, limit?, afterId? }` for this plan.
- `saved-place-fields-list`: `pathParams: { id: placeId }`, the same directory query. Both return `nextCursor`; carry it unchanged as `afterId` for requested pages, resetting on scope/search change. Keep the returned parent version with each Field reference. `canSelect` is not event-edit permission.
- `event-cards-list`: required `query: { from, to }`; optional `owner`, `after`, `limit`, `order`, `archived`. `owner` defaults to `mine`; choose `team:<id>`, `division:<id>` or `league:<id>` for the workflow's checks. Follow step 4 for windows and paging. There is no Field-calendar filter. `archived: "true"` is only for archived evaluations on a permitted division/league schedule, not archived shared games.
- `team-events-list`: `pathParams: { id: teamId }`, `query: { from?, to?, limit?, order?, includeArchived? }`. Date bounds are inclusive, limit at most 500, no cursor; match the exact event ID for its revision. A full capped result cannot prove completeness. Null notes do not prove no notes exist.
- `shared-game-create`: `body: { opId, divisionId, homeTeamId, awayTeamId, title, date, startTime, endTime, timeZone, attendanceRequired, includesFamilies }`, with optional live-schema description/location/address/arrival offset. Distinct admitted teams, a future start and same-local-day end after start are required. For the guarded season path use `attendanceRequired: true` and the agreed family flag. Today's text-only body must not be used to save the whole-season plan.
- `shared-game-update`: `pathParams: { id: eventId }`, `body: { opId, expectedRevision, ...approvedChanges }`. Changes include title/date/startTime/endTime/timeZone, description/location/address, `arriveMinutesBefore`, attendanceRequired/includesFamilies and `swapSides: true`. No saved Place/Field IDs or versions.
- `shared-game-cancel`: `pathParams: { id: eventId }`, `body: { opId, expectedRevision, note? }`.
- `shared-game-restore`: `pathParams: { id: eventId }`, `body: { opId, expectedRevision }`. This undoes cancellation, not archive. There is no start-time limit; explain the quiet restored notice described in step 9 before approval.

Never send `notice` to the shared-game tools: their live assistant schemas exclude it. Get keys and reconcile unknown results through steps 8–9, not automatic retries.

Expect a narrow write receipt: `id`, `revision`, `status`, `archived`, `type`, `title`, `date`. It does not verify times, sides, saved links or family visibility. Follow step 9's readback and keep unreadable facts unverified.

## Verification limits

These instructions alone do not prove installed slash invocation, interactive per-write approvals, family visibility, pagination, daylight-saving runtime or uncertainty recovery. Whole-season saving remains stopped. Successful individual operations do not verify the whole skill.
