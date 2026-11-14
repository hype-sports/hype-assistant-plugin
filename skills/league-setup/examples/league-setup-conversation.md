# League-setup worked conversation

Read this example of the [workflow](../SKILL.md) as a worked conversation, not a tool run or permission to save. Names, birth date and example.net addresses are invented. For actual calls, use returned ids and live schemas, not example ids.

## Find or create a league

**Commissioner:** `/hype:league-setup` — Help me set up Meadowbrook Youth League for Spring 2027 in Cedar Glen, TX.

**Assistant:** I'll check the signed-in Hype tools first. Installing the plugin grants no access; starting it approves no changes. Look for an existing league?

**Commissioner:** Yes.

_Check live tools/schemas and use `league-search` for the requested first page; in this example, observe no matching active league._

**Assistant:** No active match on this page. That does not rule out another name or an archived league. Search again, or deliberately create a new league?

**Commissioner:** Create one. Football, Spring 2027, Cedar Glen, TX. Private, no logo.

_Use listed sport choices if the live create schema provides them; otherwise only lowercase the person's supplied sport when that fits the schema. There is no sport-list tool; Hype still validates the sport. On a sport refusal, stop and explain, never try another key._

**Assistant:** Create this league?

| Detail | Save |
| --- | --- |
| Name | Meadowbrook Youth League |
| Sport | Football |
| Season | Spring 2027 |
| City / state | Cedar Glen, TX |
| Private | Yes — basic league discovery can still show it |
| Logo | None supplied |

Creation makes the caller League Admin and Commissioner. Season is fixed after creation. No divisions, players, invitations or games are included.

**Commissioner:** Yes, create that league.

_These are separate requests arriving over time, not a policy of one approval per setup step. For a single request covering the league, divisions and invitations, gather all choices and show the whole list once, then use one next-message yes for the exact sequence._

_Call `league-create` once, then read the returned id with `league-get` after clear success. Report “Private: yes — sent at creation, not confirmed”; Hype does not return that choice. In this example, observe no active divisions from `league-divisions-list`._

## Add a division and its starting teams

**Assistant:** What age group and gender should the first division use?

**Commissioner:** 8U Boys, named 8U Boys.

_Obtain the remaining setup choices one question at a time; do not infer numeric eligibility from “8U”._

**Assistant:** Create this division in Meadowbrook Youth League, Spring 2027?

| Detail | Save |
| --- | --- |
| Name | 8U Boys |
| Age group / gender | 8U / Boys |
| Minimum / maximum age | 6 / 8 |
| Count age on | April 1, 2027 |
| New teams' age group | 8U |
| Teams to create | 4 |
| Players per team setting | 10 |
| Allow player exceptions | No |

This also creates **Team 1, Team 2, Team 3 and Team 4 without coaches**. There is no team-name field; rename each team on the team itself, outside this skill. No existing teams, players or games are added.

**Commissioner:** Yes, create that division and those four teams.

_Call `league-division-create` once and read the returned division id after clear success._

## Fix a saved detail

**Commissioner:** Change 8U Boys' configured team count to six.

_Read `division-get` immediately before the change._

**Assistant:** In **8U Boys**, change **configured team count: 4 → 6**, leaving all other settings unchanged? This **does not create two teams or remove any teams**; the returned placed-team count is still four.

**Commissioner:** Yes, change only that setting.

_Call `division-update` once, read the same id and compare the saved setting and any derived name. Keep the visible placed-team count and configured count separate._

## Include staff offers in the complete requested review

**Commissioner:** Invite Morgan Vale at morgan.vale@example.net as Commissioner, not Admin.

_Use `/hype:league-staff` and its exact invitation policy; read `league-staff-list` as the League Admin in this example._

**Assistant:** Invite **morgan.vale@example.net** to **Meadowbrook Youth League**? **Admin: no. Commissioner: yes.** This creates a pending offer and attempts email. Morgan must accept separately. A pending offer to the same address would be replaced.

**Commissioner:** Yes, send that invitation.

_Get a fresh key from `request-key-new`, then call `league-staff-invite` once with it as `idempotencyKey`; in this example, receive an invitation id with email not sent._

**Assistant:** Invitation created; email not sent. Morgan has not joined staff.

**Commissioner:** Invite Avery Reed at avery.reed@example.net as Division Admin for 8U Boys.

_Read the authorized `division-admin-list`; in this example, observe no accepted appointments or pending invitations._

**Assistant:** Invite **avery.reed@example.net** as **Division Admin of 8U Boys**, not League Admin? **No email is sent.** Avery must accept separately.

**Commissioner:** Yes.

_Call `division-admin-invite` once; treat the returned invitation id as an offer, not an appointment or email receipt._

## Register a player; then invite a parent/guardian

**Commissioner:** Add Rowan Finch to 8U Boys.

_First use `division-players-lookup`; in this example, observe no matching unarchived registration. Explain the limits and ask for required details, without collecting optional contacts for readiness._

**Commissioner:** Rowan Finch, male, born May 14, 2019. Did not come to evaluations. No optional contacts or evaluation number.

**Assistant:** Add this registration to **8U Boys**, Meadowbrook Youth League, Spring 2027?

| Detail | Save |
| --- | --- |
| First / last name | Rowan / Finch |
| Gender | Male |
| Birth date | May 14, 2019 — please check this date |
| Came to evaluations | No |
| Parent email / phone | Not supplied |
| Evaluation number / exception approval | Not supplied |

This does not assign a team or create/link a family profile.

**Commissioner:** Yes, that date and those details are correct; save the registration.

_Call `division-player-create` once; check its returned registration id with a permitted lookup after clear success. Do not echo the birth date again or copy it into summaries/files. Do not treat the lookup as verification of private fields._

**Commissioner:** Invite Taylor Finch at taylor.finch@example.net as Rowan's parent/guardian.

_Confirm registration/league ids and read `league-player-guardian-invitations-list`. Do not treat its address-free rows as proof of address-specific duplication or accepted guardian status._

**Assistant:** Invite **taylor.finch@example.net** as **parent/guardian of Rowan Finch's registration in Meadowbrook Youth League**? This attempts email and sends an in-app notice. A pending offer to that address would be replaced. Taylor must accept separately; no profile is created or linked.

**Commissioner:** Yes.

_Get a fresh key from `request-key-new`, then call `league-player-guardian-invitation-create` once with it as `idempotencyKey`; in this example, receive an invitation id and email-service acceptance, not mailbox delivery or guardian acceptance._

## Read-only readiness

_After the person requests readiness, read `division-onboarding-get` for 8U Boys and supplement only with permitted requested reads. Report returned checklist items/details as in place, missing or unknown. A done flag is a snapshot, not scheduling proof or authority to fill gaps. Support only this additional summary._

| 8U Boys | In place | Missing or unknown |
| --- | --- | --- |
| Setup | Active Spring 2027 division; saved 8U Boys setup | No automatic completion claim |
| Teams | Visible placed count: 4; configured count: 6 | Complete team ids, current seasons and coaching unverified by counts |
| Staff | Caller is accepted league staff | No accepted Division Admin in the returned list; Avery/Morgan offers are pending |
| Players | One visible active registration | Team assignment and accepted guardian access unknown |

**Assistant:** This setup check does not prove whether games are scheduled. Use **`/hype:season-schedule`** next; it checks its own live tools, complete teams, saved Fields, dates and conflicts.

## A later season-end request

**Commissioner:** Archive 8U Boys.

_Read the exact division and `division-impact`, show returned counts and explain they are deletion impact, not an exact archive preview._

**Assistant:** Archive **8U Boys**, Meadowbrook Youth League, Spring 2027? Its registrations and eligible league-made teams are archived in a restorable batch. Coach-run teams stay active; teams needed by another league's open draft may stay active too. The division becomes read-only; nothing is deleted.

**Commissioner:** Yes, archive that division.

_Call `division-archive` once. Report actual skipped-team counts, or “not told” when absent. For a later restore, obtain its own preview/yes, league first if needed; leave teams placed elsewhere where they are. For any unclear result at any step, follow only the workflow's [single recovery rule](../SKILL.md#if-a-result-is-unclear)._
