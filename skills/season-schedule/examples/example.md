# Season-scheduling examples

Apply the [season-schedule workflow](../SKILL.md); check actual rows before approval. Treat names as neither saved references nor permission to create anything. Team lists and saved Place/Field reads exist today, but shared-game saved-Field attachment is missing. Keep whole-season plans unsaved; these calculations do not prove live saving. Obtain a separate explicit yes for each one-game change.

## Twelve teams, once each

The Juniors division has teams Aster, Birch, Cedar, Dahlia, Elm, Fern, Grove, Hazel, Iris, Juniper, Linden, and Maple. The commissioner selects the league's saved North Park Fields 1 and 2, Saturdays from April 3 through June 19, 2027, `America/Chicago`, 60-minute games, 15-minute gaps, and three slots per Field: 09:00, 10:15, 11:30. Every pair meets once, at most one game per team per day, and May 15 is a league day off. Confirm team days off and Field closures too; never assume their absence in an actual run.

There are **66 games**, **11 games per team**, **11 rounds of six games**, **no byes**, and each team has **six Home/five Away or five Home/six Away** games. Twelve Saturdays minus May 15 leave eleven playing dates with six slots each: exactly 66 slots before any other exclusions or existing bookings. No spare capacity is promised. Totals are balanced; runs of Home or Away games can be long.

With the listed team order and the skill's circle rotation and side assignment, the first date is:

| Date | Zone | Start–end | Saved Place / Field | Home | Away |
| --- | --- | --- | --- | --- | --- |
| 2027-04-03 | America/Chicago | 09:00–10:00 | North Park / Field 1 | Maple | Aster |
| 2027-04-03 | America/Chicago | 09:00–10:00 | North Park / Field 2 | Linden | Birch |
| 2027-04-03 | America/Chicago | 10:15–11:15 | North Park / Field 1 | Juniper | Cedar |
| 2027-04-03 | America/Chicago | 10:15–11:15 | North Park / Field 2 | Dahlia | Iris |
| 2027-04-03 | America/Chicago | 11:30–12:30 | North Park / Field 1 | Elm | Hazel |
| 2027-04-03 | America/Chicago | 11:30–12:30 | North Park / Field 2 | Fern | Grove |

This shows one date, **not** the complete approval plan. Show all 66 rows before actual saving, use returned saved references rather than invented IDs, and pass the skill's checklist. If Field 1 closes April 10, capacity drops to **63**: show three unplaced games and ask what to change, rather than squeezing them in or saving an unreviewed partial plan.

## Twice each

Twelve teams meeting twice means **132 games**, **22 per team**, **11 Home and 11 Away**. Reverse each first meeting's sides. It cannot fit the same 66 available slots; do not silently extend dates or remove games.

## Seven teams and byes

One meeting means **21 games**, **7 rounds**, **6 games and one bye per team**, with **3 Home and 3 Away**. Twice means **42 games**, **12 per team**, **6 Home and 6 Away**, and **two byes per team**. Byes never create events.

## A stopped save, if saved-Field support is added

Do not start this path with today's text-only tools. For a stopped 66-new-game run with **23 confirmed, one unknown and 42 not attempted**, report exactly those counts, not “24 saved” or “failed, starting over.” Preserve the progress file and original request IDs; reconcile and resume only through the skill's deliberate recovery steps. Twelve teams is an example, not a product cap. After reconciling the unknown through fresh reads, ask for a decision; do not automatically resend it or continue to the next game. A previous whole-plan yes is not approval for another write.

## One correction, one new yes

The commissioner asks to move Aster versus Birch to 10:15–11:15 on the same date. Read the exact shared game ID/revision through either admitted team's `team-events-list`, check relevant occupancy, then show the old and proposed time, zone, teams and effects on both schedules. Wait for an explicit yes before calling `shared-game-update` once with that revision and a tool-generated operation UUID. Read back both schedules; do not claim changed times solely from the write receipt.

For a later cancellation, read the current revision again, explain that the event and answers remain and any cancellation note is visible to event readers, then wait for another explicit yes before `shared-game-cancel`. Read back the cancelled status on both schedules. Do not delete, recreate or choose a notice.

If the commissioner asks to undo that cancellation, read the same game's current revision and check occupancy again. Show the exact game and explain that restore keeps its audiences/answers, clears the cancellation note and returns it to scheduled. If it has not ended, Hype sends a quiet restored notice to eligible audience members except the person restoring it; ended games and exact replays send none. Ask for one new explicit yes, then call `shared-game-restore` once with `pathParams: { id: eventId }` and `body: { opId: freshToolKey, expectedRevision: observedRevision }`. Read back both schedules. After any unclear change, follow step 9's recovery rules; never blindly resend.

## Missing information stays visible

For an unresolved draft opponent, show **TBD**, never blank. Stop shared-game saving until both exact eligible teams are known. If a family's read withholds the other team's identity, preserve that boundary; do not fill it from the commissioner's view or promise a hidden game will appear for the family. Explain missing access and tool failures in plain words, without error codes.

## Time changes need clarification

A proposed 01:30 start on a daylight-saving fallback date can describe two instants. Ask which instant is intended and check the chosen zone before review; do not silently pick one. Show unplaced games when a closure leaves too few slots, and obtain new whole-plan review plus a separate per-game yes after constraints change.
