# My-account inputs and boundaries

Use the [skill](../SKILL.md) and [detailed workflows](workflows.md), not this table alone. This reference is not proof that a connection is available, grants access, or has completed an end-to-end journey.

## Tool status

Check the live tool list before use.

| Tools | Status / use |
| --- | --- |
| `my-identity-read`, `my-profile-read` | Read own identity/name, with save version `updatedAt` on the profile read |
| `my-preferences-read`, `my-preferences-update` | Read preferences or change the requested time zone |
| `my-profile-update` | Save the requested name with the current profile version |
| `open-password-settings` | Separately registered read-only screen hand-off, not a password-change operation |
| `my-deletion-request` | Start an email-confirmed request, not erasure or confirmation |
| `my-deletion-status-read`, `my-deletion-cancel` | Read status or cancel the pending request |
| `my-sessions-list`, `my-session-revoke`, `my-other-sessions-revoke` | List own devices, sign out one other session or all other sessions |

## Current tool inputs

Route-backed tools use the strict envelope: `catalogVersion: 1`, plus only the `pathParams`, `query` or `body` the live schema declares. No target account, extra fields or operation replay IDs. A route read with no parameters still needs `catalogVersion`; the password-screen hand-off instead takes `{}`. Check the live schemas before every job.

| Operation ID / registered hand-off name | Read or change | Inputs for this skill |
| --- | --- | --- |
| `my-identity-read` | Read own ID/name; no profile repair | No parameters beyond the envelope above |
| `my-profile-read` | Read own ID/name/save version; no profile repair | No parameters beyond the envelope above |
| `my-profile-update` | Change own name | `body.name`, current `body.updatedAt`; name 1–100 characters after trimming. Other schema fields are outside this skill |
| `my-preferences-read` | Read appearance/time zone | No parameters beyond the envelope above |
| `my-preferences-update` | Change own saved time zone | Only `body.timezone` here, an IANA name or null for device behavior |
| `open-password-settings` | Read-only screen hand-off; never changes a password | Strict empty object, no `catalogVersion`; registered separately, not a catalog operation |
| `my-deletion-request` | Start own pending request and send confirmation email; not confirmation/erasure | `body.confirmation: "delete"` only after later-turn explicit approval |
| `my-deletion-status-read` | Read own status/timestamps/advisory waiting list | No parameters beyond the envelope above |
| `my-deletion-cancel` | Cancel whatever own request is pending at execution | No parameters beyond the envelope above, no body or confirmation word |
| `my-sessions-list` | Read own device sessions | No parameters beyond the envelope above |
| `my-session-revoke` | Sign out one exact other own session | `pathParams.id`, a UUID returned by the own-session list |
| `my-other-sessions-revoke` | Sign out all own sessions except the assistant's | `query.scope: "others"` |

`my-profile-update` can also accept an own phone change/clear or explicit photo removal, but this skill deliberately covers name only. Do not include those fields in a name save. Its answer and `my-profile-read` expose only ID, name and version; no email, phone or photo. Appearance settings other than the time zone, player erasure and ownership transfers are also outside this workflow.

## Availability and exclusions

- Account tools remain subject to the live connection's admission and access checks.
- The password hand-off returns the app's own Settings link alongside permitted route tools. Only the person opens it.
- Device-bound account cleanup and password submission are app-only, not missing assistant tools to invent or direct routes to call. Passwords never enter the assistant. Own-account deletion confirmation likewise stays with the person's separate email-linked confirmation button; this skill never handles its link/token or executes erasure.
- Request/cancel/status behavior is caller-only. Deletion ownership checks cover Team and League only; Club/Tournament ownership integration is not available yet. Team/League-only status is not full erasure clearance.
- Profile and session writes forbid automatic follow-up reads; deletion request/cancel do too. Stop on an unclear result, get a separate request to read again, then ask before any newly proposed change. No lost-result retry or automatic action chain.

## Data handling and verification

The plugin adds no service or credential store. Only the signed-in person's limited identity, preferences, own-device details and deletion status needed for the job enter the private conversation. Do not publish them or write them into this repository; do not retain credentials or confirmation links. The assistant client's handling applies to the conversation.

Treat both strict plugin validations as file-structure checks only. Do not call this a working signed-in journey until an end-to-end test-account run is separately verified; installing it does not enable assistant sign-in or change deployment restrictions.
