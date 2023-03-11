# mbw-helpers
Collections of builder helpers to help you develop a mb: warband mod and make code more readable

Requires python 2.7 or above.

Recommended to be used alongside with vscode as your IDE, it will help you a lot.

## Example
Want to see how it works? Here is an example of how to use the dialog builder based on native where lord first time meet the player.

```python
from DialogBuilder import DialogBuilder

dialogs = [
    DialogBuilder()
        .partner(anyone) # or .partner([anyone, plyr]) if you want to make a player response/choice
        .pre_state("start") # or .state("start", "lord_start") to set the pre_state and post_state
        .condition([
            (troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
            (eq, "$g_talk_troop_met", 0),
            (ge, "$g_talk_troop_faction_relation", 0),
            (le,"$talk_context",tc_siege_commander),
        ])
        .dialog("Do I know you?")
        .post_state("lord_meet_neutral") # if you don't pass the post_state it will automatically set it to "close_window"
        .build() # you don't need to call .condition() or .consequence() if your dialog doesn't have any, they automatically return an empty list
    # let's build the dialog responses
    DialogBuilder()
        .partner([anyone, plyr])
        .state("lord_meet_neutral", "lord_intro")
        .dialog("I am {playername}.")
        .build()
    DialogBuilder()
        .partner(plyr) # or just plyr, it will automatically convert it to [anyone, plyr] by the builder
        .state("lord_meet_neutral", "lord_intro")
        .dialog("My name is {playername}. At your service sir.")
        .build()
    # and so on...
]

# From that, I guess you know how to build another dialog and it's responses.
# That if you're using python 2.7, and standard mod development workflow. In modern development workflow, you can't use below inside the dialogs list, but, in exchange you can do even better:

dialogs.extend( # append [[dialog], [dialog], [dialog]...] from .done() to the dialogs list variable
    DialogBuilder()
        .start() # optional, it only used to make the code more readable and doesn't do anything
            .partner(anyone)
            .state("start", "lord_start")
            .condition([
                (troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                (eq, "$g_talk_troop_met", 0),
                (ge, "$g_talk_troop_faction_relation", 0),
                (le,"$talk_context",tc_siege_commander),
            ])
            .dialog("Do I know you?")
            .append() # append to list of dialogs property/variable within the builder itself
            # start building player responses
            .replies_start() # if you don't pass any parameter, it will automatically set the post_state of the previous dialog as the pre_state of the player response. It also automatically set the partner to [anyone, plyr]
                #.condition()
                .reply("I am {playername}.", "lord_intro") # dialog and post_state, if you don't pass the post_state it will automatically set it to "close_window"
                #.consequence() # Pass False to .reply() third parameter to enable consequence
                .reply("My name is {playername}. At your service sir.", "lord_intro")
            .replies_end() # end building player responses, it doesn't nothing and only used for readability
        .end() # optional
        .start() # optional
            # a new dialog here, and maybe another player responses
        .end() # optional
        # and so on...
        .done() # return the list of dialogs: [[dialog], [dialog], [dialog]...]
)
```

## TODO
Not all of the todos are going to be worked on, most of them are just ideas. I will only work on the ones that I need for my mod or important ones. If you want to help, feel free to make a pull request.

- [x] Dialog builder*
- [ ] Tuple Operation builder* (In progress)
- [ ] Animation builder
- [ ] Faction builder*
- [ ] Game Menu builder
- [ ] Info Page builder
- [ ] Item builder*
- [ ] Map Icon builder
- [ ] Mesh builder
- [ ] Mission Template builder
- [ ] Music builder
- [ ] Particle System builder
- [ ] Party Builder*
- [ ] Party Template builder*
- [ ] Postfx builder
- [ ] Presentation builder
- [ ] Quest builder
- [ ] Scene Prop builder
- [ ] Scene builder
- [ ] Script builder*
- [ ] Simple Trigger builder
- [ ] Skill builder
- [ ] Skin builder
- [ ] Sound builder
- [ ] String Table builder*
- [ ] Tableau Material builder
- [ ] Trigger builder
- [ ] Troop builder
- [ ] Variable builder