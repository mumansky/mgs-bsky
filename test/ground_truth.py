# Ground truth for all OCR test images.
# Keys are paths relative to the repo root.
# type: "dialogue", "codec", "codec+dialogue", or "none"
# text: expected dialogue/subtitle text (None if no text expected)

GROUND_TRUTH = {
    # ── Original test images (test/) ─────────────────────────────────────────

    # MGS1
    "test/mgs1.jpg":         {"type": "dialogue",       "text": "are you just going to sit by and watch him die?"},
    "test/mgs1_1.jpg":       {"type": "dialogue",       "text": "it's him."},
    "test/mgs1_2.jpg":       {"type": "dialogue",       "text": "Otacon?"},
    "test/mgs1_3.jpg":       {"type": "codec+dialogue", "text": "I shouldn't have pushed her so hard. ...It's all my fault."},
    "test/mgs1_4.jpg":       {"type": "none",           "text": None},
    "test/mgs1_5.jpg":       {"type": "dialogue",       "text": "responsible for everything from strategic thinking..."},

    # MGS2
    "test/mgs2.jpg":         {"type": "none",           "text": None},
    "test/codec.webp":       {"type": "codec",          "text": None},
    "test/mgs2_1.jpg":       {"type": "codec+dialogue", "text": "There was a brand-new hole cut through the oil fence."},
    "test/mgs2_2.jpg":       {"type": "codec",          "text": None},
    "test/mgs2_3.jpg":       {"type": "codec",          "text": None},
    "test/mgs2_4.jpg":       {"type": "dialogue",       "text": "Ignore them."},
    "test/mgs2_5.jpg":       {"type": "dialogue",       "text": "...and clean up the refuse from the exercise."},

    # MGS3
    "test/mgs3.jpg":         {"type": "dialogue",       "text": "I had no choice but to cooperate!"},
    "test/mgs3_1.jpg":       {"type": "none",           "text": None},
    "test/mgs3_2.jpg":       {"type": "codec+dialogue", "text": "Depending on how long you sleep, you may also recover naturally from sickness and injury."},
    "test/mgs3_3.jpg":       {"type": "dialogue",       "text": "Now --"},
    "test/mgs3_4.jpg":       {"type": "dialogue",       "text": "Motorcycle gasoline."},
    "test/mgs3_5.jpg":       {"type": "dialogue",       "text": "We're both slowly being eaten away by the karma of others."},

    # MGS4
    "test/near.webp":        {"type": "dialogue",       "text": "I wanted to be near you..."},
    "test/mgs4_1.jpg":       {"type": "none",           "text": None},
    "test/mgs4_2.jpg":       {"type": "none",           "text": None},
    "test/mgs4_3.jpg":       {"type": "dialogue",       "text": "Let me out of this cage."},
    "test/mgs4_4.jpg":       {"type": "dialogue",       "text": "The only place where they are truly released from the shackles of the Patriots..."},
    "test/mgs4_5.jpg":       {"type": "none",           "text": None},

    # MGS5
    "test/mgs5_1.jpg":       {"type": "dialogue",       "text": "Hang on!"},
    "test/mgs5_2.jpg":       {"type": "dialogue",       "text": "Search over there."},
    "test/mgs5_3.jpg":       {"type": "none",           "text": None},
    "test/mgs5_4.jpg":       {"type": "none",           "text": None},
    "test/mgs5_5.jpg":       {"type": "none",           "text": None},

    # Twin Snakes
    "test/frame.jpg":        {"type": "codec+dialogue", "text": "...maybe now he's finally found some peace."},
    "test/twinsnakes_1.jpg": {"type": "dialogue",       "text": "That female soldier...?"},
    "test/twinsnakes_2.jpg": {"type": "dialogue",       "text": "and supercomputers."},
    "test/twinsnakes_3.jpg": {"type": "codec+dialogue", "text": "Snake, are you okay?"},
    "test/twinsnakes_4.jpg": {"type": "none",           "text": None},
    "test/twinsnakes_5.jpg": {"type": "dialogue",       "text": "Too bad. It looks like your revolution was a failure."},

    # Peace Walker
    "test/peacewalker_1.jpg": {"type": "none",          "text": None},
    "test/peacewalker_2.jpg": {"type": "dialogue",      "text": "IT CAN MOVE ON ITS OWN, AND STEALTH SHIELDS IT FROM RADAR AND SATELLITE DETECTION, DRASTICALLY REDUCING THE RISK OF IT BEING DESTROYED IN A PRE-EMPTIVE STRIKE."},
    "test/peacewalker_3.jpg": {"type": "dialogue",      "text": "AN AGE IN WHICH PEACE WALKER, AN INFALLIBLE NUCLEAR DETERRENT SYSTEM WITH THE PATIENCE AND COLD LOGIC OF A MACHINE, WILL PLAY A VITAL ROLE."},
    "test/peacewalker_4.jpg": {"type": "dialogue",      "text": "BACK WITH HER COMPAS. SHE'LL CATCH UP LATER."},
    "test/peacewalker_5.jpg": {"type": "dialogue",      "text": "From now on, call me Big Boss."},

    # ── Extended test images (test/new/, seed=42) ─────────────────────────────

    # MGS1
    "test/new/mgs1_new_1.jpg":  {"type": "codec+dialogue", "text": "Two F-16s just took off from Galena and are headed your way."},
    "test/new/mgs1_new_2.jpg":  {"type": "none",            "text": None},
    "test/new/mgs1_new_3.jpg":  {"type": "dialogue",        "text": "...No."},
    "test/new/mgs1_new_4.jpg":  {"type": "dialogue",        "text": "All the data collected from this exercise."},
    "test/new/mgs1_new_5.jpg":  {"type": "codec+dialogue",  "text": "I can't allow myself to quit now."},
    "test/new/mgs1_new_6.jpg":  {"type": "dialogue",        "text": "It was inside the pocket of the uniform I was wearing."},
    "test/new/mgs1_new_7.jpg":  {"type": "dialogue",        "text": "Meryl's?"},
    "test/new/mgs1_new_8.jpg":  {"type": "dialogue",        "text": "The man who stole what was rightly mine..."},
    "test/new/mgs1_new_9.jpg":  {"type": "dialogue",        "text": "the only thing I was good at."},
    "test/new/mgs1_new_10.jpg": {"type": "codec+dialogue",  "text": "He fought with every ounce of strength in his body."},

    # MGS2
    "test/new/mgs2_new_1.jpg":  {"type": "none",           "text": None},
    "test/new/mgs2_new_2.jpg":  {"type": "none",           "text": None},
    "test/new/mgs2_new_3.jpg":  {"type": "none",           "text": None},
    "test/new/mgs2_new_4.jpg":  {"type": "none",           "text": None},
    "test/new/mgs2_new_5.jpg":  {"type": "none",           "text": None},
    "test/new/mgs2_new_6.jpg":  {"type": "none",           "text": None},
    "test/new/mgs2_new_7.jpg":  {"type": "codec+dialogue", "text": "Otacon's here for someone -- I'm not."},
    "test/new/mgs2_new_8.jpg":  {"type": "dialogue",       "text": "Human muscles are quite eloquent."},
    "test/new/mgs2_new_9.jpg":  {"type": "none",           "text": None},
    "test/new/mgs2_new_10.jpg": {"type": "dialogue",       "text": "We only wanted to be loved..."},

    # MGS3
    "test/new/mgs3_new_1.jpg":  {"type": "none",           "text": None},
    "test/new/mgs3_new_2.jpg":  {"type": "none",           "text": None},
    "test/new/mgs3_new_3.jpg":  {"type": "dialogue",       "text": "Volgin's father was in charge of the Philosophers' money laundering activities."},
    "test/new/mgs3_new_4.jpg":  {"type": "codec+dialogue", "text": "Uh huh. But he doesn't know you. I'm sure you can beat him."},
    "test/new/mgs3_new_5.jpg":  {"type": "dialogue",       "text": "Every day, I help create things that should never be used -"},
    "test/new/mgs3_new_6.jpg":  {"type": "none",           "text": None},
    "test/new/mgs3_new_7.jpg":  {"type": "dialogue",       "text": "Use this key to open that door."},
    "test/new/mgs3_new_8.jpg":  {"type": "codec+dialogue", "text": "Then, by switching the Survival Viewer over to EVA you can treat her wounds, too. Now get to work."},
    "test/new/mgs3_new_9.jpg":  {"type": "none",           "text": None},
    "test/new/mgs3_new_10.jpg": {"type": "none",           "text": None},

    # MGS4
    "test/new/mgs4_new_1.jpg":  {"type": "dialogue", "text": "Never mind."},
    "test/new/mgs4_new_2.jpg":  {"type": "none",     "text": None},
    "test/new/mgs4_new_3.jpg":  {"type": "none",     "text": None},
    "test/new/mgs4_new_4.jpg":  {"type": "none",     "text": None},
    "test/new/mgs4_new_5.jpg":  {"type": "none",     "text": None},
    "test/new/mgs4_new_6.jpg":  {"type": "dialogue", "text": "It's the final key he needs to gain access to SOP."},
    "test/new/mgs4_new_7.jpg":  {"type": "none",     "text": None},
    "test/new/mgs4_new_8.jpg":  {"type": "none",     "text": None},
    "test/new/mgs4_new_9.jpg":  {"type": "none",     "text": None},
    "test/new/mgs4_new_10.jpg": {"type": "none",     "text": None},

    # MGS5
    "test/new/mgs5_new_1.jpg":  {"type": "none",     "text": None},
    "test/new/mgs5_new_2.jpg":  {"type": "none",     "text": None},
    "test/new/mgs5_new_3.jpg":  {"type": "dialogue", "text": "Cipher... just keeps growing."},
    "test/new/mgs5_new_4.jpg":  {"type": "none",     "text": None},
    "test/new/mgs5_new_5.jpg":  {"type": "none",     "text": None},
    "test/new/mgs5_new_6.jpg":  {"type": "dialogue", "text": "Make contact with the target - Code Talker,"},
    "test/new/mgs5_new_7.jpg":  {"type": "dialogue", "text": "Now they turn their knives on me."},
    "test/new/mgs5_new_8.jpg":  {"type": "none",     "text": None},
    "test/new/mgs5_new_9.jpg":  {"type": "none",     "text": None},
    "test/new/mgs5_new_10.jpg": {"type": "none",     "text": None},

    # Twin Snakes
    "test/new/twinsnakes_new_1.jpg":  {"type": "none",           "text": None},
    "test/new/twinsnakes_new_2.jpg":  {"type": "codec+dialogue", "text": "I can't quit. I can't allow myself to quit now."},
    "test/new/twinsnakes_new_3.jpg":  {"type": "none",           "text": None},
    "test/new/twinsnakes_new_4.jpg":  {"type": "none",           "text": None},
    "test/new/twinsnakes_new_5.jpg":  {"type": "dialogue",       "text": "You said that love could bloom on a battlefield..."},
    "test/new/twinsnakes_new_6.jpg":  {"type": "codec+dialogue", "text": "Dr. Hunter's story about her background... about her grandfather being an assistant secretary to Hoover in the FBI..."},
    "test/new/twinsnakes_new_7.jpg":  {"type": "dialogue",       "text": "Washington won't be very happy"},
    "test/new/twinsnakes_new_8.jpg":  {"type": "none",           "text": None},
    "test/new/twinsnakes_new_9.jpg":  {"type": "none",           "text": None},
    "test/new/twinsnakes_new_10.jpg": {"type": "none",           "text": None},

    # Peace Walker
    "test/new/peacewalker_new_1.jpg":  {"type": "dialogue", "text": "WE, ON THE OTHER HAND, WOULD GAIN A BASE FROM WHICH ALL OF LATIN AMERICA WOULD BE WELL WITHIN OUR REACH."},
    "test/new/peacewalker_new_2.jpg":  {"type": "dialogue", "text": "OH. OK WE CAN TALK UNTIL I FINISH THIS."},
    "test/new/peacewalker_new_3.jpg":  {"type": "none",     "text": None},
    "test/new/peacewalker_new_4.jpg":  {"type": "dialogue", "text": "THEY TOLD ME THIS WAS A PARADISE... THAT THERE WERE MORE RARE BIRDS HERE THAN ANYWHERE ELSE... THAT THERE WAS NO WAR HERE... THAT IT WAS SAFE..."},
    "test/new/peacewalker_new_5.jpg":  {"type": "none",     "text": None},
    "test/new/peacewalker_new_6.jpg":  {"type": "none",     "text": None},
    "test/new/peacewalker_new_7.jpg":  {"type": "none",     "text": None},
    "test/new/peacewalker_new_8.jpg":  {"type": "dialogue", "text": "I NOTICED THAT."},
    "test/new/peacewalker_new_9.jpg":  {"type": "dialogue", "text": "THE ONE WHO SURVIVES WILL INHERIT THE TITLE OF BOSS."},
    "test/new/peacewalker_new_10.jpg": {"type": "none",     "text": None},
}
