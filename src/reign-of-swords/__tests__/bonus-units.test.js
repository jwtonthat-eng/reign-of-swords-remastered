// The six BONUS units (Tilicia & Isoluccia — ours, data/bonus-units.js) and their abilities: Climb, Nullify,
// Unyielding, Amphibious, Pavise and Chain Lightning. Played on Episode II's own maps.
import { describe, it, expect } from "vitest";
import { loadEpisode, makeGame, startBattle, spawn, only, settle } from "./battle.js";
import { UNIT_TYPES, DEPLOY_COST } from "../data/game-data.js";
import { WEAPON_DMG, UNIT_COMBAT } from "../data/combat-data.js";
import { BONUS_ORDER, BONUS_WEAPONS, BONUS_UPGRADES } from "../data/bonus-units.js";
import { UNIT_META, unitSkills, upgradeOffered, upgradeGate, bonusOpen, UPGRADE_FROM } from "../data/shell-data.js";
import { DEPLOY_ELITE, DEPLOY_ORDER } from "../data/missions.js";
import { moveType } from "../rules/terrain.js";

await loadEpisode(2);

// a clean board on Zayandi Shores' open sand (5424): only the units a test sets down
function field() {
  const g = startBattle(makeGame(5424));
  only(g);
  return g;
}
// the first tile of terrain type `type` with a walkable neighbour: [tile, neighbour]
function edgeTile(g, type) {
  for (let y = 1; y < g.rows - 1; y++)
    for (let x = 1; x < g.cols - 1; x++) {
      if (moveType(g.tileAt(x, y)) !== type) continue;
      for (const [dx, dy] of [
        [1, 0],
        [-1, 0],
        [0, 1],
        [0, -1],
      ])
        if ([2, 26].includes(moveType(g.tileAt(x + dx, y + dy))))
          return [
            [x, y],
            [x + dx, y + dy],
          ];
    }
  return null;
}

describe("bonus units: the data", () => {
  it("six units, each on an original weapon row and armour column, with a cost and a courage tier", () => {
    expect(BONUS_ORDER).toEqual(["cragsmen", "spellwardens", "sentinel", "marines", "pavisiers", "battlemage"]);
    for (const k of BONUS_ORDER) {
      const T = UNIT_TYPES[k];
      expect(T.bonus).toBe(true);
      expect(DEPLOY_COST[k]).toBeGreaterThan(0);
      expect(T.courage).toBeGreaterThanOrEqual(2);
      expect(UNIT_COMBAT[k].armour).toBeLessThanOrEqual(15);
      expect(DEPLOY_ORDER).toContain(k);
    }
    for (const [id, w] of Object.entries(BONUS_WEAPONS)) expect(WEAPON_DMG[id]).toEqual(WEAPON_DMG[w.row]);
    expect(DEPLOY_ELITE.battlemage && DEPLOY_ELITE.sentinel).toBe(true);
    expect(DEPLOY_ELITE.cragsmen).toBeUndefined();
  });
  it("the original units' records are untouched", () => {
    expect(UNIT_COMBAT.footmen).toMatchObject({ weapon: 3, armour: 6, rating: 2 });
    expect(Object.keys(WEAPON_DMG).filter((w) => w <= 34).length).toBe(34);
    expect(UNIT_TYPES.footmen.bonus).toBeUndefined();
  });
  it("each has its ability as a skill pill with an icon", () => {
    const skill = (k) => unitSkills(k).map((s) => s.n);
    expect(skill("cragsmen")).toContain("Climb");
    expect(skill("spellwardens")).toContain("Nullify");
    expect(skill("sentinel")).toEqual(expect.arrayContaining(["Unyielding", "Fear", "Last Strike", "Fearless"]));
    expect(skill("marines")).toContain("Amphibious");
    expect(skill("pavisiers")).toEqual(expect.arrayContaining(["Pavise", "Formation", "Move or Shoot"]));
    expect(skill("battlemage")).toEqual(expect.arrayContaining(["Chain Lightning", "Battle Standard", "Fear"]));
  });
});

describe("bonus units: upgrade paths", () => {
  it("each hangs off an original unit in a collectible slot that unit left empty, behind a bonus battle", () => {
    expect(BONUS_UPGRADES.map((u) => [u.from, u.to, u.need])).toEqual([
      ["archers", "cragsmen", "Armor"],
      ["swordsmen", "spellwardens", "Lore"],
      ["craftsmen", "sentinel", "Spirit"],
      ["footmen", "marines", "Spirit"],
      ["crossbowmen", "pavisiers", "Armor"],
      ["wizards", "battlemage", "Medal"],
    ]);
    for (const { from, to, need, gate } of BONUS_UPGRADES) {
      const branches = UNIT_META[from].upgrades;
      expect(branches.filter((b) => b.need === need).length).toBe(1); // one branch per collectible
      expect(UPGRADE_FROM[to]).toEqual({ from, need });
      expect(upgradeGate(to, true)).toBe(gate);
      expect(upgradeGate(to, false)).toBeNull();
    }
  });
  it("the branches are offered only in Episode II, and only once the bonus campaigns are open", () => {
    const branch = UNIT_META.archers.upgrades.find((b) => b.to === "cragsmen");
    expect(upgradeOffered(branch, false, false)).toBe(false);
    expect(upgradeOffered(branch, true, false)).toBe(false);
    expect(upgradeOffered(branch, true, true)).toBe(true);
    const original = UNIT_META.archers.upgrades.find((b) => b.to === "crossbowmen");
    expect(upgradeOffered(original, false)).toBe(true);
    expect(bonusOpen(true, new Set([5431]))).toBe(false);
    expect(bonusOpen(true, new Set([5432]))).toBe(true);
    expect(bonusOpen(false, new Set([5432]))).toBe(false);
  });
});

describe("Climb and Amphibious", () => {
  it("Cragsmen cross cliffs at 2 a tile; nobody else on the ground does", () => {
    const g = startBattle(makeGame(5430)); // Dune with a View: rock ridges
    const [[cx, cy], [nx, ny]] = edgeTile(g, 21);
    const crag = spawn(g, "cragsmen", "blue", nx, ny),
      foot = spawn(g, "footmen", "blue", nx, ny);
    expect(g.moveCost(crag, cx, cy, nx, ny)).toBe(2);
    expect(g.moveCost(foot, cx, cy, nx, ny)).toBe(99);
    expect(g.moveCost(spawn(g, "marines", "blue", nx, ny), cx, cy, nx, ny)).toBe(99);
  });
  it("Marines wade deep water at 2 a tile, and cannot attack while standing in it", () => {
    const g = startBattle(makeGame(5424)); // Zayandi Shores: the sea
    const [[wx, wy], [nx, ny]] = edgeTile(g, 19);
    only(g);
    const marine = spawn(g, "marines", "blue", wx, wy),
      foe = spawn(g, "footmen", "red", nx, ny);
    expect(g.moveCost(marine, wx, wy)).toBe(2);
    expect(g.moveCost(foe, wx, wy)).toBe(99);
    expect(g.targetsFrom(marine, wx, wy)).toEqual([]);
    expect(g.targetsFrom(foe, nx, ny)).toContain(marine); // …but it can be struck there
    const ashore = spawn(g, "marines", "blue", nx, ny); // (moves the footman aside) — on land it fights as usual
    foe.tx = wx;
    foe.ty = wy;
    marine.dead = true;
    expect(g.targetsFrom(ashore, nx, ny)).toContain(foe);
  });
});

describe("Nullify (Spellwardens)", () => {
  it("enemy spells deal nothing within 2 tiles of a Spellwarden — and full damage beyond", () => {
    const g = field();
    const wizard = spawn(g, "wizards", "red", 5, 5),
      warden = spawn(g, "spellwardens", "blue", 10, 5),
      near = spawn(g, "footmen", "blue", 10, 7),
      far = spawn(g, "footmen", "blue", 10, 8);
    for (const weapon of [25, 26, 27, 36]) {
      expect(g.computeDamage(wizard, warden, { weapon })).toBe(0);
      expect(g.computeDamage(wizard, near, { weapon })).toBe(0);
      expect(g.computeDamage(wizard, far, { weapon })).toBeGreaterThan(0);
    }
    expect(g.computeDamage(wizard, near, { weapon: 16 })).toBeGreaterThan(0); // an arrow is no spell
    warden.dead = true;
    expect(g.computeDamage(wizard, near, { weapon: 25 })).toBeGreaterThan(0);
  });
  it("a friendly wizard's own blast still burns them, an enemy Shroud saps nothing, quicksand lets them pass", () => {
    const g = field();
    const warden = spawn(g, "spellwardens", "blue", 10, 5),
      ally = spawn(g, "footmen", "blue", 10, 6),
      mage = spawn(g, "wizards", "blue", 4, 5),
      shaman = spawn(g, "shamans", "red", 12, 6),
      lone = spawn(g, "footmen", "blue", 15, 6);
    expect(g.computeDamage(mage, ally, { weapon: 25 })).toBeGreaterThan(0);
    expect(g._auraFlags(ally).shroud).toBe(false);
    expect(g._auraFlags(lone).shroud).toBe(true);
    expect(g._quicksandImmune(ally)).toBe(true);
    expect(g._quicksandImmune(lone)).toBe(false);
    expect(g._statusesOf(ally).map((s) => s.name)).toContain("Warded");
    expect(shaman.dead).toBeFalsy();
    expect(warden.T.nullify).toBe(true);
  });
});

describe("Pavise (Pavisiers)", () => {
  it("planted, they and the friendly unit directly behind take half ranged damage; melee is unchanged", () => {
    const g = field();
    const archer = spawn(g, "archers", "red", 5, 5),
      pav = spawn(g, "pavisiers", "blue", 9, 5),
      behind = spawn(g, "militiamen", "blue", 10, 5),
      beside = spawn(g, "militiamen", "blue", 9, 8);
    const open = g.computeDamage(archer, beside),
      covered = g.computeDamage(archer, behind);
    expect(covered).toBeLessThan(open);
    expect(covered).toBeGreaterThanOrEqual(Math.floor(open / 2) - 1);
    const planted = g.computeDamage(archer, pav);
    pav.planted = false; // it moved on its last turn
    expect(g.computeDamage(archer, pav)).toBeGreaterThan(planted);
    expect(g.computeDamage(archer, behind)).toBe(open);
    pav.planted = true;
    const sword = spawn(g, "swordsmen", "red", 9, 4);
    const blow = g.computeDamage(sword, pav);
    pav.planted = false;
    expect(g.computeDamage(sword, pav)).toBe(blow);
  });
  it("is planted by ending a turn without moving", () => {
    const g = field();
    const still = spawn(g, "pavisiers", "blue", 9, 5),
      mover = spawn(g, "pavisiers", "blue", 9, 8);
    mover._movedTurn = g.turn;
    g._endTurnBrace([still, mover]);
    expect(still.planted).toBe(true);
    expect(mover.planted).toBe(false);
    expect(g._statusesOf(still).map((s) => s.name)).toContain("Pavise planted");
  });
});

describe("Chain Lightning (Battlemage)", () => {
  it("hits the target in full, then leaps to up to two adjacent enemies at half strength — never to friends", () => {
    const g = field();
    const mage = spawn(g, "battlemage", "blue", 5, 5),
      target = spawn(g, "footmen", "red", 9, 5),
      a = spawn(g, "footmen", "red", 10, 5),
      b = spawn(g, "footmen", "red", 9, 6),
      c = spawn(g, "footmen", "red", 9, 4),
      friend = spawn(g, "footmen", "blue", 8, 5),
      away = spawn(g, "footmen", "red", 12, 5);
    c.hp = 100;
    a.hp = 60; // the weakest neighbours are struck first
    b.hp = 70;
    const full = g.computeDamage(mage, target);
    expect(g._weaponAt(mage, 4)).toBe(36);
    g.resolveDamage(mage, target, {});
    settle(g);
    for (let i = 0; i < 40; i++) g.update(0.05);
    expect(100 - target.hp).toBe(full);
    expect(60 - a.hp).toBeGreaterThan(0);
    expect(60 - a.hp).toBeLessThan(full);
    expect(70 - b.hp).toBeGreaterThan(0);
    expect(c.hp).toBe(100); // only two leaps
    expect(friend.hp).toBe(100);
    expect(away.hp).toBe(100);
  });
  it("up close the Battlemage swings its Runesword, with no leap", () => {
    const g = field();
    const mage = spawn(g, "battlemage", "blue", 5, 5),
      target = spawn(g, "footmen", "red", 6, 5),
      next = spawn(g, "footmen", "red", 7, 5);
    expect(g._weaponAt(mage, 1)).toBe(6);
    g.resolveDamage(mage, target, {});
    for (let i = 0; i < 40; i++) g.update(0.05);
    expect(next.hp).toBe(100);
    expect(target.hp).toBeLessThan(100);
  });
});

describe("Unyielding (Stone Sentinel)", () => {
  it("feels no Fear, ignores quicksand, cannot be healed by a Priest, and Craftsmen can repair it", () => {
    const g = field();
    const sentinel = spawn(g, "sentinel", "blue", 8, 5),
      priest = spawn(g, "priests", "blue", 8, 6),
      crafts = spawn(g, "craftsmen", "blue", 9, 5),
      griffon = spawn(g, "griffon", "red", 8, 4);
    sentinel.hp = 50;
    expect(g._needsCourage(sentinel, griffon)).toBe(false);
    expect(g._needsCourage(priest, sentinel)).toBe(true); // …and it causes Fear itself
    expect(g._quicksandImmune(sentinel)).toBe(true);
    expect(g._canHealNow(priest)).toBe(false);
    g.selected = priest;
    expect(g._clickHeal(sentinel)).toBe(false);
    expect(g._repairTargetFor(crafts)).toBe(sentinel);
  });
});
