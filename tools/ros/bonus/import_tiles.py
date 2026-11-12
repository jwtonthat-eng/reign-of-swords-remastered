#!/usr/bin/env python3
"""The BONUS terrain tiles (ours — MECHANICS.md §13): nineteen kinds of ground for the bonus campaigns, added after the
260 tiles of Episode II's own set.

Fourteen are cut from the two supplied sheets (tools/ros/bonus/art/terrain-tiles-sheet*.jpg). The sheets draw each tile
as an isometric block; the game's tiles are seen from above, 40 px wide, with 15 px of headroom over the 40 px of
ground for whatever stands on it. So the top face of each block (a rhombus) is squared up into the ground, and what
rises from it (a monolith, bamboo, obsidian) is cut out upright and stood back on top. Five tiles came without art
(Vent Grate, Thermal Chimney, Mirage Sand, Sacrificial Altar Steps, Overgrown Jungle Ruins) and are drawn here from the
game's own tiles; so are the two a tile turns into (ash, cleared ruins).

It rewrites, each time from the first 260 tiles so it can be run again:

    tileset.png          the strip, 260 + the new cells
    terrain.json         the per-tile legend
    movement.json        types[] per tile, and a row / defence / heal for each new terrain type (30-48)
    terrain-types.json   the same types[]
    structures.json      the Jungle Ruins' two stages (they fall to any weapon)
    docs/images/bonus-tiles.png   a preview

    python3 tools/ros/bonus/import_tiles.py

The rules of each tile are in src/reign-of-swords/rules/tiles.js; build_bonus.py lays them by letter.
"""
import json
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ART = os.path.join(ROOT, "tools", "ros", "bonus", "art")
DATA = os.path.join(ROOT, "public", "games", "reign-of-swords-2")
BASE_TILES = 260  # Episode II's own
W, H, TOP = 40, 55, 15  # a cell, and the headroom over its ground
SHEET_BG = (45, 62, 50)

# kind -> terrain type, the name the terrain card shows, the move cost per class [fly, skirmish, formation, cavalry,
# war engine] (100 = cannot enter), the damage taken there in % (100 = no cover), HP healed a turn, and the legend
# category the minimap colours by
KINDS = {
    "conveyor": (30, "Conveyor belt", [1, 1, 1, 1, 1], 100, 0, "road"),
    "vent": (31, "Vent grate", [1, 1, 1, 1, 1], 100, 0, "road"),
    "muck": (32, "Abyssal muck", [1, 2, 2, 2, 3], 100, 0, "grass"),
    "chimney": (33, "Thermal chimney", [1, 2, 2, 3, 100], 100, 0, "hill"),
    "tar": (34, "Tar pit", [1, 2, 2, 100, 100], 110, 0, "grass"),
    "fern": (35, "Giant fern canopy", [1, 2, 2, 3, 100], 90, 0, "forest"),
    "ice": (36, "Black ice", [1, 1, 1, 1, 1], 100, 0, "road"),
    "monolith": (37, "Runic monolith", [1, 100, 100, 100, 100], 100, 0, "wall"),
    "sinkhole": (38, "Quicksand sinkhole", [1, 1, 1, 1, 1], 100, 0, "grass"),
    "mirage": (39, "Mirage sand", [1, 1, 1, 1, 1], 100, 0, "grass"),
    "altar": (40, "Sacrificial altar steps", [1, 1, 1, 2, 100], 100, 0, "road"),
    "ruins": (41, "Overgrown jungle ruins", [1, 100, 100, 100, 100], 100, 0, "wall"),
    "coral": (42, "Razor coral", [1, 2, 3, 3, 100], 120, 0, "water"),
    "cenote": (43, "Cenote", [1, 2, 2, 2, 100], 100, 0, "water"),
    "glyph": (44, "Astral glyph", [1, 1, 1, 1, 1], 100, 0, "road"),
    "chinampa": (45, "Chinampa", [1, 2, 2, 2, 100], 100, 10, "village"),
    "obsidian": (46, "Obsidian spikes", [1, 2, 2, 3, 100], 100, 0, "hill"),
    "bamboo": (47, "Bamboo thicket", [1, 2, 2, 100, 100], 100, 0, "forest"),
    "zen": (48, "Zen sand garden", [1, 1, 1, 1, 1], 100, 0, "road"),
}
# The new tiles in order (tile id = 260 + index): (key, kind or an original terrain type, the name if it differs).
TILES = [
    ("conveyor_n", "conveyor"),
    ("conveyor_e", "conveyor"),
    ("conveyor_s", "conveyor"),
    ("conveyor_w", "conveyor"),
    ("vent", "vent"),
    ("muck", "muck"),
    ("chimney", "chimney"),
    ("tar", "tar"),
    ("fern", "fern"),
    ("ice", "ice"),
    ("monolith", "monolith"),
    ("sinkhole", "sinkhole"),
    ("mirage", "mirage"),
    ("altar", "altar"),
    ("ruins", "ruins"),
    ("ruins_broken", "ruins"),
    ("coral", "coral"),
    ("cenote", "cenote"),
    ("glyph", "glyph"),
    ("chinampa", "chinampa"),
    ("obsidian", "obsidian"),
    ("bamboo", "bamboo"),
    ("ash", 2),  # what burnt bamboo leaves: open ground
    ("zen", "zen"),
    ("ruins_cleared", 15),  # what the ruins fall to: rubble
]
TILE_ID = {key: BASE_TILES + i for i, (key, _) in enumerate(TILES)}


def sheet(name):
    return Image.open(os.path.join(ART, name)).convert("RGB")


def top_face(src, cx, top, width, size=W, ss=4):
    """The block's top face — a rhombus `width` wide whose upper corner is (cx, top) — squared up, seen from above."""
    h = width / 2
    quad = (cx, top, cx - width / 2, top + h / 2, cx, top + h, cx + width / 2, top + h / 2)  # UL, LL, LR, UR
    big = src.transform((size * ss, size * ss), Image.QUAD, quad, Image.BICUBIC)
    return big.resize((size, size), Image.LANCZOS).convert("RGBA")


def cell(ground):
    """A 40 x 55 cell with `ground` (40 x 40) under 15 px of clear headroom."""
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.alpha_composite(ground.convert("RGBA"), (0, TOP))
    return out


def near(c, ref, tol):
    return abs(c[0] - ref[0]) + abs(c[1] - ref[1]) + abs(c[2] - ref[2]) < tol


def upright(src, box, keep, width, feather=0):
    """What stands on a block: the pixels of `box` that `keep` accepts, scaled to `width` px across."""
    crop = src.crop(box).convert("RGBA")
    px = crop.load()
    for y in range(crop.height):
        for x in range(crop.width):
            r, g, b, _ = px[x, y]
            if not keep((r, g, b), x, y, crop.width, crop.height):
                px[x, y] = (0, 0, 0, 0)
    bbox = crop.getbbox()
    crop = crop.crop(bbox)
    scale = width / crop.width
    small = crop.resize((max(1, round(crop.width * scale)), max(1, round(crop.height * scale))), Image.LANCZOS)
    px = small.load()
    for y in range(small.height):
        for x in range(small.width):
            r, g, b, a = px[x, y]
            fade = 255
            if feather and y >= small.height - feather:
                fade = round(255 * (small.height - y) / (feather + 1))
            px[x, y] = (r, g, b, min(fade, 255 if a >= 110 else 0))
    return small


def stand(tile, obj, bottom=H - 4, dx=0):
    tile.alpha_composite(obj, ((W - obj.width) // 2 + dx, max(0, bottom - obj.height)))
    return tile


def original(tileset, tile_id):
    return tileset.crop((tile_id * W, 0, tile_id * W + W, H)).convert("RGBA")


def ground_of(tileset, tile_id):
    return original(tileset, tile_id).crop((0, TOP, W, H))


def tinted(image, mul, add=(0, 0, 0)):
    px = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = px[x, y]
            px[x, y] = tuple(max(0, min(255, round(c * m + d))) for c, m, d in zip((r, g, b), mul, add)) + (a,)
    return image


def painted(draw_fn, ss=4):
    """A cell drawn at `ss` times its size and scaled down (soft edges)."""
    big = Image.new("RGBA", (W * ss, H * ss), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(big, "RGBA"), ss)
    return big.resize((W, H), Image.LANCZOS)


# ---------------------------------------------------------------- the tiles
def build_all(tileset):
    s1, s2 = sheet("terrain-tiles-sheet.jpg"), sheet("terrain-tiles-sheet-2.jpg")
    grass, sand, paving = ground_of(tileset, 63), ground_of(tileset, 133), ground_of(tileset, 66)
    rng = random.Random(5010)
    out = {}

    # CONVEYOR BELT: the belt's face runs north; paving shows where the art is the sheet's own ground. An arrow of
    # brass chevrons says which way it carries; the other three directions are quarter turns.
    belt = top_face(s1, 347, 255, 560)
    ground = paving.copy()
    px, gx = belt.load(), ground.load()
    for y in range(W):
        for x in range(W):
            if not near(px[x, y], SHEET_BG, 26):
                gx[x, y] = px[x, y]
    draw = ImageDraw.Draw(ground, "RGBA")
    for cy in (8, 20, 32):
        draw.line([(15, cy + 4), (20, cy - 1), (25, cy + 4)], fill=(250, 214, 110, 235), width=2)
    for turn, name in enumerate(("conveyor_n", "conveyor_w", "conveyor_s", "conveyor_e")):
        out[name] = cell(ground.rotate(90 * turn))

    # VENT GRATE (no art): an iron grating let into paving, and the steam that hides whatever is beyond it.
    def vent(d, s):
        d.rectangle([5 * s, (TOP + 6) * s, 35 * s, (TOP + 34) * s], fill=(38, 40, 46, 255), outline=(96, 98, 104, 255), width=s)
        for i in range(6):
            x = (8 + i * 5) * s
            d.line([(x, (TOP + 8) * s), (x, (TOP + 32) * s)], fill=(120, 124, 132, 255), width=s)
        for y in (13, 20, 27):
            d.line([(6 * s, (TOP + y) * s), (34 * s, (TOP + y) * s)], fill=(74, 76, 84, 255), width=s)
        for cx, cy, r, a in ((14, 24, 9, 150), (25, 19, 10, 165), (19, 11, 9, 140), (27, 7, 7, 105), (12, 6, 6, 90)):
            d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=(244, 246, 248, a))

    out["vent"] = cell(paving)
    out["vent"].alpha_composite(painted(vent))

    out["muck"] = cell(top_face(s1, 1032, 244, 642))

    # THERMAL CHIMNEY (no art): a rock vent on dark sea-bed, and the black water it throws up.
    seabed = tinted(top_face(s1, 1719, 244, 642), (0.55, 0.6, 0.75), (10, 16, 30))

    def chimney(d, s):
        d.polygon([(8 * s, 50 * s), (15 * s, 22 * s), (25 * s, 22 * s), (33 * s, 50 * s)], fill=(74, 66, 62, 255))
        d.polygon([(8 * s, 50 * s), (15 * s, 22 * s), (19 * s, 22 * s), (17 * s, 50 * s)], fill=(104, 94, 86, 255))
        d.polygon([(25 * s, 22 * s), (33 * s, 50 * s), (27 * s, 50 * s), (22 * s, 22 * s)], fill=(48, 43, 42, 255))
        d.ellipse([15 * s, 19 * s, 25 * s, 25 * s], fill=(20, 16, 18, 255), outline=(200, 96, 40, 255), width=s)
        for cx, cy, r, a in ((20, 15, 6, 210), (17, 9, 6, 180), (24, 6, 5, 150), (19, 3, 4, 110)):
            d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=(18, 18, 24, a))

    out["chimney"] = cell(seabed)
    out["chimney"].alpha_composite(painted(chimney))

    out["tar"] = cell(top_face(s1, 1719, 244, 642))

    # GIANT FERN CANOPY: the fronds from above, and the tops of them standing over the tile.
    out["fern"] = cell(top_face(s1, 2406, 244, 645))
    fronds = upright(s1, (2084, 150, 2729, 430), lambda c, x, y, w, h: not near(c, SHEET_BG, 46), 44, feather=6)
    stand(out["fern"], fronds, bottom=TOP + 14)

    out["ice"] = cell(top_face(s1, 343, 988, 644))

    # RUNIC MONOLITH: the snow from above (the stone's own smear painted out), the stone stood back up on it.
    snow = Image.new("RGBA", (W, W), (236, 242, 252, 255))
    d = ImageDraw.Draw(snow, "RGBA")
    for _ in range(70):
        x, y = rng.randint(0, W - 1), rng.randint(0, W - 1)
        d.line([(x, y), (x + rng.randint(1, 4), y)], fill=rng.choice([(255, 255, 255, 255), (208, 222, 244, 255), (190, 208, 236, 255)]))
    d.ellipse([7, 24, 33, 38], fill=(150, 176, 216, 120))  # the stone's shadow, and its glow on the snow
    out["monolith"] = cell(snow)

    def is_stone(c, x, y, w, h):
        grey = max(c) - min(c) < 46 and 64 < max(c) < 200
        rune = c[2] > 180 and c[1] > 140 and c[0] < 170
        cap = min(c) > 205 and y < h * 0.45
        return (grey or rune or cap) and abs(x - w / 2) < w * 0.46

    stone = upright(s1, (930, 815, 1140, 1250), is_stone, 24)
    stand(out["monolith"], stone, bottom=H - 4)

    out["sinkhole"] = cell(top_face(s1, 1718, 997, 643))

    # MIRAGE SAND (no art): the desert's own sand under a shimmer of heat and the pale blue of water that is not there.
    def mirage(d, s):
        for i, y in enumerate((20, 26, 31, 37, 43, 49)):
            pts = [((x * 2) * s, (y + 1.6 * math.sin(x * 0.9 + i * 1.7)) * s) for x in range(21)]
            d.line(pts, fill=(170, 226, 244, 150 if i % 2 else 105), width=s + (i % 2))
        d.ellipse([9 * s, 27 * s, 31 * s, 40 * s], fill=(150, 214, 240, 70))

    out["mirage"] = cell(tinted(sand.copy(), (1.04, 1.02, 0.96), (6, 6, 4)))
    out["mirage"].alpha_composite(painted(mirage))

    # SACRIFICIAL ALTAR STEPS (no art): three stone steps seen from above, crimson running in the grooves.
    def altar(d, s):
        for inset, shade in ((0, (118, 108, 98)), (6, (146, 134, 120)), (12, (176, 162, 144))):
            box = [inset * s, (TOP + inset) * s, (W - inset) * s - 1, (H - inset) * s - 1]
            d.rectangle(box, fill=shade + (255,), outline=(70, 62, 58, 255), width=s)
        for x in (10, 20, 30):
            d.line([(x * s, TOP * s), (x * s, (TOP + 12) * s)], fill=(190, 30, 34, 255), width=s)
            d.line([(x * s, (H - 12) * s), (x * s, H * s)], fill=(190, 30, 34, 255), width=s)
        for y in (TOP + 10, TOP + 20, TOP + 30):
            d.line([(0, y * s), (12 * s, y * s)], fill=(190, 30, 34, 255), width=s)
            d.line([((W - 12) * s, y * s), (W * s, y * s)], fill=(190, 30, 34, 255), width=s)
        d.rectangle([15 * s, (TOP + 15) * s, 25 * s, (TOP + 25) * s], fill=(120, 24, 30, 255), outline=(230, 60, 50, 255), width=s)

    out["altar"] = painted(altar)

    # OVERGROWN JUNGLE RUINS (no art): the game's own broken towers on grass, choked with vines; and what is left
    # when they are cleared.
    def vines(tile, seed, count):
        vr = random.Random(seed)
        d = ImageDraw.Draw(tile, "RGBA")
        solid = tile.copy().load()
        for _ in range(count):
            x, y = vr.randint(4, 35), vr.randint(8, 30)
            for _ in range(vr.randint(8, 16)):
                if not (0 <= x < W and 0 <= y < H) or not solid[x, y][3]:
                    break
                d.point((x, y), fill=vr.choice([(44, 120, 40, 255), (66, 150, 52, 255), (30, 92, 34, 255)]))
                if vr.random() < 0.3:
                    d.point((x + vr.choice((-1, 1)), y), fill=(96, 176, 70, 255))
                x += vr.choice((-1, 0, 0, 1))
                y += 1
        return tile

    for name, source, count in (("ruins", 35, 26), ("ruins_broken", 34, 18)):
        tile = cell(grass)
        tile.alpha_composite(vines(original(tileset, source), source, count))
        out[name] = tile
    cleared = cell(grass)
    d = ImageDraw.Draw(cleared, "RGBA")
    for _ in range(16):
        x, y, r = rng.randint(3, 34), rng.randint(TOP + 4, H - 6), rng.randint(1, 3)
        shade = rng.choice([(150, 146, 140), (118, 114, 110), (176, 172, 164)])
        d.ellipse([x, y, x + r + 1, y + r], fill=shade + (255,), outline=(70, 68, 66, 255))
    for _ in range(10):
        x, y = rng.randint(2, 36), rng.randint(TOP + 2, H - 4)
        d.line([(x, y), (x + rng.randint(-2, 2), y + 3)], fill=(40, 110, 40, 255))
    out["ruins_cleared"] = cleared

    out["coral"] = cell(top_face(s1, 2405, 988, 642))
    out["cenote"] = cell(top_face(s2, 414, 300, 687))
    out["glyph"] = cell(top_face(s2, 1261, 271, 733))
    out["chinampa"] = cell(top_face(s2, 2104, 241, 779))

    # OBSIDIAN SPIKES: the dark ground from above, the glass standing on it.
    out["obsidian"] = cell(top_face(s2, 417, 1093, 701))
    glass = upright(
        s2,
        (120, 965, 715, 1400),
        lambda c, x, y, w, h: not near(c, SHEET_BG, 40) and c[0] < c[2] + 10 and (max(c) < 150 or min(c) > 170),
        38,
    )
    stand(out["obsidian"], glass, bottom=H - 5)

    # BAMBOO THICKET: its floor from above, the canes standing over it; and the ash it burns to.
    out["bamboo"] = cell(top_face(s2, 1264, 1081, 719))
    canes = upright(s2, (1075, 905, 1455, 1345), lambda c, x, y, w, h: not near(c, SHEET_BG, 46), 40, feather=6)
    stand(out["bamboo"], canes, bottom=H - 3)
    ash = cell(tinted(grass.copy(), (0.36, 0.3, 0.52), (52, 50, 46)))
    d = ImageDraw.Draw(ash, "RGBA")
    for _ in range(9):
        x, y = rng.randint(4, 35), rng.randint(TOP + 4, H - 6)
        d.line([(x, y), (x, y - rng.randint(2, 5))], fill=(24, 22, 20, 255), width=1)
        d.point((x, y - 6), fill=(240, 130, 40, 200))
    out["ash"] = ash

    out["zen"] = cell(top_face(s2, 2121, 1088, 754))
    return out


# ---------------------------------------------------------------- the tables
def write_json(path, data, compact=True):
    """As the file was written by the exporters: one line, no newline at its end."""
    with open(path, "w") as f:
        json.dump(data, f, separators=(",", ":") if compact else None)


def main():
    strip_path = os.path.join(DATA, "tileset.png")
    tileset = Image.open(strip_path).convert("RGBA").crop((0, 0, BASE_TILES * W, H))
    tiles = build_all(tileset)
    strip = Image.new("RGBA", ((BASE_TILES + len(TILES)) * W, H), (0, 0, 0, 0))
    strip.alpha_composite(tileset)
    for i, (key, _) in enumerate(TILES):
        strip.alpha_composite(tiles[key], ((BASE_TILES + i) * W, 0))
    strip.save(strip_path)

    types_of = [KINDS[kind][0] if kind in KINDS else kind for _, kind in TILES]

    movement_path = os.path.join(DATA, "movement.json")
    movement = json.load(open(movement_path))
    movement["types"] = movement["types"][:BASE_TILES] + types_of
    for field in ("rows", "def", "heal"):
        movement[field] = movement[field][:30]
    for _, (number, _, row, defence, heal, _) in sorted(KINDS.items(), key=lambda kv: kv[1][0]):
        assert number == len(movement["rows"])
        movement["rows"].append(row)
        movement["def"].append(defence)
        movement["heal"].append(heal)
    # the names of the bonus terrain types (30+), for the terrain card (rules/terrain.js)
    movement["names"] = {str(v[0]): v[1] for v in KINDS.values()}
    movement["tileNames"] = {str(TILE_ID["ash"]): "Ash", str(TILE_ID["ruins_cleared"]): "Cleared ruins"}
    write_json(movement_path, movement)

    types_path = os.path.join(DATA, "terrain-types.json")
    terrain_types = json.load(open(types_path))
    terrain_types["types"] = terrain_types["types"][:BASE_TILES] + types_of
    write_json(types_path, terrain_types)

    terrain_path = os.path.join(DATA, "terrain.json")
    terrain = json.load(open(terrain_path))
    terrain["props"] = {k: v for k, v in terrain["props"].items() if int(k) < BASE_TILES}
    for i, (key, kind) in enumerate(TILES):
        if kind in KINDS:
            _, _, row, defence, heal, category = KINDS[kind]
        else:
            row, defence, heal, category = movement["rows"][kind], movement["def"][kind], 0, "grass" if kind == 2 else "rubble"
        terrain["props"][str(BASE_TILES + i)] = {
            "category": category,
            "passable": row[1] < 90,
            "movecost": 1 if row[1] >= 90 else row[1],
            "defBonus": round((100 - defence) / 100, 2),
            "blocksMounted": row[3] >= 90,
            "blocksEngine": row[4] >= 90,
            "heal": heal,
        }
    terrain["count"] = BASE_TILES + len(TILES)
    write_json(terrain_path, terrain, compact=False)

    # The Jungle Ruins are a structure of two stages that falls to rubble; `soft` is the least any weapon does to them
    # (vines and loose stone give way to a sword as they do to a catapult).
    structures_path = os.path.join(DATA, "structures.json")
    structures = json.load(open(structures_path))
    for field in ("armor", "trans", "pre", "rubble"):
        structures[field] = {k: v for k, v in structures[field].items() if int(k) < BASE_TILES}
    ruins, broken, cleared = TILE_ID["ruins"], TILE_ID["ruins_broken"], TILE_ID["ruins_cleared"]
    structures["armor"].update({str(ruins): 14, str(broken): 14})
    structures["trans"].update({str(ruins): broken, str(broken): cleared})
    structures["pre"].update({str(broken): ruins, str(cleared): broken})
    structures["rubble"][str(cleared)] = {"def": movement["def"][15], "mv": movement["rows"][15], "heal": 0}
    structures["soft"] = {str(ruins): 30, str(broken): 30}
    write_json(structures_path, structures)

    # a preview, 4x, with each tile's letter-key under it
    scale, cols = 4, 9
    rows = math.ceil(len(TILES) / cols)
    sheet_out = Image.new("RGBA", (cols * (W * scale + 12) + 12, rows * (H * scale + 30) + 12), (38, 52, 42, 255))
    draw = ImageDraw.Draw(sheet_out)
    for i, (key, _) in enumerate(TILES):
        x = 12 + (i % cols) * (W * scale + 12)
        y = 12 + (i // cols) * (H * scale + 30)
        sheet_out.alpha_composite(tiles[key].resize((W * scale, H * scale), Image.NEAREST), (x, y))
        draw.text((x, y + H * scale + 4), "%d %s" % (BASE_TILES + i, key), fill=(255, 255, 255, 255))
    sheet_out.save(os.path.join(ROOT, "docs", "images", "bonus-tiles.png"))
    print("wrote %d tiles (%d-%d), terrain types 30-%d" % (len(TILES), BASE_TILES, BASE_TILES + len(TILES) - 1, 29 + len(KINDS)))


if __name__ == "__main__":
    main()
