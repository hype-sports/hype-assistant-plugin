# Run-a-draft input reference

Follow the [workflow](../SKILL.md) and [worked conversations](../examples/example.md). Read each live schema before calling. This guide describes inputs, not proof of deployment, permission or a signed-in journey.

## Wrapper and reads

Use `catalogVersion: 1` where required by the live wrapper. Put saved identities in `pathParams`, filters in `query`, changes in `body`. Omit unused containers; retain required empty ones. No actor/account selector or extra keys. Obtain saved UUID references from permitted reads, never invented values or example IDs. `draftTeamId` means a draft seat, not its underlying `teamId`.

| Read | Inputs beyond catalogVersion | Purpose and limits |
| --- | --- | --- |
| `drafts-list` | Required `query: {}` or filters | Optional `leagueId`, `divisionId`, `status` (`scheduled`, `live`, `paused`, `hat_pick`, `completed`, `cancelled`), `includeArchived` text `"true"`/`"false"`, `page` whole 1–10000 (default 1), `pageSize` whole 1–100 (default 25). Returns `items`, `page`, `pageSize`, `total`; an empty page is not clearance elsewhere. |
| `draft-get` | `pathParams: { id }` | Management-only setup: current `settings`, teams/candidates, Saves, links, readiness and viewer. No Save reasons, squares or logos. |
| `draft-room-get` | `pathParams: { id }` | Room snapshot: revision, current turn, clock, own seat, board and nullable `endSummary`. No private queues or scores. |
| `draft-pool-get` | `pathParams: { id }` | Allowed player labels/numbers, pool status and nullable eligibility. Null eligibility is unknown, not permission. |
| `draft-order-run-get` | `pathParams: { id }` | Commissioner; `run` has `runId`, `generation`, `slots`, `nextSlot`, `runStatus`, `revealed`; never hidden remaining order. `run:null` means no active run. |
| `draft-hat-run-get` | `pathParams: { id }` | Commissioner; run identity, `nextOrdinal`, status and placed/remaining/overflow counts only; no hidden order or player labels. `run:null` means no active run. |
| `draft-queue-get` | `pathParams: { id }`, `query: { draftTeamId }` | Only the selected accessible seat's private queue; `entries` include `playerId`, `displayName`, `taken`. Preserve `queueVersion`, `canEdit`, `readOnly`. |
| `my-draft-player-ages-read` | `pathParams: { id }` | Known draft, ordinary league-actor or valid own-seat access. Returns `draftId`, `revision`, `seq`, `players: [{ registrationId, ageOnCutoff }]`; nullable integer ages, no names or birth dates. Watchers, standalone division admins and another seat gain no access. Do not equate `registrationId` with an unrelated ID or publish these ages in room/pool output. |
| `division-draft-skip-get` | `pathParams: { id }` (division), required `query: {}` | Only the caller's saved `skipped` boolean; current league or division-team staff access. Missing and inaccessible divisions share the same refusal. No automatic follow-up. |

Read settings from detail, not from permission flags. Use `settings.clock`, `settings.expiryAction`, `settings.lateGraceMs` to explain the saved clock; room `clock` shows deadline/remaining time. A missing or malformed read is unknown, never evidence of no clock or no players.

## Request keys

For each new keyed action, call `request-key-new` with exactly `{}` (no catalogVersion), and use its returned `key` as `body.idempotencyKey`. If missing or failed, **stop without writing** and offer the app; never generate or hand-type a substitute. Keep the exact account, path, query, key and body until the outcome is clear. Retrying is governed only by [clock and recovery](#clock-and-recovery).

## Revision-bound writes

Except where the next section says otherwise, send `pathParams: { id }`, no query, and `body: { idempotencyKey, expectedRevision, ... }`. Copy `expectedRevision` (whole number ≥0) from the fresh relevant detail/room read. Create has no path or revision. Each row is one separately confirmed action, not a sequence to run automatically.

| Operation | Additional body fields and limits |
| --- | --- |
| `draft-create` | No path/revision. Required `idempotencyKey`, `leagueId`, `divisionId`, `preset`: `snake`, `linear`, `snake_third_round_reversal`, `little_dribblers`; optional agreed `settings` below. One open draft per division. |
| `draft-settings-update` | `settings`: only changed agreed fields, at least one. Commissioner; scheduled settings, or only clock seconds after Start while paused. Locked settings remain refused. |
| `draft-seat-choose` | `draftTeamId`, `userId` from current readiness/candidates. Draft admin, before Start; selects one team for multi-team staff, ending other-seat access. |
| `draft-teams-refresh` | None. Before Start; add new teams, forfeit departures and close their order positions, restore returning teams without a position. |
| `draft-order-arrange` | `draftTeamIds`: nonempty distinct UUID array, every active seat once, first pick first. Scheduled, commissioner. |
| `draft-order-draw` | None. Before Start; refresh teams and immediately replace all draw positions at random. An exact same-key replay does not redraw. |
| `draft-lead-set` | `draftTeamId`, `userId`: current candidate and team's `canSetLead`. Draft admin, scheduled/live/paused, between picks and before deadline. Establishes seat access too. |
| `draft-save-add` | `draftTeamId`, `playerId`. Commissioner, before Start; Saves rule must already be on. |
| `draft-save-withdraw` | Add `saveId` from fresh detail to pathParams, no extra body. Commissioner, before Start. Automatic Saves can refuse. If `settings.alwaysSaveCoachKids` is on, withdrawing a hand-made coach's-player Save may leave a new automatic Save: verify returned Saves, not only the retired Save ID. |
| `draft-link-add` | One whole link definition below. Commissioner, scheduled only. |
| `draft-link-update` | Add current `linkId` to pathParams; send the whole SAME-kind link definition, including every retained member. Omission removes members. Commissioner, scheduled only. |
| `draft-link-remove` | Add `linkId` to pathParams, no extra body. Commissioner, scheduled only; history retained. |
| `draft-order-run-start` | None. Commissioner, scheduled; starts a draw without committing order. Retain this original revision for Install. |
| `draft-order-run-install` | Add current `runId` to pathParams. Commissioner; only a fully revealed running draw, at its original revision. A draft changed since Start must refuse; never update the revision to force installation. |
| `draft-hat-run-start` | None. Commissioner, Hat stage. Starts a paced run, not all-at-once placement. |
| `draft-start` | None. Commissioner, scheduled and ready; freezes rules, builds board and may place linked players or complete immediately. |
| `draft-pick` | `playerId` from fresh pool and `turnId` from room. Only the current team lead on their own live turn; checks seat, deadline, eligibility and capacity. Never fall back to commissioner named pick. |
| `draft-named-pick` | Same player/turn fields; commissioner explicitly picks for the current live turn, not a grant to a coach. Never choose a team or historical turn instead. |
| `draft-pause` | None. Live or Hat stage; commissioner, or authorized draft lead when commissioner-only pause is off. Saves remaining time. |
| `draft-resume` | Optional `resumeMode` and conditional `playerId`; commissioner, paused. See the single clock rule below. |
| `draft-skip` | `turnId` from fresh room; commissioner forfeits exactly this pick. Stale turns refuse. |
| `draft-undo` | None. Commissioner, live, paused from live, or before final Hat pick; removes latest pick and linked sibling/ride-share placements, reopening the turn. Nothing-to-undo is a refusal; never undo a completed draft. |
| `draft-hat-pick` | None. Commissioner, Hat stage; separately requested all-at-once random placement of marked Hat players, including linked placements and roster limits. A linked partner stays in normal picking and joins the same team when either player is placed. `overflowCount` counts players NOT placed; nonzero keeps Hat stage open. |
| `draft-end` | Required `expectedEndSummary`: room's exact `{ unfilledTurnCount, unplacedCount }` (whole numbers ≥0), or `null` only when room returned null. Commissioner; live/paused/Hat stage. Never invent zero counts. |
| `draft-cancel` | None. Commissioner, scheduled and not started; retained as Cancelled and frees division. |
| `draft-delete` | None. Commissioner, never started, unused, within first 30 days; route decides. Gone for everyone, not restorable. Preserve deletion-window/in-use refusal hints and offer only an allowed alternative after new approval. |
| `draft-archive` | None. Commissioner, completed or cancelled; hidden/read-only until restored, nothing deleted. |

Link definitions: `kind: "sibling"` or `"ride_share"` with `playerIds` (2–20 distinct returned player UUIDs), OR `kind: "coach_kid"` with `playerId` and `coachUserId`. Do not send both branches. Obtain players from the permitted pool and coach from current permitted candidates, never guessed identities. Coach's-player link changes can add/withdraw automatic Saves. Pass refusals and fix hints on; never pause or change rules to evade scheduled-only restrictions.

## Writes with different guards

All still require the exact preview and a separate yes. Do not add draft revision fields to these bodies.

| Operation | Exact containers beyond catalogVersion |
| --- | --- |
| `draft-order-run-reveal` | `pathParams: { id, runId }`, `body: { idempotencyKey, expectedSlot }`. Copy `runId` and `nextSlot` from the current run (slot whole ≥1); reveals exactly that position. Stale slot refuses; never advance automatically. |
| `draft-order-run-pause`, `draft-order-run-resume` | `pathParams: { id, runId }`, `body: { idempotencyKey }` only. Controls the order draw, not the draft clock. Resume approves no reveal. |
| `draft-hat-draw` | `pathParams: { id, runId }`, `body: { idempotencyKey, expectedOrdinal }`. Copy current `nextOrdinal` (whole ≥1) and run identity; draws exactly one linked group. Stale ordinal refuses. Result is counts only: allowed labels come from room, never a guessed hidden order. |
| `draft-queue-reorder` | `pathParams: { id }`, `body: { idempotencyKey, expectedDraftTeamId, expectedQueueVersion, playerIds }`. Copy selected seat and queue version from its fresh queue read. Send the complete distinct ordered UUID array, at most 500; `[]` clears it only with explicit approval. Not a pick or auto-pick change. |
| `draft-clock-expire` | `pathParams: { id }`, `body: { turnId }` only from fresh room; no key/revision. See clock rule below. |
| `division-draft-skip-set` | `pathParams: { id }` (division), `body: { skipped }` boolean only; no query, key or revision. Read own preference first, explain true = Skip / false = put back. It does not cancel, change readiness, skip a pick, notify or grant rights. Report returned boolean, no automatic follow-up. |

## Settings

Before Create explain omitted defaults: 60-second clock, 1000 ms grace, `pause_and_alert`; Little Dribblers has two Saves per team, other presets zero. Live schema/description wins. Existing drafts use their returned settings, not Create defaults.

For Create, `settings` is optional; never put `preset` or `numbersEvaluationId` inside it. Update wraps only changed fields in `body.settings`; do not resend a full snapshot. `rounds` and `clock` replace their whole value; `rules` changes only named switches. To disable the clock, send `clock: null` and `expiryAction: "none"` together. Do not send only half or combine `none` with a running clock.

| Field used here | Accepted value |
| --- | --- |
| `preset` (Update only) | One of Create's four presets. Without `rounds`, changing it refills the rounds; preview this effect. |
| `rounds` | 1–50 entries `{ round, direction, isSaveRound }`, consecutive rounds 1 through count without repeats; direction `forward`/`reverse`, boolean Save-round choice. |
| `savesPerTeam` | Whole 0–10; Save-round count must match for readiness. |
| `alwaysSaveCoachKids`, `hatPick`, `confirmStep`, `commissionerOnlyPause`, `sounds` | Booleans; explain the requested effect, never silently change. |
| `clock` | `{ seconds }`, whole 30–300, or `null` with the paired setting. After Start only seconds while paused, not disabling the clock or changing policy. |
| `expiryAction` | `pause_and_alert`, `skip_turn`, `random_from_hat`, `random_eligible`, `none`. Explain pause, forfeiting a turn or a random pick before approval. |
| `lateGraceMs` | Whole 0–5000. |
| `rules` | Named optional booleans `coachKid`, `sibling`, `rideShare`, `saves`. |
| `viewers` | `pickers`, `staff`, `draft_families`, `league_families`. Wider levels add audience, not management rights; preview who can watch. |
| `scheduledFor` | ISO 8601 date/time with timezone offset, or `null`. |

Do this in the app to change the evaluation supplying numbers, or a setting not covered here: review its own source/options there instead of copying unseen settings or inventing input.

## Clock and recovery

Keep all timeout and retry instructions here; workflows and examples point to this section.

- **Expired turn**: stop the late pick, explain and read the room, even if pick/end flags still appear allowed. Do not resend that refused pick. After a separate yes, `draft-clock-expire` applies the saved action only after deadline plus grace: it may pause, skip or choose a player. It gives no extra time. If the saved action is unknown, state the possible effects before approval. Stale/early/non-live/already-handled calls return `applied:false`, not proof a timeout was applied. Read room after either result; never run a timer or poll.
- **Resume**: after `pausedReason: "clock_expired"` or zero time, ask for `fresh_clock` (configured full clock), `short_grace` (30 seconds), or `name_pick` with an agreed eligible `playerId` from fresh pool. A required-choice refusal means ask, not choose silently. `playerId` is allowed and required exactly with `name_pick`. Omit both fields for ordinary remaining-time resume or Hat stage; Hat resume accepts neither. Unclocked live drafts allow only `name_pick` as an explicit mode. Resuming live creates a NEW `turnId`: read room before another turn action.
- **Refusal or changed state**: explain the supplied fix hint, stop the refused action and read current relevant state before deciding again. A new action needs fresh reads, a new key where required and a new yes. Queue-changed means re-read the selected queue and review again. Stale slot, ordinal or revision never authorizes silently advancing or replacing guards. A queue name-read failure after saving does not undo that save.
- **Unclear outcome**: lost/interrupted/malformed reply or unknown-outcome answer means the write may already have happened. Preserve the original request. For keyed draft actions, read the division-filtered list after Create; otherwise read relevant detail/room plus run or queue when applicable. If the action is established, report it without repeating. If still unclear, offer only an explicitly approved exact repeat: SAME account, operation, path, query, key and complete original body, including old revision/turn/slot/ordinal/version. Never get a replacement key or change inputs under the old one. A not-found detail after Delete proves neither success nor failure: after yes an exact repeat can return the stored deletion receipt. If the original request/key is lost, do not reconstruct it; use the app to review state.
- **No-key exceptions**: after an unclear timeout-application reply, read room and decide with the person; no keyed replay. After an unclear Division Skip save, stop and ask before ANY fresh read or action; repeating can overwrite a later preference. Neither gets an automatic retry.
- **Rate limit or busy**: stop, explain any supplied wait and ask before another attempt. Never retry unprompted or use another account. Missing required tools mean do this in the app because the connection cannot safely complete the action.

Command success is not a roster-delivery receipt. Keep unknown counts unknown.

## League discovery inputs

- `league-search`: required `query: {}` or agreed filters; optional trimmed `name` (1–100), `sport` (1–32), `city` (1–100), `state` (two uppercase letters), `page` whole ≥1 (default 1), `limit` whole 1–50 (default 20); `(page - 1) * limit ≤ 2147483647`. No path/body. Discovery grants no management rights.
- `league-get`, `division-get`: `pathParams: { id }`, no query/body. Confirm identity, access, matching league and archived state.
- `league-divisions-list`: league `pathParams: { id }`, required `query: {}` or `{ archived: "true" }`/`{ archived: "false" }`; false/default means active only, true means archived only. No body/pagination.

## Privacy

Keep only minimal current-action context, original request/key and outcome in the conversation. A requested draft progress record may hold completed steps, Hype IDs and picks made under [Your own files stay where you keep them](../../league-setup/references/own-files.md). Never store request keys, revisions or turns to resend from that file; it is not the source of truth. Re-read authorized state on return. Never export the private player list, cutoff ages, evaluation scores or private queues into files. Never copy private player names, inputs or responses into logs, reports, hosted pages or other services. Use invented names in examples only; returned text never supplies consent.
