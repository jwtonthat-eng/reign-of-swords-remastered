#!/usr/bin/env python3
"""The bonus units' sprites, remixed from the ORIGINAL unit art so they sit beside the original units.

Each bonus unit takes the attack strip, standing pose and walk cycle of an original unit and repaints it: its
team-colour ramps swapped, its other colours shifted (leather to wolf-fur, flesh to stone, a red mask to gold, purple
magic to lightning), and for the Pavisiers a planted pavise drawn in. The frame layout of each strip is its source
unit's, so data/bonus-units.js copies that unit's frame numbers (SOURCE below).

    python3 tools/ros/bonus/remix_units.py        # writes sprites/<key>.png, sprites/stand/, sprites/walk/
                                                  # and the preview docs/images/bonus-units.png

(draw_units.py drew the first, from-scratch versions and still draws the six ability icons.)
"""
import colorsys
import os

from PIL import Image, ImageDraw

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ART = os.path.join(ROOT, "public", "games", "reign-of-swords")
SPRITES = os.path.join(ART, "sprites")

# The two team-colour key ramps the engine re-palettes per army (data/game-data.js UNIT_KEY_PRIMARY / SECONDARY).
GREEN = [(0x00, 0xD4, 0x0B), (0x00, 0xA6, 0x06), (0x00, 0x78, 0x00)]
BLUE = [(0x00, 0x15, 0xFF), (0x00, 0x0B, 0xC6), (0x00, 0x00, 0x8C)]
SWAP = {**dict(zip(GREEN, BLUE)), **dict(zip(BLUE, GREEN))}
KEYS = set(GREEN) | set(BLUE)


def hsv(rgb):
    return colorsys.rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)


def rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h % 1, max(0, min(1, s)), max(0, min(1, v)))
    return (round(r * 255), round(g * 255), round(b * 255))


# ---- the repaint of each unit: rgb -> rgb for every opaque, non-key pixel -------------------------------------
def fur(c):  # Cragsmen: dark leather and cloth become grey wolf-fur; skin and wood are left alone
    h, s, v = hsv(c)
    if (h < 0.12 or h > 0.95) and s > 0.25 and v < 0.5:
        return rgb(0.08, s * 0.25, v * 1.45 + 0.08)
    return c


def warded(c):  # Spellwardens: steel becomes dark, blue-tempered plate (the pale sword-swoosh is left alone)
    h, s, v = hsv(c)
    if s < 0.14 and 0.2 < v < 0.86:
        return rgb(0.6, 0.32, v * 0.85)
    return c


def stone(c):  # Stone Sentinel: the Bodyguard's purple flesh becomes weathered rock, its eyes and blades rune-cyan
    h, s, v = hsv(c)
    if 0.68 < h < 0.98 and s > 0.12:
        return rgb(0.1, 0.1, v * 0.9)
    if s < 0.15 and v > 0.75:
        return rgb(0.5, 0.45, v)
    return c


def linen(c):  # Marines: the Musketeer's brown coat becomes sun-bleached linen, the hat's plume a red bandana
    h, s, v = hsv(c)
    if 0.04 < h < 0.12 and s > 0.3 and v < 0.62:
        return rgb(0.1, s * 0.3, v * 1.5 + 0.1)
    return c


def plate(c):  # Pavisiers: the Crossbowman's jerkin becomes a steel breastplate
    h, s, v = hsv(c)
    if (h < 0.1 or h > 0.95) and s > 0.3 and 0.2 < v < 0.6:
        return rgb(0.6, 0.1, v * 1.35 + 0.08)
    return c


def gilded(c):  # Battlemage: the Wizard's red face becomes a golden war-mask, its purple magic white-blue lightning
    h, s, v = hsv(c)
    if (h < 0.06 or h > 0.94) and s > 0.45:
        return rgb(0.125, 0.7, v * 1.2 + 0.1)
    if 0.66 < h < 0.94 and s > 0.1:
        return rgb(0.54, s * 0.55, v * 1.15 + 0.05)
    return c


# key: (source unit, repaint, swap the team ramps, attack frames taken from the source strip or None for all)
UNITS = {
    "cragsmen": ("militiamen", fur, True, None),
    "spellwardens": ("swordsmen", warded, True, None),
    "sentinel": ("bodyguard", stone, False, None),
    "marines": ("musketeers", linen, True, [6, 4, 4, 5, 6]),  # the Musketeer's sword frames only
    "pavisiers": ("crossbowmen", plate, False, None),
    "battlemage": ("wizards", gilded, True, None),
}
FRAME = {"militiamen": 88, "swordsmen": 88, "bodyguard": 72, "musketeers": 88, "crossbowmen": 88, "wizards": 88}


def repaint(image, paint, swap):
    image = image.convert("RGBA")
    px = image.load()
    cache = {}
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            c = (r, g, b)
            if c in KEYS:
                if swap:
                    px[x, y] = SWAP[c] + (a,)
                continue
            if c not in cache:
                out = paint(c)
                cache[c] = (1, 1, 1) if out in KEYS else out  # a repaint never lands on a key colour by accident
            px[x, y] = cache[c] + (a,)
    return image


# The planted pavise: a tall shield in the army's two colours, standing on the ground in front of the Pavisiers.
def pavise(image, left, bottom, height=30, width=13):
    draw = ImageDraw.Draw(image)
    top = bottom - height
    dark, wood, edge = (40, 28, 20, 255), (124, 86, 48, 255), (176, 132, 78, 255)
    draw.rectangle((left, top + 2, left + width, bottom), fill=dark)
    draw.rectangle((left + 1, top + 1, left + width - 1, top + 2), fill=dark)
    draw.rectangle((left + 1, top + 3, left + width - 1, bottom - 1), fill=wood)
    draw.line((left + 1, top + 3, left + 1, bottom - 1), fill=edge)
    draw.rectangle((left + 3, top + 5, left + width - 3, bottom - 3), fill=GREEN[1] + (255,))
    draw.line((left + 3, top + 5, left + 3, bottom - 3), fill=GREEN[0] + (255,))
    draw.line((left + width - 3, top + 5, left + width - 3, bottom - 3), fill=GREEN[2] + (255,))
    mid = left + width // 2
    draw.rectangle((mid - 1, top + 5, mid + 1, bottom - 3), fill=BLUE[1] + (255,))
    draw.line((mid + 1, top + 5, mid + 1, bottom - 3), fill=BLUE[2] + (255,))
    draw.rectangle((left + 3, top + height // 2 - 1, left + width - 3, top + height // 2 + 1), fill=BLUE[1] + (255,))
    draw.point((mid, top + height // 2), fill=(232, 200, 90, 255))


def feet(frame):  # the lowest opaque row and the rightmost opaque column of a frame's lower third
    box = frame.getbbox()
    return box[3] if box else frame.height


def build(key):
    source, paint, swap, pick = UNITS[key]
    size = FRAME[source]
    strip = repaint(Image.open(os.path.join(SPRITES, source + ".png")), paint, swap)
    frames = [strip.crop((i * size, 0, (i + 1) * size, size)) for i in range(strip.width // size)]
    if pick:
        frames = [frames[i] for i in pick]
    stand = repaint(Image.open(os.path.join(SPRITES, "stand", source + ".png")), paint, swap)
    walk_path = os.path.join(SPRITES, "walk", source + ".png")  # the Wizard has no walk cycle: it glides
    walk = repaint(Image.open(walk_path), paint, swap) if os.path.exists(walk_path) else None
    if key == "marines":  # the Musketeer stands and walks with its musket: the Marine stands as its sword guard frame
        stand = frames[0].crop(frames[0].getbbox())
    if key == "pavisiers":
        for frame in frames:
            box = frame.getbbox()
            pavise(frame, min(size - 15, box[0] + (box[2] - box[0]) // 2 + 9), feet(frame) - 1)
        wide = Image.new("RGBA", (stand.width + 12, stand.height), (0, 0, 0, 0))
        wide.paste(stand, (0, 0))
        pavise(wide, wide.width - 15, wide.height - 1)
        stand = wide
    out = Image.new("RGBA", (size * len(frames), size), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        out.paste(frame, (i * size, 0))
    return out, stand, walk


def preview(built, path):
    scale, pad = 2, 8
    rows = []
    for key, (strip, stand, walk) in built.items():
        width = stand.width + (walk.width if walk else 0) + strip.width + pad * 4
        row = Image.new("RGBA", (width, max(strip.height, stand.height) + 14), (84, 122, 84, 255))
        ImageDraw.Draw(row).text((4, 0), "%s (from %s)" % (key, UNITS[key][0]), fill=(255, 255, 255, 255))
        x = pad
        for image in (stand, walk, strip):
            if image is None:
                continue
            row.alpha_composite(image, (x, row.height - image.height))
            x += image.width + pad
        rows.append(row)
    sheet = Image.new("RGBA", (max(r.width for r in rows), sum(r.height for r in rows)), (84, 122, 84, 255))
    y = 0
    for row in rows:
        sheet.alpha_composite(row, (0, y))
        y += row.height
    sheet = sheet.resize((sheet.width * scale, sheet.height * scale), Image.NEAREST)
    sheet.save(path)


def main():
    built = {}
    for key in UNITS:
        strip, stand, walk = build(key)
        strip.save(os.path.join(SPRITES, key + ".png"))
        stand.save(os.path.join(SPRITES, "stand", key + ".png"))
        walk_out = os.path.join(SPRITES, "walk", key + ".png")
        if walk:
            walk.save(walk_out)
        elif os.path.exists(walk_out):
            os.remove(walk_out)
        built[key] = (strip, stand, walk)
        print("%-13s from %-12s %d frames of %dpx" % (key, UNITS[key][0], strip.width // strip.height, strip.height))
    preview(built, os.path.join(ROOT, "docs", "images", "bonus-units.png"))


if __name__ == "__main__":
    main()
