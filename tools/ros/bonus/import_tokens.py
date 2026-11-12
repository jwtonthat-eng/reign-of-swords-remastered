#!/usr/bin/env python3
"""The eight campaign upgrade tokens, cut from the two supplied sheets (tools/ros/bonus/art/campaign-tokens-sheet*.jpg) into
52 px icons beside the game's own six collectibles (public/games/reign-of-swords/icons/).

    python3 tools/ros/bonus/import_tokens.py
"""
import os
from collections import deque

from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ART = os.path.join(ROOT, "tools", "ros", "bonus", "art")
ICONS = os.path.join(ROOT, "public", "games", "reign-of-swords", "icons")
# sheet -> name -> the box of its drawing on that sheet
TOKENS = {
    "campaign-tokens-sheet.jpg": {
        "bloodstone": (110, 540, 590, 1340),
        "scarab": (640, 650, 1200, 1250),
        "obsidian": (1250, 500, 1740, 1380),
        "whalebone": (1820, 540, 2320, 1290),
    },
    "campaign-tokens-sheet-2.jpg": {
        "anchor": (470, 180, 930, 690),
        "tsuba": (1820, 190, 2320, 690),
        "jade": (490, 880, 950, 1360),
        "void": (1850, 870, 2290, 1350),
    },
}


def cut(sheet, box):
    cell = sheet.crop(box).convert("RGBA")
    w, h = cell.size
    px = cell.load()
    ground = px[2, 2][:3]
    near = lambda c: abs(c[0] - ground[0]) + abs(c[1] - ground[1]) + abs(c[2] - ground[2]) < 40
    seen = [[False] * w for _ in range(h)]
    queue = deque([(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)])
    while queue:
        x, y = queue.popleft()
        if not (0 <= x < w and 0 <= y < h) or seen[y][x]:
            continue
        seen[y][x] = True
        if not near(px[x, y]):
            continue
        px[x, y] = (0, 0, 0, 0)
        queue.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return cell.crop(cell.getbbox())


def main():
    for file, tokens in TOKENS.items():
        sheet = Image.open(os.path.join(ART, file)).convert("RGB")
        for name, box in tokens.items():
            art = cut(sheet, box)
            scale = 48 / max(art.size)
            art = art.resize((max(1, round(art.width * scale)), max(1, round(art.height * scale))), Image.LANCZOS)
            icon = Image.new("RGBA", (52, 52), (0, 0, 0, 0))
            icon.alpha_composite(art, ((52 - art.width) // 2, (52 - art.height) // 2))
            icon.save(os.path.join(ICONS, name + ".png"))
            print("wrote icons/%s.png" % name)


if __name__ == "__main__":
    main()
