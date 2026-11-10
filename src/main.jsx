import { createRoot } from "react-dom/client";
import { useEffect, useState } from "react";
import ReignShell from "./reign-of-swords/ui/ReignShell.jsx";
import { ROS_SEO } from "./reign-of-swords/seo.js";
import { useGameLang } from "./reign-of-swords/i18n/i18n.js";
import { AuthProvider } from "./auth/AuthContext.jsx";
import "./app.css";

// The two games, as on the website's game pages: Episode I runs off public/games/reign-of-swords/, Episode II off its
// own data folder (sprites and audio are shared with Episode I). The address hash picks the game: #reign-of-swords-2.
const GAMES = {
  "reign-of-swords": { assetBase: undefined },
  "reign-of-swords-2": { assetBase: import.meta.env.BASE_URL + "games/reign-of-swords-2/" },
};
const fromHash = () => (location.hash.slice(1) in GAMES ? location.hash.slice(1) : "reign-of-swords");

function App() {
  const [gameId, setGameId] = useState(fromHash);
  const lang = useGameLang();
  useEffect(() => {
    const onHash = () => setGameId(fromHash());
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);
  const seo = ROS_SEO[gameId];
  useEffect(() => {
    document.title = seo.heading + " — Remastered";
  }, [seo]);
  return (
    // The game fills the window (app.css .game-screen): the episode switch is a slim row above it and nothing else
    // shares the page, so the page itself never scrolls — a screen taller than the window scrolls inside the frame.
    <section className="game-screen">
      <nav className="game-switch">
        {Object.keys(GAMES).map((id) => (
          <a key={id} href={"#" + id} className={id === gameId ? "on" : ""}>
            {ROS_SEO[id].heading}
          </a>
        ))}
      </nav>
      <h1 className="visually-hidden">{seo.heading}</h1>
      <p className="visually-hidden">{seo.blurb[lang] || seo.blurb.en}</p>
      <div className="game-fit">
        <div className="wrap">
          <ReignShell key={gameId} assetBase={GAMES[gameId].assetBase} />
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
