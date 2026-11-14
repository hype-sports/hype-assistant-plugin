# Run-a-draft worked conversations

Use these illustrations with the [workflow](../SKILL.md), [input reference](../references/reference.md) and [request-key rules](../references/reference.md#request-keys), not as tool runs or permission. Use returned records and live schemas, never example IDs. If the key tool is missing or fails, stop; never invent a key. Apply the single [clock and recovery rules](../references/reference.md#clock-and-recovery) whenever an answer is unclear or time runs out.

## Draw every requested position under one yes

**Commissioner:** Draw the pick order for Meadowbrook League, 10U, one team at a time, then save the resulting random order.

Check tools and versions; find the exact scheduled draft and read detail, room and current run. In this illustration it has Comets, Falcons and Otters, with no active run. Show the whole sequence once:

1. Start the order draw; this does not replace the saved order.
2. Reveal positions 1, 2 and 3 in order, one call per position. Their random contents are unknown before reveal, and watching coaches see the results.
3. Install that resulting random order, replacing the saved order without starting the draft.

**Assistant:** Shall I do all those steps, including saving the resulting random order?

**Commissioner:** Yes.

Get a new server key for Start and retain its original draft revision. Read the confirmed run, then reveal each reviewed next position with its own key and fresh exact run/slot guard, without asking again. Never guess unrevealed teams or advance beyond the listed positions. Suppose the confirmed results are Falcons, Otters, Comets. After all positions are confirmed, install that order with its own key and the draw's original revision; never substitute a newer revision to bypass a conflict. Read detail to verify.

**Assistant:** Saved: Falcons, Otters, Comets. The draft has not started.

A refused Start blocks every reveal and install. A lost reply stops writes for supported current-state inspection. If the original request did not include installing the resulting random order, show the revealed order for a later decision instead; do not silently add Install. For “randomize the order now,” use the separately reviewed `draft-order-draw`, not a paced run.

## Change settings and Start in the same request

**Commissioner:** Give each turn 90 seconds and start the draft.

Read fresh detail and readiness. In this illustration the scheduled draft has a 60-second clock with pause-and-alert, and no blockers. Review both changes together: clock 60 → 90 seconds with the other settings unchanged; then Start, freezing rules, building the board and possibly placing linked players or finishing immediately if no picks remain. Explain the actual grace period, clock effects, audience and Undo limits.

**Commissioner:** Yes.

Call `draft-settings-update` with a fresh key and exact revision, read back the confirmed clock and readiness, then Start with its own new key and fresh valid revision. No second yes. If the settings change is refused, do not start with the old 60-second clock: Start depends on the approved change. A materially changed setting or readiness returns to the shared review. Report returned state, never roster delivery.

## A team's private list is not a pick

**Coach:** Put Rowan Finch first and Avery Vale second on my Falcons list. Remove the other players from that list.

_Read the known draft's room and the explicitly selected accessible Falcons queue using `draft-queue-get`; resolve players through permitted reads. In this illustration this caller can edit Falcons' queue._

**Assistant:** Replace your private **Falcons** pick list in **Meadowbrook League, 10U** with only:

1. Rowan Finch
2. Avery Vale

The other entries will leave this list. This does not pick anyone or change auto-pick. Save it?

**Coach:** Yes.

_Get a new key; send `draft-queue-reorder` with the complete ordered list, selected seat and queue version—not draft revision. Verify the selected queue._

**Coach:** Who's on the clock? Pick Rowan if it's us.

_Read room and pool; in this illustration Falcons have round 1, pick 1, Rowan is eligible, and the caller is Falcons' current lead._

**Assistant:** Falcons are on the clock for round 1, pick 1. Pick **Rowan Finch** for that turn? Coaches see it at once, and linked players may fill later Falcons squares. Undo can remove only the latest pick and linked placements in an allowed stage; completed drafts cannot be undone.

**Coach:** Yes.

_Get a new key; send `draft-pick` once with the current turn, revision and returned player reference. A commissioner explicitly picking for the current team would use `draft-named-pick` instead; never substitute it after a coach's refusal._

## Multiple Hat draws, not an invented timer

**Commissioner:** Start the Hat run and draw the next two marked groups, one after another.

Read room and `draft-hat-run-get`; confirm commissioner access, Hat stage and enough remaining groups where the returned state establishes it. Review Start and the next two group draws together. Explain random group selection, linked placements, roster limits, immediate visibility and Undo limits; do not claim to know hidden players or order. State that assistant calls do not drive an automatic timed presentation; continuous paced presentation stays in the app.

**Commissioner:** Yes.

Call Start once with its new server key, read the confirmed run, then make the two reviewed draws sequentially with fresh exact run/ordinal reads and separate keys. No additional yes per group. Stop dependent draws after a refusal or changed stage; an unknown reply stops writes. Report only returned counts and allowed room labels. Overflow means players remain unplaced, not delivered rosters. Never draw more groups than reviewed.

For an explicit request to place all marked Hat players at once, include the visible final-placement effects of `draft-hat-pick` in the shared review instead; never silently substitute it for a paced run.

## A Save withdrawal may leave the player saved

**Commissioner:** Withdraw Rowan's Falcons Save.

_Read detail to identify that Save. In this illustration “Always save coaches' players” is on and Rowan has a coach's-player link._

**Assistant:** Withdraw **Rowan Finch's Falcons Save** in **Meadowbrook League, 10U**? Hype may refuse an automatic Save. With “Always save coaches' players” on, withdrawing a hand-made Save may leave Rowan saved automatically. This changes who Falcons gets; I will check the returned Saves before saying Rowan is unsaved.

**Commissioner:** Yes.

_Get a new key and send `draft-save-withdraw` with the Save reference and current revision. In this illustration it succeeds but the returned list still includes Rowan under a new automatic Save._

**Assistant:** The hand-made Save was withdrawn, but Rowan is still saved for Falcons automatically. I have not changed the coach link or the rule.

## Delete: explain what goes, not a restart

**Commissioner:** Delete the unused Meadowbrook 12U draft I just created by mistake.

_Find that exact draft and read detail. In this illustration it is scheduled and Hype's current delete flag allows the action._

**Assistant:** **What this affects:** Delete the **Meadowbrook League, 12U** draft for everyone? The app's confirmation says: “This permanently removes the draft. The teams and players themselves are not deleted. It cannot be undone, and the fact that it existed stays in the history. A draft can be deleted only in its first 30 days, before it starts.” The tool also requires it to be unused; deletion frees the division for a new draft.

**Commissioner:** Yes.

_Get a new key and send `draft-delete` with current revision. Report the returned deletion receipt. If the answer is unclear, follow the single recovery rule; a not-found read alone does not prove deletion. Never turn a refused Delete into an automatic Cancel or Archive._
