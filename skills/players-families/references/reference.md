# Players & Families tool reference

The live connection's descriptions and schemas win. These are operation IDs; discover full prefixed names before use. These route tools currently require `catalogVersion: 1`. **Exception: `request-key-new` takes only `{}`**, with no catalogVersion. “None” means omit that section, not send null. Required empty `query`/`body` objects are shown explicitly. Use exact saved IDs from authorized results or a trustworthy known request, never generated/guessed IDs or another record type. Supply no caller, credential, header or recipient-identity overrides.

## Parent/guardian tools

| Operation | pathParams | Other inputs / result and limit |
| --- | --- | --- |
| `request-key-new` | None | Input `{}` only; returns `{key}`. One fresh key per intended keyed change, never a new key for a retry; grants no access |
| `my-player-profiles-list` | None | No body/query; `players` with `id`, `firstName`, `lastName` only |
| `player-profile-read` | `{id: playerProfileId}` | No body/query; `id`, name and `sports: [{id, sport, details}]` only, no saved contacts or contact IDs |
| `player-profile-create` | None | Required `body: {firstName, lastName, dateOfBirth}`; optional profile fields, `sports` and `emergencyContacts` per live schema; returns `{id}`. Check managed list first; parent/guardian creates as themselves |
| `player-profile-update` | `{id: playerProfileId}` | Required nonempty `body`; send only requested `firstName`, `lastName`, `currentSchool`, `currentGrade`, `graduationYear`, `bio`, `city`, `state`. City/state together, both values or both null. **Never send `emergencyContacts[]` or `sports[]`: they replace whole lists.** No birth date/photos in this workflow. Returns `{}`; no revision protection |
| `emergency-contact-add` | `{id: playerProfileId}` | `body: {name, phone, email?, relationship?}`; name 1–100 trimmed characters, phone 7–25 trimmed characters and accepted by Hype's phone validation; optional nullable valid email (max 254) and relationship (max 50). Returns authoritative contact `{id}` |
| `emergency-contact-update` | `{id: playerProfileId, contactId}` | Required nonempty `body` with at least one of `name`, `phone`, `email`, `relationship`; same validation as add. Omitted fields unchanged; null email/relationship clears. Returns `{}`; never replaces other contacts |
| `emergency-contact-delete-check` | `{id: playerProfileId, contactId}` | No body/query; current managing parent/guardian only. Saves a short-lived confirmation but deletes nothing. Returns `{name, relationship, confirmationId, expiresAt}`, no phone/email. Show the name, nullable relationship, target player and permanent-deletion effect in the one shared review before yes |
| `emergency-contact-delete` | `{id: playerProfileId, contactId}` | Required `body: {confirmationId}` from that exact read-back, no query. After the shared review and person's yes, call once with the same profile/contact IDs; never reuse, invent or transfer the confirmation ID. Permanently deletes ONE contact, not the player; returns `{}`. Lasts until `expiresAt` (about five minutes); a newer check or an edit to the contact cancels it, and any of these answers not found. No automatic retry or confirmation renewal |
| `player-profile-owners-read` | `{id: playerProfileId}` | No body/query; `{owners: [{name, isYou, since}], invitations: [{id, createdAt, expiresAt}]}`. Current managers only, no contacts/user IDs; pending unexpired offers only |
| `owner-invitation-create` | `{id: playerProfileId}` | `body: {email, idempotencyKey}`; directly supplied trimmed lowercase valid address, max 254; current manager only. New key replaces pending same-address offer. Returns `{id, email: "sent" \| "not_sent" \| "not_resent"}` |
| `owner-invitation-resend` | `{id: invitationId}` | `body: {idempotencyKey}`; current profile manager, exact known offer. Returns `{email: "sent" \| "not_sent" \| "not_resent"}` |
| `owner-invitation-cancel` | `{id: invitationId}` | No body/query; current manager may cancel another sender's pending offer. Returns `{}`; no accepted-manager removal or email |
| `player-profile-leave` | `{id: playerProfileId}` | No body/query; `{hidden: boolean}`. Ends only caller's management and their pending offers; no team departure/deletion. Last manager's departure hides the profile from everyone and cannot be undone in the app |
| `player-profile-teams-list` | `{id: playerProfileId}` | No body/query; historical references, not current membership or team-opening rights |
| `player-profile-registrations-list` | `{id: playerProfileId}` | No body/query; linked/linkable registrations and read-time rights; current profile manager only |
| `my-guardian-seasons-list` | None | Required `query: {}` or optional live-schema team filter; no body. History/order/nulls are not permission to open a team |
| `my-parent-guardian-invitations-list` | None | No body/query; incoming profile offers with first names, nullable inviter name and expiry |
| `my-team-guardian-invitations-list` | None | No body/query; incoming team offers with team name, player first name, nullable sender and expiry |
| `my-league-guardian-invitations-list` | None | No body/query; invitation IDs only, no player/league/sender labels |
| `my-guardian-requests-list` | None | No body/query; own sent requests, not a staff queue. Preserve order, duplicates, labels and nulls; statuses pending/accepted/declined/cancelled/expired, closedBy you/team/null |
| `my-unlinked-guardian-spots-list` | None | No body/query/person selector; `{spots: [{rosterEntryId, teamId, teamName, playerFirstName, registrationId, leagueId}]}`; registrationId/leagueId nullable. Own live current-season spots only. Set registrationId means link through that registration; null means the spot itself. No linking authority or staff queue; empty is not no history |
| `team-guardian-request-create` | `{id: teamId}` | `body: {entryIds, profiles?}`; 1–10 distinct live roster entry IDs. Optional `profiles: [{entryId, playerProfileId}]`, one managed profile per selected entry, each profile once. No private-link field. Returns `{askGroupId}`, not approval |
| `owner-invitation-accept` | `{id: invitationId}` | No body/query; `{playerProfileId}`; profile management plus eligible linked rights, not team/league acceptance |
| `owner-invitation-decline` | `{id: invitationId}` | No body/query; `{}`; refuses only this profile offer |
| `guardian-invitation-accept` | `{id: invitationId}` | Required `body: {}` or `{playerProfileId}` for optional linking explicitly included in the complete review; no query. `{guardianId, linkedProfileId}`; linkedProfileId is null without a supplied profile |
| `guardian-invitation-decline` | `{id: invitationId}` | No body/query; `{}`; refuses team offer, removes no accepted access/link |
| `league-guardian-invitation-accept` | `{id: invitationId}` | No body/query; `{guardianId}`; registration access/notifications, no profile creation/link |
| `league-guardian-invitation-decline` | `{id: invitationId}` | No body/query; `{}`; refuses only this offer |
| `league-guardian-invitation-registration-read` | `{id: acceptedInvitationId}` | No body/query; current player first name, league name and nullable division name only after own acceptance with continuing independent guardian standing |
| `league-player-profile-link` | `{id: leagueId, playerId: leaguePlayerId}` | `body: {playerProfileId}`; caller must manage profile AND already be a registration parent/guardian. Returns `{leaguePlayerId, playerProfileId, registrationLinked}`; false is still successful repair, not an undo token |
| `player-profile-sport-add` | `{id: playerProfileId}` | `body: {sport, details?}`; confirmed lowercase catalog code and allowed sport details; authoritative sport-row `{id}` |
| `player-profile-sport-update` | `{id: playerProfileId, sportId}` | `body: {details}`; COMPLETE replacement of stored sport details, omitted fields cleared; `{}` |
| `player-profile-sport-remove` | `{id: playerProfileId, sportId}` | No body/query; `{}` removes only that sport row |

For profile creation, names are 1–50 trimmed characters and birth date is the supplied valid `YYYY-MM-DD` date Hype accepts, not an inferred age. Include optional fields only when requested; city/state go together. Optional creation contacts require each `name` and `phone`; optional sports require each `sport` and the matching detail rules below. Never guess stored facts, fill optional fields with defaults, or invent photo paths. Creation does not register a player or add a team spot.

A contact ID from a confirmed add is authoritative only for that exact contact/profile. A name or phone is not an ID. The profile read cannot discover or review existing contacts: hand off unidentified edits to the app. Never bulk-replace or wipe contacts, or use team-staff contacts as a workaround. Deleting one known contact uses the read-back and delete pair above under the same shared review and yes.

## Coach / team staff tools

| Operation | pathParams | Other inputs / result and limit |
| --- | --- | --- |
| `team-guardian-requests-list` | `{id: teamId}` | Required `query: {}`; no body. Pending asks only: `{requests: [{id, playerName, askerName, status, isSelfAsk, askedByYou, askerMatchesEntryEmail}]}`. **No askGroupId or outgoing invitations**. Current team-decider access |
| `guardian-request-approve` | `{id: requestId}` | No body/query; `{requestId, outcome}` for one selected player row; that person's other rows stay waiting. Show player/asker names, never the request ID. `already` grants no new access; do not invent a guardian ID |
| `guardian-request-decline` | `{id: requestId}` | No body/query; `{}` retains the request as declined, tells asker once without coach name; no email or access grant |
| `guardian-request-group-approve` | `{askGroupId}` | No body/query; `{results: [{requestId, outcome}]}` only. Independently known exact whole group and all waiting players required; not discoverable from the staff queue |
| `guardian-request-group-decline` | `{askGroupId}` | No body/query; `{}` retains waiting requests as declined, answered players unchanged; no access grant/deletion/email |
| `guardian-invitation-resend` | `{id: invitationId}` | **No body/query/key**; `{email: "sent" \| "not_sent"}`. Current team authority; recipient or profile manager alone insufficient |
| `guardian-invitation-cancel` | `{id: invitationId}` | No body/query; `{}` ends pending offer only, no accepted-parent removal/email. Current permitted same-team staff/owner or permitted creating-co-owning unarchived league authority |

Use `askedByYou` to identify the caller's own pending ask. `isSelfAsk` means self-approved, not “this pending ask is yours.” `askerMatchesEntryEmail` compares verified sign-in email with the held parent email; it exposes no address and is not approval or identity proof.

### Whole request groups

Never substitute an individual request ID for `askGroupId`, infer groups from names or derive staff authority from the asker's outgoing list. For a separately supplied trustworthy exact group, show the asker, team and **every waiting player exactly as the app shows them**, state when Hype cannot confirm those details here, explain effects, and get a yes in the person's next message. If anything is missing, use the list-first individual flow or the app, not a guessed group.

Group approval grants eligible waiting players' access, with possible profile-link/audience/notices. Preserve all `results` and order; one refusal does not stop other players. Outcomes include `approved`, `already`, `PLAYER_NOT_ON_ROSTER`, `INVITATION_EXPIRED`, `INVITATION_REVOKED`, `ALREADY_RESPONDED`. Empty/missing results are not whole-group success. Decline tells the asker once without naming the coach and allows a later ask. Neither action sends email. No automatic follow-up read or retry.

## League / division tools and shared discovery

| Operation | pathParams | Other inputs / result and limit |
| --- | --- | --- |
| `my-home-entities-list` | None | Required `query: {}` or live-schema filters; no body. Start here to find the requested team; exact IDs, types, parent scope and userRoles guide selection, not authorization. Home IDs are not registrations |
| `team-search` | None | Required `query` with supplied-name/live-schema filters; no body. If the team is absent from Home, show one requested public search page and let the person choose the exact match. Hidden/archived teams excluded; no new access or automatic next page |
| `team-roster-list` | `{id: teamId}` | Required `query: {}` for current roster; no body. Select `role: player` rows and use their `id` as entryId, not person/profile IDs. Facts are tier-filtered; no contacts/photos/profile IDs. If those facts cannot identify the right child, use the app; never guess |
| `division-players-lookup` | `{id: divisionId}` | Required `query: {}` or live-schema filters; active-division narrow lookup and page metadata, not a complete directory |
| `division-players-list` | `{id: divisionId}` | Required `query: {}` or live-schema search/page/pageSize/archived filters; default page 1, size 25, max 100. `archived: "only"` requires commissioner |
| `league-players-list` | `{id: leagueId}` | Required `query: {}` or live-schema search/page/pageSize/divisionId filters; same pagination, no archived filter |
| `division-player-read` | `{id: registrationId}` | Required `query: {divisionId}`; optional `archived: "only"` for commissioner. Registration identity/status; commissioners may also receive joined guardian `{userId, name}` rows. Show guardian names only, never user IDs. Missing guardians stay unknown |
| `division-registration-read` | `{id: divisionId, registrationId}` | Required `query: {}`; no body. Accepted Division Admin in this exact live division only; identity and read-only viewer capabilities, no birth dates/contacts/evaluation details |
| `league-player-guardian-remove` | `{id: leagueId, playerId: leaguePlayerId, userId}` | No body/query; current league staff removing another adult, or permitted self-leave. Adult `userId` comes only from commissioner-view `division-player-read`. Follow the [removal workflow](../SKILL.md) for exact scope, notices, lasting removal, archive refusals and shared review/next-message yes. Links end, history and independent profile/team rights stay; no player/profile deletion. Returns `{}`. Exception to lost-answer re-reading: no automatic read or retry; keep unknown and use app inspection |
| `league-guardian-invitation-read` | `{id: invitationId}` | No body/query; `{invitation: {id, status, expiresAt}}` only, even for staff. No target/sender/recipient labels or new authority |
| `league-player-guardian-invitations-list` | `{id: leagueId, playerId: leaguePlayerId}` | No body/query; pending registration offers, `inviteeEmail: null`; cannot identify recipient by address |
| `league-guardian-invitation-cancel` | `{id: invitationId}` | No body/query; current same-league staff; `{}` cancels pending offer, leaves accepted standing alone |
| `league-guardian-invitation-resend` | `{id: invitationId}` | `body: {idempotencyKey}` from request-key-new; current league staff, exact identified offer. `{email: "sent" \| "not_sent" \| "unknown", replayed}`. If the first email result is not known from this conversation, treat it as unknown; the invitation reads do not supply it. Explain that the first email may have gone out and another could arrive twice, then ask for yes |

Player lists return `{items, page, pageSize, total}` with registration IDs, first/last names, division labels and status only. No contacts, birth dates, photos or evaluation details. A search may match fields not returned; do not infer those fields. Empty/partial pages prove no census and grant no access; no automatic traversal or enrichment. League staff status does not substitute for the exact Division Admin appointment required by `division-registration-read`.

Create league parent invitations through [league-setup](../../league-setup/SKILL.md#5-register-players-invite-parentsguardians) or [invite-families](../../invite-families/SKILL.md), not a duplicate send workflow here. Those skills cover supplied-address checks, required `request-key-new` keys, shared list approval, replacement/replay and recipient ordering. Imports preserve both parents; include requested invitations explicitly in the same review, never infer consent for omitted sends.

## Team acceptance with a profile

Without a profile, accepting grants only the recipient's parent/guardian access to that player on that team and sends in-app notices. To add the optional profile, select it from the caller's managed list and explicitly review all these effects before yes:

- Share the profile with the team and its other parents/guardians.
- Add its other current managers as that player's team parents/guardians unless a prior removal still blocks that grant.
- Extend an earlier coach removal to the removed adult's other covered roster spots, ending their access and cancelling waiting requests/invitations there; a later coach-approved grant remains.
- Notify the other profile managers and the team owners/titled coaches of the link, and the player's other parents/guardians and team owners/titled coaches of acceptance.

If the optional link refuses, the invitation stays waiting. Never infer identity/link eligibility from matching names. Acceptance, profile management and registration linking are separate scopes.

## Invitation keys and delivery

For `owner-invitation-create`, `owner-invitation-resend` and `league-guardian-invitation-resend`, get a fresh key from `request-key-new` **only for a new approved action**. Keep the original key and exact inputs after an unclear result; never mint a replacement key to recover it. A person-requested unchanged retry needs a fresh complete review of the original exact request and its email effects and a yes in the person's next message. `IDEMPOTENCY_KEY_REUSED` is a stop, not permission to change the key. Team parent/guardian resend takes no key and has no replay protection.

- Profile create/resend replay returns `not_resent`, sends nothing new and proves no earlier delivery. Changed, foreign, expired or scrubbed keys refuse.
- League resend replay returns the first email outcome with `replayed: true`, no new email. If this conversation records the first result, offer a new Resend for `not_sent` or `unknown`, not a known `sent`. The pending-invitation list and exact-invitation read return no email outcome. If it is not known from this conversation, treat delivery as unknown: say the first email may have gone out, a resend could arrive twice, and ask whether the person wants another attempt. Wait for their yes in the person's next message; never infer delivery from an invitation row.
- Resend renews the pending invitation and attempts email; a failed email does not undo that saved change. Team resend makes the caller its sender.
- Team/league resend may require the original sender for untyped, non-draft invitations. On `INVITATION_SENDER_REQUIRED`, explain that the sender must resend or a current decider can request a new invitation; never substitute a new send automatically.
- `sent` means service acceptance, not mailbox delivery, acceptance or access. `not_sent` leaves the offer saved. `unknown` may already have reached the recipient. Never retry or resend as an automatic repair.
- Cancellation/decline keeps the offer record and changes no accepted rights. Expired/answered/hidden offers may be absent from lists; disappearance is never a receipt for a lost write. A pending invitation grants no player/profile facts or identity proof.

## Sport detail fields

Map and confirm lowercase catalog codes: `baseball`, `softball`, `basketball`, `cheerleading`, `football`, `soccer`, `hockey`, `volleyball`, `lacrosse`, `other`. Hype's active catalog decides acceptance. Clarify ambiguous sport words; never use a free-text name as a code. `other` displays as Other and does not save a custom sport name; its `position` is a detail, not a name workaround.

Use only requested fields for the confirmed sport. Omit `details` on add when none were requested. Treat update `details` as the complete replacement: review retained and cleared fields before yes. Never infer validation from an open-object schema.

| Sport code | Optional detail fields and values |
| --- | --- |
| `baseball`, `softball` | `bats`: `L`/`R`/`S`; `throws`: `L`/`R`; `positions`: text list |
| `basketball` | `primaryPosition`, `secondaryPosition`: `PG`/`SG`/`SF`/`PF`/`C` |
| `football` | `primaryPosition`, `secondaryPosition`: text |
| `soccer` | `dominantFoot`: `L`/`R`; `positions`: text list |
| `hockey` | `shoots`: `L`/`R`; `positions`: text list |
| `volleyball` | `primaryPosition`: text |
| `lacrosse` | `positions`: text list |
| `other` | `position`: text; not a custom sport name |
| `cheerleading` | No detail fields; omit add details and do not attempt a details update |

Trim text positions to 1–30 UTF-16 units; limit lists to 10 entries. Confirm L as left, R as right, S as switch. Use the app when a newer code's details cannot be safely described. Duplicate adds or missing rows are refusals, not replay success. No revision protection: after an unclear sports change, say it may have happened, stop writes and inspect only the affected sports item once if a supported authorized read exists; otherwise keep it unknown and use the app, with no automatic retry.

## Boundaries and verification

Erasing a player or their data stays in the **Hype app**, because it cannot be undone and the app walks through it. The assistant does not invoke those tools here; they are not “unavailable.” Do not substitute leaving, unlinking, registration deletion or another family's profile work. Withdraw a mistaken team request in the app: `guardian-request-withdraw` is deliberately outside this skill. Unrelated friend-card, removal, archive and direct team-spot linking workflows are not added by this guide.

Ordinary empty 204 write success is strict `{}`; a lost/malformed reply is different and may follow a saved change. Stop writes without automatic retry or polling. Read only the affected item once through a supported authorized item read and report its state; if unavailable, keep it unknown and use the app rather than scan broader lists; current state cannot settle the lost call's historical outcome. Reads can still write private activity/rate bookkeeping; never promise zero internal activity. Every admitted MCP POST shares the 60-per-rolling-minute account bucket; wait timing reserves no slot.

Keep the [workflow's confirmation and recovery rules](../SKILL.md).
