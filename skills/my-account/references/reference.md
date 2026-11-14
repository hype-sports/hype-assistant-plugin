# My-account inputs and boundaries

Use the [skill](../SKILL.md) and [detailed workflows](workflows.md), not this table alone. This reference is not proof that a connection is available, grants access, or has completed an end-to-end journey.

## Tool status

Check the live tool list before use.

| Tools | Status / use |
| --- | --- |
| `my-identity-read`, `my-profile-read` | Read own identity/name; identity also returns `operationCatalogVersion` and `minimumPluginVersion` and alone accepts any positive whole-number `catalogVersion` (see [version check](tool-versions.md)); profile returns save version `updatedAt` |
| `my-preferences-read`, `my-preferences-update` | Read preferences or change the requested time zone |
| `my-profile-update` | Save the requested name with the current profile version |
| `open-password-settings` | Separately registered read-only screen hand-off, not a password-change operation |
| `my-deletion-request` | Start an email-confirmed request, not erasure or confirmation |
| `my-deletion-status-read`, `my-deletion-cancel` | Read status or cancel the pending request |
| `my-sessions-list`, `my-session-revoke`, `my-other-sessions-revoke` | List own devices, sign out one other session or all other sessions |
| `my-assistant-connections-list`, `my-assistant-disconnect` | List own connected assistants, or disconnect exactly one of them (including this assistant). A read-only connection has no disconnect tool |
| `my-login-history-list`, `my-assistant-activity-list` | Read own recorded login events or assistant activity |
| `my-blocked-people-list`, `my-person-blocks-list` | Read own blocked people's current names/IDs or blocked account IDs and Block times |
| `person-block`, `person-unblock` | Change only the signed-in person's own Block of one exact account |
| `my-player-profiles-list` | Select a player profile the person manages |
| `player-profile-erasure-status-read`, `player-profile-erasure-request-read` | Read latest or exact managed-player erase request |
| `player-profile-erasure-request-create`, `player-profile-erasure-request-confirm`, `player-profile-erasure-request-cancel` | App-only in this plugin; do not call these writes |

## Current tool inputs

Route-backed tools use the strict envelope: `catalogVersion: 1` (`my-identity-read` alone accepts any positive whole number; see [version check](tool-versions.md)), plus only the `pathParams`, `query` or `body` the live schema declares. No target account, extra fields or operation replay IDs. A route read with no parameters still needs `catalogVersion`; the password-screen hand-off instead takes `{}`. Check the live schemas before every job.

| Operation ID / registered hand-off name | Read or change | Inputs for this skill |
| --- | --- | --- |
| `my-identity-read` | Read own ID/name and `operationCatalogVersion`/`minimumPluginVersion`; no profile repair | Only `catalogVersion`, any positive whole number for this tool alone (see [version check](tool-versions.md)) |
| `my-profile-read` | Read own ID/name/save version; no profile repair | No parameters beyond the envelope above |
| `my-profile-update` | Change own name | `body.name`, current `body.updatedAt`; name 1–100 characters after trimming. Other schema fields are outside this skill |
| `my-preferences-read` | Read appearance/time zone | No parameters beyond the envelope above |
| `my-preferences-update` | Change own saved time zone | Only `body.timezone` here, an IANA name or null for device behavior |
| `open-password-settings` | Read-only screen hand-off; never changes a password | Strict empty object, no `catalogVersion`; registered separately, not a catalog operation |
| `my-deletion-request` | Start own pending request and send confirmation email; not confirmation/erasure | `body.confirmation: "delete"` only after explicit approval in the person's next message |
| `my-deletion-status-read` | Read own status/timestamps/advisory waiting list | No parameters beyond the envelope above |
| `my-deletion-cancel` | Cancel whatever own request is pending at execution | No parameters beyond the envelope above, no body or confirmation word |
| `my-sessions-list` | Read own device sessions | No parameters beyond the envelope above |
| `my-session-revoke` | Sign out one exact other own session | `pathParams.id`, a UUID returned by the own-session list |
| `my-other-sessions-revoke` | Sign out all own sessions except the assistant's | `query.scope: "others"` |
| `my-login-history-list` | Read up to 50 own login events | No parameters beyond the envelope above |
| `my-assistant-activity-list` | Read own assistant activity from the last 90 days | `query: {}` for the first page; optional `query.limit` from 1–100. Further pages use both exact `beforeAt` and `beforeId` from returned `nextCursor` |
| `my-assistant-connections-list` | Read own connected assistants: `clientId`, `clientName`, `mode`, connection and last-used times; `clientName` may be null | Only the envelope plus an empty `query: {}` |
| `my-assistant-disconnect` | Disconnect exactly one own assistant | `body.clientId`, an exact `clientId` returned by the connections list |
| `my-blocked-people-list` | Read own blocked people's names/IDs, nullable for unavailable accounts | No parameters beyond the envelope above |
| `my-person-blocks-list` | Read own blocked account `profileId` values and `blockedAt` times | No parameters beyond the envelope above |
| `person-block`, `person-unblock` | Block or Unblock one exact identified account as the signed-in person | Only `body.profileId`, the exact account UUID; no target caller ID |
| `my-player-profiles-list` | Read managed-player names/IDs for selection | No parameters beyond the envelope above |
| `player-profile-erasure-status-read` | Read the latest erase request visible to this manager | `pathParams.id`, the exact managed-player profile UUID |
| `player-profile-erasure-request-read` | Read one known exact request, never fall back to latest | `pathParams.id` and `pathParams.requestId`, the exact known profile/request UUID pair |

`my-profile-update` can also accept an own phone change/clear or explicit photo removal, but this skill deliberately covers name only. Do not include those fields in a name save. Its answer and `my-profile-read` expose only ID, name and version; no email, phone or photo. Other appearance settings and role handovers are done in the app; use `notification-settings` for Quiet Hours and notification switches. Supporter-ring changes use `my-support`.

## Availability and exclusions

- Account tools remain subject to the live connection's admission and access checks.
- The password hand-off returns the app's own Settings link alongside permitted route tools. Only the person opens it.
- Device-bound account cleanup and password submission are app-only, not missing assistant tools to invent or direct routes to call. Passwords never enter the assistant. Own-account deletion confirmation likewise stays with the person's separate email-linked confirmation button; this skill never handles its link/token or executes erasure.
- Own-account deletion is caller-only. Starting a request requires leaving or handing over every Team staff, League staff, Division Admin, Club Admin and Tournament Admin role. The assistant's held-role refusal `ACCOUNT_HAS_ROLES` carries the complete list in `details.blockers`; it is missing only when the server could not read it. Explain before an app handoff: its **Delete account** action is a real request; if roles remain, the attempt is refused and lists every role, but if none remain it starts the request and sends the confirmation email. Never reconstruct the list. The status tool's advisory `waitingFor` list covers Team, League, Club and Tournament ownership only, not all held-role blockers. Missing or unreadable is unknown; empty is not erasure clearance.
- Managed-player erasure is separate from own-account deletion. Only a current managing parent/guardian may use it; viewer, follower, friend, coach or staff access alone is not enough. Unscheduled requests remain tied to the original requester, their same open management stint and unchanged captured links. Confirmation requires that original requester/stint. Scheduled requests can be read or, before due and subject to server checks, canceled by another current manager. `canCancel` is display information, not approval or authority.
- Continue only already-reviewed independent changes after clear success or a confirmed refusal. On uncertainty, say the write may have happened, stop writes and inspect only the affected item once through a supported authorized read; if unavailable, keep it unknown rather than scan wider lists. No automatic retry. Player-erasure writes remain in the app.

## Data handling

The plugin adds no service or credential store. Keep only the requested own-account, history, connected-assistant names, block-list or managed-player request details in the private conversation. Do not publish them or write them into this repository; do not retain credentials or confirmation links. The assistant client's handling applies to the conversation.
