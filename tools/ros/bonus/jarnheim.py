"""The Holds of Jarnheim — three story battles and two raids in the northern mountains (ours; see build_bonus.py).
A Norse mountain kingdom whose heart is a walled fortress town: a pass held by Berserkers, a Shieldmaiden wall at the
town's river gate, and the Jarl's hold itself, kept by Einherjar and a frost giant. It opens with the bonus campaigns
(beside Tilicia) and nothing waits on it."""
from build_bonus import U

LEVELS = []
ARMY = "Carrone Army"
HOLD = "Jarl Haldor's Hird"

# ---------------------------------------------------------------- 1. The Raven Pass (Berserkers in a mountain pass)
LEVELS.append(
    {
        "id": 5914,
        "group": "story",
        "name": "The Raven Pass",
        "objective": "Force the pass into Jarnheim. Eliminate all enemies.",
        "turn_limit": 30,
        "budget": 3450,
        "sides": {"P": ARMY, "E": HOLD},
        "terrain": """
^^^^^^^^.==.^^^^^^^^
^^^^^..r.==.r..^^^^^
^^^...h..==..h...^^^
^^.r.....==.....r.^^
^^......x==x......^^
^^^.r....==....r.^^^
^^^^.ii..==..ii.^^^^
^^^^^.r..==..r.^^^^^
^^^^.....==.....^^^^
^^^..f...==...f..^^^
^^..ff...==...ff..^^
^^.......==.......^^
^^^.r....==....r.^^^
^^^^.....==.....^^^^
^^^..,...==...,..^^^
^^.......==.......^^
^..f.....==.....f..^
^...R....==....R...^
^........==........^
^^.......==.......^^
^^^......==......^^^
^^^^.....==.....^^^^
^^^^^^...==...^^^^^^
^^^^^^^^.==.^^^^^^^^
""",
        "units": """
....................
....................
......a..z...a......
....a..........a....
.......lh..hl.......
.......l....l.......
....................
....................
......B.B..B.B......
....................
....................
.....C........C.....
....................
....................
....................
....................
....................
....................
....DDDDDDDDDDDD....
....DDDDDDDDDDDD....
....DDDDDDDDDDDD....
....................
....................
....................
""",
        "legend": {
            "a": U("archers", "E", group=1, hold=True),
            "z": U("shamans", "E", group=1, hold=True),
            "l": U("footmen", "E", group=2, hold=True),
            "h": U("halberdiers", "E", group=2, hold=True),
            "B": U("berserker", "E", group=3),
            "C": U("berserker", "E", group=4),
        },
        "camera": (9, 5),
        "intro": [
            ("officer", "The Raven Pass, Commander. One road, a barricade across it, and rock on both sides too steep for a goat."),
            ("eirik", "Those are Haldor's bear-shirts in front of the barricade. They wear no mail and carry no shield, and they do not need to."),
            ("advisor", "Berserkers, Varius. Wound one and it only hits harder. Put each of them down in a single turn, or do not touch it at all."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (2, 15),
                "spawn": [
                    ("berserker", (2, 15), "E"),
                    ("berserker", (3, 15), "E"),
                    ("berserker", (16, 15), "E"),
                    ("berserker", (17, 15), "E"),
                ],
                "say": [("officer_alarm", "Bear-shirts in the gullies, Commander! They have come down the rock behind our line!")],
            },
            {
                "when": ("round", 6),
                "cam": (9, 0),
                "spawn": [
                    ("berserker", (9, 0), "E"),
                    ("berserker", (10, 0), "E"),
                    ("halberdiers", (9, 1), "E"),
                    ("halberdiers", (10, 1), "E"),
                ],
                "say": [("enemy", "The Jarl sends his greeting, southerner, and his axes with it!")],
            },
        ],
        "brief": [
            ("eirik", "I am Eirik, Commander, a skald of the Holds, and I have sung for three Jarls. This one I will not sing for. Haldor burns farms that owe him nothing."),
            ("advisor", "The skald knows the road, Varius, and the road is the Raven Pass. Haldor's bear-shirts hold it."),
        ],
        "victory": [
            ("officer", "The pass is ours, Commander. Not one of the bear-shirts ran."),
            ("eirik", "They never do. But some of your axemen watched how they fought, and they have been very quiet since. Give those men a bearskin and they will not be quiet long."),
        ],
        "defeat": [("officer_hurt", "We cannot hold the road, Commander. The pass is theirs.")],
        "reward": {"units": {"berserker": 1}, "spoils": {"Spirit": 1, "Weapons": 1, "Bloodstone": 2}},
    }
)

# ---------------------------------------------------------------- 2. The Shield Bridge (a shield wall at the river gate)
LEVELS.append(
    {
        "id": 5915,
        "group": "story",
        "name": "The Shield Bridge",
        "objective": "Break the shield wall at the river gate. Eliminate all enemies.",
        "turn_limit": 32,
        "budget": 4050,
        "sides": {"P": ARMY, "E": HOLD},
        "terrain": """
^^^^.......==.......^^^^
^^^...h....==....h...^^^
^^.........==.........^^
^TWWWWWWWWTGGTWWWWWWWWT^
^..........==..........^
^..r.......==.......r..^
^..........==..........^
~~~~~--~~~~bb~~~~--~~~~~
~~~~~ii~~~~bb~~~~ii~~~~~
~~~~~--~~~~bb~~~~--~~~~~
...........==...........
..f....x...==...x....f..
.ff........==........ff.
...........==...........
....R......==......R....
...........==...........
..,,.......==.......,,..
...........==...........
.f.........==.........f.
...........==...........
...........==...........
...........==...........
...........==...........
...........==...........
""",
        "units": """
........................
........................
........................
....a..a........a..a....
........B.B..B.B........
.....c............c.....
.........S.SS.S.........
........................
...........SS...........
........................
.........SSSSSS.........
.........w.ww.w.........
........................
........................
........................
........................
........................
........................
......DDDDDDDDDDDD......
......DDDDDDDDDDDD......
......DDDDDDDDDDDD......
........................
........................
........................
""",
        "legend": {
            "a": U("archers", "E", group=1, hold=True),
            "c": U("crossbowmen", "E", group=2, hold=True),
            "S": U("shieldmaiden", "E", group=3, hold=True),
            "w": U("swordsmen", "E", group=3, hold=True),
            "B": U("berserker", "E", group=4),
        },
        "camera": (11, 9),
        "intro": [
            ("eirik", "Jarnborg, Commander. The river runs round the town like a ditch, and there is one bridge."),
            ("officer", "And a wall of shields across it. Women, by their hair. They have not moved since sunrise."),
            ("eirik", "Shieldmaidens. Each one covers the fighter beside her, so a line of them is harder than the sum of it. Break the line and they are only soldiers."),
            ("advisor", "There are fords up and down the river, Varius. Slow going, but they come out behind that wall."),
        ],
        "events": [
            {
                "when": ("round", 4),
                "cam": (5, 6),
                "spawn": [
                    ("berserker", (5, 6), "E"),
                    ("berserker", (6, 6), "E"),
                    ("berserker", (17, 6), "E"),
                    ("berserker", (18, 6), "E"),
                ],
                "say": [("officer_alarm", "Bear-shirts at the fords, Commander! They are wading over to take us in the flank!")],
            },
            {
                "when": ("round", 7),
                "cam": (11, 2),
                "spawn": [
                    ("einherjar", (11, 2), "E"),
                    ("einherjar", (12, 2), "E"),
                    ("shieldmaiden", (10, 2), "E"),
                    ("shieldmaiden", (13, 2), "E"),
                ],
                "say": [
                    ("eirik", "The gate is opening. Look at their faces, Commander. Those men were buried years ago. I sang at two of the graves."),
                ],
            },
        ],
        "brief": [
            ("eirik", "Below the pass lies Jarnborg, the iron town. Its outer gate stands on the far bank of the river, and Haldor's shieldmaidens stand on the near one."),
            ("advisor", "A shield wall on a bridge, Varius. We go through it, or we get wet going round it."),
        ],
        "victory": [
            ("officer", "The bridge is ours, Commander, and the gate behind it. The shield wall is broken."),
            ("eirik", "Three of them have asked to stand in your line instead. They say a wall should have something worth standing in front of."),
            ("advisor", "The dead men at the gate trouble me more, Varius. Somebody in that town is calling the Jarl's old warriors back out of the ground."),
        ],
        "defeat": [("officer_hurt", "We could not break the wall, Commander. The bridge is still theirs.")],
        "reward": {"units": {"shieldmaiden": 1}, "spoils": {"Armor": 1, "Weapons": 1, "Bloodstone": 2}},
    }
)

# ---------------------------------------------------------------- 3. The Jarl's Hold (the fortress town and its keep)
LEVELS.append(
    {
        "id": 5916,
        "group": "story",
        "name": "The Jarl's Hold",
        "objective": "Storm Jarnborg and defeat Jarl Haldor.",
        "turn_limit": 34,
        "budget": 4250,
        "sides": {"P": ARMY, "E": HOLD},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^TWWWWWWWWWWWWWWWWWWT^^^
^^^W__________________W^^^
^^^W__h_____K____h____W^^^
^^^W__________________W^^^
^^^W_h_____________h__W^^^
^^^W____R_____________W^^^
^^^W__h__________h____W^^^
^^^W__________________W^^^
^^^TWWWWWWWTGGTWWWWWWWT^^^
^^.........,==,.........^^
^..r....x...==...x....r..^
^........ii.==.ii........^
^^..f....ii.==.ii....f..^^
^^.ff.......==.......ff.^^
^...........==...........^
^....r......==......r....^
............==............
..,,........==........,,..
............==............
.f..........==..........f.
............==............
............==............
............==............
^^..........==..........^^
^^^^........==........^^^^
""",
        "units": """
..........................
..........................
..........................
............J.............
.........e.....e..........
............Y.............
.........e.....e..........
..........................
..........SSSS............
......a.a........a.a......
..........................
........pp......pp........
..........................
..........................
...B..................B...
....B................B....
..........................
..........................
..........................
..........................
.......DDDDDDDDDDDD.......
.......DDDDDDDDDDDD.......
.......DDDDDDDDDDDD.......
..........................
..........................
..........................
""",
        "legend": {
            "J": U("king", "E", group=1, hold=True, name="haldor"),
            "e": U("einherjar", "E", group=1, hold=True),
            "Y": U("jotunn", "E", group=2, hold=True),
            "S": U("shieldmaiden", "E", group=2, hold=True),
            "a": U("archers", "E", group=3, hold=True),
            "p": U("pikemen", "E", group=4, hold=True),
            "B": U("berserker", "E", group=5),
        },
        "camera": (12, 4),
        "intro": [
            ("haldor", "So the Emperor has sent a clerk with a sword to collect for some burnt barns."),
            ("haldor", "Look behind me, clerk. My fathers' hirdmen have come back from the hall of the slain to drink with me, and a son of the old frost stands at my gate. What have you brought?"),
            ("eirik", "The dead ones mend themselves on every man they kill, Commander. Do not feed them your wounded. And where the giant's club lands, men move like old women for a while."),
            ("advisor", "The Jarl is the keystone, Varius. When he falls, the dead have nobody left to drink with."),
        ],
        "events": [
            {
                "when": ("kill", "haldor"),
                "say": [
                    ("haldor_hurt", "A clerk... Sing it kindly, skald..."),
                    ("eirik", "I will sing it truly, Haldor. Hird of Jarnborg! Your Jarl is dead and your dead are tired. Let them sleep."),
                ],
                "end": "victory",
            },
            {
                "when": ("round", 5),
                "cam": (1, 15),
                "spawn": [
                    ("berserker", (1, 15), "E"),
                    ("berserker", (2, 15), "E"),
                    ("berserker", (23, 15), "E"),
                    ("berserker", (24, 15), "E"),
                ],
                "say": [("officer_alarm", "Bear-shirts out of the woods on both flanks, Commander!")],
            },
            {
                "when": ("round", 8),
                "cam": (12, 6),
                "spawn": [
                    ("einherjar", (10, 6), "E"),
                    ("einherjar", (14, 6), "E"),
                    ("shieldmaiden", (11, 7), "E"),
                    ("shieldmaiden", (13, 7), "E"),
                ],
                "say": [("haldor", "Up, old friends! There is one more night's work in you yet!")],
            },
        ],
        "brief": [
            ("eirik", "Jarnborg itself, Commander. One wall, one gate, the long houses inside it, and the Jarl's hall against the mountain."),
            ("advisor", "Einherjar in the court and a frost giant at the gate, Varius. I have fought kings who kept worse company, but not many."),
        ],
        "victory": [
            ("officer", "Jarl Haldor is dead, Commander. The hird has laid down its axes, and the pale ones have simply stopped."),
            ("eirik", "Not all of them. One of the chosen has knelt to your banner. He says he was promised a fight worth leaving the hall for, and he has only now had it."),
            ("advisor", "The Holds will choose a new Jarl by spring, Varius. Let us see that the skald has a say in it."),
        ],
        "defeat": [("officer_hurt", "The gate held, Commander. Jarnborg is still his.")],
        "reward": {"units": {"einherjar": 1}, "spoils": {"Lore": 1, "Beasts": 1, "Armor": 1, "Bloodstone": 2}},
    }
)

# ---------------------------------------------------------------- Raid 1. The Mead Hall (a palisaded hall at feast)
LEVELS.append(
    {
        "id": 5917,
        "group": "siege",
        "name": "The Mead Hall",
        "objective": "Take the mead hall before the hunting party returns. Eliminate all enemies.",
        "turn_limit": 22,
        "budget": 2600,
        "sides": {"P": ARMY, "E": "Bear-shirt Lodge"},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^
^^..f..........f..^^
^...PPPPPPPPPPPP...^
^.f.P..........P.f.^
^...P.h..hh..h.P...^
^...P..........P...^
^.R.P.h......h.P...^
^.r.P..........P.r.^
^...PPPPPppPPPPP...^
^........==........^
^^..x....==....x..^^
^^.......==.......^^
^...f....ii....f...^
^..ff....==....ff..^
.........==.........
..,......==......,..
.........==.........
.........==.........
.........==.........
^^.......==.......^^
""",
        "units": """
....................
....................
....................
......a......a......
.......B..B.........
.....B........B.....
.........a..........
.......B....B.......
.........SS.........
....................
.....l........l.....
....................
....................
....................
....................
....DDDDDDDDDDDD....
....DDDDDDDDDDDD....
....DDDDDDDDDDDD....
....................
....................
""",
        "legend": {
            "B": U("berserker", "E", group=1, hold=True),
            "a": U("archers", "E", group=1, hold=True),
            "S": U("shieldmaiden", "E", group=2, hold=True),
            "l": U("footmen", "E", group=3, hold=True),
        },
        "camera": (9, 5),
        "intro": [
            ("eirik", "The lodge of the bear-shirts, Commander. They feast here between raids, and half of them are out hunting."),
            ("advisor", "A palisade a man can climb and a gate two shieldmaidens can hold. Be inside before the hunters come home, Varius."),
        ],
        "events": [
            {
                "when": ("round", 5),
                "cam": (2, 1),
                "spawn": [
                    ("berserker", (2, 1), "E"),
                    ("berserker", (3, 1), "E"),
                    ("berserker", (16, 1), "E"),
                    ("berserker", (17, 1), "E"),
                ],
                "say": [("officer_alarm", "Horns in the high woods, Commander. The hunting party is back!")],
            },
        ],
        "victory": [("eirik", "No more feasts on other men's cattle. The valley farms will send you a barrel for this, Commander.")],
        "defeat": [("officer_hurt", "They have thrown us back from the palisade, Commander.")],
        "reward": {"units": {"halberdiers": 1}, "spoils": {"Spirit": 1, "Beasts": 1, "Weapons": 1, "Bloodstone": 2}},
    }
)

# ---------------------------------------------------------------- Raid 2. The Giants' Stair (a giant hunt in the rocks)
LEVELS.append(
    {
        "id": 5918,
        "group": "siege",
        "name": "The Giants' Stair",
        "objective": "Hunt down the frost giants on the high rocks. Eliminate all enemies.",
        "turn_limit": 24,
        "budget": 2950,
        "sides": {"P": ARMY, "E": "Sons of the Frost"},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^^^
^..rr....r....r..rr..^
^....................^
^r..^^^...rr...^^^..r^
^.....^........^.....^
^..r......R.......r..^
^.........,,.........^
^^^^....r....r....^^^^
^..r......ii........r^
^....o..........o....^
^.....r....r.....r...^
^..^^^..........^^^..^
^.r........,,.......r^
..f................ff.
.ff...............f...
......................
......................
......................
""",
        "units": """
......................
......................
..........Y...........
......................
....B...........B.....
......................
......Y.......Y.......
......................
......................
.........B..B.........
......................
......................
......................
......................
......DDDDDDDDDD......
......DDDDDDDDDD......
......DDDDDDDDDD......
......................
""",
        "legend": {
            "Y": U("jotunn", "E", group=1),
            "B": U("berserker", "E", group=2),
        },
        "camera": (10, 5),
        "intro": [
            ("eirik", "The Giants' Stair, Commander. Haldor fed the sons of the frost on stolen cattle, and now that the cattle have stopped they are coming down for the farms."),
            ("advisor", "Three of them, and their thralls. A giant's club slows whatever it does not kill, Varius. Do not let them catch the line bunched."),
        ],
        "events": [
            {
                "when": ("round", 4),
                "cam": (10, 1),
                "spawn": [("jotunn", (10, 1), "E"), ("berserker", (8, 2), "E"), ("berserker", (12, 2), "E")],
                "say": [("officer_alarm", "Another one on the top stair, Commander, and bigger than the rest!")],
            },
        ],
        "victory": [("eirik", "Four giants in a morning. I shall need a longer metre, Commander.")],
        "defeat": [("officer_hurt", "The giants have broken us, Commander. We are falling back down the stair.")],
        "reward": {"units": {"greatswordsmen": 1}, "spoils": {"Beasts": 2, "Lore": 1, "Bloodstone": 2}},
    }
)

KINGDOM = {
    "id": "jarnheim",
    "short": "Jarnheim",
    "name": "The Holds of Jarnheim",
    "order": 17,
    "theme": "green",
    "unlock_after": ["Abbisin"],  # with the bonus campaigns, beside Tilicia; nothing waits on it
    "heraldry": {"E": ("argent", "gules", 44, 6)},
    "brief": [
        (
            "emperor",
            "Commander Varius, the north is burning. Longships out of the mountain holds of Jarnheim have raided Hunewold and Rukiev three summers running, and this summer they did not go home.",
        ),
        (
            "thaddius",
            "Their Jarl is a man named Haldor, Commander. The Hunewold say his dead fight for him and that a giant keeps his gate. I would call that a fireside tale, if the survivors did not all tell it the same way.",
        ),
        (
            "emperor",
            "A skald of theirs has come to my court to ask for an army, which tells you what his own people think of this Jarl. Take the pass, take the town, and bring me Haldor's oath or his axe.",
        ),
    ],
    "levels": LEVELS,
}
