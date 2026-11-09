"""Tilicia — "The Empty Tomb": six story battles and three raids (ours; see build_bonus.py)."""
from build_bonus import U

LEVELS = []

# ---------------------------------------------------------------- 1. The Tolm Road (escape through the pass)
LEVELS.append(
    {
        "id": 5901,
        "group": "story",
        "name": "The Tolm Road",
        "objective": "Fight through the pass. At least four of your units must reach the head of the Tolm Road.",
        "mission_type": 3,
        "turn_limit": 30,
        "sides": {"P": "Carrone Army", "E": "Tolm's Wardens"},
        "terrain": """
^^^^^^^.==.^^^^^^^
^ff..r.,==,.r..ff^
^f......==....fff^
^..^^^..==..^^^.f^
^,.^r...==...r^..^
^.......==.......^
^,,..f..==..ff.,,^
^^^^.r..==..r.^^^^
.ff^....==....^.f.
..f^^..===..^^^...
~~~~~~--~~~~--~~~~
~~~~~~--~~~~--~~~~
.ff..===...^^^^..r
^^^r.==..x.^,,^...
.f^..==.......^.,,
..^r.==..ff...^^^^
.....===..ff...f..
.hh....==...,,....
.h.....==..r^^^..f
^^^^.,.==...^.ff..
.ff^r..==...^..f..
..f^..===.....,,..
......==.....ff...
..f...==..,...ff..
.ff...==.........f
.f....==..........
""",
        "units": """
.......gggg.......
..................
..................
....c........c....
......hhhhh.......
.....a...a..a.....
..................
..c............c..
..................
..................
..................
..................
............d.....
.d................
.......rrr........
..................
..................
..................
.............e....
..e...............
..................
..................
.....ffxxff.......
.....sskksp.......
......bbpp........
.......vv.........
""",
        "legend": {
            "f": U("footmen", "P"),
            "s": U("swordsmen", "P"),
            "k": U("knights", "P"),
            "x": U("halberdiers", "P"),
            "p": U("pikemen", "P"),
            "b": U("archers", "P"),
            "v": U("cavalry", "P"),
            "c": U("cragsmen", "E", group=1, hold=True),
            "d": U("cragsmen", "E", group=5, hold=True),
            "e": U("cragsmen", "E", group=6, hold=True),
            "h": U("halberdiers", "E", group=2, hold=True),
            "a": U("archers", "E", group=3, hold=True),
            "r": U("raiders", "E", group=4),
        },
        "camera": (8, 22),
        "intro": [
            ("officer", "Commander, this is the Tolm Road, the only pass into Tilicia wide enough for an army."),
            ("advisor", "And Warden Tolm knows it. Look to the cliffs, Varius. Those are no goatherds."),
            ("officer_alarm", "Javelins! They are throwing from heights our men cannot climb!"),
            ("advisor", "Then we do not stop to trade blows with a mountainside. Get the column to the head of the pass."),
        ],
        "events": [
            {
                "when": ("round", 4),
                "cam": (10, 25),
                "spawn": [("raiders", (9, 25), "E"), ("raiders", (10, 25), "E"), ("raiders", (11, 25), "E")],
                "say": [("officer_alarm", "Riders behind us, Commander! They mean to shut the pass at both ends.")],
            },
            {
                "when": ("round", 6),
                "cam": (9, 25),
                "spawn": [
                    ("footmen", (8, 25), "E"),
                    ("footmen", (9, 25), "E"),
                    ("cragsmen", (10, 25), "E"),
                    ("cragsmen", (11, 25), "E"),
                ],
                "say": [("officer", "Foot coming up the road behind the riders, Commander. We cannot stay in this cut.")],
            },
            {
                "when": ("escaped", 4, "g"),
                "say": [("advisor", "The column is through. Well marched. Tilicia lies before us.")],
            },
        ],
        "brief": [
            ("advisor", "The letters we took from Landower's messenger name a Warden Hadrik Tolm, in Tilicia."),
            ("advisor", "Tilicia is all mountain, Varius. There is one road in, and it bears the Warden's name."),
        ],
        "victory": [
            ("officer", "We are through the pass, Commander, though the cliffs took their toll."),
            ("advisor", "Men who climb like that would be worth having on our side of a wall."),
            ("officer", "The scouts report a clan village in the next valley. They say its people have no love for the Warden."),
        ],
        "defeat": [("officer_hurt", "The pass is shut, Commander. We never saw half of them.")],
        "reward": {"units": {}, "spoils": {"Armor": 1, "Weapons": 1}},
    }
)

# ---------------------------------------------------------------- 2. Ostrak's Bargain (defend the clan village)
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
DDDD.......m............
DDDD......C..C..........
DDDD...........C....ff..
DDDD...........m.....r..
DDDD...........m.....r..
DDDD...........C....ff..
DDDD......C..C..........
DDDD........m...........
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
            ("ostrak", "So the Empire comes to my door. The Warden's men are an hour behind you, Commander."),
            ("ostrak", "Hadrik Tolm takes our sons to dig in his tomb and burns the roof of any clan that refuses. Stand with us today and Clan Ostrak stands with you after."),
            ("advisor", "A fair bargain. Keep the clansmen alive, Varius. We will want every one of them."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (11, 0),
                "spawn": [
                    ("swordsmen", (11, 0), "E"),
                    ("swordsmen", (12, 0), "E"),
                    ("footmen", (10, 0), "E"),
                    ("footmen", (13, 0), "E"),
                    ("swordsmen", (11, 1), "E"),
                    ("halberdiers", (12, 1), "E"),
                    ("halberdiers", (10, 1), "E"),
                ],
                "say": [("officer_alarm", "More of them on the north road, Commander!")],
            },
            {
                "when": ("round", 5),
                "cam": (11, 15),
                "spawn": [
                    ("swordsmen", (11, 15), "E"),
                    ("footmen", (12, 15), "E"),
                    ("footmen", (10, 15), "E"),
                    ("raiders", (13, 15), "E"),
                    ("raiders", (12, 14), "E"),
                    ("swordsmen", (11, 14), "E"),
                    ("halberdiers", (10, 14), "E"),

                ],
                "say": [("clansman", "The south gap! They are in the south gap!")],
            },
            {
                "when": ("round", 7),
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
                    ("swordsmen", (22, 5), "E"),
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
            ("officer", "The village belongs to Clan Ostrak, Commander. Their chief is one Maren Ostrak."),
            ("advisor", "The Warden's riders are on the valley road. If we mean to win these people, now is the hour."),
        ],
        "victory": [
            ("ostrak", "You bled for a village that is not yours. I did not expect that of the Empire."),
            ("ostrak", "Take two bands of my Cragsmen. No wall in Tilicia was built to stop them."),
            ("advisor", "She says the tomb lies past a sealed vale, and past that the fortress of Frostgate."),
        ],
        "defeat": [("officer_hurt", "The village is lost, Commander, and the clans with it.")],
        "reward": {"units": {"cragsmen": 2}, "spoils": {}},
    }
)

# ---------------------------------------------------------------- 3. The Sealed Vale (hold the rune-stones)
LEVELS.append(
    {
        "id": 5903,
        "group": "story",
        "name": "The Sealed Vale",
        "objective": "Hold the vale of the rune-stones for ten turns against the Warden's Spellwardens.",
        "mission_type": 1,
        "areas": ["1", "2", "3"],
        "turn_limit": 20,
        "budget": 3500,
        "win_switch": False,
        "sides": {"P": "Carrone Army", "E": "Tolm's Wardens"},
        "terrain": """
^^^^^^^..==..^^^^^^^
^fff.r...==...,,.ff^
^ff......==.......f^
^f...,,..==..r.....^
^........===..~~~..^
^..r......==..~~~.f^
^.........==.......^
^.oo.o....==.oo.o..^
^.o.......==.o.....^
^....o...===....o.r^
^.o.oo...==..o.oo..^
^f......o==o......f^
^ff.....o==.....ff.^
^f.,,....==o...,,..^
^.......o==o....f..^
^..ff....==....fff.^
..f......==.......f.
.........==.........
..h.h....==.....h...
.........==.........
""",
        "units": """
....................
......x.wSSw.x......
.......hhhhhh.......
......x.w..w.x......
....................
....................
....................
....................
...11.........22....
...11.........22....
....................
....................
.........33.........
.........33.........
....................
....................
....................
.....DDDDDDDDDD.....
.....DDDDDDDDDD.....
.....DDDDDDDDDD.....
""",
        "legend": {
            "w": U("spellwardens", "E", group=1),
            "h": U("halberdiers", "E", group=1),
            "x": U("crossbowmen", "E", group=2),
            "S": U("shamans", "E", group=2),
        },
        "camera": (9, 2),
        "intro": [
            ("officer", "Three rings of standing stones, Commander, and every one of them carved."),
            ("advisor", "Rune-stones. They seal the road to the tomb. The Warden cannot pass his diggers through while we stand among them."),
            ("officer_alarm", "Heavy foot coming down the vale, with rune-marked shields. Our Wizards say their spells die in the air near those men."),
            ("advisor", "Spellwardens. Then it is steel today. Hold the stones until Ostrak's clans close the vale behind them."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (9, 0),
                "spawn": [
                    ("spellwardens", (8, 0), "E"),
                    ("spellwardens", (11, 0), "E"),
                    ("halberdiers", (9, 0), "E"),
                    ("halberdiers", (10, 0), "E"),
                    ("crossbowmen", (7, 0), "E"),
                    ("crossbowmen", (12, 0), "E"),
                    ("halberdiers", (9, 1), "E"),
                    ("spellwardens", (10, 1), "E"),
                ],
                "say": [("officer", "A second company at the head of the vale, Commander.")],
            },
            {
                "when": ("round", 6),
                "cam": (9, 0),
                "spawn": [
                    ("spellwardens", (8, 0), "E"),
                    ("spellwardens", (11, 0), "E"),
                    ("halberdiers", (9, 0), "E"),
                    ("halberdiers", (10, 0), "E"),
                    ("halberdiers", (9, 1), "E"),
                    ("shamans", (10, 1), "E"),
                    ("crossbowmen", (7, 0), "E"),
                    ("crossbowmen", (12, 0), "E"),
                ],
                "say": [("enemy", "The Warden wants this vale by nightfall. Forward!")],
            },
            {
                "when": ("round", 8),
                "cam": (9, 0),
                "spawn": [
                    ("swordsmen", (8, 0), "E"),
                    ("swordsmen", (9, 0), "E"),
                    ("swordsmen", (10, 0), "E"),
                    ("spellwardens", (11, 0), "E"),
                    ("halberdiers", (7, 0), "E"),
                    ("halberdiers", (12, 0), "E"),
                    ("raiders", (9, 1), "E"),
                    ("raiders", (10, 1), "E"),
                ],
                "say": [("officer_alarm", "They are throwing in their reserve!")],
            },
            {
                "when": ("round", 11),
                "say": [
                    ("officer", "Horns on the ridge, Commander! The clans have closed the vale behind them."),
                    ("advisor", "The Warden's men are breaking. The stones are ours.")
                ],
                "end": "victory",
            },
        ],
        "brief": [
            ("advisor", "Chief Ostrak's people call it the Sealed Vale. Nothing the Warden digs up can leave Tilicia except through it."),
            ("advisor", "Her clans need until dusk to take the ridges. Until then the vale is ours to hold."),
        ],
        "victory": [
            ("officer", "The vale is held, Commander. The Spellwardens have fallen back on Frostgate."),
            ("advisor", "Men who can snuff out a Wizard's fire. The Warden has been preparing to face magic for some time."),
            ("advisor", "Or to keep some of his own on a leash."),
        ],
        "defeat": [("officer_hurt", "They have the stones, Commander. The road to the tomb is open to them.")],
        "reward": {"units": {}, "spoils": {"Lore": 1, "Spirit": 1}},
    }
)

# ---------------------------------------------------------------- 4. Frostgate (storm the fortress)
LEVELS.append(
    {
        "id": 5904,
        "group": "story",
        "name": "Frostgate",
        "objective": "Storm the fortress of Frostgate and destroy its garrison.",
        "turn_limit": 30,
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
~~~~~--~~--~~~~.......
~~~~~--~~--~~~~..r....
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
.....b...s..s.........
............t.........
......w.w..b..........
.....w...w............
......pppp............
....MM....MMM.........
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
        ],
        "events": [
            {
                "when": ("round", 6),
                "cam": (21, 14),
                "spawn": [
                    ("cavalry", (21, 13), "E"),
                    ("cavalry", (21, 14), "E"),
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
            ("advisor", "They say the Warden broke the last seal on the tomb two days ago, and that the mountain has not been quiet since."),
            ("officer", "They are asking to march with us, Sir Anston. They would rather face what is in that tomb beside an army."),
        ],
        "defeat": [("officer_hurt", "We broke on the gate, Commander. Frostgate still stands.")],
        "reward": {"units": {"spellwardens": 2}, "spoils": {}},
    }
)

# ---------------------------------------------------------------- 5. The Sleepers Wake (the tomb's guardians)
LEVELS.append(
    {
        "id": 5905,
        "group": "story",
        "name": "The Sleepers Wake",
        "objective": "Destroy every Stone Sentinel that wakes among the ruins.",
        "turn_limit": 30,
        "budget": 2500,
        "win_switch": False,
        "sides": {"P": "Carrone Army", "E": "Tomb Keepers", "E2": "Stone Sentinels"},
        "terrain": """
^^^^^^^^^^^^^^^^^^^^^
^..O.r...T_T..r..O.f^
^f.......___.....,..^
^..r..T..___..T..r..^
^.,......___.....ff.^
^o......_____...r..o^
^..T...._____....T..^
^O.....r_____......O^
^f.r.....___..o..r..^
^ff......___......f.^
^,,...o..___..T...,,^
^O...r...___.....f.O^
.ff.....r___.....ff..
..f......___..,,.....
.........___......f..
....,,...___.........
.....................
.....................
""",
        "units": """
.....................
.....................
..........c..........
........S.c.S........
.......h.S.S.h.......
........h...h........
.....................
.....................
.....................
.....................
.....................
.....................
.....................
.........g.g.........
........w...w........
.........kpk.........
...DDDDDDDDDDDDDDD...
...DDDDDDDDDDDDDDD...
""",
        "legend": {
            "S": U("sentinel", "E2", group=1),
            "c": U("conjurer", "E", group=1, hold=True),
            "h": U("halberdiers", "E", group=2),
            "g": U("greatswordsmen", "P"),
            "w": U("spellwardens", "P"),
            "k": U("catapult", "P"),
            "p": U("priests", "P"),
        },
        "camera": (10, 3),
        "intro": [
            ("officer", "The outer tomb, Commander. The Warden's diggers have been through here, and left in a hurry."),
            ("officer_alarm", "Sir Anston, the statues. The statues are moving!"),
            ("advisor", "Guardians of living stone. Arrows will not trouble them and our Priests cannot mend what they break."),
            ("advisor", "Greatswords and siege stone, Varius. And watch those rune gates. I do not think these two are alone."),
        ],
        "events": [
            {
                "when": ("round", 3),
                "cam": (3, 1),
                "spawn": [("sentinel", (3, 1), "E2"), ("sentinel", (17, 1), "E2")],
                "say": [("officer_alarm", "The northern gates are glowing. Two more of them, Commander!")],
            },
            {
                "when": ("round", 4),
                "cam": (1, 7),
                "spawn": [("sentinel", (1, 7), "E2"), ("sentinel", (19, 7), "E2")],
                "say": [("officer_alarm", "On the flanks! They are stepping out of the walls!")],
            },
            {
                "when": ("round", 6),
                "cam": (1, 11),
                "spawn": [("sentinel", (1, 11), "E2"), ("sentinel", (19, 11), "E2")],
                "say": [("advisor", "Behind our line, by the southern gates! Those are the last. Bring them down.")],
                "win_switch": True,
            },
        ],
        "brief": [
            ("advisor", "The Spellwardens speak of sleepers in the outer tomb, set there by whoever sealed the Battlemage in."),
            ("advisor", "The Warden marched past them with the right words. We do not have the words."),
        ],
        "victory": [
            ("officer", "The last of them is rubble, Commander."),
            ("advisor", "Built to keep the world out, or to keep something in. I begin to wonder which."),
            ("officer", "The inner tomb is on the plateau above. The Warden's banner is flying over it."),
        ],
        "defeat": [("officer_hurt", "They do not tire, Commander. They do not even slow.")],
        "reward": {"units": {}, "spoils": {"Weapons": 1, "Lore": 1, "Beasts": 1}},
    }
)

# ---------------------------------------------------------------- 6. The Empty Tomb (Warden Tolm)
LEVELS.append(
    {
        "id": 5906,
        "group": "story",
        "name": "The Empty Tomb",
        "objective": "Defeat Warden Tolm before the tomb of the Battlemage.",
        "turn_limit": 30,
        "budget": 5000,
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
.........S....S.........
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
            ("advisor", "The inner tomb, Varius. Warden Tolm has drawn up everything he has left before its doors."),
            ("advisor", "Clansmen, Spellwardens, even the stone guardians answer him here. Mind your rear on that plateau."),
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
        "budget": 3000,
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
        "objective": "Destroy every Stone Sentinel in the old quarry.",
        "turn_limit": 30,
        "budget": 3500,
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
.....S.....S.....S.....
.......................
.......................
........T.....T........
.......................
....U......V......U....
.......................
.......................
........W.....W........
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
            "V": U("sentinel", "E", group=3),
            "W": U("sentinel", "E", group=5),
        },
        "camera": (11, 7),
        "intro": [
            ("officer", "The clans call this the Quarry of Giants, Commander. They say the stone here was never cut by men."),
            ("advisor", "It was cut into soldiers. Ten of them, by my count, and all of them awake."),
        ],
        "events": [],
        "victory": [("officer", "The quarry is quiet, Commander. Nothing in it is standing.")],
        "defeat": [("officer_hurt", "We cannot stand against them in the open, Commander.")],
        "reward": {"units": {}, "spoils": {"Lore": 2, "Armor": 1}},
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
..........c...........
.........cc...........
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
