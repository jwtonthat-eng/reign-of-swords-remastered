// The three factions (ours; designs supplied by the user — data/bonus-units.js, MECHANICS.md §13): the Trench Brood,
// the Clockwork Syndicate and the Saurian Exiles. Twelve units, three upgrade tokens and the gift each token gives
// every unit made with it: Crush Depth, Overdrive, Apex Roar. Played on Episode II's own maps.
import { describe, it, expect } from "vitest";
import { loadEpisode, makeGame, startBattle, spawn, only, settle, step, nextRound, attack, moveTo } from "./battle.js";
import { UNIT_TYPES, DEPLOY_COST } from "../data/game-data.js";
import { WEAPON_DMG } from "../data/combat-data.js";
import { BONUS_ORDER, BONUS_UPGRADES, OVERDRIVE_COST, CALTROP_DAMAGE, FLOOD } from "../data/bonus-units.js";
import { COLLECTIBLES, TRADE_GOODS, RES_ICON, NEED_COLOR, UNIT_META } from "../data/shell-data.js";
import { DEPLOY_ELITE } from "../data/missions.js";
import { moveType, structTrans } from "../rules/terrain.js";

await loadEpisode(2);

const TRENCH = ["scuttler", "siren", "brinehurler", "behemoth"],
  CLOCKWORK = ["phalanx", "arccaster", "gyrocopter", "automaton"],
  SAURIAN = ["raptor", "ankylosaur", "pterosaur", "tyrant"];

// a clean board on Zayandi Shores (5424): only the units a test sets down. Its tiles x 4–13, y 3–7 are open ground.
function field() {
  const g = startBattle(makeGame(5424));
  only(g);
  return g;
}
// an idle friend and a far foe, so neither side's turn ends by itself
function keepers(g) {
  return [spawn(g, "swordsmen", "blue", 26, 4), spawn(g, "footmen", "red", 27, 9)];
}
// the first tile of terrain type `type` with open ground beside it: [tile, neighbour]
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

describe("the three factions: the data", () => {
  it("twelve units, four to a faction, each with its faction's gift, a cost, a camp card and its art", () => {
    for (const unit of [...TRENCH, ...CLOCKWORK, ...SAURIAN]) {
      expect(BONUS_ORDER, unit).toContain(unit);
      expect(DEPLOY_COST[unit], unit).toBeGreaterThan(0);
      expect(UNIT_META[unit].note, unit).toBeTruthy();
      expect(UNIT_TYPES[unit].frames, unit).toBe(4);
    }
    for (const unit of TRENCH) expect([UNIT_TYPES[unit].crush, UNIT_TYPES[unit].culture]).toEqual([true, "trench"]);
    for (const unit of CLOCKWORK)
      expect([UNIT_TYPES[unit].overdrive, UNIT_TYPES[unit].culture]).toEqual([true, "clockwork"]);
    for (const unit of SAURIAN) expect([UNIT_TYPES[unit].apexRoar, UNIT_TYPES[unit].culture]).toEqual([15, "saurian"]);
    // the two Huge units are elites: one per 1000 points
    expect([DEPLOY_ELITE.behemoth, DEPLOY_ELITE.tyrant, DEPLOY_ELITE.raptor]).toEqual([true, true, undefined]);
    // the two fliers fly
    expect([UNIT_TYPES.gyrocopter.fly, UNIT_TYPES.pterosaur.fly, UNIT_TYPES.gyrocopter.al]).toEqual([true, true, 0]);
  });
  it("three tokens: collectibles kept off the Merchant's counter, each the price of its own faction's four units", () => {
    const tokens = { Pearl: TRENCH, Mainspring: CLOCKWORK, Amber: SAURIAN };
    for (const [token, units] of Object.entries(tokens)) {
      const entry = COLLECTIBLES.find((c) => c.id === token);
      expect(entry && entry.token, token).toBeTruthy();
      expect(entry.gift, token).toBeTruthy();
      expect(TRADE_GOODS.some((c) => c.id === token)).toBe(false);
      expect(RES_ICON[token] && NEED_COLOR[token], token).toBeTruthy();
      expect(
        BONUS_UPGRADES.filter((u) => u.need === token)
          .map((u) => u.to)
          .sort(),
      ).toEqual([...units].sort());
    }
    // each faction's first unit comes straight from the Militia, and its Huge unit from one of its own
    for (const first of ["scuttler", "automaton", "raptor"])
      expect(BONUS_UPGRADES.find((u) => u.to === first).from).toBe("militiamen");
    expect(BONUS_UPGRADES.find((u) => u.to === "behemoth").from).toBe("scuttler");
    expect(BONUS_UPGRADES.find((u) => u.to === "tyrant").from).toBe("ankylosaur");
  });
});

describe("the Trench Brood", () => {
  it("Crush Depth: the foe any Trench unit strikes cannot move on its next turn; a war engine is not held", () => {
    const g = field();
    const scuttler = spawn(g, "scuttler", "blue", 6, 5),
      foe = spawn(g, "footmen", "red", 7, 5),
      engine = spawn(g, "catapult", "red", 6, 6);
    g.resolveDamage(scuttler, foe, {});
    g.resolveDamage(scuttler, engine, {});
    expect([g.moveOf(foe), g.moveOf(engine)]).toEqual([0, engine.T.move]);
    g._endTurnHide([foe]); // the hold ends with the victim's own turn
    expect(g.moveOf(foe)).toBe(foe.T.move);
  });
  it("Carapace: the shell turns 40% of a blow — unless the attacker has a friend directly opposite", () => {
    const g = field();
    const scuttler = spawn(g, "scuttler", "red", 6, 5),
      foe = spawn(g, "swordsmen", "blue", 5, 5);
    const T = scuttler.T;
    const shelled = g._damage256(foe, scuttler);
    scuttler.T = { ...T, carapace: 0 };
    const bare = g._damage256(foe, scuttler);
    scuttler.T = T;
    expect(shelled).toBe(Math.trunc((bare * 60) / 100));
    spawn(g, "footmen", "blue", 6, 6); // a friend on a side is a flank, not the underside
    expect(g._exposed(foe, scuttler)).toBe(false);
    only(g, scuttler, foe);
    spawn(g, "footmen", "blue", 7, 5); // directly opposite
    expect(g._exposed(foe, scuttler)).toBe(true);
    // the blow reads the Sword's No Armour column, with no shell on it: far more than the shelled blow
    expect(WEAPON_DMG[foe.T.weapon][0]).toBeGreaterThan(WEAPON_DMG[foe.T.weapon][scuttler.T.armour] * 3);
    expect(g._damage256(foe, scuttler)).toBeGreaterThan(shelled * 4);
  });
  it("Lure: the Siren drags a foe 2 tiles towards her and Snares it, without a scratch", () => {
    const g = field();
    keepers(g);
    const siren = spawn(g, "siren", "blue", 4, 5),
      foe = spawn(g, "footmen", "red", 8, 5),
      engine = spawn(g, "catapult", "red", 4, 7),
      brute = spawn(g, "behemoth", "red", 4, 3);
    expect([g._lureTarget(siren, foe), g._lureTarget(siren, engine), g._lureTarget(siren, brute)]).toEqual([
      true,
      false,
      false,
    ]);
    g.select(siren);
    expect(g.aimSkills().map((skill) => skill.id)).toContain("lure");
    g.aimSkill("lure");
    g.click({ tx: foe.tx, ty: foe.ty });
    settle(g);
    expect([foe.tx, foe.ty, foe.hp, g.moveOf(foe), siren.acted]).toEqual([6, 5, 100, 0, true]);
  });
  it("Lure: whatever stands in the way stops the drag, and a foe beside her is out of her reach", () => {
    const g = field();
    const siren = spawn(g, "siren", "blue", 4, 5),
      foe = spawn(g, "footmen", "red", 7, 5),
      close = spawn(g, "footmen", "red", 4, 6);
    spawn(g, "swordsmen", "blue", 6, 5); // in the way, with no step to the side that brings it nearer
    expect(g._lurePath(siren, foe)).toEqual([]);
    expect(g._lureTarget(siren, close)).toBe(false);
    g._lure(siren, foe);
    expect([foe.tx, g.moveOf(foe)]).toEqual([7, 0]); // not moved, but Snared all the same
  });
  it("Toxic Coral: the tile it lands on stays Flooded — double the cost and 20% more damage, but not for the Brood", () => {
    const g = field();
    keepers(g);
    const hurler = spawn(g, "brinehurler", "blue", 4, 5),
      foe = spawn(g, "footmen", "red", 8, 5),
      crab = spawn(g, "scuttler", "red", 8, 7),
      flier = spawn(g, "griffon", "red", 11, 7),
      striker = spawn(g, "swordsmen", "blue", 8, 4),
      walker = spawn(g, "footmen", "red", 11, 5);
    expect([UNIT_TYPES.brinehurler.minRange, UNIT_TYPES.brinehurler.range]).toEqual([1, 7]);
    const dry = g._damage256(striker, foe);
    const [walkDry, crabDry] = [g.moveCost(walker, 8, 5), g.moveCost(crab, 8, 5)];
    attack(g, hurler, foe);
    expect(g._floodedAt(8, 5)).toBe(true);
    expect(g._damage256(striker, foe)).toBeGreaterThan(dry);
    expect(FLOOD).toEqual({ cost: 2, damage: 20 });
    expect(g.moveCost(walker, 8, 5)).toBe(2 * walkDry);
    expect(g.moveCost(crab, 8, 5)).toBe(crabDry);
    expect(g.moveCost(flier, 8, 5)).toBe(1);
    // …and it floods empty ground too
    const second = spawn(g, "brinehurler", "blue", 4, 7);
    g.select(second);
    expect(g.aimSkills()[0].name).toBe("Toxic Coral");
    g.aimSkill("aim");
    g.click({ tx: 8, ty: 6 });
    settle(g);
    expect([g._floodedAt(8, 6), second.acted]).toEqual([true, true]);
  });
  it("Trench Behemoth: its bite takes in the foes on either side of its target, and nothing moves it", () => {
    const g = field();
    const brute = spawn(g, "behemoth", "blue", 6, 5),
      target = spawn(g, "archers", "red", 7, 5),
      above = spawn(g, "spellwardens", "red", 7, 4), // (heavy enough to stand the bite, and no Formation to share)
      below = spawn(g, "spellwardens", "red", 7, 6),
      behind = spawn(g, "archers", "red", 8, 5);
    const whole = g.computeDamage(brute, target);
    g.resolveDamage(brute, target, {});
    expect(Math.min(100, whole)).toBe(100 - target.hp);
    expect(above.hp).toBe(below.hp);
    expect(above.hp).toBeLessThan(100);
    expect(behind.hp).toBe(100);
    expect([g.moveOf(above), g.moveOf(below)]).toEqual([0, 0]); // Crush Depth goes with the bite
    // a Tengu's gale throws a footman back, never the Behemoth
    const tengu = spawn(g, "tengu", "red", 5, 5);
    g.resolveDamage(tengu, brute, {});
    expect([brute.tx, brute.ty]).toEqual([6, 5]);
    expect([UNIT_TYPES.behemoth.fear, UNIT_TYPES.behemoth.anchored, UNIT_TYPES.behemoth.aquatic]).toEqual([
      true,
      true,
      true,
    ]);
  });
});

describe("the Clockwork Syndicate", () => {
  it("Overdrive: wound up, a unit acts twice in the turn and then loses 25 HP", () => {
    const g = field();
    keepers(g);
    const phalanx = spawn(g, "phalanx", "blue", 6, 5),
      foe = spawn(g, "catapult", "red", 7, 5); // it stands one blow and gives none back
    g.select(phalanx);
    expect(g.aimSkills().map((skill) => skill.id)).toContain("overdrive");
    g.aimSkill("overdrive");
    expect(phalanx._od).toEqual({ turn: g.turn, stage: 0 });
    attack(g, phalanx, foe);
    const afterOne = foe.hp;
    expect(afterOne).toBeLessThan(100);
    expect([phalanx.acted, phalanx._od.stage, g.selected === phalanx, phalanx.hp]).toEqual([false, 1, true, 100]);
    attack(g, phalanx, foe);
    expect(foe.hp).toBeLessThan(afterOne);
    expect([phalanx.acted, phalanx._od.stage, phalanx.hp]).toEqual([true, 2, 100 - OVERDRIVE_COST]);
  });
  it("Overdrive: tapped again before acting the spring is let down; unfinished, it is still paid for at the turn's end", () => {
    const g = field();
    keepers(g);
    const caster = spawn(g, "arccaster", "blue", 6, 5);
    g.select(caster);
    g.aimSkill("overdrive");
    g.aimSkill("overdrive");
    expect(caster._od).toBe(null);
    g.aimSkill("overdrive");
    g.holdUnit(); // its first action: nothing
    expect([caster.acted, caster._od.stage, caster.hp]).toEqual([false, 1, 100]);
    nextRound(g); // the turn ends with the second action never taken
    expect(caster.hp).toBe(100 - OVERDRIVE_COST);
  });
  it("Overdrive under the computer: a healthy unit with a foe in reach acts twice and pays", () => {
    const g = field();
    const group = g.mission.groupOrder.find((x) => x.side === "enemy").gi; // (an enemy army that takes a turn)
    const mine = spawn(g, "catapult", "blue", 6, 5); // it gives no blow back
    spawn(g, "swordsmen", "blue", 26, 4);
    const automaton = spawn(g, "automaton", "red", 9, 5, { group });
    const whole = g.computeDamage(automaton, mine);
    nextRound(g);
    expect([automaton._od && automaton._od.stage, automaton.hp]).toEqual([2, 100 - OVERDRIVE_COST]);
    expect(100 - mine.hp).toBeGreaterThan(whole); // two rams
  });
  it("Shield Lock: two Brass Phalanx side by side take 30% less from every shot, and no less hand to hand", () => {
    const g = field();
    const phalanx = spawn(g, "phalanx", "red", 6, 5),
      archers = spawn(g, "archers", "blue", 6, 3),
      sword = spawn(g, "swordsmen", "blue", 5, 5);
    spawn(g, "phalanx", "red", 7, 5);
    // (two Formation units side by side also share the original's 10% formation cover: measure the lock alone)
    const T = phalanx.T;
    phalanx.T = { ...T, shieldLock: 0 };
    const [shot, blow] = [g._damage256(archers, phalanx), g._damage256(sword, phalanx)];
    phalanx.T = T;
    expect(shot).toBeGreaterThan(0);
    expect(g._damage256(archers, phalanx)).toBe(Math.trunc((shot * 70) / 100));
    expect(g._damage256(sword, phalanx)).toBe(blow);
    only(g, phalanx, archers, sword); // alone, its shield is only its own
    expect(g._shieldLocked(phalanx)).toBe(false);
  });
  it("Chain Arc: the bolt leaps at half strength to heavy armour beside its target, or to anyone if the target stands in water", () => {
    const g = field();
    const caster = spawn(g, "arccaster", "blue", 4, 5),
      target = spawn(g, "archers", "red", 7, 5),
      light = spawn(g, "archers", "red", 7, 6),
      heavy = spawn(g, "knights", "red", 8, 5);
    expect([UNIT_TYPES.arccaster.minRange, UNIT_TYPES.arccaster.range, UNIT_TYPES.arccaster.shootMove]).toEqual([
      1,
      4,
      true,
    ]);
    const full = g.computeDamage(caster, heavy, { weapon: 94 });
    g.resolveDamage(caster, target, {});
    step(g, 10);
    expect(target.hp).toBeLessThan(100);
    expect(light.hp).toBe(100); // dry ground, light armour: no leap to it
    expect(100 - heavy.hp).toBe(Math.max(1, Math.round((full * 128) / 256)));
    // in the shallows the bolt leaps to whoever stands beside the target
    const shore = field();
    const edge = edgeTile(shore, 5);
    expect(edge).toBeTruthy();
    const [[wx, wy], [nx, ny]] = edge;
    const wet = spawn(shore, "archers", "red", wx, wy),
      beside = spawn(shore, "archers", "red", nx, ny),
      second = spawn(shore, "arccaster", "blue", 10, 5);
    shore.resolveDamage(second, wet, { weapon: 94 });
    step(shore, 10);
    expect(wet.hp).toBeLessThan(100);
    expect(beside.hp).toBeLessThan(100);
  });
  it("Caltrops: what the Gyrocopter strews stops and wounds an enemy on foot, not a flier, not its own side", () => {
    const g = field();
    keepers(g);
    const gyro = spawn(g, "gyrocopter", "red", 8, 5),
      mine = spawn(g, "footmen", "blue", 6, 5);
    g.resolveDamage(gyro, mine, {});
    expect(g._caltropsAt(6, 5)).toBe("red");
    g._layCaltrops(5, 3, "red");
    const walker = spawn(g, "footmen", "blue", 4, 3);
    moveTo(g, walker, 5, 3);
    expect([walker.tx, walker.hp]).toEqual([5, 100 - CALTROP_DAMAGE]);
    // a ground unit cannot walk on through them: the tile beyond costs the way round
    const runner = spawn(g, "cavalry", "blue", 4, 7);
    g._layCaltrops(5, 7, "red");
    const reach = g.computeReach(runner);
    expect(reach.dist.get("6,7")).toBeGreaterThan(2);
    expect(reach.stops.has("5,7")).toBe(true);
    const griffon = spawn(g, "griffon", "blue", 10, 3),
      theirs = spawn(g, "footmen", "red", 10, 7);
    g._layCaltrops(11, 3, "red");
    g._layCaltrops(11, 7, "red");
    expect([g._caltropsAgainst(griffon, 11, 3), g._caltropsAgainst(theirs, 11, 7)]).toEqual([false, false]);
    expect(g._weaponUselessVs(gyro, griffon, 2)).toBe(true); // nor can it strew them on a flier
    // an enemy standing on or beside them can spend its action to clear them
    const sweeper = spawn(g, "footmen", "blue", 5, 4);
    g.select(sweeper);
    expect(g.aimSkills().map((skill) => skill.id)).toContain("sweep_caltrops");
    g.aimSkill("sweep_caltrops");
    settle(g);
    expect([g._caltropsAt(5, 3), sweeper.acted]).toEqual([null, true]);
  });
  it("Volatile Automaton: it bursts on all eight tiles when it falls, friend or foe, and one blast sets off the next", () => {
    const g = field();
    const bomb = spawn(g, "automaton", "red", 6, 5, { hp: 5 }),
      killer = spawn(g, "swordsmen", "blue", 5, 5),
      friend = spawn(g, "footmen", "red", 7, 6), // diagonal: still inside the blast
      second = spawn(g, "automaton", "red", 7, 5, { hp: 5 }),
      far = spawn(g, "footmen", "red", 8, 5), // beside the second bomb only
      safe = spawn(g, "footmen", "red", 10, 5);
    g.resolveDamage(killer, bomb, {});
    expect([bomb.dead, second.dead]).toEqual([true, true]);
    expect(killer.hp).toBeLessThan(100);
    expect(friend.hp).toBeLessThan(100);
    expect(far.hp).toBeLessThan(100);
    expect(safe.hp).toBe(100);
    // no Priest can mend one
    const priest = spawn(g, "priests", "red", 12, 3);
    spawn(g, "automaton", "red", 12, 4, { hp: 40 });
    expect(g._canHealNow(priest)).toBe(false);
    expect([UNIT_TYPES.automaton.unyielding, UNIT_TYPES.automaton.fearless]).toEqual([true, true]);
  });
});

describe("the Saurian Exiles", () => {
  it("Apex Roar: a kill gives every friend within 2 tiles +15 attack until the end of its next turn", () => {
    const g = field();
    const raptor = spawn(g, "raptor", "blue", 6, 5),
      near = spawn(g, "ankylosaur", "blue", 6, 7),
      far = spawn(g, "ankylosaur", "blue", 10, 7),
      prey = spawn(g, "archers", "red", 7, 5, { hp: 1 }),
      dummy = spawn(g, "footmen", "red", 7, 7);
    const before = g._damage256(near, dummy);
    g.resolveDamage(raptor, prey, {});
    expect([prey.dead, near._roar, far._roar || 0, raptor._roar || 0]).toEqual([true, 15, 0, 0]);
    expect(g._damage256(near, dummy)).toBeGreaterThan(before);
    g._endTurnHide([near]);
    expect(near._roar).toBe(0);
    expect(g._damage256(near, dummy)).toBe(before);
  });
  it("Pack Hunter: a Raptor's blow at a foe caught between it and a friend ignores armour and cover", () => {
    const g = field();
    const raptor = spawn(g, "raptor", "blue", 5, 5),
      knight = spawn(g, "knights", "red", 6, 5);
    const alone = g._damage256(raptor, knight);
    spawn(g, "footmen", "blue", 6, 6); // on a side: the original's flank bonus only
    const flanked = g._damage256(raptor, knight);
    spawn(g, "footmen", "blue", 7, 5); // directly opposite
    const caught = g._damage256(raptor, knight);
    expect(flanked).toBeGreaterThan(alone);
    expect(caught).toBeGreaterThan(flanked * 2);
    // a Bulwark gives no opening
    const sentinel = spawn(g, "sentinel", "red", 10, 7);
    const lone = spawn(g, "raptor", "blue", 9, 7);
    const base = g._damage256(lone, sentinel);
    spawn(g, "footmen", "blue", 11, 7);
    expect(g._damage256(lone, sentinel)).toBe(base);
    expect(UNIT_TYPES.raptor.move).toBe(7);
  });
  it("Spiked Shell: whoever strikes an Ankylosaur hand to hand takes back 30% of the blow; a shot costs nothing", () => {
    const g = field();
    const beast = spawn(g, "ankylosaur", "red", 6, 5),
      sword = spawn(g, "greatswordsmen", "blue", 5, 5),
      archers = spawn(g, "archers", "blue", 6, 3);
    const blow = g.computeDamage(sword, beast);
    expect(blow).toBeGreaterThan(3);
    g.resolveDamage(sword, beast, {});
    expect(100 - sword.hp).toBe(Math.round((blow * 30) / 100));
    g.resolveDamage(archers, beast, {});
    expect(archers.hp).toBe(100);
  });
  it("Harvest: a Pterosaur lifts a hazard off the map and drops it, with a burst, where its next stone lands", () => {
    const g = field();
    keepers(g);
    const ptero = spawn(g, "pterosaur", "blue", 4, 5);
    g.select(ptero);
    expect(g.aimSkills().find((skill) => skill.id === "harvest").disabled).toBe(true); // nothing to lift here
    g._layCaltrops(4, 6, "red");
    expect(g._harvestable(ptero, 4, 6)).toBe("caltrops");
    expect(g._harvestable(ptero, 4, 7)).toBe(null); // not beside it
    g.select(ptero);
    g.aimSkill("harvest");
    g.click({ tx: 4, ty: 6 });
    settle(g);
    expect([ptero._cargo, g._caltropsAt(4, 6), ptero.acted]).toEqual(["caltrops", null, true]);
    const target = spawn(g, "footmen", "red", 6, 5),
      beside = spawn(g, "footmen", "red", 6, 6),
      apart = spawn(g, "footmen", "red", 8, 5);
    ptero._cargo = null;
    const plain = g.computeDamage(ptero, target);
    ptero._cargo = "caltrops";
    const loaded = g.computeDamage(ptero, target);
    expect(loaded).toBeGreaterThan(plain);
    g.resolveDamage(ptero, target, {});
    expect([ptero._cargo, g._caltropsAt(6, 5)]).toEqual([null, "blue"]); // they are its own side's now
    expect(100 - target.hp).toBe(loaded);
    expect(beside.hp).toBeLessThan(100);
    expect(apart.hp).toBe(100);
    // quicksand and Flooded ground travel the same way
    const second = spawn(g, "pterosaur", "blue", 10, 5);
    g._flood(10, 6);
    g._harvest(second, 10, 6);
    g.resolveDamage(second, spawn(g, "footmen", "red", 12, 5), {});
    expect([g._floodedAt(10, 6), g._floodedAt(12, 5)]).toEqual([false, true]);
  });
  it("Devastation: whatever the Tyrant's jaws close on comes straight down, and stays down", () => {
    const g = startBattle(makeGame(5428));
    only(g);
    let wall = null;
    for (let y = 1; y < g.rows - 1 && !wall; y++)
      for (let x = 1; x < g.cols - 1 && !wall; x++)
        if (g.isStructure(x, y) && structTrans(structTrans(g.tileAt(x, y))) != null) wall = [x, y]; // two stages to fall
    expect(wall).toBeTruthy();
    const [x, y] = wall;
    const tyrant = spawn(g, "tyrant", "blue", x - 1, y),
      knights = spawn(g, "knights", "blue", x + 1, y);
    expect(g._structDmgCol(knights, 1, g.tileAt(x, y))).toBe(0); // a lance does nothing to it
    expect(g._structDmgCol(tyrant, 1, g.tileAt(x, y))).toBeGreaterThan(0);
    expect(g.structureHit(tyrant, x, y)).toBe(true);
    expect(structTrans(g.tileAt(x, y))).toBe(null); // its last stage, in one bite
    expect(g.razed.has(x + "," + y)).toBe(true);
    expect([UNIT_TYPES.tyrant.fear, UNIT_TYPES.tyrant.fearless, UNIT_TYPES.tyrant.raze]).toEqual([true, true, true]);
  });
});
