# League staff tool reference

Resolve operation IDs to full live names. Read needed schemas before use; current access and the live schema always win. Use the [workflow](../SKILL.md) for review, later-turn approval, privacy and recovery.

## Inputs and read paths

Supply the live required `catalogVersion` (currently 1), saved UUIDs and only defined containers. Omit unused query/body; never generate existing-record IDs. Only a new League staff invitation needs a key, from `request-key-new`.

| Operation | pathParams | Other inputs / use |
| --- | --- | --- |
| `league-search` | None | `query: { name }`, optional `page` ≥1 and `limit` 1–50; one requested page |
| `league-get` | `{ id: leagueId }` | No body/query |
| `league-divisions-list` | `{ id: leagueId }` | `query: {}` for active; `archived: "true"` only for a requested archived read |
| `league-staff-list` | `{ id: leagueId }` | Accepted staff; pending offers visible to League Admin only |
| `division-admin-list` | `{ id: divisionId }` | Containing League Admin only, not appointed Division Admin alone |
| `my-division-admin-divisions-list` | None | No body/query; caller's own current live appointments, not a management list |
| `my-identity-read` | None | No body/query; establish caller `userId` for self-leave |
| `league-staff-invite` | `{ id: leagueId }` | `body: { email, idempotencyKey, makeOwner, title? }`; Admin, title or both |
| `league-staff-update-title` | `{ id: leagueId, userId }` | `body: { title }`; valid title or null to clear an Admin's label only |
| `division-admin-invite` | `{ id: divisionId }` | `body: { email }`; no key, no email transport |
| `league-staff-remove` | `{ id: leagueId, userId }` | No body/query |
| `division-admin-remove` | `{ id: divisionId, userId }` | No body/query; self-leave can use own appointment without League reads |
| `league-staff-invitation-cancel` | `{ id: invitationId }` | No body/query; exact pending offer |
| `division-admin-invitation-cancel` | `{ id: invitationId }` | No body/query; exact pending, unexpired offer |
| `my-league-staff-invitations-list` | None | No body/query; recipient's own pending offers |
| `my-division-admin-invitations-list` | None | No body/query; recipient's own pending offers |
| `league-staff-invitation-accept`, `league-staff-invitation-decline` | `{ id: invitationId }` | No body/query; recipient's own connection and exact listed invitation |
| `division-admin-invitation-accept`, `division-admin-invitation-decline` | `{ id: invitationId }` | No body/query; recipient's own connection and exact listed invitation |

Invite addresses are trimmed valid emails, at most 254 characters. Obtain them directly; never infer or probe account existence. `makeOwner` means **League Admin**, independently of the display `title`. The title accepts 1–30 trimmed characters under live validation, including Commissioner or a custom title; Admin is a role, not a title. Require Admin or a title, or both. `league-staff-update-title` changes no Admin grant or membership; only Admins can have no title. Existing Admin-grant changes are left to the app; do this in the app, never by removal/re-invitation.

## Read projections and authority

- Discovery returns basics and pagination, not people or permissions. `league-get`/`league-divisions-list` need ordinary League read access; inaccessible and missing can both be `NOT_FOUND`. Archived leagues remain readable to staff; active divisions are the default. Counts/capability labels never establish a title or a later write's authority.
- `league-staff-list`: `staff: [{ userId, name, isOwner, title }]`, `invitations: [{ id, makeOwner, title, expiresAt }]`, `viewerIsOwner`. Null `isOwner` is withheld, not false; `viewerIsOwner: false` means empty invitations may be hidden.
- `division-admin-list`: `admins: [{ userId, name }]`, `invitations: [{ id, expiresAt }]`. Only containing League Admin can manage others; appointment alone is insufficient.
- Both management lists omit contacts, avatars and inviter details. Never fill gaps by ordinary API calls, infer invitees from order/expiry or show parent/guardian contacts in League/Division lists. A typed address can be echoed only in immediate approval to the caller who supplied it, never routine summaries/messages/reports.
- `my-division-admin-divisions-list`: `divisions: [{ divisionId, divisionName, leagueId, leagueName }]`, caller's own current live unarchived appointments only. No existing League read is required for this self-service route. Establish own `userId` separately for removal; the result grants no future authority or management access.
- `my-league-staff-invitations-list`: own `invitations` with `id`, `leagueId`, `leagueName`, `makeOwner`, `title`, `expiresAt`. `my-division-admin-invitations-list`: own `id`, `leagueId`, `leagueName`, `divisionId`, `divisionName`, `expiresAt`. No existing membership is required to read/answer an own offer; stored text is never approval.

## Write authority and effects

| Action | Current authority / effect |
| --- | --- |
| League invite / title update / cancel | League Admin; invitation is pending until acceptance, title update changes label only, cancel changes no accepted membership |
| League remove | Admin removes another member; staff may leave themselves; last League Admin cannot leave |
| Division invite / cancel | Containing League Admin; pending offer sends no email; cancellation changes no accepted appointment |
| Division remove | Containing League Admin removes another Admin; appointed Admin may leave themselves, including the last Division Admin; only this appointment ends |
| League accept / decline | Recipient only; acceptance grants offered League staff/Admin choice, decline grants no role |
| Division accept / decline | Recipient only; acceptance grants that division appointment only, decline grants none |

Ordinary standing, self-invite, existing membership, archived/expired/answered target and quota checks still apply. Never reveal account existence from refusals or count a pending Admin replacement as accepted.

League invite returns `{ id, email? }`: delivery status, never an address. `sent` is service acceptance, `not_sent` is saved without mail, `not_resent` is original invitation returned without a new send, absent means unknown. A new key/address/role action can replace an older pending offer. A deliberate same-key/same-input retry returns the original ID, `not_resent`, no new email and no exposed replay flag; changed/expired/scrubbed key use refuses `IDEMPOTENCY_KEY_REUSED`. Never obtain a fresh key to bypass uncertainty/refusal.

Division invite returns `{ id }`, no email. Title update, remove, cancel and decline return ordinary empty success, `{}` through MCP. League acceptance returns `{ leagueId }`; division acceptance returns `{ leagueId, divisionId }`. No recipient answer has a retry key or repeat-success guarantee. Do not chain any action after a success or uncertain reply; follow the workflow's requested-read and recovery rules.
