"""The Highlands of Coatlan — three story battles and two raids above the jungles of Tezcal (ours; see
build_bonus.py). A second Aztec realm, the serpent order's highlands: a cloud forest held by Coatecpatl Warriors, a
lake causeway with Ahuizotl coming out of the water, and a star-temple where a Tzitzimitl must be destroyed behind a
Cuahchic captain's banner line. Tezcal's own orders serve here as rank and file. It opens with the bonus campaigns
(beside Tilicia) and nothing waits on it."""
from build_bonus import U

LEVELS = []
ARMY = "Carrone Army"
ORDER = "The Serpent Order"
TEMPLE = "The Star Temple"

# ---------------------------------------------------------------- 1. The Cloud Forest (Coatecpatl Warriors in the trees)
LEVELS.append(
    {
        "id": 5954,
        "group": "story",
        "name": "The Cloud Forest",
        "objective": "Force the forest road into the highlands. Eliminate all enemies.",
        "turn_limit": 30,
        "budget": 3500,
        "sides": {"P": ARMY, "E": ORDER},
        "terrain": """
ffffffff..==..ffffffff
fff..ff...==...ff..fff
ff....f...==...f....ff
f...,.....==.....,...f
ff.....x..==..x.....ff
fff.ff....==....ff.fff
ffffff....==....ffffff
fff..f....==....f..fff
ff....ff..==..ff....ff
f..,...f..==..f...,..f
ff....ff..==..ff....ff
ffff.fff..==..fff.ffff
fff...f...==...f...fff
ff........==........ff
f....,....==....,....f
ff........==........ff
f.........==.........f
f.........==.........f
f.........==.........f
ff........==........ff
fff.......==.......fff
ffffff....==....ffffff
""",
        "units": """
......................
......................
....e...........e.....
........e....e........
........C....C........
.........C..C.........
......................
......................
...c..............c...
....c............c....
......................
......................
....j............j....
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
            "e": U("eagle", "E", group=1, hold=True),
            "C": U("coatecpatl", "E", group=2, hold=True),
            "c": U("coatecpatl", "E", group=3),
            "j": U("jaguar", "E", group=4),
        },
        "camera": (10, 6),
        "intro": [
            ("cuali", "The cloud forest, Commander. Up here the trees never dry, and the serpent order has kept this road since before my grandfather's grandfather."),
            ("officer", "Men in snake-skins at the barricade, and more in the trees. Their blades are black glass, and wet."),
            ("cuali", "Wet with venom. A cut from a Coatecpatl goes on killing for three days, or for three turns of your glass. Do not trade scratches with them."),
            ("advisor", "Then we kill them quickly or not at all, Varius. Priests behind the line, and nobody fights wounded."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (1, 14),
                "spawn": [
                    ("coatecpatl", (1, 14), "E"),
                    ("jaguar", (2, 13), "E"),
                    ("coatecpatl", (20, 14), "E"),
                    ("jaguar", (19, 13), "E"),
                ],
                "say": [("officer_alarm", "They are in the trees behind us, Commander! Both sides of the road!")],
            },
            {
                "when": ("round", 6),
                "cam": (10, 0),
                "spawn": [
                    ("coatecpatl", (10, 0), "E"),
                    ("jaguar", (11, 0), "E"),
                    ("eagle", (8, 1), "E"),
                    ("eagle", (13, 1), "E"),
                ],
                "say": [("enemy", "The serpent does not let go, stranger! Close the road behind them!")],
            },
        ],
        "brief": [
            ("cuali", "I am Cuali, Commander, a captain of the eagle order of the jungle. My people serve the sun. Above us, in Coatlan, there is an older temple, and what it serves is not the sun."),
            ("advisor", "The Eagle Captain will guide us up, Varius. He says the road runs through a forest that belongs to men who dress as snakes."),
        ],
        "victory": [
            ("officer", "The road is open, Commander. The snake-skins have gone back up the mountain."),
            ("cuali", "My jaguars watched them fight, and two have asked the order's leave to take the serpent's skin. I have given it. A man should know his enemy's poison."),
        ],
        "defeat": [("officer_hurt", "We cannot hold the road, Commander. The forest is full of them.")],
        "reward": {"units": {"coatecpatl": 1}, "spoils": {"Weapons": 1, "Beasts": 1, "Obsidian": 2}},
    }
)

# ---------------------------------------------------------------- 2. The Lake Causeway (Ahuizotl out of the water)
LEVELS.append(
    {
        "id": 5955,
        "group": "story",
        "name": "The Lake Causeway",
        "objective": "Cross the causeway over the highland lake. Eliminate all enemies.",
        "turn_limit": 32,
        "budget": 2750,
        "sides": {"P": ARMY, "E": ORDER},
        "terrain": """
ffff.......==.......ffff
ff....h....==....h....ff
f..........==..........f
...,.......==.......,...
.......x...==...x.......
...........==...........
---~~~~~~~~bb~~~~~~~~---
---~~~~~~~~bb~~~~~~~~---
---~~~~~~~~bb~~~~~~~~---
---~~~~~~~~bb~~~~~~~~---
---~~~~~~~~bb~~~~~~~~---
---~~~~~~~~bb~~~~~~~~---
...........==...........
..f........==........f..
.ff........==........ff.
...........==...........
....r......==......r....
...........==...........
..,,.......==.......,,..
...........==...........
.f.........==.........f.
...........==...........
...........==...........
...........==...........
""",
        "units": """
........................
........................
......e..........e......
.........e....e.........
........C......C........
.j........CC..C.......j.
........................
........................
..........A.............
.............A..........
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
........................
""",
        "legend": {
            "e": U("eagle", "E", group=1, hold=True),
            "C": U("coatecpatl", "E", group=2, hold=True),
            "j": U("jaguar", "E", group=3),
            "A": U("ahuizotl", "E", group=4),
        },
        "camera": (11, 8),
        "intro": [
            ("cuali", "The lake of Coatlan, Commander. The temple is on the far shore, and the causeway is the only dry way to it."),
            ("officer", "There are fords at either end, but something keeps breaking the surface beside the stones."),
            ("cuali", "Ahuizotl. Water-dogs, with a hand where the tail should end. What one bites, it holds, and a man who is held cannot lift his sword."),
            ("advisor", "They will come over the side at whoever is in the middle of that causeway, Varius. Cross in a column that can fight to both flanks."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (11, 9),
                "spawn": [("ahuizotl", (10, 10), "E"), ("ahuizotl", (13, 7), "E")],
                "say": [("officer_alarm", "Out of the water, Commander! They are climbing the causeway on both sides!")],
            },
            {
                "when": ("round", 6),
                "cam": (11, 1),
                "spawn": [
                    ("ahuizotl", (3, 9), "E"),
                    ("ahuizotl", (20, 8), "E"),
                    ("coatecpatl", (11, 0), "E"),
                    ("coatecpatl", (12, 0), "E"),
                ],
                "say": [("enemy", "Feed the lake! Drive them off the stones!")],
            },
        ],
        "brief": [
            ("cuali", "Beyond the forest the land opens on a lake as wide as a day's march, Commander. The serpent order drowned its prisoners there for the things that live in it."),
            ("advisor", "So the lake is on their side as well, Varius. I am beginning to miss the jungle."),
        ],
        "victory": [
            ("officer", "We hold both ends of the causeway, Commander. The lake has gone still."),
            ("cuali", "One of the water-dogs has followed your leech-keepers back to camp and is eating out of their hands. I cannot explain it. Perhaps it only wanted feeding."),
        ],
        "defeat": [("officer_hurt", "They have pulled the column apart, Commander. We are back on the near shore.")],
        "reward": {"units": {"ahuizotl": 1}, "spoils": {"Beasts": 1, "Armor": 1, "Obsidian": 2}},
    }
)

# ---------------------------------------------------------------- 3. The Temple of Stars (the Tzitzimitl and the banner line)
LEVELS.append(
    {
        "id": 5956,
        "group": "story",
        "name": "The Temple of Stars",
        "objective": "Storm the star-temple by night and destroy Itzpapal.",
        "turn_limit": 34,
        "budget": 3650,
        "sides": {"P": ARMY, "E": TEMPLE},
        "terrain": """
ffffffffffffffffffffffffff
fff.TWWWWWWWWWWWWWWWWT.fff
ff..W________________W..ff
ff..W____o______o____W..ff
ff..W_______K________W..ff
ff..W____o______o____W..ff
ff..W________________W..ff
ff..W__h__________h__W..ff
ff..W________________W..ff
ff..TWWWWWWTGGTWWWWWWT..ff
fff........,==,........fff
ff.....x....==....x.....ff
f...........==...........f
ff..f.......==.......f..ff
ff.ff.......==.......ff.ff
f...........==...........f
f....r......==......r....f
............==............
..,,........==........,,..
............==............
.f..........==..........f.
............==............
............==............
............==............
ff..........==..........ff
ffff........==........ffff
""",
        "units": """
..........................
..........................
..........................
..........................
..........................
.............Z............
........e...z....e........
..........................
......e...HccH.....e......
..........................
.........c....c...........
..........................
..........................
....j...............j.....
...j.................j....
..........................
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
            "Z": U("tzitzimitl", "E", group=1, hold=True, name="itzpapal"),
            "z": U("tzitzimitl", "E", group=1, hold=True),
            "H": U("chieftain", "E", group=2, hold=True),
            "c": U("coatecpatl", "E", group=2, hold=True),
            "e": U("eagle", "E", group=3, hold=True),
            "j": U("jaguar", "E", group=4),
        },
        "camera": (12, 5),
        "intro": [
            ("itzpapal", "The little captain has brought the sun-killers to my door. Good. I have been hungry since the last eclipse."),
            ("itzpapal", "Come in, come in. Everything that burns in you, I will drink, and be the brighter for it."),
            ("cuali", "That is Itzpapal, Commander. A star that fell and was fed. Whatever its fire takes from your men, it keeps. Starve it: strike it hard and all at once."),
            ("advisor", "And mind the shorn ones under the banner, Varius. Men who stand beside a Cuahchic strike before they are struck."),
        ],
        "events": [
            {
                "when": ("kill", "itzpapal"),
                "say": [
                    ("itzpapal_hurt", "Dark... it is so dark down here..."),
                    ("cuali", "Shorn ones! Your star is out. There is nothing left on that altar to die for."),
                ],
                "end": "victory",
            },
            {
                "when": ("round", 5),
                "cam": (1, 15),
                "spawn": [
                    ("jaguar", (1, 15), "E"),
                    ("jaguar", (2, 15), "E"),
                    ("jaguar", (23, 15), "E"),
                    ("jaguar", (24, 15), "E"),
                ],
                "say": [("officer_alarm", "Jaguars out of the trees on both flanks, Commander!")],
            },
            {
                "when": ("round", 8),
                "cam": (12, 7),
                "spawn": [
                    ("chieftain", (12, 7), "E"),
                    ("coatecpatl", (10, 7), "E"),
                    ("coatecpatl", (15, 7), "E"),
                    ("tzitzimitl", (13, 3), "E"),
                ],
                "say": [("itzpapal", "Another star for the altar! Wake, little sister, and eat!")],
            },
        ],
        "brief": [
            ("cuali", "The Temple of Stars, Commander. It is only open at night, because the thing it houses cannot bear the sun. Every priest in the lowlands fears it, and pays it, and never speaks of it."),
            ("advisor", "A demon behind a wall and a captain who has sworn never to step back, Varius. We go in after dark, and we do not stop at the gate."),
        ],
        "victory": [
            ("officer", "The thing on the altar is gone, Commander. It went out like a lamp."),
            ("cuali", "The captain of the shorn ones lives, and he has cut his banner from its pole and laid it at your feet. He kept his oath. He never stepped back. Take him, Commander. There are few like him."),
            ("advisor", "The hill villages will send their tithe again, Varius, and this time nobody will be sending heads back with it."),
        ],
        "defeat": [("officer_hurt", "The gate held, Commander, and it is nearly dawn. We must fall back.")],
        "reward": {"units": {"chieftain": 1}, "spoils": {"Lore": 1, "Spirit": 1, "Armor": 1, "Obsidian": 2}},
    }
)

# ---------------------------------------------------------------- Raid 1. The Skull Rack (reach the court in time)
LEVELS.append(
    {
        "id": 5957,
        "group": "siege",
        "name": "The Skull Rack",
        "objective": "Reach the skull rack in the temple court within fourteen turns, or eliminate all enemies.",
        "turn_limit": 14,
        "budget": 3000,
        "sides": {"P": ARMY, "E": "Court Guard"},
        "terrain": """
ffffffffffffffffffffff
fff.TWWWWWWWWWWT.fffff
ff..W__________W..ffff
ff..W___o__o___W..ffff
ff..W__________W..ffff
ff..TWWWTGGTWWWT..ffff
fff......==......fffff
ff...x...==...x...ffff
f........==........fff
ff..f....==....f...fff
f...ff...==...ff....ff
f........==.........ff
..,......==......,...f
.........==..........f
.........==...........
.........==...........
f........==..........f
ff.......==.........ff
""",
        "units": """
......................
......................
.......e....e.........
.........11...........
........cHc...........
......................
........c..c..........
......e......e........
......................
......................
..j..............j....
......................
......................
....DDDDDDDDDDDD......
....DDDDDDDDDDDD......
....DDDDDDDDDDDD......
......................
......................
""",
        "legend": {
            "e": U("eagle", "E", group=1, hold=True),
            "c": U("coatecpatl", "E", group=2, hold=True),
            "H": U("chieftain", "E", group=2, hold=True),
            "j": U("jaguar", "E", group=3),
        },
        "camera": (9, 3),
        "intro": [
            ("cuali", "The serpent order's court, Commander. The rack in the middle holds the heads of every envoy the lowlands ever sent up here."),
            ("advisor", "Pull it down before the temple guard can muster, Varius, and the hill villages will know the order is finished. Fourteen turns."),
        ],
        "events": [
            {
                "when": ("reach", "1"),
                "say": [("officer", "The rack is down, Commander. The court is ours.")],
                "end": "victory",
            },
            {
                "when": ("round", 4),
                "cam": (18, 12),
                "spawn": [
                    ("jaguar", (18, 12), "E"),
                    ("jaguar", (19, 12), "E"),
                    ("coatecpatl", (18, 13), "E"),
                    ("coatecpatl", (19, 13), "E"),
                ],
                "say": [("officer_alarm", "The temple guard, Commander. Out of the east wood!")],
            },
        ],
        "victory": [("cuali", "My own father's brother was on that rack, Commander. I will see him buried now.")],
        "defeat": [("officer_hurt", "We did not reach the court, Commander. The guard is fully roused.")],
        "reward": {"units": {"pikemen": 1}, "spoils": {"Weapons": 1, "Lore": 1, "Obsidian": 2}},
    }
)

# ---------------------------------------------------------------- Raid 2. The Drowned Village (hold a fenced village)
LEVELS.append(
    {
        "id": 5958,
        "group": "siege",
        "name": "The Drowned Village",
        "objective": "Hold the fishing village for 8 turns against the lake.",
        "turn_limit": 12,
        "budget": 2400,
        "win_switch": False,
        "sides": {"P": ARMY, "E": "The Lake"},
        "terrain": """
~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~
----~~~~------~~~~----
......................
..PPPPPPPPppPPPPPPPP..
..P................P..
..P..h..........h..P..
..P................P..
..p................p..
..P................P..
..P..h..........h..P..
..P................P..
..PPPPPPPPppPPPPPPPP..
......................
f....................f
ff..,,..........,,..ff
fff................fff
ffffffffffffffffffffff
""",
        "units": """
......................
......................
.........A..A.........
.....a..........b.....
......................
......................
......................
.....DDDDDDDDDDDD.....
c....DDDDDDDDDDDD....d
.....DDDDDDDDDDDD.....
......................
......................
......................
......................
..........eg..........
......................
......................
......................
""",
        "legend": {"A": U("ahuizotl", "E", group=1)},
        "camera": (10, 8),
        "intro": [
            ("officer", "The fishers have let us inside their fence, Commander. They say the lake comes for the village every dark of the moon."),
            ("cuali", "The water-dogs. With the star-temple silent there is nobody to feed them, and they are coming ashore to feed themselves."),
            ("advisor", "Eight turns of the glass until first light, Varius. Keep the fence, and keep the men who are bitten out of the front rank."),
        ],
        "events": [
            {
                "when": ("round", 2),
                "cam": (5, 3),
                "spawn": [("ahuizotl", "a", "E"), ("ahuizotl", "b", "E"), ("coatecpatl", "c", "E")],
                "say": [("officer_alarm", "More of them out of the shallows, Commander!")],
            },
            {
                "when": ("round", 3),
                "cam": (21, 8),
                "spawn": [("coatecpatl", "d", "E"), ("ahuizotl", (9, 2), "E")],
            },
            {
                "when": ("round", 4),
                "cam": (10, 14),
                "spawn": [("coatecpatl", "e", "E"), ("coatecpatl", "g", "E"), ("ahuizotl", (12, 2), "E")],
                "say": [("officer", "Snake-skins at the south gate, Commander. They have come down to watch us drown.")],
            },
            {
                "when": ("round", 5),
                "cam": (0, 8),
                "spawn": [("ahuizotl", "a", "E"), ("ahuizotl", "c", "E"), ("coatecpatl", "d", "E")],
            },
            {
                "when": ("round", 6),
                "cam": (16, 3),
                "spawn": [("ahuizotl", "b", "E"), ("ahuizotl", (9, 2), "E"), ("coatecpatl", "e", "E")],
                "say": [("officer_alarm", "The whole lake is moving, Commander!")],
            },
            {
                "when": ("round", 7),
                "cam": (10, 2),
                "spawn": [("ahuizotl", (12, 2), "E"), ("ahuizotl", "a", "E"), ("coatecpatl", "g", "E")],
            },
            {
                "when": ("round", 9),
                "say": [("cuali", "First light, Commander. They will not come out of the water in the sun.")],
                "end": "victory",
            },
        ],
        "victory": [("officer", "Dawn, Commander. The fence held, and the fishers are already mending their nets.")],
        "defeat": [("officer_hurt", "They are inside the fence, Commander. The village is lost.")],
        "reward": {"units": {"footmen": 1}, "spoils": {"Beasts": 1, "Armor": 1, "Spirit": 1, "Obsidian": 2}},
    }
)

KINGDOM = {
    "id": "coatlan",
    "short": "Coatlan",
    "name": "The Highlands of Coatlan",
    "order": 20,
    "theme": "green",
    "unlock_after": ["Abbisin"],  # with the bonus campaigns, beside Tilicia; nothing waits on it
    "heraldry": {"E": ("or", "sable", 33, 5)},
    "brief": [
        (
            "emperor",
            "Commander Varius, the hill villages east of Tilicia have stopped sending their tithe, and the men I sent to ask why have not come back. Their heads have, on a rack, by way of a trader.",
        ),
        (
            "thaddius",
            "The highlands are called Coatlan, Commander, the place of serpents. An order of warriors rules there in the name of something they keep in a temple that is only opened at night. The lowland priests will not say its name.",
        ),
        (
            "emperor",
            "An Eagle Captain of the jungle orders has offered to guide an army up the mountain. He says his people have paid that temple for long enough. Go up with him, and put out whatever is burning there.",
        ),
    ],
    "levels": LEVELS,
}
