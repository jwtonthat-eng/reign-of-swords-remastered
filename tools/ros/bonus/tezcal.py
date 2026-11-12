"""The Jungles of Tezcal — three story battles and two raids on the jungle coast east of the Mirror Sea (ours; see
build_bonus.py). Woods are the ground here: Jaguar and Eagle Warriors cross them as open ground, everyone else
is slowed, and the battles are laid out so that the enemy comes through the trees."""
from build_bonus import U

LEVELS = []
ARMY = "Carrone Army"
TEMPLE = "Host of the Sun"

# ---------------------------------------------------------------- 1. The Green Road (an ambush on the jungle road)
LEVELS.append(
    {
        "id": 5994,
        "group": "story",
        "name": "The Green Road",
        "objective": "Break the ambush on the jungle road. Eliminate all enemies.",
        "turn_limit": 30,
        "budget": 3750,
        "sides": {"P": ARMY, "E": TEMPLE},
        "terrain": """
fffffffff==fffffffff
ffff,,..f==f..,,ffff
fff..h...==...h..fff
ff...,...==...,...ff
fff.....x==x.....fff
fffff....==....fffff
ffffff,..==..,ffffff
fff,fff..==..fff,fff
ff...ff..==..ff...ff
ff.,.fff.==.fff.,.ff
fff..fff.==.fff..fff
ffffffff.==.ffffffff
fff,ffff.==.ffff,fff
ff...fff.==.fff...ff
ff.,..ff.==.ff..,.ff
fff...f..==..f...fff
ffff.....==.....ffff
fff...,..==..,...fff
ff.......==.......ff
ff.......==.......ff
fff......==......fff
ffff.....==.....ffff
fffff....==....fffff
ffffffff.==.ffffffff
""",
        "units": """
....................
....................
....a.a..z...a.a....
....................
.......lw..wl.......
........w..w........
....................
....................
..jj............jj..
...j............j...
....................
....................
....................
..k.k..........k.k..
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
            "w": U("swordsmen", "E", group=2, hold=True),
            "j": U("jaguar", "E", group=3),
            "k": U("jaguar", "E", group=4),
        },
        "camera": (9, 5),
        "intro": [
            ("officer", "One road inland, Commander, and trees to either side so thick a man cannot see his own shield arm."),
            ("advisor", "Those are Skarl's runaway captains at the barricade. They did not build it alone, Varius."),
            ("officer_alarm", "Movement in the trees! Men in spotted hides, and they are running through that tangle as if it were a parade ground!"),
            ("advisor", "Jaguar warriors. Keep our line on the road and in the clearings. In the woods they are worth two of us."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (5, 21),
                "spawn": [
                    ("jaguar", (4, 22), "E"),
                    ("jaguar", (3, 21), "E"),
                    ("jaguar", (15, 22), "E"),
                    ("jaguar", (16, 21), "E"),
                ],
                "say": [("officer_alarm", "They are behind us, Commander! Out of the trees on both sides of the road!")],
            },
            {
                "when": ("round", 6),
                "cam": (9, 0),
                "spawn": [
                    ("jaguar", (9, 0), "E"),
                    ("jaguar", (10, 0), "E"),
                    ("archers", (9, 1), "E"),
                    ("archers", (10, 1), "E"),
                ],
                "say": [("enemy", "The Sun-Speaker pays in gold for every heart, Carrone! Yours will buy me a new ship.")],
            },
        ],
        "brief": [
            ("advisor", "The jungle coast of Tezcal, Varius. Skarl's captains ran here when their king fell, and somebody ashore has given them a roof."),
            ("officer", "There is one road up from the beach. We march in column and we keep the scouts close."),
        ],
        "victory": [
            ("officer", "The road is clear, Commander. The reavers are dead and the spotted men have gone back into the trees."),
            ("advisor", "They fought for a paymaster they called the Sun-Speaker. Reavers do not learn a word like that for nothing."),
            ("officer", "Some of their dead carried our own pikes, Commander, cut short for the forest. The men want to try it."),
        ],
        "defeat": [("officer_hurt", "We are cut to pieces on the road, Commander. Back to the boats.")],
        "reward": {"units": {"jaguar": 1}, "spoils": {"Beasts": 1, "Weapons": 1, "Obsidian": 2}},
    }
)

# ---------------------------------------------------------------- 2. The Serpent Ford (a river crossing under darts)
LEVELS.append(
    {
        "id": 5995,
        "group": "story",
        "name": "The Serpent Ford",
        "objective": "Force the river and clear the far bank. Eliminate all enemies.",
        "turn_limit": 32,
        "budget": 4500,
        "sides": {"P": ARMY, "E": TEMPLE},
        "terrain": """
ffffffffff.==.ffffffffff
fff..h..ff.==.ff..h..fff
ff..,....f.==.f....,..ff
ff.......ff==ff.......ff
fff.ff....,==,....ff.fff
ffffff.ff..==..ff.ffffff
fffffffff..==..fffffffff
ff,.ffff...==...ffff.,ff
f....,.....==.....,....f
~~~~~---~~~bb~~~---~~~~~
~~~~~---~~~bb~~~---~~~~~
~~~~~---~~~bb~~~---~~~~~
f....,.....==.....,....f
ff..ff.....==.....ff..ff
fff.fff....==....fff.fff
ff...f.....==.....f...ff
f.....,....==....,.....f
f..........==..........f
ff.........==.........ff
fff........==........fff
ffff.......==.......ffff
ffffff.....==.....ffffff
""",
        "units": """
........................
........................
....a.a...........a.a...
........S..z...S........
........................
......j..........j......
........................
.....ee...l..l...ee.....
..j.j......pp......j.j..
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
            "a": U("archers", "E", group=1, hold=True),
            "z": U("shamans", "E", group=1, hold=True),
            "e": U("eagle", "E", group=2, hold=True),
            "p": U("pikemen", "E", group=3, hold=True),
            "l": U("footmen", "E", group=3, hold=True),
            "j": U("jaguar", "E", group=4),
            "S": U("serpent", "E", group=5),
        },
        "camera": (11, 8),
        "intro": [
            ("officer", "The river, Commander. A plank bridge on the road and a ford on either hand, waist deep."),
            ("advisor", "Men in eagle feathers in the trees on the far bank. Dart-throwers. They will not need to see us to hit us."),
            ("officer_alarm", "Commander, above the water... By the Emperor, they have wings. Serpents with wings!"),
            ("advisor", "They throw a wind and are gone before a bow can answer, Varius. Do not chase them. Take the bank and they have nowhere to rest."),
        ],
        "events": [
            {
                "when": ("round", 4),
                "cam": (11, 0),
                "spawn": [
                    ("serpent", (11, 1), "E"),
                    ("jaguar", (11, 0), "E"),
                    ("jaguar", (12, 0), "E"),
                ],
                "say": [("officer_alarm", "More of them on the north road, Commander, and another of those serpents over the trees.")],
            },
            {
                "when": ("round", 7),
                "cam": (2, 14),
                "spawn": [
                    ("jaguar", (1, 14), "E"),
                    ("jaguar", (2, 13), "E"),
                    ("jaguar", (22, 14), "E"),
                    ("jaguar", (21, 13), "E"),
                ],
                "say": [("officer_alarm", "Jaguar men on our own bank, Commander! They swam the river above the fords!")],
            },
        ],
        "brief": [
            ("advisor", "The Sun-Speaker's city lies beyond the river, Varius. He has posted his eagle order at the only crossing for thirty miles."),
            ("officer", "Our prisoners say the eagles and the priest are no friends. They hold the ford because he holds their families."),
        ],
        "victory": [
            ("officer", "The far bank is ours, Commander. One of the eagle captains has laid his spear-thrower at your feet."),
            ("cuali", "I am Cuali. The Sun-Speaker Itzcal told us you carry a stolen sun, a man who throws the sky's own fire. He means to feed that man to the altar and take the fire for himself."),
            ("cuali", "He has fed it enough of my people already. Let me show your archers the atlatl. Then let me show you his temple."),
            ("advisor", "The Battlemage, Varius. The reavers sold him the story, and he believed all of it."),
        ],
        "defeat": [("officer_hurt", "The river ran red and we never reached the bank, Commander.")],
        "reward": {"units": {"eagle": 1}, "spoils": {"Lore": 1, "Armor": 1, "Obsidian": 2}},
    }
)

# ---------------------------------------------------------------- 3. The Temple of the Sun (kill the Sun-Speaker)
LEVELS.append(
    {
        "id": 5996,
        "group": "story",
        "name": "The Temple of the Sun",
        "objective": "Storm the temple and defeat Sun-Speaker Itzcal.",
        "turn_limit": 36,
        "budget": 4750,
        "sides": {"P": ARMY, "A": "Cuali's Eagles", "E": TEMPLE},
        "terrain": """
ffffffffffffffffffffffff
fff.TWWWWWWWWWWWWWWT.fff
ff..W______________W..ff
ff..W_____o__o_____W..ff
ff..W______K_______W..ff
ff..W_____o__o_____W..ff
ff..W______________W..ff
ff..TWWWWWTGGTWWWWWT..ff
fff.......,==,.......fff
ffff.ff....==....ff.ffff
fffffff.x..==..x.fffffff
ffff,fff...==...fff,ffff
ff....ff...==...ff....ff
ff.,...f...==...f...,.ff
fff..ffff..==..ffff..fff
ffffffff...==...ffffffff
ffff,ff....==....ff,ffff
ff....f....==....f....ff
f..........==..........f
f...hh.....==.....hh...f
ff.........==.........ff
ff.........==.........ff
fff........==........fff
ffff.......==.......ffff
fffff......==......fffff
ffffffff...==...ffffffff
""",
        "units": """
........................
........................
.......S........S.......
..............q.........
...........I............
.........j..j.j.........
........j..jj...j.......
......e.e..pp..e.e......
........................
........................
.........l....l.........
........................
....jj............jj....
...j................j...
........................
........................
........................
........................
....cc............cc....
......J..........J......
........................
......DDDDDDDDDDDD......
......DDDDDDDDDDDD......
......DDDDDDDDDDDD......
........................
........................
""",
        "legend": {
            "I": U("sunpriest", "E", group=1, hold=True, name="itzcal"),
            "q": U("sunpriest", "E", group=1, hold=True),
            "p": U("pikemen", "E", group=3, hold=True),
            "j": U("jaguar", "E", group=2, hold=True),
            "e": U("eagle", "E", group=3, hold=True),
            "l": U("footmen", "E", group=4, hold=True),
            "S": U("serpent", "E", group=5),
            "c": U("eagle", "A", group=1),
            "J": U("jaguar", "A", group=1),
        },
        "camera": (11, 4),
        "intro": [
            ("itzcal", "So the thieves of the sun have come to my steps. Good. I was going to send for you."),
            ("itzcal", "You keep a man who throws the sky's fire. Fire belongs to the Sun, and the Sun speaks through me. Give him to the altar and you may sail home."),
            ("cuali", "He will blind your best soldiers and burn them one at a time, Commander, and mend his guard while he does it. He must die first or last. Not in between."),
            ("advisor", "The Speaker is the keystone, Varius. His jaguars hold the court and his eagles the wall. Cuali's people will take the woods with us."),
        ],
        "events": [
            {
                "when": ("kill", "itzcal"),
                "say": [
                    ("itzcal_hurt", "The Sun... does not... set..."),
                    ("cuali", "It has set on you, Speaker. Jaguars! Eagles! The altar is cold. Put down your clubs."),
                ],
                "end": "victory",
            },
            {
                "when": ("round", 5),
                "cam": (3, 23),
                "spawn": [
                    ("jaguar", (3, 23), "E"),
                    ("jaguar", (2, 22), "E"),
                    ("jaguar", (20, 23), "E"),
                    ("jaguar", (21, 22), "E"),
                ],
                "say": [("officer_alarm", "Jaguar men in the trees behind us, Commander!")],
            },
            {
                "when": ("round", 8),
                "cam": (2, 3),
                "spawn": [
                    ("serpent", (2, 3), "E"),
                    ("serpent", (21, 3), "E"),
                    ("eagle", (3, 2), "E"),
                    ("eagle", (20, 2), "E"),
                ],
                "say": [("itzcal", "Come down, children of the wind! Carry these thieves up to me!")],
            },
        ],
        "brief": [
            ("cuali", "The Temple of the Sun, Commander. One gate, a wall my own order built, and Itzcal on the altar stone at the heart of it."),
            ("advisor", "He wants the Battlemage on that stone, Varius. I should prefer to disappoint him in person."),
        ],
        "victory": [
            ("officer", "The Sun-Speaker is dead, Commander. The temple guard have thrown down their clubs."),
            ("cuali", "My people will choose a quieter priest. The serpents are no man's servants, but one of them has followed your banner down the steps. I would not send it away."),
            ("advisor", "Tolm, the Doge, Corvane, Kagemori, and now a priest who had never even seen it. The Battlemage has killed more men by rumour than by lightning, Varius."),
            ("advisor", "Let us go home before the rumour finds another shore."),
        ],
        "defeat": [("officer_hurt", "We could not carry the gate, Commander. The altar is still burning.")],
        "reward": {"units": {"serpent": 1}, "spoils": {"Spirit": 1, "Lore": 1, "Armor": 1, "Obsidian": 2}},
    }
)

# ---------------------------------------------------------------- Raid 1. The Night Hunt (hold the clearing)
LEVELS.append(
    {
        "id": 5997,
        "group": "siege",
        "name": "The Night Hunt",
        "objective": "Hold your camp in the clearing for 8 turns against the jaguar hunt.",
        "turn_limit": 12,
        "budget": 3250,
        "win_switch": False,
        "sides": {"P": ARMY, "E": "Jaguar Order"},
        "terrain": """
ffffffffffffffffffffff
fff,fffff....fffff,fff
ff...fff......fff...ff
ff.,..ff..,,..ff..,.ff
fff...f........f...fff
ffff....x....x....ffff
fff.....PP..PP.....fff
ff......P....P......ff
f...,..........,.....f
f.........hh.........f
f...,..........,.....f
ff......P....P......ff
fff.....PP..PP.....fff
ffff....x....x....ffff
fff...f........f...fff
ff.,..ff..,,..ff..,.ff
ff...fff......fff...ff
fff,fffff....fffff,fff
ffffffffffffffffffffff
""",
        "units": """
......................
..........aa..........
...b.....j..j.....c...
......................
......................
......................
......................
.........DDDD.........
.......DDDDDDDD.......
.......DDD..DDD.......
.......DDDDDDDD.......
.........DDDD.........
......................
......................
......................
......................
...d.....j..j.....e...
..........gg..........
......................
""",
        "legend": {"j": U("jaguar", "E", group=1)},
        "camera": (10, 9),
        "intro": [
            ("officer", "We camp in the clearing tonight, Commander. Fence on four sides and a fire in the middle."),
            ("cuali", "The jaguar order hunts at night, and it hunts camps. They will come through the trees from every side until the moon is down."),
            ("advisor", "Eight turns of the glass, Varius. Keep the men inside the fence and let the forest come to us."),
        ],
        "events": [
            {
                "when": ("round", 2),
                "cam": (3, 2),
                "spawn": [("jaguar", "b", "E"), ("jaguar", "e", "E"), ("eagle", "c", "E")],
                "say": [("officer_alarm", "Eyes in the trees, Commander. North-west and south-east!")],
            },
            {
                "when": ("round", 3),
                "cam": (18, 2),
                "spawn": [("jaguar", "c", "E"), ("jaguar", "d", "E"), ("eagle", "b", "E")],
            },
            {
                "when": ("round", 4),
                "cam": (10, 17),
                "spawn": [("jaguar", "g", "E"), ("jaguar", "a", "E")],
                "say": [("officer", "They are coming over the south fence, Commander!")],
            },
            {
                "when": ("round", 5),
                "cam": (3, 16),
                "spawn": [("jaguar", "d", "E"), ("jaguar", "b", "E"), ("eagle", "e", "E")],
            },
            {
                "when": ("round", 6),
                "cam": (18, 16),
                "spawn": [("jaguar", "e", "E"), ("jaguar", "c", "E"), ("jaguar", "a", "E")],
                "say": [("officer_alarm", "The whole order is out there, Commander. I can hear them calling to each other.")],
            },
            {
                "when": ("round", 7),
                "cam": (10, 1),
                "spawn": [("jaguar", "g", "E"), ("jaguar", "b", "E"), ("eagle", "d", "E")],
            },
            {
                "when": ("round", 9),
                "say": [("cuali", "The moon is down. The hunt is over, Commander. They will not come again tonight.")],
                "end": "victory",
            },
        ],
        "victory": [("officer", "Dawn, Commander. The fence held, and there are spotted hides all round it.")],
        "defeat": [("officer_hurt", "They are inside the fence, Commander. The camp is lost.")],
        "reward": {"units": {"pikemen": 1}, "spoils": {"Beasts": 2, "Armor": 1, "Obsidian": 2}},
    }
)

# ---------------------------------------------------------------- Raid 2. The Sun Treasury (reach the vault in time)
LEVELS.append(
    {
        "id": 5998,
        "group": "siege",
        "name": "The Sun Treasury",
        "objective": "Reach the temple treasury within fourteen turns, or eliminate all enemies.",
        "turn_limit": 14,
        "budget": 3500,
        "sides": {"P": ARMY, "E": "Treasury Guard"},
        "terrain": """
ffffffffffffffffffffff
fffff.TWWWWWWWWT.fffff
ffff..W___K____W..ffff
fff...W________W...fff
fff...TWWWGGWWWT...fff
ffff......==......ffff
fffff.x...==...x.fffff
ffffff....==....ffffff
fff,fff...==...fff,fff
ff...ff...==...ff...ff
ff.,..f...==...f..,.ff
fff.......==.......fff
ffff.ff...==...ff.ffff
fffffff...==...fffffff
ffff,f....==....f,ffff
ff........==........ff
ff........==........ff
fff.......==.......fff
ffff......==......ffff
ffffff....==....ffffff
""",
        "units": """
......................
......................
.......j..1.Q.j.......
.........j..j.........
.......e.e..e.e.......
......................
.......l......l.......
......................
......................
...kk............kk...
....k............k....
......................
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
            "Q": U("sunpriest", "E", group=1, hold=True),
            "j": U("jaguar", "E", group=1, hold=True),
            "e": U("eagle", "E", group=2, hold=True),
            "l": U("footmen", "E", group=3, hold=True),
            "k": U("jaguar", "E", group=4),
        },
        "camera": (10, 2),
        "intro": [
            ("cuali", "Itzcal kept the tribute of forty towns in that vault, Commander. His under-priests are loading it onto litters for the hills."),
            ("advisor", "A priest of the sun inside, eagles on the wall, jaguars in the trees. We have until the litters are full, Varius."),
        ],
        "events": [
            {
                "when": ("reach", "1"),
                "say": [("officer", "We have the vault, Commander. The gold is still on the floor.")],
                "end": "victory",
            },
            {
                "when": ("round", 5),
                "cam": (2, 15),
                "spawn": [
                    ("serpent", (2, 15), "E"),
                    ("jaguar", (2, 16), "E"),
                    ("jaguar", (19, 16), "E"),
                ],
                "say": [("officer_alarm", "A serpent over the trees behind us, Commander, and more of the spotted men under it!")],
            },
        ],
        "victory": [("cuali", "Forty towns will eat this winter, Commander. They will know whose soldiers carried it back.")],
        "defeat": [("officer_hurt", "The vault is empty, Commander. They got it away into the hills.")],
        "reward": {"units": {"archers": 1}, "spoils": {"Weapons": 1, "Lore": 1, "Spirit": 1, "Obsidian": 2}},
    }
)

KINGDOM = {
    "id": "tezcal",
    "short": "Tezcal",
    "name": "The Jungles of Tezcal",
    "order": 16,
    "theme": "green",
    "unlock_after": ["The Mirror Sea"],  # matched on the region's full name (campaign-rules shortName)
    "heraldry": {"E": ("or", "vert", 33, 5), "A": ("argent", "vert", 14, 3)},
    "brief": [
        (
            "emperor",
            "Commander Varius, the Reaver-King is dead and his captains are not. They have run east from the Mirror Sea to a jungle coast the Rukiev call Tezcal, and they have found a patron there.",
        ),
        (
            "thaddius",
            "A priest-king, Commander, the Sun-Speaker Itzcal. The reavers bought their welcome with a story: that the Emperor keeps a man who throws lightning. Itzcal has decided that such fire belongs to his god, and he is taking Rukiev fishermen for his altar until he gets it.",
        ),
        (
            "emperor",
            "I will not have a Battlemage bargained for by anyone, least of all by a man who has never seen one. Land at Tezcal. End the reavers, and persuade this priest that the sky is not his to collect.",
        ),
    ],
    "levels": LEVELS,
}
