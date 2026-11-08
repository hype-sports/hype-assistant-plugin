# Players & Families tool reference

The live connection's descriptions and schemas always win. These are catalog operation ids; discover full prefixed names on that connection. Hype's active sport catalog decides supported codes; sport-detail rules alone do not define that catalog.

## Current tools used by this skill

All currently take `catalogVersion: 1`. “None” means omit that section, not send null. UUIDs must identify the exact saved record from an authorized result or trustworthy known request; never generate or guess one. No caller, email-recipient identity, method, headers or token overrides.

| Operation | pathParams | Other inputs / safe result |
| --- | --- | --- |
| `my-player-profiles-list` | None | No body/query; `players` with `id`, `firstName`, `lastName` only |
| `player-profile-read` | `{ id: playerProfileId }` | No body/query; name and `sports: [{ id, sport, details }]` only |
| `player-profile-teams-list` | `{ id: playerProfileId }` | No body/query; historical team references, not current roster membership |
| `player-profile-registrations-list` | `{ id: playerProfileId }` | No body/query; linked/linkable registrations and read-time rights; current profile manager only |
| `my-guardian-seasons-list` | None | Optional live-schema team filter; preserve history/order/nulls, not permission to open a team |
| `my-parent-guardian-invitations-list` | None | No body/query; incoming profile offers with first names, nullable inviter name and expiry |
| `my-team-guardian-invitations-list` | None | No body/query; incoming team offers with team name, player first name, nullable sender and expiry |
| `my-league-guardian-invitations-list` | None | No body/query; invitation IDs only, no player/league/sender facts |
| `my-guardian-requests-list` | None | No body/query; own sent requests only, no team/entry IDs; statuses pending, accepted, declined, cancelled, expired; closedBy you/team/null |
| `owner-invitation-accept` | `{ id: invitationId }` | No body/query; returns `{ playerProfileId }`; profile management, not team/league acceptance |
| `owner-invitation-decline` | `{ id: invitationId }` | No body/query; returns `{}`; refuses profile-management offer only |
| `guardian-invitation-decline` | `{ id: invitationId }` | No body/query; returns `{}`; refuses team parent/guardian offer only |
| `league-guardian-invitation-accept` | `{ id: invitationId }` | No body/query; returns `{ guardianId }`; no profile creation/link |
| `league-guardian-invitation-decline` | `{ id: invitationId }` | No body/query; returns `{}`; no access granted or removed |
| `league-guardian-invitation-registration-read` | `{ id: acceptedInvitationId }` | No body/query; current player first name, league name, nullable division name, only after own acceptance with continuing independent standing |
| `league-player-profile-link` | `{ id: leagueId, playerId: leaguePlayerId }` | `body: { playerProfileId }`; returns `{ leaguePlayerId, playerProfileId }` |
| `player-profile-sport-add` | `{ id: playerProfileId }` | `body: { sport, details? }`; map and confirm a lowercase code from SKILL.md, not a free-text name; `other` has its own `position` detail; follow the live input schema; returns authoritative sport-row `{ id }` |
| `player-profile-sport-update` | `{ id: playerProfileId, sportId }` | `body: { details }`, COMPLETE replacement for stored sport; returns `{}` |
| `player-profile-sport-remove` | `{ id: playerProfileId, sportId }` | No body/query; returns `{}`, removes sport row only |
| `my-home-entities-list` | None | `query: {}` or optional `search` and `includeArchived` strings (only `"true"` includes archived records); no body; returns `entities` with `id`, `type`, optional `parentLeagueId`/`parentDivisionId` and `userRoles`, not registration IDs; roles are information, not permission |
| `division-players-lookup` | `{ id: divisionId }` | `query: {}` or live-schema name/page filters; limited identities/status and page metadata |
| `league-player-guardian-invitations-list` | `{ id: leagueId, playerId: leaguePlayerId }` | No body/query; pending registration offers, address always withheld as `inviteeEmail: null` |
| `league-player-guardian-invitation-create` | `{ id: leagueId, playerId: leaguePlayerId }` | `body: { email }`, supplied for this send, valid trimmed/lowercase address ≤254 characters; add `idempotencyKey` from `request-key-new` only when the live schema has that field, otherwise send no key and don't call the key tool; follow the [workflow](../SKILL.md#4-execute-once-stop-safely); returns `{ id, email: "sent" or "not_sent" }` |
| `league-guardian-invitation-cancel` | `{ id: invitationId }` | No body/query; current same-league staff; `{}` cancels pending offer, not accepted standing |
| `guardian-invitation-cancel` | `{ id: invitationId }` | No body/query; current permitted same-team decider; `{}` cancels pending offer, not accepted standing |

These are not the whole Players catalog. Profile creation, division registration creation, friend cards, profile-match hints and profile-offer cancellation are outside this skill's workflows; do not improvise them as workarounds.

## Sport detail fields

Use only requested fields for the confirmed sport. Omit `details` on add when no details are requested. Treat update `details` as the complete replacement, not a patch; show retained and cleared fields before approval. Refuse to guess fields from the tool's open-object schema. Stop on validation refusal.

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

Trim text positions to 1–30 UTF-16 units; limit position lists to 10 entries. Confirm `L` as left, `R` as right and `S` as switch. Do not invent detail rules for a newer catalog code; use Hype's app when the live schema and this reference cannot safely describe the requested change.

## Access and effects to keep distinct

- A profile manager can read only their allowed profile facts; readable staff access does not permit managing its sports. Team or registration parent/guardian standing alone does not grant full-profile access. There is no manager directory in current profile output.
- Lookup is an active-division name search for permitted league staff, exact-division team staff or a scoped Division Admin, not a complete player directory. No birth dates, contacts or evaluation numbers are exposed. Page metadata limits completeness claims.
- Invitations addressed to the caller require their current confirmed sign-in email; supplying an address or changing caller identity is not allowed. Expired/answered/hidden invitations may be absent from incoming lists. An exact known still-pending offer may be declined even past its deadline; a persisted expired or answered state refuses. Cancelled offers refuse as revoked; terminal states are never repeat success.
- Profile acceptance grants management plus eligible linked-record rights and inherited family-audience/chat effects, preserving existing removal limits. League acceptance grants registration parent/guardian access and notifications only. Link requires BOTH current profile management and existing independent registration standing; it immediately extends registration access to other profile managers. It can attach eligible existing draft team spots, never add team membership. Pending invitation, accepted access and profile link are three different states.
- League staff invite sends an in-app notice and attempts email; same-address pending replacement is a new send, not a harmless retry. Returned `email` is delivery status, never an address. `not_sent` does not undo the offer. Contact-free pending lists cannot establish an address-specific duplicate or identify the invitee.
- Coach cancellation needs permitted same-team standing, not any league role. Creating-league authority is limited to the unarchived league still co-owning the team; a merely joined league is not enough. No team staff invitation discovery tool is supplied here.
- Sports updates replace, not merge, details and have no version guard. Use read/receipt sport-row IDs. Duplicate add, missing remove and repeated answer/cancel refusals are not replay success.
- Ordinary empty 204 write success is represented as strict `{}` by MCP; it is not a missing reply. Lost/malformed replies differ: stop without retry. A later current read informs a new decision but cannot prove a past dispatched write happened or did not happen. Ask for that read first; never quietly chain it. Sports recovery requires inspection in the app before another write.
- Reads can still write private activity/rate bookkeeping; do not promise zero internal activity. Every admitted MCP POST, discovery included, shares the 60-per-rolling-minute account bucket. Respect returned wait timing and obtain a separate request before resuming.

## Coming soon — do not call or guess names

These capabilities are not available yet and remain outside this workflow. Re-check live tools and schemas before extending this skill; a proposed tool name is not proof of availability.

- Division and league player lists
- Who manages a player
- Read one player of a division
- Resend an invitation
- Read one league invitation before acceptance
- Accept a team parent/guardian invitation
- Coach reads incoming join requests
- Coach approves or declines join requests

Inviting another parent/guardian to a personal profile also has no supported create tool here. Use Hype's app; no substitute email, staff invitation or new connection. Read the [workflow and verification limits](../SKILL.md) before making readiness claims.
