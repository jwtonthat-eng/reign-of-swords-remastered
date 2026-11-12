// The nineteen BONUS terrain tiles (ours; designs supplied by the user — rules/tiles.js, tools/ros/bonus/
// import_tiles.py, MECHANICS.md §13). Each test lays the tiles it needs on Zayandi Shores' open ground.
import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { loadEpisode, makeGame, startBattle, spawn, only, settle, nextRound, moveTo } from "./battle.js";
import { UNIT_TYPES } from "../data/game-data.js";
import { moveType, moveRow, tileName, tileProp, structTrans } from "../rules/terrain.js";
import { TILE, TILE_RULE, TILE_HELP } from "../rules/tiles.js";

await loadEpisode(2);

const DATA = join("public", "games", "reign-of-swords-2");
const json = (file) => JSON.parse(readFileSync(join(DATA, file), "utf8"));
// the new tiles' ids (import_tiles.py TILES, in order from 260)
const ID = {
  north: 260,
  east: 261,
  south: 262,
  west: 263,
  vent: 264,
  muck: 265,
  chimney: 266,
  tar: 267,
  fern: 268,
  ice: 269,
  monolith: 270,
  sinkhole: 271,
  mirage: 272,
  altar: 273,
  ruins: 274,
  ruinsBroken: 275,
  coral: 276,
  cenote: 277,
  glyph: 278,
  chinampa: 279,
  obsidian: 280,
  bamboo: 281,
  ash: 282,
  zen: 283,
  ruinsCleared: 284,
};
// a clean board on Zayandi Shores (5424): its tiles x 4–13, y 3–7 are open ground
function field() {
  const g = startBattle(makeGame(5424));
  only(g);
  return g;
}
const lay = (g, x, y, tile) => (g.tiles[y * g.cols + x] = tile);
const keepers = (g) => [spawn(g, "swordsmen", "blue", 26, 4), spawn(g, "footmen", "red", 27, 9)];

describe("bonus tiles: the data", () => {
  it("twenty-five tiles after Episode II's 260, nineteen terrain types after its 30, each with a row, a name and a rule", () => {
    const movement = json("movement.json"),
      terrain = json("terrain.json");
    expect([movement.types.length, terrain.count, json("terrain-types.json").types.length]).toEqual([285, 285, 285]);
    expect([movement.rows.length, movement.def.length, movement.heal.length]).toEqual([49, 49, 49]);
    expect(movement.types.slice(0, 260)).toEqual(json("terrain-types.json").types.slice(0, 260)); // the originals: untouched
    for (const [key, type] of Object.entries(TILE)) {
      expect(moveRow(type), key).toHaveLength(5);
      expect(TILE_HELP[type], key).toBeTruthy();
      expect(movement.names[type], key).toBeTruthy();
    }
    expect(Object.values(TILE).sort((a, b) => a - b)).toEqual(Array.from({ length: 19 }, (_, i) => 30 + i));
    expect([ID.north, ID.east, ID.south, ID.west].map(moveType)).toEqual([30, 30, 30, 30]);
    expect([tileName(ID.ice), tileName(ID.ash), tileName(ID.ruinsCleared)]).toEqual([
      "Black ice",
      "Ash",
      "Cleared ruins",
    ]);
    expect([moveType(ID.ash), moveType(ID.ruinsCleared)]).toEqual([2, 15]); // open ground, rubble
    // the Chinampa heals by the original's own table; the Tar Pit and Razor Coral cost cover by it
    expect([tileProp(ID.chinampa).heal, tileProp(ID.tar).defBonus, tileProp(ID.coral).defBonus]).toEqual([
      10, -0.1, -0.2,
    ]);
  });
  it("who may enter: no one a monolith or the ruins, no horse or engine tar and bamboo, fliers everything", () => {
    const g = field();
    const foot = spawn(g, "footmen", "blue", 4, 3),
      horse = spawn(g, "cavalry", "blue", 4, 4),
      engine = spawn(g, "catapult", "blue", 4, 5),
      flier = spawn(g, "griffon", "blue", 4, 6);
    const cost = (tile) => {
      lay(g, 8, 5, tile);
      return [foot, horse, engine, flier].map((u) => g.moveCost(u, 8, 5));
    };
    expect(cost(ID.monolith)).toEqual([99, 99, 99, 1]);
    expect(cost(ID.ruins)).toEqual([99, 99, 99, 1]);
    expect(cost(ID.tar)).toEqual([2, 99, 99, 1]);
    expect(cost(ID.bamboo)).toEqual([2, 99, 99, 1]);
    expect(cost(ID.muck)).toEqual([2, 2, 3, 1]);
    expect(cost(ID.chinampa)).toEqual([2, 2, 99, 1]);
    expect(cost(ID.cenote)).toEqual([2, 2, 99, 1]);
    // a faction on its own ground
    expect(g.moveCost(spawn(g, "raptor", "blue", 5, 3), 8, 5)).toBe(2); // (a cenote)
    lay(g, 8, 5, ID.tar);
    expect(g.moveCost(spawn(g, "raptor", "blue", 5, 4), 8, 5)).toBe(1);
    lay(g, 8, 5, ID.muck);
    expect(g.moveCost(spawn(g, "scuttler", "blue", 5, 5), 8, 5)).toBe(1);
  });
});

describe("bonus tiles: the three factions' ground", () => {
  it("Conveyor Belt: as the round ends, what stands on a belt is carried a tile along it — a full belt as one", () => {
    const g = field();
    keepers(g);
    for (const x of [5, 6, 7]) lay(g, x, 5, ID.east);
    lay(g, 5, 7, ID.north);
    const front = spawn(g, "footmen", "blue", 7, 5),
      behind = spawn(g, "footmen", "blue", 6, 5),
      flier = spawn(g, "griffon", "blue", 5, 5),
      brute = spawn(g, "behemoth", "blue", 5, 7); // Immovable
    nextRound(g);
    expect([front.tx, behind.tx, flier.tx, brute.ty]).toEqual([8, 7, 5, 7]);
    // a tile that is taken stops the belt
    const g2 = field();
    lay(g2, 6, 5, ID.east);
    const rider = spawn(g2, "footmen", "blue", 6, 5);
    spawn(g2, "footmen", "red", 7, 5);
    g2._conveyorTurn();
    expect(rider.tx).toBe(6);
  });
  it("Vent Grate: no shot can be aimed across the steam; a war engine lobs over it", () => {
    const g = field();
    lay(g, 7, 5, ID.vent);
    const archers = spawn(g, "archers", "blue", 5, 5),
      beyond = spawn(g, "footmen", "red", 9, 5),
      open = spawn(g, "footmen", "red", 5, 3),
      catapult = spawn(g, "catapult", "blue", 4, 5);
    expect(g.targetsFrom(archers, archers.tx, archers.ty)).toEqual([open]);
    expect(g.targetsFrom(catapult, catapult.tx, catapult.ty)).toContain(beyond);
    expect(g._shotBlocked(archers, 5, 5, 7, 5)).toBe(false); // a unit standing ON the vent can be shot
    expect(g.moveCost(archers, 7, 5)).toBe(1);
  });
  it("Abyssal Muck and Thermal Chimney: one lets 25% more of a shot through, the other turns 30% and burns", () => {
    const g = field();
    const archers = spawn(g, "archers", "blue", 5, 3),
      foe = spawn(g, "footmen", "red", 5, 6),
      sword = spawn(g, "swordsmen", "blue", 4, 6);
    const [shot, blow] = [g._damage256(archers, foe), g._damage256(sword, foe)];
    lay(g, 5, 6, ID.muck);
    expect(g._damage256(archers, foe)).toBe(Math.trunc((shot * 125) / 100));
    expect(g._damage256(sword, foe)).toBe(blow);
    foe.T = UNIT_TYPES.scuttler; // the Trench Brood is at home in it
    const crabShot = g._damage256(archers, foe);
    lay(g, 5, 6, 133);
    expect(g._damage256(archers, foe)).toBe(crabShot);
    foe.T = UNIT_TYPES.footmen;
    lay(g, 5, 6, ID.chimney);
    expect(g._damage256(archers, foe)).toBe(Math.trunc((shot * 70) / 100));
    g._tileTurnStart(foe);
    expect(foe.hp).toBe(100 - TILE_RULE.chimneyBurn);
  });
  it("Tar Pit: a unit on foot stops in it and cannot move on its next turn; a Saurian runs through", () => {
    const g = field();
    keepers(g);
    lay(g, 6, 5, ID.tar);
    const foot = spawn(g, "footmen", "blue", 5, 5),
      raptor = spawn(g, "raptor", "blue", 5, 6);
    expect(g.computeReach(foot).dist.get("7,5")).toBeGreaterThan(2); // not through it: the way round
    expect(g.computeReach(raptor).dist.get("7,5")).toBeLessThanOrEqual(3);
    moveTo(g, foot, 6, 5);
    expect([foot.tx, foot._snareNext, g.moveOf(foot)]).toEqual([6, true, foot.T.move]);
    nextRound(g);
    expect(g.moveOf(foot)).toBe(0); // its next turn
    nextRound(g);
    expect(g.moveOf(foot)).toBe(foot.T.move);
  });
  it("Giant Fern Canopy: a unit under it is hidden until an enemy steps beside it", () => {
    const g = field();
    keepers(g);
    lay(g, 6, 5, ID.fern);
    const lurker = spawn(g, "footmen", "blue", 5, 5),
      archers = spawn(g, "archers", "red", 6, 3);
    expect(g._canHideUnit(lurker)).toBe(false);
    moveTo(g, lurker, 6, 5); // it hides as it arrives: nobody stands beside it
    expect([g._canHideUnit(lurker), g._isHidden(lurker)]).toEqual([true, true]);
    expect(g.targetsFrom(archers, archers.tx, archers.ty)).toEqual([]);
    archers.tx = 6;
    archers.ty = 4; // beside it
    g._endTurnHide([lurker]);
    expect(g._isHidden(lurker)).toBe(false);
  });
});

describe("bonus tiles: the older regions", () => {
  it("Black Ice: a unit that steps on slides on the way it came, off the far side — or into whatever stands there", () => {
    const g = field();
    keepers(g);
    for (const x of [6, 7, 8]) lay(g, x, 5, ID.ice);
    const slider = spawn(g, "footmen", "blue", 5, 5);
    moveTo(g, slider, 6, 5);
    expect([slider.tx, slider.ty, slider.hp]).toEqual([9, 5, 100]);
    // a unit in the way: both are hurt, and the slider stops short
    for (const x of [6, 7, 8]) lay(g, x, 7, ID.ice);
    const second = spawn(g, "footmen", "blue", 5, 7),
      wall = spawn(g, "footmen", "red", 8, 7);
    moveTo(g, second, 6, 7);
    expect([second.tx, second.hp, wall.hp]).toEqual([7, 100 - TILE_RULE.iceBump, 100 - TILE_RULE.iceBump]);
    // nobody walks on through the ice, and a flier does not slide
    expect(g._tileStops(second, 6, 5)).toBe(true);
    const griffon = spawn(g, "griffon", "blue", 5, 3);
    lay(g, 6, 3, ID.ice);
    moveTo(g, griffon, 6, 3);
    expect(griffon.tx).toBe(6);
  });
  it("Runic Monolith: every unit on the eight tiles around it mends 5 HP a turn", () => {
    const g = field();
    lay(g, 7, 5, ID.monolith);
    const beside = spawn(g, "footmen", "blue", 6, 4, { hp: 50 }), // diagonal
      apart = spawn(g, "footmen", "blue", 5, 5, { hp: 50 });
    g.healOnKeeps("blue");
    expect([beside.hp, apart.hp]).toEqual([50 + TILE_RULE.monolithMend, 50]);
  });
  it("Quicksand Sinkhole: the turn after falling in goes on climbing out — one tile, and no attack", () => {
    const g = field();
    keepers(g);
    lay(g, 6, 5, ID.sinkhole);
    const foot = spawn(g, "footmen", "blue", 5, 5),
      foe = spawn(g, "archers", "red", 6, 6);
    moveTo(g, foot, 6, 5);
    expect([foot.tx, foot.hp]).toEqual([6, 100]); // no damage
    foe.tx = 20; // (out of the way of the enemy's turn)
    nextRound(g);
    foe.tx = 6;
    expect([foot._sunk, g.moveOf(foot), g.targetsFrom(foot, 6, 5)]).toEqual([true, 1, []]);
    nextRound(g);
    foot.tx = 5; // climbed out
    g._endTurnHide([foot]);
    expect(g.moveOf(foot)).toBe(foot.T.move);
    const siren = spawn(g, "dunesirens", "blue", 6, 5),
      griffon = spawn(g, "griffon", "blue", 7, 7);
    expect([g._tileStops(siren, 6, 5), g._tileStops(griffon, 6, 5)]).toEqual([false, false]);
  });
  it("Mirage Sand: every shot at a unit on it does half; a blow hand to hand does all", () => {
    const g = field();
    const archers = spawn(g, "archers", "blue", 5, 3),
      sword = spawn(g, "swordsmen", "blue", 4, 6),
      foe = spawn(g, "footmen", "red", 5, 6);
    const [shot, blow] = [g._damage256(archers, foe), g._damage256(sword, foe)];
    lay(g, 5, 6, ID.mirage);
    expect([g._damage256(archers, foe), g._damage256(sword, foe)]).toEqual([Math.trunc(shot / 2), blow]);
  });
  it("Sacrificial Altar Steps: whoever strikes a unit down on them is healed 20 HP", () => {
    const g = field();
    lay(g, 6, 5, ID.altar);
    const killer = spawn(g, "swordsmen", "blue", 5, 5, { hp: 50 }),
      victim = spawn(g, "archers", "red", 6, 5, { hp: 1 }),
      other = spawn(g, "archers", "red", 5, 6, { hp: 1 });
    g.resolveDamage(killer, victim, {});
    expect([victim.dead, killer.hp]).toEqual([true, 50 + TILE_RULE.altarTithe]);
    g.resolveDamage(killer, other, {}); // off the steps: nothing
    expect(killer.hp).toBe(70);
  });
  it("Overgrown Jungle Ruins: a wall any weapon can bring down, in two stages, to rough open ground", () => {
    const g = field();
    lay(g, 6, 5, ID.ruins);
    const sword = spawn(g, "swordsmen", "blue", 5, 5);
    expect([g.isStructure(6, 5), g.canHitStructure(sword, 6, 5), g.moveCost(sword, 6, 5)]).toEqual([true, true, 99]);
    expect(structTrans(ID.ruins)).toBe(ID.ruinsBroken);
    let blows = 0;
    while (g.tileAt(6, 5) !== ID.ruinsCleared && blows < 12) {
      g.structureHit(sword, 6, 5);
      blows++;
    }
    expect(blows).toBeGreaterThan(1);
    expect(blows).toBeLessThan(12);
    // (rubble: 2 for a Formation unit, as the original's breached walls)
    expect([g.tileAt(6, 5), g.razed.has("6,5"), g.moveCost(sword, 6, 5)]).toEqual([ID.ruinsCleared, true, 2]);
    // the Tyrant needs one bite
    lay(g, 6, 7, ID.ruins);
    g.structureHit(spawn(g, "tyrant", "blue", 5, 7), 6, 7);
    expect(g.tileAt(6, 7)).toBe(ID.ruinsCleared);
  });
  it("Razor Coral: every tile of it crossed costs 5 HP — but not the people of the reef, nor the Trench Brood", () => {
    const g = field();
    keepers(g);
    for (const x of [6, 7]) for (const y of [3, 5, 7]) lay(g, x, y, ID.coral);
    const archers = spawn(g, "archers", "blue", 5, 5),
      toa = spawn(g, "toa", "blue", 5, 3),
      crab = spawn(g, "scuttler", "blue", 5, 7);
    expect(g.moveCost(spawn(g, "cavalry", "blue", 4, 4), 6, 5)).toBe(3); // shallows to a horse
    moveTo(g, archers, 7, 5); // two tiles of it
    expect([archers.tx, archers.hp]).toEqual([7, 100 - 2 * TILE_RULE.coralCut]);
    moveTo(g, toa, 6, 3);
    moveTo(g, crab, 6, 7);
    expect([toa.hp, crab.hp]).toEqual([100, 100]);
  });
  it("Cenote: a unit in one dives and comes up in any other that is free", () => {
    const g = field();
    keepers(g);
    lay(g, 6, 5, ID.cenote);
    lay(g, 12, 7, ID.cenote);
    lay(g, 12, 3, ID.cenote);
    spawn(g, "footmen", "red", 12, 3); // that one is taken
    const diver = spawn(g, "footmen", "blue", 5, 5);
    moveTo(g, diver, 6, 5);
    expect(g._cenoteExits(diver)).toEqual([{ x: 12, y: 7 }]);
    diver.acted = false; // (with no foe in reach its turn ended where it stopped)
    g.select(diver);
    expect(g.aimSkills().map((skill) => skill.id)).toContain("dive");
    g.aimSkill("dive");
    g.click({ tx: 12, ty: 7 });
    settle(g);
    expect([diver.tx, diver.ty, g._cenoteExits(diver)]).toEqual([12, 7, []]); // once a turn
    expect(g._tileStops(diver, 6, 5)).toBe(true);
  });
  it("Astral Glyph: a shot from it reaches 2 tiles farther, and one aimed back does a quarter more", () => {
    const g = field();
    const archers = spawn(g, "archers", "blue", 5, 5),
      far = spawn(g, "archers", "red", 13, 5); // 8 away: a Longbow reaches 6
    expect(g.targetsFrom(archers, 5, 5)).toEqual([]);
    const back = g._damage256(far, { ...archers, T: archers.T, tx: 7, ty: 5 });
    lay(g, 5, 5, ID.glyph);
    expect(g.targetsFrom(archers, 5, 5)).toEqual([far]);
    far.tx = 7;
    expect(g._damage256(far, archers)).toBeGreaterThan(0);
    lay(g, 5, 5, 133);
    const plain = g._damage256(far, archers);
    lay(g, 5, 5, ID.glyph);
    expect(g._damage256(far, archers)).toBe(Math.trunc((plain * 125) / 100));
    expect(back).toBeGreaterThan(0);
    // a sword gains nothing from it
    const sword = spawn(g, "swordsmen", "blue", 5, 7);
    lay(g, 5, 7, ID.glyph);
    spawn(g, "footmen", "red", 7, 7);
    expect(g.targetsFrom(sword, 5, 7)).toEqual([]);
  });
  it("Chinampa: a unit that starts its turn on one mends 10 HP", () => {
    const g = field();
    lay(g, 6, 5, ID.chinampa);
    const hurt = spawn(g, "footmen", "blue", 6, 5, { hp: 50 });
    g.healOnKeeps("blue");
    expect(hurt.hp).toBe(60);
  });
  it("Obsidian Spikes: they cut whoever crosses, and heavy armour shatters on them for the rest of the battle", () => {
    const g = field();
    keepers(g);
    lay(g, 6, 5, ID.obsidian);
    lay(g, 6, 7, ID.obsidian);
    const knights = spawn(g, "spellwardens", "blue", 5, 5), // Heavy Armour & Shield
      light = spawn(g, "archers", "blue", 5, 7),
      foe = spawn(g, "swordsmen", "red", 12, 3);
    const before = g._damage256(foe, knights);
    moveTo(g, knights, 6, 5);
    moveTo(g, light, 6, 7);
    expect([knights.hp, knights._shattered, light.hp, !!light._shattered]).toEqual([
      100 - TILE_RULE.obsidianCut,
      true,
      100 - TILE_RULE.obsidianCut,
      false,
    ]);
    knights.hp = 100;
    lay(g, 6, 5, 133);
    expect(g._damage256(foe, knights)).toBeGreaterThan(before);
  });
  it("Bamboo Thicket: troops on foot take 40% less from a shot; fire burns it to ash and scorches who is inside", () => {
    const g = field();
    lay(g, 5, 6, ID.bamboo);
    const crossbow = spawn(g, "crossbowmen", "blue", 5, 3),
      foe = spawn(g, "footmen", "red", 5, 6);
    lay(g, 5, 6, 133);
    const open = g._damage256(crossbow, foe);
    lay(g, 5, 6, ID.bamboo);
    expect(g._damage256(crossbow, foe)).toBe(Math.trunc((open * 60) / 100));
    g.resolveDamage(crossbow, foe, {}); // a bolt is no fire
    expect(g.tileAt(5, 6)).toBe(ID.bamboo);
    const hpBefore = foe.hp;
    const wizard = spawn(g, "wizards", "blue", 9, 6);
    g.resolveDamage(wizard, foe, {}); // a Fireball is
    expect(g.tileAt(5, 6)).toBe(ID.ash);
    expect(foe.hp).toBeLessThan(hpBefore - TILE_RULE.bambooBurn + 1);
    expect(g.moveCost(spawn(g, "cavalry", "blue", 4, 4), 5, 6)).toBe(1); // open ground now
  });
  it("Zen Sand Garden: stepping in clears every ailment, and nothing drags a unit out of it", () => {
    const g = field();
    keepers(g);
    lay(g, 6, 5, ID.zen);
    const monk = spawn(g, "footmen", "blue", 5, 5, { _acid: { turns: 3, by: null }, _blind: true, _shattered: true });
    moveTo(g, monk, 6, 5);
    expect([monk._acid, monk._blind, monk._shattered]).toEqual([null, false, false]);
    const siren = spawn(g, "siren", "red", 9, 5),
      tengu = spawn(g, "tengu", "red", 6, 4);
    expect(g._lureTarget(siren, monk)).toBe(false);
    g.resolveDamage(tengu, monk, {});
    expect([monk.tx, monk.ty]).toEqual([6, 5]);
  });
});
