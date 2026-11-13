# Review an own saved tryout ranking

This illustrates the [main workflow](../SKILL.md) and [result rules](../references/results.md), not a live run or permission to fetch or save anything.

**Person:** /hype:review-evaluations Who did I rate highest at tryouts?

Read the person's own saved headers after checking the connection, versions and live schemas. Resolve the selected set without guessing a title or treating a dataset ID as an evaluation ID. Ask whether to use saved history without refreshing players, or open a current sheet with its separate refresh warning and yes. Suppose the person chooses saved history and asks for Calculated average, highest first.

For illustration, a permitted own-history read contains three categories and these observed points:

| Player | Observed category points | Calculated average | Observed/total |
| --- | --- | --- | --- |
| Robin Lane | 8, 7 | 3.75 stars, provisional | 2/3 |
| Avery Moss | 8, 7 | 3.75 stars, provisional | 2/3 |
| Quinn Reed | 0 | 0 stars, provisional | 1/3 |
| Unavailable name | none | No calculated score; unranked | 0/3 |

Calculate Robin and Avery as `(8 / 2 + 7 / 2) / 2`, not divided by all three categories. Preserve their tie. Quinn's observed zero counts; blank or skipped categories do not. Keep any Hand-set score separate and do not recover the unavailable name from another list.

**Person:** Save that as a CSV.

Preview the chosen own saved set, exact columns, destination and unavailable fields, excluding written notes unless requested. Wait for a separate yes before saving. Quote fields and neutralize formula-leading text as the reference requires. Do not upload or send the file. If this were a received share, offer an on-screen ranking only, not a file or a re-share.

## Read who came without changing anything

For “who came to tryouts,” use `evaluation-attendance-read` for the exact evaluation and event, joining participant IDs only to the same evaluation's permitted player list. Explain “not marked came” rather than asserting absence. If asked to mark or clear a player, hand off to `/hype:run-evaluations`; this review never calls `evaluation-attendance-set`.
