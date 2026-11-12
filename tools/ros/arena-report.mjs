#!/usr/bin/env node
// Gather the unit arena's rows (reports/ros-arena/arena-*.json — `npm run e2e:arena`, whole or in shards) into one
// table, docs/unit-balance.md: each unit's mean margin in the duels and in every battle type, whether it beats the
// unit it is upgraded from one for one, and how an army of it fares in the last battle of each original kingdom.
//
//   npm run e2e:arena            (or four shards: ROS_ARENA_SHARD=0/4 … 3/4)
//   node tools/ros/arena-report.mjs [rows.json …]
import { readFileSync, writeFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { DEPLOY_COST, UNIT_TYPES } from "../../src/reign-of-swords/data/game-data.js";
import { BONUS_UPGRADES_ALL, BONUS_ORDER } from "../../src/reign-of-swords/data/bonus-units.js";

const root = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const dir = join(root, "reports", "ros-arena");
const files =
  process.argv.length > 2
    ? process.argv.slice(2)
    : readdirSync(dir)
        .filter((f) => /^arena-\d+\.json$/.test(f))
        .map((f) => join(dir, f));
const rows = files.flatMap((f) => JSON.parse(readFileSync(f, "utf8")));
const base = Object.fromEntries(BONUS_UPGRADES_ALL.map((u) => [u.to, u]));
const mean = (list) => (list.length ? list.reduce((a, b) => a + b, 0) / list.length : null);
const show = (n) => (n == null || Number.isNaN(n) ? "" : (n > 0 ? "+" : "") + n.toFixed(2));
const units = [...new Set(rows.map((r) => r.unit))];
const table = units.map((unit) => {
  const of = (scenario) => rows.filter((r) => r.unit === unit && r.scenario === scenario);
  const cells = ["open", "cavalry", "castle", "line"].map((s) => mean(of(s).map((r) => r.margin)));
  const upgrade = of("upgrade")[0],
    finals = of("finals")[0];
  return { unit, cells, all: mean(cells.filter((c) => c != null)), upgrade, finals };
});
table.sort((a, b) => (b.all ?? -9) - (a.all ?? -9));
const name = (unit) => (UNIT_TYPES[unit] ? UNIT_TYPES[unit].name : unit);
const lines = [
  "# Unit balance: the arena",
  "",
  "Written by `tools/ros/arena-report.mjs` from the rows of `npm run e2e:arena` (src/reign-of-swords/e2e/arena.e2e.js).",
  "Every number is a margin: the share of its points one side has left minus the share the other has left, from -1 to",
  "+1, so 0 is an even fight for the price. The original units run the same tests and are the yardstick.",
  "",
  "- **Duels**: equal-points squads against each of fourteen original units on an open field, from both sides.",
  "- **Cavalry / Castle / Spear line**: a 1500-point squad against a mounted army; holding a castle against a",
  "  storming party with Catapults; behind six Pikemen with six Archers behind it, advancing on a mixed army.",
  "- **One for one**: six of the unit against six of the unit it is upgraded from. An upgrade must come out ahead.",
  "- **Original finals**: the last battle of each original kingdom of Episode II, fought by the Autopilot with as many",
  "  of the unit as the battle's points and the elite rule allow, Swordsmen and Militiamen for the rest: the share of",
  "  the army kept on a victory, -1 on a defeat, and how many of those battles were won. A new unit far above every",
  "  original unit here would steamroll the original game.",
  "",
  "| Unit | New | Points | All | Duels | Cavalry | Castle | Spear line | Upgraded from | Token | One for one | Original finals | Won |",
  "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
  ...table.map((t) => {
    const u = base[t.unit];
    return `| ${name(t.unit)} | ${BONUS_ORDER.includes(t.unit) ? "yes" : ""} | ${DEPLOY_COST[t.unit] ?? ""} | ${show(t.all)} | ${t.cells.map(show).join(" | ")} | ${u ? name(u.from) : ""} | ${u ? u.need : ""} | ${t.upgrade ? show(t.upgrade.margin) : ""} | ${t.finals ? show(t.finals.margin) : ""} | ${t.finals ? t.finals.wins + "/" + t.finals.fights : ""} |`;
  }),
  "",
];
writeFileSync(join(root, "docs", "unit-balance.md"), lines.join("\n"));
console.log("wrote docs/unit-balance.md — " + table.length + " units from " + files.length + " file(s)");
