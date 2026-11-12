"""The Amber Reach — three story battles and two raids in the lost valley beyond the western mountains (ours; see
build_bonus.py). The land of the Saurian Exiles: tar flats hunted by Raptor packs, a river line held by Ankylosaurs
with Pterosaurs overhead, and the hollow of the Theropod Tyrant, which no palisade keeps out. Its ground is its own:
Tar Pits (t) and Giant Fern Canopy (e). It opens with the bonus campaigns (beside Tilicia) and nothing waits on it."""
from build_bonus import U

LEVELS = []
ARMY = "Carrone Army"
EXILES = "The Saurian Exiles"

# ---------------------------------------------------------------- 1. The Tar Flats (Raptor packs among the tar)
LEVELS.append(
    {
        "id": 5984,
        "group": "story",
        "name": "The Tar Flats",
        "objective": "Cross the tar flats into the Reach. Eliminate all enemies.",
        "turn_limit": 30,
        "budget": 2750,
        "sides": {"P": ARMY, "E": EXILES},
        "terrain": """
^^^^^^^......^^^^^^^
^^^..ee......ee..^^^
^^..eee......eee..^^
^....e...tt...e....^
^.......tttt.......^
^..f.....tt.....f..^
^..ff..........ff..^
^.....tt....tt.....^
^....ttt....ttt....^
^.....t......t.....^
^^................^^
^^..ee........ee..^^
^...ee...tt...ee...^
^........tt........^
^..................^
^..r............r..^
^..................^
^^................^^
^^^..............^^^
^^^^^^^......^^^^^^^
""",
        "units": """
....................
....................
.........zz.........
......a..K...a......
....................
.....R........R.....
.........RR.........
...R............R...
....................
.......R....R.......
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
            "R": U("raptor", "E", group=1),
            "K": U("ankylosaur", "E", group=2, hold=True),
            "a": U("archers", "E", group=2, hold=True),
            "z": U("shamans", "E", group=2, hold=True),
        },
        "camera": (9, 6),
        "intro": [
            ("orin", "The tar flats, Commander. Keep the horses out of the black: it will have them to the belly, and a man who steps in it stands there all the next turn."),
            ("officer", "Lizards, sir. On two legs. With knives. They are running straight across the tar as if it were turf."),
            ("advisor", "They hunt in packs, Varius. One of them is a nuisance. Two of them with a man between them will open him like a letter, mail or no mail. Do not let them get round the ends of the line."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (4, 12),
                "spawn": [
                    ("raptor", (4, 11), "E"),
                    ("raptor", (5, 12), "E"),
                    ("raptor", (15, 11), "E"),
                    ("raptor", (14, 12), "E"),
                ],
                "say": [("officer_alarm", "They were in the ferns, Commander! They are behind us!")],
            },
            {
                "when": ("round", 6),
                "cam": (9, 0),
                "spawn": [
                    ("raptor", (8, 0), "E"),
                    ("raptor", (11, 0), "E"),
                    ("pterosaur", (9, 1), "E"),
                ],
                "say": [("enemy", "The old blood remembers this ground, warm-skin. Yours will only stain it.")],
            },
        ],
        "brief": [
            ("orin", "Orin, Commander. I trap in the western mountains, and last spring I followed a pass that is on no map. It goes down into a valley that the world forgot to finish killing."),
            ("advisor", "The trapper says the first of it is a plain of tar with things running on it, Varius. Tar and fast enemies. Bring pikes."),
        ],
        "victory": [
            ("officer", "The flats are ours, Commander. We lost two horses to the tar and I am not sure they are dead yet."),
            ("orin", "One of the runners keeps circling the camp, Commander. It has been watching your scouts work. I believe it thinks it has found a better pack."),
        ],
        "defeat": [("officer_hurt", "They got round us, Commander. The line is cut to pieces.")],
        "reward": {"units": {"raptor": 1}, "spoils": {"Beasts": 1, "Weapons": 1, "Amber": 2}},
    }
)

# ---------------------------------------------------------------- 2. The Thunder Ford (Ankylosaurs at a ford, Pterosaurs above)
LEVELS.append(
    {
        "id": 5985,
        "group": "story",
        "name": "The Thunder Ford",
        "objective": "Force the river and break the armoured herd. Eliminate all enemies.",
        "turn_limit": 32,
        "budget": 3750,
        "sides": {"P": ARMY, "E": EXILES},
        "terrain": """
^^^^.......ee.......^^^^
^^^...ee........ee...^^^
^^....ee........ee....^^
^......................^
^..r......,,,,......r..^
^......................^
^....tt..........tt....^
~~~~~--~~~~--~~~~--~~~~~
~~~~~--~~~~--~~~~--~~~~~
~~~~~--~~~~--~~~~--~~~~~
........................
..f....x........x....f..
.ff..................ff.
........................
....r....tt.tt.....r....
........................
..ee................ee..
..ee................ee..
........................
.f....................f.
........................
........................
""",
        "units": """
........................
........................
........................
....a......K.......a....
.........p....p.........
........................
....K......KK......K....
........................
........................
........................
....R....R....R....R....
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
            "K": U("ankylosaur", "E", group=1, hold=True),
            "p": U("pterosaur", "E", group=2),
            "a": U("archers", "E", group=3, hold=True),
            "R": U("raptor", "E", group=4, hold=True),
        },
        "camera": (11, 7),
        "intro": [
            ("orin", "The river, Commander, and three fords. And at each ford one of those."),
            ("officer", "A hill with a tail, sir. Our front rank hit the first one and half of them are bleeding from their own blows."),
            ("advisor", "That shell gives back a third of what you put into it, Varius. Shoot it, or burn it, but do not send the swordsmen to hammer on it. And watch the sky: the fliers pick things up off the field, and drop them."),
        ],
        "events": [
            {
                "when": ("round", 4),
                "cam": (2, 13),
                "spawn": [
                    ("raptor", (1, 13), "E"),
                    ("raptor", (2, 14), "E"),
                    ("raptor", (22, 13), "E"),
                    ("raptor", (21, 14), "E"),
                ],
                "say": [("officer_alarm", "Runners on our bank, Commander, both flanks! They must have swum it upstream!")],
            },
            {
                "when": ("round", 7),
                "cam": (11, 1),
                "spawn": [
                    ("ankylosaur", (10, 2), "E"),
                    ("ankylosaur", (13, 2), "E"),
                    ("pterosaur", (8, 1), "E"),
                    ("pterosaur", (15, 1), "E"),
                ],
                "say": [("rashkar", "You are in the old country now, soft things. Here the ground itself is against you.")],
            },
        ],
        "brief": [
            ("orin", "Beyond the tar is the river, Commander. The herds water there. So do the ones who drive them."),
            ("advisor", "Somebody commands these beasts, Varius. Beasts do not hold three fords at once and keep a reserve in the air."),
        ],
        "victory": [
            ("officer", "We are across, Commander. The herd has broken, what is left of it."),
            ("orin", "A cow and a flier stayed on the bank, Commander. The cow is eating our fodder and the rider on the flier wants to know what you pay. I told her: better than the Exile-King."),
        ],
        "defeat": [("officer_hurt", "We cannot force the fords, Commander. The river is theirs.")],
        "reward": {"units": {"ankylosaur": 1, "pterosaur": 1}, "spoils": {"Beasts": 1, "Armor": 1, "Amber": 2}},
    }
)

# ---------------------------------------------------------------- 3. The Tyrant's Hollow (the Theropod Tyrant)
LEVELS.append(
    {
        "id": 5986,
        "group": "story",
        "name": "The Tyrant's Hollow",
        "objective": "Bring down the Theropod Tyrant.",
        "turn_limit": 34,
        "budget": 4000,
        "sides": {"P": ARMY, "E": EXILES},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^.....eeee.....^^^^^^
^^^^......eeeeee......^^^^
^^^....tt........tt....^^^
^^.....tt........tt.....^^
^^......................^^
^...f....r......r....f...^
^..ff................ff..^
^........................^
^^......ee......ee......^^
^^^.....ee......ee.....^^^
^^^^..................^^^^
^^^^PPPPPPPPppPPPPPPPP^^^^
^^^^..................^^^^
^^^.....x........x.....^^^
^^......................^^
^...f................f...^
^..ff................ff..^
^........................^
^........................^
^^......................^^
^^^....................^^^
^^^^^^^^..........^^^^^^^^
""",
        "units": """
..........................
..........................
............X.............
...........K.K............
..........p....p..........
........K...K....K........
..........................
....R.................R...
......R............R......
.........R......R.........
............pp............
.........R......R.........
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
..........................
""",
        "legend": {
            "X": U("tyrant", "E", group=1, hold=True, name="tyrant"),
            "K": U("ankylosaur", "E", group=2, hold=True),
            "p": U("pterosaur", "E", group=3),
            "R": U("raptor", "E", group=4),
        },
        "camera": (12, 3),
        "intro": [
            ("rashkar", "We were kings of everything once. Then the ice came, and the small warm things, and we were put away in this valley like a bad dream."),
            ("rashkar", "The dream is awake. Look up the hollow, soft things, and see what your forefathers ran from."),
            ("orin", "The fence was ours, Commander: my people built it to keep that out. It will not. Nothing it bites stays standing: tree, gate or wall."),
            ("advisor", "Then do not count on the fence, Varius. Make it come to you through its own pack, and put every pike and bolt we have into it. When the Tyrant falls, the Exile-King has nothing left to be king of."),
        ],
        "events": [
            {
                "when": ("kill", "tyrant"),
                "say": [
                    ("rashkar_hurt", "The last... of the great ones..."),
                    ("orin", "It is down, Commander. I can feel the ground again. I had forgotten it did not always shake."),
                ],
                "end": "victory",
            },
            {
                "when": ("round", 5),
                "cam": (2, 17),
                "spawn": [
                    ("raptor", (1, 17), "E"),
                    ("raptor", (2, 18), "E"),
                    ("raptor", (24, 17), "E"),
                    ("raptor", (23, 18), "E"),
                ],
                "say": [("officer_alarm", "The pack is over the ridge behind us, Commander!")],
            },
            {
                "when": ("round", 8),
                "cam": (12, 2),
                "spawn": [
                    ("ankylosaur", (9, 3), "E"),
                    ("ankylosaur", (16, 3), "E"),
                    ("pterosaur", (12, 1), "E"),
                ],
                "say": [("rashkar", "Drive them into the tar! Let the valley keep their bones with ours!")],
            },
        ],
        "brief": [
            ("orin", "The hollow at the head of the valley, Commander. My grandfather's people fenced it across and never went back to see why."),
            ("advisor", "The beast-king has let it out, Varius. One animal, they say. I have read the scouts' report three times and I still do not believe the footprints."),
        ],
        "victory": [
            ("officer", "The Tyrant is dead, Commander. It took four volleys after it should have fallen."),
            ("orin", "There was a clutch in the hollow, Commander. One egg, and it has hatched, and the first thing it saw was your banner. I do not know what you do with a thing like that. I know I should not like to be your enemy in ten years."),
            ("advisor", "The Reach is quiet, Varius. Let us fence the pass properly this time, and leave a guard who knows why."),
        ],
        "defeat": [("officer_hurt", "It walked through the fence as if it were grass, Commander. We cannot stop it.")],
        "reward": {"units": {"tyrant": 1}, "spoils": {"Beasts": 2, "Lore": 1, "Amber": 2}},
    }
)

# ---------------------------------------------------------------- Raid 1. The Nesting Cliffs (reach the Pterosaur nests)
LEVELS.append(
    {
        "id": 5987,
        "group": "siege",
        "name": "The Nesting Cliffs",
        "objective": "Reach the nests on the cliff top.",
        "turn_limit": 20,
        "budget": 2400,
        "sides": {"P": ARMY, "E": "Cliff Flight"},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^
^^^^^..oooo..^^^^^^^
^^^^..........^^^^^^
^^^....r..r....^^^^^
^^..............^^^^
^^..ee......ee..^^^^
^...ee......ee...^^^
^.......tt.......^^^
^..r....tt....r..^^^
^................^^^
^^..............^^^^
^^..f........f..^^^^
^...ff......ff...^^^
^................^^^
^................^^^
^^..............^^^^
^^^............^^^^^
^^^^^........^^^^^^^
""",
        "units": """
....................
.......1111.........
........K...........
......p....p........
....................
.........p..........
....R........R......
....................
.....R......R.......
.......R..R.........
....................
....................
...DDDDDDDDDDDD.....
...DDDDDDDDDDDD.....
...DDDDDDDDDDDD.....
....................
....................
....................
""",
        "legend": {
            "p": U("pterosaur", "E", group=1),
            "K": U("ankylosaur", "E", group=1, hold=True),
            "R": U("raptor", "E", group=2, hold=True),
        },
        "camera": (8, 3),
        "intro": [
            ("orin", "The nesting cliffs, Commander. Every flier in the valley is hatched on that ledge."),
            ("advisor", "We do not need to kill them all, Varius, only to stand among the nests. The fliers will not fight over their own eggs. But the tar is in the way, and so are the runners."),
        ],
        "events": [
            {
                "when": ("reach", "1"),
                "say": [("officer", "We are on the ledge, Commander. The fliers are wheeling off. They will not come down on us here.")],
                "end": "victory",
            },
            {
                "when": ("round", 4),
                "cam": (8, 10),
                "spawn": [("raptor", (2, 10), "E"), ("raptor", (14, 10), "E"), ("pterosaur", (8, 2), "E")],
                "say": [("officer_alarm", "Runners on both sides of the gully, Commander!")],
            },
        ],
        "victory": [("orin", "A dozen eggs, Commander, and warm. Raise one by hand and it will carry a rider. Ask the girl on the river bank.")],
        "defeat": [("officer_hurt", "We cannot reach the ledge, Commander. They have the height of us.")],
        "reward": {"units": {"raiders": 1}, "spoils": {"Beasts": 2, "Spirit": 1, "Amber": 2}},
    }
)

# ---------------------------------------------------------------- Raid 2. The Amber Mine (a guarded dig)
LEVELS.append(
    {
        "id": 5988,
        "group": "siege",
        "name": "The Amber Mine",
        "objective": "Take the amber diggings. Eliminate all enemies.",
        "turn_limit": 24,
        "budget": 2250,
        "sides": {"P": ARMY, "E": "Mine Guard"},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^^^
^..rr....r....r..rr..^
^....................^
^r..^^^...oo...^^^..r^
^.....^........^.....^
^..r......o.......r..^
^.........,,.........^
^^^^....r....r....^^^^
^..r................r^
^....tt........tt....^
^.....t....r....t....^
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
..........K...........
......................
....R...........R.....
..........K...........
......K.......K.......
......................
.....R..........R.....
.........R..R.........
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
            "K": U("ankylosaur", "E", group=1, hold=True),
            "R": U("raptor", "E", group=2),
        },
        "camera": (10, 5),
        "intro": [
            ("orin", "The amber diggings, Commander. The Exile-King feeds his great beasts something he gets out of that rock. They are bigger every season."),
            ("advisor", "Three of the armoured ones on the spoil heaps and a pack in the cut, Varius. The archers can earn their bread today."),
        ],
        "events": [
            {
                "when": ("round", 4),
                "cam": (10, 1),
                "spawn": [("ankylosaur", (10, 1), "E"), ("raptor", (8, 2), "E"), ("raptor", (12, 2), "E")],
                "say": [("officer_alarm", "Another one coming out of the adit, Commander, and it has brought its herders!")],
            },
        ],
        "victory": [("orin", "The diggings are yours, Commander. Whatever is in that amber, it is better in your wagons than in his feed troughs.")],
        "defeat": [("officer_hurt", "The herd has trampled the line, Commander. We are falling back down the cut.")],
        "reward": {"units": {"pikemen": 1}, "spoils": {"Lore": 1, "Armor": 1, "Amber": 2}},
    }
)

KINGDOM = {
    "id": "amber-reach",
    "short": "Amber Reach",
    "name": "The Amber Reach",
    "order": 23,
    "theme": "green",
    "unlock_after": ["Abbisin"],  # with the bonus campaigns, beside Tilicia; nothing waits on it
    "heraldry": {"E": ("or", "vert", 9, 6)},
    "brief": [
        (
            "emperor",
            "Commander Varius, the garrison at the western passes has sent me a tooth. It is as long as my forearm. They want to know what they are supposed to do about the rest of the animal.",
        ),
        (
            "thaddius",
            "There is a valley beyond the western mountains that the old ice never reached, Commander, and what lived everywhere before the ice lives there still. The mountain people call them the Exiles. Something has taught them to follow a banner.",
        ),
        (
            "emperor",
            "I do not mean to be the Emperor who lost the west to a lizard. A trapper named Orin found the pass and will show you down it. Take pikes, Commander. A great many pikes.",
        ),
    ],
    "levels": LEVELS,
}
