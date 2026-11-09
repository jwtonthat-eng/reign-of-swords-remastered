#!/usr/bin/env python3
"""Build the BONUS campaigns (Tilicia & Isoluccia) -> public/games/reign-of-swords-2/bonus.json.

These two campaigns are NOT from the original games: they are authored for this project (MECHANICS.md §13).
Unlike levels.json (exported from the original .dat by export_levels.py), every record here is written by hand in
tilicia.py / isoluccia.py as two ASCII grids (terrain, units) plus a short description of what happens, and this
tool turns it into the SAME record shapes the engine already plays: a levels.json level (tiles, armies, groups,
markers, the scenario script with its triggers), its rewards, hold tiles, heraldry and the campaign entry.

    python3 tools/ros/bonus/build_bonus.py            # write bonus.json
    python3 tools/ros/bonus/build_bonus.py --check    # build and validate only

Edit the level files and re-run; don't hand-edit bonus.json.
"""
import json
import os
import random
import sys
from collections import Counter, defaultdict, deque

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(ROOT, "public", "games", "reign-of-swords-2")
OUT = os.path.join(DATA, "bonus.json")

MOVEMENT = json.load(open(os.path.join(DATA, "movement.json")))
TYPES = MOVEMENT["types"]
ROWS = MOVEMENT["rows"]
LINKS = {int(k): v for k, v in MOVEMENT.get("links", {}).items()}
ORIG = json.load(open(os.path.join(DATA, "levels.json")))["levels"]

# ---------------------------------------------------------------- speakers
SPEAKERS = {
    "advisor": ("War Advisor", "you", "face001"),
    "advisor_grim": ("War Advisor", "you", "face003"),
    "officer": ("Field Officer", "you", "face059"),
    "officer_alarm": ("Field Officer", "you", "face061"),
    "officer_hurt": ("Field Officer", "you", "face063"),
    "thaddius": ("Archwizard Thaddius", "you", ""),
    "emperor": ("Emperor Sebatini", "you", "face056"),
    "tolm": ("Warden Tolm", "foe", "face069"),
    "tolm_hurt": ("Warden Tolm", "foe", "face071"),
    "ostrak": ("Chief Ostrak", "you", "face075"),
    "bellaro": ("Captain Bellaro", "you", "face078"),
    "doge": ("Doge Sant'Abra", "foe", "face072"),
    "doge_angry": ("Doge Sant'Abra", "foe", "face073"),
    "doge_hurt": ("Doge Sant'Abra", "foe", "face074"),
    "battlemage": ("The Battlemage", "foe", "face083"),
    "enemy": ("Enemy Commander", "foe", "face066"),
    "enemy_hurt": ("Enemy Commander", "foe", "face068"),
    "clansman": ("Tilician Clansman", "you", "face086"),
}


def lines(pairs):
    out = []
    for who, text in pairs or []:
        name, side, face = SPEAKERS[who]
        out.append({"speaker": name, "side": side, "face": face, "text": text})
    return out


# ---------------------------------------------------------------- terrain
# Two looks, both from the Episode II tileset: "green" (grass, forest, grey stone, river blue) for Tilicia and
# "sand" (dunes, turquoise sea, sandstone) for Isoluccia. The edge pieces of water, shallows, cliffs and roads are
# picked the way the ORIGINAL maps use them: for every such tile in the original levels the 4-neighbour pattern is
# tallied, and a new map takes the most common tile for its own pattern.
THEMES = {
    "green": {
        "tiles": set(range(0, 124)),
        "ground": [63],
        "rough": [64],
        "forest": [0],
        "house": [3],
        "rocky": [101, 102, 103, 104],
        "stone": [103],  # a rock mound (the standing stone 250 sits on a sand plinth)
        "scrub": [64],
        "floor": [66],
        "road": None,  # autotiled
        "tower": [36],
        "keep": [33],
        "wall": {"top": 39, "bottom": 48, "west": 42, "east": 45},
        "gate": {"top": 56, "bottom": 50, "west": 52, "east": 52},
        "palisade": [6],
        "woodgate": [59],
        "barricade": [18],
        "portal": [217],
        "fountain": [33],
    },
    "sand": {
        "tiles": set(range(124, 260)),
        "ground": [133, 133, 133, 133, 134, 135],
        "rough": [136, 137],
        "forest": [180],
        "house": [185],
        "rocky": [155, 156, 157, 158],
        "stone": [182],
        "scrub": [138],
        "floor": [177, 177, 177, 178],
        "road": [177],
        "tower": [200],
        "keep": [214],
        "wall": {"top": 191, "bottom": 188, "west": 194, "east": 197},
        "gate": {"top": 211, "bottom": 213, "west": 211, "east": 213},
        "palisade": [6],
        "woodgate": [59],
        "barricade": [18],
        "portal": [215],
        "fountain": [214],
    },
}
WATERISH = (19, 20, 5)
DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # N E S W  -> mask bits 1 2 4 8


def learn(theme_tiles, member_type, same_types):
    table = defaultdict(Counter)
    for level in ORIG:
        cols, rows, tiles = level["cols"], level["rows"], level["tiles"]
        for y in range(rows):
            for x in range(cols):
                tile = tiles[y * cols + x]
                if TYPES[tile] != member_type or tile not in theme_tiles:
                    continue
                mask = 0
                for i, (dx, dy) in enumerate(DIRS):
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < cols and 0 <= ny < rows) or TYPES[tiles[ny * cols + nx]] in same_types:
                        mask |= 1 << i
                table[mask][tile] += 1
    best = {mask: counts.most_common(1)[0][0] for mask, counts in table.items()}
    overall = Counter()
    for counts in table.values():
        overall.update(counts)
    return best, overall.most_common(1)[0][0]


AUTOTILE = {}
for theme_name, theme in THEMES.items():
    AUTOTILE[theme_name] = {
        "~": learn(theme["tiles"], 19, WATERISH),
        "-": learn(theme["tiles"], 5, WATERISH),
        "^": learn(theme["tiles"], 21, (21,)),
    }
AUTOTILE["green"]["="] = learn(set(range(116, 124)) | {66}, 18, (18,))

WALLISH = "WTGK"


def compile_terrain(theme_name, grid, seed):
    """ASCII terrain -> tile ids.
    . ground   , rough (tall grass / boulders)   f forest   s scrub   r rocky ground   o standing stone
    ~ deep water   - shallows   ^ cliffs   = road / paving   b bridge (green)   h house   F fountain
    W wall  T tower  G gate  K keep  _ courtyard floor   P palisade  p wooden gate  x barricade  O rune gate
    """
    theme = THEMES[theme_name]
    rng = random.Random(seed)
    rows = len(grid)
    cols = len(grid[0])
    at = lambda x, y: grid[y][x] if 0 <= x < cols and 0 <= y < rows else None
    pick = lambda key: rng.choice(theme[key])
    out = []
    for y in range(rows):
        for x in range(cols):
            ch = grid[y][x]
            if ch in "~-^" or (ch == "=" and theme["road"] is None):
                same = {"~": "~-b", "-": "~-b", "^": "^", "=": "=bG_"}[ch]
                mask = 0
                for i, (dx, dy) in enumerate(DIRS):
                    n = at(x + dx, y + dy)
                    if n is None or n in same:
                        mask |= 1 << i
                best, fallback = AUTOTILE[theme_name][ch]
                out.append(best.get(mask, fallback))
            elif ch == "=":
                out.append(pick("road"))
            elif ch == "b":
                if theme_name != "green":
                    out.append(pick("road"))  # the sand set has no bridge: a paved causeway
                elif at(x - 1, y) in "~-b" and at(x + 1, y) in "~-b" and at(x, y - 1) not in ("~", "-"):
                    out.append(116)  # mid-span of an east-west bridge
                elif at(x, y - 1) in ("~", "-", "b") or at(x, y + 1) in ("~", "-", "b"):
                    out.append(71 if at(x, y - 1) != "b" else 117)  # a north-south deck
                else:
                    out.append(68 if at(x + 1, y) == "b" else 69)
            elif ch == "W" or ch == "G":
                horizontal = (at(x - 1, y) or " ") in WALLISH or (at(x + 1, y) or " ") in WALLISH
                table = theme["wall" if ch == "W" else "gate"]
                if horizontal:
                    out.append(table["top" if at(x, y + 1) == "_" else "bottom"])
                else:
                    out.append(table["west" if at(x + 1, y) == "_" else "east"])
            else:
                key = {
                    ".": "ground",
                    ",": "rough",
                    "f": "forest",
                    "s": "scrub",
                    "r": "rocky",
                    "o": "stone",
                    "h": "house",
                    "F": "fountain",
                    "T": "tower",
                    "K": "keep",
                    "_": "floor",
                    "P": "palisade",
                    "p": "woodgate",
                    "x": "barricade",
                    "O": "portal",
                }.get(ch)
                if key is None:
                    raise ValueError("unknown terrain %r at %d,%d" % (ch, x, y))
                out.append(pick(key))
    return out


# ---------------------------------------------------------------- level builder
OP_SPAWN, OP_SCREEN, OP_CAMERA, OP_COUNTER, OP_SETFLAG = 0, 1, 2, 9, 10
MOVE_CLASS = {
    "cavalry": 3, "knights": 3, "king": 3, "raiders": 3, "horsebowmen": 3,
    "catapult": 4, "trebuchet": 4, "cannon": 4, "ballistae": 4,
    "griffon": 0,
    "footmen": 2, "swordsmen": 2, "greatswordsmen": 2, "pikemen": 2, "halberdiers": 2, "crossbowmen": 2,
    "musketeers": 2, "conjurer": 2, "bodyguard": 2, "bloodgorgers": 2,
    "spellwardens": 2, "sentinel": 2, "pavisiers": 2, "battlemage": 2,
}
CROSSES = {"cragsmen": 21, "marines": 19}  # Climb / Amphibious


def U(key, side="E", group=None, hold=False, name=None):
    """A unit in a level's legend. side: 'P' the player's preset force, 'E'/'E2' an enemy army, 'A' an allied army.
    group: its AI group number (units of a side sharing a number march as one formation); hold: the group stands
    its ground until attacked; name: a handle the level's events can refer to (a kill trigger, an escort)."""
    return {"key": key, "side": side, "group": group, "hold": hold, "name": name}


class Level:
    def __init__(self, spec):
        self.s = spec
        self.terrain = [row for row in spec["terrain"].strip("\n").split("\n")]
        self.units_grid = [row for row in spec["units"].strip("\n").split("\n")]
        self.rows = len(self.terrain)
        self.cols = len(self.terrain[0])
        name = spec["name"]
        for label, grid in (("terrain", self.terrain), ("units", self.units_grid)):
            if len(grid) != self.rows or any(len(row) != self.cols for row in grid):
                raise ValueError("%s: the %s grid is not %dx%d" % (name, label, self.cols, self.rows))
        self.tiles = compile_terrain(spec["theme"], self.terrain, spec["id"])
        self.actions, self.triggers = [], []
        self.next_sid = 0
        self.next_counter = 1
        self.named = defaultdict(list)  # handle -> [sid]
        self.points = defaultdict(list)  # digit / letter -> [(x, y)]

    # --- script helpers
    def chain(self, ops):
        """Append actions linked by `next`; returns the index of the first (or -1 for none)."""
        if not ops:
            return -1
        start = len(self.actions)
        for i, op in enumerate(ops):
            op = dict(op)
            op["next"] = start + i + 1 if i + 1 < len(ops) else -1
            self.actions.append(op)
        return start

    def op_spawn(self, key, gi, x, y, handle=None):
        sid = self.next_sid
        self.next_sid += 1
        if handle:
            self.named[handle].append(sid)
        return {"op": OP_SPAWN, "a": [x, y, sid, 1, -1, -1], "key": key, "gi": gi, "x": x, "y": y, "sid": sid}

    def op_say(self, pairs, end=None):
        op = {"op": OP_SCREEN, "a": [0], "lines": lines(pairs)}
        if end:
            op["end"] = end
        return op

    def body(self, event):
        """The actions of one event: camera, reinforcements, a line or two, the win switch, the ending."""
        ops = []
        if event.get("cam"):
            x, y = self.point(event["cam"])
            ops.append({"op": OP_CAMERA, "a": [x, y]})
        for key, where, side, *rest in event.get("spawn", []):
            gi = self.gi[side]
            for x, y in self.point_list(where):
                ops.append(self.op_spawn(key, gi, x, y, rest[0] if rest else None))
        if event.get("say") or event.get("end"):
            ops.append(self.op_say(event.get("say"), event.get("end")))
        if "win_switch" in event:
            ops.append({"op": OP_SETFLAG, "a": [1 if event["win_switch"] else 0]})
        return ops

    def point_list(self, where):
        if isinstance(where, (tuple, list)):
            return [tuple(where)]
        if where not in self.points:
            raise ValueError("%s: no point %r on the units grid" % (self.s["name"], where))
        return self.points[where]

    def point(self, where):
        return self.point_list(where)[0]

    def counter(self):
        self.next_counter += 1
        return self.next_counter

    # --- build
    def build(self):
        s = self.s
        legend = s.get("legend", {})
        sides = s["sides"]  # {"P": name, "A": name, "E": name, "E2": name}
        order = [k for k in ("P", "A", "A2", "E", "E2", "E3") if k in sides]
        if s.get("enemy_first"):
            order = [k for k in order if k.startswith("E")] + [k for k in order if not k.startswith("E")]
        self.gi = {side: i for i, side in enumerate(order)}
        heraldry = s.get("heraldry", {})
        group_order, enemy_groups, ally_groups, herald = [], {}, {}, {}
        for side in order:
            gi = self.gi[side]
            kind = "player" if side == "P" else "ally" if side.startswith("A") else "enemy"
            arms = heraldry.get(side) or DEFAULT_ARMS[kind]
            group_order.append(
                {"gi": gi, "name": sides[side], "banner": arms[3], "team": 1 if kind == "enemy" else 0, "side": kind}
            )
            herald[str(gi)] = {
                "name": sides[side],
                "team": 1 if kind == "enemy" else 0,
                "symbolColor": arms[0],
                "bgColor": arms[1],
                "symbol": arms[2],
                "bgType": 0,
                "banner": arms[3],
            }
            if kind == "enemy":
                enemy_groups[str(len(enemy_groups))] = {"name": sides[side], "src": gi, "banner": arms[3], "team": 1}
            elif kind == "ally":
                ally_groups[str(len(ally_groups))] = {"name": sides[side], "src": gi, "banner": arms[3], "team": 0}
        side_index = {}
        for side in order:
            kind = "E" if side.startswith("E") else "A" if side.startswith("A") else "P"
            side_index[side] = sum(1 for o in order[: order.index(side)] if o.startswith(kind) and kind != "P")

        player, enemy, allies, deploy, markers, hold_tiles, spawn_ops = [], [], [], [], [], [], []
        marker_group = {}
        for y, row in enumerate(self.units_grid):
            for x, ch in enumerate(row):
                if ch == ".":
                    continue
                if ch == "D":
                    deploy.append([x, y])
                    continue
                if ch not in legend:
                    self.points[ch].append((x, y))
                    continue
                unit = legend[ch]
                side, key = unit["side"], unit["key"]
                gi = self.gi[side]
                spawn_ops.append(self.op_spawn(key, gi, x, y, unit["name"]))
                if side == "P":
                    player.append([key, x, y, 0, gi])
                elif side.startswith("A"):
                    allies.append([key, x, y, side_index[side], gi])
                else:
                    enemy.append([key, x, y, side_index[side], gi])
                if side != "P" and unit["group"] is not None:
                    group_key = (side, unit["group"])
                    number = marker_group.setdefault(group_key, len(marker_group))
                    markers.append([x, y, number, 1 if side.startswith("E") else 0])
                    if unit["hold"]:
                        hold_tiles.append([x, y])

        # the opening chain: win switch, camera, every unit on the field (so events can name them), the opening lines
        opening = []
        if "win_switch" in s:
            opening.append({"op": OP_SETFLAG, "a": [1 if s["win_switch"] else 0]})
        focus = s.get("camera") or (enemy[0][1:3] if enemy else [self.cols // 2, self.rows // 2])
        if isinstance(focus, str):
            focus = self.point(focus)
        opening.append({"op": OP_CAMERA, "a": list(focus)})
        opening += spawn_ops
        if s.get("intro"):
            opening.append(self.op_say(s["intro"]))
        head = self.chain(opening)
        initial = list(range(head, len(self.actions)))
        self.triggers.append({"tag": 2, "a": [head]})

        goals, escort = [], None
        for event in s.get("events", []):
            when = event["when"]
            body = self.chain(self.body(event))
            if when[0] == "round":  # ("round", n)
                counter = self.counter()
                gate = self.chain([{"op": OP_COUNTER, "a": [counter]}])
                self.triggers.append({"tag": 0, "a": [when[1], 0, -1, -1, gate]})
                self.triggers.append({"tag": 8, "a": [counter, 1, body]})
            elif when[0] == "kill":  # ("kill", handle[, count]) — `count` of the named units have fallen
                sids = self.named[when[1]]
                if not sids:
                    raise ValueError("%s: no unit named %r" % (s["name"], when[1]))
                need = when[2] if len(when) > 2 else len(sids)
                counter = self.counter()
                bump = self.chain([{"op": OP_COUNTER, "a": [counter]}])
                for sid in sids:
                    self.triggers.append({"tag": 7, "a": [sid, bump]})
                self.triggers.append({"tag": 8, "a": [counter, need, body]})
            elif when[0] == "reach":  # ("reach", point) — one of your units ends a move on any tile of the point
                counter = self.counter()
                for x, y in self.point_list(when[1]):
                    self.triggers.append({"tag": 6, "a": [x, y, counter, 0, -1, body]})
            elif when[0] == "reach_all":  # ("reach_all", [points]) — a unit has stood on each point in turn
                counter = self.counter()
                bump = self.chain([{"op": OP_COUNTER, "a": [counter]}])
                for where in when[1]:
                    gate = self.counter()
                    for x, y in self.point_list(where):
                        self.triggers.append({"tag": 6, "a": [x, y, gate, 0, -1, bump]})
                self.triggers.append({"tag": 8, "a": [counter, len(when[1]), body]})
            elif when[0] == "escaped":  # ("escaped", n, point) — n of your units have left by the goal tiles
                goals = [list(p) for p in self.point_list(when[2])]
                self.triggers.append({"tag": 9, "a": [when[1], 0, body]})
            elif when[0] == "escorted":  # ("escorted", handle, n, point) — n of the named units reach the goal
                escort = {
                    "units": self.named[when[1]],
                    "markers": [list(p) for p in self.point_list(when[3])],
                    "required": when[2],
                    "doneCmd": body,
                }
            else:
                raise ValueError("unknown event %r" % (when,))

        areas = [
            {"points": 50, "tiles": [list(p) for p in self.point_list(where)]} for where in s.get("areas", [])
        ]
        budget = s.get("budget", 0)
        level = {
            "bid": s["id"],
            "group": s["group"],
            "mapId": s["id"],
            "cols": self.cols,
            "rows": self.rows,
            "tiles": self.tiles,
            "name": s["name"],
            "kingdom": s["kingdom"],
            "subtitle": "%s vs %s" % (sides["P"], sides.get("E", "")),
            "objectiveText": s["objective"],
            "enemy": enemy,
            "budget": budget,
            "deployZone": deploy,
            "hero": None,
            "turnLimit": s.get("turn_limit", 30),
            "objectives": [],
            "player": player,
            "playerBudget": budget,
            "enemyFirst": bool(s.get("enemy_first")),
            "enemyGroups": enemy_groups,
            "allies": allies,
            "allyGroups": ally_groups,
            "groupOrder": group_order,
            "playerGroup": self.gi["P"],
            "startFallback": False,
            "areas": areas,
            "markers": markers,
            "factions": [
                {"name": sides["P"], "team": 0, "gold": budget, "objective": s["objective"]},
                {"name": sides.get("E", "Enemy"), "team": 1, "gold": 0, "objective": "Destroy the opponent's army."},
            ],
            "portals": [],
            "enemyBudget": 0,
            "missionType": s.get("mission_type", 0),
            "hidden": False,
            "victoryLines": lines(s.get("victory")),
            "defeatLines": lines(s.get("defeat")),
            "script": {
                "actions": self.actions,
                "triggers": self.triggers,
                "initial": initial,
                "rounds": [],
                "goals": goals,
                "escort": escort,
            },
            "ep": 2,
            "bonus": True,
        }
        self.validate(level, deploy)
        return level, hold_tiles, herald

    # --- checks: every unit stands on ground it can stand on, and your side can reach the enemy and its goals
    def cost(self, tile, move_class, key=None):
        kind = TYPES[tile]
        if key and CROSSES.get(key) == kind:
            return 2
        cost = ROWS[kind][move_class] or 1
        return 99 if cost >= 90 else cost

    def validate(self, level, deploy):
        name = self.s["name"]
        tiles, cols, rows = level["tiles"], self.cols, self.rows
        seen = set()
        for key, x, y, *_ in level["player"] + level["enemy"] + level["allies"]:
            if (x, y) in seen:
                raise ValueError("%s: two units at %d,%d" % (name, x, y))
            seen.add((x, y))
            if self.cost(tiles[y * cols + x], MOVE_CLASS.get(key, 1), key) >= 99:
                raise ValueError("%s: %s at %d,%d cannot stand there" % (name, key, x, y))
        for action in self.actions:
            if action["op"] == OP_SPAWN and self.cost(
                tiles[action["y"] * cols + action["x"]], MOVE_CLASS.get(action["key"], 1), action["key"]
            ) >= 99:
                raise ValueError("%s: %s spawns on impassable %d,%d" % (name, action["key"], action["x"], action["y"]))
        for x, y in deploy:
            if self.cost(tiles[y * cols + x], 2) >= 99:
                raise ValueError("%s: deploy tile %d,%d is impassable" % (name, x, y))
        if level["budget"] and len(deploy) < 12:
            raise ValueError("%s: only %d deploy tiles" % (name, len(deploy)))
        starts = [(x, y) for x, y in deploy] + [(x, y) for _, x, y, *_ in level["player"]]
        if not starts:
            raise ValueError("%s: the player has neither a force nor a deploy zone" % name)
        reach = self.flood(tiles, starts, 2)
        targets = [(x, y, "enemy " + key) for key, x, y, *_ in level["enemy"]]
        targets += [(a["x"], a["y"], "spawn " + a["key"]) for a in self.actions if a["op"] == OP_SPAWN]
        script = level["script"]
        targets += [(x, y, "goal") for x, y in script["goals"]]
        if script["escort"]:
            targets += [(x, y, "escort goal") for x, y in script["escort"]["markers"]]
        targets += [(t["a"][0], t["a"][1], "trigger tile") for t in self.triggers if t["tag"] == 6]
        for x, y, what in targets:
            near = [(x, y)] + [(x + dx, y + dy) for dx, dy in DIRS]
            if not any(p in reach for p in near):
                raise ValueError("%s: your foot soldiers cannot reach the %s at %d,%d" % (name, what, x, y))

    def flood(self, tiles, starts, move_class):
        cols, rows = self.cols, self.rows
        reach = set(starts)
        queue = deque(starts)
        while queue:
            x, y = queue.popleft()
            here = TYPES[tiles[y * cols + x]]
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < cols and 0 <= ny < rows) or (nx, ny) in reach:
                    continue
                there = TYPES[tiles[ny * cols + nx]]
                if self.cost(tiles[ny * cols + nx], move_class) >= 99:
                    continue
                if here != there:  # Map::isMoveAllowed: battlements are walked from inside
                    if there in LINKS and here not in LINKS[there]:
                        continue
                    if here in LINKS and there not in LINKS[here]:
                        continue
                reach.add((nx, ny))
                queue.append((nx, ny))
        return reach


# symbolColor, bgColor, device, banner
DEFAULT_ARMS = {"player": ("gules", "argent", 51, 0), "ally": ("or", "vert", 12, 3), "enemy": ("argent", "azure", 30, 4)}


def build(kingdoms):
    out = {"kingdoms": [], "levels": [], "rewards": {}, "scripts_ai": {}, "group_heraldry": {}}
    for kingdom in kingdoms:
        missions = []
        for spec in kingdom["levels"]:
            spec = dict(spec, kingdom=kingdom["short"], theme=spec.get("theme", kingdom["theme"]))
            spec.setdefault("heraldry", {})
            for side, arms in kingdom.get("heraldry", {}).items():
                spec["heraldry"].setdefault(side, arms)
            level, hold_tiles, herald = Level(spec).build()
            out["levels"].append(level)
            if hold_tiles:
                out["scripts_ai"][str(spec["id"])] = {"holdTiles": hold_tiles}
            out["group_heraldry"][str(spec["id"])] = herald
            out["rewards"][str(spec["id"])] = spec.get("reward", {"units": {}, "spoils": {}})
            if spec["group"] == "story":
                missions.append(
                    {
                        "mapId": spec["id"],
                        "title": spec["name"],
                        "intro": lines(spec.get("brief")),
                        "victory": lines(spec.get("victory")),
                        "defeat": lines(spec.get("defeat")),
                    }
                )
        out["kingdoms"].append(
            {
                "id": kingdom["id"],
                "name": "Kingdom of " + kingdom["short"],
                "order": kingdom["order"],
                "emperorBrief": lines(kingdom["brief"]),
                "legacy": False,
                "bonus": True,
                "missions": missions,
                "unlockAfter": kingdom["unlock_after"],
            }
        )
    return out


def main():
    sys.path.insert(0, HERE)
    import tilicia
    import isoluccia

    data = build([tilicia.KINGDOM, isoluccia.KINGDOM])
    stats = ", ".join("%d %s" % (sum(1 for l in data["levels"] if l["group"] == g), g) for g in ("story", "siege"))
    if "--check" in sys.argv:
        print("ok:", stats)
        return
    with open(OUT, "w") as f:
        json.dump(data, f, separators=(",", ":"))
        f.write("\n")
    print("wrote", os.path.relpath(OUT, ROOT), "-", stats)


if __name__ == "__main__":
    main()
