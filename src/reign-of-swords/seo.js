// Search metadata for the Reign of Swords page — same shape as story-game/seo.js (GAME_SEO), so the runtime <Seo>
// (GamePage) and a build step that writes a static index.html per page both pick it up.
// THE SITE OFFERS EPISODE II ONLY (user decision; src/site.js): Episode I's entry was removed with its page, so nothing
// here advertises a game the page no longer shows. Worded for people searching for the ORIGINAL game, Punch
// Entertainment's "Reign of Swords Episode II" (iPhone, 2009). Facts come from the original build's own about/credits.
import { SITE_URL } from "../site.js";

const PUNCH = { "@type": "Organization", name: "Punch Entertainment" };

export const ROS_SEO = {
  "reign-of-swords-2": {
    path: "/games/reign-of-swords-2",
    lang: "en",
    locale: "en_US",
    title: "Reign of Swords Episode II (iPhone 2009) — play online",
    description:
      "An unofficial fan remake of Mobile Battles: Reign of Swords Episode II, Punch Entertainment's 2009 iPhone sequel, playable in the browser: the full campaign with new units, sieges and the desert kingdoms.",
    heading: "Reign of Swords II",
    blurb: {
      en: "An unofficial fan remake of Mobile Battles: Reign of Swords Episode II, Punch Entertainment's 2009 iPhone sequel, rebuilt from the original game data so it plays in the browser.",
      ru: "Неофициальный фанатский ремейк Mobile Battles: Reign of Swords Episode II — продолжения от Punch Entertainment для iPhone (2009), восстановленный по данным оригинала: играйте прямо в браузере.",
      uk: "Неофіційний фанатський ремейк Mobile Battles: Reign of Swords Episode II — продовження від Punch Entertainment для iPhone (2009), відновлений з даних оригіналу: грайте просто в браузері.",
    },
    intro: [
      "Reign of Swords Episode II (Mobile Battles: Reign of Swords Episode II) is the 2009 sequel to Punch Entertainment's iPhone tactics game. Sir Varius returns to defend the Empire of Carrone against Martin Landower, and the 33-mission campaign carries the war beyond the old kingdoms into the desert lands of Zayandi, Sabbi Amar and Abbisin.",
      "This unofficial browser remake is rebuilt from the original Episode II data and code, with every difference from the original documented. It adds the sequel's new units — Craftsmen who build and repair, Ballistae, Conjurers, Sappers, Bodyguards, Dune Sirens and Blood Gorgers — alongside the Episode I army, with destructible walls, gates and houses. No download or install — it runs in any modern browser.",
    ],
    game: {
      name: "Mobile Battles: Reign of Swords Episode II",
      alternateName: ["Reign of Swords Episode II", "Reign of Swords 2", "Reign of Swords II"],
      genre: ["Turn-based tactics", "Strategy", "Fantasy"],
      datePublished: "2009",
      gamePlatform: ["iOS", "iPhone", "Web browser"],
    },
  },
};

// schema.org JSON-LD: the page is ABOUT the original game (author/publisher = Punch Entertainment), playable here.
function rosJsonLd(s) {
  return {
    "@context": "https://schema.org",
    "@type": "WebPage",
    url: SITE_URL + s.path,
    name: s.title,
    description: s.description,
    inLanguage: s.lang,
    about: {
      "@type": "VideoGame",
      name: s.game.name,
      alternateName: s.game.alternateName,
      genre: s.game.genre,
      gamePlatform: s.game.gamePlatform,
      datePublished: s.game.datePublished,
      author: PUNCH,
      publisher: PUNCH,
      playMode: "SinglePlayer",
      url: SITE_URL + s.path,
    },
  };
}
Object.values(ROS_SEO).forEach((s) => {
  s.jsonLd = () => rosJsonLd(s);
});
