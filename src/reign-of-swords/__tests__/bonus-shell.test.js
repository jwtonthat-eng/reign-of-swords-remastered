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
import { combineCounts, KINGDOM_POS_EP2, unlocksOf, ALL_TYPES, EP2_ORDER, BONUS_ORDER } from "../data/shell-data.js";
import { isBonusMap } from "../data/bonus-units.js";

const dir = join(process.cwd(), "public/games/reign-of-swords-2");
const json = (f) => JSON.parse(readFileSync(join(dir, f), "utf8"));
const campaign = json("campaign.json"),
  bonus = json("bonus.json"),
  rewards = { ...json("rewards.json"), ...bonus.rewards },
  levels = [...json("levels.json").levels, ...bonus.levels].filter((l) => !l.hidden);
const camp = { ...campaign, kingdoms: [...campaign.kingdoms, ...bonus.kingdoms] };
const original = { ...campaign };
const idx = (id) => camp.kingdoms.findIndex((k) => k.id === id);
const storyOf = (id) => camp.kingdoms[idx(id)].missions.map((m) => m.mapId);

describe("bonus kingdoms on the campaign map", () => {
  it("are six extra regions with their story battles and raids, each with a place on the Episode II map", () => {
    expect(bonus.kingdoms.map((k) => k.id)).toEqual([
      "tilicia",
      "isoluccia",
      "mare-nostra",
      "satoshi",
      "mirror-sea",
      "tezcal",
    ]);
    expect(bonus.kingdoms.map((k) => k.name).slice(2)).toEqual([
      "Mare Nostra",
      "The Isles of Satoshi",
      "The Mirror Sea",
      "The Jungles of Tezcal",
    ]);
    for (const kingdom of bonus.kingdoms) {
      const small = ["mare-nostra", "satoshi", "mirror-sea", "tezcal"].includes(kingdom.id); // 2 raids; the first two have 3
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
  it("Tilicia opens when Abbisin is complete, Isoluccia when Tilicia is", () => {
    const beforeLast = new Set([...progressBefore(original, levels, -1)].filter((id) => id !== 5432));
    expect(kingdomUnlocked(camp, idx("tilicia"), beforeLast)).toBe(false);
    const done = progressBefore(original, levels, -1);
    expect(kingdomUnlocked(camp, idx("tilicia"), done)).toBe(true);
    expect(kingdomUnlocked(camp, idx("isoluccia"), done)).toBe(false);
    expect(missionUnlocked(camp, idx("tilicia"), 0, done)).toBe(true);
    expect(missionUnlocked(camp, idx("tilicia"), 1, done)).toBe(false);
    const tiliciaDone = new Set([...done, ...storyOf("tilicia")]);
    expect(kingdomUnlocked(camp, idx("isoluccia"), tiliciaDone)).toBe(true);
    // …then Mare Nostra after Isoluccia, and both Satoshi and the Mirror Sea after Mare Nostra
    expect(kingdomUnlocked(camp, idx("mare-nostra"), tiliciaDone)).toBe(false);
    const isolucciaDone = new Set([...tiliciaDone, ...storyOf("isoluccia")]);
    expect(kingdomUnlocked(camp, idx("mare-nostra"), isolucciaDone)).toBe(true);
    expect(kingdomUnlocked(camp, idx("satoshi"), isolucciaDone)).toBe(false);
    expect(kingdomUnlocked(camp, idx("mirror-sea"), isolucciaDone)).toBe(false);
    const seaDone = new Set([...isolucciaDone, ...storyOf("mare-nostra")]);
    expect(kingdomUnlocked(camp, idx("satoshi"), seaDone)).toBe(true);
    expect(kingdomUnlocked(camp, idx("mirror-sea"), seaDone)).toBe(true);
    // …and Tezcal after the Mirror Sea
    expect(kingdomUnlocked(camp, idx("tezcal"), seaDone)).toBe(false);
    const mirrorDone = new Set([...seaDone, ...storyOf("mirror-sea")]);
    expect(kingdomUnlocked(camp, idx("tezcal"), mirrorDone)).toBe(true);
  });
  it("their raids open as the story advances, like the Eastern Kingdoms' (raid n after story battle n + 1)", () => {
    const done = progressBefore(original, levels, -1);
    const story = storyOf("tilicia");
    expect(raidUnlocked(camp, idx("tilicia"), 0, new Set([...done, story[0]]))).toBe(false);
    expect(raidUnlocked(camp, idx("tilicia"), 0, new Set([...done, story[0], story[1]]))).toBe(true);
    // Tilicia has three battles and three raids: its last raid opens with its last battle, as the second does
    expect(story.length).toBe(3);
    expect(raidUnlocked(camp, idx("tilicia"), 1, new Set([...done, story[0], story[1]]))).toBe(false);
    expect(raidUnlocked(camp, idx("tilicia"), 2, new Set([...done, story[0], story[1]]))).toBe(false);
    expect(raidUnlocked(camp, idx("tilicia"), 1, new Set([...done, ...story]))).toBe(true);
    expect(raidUnlocked(camp, idx("tilicia"), 2, new Set([...done, ...story]))).toBe(true);
    expect(raidUnlocked(camp, idx("isoluccia"), 2, new Set([...done, ...story, ...storyOf("isoluccia")]))).toBe(true);
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
    expect(Object.keys(got.units).length).toBe(48);
    expect(got.spoils).toEqual({ Medal: 8, Armor: 8, Weapons: 8, Beasts: 8, Spirit: 8, Lore: 8 });
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
    const earned = combineCounts(...[...won].map((id) => (rewards[id] && rewards[id].units) || {}));
    const got = readResume(exported);
    const army = combineCounts(earned, resumeDelta(got.units, earned));
    for (const k of new Set([...Object.keys(army), ...Object.keys(got.units)]))
      expect(army[k] || 0).toBe(got.units[k] || 0);
    expect(army.militiamen || 0).toBe(0); // the file has none, whatever the battles handed out
  });
});
