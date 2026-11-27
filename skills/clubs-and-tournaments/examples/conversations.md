# Club and Tournament examples

Follow the [workflow](../SKILL.md) and [tool reference](../references/tools.md). Present invitation choices neutrally and report only returned fields. Each example uses the one complete review for the whole requested change list, not a yes per item. A lost answer always stops writes without an automatic recovery read.

## “Which Clubs and Tournaments do I run?”

Read `my-clubs-list` after checking the live tool/schema. If Cedar Hollow Club has `season_name: "Spring 2027"`, report that as its current season. If another Club's season is null, say it is not shown. If `nextCursor` is present, explain more Clubs may remain and ask before the next page. A failed page is unverified, not an empty directory. For requested archived Clubs, use `query: { archived: "true" }` and retain that filter with `after` on a requested next page. Before a requested Restore, read `club-lifecycle-read` for the exact returned Club ID; the list itself does not authorize restoration.

For just a Club's current season use `club-current-season-read`; `club-details-read` also returns `seasonName`. It is chosen at creation, not editable afterward.

Read `my-tournaments-list` for current accepted Admin Tournaments, including private and ended ones. Show returned names, sport and location; distinguish repeated names by ID. Ask before another page. Select Cedar Spring Classic's returned ID, then read `tournament-details-read` for requested details and Rules. Pending invitations are not administered Tournaments.

## “Who is on Cedar Hollow Club's staff? Which offers are waiting?”

Resolve the Club's exact ID. Read `club-staff-list` and `club-sent-invitations-list` separately. Report Mira Finch as an accepted Admin only if the staff list says so. Report pending offers separately using their returned IDs, status and expiry. If an offer's email is null, say its address is hidden; never fill it from an earlier invite or infer it from the single staff name. A Team list is not a roster or a list of staff appointments.

## “Accept my Admin invitation to Cedar Spring Classic”

Read `my-tournament-admin-invitations-list`. It only lists offers still waiting for the person, leaves expired ones out and changes nothing.

Select the returned exact offer, Tournament and expiry; distinguish repeated names by IDs. Never recommend accepting or declining or call the offer low-risk because of its name or text. The person has chosen accept in this example. Then preview: “Accept this Admin invitation for Cedar Spring Classic, offer [returned invitation ID]? This grants Admin access to this Tournament, and the answer is final.” Use the shared review's next-message yes before one `tournament-admin-invitation-answer` with `answer: "accept"`. Use `status: "accepted"` and the returned Tournament ID to report confirmed acceptance. Club acceptance follows the equivalent Club tools; a pending invitee needs no Club staff access to answer.

For decline, include the exact offer and final decline effect in the same complete review. If the reply is lost, say it may have happened and stop without reading or answering again. Only a separately requested fresh list can show current offers; a vanished row proves neither answer.

## “Change Cedar Hollow Club's city”

Read fresh Club details and preserve the returned name, sports, state and Private choice. Show the old city and proposed new city, required unchanged fields and “Current season: unchanged.” Wait for the complete-list yes before one `club-details-update` using the exact saved revision. Report its returned details; do not add an automatic read-back. A Club city read says nothing about its Team's city. A revision conflict stops the edit; a later requested edit needs fresh state and a newly reviewed comparison, never an overwrite.

For a Tournament, preserve all details, including dates and explicit nulls: omitting an old date can clear it. To change Rules, read `tournament-details-read`, preview the full old/new Rules and preserved details, then use the shared complete-list approval. Send the complete approved Rules as `body.rules` with the saved revision in `tournament-details-update`. Omit Rules for a details-only edit. Include any requested Rules verification read in that review; the save reply does not include Rules. If the write reply is lost, stop without automatic verification. Never recreate a Tournament to change Rules.

## “Invite an Admin and cancel this waiting Tournament offer”

Read both selected scopes and sent-offer lists first. Obtain the new recipient's exact email directly from the person. Select the cancellation's exact pending, unexpired ID; a masked address is not an email match, so require exact row selection or hand that action to the app.

Show one list containing the new address, scope, Admin role and attempted email, plus the exact offer/Tournament to cancel and the fact it can no longer be accepted. After one next-message yes, make the two approved calls in order, not another yes per call. Use `tournament-admin-invite` and `tournament-admin-invitation-cancel` (or the matching Club tools). Neither a saved offer nor cancellation removes an accepted appointment. A receipt with `delivery: "sent"` confirms sending, not inbox delivery or accepted staff; `failed` means sending was not confirmed. Do not invite again to repair delivery. A confirmed refusal blocks only dependent actions; an unknown result stops writes.

## “Send that Admin invitation again”

Read `club-sent-invitations-list` or `tournament-sent-invitations-list`, and select the exact requested row only if `canResend: true`. Never reconstruct a hidden address. In the full review identify scope/row, the stored-address email effect, no Admin access before acceptance, and possible renewal of an expired retained offer without extending its original resend cutoff.

Get a fresh `idempotencyKey` from `request-key-new` for this deliberate send. After the one shared yes, use `club-admin-invitation-resend` or `tournament-admin-invitation-resend` with the exact invitation ID and retained key. Report returned expiry/delivery, not acceptance. If the answer is lost, retain the key, report unknown and stop; no automatic list read or replacement offer. A separately requested fresh list may inform a later decision; a requested same-operation repeat needs the fresh complete review and original-input/key rules, never a new key to resolve uncertainty.

## “Remove Mira as a Club Admin”

Read `club-staff-list` and select Mira Finch's returned `userId`. Preview the exact Club and person: Mira loses Club Admin access and Club Admin invitations she sent can no longer be accepted; staff history stays, and the Club, Teams and other Admins remain. Under the shared list approval, call `club-admin-remove` once. Only `{ removed: true }` confirms removal. Never use it to leave yourself; do that in the app. Removing another Tournament Admin is not available in the assistant or the app yet. A lost reply stays unknown: stop without scanning staff or removing again.

## “Delete Cedar Hollow Club — I created it by mistake”

Resolve the exact Club ID and read `club-lifecycle-read`. Show the returned Team/Admin/season/pending-invitation counts and `canDelete`; `teams` includes archived Teams and `invitations` means pending invitations. Do not calculate eligibility yourself or propose/call Delete when `canDelete` is false. If it is true, include the permanent loss of Club setup and finished invitation history, the retained shared deletion record and notes to Admins present at deletion in the complete review. Only the person's yes in their next message allows one `club-delete`; only `{ changed: true }` confirms it.

A refused Delete returns only a code and fixed message, not a list of what uses the Club. Name a use only if the lifecycle read shows `teams > 0` (including archived Teams) or `invitations > 0` (pending invitations); Admins/seasons are normal setup and Overview, Feed and history have no count, so never infer other uses. Offer Archive only for `DELETE_WINDOW_PASSED` or `IN_USE_ARCHIVE_INSTEAD`: it hides the Club from active lists/public results, keeps history and leaves Teams unchanged. For `CLUB_ARCHIVED`, say it is already archived and Restore is the option; other refusals stop without an Archive alternative. Any changed action needs a revised complete review and next-message yes, not the earlier Delete approval. A lost reply is unknown, not a refusal: stop writes without automatic reads, retries or changed actions. A separately requested `club-lifecycle-read` can show current state but cannot prove the lost deletion.

## “Change the Club Overview FAQ heading”

Read `club-overview-get` and, for this editing request, `club-overview-editor-get`. Read the chosen section's long text when needed with `club-overview-block-body-get`; archived long text uses `club-overview-block-archived-body-get`. Keep its returned title/text and every unchanged FAQ question/answer item in authored order when supplying replacement content. Omitting `items` would remove the list, not preserve it.

Preview the changed heading, retained questions/answers, unchanged audience and any order/lifecycle effects. Let the person name a new audience if wanted. Under the shared list approval, send one `club-overview-save` with the exact revision and approved staged changes. Explain permanent loss of the section and long text before any approved deletion. Do not automatically read back. If the save reply is lost, report unknown and stop; only separately requested fresh Overview/editor reads can inform a later decision, never prove rollback or authorize a resend.

## “Make a Club Team and enter it in the Tournament”

Read Cedar Hollow Club's Teams before preparing a new Team. Preview the requested Team name, sport, location, season, age group, Private choice and dates/omissions. Explain it permanently belongs to this Club, with no staff appointment, players or invitations added. Do not adopt or transfer an existing Team or assume Club Admin grants Team staff authority.

Explain which entry action can actually be prepared under current rights before the complete review. An authorized Tournament Admin can invite a Team; authorized Team staff can request entry. Neither means instant acceptance, and a new Club Team gives its creator no Team staff appointment. If the exact entry target/prerequisites cannot be resolved, mark that part not attempted rather than promise enrollment. After the one reviewed yes, create only what was approved and ready. A lost Team-creation answer stays unknown without a list probe or a second Team.

For a separately requested new Club/Tournament, preview all creation fields and Admin membership effects. Explain that empty Tournament Rules answers leave them unanswered, not defaulted; creation saves no bracket or computed standings. Obtain the complete-list yes and retain the original creation key/ID. Do not create a duplicate because discovery is incomplete.

## “Invite Cedar Comets to Cedar Spring Classic; answer this Team's other invitation”

As Tournament Admin, use `tournament-team-search` and `tournament-entries-list` to select the exact Comets Team and Tournament. For the independent answer, use `my-tournament-invitations-list` or `team-tournament-entries-list` and verify ordinary Team-side answering rights. Keep entry IDs separate from Team IDs; discovery, status and `canOpenTeam` grant no answering right.

Review both exact targets once: send Comets a pending Team invitation, with possible ordinary notices, and accept or decline the other exact invitation as explicitly chosen. After one next-message yes, use `tournament-team-invite` and `tournament-entry-respond` sequentially. Do not answer the newly created invitation or infer acceptance. The first returns only an entry `id`; the second succeeds as `{}`, not a saved receipt. On a lost answer stop writes without a follow-up read; only a separately requested fresh entry list can inform later work.

For an authorized Team-side request, use `team-tournament-search`, `team-tournament-entries-list` and `tournament-entry-request`. For requested leave use that Team entry list and `tournament-entry-leave`; for Tournament Admin removal use the Tournament entry list and `tournament-entry-remove`. Review the exact entry and possible notices; leave/removal keep Team/history and do not remove staff or accounts. `my-tournament-requests-list` shows visible requests, while `tournament-current-teams-list` shows current Team cards, not pending decisions. A withheld Team ID stays withheld.

## “Accept Cedar Comets' games for Cedar Spring Classic”

**Person:** “Accept Cedar Comets' game requests for Cedar Spring Classic.”

Read `tournament-game-requests-list` as current Comets staff, not merely as Tournament director. Select the exact returned Tournament/Team group and show every displayed detail for both games in this example, including dates/times/time zone, opponents/sides, Place/Field/address, arrival, description and attendance/family choices; preserve nulls. Include any other requested changes in this same review.

For example, show this whole two-game group for Cedar Comets at Cedar Spring Classic:

- **Game 1 — Cedar Comets vs Willow Owls:** April 10, 2027, 10:00–11:00 a.m., Central Time (`America/Chicago`); Comets home, Owls away; Cedar Hollow Park, Field 1, 100 Example Way; arrive 20 minutes early; description “Opening game”; attendance required, families included.
- **Game 2 — Pine Foxes vs Cedar Comets:** April 10, 2027, 1:00–2:00 p.m., Central Time (`America/Chicago`); Foxes home, Comets away; Cedar Hollow Park, Field 2, 100 Example Way; arrive 20 minutes early; description not provided (`null`); attendance required, families included.

**Assistant:** “Before you say yes: accepting notifies Cedar Comets' audience that these games are scheduled. Accept both games in this group for Cedar Spring Classic?”

**Person:** “Yes.”

Get an `opId` from `request-key-new`, retain the exact input and call `tournament-game-requests-answer` once with the displayed `tournamentId`, `teamId`, unchanged `snapshot` and every offer id/revision. Report only the returned status/count. `EVENT_STALE` stops: a requested fresh list and fresh reviewed yes are needed. A lost/malformed reply stays unknown, with original input/key retained and no automatic read or retry; a missing pending group proves neither success nor failure.

## “Make a Double elimination bracket”

Read current Teams and `tournament-bracket-read` as current Tournament Admin. Resolve the full Team set; ask for explicit seed order, seed slots/byes and Double format with `consolation: "none"`. Single can instead choose `none` or `third-place`. Warn that a Double bracket shows only on the computer version for now; phones show no bracket, and it cannot be remade as Single from a phone. Put these exact choices and advancement/correction warnings into the one complete review with any other requested changes; do not ask a second yes just for the bracket. If live descriptions still demand separate approval, stop that bracket write until aligned descriptions are released.

After the shared yes, send one `tournament-bracket-create`, not a new schedule or pool command. To record a separately requested result, first read the bracket and select returned `resolution.games.gameNumber`, exact `gameId`, side-ordered scores and revision. A tie needs the person's participating winner; never use array position or infer the winner. Under the complete-list approval call `tournament-bracket-result-record` once. Double routes losers until their second loss. Final 2 is If needed while waiting, playable only when ready, unnecessary when inactive. A played dependent game can block correction; report any `schedulingRefusals` without claiming all games were booked. A lost reply stays unknown with no automatic read/retry.

## “Change the Tournament sign-up link and clear the deadline”

Read shared `page-signup-link-read` for the exact Tournament with `kind: "tournament"`. Review the person's complete HTTPS URL and `deadline: null` with the rest of the requested changes. After the one shared yes, call `page-signup-link-set` with those values and the read's exact `expectedLinkRevision`; for Club/Tournament kinds send no event revision or `opId`. Clearing the whole link uses both `url: null` and `deadline: null`.

Report only the returned link revision. This changes an external link, not a payment or Team registration; never fetch it. A hidden invalid link is not a blank to overwrite. Unknown or stale outcomes do not permit automatic reads/retries or silently refreshed revisions. A Club's general details link list is different and remains dependent on the coordinated product release exposing its complete `links` read.
