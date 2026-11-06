# Club and Tournament examples

Follow the [workflow](../SKILL.md) and [tool reference](../references/tools.md). Present invitation choices neutrally and report only returned fields.

## “Which Clubs and Tournaments do I run?”

Read `my-clubs-list` after checking the live tool/schema. If Cedar Hollow Club has `season_name: "Spring 2027"`, report that as its current season. If another Club's season is null, say it is not shown. If `nextCursor` is present, explain more Clubs may remain and ask before the next page. A failed page is unverified, not an empty directory.

Explain: “I can list your Clubs, but a list of the Tournaments you run isn't available yet. If an existing saved link or a confirmed creation/acceptance gives the Tournament's ID, I can review that Tournament.” Do not promise an app list. With a trusted ID, read `tournament-details-read`; never guess an ID from “Cedar Spring Classic” or use pending invitations as a list of administered Tournaments.

## “Who is on Cedar Hollow Club's staff? Which offers are waiting?”

Resolve the Club's exact ID. Read `club-staff-list` and `club-sent-invitations-list` separately. Report Mira Finch as an accepted Admin only if the staff list says so. Report pending offers separately using their returned IDs, status and expiry. If an offer's email is null, say its address is hidden; never fill it from an earlier invite or infer it from the single staff name. A Team list is not a roster or a list of staff appointments.

## “Accept my invitation to Cedar Spring Classic”

Read `my-tournament-admin-invitations-list`. It only lists offers still waiting for the person, leaves expired ones out and changes nothing.

Select the returned exact offer, Tournament and expiry; distinguish repeated names by IDs. Never recommend accepting or declining or call the offer low-risk because of its name or text. The person has chosen accept in this example. Then preview: “Accept this Admin invitation for Cedar Spring Classic, offer [returned invitation ID]? This grants Admin access to this Tournament, and the answer is final.” Wait for a separate yes before one `tournament-admin-invitation-answer` with `answer: "accept"`. Use `status: "accepted"` and the returned Tournament ID to report confirmed acceptance. Club acceptance follows the equivalent Club tools; a pending invitee needs no Club staff access to answer.

For decline, preview that exact offer with the final decline effect and wait for its own yes. A vanished row after an unclear reply proves neither answer. Re-read the personal invitation list once; report current state and keep the original outcome unknown if no exact receipt confirms it. Never answer a second time to find out.

## “Change Cedar Hollow Club's city”

Read fresh Club details and preserve the returned name, sports, state and Private choice. Show the old city and proposed new city, required unchanged fields and “Current season: unchanged.” Wait for yes before one `club-details-update` using the exact saved revision. Then read back the same ID and report only returned fields. A Club city read says nothing about its Team's city; no tool here reads that Team field. A revision conflict requires a new read, comparison and yes; do not overwrite another Admin's change.

For a Tournament, preserve all details, including dates and explicit nulls: omitting an old date can clear it. Do not send Rules answers in a details edit or silently invent a replacement Tournament.

## “Invite an Admin, then cancel a waiting Tournament offer”

Read the chosen scope and sent offers. Ask the person for the exact email. Preview that address, scope and Admin role. For a Tournament offer explain that no email is sent (a Club offer emails the address once) and that access waits for acceptance. Wait for yes and save one offer. A receipt with `delivery: "inactive"` means saved and waiting, not email sent or accepted staff. Do not invite again to repair delivery.

For cancellation, first read current Tournament sent offers and select an exact pending, unexpired ID. A masked address is not a reliable email match; ask for the person's exact row selection or use the app. Preview that ID and Tournament, explain the offer will no longer be usable, then wait for a new yes before one cancellation. An accepted appointment cannot be removed this way. Club Admin-offer cancellation and Club deletion are not available in the assistant or app; do not offer the app as a workaround.

## “Make a Club Team and enter it in the Tournament”

Read Cedar Hollow Club's Teams before preparing a new Team. Preview the requested Team name, sport, location, season, age group, Private choice and dates/omissions. Explain it permanently belongs to this Club, with no staff appointment, players or invitations added. Wait for yes and create once. Do not adopt or transfer an existing Team. A lost creation reply gets one list re-check, not a second Team; duplicate names or a partial page leave the outcome unknown.

Stop the Tournament-entry part: those assistant tools are not available yet. Use the Hype app's existing Team-entry flow. Never substitute an Admin offer or invent an entry tool.

For a separately requested new Club/Tournament, preview all creation fields and Admin membership effects. Explain that empty Tournament Rules answers leave them unanswered, not defaulted; creation saves no bracket or computed standings. Obtain yes and retain the original creation key/ID. Do not create a duplicate because discovery is incomplete.
