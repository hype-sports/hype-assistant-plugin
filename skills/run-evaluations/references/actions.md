# Evaluation action details

Read the [main workflow](../SKILL.md) first. Its live-tool checks, exact-target approval, privacy, request-key and unknown-outcome rules apply to every action here. Read only the section needed for the requested change.

## 2. Score a player, set a Hand-set score or save a private note

Use a fresh own `my-private-evaluation-open` response for categories, player identity and the separate observation, overall and note revisions. Respect its current/read-only/removed states. Revisions are not interchangeable and must never be guessed.

| Exact operation ID | Inputs after `catalogVersion` |
| --- | --- |
| `my-private-evaluation-participant-score-save` | `pathParams: { id: datasetId, participantId }`; `body: { operationId, categoryId, state, points, expectedRevision }`. Supports registered and typed-in players. Take `participantId` from the own open response or the matching evaluation's permitted player list, and category/revision from the own open response. |
| `my-private-evaluation-score-save` | `pathParams: { id: datasetId }`; `body: { operationId, registrationId, categoryId, state, points, expectedRevision }`. Registered-player form; use the returned registration ID, never a participant ID in its place. For typed-in players, use only the participant form. |
| `my-private-evaluation-overall-save` | `pathParams: { id: datasetId }`; `body: { operationId, registrationId, manualPoints, expectedOverallRevision }`. Use the registration ID and `overallRevision` from the own sheet. |
| `my-private-evaluation-note-save` | `pathParams: { id: datasetId }`; `body: { operationId, registrationId, authorNote, expectedNoteRevision }`. Use the registration ID and `noteRevision` from the own sheet. |

For an observed category, send `state: "observed"` with whole points 0–10. Convert the requested 0–5 stars in half-star steps to points by multiplying by two; zero is a real score. Distinguish not observed (`"skipped"`) from clearing the category (`"blank"`), both with `points: null`; ask which is intended when unclear. Use revision 0 only when the read actually shows no saved observation. Category clearing does not clear the hand overall.

Call the hand overall **Hand-set score**, separate from **Calculated average**. Set `manualPoints` to whole points 0–10 using the same star conversion, or explicit null only for a requested clear. This never changes category scores. Copy the returned overall revision even when no score has yet been set; do not invent 0. Save notes as exact approved text up to 2,000 Unicode characters, or explicit null for a requested clear. Never silently shorten or rewrite a note. Before saving a note, read the own sheet's `my-private-evaluation-share-recipients-list` and check `activeShares`. A note stays private unless included in an active share; warn in the preview if it is already shared with notes on.

The documented overall/note tools require a registration ID. If a typed-in row has none, explain that these tools cannot save hand-set scores or private notes for that typed-in player. Stop those two actions; do not substitute its participant ID or invent a participant overall/note tool. Typed-in category scoring remains supported through the participant tool.

## 3. Share scores, change included notes or stop a share

Read `my-private-evaluation-share-recipients-list` with `pathParams: { id: datasetId }` for the person's own sheet. Select a new recipient only from `recipients`; select an existing own share only from `activeShares`. Resolve repeated names before proceeding. The eligible list is not proof that everyone on it has a share. Never look up contacts or type a recipient ID.

- **Share**: `my-private-evaluation-share-create`, `pathParams: { id: datasetId }`, `body: { operationId, recipientId, includeNotes }`. Ask explicitly whether to include notes; no default. Explain that this shares the coach's current scores, not a frozen file, and includes private notes only if chosen. Both coaches must remain eligible. Preview the exact coach and notes choice, then wait for yes. Do not promise an email or other notice.
- **Include or exclude notes on a share**: `my-private-evaluation-share-notes-set`, `pathParams: { shareId }`, `body: { includeNotes }`. No operation ID. Explain whether the other coach will gain or lose access to notes; scores stay shared. Notes-on requires both coaches still eligible; notes-off does not require recipient eligibility. Obtain yes to this exact change, not permission to rewrite the note itself.
- **Stop sharing**: `my-private-evaluation-share-stop`, `pathParams: { shareId }`, no body or query. No operation ID. Explain: **This removes the other coach's access to these shared scores and notes. Your own scores stay saved.** Wait for yes. Do not promise to erase anything they already saw.

A share-create replay returns an active share's current notes choice, not necessarily its original one; a stopped share or changed original command is refused. Notes-set and stop have no replay receipt. Never treat a repeat-safe tool label as permission to retry. No share action is covered by the score receipt lookup.

## 4. Change the evaluation's player list

Read `private-evaluation-players-list` with `pathParams: { id: evaluationId }`. Only a current list manager may change it; scoring or a received share is insufficient. Preserve unsaved, archived, removed and number-conflict states. A projected unsaved registration is not yet a saved participant.

Use `private-evaluation-players-change` with `pathParams: { id: evaluationId }`, `body: { operationId, expectedRevision, change }`. Copy the list's current `revision` into `expectedRevision`, not a score or dataset revision. Prepare only the requested form:

- Registered add: `change: { kind: "add", registrationId }`, using the registration from that list. Explain that this may restore a removed registered player or assign the next evaluation number.
- Typed-in add: `change: { kind: "add", firstName, lastName }`, with optional `guardianEmail` only if explicitly supplied by the person. Names must already be trimmed, 1–60 characters and free of control characters. An optional parent/guardian email must already be trimmed and lowercase; ask for a correction rather than silently rewriting it. Do not collect it unless needed for the requested add; never look it up or repeat it in summaries. The email is not returned, and saving it is not proof of an invitation or notice.
- Remove: `change: { kind: "remove", participantId }`, from the list. Warn: **Removing a typed-in player cannot be undone. Adding the same name later makes a new player with a new number; earlier scores stay with the removed player.** A name fix must use edit, not remove then add.
- Typed-in name fix: `change: { kind: "edit", participantId, firstName, lastName }`. Use the same name checks, and explain that this keeps the player's identity and earlier scores. Do not use this to rename a registered player's profile.
- Requested number changes: `change: { kind: "renumber", numbers: [{ participantId, number }] }`, using current participants, each once, with whole numbers 1–9999. Show the complete requested mapping and any conflicts before approval; never repair numbers as a side effect of scoring or reading.

List changes can update invitee housekeeping but do not save/share scores. After an unclear result, the score receipt tool cannot resolve this operation. Offer a fresh authorized list read, not an automatic repeat.

## 5. Start an evaluation or add a date

Distinguish starting a personal sheet at an existing event from creating a new division evaluation. Never create one just to obtain IDs or discover access.

- **Personal sheet at a known event**: after the approved `private-evaluation-setup-read` on that event, choose only its admitted registration tokens and explicitly agreed `categoryNames`; suggestions are not approval. Use `my-private-evaluation-create`, no path/query, `body: { operationId, eventId, registrationIds, categoryNames }`. Explain that it creates the coach's private sheet/categories, not a calendar event, scores or share. There is one sheet per coach/evaluation; do not create a duplicate after a refusal.
- **New division evaluation**: use permitted league/division reads and `division-players-lookup` to resolve the division and selected registration IDs, asking before more pages. Do not borrow player IDs from another division. Require ordinary league authority OR a live Division Admin appointment for this exact active division; scoring access alone is insufficient. Agree title, date, explicit IANA time zone (such as `America/Chicago`), exact players and categories. Use `division-evaluation-create`, no path/query, `body: { operationId, divisionId, title, eventDate, timeZone, registrationIds, categoryNames }`. Explain that it creates an all-day calendar event, evaluation/date link and player list/numbers. With league authority it also creates the person's private sheet/categories and receipts; through Division Admin authority it returns only a management receipt, with no dataset or private categories and no scoring admission. Report only the returned result. Neither path saves scores, shares anything or sends notices. Send no invented notice field.
- **Another date for an existing evaluation**: find its evaluation ID from event context or `private-evaluation-date-candidates-list`, `pathParams: { id: divisionId }`, `query: {}` initially. This lists eligible evaluations, not free calendar slots. For a requested later page, carry `nextCursor.afterId` unchanged as `query.afterId` with the same division; optional `pageSize` accepts a number or digit string for a whole value 1–50 under the coercing route schema, default 50 (saved-header/share lists require digit strings). Require current list-management rights and active evaluation/parents. Agree today-or-later `eventDate` in the chosen IANA zone. Use `private-evaluation-date-add`, `pathParams: { id: evaluationId }`, `body: { operationId, eventDate, timeZone, notice }`.

**Ask the person to choose the date's notice setting; never default it.** Currently supported saving uses `notice: { notify: false }` and sends no notice. If the person chooses a notice, the prepared form is `{ notify: true, commentsEnabled, noticeMessage }` with their explicit choices, but current notice sending is unavailable: stop and explain rather than silently switching it off. Only save without a notice after fresh agreement to that exact plan. Adding a date creates an all-day event linked to the same evaluation, not another sheet or a copy of scores. No setup or date action is covered by score receipts.

## 6. Choose the evaluation shown privately in a draft

Use known draft IDs from permitted draft reads; follow [run-a-draft](../../run-a-draft/SKILL.md) for commissioner draft actions. Read `my-draft-private-evaluation-read` with `pathParams: { id: draftId }`, `query: {}` or `{ expectedDraftTeamId }` only to assert a known current coach seat. This requires the person's own coach seat; commissioner status alone grants no other coach's choice. Treat `none` and `unavailable` literally; never pick a default/latest fallback or reveal a hidden source.

For the explicitly chosen own dataset from own evaluation reads, use `my-draft-private-evaluation-set` with the same path/query and `body: { operationId, datasetId, expectedRevision }`, copying the choice revision just read. Explicit `datasetId: null` clears the choice. For an explicitly chosen eligible received share, the alternative body uses `shareId` instead of `datasetId`, from the person's received-shares read; never send both. A share does not become an own sheet.

Explain before yes: **This changes only the evaluation scores shown to you in this draft. It does not change your scores, share them, choose another coach's source or change the draft's player numbers.** `draft-number-evaluations-list` is a commissioner-only read of possible number sources, not a setter; do not promise a number-source change through it.
