# Club and Tournament examples

Follow the [workflow](../SKILL.md) and [tool reference](../references/tools.md). Present invitation choices neutrally and report only returned fields.

## “Which Clubs and Tournaments do I run?”

Read `my-clubs-list` after checking the live tool/schema. If Cedar Hollow Club has `season_name: "Spring 2027"`, report that as its current season. If another Club's season is null, say it is not shown. If `nextCursor` is present, explain more Clubs may remain and ask before the next page. A failed page is unverified, not an empty directory.

Read `my-tournaments-list` for current accepted Admin Tournaments, including private and ended ones. Show returned names, sport and location; distinguish repeated names by ID. Ask before another page. Select Cedar Spring Classic's returned ID, then read `tournament-details-read` for details and Rules. Pending invitations are not administered Tournaments.

## “Who is on Cedar Hollow Club's staff? Which offers are waiting?”

Resolve the Club's exact ID. Read `club-staff-list` and `club-sent-invitations-list` separately. Report Mira Finch as an accepted Admin only if the staff list says so. Report pending offers separately using their returned IDs, status and expiry. If an offer's email is null, say its address is hidden; never fill it from an earlier invite or infer it from the single staff name. A Team list is not a roster or a list of staff appointments.

## “Accept my invitation to Cedar Spring Classic”

Read `my-tournament-admin-invitations-list`. It only lists offers still waiting for the person, leaves expired ones out and changes nothing.

Select the returned exact offer, Tournament and expiry; distinguish repeated names by IDs. Never recommend accepting or declining or call the offer low-risk because of its name or text. The person has chosen accept in this example. Then preview: “Accept this Admin invitation for Cedar Spring Classic, offer [returned invitation ID]? This grants Admin access to this Tournament, and the answer is final.” Use the shared review's next-message yes before one `tournament-admin-invitation-answer` with `answer: "accept"`. Use `status: "accepted"` and the returned Tournament ID to report confirmed acceptance. Club acceptance follows the equivalent Club tools; a pending invitee needs no Club staff access to answer.

For decline, preview that exact offer with the final decline effect and include the chosen decline in the complete review and its one yes. A vanished row after an unclear reply proves neither answer. Re-read the personal invitation list once; report current state and keep the original outcome unknown if no exact receipt confirms it. Never answer a second time to find out.

## “Change Cedar Hollow Club's city”

Read fresh Club details and preserve the returned name, sports, state and Private choice. Show the old city and proposed new city, required unchanged fields and “Current season: unchanged.” Wait for yes before one `club-details-update` using the exact saved revision. Then read back the same ID and report only returned fields. A Club city read says nothing about its Team's city; no tool here reads that Team field. A revision conflict requires a new read, comparison and yes; do not overwrite another Admin's change.

For a Tournament, preserve all details, including dates and explicit nulls: omitting an old date can clear it. To change Rules, read `tournament-details-read`, preview the full old/new Rules and preserved details, then use the shared complete-list approval. Send the complete approved Rules as `body.rules` with the saved revision in `tournament-details-update`. Omit Rules for a details-only edit. Read back to check Rules; the save reply does not include them. Never recreate a Tournament to change Rules.

## “Invite an Admin, then cancel a waiting Tournament offer”

Read the chosen scope and sent offers. Ask the person for the exact email. Preview that address, scope and Admin role. Explain that a Tournament offer attempts email through the shared staff invitation sender and that access waits for acceptance. Wait for yes and save one offer. A receipt with `delivery: "sent"` confirms sending, not inbox delivery or accepted staff; `failed` means sending was not confirmed. Do not invite again to repair delivery.

For cancellation, first read current Tournament sent offers and select an exact pending, unexpired ID. A masked address is not a reliable email match; ask for the person's exact row selection or use the app. Preview that ID and Tournament, explain the offer will no longer be usable, then wait for a new yes before one `tournament-admin-invitation-cancel`. Club cancellation uses `club-sent-invitations-list` and `club-admin-invitation-cancel` under the same complete-list approval. Neither removes an accepted appointment.

## “Remove Mira as a Club Admin”

Read `club-staff-list` and select Mira Finch's returned `userId`. Preview the exact Club and person: Mira loses Club Admin access and Club Admin invitations she sent can no longer be accepted; staff history stays, and the Club, Teams and other Admins remain. Under the shared list approval, call `club-admin-remove` once. Only `{ removed: true }` confirms removal. Never use it to leave yourself; do that in the app. Removing another Tournament Admin is not available in the assistant or the app yet. A lost reply stays unknown: read only that affected membership once through a supported authorized item read, or keep it unknown and use the app if none exists, never scan staff lists and never remove again blindly.

## “Delete Cedar Hollow Club — I created it by mistake”

Resolve the exact Club ID and read `club-lifecycle-read`. Show the returned Team/Admin/season/pending-invitation counts and `canDelete`; `teams` includes archived Teams and `invitations` means pending invitations. Do not calculate eligibility yourself or propose/call Delete when `canDelete` is false. If it is true, include the permanent loss of Club setup and finished invitation history, the retained shared deletion record and notes to Admins present at deletion in the complete review. Only the person's yes in their next message allows one `club-delete`; only `{ changed: true }` confirms it.

A refused Delete returns only a code and fixed message, not a list of what uses the Club. Name a use only if the lifecycle read shows `teams > 0` (including archived Teams) or `invitations > 0` (pending invitations); Admins/seasons are normal setup and Overview, Feed and history have no count, so never infer other uses. Offer Archive only for `DELETE_WINDOW_PASSED` or `IN_USE_ARCHIVE_INSTEAD`: it hides the Club from active lists/public results, keeps history and leaves Teams unchanged. For `CLUB_ARCHIVED`, say it is already archived and Restore is the option; other refusals stop without an Archive alternative. Any changed action needs a revised complete review and next-message yes, not the earlier Delete approval. A lost reply is unknown, not a refusal: stop writes and inspect only that Club once with `club-lifecycle-read`, never retry or switch actions automatically.

## “Change the Club Overview welcome section”

Read `club-overview-get` and, for this editing request, `club-overview-editor-get`. If the person asks to edit its long text, read that section with `club-overview-block-body-get`; archived long text uses `club-overview-block-archived-body-get`. Preview the exact changed text, unchanged audience and any order/lifecycle effects. Let the person name a new audience if wanted. Under the shared list approval, send one `club-overview-save` with the exact revision and approved staged changes. Explain permanent loss of the section and long text before any approved deletion. Do not automatically read back. If the save reply is lost, stop writes and inspect authorized current Overview/editor state; never resend or assume rollback.

## “Make a Club Team and enter it in the Tournament”

Read Cedar Hollow Club's Teams before preparing a new Team. Preview the requested Team name, sport, location, season, age group, Private choice and dates/omissions. Explain it permanently belongs to this Club, with no staff appointment, players or invitations added. Wait for yes and create once. Do not adopt or transfer an existing Team. A lost creation reply gets one list re-check, not a second Team; duplicate names or a partial page leave the outcome unknown.

Stop the Tournament-entry part: those assistant tools are not available yet. Use the Hype app's existing Team-entry flow. Never substitute an Admin offer or invent an entry tool.

For a separately requested new Club/Tournament, preview all creation fields and Admin membership effects. Explain that empty Tournament Rules answers leave them unanswered, not defaulted; creation saves no bracket or computed standings. Obtain yes and retain the original creation key/ID. Do not create a duplicate because discovery is incomplete.
