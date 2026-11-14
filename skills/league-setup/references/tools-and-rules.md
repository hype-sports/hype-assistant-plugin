# League-setup reference

Use the [workflow](../SKILL.md); see the [worked conversation](../examples/league-setup-conversation.md). Use live schemas and never create records to test access. For unclear results, follow only the workflow's [single recovery rule](../SKILL.md#if-a-result-is-unclear).

## Reads and saves

| Step | Reads | Save after preview and yes |
| --- | --- | --- |
| League | `league-search`, `league-get` | `league-create` |
| Divisions | `league-divisions-list`, `division-get` | `league-division-create`, including initial teams |
| Details | `league-get` or `division-get` | `league-update` or `division-update` |
| Staff | Use `league-staff` | Follow that skill's role choices under the shared list approval |
| Players | `division-players-lookup` | `division-player-create` |
| Parents/guardians | `league-player-guardian-invitations-list`, `league-invitation-allowance-get` | One approved `league-player-guardian-invitation-create`; use `invite-families` for many parents |
| Roster import | `division-player-import-preview` or `league-player-import-preview` | Matching `division-player-import` or `league-player-import`, with complete reviewed rows and choices; no invitations |
| Saved-import parents | Confirmed import's `inviteRecipients` | Reviewed `league-import-guardian-invitation-create` per recipient, fresh key from `request-key-new` |
| Readiness | `division-onboarding-get`, supplemented by permitted requested reads | Nothing |
| Season end | Exact scope, `division-impact` as applicable | Archive/restore included in the shared review |

Treat these operations as reference shapes, including `league-update`, `division-update` and the five import operations, not as a promise of live availability or access. Check the actual connection before offering a step.

## Current input shapes

Use these input shapes as a reference. Supply the current wrapper's required `catalogVersion: 1` and defined `pathParams`, `query`, `body` containers; omit undefined containers and unlisted keys. Never send an actor/account id. Re-read the live version/schema; list outputs may be wrapped in `items`.

### League discovery and creation

- `league-search.query`: optional nonempty `name`, `sport`, `city`, `state`; `page` ≥1 (default 1), `limit` 1–50 (default 20). Output has `results` and `pagination` (`page`, `limit`, `total`, `totalPages`, `hasNext`, `hasPrev`). One requested page at a time; no automatic traversal. Active league basics include Private leagues, not management authority or an exhaustive directory.
- `league-get.pathParams`: `{ id }`. Report the Private choice as **sent at creation, not confirmed**: `hiddenFromPublic` is a create input only, and league detail has no such field. Visible counts may be lower for coaches. `viewerStaff` describes the caller and may be unknown; `viewer.role: commissioner` is a capability label, not proof of their Commissioner title or Admin role. Missing and inaccessible share `NOT_FOUND`.
- `league-create.body`: required `name` (trimmed, 3–100 characters), `sport`, `season`, `city` (2–100), `state` (two uppercase letters), explicit boolean `hiddenFromPublic`. Omit optional `logoUrl` for ordinary creation; use the app for a custom logo. Never fetch or accept a chat URL. `season` is `Spring YYYY`, `Summer YYYY`, `Fall YYYY` or `Winter YYYY-YYYY` with consecutive winter years. No separate `year` or time-zone input. Creation returns detail and makes the caller League Admin and Commissioner.
- There is no sport-list operation. Ask for the sport; use `league-create`'s live allowed values if enumerated. Current `sport` schema checks the lowercase-key shape, not catalog membership. Lowercasing the supplied word is allowed when it fits; never invent an alternate mapping/key. A sport refusal stops the save, not an automatic substitution.
- `league-divisions-list`: league `pathParams.id`; `query.archived` is optional text `"true"` or `"false"` at schema input. Default/false reads active divisions, true archived only; no pagination or combined filter.
- `division-get`: division `pathParams.id`. Verify `league.id` and both archived states. `numTeams` is configured; `teamCount` / `counts.teams` are visible current counts, not a complete team/season/coach set.

### Division creation

`league-division-create`: existing league `pathParams.id`, plus `body`:

| Field | Meaning / limits |
| --- | --- |
| `name` | Trimmed, 3–50 characters; age group plus Boys/Girls/Coed or an approved custom name |
| `gender` | `male`, `female`, `coed`; display Boys, Girls, Coed |
| `ageGroup` | Contract-optional `5U`–`18U`; ask explicitly in this workflow |
| `minAge` | Whole number, 4–18 |
| `maxAge` | Whole number, 5–18, strictly above minimum |
| `ageCalculationDate` | Real `YYYY-MM-DD` eligibility date, not season start |
| `teamSeasonAgeGroup` | Required `5U`–`18U` for new teams; explicitly match the division choice, independently of numeric eligibility |
| `numTeams` | Whole number, 2–50; actually creates Team 1 through Team N without coaches |
| `playersPerTeam` | Whole number, 5–30; setting, not roster count |
| `allowPlayerExceptions` | Boolean, default true; approve an explicit choice |

Require all other fields in this table. Explain that division/initial teams save in one transaction; existing teams, coaches and registrations are not attached. Do not collect initial team names: `numTeams` creates Team 1 through Team N with no team-name field. Leave renaming to each team itself, outside this skill. Never infer division age group or numeric eligibility from names or team seasons.

### Detail edits

Use the exact existing scope's `pathParams.id` for both edits. Read immediately before preview; show changed values and required unchanged ones. Compare the saved readback, including any derived division name. Do not assume a revision/retry key; neither edit has one, so a repeat may overwrite later work.

- `league-update` uses a strict assistant `body`: **`name` and `sport` required** even when unchanged; optional `city` and `state`. Copy required unchanged values from the fresh read, include them in approval, and omit untouched fields. Empty city/state leave them unchanged. Validation follows creation. **Never send `season`, `year` or a time zone**: season/year are locked; Hype derives the time zone. Current league staff only; archived leagues refuse. Linked profiles can lock sport changes (`LEAGUE_SPORT_LOCKED`); never guess an alternate sport.
- For optional `logoUrl`, use only the returned address of an explicitly reviewed `demo-logo-upload` for this caller and logo kind. Offer it only when the person asks for the demo artwork: it uploads approved made-up shipped art by `assetId`, never their own picture. Any signed-in caller may use it within current upload rights. Custom logos stay in the app. Include both upload and attachment effects in the same complete review and yes; bind the attachment only to the confirmed upload receipt. Discover the live `body: { assetId, kind }`, use `kind: "league-logo"` and a matching allowed asset; never invent an asset, fetch an image or use a chat URL.
- A demo upload returns `path`/`publicUrl` without attaching. Each call spends quota and may leave an unused object; never retry uncertainty. Attachment checks caller-owned storage. `logoUrl: null` removes a logo only on explicit yes; omitting it keeps the logo. The assistant cannot view it; ask the person to check the app. Assistant detail always returns `logoUrl: null`, not proof that no logo exists.
- `division-update`: send only changed fields, at least one: `name` (3–50), `gender`, `ageGroup` (`5U`–`18U`, cannot clear a saved group), `minAge`/`maxAge` (whole numbers 4–18, minimum strictly below maximum including stored values), `ageCalculationDate` (real date), `allowPlayerExceptions`, `playersPerTeam` (5–30), `numTeams` (2–50). Current league staff or accepted scoped Division Admin only; a **Division Admin cannot send `name`**. No completion flag in the tool schema. **`numTeams` only changes configuration: no team is created/removed.** Archived league/division refuses edits; name/age-group changes can yield a derived name or a name-conflict refusal. Explain known effects in the preview, not an unapproved rename afterwards.

### Staff invitations

Use [League staff](../../league-staff/SKILL.md) and its [tool reference](../../league-staff/references/reference.md) for the single staff policy, live role/title fields, keys, permissions, private previews, recipient answers and recovery. Do not duplicate that workflow here.

### Registrations and parents/guardians

- `division-players-lookup`: division `pathParams.id`; `query.page` ≥1 (default 1), `pageSize` 1–100 (default 25), optional trimmed `search` ≤100. Search matches first/last name; `*` and NUL refuse. Output: `items`, `page`, `pageSize`, `total`; assistant items have registration `id`, `divisionId`, first/last name, `status` (`active`/`inactive`). No birth dates, contacts, evaluation numbers or profile links. Archived registrations omitted, inactive included. Pages are fresh reads, not one snapshot; ask before more pages. Filtered absence is not a division-wide census.
- `division-player-create`: division `pathParams.id`; required `body.firstName`, `lastName` (trimmed 1–50), `dateOfBirth` (real date, not future/before 1900), `gender` (`male`/`female`), explicit boolean `evaluationAttended`. Only league staff may create. Follow the workflow's immediate [birth-date confirmation](../SKILL.md#5-register-players-invite-parentsguardians); do not copy it into later summaries.
- For that **single-registration create only**, optional `parentEmail`/`parentPhone` may be omitted/null, otherwise must validate. It has no second-parent or `emergencyContacts` field: never use it to import a two-parent sheet. Use the roster-import tools below instead, not repeated creates or contact writes to somebody else's profile. `evaluationNumber` is optional and not needed here. `exceptionConsent` is an approval value, not invented or replaced by a general yes; unavailable exception handling goes to the app.
- Create output: registration `id`, names, `divisionId`, `divisionName`, `status`, `evaluationAttended`; no private-field readback. Use registration ids, not family profile or team roster-entry ids. A failed readback can follow a saved registration; apply the linked recovery rule.
- Both parent/guardian tools: `pathParams: { id: leagueId, playerId: registrationId }`. Confirm actual registration scope; knowing an id is not authority. Create `body: { email, idempotencyKey }`; `idempotencyKey` is a fresh key from `request-key-new` per new invite, reused unchanged only for a retry the person explicitly asks for after a fresh complete review and a yes in their next message; trimmed/lowercased valid email ≤254 characters.
- Create returns `{ id, email, replayed, replaced, replacedInvitationId }`. A new invite attempts email, sends an in-app notice and replaces a pending offer to that address; `replacedInvitationId` is null when none. `email` is `sent` (service acceptance), `not_sent` (still created) or `unknown` (may already have gone out); never resend on email status alone. With `replayed: true`, it returns the first outcome and original replacement facts, with no new email, notice or replacement.
- List contains pending references with `inviteeEmail: null`, not address-specific duplicate evidence or accepted guardians. Never accept or link a profile on the recipient's behalf.
- Follow [Invitation allowance](reviewed-batch.md#invitation-allowance) for the appropriate allowance read/preview.
- Existing registration edit/move/archive/restore, deletion and unlink tools are left to the app by this skill, not unavailable. Do those actions in the app with exact identity, field/exception and access review.

### Two-parent roster imports

Follow the workflow's [import and invitation review](../SKILL.md#import-a-sign-up-sheet-without-losing-either-parent). These tools use the ordinary import routes, not personal-profile contact management. Use the person's own connection as the containing league commissioner; the server rechecks access. Missing and refused scopes share `NOT_FOUND`.

- `division-player-import-preview` and `division-player-import`: `pathParams: { id: divisionId }`. Every row is placed in that exact division, regardless of the row's division field.
- `league-player-import-preview` and `league-player-import`: `pathParams: { id: leagueId }`. Each row names an exact authorized division in that league. Neither path creates team roster entries or family profiles.
- Both preview and commit bodies have `rows`, **1–1,000** entries. Each row requires `divisionId`, `firstName`, `lastName`, `dateOfBirth`, `gender` (the live gender value or null), `parentEmail` (valid email or null), `parentPhone` (text or null), `evaluationAttended` (boolean or null), and `evaluationNumber` (valid number or null). A null optional roster value means the sheet did not say, not a request to clear saved data. Follow the live schema for names, dates, gender and numbers; do not guess a missing birth date or attendance answer.
- Each row may include `emergencyContacts`, at most **two** entries in the source's parent order. Each contact needs `firstName`, `lastName` and a normalized full international `phone` (for example `+12025550123`). In league-setup imports only (other skills keep their own phone rules), before the first review, and only when the league's state is a US state or DC, convert a number written with just digits, spaces, dashes, dots or parentheses that is exactly 10 digits (or 11 starting with 1) and whose area code and exchange each start 2–9 to `+1` and those 10 digits; show each as "was → becomes" with a count. Anything else (a `+` or `00` prefix, an extension, another digit count, a non-US league) is listed for the person to correct, never converted, dropped or left out on your own. The same applies to the row's `parentPhone`; `email` is optional or null. Preserve both supplied parents, not two competing values of `parentEmail`. Do not invent a phone to keep an email-only parent; report incomplete source details and ask for correction before committing an affected row. The single sign-up email/phone fields do not replace this array.
- Preview takes optional `choices`; commit **requires** `choices`, even an empty array. Each choice names `rowIndex` (one-based source row). The ordinary optional fields are `action` (`skip`, `update_candidate`, `add_new`), `registrationId`, `updateFields`, `clearFields`, `stored`, `updatedAt`, `acceptOutsideRules`, `exceptionConsent`, `previewedStatus`, `replaceEmergencyContacts`, and `contactsRevision`. Keep actual reviewed values from the preview. The live schema controls allowed field names and values; do not add a retry key, invent exception consent or silently turn on an exception/contact replacement.
- Read only the person's chosen sheet under [own-files privacy](own-files.md), map its columns and retain source positions and both parents in their original slots. Never silently discard incomplete contacts or collapse them into the single sign-up email. Leave an affected row out for correction where required; never invent missing phones/names or swap slots.
- Preview returns `rows` describing matches, differences, identity candidates, contact status/revision, warnings and errors; it saves no players, contacts or invitations. Review all intended additions, omissions, updates, separate same-name registrations, contact replacements and exact eligibility exceptions. Preserve actual reviewed stored values, update time, contact revision and exception consent. Show supplied birth dates only to this asker in the immediate approval, never summaries. A changed plan needs another preview/yes; a preview is not a permission lease.
- Ask for explicit approval of the exact target, complete rows and choices, wait for yes in the person's next message, then commit once. Continue only other requested actions included in the shared review; importing alone never approves omitted sends.
- Commit returns `applied`, `batchId`, per-division `created`/`updated` counts, `skipped`, `alreadyHere`, `duplicatesInFile`, `errors`, `notes`, `stale`, optional `emergencyContacts` counts, and `inviteRecipients`. `applied: false` means no player changes were saved; review `stale` rows and get a new yes, never automatically resubmit. Contact counts distinguish saved/kept and family, incomplete, candidate, duplicate, coach or capacity skips where returned; an absent count or unassigned reason is unknown, not zero or a guessed row-level result.
- Each saved `inviteRecipients` entry has `rowIndex`, `parentSlot` (1 or 2), nullable `parentName`, `playerId`, `divisionId` and normalized `email`. Retain **every** recipient, including slot 2. This is a saved-import receipt, not approval to send or proof of an invitation. Keep its private details for the person's requested work and under the existing own-files limits; do not repeat addresses in summaries, logs, reports or messages.
- There is **no import retry key**. An unclear commit may already have saved data; stop, do not repeat or start invitations, and inspect only the affected item once through a supported authorized read, without extra approval; if unavailable, keep it unknown and use the app rather than scan broader lists. Current state cannot prove that lost call's outcome.

### Import into divisions created in the same plan

This is the only case where the preview runs after the yes, because the league or divisions it needs do not exist yet.

- In the one plan, show every row in a placement table (names, birth date and gender for this asker only) with the division it will land in. Work this out from each new division's gender, age calculation date and age range. Show as **not placed, needs your choice** any row with a missing or invalid birth date or gender, any row that fits no division, and any row that fits more than one. Say plainly that those rows are left out, never imported as exceptions under this yes. A division-level import into one new division places every row there regardless of birth date; say so instead of a worked-out placement.
- Say in the plan that the import is conditional: it runs under this yes only if the server's preview confirms the plan exactly.
- Never edit, drop, reformat or leave out any row or value (a phone, an email, a name, a division) to get past a preview refusal or difference; conversions happen only before the first review. Dropping a parent's phone is a change the person did not approve.
- After creating the structure, run the preview. Import under the same yes only if every planned row comes back as a plain new addition in its planned division: no match, identity candidate, update, contact replacement, exception, warning, error, skip or in-file duplicate. Every choice must be `add_new`, and the counts must equal the plan. Anything else: stop, show exactly what differs, and wait for a new yes. If time passes or anything changes before that yes, preview again.
- Invitations in the same plan depend on the import's receipts; a skipped or changed recipient needs a revised review (see the invitation section).
- The plan lists the exact invitations it will send. Read the invitation allowance only for the league being acted on, right after it is created; never borrow an allowance, default or setting from another league, archived or not. If the allowance is lower than the list, or the saved recipients differ from the plan, show the shorter or changed list in send order for a fresh complete review and next-message yes before sending any. Skips at send time (already invited, already linked) are reported, not a stop. Never send more invitations than the plan listed, and report every listed parent who got none, with the reason returned or "unknown" if none was.

### Invitations to saved import parents

`league-import-guardian-invitation-create` takes `pathParams: { id: leagueId, playerId: savedRegistrationId }`, no query, and `body: { email, idempotencyKey }`. Use the exact email from a confirmed saved `inviteRecipients` entry and a new key from `request-key-new` for each new send. Existing pending offers are **not replaced**: do not substitute generic `league-player-guardian-invitation-create` to work around a refusal. Current authority and saved-import contact checks still apply at the write.

Use only the confirmed import's saved registration/division, source-row/parent-slot references and exact address, never an unsaved recipient or profile ID. Explain absent parents from returned contact/skipped results; an unassigned reason is unknown. Keep all first parents before any second parents across the whole import, preserving source order within each slot. Review all recipients together; send first parents before second parents without another yes between groups. Keep distinct registration/address pairs; siblings sharing an address still need separate invitations. Warn about repeated emails with source references, not repeated addresses.

Show each complete numbered page: exact league/division, every source row, parent slot, saved registration and intended send, omitted rows/reasons and total send count. Use stable unambiguous supplied-address references without echoing addresses. Explain real email/in-app notice, preservation of pending offers and no access until acceptance. Show the complete requested recipient list across divisions, grouped for clarity with no per-page ceiling or approval. Apply the shared single yes and revised-list rules. Get one fresh key per approved recipient, then send individually in reviewed order; no parallel/background writes or unreviewed follow-up.

Before page review, follow [Invitation allowance](reviewed-batch.md#invitation-allowance) for individual sends (for a league created in the same plan, read it right after creation instead; see [Import into divisions created in the same plan](#import-into-divisions-created-in-the-same-plan)). Space MCP starts at least 1.1 seconds apart, including key requests, and respect shared-account and ordinary invitation limits. A rate refusal blocks sends covered by that limit and dependent steps; finish only other approved independent parts still allowed. On deliberate resumption require a current reviewed remainder and one new yes; never wait out a daily cap on old approval.

Success returns `{ id, email, replayed, replaced, replacedInvitationId }`; `email` is a send outcome, not an address. `sent` means service acceptance, not mailbox delivery; `not_sent` means saved without email delivery to the service; `unknown` may already have reached the parent. No access until acceptance. A replay returns the first outcome without another send. Keep the same key and exact inputs only for a later deliberately requested retry after a fresh complete review and a yes in the person's next message; never retry automatically or send again to repair an email status. Unexpected replacement is a changed effect: stop and report it, never treat it as ordinary saved-import behavior.

Report confirmed `INVITATION_ALREADY_PENDING` as Already invited, skipped, and `ALREADY_A_GUARDIAN` as Already linked, skipped. Other confirmed refusals and authorization/rate limits block the affected sends and dependent steps, not approved independent work still allowed. Interruption or an unclear write stops all writes for inspection. Record each remaining source row/parent slot as Not sent with the reason; distinguish an unknown attempted write from an unattempted one. Never discard Parent 2 or claim a skipped/unknown parent was invited. A missing key or key tool stops before sending; a key-reuse refusal never permits a fresh-key workaround.

### Season-end effects

Treat `archive: false` / `delete: true` on a brand-new unused league or division as available-action flags, not a refused archive call. Explain that Hype offers Delete while the scope is new and unused; Archive appears once it has players. For cleanup requiring Delete, use the app; never delete through this skill or extend its separately requested archive/restore steps.

Lifecycle/impact tools take only exact `pathParams: { id }`; no body, query, cascade/confirmation selector or retry key. `division-impact` returns `teams`, `coachOwnedTeams`, `players`: deletion-impact counts, **not an exact archive batch**. League visible counts are not an archive preview either.

Archive includes registrations/eligible league-made teams; league archive also includes divisions. Coach-run teams stay active, as can league-made teams in another league's open draft. Optional archive `teamsLeftActive` counts skipped teams; absent means not told. Restore reverses the matching batch, league first; separately archived divisions need their own restore. Division restore's `teamsPlacedElsewhere` is not returned by plain league restore; moved teams stay put. Restore does not resume age-group control without later placement.

## Refusals

Explain the actual stable code and safe hint, never raw errors quoting private inputs. Corrected writes need a fresh complete review and next-message yes.

| Answer | Meaning / next step |
| --- | --- |
| Missing tool/connection or sign-in cannot finish | Stop this step; no workaround. |
| `FORBIDDEN`, `NOT_FOUND`, sign-in required | No current access or missing scope; do not probe hidden versus missing or create replacements. |
| Validation/version/sport refusal | Explain the rejected field and stop; no guessed keys, sport substitution or stripped safeguards. |
| Archived / already archived / not archived | Wrong current state; no automatic restore or replacement. |
| `LEAGUE_SEASON_LOCKED`, `LEAGUE_SPORT_LOCKED` | Season is fixed or linked players prevent this sport change. Leave locked data alone. |
| `DRAFT_IN_PROGRESS` | Open draft blocks archive; do not close it. |
| Duplicate / `CONFLICT`, eligibility/exception refusal | Check identity or use supported app handling; no fabricated consent, altered identity or deletion. |
| Staff self-invite, existing staff or invitation budget | Offer refused; no unapproved replacement, role or recipient change. |
| `IDEMPOTENCY_KEY_REUSED` (409, not retryable) | For League staff or parent/guardian invites, the key belongs to a different action or an invite that is no longer pending. Stop; never get a new key to try again. Send the person to the app's Staff screen or the player's invitations. |
| Restore registration conflict | Stop; no deletion/move to force restore. |
| `RATE_LIMITED`, `BUSY` | Respect the returned wait and deliberate resume; no retry loop/account switching. |
| `WRITE_OUTCOME_UNKNOWN` or unclear save | Apply only the [single recovery rule](../SKILL.md#if-a-result-is-unclear). |

## Data handling

Follow [Your own files stay where you keep them](own-files.md) for the person's files and progress record. Never copy private inputs into anything other than the person's chosen place, subject to that rule's content limits. The assistant client's conversation handling applies. If context is lost, re-establish authorized identity/state, not records through recreation or reinvitation. Keep the workflow's confirmation/privacy limits; do not copy private inputs or rosters into logs, reports or examples. The intended approved Hype write is their only external destination. Do not fetch logo/avatar URLs or promise cross-session memory.
