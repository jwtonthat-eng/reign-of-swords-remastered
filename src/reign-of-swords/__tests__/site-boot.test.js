// The page around the game (src/site.js, src/main.jsx): the site offers Episode II only and boots straight into it —
// no episode switch, and an address from when the page had both games lands on Episode II.
import { describe, it, expect, vi } from "vitest";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { SITE_GAME, landOnGame } from "../../site.js";
import { ROS_SEO } from "../seo.js";
import { GAME_OF_EPISODE } from "../online/net.js";
import { loadEpisode, makeGame } from "./battle.js";
import { missionList } from "../engine/engine.js";

describe("the site boots straight into Episode II", () => {
  it("the one game the page shows is Episode II, and it has the page's search metadata", () => {
    expect(SITE_GAME).toBe("reign-of-swords-2");
    expect(SITE_GAME).toBe(GAME_OF_EPISODE[2]);
    expect(ROS_SEO[SITE_GAME].heading).toBe("Reign of Swords II");
  });

  it("an old Episode I address lands on Episode II, and the stale hash leaves the address bar", () => {
    for (const hash of ["#reign-of-swords", "#reign-of-swords-2", "#anything"]) {
      const hist = { replaceState: vi.fn() };
      expect(landOnGame({ hash, pathname: "/play", search: "?x=1" }, hist)).toBe("reign-of-swords-2");
      expect(hist.replaceState).toHaveBeenCalledWith(null, "", "/play?x=1");
    }
    const hist = { replaceState: vi.fn() };
    expect(landOnGame({ hash: "", pathname: "/", search: "" }, hist)).toBe("reign-of-swords-2");
    expect(hist.replaceState).not.toHaveBeenCalled(); // a clean address is left alone
  });

  it("the page has no episode switch, and its description names Episode II alone", () => {
    const root = process.cwd();
    const page = readFileSync(join(root, "src", "main.jsx"), "utf8");
    expect(page).not.toMatch(/game-switch|location\.hash|GAMES\b/);
    expect(page).toMatch(/SITE_GAME/);
    expect(readFileSync(join(root, "src", "app.css"), "utf8")).not.toMatch(/game-switch/);
    const html = readFileSync(join(root, "index.html"), "utf8");
    expect(html).toMatch(/Reign of Swords Episode II,/);
    expect(html).not.toMatch(/Episode I &/);
  });

  it("Episode I is hidden, not gone: its data still loads for the tests and the tools", async () => {
    await loadEpisode(1);
    const maps = missionList();
    expect(maps.length).toBeGreaterThan(20);
    expect(maps.every((m) => m.ep !== 2)).toBe(true);
    const game = makeGame(maps[0].mapId);
    expect(game.cols).toBeGreaterThan(0);
    await loadEpisode(2); // (leave the shared tables as the other files in this worker expect them)
  });
});
