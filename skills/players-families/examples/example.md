# Link a player profile

This short conversation uses invented names and describes expected decisions, not a record of executed actions. IDs below stand for exact IDs returned by authorized reads, never literal inputs or guesses.

**Person:** Link Maya Example's profile to my registration in Cedar Example League.

**Assistant:** I'll check the available tools and your managed profiles, then the registrations you are allowed to link. I won't change anything yet.

The live tools are available. `my-player-profiles-list` identifies the selected profile; `player-profile-registrations-list` returns the exact linkable registration. The person already manages the profile and has independent parent/guardian standing on that registration.

**Assistant:** Link Maya Example's selected profile [returned profile ID] to the selected registration [returned registration ID] in Cedar Example League [returned league ID]? This immediately gives the profile's other managing parents/guardians access to that registration and notifies league staff and profile managers. It may also link eligible draft-assigned team spots where you are already a parent/guardian and no profile is linked; it won't add anyone to a team. Shall I make this exact link?

**Person:** Yes.

Call `league-player-profile-link` once with the approved returned league, registration and profile IDs, using its full live name and schema. A valid result returns the exact linked registration and profile IDs.

**Assistant:** The selected profile is linked to that registration. I haven't sent an invitation, accepted another offer or added anyone to a team.

If the reply were lost instead, stop: say the link may have happened, never repeat it or claim failure. Ask whether the person wants a separate authorized current registration read; current state cannot prove what the lost call did. Any new change needs a fresh review and yes.
