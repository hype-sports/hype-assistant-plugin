# Run-a-draft worked conversations

Use these illustrations with the [workflow](../SKILL.md) and [input reference](../references/reference.md), not as tool runs or permission. Use returned records and live schemas, never example IDs. Apply the single [clock and recovery rules](../references/reference.md#clock-and-recovery) whenever an answer is unclear or time runs out.

## Draw an order, then install it separately

**Commissioner:** `/hype:run-a-draft` — Draw the pick order for Meadowbrook League, 10U, one team at a time.

_Check tools and versions; find the requested draft with `drafts-list` and read `draft-get`. In this illustration it is scheduled, with Comets, Falcons and Otters. Read room and `draft-order-run-get`; no run is active._

**Assistant:** Start a one-position-at-a-time order draw for **Meadowbrook League, 10U**? Coaches watching will see each revealed position. Starting the draw does not replace the saved pick order. Each reveal and saving the final order will need a separate yes.

**Commissioner:** Yes.

_Get a new key from `request-key-new`; call `draft-order-run-start` once with the fresh revision. Retain that original revision. Read room/run for the requested next step._

**Assistant:** The draw is ready. Reveal the first pick position now?

**Commissioner:** Yes.

_Get a new key; call `draft-order-run-reveal` with the current run's next slot, without a revision. In this illustration Falcons are revealed first. Stop; do not reveal another slot from that yes._

**Assistant:** Falcons have first pick. No other positions have been revealed.

_After the commissioner separately requests and approves each remaining reveal, fresh run reads show the complete order: Falcons, Otters, Comets. Do not fabricate the unrevealed order._

**Assistant:** Save this complete pick order for **Meadowbrook League, 10U**?

1. Falcons
2. Otters
3. Comets

This replaces the saved order but does not start the draft.

**Commissioner:** Yes.

_Confirm the draft still has the draw's original revision; get a new key and send `draft-order-run-install` for the current run. Read detail to verify. If the draft changed, follow the recovery rule rather than silently installing at a new revision._

**Assistant:** Saved: Falcons, Otters, Comets. The draft has not started.

_For “randomize the order now” instead, preview that `draft-order-draw` refreshes teams and immediately replaces all draw positions. Do not start a paced run for that request._

## Change settings, then Start under a separate yes

**Commissioner:** Give each turn 90 seconds.

_Read detail. In this illustration, the scheduled draft has a 60-second clock and pause-and-alert policy._

**Assistant:** Change **Meadowbrook League, 10U** from 60 to 90 seconds per turn? Its existing grace time and pause-and-alert setting stay unchanged. This affects every team's turns and does not start the draft.

**Commissioner:** Yes.

_Get a new key and send `draft-settings-update` with only `settings: { clock: { seconds: 90 } }` plus revision/key. Read detail; in this illustration the clock is now 90 seconds._

**Assistant:** Saved: 90 seconds per turn.

**Commissioner:** Start it.

_Read detail again; require no readiness blockers._

**Assistant:** Start **Meadowbrook League, 10U** now? Starting is final for every coach watching: the rules freeze and the board is built. Usually the first team goes on the clock; if there is nothing to pick, the draft may go straight to Hat picks or finish and begin sending rosters. Linked players may fill squares automatically. This draft gives each turn 90 seconds, then its saved grace period, and pauses and alerts you when time runs out. Pause and Undo have limits; there is no restart here.

**Commissioner:** Yes.

_Get a new key, send `draft-start` once, then read room/pool. Report the returned state, not roster delivery._

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

## Paced Hat: one marked group per approved draw

**Commissioner:** Run the Hat pick slowly.

_Read room and `draft-hat-run-get`; in this illustration the draft is in Hat stage and this caller is commissioner._

**Assistant:** Start the paced Hat run for **Meadowbrook League, 10U**? Only players marked Hat pick are drawn, not everyone who missed evaluations. The app draws one marked Hat group about every 5 seconds, with linked players kept on the same team and roster limits respected. Placements are visible and final. Here, each group draw needs a separate yes; for continuous timed presentation, do this in the app because its screen controls drive that pace. Starting this run does not approve drawing every group.

**Commissioner:** Yes.

_Get a new key and send `draft-hat-run-start` once. Read room/current run; do not draw from the Start approval._

**Assistant:** The run is ready. Draw the next marked Hat group now? Hype chooses the group; I cannot see the hidden remaining order.

**Commissioner:** Yes.

_Get a new key; send `draft-hat-draw` with that current run and next ordinal, no revision. Report returned placed/unplaced counts and use room for any allowed labels. Stop before another draw. Overflow means players remain unplaced; do not claim a roster was delivered._

_For an explicit request to place all marked Hat players at once, explain the difference and separately confirm `draft-hat-pick`; never silently replace a paced run with it._

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

**Assistant:** **What this affects:** Delete the **Meadowbrook League, 12U** draft for everyone? This permanently removes the draft. The teams and players themselves are not deleted. It cannot be undone, and the fact it existed stays in history. The division will be free for a new draft. Hype allows this only while unused, before Start and within its first 30 days.

**Commissioner:** Yes.

_Get a new key and send `draft-delete` with current revision. Report the returned deletion receipt. If the answer is unclear, follow the single recovery rule; a not-found read alone does not prove deletion. Never turn a refused Delete into an automatic Cancel or Archive._
