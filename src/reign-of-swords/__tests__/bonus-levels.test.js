// The BONUS campaigns (Tilicia & Isoluccia — ours, built by tools/ros/bonus/build_bonus.py into bonus.json): the
// records load beside Episode II's own maps and their scripted events fire through the original's scenario VM.
import { describe, it, expect } from "vitest";
import { loadEpisode, makeGame, startBattle, nextRound, put, step } from "./battle.js";
import { missionList } from "../engine/engine.js";

await loadEpisode(2);
const mine = (g) => g.units.filter((u) => !u.dead && u.team === "blue" && !u.ally);
const foes = (g) => g.units.filter((u) => !u.dead && u.team === "red");

describe("bonus campaigns: loading", () => {
  it("adds 18 bonus battles to Episode II and leaves its own 100-odd maps in place", () => {
    const maps = missionList();
    const bonus = maps.filter((m) => m.mapId >= 5900 && m.mapId < 6000);
    expect(bonus.filter((m) => m.group === "story").length).toBe(12);
    expect(bonus.filter((m) => m.group === "siege").length).toBe(6);
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
