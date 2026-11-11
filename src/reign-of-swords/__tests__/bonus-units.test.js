// The six BONUS units (Tilicia & Isoluccia — ours, data/bonus-units.js) and their abilities: Climb, Nullify,
// Unyielding, Amphibious, Pavise and Chain Lightning. Played on Episode II's own maps.
import { describe, it, expect } from "vitest";
import { loadEpisode, makeGame, startBattle, spawn, only, settle, step, nextRound } from "./battle.js";
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
  it("fourteen units, each on an original weapon row and armour column, with a cost and a courage tier", () => {
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
    expect(skill("sentinel")).toEqual(expect.arrayContaining(["Unyielding", "Fear", "Last Strike", "Fearless"]));
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
      ["footmen", "marines", "Spirit"],
      ["crossbowmen", "pavisiers", "Armor"],
      ["wizards", "battlemage", "Medal"],
      ["halberdiers", "gladiator", "Weapons"],
      ["swordsmen", "samurai", "Spirit"],
      ["griffon", "dragonrider", "Medal"],
      ["militiamen", "beastmaster", "Medal"],
      ["priests", "sohei", "Weapons"],
      ["rangers", "shinobi", "Lore"],
      ["greatswordsmen", "oni", "Spirit"],
      ["griffon", "tengu", "Spirit"],
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
  it("Battlemage: Chain Lightning at 2–7, teleports like a Wizard, strikes first, may attack after moving", () => {
    const g = field();
    const mage = spawn(g, "battlemage", "blue", 5, 5),
      far = spawn(g, "footmen", "red", 12, 5),
      beyond = spawn(g, "footmen", "red", 13, 6);
    expect(mage.T.minRange).toBe(1);
    expect(mage.T.range).toBe(7);
    expect(g.targetsFrom(mage, 5, 5)).toContain(far); // 7 away
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
  it("Marines: a Boarding Musket at 2–3 from open ground, 2 from rough ground, a Short Sword up close", () => {
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
    expect(g._weaponAt(marine, 1)).toBe(8);
    expect(g.targetsFrom(marine, open[0], open[1], false)).toEqual(expect.arrayContaining([at2, at3]));
    expect(g.targetsFrom(marine, open[0], open[1], true)).toEqual([]); // Move or Shoot
    expect(g.computeDamage(marine, at3)).toBe(
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
  it("a 750-point elite flier in Relic Armour at the Hero's rating, upgraded from Griffon Riders with a Medal", () => {
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
    expect(UPGRADE_FROM.dragonrider).toEqual({ from: "griffon", need: "Medal" });
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
    expect(UPGRADE_FROM.beastmaster).toEqual({ from: "militiamen", need: "Medal" });
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
  it("Earthshaker: the Oni's blow also lands, at half strength, on every other enemy beside its target", () => {
    const g = field();
    const oni = spawn(g, "oni", "blue", 10, 10),
      target = spawn(g, "footmen", "red", 11, 10),
      beside = spawn(g, "footmen", "red", 12, 10),
      besideOni = spawn(g, "footmen", "red", 10, 11),
      friend = spawn(g, "footmen", "blue", 11, 9);
    g.resolveDamage(oni, target);
    expect(target.hp).toBeLessThan(100);
    expect(beside.hp).toBeLessThan(100);
    expect(100 - beside.hp).toBeLessThan(100 - target.hp);
    expect(besideOni.hp).toBe(100); // beside the Oni, not beside the target
    expect(friend.hp).toBe(100);
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
    expect([DEPLOY_COST.sohei, DEPLOY_COST.shinobi, DEPLOY_COST.oni, DEPLOY_COST.tengu]).toEqual([175, 225, 350, 225]);
    expect(upgradeGate("sohei", true)).toBe(5961);
    expect(upgradeGate("shinobi", true)).toBe(5962);
    expect(upgradeGate("oni", true)).toBe(5963);
    expect(upgradeGate("tengu", true)).toBe(5963);
  });
});
