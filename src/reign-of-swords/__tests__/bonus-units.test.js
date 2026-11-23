// The six BONUS units (Tilicia & Isoluccia — ours, data/bonus-units.js) and their abilities: Climb, Nullify,
// Unyielding, Amphibious, Pavise and Chain Lightning. Played on Episode II's own maps.
import { describe, it, expect } from "vitest";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { loadEpisode, makeGame, startBattle, spawn, only, settle, step, nextRound } from "./battle.js";
import { UNIT_TYPES, DEPLOY_COST } from "../data/game-data.js";
import { WEAPON_DMG, UNIT_COMBAT } from "../data/combat-data.js";
import {
  BONUS_ORDER,
  BONUS_WEAPONS,
  BONUS_UPGRADES,
  BONUS_UPGRADES_ALL,
  BONUS_HIDDEN,
  BONUS_FORMS,
} from "../data/bonus-units.js";
import {
  UNIT_META,
  unitSkills,
  upgradeOffered,
  upgradeGate,
  bonusOpen,
  UPGRADE_FROM,
  COLLECTIBLES,
  TRADE_GOODS,
  RES_ICON,
  NEED_COLOR,
} from "../data/shell-data.js";
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
  it("forty-nine units on offer (four more are hidden), each on an original weapon row and armour column, with a cost and a courage tier", () => {
    expect(BONUS_ORDER).toEqual([
      "cragsmen",
      "spellwardens",
      "sentinel",
      "marines",
      "pavisiers",
      "battlemage",
      "gladiator",
      "samurai",
      "dragonrider",
      "beastmaster",
      "sohei",
      "shinobi",
      "oni",
      "tengu",
      "alchemist",
      "golem",
      "jaguar",
      "eagle",
      "sunpriest",
      "serpent",
      "berserker",
      "shieldmaiden",
      "einherjar",
      "jotunn",
      "medjay",
      "khopesh",
      "anubis",
      "ammit",
      "toa",
      "tahuanui",
      "tohunga",
      "taniwha",
      "coatecpatl",
      "ahuizotl",
      "chieftain",
      "tzitzimitl",
      "warden",
      // the three factions (their own tests: faction-units.test.js)
      "scuttler",
      "siren",
      "brinehurler",
      "behemoth",
      "phalanx",
      "arccaster",
      "gyrocopter",
      "automaton",
      "raptor",
      "ankylosaur",
      "pterosaur",
      "tyrant",
    ]);
    for (const k of BONUS_ORDER) {
      const T = UNIT_TYPES[k];
      expect(T.bonus).toBe(true);
      expect(DEPLOY_COST[k]).toBeGreaterThan(0);
      expect(T.courage).toBeGreaterThanOrEqual(2);
      expect(UNIT_COMBAT[k].armour).toBeLessThanOrEqual(15);
      expect(DEPLOY_ORDER).toContain(k);
    }
    for (const [id, w] of Object.entries(BONUS_WEAPONS))
      expect(WEAPON_DMG[id]).toEqual(Object.assign(WEAPON_DMG[w.row].slice(), w.patch || {})); // (Dragonfire patches one cell)
    expect(DEPLOY_ELITE.battlemage && DEPLOY_ELITE.dragonrider).toBe(true);
    expect(DEPLOY_ELITE.sentinel).toBeUndefined(); // the Stone Sentinel is no elite
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
    expect(skill("sentinel")).toEqual(expect.arrayContaining(["Unyielding", "Fear", "Bulwark", "Fearless"]));
    expect(skill("marines")).toEqual(expect.arrayContaining(["Amphibious", "Boarding Musket", "Move or Shoot"]));
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
      ["crossbowmen", "pavisiers", "Armor"],
      ["wizards", "battlemage", "Medal"],
      ["footmen", "marines", "Anchor"],
      ["swordsmen", "gladiator", "Anchor"],
      ["raiders", "beastmaster", "Anchor"],
      ["halberdiers", "sohei", "Tsuba"],
      ["footmen", "samurai", "Tsuba"],
      ["rangers", "shinobi", "Tsuba"],
      ["samurai", "oni", "Tsuba"],
      ["beastmaster", "tengu", "Tsuba"],
      ["cavalry", "dragonrider", "Void"],
      ["shamans", "alchemist", "Void"],
      ["craftsmen", "golem", "Void"],
      ["druids", "warden", "Void"],
      ["militiamen", "jaguar", "Jade"],
      ["archers", "eagle", "Jade"],
      ["cavalry", "serpent", "Jade"],
      ["priests", "sunpriest", "Jade"],
      ["militiamen", "berserker", "Bloodstone"],
      ["footmen", "shieldmaiden", "Bloodstone"],
      ["shieldmaiden", "einherjar", "Bloodstone"],
      ["berserker", "jotunn", "Bloodstone"],
      ["archers", "medjay", "Scarab"],
      ["swordsmen", "khopesh", "Scarab"],
      ["shamans", "anubis", "Scarab"],
      ["dunesirens", "ammit", "Scarab"],
      ["militiamen", "toa", "Whalebone"],
      ["raiders", "tahuanui", "Whalebone"],
      ["shamans", "tohunga", "Whalebone"],
      ["dunesirens", "taniwha", "Whalebone"],
      ["jaguar", "coatecpatl", "Obsidian"],
      ["raiders", "ahuizotl", "Obsidian"],
      ["eagle", "chieftain", "Obsidian"],
      ["shamans", "tzitzimitl", "Obsidian"],
      ["footmen", "scuttler", "Pearl"],
      ["dunesirens", "siren", "Pearl"],
      ["crossbowmen", "brinehurler", "Pearl"],
      ["scuttler", "behemoth", "Pearl"],
      ["militiamen", "automaton", "Mainspring"],
      ["halberdiers", "phalanx", "Mainspring"],
      ["crossbowmen", "arccaster", "Mainspring"],
      ["archers", "gyrocopter", "Mainspring"],
      ["raiders", "raptor", "Amber"],
      ["halberdiers", "ankylosaur", "Amber"],
      ["horsebowmen", "pterosaur", "Amber"],
      ["raptor", "tyrant", "Amber"],
    ]);
    // the shape of the tree: at most three upgrades from the Militia, at most four bonus branches on any one unit,
    // and no upgrade cheaper to deploy than the unit it is made from
    const depth = (unit) => (UPGRADE_FROM[unit] ? depth(UPGRADE_FROM[unit].from) + 1 : 0);
    for (const { from, to, need, gate } of BONUS_UPGRADES) {
      expect(depth(to), to).toBeLessThanOrEqual(3);
      expect(BONUS_UPGRADES.filter((u) => u.from === from).length, from).toBeLessThanOrEqual(4);
      expect(DEPLOY_COST[to], to).toBeGreaterThanOrEqual(DEPLOY_COST[from]);
      const branches = UNIT_META[from].upgrades;
      expect(branches.filter((b) => b.need === need).length).toBe(1); // one branch per collectible
      expect(UPGRADE_FROM[to]).toEqual({ from, need });
      expect(upgradeGate(to, true)).toBe(gate);
      expect(upgradeGate(to, false)).toBeNull();
    }
  });
  it("the branches are offered only in Episode II, where the bonus campaigns are open from the start", () => {
    const branch = UNIT_META.archers.upgrades.find((b) => b.to === "cragsmen");
    expect(upgradeOffered(branch, false, false)).toBe(false);
    expect(upgradeOffered(branch, true, false)).toBe(false);
    expect(upgradeOffered(branch, true, true)).toBe(true);
    const original = UNIT_META.archers.upgrades.find((b) => b.to === "crossbowmen");
    expect(upgradeOffered(original, false)).toBe(true);
    expect(bonusOpen(true)).toBe(true);
    expect(bonusOpen(false)).toBe(false);
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
  it("planted, they and the friendly unit directly behind take half ranged damage; in melee a quarter less", () => {
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
    const unplanted = g.computeDamage(sword, pav);
    expect(blow).toBeLessThan(unplanted);
    expect(blow).toBeGreaterThanOrEqual(Math.floor((unplanted * 3) / 4) - 1);
  });
  it("a planted Pavisier's own bolt is braced: 10 stronger on the table than one loosed after a move", () => {
    const g = field();
    const pav = spawn(g, "pavisiers", "blue", 9, 5),
      crossbow = spawn(g, "crossbowmen", "blue", 9, 7),
      foe = spawn(g, "footmen", "red", 13, 5),
      foe2 = spawn(g, "footmen", "red", 13, 7);
    const braced = g.computeDamage(pav, foe);
    pav.planted = false;
    const loose = g.computeDamage(pav, foe);
    expect(braced).toBeGreaterThan(loose);
    expect(loose).toBe(g.computeDamage(crossbow, foe2)); // unbraced it is a plain Crossbow
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
  it("hits the target in full, then leaps on through up to four enemies within 2 tiles of the last — never friends", () => {
    const g = field();
    const mage = spawn(g, "battlemage", "blue", 5, 5),
      target = spawn(g, "footmen", "red", 9, 5),
      a = spawn(g, "footmen", "red", 10, 5),
      b = spawn(g, "footmen", "red", 9, 6),
      c = spawn(g, "footmen", "red", 9, 4),
      friend = spawn(g, "footmen", "blue", 8, 5),
      away = spawn(g, "footmen", "red", 12, 5);
    a.hp = 60; // the nearest unstruck enemy takes each leap; the weakest on a tie
    b.hp = 70;
    const full = g.computeDamage(mage, target);
    expect(g._weaponAt(mage, 4)).toBe(36);
    expect(full).toBeGreaterThan(g.computeDamage(mage, target, { weapon: 25 })); // +10 on the Fireball's row
    g.resolveDamage(mage, target, {});
    settle(g);
    for (let i = 0; i < 40; i++) g.update(0.05);
    expect(100 - target.hp).toBe(full);
    // target → a (beside it, weakest) → b (2 from a, weaker than c) → c (2 from b) → nothing within 2 of c
    const lost = [60 - a.hp, 70 - b.hp, 100 - c.hp];
    expect(lost.every((n) => n > 0 && n < full)).toBe(true);
    expect(lost[0]).toBeGreaterThanOrEqual(lost[1]);
    expect(friend.hp).toBe(100);
    expect(away.hp).toBe(100); // 4 tiles from the last unit struck
  });
  it("the chain runs out after four leaps", () => {
    const g = field();
    const mage = spawn(g, "battlemage", "blue", 5, 5);
    const line = [9, 10, 11, 12, 13, 14].map((x) => spawn(g, "footmen", "red", x, 5));
    g.resolveDamage(mage, line[0], {});
    settle(g);
    for (let i = 0; i < 60; i++) g.update(0.05);
    expect(line.map((u) => u.hp < 100)).toEqual([true, true, true, true, true, false]);
    expect(100 - line[4].hp).toBeLessThan(100 - line[1].hp);
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

describe("Whirl (Gladiators)", () => {
  it("the blow lands on its target in full and spins through every other adjacent enemy at 3/4 — never a friend", () => {
    const g = field();
    const glad = spawn(g, "gladiator", "blue", 8, 5),
      target = spawn(g, "footmen", "red", 9, 5),
      north = spawn(g, "militiamen", "red", 8, 4),
      south = spawn(g, "militiamen", "red", 8, 6),
      friend = spawn(g, "footmen", "blue", 7, 5),
      apart = spawn(g, "militiamen", "red", 10, 5);
    const full = g.computeDamage(glad, target),
      side = g.computeDamage(glad, north);
    g.resolveDamage(glad, target, {});
    expect(100 - target.hp).toBe(full);
    for (const e of [north, south]) {
      expect(100 - e.hp).toBeGreaterThan(0);
      expect(100 - e.hp).toBeLessThan(side);
      expect(100 - e.hp).toBeGreaterThanOrEqual(Math.floor(side * 0.7));
    }
    expect(friend.hp).toBe(100);
    expect(apart.hp).toBe(100);
    expect(unitSkills("gladiator").map((s) => s.n)).toContain("Whirl");
  });
  it("an ordinary swordsman's blow touches nobody else", () => {
    const g = field();
    const sword = spawn(g, "swordsmen", "blue", 8, 5),
      target = spawn(g, "footmen", "red", 9, 5),
      north = spawn(g, "militiamen", "red", 8, 4);
    g.resolveDamage(sword, target, {});
    expect(north.hp).toBe(100);
  });
});

describe("Lesser Shroud (Samurai)", () => {
  it("is a Spirit Shroud that reaches 2 tiles: enemies within 2 lose 15, a Shaman's own still reaches 4", () => {
    const g = field();
    const samurai = spawn(g, "samurai", "blue", 8, 5),
      near = spawn(g, "footmen", "red", 10, 5),
      far = spawn(g, "footmen", "red", 11, 5);
    expect(samurai.T.shroud && samurai.T.shroudRange).toBe(2);
    expect(g._auraFlags(near).shroud).toBe(true);
    expect(g._auraFlags(far).shroud).toBe(false);
    expect(g.ratingAura(near)).toBe(-15);
    const shaman = spawn(g, "shamans", "blue", 8, 6);
    expect(shaman.T.shroudRange).toBe(4);
    expect(g._auraFlags(far).shroud).toBe(true); // 4 from the Shaman
  });
  it("once raised it steadies allies within 2, and the Samurai fights as a swordsman", () => {
    const g = field();
    const samurai = spawn(g, "samurai", "blue", 8, 5),
      beside = spawn(g, "footmen", "blue", 8, 7),
      beyond = spawn(g, "footmen", "blue", 8, 8),
      foe = spawn(g, "footmen", "red", 9, 5);
    expect(g._auraFlags(beside).rally).toBe(false); // not raised yet
    g._shroudEndTurn(samurai); // an enemy is near: the shroud rises
    expect(samurai._shroudOn).toBe(true);
    expect(g._auraFlags(beside).rally).toBe(true);
    expect(g._auraFlags(beyond).rally).toBe(false);
    expect(g.computeDamage(samurai, foe)).toBeGreaterThan(0);
    expect(g._weaponAt(samurai, 1)).toBe(41);
    expect(unitSkills("samurai").map((s) => s.n)).toEqual(["Pike Wall", "Lesser Shroud", "Master Swordsman"]);
  });
});

describe("the units as retuned", () => {
  it("Battlemage: Chain Lightning at 2–6, teleports like a Wizard, strikes first, may attack after moving", () => {
    const g = field();
    const mage = spawn(g, "battlemage", "blue", 5, 5),
      far = spawn(g, "footmen", "red", 11, 5),
      beyond = spawn(g, "footmen", "red", 13, 6);
    expect(mage.T.minRange).toBe(1);
    expect(mage.T.range).toBe(6);
    expect(g.targetsFrom(mage, 5, 5)).toContain(far); // 6 away
    expect(g.targetsFrom(mage, 5, 5)).not.toContain(beyond); // 9 away
    expect(mage.T.teleport).toBe(true);
    expect(mage.T.firstStrike).toBe(true);
    expect(mage.T.shootMove).toBe(true);
    expect(g.targetsFrom(mage, 5, 5, true)).toContain(far); // judged as having moved: it still shoots
    // the blink: an empty tile within its move is a stop even with a wall of foes between
    spawn(g, "footmen", "red", 6, 5);
    spawn(g, "footmen", "red", 5, 4);
    spawn(g, "footmen", "red", 5, 6);
    spawn(g, "footmen", "red", 4, 5);
    expect(g.computeReach(mage).stops.has("7,5")).toBe(true);
    const sword = spawn(g, "swordsmen", "blue", 2, 2);
    for (const [x, y] of [
      [3, 2],
      [1, 2],
      [2, 1],
      [2, 3],
    ])
      spawn(g, "footmen", "red", x, y);
    expect(g.computeReach(sword).stops.has("4,2")).toBe(false); // a walker is boxed in
  });
  it("Marines: a Boarding Musket at 2–3 from open ground, 2 from rough ground, a Sword up close", () => {
    const g = startBattle(makeGame(5430)); // Dune with a View: sand, scrub and boulders
    only(g);
    let open = null,
      rough = null;
    for (let y = 2; y < g.rows - 2 && !(open && rough); y++)
      for (let x = 4; x < g.cols - 4; x++) {
        const type = moveType(g.tileAt(x, y)),
          clear = [1, 2, 3].every((d) => [2, 26].includes(moveType(g.tileAt(x + d, y))));
        if (!open && [2, 26].includes(type) && clear) open = [x, y];
        if (!rough && [3, 22, 27].includes(type)) rough = [x, y];
      }
    const marine = spawn(g, "marines", "blue", open[0], open[1]),
      at2 = spawn(g, "footmen", "red", open[0] + 2, open[1]),
      at3 = spawn(g, "footmen", "red", open[0] + 3, open[1]);
    expect(g._weaponAt(marine, 3)).toBe(39);
    expect(g._weaponAt(marine, 1)).toBe(5);
    expect(g.targetsFrom(marine, open[0], open[1], false)).toEqual(expect.arrayContaining([at2, at3]));
    expect(g.targetsFrom(marine, open[0], open[1], true)).toEqual([]); // Move or Shoot
    // the Musket's row, a rating tier above the Musketeers since the upgrade retune
    expect(g.computeDamage(marine, at3)).toBeGreaterThan(
      g.computeDamage(spawn(g, "musketeers", "blue", open[0], open[1] + 0), at3),
    );
    // from rough ground the same two foes: only the one 2 away
    only(g);
    const scout = spawn(g, "marines", "blue", rough[0], rough[1]),
      near = spawn(g, "footmen", "red", rough[0], rough[1] + 2),
      far = spawn(g, "footmen", "red", rough[0], rough[1] + 3);
    const seen = g.targetsFrom(scout, rough[0], rough[1], false);
    expect(seen).toContain(near);
    expect(seen).not.toContain(far);
  });
  it("Stone Sentinel moves 4; Spellwardens mend 10 HP at the start of their turn", () => {
    expect(UNIT_TYPES.sentinel.move).toBe(4);
    const g = field();
    const warden = spawn(g, "spellwardens", "blue", 8, 5),
      foot = spawn(g, "footmen", "blue", 8, 6);
    warden.hp = 50;
    foot.hp = 50;
    g.healOnKeeps("blue");
    expect(warden.hp).toBe(60);
    expect(foot.hp).toBe(50);
    warden.hp = 95;
    g.healOnKeeps("blue");
    expect(warden.hp).toBe(100);
    expect(unitSkills("spellwardens").map((s) => s.n)).toContain("Mending Runes");
  });
  it("Samurai: +10 on the blows they deal, −10 on the blows they take, and a Pike Wall", () => {
    const g = field();
    const samurai = spawn(g, "samurai", "blue", 8, 5),
      plain = spawn(g, "swordsmen", "blue", 8, 9),
      foe = spawn(g, "footmen", "red", 9, 5),
      foe2 = spawn(g, "footmen", "red", 9, 9);
    samurai._shroudOn = false;
    // the same Sword row and rating tier as… a Swordsman is tier 2; compare cell by cell instead
    const cell = WEAPON_DMG[41][foe.T.armour];
    expect(WEAPON_DMG[41]).toEqual(WEAPON_DMG[5]);
    only(g, samurai, foe);
    const withBonus = g.computeDamage(samurai, foe);
    samurai.T = { ...samurai.T, dmgBonus: 0 };
    expect(withBonus).toBeGreaterThan(g.computeDamage(samurai, foe));
    expect(cell).toBeGreaterThan(0);
    const taken = g.computeDamage(foe, samurai);
    samurai.T = { ...samurai.T, armourBonus: 0 };
    expect(taken).toBeLessThan(g.computeDamage(foe, samurai));
    expect(UNIT_TYPES.samurai.pikeWall).toBe(true);
    expect(plain && foe2).toBeTruthy();
  });
});

describe("Dragon Riders", () => {
  const run = (g, n = 400) => {
    for (let i = 0; i < n; i++) step(g);
  };
  it("a 750-point elite flier in Relic Armour at the Hero's rating, upgraded from Cavalry with a Void Rift Crystal", () => {
    const T = UNIT_TYPES.dragonrider,
      hero = UNIT_TYPES.king;
    expect(DEPLOY_COST.dragonrider).toBe(750);
    expect(T.fly && T.al === 0).toBe(true);
    expect(T.armour).toBe(hero.armour);
    expect(T.rf).toBe(hero.rf);
    expect(T.move).toBeGreaterThanOrEqual(hero.move);
    expect(T.firstStrike && T.fear && T.hasCharge && T.twinAttack).toBe(true);
    expect(T.harasser).toBe(false); // the computer flies it in to fight instead of hovering at range
    expect([T.minRange, T.range]).toEqual([1, 8]); // the lance at 1, the breath at 2–8: no dead zone
    expect(UPGRADE_FROM.dragonrider).toEqual({ from: "cavalry", need: "Void" });
    expect(upgradeGate("dragonrider", true)).toBe(5943);
    expect(unitSkills("dragonrider").map((s) => s.n)).toEqual(
      expect.arrayContaining(["Dragonfire", "Fire and Lance", "Flight", "Fear"]),
    );
  });
  it("Dragonfire burns its target, then the two tiles beyond it at 60% and 35% — fliers and war engines too", () => {
    const g = field();
    const dragon = spawn(g, "dragonrider", "blue", 4, 5),
      first = spawn(g, "footmen", "red", 8, 5),
      second = spawn(g, "footmen", "red", 9, 5),
      third = spawn(g, "footmen", "red", 10, 5),
      fourth = spawn(g, "footmen", "red", 11, 5),
      aside = spawn(g, "footmen", "red", 8, 6);
    only(g, dragon, first, second, third, fourth, aside);
    expect(g._weaponAt(dragon, 4)).toBe(42);
    expect(g._weaponAt(dragon, 2)).toBe(42);
    expect(g._weaponAt(dragon, 1)).toBe(15);
    const full = g.computeDamage(dragon, first);
    g.resolveDamage(dragon, first, {});
    expect(100 - first.hp).toBe(full);
    expect(100 - second.hp).toBeGreaterThan(100 - third.hp);
    expect(100 - second.hp).toBeLessThan(full);
    expect(third.hp).toBeLessThan(100);
    expect(fourth.hp).toBe(100);
    expect(aside.hp).toBe(100);
    const griffon = spawn(g, "griffon", "red", 4, 9),
      catapult = spawn(g, "catapult", "red", 4, 10),
      cannon = spawn(g, "cannon", "blue", 1, 9);
    expect(g.computeDamage(dragon, griffon, { weapon: 42 })).toBeGreaterThan(0);
    expect(g.computeDamage(cannon, griffon, { weapon: 23 })).toBe(0); // a Cannonball cannot touch a flier
    expect(g.computeDamage(dragon, catapult, { weapon: 42 })).toBeGreaterThan(g.computeDamage(dragon, first));
  });
  it("a tap on a foe it can reach flies in with the lance; the breath is left for another foe that turn", () => {
    const g = field();
    const dragon = spawn(g, "dragonrider", "blue", 2, 5),
      near = spawn(g, "footmen", "red", 7, 5),
      far = spawn(g, "footmen", "red", 9, 9),
      keep = spawn(g, "footmen", "blue", 1, 1); // (a second unit of yours, so the turn does not end by itself)
    g.select(dragon);
    expect(g.aimSkills().map((s) => s.id)).toEqual(["dragonfire"]);
    g.click({ tx: 7, ty: 5 });
    run(g);
    expect(Math.abs(dragon.tx - near.tx) + Math.abs(dragon.ty - near.ty)).toBe(1); // it flew in
    expect(near.hp).toBeLessThan(40); // a lance charge, not a 46-point breath
    expect(dragon.acted).toBe(false);
    expect(g.targets).toContain(far); // the breath is still to come
    g.click({ tx: 9, ty: 9 });
    run(g);
    expect(far.hp).toBeLessThan(100);
    expect(dragon.acted).toBe(true); // lance, breath and move all spent
    expect(keep.acted).toBeFalsy();
  });
  it("🔥 Dragonfire armed: the tap breathes instead, and the lance and the move are still to come", () => {
    const g = field();
    const dragon = spawn(g, "dragonrider", "blue", 2, 5),
      near = spawn(g, "footmen", "red", 7, 5);
    spawn(g, "footmen", "blue", 1, 1);
    g.select(dragon);
    g.aimSkill("dragonfire");
    expect(g.aimMode).toBe(true);
    g.click({ tx: 7, ty: 5 });
    run(g);
    expect([dragon.tx, dragon.ty]).toEqual([2, 5]); // it stayed and breathed
    const burned = near.hp;
    expect(burned).toBeLessThan(100);
    expect(g.aimSkills()).toBeNull(); // one breath a turn
    expect(dragon.acted).toBe(false);
    g.click({ tx: 7, ty: 5 });
    run(g);
    expect(near.dead || near.hp < burned).toBe(true); // …then the lance
  });
  it("the computer's Dragon Rider flies in and fights hand to hand", () => {
    const g = startBattle(makeGame(5424));
    const group = g.mission.groupOrder.find((x) => x.side === "enemy").gi; // (an enemy army that takes a turn)
    only(g);
    const mine = [
      spawn(g, "footmen", "blue", 6, 5),
      spawn(g, "archers", "blue", 6, 7),
      spawn(g, "swordsmen", "blue", 5, 6),
    ];
    const dragon = spawn(g, "dragonrider", "red", 13, 5, { group });
    nextRound(g);
    expect(mine.some((u) => Math.abs(u.tx - dragon.tx) + Math.abs(u.ty - dragon.ty) === 1)).toBe(true);
    expect(mine.some((u) => u.dead || u.hp < 60)).toBe(true);
  });
});

describe("after the arena: the computer's Dragon Rider, and ship bulwarks", () => {
  it("the computer's Dragon Rider follows its lance blow with its breath in the same turn", () => {
    const g = startBattle(makeGame(5204));
    only(g);
    const gi = g.mission.groupOrder.find((x) => x.side === "enemy").gi;
    const dragon = spawn(g, "dragonrider", "red", 12, 12, { group: gi });
    const near = spawn(g, "footmen", "blue", 12, 13),
      far = spawn(g, "footmen", "blue", 12, 8);
    nextRound(g);
    expect(dragon._lanced).toBe(1);
    expect(dragon._fired).toBe(1);
    expect(near.hp + far.hp).toBeLessThan(190);
    expect(near.hp < 100 || near.dead).toBe(true);
    expect(far.hp < 100 || far.dead).toBe(true);
  });
  it("a ship's deck is edged with a wooden bulwark that foot man, horse cannot, and Marines board from the sea", () => {
    const g = startBattle(makeGame(5941));
    only(g);
    const type = (x, y) => moveType(g.tileAt(x, y));
    // Grapples Away: the big hull's north rail is row 2 (x 6–15); the gangplank at (8, 7) stays open deck
    expect(type(8, 2)).toBe(14);
    expect(type(8, 3)).toBe(18);
    expect(type(8, 7)).toBe(18);
    const foot = spawn(g, "footmen", "blue", 8, 3),
      horse = spawn(g, "cavalry", "blue", 9, 3),
      marines = spawn(g, "marines", "blue", 8, 1);
    expect(type(8, 1)).toBe(19);
    expect(g.moveCost(foot, 8, 2, 8, 3)).toBe(1);
    expect(g.moveCost(horse, 9, 2, 9, 3)).toBe(99);
    expect(g.moveCost(marines, 8, 2, 8, 1)).toBe(1);
    expect(g.moveCost(foot, 8, 2, 8, 1)).toBe(99); // nobody else comes over the side
  });
});

describe("Marines: Grapple and Breach", () => {
  it("once a battle the Grapple swings them up to 6 tiles, over water onto a rampart, in place of the move", () => {
    const g = startBattle(makeGame(5941));
    only(g);
    const marines = spawn(g, "marines", "blue", 8, 9); // on your own deck, the enemy hull's south rail 3 tiles north
    g.selected = marines;
    expect(g._abilitySkills(marines).find((s) => s.id === "grapple")).toMatchObject({ disabled: false, count: "1/1" });
    expect(g._grappleTile(marines, 8, 15)).toBe(false); // out of the map / too far
    expect(g._grappleTile(marines, 9, 7)).toBe(false); // open sea
    expect(moveType(g.tileAt(9, 6))).toBe(14); // the bulwark of the hull opposite
    expect(g._grappleTile(marines, 9, 6)).toBe(true);
    g._castGrapple(marines, 9, 6);
    settle(g);
    expect([marines.tx, marines.ty]).toEqual([9, 6]);
    expect(marines._grappled).toBe(true);
    expect(g._movedThisTurn(marines)).toBe(true);
    marines.acted = false; // (the swing was its move; its turn ended with no foe beside it)
    expect(g._abilitySkills(marines).find((s) => s.id === "grapple").disabled).toBe(true);
    expect(g._grappleTile(marines, 9, 5)).toBe(false);
  });
  it("Breach: a wall gives no cover against Marines, though it does against anyone else", () => {
    const g = startBattle(makeGame(5941));
    only(g);
    const onWall = spawn(g, "footmen", "red", 8, 2),
      onDeck = spawn(g, "footmen", "red", 10, 4);
    const marines = spawn(g, "marines", "blue", 8, 4),
      archers = spawn(g, "archers", "blue", 10, 6);
    expect(moveType(g.tileAt(8, 2))).toBe(14);
    expect(UNIT_TYPES.marines.breach).toBe(true);
    const move = (u, x, y) => Object.assign(u, { tx: x, ty: y });
    const wallHit = g.computeDamage(marines, onWall);
    move(marines, 10, 2);
    expect(wallHit).toBe(g.computeDamage(marines, onDeck)); // the same 2 tiles away, cover or none
    move(archers, 8, 4);
    const covered = g.computeDamage(archers, onWall);
    move(archers, 10, 2);
    expect(covered).toBeLessThan(g.computeDamage(archers, onDeck));
  });
});

describe("Gladiators and the Beast Master", () => {
  it("Gladiators cost 175 and take less from every blow than Greatswordsmen do", () => {
    expect(DEPLOY_COST.gladiator).toBe(175);
    const g = startBattle(makeGame(5204));
    only(g);
    const glad = spawn(g, "gladiator", "blue", 10, 10),
      great = spawn(g, "greatswordsmen", "blue", 14, 10);
    for (const type of ["swordsmen", "halberdiers", "greatswordsmen", "knights"]) {
      const foe = spawn(g, type, "red", 10, 11);
      const onGlad = g.computeDamage(foe, glad);
      Object.assign(foe, { tx: 14, ty: 11 });
      expect(onGlad).toBeLessThan(g.computeDamage(foe, great));
      foe.dead = true;
    }
  });
  it("a 250-point Beast Master, upgraded from Militia with a Medal, calls up to two packs of leashed Hounds", () => {
    expect(DEPLOY_COST.beastmaster).toBe(250);
    expect(DEPLOY_ELITE.beastmaster).toBeFalsy();
    expect(UPGRADE_FROM.beastmaster).toEqual({ from: "raiders", need: "Anchor" });
    expect(upgradeGate("beastmaster", true)).toBe(5982);
    const hounds = UNIT_TYPES.hounds,
      stag = UNIT_TYPES.stag;
    expect(hounds.summoned).toBe(true);
    expect(DEPLOY_ORDER).not.toContain("hounds");
    expect(hounds.move).toBeLessThan(stag.move); // a little less than a Stag all round
    expect(hounds.rf).toBeLessThan(stag.rf);
    expect(hounds.hasCharge).toBe(false);
    const g = startBattle(makeGame(5204));
    only(g);
    const master = spawn(g, "beastmaster", "blue", 10, 10);
    g.selected = master;
    const skills = g._abilitySkills(master).filter((s) => s.id.startsWith("conjure"));
    expect(skills.map((s) => s.id)).toEqual(["conjure_hounds"]);
    g._castConjure(master, "hounds", 11, 10);
    settle(g);
    master.acted = false;
    g._castConjure(master, "hounds", 9, 10);
    settle(g);
    const packs = g.units.filter((u) => !u.dead && u.type === "hounds");
    expect(packs.length).toBe(2);
    expect(packs.every((u) => u._conjuredBy === master.id && u.acted)).toBe(true);
    master.acted = false;
    expect(g._abilitySkills(master).find((s) => s.id === "conjure_hounds").disabled).toBe(true);
    g._killConjuredChildren(master); // what the Beast Master's death does
    expect(g.units.filter((u) => !u.dead && u.type === "hounds").length).toBe(0);
  });
  it("the computer's Beast Master calls Hounds, not the Conjurer's minions", () => {
    const g = startBattle(makeGame(5204));
    only(g);
    const gi = g.mission.groupOrder.find((x) => x.side === "enemy").gi;
    const master = spawn(g, "beastmaster", "red", 12, 12, { group: gi });
    spawn(g, "footmen", "blue", 12, 4);
    nextRound(g);
    const called = g.units.filter((u) => !u.dead && u._conjuredBy === master.id);
    expect(called.length).toBe(1);
    expect(called[0].type).toBe("hounds");
  });
});

describe("Satoshi's second wave: Sohei, Shinobi, Oni, Tengu", () => {
  const field = () => {
    const g = startBattle(makeGame(5204));
    only(g);
    return g;
  };
  it("Sutra: friends beside a Sohei mend 10 HP at the start of its side's turn; a Stone Sentinel does not", () => {
    const g = field();
    spawn(g, "sohei", "blue", 10, 10);
    const beside = spawn(g, "footmen", "blue", 11, 10),
      apart = spawn(g, "footmen", "blue", 13, 10),
      stone = spawn(g, "sentinel", "blue", 10, 11);
    for (const u of [beside, apart, stone]) u.hp = 50;
    g.healOnKeeps("blue");
    expect([beside.hp, apart.hp, stone.hp]).toEqual([60, 50, 50]);
    expect(UNIT_TYPES.sohei.fearless).toBe(true);
  });
  it("Shadow: a Shinobi hides on open ground, and its blow from hiding is 30 stronger on the table", () => {
    const g = field();
    const shinobi = spawn(g, "shinobi", "blue", 10, 10),
      ranger = spawn(g, "rangers", "blue", 10, 14),
      foe = spawn(g, "footmen", "red", 12, 10);
    expect(g._canHide(shinobi)).toBe(true); // open field: no cover at all
    expect(g._canHide(ranger)).toBe(false);
    const plain = g.computeDamage(shinobi, foe);
    g._setHidden(shinobi, true);
    g.healOnKeeps("blue"); // its turn begins in hiding
    expect(shinobi._ambushReady).toBe(true);
    expect(g.computeDamage(shinobi, foe)).toBeGreaterThan(plain);
    g._endTurnHide([shinobi]);
    expect(shinobi._ambushReady).toBe(false);
    Object.assign(foe, { tx: 11, ty: 10 }); // an enemy beside it: nowhere to hide
    expect(g._canHide(shinobi)).toBe(false);
  });
  it("Sunder: the foe an Oni strikes is Shattered — every blow at it lands harder from then on, magic excepted", () => {
    const g = field();
    const oni = spawn(g, "oni", "blue", 10, 10),
      target = spawn(g, "knights", "red", 11, 10),
      beside = spawn(g, "footmen", "red", 12, 10),
      friend = spawn(g, "footmen", "blue", 11, 9),
      wizard = spawn(g, "wizards", "blue", 11, 13);
    const blow = g.computeDamage(friend, target),
      spell = g.computeDamage(wizard, target);
    g.resolveDamage(oni, target);
    expect([target._shattered, !!beside._shattered]).toEqual([true, false]);
    expect(beside.hp).toBe(100); // (it was Earthshaker: the blow no longer spreads)
    target.hp = 100;
    expect(g.computeDamage(friend, target)).toBeGreaterThan(blow);
    expect(g.computeDamage(wizard, target)).toBe(spell);
    expect(g._statusesOf(target).some((status) => status.name === "Armour shattered")).toBe(true);
    expect(UNIT_TYPES.oni.fear && UNIT_TYPES.oni.armourName === "Oni Hide").toBe(true);
  });
  it("Gale: the Tengu's foe is thrown a tile back and cannot strike back; with no room behind, it stands", () => {
    const g = field();
    const tengu = spawn(g, "tengu", "blue", 10, 10),
      foe = spawn(g, "footmen", "red", 11, 10);
    g.resolveDamage(tengu, foe);
    expect([foe.tx, foe.ty]).toEqual([12, 10]);
    expect(g._countersAfter(tengu, foe, false)).toBe(false);
    const pinned = spawn(g, "footmen", "red", 10, 11);
    spawn(g, "footmen", "red", 10, 12);
    g.resolveDamage(tengu, pinned);
    expect([pinned.tx, pinned.ty]).toEqual([10, 11]);
    expect(UNIT_TYPES.tengu.fly && UNIT_TYPES.tengu.al === 0).toBe(true);
  });
  it("each has its price, its upgrade and its Satoshi battle", () => {
    expect([DEPLOY_COST.sohei, DEPLOY_COST.shinobi, DEPLOY_COST.oni, DEPLOY_COST.tengu]).toEqual([175, 225, 325, 325]);
    expect(upgradeGate("sohei", true)).toBe(5961);
    expect(upgradeGate("shinobi", true)).toBe(5962);
    expect(upgradeGate("oni", true)).toBe(5963);
    expect(upgradeGate("tengu", true)).toBe(5963);
  });
});

describe("The laboratory and its creatures: Alchemist, Imp, Golem, Unicorn, Efreet, Naga, Skeletons", () => {
  const field = () => {
    const g = startBattle(makeGame(5204));
    only(g);
    return g;
  };
  it("the Acid Flask bursts on its target and the tiles around it, and leaves 5 HP a turn of acid for 3 turns", () => {
    const g = field();
    const alchemist = spawn(g, "alchemist", "blue", 5, 10),
      target = spawn(g, "footmen", "red", 9, 10),
      beside = spawn(g, "footmen", "red", 9, 11),
      apart = spawn(g, "footmen", "red", 11, 10);
    expect(g._weaponAt(alchemist, 4)).toBe(50);
    expect(UNIT_TYPES.alchemist.range).toBe(6);
    g.resolveDamage(alchemist, target, {});
    expect(100 - beside.hp).toBeGreaterThan(0);
    expect(100 - beside.hp).toBeLessThan(100 - target.hp); // the cross takes 60%
    expect(apart.hp).toBe(100);
    expect(target._acid.turns).toBe(3);
    expect(beside._acid.turns).toBe(3);
    expect(apart._acid).toBeFalsy();
    const after = target.hp;
    for (let turn = 1; turn <= 4; turn++) g.healOnKeeps("red");
    expect(after - target.hp).toBe(15); // 5 + 5 + 5, then nothing
    expect(target._acid).toBeNull();
  });
  it("the Alchemist heals 30 HP at up to 2 tiles, and summons Imps where a Beast Master calls Hounds", () => {
    const g = field();
    const alchemist = spawn(g, "alchemist", "blue", 10, 10),
      near = spawn(g, "footmen", "blue", 12, 10),
      far = spawn(g, "footmen", "blue", 13, 10);
    near.hp = 40;
    far.hp = 40;
    g.selected = alchemist;
    expect(g._clickHeal(far)).toBe(false); // 3 tiles away
    expect(g._clickHeal(near)).toBe(true);
    for (let i = 0; i < 200; i++) step(g);
    expect(near.hp).toBe(70);
    alchemist.acted = false;
    expect(g._abilitySkills(alchemist).map((s) => s.id)).toContain("conjure_imp");
    g._castConjure(alchemist, "imp", 10, 11);
    settle(g);
    const imp = g.units.find((u) => u.type === "imp");
    expect(imp._conjuredBy).toBe(alchemist.id);
    expect(UNIT_TYPES.imp.summoned && UNIT_TYPES.imp.fly).toBe(true);
    expect(DEPLOY_ORDER).not.toContain("imp");
  });
  it("Stoneskin: no single blow takes more than 20 HP from a Golem", () => {
    const g = field();
    const golem = spawn(g, "golem", "blue", 10, 10);
    for (const [type, x] of [
      ["greatswordsmen", 11],
      ["knights", 9],
    ]) {
      const foe = spawn(g, type, "red", x, 10);
      expect(g.computeDamage(foe, golem)).toBeLessThanOrEqual(20);
      expect(g.computeDamage(foe, golem, { charge: true })).toBeLessThanOrEqual(20);
    }
    const cannon = spawn(g, "cannon", "red", 10, 15);
    expect(g.computeDamage(cannon, golem)).toBeLessThanOrEqual(20);
    expect(UNIT_TYPES.golem.unyielding && UNIT_TYPES.golem.fear).toBe(true);
  });
  it("Purity: friends within 2 tiles of a Unicorn feel no Fear and are washed clean of acid", () => {
    const g = field();
    spawn(g, "unicorn", "blue", 10, 10);
    const near = spawn(g, "footmen", "blue", 12, 10),
      far = spawn(g, "footmen", "blue", 14, 10),
      oni = spawn(g, "oni", "red", 12, 11);
    expect(g._purified(near)).toBe(true);
    expect(g._purified(far)).toBe(false);
    g.rng = () => 0.999; // the worst courage roll there is
    expect(g._fearCheck(near, oni, () => {})).toBe(false); // never balks
    near._acid = { turns: 3, by: oni };
    far._acid = { turns: 3, by: oni };
    g.healOnKeeps("blue");
    expect([near.hp, far.hp]).toEqual([100, 95]);
    expect(near._acid).toBeNull();
    expect(UNIT_TYPES.unicorn.fly).toBe(true);
  });
  it("Burning Aura: an enemy beside an Efreet loses 20 HP as its turn begins; its friends do not", () => {
    const g = field();
    spawn(g, "efreet", "blue", 10, 10);
    const foe = spawn(g, "footmen", "red", 11, 10),
      farFoe = spawn(g, "footmen", "red", 13, 10),
      friend = spawn(g, "footmen", "blue", 10, 11);
    g.healOnKeeps("red");
    g.healOnKeeps("blue");
    expect([foe.hp, farFoe.hp, friend.hp]).toEqual([80, 100, 100]);
  });
  it("Constrict: the foe a Naga strikes cannot move on its next turn, and is free again after it", () => {
    const g = field();
    const naga = spawn(g, "naga", "blue", 10, 10),
      foe = spawn(g, "footmen", "red", 11, 10);
    g.resolveDamage(naga, foe, {});
    expect(foe._held).toBe(true);
    expect(g.moveOf(foe)).toBe(0);
    expect(g.computeReach(foe).stops.size).toBe(1); // its own tile
    g._endTurnHide([foe]);
    expect(g.moveOf(foe)).toBe(4);
    expect(UNIT_TYPES.naga.amphibious).toBe(true);
  });
  it("Rise Again: a Skeleton struck down gets up once at full strength, and stays down the second time", () => {
    const g = field();
    const skeleton = spawn(g, "skeleton", "blue", 10, 10),
      foe = spawn(g, "knights", "red", 11, 10);
    g._applyHit(skeleton, foe, 150, false);
    expect([skeleton.dead, skeleton.hp]).toEqual([false, 100]);
    g._applyHit(skeleton, foe, 150, false);
    expect(skeleton.dead).toBe(true);
  });
  it("each has its price; Alchemist and Golem have their upgrade and the battle that opens it", () => {
    const cost = (k) => DEPLOY_COST[k];
    expect(["alchemist", "golem", "unicorn", "efreet", "naga", "skeleton"].map(cost)).toEqual([
      250, 325, 275, 350, 300, 500,
    ]);
    expect(upgradeGate("alchemist", true)).toBe(5925);
    expect(upgradeGate("golem", true)).toBe(5912);
  });
  it("Unicorn, Efreet, Naga and Skeletons are hidden for now: built, but nowhere in the game", () => {
    expect(BONUS_HIDDEN).toEqual(["unicorn", "efreet", "naga", "skeleton"]);
    for (const unit of BONUS_HIDDEN) {
      expect(UNIT_TYPES[unit]).toBeTruthy(); // the unit itself still works (the tests above)
      expect(BONUS_ORDER).not.toContain(unit);
      expect(DEPLOY_ORDER).not.toContain(unit);
      expect(UNIT_META[unit]).toBeUndefined(); // no camp or Field Manual card
      expect(UPGRADE_FROM[unit]).toBeUndefined(); // no upgrade branch
      expect(BONUS_UPGRADES.some((u) => u.to === unit || u.from === unit)).toBe(false);
    }
    const veteran = JSON.parse(readFileSync(join("public", "games", "reign-of-swords-2", "veteran-army.json"), "utf8"));
    const bonus = JSON.parse(readFileSync(join("public", "games", "reign-of-swords-2", "bonus.json"), "utf8"));
    for (const unit of BONUS_HIDDEN) expect(veteran.army[unit]).toBeUndefined();
    for (const level of bonus.levels) {
      const fielded = [...level.player, ...level.allies, ...level.enemy].map((u) => u[0]);
      const spawned = level.script.actions.filter((a) => a.op === 0).map((a) => a.key);
      for (const unit of BONUS_HIDDEN) expect([...fielded, ...spawned]).not.toContain(unit);
    }
    for (const reward of Object.values(bonus.rewards))
      for (const unit of BONUS_HIDDEN) expect((reward.units || {})[unit]).toBeUndefined();
  });
});

describe("Stone Sentinel and Golem: Bulwark", () => {
  it("a charge and a flank attack gain nothing against a Bulwark, and a Tengu cannot throw it", () => {
    const g = startBattle(makeGame(5204));
    only(g);
    const sentinel = spawn(g, "sentinel", "blue", 10, 10),
      footmen = spawn(g, "footmen", "blue", 10, 14);
    const knights = spawn(g, "knights", "red", 11, 10),
      knights2 = spawn(g, "knights", "red", 11, 14);
    expect(g.computeDamage(knights, sentinel, { charge: true })).toBe(g.computeDamage(knights, sentinel));
    expect(g.computeDamage(knights2, footmen, { charge: true })).toBeGreaterThan(g.computeDamage(knights2, footmen));
    const front = g.computeDamage(knights, sentinel);
    spawn(g, "footmen", "red", 9, 10); // a foe on the far side: a flank for anyone else
    expect(g.computeDamage(knights, sentinel)).toBe(front);
    const tengu = spawn(g, "tengu", "red", 10, 9);
    g.resolveDamage(tengu, sentinel);
    expect([sentinel.tx, sentinel.ty]).toEqual([10, 10]);
    expect(UNIT_TYPES.sentinel.lastStrike).toBe(false); // it no longer strikes last
    expect(UNIT_TYPES.golem.bulwark).toBe(false); // Bulwark is the Sentinel's alone; the Golem has Stoneskin
    expect(DEPLOY_COST.sentinel).toBe(300);
  });
});

describe("Tezcal: Jaguar Warriors, Eagle Warriors, the Sun Priest and the Feathered Serpent", () => {
  const field = () => {
    const g = startBattle(makeGame(5204));
    only(g);
    return g;
  };
  const woods = (g) => {
    for (let y = 0; y < g.rows; y++)
      for (let x = 1; x < g.cols - 1; x++)
        if ([4, 28].includes(moveType(g.tileAt(x, y))) && ![3, 4, 22, 27, 28].includes(moveType(g.tileAt(x + 1, y))))
          return [x, y];
    return null;
  };
  it("Jungle Stride: Jaguar and Eagle Warriors cross woods at 1 a tile; Pounce strikes harder from cover", () => {
    const g = startBattle(makeGame(5961)); // The Paddy Road: woods beside the road
    only(g);
    const spot = woods(g);
    expect(spot).toBeTruthy();
    const [x, y] = spot;
    const jaguar = spawn(g, "jaguar", "blue", x, y),
      eagle = spawn(g, "eagle", "blue", 0, 0),
      footmen = spawn(g, "footmen", "blue", 1, 0);
    expect(g.moveCost(jaguar, x, y)).toBe(1);
    expect(g.moveCost(eagle, x, y)).toBe(1);
    expect(g.moveCost(footmen, x, y)).toBeGreaterThan(1);
    const foe = spawn(g, "footmen", "red", x + 1, y);
    const fromWoods = g.computeDamage(jaguar, foe);
    Object.assign(jaguar, { tx: x + 2, ty: y }); // the same foe from the far side
    if (![3, 4, 22, 27, 28].includes(moveType(g.tileAt(x + 2, y))))
      expect(fromWoods).toBeGreaterThan(g.computeDamage(jaguar, foe));
    expect(UNIT_TYPES.jaguar.pounce).toBe(20);
    expect(UNIT_TYPES.jaguar.forestWalk && UNIT_TYPES.eagle.forestWalk).toBe(true);
  });
  it("Eagle Eye: an Eagle Warrior's dart ignores its target's cover; a Cragsman's javelin does not", () => {
    const g = startBattle(makeGame(5941)); // a ship: the bulwark is cover
    only(g);
    const onWall = spawn(g, "footmen", "red", 8, 2),
      onDeck = spawn(g, "footmen", "red", 10, 4);
    const eagle = spawn(g, "eagle", "blue", 8, 4),
      crag = spawn(g, "cragsmen", "blue", 6, 4);
    const move = (u, tx, ty) => Object.assign(u, { tx, ty });
    const covered = g.computeDamage(eagle, onWall);
    move(eagle, 10, 2);
    expect(covered).toBe(g.computeDamage(eagle, onDeck));
    move(crag, 8, 4);
    move(eagle, 0, 0);
    const cragCovered = g.computeDamage(crag, onWall);
    move(crag, 10, 2);
    expect(cragCovered).toBeLessThan(g.computeDamage(crag, onDeck));
    expect(g._weaponAt(eagle, 1)).toBe(59); // a Macuahuitl up close, where the Cragsman has a Spear
  });
  it("Sun Priest: Sunbeam burns on in a line; Dawn mends friends within 2 tiles; Eclipse halves a foe's blows", () => {
    const g = field();
    const priest = spawn(g, "sunpriest", "blue", 5, 10),
      target = spawn(g, "footmen", "red", 9, 10),
      behind = spawn(g, "footmen", "red", 10, 10),
      beside = spawn(g, "footmen", "red", 9, 11);
    expect(g._weaponAt(priest, 4)).toBe(61);
    expect(g.computeDamage(priest, target)).toBeGreaterThan(g.computeDamage(priest, target, { weapon: 25 }));
    g.resolveDamage(priest, target, {});
    expect(target.hp).toBeLessThan(100);
    expect(behind.hp).toBeLessThan(100); // the beam goes on
    expect(beside.hp).toBe(100); // no burst
    const skills = g._abilitySkills(priest).map((s) => s.id);
    expect(skills).toEqual(expect.arrayContaining(["dawn", "eclipse"]));
    const near = spawn(g, "footmen", "blue", 5, 12),
      far = spawn(g, "footmen", "blue", 5, 14);
    near.hp = 50;
    far.hp = 50;
    priest.hp = 60;
    g._dawn(priest);
    expect([near.hp, far.hp, priest.hp]).toEqual([65, 50, 75]);
    const knight = spawn(g, "knights", "red", 7, 10),
      victim = spawn(g, "footmen", "blue", 7, 11);
    const full = g.computeDamage(knight, victim);
    g._eclipse(knight);
    expect(g.computeDamage(knight, victim)).toBeLessThanOrEqual(Math.ceil(full / 2));
    g._endTurnHide([knight]);
    expect(g.computeDamage(knight, victim)).toBe(full);
    expect(DEPLOY_ELITE.sunpriest).toBe(true);
  });
  it("Feathered Serpent: a flier that shoots and moves; Tailwind carries the friends beside it a tile further", () => {
    const g = field();
    spawn(g, "serpent", "blue", 10, 10);
    const beside = spawn(g, "footmen", "blue", 11, 10),
      apart = spawn(g, "footmen", "blue", 14, 10);
    expect(g.moveOf(beside)).toBe(g.moveOf(apart) + 1);
    const T = UNIT_TYPES.serpent;
    expect(T.fly && T.al === 0 && T.shootMove).toBe(true);
    expect([T.minRange, T.range]).toEqual([1, 4]);
  });
  it("the Beast Master's tree: Tengu, and (hidden for now) Unicorn, Efreet, Naga and Skeletons", () => {
    expect(BONUS_UPGRADES.filter((u) => u.from === "beastmaster").map((u) => u.to)).toEqual(["tengu"]);
    const tree = BONUS_UPGRADES_ALL.filter((u) => u.from === "beastmaster").map((u) => [u.to, u.need]);
    expect(tree).toEqual([
      ["tengu", "Tsuba"],
      ["unicorn", "Lore"],
      ["efreet", "Weapons"],
      ["naga", "Beasts"],
      ["skeleton", "Armor"],
    ]);
    expect(UPGRADE_FROM.tengu.from).toBe("beastmaster");
    const cost = (k) => DEPLOY_COST[k];
    expect(["jaguar", "eagle", "sunpriest", "serpent"].map(cost)).toEqual([150, 175, 325, 300]);
    expect(upgradeGate("jaguar", true)).toBe(5994);
    expect(upgradeGate("eagle", true)).toBe(5995);
    expect(upgradeGate("serpent", true)).toBe(5996);
    expect(upgradeGate("sunpriest", true)).toBe(5996);
  });
});

describe("Jarnheim and Khemret: the Norse and Egyptian units", () => {
  const field = () => {
    const g = startBattle(makeGame(5204));
    only(g);
    return g;
  };
  it("Rage: a wounded Berserker's blow lands on a higher cell of the table than the same blow without Rage", () => {
    const g = field();
    const berserker = spawn(g, "berserker", "blue", 10, 10),
      foe = spawn(g, "footmen", "red", 11, 10);
    const T = berserker.T;
    const fresh = g._damage256(berserker, foe);
    berserker.T = { ...T, rage: 0 };
    expect(g._damage256(berserker, foe)).toBe(fresh); // at full health Rage adds nothing
    berserker.hp = 40;
    const calm = g._damage256(berserker, foe);
    berserker.T = T;
    expect(g._damage256(berserker, foe)).toBeGreaterThan(calm);
    expect(UNIT_TYPES.berserker.fearless).toBe(true);
  });
  it("Shield Wall: an enemy ground unit that steps beside a Shieldmaiden stops there; fliers and friends do not", () => {
    const g = field();
    const maiden = spawn(g, "shieldmaiden", "blue", 10, 10),
      runner = spawn(g, "raiders", "red", 14, 10),
      flier = spawn(g, "griffon", "red", 14, 12),
      friend = spawn(g, "raiders", "blue", 14, 8);
    const steps = (u, x, y) => g.computeReach(u).dist.get(x + "," + y);
    expect(steps(runner, 11, 10)).toBe(3); // up to her: it can stand beside her, and strike from there
    expect(steps(runner, 11, 11)).toBe(4);
    expect(steps(runner, 9, 10)).toBeUndefined(); // …but not round her: every tile beside her is where a move ends
    expect(steps(runner, 8, 10)).toBeUndefined();
    expect(steps(flier, 8, 10)).toBeDefined();
    expect(steps(friend, 8, 10)).toBeDefined();
    Object.assign(runner, { tx: 11, ty: 10 }); // beside her already: it may leave, but round her is the long way
    expect(steps(runner, 13, 10)).toBe(2);
    expect(steps(runner, 10, 11)).toBe(2);
    expect(steps(runner, 9, 10)).toBe(6); // (four, were the tile under her shield not the end of a move)
    maiden.dead = true;
    expect(steps(runner, 8, 10)).toBeDefined();
    // (it was a quarter off the blows at her neighbours: that is gone)
    maiden.dead = false;
    const foe = spawn(g, "swordsmen", "red", 10, 12),
      beside = spawn(g, "berserker", "blue", 10, 11);
    const blow = g.computeDamage(foe, beside);
    maiden.dead = true;
    expect(g.computeDamage(foe, beside)).toBe(blow);
  });
  it("Chosen of the Slain: an Einherjar regains 50 HP when it strikes a foe down", () => {
    const g = field();
    const einherjar = spawn(g, "einherjar", "blue", 10, 10),
      foe = spawn(g, "footmen", "red", 11, 10);
    einherjar.hp = 30;
    g._applyHit(foe, einherjar, 20, false);
    expect(einherjar.hp).toBe(30); // a wound is not a kill
    g._applyHit(foe, einherjar, 200, false);
    expect([foe.dead, einherjar.hp]).toEqual([true, 80]);
  });
  it("Frost Slam: a Jotunn's target and the foes beside it move at half pace for a turn", () => {
    const g = field();
    const jotunn = spawn(g, "jotunn", "blue", 10, 10),
      target = spawn(g, "footmen", "red", 11, 10),
      beside = spawn(g, "footmen", "red", 12, 10),
      apart = spawn(g, "footmen", "red", 14, 10);
    g.resolveDamage(jotunn, target, {});
    expect([g.moveOf(target), g.moveOf(beside), g.moveOf(apart)]).toEqual([2, 2, 4]);
    g._endTurnHide([target, beside]);
    expect(g.moveOf(beside)).toBe(4);
    expect(UNIT_TYPES.jotunn.fear).toBe(true);
  });
  it("Medjay: a Composite Bow at 2–7, and desert brush costs them 1", () => {
    expect([UNIT_TYPES.medjay.minRange, UNIT_TYPES.medjay.range]).toEqual([1, 7]);
    expect(UNIT_TYPES.archers.range).toBe(6);
    const g = startBattle(makeGame(5934));
    only(g);
    let brush = null;
    for (let y = 0; y < g.rows && !brush; y++)
      for (let x = 0; x < g.cols && !brush; x++) if (moveType(g.tileAt(x, y)) === 28) brush = [x, y];
    expect(brush).toBeTruthy();
    const medjay = spawn(g, "medjay", "blue", 0, 0),
      archers = spawn(g, "archers", "blue", 1, 0);
    expect(g.moveCost(medjay, brush[0], brush[1])).toBe(1);
    expect(g.moveCost(archers, brush[0], brush[1])).toBeGreaterThan(1);
  });
  it("Shield Hook: against a Khopesh a shield counts for nothing; against bare armour it is a plain sword", () => {
    const g = field();
    const khopesh = spawn(g, "khopesh", "blue", 10, 10),
      shielded = spawn(g, "footmen", "red", 11, 10), // Light Armour & Shield
      bare = spawn(g, "archers", "red", 9, 10); // No Armour: nothing to hook
    const T = khopesh.T;
    const hooked = [g._damage256(khopesh, shielded), g._damage256(khopesh, bare)];
    khopesh.T = { ...T, hook: false };
    expect(hooked[0]).toBeGreaterThan(g._damage256(khopesh, shielded));
    expect(hooked[1]).toBe(g._damage256(khopesh, bare));
  });
  it("Weighing of the Heart: an Anubis Priest's Soulfire hits a wounded foe harder", () => {
    const g = field();
    const anubis = spawn(g, "anubis", "blue", 5, 10),
      foe = spawn(g, "footmen", "red", 9, 10);
    expect(g._weaponAt(anubis, 4)).toBe(70);
    const fresh = g.computeDamage(anubis, foe);
    foe.hp = 40;
    expect(g.computeDamage(anubis, foe)).toBeGreaterThan(fresh);
    expect(UNIT_TYPES.anubis.shotHue).toBe(250);
  });
  it("Devourer: an Ammit swallows a foe its bite leaves at 20 HP or fewer; a war engine it does not", () => {
    const g = field();
    const ammit = spawn(g, "ammit", "blue", 10, 10),
      foe = spawn(g, "footmen", "red", 11, 10),
      tough = spawn(g, "footmen", "red", 10, 11),
      engine = spawn(g, "catapult", "red", 9, 10);
    foe.hp = 30;
    g._applyHit(foe, ammit, 12, false); // 18 left: gone
    expect(foe.dead).toBe(true);
    g._applyHit(tough, ammit, 12, false); // 88 left: alive
    expect([tough.dead, tough.hp]).toEqual([false, 88]);
    engine.hp = 30;
    g._applyHit(engine, ammit, 12, false);
    expect(engine.dead).toBe(false);
  });
});

describe("Moananui and Coatlan: the Polynesian and serpent-order units", () => {
  const field = () => {
    const g = startBattle(makeGame(5204));
    only(g);
    return g;
  };
  const water = (g, type) => {
    for (let y = 0; y < g.rows; y++)
      for (let x = 0; x < g.cols; x++) if (moveType(g.tileAt(x, y)) === type && !g.unitAt(x, y)) return [x, y];
    return null;
  };
  it("First Thrust: a Toa hits a foe at full health harder; Wayfinder: shallows cost it 1", () => {
    const g = startBattle(makeGame(5941)); // a ship map: shallows at its edge
    only(g);
    const toa = spawn(g, "toa", "blue", 8, 4),
      foe = spawn(g, "footmen", "red", 9, 4);
    const fresh = g._damage256(toa, foe);
    foe.hp = 99;
    expect(g._damage256(toa, foe)).toBeLessThan(fresh);
    const shallows = water(g, 5);
    expect(shallows).toBeTruthy();
    const footmen = spawn(g, "footmen", "blue", 8, 5);
    expect(g.moveCost(toa, shallows[0], shallows[1])).toBe(1);
    expect(g.moveCost(footmen, shallows[0], shallows[1])).toBeGreaterThan(1);
  });
  it("Sky Hunter: a Tahuanui Rider hits archers and war engines harder; infantry it hits as anyone would", () => {
    const g = field();
    const rider = spawn(g, "tahuanui", "blue", 10, 10);
    const archers = spawn(g, "archers", "red", 11, 10),
      footmen = spawn(g, "footmen", "red", 10, 11),
      catapult = spawn(g, "catapult", "red", 9, 10);
    const T = rider.T;
    const hunting = [archers, catapult, footmen].map((foe) => g._damage256(rider, foe));
    rider.T = { ...T, skyHunter: 0 };
    const plain = [archers, catapult, footmen].map((foe) => g._damage256(rider, foe));
    expect(hunting[0]).toBeGreaterThan(plain[0]);
    expect(hunting[1]).toBeGreaterThan(plain[1]);
    expect(hunting[2]).toBe(plain[2]);
    expect(UNIT_TYPES.tahuanui.fly).toBe(true);
  });
  it("Karakia: as its turn begins a Tohunga mends the most wounded friend within 3 tiles by 15", () => {
    const g = field();
    spawn(g, "tohunga", "blue", 10, 10);
    const worst = spawn(g, "footmen", "blue", 12, 10),
      other = spawn(g, "footmen", "blue", 10, 12),
      far = spawn(g, "footmen", "blue", 15, 10);
    worst.hp = 30;
    other.hp = 60;
    far.hp = 10;
    g.healOnKeeps("blue");
    expect([worst.hp, other.hp, far.hp]).toEqual([45, 60, 10]);
  });
  it("Lurker of the Deep: a Taniwha swims deep water at 1, fights from it, and strikes harder out of it", () => {
    const g = startBattle(makeGame(5941));
    only(g);
    const deep = water(g, 19);
    const taniwha = spawn(g, "taniwha", "blue", 8, 4),
      marines = spawn(g, "marines", "blue", 9, 4);
    expect(g.moveCost(taniwha, deep[0], deep[1])).toBe(1);
    expect(g.moveCost(marines, deep[0], deep[1])).toBe(2);
    // from the deck, then from the sea beside the same foe
    const foe = spawn(g, "footmen", "red", 8, 2); // on the north rail; the sea is at (8, 1)
    expect(moveType(g.tileAt(8, 1))).toBe(19);
    Object.assign(taniwha, { tx: 8, ty: 3 });
    const dry = g._damage256(taniwha, foe);
    Object.assign(taniwha, { tx: 8, ty: 1 });
    expect(g._damage256(taniwha, foe)).toBeGreaterThan(dry);
    expect(g.targetsFrom(taniwha, 8, 1, false)).toContain(foe);
    Object.assign(marines, { tx: 9, ty: 1 });
    spawn(g, "footmen", "red", 9, 2);
    expect(g.targetsFrom(marines, 9, 1, false)).toEqual([]); // Marines still cannot attack from the deep
  });
  it("Serpent Venom: a Coatecpatl's blow leaves 5 HP a turn of poison for 3 turns", () => {
    const g = field();
    const warrior = spawn(g, "coatecpatl", "blue", 10, 10),
      foe = spawn(g, "knights", "red", 11, 10);
    g.resolveDamage(warrior, foe, {});
    expect(foe._acid.turns).toBe(3);
    const after = foe.hp;
    for (let turn = 1; turn <= 4; turn++) g.healOnKeeps("red");
    expect(after - foe.hp).toBe(15);
    expect(UNIT_TYPES.coatecpatl.forestWalk).toBe(true);
  });
  it("Drowning Grasp: the foe an Ahuizotl strikes cannot attack on its next turn, and can after it", () => {
    const g = field();
    const beast = spawn(g, "ahuizotl", "blue", 10, 10),
      foe = spawn(g, "footmen", "red", 11, 10);
    expect(g.targetsFrom(foe, 11, 10, false)).toContain(beast);
    g.resolveDamage(beast, foe, {});
    expect(foe._seized).toBe(true);
    expect(g.targetsFrom(foe, 11, 10, false)).toEqual([]);
    expect(g.moveOf(foe)).toBe(4); // it can still walk away
    g._endTurnHide([foe]);
    expect(g.targetsFrom(foe, 11, 10, false)).toContain(beast);
  });
  it("Vanguard: a unit beside a Cuahchic Chieftain strikes first; the Chieftain carries a Battle Standard", () => {
    const g = field();
    const friend = spawn(g, "footmen", "blue", 10, 10);
    expect(g._hasFirstStrike(friend)).toBe(false);
    spawn(g, "chieftain", "blue", 10, 11);
    expect(g._hasFirstStrike(friend)).toBe(true);
    const apart = spawn(g, "footmen", "blue", 14, 10);
    expect(g._hasFirstStrike(apart)).toBe(false);
    expect(UNIT_TYPES.chieftain.standard).toBe(true);
    expect([UNIT_TYPES.chieftain.minRange, UNIT_TYPES.chieftain.range]).toEqual([1, 4]);
  });
  it("Star Hunger: half of what a Tzitzimitl's Starfire burns away returns to it", () => {
    const g = field();
    const spectre = spawn(g, "tzitzimitl", "blue", 5, 10),
      foe = spawn(g, "footmen", "red", 9, 10);
    spectre.hp = 50;
    const blow = g.computeDamage(spectre, foe);
    g.resolveDamage(spectre, foe, {});
    expect(spectre.hp).toBe(50 + Math.round(blow / 2));
    expect(UNIT_TYPES.tzitzimitl.fly && UNIT_TYPES.tzitzimitl.fear).toBe(true);
  });
});

describe("the culture tokens", () => {
  it("are collectibles of their own: kept off the Merchant's counter, and the price of their culture's units", () => {
    const tokens = COLLECTIBLES.filter((c) => c.token).map((c) => c.id);
    expect(tokens).toEqual([
      "Bloodstone",
      "Scarab",
      "Obsidian",
      "Whalebone",
      "Anchor",
      "Tsuba",
      "Jade",
      "Void",
      "Pearl", // the three factions' (faction-units.test.js)
      "Mainspring",
      "Amber",
    ]);
    expect(TRADE_GOODS.map((c) => c.id)).toEqual(["Medal", "Armor", "Weapons", "Beasts", "Spirit", "Lore"]);
    for (const id of tokens) {
      expect(RES_ICON[id]).toBeTruthy();
      expect(NEED_COLOR[id]).toBeTruthy();
      expect(existsSync(join("public", "games", "reign-of-swords", "icons", RES_ICON[id] + ".png"))).toBe(true);
    }
    const priceOf = Object.fromEntries(BONUS_UPGRADES.map((u) => [u.to, u.need]));
    const paid = (token, units) => units.forEach((unit) => expect(priceOf[unit], unit).toBe(token));
    paid("Bloodstone", ["berserker", "shieldmaiden", "einherjar", "jotunn"]);
    paid("Scarab", ["medjay", "khopesh", "anubis", "ammit"]);
    paid("Whalebone", ["toa", "tahuanui", "tohunga", "taniwha"]);
    paid("Obsidian", ["coatecpatl", "ahuizotl", "chieftain", "tzitzimitl"]);
    paid("Jade", ["jaguar", "eagle", "sunpriest", "serpent"]);
    paid("Tsuba", ["samurai", "sohei", "shinobi", "oni", "tengu"]);
    paid("Anchor", ["marines", "gladiator", "beastmaster"]);
    paid("Void", ["dragonrider", "alchemist", "golem"]);
    // the first bonus units keep the game's own collectibles
    expect([priceOf.cragsmen, priceOf.spellwardens, priceOf.sentinel, priceOf.pavisiers, priceOf.battlemage]).toEqual([
      "Armor",
      "Lore",
      "Spirit",
      "Armor",
      "Medal",
    ]);
    // a culture's later units come from its earlier ones
    expect(UPGRADE_FROM.einherjar.from).toBe("shieldmaiden");
    expect(UPGRADE_FROM.jotunn.from).toBe("berserker");
    expect(UPGRADE_FROM.coatecpatl.from).toBe("jaguar");
    expect(UPGRADE_FROM.chieftain.from).toBe("eagle");
    expect(UPGRADE_FROM.golem.from).toBe("craftsmen"); // (beside the Stone Sentinel, not after it: three upgrades at most)
  });
});

describe("the Primal Warden", () => {
  const field = () => {
    const g = startBattle(makeGame(5204));
    only(g);
    return g;
  };
  it("is a hero made from a Druid with a Void Rift Crystal, and shifts between three shapes of its own", () => {
    expect(UPGRADE_FROM.warden).toEqual({ from: "druids", need: "Void" });
    expect(DEPLOY_ELITE.warden).toBe(true);
    expect(DEPLOY_COST.warden).toBe(300);
    for (const form of BONUS_FORMS) expect(DEPLOY_ORDER).not.toContain(form);
    const g = field();
    const warden = spawn(g, "warden", "blue", 10, 10);
    warden.hp = 70;
    expect(UNIT_TYPES.warden.shapeshiftForms).toEqual(["panther", "tortoise", "manta"]);
    expect(g._shapeshift(warden, "panther")).toBe(true);
    expect([warden.type, warden.hp, warden._druidType]).toEqual(["panther", 70, "warden"]); // HP carries over
    expect(warden.T.shapeshiftForms).toEqual(["druids", "tortoise", "manta"]);
    warden._shiftTurn = null;
    expect(g._shapeshift(warden, "druids")).toBe(true); // "druids" = its own first form
    expect(warden.type).toBe("warden");
  });
  it("Cleansing Touch: its heal mends 20 HP at 2 tiles and lifts acid, chill, blindness and holds", () => {
    const g = field();
    const warden = spawn(g, "warden", "blue", 10, 10),
      friend = spawn(g, "footmen", "blue", 12, 10);
    Object.assign(friend, { hp: 50, _acid: { turns: 3, by: warden }, _chilled: true, _blind: true, _seized: true });
    g.selected = warden;
    expect(g._clickHeal(friend)).toBe(true);
    for (let i = 0; i < 200; i++) step(g);
    expect(friend.hp).toBe(70);
    expect([friend._acid, friend._chilled, friend._blind, friend._seized]).toEqual([null, false, false, false]);
  });
  it("Storm-Stalker Panther: a Static Arc at 2–3 that it may follow with a move", () => {
    const T = UNIT_TYPES.panther;
    expect([T.minRange, T.range, T.move]).toEqual([1, 3, 8]);
    expect(T.shootMove).toBe(true);
  });
  it("Volcanic Siege-Tortoise: a mortar on a 3 by 3 area, never beside itself; blades do half, magic all", () => {
    const g = field();
    const tortoise = spawn(g, "tortoise", "blue", 5, 10),
      target = spawn(g, "footmen", "red", 9, 10),
      diagonal = spawn(g, "footmen", "red", 10, 11),
      apart = spawn(g, "footmen", "red", 11, 10);
    expect(g._weaponAt(tortoise, 4)).toBe(86);
    expect(g._weaponAt(tortoise, 1)).toBe(87); // only its Bite up close
    expect(UNIT_TYPES.tortoise.move).toBe(2);
    g.resolveDamage(tortoise, target, {});
    expect(target.hp).toBeLessThan(100);
    expect(diagonal.hp).toBeLessThan(100); // the corner of the 3 x 3
    expect(apart.hp).toBe(100);
    const sword = spawn(g, "swordsmen", "red", 5, 11),
      wizard = spawn(g, "wizards", "red", 5, 5);
    const T = tortoise.T;
    const blade = g._damage256(sword, tortoise),
      spell = g._damage256(wizard, tortoise, { weapon: 25 });
    tortoise.T = { ...T, physicalHalf: false };
    expect(blade).toBeLessThan(g._damage256(sword, tortoise));
    expect(spell).toBe(g._damage256(wizard, tortoise, { weapon: 25 }));
  });
  it("Astral Manta: its Void Beam goes on through three tiles beyond its target at full strength, friend or foe", () => {
    const g = field();
    const manta = spawn(g, "manta", "blue", 5, 10),
      target = spawn(g, "archers", "red", 7, 10),
      second = spawn(g, "archers", "red", 8, 10),
      friend = spawn(g, "footmen", "blue", 10, 10),
      beyond = spawn(g, "archers", "red", 11, 10),
      beside = spawn(g, "archers", "red", 7, 11);
    g.resolveDamage(manta, target, {});
    expect(100 - second.hp).toBe(100 - target.hp); // in full
    expect(friend.hp).toBeLessThan(100); // it does not spare its own side
    expect(beyond.hp).toBe(100); // four tiles in all
    expect(beside.hp).toBe(100);
    expect(UNIT_TYPES.manta.fly).toBe(true);
  });
});
