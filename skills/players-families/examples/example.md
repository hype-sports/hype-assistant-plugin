# Players & Families examples

These conversations use invented details and describe expected decisions, not executed actions. Keep exact returned IDs inside tool calls; speak in names and recognizable labels, never raw record IDs. Clarify ambiguous matches before proposing a change.

## Add my child

**Person:** Add my child, Rowan Example.

**Assistant:** I'll check your managed players first so we don't add a duplicate. I won't save anything yet.

After the tool-version check, inspect the live `player-profile-create` schema and read `my-player-profiles-list`. In this example, that list is empty. If profiles were returned, ask whether the child is already listed rather than deciding from a matching name alone.

**Assistant:** What is Rowan's birth date?

**Person:** March 14, 2017.

**Assistant:** Create a player profile for Rowan Example, born March 14, 2017, with you as a managing parent/guardian? This won't register Rowan in a league, add a team spot or invite anyone. No optional details will be added. Shall I save this exact profile?

**Person:** Yes.

Call `player-profile-create` once with `catalogVersion: 1` and `body: { firstName: "Rowan", lastName: "Example", dateOfBirth: "2017-03-14" }`. Supply no pathParams or query. Keep the returned `{id}` as this profile's authoritative ID.

**Assistant:** Rowan's profile was created with you as a managing parent/guardian. I haven't registered Rowan, added a team spot or invited anyone.

If the reply is lost, stop without creating again; it may already have saved. Ask before a separate managed-player read. Current state cannot prove what the lost call did, and another create may duplicate the profile.

## Link a player profile

**Person:** Link Maya Example's profile to my registration in Cedar Example League.

**Assistant:** I'll check the available tools and your managed profiles, then the registrations you are allowed to link. I won't change anything yet.

`my-player-profiles-list` identifies the selected profile; `player-profile-registrations-list` returns one unambiguous linkable registration for this request. The person already manages the profile and has independent parent/guardian standing on that registration. Keep the returned IDs for the call, not the review text.

**Assistant:** Link Maya Example's profile to Maya's registration in Cedar Example League? This immediately gives the profile's other managing parents/guardians access to that registration and notifies league staff and profile managers. It may also link eligible draft-assigned team spots where you are already a parent/guardian and no profile is linked; it won't add anyone to a team. Shall I make this exact link?

**Person:** Yes.

Call `league-player-profile-link` once with the approved returned league, registration and profile IDs, using its full live name and schema. Report only the confirmed result; `registrationLinked: false` is still a successful repair, not an undo token.

**Assistant:** Maya's profile is linked to that registration. I haven't sent an invitation, accepted another offer or added anyone to a team.

If the reply were lost, say the link may have happened, never repeat it or claim failure. Ask before a separate authorized current registration read; current state cannot prove what the lost call did. Any new change needs a fresh review and yes.

## Coach: approve one request, decline another

**Person:** Show parent/guardian requests for Cedar Example Stars.

Find the exact team through `my-home-entities-list` or a requested public `team-search`, then read `team-guardian-requests-list` using that team's ID. In this example, it returns two pending individual rows from Casey Example, one for Rowan Example and one for Maya Example. Keep each row's ID inside tool calls.

**Assistant:** Casey Example has waiting requests for Rowan Example and Maya Example on Cedar Example Stars. I haven't answered either.

**Person:** Approve the request for Rowan.

**Assistant:** Approve Casey Example as a parent/guardian of Rowan Example on Cedar Example Stars? This gives Casey access to Rowan on this team, with any profile-link and notice effects that apply. It answers only Rowan's request; Casey's request for Maya stays waiting. Shall I approve Rowan's request?

**Person:** Yes.

Call `guardian-request-approve` once with Rowan's selected request ID. Continue only after its confirmed `approved` outcome; `already` means no new access was added.

**Assistant:** Casey's request for Rowan was approved. I haven't answered the request for Maya.

**Person:** Decline the request for Maya.

**Assistant:** Decline Casey Example's request for Maya Example on Cedar Example Stars? Hype keeps the declined request, tells Casey once without naming the coach, and allows Casey to ask again. It sends no email and grants no access. Shall I decline it?

**Person:** Yes.

Call `guardian-request-decline` once with Maya's selected request ID; `{}` confirms success. Never substitute a group ID or answer another row automatically.

**Assistant:** Casey's request for Maya was declined. I haven't changed Rowan's approved access.

## League admin: read a player, then review a resend

**Person:** Show Rowan Example's registration in Cedar Example League.

Find the league/division in `my-home-entities-list`, select the exact registration from one requested player-list page, then use `division-player-read` with that registration and division. In this example, the commissioner receives a joined guardian named Morgan Example. Keep the returned user ID out of the response.

**Assistant:** Rowan Example is registered in Cedar Example League's Junior division. Morgan Example is listed as a parent/guardian.

**Person:** Resend the pending invitation I selected in Hype for Rowan's other parent, Casey Example.

The person has identified the exact pending offer and recipient from the app; never infer either from the list order. An authorized invitation read confirms the pending offer but returns no email outcome. No first-email result is known from this conversation.

**Assistant:** Resend the existing invitation you selected for Casey Example to join Rowan Example's registration in Cedar Example League? I can't tell whether the first email went out. A resend could arrive twice. Shall I make another attempt?

**Person:** Yes.

Get a new key from `request-key-new` for this approved new resend and call `league-guardian-invitation-resend` once with the exact invitation ID and `body: {idempotencyKey}`. Keep the key with its inputs; never get another key to repair a lost answer. In this example, the confirmed response is `email: "sent", replayed: false`.

**Assistant:** Hype reports the resend was accepted by the email service. That does not prove it reached Casey's mailbox or that Casey accepted the invitation.

If the response were lost, stop and say the resend may have happened. Never repeat it automatically or claim that reading the pending offer proves what happened to the email.
