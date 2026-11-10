"""The Mirror Sea — three story battles and two raids fought ship to ship in Mare Nostra (ours; see build_bonus.py).

Every map is open sea with hulls laid on it: "b" deck, "m" a mast, "c" a cabin. Ships are joined by gangplanks (one or
two "b" tiles) or lie hull to hull. Only Marines leave the decks.
"""
from build_bonus import U

LEVELS = []
ARMY = "Carrone Army"
FLEET = "Corvane's Fleet"
COMPANY = "Free Company"

# ---------------------------------------------------------------- 1. Grapples Away (first boarding action)
LEVELS.append(
    {
        "id": 5941,
        "group": "story",
        "name": "Grapples Away",
        "objective": "Board the picket ship and its cutter. Eliminate all enemies.",
        "turn_limit": 30,
        "budget": 2500,
        "sides": {"P": ARMY, "A": COMPANY, "E": FLEET},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~bbbbbbbbbb~~~~~~b~~~
~~~~~bbbbbbbbbbbbb~~~bbb~~
~~~~ccbbmbbbbmbbbbbbbbmb~~
~~~~~bbbbbbbbbbbbb~~~bbb~~
~~~~~~bbbbbbbbbb~~~~~bbb~~
~~~~~~~~b~~~~b~~~~~~~bcb~~
~~~~~~bbbbbbbbbb~~~~~bbb~~
~~~~~bbbbbbbbbbbb~~~~~b~~~
~~~~bbbbmbbbbmbbccb~~~~~~~
~~~~~bbbbbbbbbbbb~~~~~~~~~
~~~~~~bbbbbbbbbb~~~~~~~~~~
~~-~~~~~~~~~~~~~~~~~~--~~~
""",
        "units": """
..........................
..........................
.......x..x..x............
.....m..s.....s..m...a.a..
......m...h..........pp...
.....m..g.h.sg...m....B...
.......gf.s..fg...........
..........................
......M........M..........
........DDDDDD............
....DDDD.DDDD.DD..D.......
.....DDDDDDDDDDDD.........
......M........M..........
..........................
""",
        "legend": {
            "M": U("marines", "A", group=1),
            "g": U("gladiator", "E", group=2, hold=True),
            "f": U("footmen", "E", group=3, hold=True),
            "h": U("halberdiers", "E", group=4, hold=True),
            "x": U("crossbowmen", "E", group=5, hold=True),
            "a": U("archers", "E", group=6, hold=True),
            "B": U("ballistae", "E", group=7, hold=True),
            "m": U("marines", "E"),
            "s": U("swordsmen", "E", group=8, hold=True),
            "p": U("pavisiers", "E", group=9, hold=True),
        },
        "camera": (11, 5),
        "intro": [
            ("bellaro", "Grapples are fast, Commander. Two planks across, and not a breath of wind to part us."),
            ("officer", "Those are no sailors on her deck. Net and trident, sword and buckler. Arena men."),
            ("advisor", "Gladiators, Varius. Crowd one and his blade finds every man around him. Come at them one rank at a time."),
        ],
        "brief": [
            ("bellaro", "There she lies, Commander. One of Corvane's pickets, with a cutter in tow, and the sea like glass."),
            ("advisor", "No wind, no oars worth the name. A sea battle here is a land battle on planks. We know how to fight those."),
        ],
        "victory": [
            ("officer", "The picket is ours, Commander, and the cutter with her."),
            ("bellaro", "Her log says the Admiral is moving a convoy through the calm. Three hulls lashed together, low in the water."),
            ("advisor", "Then that is where his fighters will be. And his silver."),
        ],
        "defeat": [("officer_hurt", "They have cut the grapples, Commander. We are adrift.")],
        "reward": {"units": {}, "spoils": {"Weapons": 1, "Armor": 1}},
    }
)

# ---------------------------------------------------------------- 2. The Lashed Convoy
LEVELS.append(
    {
        "id": 5942,
        "group": "story",
        "name": "The Lashed Convoy",
        "objective": "Take the three lashed hulls of the convoy. Eliminate all enemies.",
        "turn_limit": 36,
        "budget": 3500,
        "sides": {"P": ARMY, "A": COMPANY, "E": FLEET},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~bbb~~~~~~~~~~~~
~~~~bb~~~~bbbbb~~~~~~~~~~~
~~~bbbb~~~bbmbb~~~~bb~~~~~
~~~bmbb~~~bbbbbbbbbbbb~~~~
~~~bbbbbbbbbbbb~~~bbmb~~~~
~~~bbbb~~~bbmbb~~~bbbb~~~~
~~~bbbb~~~bbbbb~~~bbbb~~~~
~~~bmbb~~~bbbbb~~~bbbb~~~~
~~~bbbb~~~bbbbbbbbbbmb~~~~
~~~bbbbbbbbbmbb~~~bbbb~~~~
~~~bbbb~~~bbbbb~~~bbbb~~~~
~~~bccb~~~bcccb~~~bccb~~~~
~~~~bb~~~~bbbbb~~~~bb~~~~~
~~~~~b~~~~~bbb~~~~~~~~~~~~
~~~~~b~~~~~~b~~~~~~~~~~~~~
~~~~~bbbbbbbbbbbbb~~~~~~~~
~~~~bbbmbbbbbbmbbbb~~~~~~~
~~~~bbbbbbbbbbbbbcc~~~~~~~
~~~~~bbbbbbbbbbbbb~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~--~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~
""",
        "units": """
..........................
..........................
....yy.....a.a............
...m..m............bb.....
..................n..n....
....f......x.x............
...................ss.....
....ff.....sBs.....ss.....
..........t...t...........
....g......hGh............
...................kk.....
....gg.....G.G............
....................k.....
............G.............
...........v.v............
..........................
..........................
....DDD.DDDDDD.DDDD.......
....DDDDDDDDDDDDD.........
......M....M....M.........
..........................
..........................
""",
        "legend": {
            "M": U("marines", "A", group=1),
            "m": U("marines", "E"),
            "n": U("marines", "E"),
            "f": U("footmen", "E", group=2, hold=True),
            "g": U("gladiator", "E", group=3, hold=True),
            "a": U("archers", "E", group=4, hold=True),
            "x": U("crossbowmen", "E", group=5, hold=True),
            "B": U("ballistae", "E", group=6, hold=True),
            "h": U("halberdiers", "E", group=7, hold=True),
            "G": U("gladiator", "E", group=8, hold=True),
            "s": U("swordsmen", "E", group=9, hold=True),
            "k": U("gladiator", "E", group=10, hold=True),
            "y": U("crossbowmen", "E", group=11, hold=True),
            "b": U("archers", "E", group=12, hold=True),
            "t": U("swordsmen", "E", group=13, hold=True),
            "v": U("pavisiers", "E", group=14, hold=True),
        },
        "camera": (12, 9),
        "intro": [
            ("officer", "Three hulls lashed beam to beam, Commander, and planks between them like streets."),
            ("gladiator", "Come aboard, soldiers of the Empire. The sand is wet today, but the crowd is the same."),
            ("advisor", "Two planks lead from our deck, Varius. Whatever crosses them fights alone until the next man is over. Let Bellaro's marines take the long way round."),
        ],
        "brief": [
            ("bellaro", "The convoy, Commander. Corvane emptied the arenas of six cities to guard it."),
            ("advisor", "Men who fight for a crowd fight to be seen. Give them nothing to play to."),
        ],
        "victory": [
            ("gladiator", "Well fought. We were sold to the Admiral by the season. The season is over."),
            ("officer", "Commander, a good number of the arena men are asking for our colors."),
            ("advisor", "Take them, Varius. I would sooner have that sword arm beside me than across a plank."),
            ("bellaro", "And the convoy's master has talked. Corvane's flagship lies a day's drift to the east."),
        ],
        "defeat": [("officer_hurt", "We never got off our own deck, Commander.")],
        "reward": {"units": {"gladiator": 2}, "spoils": {"Beasts": 1}},
    }
)

# ---------------------------------------------------------------- 3. The Admiral's Deck
LEVELS.append(
    {
        "id": 5943,
        "group": "story",
        "name": "The Admiral's Deck",
        "objective": "Board the flagship and defeat Admiral Corvane.",
        "turn_limit": 32,
        "budget": 4500,
        "sides": {"P": ARMY, "A": COMPANY, "E": FLEET},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~bbbbbbbbbb~~~~~~~~~
~~~~b~~~bbbbbbbbbbbb~~~b~~~~
~~~bbbbccbmbbbmbbbmbbbbbb~~~
~~~bmb~~bbbbbbbbbbbb~~bmb~~~
~~~bbb~~~bbbbbbbbbb~~~bbb~~~
~~~bbb~~~~~b~~~~b~~~~~bbb~~~
~~~bbb~~~~~b~~~~b~~~~~bbb~~~
~~~bmb~~~bbbbbbbbbb~~~bmb~~~
~~~bbb~~bbbbbbbbbbbb~~bbb~~~
~~~bbbbbbbbmbbbbmbbbbbbbb~~~
~~~bcb~~bbbbbbbbbbbb~~bcb~~~
~~~~b~~~~bbbbbbbccb~~~~b~~~~
~~~~~~~~~~~~~-~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""",
        "units": """
............................
............................
...........x.....x..........
....m....x........xn...o....
........Kp..h...h...........
...m.m..p..g.g.g.tt...o.o...
....B......g.h..g......b....
....w..................e....
............................
...w.w...M........M...e.e...
....w.......DDDDDD.....e....
.......DDDD.DDDD.DDDD.......
........DDDDDDDDDDDD........
..........M....M............
............................
............................
""",
        "legend": {
            "M": U("marines", "A", group=1),
            "K": U("king", "E", group=2, hold=True, name="corvane"),
            "g": U("gladiator", "E", group=3, hold=True),
            "h": U("halberdiers", "E", group=2, hold=True),
            "x": U("crossbowmen", "E", group=4, hold=True),
            "B": U("ballistae", "E", group=5, hold=True),
            "b": U("ballistae", "E", group=6, hold=True),
            "w": U("swordsmen", "E", group=7),
            "e": U("swordsmen", "E", group=8),
            "m": U("marines", "E"),
            "n": U("marines", "E"),
            "o": U("marines", "E"),
            "p": U("pavisiers", "E", group=2, hold=True),
            "t": U("swordsmen", "E", group=9, hold=True),
        },
        "camera": (13, 4),
        "intro": [
            ("admiral", "Commander Varius. You have come a long way to drown. The Doge is dead, but his fleet is mine, and the sea lanes with it."),
            ("bellaro", "His escorts lie either side of us, Commander. Planks to both, and two more straight onto the flagship."),
            ("advisor", "Four ways across and none of them wide. The Admiral stands at the stern. Take him and the fleet strikes its colors."),
        ],
        "events": [
            {
                "when": ("kill", "corvane"),
                "say": [("admiral_hurt", "Strike... strike the colors. The calm has beaten me, not you.")],
                "end": "victory",
            },
        ],
        "brief": [
            ("bellaro", "The flagship, Commander, with an escort on each beam. He has nowhere to run without a wind."),
            ("advisor", "Nor have we. Whoever holds these decks at sunset holds Mare Nostra."),
        ],
        "victory": [
            ("officer", "The fleet has struck, Commander. The sea lanes are open."),
            ("bellaro", "You will want to see the Admiral's chart room. He was not only starving the Empire."),
            ("advisor", "Letters, Varius. Corvane was selling what the Doge learned from the Battlemage. Runes, rites, all of it."),
            ("advisor", "The buyer is a warlord in the isles of Satoshi, far to the east. It seems our voyage is not over."),
        ],
        "defeat": [("officer_hurt", "The flagship has thrown us back, Commander. Our own deck is burning.")],
        "reward": {"units": {}, "spoils": {"Lore": 1, "Spirit": 1, "Armor": 1}},
    }
)

# ---------------------------------------------------------------- Raid 1. Blockade Runner (hold for 8 turns)
LEVELS.append(
    {
        "id": 5951,
        "group": "siege",
        "name": "Blockade Runner",
        "objective": "Hold your deck for 8 turns against the boarders.",
        "turn_limit": 12,
        "budget": 3000,
        "win_switch": False,
        "sides": {"P": ARMY, "E": FLEET},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~bbbbbbbbbb~~~~~~~
~~~~~~bbbmbbbbmbbb~~~~~~
~~~~~~~bbbbbbbbbb~~~~~~~
~~~~~~~~b~~~~~~b~~~~~~~~
~~~~~~~bbbbbbbbbb~~~~~~~
~~~~~~bbbbbbbbbbbb~~~~~~
~~~~~bbbmbbbbbbmbccb~~~~
~~~~~~bbbbbbbbbbbb~~~~~~
~~~~~~~bbbbbbbbbb~~~~~~~
~~~~~~~~~b~~~~b~~~~~~~~~
~~~~~~~bbbbbbbbbb~~~~~~~
~~~~~~bbbmbbbbmbbb~~~~~~
~~~~~~~bbbbbbbbbb~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~
""",
        "units": """
........................
.........e..e...........
......a.f..gg..f.a......
.........y..y...........
........................
........................
.......DDDDDDDDDD.......
.........DDDDDD.........
.......DDDDDDDDDD.......
........................
........................
.........s..s...........
......d.c.x..x.c.d......
..........h..h..........
........................
""",
        "legend": {
            "g": U("gladiator", "E", group=1),
            "s": U("swordsmen", "E", group=2),
            "x": U("crossbowmen", "E", group=3, hold=True),
        },
        "camera": (11, 7),
        "intro": [
            ("officer", "Two galleys alongside, Commander, one on each beam. They have us grappled."),
            ("advisor", "The current will carry us past the blockade in eight turns. Hold the deck until then, Varius. Watch the planks, and watch the water."),
        ],
        "events": [
            {
                "when": ("round", 2),
                "cam": (11, 2),
                "spawn": [("marines", "a", "E"), ("footmen", "f", "E"), ("gladiator", "e", "E")],
                "say": [("officer_alarm", "Marines over the side to the north!")],
            },
            {
                "when": ("round", 3),
                "cam": (11, 12),
                "spawn": [("gladiator", "c", "E"), ("marines", "d", "E"), ("swordsmen", "h", "E")],
            },
            {"when": ("round", 4), "cam": (11, 2), "spawn": [("marines", "a", "E"), ("crossbowmen", "y", "E")]},
            {
                "when": ("round", 5),
                "cam": (11, 2),
                "spawn": [("gladiator", "e", "E"), ("marines", "d", "E")],
                "say": [("officer", "More arena men on the north galley, Commander!")],
            },
            {
                "when": ("round", 6),
                "cam": (11, 12),
                "spawn": [("swordsmen", "h", "E"), ("gladiator", "c", "E"), ("marines", "a", "E")],
            },
            {
                "when": ("round", 7),
                "cam": (11, 2),
                "spawn": [("footmen", "f", "E"), ("marines", "d", "E"), ("gladiator", "e", "E")],
            },
            {
                "when": ("round", 9),
                "say": [("officer", "We are through the blockade, Commander! They are cutting their own grapples!")],
                "end": "victory",
            },
        ],
        "victory": [("officer", "We ran the blockade, Commander. The grain ships can follow.")],
        "defeat": [("officer_hurt", "They have the deck, Commander.")],
        "reward": {"units": {"footmen": 1}, "spoils": {"Armor": 1, "Spirit": 1}},
    }
)

# ---------------------------------------------------------------- Raid 2. Prize Convoy
LEVELS.append(
    {
        "id": 5952,
        "group": "siege",
        "name": "Prize Convoy",
        "objective": "Take both prize hulls. Eliminate all enemies.",
        "turn_limit": 30,
        "budget": 3500,
        "sides": {"P": ARMY, "E": FLEET},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~-~~~~~~~~~~~~~
~~~bbbbbbbbb~~~~bbbbbbbbb~~~
~~bbbmbbbbbbbbbbbbbbbbmbbb~~
~~bccbbbbmbbb~~bbbmbbbbccb~~
~~~bbbbbbbbb~~~~bbbbbbbbb~~~
~~~~~~~~~b~~~~~~~~b~~~~~~~~~
~~~~~~~~~b~~~~~~~~b~~~~~~~~~
~~~~~~~~bbbbbbbbbbbb~~~~~~~~
~~~~~~~bbbmbbbbbbmbbb~~~~~~~
~~~~~~~bbbbbbbbbbbccb~~~~~~~
~~~~~~~~bbbbbbbbbbbb~~~~~~~~
~~~~-~~~~~~~~~~~~~~~~~~-~~~~
""",
        "units": """
............................
............................
....x..x..x......a..a.......
..m......gf.....s....k.B.n..
......g.g..w...p..k.k.......
...m..w.g.f.....s..s..s..n..
............................
............................
........DDDDDDDDDDDD........
.......DDD.DDDDDD.DDD.......
............................
............................
............................
""",
        "legend": {
            "x": U("crossbowmen", "E", group=1, hold=True),
            "g": U("gladiator", "E", group=2, hold=True),
            "f": U("footmen", "E", group=3, hold=True),
            "a": U("archers", "E", group=4, hold=True),
            "k": U("gladiator", "E", group=5, hold=True),
            "s": U("swordsmen", "E", group=6, hold=True),
            "B": U("ballistae", "E", group=7, hold=True),
            "m": U("marines", "E"),
            "n": U("marines", "E"),
            "w": U("swordsmen", "E", group=8, hold=True),
            "p": U("pavisiers", "E", group=9, hold=True),
        },
        "camera": (13, 4),
        "intro": [
            ("officer", "Two prizes under tow, Commander, and prize crews of arena men aboard both."),
            ("advisor", "One plank to each hull. Split the army or take them in turn, Varius, but mind the swimmers."),
        ],
        "victory": [("officer", "Both prizes are ours, Commander. The cargo is Imperial grain. It can go home.")],
        "defeat": [("officer_hurt", "We are driven back to our own deck, Commander.")],
        "reward": {"units": {"crossbowmen": 1}, "spoils": {"Weapons": 1, "Lore": 1}},
    }
)

KINGDOM = {
    "id": "mirror-sea",
    "short": "Mirror Sea",
    "name": "The Mirror Sea",
    "order": 13,
    "theme": "sand",
    "unlock_after": ["Isoluccia"],
    "heraldry": {"E": ("argent", "sable", 20, 5), "A": ("cyan", "azure", 8, 3)},
    "brief": [
        (
            "emperor",
            "Commander Varius, the Doge is fallen but his fleet is not. Admiral Corvane has taken it out into the becalmed heart of Mare Nostra, the water our sailors call the Mirror Sea, and no grain ship has reached Carrone in a month.",
        ),
        (
            "emperor",
            "He has filled his decks with the arena gladiators of the island cities. Captain Bellaro and his Free Company will sail with you. Find the Admiral, board him, and open my sea lanes.",
        ),
    ],
    "levels": LEVELS,
}
