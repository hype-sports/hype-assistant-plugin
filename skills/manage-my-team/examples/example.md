# Manage my team: worked scenarios

Use these invented scenarios as expected behavior, not a live-run record. Bracketed IDs stand for exact authorized returned IDs, never literal inputs or generated values. Use each person's own connection; never switch accounts to complete a workflow.

## 1. Current Roster, Staff and a past season

**Person:** Show Cedar Comets' Roster this season and who coaches them.

Check live tools/schemas. Resolve the exact team using its known ID or a requested public `team-search`; clarify duplicate matches. Call `team-roster-list` with that ID and `query: {}`, then `team-staff-list`. Show player names/jerseys/positions only as returned, separate from Staff. Display a jersey 0 as 0, not missing; display 00 separately. Translate Admin marks and titles without reconstructing withheld names or contacts. Mark refused or empty visibility honestly.

**Person:** Show their previous season too.

Read `team-seasons-list`; let the person choose [returned season ID] for this team, then call `team-roster-list` with `query: { season: [returned season ID] }`. Keep current/past labels clear. Describe an empty result as no entries visible, not proof there were no players. Make no changes.

## 2. Add, change, take off and put back

**Person:** Add Quinn Example to Cedar Comets with jersey 0.

Read `team-roster-list` (current season) and check no Quinn Example is already listed.

**Assistant:** Add Quinn Example to Cedar Comets' Roster this season as a player with jersey 0? No parent details are needed. Shall I add this player?

**Person:** Yes.

Call `team-roster-entry-create` once with `role: "player"`, the names and `jerseyNumber: 0`. Report the returned [entry ID] as added. Never call again for the same player; another call can create a duplicate.

**Person:** Add Avery Example with jersey 4, make Quinn number 7, then take Rowan Sample off the Roster.

Read the current Roster and resolve exact entries. Show all three changes once:

| Target | Exact change | Effect / notifications |
| --- | --- | --- |
| Avery Example, current Cedar Comets season | Add player, jersey 4 | New Roster entry, no Staff or guardian grant; state notice behavior only if the live tool specifies it |
| Quinn Example, selected entry | Jersey 0 → 7 | Other fields unchanged; state notice behavior only if the live tool specifies it |
| Rowan Sample, selected entry | Take off this season's Roster | Keeps history and profile; notifies parents/guardians |

**Assistant:** Shall I make all three listed changes?

**Person:** Yes.

Call create, update and remove once each, in that order, without another question. Bind Avery only to the confirmed create receipt. If Quinn's update is refused, report it and still attempt Rowan's independent approved removal; if a reply is lost, stop writes and inspect authorized current state before recovery. Report done, refused, unknown and not attempted separately.

**Person:** Put Rowan back.

Read `team-roster-removed-list`, choose Rowan's exact [removed entry ID], explain that parents/guardians are notified, and after a later yes call `team-roster-entry-restore` once. If it refuses `PAST_SEASON`, explain the entry belongs to an earlier season and offer a fresh add to this season instead; on `PROFILE_ALREADY_ON_ROSTER`, read the Roster again and show Rowan is already on it. Never add a duplicate as a substitute.

**Person:** Roll the Roster over to next season.

Read `team-roster-start-sources-list` for Cedar Comets and `team-seasons-list` for its [next season ID]. Show the source team and season, the destination season and every selected player and staff member. Explain they are added directly with eligible parent/guardian links and staff permissions, and no invitation or email is sent. After a later yes, get a fresh key from `request-key-new` and call `team-roster-roll-over` once with it as `operationId`; report the six counts.

## 3. Invite a coach; delivery is not membership

**Person:** Invite Robin Example as Assistant Coach for Cedar Comets.

Resolve the exact team; read its role from `my-home-entities-list` and proceed only for Admin or Staff. Inspect `team-staff-list`. Ask for the exact address directly, without account lookup. Check only that supplied address with `team-invitations-list`. For the example's false pending answer, prepare email-only `team-invitation-create`, `title: "assistant_coach"`, `makeOwner: false`. Stop a new create if true (offer resend); explain and ask if null, never assume no pending offer.

**Assistant:** Invite Robin to Cedar Comets [team ID] as Assistant Coach, not Admin, at the address supplied? This sends a real invitation email attempt; Robin gains Staff access only after accepting. Staff can see players' emergency contacts in Hype while on the current roster of an active team. Repeating a send can replace an earlier pending offer and send another email. Shall I send this exact invitation?

**Person:** Yes.

Get a fresh key from `request-key-new` (input `{}`), send it as `idempotencyKey` and call once. With `{ id, recipientMode: "email", email: "not_sent", overlaps: [] }`, say the invitation was created and is waiting for Robin's answer, but email was not sent. Do not create again or send a separate message.

**Person:** Resend it.

Read `team-invitations-list` and choose Robin's exact [invitation ID] by title, expiry and last sent (no addresses are shown). If `canResend` is true, explain that it sends another real email; after a later yes, get a fresh key and call `team-invitation-resend` once. Never use create as a resend.

**Person:** Actually, cancel Robin's invitation.

Review the same exact invitation: it withdraws the offer and removes nobody already on Staff. After a later yes, call `team-invitation-cancel` once. For verification, cancel any test invitation this way so none is left behind.

## 4. Answer my Staff invitation

**Person:** Show my team Staff invitations.

Use `my-team-invitations-list` as the recipient. Show only returned team, title, Admin grant, expiry, inviter and overlap facts; make no change.

**Person:** Accept the Cedar Comets offer.

Select its exact returned invitation ID; clarify if there are multiple offers. Explain Staff and emergency-contact access, including Admin rights only if this exact offer grants them. Review [invitation ID], team, title and effects. Wait for a later explicit yes, then call `team-invitation-accept` once and report only the returned team joined. Do not add a player or accept another invitation.

For a decline request instead, review the exact offer and explain no joining or existing staff removal; after explicit yes call `team-invitation-decline` once. Treat `{}` as success, not a missing reply. These are alternative decisions, not a sequence on one invitation. For verification, accept/decline only when the target and cleanup are safe; otherwise stop and report unverified.

## 5. Who is waiting; league history and division placement

**Person:** Who is waiting to join Cedar Comets?

Check that `my-home-entities-list` shows Admin or Staff for this team before offering Staff offers or follow requests; for parent/guardian requests and league memberships the Home role only tailors the offer and the live tool decides. Ask which list: Staff offers, followers, player parent/guardian requests or league memberships. Use `team-invitations-list` for the first, `team-relationship-requests-list` with `status: "pending"` for followers and `team-guardian-requests-list` for parent/guardian requests; never treat the follower list as that queue. Do not answer any request as part of listing.

**Person:** Approve Casey Sample's request for Quinn.

Select that exact [request ID] from `team-guardian-requests-list`, show the player and asker, and explain that approving gives Casey parent/guardian access to Quinn on this team and may also link a player profile Casey offered, with its family and notice effects. After a later yes, call `guardian-request-approve` once and report the returned outcome (`already` means nobody new was added).

**Person:** Show the team's leagues and put it in Cedar Division.

Read `team-memberships-list` for the exact team. Preserve its scope, archive dates and unknown co-owner state. Placing a team in a division is a League staff action: proceed only when Home shows the person as staff of that league, read `league-divisions-list` for Cedar Division's exact ID, review the move and, after a later yes, call `team-membership-place-in-division` once. Otherwise explain that the league's staff place teams. Do not infer placement powers from membership facts or create a replacement team.

## 6. Refused tool or unclear send

If a needed tool is absent/refused, explain the limit and stop that part; still complete other requested independent reads and approved independent changes that remain allowed, each refusal reported beside them. No direct API, account change or guessed input, and nothing that depended on the refused part.

If the approved coach invite has a lost reply instead of a confirmed result, say it may have happened. Do not resend, cancel or poll. Read authorized current Staff state and use the app if it cannot resolve the result; the read shows only current facts, not whether the earlier email was sent; never treat a missing pending row as permission to send again. Require fresh review and yes for any later supported action.

## 7. A follower asks for team management lists

**Person:** Show Cedar Comets' Roster, pending Staff invitations, follow requests and league memberships, then invite a coach.

Discover live tools/schemas and select Cedar Comets' exact team row from `my-home-entities-list`. For this scenario, its `userRoles` is `["fan"]`: follower, not Admin or Staff. Use that role to limit offers, not to test permission by calling restricted tools.

**Assistant:** Your Home list shows you follow Cedar Comets, rather than being team Admin or Staff. Pending Staff invitations, follow requests and coach invitations need that team access, so I won't request those lists or send an invitation. I can show the Roster within your access, and I can ask Hype for the league memberships it lets you see; I can also help with Staff or season information that Hype allows you to see.

Complete the requested independent `team-roster-list` read and show only its returned fields. Do not call `team-invitations-list` (with or without an email), `team-relationship-requests-list` or `team-invitation-create`; `team-memberships-list` may be read and its refusal, if any, reported; do not ask for a coach's address. Offer the same limited choices for a missing or unknown role. Keep the person's own incoming Staff invitation inbox available through SKILL.md section 5 (scenario 4 above). If a later Home read shows Admin or Staff, allow the requested staff workflow to proceed normally, but report any subsequent server refusal if that role has changed again; never retry or work around it.
