#!/usr/bin/env python3
"""Lay out the Episode II campaign map's markers so that no name, dot or raid pip overlaps another or leaves the map.

A marker is a dot centred on its position with its name under it and its raid pips under that (or both over it:
`up`). Names are a fixed size in pixels while the map shrinks with the window, so the layout has to hold on the
smallest map as well as the largest. This script takes the measured size of every marker's parts at several window
sizes (a JSON file: {size: {w, h, marks: {id: {dot: [w, h], label: [w, h], raids: [w, h] | null}}}}, written by a
browser run over the campaign screen with every region open) and searches for positions, in percent of the map, that
keep every part clear of every other at every one of those sizes, as near as it can to where each region lies on the
painted map (WANT below: the dot's place). It prints the KINGDOM_POS_EP2 table for data/shell-data.js.

    python3 tools/ros/map_labels.py sizes.json [seed [positions.txt]]

Give it sizes across the whole range, not only the smallest map: two names that pass each other on a small map (one
hanging under its dot, the other standing over the dot below) run into each other as the map grows. With a third
argument it starts from a table it printed earlier and only repairs it.
"""
import json
import math
import random
import re
import sys

# where each region's dot belongs on the painted map (percent of the map: left, top), and how hard to hold it there:
# the original kingdoms sit on the names the map prints, the bonus regions on a stretch of land or sea
WANT = {
    "hunewold": (29.4, 8.3, 4), "rukiev": (63.6, 10.4, 4), "sangsoleil": (11.8, 30.0, 4), "carrone": (46.0, 33.4, 4),
    "merovin": (26.6, 39.2, 4), "bordavia": (58.9, 42.1, 4), "marsur": (40.0, 52.0, 4), "aguilleon": (23.3, 75.5, 4),
    "zayandi": (45.0, 91.8, 4), "sabbi-amar": (76.0, 87.8, 4), "abbisin": (87.0, 73.8, 4),
    "tilicia": (87.5, 41.8, 2), "isoluccia": (75.0, 61.8, 2), "mare-nostra": (57.0, 69.8, 1),
    "mirror-sea": (80.0, 28.8, 1), "satoshi": (90.0, 6.8, 1), "tezcal": (93.0, 24.8, 1), "jarnheim": (46.0, 5.8, 1),
    "khemret": (61.0, 84.0, 1), "moananui": (37.0, 67.8, 1), "coatlan": (93.0, 56.8, 1), "thalassar": (33.0, 87.0, 1),
    "brasshaven": (68.0, 18.8, 1), "amber-reach": (15.0, 54.8, 1),
}
GAP = 2  # the marker's flex gap, px
CLEAR = 1.5  # px kept between two parts
EDGE = 3  # px kept from the map's frame
BORDER = 4  # the frame itself: positions are percentages of the map inside it


def parts(view, key, x, y, up):
    """The rectangles (x0, y0, x1, y1), in px inside the frame, of a marker at (x, y) percent."""
    m = view["marks"][key]
    ax, ay = x / 100 * (view["w"] - 2 * BORDER), y / 100 * (view["h"] - 2 * BORDER)
    dw, dh = m["dot"]
    out = [(ax - dw / 2, ay - dh / 2, ax + dw / 2, ay + dh / 2)]
    edge = ay - dh / 2 if up else ay + dh / 2
    for size in (m["label"], m.get("raids") or view["pips"]):  # (a region not yet open has no pips: room is kept)
        w, h = size
        if up:
            out.append((ax - w / 2, edge - GAP - h, ax + w / 2, edge - GAP))
            edge -= GAP + h
        else:
            out.append((ax - w / 2, edge + GAP, ax + w / 2, edge + GAP + h))
            edge += GAP + h
    return out


def clash(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0]) + CLEAR
    h = min(a[3], b[3]) - max(a[1], b[1]) + CLEAR
    return w * h if w > 0 and h > 0 else 0.0


def outside(view, rect):
    w, h = view["w"] - 2 * BORDER, view["h"] - 2 * BORDER
    return (max(0, EDGE - rect[0]) + max(0, EDGE - rect[1]) + max(0, rect[2] - (w - EDGE)) + max(0, rect[3] - (h - EDGE))) * 12


def cost_of(views, pos, key, rects):
    """What marker `key` costs: its clashes with every other marker and the frame, and its distance from home."""
    total = 0.0
    for vi, view in enumerate(views):
        mine = rects[key][vi]
        for r in mine:
            total += outside(view, r)
        for other, theirs in rects.items():
            if other == key:
                continue
            for a in mine:
                for b in theirs[vi]:
                    if a[0] < b[2] + CLEAR and b[0] < a[2] + CLEAR:
                        total += clash(a, b)
    x, y, up = pos[key]
    wx, wy, hold = WANT[key]
    return total * 40 + hold * ((x - wx) ** 2 + (y - wy) ** 2) + (3 if up else 0)


def solve(views, seed, start=None):
    rng = random.Random(seed)
    pos = {k: (WANT[k][0], WANT[k][1], False) for k in WANT}
    pos.update(start or {})
    warm = 0.08 if start else 1.0  # a table to repair: small moves, little heat
    rects = {k: [parts(v, k, *pos[k]) for v in views] for k in WANT}
    keys = list(WANT)
    steps = 700000 if not start else 260000
    for step in range(steps):
        # cool for most of the run, then only ever take a move that is no worse
        heat = warm * 60 * max(0.0, 1 - step / (0.85 * steps)) ** 3 + 0.01
        key = rng.choice(keys)
        x, y, up = pos[key]
        before = cost_of(views, pos, key, rects)
        if rng.random() < 0.12:
            new = (x, y, not up)
        else:
            reach = 0.3 + warm * 6 * (1 - step / steps) ** 2
            new = (min(98, max(2, x + rng.gauss(0, reach))), min(98, max(2, y + rng.gauss(0, reach))), up)
        old_rects = rects[key]
        pos[key], rects[key] = new, [parts(v, key, *new) for v in views]
        after = cost_of(views, pos, key, rects)
        if after > before and rng.random() > math.exp((before - after) / heat):
            pos[key], rects[key] = (x, y, up), old_rects
    return pos, rects


def problems(views, names, rects):
    found = []
    for vi, view in enumerate(views):
        keys = list(rects)
        for i, a in enumerate(keys):
            if any(outside(view, r) for r in rects[a][vi]):
                found.append("%s: %s leaves the map" % (names[vi], a))
            for b in keys[i + 1 :]:
                if any(clash(p, q) for p in rects[a][vi] for q in rects[b][vi]):
                    found.append("%s: %s × %s" % (names[vi], a, b))
    return found


def main():
    data = json.load(open(sys.argv[1]))
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    names = list(data)
    views = [data[n] for n in names]
    for view in views:  # the widest row of pips at this size stands in for a region that shows none yet
        view["pips"] = max((m["raids"] for m in view["marks"].values() if m.get("raids")), default=[0, 0])
    start = None
    if len(sys.argv) > 3:
        row = re.compile(r'"?([\w-]+)"?: \{ left: "([\d.]+)%", top: "([\d.]+)%"(, up: true)? \}')
        start = {m[1]: (float(m[2]), float(m[3]), bool(m[4])) for m in row.finditer(open(sys.argv[3]).read())}
    pos, rects = solve(views, seed, start)
    found = problems(views, names, rects)
    moved = sum(math.hypot(pos[k][0] - WANT[k][0], pos[k][1] - WANT[k][1]) for k in WANT)
    print("// seed %d: %d problems, %.0f%% moved in all" % (seed, len(found), moved), file=sys.stderr)
    for line in found:
        print("//   " + line, file=sys.stderr)
    for key in WANT:
        x, y, up = pos[key]
        name = '"%s"' % key if "-" in key else key
        print('  %s: { left: "%.1f%%", top: "%.1f%%"%s },' % (name, x, y, ", up: true" if up else ""))
    return len(found)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
