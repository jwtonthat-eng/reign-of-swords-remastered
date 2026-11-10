#!/usr/bin/env python3
"""The bonus units' sprites, cut from the supplied art sheet (tools/ros/bonus/art/bonus-units-sheet.jpg).

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
SHEET = os.path.join(ROOT, "tools", "ros", "bonus", "art", "bonus-units-sheet.jpg")
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
}


def cut(sheet, box):
    """One pose, its ground flood-filled to transparent from the cell's edges."""
    cell = sheet.crop(box).convert("RGBA")
    w, h = cell.size
    px = cell.load()
    near = lambda c: abs(c[0] - GROUND[0]) + abs(c[1] - GROUND[1]) + abs(c[2] - GROUND[2]) < 46
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
    return cell.crop(cell.getbbox())


def team_colours(image):
    """Blue and green cloth -> the key ramps (three flat shades each), so an army's heraldry recolours it."""
    px = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            ramp = BLUE if 0.57 < h < 0.72 and s > 0.42 and v > 0.2 else GREEN if 0.24 < h < 0.44 and s > 0.42 and v > 0.2 else None
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
    return team_colours(small) if team else small


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
    top, bottom = unit["rows"]
    poses = [cut(sheet, (x0, top, x1, bottom)) for x0, x1 in unit["cells"]]
    scale = unit["height"] / poses[unit["stand"]].height
    small = [scaled(p, scale, unit["team"]) for p in poses]
    stand = small[unit["stand"]]
    strip = Image.new("RGBA", (FRAME * len(unit["attack"]), FRAME), (0, 0, 0, 0))
    for i, n in enumerate(unit["attack"]):
        strip.alpha_composite(framed(small[n], FRAME, FRAME, 40), (i * FRAME, 0))
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
        row = Image.new("RGBA", (sum(p.width for p in parts) + 8 * (len(parts) + 1), FRAME + 14), (84, 122, 84, 255))
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
    sheet = Image.open(SHEET).convert("RGB")
    built = {}
    for key in UNITS:
        strip, stand, walk = build(sheet, key)
        strip.save(os.path.join(SPRITES, key + ".png"))
        stand.save(os.path.join(SPRITES, "stand", key + ".png"))
        walk_path = os.path.join(SPRITES, "walk", key + ".png")
        if walk:
            walk.save(walk_path)
        elif os.path.exists(walk_path):
            os.remove(walk_path)
        built[key] = (strip, stand, walk)
        print("%-13s attack %d frames  stand %dx%d" % (key, strip.width // FRAME, stand.width, stand.height))
    preview(built, os.path.join(ROOT, "docs", "images", "bonus-units.png"))


if __name__ == "__main__":
    main()
