# Manage my team: worked scenarios

Use these invented scenarios as expected behavior, not a live-run record. Bracketed IDs stand for exact authorized returned IDs, never literal inputs or generated values. Use each person's own connection; never switch accounts to complete a workflow.

## 1. Current Roster, Staff and a past season

**Person:** Show Cedar Comets' Roster this season and who coaches them.

Check live tools/schemas. Resolve the exact team using its known ID or a requested public `team-search`; clarify duplicate matches. Call `team-roster-list` with that ID and `query: {}`, then `team-staff-list`. Show player names/jerseys/positions only as returned, separate from Staff. Display a jersey 0 as 0, not missing; display 00 separately. Translate Admin marks and titles without reconstructing withheld names or contacts. Mark refused or empty visibility honestly.

**Person:** Show their previous season too.

Read `team-seasons-list`; let the person choose [returned season ID] for this team, then call `team-roster-list` with `query: { season: [returned season ID] }`. Keep current/past labels clear. Describe an empty result as no entries visible, not proof there were no players. Make no changes.

## 2. Add, take off and put back

**Person:** Add Quinn Example to Cedar Comets with jersey 0.

**Assistant:** Adding a player through the assistant is coming soon. Use Cedar Comets' Roster in Hype; a jersey is optional and 0 is valid. I haven't added a player.

**Person:** Take Quinn off the Roster, then put Quinn back.

Explain that these assistant tools are also unavailable through the assistant. Direct removal to the app's Roster and put-back to Removed this season. Explain history is kept; do not delete a profile or create a duplicate player. Keep the unavailable roster actions outside this skill; never execute either write or treat one request as approval for two changes.

## 3. Invite a coach; delivery is not membership

**Person:** Invite Robin Example as Assistant Coach for Cedar Comets.

Resolve the exact team; read its role from `my-home-entities-list` and proceed only for Admin or Staff. Inspect `team-staff-list`. Ask for the exact address directly, without account lookup. Check only that supplied address with `team-invitations-list`. For the example's false pending answer, prepare email-only `team-invitation-create`, `title: "assistant_coach"`, `makeOwner: false`. Stop a new create if true; explain and ask if null, never assume no pending offer.

**Assistant:** Invite Robin to Cedar Comets [team ID] as Assistant Coach, not Admin, at the address supplied? This sends a real invitation email attempt; Robin gains Staff access only after accepting. Staff can see players' emergency contacts in Hype while on the current roster of an active team. Repeating a send can replace an earlier pending offer and send another email. Shall I send this exact invitation?

**Person:** Yes.

Call once. With `{ id, recipientMode: "email", email: "not_sent", overlaps: [] }`, say the invitation was created and is waiting for Robin's answer, but email was not sent. Do not create again or send a separate message.

**Person:** Resend it.

Explain resend and repeat-safe invitations are not available yet; hand off to Hype's Staff area. Never substitute another create.

For verification, do not create this invitation unless a supported immediate cancellation/cleanup route exists. Staff-invite cancellation is not available through the assistant. Stop irreversible verification sends and report the limit; never leave an invitation behind just to claim a pass.

## 4. Answer my Staff invitation

**Person:** Show my team Staff invitations.

Use `my-team-invitations-list` as the recipient. Show only returned team, title, Admin grant, expiry, inviter and overlap facts; make no change.

**Person:** Accept the Cedar Comets offer.

Select its exact returned invitation ID; clarify if there are multiple offers. Explain Staff and emergency-contact access, including Admin rights only if this exact offer grants them. Review [invitation ID], team, title and effects. Wait for a later explicit yes, then call `team-invitation-accept` once and report only the returned team joined. Do not add a player or accept another invitation.

For a decline request instead, review the exact offer and explain no joining or existing staff removal; after explicit yes call `team-invitation-decline` once. Treat `{}` as success, not a missing reply. These are alternative decisions, not a sequence on one invitation. For verification, accept/decline only when the target and cleanup are safe; otherwise stop and report unverified.

## 5. Who is waiting; league history and division placement

**Person:** Who is waiting to join Cedar Comets?

Check that `my-home-entities-list` shows Admin or Staff for this team before offering the staff-only lists below. Ask which list: Staff offers, followers, player parent/guardian requests or league memberships. Use `team-invitations-list` for the first and `team-relationship-requests-list` with `status: "pending"` for follower/historical family requests. Explain that incoming player parent/guardian requests are not available yet; do not pretend the follower list is that queue. Do not answer any request as part of listing.

**Person:** Show the team's leagues and put it in Cedar Division.

Read `team-memberships-list` for the exact team. Preserve its scope, archive dates and unknown co-owner state. Explain that placing a team, answering or leaving a membership is not available yet; direct league staff to Hype. Do not infer placement powers from membership/destination facts or create a replacement team.

## 6. Refused tool or unclear send

If a needed tool is absent/refused, explain the limit and stop that part; still answer any other independent reads asked for in the same message, each refusal reported beside them. No direct API, account change or guessed input, and nothing that depended on the refused part.

If the approved coach invite has a lost reply instead of a confirmed result, say it may have happened. Do not resend, cancel, poll or automatically read. Ask the person to check Staff in Hype. A separately requested authorized read shows only current facts, not whether the earlier email was sent; never treat a missing pending row as permission to send again. Require fresh review and yes for any later supported action.

## 7. A follower asks for team management lists

**Person:** Show Cedar Comets' Roster, pending Staff invitations, follow requests and league memberships, then invite a coach.

Discover live tools/schemas and select Cedar Comets' exact team row from `my-home-entities-list`. For this scenario, its returned role is follower, not Admin or Staff. Use that role to limit offers, not to test permission by calling restricted tools.

**Assistant:** Your Home list shows you follow Cedar Comets, rather than being team Admin or Staff. Pending Staff invitations, follow requests, league memberships and coach invitations need that team access, so I won't request those lists or send an invitation. I can show the Roster within your access; I can also help with Staff or season information that Hype allows you to see.

Complete the requested independent `team-roster-list` read and show only its returned fields. Do not call `team-invitations-list` (with or without an email), `team-relationship-requests-list`, `team-memberships-list` or `team-invitation-create`; do not ask for a coach's address. Offer the same limited choices for a missing or unknown role. Keep the person's own incoming Staff invitation inbox available through section 5. If a later Home read shows Admin or Staff, allow the requested staff workflow to proceed normally, but report any subsequent server refusal if that role has changed again; never retry or work around it.
