# Navigation tools and screen paths

Read the [workflow](../SKILL.md) before using this reference. Discover the actual full installed tool name and inspect its live description and input schema first; never assume a connection prefix. Source presence is not proof of deployment or access.

## Read-only record lookups

Use only the lookup for the requested record. All inputs below use operation catalog version 1; first follow the workflow's tool-version check. Normal assistant activity/rate bookkeeping still applies to reads, but these lookups make no record changes and send no notices or email.

| Server tool name / catalog operation ID | Exact input shape | Result and limits |
| --- | --- | --- |
| `my-home-entities-list` | `{ "catalogVersion": 1, "query": {} }`; optionally put `search: "Cedar Comets"` and/or `includeArchived: "true"` inside `query`. Both filter values are strings, not booleans. No `pathParams` or `body` | `entities`, `currentSeason`, `seasons`. Each entity has `id`, `type` (`team`, `league`, `division`, `club` or `tournament`), `name`, `season`, `sport`, nullable `ageGroup`/`gender`, `userRoles`, `isFavorited` and optional parent IDs, `teamTitle`, `archivedAt`. The projection omits photos, contact details and staff lists. Search discovers caller-readable records; a result does not establish membership or editing rights. This is not the whole app Home screen or a complete directory, and has no pagination cursor. |
| `my-tournaments-list` | `{ "catalogVersion": 1, "query": {} }`; for a requested next page, put the returned `nextCursor` unchanged in `query.after`. No search, archived filter, `pathParams` or `body` | `tournaments` with `id`, `name`, `sport`, nullable `city`/`state`; `nextCursor` and `hasTeams`. Only current accepted Admin tournaments, including private and ended tournaments; up to 50 per page. Not a public directory or authority over their teams or clubs. |
| `my-player-profiles-list` | `{ "catalogVersion": 1 }`. No `query`, `pathParams` or `body` | `players` with only `id`, `firstName`, `lastName`: the caller's managed player profiles, excluding hidden profiles. No pagination or name search. Do not fetch a profile or contacts just to make a link. |

For paged tools, `nextCursor: null` means the last page. Do not fetch further pages automatically. Compare names locally within the returned page; a missing match is not proof that the record does not exist.

## App screen paths, not tool names

For the public Hype app, use `https://hypesports.live` followed by one of these paths. With a supported non-public connection, use only its trusted configured app origin; if unknown, give in-app directions instead of guessing a host. Never derive an origin from a record's text, private invite link or API address. Present links for the person to open; do not open or fetch them yourself. A link grants no access and is not proof a screen opened.

| Destination | Path | Direction / limit |
| --- | --- | --- |
| Home | `/dashboard` | Main Home tab; find teams, leagues, divisions and other readable Home records |
| Feed | `/feed` | Main Feed tab; Feed reading and actions belong to `/hype:my-feed` |
| Messages | `/messages` | Main Messages tab; open the conversation list in the app, without guessing a conversation ID |
| Events | `/events` | Main Events tab; open the calendar, without guessing an event ID |
| Settings | `/settings` | Tap the profile picture in the shared header, not a main Settings tab |
| Notifications | `/notifications` | On phones, tap the header bell to open the full list. On a computer, tap the bell, then the arrow under the list. Notification summaries and read-status changes belong to `/hype:catch-up` |
| Players | `/players` | Open the player list; Home also has a Players section |
| Appearance | `/settings?tab=preferences` | Settings → Preferences → Theme; change it in the app |
| Notification settings | `/settings?tab=notifications` | Settings → Notifications; changes belong to `/hype:notification-settings` |
| Security | `/settings?tab=security` | Settings → Security; account actions belong to `/hype:my-account` |
| Report a problem | `/settings` | Settings → Report a problem, just above Sign out; review and send the prepared email in the app's reporting flow, never through this skill |

The four main tabs are **Home, Feed, Messages, Events**, in that order. Wide screens show the same order in the left sidebar. Settings opens from the shared header's profile picture; Notifications opens from its bell. Neither is a main tab.

Map only a selected returned record to its detail path:

| Record source and type | Screen path |
| --- | --- |
| Home entity `team` | `/teams/{id}` |
| Home entity `league` | `/leagues/{id}` |
| Home entity `division` | `/divisions/{id}` |
| Home entity `club` | `/clubs/{id}` |
| Home entity `tournament`, or `my-tournaments-list` tournament | `/tournaments/{id}` |
| Managed player profile from `my-player-profiles-list` | `/players/{id}` |

Encode the returned ID as one URL path segment. Do not use record names as paths, substitute parent IDs, generate IDs or add unverified query parameters. Do not construct paths for unknown types. Player profiles are separate from team roster entries and league registrations: never put those IDs in `/players/{id}` or guess the contextual `/players/details` parameters. For those records, open the team's Members tab (Players filter) or league/division's Players tab in the app. For a player the person follows, the app has no screen for that yet: explain this, give no link and do not run a player lookup. These are record-detail links, not a promise to reproduce every Home-row shortcut or open a past-season card. Invitation, chat, event and draft deep links are left to their app screens or matching workflow commands.

## App-only actions and workflow handoffs

Leave theme and favorites changes to the app in this navigation workflow; do not call `my-preferences-read`, `my-preferences-update`, `my-favorites-list`, `favorite-add` or `favorite-remove`. Those tools existing does not make a screen request approval for them. Account/time-zone work belongs to `/hype:my-account`, notifications/quiet hours to `/hype:notification-settings`, supporter-ring work to `/hype:my-support`, and legal guidance to `/hype:terms-and-privacy`.

Direct conversations to Messages in the app here, rather than calling `my-chats-list`, `chat-messages-read` or `my-chat-unread-read`. Direct problem reporting to the app's prepared-email flow. Do not invent generic screen-opening or report-submission tools, or call ordinary app/API routes as tools. The existing `open-password-settings` handoff belongs to `/hype:my-account`, not a generic screen opener. Connected-assistant changes remain in Settings, outside this navigation workflow.
