import { createRoot } from "react-dom/client";
import { useEffect } from "react";
import ReignShell from "./reign-of-swords/ui/ReignShell.jsx";
import { ROS_SEO } from "./reign-of-swords/seo.js";
import { SITE_GAME, landOnGame } from "./site.js";
import { useGameLang } from "./reign-of-swords/i18n/i18n.js";
import { AuthProvider } from "./auth/AuthContext.jsx";
import "./app.css";

// The page shows Episode II (site.js SITE_GAME): it runs off its own data folder, public/games/reign-of-swords-2/,
// and shares Episode I's sprites and audio. An address that still carries an episode hash is settled by landOnGame.
const ASSET_BASE = import.meta.env.BASE_URL + "games/" + SITE_GAME + "/";

function App() {
  const lang = useGameLang();
  useEffect(() => {
    const settle = () => landOnGame();
    settle();
    window.addEventListener("hashchange", settle);
    return () => window.removeEventListener("hashchange", settle);
  }, []);
  const seo = ROS_SEO[SITE_GAME];
  useEffect(() => {
    document.title = seo.heading + " — Remastered";
  }, [seo]);
  return (
    // The game fills the window (app.css .game-screen): nothing else shares the page, so the page itself never
    // scrolls — a screen taller than the window scrolls inside the frame.
    <section className="game-screen">
      <h1 className="visually-hidden">{seo.heading}</h1>
      <p className="visually-hidden">{seo.blurb[lang] || seo.blurb.en}</p>
      <div className="game-fit">
        <div className="wrap">
          <ReignShell assetBase={ASSET_BASE} />
        </div>
      </div>
    </section>
  );
}

createRoot(document.getElementById("root")).render(
  <AuthProvider>
    <App />
  </AuthProvider>,
);
