"""Tilicia — "The Empty Tomb": three story battles and three raids (ours; see build_bonus.py).

Every battle is fought with an army the player musters from the budget (user decision): the three battles that
handed out a fixed force or preset troops (The Tolm Road, The Sealed Vale, The Sleepers Wake) are gone, and the
story runs Ostrak's Bargain, Frostgate, The Empty Tomb."""
from build_bonus import U

LEVELS = []

# ---------------------------------------------------------------- 1. Ostrak's Bargain (defend the clan village)
LEVELS.append(
    {
        "id": 5902,
        "group": "story",
        "name": "Ostrak's Bargain",
        "objective": "Defend the clan village from the Warden's men. At least three of the six Cragsmen bands must survive.",
        "turn_limit": 30,
        "budget": 3000,
        "win_switch": False,
        "sides": {"P": "Carrone Army", "A": "Clan Ostrak", "E": "Tolm's Wardens"},
        "terrain": """
^^^^^^^^^^.==.^^^^^^^^^^
^ff.r....,.==..,...rff.^
^f......ff.==.f......ff^
..f....PPPP==PPPP....f..
.......P.h.==.h.P.,,....
....,,.P...==...P.......
.......P.h.==.h.P...ff..
========================
========================
.......P.h.==.h.P....f..
....f..P...==...P.......
.......P.h.==.h.P..,,...
..f....PPPP==PPPP...f...
^f......f..==.ff.....ff^
^ff.r...,..==...,..r.ff^
^^^^^^^^^^.==.^^^^^^^^^^
""",
        "units": """
........................
........................
........................
........................
DDDD.......mm...........
DDDD....C...............
DDDD......C..C......ff..
DDDD...........m.....r..
DDDD...........m.....r..
DDDD......C..C......ff..
DDDD...........C........
DDDD.......mm...........
........................
........................
........................
........................
""",
        "legend": {
            "C": U("cragsmen", "A", group=1, hold=True, name="clan"),
            "m": U("militiamen", "A", group=2, hold=True),
            "f": U("footmen", "E", group=1),
            "r": U("raiders", "E", group=1),
        },
        "camera": (12, 7),
        "intro": [
            ("ostrak", "So the Empire comes to my door. You climbed the Warden's road to do it, and his men are an hour behind you, Commander."),
            ("ostrak", "Hadrik Tolm takes our sons to dig in his tomb and burns the roof of any clan that refuses. Stand with us today and Clan Ostrak stands with you after."),
            ("advisor", "A fair bargain. Keep the clansmen alive, Varius. We will want every one of them."),
        ],
        "events": [
            {
                "when": ("round", 4),
                "cam": (11, 0),
                "spawn": [
                    ("swordsmen", (11, 0), "E"),
                    ("swordsmen", (12, 0), "E"),
                    ("footmen", (10, 0), "E"),
                    ("footmen", (13, 0), "E"),
                    ("swordsmen", (11, 1), "E"),
                    ("halberdiers", (12, 1), "E"),
                    ("swordsmen", (10, 1), "E"),
                ],
                "say": [("officer_alarm", "More of them on the north road, Commander!")],
            },
            {
                "when": ("round", 6),
                "cam": (11, 15),
                "spawn": [
                    ("swordsmen", (11, 15), "E"),
                    ("footmen", (12, 15), "E"),
                    ("footmen", (10, 15), "E"),
                    ("raiders", (13, 15), "E"),
                    ("raiders", (12, 14), "E"),
                    ("halberdiers", (10, 14), "E"),
                    ("swordsmen", (11, 14), "E"),

                ],
                "say": [("clansman", "The south gap! They are in the south gap!")],
            },
            {
                "when": ("round", 8),
                "cam": (23, 7),
                "spawn": [
                    ("swordsmen", (23, 6), "E"),
                    ("swordsmen", (23, 7), "E"),
                    ("swordsmen", (23, 8), "E"),
                    ("footmen", (23, 5), "E"),
                    ("footmen", (23, 9), "E"),
                    ("raiders", (22, 7), "E"),
                    ("raiders", (22, 8), "E"),
                    ("halberdiers", (22, 6), "E"),
                    ("halberdiers", (22, 9), "E"),
                ],
                "say": [("advisor", "That is the last of the Warden's column. Break it and the village is safe.")],
                "win_switch": True,
            },
            {
                "when": ("kill", "clan", 4),
                "say": [("ostrak", "Enough. My clan is bleeding out for your Emperor. Go back down your road, Commander.")],
                "end": "defeat",
            },
        ],
        "brief": [
            ("advisor", "Tilicia is all mountain, Varius, and Warden Tolm holds the one road wide enough for an army. We will need friends who know the others."),
            ("officer", "The village ahead belongs to Clan Ostrak, Commander. Their chief is one Maren Ostrak, and her people have no love for the Warden."),
            ("advisor", "His riders are on the valley road. If we mean to win these people, now is the hour."),
        ],
        "victory": [
            ("ostrak", "You bled for a village that is not yours. I did not expect that of the Empire."),
            ("ostrak", "Take two bands of my Cragsmen. No wall in Tilicia was built to stop them."),
            ("advisor", "She says one fortress bars the road to the tomb: Frostgate. And that its builders never reckoned with men who climb."),
        ],
        "defeat": [("officer_hurt", "The village is lost, Commander, and the clans with it.")],
        "reward": {"units": {"cragsmen": 2}, "spoils": {}},
    }
)

# ---------------------------------------------------------------- 2. Frostgate (storm the fortress)
LEVELS.append(
    {
        "id": 5904,
        "group": "story",
        "name": "Frostgate",
        "objective": "Storm the fortress of Frostgate and destroy its garrison.",
        "turn_limit": 35,
        "budget": 4500,
        "sides": {"P": "Carrone Army", "E": "Frostgate Garrison"},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^^^
^fff.....r....r.,,.ff^
^ff..............r.f.^
^..TWWWWWWWWWWT..r...^
^..W__________^...ff.^
^..W____K_____^r.....^
^f.W__________^..,,..^
^..W__________^......^
^r.W__________^.ff...^
^..W__________^..f...^
^..TWWWTGTWWWWT......^
^.......==........r..^
^.xxx...==..xxx...ff.^
.ff.....==........f...
..f......==....,,.....
.........==...........
~~~~--~~..............
~~~~--~~.........r....
.f.......==......ff...
..h......==.......f...
.........==....h......
.........==...........
..,,.....==.......,,..
.........==...........
""",
        "units": """
......................
......................
......................
......................
....s..s....t.........
.....b......s.........
............t.........
......w.w..b..........
.......w..............
......ppp.............
....MM....MM..........
......................
......................
......................
......................
......................
......................
......................
......................
......................
.....DDDDDDDDD........
.....DDDDDDDDD........
.....DDDDDDDDD........
.....DDDDDDDDD........
""",
        "legend": {
            "M": U("musketeers", "E", group=1, hold=True),
            "p": U("pikemen", "E", group=2, hold=True),
            "w": U("spellwardens", "E", group=3, hold=True),
            "t": U("trebuchet", "E", group=4, hold=True),
            "b": U("ballistae", "E", group=5, hold=True),
            "s": U("swordsmen", "E", group=6, hold=True),
        },
        "camera": (8, 9),
        "intro": [
            ("officer", "Frostgate, Commander. One gate, and Musketeers on the wall either side of it."),
            ("advisor", "That gate is a killing ground. But look east. The wall ends where the cliff begins."),
            ("advisor", "No soldier of ours can climb it. Ostrak's Cragsmen can, and the Warden's engines stand just behind."),
            ("advisor", "And mark the maces behind the gate. Spellwardens, the tomb's old keepers: no Wizard's fire touches a man who stands near one."),
        ],
        "events": [
            {
                "when": ("round", 6),
                "cam": (21, 14),
                "spawn": [
                    ("cavalry", (21, 13), "E"),
                    ("raiders", (20, 13), "E"),
                    ("raiders", (20, 14), "E"),
                ],
                "say": [("officer_alarm", "Horsemen on the east road, Commander! The Warden has sent riders back to relieve the fortress.")],
            },
        ],
        "brief": [
            ("advisor", "Frostgate bars the last road to the tomb. The Warden has left it a strong garrison and gone on ahead."),
            ("advisor", "Its builders trusted the mountain to guard the eastern side. Let us see whether they were right."),
        ],
        "victory": [
            ("officer", "Frostgate is ours, Commander. A handful of the Spellwardens have laid down their maces."),
            ("advisor", "Men who can snuff out a Wizard's fire. The Warden has been preparing to face magic for some time. Or to keep some of his own on a leash."),
            ("advisor", "They say the Warden broke the last seal on the tomb two days ago, and that the mountain has not been quiet since."),
            ("officer", "They are asking to march with us, Sir Anston. They would rather face what is in that tomb beside an army."),
        ],
        "defeat": [("officer_hurt", "We broke on the gate, Commander. Frostgate still stands.")],
        "reward": {"units": {"spellwardens": 2}, "spoils": {}},
    }
)

# ---------------------------------------------------------------- 3. The Empty Tomb (Warden Tolm)
LEVELS.append(
    {
        "id": 5906,
        "group": "story",
        "name": "The Empty Tomb",
        "objective": "Defeat Warden Tolm before the tomb of the Battlemage.",
        "turn_limit": 30,
        "budget": 6000,
        "sides": {"P": "Carrone Army", "E": "Warden Tolm", "E2": "Stone Sentinels"},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^^^^^
^ff.r...TWWWWWWT..r..ff^
^f......W______W.....f.^
^..,,...W__KK__W..o....^
^.......W______W....r..^
^..o..r.TWWGGWWT.......^
^.....xx...==...xx.,,..^
^...^^^....==....^^^.f.^
^.f........==..........^
^.,,..r....==.......ff.^
^..........===.....r...^
^^^^^..r....==..r..^^^^^
.ff.........==.......f..
..f....,,...==..........
~~~~~--~~~..==..~~~~--~~
~~~~~--~~~..==..~~~~--~~
....f.......==.....ff...
^^^^...r...===......^^^^
.f.........==.......f...
..ff...,,..==........ff.
...........==...........
...........==...........
...........==...........
...........==...........
""",
        "units": """
........................
........................
........................
........................
..........zKz...........
........................
.........aw..wa.........
.....c....ww......c.....
........SS....S.........
.....k.....S......k.....
.........hh..hh.........
..c..................c..
........................
........................
........................
........................
........................
.11..................11.
........................
........................
........................
......DDDDDDDDDDDD......
......DDDDDDDDDDDD......
......DDDDDDDDDDDD......
""",
        "legend": {
            "K": U("king", "E", group=2, hold=True, name="tolm"),
            "z": U("wizards", "E", group=2, hold=True),
            "w": U("spellwardens", "E", group=1, hold=True),
            "a": U("archers", "E", group=1, hold=True),
            "c": U("cragsmen", "E", group=4, hold=True),
            "k": U("knights", "E", group=3),
            "h": U("halberdiers", "E", group=5),
            "S": U("sentinel", "E2", group=1, hold=True),
        },
        "camera": (11, 4),
        "intro": [
            ("tolm", "So this is the Emperor's hound. You are late, Commander. Years late."),
            ("tolm", "Do you know what the old kings paid to bury what lay here? I have dug it out with goatherds."),
            ("officer_alarm", "Sir Anston, the statues before the doors. The statues are moving!"),
            ("advisor", "Guardians of living stone, set there by whoever sealed the Battlemage in. Our Priests cannot mend what they break, and no charge will move them."),
            ("advisor", "He is playing for time, Varius. Take the Warden and this ends."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (2, 17),
                "spawn": [("cragsmen", "1", "E")],
                "say": [("officer_alarm", "Cragsmen on the ledges behind us, Commander! The Warden kept some clans of his own.")],
            },
            {
                "when": ("kill", "tolm"),
                "say": [
                    ("tolm_hurt", "Fools. Open it. Go on, open it and see what you have won."),
                    ("officer", "The Warden is down, Commander. His men are throwing down their arms."),
                ],
                "end": "victory",
            },
        ],
        "brief": [
            ("advisor", "The tomb, Varius, on the plateau above Frostgate. Warden Tolm has drawn up everything he has left before its doors."),
            ("advisor", "Clansmen, Spellwardens, and they say the tomb's own sleepers answer him here. Mind your rear on that plateau."),
        ],
        "victory": [
            ("officer", "Commander, the tomb is open. The sarcophagus is gone. There are drag marks, and cart ruts leading down to the river."),
            ("advisor", "Gone a week, by the look of it. The Warden was never guarding the Battlemage. He was guarding the road it left by."),
            ("officer", "The bargemen say the river runs to the sea, Sir Anston. And that a ship with purple sails was waiting at its mouth."),
            ("advisor", "Purple sails. Isoluccia. One of the stone guardians knelt when the Warden fell, Varius. It seems to be yours now."),
        ],
        "defeat": [("officer_hurt", "The Warden holds the plateau, Commander. We could not reach him.")],
        "reward": {"units": {"sentinel": 1}, "spoils": {}},
    }
)

# ---------------------------------------------------------------- Raid 1. Goat Track (ambush the supply column)
LEVELS.append(
    {
        "id": 5911,
        "group": "siege",
        "name": "Goat Track",
        "objective": "Set an ambush along the track and destroy the Warden's supply column.",
        "turn_limit": 30,
        "budget": 3250,
        "win_switch": False,
        "sides": {"P": "Carrone Army", "E": "Supply Column"},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^^^
^.fff..r..........ff.^
^..f.............,,f.^
^^^^^.r.^^^^...^^^^..^
...r........x.........
======================
======================
.....,,......r........
^^^...^^^^...^^^^.r.^^
^.f................f.^
^fff..r..........,,ff^
^^^^^^^^^^^^^^^^^^^^^^
""",
        "units": """
......................
.........DDDDDDDD.....
.........DDDDDDDD.....
......................
......................
......................
......................
......................
......................
.........DDDDDDDD.....
.........DDDDDDDD.....
......................
""",
        "legend": {},
        "camera": (0, 5),
        "intro": [
            ("officer", "The Warden's supplies come up this track, Commander. The column is due within the hour."),
            ("advisor", "Then we shall be in the trees when it arrives. Let them come well into the cut before we spring it."),
        ],
        "events": [
            {
                "when": ("round", 2),
                "cam": (0, 5),
                "spawn": [
                    ("raiders", (0, 5), "E"),
                    ("raiders", (0, 6), "E"),
                    ("raiders", (1, 5), "E"),
                    ("raiders", (1, 6), "E"),
                    ("raiders", (0, 4), "E"),
                    ("raiders", (0, 7), "E"),
                ],
                "say": [("officer", "Outriders on the track, Commander. The column is behind them.")],
            },
            {
                "when": ("round", 3),
                "cam": (0, 5),
                "spawn": [
                    ("halberdiers", (0, 5), "E"),
                    ("halberdiers", (0, 6), "E"),
                    ("footmen", (1, 5), "E"),
                    ("footmen", (1, 6), "E"),
                    ("cragsmen", (0, 4), "E"),
                    ("cragsmen", (0, 7), "E"),
                    ("cragsmen", (1, 4), "E"),
                    ("cragsmen", (1, 7), "E"),
                ],
            },
            {
                "when": ("round", 4),
                "cam": (0, 5),
                "spawn": [
                    ("swordsmen", (0, 5), "E"),
                    ("swordsmen", (0, 6), "E"),
                    ("swordsmen", (1, 5), "E"),
                    ("rangers", (0, 4), "E"),
                    ("rangers", (0, 7), "E"),
                    ("halberdiers", (1, 6), "E"),
                ],
                "say": [("advisor", "That is the rearguard. The whole column is in the cut. Now, Varius.")],
                "win_switch": True,
            },
        ],
        "victory": [("officer", "The column is taken, Commander. The Warden's garrisons will go hungry.")],
        "defeat": [("officer_hurt", "They cut their way out of the trap, Commander.")],
        "reward": {"units": {"raiders": 1}, "spoils": {"Beasts": 1, "Weapons": 1}},
    }
)

# ---------------------------------------------------------------- Raid 2. Quarry of Giants (Stone Sentinels)
LEVELS.append(
    {
        "id": 5912,
        "group": "siege",
        "name": "Quarry of Giants",
        "objective": "Destroy every stone guardian in the old quarry.",
        "turn_limit": 30,
        "budget": 3000,
        "sides": {"P": "Carrone Army", "E": "Stone Sentinels"},
        "heraldry": {"E": ("cyan", "sable", 44, 6)},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^^^^
^..rr..r....r..r..rr..^
^.....................^
^r..^^^....r....^^^..r^
^.....^....o....^.....^
^..~~.........r.......^
^..~~......,,......r..^
^.r...................^
^^^^.....r...r....^^^^^
^..r.............~~~..^
^...o............~~~..^
^.....r...............^
^..^^^....rr.....^^^.r^
^.r.........,,........^
..f.................ff.
.ff................f...
.......................
.......................
.......................
""",
        "units": """
.......................
.......................
.....S..S..S..S..S.....
.......................
.......................
........T.....T........
.......................
....U...U..V..U...U....
.......................
.......................
......W.W..W..W........
.......................
.......................
.......................
.......................
.......................
......DDDDDDDDDDD......
......DDDDDDDDDDD......
......DDDDDDDDDDD......
""",
        "legend": {
            "S": U("sentinel", "E", group=1),
            "T": U("sentinel", "E", group=2),
            "U": U("sentinel", "E", group=3),
            "V": U("golem", "E", group=3),  # the largest of them (the raid opens the Golem upgrade)
            "W": U("sentinel", "E", group=5),
        },
        "camera": (11, 7),
        "intro": [
            ("officer", "The clans call this the Quarry of Giants, Commander. They say the stone here was never cut by men."),
            ("advisor", "It was cut into soldiers. Sixteen of them, by my count, all of them awake, and one in the middle that the others were only practice for."),
        ],
        "events": [],
        "victory": [
            ("officer", "The quarry is quiet, Commander. Nothing in it is standing."),
            ("advisor", "The great one is whole under the rubble, Varius, runes and all. The craftsmen think they can raise it again, for us."),
        ],
        "defeat": [("officer_hurt", "We cannot stand against them in the open, Commander.")],
        "reward": {"units": {"golem": 1}, "spoils": {"Lore": 2, "Armor": 1}},
    }
)

# ---------------------------------------------------------------- Raid 3. Winter Stores (seize the granaries)
LEVELS.append(
    {
        "id": 5913,
        "group": "siege",
        "name": "Winter Stores",
        "objective": "Seize both of the Warden's granaries within fifteen turns.",
        "mission_type": 2,
        "areas": ["1", "2"],
        "turn_limit": 15,
        "budget": 2500,
        "sides": {"P": "Carrone Army", "E": "Granary Guard"},
        "terrain": """
.ff.........r.......f.
.f.................ff.
...hh..,,.......hh....
...hh....^^^^...hh....
.........^rr^.........
..,,.....^..^.....,,..
.x.......^..^.......x.
.x..f....^..^....f..x.
......r...........r...
...........,,.........
...^^^..........^^^...
.f....................
.ff..f....,,....f..ff.
..f.................f.
~~~~--~~.......~~--~~~
~~~~--~~.......~~--~~~
..h................h..
......................
......................
...,,.............,,..
""",
        "units": """
......................
......................
......................
..a..a.........b..b...
..m11m.........n22n...
...xw...........yv....
...mx...........yn....
......................
..........cc..........
.........ccc..........
......................
......................
......................
......................
......................
......................
......................
......DDDDDDDDDD......
......DDDDDDDDDD......
......DDDDDDDDDD......
""",
        "legend": {
            "a": U("archers", "E", group=1, hold=True),
            "m": U("militiamen", "E", group=1, hold=True),
            "x": U("halberdiers", "E", group=1, hold=True),
            "w": U("spellwardens", "E", group=1, hold=True),
            "b": U("archers", "E", group=2, hold=True),
            "n": U("militiamen", "E", group=2, hold=True),
            "y": U("halberdiers", "E", group=2, hold=True),
            "v": U("spellwardens", "E", group=2, hold=True),
            "c": U("cavalry", "E", group=3),
        },
        "camera": (4, 3),
        "intro": [
            ("officer", "Two granaries, Commander, one either side of that ridge. The Warden's winter stores."),
            ("advisor", "The guard will burn them if we give them a day to think of it. Take both, and quickly."),
        ],
        "events": [
            {
                "when": ("reach_all", ["1", "2"]),
                "say": [("officer", "Both granaries are in our hands, Commander. The guard is running for the hills.")],
                "end": "victory",
            },
        ],
        "victory": [("officer", "The stores are ours, Commander. The clans will eat this winter and the Warden's men will not.")],
        "defeat": [("officer_hurt", "There is smoke over the granaries, Commander. We were too slow.")],
        "reward": {"units": {"militiamen": 2}, "spoils": {"Armor": 1, "Spirit": 1}},
    }
)

KINGDOM = {
    "id": "tilicia",
    "short": "Tilicia",
    "order": 11,
    "theme": "green",
    "unlock_after": ["Abbisin"],
    "heraldry": {"E": ("argent", "azure", 30, 4), "A": ("or", "vert", 12, 3), "E2": ("cyan", "sable", 44, 6)},
    "brief": [
        (
            "thaddius",
            "Commander, we have read the letters Landower's messenger carried. The 'Battlemage' is no spell and no engine. It is a person: a war-sorcerer of the old world, sealed alive in a tomb in the mountains of Tilicia.",
        ),
        (
            "thaddius",
            "Landower's ally there, Warden Hadrik Tolm, is digging that tomb out. If the old texts are true, whoever wakes the Battlemage commands it. Go to Tilicia. Reach the tomb before the Warden opens it.",
        ),
    ],
    "levels": LEVELS,
}
