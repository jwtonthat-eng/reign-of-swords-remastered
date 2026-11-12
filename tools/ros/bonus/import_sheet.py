#!/usr/bin/env python3
"""The bonus units' sprites, cut from the supplied art sheets (tools/ros/bonus/art/*.jpg).

The sheet shows each unit as a row of poses on a flat green ground: a standing pose, walk frames, attack frames.
This tool cuts every pose out (the ground is flood-filled away from the edges of its cell, so greens inside a figure
stay), scales it to the game's pixel scale (a foot soldier about 62 px tall, feet on the bottom line), turns the
figures' blue and green cloth into the two team-colour key ramps the engine re-palettes per army, and writes:

    sprites/<key>.png         the attack strip, 88 px frames (the frame numbers are in data/bonus-units.js)
    sprites/stand/<key>.png   the standing pose, cropped
    sprites/walk/<key>.png    four 64x72 walk frames (none for the Battlemage: it glides, like the Wizard)
    docs/images/bonus-units.png   a preview of the result

    python3 tools/ros/bonus/import_sheet.py

(draw_units.py draws the six ability icons.)
"""
import colorsys
import os
from collections import deque

from PIL import Image, ImageDraw

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ART = os.path.join(ROOT, "tools", "ros", "bonus", "art")
SHEETS = {"first": "bonus-units-sheet.jpg", "second": "samurai-gladiator-sheet.jpg", "dragon": "dragon-rider-sheet.jpg",
          "beasts": "beastmaster-hounds-sheet.jpg", "satoshi": "satoshi-units-sheet.jpg",
          "alchemy": "alchemy-units-sheet.jpg", "mythic": "mythic-units-sheet.jpg",
          "aztec": "aztec-units-sheet.jpg", "north": "norse-egypt-units-sheet.jpg",
          "ocean": "polynesian-units-sheet.jpg", "aztec2": "aztec2-units-sheet.jpg"}  # a unit's "sheet" (default first)
SPRITES = os.path.join(ROOT, "public", "games", "reign-of-swords", "sprites")
FRAME, WALK_W, WALK_H = 88, 64, 72
GROUND = (83, 116, 79)  # the sheet's green
GREEN = [(0x00, 0xD4, 0x0B), (0x00, 0xA6, 0x06), (0x00, 0x78, 0x00)]  # data/game-data.js UNIT_KEY_PRIMARY
BLUE = [(0x00, 0x15, 0xFF), (0x00, 0x0B, 0xC6), (0x00, 0x00, 0x8C)]  # UNIT_KEY_SECONDARY
KEYS = set(GREEN) | set(BLUE)

# Per unit: the sheet rows it occupies, the x-range of each pose (left to right), which poses are the stand, the walk
# cycle and the attack, the height in game pixels of its standing pose, and whether its cloth takes team colours.
UNITS = {
    "cragsmen": {
        "rows": (36, 188),
        "cells": [(14, 135), (160, 283), (320, 435), (457, 569), (571, 691), (721, 843), (869, 989), (1055, 1201),
                  (1265, 1424), (1481, 1672), (1717, 1896)],
        "stand": 0, "walk": [1, 4, 5, 6], "attack": [6, 7, 8, 9, 10], "height": 62, "team": True,
    },
    "spellwardens": {
        "rows": (218, 374),
        "cells": [(29, 122), (178, 272), (319, 415), (456, 553), (588, 685), (742, 837), (870, 994), (1025, 1148),
                  (1196, 1295), (1337, 1477), (1507, 1651), (1697, 1847)],
        "stand": 0, "walk": [1, 2, 3, 4], "attack": [5, 6, 7, 8, 9, 5], "height": 62, "team": True,
    },
    "sentinel": {
        "rows": (408, 565),
        "cells": [(30, 138), (171, 279), (309, 409), (443, 546), (582, 683), (737, 843), (870, 1001), (1033, 1145),
                  (1181, 1299), (1335, 1486), (1496, 1651), (1664, 1829), (1841, 1961)],
        "stand": 0, "walk": [1, 2, 3, 4], "attack": [5, 6, 7, 8, 9, 10, 11, 12], "height": 70, "team": False,
    },
    "marines": {
        "rows": (596, 753),
        "cells": [(38, 148), (189, 300), (323, 435), (455, 566), (592, 704), (747, 856), (898, 1015), (1050, 1161),
                  (1197, 1346), (1349, 1496), (1512, 1690), (1693, 1849)],
        "stand": 0, "walk": [1, 2, 3, 4], "attack": [5, 6, 7, 8, 9, 10, 11], "height": 63, "team": True,
    },
    "pavisiers": {
        "rows": (790, 940),
        "cells": [(29, 136), (178, 285), (310, 413), (436, 550), (573, 685), (729, 846), (878, 996), (1032, 1147),
                  (1188, 1324), (1340, 1475), (1506, 1641), (1676, 1810), (1838, 1973)],
        "stand": 0, "walk": [1, 2, 3, 4], "attack": [5, 6, 7, 8, 9, 10, 11, 12], "height": 62, "team": True,
    },
    "battlemage": {
        "rows": (968, 1114),
        "cells": [(31, 129), (181, 280), (437, 535), (547, 676), (703, 842), (886, 974), (991, 1154), (1168, 1317),
                  (1343, 1476), (1506, 1636), (1677, 1807)],
        "stand": 0, "walk": None, "attack": [3, 4, 5, 6, 7, 8, 9, 10], "height": 72, "team": True,
    },
    # the second sheet draws each unit three times over; one row of each is used
    "gladiator": {
        "sheet": "second",
        "rows": (776, 940),
        "cells": [(26, 126), (174, 274), (314, 415), (446, 549), (588, 684), (739, 834), (880, 992), (1036, 1175),
                  (1186, 1330), (1340, 1485), (1504, 1646), (1655, 1811), (1838, 1985)],
        "stand": 0, "walk": [1, 2, 3, 4], "attack": [6, 7, 8, 10, 11, 12, 5], "height": 62, "team": True,
    },
    "samurai": {
        "sheet": "second",
        "rows": (26, 190),
        "cells": [(21, 113), (168, 266), (310, 409), (442, 541), (582, 680), (740, 882), (892, 1044), (1059, 1228),
                  (1321, 1431), (1512, 1671), (1722, 1824)],
        "stand": 0, "walk": [1, 2, 3, 4], "attack": [5, 6, 7, 8, 9, 10], "height": 64, "team": True,
    },
    # The Dragon Rider's sheet is laid out freely, so each pose is a box (x0, y0, x1, y1) with the x of the dragon's
    # body in it ("anchor": what stands on the tile's centre). Its frames are larger (176 x 128), the flying poses
    # hang a little above the ground line ("lift"), and the fire-breath pose is cut where the flame leaves the frame
    # (the shot itself is the engine's fireball). Attack strip: fly, breathe, fly | fly, dive, strike, fly.
    "dragonrider": {
        "sheet": "dragon",
        "boxes": [(4, 120, 370, 392), (5, 610, 428, 992), (457, 616, 985, 1108), (1176, 612, 1568, 1030),
                  (1570, 660, 1986, 1030)],
        "anchors": [185, 215, 690, 1370, 1770],
        "stand": 0, "walk": None, "attack": [1, 2, 1, 1, 3, 4, 1], "height": 84, "team": "blue",
        "frame": (176, 128), "lift": 10,
    },
    # the Beast Master and its Hounds: stand, stand, run, run, then the whip (raise, coil, wind, crack) / the pack's
    # run, leap, snarl and bite
    "beastmaster": {
        "sheet": "beasts",
        "rows": (195, 455),
        "cells": [(21, 141), (183, 308), (357, 553), (594, 778), (810, 1028), (1065, 1258), (1303, 1485),
                  (1525, 1817), (1865, 2015), (2060, 2225), (2253, 2489)],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [4, 5, 6, 7, 8], "height": 62, "team": True,
    },
    "hounds": {
        "sheet": "beasts",
        "rows": (933, 1107),
        "cells": [(12, 162), (184, 336), (363, 590), (615, 847), (871, 1106), (1137, 1378), (1398, 1586),
                  (1606, 1850), (1877, 2065), (2096, 2334)],
        "stand": 0, "walk": [2, 3, 4, 3], "attack": [4, 5, 7, 6], "height": 36, "team": True,
    },
    # The Satoshi sheet (Sohei, Shinobi, Oni, Tengu). Its poses overlap here and there: "solo" lists the cells where
    # only the largest connected shape is kept (a neighbour's blade tip pokes in). Wide blows get a wider frame.
    "sohei": {
        "sheet": "satoshi",
        "rows": (100, 423),
        "cells": [(52, 191), (239, 512), (518, 756), (760, 1050), (1088, 1521), (1581, 1930), (1944, 2185)],
        "solo": [3],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [1, 4, 5, 6], "height": 80, "team": False,
        "frame": (128, 88),
    },
    # strip: crouch, slash, dash (the sword) | ready, throw, ready (the shuriken)
    "shinobi": {
        "sheet": "satoshi",
        "rows": (542, 822),
        "cells": [(70, 201), (252, 410), (472, 708), (760, 992), (1066, 1434), (1454, 1842), (1906, 2119)],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [2, 4, 3, 1, 5, 1], "height": 52, "team": False,
        "frame": (104, 88),
    },
    # strip: brace, raise, slam, brace
    "oni": {
        "sheet": "satoshi",
        "boxes": [(17, 935, 256, 1262), (541, 935, 783, 1262), (803, 935, 1034, 1262), (1097, 935, 1333, 1262),
                  (1336, 935, 1807, 1262), (1860, 935, 2091, 1262)],
        "anchors": [127, 653, 920, 1200, 1447, 1960],
        "stand": 0, "walk": [1, 2, 1, 2], "attack": [5, 3, 4, 5], "height": 74, "team": False,
        "frame": (128, 96), "lift": 0,
    },
    # strip: fly, fly with the blade, the gale, fly with the blade
    "tengu": {
        "sheet": "satoshi",
        "boxes": [(17, 1352, 252, 1683), (272, 1352, 499, 1683), (539, 1297, 809, 1683), (849, 1297, 1122, 1683),
                  (1181, 1297, 1750, 1683), (1802, 1297, 2081, 1683)],
        "anchors": [140, 387, 680, 1013, 1413, 1953],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [2, 3, 4, 3], "height": 70, "team": False,
        "frame": (144, 104), "lift": 0,
    },
    # The alchemy sheet (Alchemist, Golem, Imp; its Gryphon Rider row is not used) and the mythic sheet (Unicorn,
    # Efreet, Naga, Skeleton). The splashes, beams and flames drawn beside the figures are left out: the engine
    # draws the shots.
    "alchemist": {
        "sheet": "alchemy",
        "rows": (460, 649),
        "cells": [(9, 111), (121, 224), (280, 376), (385, 479), (491, 599), (664, 785), (789, 891), (898, 1014),
                  (1514, 1622)],
        "stand": 0, "walk": [2, 3, 4, 3], "attack": [1, 5, 6, 7], "height": 62, "team": False,
    },
    "golem": {
        "sheet": "alchemy",
        "rows": (741, 987),
        "cells": [(6, 144), (156, 289), (341, 489), (501, 651), (694, 856), (867, 1040), (1051, 1218),
                  (1227, 1416), (1463, 1635)],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [5, 6, 7, 8], "height": 76, "team": False,
        "frame": (104, 104),
    },
    "imp": {
        "sheet": "alchemy",
        "rows": (1107, 1251),
        "cells": [(15, 104), (124, 214), (277, 366), (383, 480), (494, 615), (661, 789), (809, 952), (969, 1093)],
        "stand": 0, "walk": [2, 3, 4, 3], "attack": [4, 5, 6, 7], "height": 46, "team": False,
    },
    "unicorn": {
        "sheet": "mythic",
        "rows": (74, 354),
        "cells": [(21, 202), (238, 419), (472, 697), (708, 933), (959, 1189), (1504, 1717)],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [1, 4, 5, 4], "height": 78, "team": False,
        "frame": (112, 104),
    },
    "efreet": {
        "sheet": "mythic",
        "rows": (436, 655),
        "cells": [(51, 139), (187, 310), (465, 648), (664, 891), (915, 1150), (1525, 1694)],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [1, 3, 4, 1], "height": 70, "team": False,
    },
    "naga": {
        "sheet": "mythic",
        "rows": (756, 1000),
        "cells": [(16, 167), (190, 342), (413, 636), (642, 830), (1255, 1438), (1478, 1651)],
        "stand": 0, "walk": [0, 1, 0, 1], "attack": [0, 1, 4, 5], "height": 70, "team": False,
    },
    # (its walking and overhead poses are drawn without the helmet, so the helmeted ones are used throughout)
    "skeleton": {
        "sheet": "mythic",
        "rows": (1075, 1315),
        "cells": [(20, 153), (187, 320), (403, 539), (568, 713), (802, 947), (974, 1209), (1256, 1429)],
        "stand": 0, "walk": [1, 4, 1, 4], "attack": [0, 4, 5, 4], "height": 62, "team": False,
    },
    # The Aztec sheet (Jaguar Warrior, Eagle Warrior, Sun Priest, Feathered Serpent). The Eagle Warrior's two throwing
    # poses are drawn with their darts in flight beside them ("solo" keeps the figure only).
    "jaguar": {
        "sheet": "aztec",
        "rows": (75, 332),
        "cells": [(13, 189), (211, 378), (419, 587), (613, 873), (886, 1205), (1240, 1487), (1521, 1685)],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [0, 6, 4, 5], "height": 66, "team": False,
        "frame": (112, 88),
    },
    "eagle": {
        "sheet": "aztec",
        "rows": (429, 662),
        "cells": [(28, 185), (219, 375), (417, 598), (612, 803), (833, 1075), (1160, 1370), (1509, 1688)],
        "solo": [4, 5],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [1, 4, 5, 1], "height": 70, "team": False,
        "frame": (104, 88),
    },
    "sunpriest": {
        "sheet": "aztec",
        "rows": (745, 995),
        "cells": [(45, 216), (234, 385), (451, 617), (632, 805), (877, 1069), (1072, 1265), (1504, 1656)],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [1, 4, 5, 1], "height": 74, "team": False,
        "frame": (96, 88),
    },
    # strip: hover, hover, the gale, hover (no walk sheet: it glides, like the Dragon Rider)
    "serpent": {
        "sheet": "aztec",
        "boxes": [(11, 1072, 218, 1335), (224, 1072, 432, 1335), (464, 1072, 905, 1335), (938, 1072, 1389, 1335),
                  (1435, 1072, 1666, 1335)],
        "anchors": [115, 330, 690, 1090, 1550],
        "stand": 0, "walk": None, "attack": [0, 1, 3, 1], "height": 72, "team": False,
        "frame": (144, 104), "lift": 0,
    },
    # The Norse and Egyptian sheet. Its rows are packed, with each unit's label printed over the left of its row, so
    # every pose is a box measured by eye (the boxes start below the label where a pose stands under it).
    "berserker": {
        "sheet": "north",
        "boxes": [(18, 92, 269, 302), (271, 92, 467, 302), (469, 92, 746, 302), (809, 92, 986, 302),
                  (1104, 42, 1455, 302), (1490, 42, 1658, 302), (1716, 42, 1880, 302), (1971, 42, 2125, 302)],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [0, 5, 4, 6], "height": 64, "team": False,
        "frame": (128, 96),
    },
    "einherjar": {
        "sheet": "north",
        "boxes": [(40, 362, 190, 540), (245, 362, 395, 540), (597, 345, 742, 540), (901, 345, 1065, 540),
                  (1190, 308, 1410, 540), (1482, 308, 1674, 540), (1714, 330, 1869, 540)],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [1, 4, 5, 6], "height": 62, "team": False,
        "frame": (96, 88),
    },
    "shieldmaiden": {
        "sheet": "north",
        "boxes": [(40, 594, 200, 740), (240, 594, 400, 740), (650, 575, 745, 740), (899, 560, 1051, 740),
                  (1175, 560, 1457, 740), (1487, 560, 1649, 740), (1727, 560, 1865, 740)],
        "stand": 0, "walk": [1, 3, 1, 3], "attack": [0, 5, 4, 5], "height": 56, "team": False,
        "frame": (128, 88),
    },
    "jotunn": {
        "sheet": "north",
        "boxes": [(13, 796, 215, 1000), (238, 796, 430, 1000), (534, 742, 740, 1000), (880, 760, 1086, 1000),
                  (1257, 742, 1801, 1000), (1928, 760, 2106, 1000)],
        "anchors": [110, 335, 650, 985, 1380, 2015],
        "stand": 0, "walk": [3, 5, 3, 5], "attack": [0, 2, 4, 5], "height": 76, "team": False,
        "frame": (160, 104), "lift": 0,
    },
    "medjay": {
        "sheet": "north",
        "boxes": [(55, 1054, 185, 1190), (240, 1054, 380, 1190), (607, 1014, 741, 1190), (912, 1040, 1072, 1190),
                  (1232, 1014, 1420, 1190), (1948, 1030, 2068, 1190)],
        "stand": 0, "walk": [3, 1, 3, 1], "attack": [1, 2, 4, 2], "height": 58, "team": False,
    },
    "khopesh": {
        "sheet": "north",
        # (its two standing poses are printed under the label; the ready pose with the khopesh raised stands in)
        "boxes": [(939, 1195, 1079, 1348), (1242, 1160, 1470, 1348), (1931, 1195, 2089, 1348)],
        "stand": 2, "walk": [0, 2, 0, 2], "attack": [2, 0, 1, 2], "height": 64, "team": False,
        "frame": (128, 88),
    },
    "anubis": {
        "sheet": "north",
        "boxes": [(68, 1402, 180, 1514), (236, 1402, 365, 1514), (932, 1380, 1062, 1514), (1223, 1350, 1410, 1514),
                  (1926, 1360, 2087, 1514)],
        "stand": 0, "walk": [2, 0, 2, 0], "attack": [1, 4, 3, 4], "height": 58, "team": False,
        "frame": (104, 88),
    },
    # (no walk sheet: the beast is longer than a walk frame, so it glides like the Dragon Rider)
    "ammit": {
        "sheet": "north",
        "boxes": [(526, 1535, 812, 1690), (1192, 1535, 1520, 1690), (1895, 1525, 2102, 1690)],
        "stand": 0, "walk": None, "attack": [0, 2, 1, 0], "height": 46, "team": False,
        "frame": (112, 88),
    },
    # The Polynesian sheet and the second Aztec sheet (a darker ground; boxes by eye again).
    "toa": {
        "sheet": "ocean", "ground": (61, 78, 64),
        "boxes": [(60, 110, 278, 378), (308, 110, 516, 378), (570, 130, 845, 378), (875, 130, 1065, 378),
                  (1120, 90, 1470, 378), (1482, 130, 1778, 378), (1822, 130, 2045, 378)],
        "stand": 0, "walk": [3, 2, 3, 2], "attack": [1, 5, 4, 6], "height": 82, "team": False,
        "frame": (128, 96),
    },
    "tahuanui": {
        "sheet": "ocean", "ground": (61, 78, 64),
        "boxes": [(13, 500, 362, 860), (385, 500, 735, 860), (740, 560, 1190, 860), (1175, 590, 1660, 860),
                  (1668, 500, 2030, 860)],
        "anchors": [200, 573, 973, 1440, 1867],
        "solo": [4],
        "stand": 0, "walk": None, "attack": [0, 2, 3, 4], "height": 84, "team": False,
        "frame": (144, 104), "lift": 0,
    },
    "tohunga": {
        "sheet": "ocean", "ground": (61, 78, 64),
        "boxes": [(520, 985, 660, 1285), (687, 985, 910, 1285), (913, 985, 1135, 1285), (1133, 985, 1395, 1285),
                  (1390, 960, 1800, 1285), (1815, 985, 2038, 1285)],
        "stand": 0, "walk": [1, 2, 1, 2], "attack": [0, 3, 4, 5], "height": 64, "team": False,
        "frame": (128, 96),
    },
    "taniwha": {
        "sheet": "ocean", "ground": (61, 78, 64),
        "boxes": [(13, 1500, 402, 1785), (405, 1425, 722, 1785), (722, 1600, 1162, 1785), (1195, 1440, 1740, 1785),
                  (1745, 1440, 2030, 1785)],
        "anchors": [200, 573, 933, 1507, 1893],
        "stand": 0, "walk": None, "attack": [0, 1, 3, 4], "height": 70, "team": False,
        "frame": (160, 104), "lift": 0,
    },
    "coatecpatl": {
        "sheet": "aztec2", "ground": (61, 78, 64),
        "boxes": [(45, 105, 295, 398), (300, 105, 548, 398), (548, 105, 735, 398), (735, 130, 1000, 398),
                  (1000, 85, 1400, 398), (1825, 100, 2050, 398)],
        "solo": [2, 3],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [1, 5, 4, 1], "height": 66, "team": False,
        "frame": (128, 96),
    },
    "chieftain": {
        "sheet": "aztec2", "ground": (61, 78, 64),
        "boxes": [(45, 515, 243, 838), (298, 515, 490, 838), (500, 515, 800, 838), (802, 515, 1182, 838),
                  (1187, 515, 1585, 838), (1810, 560, 2015, 838)],
        "stand": 0, "walk": [0, 1, 0, 1], "attack": [1, 2, 4, 1], "height": 78, "team": False,
        "frame": (128, 96),
    },
    "tzitzimitl": {
        "sheet": "aztec2", "ground": (61, 78, 64),
        "boxes": [(80, 965, 300, 1305), (340, 965, 560, 1305), (587, 985, 875, 1305), (878, 985, 1205, 1305),
                  (1207, 945, 1470, 1305), (1470, 945, 1770, 1305)],
        "stand": 0, "walk": [2, 3, 2, 3], "attack": [1, 4, 5, 4], "height": 74, "team": False,
        "frame": (96, 96),
    },
    "ahuizotl": {
        "sheet": "aztec2", "ground": (61, 78, 64),
        "boxes": [(38, 1490, 335, 1772), (358, 1490, 655, 1772), (730, 1550, 1162, 1772), (1205, 1480, 1760, 1772),
                  (1765, 1490, 1990, 1772)],
        "anchors": [187, 507, 960, 1453, 1867],
        "stand": 0, "walk": [0, 1, 0, 1], "attack": [0, 2, 3, 4], "height": 50, "team": False,
        "frame": (128, 88), "lift": 0,
    },
}


def largest_shape(cell):
    """Clear everything but the largest connected shape (8-connected) of a cut pose."""
    w, h = cell.size
    px = cell.load()
    label = [[0] * w for _ in range(h)]
    sizes = {}
    for sy in range(h):
        for sx in range(w):
            if not px[sx, sy][3] or label[sy][sx]:
                continue
            n = len(sizes) + 1
            label[sy][sx] = n
            queue, count = deque([(sx, sy)]), 0
            while queue:
                x, y = queue.popleft()
                count += 1
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] and not label[ny][nx]:
                            label[ny][nx] = n
                            queue.append((nx, ny))
            sizes[n] = count
    keep = max(sizes, key=sizes.get)
    for y in range(h):
        for x in range(w):
            if label[y][x] and label[y][x] != keep:
                px[x, y] = (0, 0, 0, 0)


def cut(sheet, box, solo=False, ground=GROUND):
    """One pose, its ground flood-filled to transparent from the cell's edges."""
    cell = sheet.crop(box).convert("RGBA")
    w, h = cell.size
    px = cell.load()
    near = lambda c: abs(c[0] - ground[0]) + abs(c[1] - ground[1]) + abs(c[2] - ground[2]) < 46
    seen = [[False] * w for _ in range(h)]
    queue = deque()
    for x in range(w):
        queue.extend(((x, 0), (x, h - 1)))
    for y in range(h):
        queue.extend(((0, y), (w - 1, y)))
    while queue:
        x, y = queue.popleft()
        if not (0 <= x < w and 0 <= y < h) or seen[y][x]:
            continue
        seen[y][x] = True
        if not near(px[x, y]):
            continue
        px[x, y] = (0, 0, 0, 0)
        queue.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    # specks left by the JPEG around the figure: drop opaque pixels with almost no opaque neighbours
    for _ in range(2):
        drop = []
        for y in range(h):
            for x in range(w):
                if px[x, y][3] and sum(
                    1 for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                    if 0 <= x + dx < w and 0 <= y + dy < h and px[x + dx, y + dy][3]
                ) <= 3:
                    drop.append((x, y))
        for x, y in drop:
            px[x, y] = (0, 0, 0, 0)
    if solo:
        largest_shape(cell)
    box = cell.getbbox()
    out = cell.crop(box)
    out.info["dx"] = box[0]  # how far the crop moved the pose's left edge (for poses placed by a measured anchor)
    return out


def team_colours(image, only=None):
    """Blue and green cloth -> the key ramps (three flat shades each), so an army's heraldry recolours it."""
    px = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            ramp = BLUE if 0.57 < h < 0.72 and s > 0.42 and v > 0.2 else GREEN if 0.24 < h < 0.44 and s > 0.42 and v > 0.2 else None
            if only == "blue" and ramp is GREEN:
                ramp = None  # (a green dragon stays green: only its blue wing membranes take the army's colour)
            if ramp:
                px[x, y] = ramp[0 if v > 0.62 else 1 if v > 0.42 else 2] + (255,)
            elif (r, g, b) in KEYS:
                px[x, y] = (r, g, max(1, b - 2), 255)
    return image


def scaled(pose, scale, team):
    size = (max(1, round(pose.width * scale)), max(1, round(pose.height * scale)))
    small = pose.resize(size, Image.LANCZOS)
    px = small.load()
    for y in range(small.height):
        for x in range(small.width):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 255) if a >= 120 else (0, 0, 0, 0)
    small = small.crop(small.getbbox())
    return team_colours(small, team if isinstance(team, str) else None) if team else small


def feet_x(pose):
    """The middle of what the figure stands on (its lowest rows)."""
    xs = [x for y in range(max(0, pose.height - 5), pose.height) for x in range(pose.width) if pose.getpixel((x, y))[3]]
    return sum(xs) / len(xs) if xs else pose.width / 2


def framed(pose, width, height, at):
    """A pose in a frame: feet on the bottom line, its footing at x = `at` (nudged in if the pose would spill)."""
    frame = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    if pose.height > height:
        pose = pose.crop((0, pose.height - height, pose.width, pose.height))
    if pose.width > width:
        pose = pose.crop((0, 0, width, pose.height))
    left = round(at - feet_x(pose))
    left = max(0, min(width - pose.width, left))
    frame.alpha_composite(pose, (left, height - pose.height))
    return frame


def build(sheet, key):
    unit = UNITS[key]
    ground = unit.get("ground", GROUND)  # (the later sheets stand on a darker green)
    if "boxes" in unit:
        poses = [cut(sheet, box, i in unit.get("solo", ()), ground) for i, box in enumerate(unit["boxes"])]
    else:
        top, bottom = unit["rows"]
        poses = [
            cut(sheet, (x0, top, x1, bottom), i in unit.get("solo", ()), ground)
            for i, (x0, x1) in enumerate(unit["cells"])
        ]
    scale = unit["height"] / poses[unit["stand"]].height
    small = [scaled(p, scale, unit["team"]) for p in poses]
    stand = small[unit["stand"]]
    width, height = unit.get("frame", (FRAME, FRAME))
    strip = Image.new("RGBA", (width * len(unit["attack"]), height), (0, 0, 0, 0))
    for i, n in enumerate(unit["attack"]):
        if "anchors" in unit:  # the body's x, measured on the sheet: put it on the frame's centre, lifted off the ground
            # (cut() crops to the pose's own bounding box, which starts at or after the box's left edge)
            frame = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            pose = small[n]
            left = round(width / 2 - (unit["anchors"][n] - unit["boxes"][n][0] - poses[n].info.get("dx", 0)) * scale)
            frame.alpha_composite(pose, (max(0, left), max(0, height - pose.height - unit.get("lift", 0))))
        else:
            frame = framed(small[n], width, height, 40 if width == FRAME else width // 2 - 4)
        strip.alpha_composite(frame, (i * width, 0))
    walk = None
    if unit["walk"]:
        walk = Image.new("RGBA", (WALK_W * 4, WALK_H), (0, 0, 0, 0))
        for i, n in enumerate(unit["walk"]):
            walk.alpha_composite(framed(small[n], WALK_W, WALK_H, WALK_W // 2), (i * WALK_W, 0))
    return strip, stand, walk


def preview(built, path):
    rows = []
    for key, (strip, stand, walk) in built.items():
        parts = [stand] + ([walk] if walk else []) + [strip]
        row = Image.new(
            "RGBA", (sum(p.width for p in parts) + 8 * (len(parts) + 1), strip.height + 14), (84, 122, 84, 255)
        )
        ImageDraw.Draw(row).text((4, 0), key, fill=(255, 255, 255, 255))
        x = 8
        for part in parts:
            row.alpha_composite(part, (x, row.height - part.height))
            x += part.width + 8
        rows.append(row)
    sheet = Image.new("RGBA", (max(r.width for r in rows), sum(r.height for r in rows)), (84, 122, 84, 255))
    y = 0
    for row in rows:
        sheet.alpha_composite(row, (0, y))
        y += row.height
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(path)


def main():
    sheets = {name: Image.open(os.path.join(ART, file)).convert("RGB") for name, file in SHEETS.items()}
    built = {}
    for key in UNITS:
        strip, stand, walk = build(sheets[UNITS[key].get("sheet", "first")], key)
        strip.save(os.path.join(SPRITES, key + ".png"))
        stand.save(os.path.join(SPRITES, "stand", key + ".png"))
        walk_path = os.path.join(SPRITES, "walk", key + ".png")
        if walk:
            walk.save(walk_path)
        elif os.path.exists(walk_path):
            os.remove(walk_path)
        built[key] = (strip, stand, walk)
        frame_w = UNITS[key].get("frame", (FRAME, FRAME))[0]
        print("%-13s attack %d frames  stand %dx%d" % (key, strip.width // frame_w, stand.width, stand.height))
    preview(built, os.path.join(ROOT, "docs", "images", "bonus-units.png"))


if __name__ == "__main__":
    main()
