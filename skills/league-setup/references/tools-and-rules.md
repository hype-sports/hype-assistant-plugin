# League-setup reference

Run `/hype:league-setup` for the [workflow](../SKILL.md); see the [worked conversation](../examples/league-setup-conversation.md). Do not treat source checks as proof of live tools, access or an end-to-end pilot. Use live schemas and never create records to test access. For unclear results, follow only the workflow's [single recovery rule](../SKILL.md#if-a-result-is-unclear).

## Reads and saves

| Step | Reads | Save after preview and yes |
| --- | --- | --- |
| League | `league-search`, `league-get` | `league-create` |
| Divisions | `league-divisions-list`, `division-get` | `league-division-create`, including initial teams |
| Details | `league-get` or `division-get` | `league-update` or `division-update` |
| Staff | `league-staff-list`, `division-admin-list` | Respective `league-staff-invite`, `division-admin-invite` |
| Players | `division-players-lookup` | `division-player-create` |
| Parents/guardians | `league-player-guardian-invitations-list` | `league-player-guardian-invitation-create` |
| Readiness | Permitted scope/staff/registration reads | Nothing |
| Season end | Exact scope, `division-impact` as applicable | Separately approved archive/restore |

Treat all 21 named operations as available in the reference, including `league-update` and `division-update`, not as a promise of live availability or access.

## Current input shapes

Use these input shapes as a reference. Supply the current wrapper's required `catalogVersion: 1` and defined `pathParams`, `query`, `body` containers; omit undefined containers and unlisted keys. Never send an actor/account id. Re-read the live version/schema; list outputs may be wrapped in `items`.

### League discovery and creation

- `league-search.query`: optional nonempty `name`, `sport`, `city`, `state`; `page` ≥1 (default 1), `limit` 1–50 (default 20). Output has `results` and `pagination` (`page`, `limit`, `total`, `totalPages`, `hasNext`, `hasPrev`). One requested page at a time; no automatic traversal. Active league basics include Private leagues, not management authority or an exhaustive directory.
- `league-get.pathParams`: `{ id }`. Report the Private choice as **sent at creation, not confirmed**: `hiddenFromPublic` is a create input only, and league detail has no such field. Visible counts may be lower for coaches. `viewerStaff` describes the caller and may be unknown; `viewer.role: commissioner` is a capability label, not proof of their Commissioner title or Admin role. Missing and inaccessible share `NOT_FOUND`.
- `league-create.body`: required `name` (trimmed, 3–100 characters), `sport`, `season`, `city` (2–100), `state` (two uppercase letters), explicit boolean `hiddenFromPublic`. Optional `logoUrl` is null or an already-supported caller-owned league-logo image; no uploads/fetches. `season` is `Spring YYYY`, `Summer YYYY`, `Fall YYYY` or `Winter YYYY-YYYY` with consecutive winter years. No separate `year` or time-zone input. Creation returns detail and makes the caller League Admin and Commissioner.
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

- `league-update` uses a strict assistant `body`: **`name` and `sport` required** even when unchanged; optional `city` and `state`. Copy required unchanged values from the fresh read, include them in approval, and omit other untouched fields. Empty city/state leave them unchanged. Name/city/state/sport validation follows creation. **Never send `season`, `year` or a time zone**: season/year are locked and Hype derives the time zone. Optional `logoUrl` takes only the address `demo-logo-upload` returned for this person's own upload (Hype checks it is our image storage and their own folder); never a URL from the chat, never fetched. `null` removes the logo and needs the person's explicit yes; omitting it keeps the logo. You cannot see the picture: ask them to check it in the app. Assistant detail always returns `logoUrl: null`, not proof there is no logo. Current league staff only; archived leagues refuse. Linked profiles can lock sport changes (`LEAGUE_SPORT_LOCKED`); no alternate sport guessing.
- `division-update`: send only changed fields, at least one: `name` (3–50), `gender`, `ageGroup` (`5U`–`18U`, cannot clear a saved group), `minAge`/`maxAge` (whole numbers 4–18, minimum strictly below maximum including stored values), `ageCalculationDate` (real date), `allowPlayerExceptions`, `playersPerTeam` (5–30), `numTeams` (2–50). Current league staff or accepted scoped Division Admin only; a **Division Admin cannot send `name`**. No completion flag in the tool schema. **`numTeams` only changes configuration: no team is created/removed.** Archived league/division refuses edits; name/age-group changes can yield a derived name or a name-conflict refusal. Explain known effects in the preview, not an unapproved rename afterwards.

### Staff invitations

- League tools: league `pathParams.id`. Invite `body`: `{ email, makeOwner?, title? }`; trimmed email ≤254 characters. `makeOwner` defaults false and offers **Admin**; `title` can only be `commissioner`. At least one role required. Only a current League Admin may invite; no account search by email.
- List returns accepted `staff` and pending `invitations`. Assistant pending rows hide addresses. `viewerIsOwner: false` gives `invitations: []` even when offers exist; `isOwner: null` is withheld, not false.
- League invite returns `{ id, email? }`: `email` is send status, not an address. `sent` means mail-service acceptance, `not_sent` still means created, absent means unknown. Recipient acceptance is separate.
- Division Admin tools: division `pathParams.id`; invite `body: { email }`, trimmed/valid ≤254, output `{ id }`. Only the containing League Admin may list/invite; Commissioner/Division Admin alone is insufficient. List has `admins` and pending `invitations`, without addresses in the connector. **No email transport** for the invite; no appointment until acceptance.
- Both staff invites replace a pending offer for the same normalized address, not harmless deduplication. Address-free rows cannot identify the recipient.

### Registrations and parents/guardians

- `division-players-lookup`: division `pathParams.id`; `query.page` ≥1 (default 1), `pageSize` 1–100 (default 25), optional trimmed `search` ≤100. Search matches first/last name; `*` and NUL refuse. Output: `items`, `page`, `pageSize`, `total`; assistant items have registration `id`, `divisionId`, first/last name, `status` (`active`/`inactive`). No birth dates, contacts, evaluation numbers or profile links. Archived registrations omitted, inactive included. Pages are fresh reads, not one snapshot; ask before more pages. Filtered absence is not a division-wide census.
- `division-player-create`: division `pathParams.id`; required `body.firstName`, `lastName` (trimmed 1–50), `dateOfBirth` (real date, not future/before 1900), `gender` (`male`/`female`), explicit boolean `evaluationAttended`. Only league staff may create. Follow the workflow's immediate [birth-date confirmation](../SKILL.md#5-register-players-invite-parentsguardians); do not copy it into later summaries.
- Optional `parentEmail`/`parentPhone` may be omitted/null, otherwise must validate. `evaluationNumber` is optional and not needed here. `exceptionConsent` is an approval value, not invented or replaced by a general yes; unavailable exception handling goes to the app.
- Create output: registration `id`, names, `divisionId`, `divisionName`, `status`, `evaluationAttended`; no private-field readback. Use registration ids, not family profile or team roster-entry ids. A failed readback can follow a saved registration; apply the linked recovery rule.
- Both parent/guardian tools: `pathParams: { id: leagueId, playerId: registrationId }`. Confirm actual registration scope; knowing an id is not authority. Create `body: { email }`, trimmed/lowercased/valid ≤254. It attempts email, sends an in-app notice and replaces a pending offer to that address. Output `{ id, email }` has send status `sent`/`not_sent`; failed mail does not undo creation. List contains pending references with `inviteeEmail: null`, not address-specific duplicate evidence or accepted guardians. Never accept or link a profile on the recipient's behalf.

### Season-end effects

Treat `archive: false` / `delete: true` on a brand-new unused league or division as available-action flags, not a refused archive call. Explain that Hype offers Delete while the scope is new and unused; Archive appears once it has players. For cleanup requiring Delete, use the app; never delete through this skill or extend its separately requested archive/restore steps.

Lifecycle/impact tools take only exact `pathParams: { id }`; no body, query, cascade/confirmation selector or retry key. `division-impact` returns `teams`, `coachOwnedTeams`, `players`: deletion-impact counts, **not an exact archive batch**. League visible counts are not an archive preview either.

Archive includes registrations/eligible league-made teams; league archive also includes divisions. Coach-run teams stay active, as can league-made teams in another league's open draft. Optional archive `teamsLeftActive` counts skipped teams; absent means not told. Restore reverses the matching batch, league first; separately archived divisions need their own restore. Division restore's `teamsPlacedElsewhere` is not returned by plain league restore; moved teams stay put. Restore does not resume age-group control without later placement.

## Refusals

Explain the actual stable code and safe hint, never raw errors quoting private inputs. Corrected writes need a new preview/yes.

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
| Restore registration conflict | Stop; no deletion/move to force restore. |
| `RATE_LIMITED`, `BUSY` | Respect the returned wait and deliberate resume; no retry loop/account switching. |
| `WRITE_OUTCOME_UNKNOWN` or unclear save | Apply only the [single recovery rule](../SKILL.md#if-a-result-is-unclear). |

## Data handling

The plugin stores no progress file or server-side record; the assistant client's conversation handling applies. Keep minimal scope/id/outcome context, not a private-data export. If context is lost, re-establish authorized identity/state, not records through recreation or reinvitation. Follow the workflow's confirmation/privacy limits; never copy private inputs or rosters into files, git, reports, hosted pages, logs, other services or examples. The intended approved Hype write is their only external destination. Do not fetch logo/avatar URLs or promise cross-session memory.
