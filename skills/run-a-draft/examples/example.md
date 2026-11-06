# Run-a-draft worked conversation

Use this illustration of the [workflow](../SKILL.md) with the [input reference](../references/reference.md), not as a tool run or approval to save. All names are invented. Use returned records and live schemas, never example IDs.

## Find one draft

**Commissioner:** `/hype:run-a-draft` — Help me run the Meadowbrook League 10U draft.

**Assistant:** I'll check the tools on your signed-in Hype connection first. Starting this skill approves no changes.

_Check live capabilities and schemas. Read one requested `drafts-list` page; show league, division, status and scheduled time. Ask which draft if needed, then read `draft-get`. In this illustration, management access is allowed and the selected draft is scheduled._

**Assistant:** Meadowbrook League, 10U, is not started. The pick order needs attention. The teams are Comets, Falcons and Otters. What order should they pick in?

## Fix the order

**Commissioner:** Falcons, Otters, Comets.

_Read fresh detail; confirm permission and every active draft seat. Retain returned revision and seat references internally._

**Assistant:** Set the full pick order for **Meadowbrook League, 10U**, first pick first?

1. Falcons
2. Otters
3. Comets

This saves the order only; it does not start the draft or draw a random order.

**Commissioner:** Yes, save that order.

_Generate a random UUID with a tool. Send `draft-order-arrange` once with the fresh revision and all active seats in order. Read detail again to verify._

**Assistant:** Saved: Falcons first, Otters second, Comets third.

## Check the clock and start separately

**Commissioner:** Will this wait while I think about each pick?

_In this illustration the clock setting for this existing draft is not exposed in the setup read. Do not mistake that for no clock. Check live recovery tools before offering them._

**Assistant:** It may be timed; this setup read does not show its clock setting. New drafts give each turn 60 seconds by default, plus about one second of grace; when time runs out, the draft pauses and the commissioner is alerted. If the live schema or tool description shows a different default, that wins. A late pick can be refused until the timeout is handled. For a new draft, I can offer no clock only if the live creation options support it. For this draft, check its settings in the Hype app before Start if the timing needs changing. The live tools here support Pause before stepping away and recovery after time runs out; each change needs your approval. If those tools are missing, use the draft in the Hype app at that moment.

**Commissioner:** I checked the app: this draft has a one-minute clock and pauses when time runs out. Start it.

_Read fresh detail. Require no blockers and permission. Treat the commissioner's setting report as context for the warning, never as a substitute for server access checks._

**Assistant:** Start **Meadowbrook League, 10U** now? Starting is final for every coach watching: the rules freeze and the board is built. Usually the first team goes on the clock. If there is nothing to pick, it may go straight to the hat pick or finish and begin sending rosters. Linked players may fill squares automatically. Pause and Undo are available here within their limits, but restarting is not.

**Commissioner:** Yes, start this draft now.

_Generate a new random UUID, send `draft-start` once, then read room and pool. In this illustration status is live, Falcons have round 1, pick 1, and Rowan Finch is available and eligible._

**Assistant:** Picks are running. Falcons are on the clock for round 1, pick 1.

## One pick, with an unclear outcome

**Commissioner:** Pick Rowan Finch for Falcons.

_Read fresh room and pool. Confirm the exact open turn, permission, availability and eligibility. If the turn/action changes, obtain new approval._

**Assistant:** Pick **Rowan Finch for Falcons, round 1, pick 1**, in **Meadowbrook League, 10U**? Coaches see it at once, and linked players may fill later Falcons squares. Undo can remove only the latest pick and its linked placements while the draft is still in an allowed stage; a completed draft cannot be undone.

**Commissioner:** Yes, make that pick.

_Generate a fresh random UUID; send `draft-named-pick` once with room revision, current turn and returned player reference. Retain that exact request/key. In this illustration the reply is lost before the clock expires. Do not pick again. Read room and pool; they do not clearly establish whether the pick saved._

**Assistant:** The reply was lost, and the fresh reads do not clearly show whether Rowan's pick saved. I have not sent another pick. Repeat only the original request, unchanged, so Hype can return its recorded result if it already saved?

**Commissioner:** Yes, repeat only that original request.

_Repeat the exact original request/key, including original revision and turn. Do not substitute fresh fields. In this illustration Hype returns the recorded success. Read room and pool; both confirm Rowan for Falcons in round 1, pick 1._

**Assistant:** Confirmed: Rowan Finch is picked for Falcons, round 1, pick 1. No second pick was made. Otters are now on the clock.

_If the first recovery reads show the saved pick, report without repeating. If a repeat is refused for time running out, do not retry: explain, read the room and offer only discovered recovery tools with separate approval, or use the app. Do not trust pick/end flags alone after expiry. Applying a timeout may pause, skip or pick under the saved rules; it is not extra time. Once paused, ask for the supported Resume choice and re-read afterwards for the new turn. Never claim roster delivery from command success or export actual player details/requests to files._
