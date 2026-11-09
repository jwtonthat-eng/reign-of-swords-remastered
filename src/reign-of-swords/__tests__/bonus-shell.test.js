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
import { combineCounts, KINGDOM_POS_EP2, unlocksOf } from "../data/shell-data.js";
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
  it("are two extra kingdoms, six story battles and three raids each, with a place on the Episode II map", () => {
    expect(bonus.kingdoms.map((k) => k.id)).toEqual(["tilicia", "isoluccia"]);
    for (const kingdom of bonus.kingdoms) {
      expect(kingdom.bonus).toBe(true);
      expect(kingdom.missions.length).toBe(6);
      expect(kingdomRaids(levels, kingdom).length).toBe(3);
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
  });
  it("their raids open as the story advances, like the Eastern Kingdoms' (raid n after story battle n + 1)", () => {
    const done = progressBefore(original, levels, -1);
    const story = storyOf("tilicia");
    expect(raidUnlocked(camp, idx("tilicia"), 0, new Set([...done, story[0]]))).toBe(false);
    expect(raidUnlocked(camp, idx("tilicia"), 0, new Set([...done, story[0], story[1]]))).toBe(true);
    expect(raidUnlocked(camp, idx("tilicia"), 2, new Set([...done, ...story.slice(0, 4)]))).toBe(true);
  });
  it("the battles that hand out a bonus unit also open its upgrade", () => {
    const gives = (mapId) => Object.keys(rewards[mapId].units || {});
    for (const [mapId, unit] of [
      [5902, "cragsmen"],
      [5904, "spellwardens"],
      [5906, "sentinel"],
      [5923, "marines"],
      [5924, "pavisiers"],
      [5926, "battlemage"],
    ]) {
      expect(gives(mapId)).toContain(unit);
      expect(unlocksOf(mapId, true)).toEqual([unit]);
    }
    expect(rewards[5906].units.sentinel).toBe(1);
    expect(rewards[5926].units.battlemage).toBe(1);
    for (const id in bonus.rewards) expect((bonus.rewards[id].spoils || {}).Medal).toBeUndefined(); // Medals come from Major Victories
  });
});

describe("Resume Episode II (⚙ Settings)", () => {
  const veteran = json("veteran-army.json");
  it("reads an Episode II army file whole — no transfer limits", () => {
    const got = readResume(veteran);
    expect(got.units).toMatchObject({ pikemen: 11, cavalry: 11, king: 2, conjurer: 3, bloodgorgers: 4 });
    expect(got.spoils).toEqual({ Medal: 4, Weapons: 1, Spirit: 1 });
    expect(Object.values(got.units).reduce((a, n) => a + n, 0)).toBe(
      Object.values(veteran.army).reduce((a, n) => a + n, 0),
    );
    expect(() => readTransfer(veteran, { ep2: true })).toThrow(/import it in Episode I/); // the ordinary import refuses it
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
    const got = readResume(veteran);
    const army = combineCounts(earned, resumeDelta(got.units, earned));
    for (const k of new Set([...Object.keys(army), ...Object.keys(got.units)]))
      expect(army[k] || 0).toBe(got.units[k] || 0);
    expect(army.militiamen || 0).toBe(0); // the file has none, whatever the battles handed out
  });
});
