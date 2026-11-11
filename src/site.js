// The public origin the game's search metadata (src/reign-of-swords/seo.js) builds its page URLs on.
export const SITE_URL = "https://github.com/Tsarar/reign-of-swords-remastered";

// THE SITE OFFERS EPISODE II ONLY (user decision). Episode I stays in the repository — Episode II draws its sprites
// and sounds from Episode I's folder and a third of the tests run on it — but nothing on the page leads to it: there
// is no episode switch, and the page boots straight into Episode II.
export const SITE_GAME = "reign-of-swords-2";
// The game the page shows for an address. The hash used to pick the episode (#reign-of-swords, #reign-of-swords-2):
// whatever it says now, it is Episode II, and the stale hash is dropped from the address bar so an old Episode I
// link or bookmark lands here cleanly.
export function landOnGame(loc = window.location, hist = window.history) {
  if (loc.hash) hist.replaceState(null, "", loc.pathname + loc.search);
  return SITE_GAME;
}
