// The bonus campaigns in the campaign shell (ours): where the two kingdoms sit in the unlock graph, and the
// ⚙ Settings → Resume Episode II army file.
import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { readResume, resumeDelta, readTransfer } from "../data/save-transfer.js";
import {
  kingdomUnlocked,
  missionUnlocked,
  raidUnlocked,
  kingdomRaids,
  progressBefore,
} from "../data/campaign-rules.js";
import {
  combineCounts,
  KINGDOM_POS_EP2,
  unlocksOf,
  ALL_TYPES,
  EP2_ORDER,
  BONUS_ORDER,
  STARTER_ARMY_EP2,
  starterArmy,
  ARMY_GROUPS,
} from "../data/shell-data.js";
import { isBonusMap, BONUS_HIDDEN } from "../data/bonus-units.js";
import { DEPLOY_COST } from "../data/game-data.js";

const dir = join(process.cwd(), "public/games/reign-of-swords-2");
const json = (f) => JSON.parse(readFileSync(join(dir, f), "utf8"));
const campaign = json("campaign.json"),
  bonus = json("bonus.json"),
  rewards = { ...json("rewards.json"), ...bonus.rewards },
  levels = [...json("levels.json").levels, ...bonus.levels].filter((l) => !l.hidden);
const camp = { ...campaign, kingdoms: [...campaign.kingdoms, ...bonus.kingdoms] };
const original = { ...campaign };
const idx = (id) => camp.kingdoms.findIndex((k) => k.id === id);

describe("the army an Episode II save begins with", () => {
  it("is 50 Militiamen, six of each original unit under 300 points, two of each at 300 or more, two of every bonus unit", () => {
    const army = starterArmy(true);
    expect(army.militiamen).toBe(50);
    for (const unit of [...ALL_TYPES, ...EP2_ORDER]) {
      if (unit === "militiamen") continue;
      const cost = DEPLOY_COST[unit];
      expect(army[unit], unit).toBe(!cost ? undefined : cost < 300 ? 6 : 2); // (a conjured unit has no cost)
    }
    expect([army.footmen, army.archers, army.horsebowmen, army.dunesirens, army.bloodgorgers]).toEqual([6, 6, 6, 6, 6]);
    expect([army.knights, army.catapult, army.king, army.wizards, army.craftsmen]).toEqual([2, 2, 2, 2, 2]);
    expect([army.sapper, army.bodyguard]).toEqual([undefined, undefined]);
    expect(BONUS_ORDER.length).toBe(49);
    for (const unit of BONUS_ORDER) expect(army[unit], unit).toBe(2);
    for (const unit of [...BONUS_HIDDEN, "hounds", "imp", "panther"]) expect(army[unit], unit).toBeUndefined();
    expect(Object.keys(army).length).toBe(28 + 49);
  });
  it("every unit of it has a tile in the camp (the grid is drawn from the camp's groups)", () => {
    const shown = ARMY_GROUPS.flatMap((group) => group.units);
    for (const unit of Object.keys(starterArmy(true))) expect(shown, unit).toContain(unit);
    expect(new Set(shown).size).toBe(shown.length);
  });
  it("Episode I still begins with nothing", () => {
    expect(starterArmy(false)).toEqual({});
  });
});

describe("bonus kingdoms on the campaign map", () => {
  it("are thirteen extra regions with their story battles and raids, each with a place on the Episode II map", () => {
    expect(bonus.kingdoms.map((k) => k.id)).toEqual([
      "tilicia",
      "isoluccia",
      "mare-nostra",
      "satoshi",
      "mirror-sea",
      "tezcal",
      "jarnheim",
      "khemret",
      "moananui",
      "coatlan",
      "thalassar",
      "brasshaven",
      "amber-reach",
    ]);
    expect(bonus.kingdoms.map((k) => k.name).slice(2)).toEqual([
      "Mare Nostra",
      "The Isles of Satoshi",
      "The Mirror Sea",
      "The Jungles of Tezcal",
      "The Holds of Jarnheim",
      "The Sands of Khemret",
      "The Isles of Moananui",
      "The Highlands of Coatlan",
      "The Drowned Coast of Thalassar",
      "The Foundries of Brasshaven",
      "The Amber Reach",
    ]);
    for (const kingdom of bonus.kingdoms) {
      const small = !["tilicia", "isoluccia"].includes(kingdom.id); // 2 raids; the first two have 3
      expect(kingdom.bonus).toBe(true);
      expect(kingdom.missions.length).toBe(3); // three story battles in every bonus region
      expect(kingdomRaids(levels, kingdom).length).toBe(small ? 2 : 3);
      expect(KINGDOM_POS_EP2[kingdom.id]).toBeTruthy();
      for (const mission of kingdom.missions) {
        expect(isBonusMap(mission.mapId)).toBe(true);
        expect(mission.victory.length).toBeGreaterThan(0);
        expect(mission.defeat.length).toBeGreaterThan(0);
      }
    }
    expect(campaign.kingdoms.some((k) => k.bonus)).toBe(false); // the original campaign file is untouched
  });
  it("every bonus region is open from a new save, and every battle and raid in it, in any order", () => {
    const fresh = new Set();
    for (const kingdom of bonus.kingdoms) {
      const at = idx(kingdom.id);
      expect(kingdomUnlocked(camp, at, fresh), kingdom.id).toBe(true);
      kingdom.missions.forEach((_, missionIdx) =>
        expect(missionUnlocked(camp, at, missionIdx, fresh), kingdom.id).toBe(true),
      );
      kingdomRaids(levels, kingdom).forEach((_, raidIdx) =>
        expect(raidUnlocked(camp, at, raidIdx, fresh), kingdom.id).toBe(true),
      );
    }
    // the original kingdoms keep the original order: a root, then battle by battle and kingdom by kingdom
    expect(kingdomUnlocked(camp, 0, fresh)).toBe(true);
    expect(missionUnlocked(camp, 0, 1, fresh)).toBe(false);
    expect(kingdomUnlocked(camp, 1, fresh)).toBe(false);
    expect(raidUnlocked(camp, 0, 0, fresh)).toBe(false);
  });
  it("the battles that hand out a bonus unit also open its upgrade", () => {
    const gives = (mapId) => Object.keys(rewards[mapId].units || {});
    for (const [mapId, unit] of [
      [5902, "cragsmen"],
      [5904, "spellwardens"],
      [5906, "sentinel"],
      [5912, "golem"], // a raid: the Quarry of Giants
      [5924, "marines"], // Bellaro's Free Company comes over at the harbour chain
      [5924, "pavisiers"],
      [5926, "battlemage"],
      [5942, "gladiator"],
      [5962, "samurai"],
      [5943, "dragonrider"],
      [5994, "jaguar"],
      [5995, "eagle"],
      [5996, "serpent"],
      [5914, "berserker"],
      [5915, "shieldmaiden"],
      [5916, "einherjar"],
      [5934, "medjay"],
      [5935, "khopesh"],
      [5936, "anubis"],
      [5944, "toa"],
      [5945, "tahuanui"],
      [5946, "tohunga"],
      [5954, "coatecpatl"],
      [5955, "ahuizotl"],
      [5956, "chieftain"],
      [5964, "scuttler"], // the three factions: each story battle hands out the unit (or two) it opens
      [5965, "siren"],
      [5965, "brinehurler"],
      [5966, "behemoth"],
      [5973, "automaton"],
      [5974, "phalanx"],
      [5974, "arccaster"],
      [5975, "gyrocopter"],
      [5984, "raptor"],
      [5985, "ankylosaur"],
      [5985, "pterosaur"],
      [5986, "tyrant"],
    ]) {
      expect(gives(mapId)).toContain(unit);
      expect(unlocksOf(mapId, true)).toContain(unit);
    }
    expect(rewards[5906].units.sentinel).toBe(1);
    expect(rewards[5926].units.battlemage).toBe(1);
    for (const id in bonus.rewards) expect((bonus.rewards[id].spoils || {}).Medal).toBeUndefined(); // Medals come from Major Victories
  });
});

describe("Resume Episode II (⚙ Settings)", () => {
  const veteran = json("veteran-army.json");
  // an Episode II army as the game exports it
  const exported = {
    kind: "reign-of-swords-army",
    v: 1,
    episode: 2,
    army: { footmen: 10, pikemen: 11, cavalry: 11, king: 2, conjurer: 3, bloodgorgers: 4, wizards: 2 },
    spoils: { Medal: 4, Weapons: 1, Spirit: 1 },
  };
  it("reads an Episode II army file whole — no transfer limits", () => {
    const got = readResume(exported);
    expect(got.units).toEqual(exported.army);
    expect(got.spoils).toEqual(exported.spoils);
    expect(() => readTransfer(exported, { ep2: true })).toThrow(/import it in Episode I/); // the ordinary import refuses it
  });
  it("the built-in veteran army is 8 of every unit that can be owned, and 8 of every collectible", () => {
    const got = readResume(veteran);
    for (const k of [...ALL_TYPES, ...EP2_ORDER, ...BONUS_ORDER].filter((u) => u !== "sapper" && u !== "bodyguard"))
      expect(got.units[k], k).toBe(8);
    expect(got.units.sapper).toBeUndefined();
    expect(Object.keys(got.units).length).toBe(77);
    expect(got.spoils).toEqual({
      Medal: 8,
      Armor: 8,
      Weapons: 8,
      Beasts: 8,
      Spirit: 8,
      Lore: 8,
      Bloodstone: 8,
      Scarab: 8,
      Obsidian: 8,
      Whalebone: 8,
      Anchor: 8,
      Tsuba: 8,
      Jade: 8,
      Void: 8,
      Pearl: 8,
      Mainspring: 8,
      Amber: 8,
    });
  });
  it("…and resuming with it marks every battle of every campaign won, the bonus ones included", () => {
    const won = progressBefore(camp, levels, -1);
    for (const kingdom of camp.kingdoms) {
      for (const mission of kingdom.missions) expect(won.has(mission.mapId)).toBe(true);
      for (const raid of kingdomRaids(levels, kingdom)) expect(won.has(raid.mapId)).toBe(true);
    }
    expect(won.has(5963) && won.has(5972) && won.has(5943)).toBe(true);
    const earned = combineCounts(...[...won].map((id) => (rewards[id] && rewards[id].units) || {}));
    const army = combineCounts(earned, resumeDelta(readResume(veteran).units, earned));
    expect(army.samurai).toBe(8);
    expect(army.militiamen).toBe(8);
  });
  it("refuses anything else, and caps a count at 500", () => {
    expect(() => readResume({ kind: "x" })).toThrow(/not a Reign of Swords army file/);
    expect(() => readResume({ ...veteran, episode: 1 })).toThrow(/Episode II army file/);
    const got = readResume({ ...veteran, army: { footmen: 9999, sapper: 3, dragon: 2, archers: -4 }, spoils: null });
    expect(got).toEqual({ units: { footmen: 500 }, spoils: {} });
  });
  it("with every Episode II battle marked won, the army comes out exactly as the file's", () => {
    const won = progressBefore(original, levels, -1);
    expect([...won].some(isBonusMap)).toBe(false);
    expect(won.has(5432) && won.has(5401) && won.has(5631)).toBe(true);
    // (the starting army and the battles' unit rewards: what the save holds before the camp's own changes)
    const earned = combineCounts(STARTER_ARMY_EP2, ...[...won].map((id) => (rewards[id] && rewards[id].units) || {}));
    const got = readResume(exported);
    const army = combineCounts(earned, resumeDelta(got.units, earned));
    for (const k of new Set([...Object.keys(army), ...Object.keys(got.units)]))
      expect(army[k] || 0).toBe(got.units[k] || 0);
    expect(army.militiamen || 0).toBe(0); // the file has none, whatever the battles handed out
  });
});
