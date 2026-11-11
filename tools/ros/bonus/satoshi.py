"""Satoshi — three story battles and two raids in the island realm of the far north-east (ours; see build_bonus.py)."""
from build_bonus import U

LEVELS = []

# ---------------------------------------------------------------- 1. The Paddy Road (the landing and the road inland)
LEVELS.append(
    {
        "id": 5961,
        "group": "story",
        "name": "The Paddy Road",
        "objective": "Land on Satoshi and clear Lord Kagemori's men from the road inland.",
        "turn_limit": 30,
        "budget": 4000,
        "sides": {"P": "Carrone Army", "E": "Kagemori's Host"},
        "terrain": """
^^^^^^^^^.==.fff^^^^^^
^fff.....,==..ff....f^
^ff..hh...==...h.....^
^f...h....==..hh..ff.^
^...PPPPPP==PPPPPP.f.^
^.,,......==......x..^
^.........==..,,.....^
^ff..----.==.-----..f^
^f...----.==.-----...^
^.==================.^
^f...----.==.-----...^
^....----.==.-----.f.^
^.f..----.==.-----...^
...h.....===.....h....
..hh......==....hh..ff
.....,,...==.........f
ff........==...,,.....
f.........==..........
......................
......................
......................
~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~
""",
        "units": """
......................
......................
......................
......a.a.S..a.a......
......................
.......pwsswp.........
..cc......ww......HH..
......................
......................
.........wwww.........
......................
......................
......................
......................
......................
......................
......................
......................
.....DDDDDDDDDDDD.....
.....DDDDDDDDDDDD.....
.....DDDDDDDDDDDD.....
......................
......................
......................
""",
        "legend": {
            "a": U("archers", "E", group=1, hold=True),
            "S": U("sohei", "E", group=1, hold=True),
            "s": U("samurai", "E", group=2),
            "p": U("pikemen", "E", group=2),
            "c": U("cavalry", "E", group=3),
            "H": U("horsebowmen", "E", group=4),
            "w": U("swordsmen", "E", group=5, hold=True),
        },
        "camera": (10, 5),
        "intro": [
            ("officer", "We are ashore, Commander. One road runs inland, on a dyke between flooded fields."),
            ("ishiro", "Those are Kagemori's samurai at the village gate. Do not judge them by their number, Commander."),
            ("ishiro", "Men who stand near them fight harder, and men who face them lose heart. Break them first, or break nothing."),
            ("advisor", "Then we keep our line off those paddies, Varius. A soldier knee deep in water is half a soldier."),
        ],
        "events": [
            {
                "when": ("round", 5),
                "cam": (10, 0),
                "spawn": [
                    ("samurai", (10, 0), "E"),
                    ("swordsmen", (11, 0), "E"),
                    ("horsebowmen", (9, 1), "E"),
                    ("horsebowmen", (12, 1), "E"),
                ],
                "say": [("officer_alarm", "More banners on the north road, Commander. Kagemori has sent a second company down from the hills.")],
            },
        ],
        "brief": [
            ("ishiro", "I am Ishiro, lord of the eastern isle. Kagemori has burned three of my villages for refusing him the old shrines."),
            ("ishiro", "Land at the paddy road and I will raise my banner beside yours. It is the only road to my hill."),
        ],
        "victory": [
            ("officer", "The village is ours, Commander. The samurai would not give ground. Not one of them."),
            ("advisor", "I have not seen their like. Whatever Kagemori means to make of the Battlemage's secrets, he has the soldiers to make use of it."),
            ("ishiro", "He knows you have landed. He will come for my hill before you can reach his castle. Come quickly."),
        ],
        "defeat": [("officer_hurt", "We are driven back to the boats, Commander.")],
        "reward": {"units": {"sohei": 1}, "spoils": {"Weapons": 1, "Armor": 1, "Spirit": 1}},
    }
)

# ---------------------------------------------------------------- 2. Ishiro's Hill (hold the hill fort)
LEVELS.append(
    {
        "id": 5962,
        "group": "story",
        "name": "Ishiro's Hill",
        "objective": "Hold Lord Ishiro's hill fort for ten turns. Lord Ishiro must survive.",
        "turn_limit": 20,
        "budget": 4000,
        "win_switch": False,
        "sides": {"P": "Carrone Army", "A": "Ishiro's Retainers", "E": "Kagemori's Host"},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~
.ff.......==......fff.
.f..^^^...==...^^^..f.
....^.PPPP==PPPP.^....
..,,..P.h.==..hP......
......P.K.==...P..,,..
======p...==...p======
......P...==.h.P......
.ff...P.h.==...P...ff.
.f....PPPP==PPPP....f.
....--....==....---...
.f..--..x.==.x..---.f.
....--....==....---...
..........==..........
.ff...,,..==...,,..ff.
.f........==........f.
..........==..........
...h......==......h...
..........==..........
""",
        "units": """
......................
......................
........a.ss.a........
......................
......................
.......b..rr..........
........I.............
.......r......r.......
......................
..........rr..b.......
......................
......................
......................
......................
......................
......................
....DDDDDDDDDDDDDD....
....DDDDDDDDDDDDDD....
......................
......................
""",
        "legend": {
            "I": U("king", "A", group=1, hold=True, name="ishiro"),
            "r": U("samurai", "A", group=2, hold=True),
            "b": U("archers", "A", group=2, hold=True),
            "s": U("samurai", "E", group=1),
            "a": U("archers", "E", group=1),
        },
        "camera": (10, 6),
        "intro": [
            ("ishiro", "You honour my house, Commander. My retainers hold the gates. There are not enough of them."),
            ("officer_alarm", "Banners on the north road, and dust to the east and west. Kagemori has brought his whole host."),
            ("advisor", "If Lord Ishiro falls the island falls with him, Varius. Get our line inside that palisade."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (21, 7),
                "spawn": [
                    ("samurai", (21, 7), "E"),
                    ("samurai", (20, 7), "E"),
                    ("swordsmen", (21, 6), "E"),
                    ("swordsmen", (21, 8), "E"),
                    ("swordsmen", (20, 8), "E"),
                    ("shinobi", (20, 6), "E"),
                    ("shinobi", (21, 5), "E"),
                ],
                "say": [("officer_alarm", "They are on the east road, Commander!")],
            },
            {
                "when": ("round", 5),
                "cam": (0, 7),
                "spawn": [
                    ("samurai", (0, 7), "E"),
                    ("samurai", (1, 7), "E"),
                    ("swordsmen", (0, 6), "E"),
                    ("pikemen", (0, 8), "E"),
                    ("pikemen", (1, 8), "E"),
                    ("cavalry", (1, 6), "E"),
                    ("cavalry", (0, 5), "E"),
                ],
                "say": [("ishiro_grim", "The west gate. He means to come at us from every side at once.")],
            },
            {
                "when": ("round", 7),
                "cam": (10, 2),
                "spawn": [
                    ("samurai", (10, 2), "E"),
                    ("samurai", (11, 2), "E"),
                    ("samurai", (9, 2), "E"),
                    ("greatswordsmen", (12, 2), "E"),
                    ("greatswordsmen", (8, 2), "E"),
                    ("shamans", (13, 2), "E"),
                    ("archers", (7, 2), "E"),
                    ("archers", (14, 2), "E"),
                ],
                "say": [("daimyo", "Ishiro! You have sold our islands to a foreign emperor. Open your gate and die as a lord should.")],
            },
            {
                "when": ("round", 11),
                "say": [
                    ("officer", "They are pulling back, Commander. Kagemori's horn is sounding the retreat."),
                    ("ishiro", "He has spent his best men against my fence. Now his castle stands half empty."),
                ],
                "end": "victory",
            },
            {
                "when": ("kill", "ishiro"),
                "say": [("officer_hurt", "Lord Ishiro is down, Commander. His retainers are laying their swords beside him.")],
                "end": "defeat",
            },
        ],
        "brief": [
            ("ishiro", "My hill is a fence of logs and a hall, Commander. It has stood two hundred years because no lord of these isles would shame himself by burning it."),
            ("ishiro_grim", "Kagemori is no longer that kind of lord."),
        ],
        "victory": [
            ("ishiro", "My hill stands. I did not think to see this evening, Commander."),
            ("ishiro", "Take two bands of my own samurai into your army. They asked it of me. They wish to be there when Kagemori's gate comes down."),
            ("advisor", "His castle lies across the strait, Varius, with the sea at its back. Corvane's scrolls are inside it."),
        ],
        "defeat": [("officer_hurt", "The hill is lost, Commander, and Lord Ishiro with it.")],
        "reward": {"units": {"samurai": 2, "shinobi": 1}, "spoils": {}},
    }
)

# ---------------------------------------------------------------- 3. The Castle of Lord Kagemori (the finale)
LEVELS.append(
    {
        "id": 5963,
        "group": "story",
        "name": "The Castle of Lord Kagemori",
        "objective": "Storm the castle and defeat Lord Kagemori.",
        "turn_limit": 35,
        "budget": 5500,
        "sides": {"P": "Carrone Army", "E": "Kagemori's Host"},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~
^^..TWWWWWWWWWWWWWWT..^^
^...W______________W...^
^.f.W____K____h____W.f.^
^...W______________W...^
^...W______________W...^
^^..TWWWWWTGGTWWWWWT..^^
^..........==..........^
^.ff..x....==....x..ff.^
^.f........==.......f..^
~~~~~~--~~~--~~~~--~~~~~
~~~~~~--~~~--~~~~--~~~~~
...f.......==.......f...
.---...x...==...x..---..
.---.......==......---..
.---..hh...==..hh..---..
......h....==...h.......
========================
..ff.......==.......ff..
.f....,,...==...,,....f.
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
........q...............
.........K....z.........
.......s.....s..........
...........gg...........
......a.a......a.a......
........................
........................
......tu...tt....ut.....
........................
........................
....c..pp......pp..c....
........................
........................
........................
...H...ww..y...ww...H...
........................
........................
........................
........................
........................
......DDDDDDDDDDDD......
......DDDDDDDDDDDD......
......DDDDDDDDDDDD......
""",
        "legend": {
            "K": U("king", "E", group=1, hold=True, name="kagemori"),
            "s": U("samurai", "E", group=1, hold=True),
            "g": U("oni", "E", group=1, hold=True),
            "q": U("sohei", "E", group=1, hold=True),
            "z": U("shamans", "E", group=1, hold=True),
            "a": U("archers", "E", group=3, hold=True),
            "t": U("samurai", "E", group=2, hold=True),
            "u": U("swordsmen", "E", group=2, hold=True),
            "p": U("pikemen", "E", group=4, hold=True),
            "w": U("swordsmen", "E", group=5),
            "y": U("shamans", "E", group=5),
            "c": U("cavalry", "E", group=6),
            "H": U("tengu", "E", group=6),
        },
        "camera": (9, 4),
        "intro": [
            ("daimyo", "So the Emperor's hound has crossed the whole world to bark at my gate."),
            ("daimyo", "Corvane sold me the making of a Battlemage. In a year I would have had ten. You will not give me the year, I think."),
            ("ishiro", "The moat has three fords, Commander. His samurai will be standing in every one of them."),
            ("advisor", "Kagemori is the keystone, Varius. Bring him down and the scrolls are ours."),
        ],
        "events": [
            {
                "when": ("kill", "kagemori"),
                "say": [
                    ("daimyo_hurt", "Burn them. Burn the scrolls. If I cannot have them, no one..."),
                    ("officer", "Lord Kagemori has fallen, Commander. His samurai are kneeling."),
                ],
                "end": "victory",
            },
            {
                "when": ("round", 5),
                "cam": (23, 18),
                "spawn": [
                    ("samurai", (23, 18), "E"),
                    ("swordsmen", (22, 18), "E"),
                    ("cavalry", (23, 17), "E"),
                    ("samurai", (0, 18), "E"),
                    ("swordsmen", (1, 18), "E"),
                    ("cavalry", (0, 17), "E"),
                ],
                "say": [("officer_alarm", "Riders and samurai on the dyke road behind us, Commander, from both ends!")],
            },
            {
                "when": ("round", 8),
                "cam": (0, 13),
                "spawn": [
                    ("horsebowmen", (0, 13), "E"),
                    ("horsebowmen", (23, 13), "E"),
                ],
                "say": [("daimyo", "Every man of these isles who can ride is coming to my horn, Emperor's hound.")],
            },
        ],
        "brief": [
            ("advisor", "Kagemori's castle, Varius. Stone walls, a moat fed from the sea, and every samurai he has left."),
            ("ishiro", "My retainers will show your men the fords. After that it is swords."),
        ],
        "victory": [
            ("officer", "The keep is on fire, Commander. Kagemori's priests put the torch to the scroll room before we reached it."),
            ("advisor", "Let it burn, Varius. Tolm dug the Battlemage up, the Doge woke it, Corvane sold it, and Kagemori would have copied it. Every one of them is dead of it."),
            ("ishiro", "The old shrines say a weapon that outlives its makers is a curse. Tonight the last of it is ash on the sea wind."),
            ("advisor", "Then there is one Battlemage in the world, and it marches under your banner. See that it never needs a second. Let us go home."),
        ],
        "defeat": [("officer_hurt", "We could not carry the moat, Commander. Kagemori still holds his castle.")],
        "reward": {"units": {"oni": 1, "tengu": 1}, "spoils": {"Lore": 1, "Spirit": 1, "Armor": 1}},
    }
)

# ---------------------------------------------------------------- Raid 1. The Shrine Pass (timed capture)
LEVELS.append(
    {
        "id": 5971,
        "group": "siege",
        "name": "The Shrine Pass",
        "objective": "Reach the mountain shrine within fourteen turns, before Kagemori's men carry off its relics.",
        "turn_limit": 14,
        "budget": 3750,
        "sides": {"P": "Carrone Army", "E": "Shrine Guard"},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^
^ff...oK.o....fff.^^
^f.....==.......ff.^
^..^^^.==.^^^^.....^
^.....x==x.....,,..^
^^^^...==...^^^^^..^
^.f....==.......^.f^
^......===......^..^
^..^^^^.==...ff....^
^.......==....f.,,.^
^~~~~~~~--~~~--~~~~^
^~~~~~~~--~~~--~~~~^
...f....==..........
..ff...===......h...
.......==......hh...
...,,..==...........
.......==...........
.......==...........
""",
        "units": """
....................
.......1............
....a.aq.a.a........
.......ss...........
......sws..a........
....................
.......ww........HH.
.................H..
....................
.......ppp..........
....................
....................
....................
....................
....................
..DDDDDDDDDDDD......
..DDDDDDDDDDDD......
..DDDDDDDDDDDD......
""",
        "legend": {
            "a": U("archers", "E", group=1, hold=True),
            "q": U("sohei", "E", group=1, hold=True),
            "s": U("samurai", "E", group=2, hold=True),
            "p": U("pikemen", "E", group=3, hold=True),
            "w": U("swordsmen", "E", group=3, hold=True),
            "H": U("tengu", "E", group=4),
        },
        "camera": (7, 2),
        "intro": [
            ("ishiro", "The shrine above this pass keeps the oldest relics of my people. Kagemori's men are packing them onto mules."),
            ("advisor", "One road, one ford, and a wall of samurai at the top of it. We have until they finish loading, Varius."),
        ],
        "events": [
            {
                "when": ("reach", "1"),
                "say": [("officer", "We hold the shrine, Commander. The relics are still on the altar.")],
                "end": "victory",
            },
        ],
        "victory": [("ishiro", "You have kept faith with gods that are not your own, Commander. It will be remembered.")],
        "defeat": [("officer_hurt", "The shrine is stripped bare, Commander. We came too late.")],
        "reward": {"units": {"archers": 1}, "spoils": {"Spirit": 2, "Lore": 1}},
    }
)

# ---------------------------------------------------------------- Raid 2. The Pirate Stockade (eliminate)
LEVELS.append(
    {
        "id": 5972,
        "group": "siege",
        "name": "The Pirate Stockade",
        "objective": "Destroy the pirates in Kagemori's pay and burn out their stockade.",
        "turn_limit": 30,
        "budget": 3500,
        "sides": {"P": "Carrone Army", "E": "Coast Pirates"},
        "heraldry": {"E": ("argent", "sable", 61, 5)},
        "terrain": """
^^^^^^^^^^^^^^^^^~~~~~
^ff......,,.....f~~~~~
^f..PPPPPPPPPP...~~~~~
^...P..h...h.P...~~~~~
^...P........p===~~~~~
^.f.P..h.....P....~~~~
^...PPPPppPPPP....~~~~
^.......==..x.....~~~~
^.,,....==.....ff.~~~~
^..x....==......f.~~~~
^^^^....===.......~~~~
..f......==..--...~~~~
.ff......==..--....~~~
.........==........~~~
..h......==...,,...~~~
.........==........~~~
.........==........~~~
.........==........~~~
""",
        "units": """
......................
......................
......................
.....a.s..w.a.........
......z..s....ww......
.....a..w.w.a.........
........pp............
......hh..hhh.........
........xx............
....ff.......ff.......
......................
......................
......................
......................
......................
...DDDDDDDDDDDD.......
...DDDDDDDDDDDD.......
...DDDDDDDDDDDD.......
""",
        "legend": {
            "a": U("archers", "E", group=1, hold=True),
            "s": U("samurai", "E", group=2, hold=True),
            "z": U("shamans", "E", group=2, hold=True),
            "w": U("swordsmen", "E", group=3, hold=True),
            "p": U("pikemen", "E", group=4, hold=True),
            "h": U("halberdiers", "E", group=5),
            "x": U("crossbowmen", "E", group=4, hold=True),
            "f": U("footmen", "E", group=6),
        },
        "camera": (8, 4),
        "intro": [
            ("officer", "A stockade on the shore, Commander. These are the pirates who carry Kagemori's silver and Corvane's letters."),
            ("advisor", "Masterless samurai among them, by the look of it. Hired swords fight until the pay runs out. Let us end the pay."),
        ],
        "events": [
            {
                "when": ("round", 5),
                "cam": (18, 14),
                "spawn": [
                    ("samurai", (18, 13), "E"),
                    ("swordsmen", (18, 14), "E"),
                    ("shinobi", (17, 13), "E"),
                ],
                "say": [("officer_alarm", "A boat on the beach behind us, Commander! More of them are wading ashore.")],
            },
        ],
        "victory": [("officer", "The stockade is burning, Commander. Kagemori will get no more ships from this coast.")],
        "defeat": [("officer_hurt", "They held their fence, Commander. We will have to come again.")],
        "reward": {"units": {"swordsmen": 1}, "spoils": {"Weapons": 2, "Beasts": 1}},
    }
)

KINGDOM = {
    "id": "satoshi",
    "short": "Satoshi",
    "name": "The Isles of Satoshi",
    "order": 14,
    "theme": "green",
    "unlock_after": ["Mare Nostra"],
    "heraldry": {"E": ("gules", "sable", 33, 5), "A": ("argent", "gules", 14, 3)},
    "brief": [
        (
            "thaddius",
            "Commander, the charts you took from Admiral Corvane mark a course to the far north-east, to the Isles of Satoshi. With them were copies of every scroll the Doge's scholars made about the Battlemage. Corvane was selling them.",
        ),
        (
            "thaddius",
            "The buyer is a warlord of those isles, Lord Kagemori, who means to make a Battlemage of his own. A rival, Lord Ishiro, has sent to the Emperor for help. Sail to Satoshi. Those scrolls must not be used.",
        ),
    ],
    "levels": LEVELS,
}
