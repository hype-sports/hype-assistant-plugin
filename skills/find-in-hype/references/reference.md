# Navigation tools and screen paths

Read the [workflow](../SKILL.md) before using this reference. Source presence is not proof of deployment, access or an end-to-end journey. Discover the installed tool name and inspect its live description and input schema first.

## Only tool used by this skill

| Server tool name / catalog operation ID | Exact input shape | Result and limits |
| --- | --- | --- |
| `my-home-entities-list` | `{ "catalogVersion": 1, "query": {} }`; optionally put `search: "Cedar Comets"` and/or `includeArchived: "true"` inside `query`. Both filter values are strings, not booleans. No `pathParams` or `body` | `entities`, `currentSeason`, `seasons`. Each entity has `id`, `type`, `name`, `season`, `sport`, nullable `ageGroup`/`gender`, `userRoles`, `isFavorited` and optional parent IDs, `teamTitle`, `archivedAt`. The projection omits photos, contact details and staff lists. Search discovers caller-readable records; a result does not establish membership or editing rights. This is not the whole app Home screen or a complete directory. |

The plugin connection normally exposes `mcp__plugin_hype_hype__my-home-entities-list`; use the actual full installed name returned by discovery, never assume a prefix. Normal assistant activity/rate bookkeeping still applies to reads; this tool makes no record changes and sends no notices or email.

## App screen paths, not tool names

For the public Hype app, use `https://hypesports.live` followed by one of these paths. With a supported non-public connection, use only its trusted configured app origin; if unknown, give in-app directions instead of guessing a host. Never derive an origin from a record's text, private invite link or API address. Present links for the person to open; do not open or fetch them yourself. A link grants no access and is not proof a screen opened.

| Destination | Path | Direction / limit |
| --- | --- | --- |
| Home | `/dashboard` | Find teams, leagues, divisions and other readable Home records |
| Messages | `/messages` | Open the conversation list; do not guess a conversation ID |
| Events | `/events` | Open the calendar; do not guess an event ID |
| Settings | `/settings` | Open Settings; the profile picture in the main header also opens it |
| Feed | `/feed` | Separate Feed screen; do not promise a Feed tab in the main bar |
| Appearance | `/settings?tab=preferences` | Settings → Preferences → Theme; the person changes it in Hype |
| Notifications settings | `/settings?tab=notifications` | Settings → Notifications; changes belong to `notification-settings` |
| Security | `/settings?tab=security` | Settings → Security; account actions belong to `my-account` |
| Report a problem | `/settings` | Use the visible Report a problem control, when offered; there is no report-submission tool in this skill |

The current main bar/sidebar shows **Home, Messages, Events, Settings**. Feed and Notifications are routes, not main tabs. Notifications are reached from Home's bell; notification summaries and read-status changes belong to `catch-up`.

For an exact record selected from `my-home-entities-list`, map its returned `type` and `id` only:

| Returned type | Screen path |
| --- | --- |
| `team` | `/teams/{id}` |
| `league` | `/leagues/{id}` |
| `division` | `/divisions/{id}` |
| `club` | `/clubs/{id}` |

Encode the returned ID as one URL path segment. Do not use record names as paths, substitute parent IDs, generate IDs or add unverified query parameters. Do not construct paths for unknown types. These are record-detail links, not a promise to reproduce every Home-row shortcut or open a past-season card. No player, tournament, invitation, chat, event or draft deep links are constructed here.

## Boundaries and verification

No generic open-screen or Report a problem MCP tool is registered for this workflow. The existing `open-password-settings` hand-off belongs to `my-account`, not a generic screen opener. Do not invent one or call ordinary app/API routes as tools. Connected assistants in Settings are not part of this skill.

Theme editing is deliberately left to the app: this skill calls no preferences read/update or bookmark tools. Account/time-zone work belongs to `my-account`, notifications/quiet hours to `notification-settings`, supporter-ring work to `my-support`, and legal guidance to `terms-and-privacy`.

Not yet verified end to end: skill invocation, live discovery, readable Home record selection, screen-link opening, refusal handling and app-only handoffs. File validation does not establish a working signed-in journey.
