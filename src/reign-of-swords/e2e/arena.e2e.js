// UNIT ARENA (ours — a balance tool, not part of either game): how much fight a unit gives for its deployment points.
// Every unit under test meets a basket of original units in squads of (nearly) equal points on an open field —
// Episode II's Open Field battlefield, emptied — with the Autopilot ("attack") on one side and the computer on the
// other, each pairing fought from both sides and over several dice seeds. A battle scores the MARGIN: the share of
// its points the tested squad has left (unit cost × HP) minus the share the other squad has left, −1 … +1. A unit's
// INDEX is its mean margin over the basket: about 0 means it fights at its price, the original units themselves being
// the yardstick (they are run through the same basket).
//
// Beyond the duels it fights three BATTLE TYPES with a squad of about 1500 points of the unit: on the open field
// against a mounted army (cavalry), holding a castle against a storming party with Catapults (castle), and standing
// behind a rank of Pikemen with Archers behind it while the block advances on a mixed army (line). And the UPGRADE
// rule: six of a unit against six of the unit it is upgraded from, one for one — an upgrade must win (upgrade).
// And the ORIGINAL FINALS: the last battle of every original kingdom fought with an army of the unit, to see whether a
// new unit steamrolls the original game; the original units run the same battles as the yardstick (finals).
//
//   npm run e2e:arena                      every bonus unit and every basket unit
//   ROS_ARENA_TYPES=castle,line …          only these battle types (open, cavalry, castle, line)
//   ROS_ARENA_UNITS=samurai,knights …      only these
//   ROS_ARENA_SHARD=0/4                    one of four slices of the unit list (run the four side by side)
//   ROS_ARENA_OUT=file.json                where the rows go (default reports/ros-arena/arena-<shard>.json)
import { it } from "vitest";
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { loadEpisode, makeGame, startBattle, only, spawn, step } from "../__tests__/battle.js";
import { DEPLOY_COST } from "../data/game-data.js";
import { BONUS_ORDER, BONUS_UPGRADES } from "../data/bonus-units.js";
import { seedBattle, simulateBattle } from "../engine/sim.js";
import { missionList } from "../engine/engine.js";
import { moveType } from "../rules/terrain.js";

const ON = process.env.ROS_ARENA === "1";
// which battle types to run: open (the duels), cavalry, castle, line — all of them by default
const WANTED = (process.env.ROS_ARENA_TYPES || "open,cavalry,castle,line,upgrade,finals").split(",");
const OPEN = WANTED.includes("open"),
  TYPES = ["cavalry", "castle", "line", "upgrade"].filter((t) => WANTED.includes(t)),
  FINALS = WANTED.includes("finals");
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
  TURNS = 16,
  SQUAD_POINTS = 1500; // the tested squad in the cavalry, castle and spear-line battles

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

// Ranks of six from x0, stepping `dir` a rank, centred on the field's middle row.
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
// An army of about `points`, split by a mix of [type, share] (whole units, at least one of each).
function army(points, mix) {
  const out = [];
  for (const [type, share] of mix) {
    const n = Math.max(1, Math.round((points * share) / DEPLOY_COST[type]));
    for (let i = 0; i < n; i++) out.push(type);
  }
  return out;
}
const worth = (types) => types.reduce((sum, type) => sum + DEPLOY_COST[type], 0);
// how many of a unit make the squad a battle type is built round
const squadOf = (unit) => Math.max(1, Math.min(MAX_SQUAD, Math.round(SQUAD_POINTS / DEPLOY_COST[unit])));

// One battle: `blue` and `red` are lists of [type, x, y] (a unit that cannot stand on its tile is put on the nearest
// tile it can), the Autopilot plays blue with `strategy` and the computer plays red. Returns the share of its points
// each side has left (unit cost × HP; summoned units count for nothing).
function battle({ map = MAP, blue, red, strategy = "attack", fort = null, seed }) {
  const g = startBattle(makeGame(map));
  only(g);
  seedBattle(g, seed);
  const enemy = g.mission.groupOrder.find((x) => x.side === "enemy").gi;
  const place = (type, team, x, y, extra) => {
    const u = spawn(g, type, team, x, y, extra);
    if (g.moveCost(u, x, y) < 99) return u;
    for (let r = 1; r < 8; r++)
      for (let dy = -r; dy <= r; dy++)
        for (let dx = -r; dx <= r; dx++) {
          const tx = x + dx,
            ty = y + dy;
          if (!g.inBounds(tx, ty) || g.unitAt(tx, ty) || g.moveCost(u, tx, ty) >= 99) continue;
          if (fort && fort.has(tx + "," + ty) !== (team === "blue")) continue; // defenders inside, the rest outside
          return Object.assign(u, { tx, ty, px: tx * g.tile, py: ty * g.tile });
        }
    return u;
  };
  const mine = blue.map(([type, x, y]) => place(type, "blue", x, y));
  const foes = red.map(([type, x, y]) => place(type, "red", x, y, { group: enemy }));
  if (fort) g.deployZone = fort; // "Hold the fort": the ground the Autopilot fights from
  g._sc = null; // the battlefield's own ending lines play no part
  g.setAutopilot(strategy);
  const alive = (list) => list.filter((u) => !u.dead);
  for (let frame = 0; frame < 120000; frame++) {
    if (g.phase === "victory" || g.phase === "defeat" || g.turn > TURNS) break;
    if (!alive(mine).length || !alive(foes).length) break;
    if (g.battleEvent) g.eventClosed();
    if (g.pendingSkip) g.confirmSkip();
    step(g);
  }
  const left = (list) =>
    list.reduce((sum, u) => sum + (u.dead ? 0 : (u.hp / 100) * DEPLOY_COST[u.type]), 0) /
    Math.max(
      1,
      list.reduce((sum, u) => sum + DEPLOY_COST[u.type], 0),
    );
  const out = { blueLeft: left(mine), redLeft: left(foes), turn: g.turn };
  if (g.destroy) g.destroy();
  return out;
}
const at = (types, tiles) => types.map((type, i) => [type, ...tiles[i]]);

// OPEN FIELD, one unit against one unit of the basket (the original arena).
function fight(blue, red, nBlue, nRed, seed) {
  return battle({
    blue: at(Array(nBlue).fill(blue), line(nBlue, 6, -1, 24)),
    red: at(Array(nRed).fill(red), line(nRed, 17, 1, 24)),
    seed,
  });
}

// THE BATTLE TYPES (beyond the open-field duels). Each returns the tested side's margin, −1 … +1.
// CAVALRY — the squad on the open field against a mounted army of the same points (Knights, Cavalry, Horse Bowmen),
// fought from both sides.
const HORSE = [
  ["knights", 0.4],
  ["cavalry", 0.4],
  ["horsebowmen", 0.2],
];
function cavalryFight(unit, seed, asBlue) {
  const squad = Array(squadOf(unit)).fill(unit),
    horse = army(worth(squad), HORSE);
  const [blue, red] = asBlue ? [squad, horse] : [horse, squad];
  const r = battle({ blue: at(blue, line(blue.length, 6, -1, 24)), red: at(red, line(red.length, 17, 1, 24)), seed });
  return asBlue ? r.blueLeft - r.redLeft : r.redLeft - r.blueLeft;
}
// CASTLE — the squad holds the west castle of Obbsin (Episode II battlefield 5238: walls, towers and two gates on its
// south side) under the Autopilot's "Hold the fort", against a storming party of the same points with Catapults.
const STORM = [
  ["swordsmen", 0.35],
  ["halberdiers", 0.2],
  ["archers", 0.25],
  ["catapult", 0.2],
];
const CASTLE = 5238;
function castleFight(unit, seed) {
  const probe = makeGame(CASTLE);
  const fort = new Set();
  for (let y = 0; y <= 11; y++)
    for (let x = 0; x <= 12; x++)
      if ([10, 12, 14, 16, 18].includes(moveType(probe.tileAt(x, y)))) fort.add(x + "," + y);
  if (probe.destroy) probe.destroy();
  const squad = Array(squadOf(unit)).fill(unit),
    storm = army(worth(squad), STORM);
  const yard = [],
    outside = [];
  for (const y of [10, 9, 8, 7]) for (let x = 1; x <= 7; x++) yard.push([x, y]); // the courtyard behind the gates
  for (const y of [14, 15, 16]) for (let x = 1; x <= 12; x++) outside.push([x, y]); // the ground before them
  const r = battle({ map: CASTLE, blue: at(squad, yard), red: at(storm, outside), strategy: "fortress", fort, seed });
  return r.blueLeft - r.redLeft;
}
// SPEAR LINE — the squad stands behind a rank of six Pikemen with six Archers behind it, and the whole block advances
// as one (the Autopilot's "Advance as one") on a mixed army of the same total points.
const MIXED = [
  ["swordsmen", 0.4],
  ["cavalry", 0.3],
  ["archers", 0.3],
];
// UPGRADE — the rule that an upgrade is worth making: six of the unit against six of the unit it is upgraded from,
// one for one whatever they cost, from both sides. null for a unit that is nobody's upgrade.
const BASE_OF = Object.fromEntries(BONUS_UPGRADES.map((u) => [u.to, u.from]));
function upgradeFight(unit, seed, asBlue) {
  const base = BASE_OF[unit];
  if (!base) return null;
  const [blue, red] = asBlue ? [unit, base] : [base, unit];
  const r = fight(blue, red, 6, 6, seed);
  return asBlue ? r.blueLeft - r.redLeft : r.redLeft - r.blueLeft;
}
// FINALS — does a unit steamroll the original game? The last story battle of every original kingdom of Episode II
// (those that let you muster an army), played by the Autopilot with as many of the unit as the battle's points and
// the elite rule allow and Swordsmen, then Militiamen, for whatever is left. A battle scores the share of the army's
// points it kept on a victory, −1 on a defeat, 0 if it ran out of turns. The original units run the same battles: they
// are the yardstick (a unit far above every original one is power creep).
function finalBattles() {
  const last = {};
  for (const m of missionList()) if (m.mapId < 5900 && m.group === "story") last[m.kingdom] = m.mapId;
  return Object.values(last);
}
async function finalsFight(unit, mapId, seed) {
  const r = await simulateBattle({
    mapId,
    army: { [unit]: 99, swordsmen: 99, militiamen: 99 },
    strategy: "attack",
    seed,
    yieldMs: 0,
  });
  if (!r.spent) return null; // a battle fought with a given force: nothing of ours is in it
  return r.result === "victory" ? r.kept / 100 : r.result === "defeat" ? -1 : 0;
}
function lineFight(unit, seed) {
  const squad = Array(squadOf(unit)).fill(unit),
    ranks = Math.ceil(squad.length / 6);
  const blue = [
    ...at(Array(6).fill("pikemen"), line(6, 9, -1, 24)),
    ...at(squad, line(squad.length, 8, -1, 24)),
    ...at(Array(6).fill("archers"), line(6, 8 - ranks, -1, 24)),
  ];
  const foes = army(worth(blue.map((b) => b[0])), MIXED);
  const r = battle({ blue, red: at(foes, line(foes.length, 18, 1, 24)), strategy: "advance", seed });
  return r.blueLeft - r.redLeft;
}

it.skipIf(!ON)("unit arena", async () => {
  await loadEpisode(2);
  let units = process.env.ROS_ARENA_UNITS ? process.env.ROS_ARENA_UNITS.split(",") : [...BONUS_ORDER, ...BASKET];
  const [shard, of] = (process.env.ROS_ARENA_SHARD || "0/1").split("/").map(Number);
  units = units.filter((_, i) => i % of === shard);
  const rows = [];
  for (const unit of OPEN ? units : [])
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
        scenario: "open",
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
  for (const unit of units) {
    const run = {
      cavalry: (seed) => [cavalryFight(unit, seed, true), cavalryFight(unit, seed + 1000, false)],
      castle: (seed) => [castleFight(unit, seed), castleFight(unit, seed + 500)],
      line: (seed) => [lineFight(unit, seed), lineFight(unit, seed + 500)],
      upgrade: (seed) => [upgradeFight(unit, seed, true), upgradeFight(unit, seed + 1000, false)],
    };
    for (const scenario of TYPES) {
      const margins = SEEDS.flatMap((seed) => run[scenario](seed)).filter((m) => m != null);
      if (!margins.length) continue;
      rows.push({
        scenario,
        unit,
        foe: scenario === "upgrade" ? BASE_OF[unit] : scenario,
        margin: margins.reduce((a, b) => a + b, 0) / margins.length,
        wins: margins.filter((m) => m > 0.05).length,
        fights: margins.length,
      });
    }
  }
  if (FINALS) {
    const maps = finalBattles();
    for (const unit of units) {
      const scores = [];
      for (const mapId of maps) {
        const score = await finalsFight(unit, mapId, SEEDS[0]);
        if (score != null) scores.push(score);
      }
      if (scores.length)
        rows.push({
          scenario: "finals",
          unit,
          foe: "finals",
          margin: scores.reduce((a, b) => a + b, 0) / scores.length,
          wins: scores.filter((x) => x > 0).length,
          fights: scores.length,
        });
    }
  }
  const out = process.env.ROS_ARENA_OUT || join("reports", "ros-arena", `arena-${shard}.json`);
  mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, JSON.stringify(rows));
  // …and the same as a table: a unit's mean margin in the duels and in each battle type, best first
  const show = (n) => (n == null ? "" : (n > 0 ? "+" : "") + n.toFixed(2));
  const table = units.map((unit) => {
    const of = (scenario) => rows.filter((r) => r.unit === unit && r.scenario === scenario).map((r) => r.margin);
    const mean = (list) => (list.length ? list.reduce((a, b) => a + b, 0) / list.length : null);
    const cells = ["open", "cavalry", "castle", "line"].map((scenario) => mean(of(scenario)));
    const finals = rows.find((r) => r.unit === unit && r.scenario === "finals");
    return {
      unit,
      cells,
      all: mean(cells.filter((c) => c != null)),
      base: BASE_OF[unit],
      beats: mean(of("upgrade")),
      finals: finals ? `${show(finals.margin)} (${finals.wins}/${finals.fights})` : "",
    };
  });
  writeFileSync(
    out.replace(/\.json$/, "") + ".md",
    [
      "| Unit | Points | All | Duels | Cavalry | Castle | Spear line | Upgraded from | One for one | Original finals (won) |",
      "|---|---|---|---|---|---|---|---|---|---|",
      ...table
        .sort((a, b) => b.all - a.all)
        .map(
          (t) =>
            `| ${t.unit} | ${DEPLOY_COST[t.unit]} | ${show(t.all)} | ${t.cells.map(show).join(" | ")} | ${t.base || ""} | ${show(t.beats)} | ${t.finals} |`,
        ),
    ].join("\n") + "\n",
  );
});
