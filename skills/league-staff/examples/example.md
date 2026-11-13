# League staff examples

Use these invented scenarios as guidance, not a live-run record. Do not copy contacts into messages. For the person's own files and progress record, follow [Your own files stay where you keep them](../../league-setup/references/own-files.md).

## Invite a Commissioner

The person asks to invite Alex Example as Commissioner of Riverside Youth League. Resolve the exact league and current staff through authorized reads. Ask for the address directly, without account lookup. Prepare only `title: "commissioner"`, `makeOwner: false` and the supplied address for that league.

Before writing: explain that the offer grants no access until Alex accepts in Hype, attempts email, and replaces an older pending offer to the same address. Echo the supplied address only to the caller who entered it in this immediate approval, or use its unambiguous supplied-address reference. Ask for an explicit yes in a later turn to this exact invitation. Only then get a fresh key from `request-key-new` and call once with it as `idempotencyKey`.

A result with an invitation ID and `email: "not_sent"` means: “Alex is invited, waiting for their answer. The invitation was created, but email was not sent.” Do not invite again to fix delivery. Do not say “Alex was added.”

## Invite an Admin with a separate title

The caller requests an Admin invitation for Sam Vale with the display title Registrar. Read current authorized scope/staff; review **Admin: yes; Title: Registrar**, exact league and directly supplied address. Explain that the Admin grant is independent of the title and begins only on recipient acceptance. After later-turn yes, get a fresh key and call `league-staff-invite` once with `makeOwner: true` and the approved title. Never silently turn an ordinary Commissioner offer into an Admin offer.

## Change a label without removing membership

Alex is a League Admin and wants the Commissioner label removed. Read the exact member and show old/new title with Admin unchanged. After separate later-turn approval, call `league-staff-update-title` with `title: null`; never call removal. A non-Admin cannot have no title: explain a refusal without removing them or changing Admin rights.

## Invite a Division Admin

The person asks to invite Jamie Reed to Riverside Youth League's Cedar Division. Confirm the exact returned division and containing league; only the containing League's current owner may invite. Explain this is one division's appointment, not Coach or Admin access to its teams.

Explain before the explicit yes: Hype sends no email for this invitation; the person must let Jamie know themselves. A confirmed invite ID means “invited, waiting for their answer,” not appointed. Send no separate message.

## Address-only cancellation must stop

The person asks to cancel an invitation by address. The live list returns only IDs and expiry, with no reliable address mapping. Even if there is just one row, do not guess. Explain that the assistant cannot reliably identify the offer and direct the person to the league's Staff tab in Hype.

With an exact trusted invitation ID and confirmed target/scope/role instead, show who the offer is for only if reliably known, its ID, league/division and the fact that it can no longer be accepted. If the target is uncertain, stop and hand off to the app. Wait for a new explicit yes before cancelling once. Cancellation does not remove an already accepted member.

## Removing staff is a separate decision

Alex appears in the current league staff list as Commissioner. Show the exact returned member ID and Riverside Youth League, and explain that removal ends that League staff membership, not unrelated roles. Wait for an explicit yes. Never remove the last League Admin; a pending offer is not a replacement.

Removing Jamie from Cedar Division ends only that appointment; other divisions and independent roles remain. The last Division Admin may leave themselves if Hype permits; do not invent a last-Division-Admin restriction.

## Leave an own appointment without League access

Jamie asks to leave Cedar Division. Read `my-division-admin-divisions-list`, select the exact returned Cedar appointment and establish Jamie's own `userId` with `my-identity-read`. Do not require League reads or the management list. Review this appointment only, with other roles/history preserved; wait for later-turn yes, then call `division-admin-remove` for that division and own ID once.

## Answer an own invitation

Sam asks to accept the League Admin/Registrar invitation. Through Sam's own connection, read `my-league-staff-invitations-list`; review the exact ID, Riverside Youth League and offered Admin/title facts. After Sam's later-turn yes, call `league-staff-invitation-accept` once. Do not use the sender's connection, require pre-existing League access or read more automatically. A Division Admin recipient uses their own division invitation list and exact accept/decline tool instead. Declining always needs its own exact review/yes and grants no role.

## Lost reply must stop

An approved League staff invite returns `WRITE_OUTCOME_UNKNOWN`. Say it may have happened; do not retry, invite again, automatically read or run another change. Ask the person to check the league's Staff tab in the app. The contact-free list cannot determine what happened for an address. Do not infer failure from an absent row or claim email delivery. If the person then explicitly asks to retry that same League staff invite, send it once with the SAME key and unchanged inputs; a different email or roles needs a new key.

## Hidden is not empty

`league-staff-list` returns `viewerIsOwner: false` and an empty invitation list. Say pending invitations are not visible to this caller, not that there are none. A refused division list means that division's Admins are unverified, not zero. Null names or repeated names require exact IDs and clarification before a change.
