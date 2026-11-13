# League staff tool reference

Live tool schemas/descriptions always win. Find full prefixed names; these are catalog ids, not guessed client names.

## Tool availability

Check the live tool list before use; this reference is not proof of availability or access.

| Tools | Status / use |
| --- | --- |
| `league-get`, `league-divisions-list`, `league-staff-list` | resolve league/divisions and read staff |
| `division-admin-list` | read the selected division's Admins/invitations |
| `league-staff-invite` | invite a Commissioner, attempts email |
| `league-staff-invitation-cancel`, `league-staff-remove` | cancel one offer / remove one membership |
| `division-admin-invite` | invite a Division Admin, NO email |
| `division-admin-invitation-cancel`, `division-admin-remove` | cancel one offer / end one appointment |
| `my-identity-read` | optional, resolve the caller's own identity |
| `league-search` | optional, find league basics by name, not people or permissions |

## Inputs

All these MCP tools currently require `catalogVersion: 1`. Fields below are nested under `pathParams`, `query` or `body` exactly as shown by the live schema. Do not send absent sections as null or add an `opId`/retry key, except `league-staff-invite`'s required `idempotencyKey`. Every ID below is an exact UUID from a trustworthy request or authorized result, never generated for an existing record.

| Operation | pathParams | Other inputs |
| --- | --- | --- |
| `league-search` | None | `query: { name }`; optional `page` (integer ≥1, default 1), `limit` (1–50, default 20); no body |
| `league-get` | `{ id: leagueId }` | No body/query |
| `league-divisions-list` | `{ id: leagueId }` | `query: {}` for active divisions; `archived: "true"` inside query only for a requested archived read |
| `league-staff-list` | `{ id: leagueId }` | No body/query |
| `division-admin-list` | `{ id: divisionId }` | No body/query |
| `league-staff-invite` | `{ id: leagueId }` | `body: { email, idempotencyKey, makeOwner: false, title: "commissioner" }` |
| `division-admin-invite` | `{ id: divisionId }` | `body: { email }` |
| `league-staff-remove` | `{ id: leagueId, userId }` | No body/query |
| `division-admin-remove` | `{ id: divisionId, userId }` | No body/query |
| `league-staff-invitation-cancel` | `{ id: invitationId }` | No body/query |
| `division-admin-invitation-cancel` | `{ id: invitationId }` | No body/query |

Invite schemas trim the supplied address, require a valid email and limit it to 254 characters. Do not infer an address or probe whether it is registered. This skill invites Commissioners only at League level, not new League Admins; keep `makeOwner: false`. `commissioner` is the lowercase wire value; display **Commissioner**.

## Authorized reads and outputs

- Optional `league-search` takes the supplied league name (trimmed, 1–100 characters), returns `results` with league basics/IDs and `pagination`, and grants no staff visibility or authority. Ask before any further page; never interpret a partial page as a complete directory. Resolve ambiguous matches with the person before the protected reads. This skill requires those League reads; a Division Admin without League read access must use the ordinary app, including for self-leave.

- `league-get` and `league-divisions-list`: current League staff and its coaches only; inaccessible and missing leagues both return `NOT_FOUND`. Archived leagues remain readable to staff. Divisions are active by default, not an all-history census. Bare-array route results are wrapped by MCP; follow the actual output schema. Counts and capability labels do not establish a staff title or authority for a later write.
- `league-staff-list`: `staff: [{ userId, name, isOwner, title }]`, `invitations: [{ id, makeOwner, title, expiresAt }]`, `viewerIsOwner`. Only current League Admins see pending invitations. Null `isOwner` is withheld, not false. `isOwner` and `makeOwner` mean League Admin, independent of the Commissioner title.
- `division-admin-list`: current containing-League owner only; `admins: [{ userId, name }]`, `invitations: [{ id, expiresAt }]`. Being a Commissioner or an appointed Division Admin alone does not permit this management list. Unauthorized and missing divisions retain distinct refusals; explain only what the returned refusal safely establishes.
- Both MCP management lists omit addresses, phone numbers, avatars and inviter details even where ordinary app contracts contain them. Never fetch the ordinary API to fill these gaps. An invitation's ID, role or expiry cannot identify its address. Only a reliable exact-offer mapping already supplied/confirmed by the person or an invite receipt permits targeting; otherwise hand off to the app.
- League invite returns `{ id, email? }`; **`email` is a delivery status**, not an address: `sent` = accepted by mail service, `not_sent` = created but email not sent, absent = unknown delivery status. Division invite returns `{ id }`, with no email transport.
- Remove/cancel returns ordinary empty 204, represented as `{}` by MCP. This is success, not a missing response needing retry. Lost or malformed replies are different: stop and hand off.

## Authority and refusal boundaries

| Action | Current authority / effect |
| --- | --- |
| League invite | League Admin only; pending offer, attempts email, no access before acceptance |
| League remove | League Admin removes another member; any staff may leave themselves; last League Admin cannot leave |
| League cancel | League Admin only; exact pending offer; no accepted membership changed |
| Division invite | Containing League owner only; pending offer, no email or appointment before acceptance |
| Division remove | Containing League owner removes another Admin; appointed Admin may leave themselves, including the last Division Admin; only this appointment ends |
| Division cancel | Containing League owner only; pending, unexpired exact offer; no accepted appointment changed |

Standing, self-invite, existing membership, quota, target and other ordinary checks remain Hype's decisions. Do not turn a refusal into an account-existence claim. Prior reads never grant future rights. Never remove the last League Admin or treat a pending invitation as an accepted replacement.

`league-staff-invite` requires an `idempotencyKey`. Get a fresh key from `request-key-new` for each new invite and send it as `idempotencyKey`; never hand-type one. If that tool is missing or errors, stop without inviting. Reuse the SAME key, unchanged, only when the person explicitly asks to retry that same invite after an unclear outcome; never retry automatically. A different email or roles needs a new key. The same key and inputs return the original `id` with `email: "not_resent"` and send no new email; the same key with different inputs returns `IDEMPOTENCY_KEY_REUSED`. A new key, or a Division Admin invite (no key), to the same normalized address replaces the pending offer with a new ID, potentially another email for League staff. After `WRITE_OUTCOME_UNKNOWN`, never repeat automatically, read, chain or compensate: ask the person to check the league's Staff tab in the ordinary app. A later requested list is current state only, not proof of the earlier email/address outcome; any later change needs a new exact review and approval.
