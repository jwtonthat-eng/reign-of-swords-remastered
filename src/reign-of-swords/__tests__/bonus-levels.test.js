// The BONUS campaigns (Tilicia & Isoluccia — ours, built by tools/ros/bonus/build_bonus.py into bonus.json): the
// records load beside Episode II's own maps and their scripted events fire through the original's scenario VM.
import { describe, it, expect } from "vitest";
import { loadEpisode, makeGame, startBattle, nextRound, put, step } from "./battle.js";
import { missionList } from "../engine/engine.js";
import { readFileSync } from "node:fs";
import { join } from "node:path";

await loadEpisode(2);
const mine = (g) => g.units.filter((u) => !u.dead && u.team === "blue" && !u.ally);
const foes = (g) => g.units.filter((u) => !u.dead && u.team === "red");

describe("bonus campaigns: loading", () => {
  it("adds 32 bonus battles to Episode II and leaves its own 100-odd maps in place", () => {
    const maps = missionList();
    const bonus = maps.filter((m) => m.mapId >= 5900 && m.mapId < 6000);
    expect(bonus.filter((m) => m.group === "story").length).toBe(18); // 3 in each of the six regions
    expect(bonus.filter((m) => m.group === "siege").length).toBe(14); // 3 + 3 + 2 + 2 + 2 + 2
    expect(maps.some((m) => m.mapId === 5432)).toBe(true);
  });
});

// Tilicia and Isoluccia are three story battles each, all fought with an army mustered from the budget (user decision):
// the battles that handed out a fixed force or preset troops are gone.
describe("Tilicia and Isoluccia: three battles each, every army mustered", () => {
  const region = (lo, hi) => missionList().filter((m) => m.mapId >= lo && m.mapId <= hi);
  it("keep Ostrak's Bargain, Frostgate, The Empty Tomb and The Harbour Chain, The Arsenal, Reign of the Battlemage", () => {
    const story = (lo, hi) =>
      region(lo, hi)
        .filter((m) => m.group === "story")
        .map((m) => m.mapId);
    expect(story(5901, 5910)).toEqual([5902, 5904, 5906]);
    expect(story(5921, 5930)).toEqual([5924, 5925, 5926]);
    for (const gone of [5901, 5903, 5905, 5921, 5922, 5923])
      expect(missionList().some((m) => m.mapId === gone)).toBe(false);
  });
  it("hand the player no troops: each battle and raid has a budget, a muster zone and no unit of yours on the field", () => {
    const built = JSON.parse(readFileSync(join("public", "games", "reign-of-swords-2", "bonus.json"), "utf8")).levels;
    const two = built.filter((l) => (l.mapId >= 5901 && l.mapId <= 5913) || (l.mapId >= 5921 && l.mapId <= 5933));
    expect(two.length).toBe(12); // 3 battles and 3 raids in each
    for (const level of two) {
      expect(level.budget, level.name).toBeGreaterThan(0);
      expect(level.deployZone.length, level.name).toBeGreaterThanOrEqual(12);
      expect(level.player, level.name).toEqual([]);
      // …nor does its script land any under your command later (a spawn into the player's own group)
      const landed = level.script.actions.filter((a) => a.op === 0 && a.gi === level.playerGroup);
      expect(landed, level.name).toEqual([]);
      // …and the battle opens on the muster with nobody of yours on the field (allied armies — Clan Ostrak, the Free
      // Company, the shipwrights — are not yours)
      const g = makeGame(level.mapId);
      step(g, 20);
      expect(g.phase, level.name).toBe("deploy");
      expect(mine(g).length, level.name).toBe(0);
    }
  });
  it("Bellaro's Free Company fights beside you at the harbour chain, and the Quarry of Giants has its Golem", () => {
    const chain = startBattle(makeGame(5924), "auto");
    expect(chain.units.filter((u) => u.ally && u.type === "marines").length).toBe(4);
    const quarry = startBattle(makeGame(5912), "auto");
    expect(foes(quarry).filter((u) => u.type === "golem").length).toBe(1);
    expect(foes(quarry).filter((u) => u.type === "sentinel").length).toBe(15);
  });
});

// ---- the scripted endings of the other battles, driven through the same scenario VM -------------------------------
const fell = (g, u) => {
  u.hp = 0;
  u.dead = true;
  u.dieT = 0;
  step(g, 30);
};
const tag = (g, n) => g.mission.script.triggers.filter((t) => t.tag === n);
// stand one of your units on a tile, as if it had just walked there
const reach = (g, u, [x, y]) => {
  put(g, u, x, y);
  g.scenario.onTileReached(u);
  step(g, 30);
};
// a hold battle is judged on its clock: keep the garrison alive and the field clear while the rounds pass
const holdUntil = (g, turn) => {
  for (let i = 0; i < 60 && g.turn < turn && g.phase === "player"; i++) {
    for (const u of g.units) if (u.team === "blue") u.hp = 100;
    for (const u of foes(g)) u.dead = true;
    nextRound(g);
  }
  step(g, 30);
};

describe("Tilicia: scripted endings", () => {
  it("Ostrak's Bargain is lost when the fourth clan band falls", () => {
    const g = startBattle(makeGame(5902), "auto");
    const clan = new Set(tag(g, 7).map((t) => t.a[0]));
    const bands = g.units.filter((u) => u.ally && clan.has(u.sid));
    expect(bands.length).toBe(6);
    bands.slice(0, 3).forEach((u) => fell(g, u));
    expect(g.phase).not.toBe("defeat");
    fell(g, bands[3]);
    expect(g.phase).toBe("defeat");
  });
  it("The Empty Tomb ends when Warden Tolm falls", () => {
    const g = startBattle(makeGame(5906), "auto");
    const tolm = foes(g).find((u) => u.type === "king");
    expect(tolm).toBeTruthy();
    expect(foes(g).some((u) => u.type === "sentinel")).toBe(true);
    fell(g, tolm);
    expect(g.phase).toBe("victory");
  });
  it("Winter Stores is won only once a unit has stood in both granaries", () => {
    const g = startBattle(makeGame(5913), "auto");
    const tiles = tag(g, 6);
    const gates = [...new Set(tiles.map((t) => t.a[2]))];
    expect(gates.length).toBe(2);
    const first = tiles.find((t) => t.a[2] === gates[0]),
      second = tiles.find((t) => t.a[2] === gates[1]);
    reach(g, mine(g)[0], first.a);
    expect(g.phase).not.toBe("victory");
    reach(g, mine(g)[1], second.a);
    expect(g.phase).toBe("victory");
  });
});

describe("Isoluccia: scripted endings", () => {
  it("The Harbour Chain is won only once both towers are taken", () => {
    const g = startBattle(makeGame(5924), "auto");
    const tiles = tag(g, 6);
    const gates = [...new Set(tiles.map((t) => t.a[2]))];
    expect(gates.length).toBe(2);
    reach(g, mine(g)[0], tiles.find((t) => t.a[2] === gates[0]).a);
    expect(g.phase).not.toBe("victory");
    reach(g, mine(g)[1], tiles.find((t) => t.a[2] === gates[1]).a);
    expect(g.phase).toBe("victory");
  });
  it("The Arsenal is held until round 13, and the Sentinels come ashore on the way", () => {
    const g = startBattle(makeGame(5925), "auto");
    let sentinels = false;
    for (let i = 0; i < 60 && g.turn < 13 && g.phase === "player"; i++) {
      sentinels = sentinels || foes(g).some((u) => u.type === "sentinel");
      for (const u of g.units) if (u.team === "blue") u.hp = 100;
      for (const u of foes(g)) u.dead = true;
      nextRound(g);
    }
    step(g, 30);
    expect(sentinels).toBe(true);
    expect(g.phase).toBe("victory");
  });
  it("Reign of the Battlemage goes on after the Doge falls and ends when the Battlemage does", () => {
    const g = startBattle(makeGame(5926), "auto");
    const doge = foes(g).find((u) => u.type === "king"),
      mage = foes(g).find((u) => u.type === "battlemage");
    expect(doge && mage).toBeTruthy();
    expect(doge.group).not.toBe(mage.group); // the Battlemage is an army of its own
    fell(g, doge);
    expect(g.phase).not.toBe("victory");
    fell(g, mage);
    expect(g.phase).toBe("victory");
  });
  it("Lighthouse Rock is held until round 11", () => {
    const g = startBattle(makeGame(5932), "auto");
    holdUntil(g, 11);
    expect(g.phase).toBe("victory");
  });
});

describe("Mare Nostra, Satoshi and the Mirror Sea: scripted endings", () => {
  it("The Admiral's Deck is fought on ships and ends when Admiral Corvane falls", () => {
    const g = startBattle(makeGame(5943), "auto");
    const corvane = foes(g).find((u) => u.type === "king");
    expect(corvane).toBeTruthy();
    expect(foes(g).some((u) => u.type === "gladiator")).toBe(true);
    // every unit stands on a deck: no one starts in the sea
    for (const u of g.units) expect(g.terrainAt(u.tx, u.ty).passable, u.type).toBe(true);
    fell(g, corvane);
    expect(g.phase).toBe("victory");
  });
  it("The Reaver-King is fought from ship to islet and ends when Skarl falls", () => {
    const g = startBattle(makeGame(5983), "auto");
    const skarl = foes(g).find((u) => u.type === "king");
    expect(foes(g).some((u) => u.type === "beastmaster")).toBe(true);
    for (const u of g.units) expect(g.terrainAt(u.tx, u.ty).passable, u.type).toBe(true);
    fell(g, skarl);
    expect(g.phase).toBe("victory");
  });
  it("Blockade Runner is held until round 9", () => {
    const g = startBattle(makeGame(5951), "auto");
    holdUntil(g, 9);
    expect(g.phase).toBe("victory");
  });
  it("Ishiro's Hill is lost if Lord Ishiro falls, and won by holding to round 11", () => {
    let g = startBattle(makeGame(5962), "auto");
    const ishiro = g.units.find((u) => u.ally && u.type === "king");
    expect(ishiro).toBeTruthy();
    expect(g.units.some((u) => u.ally && u.type === "samurai")).toBe(true);
    fell(g, ishiro);
    expect(g.phase).toBe("defeat");
    g = startBattle(makeGame(5962), "auto");
    holdUntil(g, 11);
    expect(g.phase).toBe("victory");
  });
  it("The Castle of Lord Kagemori ends when he falls", () => {
    const g = startBattle(makeGame(5963), "auto");
    const kagemori = foes(g).find((u) => u.type === "king");
    expect(foes(g).filter((u) => u.type === "samurai").length).toBeGreaterThan(3);
    fell(g, kagemori);
    expect(g.phase).toBe("victory");
  });
  it("The Shrine Pass is won by reaching the shrine", () => {
    const g = startBattle(makeGame(5971), "auto");
    const shrine = tag(g, 6)[0];
    reach(g, mine(g)[0], shrine.a);
    expect(g.phase).toBe("victory");
  });
});

describe("Tezcal: jungle battles and their scripted endings", () => {
  it("The Green Road is an ambush: Jaguar Warriors stand in the woods, and more come out behind you on round 3", () => {
    const g = startBattle(makeGame(5994), "auto");
    const jaguars = () => foes(g).filter((u) => u.type === "jaguar");
    expect(jaguars().length).toBeGreaterThanOrEqual(8);
    const before = g.units.filter((u) => u.type === "jaguar").length;
    for (let i = 0; i < 2 && g.phase === "player"; i++) nextRound(g);
    expect(g.turn).toBe(3);
    expect(g.units.filter((u) => u.type === "jaguar").length).toBe(before + 4);
    expect(g.units.some((u) => u.wave && u.type === "jaguar" && u.ty > 18)).toBe(true); // south of your muster
  });
  it("The Serpent Ford puts Eagle Warriors in the trees over the fords and Feathered Serpents in the air", () => {
    const g = startBattle(makeGame(5995), "auto");
    const eagles = foes(g).filter((u) => u.type === "eagle");
    expect(eagles.length).toBe(4);
    expect(eagles.every((u) => g.terrainAt(u.tx, u.ty).defBonus > 0)).toBe(true); // in the woods
    expect(foes(g).filter((u) => u.type === "serpent").length).toBe(2);
  });
  it("The Temple of the Sun ends when Sun-Speaker Itzcal falls, with Cuali's eagles on your side", () => {
    const g = startBattle(makeGame(5996), "auto");
    const priests = foes(g).filter((u) => u.type === "sunpriest");
    expect(priests.length).toBe(2); // the Speaker and one priest of his guard
    const itzcal = priests.find((u) => u.tx === 11 && u.ty === 4); // on the altar stone
    expect(itzcal).toBeTruthy();
    expect(g.units.some((u) => u.ally && u.type === "eagle")).toBe(true);
    fell(
      g,
      priests.find((u) => u !== itzcal),
    );
    expect(g.phase).not.toBe("victory"); // the guard priest is not the keystone
    fell(g, itzcal);
    expect(g.phase).toBe("victory");
  });
  it("The Night Hunt is held until round 9", () => {
    const g = startBattle(makeGame(5997), "auto");
    holdUntil(g, 9);
    expect(g.phase).toBe("victory");
  });
  it("The Sun Treasury is won by standing on the vault", () => {
    const g = startBattle(makeGame(5998), "auto");
    const u = mine(g)[0];
    put(g, u, 10, 2);
    g.scenario.onTileReached(u);
    step(g, 5);
    expect(g.phase).toBe("victory");
  });
});
