#!/usr/bin/env python3
"""Draw bonus maps as PNGs for a visual check:  python3 tools/ros/bonus/render_map.py <out-dir> [mapId ...]"""
import json
import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
DATA = os.path.join(ROOT, "public", "games", "reign-of-swords-2")
SIDE_COLOR = {"player": (60, 200, 80), "ally": (70, 140, 240), "enemy": (230, 60, 50)}


def main():
    out_dir = sys.argv[1]
    wanted = {int(a) for a in sys.argv[2:]}
    os.makedirs(out_dir, exist_ok=True)
    tileset = Image.open(os.path.join(DATA, "tileset.png")).convert("RGBA")
    for level in json.load(open(os.path.join(DATA, "bonus.json")))["levels"]:
        if wanted and level["mapId"] not in wanted:
            continue
        cols, rows = level["cols"], level["rows"]
        image = Image.new("RGBA", (cols * 40, rows * 40 + 15), (0, 0, 0, 255))
        for y in range(rows):  # top to bottom, so tall tiles overlap the row above
            for x in range(cols):
                tile = level["tiles"][y * cols + x]
                cell = tileset.crop((tile * 40, 0, tile * 40 + 40, 55))
                image.paste(cell, (x * 40, y * 40), cell)
        draw = ImageDraw.Draw(image)
        for x, y in level["deployZone"]:
            draw.rectangle((x * 40 + 2, y * 40 + 17, x * 40 + 37, y * 40 + 52), outline=(255, 230, 60, 255))
        side_of = {g["gi"]: g["side"] for g in level["groupOrder"]}
        for key, x, y, _, gi in level["player"] + level["allies"] + level["enemy"]:
            color = SIDE_COLOR[side_of[gi]]
            draw.ellipse((x * 40 + 8, y * 40 + 23, x * 40 + 31, y * 40 + 46), fill=color + (255,), outline=(0, 0, 0))
            draw.text((x * 40 + 11, y * 40 + 29), key[:3], fill=(0, 0, 0))
        for action in level["script"]["actions"][len(level["script"]["initial"]) :]:
            if action["op"] == 0:
                x, y = action["x"], action["y"]
                draw.rectangle((x * 40 + 9, y * 40 + 24, x * 40 + 30, y * 40 + 45), outline=(255, 120, 0, 255), width=2)
                draw.text((x * 40 + 11, y * 40 + 29), action["key"][:3], fill=(255, 255, 255))
        for gx, gy in level["script"]["goals"] + ((level["script"]["escort"] or {}).get("markers", [])):
            draw.rectangle((gx * 40 + 4, gy * 40 + 19, gx * 40 + 35, gy * 40 + 50), outline=(80, 255, 255, 255), width=2)
        path = os.path.join(out_dir, "%d.png" % level["mapId"])
        image.save(path)
        print(path)


if __name__ == "__main__":
    main()
