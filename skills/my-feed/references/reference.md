# Feed tool reference

Discover full installed names and inspect live descriptions and input schemas first. The expected names are `mcp__plugin_hype_hype__<operation-id>`; the live tool list wins. These operation IDs do not grant access.

## Operations used by this skill

Current envelope: `catalogVersion: 1`, plus only the listed `pathParams`, `query` and/or `body`. Omit absent sections rather than sending null. Use exact authorized saved IDs or a trustworthy known target; generate UUID operation keys only for genuinely new approved writes, never saved-record IDs. Retain operation keys and the prepared input for person-requested recovery, not automatic replay. Do not supply a caller identity, credentials, headers or extra fields. Keep schema field names and operation keys internal; explain results in plain words as in [the workflow](../SKILL.md).

| Operation ID | Inputs besides catalogVersion | Result and meaning |
| --- | --- | --- |
| `feed-eligible-teams-list` | `query: {}` | `teams: [{ teamId, label }]`, `complete: true`; if the team list is refused or missing, stop |
| `feed-posts-list` | `body: { scope: "mine" }` for All or `{ scope: "team:<teamId>" }`; optional `limit`, `after`, `kind` | `posts`, `nextCursor`; one page, default limit 20, maximum 100. Kind may be `announcement` or `event_notice`; omit it for All, including welcome posts and moments. Never send `search`: search is not enabled |
| `feed-post-read` | `pathParams: { id: postId }` | `post`; currently authorized exact post, not a seen/read mark |
| `feed-post-comments-list` | `pathParams: { id: postId }`, `query: {}` or `{ limit, after }` | `comments`, `nextCursor`; root comments oldest first, default 20, maximum 50. Cursor is bound to caller, post and limit; even an empty page can continue |
| `feed-post-comment-create` | `pathParams: { id: postId }`, `body: { operationId, text }` | `{ status: "confirmed", commentId }` or `{ status: "unavailable" }`; only confirmed plus ID confirms publication. Exact approved text, nonblank, within live limits |
| `feed-post-hype` | `pathParams: { id: postId }`, `body: { operationId }` | `total`, `mine`, `operationId`; one-way Hype with no Undo. A replay returns its saved receipt, not current counts |
| `feed-announcement-audience-options-list` | `query: {}` | `origins: [{ origin: { type, id }, label, recipientRoles, targets: [{ type, id, label, parent? }] }]`; current permitted choices, not later authority |
| `feed-announcement-reach-read` | `body: { origin, targets, recipientRoles }` | `{ count }`; current audience-size snapshot only. Consumes reach allowance, not a reservation or delivery promise |
| `feed-announcement-intent-create` | `body: { opId, origin, targets, recipientRoles, text, commentsEnabled }` | `intentId`, `state` (`pending` or `cancelled`), `undoUntil`, `commentsEnabled`, `execution`. For a pending announcement, `queued` means lined up to go out after the 10-second Undo window unless held or refused; `unavailable` means saved but not lined up to go out. Neither proves phone delivery |
| `feed-announcement-intent-cancel` | `pathParams: { id: intentId }` | Same receipt shape; only `state: "cancelled"` confirms Undo. Cancel the exact just-saved own announcement immediately on the person's “Undo”; no extra confirmation. Original 10-second window; successful cancellation can be replayed later only when requested |

`origin` and each target are `{ type: "team" | "division" | "league", id }`, selected from the returned options for that origin. There must be 1–50 targets and 1–4 recipient roles, only as offered: `staff`, `parents_guardians`, `fans`, `league_staff`. Display these as Staff, parents/guardians, fans and league staff without inventing access. Preserve exact IDs and types. The API normalizes duplicate targets and roles; never use that as permission to broaden the approved audience. Comments setting is optional at the API boundary, but this workflow resolves and sends it explicitly for an unambiguous review.

For Feed lists, keep `scope`, `kind` and `limit` unchanged while using returned `nextCursor` as `after`. Start again without the old cursor when filters change. Cursors are opaque; do not decode or manufacture them. Reads are bounded, not full-history exports. Do not automatically fetch the next page, retry or refresh.

## Outside this workflow

Use [catch-up](../../catch-up/SKILL.md) for notification reading/read-state or [notification-settings](../../notification-settings/SKILL.md) for notification choices; a plain request selects the skill, with no typed command needed.

Listing/acknowledging failed announcement sends has no assistant binding here. Do not invent operation-status lookup or resend tools. Moment creation/withdrawal and nested comment replies are unavailable. Deletion, pins and seen counts are outside this skill; use the app.
