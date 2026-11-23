"""Isoluccia — "Reign of the Battlemage": three story battles and three raids (ours; see build_bonus.py).

Every battle is fought with an army the player musters from the budget (user decision): Landfall and Free Company,
which handed out a fixed force, are gone with The Causeway between them, and the story runs The Harbour Chain, The
Arsenal, Reign of the Battlemage. Captain Bellaro and his Free Company now come over before the harbour chain and
fight there as an allied army."""
from build_bonus import U

LEVELS = []
ARMY = "Carrone Army"
DOGE = "Doge's Guard"

# ---------------------------------------------------------------- 1. The Harbour Chain (timed capture)
LEVELS.append(
    {
        "id": 5924,
        "group": "story",
        "name": "The Harbour Chain",
        "objective": "Capture both chain towers within 20 turns: bring a unit to the well inside each tower fort.",
        "mission_type": 2,
        "turn_limit": 20,
        "budget": 4500,
        "sides": {"P": ARMY, "A": "Free Company", "E": DOGE},
        "areas": ["1", "2"],
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~~
~~~--~~~~~~~~~~~~~~~--~~~
~..TWWWT.~~~~~~~.TWWWT..~
~..W___W.~~~~~~~.W___W..~
...W_K_W.~~~~~~~.W_K_W...
...W___W.~~~~~~~.W___W...
.,.TWGWT.~~~~~~~.TWGWT.s.
....===..-~~~~~-..===....
.f..=.....~~~~~.....=..f.
....=..~~~~~~~~~~~..=....
.hh.=.=~~~~~~~~~~~=.=.hh.
.hh.=.=~~~~~~~~~~~=.=.hh.
....=.=~~~~~~~~~~~=.=....
.s..=.=--~~~~~~~--=.=..s.
....=.=============.=....
....=...hh.=.hh..o..=....
..f.=================.f..
.....hh.=..F..=.hh.......
........=.....=..........
.........................
.........................
.........................
..s..................f...
""",
        "units": """
.........................
.........................
.........................
....k.k...........K.K....
.....1.............2.....
.........................
....v.v...........V.V....
..m.hhh...........HHH.M..
.........................
..c...................C..
.........................
.........................
...xx...............XX...
.........................
.........................
.....ww...........WW.....
.........................
.........................
.BB...................BB.
.......DDDDDDDDDDD.......
.......DDDDDDDDDDD.......
.......DDDDDDDDDDD.......
.........................
""",
        "legend": {
            "k": U("musketeers", "E", group=1, hold=True),
            "K": U("musketeers", "E", group=2, hold=True),
            "v": U("pavisiers", "E", group=3, hold=True),
            "V": U("pavisiers", "E", group=4, hold=True),
            "h": U("halberdiers", "E", group=5, hold=True),
            "H": U("halberdiers", "E", group=6, hold=True),
            "m": U("musketeers", "E", group=7, hold=True),
            "M": U("musketeers", "E", group=8, hold=True),
            "c": U("catapult", "E", group=9, hold=True),
            "C": U("catapult", "E", group=10, hold=True),
            "x": U("pavisiers", "E", group=11, hold=True),
            "X": U("pavisiers", "E", group=12, hold=True),
            "w": U("halberdiers", "E", group=13, hold=True),
            "W": U("halberdiers", "E", group=14, hold=True),
            "r": U("raiders", "E", group=15),
            "B": U("marines", "A", group=1),  # Bellaro's Free Company: they wade the channel between the forts
        },
        "camera": (12, 5),
        "intro": [
            ("officer", "Two towers, Commander, one on each shore, and the chain hangs between them."),
            ("bellaro", "The windlass is by the well in each fort. Take both and the chain goes to the bottom."),
            ("advisor", "The fleet cannot wait past the tide, Varius. The Captain's marines may wade the channel. Everyone else must choose a shore."),
        ],
        "events": [
            {
                "when": ("reach_all", ["1", "2"]),
                "say": [("officer", "The chain is down, Commander! The fleet is coming in!")],
                "end": "victory",
            },
        ],
        "brief": [
            ("advisor", "There it is, Varius. Isoluccia. Half a hundred islands, one very rich Doge, and a chain as thick as a man across his harbor mouth."),
            ("officer", "A sellsword captain rowed out to the fleet in the night, Commander. Bellaro, of the Free Company. He says his marines are done with the Doge."),
            ("bellaro", "He woke something in the citadel that he cannot rule, and I do not fight beside a thing that does not sleep. No ship of yours will pass that chain. My men know the forts that hold it."),
            ("advisor", "A sellsword, but an honest one by all accounts. Then we open the harbor from the land, Captain, and your company sails with Carrone."),
        ],
        "victory": [
            ("officer", "The fleet is in the harbor, Commander. Siege engines and fresh troops are landing."),
            ("bellaro", "There is the signal. The Free Company sails with Carrone! Take two bands of my marines for your own, Commander. The sea is no wall to them."),
            ("advisor", "And the Doge's own crossbowmen are coming over to us with their shields. They can see how this ends."),
            ("officer", "The Arsenal is the next strongpoint. Whoever holds it holds the harbor."),
        ],
        "defeat": [("officer_hurt", "The tide has turned, Commander. The fleet has stood back out to sea.")],
        "reward": {"units": {"pavisiers": 2, "marines": 2}, "spoils": {"Armor": 1, "Spirit": 1, "Anchor": 2, "Void": 2}},
    }
)

# ---------------------------------------------------------------- 2. The Arsenal (hold for 12 turns)
LEVELS.append(
    {
        "id": 5925,
        "group": "story",
        "name": "The Arsenal",
        "objective": "Hold the Arsenal for 12 turns.",
        "turn_limit": 16,
        "budget": 5400,
        "win_switch": False,
        "sides": {"P": ARMY, "A": "Shipwrights", "E": DOGE, "E2": "Stone Sentinels"},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~
~--~~~~~~~~~~~~~~~--~
..s.T____~~~____T.s..
.f..W_h__~~~__h_W..f.
....W___________W....
.,..W___________W..,.
....W___________W....
.s..W_____F_____W..s.
====G___________G====
....W___________W....
..h.W___________W.h..
....W_h_______h_W....
.f..W___________W....
....TWWWWWGWWWWWT..f.
..,.....r.=.r.....,..
..s.......=.......s..
..........=....s.....
.f........=.........f
""",
        "units": """
.....................
.....................
.a.................b.
..a...............b..
.a.......C.C.......b.
.....................
cc.....DDDDDDD.....ee
..p....DDDDDDD....g..
dd.....DDDDDDD.....gg
..p....DDDDDDD....g..
cc.....DDDDDDD.....ee
.....................
.....................
.....................
.....................
.....y..ssnnnss.y....
.......o.L.x.o.......
......t.iijii.T......
""",
        "legend": {
            "C": U("craftsmen", "A", group=1, hold=True),
            "s": U("swordsmen", "E", group=2),
            "x": U("crossbowmen", "E", group=3),
            "L": U("alchemist", "E", group=3),
            "t": U("trebuchet", "E", group=4, hold=True),
            "T": U("trebuchet", "E", group=5, hold=True),
        },
        "camera": (10, 14),
        "intro": [
            ("officer", "The Arsenal is ours, Commander, but the Doge wants it back before the fleet can unload."),
            ("advisor", "Twelve turns, Varius. Hold these walls twelve turns and the harbor is ours for good."),
            ("advisor", "The yard lies open to the sea on the north side. Watch the water. And let the shipwrights mend what the engines break."),
        ],
        "events": [
            {
                "when": ("round", 2),
                "cam": (2, 3),
                "spawn": [("marines", "a", "E"), ("marines", "b", "E")],
                "say": [("officer_alarm", "The Doge's own marines on both shores, Commander! They are making for the slipway!")],
            },
            {
                "when": ("round", 3),
                "cam": (1, 8),
                "spawn": [("swordsmen", "c", "E"), ("halberdiers", "d", "E"), ("crossbowmen", "p", "E"), ("swordsmen", "o", "E")],
                "say": [("officer", "A column at the west gate!")],
            },
            {
                "when": ("round", 5),
                "cam": (19, 8),
                "spawn": [("marines", "e", "E"), ("crossbowmen", "g", "E")],
                "say": [("officer", "More of them at the east gate, Commander!")],
            },
            {"when": ("round", 6), "cam": (2, 3), "spawn": [("marines", "a", "E"), ("marines", "b", "E")]},
            {
                "when": ("round", 7),
                "cam": (10, 17),
                "spawn": [("swordsmen", "i", "E"), ("halberdiers", "y", "E"), ("trebuchet", "j", "E"), ("swordsmen", "o", "E")],
                "say": [("officer", "Fresh troops from the south, and another engine with them.")],
            },
            {
                "when": ("round", 8),
                "cam": (10, 15),
                "spawn": [("sentinel", "n", "E2"), ("swordsmen", "o", "E")],
                "say": [
                    ("officer_alarm", "Commander, the stone guardians! The ones from the tomb in Tilicia!"),
                    ("advisor", "So that is what came down the river with the sarcophagus. Steel yourselves, men. It is only stone."),
                ],
            },
            {
                "when": ("round", 11),
                "cam": (1, 8),
                "spawn": [("swordsmen", "c", "E"), ("marines", "e", "E"), ("halberdiers", "d", "E"), ("swordsmen", "i", "E")],
                "say": [("officer", "They are throwing in everything they have left, Commander!")],
            },
            {
                "when": ("round", 13),
                "say": [("officer", "The fleet is unloaded, Commander! The Doge's men are falling back to the citadel!")],
                "end": "victory",
            },
        ],
        "brief": [
            ("advisor", "The Doge will throw everything at the Arsenal, Varius. He knows what it means to lose it."),
            ("officer", "The shipwrights have stayed, Commander. They say they would rather mend our walls than his."),
        ],
        "victory": [
            ("officer", "The Arsenal held, Commander."),
            ("advisor", "Stone guardians in the streets of a merchant city. The Doge has stopped pretending."),
            ("advisor", "There is only the citadel left, Varius. And whatever he woke inside it."),
        ],
        "defeat": [("officer_hurt", "The Arsenal is lost, Commander. The fleet is burning at its moorings.")],
        "reward": {"units": {"alchemist": 1}, "spoils": {"Lore": 1, "Weapons": 1, "Spirit": 1, "Void": 2}},
    }
)

# ---------------------------------------------------------------- 3. Reign of the Battlemage
LEVELS.append(
    {
        "id": 5926,
        "group": "story",
        "name": "Reign of the Battlemage",
        "objective": "Storm the citadel and defeat the Battlemage.",
        "turn_limit": 36,
        "budget": 6000,
        "sides": {"P": ARMY, "E": DOGE, "E2": "The Battlemage"},
        "terrain": """
~~~..^^....f.....^^...f.
~~...TWWWWWWWWWWWWT.....
~~-..W____________W.^^..
~--..W____________W..^..
~~...W_____F______W.....
~~~..TWWWWWGGWWWWWT..f..
~~~..W_o________o_W.....
~~~..W____________W..hh.
~~~..TWWWWGGWWWWWWT.....
~~~.......==......hh.s..
~~~..o....==....o.......
~~-..============.hh.,,.
~~-..=hh..==..hh=.......
~~~..=.o..==..o.=..hh.f.
~~~..=hh..==..hh=.......
~~~..============.hh....
~~-...hh..==..hh.....^^.
~~-..h....==....h.s.....
~~....hh..==..hh....f...
~~~.......==............
~~~~..s...==......,,....
~~~~~...................
~~~~--..............s...
~~~~~-..................
~~~~~~..................
~~~~~~~..f..........f...
""",
        "units": """
........................
........................
........j......J........
..........nMn...........
........................
........................
..........k.K.k.........
.......u........U.......
.......v.v...w.w........
...mm...................
.........h..h...........
........................
....B............b......
.........pppp...........
.............s..........
........................
........................
...mm...................
........................
........................
........................
........................
........DDDDDDDDDDDD....
........DDDDDDDDDDDD....
........DDDDDDDDDDDD....
........................
""",
        "legend": {
            "M": U("battlemage", "E2", group=1, hold=True, name="mage"),
            "n": U("sentinel", "E2", group=2, hold=True),
            "N": U("sentinel", "E2", group=3),
            "K": U("king", "E", group=4, hold=True, name="doge"),
            "k": U("knights", "E", group=4, hold=True),
            "j": U("conjurer", "E", group=5, hold=True),
            "J": U("conjurer", "E", group=6, hold=True),
            "u": U("musketeers", "E", group=7, hold=True),
            "U": U("musketeers", "E", group=8, hold=True),
            "v": U("pavisiers", "E", group=9, hold=True),
            "w": U("pavisiers", "E", group=10, hold=True),
            "p": U("pavisiers", "E", group=11, hold=True),
            "h": U("halberdiers", "E", group=12, hold=True),
            "s": U("swordsmen", "E", group=13),
            "B": U("ballistae", "E", group=14, hold=True),
            "b": U("ballistae", "E", group=15, hold=True),
            "m": U("marines", "E"),
            "z": U("pavisiers", "E", group=16, hold=True),
            "Z": U("pavisiers", "E", group=17, hold=True),
        },
        "camera": (11, 4),
        "intro": [
            ("doge", "Commander Varius. You are in time to kneel. The Battlemage is awake, and it answers to me."),
            ("battlemage", "I answer to the one who commands the field. I have not yet seen who that is."),
            ("advisor", "Its lightning leaps from man to man, Varius. Do not pack the ranks. And keep the Tilician wardens near. Their runes are proof against it."),
        ],
        "events": [
            {
                "when": ("kill", "doge"),
                "say": [
                    ("doge_hurt", "Strike them down! I woke you! I command you!"),
                    ("battlemage", "You paid for an army. You never led one. I serve no merchant."),
                ],
            },
            {
                "when": ("kill", "mage"),
                "say": [("battlemage", "Enough. The field is yours, Commander. So, by the old law, am I.")],
                "end": "victory",
            },
        ],
        "brief": [
            ("advisor", "The citadel of Isoluccia. Everything Landower schemed for ends behind that gate."),
            ("officer", "The men are ready, Commander. They would follow you against the old world itself."),
            ("advisor", "They are about to."),
        ],
        "victory": [
            ("battlemage", "In a thousand years no commander has beaten me in the field. The old law is plain. I am yours to order."),
            ("officer", "Commander, the Doge's banners are coming down all over the city."),
            ("advisor", "Landower, Tolm, Sant'Abra. Three men who thought they could own it, and it outlived them all."),
            ("advisor", "It will march home with us, Varius. I only wonder what the Emperor will do with such a weapon."),
        ],
        "defeat": [("officer_hurt", "The lightning... Commander, there is nothing left of the line.")],
        "reward": {"units": {"battlemage": 1}, "spoils": {"Lore": 2, "Spirit": 1, "Void": 2}},
    }
)

# ---------------------------------------------------------------- Raid 1. Smugglers' Cove
LEVELS.append(
    {
        "id": 5931,
        "group": "siege",
        "name": "Smugglers' Cove",
        "objective": "Clear the cove. Eliminate all enemies.",
        "turn_limit": 30,
        "budget": 3600,
        "sides": {"P": ARMY, "E": "Smugglers"},
        "terrain": """
^^....~~~~~~~~~~....^^
^.f...~~~~~~~~~~...f.^
......-~~~~~~~~-......
..s...~~~~~~~~~~...s..
..,,..--~~~~~~--..,,..
...f....--..--....f...
......................
.,,.....h....h.....,,.
...hh............hh...
....f.............s...
.^^......r..r......^^.
..s......o.........f..
......................
......................
......................
.f..s............s..f.
""",
        "units": """
......................
..g................g..
.....m..........m.....
..g..m..........m..g..
....m............m....
...g......mm......g...
......................
........r....r........
.......r..r...r.......
....g.............g...
.........q..q.........
......................
......................
.....DDDDDDDDDDDD.....
.....DDDDDDDDDDDD.....
......................
""",
        "legend": {
            "m": U("marines", "E"),
            "g": U("rangers", "E"),
            "r": U("raiders", "E", group=1),
            "q": U("raiders", "E", group=2),
        },
        "camera": (10, 5),
        "intro": [
            ("officer", "Smugglers, Commander. They have been running the Doge's silver out through this cove."),
            ("advisor", "Mind the dunes and the shallows both. Men who hide for a living are good at it."),
        ],
        "victory": [("officer", "The cove is clear, Commander, and the silver is ours.")],
        "defeat": [("officer_hurt", "They were in the dunes all along, Commander.")],
        "reward": {"units": {"raiders": 1}, "spoils": {"Weapons": 1, "Beasts": 1, "Void": 2}},
    }
)

# ---------------------------------------------------------------- Raid 2. Lighthouse Rock (hold for 10 turns)
LEVELS.append(
    {
        "id": 5932,
        "group": "siege",
        "name": "Lighthouse Rock",
        "objective": "Hold the lighthouse for 10 turns.",
        "turn_limit": 14,
        "budget": 4500,
        "win_switch": False,
        "sides": {"P": ARMY, "E": DOGE},
        "terrain": """
..f...........s....^
....s.........f.....
..~~~~~~~~~~~~~~~~..
..~~~~~~~~~~~~~~~~..
..~~~~~....~~~~~~~..
..~~~..........~~~..
..~~~.r.s......~~~..
..~~.........h.~~~..
.s~~.........o..~~..
..~~~..........~~~.f
..~~~..........~~~..
..~~~......s.r.~~~..
..~~~..........~~~..
..~~~~........~~~~..
..~~~~~~~==~~~~~~~..
..~~~~~~~==~~~~~~~..
..~~~~~~~==~~~~~~~..
...,,...........r...
.f....s......f......
^^................^^
""",
        "units": """
....................
.....a.a.a.a.a......
....................
....................
....................
....................
....................
b......DDDDDD......c
.......DDDDDD......c
b......DDDDDD.......
.b.....DDDDDD......c
b......DDDDDD.......
...................c
....................
....................
....................
....................
......x.ssss.x......
......e.ghhg.e......
.........t..T.......
""",
        "legend": {
            "x": U("crossbowmen", "E", group=1, hold=True),
            "s": U("swordsmen", "E", group=2),
            "t": U("trebuchet", "E", group=3, hold=True),
            "T": U("trebuchet", "E", group=4, hold=True),
        },
        "camera": (9, 16),
        "intro": [
            ("officer", "The light is lit, Commander. The fleet can find the channel as long as it burns."),
            ("advisor", "One causeway for their heavy troops. But marines will come over the rocks from every side. Ten turns, Varius."),
        ],
        "events": [
            {
                "when": ("round", 2),
                "cam": (9, 1),
                "spawn": [("marines", "a", "E")],
                "say": [("officer_alarm", "Marines in the water to the north!")],
            },
            {"when": ("round", 3), "cam": (9, 18), "spawn": [("swordsmen", "g", "E"), ("halberdiers", "h", "E")]},
            {
                "when": ("round", 4),
                "cam": (0, 10),
                "spawn": [("marines", "b", "E")],
                "say": [("officer", "More of them from the west!")],
            },
            {"when": ("round", 5), "cam": (9, 18), "spawn": [("swordsmen", "g", "E"), ("crossbowmen", "e", "E"), ("marines", "b", "E")]},
            {"when": ("round", 6), "cam": (19, 10), "spawn": [("marines", "c", "E"), ("halberdiers", "h", "E")]},
            {"when": ("round", 7), "cam": (9, 18), "spawn": [("swordsmen", "g", "E"), ("swordsmen", "e", "E")]},
            {
                "when": ("round", 8),
                "cam": (9, 18),
                "spawn": [("marines", "b", "E"), ("marines", "c", "E"), ("swordsmen", "g", "E")],
                "say": [("officer_alarm", "They are coming from every side at once, Commander!")],
            },
            {
                "when": ("round", 9),
                "cam": (9, 18),
                "spawn": [("halberdiers", "h", "E"), ("swordsmen", "e", "E"), ("marines", "a", "E")],
            },
            {
                "when": ("round", 11),
                "say": [("officer", "The last ship is through the channel, Commander. They are pulling back.")],
                "end": "victory",
            },
        ],
        "victory": [("officer", "The lighthouse held, Commander.")],
        "defeat": [("officer_hurt", "The light is out, Commander.")],
        "reward": {"units": {"crossbowmen": 1}, "spoils": {"Lore": 1, "Armor": 1, "Void": 2}},
    }
)

# ---------------------------------------------------------------- Raid 3. Pavise Row
LEVELS.append(
    {
        "id": 5933,
        "group": "siege",
        "name": "Pavise Row",
        "objective": "Break the shield line in the market square. Eliminate all enemies.",
        "turn_limit": 30,
        "budget": 4500,
        "sides": {"P": ARMY, "E": DOGE},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~
~~~--~~~~~~~~~~~~~--~~~~
..hh.====.hh.hh.====.hh.
..hh.=..=.......=..=.hh.
....================....
.hh.================.hh.
.hh.==F==========F==.hh.
....================....
.hh.================.hh.
.hh.=======F========....
....================.hh.
.hh.==F==========F==.hh.
.hh.================....
....================.hh.
.f..====........====..f.
..hh.==..hh..hh.==.hh...
..hh.==..hh..hh.==.hh...
.....==.........==......
.s...==...,,....==...s..
........................
........................
........................
........................
.f..................f...
""",
        "units": """
........................
........................
...c................C...
........................
........................
.........ssss...........
.....B............b.....
.........h.hh.h.........
.......vvvvvvvvvv.......
.....gg..........GG.....
..........t..t..........
........................
........................
........................
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
""",
        "legend": {
            "v": U("pavisiers", "E", group=1, hold=True),
            "h": U("halberdiers", "E", group=2, hold=True),
            "B": U("ballistae", "E", group=3, hold=True),
            "b": U("ballistae", "E", group=4, hold=True),
            "s": U("swordsmen", "E", group=5),
            "g": U("halberdiers", "E", group=6, hold=True),
            "G": U("halberdiers", "E", group=7, hold=True),
            "t": U("swordsmen", "E", group=8),
            "c": U("cavalry", "E", group=9),
            "C": U("cavalry", "E", group=10),
        },
        "camera": (12, 8),
        "intro": [
            ("officer", "The guild crossbowmen have drawn up across the market, Commander. Shield to shield."),
            ("advisor", "No cover between us and them, and our arrows will only do half their work. This one is won by hand."),
        ],
        "victory": [("officer", "The square is ours, Commander. That was a line worth breaking.")],
        "defeat": [("officer_hurt", "We never reached their shields, Commander.")],
        "reward": {"units": {"swordsmen": 1}, "spoils": {"Armor": 1, "Weapons": 1, "Spirit": 1, "Void": 2}},
    }
)

KINGDOM = {
    "id": "isoluccia",
    "short": "Isoluccia",
    "order": 12,
    "theme": "sand",
    "unlock_after": ["Tilicia"],
    "heraldry": {"E": ("or", "purpure", 20, 5), "A": ("cyan", "azure", 8, 3), "E2": ("cyan", "sable", 44, 6)},
    "brief": [
        (
            "thaddius",
            "Commander, the tomb was empty because the sarcophagus had already gone down the river to the coast, and from there by ship to Isoluccia.",
        ),
        (
            "thaddius",
            "Doge Aurelio Sant'Abra paid for all of it: Landower, Tolm, the digging. He means to rule the Empire through the Battlemage. The Emperor's fleet will carry your army to the islands, but his harbor is chained shut. Open it, take the city, and do not let him finish waking it.",
        ),
    ],
    "levels": LEVELS,
}
