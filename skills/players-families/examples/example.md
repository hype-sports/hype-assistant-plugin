# Parent/guardian examples

These conversations use invented details and describe expected decisions, not executed actions. IDs stand for exact IDs returned by authorized reads, never literal inputs or guesses.

## Add my child

**Person:** Add my child, Rowan Example.

**Assistant:** I'll check your managed players first so we don't add a duplicate. I won't save anything yet.

After the tool-version check, inspect the live `player-profile-create` schema and read `my-player-profiles-list`. No returned profile matches the person’s intended child; clarify any ambiguity rather than treating a matching name as proof of identity.

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

The live tools are available. `my-player-profiles-list` identifies the selected profile; `player-profile-registrations-list` returns the exact linkable registration. The person already manages the profile and has independent parent/guardian standing on that registration.

**Assistant:** Link Maya Example's selected profile [returned profile ID] to the selected registration [returned registration ID] in Cedar Example League [returned league ID]? This immediately gives the profile's other managing parents/guardians access to that registration and notifies league staff and profile managers. It may also link eligible draft-assigned team spots where you are already a parent/guardian and no profile is linked; it won't add anyone to a team. Shall I make this exact link?

**Person:** Yes.

Call `league-player-profile-link` once with the approved returned league, registration and profile IDs, using its full live name and schema. A valid result returns the exact linked registration and profile IDs.

**Assistant:** The selected profile is linked to that registration. I haven't sent an invitation, accepted another offer or added anyone to a team.

If the reply were lost instead, stop: say the link may have happened, never repeat it or claim failure. Ask whether the person wants a separate authorized current registration read; current state cannot prove what the lost call did. Any new change needs a fresh review and yes.
