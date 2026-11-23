"""The Isles of Moananui — three story battles and two raids among the lagoons (ours; see build_bonus.py).
A Polynesian island realm of voyaging canoes: a landing on a black-sand beach held by Toa, a reef crossing under the
hawk riders, and the fenced hilltop village of an elder whose Taniwha rises out of the lagoon. Water matters here:
the Toa wade shallows as if they were sand, and the Taniwha swims where nothing else can stand. It opens with the
bonus campaigns (beside Tilicia) and nothing waits on it."""
from build_bonus import U

LEVELS = []
ARMY = "Carrone Army"
CANOES = "Matahi's Canoes"

# ---------------------------------------------------------------- 1. The Black Sand Landing (Toa on a beach)
LEVELS.append(
    {
        "id": 5944,
        "group": "story",
        "name": "The Black Sand Landing",
        "objective": "Land on the beach and break the Toa who hold it. Eliminate all enemies.",
        "turn_limit": 30,
        "budget": 2000,
        "sides": {"P": ARMY, "E": CANOES},
        "terrain": """
..f..h......h..f....
.ff..............ff.
.f......,,......f...
....................
..f....x..x....f....
....................
...k-k......---.....
..-----....-----....
..--~--....--~--..f.
..-----....-----....
...---......k-k.....
....................
.f................f.
ff......,,......ff..
....................
....................
....................
....................
--------------------
--------------------
~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~
""",
        "units": """
....................
....................
......a......a......
....................
........t..t........
.....t........t.....
....................
....T......T........
....................
....T.......T.......
....................
.......l..l.........
....................
....................
....................
....DDDDDDDDDDDD....
....DDDDDDDDDDDD....
....DDDDDDDDDDDD....
....................
....................
....................
....................
""",
        "legend": {
            "a": U("archers", "E", group=1, hold=True),
            "t": U("toa", "E", group=2, hold=True),
            "T": U("toa", "E", group=3),
            "l": U("footmen", "E", group=4),
        },
        "camera": (9, 7),
        "intro": [
            ("officer", "We are ashore, Commander. Black sand, two lagoons, and a village behind the palms."),
            ("kahu", "Those are Matahi's Toa in the water. Watch how they walk through it. The lagoon is a road to them, and a bog to you."),
            ("advisor", "Spearmen who strike hardest at a fresh foe, Varius. Let them spend that first thrust on our shields, not on our archers."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (1, 8),
                "spawn": [
                    ("toa", (0, 8), "E"),
                    ("toa", (1, 9), "E"),
                    ("toa", (18, 9), "E"),
                    ("toa", (19, 8), "E"),
                ],
                "say": [("officer_alarm", "More of them round the lagoons, Commander! Both flanks!")],
            },
            {
                "when": ("round", 6),
                "cam": (9, 0),
                "spawn": [
                    ("toa", (9, 0), "E"),
                    ("toa", (10, 0), "E"),
                    ("archers", (8, 1), "E"),
                    ("archers", (11, 1), "E"),
                ],
                "say": [("enemy", "Back into the sea with them! The elder has spoken!")],
            },
        ],
        "brief": [
            ("kahu", "I am Kahu, Commander. I have steered canoes between these islands since I was a boy, and I will steer your ships to the one beach where Matahi's men cannot stop you in the surf."),
            ("advisor", "They can stop us on the sand instead, Varius. The navigator says the Toa will be waiting."),
        ],
        "victory": [
            ("officer", "The beach is ours, Commander. The Toa have gone back into the palms."),
            ("kahu", "Not all of them. Some stayed to look at men who can take that first thrust and stand. They would rather fight beside such men than against them."),
        ],
        "defeat": [("officer_hurt", "They have driven us back into the surf, Commander.")],
        "reward": {"units": {"toa": 1}, "spoils": {"Spirit": 1, "Weapons": 1, "Whalebone": 2}},
    }
)

# ---------------------------------------------------------------- 2. The Reef Crossing (hawk riders over a lagoon)
LEVELS.append(
    {
        "id": 5945,
        "group": "story",
        "name": "The Reef Crossing",
        "objective": "Cross the reef to the inner island. Eliminate all enemies.",
        "turn_limit": 32,
        "budget": 2950,
        "sides": {"P": ARMY, "E": CANOES},
        "terrain": """
..f....h..........h....f
.ff..................ff.
..f.......,,..........f.
........................
......x..........x......
........................
---------......---------
--------kk....kk--------
--~~---r--------r--~~---
--~~--------------~~----
------r----------r------
------kkk......kkk------
----................----
........................
.f....................f.
ff........,,..........ff
........................
........................
........................
........................
.f....................f.
ffff................ffff
""",
        "units": """
........................
........................
.....a....R..R....a.....
...........o............
.......t........t.......
.........tt..tt.........
........................
........................
......T..........T......
........................
...T................T...
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
            "R": U("tahuanui", "E", group=2),
            "o": U("tohunga", "E", group=3, hold=True),
            "t": U("toa", "E", group=3, hold=True),
            "T": U("toa", "E", group=4),
        },
        "camera": (11, 8),
        "intro": [
            ("kahu", "The reef, Commander. Knee-deep at this tide from here to the inner island, and no other way across."),
            ("officer", "Something big is turning over the far shore. Birds, with men on them."),
            ("kahu", "Tahuanui. Sea-hawks, and the boys who are light enough to ride them. They do not trouble shield-men. They stoop on bowmen, and priests, and anything on wheels."),
            ("advisor", "Then our archers cross in the middle of the line, Varius, with spears either side of them."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (0, 13),
                "spawn": [("tahuanui", (0, 13), "E"), ("tahuanui", (23, 13), "E")],
                "say": [("officer_alarm", "Hawks behind us, Commander! They have come round over the water!")],
            },
            {
                "when": ("round", 6),
                "cam": (11, 0),
                "spawn": [
                    ("tahuanui", (4, 0), "E"),
                    ("tahuanui", (19, 0), "E"),
                    ("toa", (11, 0), "E"),
                    ("toa", (12, 0), "E"),
                ],
                "say": [("enemy", "The elder's own guard! Hold the shore until they are among them!")],
            },
        ],
        "brief": [
            ("kahu", "Matahi's village stands on the inner island, Commander, behind a reef that has drowned better armies than yours. I mean no insult. They were my cousins."),
            ("advisor", "A lagoon to wade and hawks overhead, Varius. I would rather storm a wall."),
        ],
        "victory": [
            ("officer", "We are across, Commander, and the far shore is ours."),
            ("kahu", "One of the hawks has come down among your horse-boys and will not leave them. A hawk chooses its rider, Commander, not the other way. I would let it."),
        ],
        "defeat": [("officer_hurt", "We cannot cross under those birds, Commander. The reef is theirs.")],
        "reward": {"units": {"tahuanui": 1}, "spoils": {"Beasts": 1, "Lore": 1, "Whalebone": 2}},
    }
)

# ---------------------------------------------------------------- 3. The Hill of Spirits (the elder's fenced village)
LEVELS.append(
    {
        "id": 5946,
        "group": "story",
        "name": "The Hill of Spirits",
        "objective": "Storm the hilltop village and defeat Elder Matahi.",
        "turn_limit": 34,
        "budget": 2900,
        "sides": {"P": ARMY, "E": CANOES},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^^^^^
^^^..PPPPPPPPPPPPPP..^^^
^^...P............P...^^
^^...P..h..F...h..P...^^
^^...P............P...^^
^^...P..h......h..P...^^
^^...P............P...^^
^^...PPPPPPppPPPPPP...^^
^^.........==.........^^
^..r.......==.......r..^
^..........==..........^
^^..f......==......f..^^
^^.ff......==......ff.^^
^..........==..........^
...,,......==......,,...
...........==...........
---........==........---
---kk......==......kk---
-~~---.....==.....---~~-
-~~---.....==.....---~~-
-----......==......-----
---........==........---
...........==...........
...........==...........
""",
        "units": """
........................
........................
........................
........................
...........E............
.........t....t.........
......a..........a......
........................
..........tt............
.......R........R.......
........................
......t..........t......
........................
....T..............T....
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
""",
        "legend": {
            "E": U("tohunga", "E", group=1, hold=True, name="matahi"),
            "t": U("toa", "E", group=1, hold=True),
            "a": U("archers", "E", group=2, hold=True),
            "R": U("tahuanui", "E", group=3),
            "T": U("toa", "E", group=4),
        },
        "camera": (11, 5),
        "intro": [
            ("matahi", "You have walked a long way over my reef to stand on ground that is tapu, stranger."),
            ("matahi", "My fathers sleep in this hill, and the guardian of these waters has heard them wake. Go back to your ships while the lagoon still lets you."),
            ("kahu", "He means the Taniwha, Commander. Stay off the water's edge. It swims the deep where no man can stand, and it strikes hardest from the water."),
            ("advisor", "The old man mends his warriors as fast as we cut them, Varius. Kill him and the rest is only a fence."),
        ],
        "events": [
            {
                "when": ("kill", "matahi"),
                "say": [
                    ("matahi_hurt", "Then the hill has chosen... Kahu, see that they tread softly here..."),
                    ("kahu", "I will, uncle. Toa of Moananui! The elder is gone to his fathers. Put up your spears."),
                ],
                "end": "victory",
            },
            {
                "when": ("round", 4),
                "cam": (2, 18),
                "spawn": [("taniwha", (2, 18), "E"), ("taniwha", (21, 19), "E")],
                "say": [("officer_alarm", "The lagoon, Commander! Something is coming up out of it, on both sides of us!")],
            },
            {
                "when": ("round", 7),
                "cam": (11, 8),
                "spawn": [
                    ("toa", (9, 9), "E"),
                    ("toa", (14, 9), "E"),
                    ("tahuanui", (4, 2), "E"),
                    ("tahuanui", (19, 2), "E"),
                ],
                "say": [("matahi", "Rise, sons of the canoe! The ancestors are watching you!")],
            },
        ],
        "brief": [
            ("kahu", "The Hill of Spirits, Commander. A fence of stakes, the meeting house, and Matahi himself. He is a tohunga, a keeper of the old words, and he is my mother's brother."),
            ("advisor", "And he has a sea-serpent in the lagoon at the foot of his hill, Varius, if the navigator is to be believed. After the hawks, I believe him."),
        ],
        "victory": [
            ("officer", "The elder is dead, Commander. The Toa have grounded their spears, and the thing in the lagoon has gone back under."),
            ("kahu", "The young keepers have asked to sail with you. They say the words should travel, now that the man who kept them here is gone."),
            ("advisor", "The islands will send the Emperor their canoes after this, Varius, and no reaver will ever find a harbour here again."),
        ],
        "defeat": [("officer_hurt", "The hill has thrown us back, Commander. The fence still stands.")],
        "reward": {"units": {"tohunga": 1}, "spoils": {"Spirit": 1, "Lore": 1, "Beasts": 1, "Whalebone": 2}},
    }
)

# ---------------------------------------------------------------- Raid 1. The Canoe Fleet (burn the canoes on the beach)
LEVELS.append(
    {
        "id": 5947,
        "group": "siege",
        "name": "The Canoe Fleet",
        "objective": "Reach the war canoes on the beach within fourteen turns, or eliminate all enemies.",
        "turn_limit": 14,
        "budget": 1400,
        "sides": {"P": ARMY, "E": "Canoe Guard"},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~
----------------------
----kkk--------kkk----
..x..x..x..x..x..x....
......................
.f..................f.
ff.....h....h......ff.
......................
...,,............,,...
......................
..r................r..
......................
.f..................f.
......................
......................
......................
......................
ff..................ff
""",
        "units": """
......................
......................
......................
......................
.....t...1.t..........
........t..t..........
....a...........a.....
......................
......R........R......
......................
.........tt...........
......................
......................
......................
.....DDDDDDDDDDDD.....
.....DDDDDDDDDDDD.....
.....DDDDDDDDDDDD.....
......................
""",
        "legend": {
            "t": U("toa", "E", group=1, hold=True),
            "a": U("archers", "E", group=2, hold=True),
            "R": U("tahuanui", "E", group=3),
        },
        "camera": (10, 4),
        "intro": [
            ("kahu", "Matahi's war canoes, Commander, hauled up above the tide. While they float, no fishing village on these islands sleeps."),
            ("advisor", "Reach the hulls with torches before the crews come down from the gardens, Varius. Fourteen turns of the glass, no more."),
        ],
        "events": [
            {
                "when": ("reach", "1"),
                "say": [("officer", "The canoes are burning, Commander. Every one of them.")],
                "end": "victory",
            },
            {
                "when": ("round", 4),
                "cam": (0, 9),
                "spawn": [
                    ("toa", (0, 9), "E"),
                    ("toa", (0, 10), "E"),
                    ("toa", (21, 9), "E"),
                    ("toa", (21, 10), "E"),
                ],
                "say": [("officer_alarm", "The crews are back from the gardens, Commander. Both ends of the beach!")],
            },
        ],
        "victory": [("kahu", "They will build more. But it takes a year to build a war canoe, Commander, and a year is a long peace here.")],
        "defeat": [("officer_hurt", "We never reached the hulls, Commander. The fleet will sail.")],
        "reward": {"units": {"footmen": 1}, "spoils": {"Weapons": 1, "Armor": 1, "Whalebone": 2}},
    }
)

# ---------------------------------------------------------------- Raid 2. The Taniwha's Pool (a hunt in a lagoon)
LEVELS.append(
    {
        "id": 5948,
        "group": "siege",
        "name": "The Taniwha's Pool",
        "objective": "Hunt the guardians of the lagoon. Eliminate all enemies.",
        "turn_limit": 24,
        "budget": 2500,
        "sides": {"P": ARMY, "E": "Guardians of the Deep"},
        "terrain": """
ffffffffffffffffffffff
ff....--------....ffff
f...------------....ff
f..----~~~--~~~----..f
...----~~~--~~~----...
...----------------...
....--k--------k--....
f....--~~~--~~~--....f
f....--~~~--~~~--....f
......----------......
..r....-k----k-....r..
......................
.f..................f.
......................
......................
......................
......................
ff..................ff
""",
        "units": """
......................
......................
......................
........W.............
.............W........
.....t..........t.....
......................
........W.............
......................
.........tt...........
......................
......................
......................
.....DDDDDDDDDDDD.....
.....DDDDDDDDDDDD.....
.....DDDDDDDDDDDD.....
......................
......................
""",
        "legend": {
            "W": U("taniwha", "E", group=1),
            "t": U("toa", "E", group=2),
        },
        "camera": (10, 5),
        "intro": [
            ("kahu", "The guardians' pool, Commander. With Matahi gone there is nobody to speak to them, and they have started taking fishermen."),
            ("advisor", "Three of them in the deep, and their keepers on the sandbars. Make them come to us on dry ground, Varius. In the water they are worth two."),
        ],
        "events": [
            {
                "when": ("round", 4),
                "cam": (13, 8),
                "spawn": [("taniwha", (13, 8), "E"), ("toa", (2, 4), "E"), ("toa", (19, 4), "E")],
                "say": [("officer_alarm", "Another one, Commander! It was under us the whole time!")],
            },
        ],
        "victory": [("kahu", "The lagoon is quiet. I will have a stone set here, Commander, so the next keeper knows what woke them.")],
        "defeat": [("officer_hurt", "They have dragged half the line under, Commander. We are pulling back.")],
        "reward": {"units": {"raiders": 1}, "spoils": {"Beasts": 2, "Lore": 1, "Whalebone": 2}},
    }
)

KINGDOM = {
    "id": "moananui",
    "short": "Moananui",
    "name": "The Isles of Moananui",
    "order": 19,
    "theme": "green",
    "unlock_after": ["Abbisin"],  # with the bonus campaigns, beside Tilicia; nothing waits on it
    "heraldry": {"E": ("argent", "cyan", 20, 3)},
    "brief": [
        (
            "emperor",
            "Commander Varius, the grain ships that round the western cape are not coming home. Their crews are being taken off the islands the charts call Moananui, where war canoes come out of the lagoons at dusk.",
        ),
        (
            "thaddius",
            "The islanders are led by an elder named Matahi, Commander, a keeper of their spirits. The sailors who got away speak of men riding hawks, and of a serpent in the water that answers when he calls.",
        ),
        (
            "emperor",
            "A navigator of theirs has offered to pilot my fleet through the reefs. He asks only that the villages be left standing. Grant him that, and bring me an end to those canoes.",
        ),
    ],
    "levels": LEVELS,
}
