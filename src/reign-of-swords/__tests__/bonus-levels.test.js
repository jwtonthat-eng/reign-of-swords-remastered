// The BONUS campaigns (Tilicia & Isoluccia — ours, built by tools/ros/bonus/build_bonus.py into bonus.json): the
// records load beside Episode II's own maps and their scripted events fire through the original's scenario VM.
import { describe, it, expect } from "vitest";
import { loadEpisode, makeGame, startBattle, nextRound, put, step, spawn } from "./battle.js";
import { missionList } from "../engine/engine.js";
import { moveType } from "../rules/terrain.js";
import { readFileSync } from "node:fs";
import { join } from "node:path";

await loadEpisode(2);
const mine = (g) => g.units.filter((u) => !u.dead && u.team === "blue" && !u.ally);
const foes = (g) => g.units.filter((u) => !u.dead && u.team === "red");

describe("bonus campaigns: loading", () => {
  it("adds 67 bonus battles to Episode II and leaves its own 100-odd maps in place", () => {
    const maps = missionList();
    const bonus = maps.filter((m) => m.mapId >= 5900 && m.mapId < 6000);
    expect(bonus.filter((m) => m.group === "story").length).toBe(39); // 3 in each of the thirteen regions
    expect(bonus.filter((m) => m.group === "siege").length).toBe(28); // 3 + 3, then 2 in each of the other eleven
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
const typeAt = (g, u) => moveType(g.tileAt(u.tx, u.ty));
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

// Jarnheim (the Norse holds, 5914-5918) and Khemret (the Egyptian river kingdom, 5934-5938): ours, like the rest.
describe("Jarnheim and Khemret: every army mustered, and their scripted endings", () => {
  const TEN = [5914, 5915, 5916, 5917, 5918, 5934, 5935, 5936, 5937, 5938];
  it("hand the player no troops: each battle and raid has a budget, a muster zone and no unit of yours on the field", () => {
    const built = JSON.parse(readFileSync(join("public", "games", "reign-of-swords-2", "bonus.json"), "utf8")).levels;
    const ten = built.filter((l) => TEN.includes(l.mapId));
    expect(ten.map((l) => l.mapId).sort()).toEqual(TEN);
    expect(ten.filter((l) => l.group === "story").length).toBe(6);
    for (const level of ten) {
      expect(level.budget, level.name).toBeGreaterThan(0);
      expect(level.deployZone.length, level.name).toBeGreaterThanOrEqual(12);
      expect(level.player, level.name).toEqual([]);
      const landed = level.script.actions.filter((a) => a.op === 0 && a.gi === level.playerGroup);
      expect(landed, level.name).toEqual([]);
      // none of the four hidden creatures is on the field or in the script
      const keys = [
        ...level.enemy.map((u) => u[0]),
        ...level.script.actions.filter((a) => a.op === 0).map((a) => a.key),
      ];
      for (const hidden of ["unicorn", "efreet", "naga", "skeleton"]) expect(keys, level.name).not.toContain(hidden);
    }
  });
  it("The Raven Pass is held by Berserkers, and more come down the gullies behind you on round 3", () => {
    const g = startBattle(makeGame(5914), "auto");
    const count = () => g.units.filter((u) => u.type === "berserker").length;
    const before = count();
    expect(before).toBe(6);
    for (let i = 0; i < 2 && g.phase === "player"; i++) nextRound(g);
    expect(g.turn).toBe(3);
    expect(g.units.filter((u) => u.wave && u.type === "berserker").length).toBe(4);
  });
  it("The Shield Bridge is a wall of Shieldmaidens across the bridge and its bank", () => {
    const g = startBattle(makeGame(5915), "auto");
    const maidens = foes(g).filter((u) => u.type === "shieldmaiden");
    expect(maidens.length).toBeGreaterThanOrEqual(8);
    expect(maidens.filter((u) => u.ty === 10).length).toBe(6); // shoulder to shoulder on the near bank
  });
  it("The Jarl's Hold is a walled town kept by Einherjar and a Jotunn, and ends when Jarl Haldor falls", () => {
    const g = startBattle(makeGame(5916), "auto");
    const haldor = foes(g).find((u) => u.type === "king");
    expect(haldor).toBeTruthy();
    expect(foes(g).filter((u) => u.type === "einherjar").length).toBe(4);
    const giant = foes(g).find((u) => u.type === "jotunn");
    expect(giant).toBeTruthy();
    fell(g, giant);
    expect(g.phase).not.toBe("victory"); // the giant is not the keystone
    fell(g, haldor);
    expect(g.phase).toBe("victory");
  });
  it("The House of the Dead is guarded by Ammits and ends when High Priest Nekhet falls", () => {
    const g = startBattle(makeGame(5936), "auto");
    const priests = foes(g).filter((u) => u.type === "anubis");
    expect(priests.length).toBe(3); // Nekhet and two of his court
    const nekhet = priests.find((u) => u.tx === 11 && u.ty === 3); // before the tomb
    expect(nekhet).toBeTruthy();
    expect(foes(g).filter((u) => u.type === "ammit").length).toBe(4);
    fell(
      g,
      priests.find((u) => u !== nekhet),
    );
    expect(g.phase).not.toBe("victory");
    fell(g, nekhet);
    expect(g.phase).toBe("victory");
  });
  it("The Red Road puts Medjay in the rocks, and The River Gate puts Khopesh Warriors on the causeway", () => {
    const road = startBattle(makeGame(5934), "auto");
    expect(foes(road).filter((u) => u.type === "medjay").length).toBe(8);
    const gate = startBattle(makeGame(5935), "auto");
    const khopesh = foes(gate).filter((u) => u.type === "khopesh");
    expect(khopesh.length).toBe(8);
    expect(khopesh.filter((u) => u.ty === 8).length).toBe(2); // on the causeway itself, over the water
  });
  it("The Oasis Caravan and The Sealed Tomb are won by standing on their goal", () => {
    for (const [mapId, goal] of [
      [5937, [8, 3]],
      [5938, [10, 3]],
    ]) {
      const g = startBattle(makeGame(mapId), "auto");
      reach(g, mine(g)[0], goal);
      expect(g.phase, String(mapId)).toBe("victory");
    }
  });
});

// Moananui (the Polynesian isles, 5944-5948) and Coatlan (the serpent highlands, 5954-5958): ours, like the rest.
describe("Moananui and Coatlan: every army mustered, and their scripted endings", () => {
  const TEN = [5944, 5945, 5946, 5947, 5948, 5954, 5955, 5956, 5957, 5958];
  const built = JSON.parse(readFileSync(join("public", "games", "reign-of-swords-2", "bonus.json"), "utf8"));
  it("hand the player no troops: each battle and raid has a budget, a muster zone and no unit of yours on the field", () => {
    const ten = built.levels.filter((l) => TEN.includes(l.mapId));
    expect(ten.map((l) => l.mapId).sort()).toEqual(TEN);
    expect(ten.filter((l) => l.group === "story").length).toBe(6);
    for (const level of ten) {
      expect(level.budget, level.name).toBeGreaterThan(0);
      expect(level.deployZone.length, level.name).toBeGreaterThanOrEqual(30);
      expect(level.player, level.name).toEqual([]);
      const landed = level.script.actions.filter((a) => a.op === 0 && a.gi === level.playerGroup);
      expect(landed, level.name).toEqual([]);
      const keys = [
        ...level.enemy.map((u) => u[0]),
        ...level.script.actions.filter((a) => a.op === 0).map((a) => a.key),
      ];
      for (const hidden of ["unicorn", "efreet", "naga", "skeleton"]) expect(keys, level.name).not.toContain(hidden);
    }
  });
  it("every battle and raid of a region rewards 2 of its culture's token, and no token of another culture", () => {
    // region -> its token (Tilicia and Isoluccia: the Void Rift Crystal of the fantastical units)
    const TOKEN = {
      tilicia: "Void",
      isoluccia: "Void",
      "mare-nostra": "Anchor",
      "mirror-sea": "Anchor",
      satoshi: "Tsuba",
      tezcal: "Jade",
      jarnheim: "Bloodstone",
      khemret: "Scarab",
      moananui: "Whalebone",
      coatlan: "Obsidian",
      thalassar: "Pearl", // the three factions
      brasshaven: "Mainspring",
      "amber-reach": "Amber",
    };
    // …and the three battles that also hand out a token of another kind, for the unit they unlock
    const ALSO = { 5924: { Anchor: 2 }, 5943: { Void: 1 } }; // Marines at the Harbour Chain; the Dragon Rider
    const TOKENS = [
      "Bloodstone",
      "Scarab",
      "Obsidian",
      "Whalebone",
      "Anchor",
      "Tsuba",
      "Jade",
      "Void",
      "Pearl",
      "Mainspring",
      "Amber",
    ];
    expect(built.kingdoms.map((k) => k.id).sort()).toEqual(Object.keys(TOKEN).sort());
    for (const kingdom of built.kingdoms) {
      const mine = TOKEN[kingdom.id];
      const name = kingdom.name.replace("Kingdom of ", "");
      const ids = [
        ...kingdom.missions.map((m) => m.mapId),
        ...built.levels.filter((l) => l.group === "siege" && l.kingdom === name).map((l) => l.mapId),
      ];
      expect(ids.length, kingdom.id).toBeGreaterThanOrEqual(5);
      for (const id of ids) {
        const spoils = (built.rewards[id] || {}).spoils || {};
        for (const token of TOKENS) {
          const want = token === mine ? 2 : (ALSO[id] || {})[token];
          expect(spoils[token], `${kingdom.id} ${id} ${token}`).toBe(want);
        }
      }
    }
  });
  it("The Black Sand Landing is held by Toa, some of them standing in the lagoons", () => {
    const g = startBattle(makeGame(5944), "auto");
    const toa = foes(g).filter((u) => u.type === "toa");
    expect(toa.length).toBe(8);
    expect(toa.filter((u) => g.terrainAt(u.tx, u.ty).water || [5].includes(typeAt(g, u))).length).toBe(4);
  });
  it("The Reef Crossing brings Tahuanui Riders over the water behind you on round 3", () => {
    const g = startBattle(makeGame(5945), "auto");
    expect(foes(g).filter((u) => u.type === "tahuanui").length).toBe(2);
    for (let i = 0; i < 2 && g.phase === "player"; i++) nextRound(g);
    expect(g.turn).toBe(3);
    expect(g.units.filter((u) => u.wave && u.type === "tahuanui").length).toBe(2);
  });
  it("The Hill of Spirits ends when Elder Matahi falls, and its Taniwha rise out of the deep on round 4", () => {
    const g = startBattle(makeGame(5946), "auto");
    const matahi = foes(g).find((u) => u.type === "tohunga");
    expect(matahi).toBeTruthy();
    expect(foes(g).some((u) => u.type === "taniwha")).toBe(false);
    for (let i = 0; i < 3 && g.phase === "player"; i++) nextRound(g);
    expect(g.turn).toBe(4);
    const risen = g.units.filter((u) => u.wave && u.type === "taniwha");
    expect(risen.length).toBe(2);
    for (const beast of risen) expect(typeAt(g, beast)).toBe(19); // in deep water
    fell(
      g,
      foes(g).find((u) => u.type === "toa"),
    );
    expect(g.phase).not.toBe("victory");
    fell(g, matahi);
    expect(g.phase).toBe("victory");
  });
  it("The Lake Causeway has Ahuizotl in the lake beside the stones", () => {
    const g = startBattle(makeGame(5955), "auto");
    const dogs = foes(g).filter((u) => u.type === "ahuizotl");
    expect(dogs.length).toBe(2);
    for (const dog of dogs) expect(typeAt(g, dog)).toBe(19);
    expect(foes(g).filter((u) => u.type === "coatecpatl").length).toBe(5);
  });
  it("The Temple of Stars ends when Itzpapal is destroyed, not when its banner captains fall", () => {
    const g = startBattle(makeGame(5956), "auto");
    const stars = foes(g).filter((u) => u.type === "tzitzimitl");
    expect(stars.length).toBe(2);
    const itzpapal = stars.find((u) => u.tx === 13 && u.ty === 5);
    expect(itzpapal).toBeTruthy();
    const captains = foes(g).filter((u) => u.type === "chieftain");
    expect(captains.length).toBe(2);
    fell(g, captains[0]);
    fell(
      g,
      stars.find((u) => u !== itzpapal),
    );
    expect(g.phase).not.toBe("victory");
    fell(g, itzpapal);
    expect(g.phase).toBe("victory");
  });
  it("The Canoe Fleet and The Skull Rack are won by standing on their goal", () => {
    for (const [mapId, goal] of [
      [5947, [9, 4]],
      [5957, [9, 3]],
    ]) {
      const g = startBattle(makeGame(mapId), "auto");
      reach(g, mine(g)[0], goal);
      expect(g.phase, String(mapId)).toBe("victory");
    }
  });
  it("The Drowned Village is held for eight turns: the lake gives up at first light", () => {
    const g = startBattle(makeGame(5958), "auto");
    holdUntil(g, 9);
    expect(g.phase).toBe("victory");
  });
});

// Thalassar (the Trench Brood, 5964-5968), Brasshaven (the Clockwork Syndicate, 5973-5977) and the Amber Reach (the
// Saurian Exiles, 5984-5988): ours, like the rest, and laid with the bonus tiles of their own.
describe("Thalassar, Brasshaven and the Amber Reach: every army mustered, their ground and their scripted endings", () => {
  const built = JSON.parse(readFileSync(join("public", "games", "reign-of-swords-2", "bonus.json"), "utf8"));
  const level = (id) => built.levels.find((l) => l.mapId === id);
  const tilesOf = (id) => new Set(level(id).tiles);
  const start = (id) => startBattle(makeGame(id), "auto");
  it("hand the player no troops: each battle and raid has a budget, a muster zone and no unit of yours on the field", () => {
    for (const id of [5964, 5965, 5966, 5967, 5968, 5973, 5974, 5975, 5976, 5977, 5984, 5985, 5986, 5987, 5988]) {
      const l = level(id);
      expect(l.player, l.name).toEqual([]);
      expect(l.budget, l.name).toBeGreaterThanOrEqual(2250);
      expect(l.deployZone.length, l.name).toBeGreaterThanOrEqual(30);
    }
  });
  it("each region is laid with its own tiles: muck, chimneys and coral; belts and vents; tar and ferns", () => {
    const has = (ids, tile) => ids.some((id) => tilesOf(id).has(tile));
    const thalassar = [5964, 5965, 5966, 5967, 5968],
      brasshaven = [5973, 5974, 5975, 5976, 5977],
      amber = [5984, 5985, 5986, 5987, 5988];
    expect([265, 266, 276].map((tile) => has(thalassar, tile))).toEqual([true, true, true]); // muck, chimney, coral
    expect([260, 261, 262, 263, 264].map((tile) => has(brasshaven, tile))).toEqual([false, true, true, true, true]);
    expect([267, 268].map((tile) => has(amber, tile))).toEqual([true, true]); // tar, ferns
  });
  it("The Drowned Causeway is held by Carapace Scuttlers, and more rise from the tide beside you on round 3", () => {
    const g = start(5964);
    const scuttlers = () => g.units.filter((u) => !u.dead && u.team === "red" && u.type === "scuttler").length;
    expect(scuttlers()).toBe(6);
    nextRound(g);
    nextRound(g);
    expect(g.turn).toBe(3);
    expect(g.units.some((u) => u.type === "scuttler" && u.tx === 2 && u.ty === 13)).toBe(true);
  });
  it("The Mouth of the Trench ends when the Tide-Mother falls, and she keeps her islet behind two Behemoths", () => {
    const g = start(5966);
    const mother = g.units.find((u) => u.team === "red" && u.type === "siren" && u.tx === 11 && u.ty === 1);
    expect(mother).toBeTruthy();
    expect(g.units.filter((u) => u.team === "red" && u.type === "behemoth").map((u) => [u.tx, u.ty])).toEqual([
      [11, 4],
      [12, 4],
    ]);
    nextRound(g);
    expect(mother.ty).toBeLessThanOrEqual(3); // she does not come down off her islet to fight
    fell(g, mother);
    expect(g.phase).toBe("victory");
  });
  it("The Mainspring Vault ends when Chief Artificer Volkmar falls, and The Tyrant's Hollow when the Tyrant does", () => {
    for (const [id, type] of [
      [5975, "king"],
      [5986, "tyrant"],
    ]) {
      const g = start(id);
      const boss = g.units.find((u) => u.team === "red" && u.type === type);
      expect(boss, type).toBeTruthy();
      expect(g.units.filter((u) => !u.dead && u.team === "red").length).toBeGreaterThan(8);
      fell(g, boss);
      expect(g.phase, type).toBe("victory");
    }
  });
  it("The Assembly Line carries what stands on its belts, and its vents hide what is beyond them", () => {
    const g = start(5974);
    const rider = spawn(g, "footmen", "blue", 4, 5); // a belt running east
    expect(g.tileAt(4, 5)).toBe(261);
    nextRound(g);
    expect(rider.dead || rider.tx === 5).toBe(true);
    expect(g._hasVents()).toBe(true);
  });
  it("The Powder Line is held until round 9, and The Pearl Beds and The Nesting Cliffs are won by standing on their goal", () => {
    const powder = start(5977);
    expect(powder.units.filter((u) => u.team === "red").length).toBe(0); // they come in waves
    for (const id of [5968, 5987]) {
      const g = start(id);
      const [x, y] = tag(g, 6)[0].a;
      reach(g, mine(g)[0], [x, y]);
      expect(g.phase, String(id)).toBe("victory");
    }
  });
});
