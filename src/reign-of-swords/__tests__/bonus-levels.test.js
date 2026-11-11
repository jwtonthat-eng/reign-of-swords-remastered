// The BONUS campaigns (Tilicia & Isoluccia — ours, built by tools/ros/bonus/build_bonus.py into bonus.json): the
// records load beside Episode II's own maps and their scripted events fire through the original's scenario VM.
import { describe, it, expect } from "vitest";
import { loadEpisode, makeGame, startBattle, nextRound, put, step } from "./battle.js";
import { missionList } from "../engine/engine.js";

await loadEpisode(2);
const mine = (g) => g.units.filter((u) => !u.dead && u.team === "blue" && !u.ally);
const foes = (g) => g.units.filter((u) => !u.dead && u.team === "red");

describe("bonus campaigns: loading", () => {
  it("adds 33 bonus battles to Episode II and leaves its own 100-odd maps in place", () => {
    const maps = missionList();
    const bonus = maps.filter((m) => m.mapId >= 5900 && m.mapId < 6000);
    expect(bonus.filter((m) => m.group === "story").length).toBe(21); // 6 + 6 + 3 + 3 + 3
    expect(bonus.filter((m) => m.group === "siege").length).toBe(12); // 3 + 3 + 2 + 2 + 2
    expect(maps.some((m) => m.mapId === 5432)).toBe(true);
  });
});

describe("Tilicia 1, The Tolm Road (escape)", () => {
  it("opens with Cragsmen on the cliffs, and riders shut the pass behind you on round 4", () => {
    const g = startBattle(makeGame(5901));
    expect(foes(g).some((u) => u.type === "cragsmen" && g.terrainAt(u.tx, u.ty).passable === false)).toBe(true);
    const before = foes(g).filter((u) => u.type === "raiders").length;
    for (let i = 0; i < 3 && g.phase === "player"; i++) nextRound(g);
    expect(g.turn).toBe(4);
    expect(foes(g).filter((u) => u.type === "raiders").length).toBeGreaterThan(before - 2); // + the two riders
    expect(g.units.some((u) => u.wave && u.type === "raiders")).toBe(true);
  });
  it("is won when the fourth unit leaves by the head of the pass", () => {
    const g = startBattle(makeGame(5901));
    const goals = g.mission.script.goals;
    mine(g)
      .slice(0, 4)
      .forEach((u, i) => {
        put(g, u, goals[i][0], goals[i][1]);
        g.scenario.onTileReached(u);
        step(g, 5);
      });
    expect(g.phase).toBe("victory");
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
const rounds = (g, turn) => {
  for (let i = 0; i < 60 && g.turn < turn && g.phase === "player"; i++) nextRound(g);
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
  it("The Sealed Vale is won by holding out to round 11, not by clearing the field early", () => {
    const g = startBattle(makeGame(5903), "auto");
    expect(g.captureMode).toBe(1);
    expect(g.captureAreas.length).toBe(3);
    for (const u of foes(g)) u.dead = true;
    step(g, 30);
    expect(g.phase).toBe("player"); // the win switch is off: more are coming
    holdUntil(g, 11);
    expect(g.phase).toBe("victory");
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
  it("Landfall: the second and third waves land under your command", () => {
    const g = startBattle(makeGame(5921));
    const start = mine(g).length;
    rounds(g, 3);
    expect(mine(g).length).toBeGreaterThan(start);
    expect(mine(g).every((u) => !u.ally)).toBe(true);
  });
  it("Free Company is won when Captain Bellaro reaches the quay, and lost if he falls", () => {
    let g = startBattle(makeGame(5923));
    const escort = g.mission.script.escort;
    expect(escort.units.length).toBe(1);
    expect(g.units.some((u) => u.ally && u.type === "marines")).toBe(true);
    reach(
      g,
      g.units.find((u) => u.sid === escort.units[0]),
      escort.markers[0],
    );
    expect(g.phase).toBe("victory");
    g = startBattle(makeGame(5923));
    fell(
      g,
      g.units.find((u) => u.sid === g.mission.script.escort.units[0]),
    );
    expect(g.phase).toBe("defeat");
  });
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
