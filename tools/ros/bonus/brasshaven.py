"""The Foundries of Brasshaven — three story battles and two raids on the foundry coast west of the Mirror Sea (ours;
see build_bonus.py). The city of the Clockwork Syndicate: a scrapyard gate swarming with Volatile Automatons, an
assembly yard of Conveyor Belts (> < A V) and Vent Grates (v) held by Brass Phalanx and Arc Casters, and the vault
where the Chief Artificer winds his Mainsprings. It opens with the bonus campaigns (beside Tilicia) and nothing waits
on it."""
from build_bonus import U

LEVELS = []
ARMY = "Carrone Army"
SYNDICATE = "The Clockwork Syndicate"

# ---------------------------------------------------------------- 1. The Scrapyard Gate (a swarm of Volatile Automatons)
LEVELS.append(
    {
        "id": 5973,
        "group": "story",
        "name": "The Scrapyard Gate",
        "objective": "Break through the scrapyard to the city gate. Eliminate all enemies.",
        "turn_limit": 30,
        "budget": 2650,
        "sides": {"P": ARMY, "E": SYNDICATE},
        "terrain": """
^^^^^^^^.==.^^^^^^^^
^^^..r...==...r..^^^
^^...h...==...h...^^
^....x...==...x....^
^..r.....==.....r..^
^........==........^
^..x..r..==..r..x..^
^........==........^
^^.......==.......^^
^^..r....==....r..^^
^...x....==....x...^
^........==........^
^..r.....==.....r..^
^........==........^
^........==........^
^^.......==.......^^
^^.......==.......^^
^^^......==......^^^
^^^^.....==.....^^^^
^^^^^^^..==..^^^^^^^
""",
        "units": """
....................
....................
.......c....c.......
.........zz.........
......A..AA..A......
....................
.....A........A.....
........A..A........
....................
......A......A......
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
            "A": U("automaton", "E", group=1),
            "c": U("crossbowmen", "E", group=2, hold=True),
            "z": U("arccaster", "E", group=2, hold=True),
        },
        "camera": (9, 6),
        "intro": [
            ("wren", "That is the scrapyard, Commander, and those are not scrap. Do not let them get close."),
            ("officer", "Little engines on wheels, sir, with lit fuses. A dozen at least, and they are rolling this way."),
            ("advisor", "Each one is a boiler with a ram on it, Varius. When it dies it bursts, on friend and foe alike, and one burst will set off its neighbour. Kill them at a distance, or kill them among their own."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (2, 11),
                "spawn": [
                    ("automaton", (2, 11), "E"),
                    ("automaton", (3, 12), "E"),
                    ("automaton", (17, 11), "E"),
                    ("automaton", (16, 12), "E"),
                ],
                "say": [("officer_alarm", "More of them out of the scrap heaps, Commander, on both sides!")],
            },
            {
                "when": ("round", 6),
                "cam": (9, 1),
                "spawn": [
                    ("automaton", (9, 1), "E"),
                    ("automaton", (10, 1), "E"),
                    ("arccaster", (8, 2), "E"),
                    ("arccaster", (11, 2), "E"),
                ],
                "say": [("enemy", "Units are cheap. The Syndicate has budgeted for this engagement.")],
            },
        ],
        "brief": [
            ("wren", "Wren, Commander. I wound springs for the Syndicate for six years, until I saw what they were winding them for. I can get you to the gate."),
            ("advisor", "The tinker says the first thing they will send is the cheapest, Varius. Machines built to be lost."),
        ],
        "victory": [
            ("officer", "The scrapyard is clear, Commander. We have swept up enough brass to cast a bell."),
            ("wren", "Three of them never lit, Commander. I have had the fuses out and the governors reset. They will roll for you now. I would still not stand next to one."),
        ],
        "defeat": [("officer_hurt", "They blew the line to pieces, Commander. We are falling back from the gate.")],
        "reward": {"units": {"automaton": 2}, "spoils": {"Weapons": 1, "Armor": 1, "Mainspring": 2}},
    }
)

# ---------------------------------------------------------------- 2. The Assembly Line (belts, vents, Phalanx and Arc Casters)
LEVELS.append(
    {
        "id": 5974,
        "group": "story",
        "name": "The Assembly Line",
        "objective": "Take the assembly yard. Eliminate all enemies.",
        "turn_limit": 36,
        "budget": 3050,
        "sides": {"P": ARMY, "E": SYNDICATE},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^^^^^
^TWWWWWWWWTGGTWWWWWWWWT^
^W_________==_________W^
^W__h______==______h__W^
^W_________==_________W^
^W_>>>>>>V_==_V<<<<<<_W^
^W_______V_==_V_______W^
^W__v____V_==_V____v__W^
^W_______V_==_V_______W^
^W_<<<<<<<_==_>>>>>>>_W^
^W_________==_________W^
^W__v______==______v__W^
^W_________==_________W^
^TWWWWWWWWTGGTWWWWWWWWT^
^..........==..........^
^...x......==......x...^
^..........==..........^
^..r.......==.......r..^
^..........==..........^
^^.........==.........^^
^^^........==........^^^
^^^^^^.....==.....^^^^^^
""",
        "units": """
........................
........................
........................
.......c...PP...c.......
....G..............G....
........................
....PP............PP....
........................
.....c............c.....
........................
........PP....PP........
.........c....c.........
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
            "P": U("phalanx", "E", group=1, hold=True),
            "c": U("arccaster", "E", group=2, hold=True),
            "G": U("gyrocopter", "E", group=3),
        },
        "camera": (11, 8),
        "intro": [
            ("wren", "The assembly yard, Commander. The belts never stop. Stand on one when the shift bell rings and you finish the round a pace from where you started it."),
            ("officer", "Brass men in pairs, sir, shields touching. Our arrows are doing nothing to them."),
            ("advisor", "Two of them side by side lock shields against shot, Varius: part them, or go in with steel. The casters' lightning leaps to the nearest heavy armour, so keep the knights apart. And nobody shoots through that steam."),
        ],
        "events": [
            {
                "when": ("round", 4),
                "cam": (11, 2),
                "spawn": [
                    ("automaton", (10, 2), "E"),
                    ("automaton", (13, 2), "E"),
                    ("gyrocopter", (5, 3), "E"),
                    ("gyrocopter", (18, 3), "E"),
                ],
                "say": [("officer_alarm", "Something in the air over the sheds, Commander. It is dropping iron on the road!")],
            },
            {
                "when": ("round", 7),
                "cam": (11, 3),
                "spawn": [
                    ("phalanx", (10, 4), "E"),
                    ("phalanx", (11, 4), "E"),
                    ("phalanx", (12, 4), "E"),
                    ("arccaster", (11, 3), "E"),
                ],
                "say": [("volkmar", "Second shift. Overclock them. I want that yard cleared before the furnaces cool.")],
            },
        ],
        "brief": [
            ("wren", "Through the gate is the assembly yard, Commander: four belts, four steam vents and everything the Syndicate has finished this month standing on parade."),
            ("advisor", "A drilled line of shield-machines with lightning behind it, Varius. I should call it a fortress, if a fortress could be wound up."),
        ],
        "victory": [
            ("officer", "The yard is ours, Commander. The belts are still running, with nothing on them."),
            ("wren", "A shield-pair and a caster came off the line unfinished, Commander: no orders in them yet. I have given them yours."),
        ],
        "defeat": [("officer_hurt", "We could not break the shield line, Commander. The yard is still theirs.")],
        "reward": {"units": {"phalanx": 1, "arccaster": 1}, "spoils": {"Armor": 1, "Lore": 1, "Mainspring": 2}},
    }
)

# ---------------------------------------------------------------- 3. The Mainspring Vault (the Chief Artificer's keep)
LEVELS.append(
    {
        "id": 5975,
        "group": "story",
        "name": "The Mainspring Vault",
        "objective": "Storm the vault and defeat Chief Artificer Volkmar.",
        "turn_limit": 34,
        "budget": 4250,
        "sides": {"P": ARMY, "E": SYNDICATE},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^TWWWWWWWWWWWWWWWWWWT^^^
^^^W__________________W^^^
^^^W__h_____K_____h___W^^^
^^^W__________________W^^^
^^^W_v____>>>>>>___v__W^^^
^^^W__________________W^^^
^^^W_____<<<<<<_______W^^^
^^^W__________________W^^^
^^^TWWWWWWWTGGTWWWWWWWT^^^
^^.........v==v.........^^
^..r....x...==...x....r..^
^...........==...........^
^^..........==..........^^
^^.r........==........r.^^
^...........==...........^
^....x......==......x....^
............==............
..r.........==.........r..
............==............
............==............
............==............
^^..........==..........^^
^^^^........==........^^^^
""",
        "units": """
..........................
..........................
..........................
...........PQP............
.........c.....c..........
..........................
.........PPPPPP...........
..........................
..........................
......c.c........c.c......
..........................
........PPP....PPP........
..........................
......A............A......
...A..................A...
....A................A....
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
            "Q": U("king", "E", group=9, hold=True, name="volkmar"),  # (a group of his own: he keeps the vault)
            "c": U("arccaster", "E", group=1, hold=True),
            "P": U("phalanx", "E", group=2, hold=True),
            "G": U("gyrocopter", "E", group=3),
            "A": U("automaton", "E", group=4),
        },
        "camera": (12, 4),
        "intro": [
            ("volkmar", "An army of meat. How wasteful. Every one of you needs feeding, and breaks when you drop it."),
            ("volkmar", "Mine need only winding. Wound far enough, each of them does the work of two. Observe."),
            ("wren", "That is the Overdrive, Commander. It lets a machine act twice in a turn, and it shakes a quarter of the life out of it every time. He does not care. He never has."),
            ("advisor", "Then let him spend them, Varius. It is his own coils we want. When the Artificer stops, nobody is left who knows how to wind the rest."),
        ],
        "events": [
            {
                "when": ("kill", "volkmar"),
                "say": [
                    ("volkmar_hurt", "Inefficient... I had not... budgeted..."),
                    ("wren", "Springs down, all of you! The shift is over. The shift has been over for years."),
                ],
                "end": "victory",
            },
            {
                "when": ("round", 5),
                "cam": (1, 17),
                "spawn": [
                    ("automaton", (1, 17), "E"),
                    ("automaton", (2, 18), "E"),
                    ("automaton", (24, 17), "E"),
                    ("automaton", (23, 18), "E"),
                ],
                "say": [("officer_alarm", "Bomb-carts on both flanks, Commander, and coming fast!")],
            },
            {
                "when": ("round", 8),
                "cam": (12, 6),
                "spawn": [
                    ("phalanx", (10, 4), "E"),
                    ("phalanx", (14, 4), "E"),
                    ("gyrocopter", (8, 2), "E"),
                    ("gyrocopter", (16, 2), "E"),
                ],
                "say": [("volkmar", "Everything on the floor. Wind them until they sing.")],
            },
        ],
        "brief": [
            ("wren", "The vault, Commander. It is where the Mainsprings are tempered, and where Volkmar keeps himself. One wall, one gate, and belts across the court to carry his machines to the breach."),
            ("advisor", "Flying minelayers over the gate and bombs on the flanks, Varius. Mind where you tread: what those fliers scatter stays until somebody stops to sweep it up."),
        ],
        "victory": [
            ("officer", "Chief Artificer Volkmar is dead, Commander. Every machine in the city has run down where it stood."),
            ("wren", "One of the fliers still answers, Commander. Its pilot says she was never paid, and that you seem the sort who settles accounts."),
            ("advisor", "A city of foundries with no master, Varius. The Emperor will find it one. Let us see that it is the tinker."),
        ],
        "defeat": [("officer_hurt", "The gate held, Commander. The vault is still his.")],
        "reward": {"units": {"gyrocopter": 1}, "spoils": {"Lore": 1, "Weapons": 1, "Armor": 1, "Mainspring": 2}},
    }
)

# ---------------------------------------------------------------- Raid 1. The Gyro Sheds (a flying-machine roost)
LEVELS.append(
    {
        "id": 5976,
        "group": "siege",
        "name": "The Gyro Sheds",
        "objective": "Burn the flying-machine sheds. Eliminate all enemies.",
        "turn_limit": 22,
        "budget": 2850,
        "sides": {"P": ARMY, "E": "Shed Wardens"},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^
^^..r..........r..^^
^...PPPPPPPPPPPP...^
^.r.P..........P.r.^
^...P.h..hh..h.P...^
^...P..........P...^
^...P.h......h.P...^
^.r.P..........P.r.^
^...PPPPPppPPPPP...^
^........==........^
^^..x....==....x..^^
^^.......==.......^^
^...r....==....r...^
^........==........^
.........==.........
..r......==......r..
.........==.........
.........==.........
.........==.........
^^.......==.......^^
""",
        "units": """
....................
....................
....................
......G......G......
.......c..c..c......
....................
....................
......PP....PP......
.........PP.........
....................
.....A..A..A..A.....
....................
....................
....................
....................
....DDDDDDDDDDDD....
....DDDDDDDDDDDD....
....DDDDDDDDDDDD....
....................
....................
""",
        "legend": {
            "G": U("gyrocopter", "E", group=1),
            "c": U("arccaster", "E", group=2, hold=True),
            "P": U("phalanx", "E", group=3, hold=True),
            "A": U("automaton", "E", group=4, hold=True),
        },
        "camera": (9, 5),
        "intro": [
            ("wren", "The gyro sheds, Commander. Every one of those machines that gets into the air sows a field of caltrops before breakfast."),
            ("advisor", "They cannot fight, Varius, only scatter. Archers will bring them down. And have the foot sweep the road as they go, or the horse will never reach the gate."),
        ],
        "events": [
            {
                "when": ("round", 5),
                "cam": (2, 1),
                "spawn": [
                    ("gyrocopter", (2, 1), "E"),
                    ("gyrocopter", (17, 1), "E"),
                    ("automaton", (3, 1), "E"),
                    ("automaton", (16, 1), "E"),
                ],
                "say": [("officer_alarm", "The dawn patrol is back, Commander, and it has brought friends on wheels!")],
            },
        ],
        "victory": [("wren", "They will not fly again this year. I pulled the plans out of the shed office, Commander. Somebody ought to keep them, and it had better not be the Syndicate.")],
        "defeat": [("officer_hurt", "The road is solid iron, Commander. We cannot get near the sheds.")],
        "reward": {"units": {"archers": 1}, "spoils": {"Weapons": 1, "Lore": 1, "Mainspring": 2}},
    }
)

# ---------------------------------------------------------------- Raid 2. The Powder Line (hold a depot against bomb-carts)
LEVELS.append(
    {
        "id": 5977,
        "group": "siege",
        "name": "The Powder Line",
        "objective": "Hold the powder depot for 8 turns against the bomb-carts.",
        "turn_limit": 12,
        "budget": 2400,
        "win_switch": False,
        "sides": {"P": ARMY, "E": "The Night Shift"},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^^^
......................
......................
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
r....................r
rr..,,..........,,..rr
rrr................rrr
^^^^^^^^^^^^^^^^^^^^^^
""",
        "units": """
......................
.a.........b.........c
......................
......................
......................
......................
....DDDDDDDDDDDDDD....
....DDDDDDDDDDDDDD....
d...DDDDDDDDDDDDDD...e
....DDDDDDDDDDDDDD....
....DDDDDDDDDDDDDD....
......................
......................
..........g...........
......................
......................
......................
......................
""",
        "legend": {},
        "camera": (10, 8),
        "intro": [
            ("wren", "The powder depot, Commander. If the Syndicate's carts reach it, there will be a hole here you could lose a village in."),
            ("advisor", "They will come from every side and they only have to arrive, Varius. Stop each one a tile short of the fence: what bursts outside it does the palisade no good, but it does us no harm."),
        ],
        "events": [
            {
                "when": ("round", 2),
                "cam": (10, 1),
                "spawn": [("automaton", "a", "E"), ("automaton", "b", "E"), ("automaton", "c", "E")],
                "say": [("officer_alarm", "Fuses in the dark, Commander! Carts on the north road!")],
            },
            {
                "when": ("round", 3),
                "cam": (21, 8),
                "spawn": [("automaton", "e", "E"), ("arccaster", (21, 3), "E")],
            },
            {
                "when": ("round", 4),
                "cam": (10, 13),
                "spawn": [("automaton", "g", "E"), ("automaton", "d", "E"), ("gyrocopter", (10, 2), "E")],
                "say": [("officer", "South gate now, Commander. They are trying every door.")],
            },
            {
                "when": ("round", 5),
                "cam": (0, 8),
                "spawn": [("automaton", "a", "E"), ("automaton", "c", "E"), ("arccaster", (0, 3), "E")],
            },
            {
                "when": ("round", 6),
                "cam": (10, 1),
                "spawn": [("automaton", "b", "E"), ("automaton", "e", "E"), ("automaton", "d", "E")],
                "say": [("officer_alarm", "They have emptied the whole yard at us, Commander!")],
            },
            {
                "when": ("round", 7),
                "cam": (10, 13),
                "spawn": [("automaton", "g", "E"), ("automaton", "a", "E"), ("phalanx", (10, 2), "E")],
            },
            {
                "when": ("round", 9),
                "say": [("wren", "The day shift whistle, Commander. They never work past it. The depot is safe.")],
                "end": "victory",
            },
        ],
        "victory": [("officer", "Dawn, Commander. The fence is black from end to end, and the powder is dry.")],
        "defeat": [("officer_hurt", "They are through the fence, Commander. Run!")],
        "reward": {"units": {"footmen": 1}, "spoils": {"Armor": 1, "Weapons": 1, "Spirit": 1, "Mainspring": 2}},
    }
)

KINGDOM = {
    "id": "brasshaven",
    "short": "Brasshaven",
    "name": "The Foundries of Brasshaven",
    "order": 22,
    "theme": "green",
    "unlock_after": ["Abbisin"],  # with the bonus campaigns, beside Tilicia; nothing waits on it
    "heraldry": {"E": ("or", "sable", 22, 6)},
    "brief": [
        (
            "emperor",
            "Commander Varius, the free city of Brasshaven has stopped selling us cannon. Last month it sold a thousand brass soldiers to somebody, and will not say to whom.",
        ),
        (
            "thaddius",
            "Its guild of clockmakers calls itself a Syndicate now, Commander. They have learnt to temper a spring that will drive a machine past what it was built to bear, and they are building the machines to go with it.",
        ),
        (
            "emperor",
            "I will not have an army for sale on my northern coast. One of their own tinkers has come over to us and knows the yards. Go into Brasshaven, and stop the line.",
        ),
    ],
    "levels": LEVELS,
}
