# One approved evaluation action at a time

These conversations illustrate the [main workflow](../SKILL.md); they are not tool runs, receipts or approval.

## Mark one player's attendance

**Person:** Mark Robin Lane as came at Saturday's tryout.

1. Check the signed-in connection, tool versions and live schemas. Resolve the exact evaluation through `private-evaluations-manageable-list`, even if the person has no private sheet. Resolve Saturday's exact event through permitted event discovery and confirm its evaluation with event context. Ask which date or player if ambiguous.
2. Require current permission to edit this evaluation's player list; only its current editors can read or mark attendance, and Hype checks every call. Read `private-evaluation-players-list` and `evaluation-attendance-read` for that evaluation/date. Match Robin by the permitted list's participant identity, not a registration ID. Confirm that this exact date has started before offering to mark or clear attendance; otherwise stop. Suppose the date has started and the returned attendance is not marked came.

**Assistant:** Robin Lane is not marked came at Saturday's tryout in Spring Skills. Mark Robin as came for that date? This changes shared attendance for this evaluation date, not private scores, notes, player lists or RSVPs.

**Person:** Yes.

3. Call `request-key-new` once. Call `evaluation-attendance-set` once with the exact event, participant, `came: true` and returned key. Do not mark anyone else under this yes.
4. If the matching acknowledgement confirms the mark, report that Robin is marked came for that date. Do not claim the draft changed or a message was sent. For a clear request to remove that mark, repeat the read/preview/yes flow with `came: false` and a new key for that new change.

If the reply is lost, say the outcome is unknown and stop. Keep the original request/key. Only after a separate request, read attendance for the same evaluation/date. Do not resend automatically or use the private-score receipt lookup.

## Start through Division Admin authority

**Person:** Start a Saturday evaluation for the division I administer.

Resolve the exact active division and selected players through permitted reads. Agree the title, date, time zone, players and categories; do not infer scoring admission from the appointment.

**Assistant:** This will create Spring Skills, its all-day Saturday date and player list/numbers in the selected division. Through your Division Admin authority, Hype returns a management receipt, not a private scoring sheet or categories, and it does not give you scoring access. It saves no scores, shares nothing and sends no notice. Create exactly this evaluation?

Wait for a separate yes to the complete preview. Then get a key and call `division-evaluation-create` once with the agreed inputs. Report only the returned management result; do not invent a dataset ID or open a private sheet.
