"""The Mirror Sea — three story battles and two raids fought ship to ship on the northern sea the map names (ours;
see build_bonus.py). It follows Mare Nostra (mare_nostra.py): Corvane's last captains have sold themselves to
Reaver-King Skarl, whose Beast Masters loose war hounds across the planks.

Every map is open sea with hulls laid on it: "b" deck, "m" a mast, "c" a cabin (here often a kennel). Ships are
joined by one-tile gangplanks; the builder edges every other deck tile that meets the sea with a wooden bulwark.
"""
from build_bonus import U

LEVELS = []
ARMY = "Carrone Army"
REAVERS = "Skarl's Reavers"

# ---------------------------------------------------------------- 1. The Line of Hulls (a running fight, hull to hull)
LEVELS.append(
    {
        "id": 5981,
        "group": "story",
        "name": "The Line of Hulls",
        "objective": "Fight from hull to hull along the reaver line. Eliminate all enemies.",
        "turn_limit": 32,
        "budget": 5500,
        "sides": {"P": ARMY, "E": REAVERS},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~bbbbbbbb~~~~bbbbbbbb~~~
~~bbbmbbbbbb~~bbbbbbmbbb~~
~~bbbbbbbbbbbbbbbbbbbbbb~~
~~bbbbbbbbbb~~bbbbbbbbbb~~
~~~bbbbbbbb~~~~bbbbbbbb~~~
~~~~~b~~~~~~~~~~~~~~b~~~~~
~~~~~b~~~~~~~~~~~~~~b~~~~~
~~~bbbbbbbb~~~~bbbbbbbb~~~
~~bbbbbbbbbb~~bbbbbbbbbb~~
~~bbbmbbbbbb~~bbbbbbmbccb~
~~bbbbbbbbbb~~bbbbbbbbbb~~
~~~bbbbbbbb~~~~bbbbbbbb~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~
""",
        "units": """
..........................
....x..x..........a..a....
...g..f.g.......s..p.s....
....f.g..........p...B....
...g...f.........s..s.....
..........................
..........................
..........................
................h..k.h....
...DDDDDDDD....k..w..k.n..
...DD.DDDDD...n..h........
...DDDDDDDD.....k..h......
..........................
..........................
""",
        "legend": {
            "g": U("gladiator", "E", group=1, hold=True),
            "f": U("footmen", "E", group=2, hold=True),
            "x": U("crossbowmen", "E", group=3, hold=True),
            "s": U("swordsmen", "E", group=4, hold=True),
            "p": U("pavisiers", "E", group=5, hold=True),
            "a": U("archers", "E", group=6, hold=True),
            "B": U("ballistae", "E", group=7, hold=True),
            "h": U("halberdiers", "E", group=8, hold=True),
            "k": U("gladiator", "E", group=9, hold=True),
            "w": U("greatswordsmen", "E", group=9, hold=True),
            "n": U("naga", "E"),
        },
        "camera": (6, 6),
        "intro": [
            ("officer", "Four hulls moored in a ring, Commander, and we hold only this one. The next lies across that plank."),
            ("advisor", "One plank on to each, and no way back but the way we came. Take them in turn, Varius. Their last ship lies under our own stern, and her Marines will not wait for us to walk round."),
        ],
        "brief": [
            ("officer", "The portage is behind us, Commander. Every hull we own came over the Tilician hills on rollers, and here is the Mirror Sea."),
            ("advisor", "And here are the reavers. Four ships roped stem to stern across the strait, like a boom. We go through them or we go home."),
        ],
        "victory": [
            ("officer", "The line is broken, Commander. All four hulls are ours."),
            ("advisor", "There was a cage on the last one, Varius. Iron, man-high, and chewed from the inside. Whatever they kept in it, they took it with them."),
        ],
        "defeat": [("officer_hurt", "They have thrown us back across the plank, Commander. The strait is still shut.")],
        "reward": {"units": {"naga": 1}, "spoils": {"Weapons": 1, "Armor": 1}},
    }
)

# ---------------------------------------------------------------- 2. The Kennel Ship (Beast Masters and their hounds)
LEVELS.append(
    {
        "id": 5982,
        "group": "story",
        "name": "The Kennel Ship",
        "objective": "Board the kennel ship. Eliminate all enemies.",
        "turn_limit": 32,
        "budget": 3500,
        "sides": {"P": ARMY, "E": REAVERS},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~bbbbbbbbbbbbbbbb~~~~~
~~~~bbcbbcbbbbbbcbbcbb~~~~
~~~bbbbbbbmbbbbmbbbbbbb~~~
~~~bbbbbbbbbbbbbbbbbbbb~~~
~~~~bbbbbbbbbbbbbbbbbb~~~~
~~~~~~b~~~~~b~~~~~~b~~~~~~
~~~~~~b~~~~~b~~~~~~b~~~~~~
~~~~bbbbbbbbbbbbbbbbbb~~~~
~~~bbbbbmbbbbbbbbmbbbbb~~~
~~~bbbbbbbbbbbbbbbbbbccb~~
~~~~bbbbbbbbbbbbbbbbbb~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~
""",
        "units": """
..........................
......x...x....x...x......
.....g..Z...ff...Z..g.....
....H..H....s.....H..H....
.....g....s..s......g.....
......h.....h......h......
..........................
..........................
.....DDDDDDDDDDDDDDDD.....
....DDDD.DDDDDDDD.DDDD....
....DDDDDDDDDDDDDDDD......
..........................
..........................
""",
        "legend": {
            "Z": U("beastmaster", "E", group=1, hold=True, name="master"),
            "H": U("hounds", "E", group=2),
            "g": U("gladiator", "E", group=3, hold=True),
            "f": U("footmen", "E", group=4, hold=True),
            "s": U("swordsmen", "E", group=5, hold=True),
            "h": U("halberdiers", "E", group=6, hold=True),
            "x": U("crossbowmen", "E", group=7, hold=True),
        },
        "camera": (12, 3),
        "intro": [
            ("officer_alarm", "Dogs, Commander! Big as ponies, and loose on her deck!"),
            ("advisor", "War hounds, and the men with the whips are their Beast Masters. Each keeps a pair at heel and whistles up another when one falls. Kill the handler, Varius, and the kennel stays shut."),
        ],
        "events": [
            {
                "when": ("kill", "master"),
                "say": [("officer", "Both handlers are down, Commander! The hounds have no one to answer to.")],
            },
        ],
        "brief": [
            ("officer", "We have found what was in the cage, Commander. A hulk with kennels the length of her deck, and she is coming alongside."),
            ("advisor", "Skarl breeds them on the islands. He does not waste Marines on a boarding when a pack will do it for meat. Three planks, and they will come down all three."),
        ],
        "victory": [
            ("officer", "The kennel ship is taken, Commander. The handlers' whips and whistles with her."),
            ("advisor", "There are whelps below, Varius, not yet blooded, and our militia are farm boys who grew up with dogs. Give me a season and a Medal to pin on the best of them, and the Empire will have Beast Masters of its own."),
        ],
        "defeat": [("officer_hurt", "The pack has the deck, Commander. We cannot hold the planks.")],
        "reward": {"units": {"militiamen": 2}, "spoils": {"Beasts": 2}},
    }
)

# ---------------------------------------------------------------- 3. The Reaver-King (the flagship moored at his islet)
LEVELS.append(
    {
        "id": 5983,
        "group": "story",
        "name": "The Reaver-King",
        "objective": "Cross the flagship to the islet and defeat Reaver-King Skarl.",
        "turn_limit": 34,
        "budget": 3500,
        "sides": {"P": ARMY, "E": REAVERS},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~--------~~~
~~~bbbbbbbbbbbb~~-.......-~~
~~bbbbmbbbbmbbbb~-..r.h...-~
~~bbbbbbbbbbbbbbbb........-~
~~bbbbbbbbbbbbbb~-...h..r.-~
~~~bbbbbbbbbbbb~~-.......-~~
~~~~~b~~~~~~b~~~~--------~~~
~~~~~b~~~~~~b~~~~~~~~~~~~~~~
~~~bbbbbbbbbbbb~~~~~~~~~~~~~
~~bbbbmbbbbmbbbb~~~~~~~~~~~~
~~bbbbbbbbbbbbccb~~~~~~~~~~~
~~~bbbbbbbbbbbb~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""",
        "units": """
............................
............................
....x...x..x.......c..c.....
...g...Z..........H.....K...
....g..H..s...p....w.w.w....
...g......s..h....H.Z....c..
.....h......h...............
............................
............................
....DDDDDDDDDD..............
...DDD.DDDD.DDD.............
...DDDDDDDDDDD..............
............................
............................
""",
        "legend": {
            "K": U("king", "E", group=1, hold=True, name="skarl"),
            "w": U("greatswordsmen", "E", group=1, hold=True),
            "c": U("cragsmen", "E", group=2, hold=True),
            "Z": U("beastmaster", "E", group=3, hold=True),
            "H": U("hounds", "E", group=4),
            "g": U("gladiator", "E", group=5, hold=True),
            "s": U("swordsmen", "E", group=6, hold=True),
            "p": U("efreet", "E", group=7, hold=True),
            "h": U("halberdiers", "E", group=8, hold=True),
            "x": U("crossbowmen", "E", group=9, hold=True),
        },
        "camera": (21, 4),
        "intro": [
            ("skarl", "So the Emperor carries his boats over mountains now. You should have left them there, Commander. My dogs have not eaten since the kennel ship."),
            ("officer", "His flagship lies between us and that islet, Commander. Two planks up to her deck, and one off her bow to the sand."),
            ("advisor", "The shallows round the islet will bear a man, Varius, but slowly. Skarl stands by his hall. When he falls, this sea is quiet again."),
        ],
        "events": [
            {
                "when": ("kill", "skarl"),
                "say": [("skarl_hurt", "Call them off... The sea was mine before your Empire had a name. It will be someone's after.")],
                "end": "victory",
            },
        ],
        "brief": [
            ("officer", "Skarl's own anchorage, Commander. A spit of sand, a hall, and his flagship moored across the only approach."),
            ("advisor", "Every reaver on the Mirror Sea answers to him and to nothing else. Take the man and the fleet is only boats."),
        ],
        "victory": [
            ("officer", "The Reaver-King is fallen, Commander. His captains are rowing for the far shore."),
            ("advisor", "The Rukiev coast can fish again, Varius, and so can we. Two seas in one year. The Emperor will run out of water to send you to."),
        ],
        "defeat": [("officer_hurt", "We never reached the sand, Commander. The flagship has thrown us back.")],
        "reward": {"units": {"marines": 1, "efreet": 1}, "spoils": {"Lore": 1, "Spirit": 1}},
    }
)

# ---------------------------------------------------------------- Raid 1. The Fire Ship (reach her tiller in time)
LEVELS.append(
    {
        "id": 5991,
        "group": "siege",
        "name": "The Fire Ship",
        "objective": "Reach the fire ship's tiller before turn 13, or eliminate all enemies.",
        "turn_limit": 14,
        "budget": 4750,
        "sides": {"P": ARMY, "E": REAVERS},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~
~~~bbbbbb~~~~~bbbbbbb~~~
~~bbbbbbbb~~~bbbbbbbbb~~
~~bbbbbbbbbbbbbbbmbbbbb~
~~bbbmbbbb~~~bbbbbbbbbb~
~~bbbbbbbb~~~bbbbbbbccb~
~~bbbmbbbb~~~bbbbbbbbbb~
~~bbbbbbbbbbbbbbbmbbbbb~
~~bbbbbbbb~~~bbbbbbbbb~~
~~~bbbbbb~~~~~bbbbbbb~~~
~~~~~~~~~~~~~~~~~~~~~~~~
""",
        "units": """
........................
...............x...x....
..............g..f...g..
.............h....s.....
...DD.DDD.....g..p......
...DDDDDD......f..B...1.
...DD.DDD.....g..p......
.............h....s.....
..............g..f...g..
...............x...x....
........................
""",
        "legend": {
            "g": U("swordsmen", "E", group=1, hold=True),
            "f": U("footmen", "E", group=2, hold=True),
            "h": U("halberdiers", "E", group=3, hold=True),
            "s": U("swordsmen", "E", group=4, hold=True),
            "p": U("pavisiers", "E", group=5, hold=True),
            "x": U("crossbowmen", "E", group=6, hold=True),
            "B": U("ballistae", "E", group=7, hold=True),
        },
        "camera": (17, 5),
        "intro": [
            ("officer_alarm", "She is packed to the rail with pitch, Commander, and drifting down on the grain fleet!"),
            ("advisor", "Her crew mean to light her and swim. Get one man to the tiller behind her cabin, Varius, and we can put her on the rocks instead."),
        ],
        "events": [
            {
                "when": ("reach", "1"),
                "say": [("officer", "We have the tiller, Commander! She is turning for the rocks.")],
                "end": "victory",
            },
            {
                "when": ("round", 13),
                "say": [("officer_hurt", "She is alight, Commander, and among the grain ships.")],
                "end": "defeat",
            },
        ],
        "victory": [("officer", "The fire ship is aground and burning alone, Commander.")],
        "defeat": [("officer_hurt", "The grain fleet is burning, Commander.")],
        "reward": {"units": {"footmen": 1}, "spoils": {"Armor": 1, "Lore": 1}},
    }
)

# ---------------------------------------------------------------- Raid 2. Wolf Pack (three cutters round your ship)
LEVELS.append(
    {
        "id": 5992,
        "group": "siege",
        "name": "Wolf Pack",
        "objective": "Three reaver cutters have you grappled. Eliminate all enemies.",
        "turn_limit": 30,
        "budget": 3850,
        "sides": {"P": ARMY, "E": REAVERS},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~bbbbbbb~~~~~~bbbbbbb~~~
~~bbbmbbbbb~~~~bbbbbmbbb~~
~~~bbbbbbb~~~~~~bbbbbbb~~~
~~~~~~b~~~~~~~~~~~~b~~~~~~
~~~~~bbbbbbbbbbbbbbbb~~~~~
~~~~bbbbmbbbbbbbbmbbbb~~~~
~~~~bbbbbbbbbbbbbbbbccb~~~
~~~~~bbbbbbbbbbbbbbbb~~~~~
~~~~~~~~~~~~b~~~~~~~~~~~~~
~~~~~~~~~bbbbbbb~~~~~~~~~~
~~~~~~~~bbbbmbbbb~~~~~~~~~
~~~~~~~~~bbbbbbb~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~
""",
        "units": """
..........................
....x..x.........x..x.....
...g..H.g.......g.H..g....
....f.1f.........f.2f.....
..........................
......DDDDDDDDDDDDDD......
.....DDD.DDDDDDDD.DDD.....
.....DDDDDDDDDDDDDD.......
..........................
..........................
..........s.H.s...........
.........m.....m..........
..........x...x...........
..........................
""",
        "legend": {
            "g": U("gladiator", "E", group=1),
            "f": U("footmen", "E", group=2),
            "x": U("crossbowmen", "E", group=3, hold=True),
            "H": U("hounds", "E", group=4),
            "s": U("swordsmen", "E", group=5),
            "m": U("marines", "E"),
        },
        "camera": (12, 6),
        "intro": [
            ("officer_alarm", "Cutters, Commander! Two on the bow and one astern, and hounds on every one of them!"),
            ("advisor", "They hunt as the dogs do, Varius. Three planks, three packs. Hold two and break the third."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (6, 3),
                "spawn": [("hounds", "1", "E"), ("marines", "2", "E")],
                "say": [("officer_alarm", "More of them up from below, Commander!")],
            },
            {
                "when": ("round", 5),
                "cam": (19, 3),
                "spawn": [("hounds", "2", "E"), ("gladiator", "1", "E")],
            },
        ],
        "victory": [("officer", "All three cutters are ours, Commander. The pack is broken.")],
        "defeat": [("officer_hurt", "They are over the rail on every side, Commander.")],
        "reward": {"units": {"swordsmen": 1}, "spoils": {"Weapons": 1, "Beasts": 1}},
    }
)

KINGDOM = {
    "id": "mirror-sea",
    "short": "Mirror Sea",
    "name": "The Mirror Sea",
    "order": 15,
    "theme": "sand",
    "unlock_after": ["Mare Nostra"],
    "heraldry": {"E": ("sable", "gules", 27, 5)},
    "brief": [
        (
            "emperor",
            "Commander Varius, you have given me back Mare Nostra, and I must ask for a second sea. The captains who would not strike with Admiral Corvane have gone north, to the Mirror Sea, and taken service with a pirate who calls himself Reaver-King Skarl.",
        ),
        (
            "emperor",
            "He burns the Rukiev fishing towns and sets beasts on those who run. There is no channel between the two seas. Your ships will be hauled over the Tilician hills. Find this king of reavers and end him.",
        ),
    ],
    "levels": LEVELS,
}
