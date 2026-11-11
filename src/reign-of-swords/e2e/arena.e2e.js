// UNIT ARENA (ours — a balance tool, not part of either game): how much fight a unit gives for its deployment points.
// Every unit under test meets a basket of original units in squads of (nearly) equal points on an open field —
// Episode II's Open Field battlefield, emptied — with the Autopilot ("attack") on one side and the computer on the
// other, each pairing fought from both sides and over several dice seeds. A battle scores the MARGIN: the share of
// its points the tested squad has left (unit cost × HP) minus the share the other squad has left, −1 … +1. A unit's
// INDEX is its mean margin over the basket: about 0 means it fights at its price, the original units themselves being
// the yardstick (they are run through the same basket).
//
//   npm run e2e:arena                      every bonus unit and every basket unit
//   ROS_ARENA_UNITS=samurai,knights …      only these
//   ROS_ARENA_SHARD=0/4                    one of four slices of the unit list (run the four side by side)
//   ROS_ARENA_OUT=file.json                where the rows go (default reports/ros-arena/arena-<shard>.json)
import { it } from "vitest";
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { loadEpisode, makeGame, startBattle, only, spawn, step } from "../__tests__/battle.js";
import { DEPLOY_COST } from "../data/game-data.js";
import { BONUS_ORDER } from "../data/bonus-units.js";
import { seedBattle } from "../engine/sim.js";

const ON = process.env.ROS_ARENA === "1";
export const BASKET = [
  "footmen",
  "swordsmen",
  "halberdiers",
  "pikemen",
  "greatswordsmen",
  "archers",
  "crossbowmen",
  "musketeers",
  "cavalry",
  "knights",
  "griffon",
  "wizards",
  "king",
  "catapult",
];
const MAP = 5204, // Open Field, 24 × 24
  POINTS = 2400,
  MAX_SQUAD = 12,
  SEEDS = [11, 23],
  TURNS = 16;

// Squad sizes for a pairing: as close to equal points as whole units allow, near POINTS, at most MAX_SQUAD each.
export function squads(a, b) {
  let best = null;
  for (let na = 1; na <= MAX_SQUAD; na++)
    for (let nb = 1; nb <= MAX_SQUAD; nb++) {
      const pa = na * DEPLOY_COST[a],
        pb = nb * DEPLOY_COST[b];
      if (pa > POINTS * 1.05 || pb > POINTS * 1.05) continue;
      const score = Math.abs(pa - pb) / Math.max(pa, pb) + (0.15 * (POINTS - Math.min(pa, pb))) / POINTS;
      if (!best || score < best.score) best = { na, nb, pa, pb, score };
    }
  return best;
}

// Two blocks facing each other across the middle of the field, three ranks deep.
function line(count, x0, dir, rows) {
  const out = [],
    mid = Math.floor(rows / 2);
  for (let i = 0; i < count; i++) {
    const rank = Math.floor(i / 6),
      file = i % 6;
    out.push([x0 + dir * rank, mid - 3 + file]);
  }
  return out;
}

function fight(blue, red, nBlue, nRed, seed) {
  const g = startBattle(makeGame(MAP));
  only(g);
  seedBattle(g, seed);
  const enemy = g.mission.groupOrder.find((x) => x.side === "enemy").gi;
  const mine = line(nBlue, 6, -1, g.rows).map(([x, y]) => spawn(g, blue, "blue", x, y));
  const foes = line(nRed, 17, 1, g.rows).map(([x, y]) => spawn(g, red, "red", x, y, { group: enemy }));
  g._sc = null; // the battlefield's own ending lines play no part
  g.setAutopilot("attack");
  const alive = (list) => list.filter((u) => !u.dead);
  for (let frame = 0; frame < 120000; frame++) {
    if (g.phase === "victory" || g.phase === "defeat" || g.turn > TURNS) break;
    if (!alive(mine).length || !alive(foes).length) break;
    if (g.battleEvent) g.eventClosed();
    if (g.pendingSkip) g.confirmSkip();
    step(g);
  }
  const left = (list, type, n) => alive(list).reduce((s, u) => s + u.hp / 100, 0) / n;
  const out = { blueLeft: left(mine, blue, nBlue), redLeft: left(foes, red, nRed), turn: g.turn };
  if (g.destroy) g.destroy();
  return out;
}

it.skipIf(!ON)("unit arena", async () => {
  await loadEpisode(2);
  let units = process.env.ROS_ARENA_UNITS ? process.env.ROS_ARENA_UNITS.split(",") : [...BONUS_ORDER, ...BASKET];
  const [shard, of] = (process.env.ROS_ARENA_SHARD || "0/1").split("/").map(Number);
  units = units.filter((_, i) => i % of === shard);
  const rows = [];
  for (const unit of units)
    for (const foe of BASKET) {
      if (foe === unit) continue;
      const s = squads(unit, foe);
      let margin = 0,
        fights = 0,
        wins = 0;
      for (const seed of SEEDS) {
        const asBlue = fight(unit, foe, s.na, s.nb, seed),
          asRed = fight(foe, unit, s.nb, s.na, seed + 1000);
        for (const m of [asBlue.blueLeft - asBlue.redLeft, asRed.redLeft - asRed.blueLeft]) {
          margin += m;
          fights++;
          if (m > 0.05) wins++;
        }
      }
      rows.push({
        unit,
        foe,
        n: s.na,
        nFoe: s.nb,
        points: s.pa,
        foePoints: s.pb,
        margin: margin / fights,
        wins,
        fights,
      });
    }
  const out = process.env.ROS_ARENA_OUT || join("reports", "ros-arena", `arena-${shard}.json`);
  mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, JSON.stringify(rows));
});
