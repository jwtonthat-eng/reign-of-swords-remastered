import { useEffect, useState } from "react";
import { levelTitle } from "../../data/game-data.js";

// The campaign shell's data, loaded from the EPISODE's own folder (so the Episode II route shows Episode II's
// campaign): the world map's kingdoms and missions, the in-battle dialogue table, the level list (for raids, previews
// and the dev jump menu) and each mission's real spoils. `camp` stays null until it has loaded; a missing optional
// file just leaves its default.
export function useEpisodeData(dataBase) {
  const [camp, setCamp] = useState(null); // campaign.json
  const [battleEvents, setBattleEvents] = useState(null); // battle_events.json — per-map in-battle dialogue
  const [levels, setLevels] = useState([]); // levels.json — every map (hidden ones left out)
  const [rewards, setRewards] = useState({}); // rewards.json — per-mission spoils, from the scenario records
  useEffect(() => {
    const get = (file, fallback) =>
      fetch(dataBase + file)
        .then((r) => r.json())
        .catch(() => fallback);
    const shown = (list) => (list || []).filter((l) => !l.hidden).map((l) => ({ ...l, name: levelTitle(l) }));
    // bonus.json: Episode II's two BONUS campaigns (ours — tools/ros/bonus/build_bonus.py). Its kingdoms, levels and
    // rewards join the episode's own; Episode I has no such file.
    Promise.all([
      get("campaign.json", { kingdoms: [] }),
      get("levels.json", {}),
      get("rewards.json", {}),
      get("bonus.json", null),
    ]).then(([campaign, levelData, rewardData, bonus]) => {
      const extra = bonus || {};
      setLevels(shown([...(levelData.levels || []), ...(extra.levels || [])]));
      setRewards({ ...rewardData, ...extra.rewards });
      setCamp({ ...campaign, kingdoms: [...(campaign.kingdoms || []), ...(extra.kingdoms || [])] });
    });
    get("battle_events.json", null).then((events) => events && setBattleEvents(events));
  }, [dataBase]);
  return { camp, battleEvents, levels, rewards };
}
