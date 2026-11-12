"""The Drowned Coast of Thalassar — three story battles and two raids on the tidal flats south of Mare Nostra (ours;
see build_bonus.py). The land of the Trench Brood: a causeway held by Carapace Scuttlers, shoals where Siren Channelers
sing men into the muck under Brine Hurlers' coral, and the mouth of the trench itself, where the Tide-Mother keeps her
Behemoths. Its ground is its own: Abyssal Muck (M), Thermal Chimneys (C) and Razor Coral (k). It opens with the bonus
campaigns (beside Tilicia) and nothing waits on it."""
from build_bonus import U

LEVELS = []
ARMY = "Carrone Army"
BROOD = "The Trench Brood"

# ---------------------------------------------------------------- 1. The Drowned Causeway (Scuttlers on a causeway)
LEVELS.append(
    {
        "id": 5964,
        "group": "story",
        "name": "The Drowned Causeway",
        "objective": "Force the causeway into Thalassar. Eliminate all enemies.",
        "turn_limit": 30,
        "budget": 3000,
        "sides": {"P": ARMY, "E": BROOD},
        "terrain": """
~~~~~~~..==..~~~~~~~
~~~~~-...==...-~~~~~
~~~--....==....--~~~
~~--..h..==..h..--~~
~--......==......--~
~-..M....==....M..-~
~-.......==.......-~
~--..k...==...k..--~
~~--kk---==---kk--~~
~~~-----M==M-----~~~
~~~--k---==---k--~~~
~~--.....==.....--~~
~-...M...==...M...-~
~-.......==.......-~
~-..r....==....r..-~
~--......==......--~
~~-......==......-~~
~~--.....==.....--~~
~~~--....==....--~~~
~~~~~-...==...-~~~~~
""",
        "units": """
....................
....................
.........z..........
......a......a......
........t..t........
.....t........t.....
.......S....S.......
....................
.........SS.........
....................
........S..S........
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
            "S": U("scuttler", "E", group=1, hold=True),
            "t": U("footmen", "E", group=2),
            "a": U("archers", "E", group=3, hold=True),
            "z": U("shamans", "E", group=3, hold=True),
        },
        "camera": (9, 8),
        "intro": [
            ("officer", "The causeway, Commander. It is the only dry road into Thalassar, and it is not very dry."),
            ("brannoch", "Those are not rocks on it. Scuttlers. I have seen a ballista bolt skip off one."),
            ("advisor", "A shell has a front and it has a belly, Varius. Get a man on each side of one and the shell is no use to it. And mind their claws: what they catch does not walk away next turn."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (2, 13),
                "spawn": [
                    ("scuttler", (2, 13), "E"),
                    ("scuttler", (17, 13), "E"),
                ],
                "say": [("officer_alarm", "They are coming up out of the tide on both sides of us, Commander!")],
            },
            {
                "when": ("round", 6),
                "cam": (9, 0),
                "spawn": [
                    ("scuttler", (9, 1), "E"),
                    ("scuttler", (10, 1), "E"),
                    ("footmen", (9, 0), "E"),
                    ("footmen", (10, 0), "E"),
                ],
                "say": [("enemy", "The tide gives, landsman, and the tide takes back.")],
            },
        ],
        "brief": [
            ("brannoch", "Brannoch, Commander, pilot of the Thalassar shoals for thirty years. I know every bar and channel of this coast, and none of them is where I left it."),
            ("advisor", "The pilot says the sea-folk hold the causeway with something in a shell, Varius. We go across it, or we do not go."),
        ],
        "victory": [
            ("officer", "The causeway is ours, Commander. The men are prising shells open to see what was in them."),
            ("brannoch", "One of the things has not gone back into the water. It follows the camp cook about. I would feed it, Commander, and see whose side it thinks it is on."),
        ],
        "defeat": [("officer_hurt", "We cannot get past them, Commander. The causeway is theirs.")],
        "reward": {"units": {"scuttler": 1}, "spoils": {"Armor": 1, "Beasts": 1, "Pearl": 2}},
    }
)

# ---------------------------------------------------------------- 2. The Singing Shoals (Sirens, muck and Brine Hurlers)
LEVELS.append(
    {
        "id": 5965,
        "group": "story",
        "name": "The Singing Shoals",
        "objective": "Silence the Sirens and break the coral battery. Eliminate all enemies.",
        "turn_limit": 32,
        "budget": 4350,
        "sides": {"P": ARMY, "E": BROOD},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~
~~~~--..........--~~~~
~~~-...o......o...-~~~
~~-................-~~
~-...MM........MM...-~
~-..MMM...rr...MMM..-~
~-...M..........M...-~
~--......o..o......--~
~~--..kk......kk..--~~
~~~----MM....MM----~~~
~~--...M......M...--~~
~-.....M......M.....-~
~-..................-~
~-...r..........r...-~
~-..................-~
~--................--~
~~-................-~~
~~--..............--~~
~~~--............--~~~
~~~~~-..........-~~~~~
""",
        "units": """
......................
......................
.......H......H.......
..........HH..........
......................
....................N.
.N........a.a.........
.........N..N.........
......................
.......S......S.......
.........s..s.........
.....S..........S.....
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
            "H": U("brinehurler", "E", group=1, hold=True),
            "N": U("siren", "E", group=2, hold=True),
            "a": U("archers", "E", group=1, hold=True),
            "S": U("scuttler", "E", group=3, hold=True),
            "s": U("scuttler", "E", group=4),
        },
        "camera": (10, 6),
        "intro": [
            ("brannoch", "Stop your ears if you can, Commander. That sound is the shoals."),
            ("officer", "Women on the rocks, sir, with staves. And behind them something is loading shells with... reef?"),
            ("advisor", "The singers do no harm themselves, Varius. They pull a man out of his rank and into that purple muck, where every stone the hurlers throw finds him. And where a shell lands, the sea stays. Do not stand where they have been shooting."),
        ],
        "events": [
            {
                "when": ("round", 4),
                "cam": (1, 12),
                "spawn": [
                    ("scuttler", (1, 12), "E"),
                    ("scuttler", (20, 12), "E"),
                    ("siren", (1, 14), "E"),
                    ("siren", (20, 14), "E"),
                ],
                "say": [("officer_alarm", "More of them on the bars behind us, Commander. They are singing to the rear rank!")],
            },
            {
                "when": ("round", 7),
                "cam": (10, 1),
                "spawn": [
                    ("brinehurler", (9, 1), "E"),
                    ("brinehurler", (12, 1), "E"),
                    ("scuttler", (10, 2), "E"),
                    ("scuttler", (11, 2), "E"),
                ],
                "say": [("enemy", "Every tide we raise the sea a little higher on your coast. One day you will wake and it will be ours.")],
            },
        ],
        "brief": [
            ("brannoch", "Past the causeway lie the shoals, Commander. Ships that hear singing there are found a week later, hull up, and nobody aboard."),
            ("advisor", "A battery on the far bar and singers on the near ones, Varius. Kill the singers first, or the battery will do its work on whoever they choose."),
        ],
        "victory": [
            ("officer", "The shoals are quiet, Commander. We have one of the coral throwers whole, and its crew."),
            ("brannoch", "And one of the singers has put down her staff. She says the Tide-Mother sings for all of them, and she would like to hear her own voice for once."),
        ],
        "defeat": [("officer_hurt", "They pulled the line apart, Commander. We are falling back to the causeway.")],
        "reward": {"units": {"siren": 1, "brinehurler": 1}, "spoils": {"Spirit": 1, "Lore": 1, "Pearl": 2}},
    }
)

# ---------------------------------------------------------------- 3. The Mouth of the Trench (the Tide-Mother and her Behemoths)
LEVELS.append(
    {
        "id": 5966,
        "group": "story",
        "name": "The Mouth of the Trench",
        "objective": "Defeat the Tide-Mother at the mouth of the trench.",
        "turn_limit": 34,
        "budget": 4000,
        "sides": {"P": ARMY, "E": BROOD},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~.MMMM.~~~~~~~~~
~~~~~~~~~.MMMM.~~~~~~~~~
~~~~~~~~C......C~~~~~~~~
~~~~~~~~~~MMMM~~~~~~~~~~
~~~~~~~~~~MMMM~~~~~~~~~~
~~~~~~~~~~MMMM~~~~~~~~~~
~~~~~~~--.MMMM.--~~~~~~~
~~~~~---..MMMM..---~~~~~
~~~--....C....C....--~~~
~~-..................-~~
~-...o....rr..rr..o...-~
~--..MM..........MM..--~
~~--.MM...kkkk...MM.--~~
~-.......kkkk.........-~
~-...r............r...-~
~-....................-~
~-....................-~
~--..................--~
~~--................--~~
~~~~~-............-~~~~~
~~~~~~~--......--~~~~~~~
""",
        "units": """
........................
...........Q............
..........N..N..........
.........H....H.........
..........SBBS..........
........................
........................
........................
........................
.......S........S.......
....a.....SS......a.....
......N..........N......
.......S........S.......
........................
..........s..s..........
........................
......DDDDDDDDDDDD......
......DDDDDDDDDDDD......
......DDDDDDDDDDDD......
........................
........................
........................
""",
        "legend": {
            "Q": U("siren", "E", group=9, hold=True, name="nacre"),  # (a group of her own: she keeps her islet)
            "N": U("siren", "E", group=1, hold=True),
            "H": U("brinehurler", "E", group=1, hold=True),
            "B": U("behemoth", "E", group=2, hold=True),
            "S": U("scuttler", "E", group=3, hold=True),
            "s": U("scuttler", "E", group=4),
            "a": U("archers", "E", group=3, hold=True),
        },
        "camera": (11, 3),
        "intro": [
            ("nacre", "You have walked a long way over what used to be sea-bed, dry-skin. It will be sea-bed again."),
            ("nacre", "My children are hungry and my singers are in voice. Come down into the mouth. It is warm by the chimneys."),
            ("brannoch", "She sits on the islet, Commander, and the only way to it is that neck of muck. Those in the neck are the sharks that walk. Nothing shifts one, and one bite takes a man and the man either side of him."),
            ("advisor", "The chimneys are good cover and they will cook whoever uses it, Varius. She is the one that matters. When the Tide-Mother stops singing, the rest have no song to follow."),
        ],
        "events": [
            {
                "when": ("kill", "nacre"),
                "say": [
                    ("nacre_hurt", "The tide... goes out..."),
                    ("brannoch", "Listen, Commander. No singing. I have not heard this coast silent since I was a boy."),
                ],
                "end": "victory",
            },
            {
                "when": ("round", 5),
                "cam": (2, 13),
                "spawn": [
                    ("scuttler", (2, 14), "E"),
                    ("scuttler", (21, 15), "E"),
                    ("siren", (2, 15), "E"),
                    ("siren", (21, 16), "E"),
                ],
                "say": [("officer_alarm", "They are in the shallows on both flanks, Commander!")],
            },
            {
                "when": ("round", 8),
                "cam": (12, 9),
                "spawn": [
                    ("siren", (12, 9), "E"),
                    ("scuttler", (8, 9), "E"),
                    ("scuttler", (15, 9), "E"),
                ],
                "say": [("nacre", "Rise, children! There is meat on the flats!")],
            },
        ],
        "brief": [
            ("brannoch", "The mouth of the trench, Commander. The sea-bed falls away there into water no lead line has ever found the bottom of. That is where they come from."),
            ("advisor", "And where their mother sits, Varius. A singer like the others, with two walking sharks for a bodyguard and hot vents to hide behind."),
        ],
        "victory": [
            ("officer", "The Tide-Mother is dead, Commander. The rest have gone back down the trench, and the water has stopped rising."),
            ("brannoch", "Not all of them went. One of the great sharks is sitting on the bar with its back to the sea. I do not think it has anywhere to be, Commander, and I should not like to be the man who tells it to move."),
            ("advisor", "Thalassar will be a coast again, Varius, with a pilot who knows where its sand-bars are. The Emperor will want charts."),
        ],
        "defeat": [("officer_hurt", "The sea has come in over the flats, Commander. We are cut off from the trench.")],
        "reward": {"units": {"behemoth": 1}, "spoils": {"Lore": 1, "Beasts": 1, "Armor": 1, "Pearl": 2}},
    }
)

# ---------------------------------------------------------------- Raid 1. The Brine Works (a coral battery on a reef)
LEVELS.append(
    {
        "id": 5967,
        "group": "siege",
        "name": "The Brine Works",
        "objective": "Destroy the coral battery before it floods the anchorage. Eliminate all enemies.",
        "turn_limit": 22,
        "budget": 3000,
        "sides": {"P": ARMY, "E": "Reef Battery"},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~
~~~~--......--~~~~~~
~~~-..o....o..-~~~~~
~~-............-~~~~
~-..rr......rr..-~~~
~-..............-~~~
~--..kk....kk..--~~~
~~---kk-MM-kk---~~~~
~~~-----MM-----~~~~~
~~--....MM....--~~~~
~-..............-~~~
~-...r......r...-~~~
~-..............-~~~
~--............--~~~
~~-............-~~~~
~~--..........--~~~~
~~~--........--~~~~~
~~~~~-......-~~~~~~~
""",
        "units": """
....................
....................
......H..H.H........
.....H......H.......
....................
......a....a........
.......S..S.........
....................
....................
....................
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
            "H": U("brinehurler", "E", group=1, hold=True),
            "a": U("archers", "E", group=1, hold=True),
            "S": U("scuttler", "E", group=2, hold=True),
        },
        "camera": (8, 3),
        "intro": [
            ("brannoch", "The Brine Works, Commander. Five of their coral throwers on one reef, ranging on the fishing anchorage."),
            ("advisor", "Every shell floods another piece of the flats, Varius, and flooded ground is theirs. Close with the battery quickly, by a road they have not yet drowned."),
        ],
        "events": [
            {
                "when": ("round", 4),
                "cam": (2, 10),
                "spawn": [("scuttler", (2, 10), "E"), ("scuttler", (15, 10), "E"), ("siren", (2, 11), "E")],
                "say": [("officer_alarm", "Shells in the water behind us, Commander, and they are not the kind they throw!")],
            },
        ],
        "victory": [("brannoch", "The anchorage will dry out by the spring tides, Commander. The fishers have sent you a basket of something. I would not ask what.")],
        "defeat": [("officer_hurt", "The reef is under water, Commander, and so are we. Fall back!")],
        "reward": {"units": {"crossbowmen": 1}, "spoils": {"Weapons": 1, "Lore": 1, "Pearl": 2}},
    }
)

# ---------------------------------------------------------------- Raid 2. The Pearl Beds (reach the beds through the coral)
LEVELS.append(
    {
        "id": 5968,
        "group": "siege",
        "name": "The Pearl Beds",
        "objective": "Reach the pearl beds beyond the reef.",
        "turn_limit": 20,
        "budget": 2050,
        "sides": {"P": ARMY, "E": "Bed Wardens"},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~
~~~~~--....--~~~~~~~
~~~~-...FF...-~~~~~~
~~~-..........-~~~~~
~~-...o....o...-~~~~
~~-............-~~~~
~~kkkk..kk..kkkk~~~~
~~kkkkk.kk.kkkkk~~~~
~~-kkk..MM..kkk-~~~~
~~-.....MM.....-~~~~
~-..............-~~~
~-...r......r...-~~~
~-..............-~~~
~--............--~~~
~~-............-~~~~
~~--..........--~~~~
~~~--........--~~~~~
~~~~~-......-~~~~~~~
""",
        "units": """
....................
....................
........11..........
.......N..N.........
....................
.....S......S.......
........SS..........
.......S..S.........
....................
....................
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
            "N": U("siren", "E", group=1, hold=True),
            "S": U("scuttler", "E", group=2, hold=True),
        },
        "camera": (8, 3),
        "intro": [
            ("brannoch", "The pearl beds, Commander. Whatever they grow in those pools, they make their strongest out of it, and so could we."),
            ("advisor", "There is a reef of razor coral between us and the pools, Varius, with two narrow gaps in it. It cuts whoever wades it. Take the gaps, or take the cuts, but get a man to the pools."),
        ],
        "events": [
            {
                "when": ("reach", "1"),
                "say": [("officer", "We are at the pools, Commander. There are pearls in here the size of a fist.")],
                "end": "victory",
            },
            {
                "when": ("round", 4),
                "cam": (8, 10),
                "spawn": [("scuttler", (1, 11), "E"), ("scuttler", (16, 11), "E"), ("siren", (8, 4), "E")],
                "say": [("officer_alarm", "Wardens out of the channels on both sides, Commander!")],
            },
        ],
        "victory": [("brannoch", "A sack of them, Commander, and all our own. The Brood will have to grow its next giant out of something else.")],
        "defeat": [("officer_hurt", "We never reached the pools, Commander. The reef has us.")],
        "reward": {"units": {"swordsmen": 1}, "spoils": {"Spirit": 1, "Beasts": 1, "Pearl": 2}},
    }
)

KINGDOM = {
    "id": "thalassar",
    "short": "Thalassar",
    "name": "The Drowned Coast of Thalassar",
    "order": 21,
    "theme": "sand",
    "unlock_after": ["Abbisin"],  # with the bonus campaigns, beside Tilicia; nothing waits on it
    "heraldry": {"E": ("cyan", "sable", 41, 5)},
    "brief": [
        (
            "emperor",
            "Commander Varius, the south coast is shrinking. Three fishing towns have sent to say that the sea stands in their streets and does not go out again, and that things walk in it.",
        ),
        (
            "thaddius",
            "The old charts mark a trench off Thalassar, Commander, deeper than anything else in Mare Nostra. Something in it has learnt to carry the sea up the beach a shell at a time. Where their coral lands, the water stays.",
        ),
        (
            "emperor",
            "An empire that loses a mile of coast a year is not an empire for long. A pilot named Brannoch will meet you at the causeway. Go down to the water, and push it back.",
        ),
    ],
    "levels": LEVELS,
}
