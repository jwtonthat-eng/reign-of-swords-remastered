// BONUS-UNIT STRESS (ours — a soak tool beside the arena): random play (the fuzzer of __tests__/fuzz.js — random
// taps, moves, attacks, undos, holds and marches, input pressed while actions animate, every frame checked for two
// units on a tile, sprites off their tile, stuck teleports and exceptions) with the player's whole army swapped for
// the nine bonus units, on every bonus battle and a few of Episode II's own (open field, river, fortress).
//
//   npm run e2e:stress            ROS_STRESS_SEEDS=4 for more dice   ROS_STRESS_SHARD=0/4 for one slice
import { it, expect } from "vitest";
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { loadEpisode, spawn } from "../__tests__/battle.js";
import { fuzz } from "../__tests__/fuzz.js";
import { missionList } from "../engine/engine.js";
import { BONUS_ORDER, isBonusMap } from "../data/bonus-units.js";

const ON = process.env.ROS_STRESS === "1";
const EXTRA = [5204, 5229, 5401, 5427];

it.skipIf(!ON)(
  "bonus units under random play",
  async () => {
    await loadEpisode(2);
    const seeds = Number(process.env.ROS_STRESS_SEEDS || 2);
    const [shard, of] = (process.env.ROS_STRESS_SHARD || "0/1").split("/").map(Number);
    const maps = missionList()
      .map((m) => m.mapId)
      .filter((id) => isBonusMap(id) || EXTRA.includes(id))
      .filter((_, i) => i % of === shard);
    const report = [];
    for (const mapId of maps)
      for (let seed = 1; seed <= seeds; seed++) {
        let swapped = false;
        const onStep = (g) => {
          if (swapped) return;
          swapped = true;
          const mine = g.units.filter((u) => !u.dead && u.team === "blue" && !u.ally);
          mine.forEach((u, i) => {
            const type = BONUS_ORDER[(i + seed) % BONUS_ORDER.length];
            g.units.splice(g.units.indexOf(u), 1);
            const fresh = spawn(g, type, "blue", u.tx, u.ty);
            if (g.moveCost(fresh, u.tx, u.ty) >= 99) {
              g.units.splice(g.units.indexOf(fresh), 1); // a wall-walk the newcomer cannot stand on: keep the original
              g.units.push(u);
            }
          });
        };
        let result;
        try {
          result = fuzz(mapId, 8, mapId * 10 + seed, { draw: 13, onStep });
        } catch (error) {
          result = {
            issues: ["EXCEPTION " + (error && error.stack ? error.stack.split("\n").slice(0, 4).join(" | ") : error)],
          };
        }
        if (result.issues.length) report.push({ mapId, seed, issues: result.issues.slice(0, 5) });
      }
    const dir = join("reports", "ros-arena");
    mkdirSync(dir, { recursive: true });
    writeFileSync(process.env.ROS_STRESS_OUT || join(dir, `stress-${shard}.json`), JSON.stringify(report, null, 1));
    expect(report).toEqual([]);
  },
  3600000,
);
