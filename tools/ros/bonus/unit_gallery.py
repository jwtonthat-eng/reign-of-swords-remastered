#!/usr/bin/env python3
"""One picture of every unit the game currently offers: docs/images/all-units.png.

Each unit's standing sprite (public/games/reign-of-swords/sprites/stand/<sprite>.png) at twice its size, in the
player's colours (the two key ramps the engine re-palettes per army, here azure and gold), with its name and its
deployment cost. Units hidden for now (BONUS_HIDDEN in src/reign-of-swords/data/bonus-units.js) are left out.

    python3 tools/ros/bonus/unit_gallery.py

It asks node for the unit tables, so it needs no list of its own.
"""
import json
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
SPRITES = os.path.join(ROOT, "public", "games", "reign-of-swords", "sprites", "stand")
OUT = os.path.join(ROOT, "docs", "images", "all-units.png")
DATA = os.path.join(ROOT, "src", "reign-of-swords", "data")
QUERY = """
import { UNIT_TYPES, DEPLOY_COST, UNIT_KEY_PRIMARY, UNIT_KEY_SECONDARY, UNIT_RAMPS } from "%(data)s/game-data.js";
import { BONUS_HIDDEN } from "%(data)s/bonus-units.js";
const units = Object.entries(UNIT_TYPES)
  .filter(([key]) => !BONUS_HIDDEN.includes(key))
  .map(([key, T]) => ({ key, name: T.name, sprite: T.sprite, bonus: !!T.bonus, summoned: !!T.summoned, cost: DEPLOY_COST[key] || 0 }));
console.log(JSON.stringify({ units, primary: UNIT_KEY_PRIMARY, secondary: UNIT_KEY_SECONDARY, ramps: UNIT_RAMPS }));
"""
CELL_W, CELL_H, COLUMNS, SCALE = 190, 228, 8, 2
GROUND, PANEL, INK, DIM = (58, 84, 58), (70, 100, 70), (245, 240, 220), (200, 205, 180)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf"


def font(size, bold=False):
    try:
        return ImageFont.truetype(FONT % ("-Bold" if bold else ""), size)
    except OSError:
        return ImageFont.load_default()


def rgb(value):
    return (value >> 16 & 255, value >> 8 & 255, value & 255)


def main():
    script = os.path.join(ROOT, ".unit-gallery-query.mjs")
    with open(script, "w") as handle:
        handle.write(QUERY % {"data": DATA})
    try:
        data = json.loads(subprocess.check_output(["node", script], cwd=ROOT))
    finally:
        os.remove(script)
    recolour = {rgb(key): rgb(shade) for key, shade in zip(data["primary"], data["ramps"]["azure"])}
    recolour.update({rgb(key): rgb(shade) for key, shade in zip(data["secondary"], data["ramps"]["or"])})
    summoned = lambda u: u["summoned"] or not u["cost"]  # the Druid's and the Primal Warden's forms, too
    sections = [
        ("The original units", [u for u in data["units"] if not u["bonus"] and not summoned(u)]),
        ("The bonus units", [u for u in data["units"] if u["bonus"] and not summoned(u)]),
        ("Summoned and shapeshifted (never deployed)", [u for u in data["units"] if summoned(u)]),
    ]
    title, head, label, small = font(34, True), font(24, True), font(15, True), font(13)
    rows = sum((len(units) + COLUMNS - 1) // COLUMNS for _, units in sections)
    width = COLUMNS * CELL_W + 40
    height = 90 + len(sections) * 56 + rows * CELL_H + 20
    sheet = Image.new("RGBA", (width, height), GROUND + (255,))
    draw = ImageDraw.Draw(sheet)
    total = sum(len(units) for _, units in sections)
    draw.text((20, 18), "Reign of Swords Remastered: every unit (%d)" % total, font=title, fill=INK)
    y = 80
    for name, units in sections:
        draw.text((20, y + 10), "%s (%d)" % (name, len(units)), font=head, fill=INK)
        y += 56
        for i, unit in enumerate(units):
            x0 = 20 + (i % COLUMNS) * CELL_W
            y0 = y + (i // COLUMNS) * CELL_H
            draw.rounded_rectangle((x0 + 4, y0 + 4, x0 + CELL_W - 4, y0 + CELL_H - 4), 10, fill=PANEL + (255,))
            sprite = Image.open(os.path.join(SPRITES, unit["sprite"] + ".png")).convert("RGBA")
            pixels = sprite.load()
            for py in range(sprite.height):
                for px in range(sprite.width):
                    r, g, b, a = pixels[px, py]
                    if a and (r, g, b) in recolour:
                        pixels[px, py] = recolour[(r, g, b)] + (a,)
            scale = min(SCALE, (CELL_W - 16) / sprite.width, (CELL_H - 62) / sprite.height)
            sprite = sprite.resize((max(1, round(sprite.width * scale)), max(1, round(sprite.height * scale))), Image.NEAREST)
            sheet.alpha_composite(sprite, (x0 + (CELL_W - sprite.width) // 2, y0 + CELL_H - 54 - sprite.height))
            text = unit["name"]
            draw.text((x0 + CELL_W / 2, y0 + CELL_H - 40), text, font=label, fill=INK, anchor="ma")
            form = "a Warden's shape" if unit["bonus"] else "a Druid's form"
            cost = "%d points" % unit["cost"] if unit["cost"] else "summoned" if unit["summoned"] else form
            draw.text((x0 + CELL_W / 2, y0 + CELL_H - 22), cost, font=small, fill=DIM, anchor="ma")
        y += ((len(units) + COLUMNS - 1) // COLUMNS) * CELL_H
    sheet.convert("RGB").save(OUT)
    print("wrote %s  %dx%d  %d units" % (os.path.relpath(OUT, ROOT), width, height, total))


if __name__ == "__main__":
    main()
