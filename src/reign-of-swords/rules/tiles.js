/* ============================================================
   Reign of Swords — the BONUS terrain tiles (Game mixin).
   NOT from the original games: nineteen kinds of ground for the bonus campaigns (designs supplied by the user;
   MECHANICS.md §13). Their tiles follow Episode II's 260 in the tileset and their terrain types its 30
   (tools/ros/bonus/import_tiles.py writes both, with each type's move costs, cover and healing — those three play by
   the original's own tables). What a table cannot say is here: what a tile does to the unit that walks onto it, stands
   on it as its turn begins, shoots from it or is shot on it.

   The game has no miss chance, so the designs' "evasion" is a share of the damage (user decision): Mirage Sand and
   Bamboo turn part of every shot, Abyssal Muck and an Astral Glyph let more of it through.
   ============================================================ */
import { moveType } from "./terrain.js";
import { HEAVY_ARMOUR } from "../data/bonus-units.js";

// the terrain types (movement.json types[] / rows[]: 30 and up are ours)
export const TILE = {
  CONVEYOR: 30,
  VENT: 31,
  MUCK: 32,
  CHIMNEY: 33,
  TAR: 34,
  FERN: 35,
  ICE: 36,
  MONOLITH: 37,
  SINKHOLE: 38,
  MIRAGE: 39,
  ALTAR: 40,
  RUINS: 41,
  CORAL: 42,
  CENOTE: 43,
  GLYPH: 44,
  CHINAMPA: 45,
  OBSIDIAN: 46,
  BAMBOO: 47,
  ZEN: 48,
};
// the four belts and where each carries (tile id -> step), and the tile burnt bamboo leaves
const BELT = { 260: [0, -1], 261: [1, 0], 262: [0, 1], 263: [-1, 0] };
const ASH_TILE = 282;
// the numbers
export const TILE_RULE = {
  chimneyBurn: 8, // HP a Thermal Chimney costs its occupant as its turn begins
  chimneyCover: 30, // …and the share (%) of every shot it turns
  monolithMend: 5, // HP a unit within a tile of a Runic Monolith mends each turn
  mirageCover: 50, // the share (%) of every shot Mirage Sand turns
  bambooCover: 40, // …and a Bamboo Thicket, for troops on foot
  bambooBurn: 10, // HP burning bamboo costs whoever stands in it
  exposed: 25, // the share (%) MORE of every shot a unit takes in Abyssal Muck or on an Astral Glyph
  glyphRange: 2, // tiles an Astral Glyph adds to a ranged weapon's reach
  coralCut: 5, // HP per tile of Razor Coral crossed
  obsidianCut: 5, // HP per tile of Obsidian Spikes crossed
  shattered: 10, // added to the weapon x armour cell of every blow at a unit whose heavy armour the spikes broke
  iceBump: 5, // HP each of two units loses when one slides into the other
  altarTithe: 20, // HP the Altar Steps give whoever strikes a unit down on them
};
// What the terrain card says of each kind (engine/input _tileHazards).
export const TILE_HELP = {
  [TILE.CONVEYOR]:
    "As each round ends, whatever stands on a belt is carried one tile the way its arrows point. Fliers are not, nor what cannot be moved.",
  [TILE.VENT]:
    "The steam hides what is beyond it: no bow, gun or spell can be aimed across a vent. War engines lob over it.",
  [TILE.MUCK]:
    "It costs 2 to enter, and whoever stands in it takes 25% more from every shot. The Trench Brood and fliers are at home here.",
  [TILE.CHIMNEY]:
    "Hard cover: 30% less from every shot. But it burns its occupant for 8 HP as each of its turns begins.",
  [TILE.TAR]:
    "Cavalry and war engines cannot enter. A unit on foot that steps in stops here, cannot move on its next turn, and takes 10% more damage. The Saurian Exiles cross it freely.",
  [TILE.FERN]:
    "Any unit that ends its move or its turn here unseen is hidden: it cannot be attacked until an enemy steps beside it — and then it strikes first.",
  [TILE.ICE]:
    "A unit that steps on keeps sliding the way it came until it leaves the ice or meets something. Sliding into another unit costs both 5 HP. Fliers are not troubled.",
  [TILE.MONOLITH]: "No one can stand here. Every unit on the eight tiles around it mends 5 HP as its turn begins.",
  [TILE.SINKHOLE]:
    "A unit that steps in stops. On its next turn it can only climb out to a tile beside it, and cannot attack. Fliers and Dune Sirens are immune.",
  [TILE.MIRAGE]: "No cover hand to hand, but every shot at a unit standing here does half damage.",
  [TILE.ALTAR]: "Whoever strikes a unit down on these steps is healed 20 HP.",
  [TILE.RUINS]:
    "A wall no one can pass — until it is brought down. Any weapon will do it: strike the ruins from beside them. What is left is rough open ground.",
  [TILE.CORAL]:
    "Shallows, and sharp: every tile of coral a ground unit crosses costs it 5 HP. The people of Moananui and the Trench Brood know the reef.",
  [TILE.CENOTE]:
    "It costs 2 to enter and a move ends here. A unit in a cenote can Dive, coming up in any other cenote that is free.",
  [TILE.GLYPH]:
    "A unit shooting from here reaches 2 tiles farther. Lit by it, it takes 25% more from every shot aimed back.",
  [TILE.CHINAMPA]: "It costs 2 to enter. A unit that starts its turn here mends 10 HP.",
  [TILE.OBSIDIAN]:
    "Every tile of spikes a ground unit crosses costs it 5 HP, and heavy armour shatters on them: for the rest of the battle every blow at it lands 10 harder.",
  [TILE.BAMBOO]:
    "Cavalry and war engines cannot enter. Troops on foot take 40% less from every shot. Any fire burns it to open ash, and whoever stands in it for 10 HP.",
  [TILE.ZEN]:
    "Stepping here clears every ailment: acid, venom, snares, chill, blindness, shattered armour. A unit standing here cannot be dragged or thrown.",
};

export const TileMethods = {
  // The bonus terrain type of a tile (or the original's, or undefined off the map).
  _tileKind(tx, ty) {
    return this.inBounds(tx, ty) ? moveType(this.tileAt(tx, ty)) : undefined;
  },
  _grounded(u) {
    return !!u.T && u.T.al !== 0 && !u.T.fly;
  },
  // What a faction is at home on: the move cost of the tile, or null to leave the table's.
  _tileHomeCost(u, kind) {
    if (kind === TILE.MUCK && u.T.culture === "trench") return 1;
    if (kind === TILE.TAR && u.T.culture === "saurian") return 1;
    return null;
  },
  // A tile a ground unit may step onto but not on through (engine/grid _walkReach): tar, ice, a sinkhole, a cenote.
  _tileStops(u, tx, ty) {
    if (!this._grounded(u)) return false;
    const kind = this._tileKind(tx, ty);
    if (kind === TILE.TAR) return u.T.culture !== "saurian";
    if (kind === TILE.SINKHOLE) return !this._quicksandImmune(u);
    return kind === TILE.ICE || kind === TILE.CENOTE;
  },
  _underFern(u) {
    return this._tileKind(u.tx, u.ty) === TILE.FERN;
  },
  // Nothing drags or throws a unit that is Immovable or stands in a Zen Sand Garden.
  _unmovable(u) {
    return !!u.T.anchored || this._tileKind(u.tx, u.ty) === TILE.ZEN;
  },
  _place(u, tx, ty) {
    Object.assign(u, { tx, ty, px: tx * this.tile, py: ty * this.tile });
  },
  _tileNote(u, text) {
    this.floaters.push({ x: u.px + this.tile / 2, y: u.py - 8, t: 0, life: 0.9, vy: -14, text, crit: true });
  },
  // THE END OF A MOVE. `path` = the tiles walked (start included), or none for a blink, a drag or a belt.
  _tileEnter(u, path) {
    if (!u || u.dead || !this._grounded(u)) return;
    // what was crossed on the way: coral and obsidian cut at every tile
    const crossed = path && path.length > 1 ? path.slice(1) : [{ tx: u.tx, ty: u.ty }];
    let cut = 0,
      spikes = false;
    for (const step of crossed) {
      const kind = this._tileKind(step.tx, step.ty);
      if (kind === TILE.CORAL && u.T.culture !== "trench" && u.T.culture !== "moananui") cut += TILE_RULE.coralCut;
      if (kind === TILE.OBSIDIAN) {
        cut += TILE_RULE.obsidianCut;
        spikes = true;
      }
    }
    if (spikes && HEAVY_ARMOUR.includes(u.T.armour) && !u._shattered) {
      u._shattered = true;
      this._tileNote(u, "Shattered");
    }
    if (cut) {
      this._commitMove(u);
      this._rawDamage(u, cut, null);
      if (u.dead) return;
    }
    const kind = this._tileKind(u.tx, u.ty);
    if (kind === TILE.ICE) {
      const last = path && path.length > 1 ? path[path.length - 1] : null,
        prev = last ? path[path.length - 2] : null;
      if (last && this._iceSlide(u, Math.sign(last.tx - prev.tx), Math.sign(last.ty - prev.ty))) {
        this._commitMove(u);
        this._hazardEnter(u, null); // what it slid onto
      }
      return;
    }
    if (kind === TILE.TAR && u.T.culture !== "saurian") {
      this._commitMove(u);
      // stuck for its NEXT turn: walked in on its own turn, the hold begins as that turn ends (grid _endTurnHide);
      // dragged in on the enemy's, it is held at once
      if (this._onOwnTurn(u)) u._snareNext = true;
      else u._held = true;
      this._tileNote(u, "Stuck");
    } else if (kind === TILE.SINKHOLE && !this._quicksandImmune(u)) {
      this._commitMove(u);
      if (!this._onOwnTurn(u)) u._sunk = true; // dragged in on the enemy's turn: its own next turn is the climb out
      this._tileNote(u, "Sunk");
    } else if (kind === TILE.ZEN) this._tileCleanse(u);
  },
  // BLACK ICE: the unit goes on, tile by tile, the way it was moving — across the ice and onto the first ground
  // beyond it, or until a wall, the map's edge or another unit stops it (a bump costs both).
  _iceSlide(u, dx, dy) {
    if (!dx && !dy) return false;
    let moved = false;
    while (this._tileKind(u.tx, u.ty) === TILE.ICE) {
      const nx = u.tx + dx,
        ny = u.ty + dy;
      if (!this.inBounds(nx, ny)) break;
      const other = this.unitAt(nx, ny);
      if (other) {
        this.spawnFx("slash", other.px + this.tile / 2, other.py + this.tile * 0.42, {});
        this._rawDamage(other, TILE_RULE.iceBump, null);
        this._rawDamage(u, TILE_RULE.iceBump, null);
        break;
      }
      if (this.moveCost(u, nx, ny) >= 99) break;
      this._place(u, nx, ny);
      moved = true;
    }
    return moved;
  },
  // ZEN SAND GARDEN: every ailment is left at its edge.
  _tileCleanse(u) {
    const ailing =
      u._acid || u._held || u._blind || u._chilled || u._seized || u.slowed || u._snareNext || u._shattered;
    Object.assign(u, {
      _acid: null,
      _held: false,
      _blind: false,
      _chilled: false,
      _seized: false,
      slowed: false,
      _snareNext: false,
      _shattered: false,
    });
    if (ailing) {
      this.spawnFx("spark", u.px + this.tile / 2, u.py + this.tile * 0.42, {});
      this.floaters.push({
        x: u.px + this.tile / 2,
        y: u.py - 8,
        t: 0,
        life: 0.9,
        vy: -14,
        text: "Cleansed",
        heal: true,
      });
    }
  },
  // THE START OF A UNIT'S TURN (engine healOnKeeps): a chimney burns, a monolith mends, a sinkhole holds.
  _tileTurnStart(u) {
    if (u.dead) return;
    const kind = this._tileKind(u.tx, u.ty);
    if (kind === TILE.CHIMNEY) {
      this.spawnFx("fire", u.px + this.tile / 2, u.py + this.tile * 0.42, {});
      this._rawDamage(u, TILE_RULE.chimneyBurn, null);
      if (u.dead) return;
    }
    if (kind === TILE.SINKHOLE && this._grounded(u) && !this._quicksandImmune(u)) u._sunk = true;
    if (u.hp < 100 && this._nearMonolith(u)) {
      const before = u.hp;
      u.hp = Math.min(100, before + TILE_RULE.monolithMend);
      this.floaters.push({
        x: u.px + this.tile / 2,
        y: u.py - 6,
        t: 0,
        life: 0.8,
        vy: -22,
        text: "+" + (u.hp - before),
        heal: true,
      });
    }
  },
  _nearMonolith(u) {
    for (let dy = -1; dy <= 1; dy++)
      for (let dx = -1; dx <= 1; dx++)
        if ((dx || dy) && this._tileKind(u.tx + dx, u.ty + dy) === TILE.MONOLITH) return true;
    return false;
  },
  // A SHOT at a unit on one of these tiles: the share (%) of it that lands (100 = all of it).
  _tileShotShare(defender) {
    if (!defender.T || defender._phantom) return 100;
    const kind = this._tileKind(defender.tx, defender.ty);
    if (kind === TILE.MIRAGE) return 100 - TILE_RULE.mirageCover;
    if (kind === TILE.CHIMNEY) return 100 - TILE_RULE.chimneyCover;
    if (kind === TILE.BAMBOO) return defender.T.al === 1 || defender.T.al === 2 ? 100 - TILE_RULE.bambooCover : 100;
    if (kind === TILE.GLYPH) return 100 + TILE_RULE.exposed;
    if (kind === TILE.MUCK)
      return defender.T.culture === "trench" || !this._grounded(defender) ? 100 : 100 + TILE_RULE.exposed;
    return 100;
  },
  // ASTRAL GLYPH: tiles added to the reach of a ranged weapon fired from (tx, ty).
  _tileRangeBonus(tx, ty) {
    return this._tileKind(tx, ty) === TILE.GLYPH ? TILE_RULE.glyphRange : 0;
  },
  // VENT GRATE: is the straight line from one tile to another crossed by steam? (The tiles between them the line
  // passes through; the two ends do not count.) Asked only on maps that have a vent.
  _hasVents() {
    if (this._ventsOf !== this.tiles) {
      this._ventsOf = this.tiles;
      this._vents = this.tiles.some((tileVal) => moveType(tileVal) === TILE.VENT);
    }
    return this._vents;
  },
  _shotBlocked(u, fx, fy, tx, ty) {
    if (u.T.al === 4 || !this._hasVents()) return false; // war engines lob over the steam
    const steps = Math.max(Math.abs(tx - fx), Math.abs(ty - fy)) * 2;
    for (let i = 1; i < steps; i++) {
      const x = Math.round(fx + ((tx - fx) * i) / steps),
        y = Math.round(fy + ((ty - fy) * i) / steps);
      if ((x === fx && y === fy) || (x === tx && y === ty)) continue;
      if (this._tileKind(x, y) === TILE.VENT) return true;
    }
    return false;
  },
  // SACRIFICIAL ALTAR STEPS: whoever strikes a unit down on them is healed (rules/combat _onFall).
  _altarTithe(fallen, killer) {
    if (!killer || killer.dead || !killer.T || killer === fallen || killer.hp >= 100) return;
    if (this._tileKind(fallen.tx, fallen.ty) !== TILE.ALTAR) return;
    const before = killer.hp;
    killer.hp = Math.min(100, before + TILE_RULE.altarTithe);
    this.spawnFx("spark", killer.px + this.tile / 2, killer.py + this.tile * 0.42, {});
    this.floaters.push({
      x: killer.px + this.tile / 2,
      y: killer.py - 4,
      t: 0,
      life: 0.9,
      vy: -22,
      text: "+" + Math.round(killer.hp - before),
      heal: true,
    });
  },
  // BAMBOO THICKET: fire on the tile burns it to ash, and whoever stands in it (rules/combat structureHit).
  _bambooBurn(tx, ty) {
    if (this._tileKind(tx, ty) !== TILE.BAMBOO) return false;
    this.tiles[ty * this.cols + tx] = ASH_TILE;
    this.spawnFx("fire", tx * this.tile + this.tile / 2, ty * this.tile + this.tile * 0.42, {});
    const inside = this.unitAt(tx, ty);
    if (inside) this._rawDamage(inside, TILE_RULE.bambooBurn, null);
    if (this.selected && !this.anim) {
      this.reach = this.computeReach(this.selected);
      this.recalcTargets();
    }
    return true;
  },
  // CONVEYOR BELTS: as the round ends, each unit on a belt is carried one tile along it — once, the units at the
  // front of a belt first, so a full belt moves as one. A tile it cannot stand on, or one that is taken, stops it.
  _conveyorTurn() {
    const riders = this.units.filter(
      (u) => !u.dead && this._grounded(u) && !u.T.anchored && BELT[this.tileAt(u.tx, u.ty)],
    );
    if (!riders.length) return;
    const carried = new Set();
    for (let pass = 0, moved = true; moved && pass < riders.length; pass++) {
      moved = false;
      for (const u of riders) {
        if (carried.has(u) || u.dead) continue;
        const step = BELT[this.tileAt(u.tx, u.ty)];
        if (!step) continue;
        const nx = u.tx + step[0],
          ny = u.ty + step[1];
        if (!this.inBounds(nx, ny) || this.unitAt(nx, ny) || this.moveCost(u, nx, ny) >= 99) continue;
        this._place(u, nx, ny);
        carried.add(u);
        moved = true;
      }
    }
    for (const u of carried) this._hazardEnter(u, null);
  },
  // CENOTE: the other cenotes a unit standing in one could come up in (free ones), and the dive itself — the rest of
  // its move for the turn, once a turn.
  _cenoteExits(u) {
    if (u._dived === this.turn || !this._grounded(u) || this._tileKind(u.tx, u.ty) !== TILE.CENOTE) return [];
    const out = [];
    for (let y = 0; y < this.rows; y++)
      for (let x = 0; x < this.cols; x++)
        if ((x !== u.tx || y !== u.ty) && this._tileKind(x, y) === TILE.CENOTE && !this.unitAt(x, y))
          out.push({ x, y });
    return out;
  },
  _castDive(u, tx, ty) {
    u._dived = this.turn;
    u._movedPrev = u._movedTurn;
    u._movedTurn = this.turn;
    this._commitMove(u);
    this.reach = null;
    this.targets = null;
    this._teleportMove(u, { tx, ty }, () => this._afterPlayerMove(u));
  },
};
