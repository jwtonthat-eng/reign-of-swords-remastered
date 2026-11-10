import { tr, GAME_LANGS, setGameLang, useGameLang } from "../../i18n/i18n.js";
import { useVolume, setVolume } from "../../util/volume.js";
import { useGameOptions, setGameOption } from "../../util/options.js";
import { TRANSFER_LIMITS } from "../../data/save-transfer.js";
import { useState } from "react";
import { ReportBugGroup } from "./ReportBug.jsx";

// ARMY TRANSFER (ours — the originals are separate apps): export this episode's army and collectibles to a file, import
// the other episode's within data/save-transfer.js's limits. `transfer` = { ep2, onExport, onImport }.
function ArmyTransfer({ transfer }) {
  const [status, setStatus] = useState(null);
  const other = transfer.ep2 ? "Episode I" : "Episode II";
  const exportFile = () => {
    const data = transfer.onExport();
    const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 1)], { type: "application/json" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = "reign-of-swords-episode-" + data.episode + "-army.json";
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 0);
    setStatus({ ok: true, text: tr("Army saved to a file — import it in {ep}'s Settings.", { ep: tr(other) }) });
  };
  const importFile = async (e) => {
    const file = e.target.files && e.target.files[0];
    e.target.value = ""; // the same file may be picked again
    if (!file) return;
    let data;
    try {
      data = JSON.parse(await file.text());
    } catch (err) {
      setStatus({ ok: false, text: tr("This file could not be read.") });
      return;
    }
    try {
      const got = transfer.onImport(data);
      const count = (m) => Object.values(m).reduce((a, n) => a + n, 0);
      const notes = [
        tr("Brought in {u} units and {s} collectibles.", { u: count(got.units), s: count(got.spoils) }),
        got.converted ? tr("Episode II's own units arrived as the units they are upgraded from.") : "",
        got.capped ? tr("The rest stayed behind: only the limit comes across.") : "",
      ];
      setStatus({ ok: true, text: notes.filter(Boolean).join(" ") });
    } catch (err) {
      setStatus({ ok: false, text: tr(err.message) });
    }
  };
  const L = TRANSFER_LIMITS;
  return (
    <div className="ros-settings-group">
      <div className="ros-settings-label">{tr("Army transfer")}</div>
      <div className="ros-settings-row">
        <button className="btn-run ros-settings-opt" onClick={exportFile}>
          {"⤓ " + tr("Export army")}
        </button>
        <label className="btn-run ros-settings-opt ros-settings-file" htmlFor="ros-army-import">
          {"⤒ " + tr("Import from {ep}", { ep: tr(other) })}
        </label>
        <input id="ros-army-import" type="file" accept=".json,application/json" hidden onChange={importFile} />
      </div>
      <p className="ros-settings-note">
        {tr(
          "Carry part of your army to the other episode: export it here, then import the file in the other episode's Settings. Up to {pu} of each unit and {u} in all come across, and up to {ps} of each collectible ({m} Medal). Episode II's own units reach Episode I as the unit they are upgraded from. Battles won stay behind; importing again replaces the last import.",
          { pu: L.perUnit, u: L.units, ps: L.perSpoil, m: L.medals },
        )}
      </p>
      {status && (
        <p className={"ros-settings-note ros-transfer-status" + (status.ok ? "" : " bad")} role="status">
          {status.text}
        </p>
      )}
    </div>
  );
}

// RESUME EPISODE II (ours, Episode II only): pick up a finished Episode II from an army file — every Episode II battle
// and raid is marked won, the army and collectibles become the file's, and the bonus campaigns open. `resume` =
// { base, onResume }: onResume(data) applies a parsed army file and returns { units, spoils }, or throws.
function ResumeEpisode({ resume }) {
  const [status, setStatus] = useState(null);
  const apply = (data, everything = false) => {
    if (!window.confirm(tr("Replace your Episode II progress and army with this file? This cannot be undone."))) return;
    try {
      const got = resume.onResume(data, everything);
      const count = (m) => Object.values(m).reduce((a, n) => a + n, 0);
      setStatus({
        ok: true,
        text: tr(
          everything
            ? "Every battle unlocked. Your army: {u} units and {s} collectibles."
            : "Episode II marked complete. Your army: {u} units and {s} collectibles. The bonus campaigns are open.",
          { u: count(got.units), s: count(got.spoils) },
        ),
      });
    } catch (err) {
      setStatus({ ok: false, text: tr(err.message) });
    }
  };
  const unreadable = () => setStatus({ ok: false, text: tr("This file could not be read.") });
  const fromFile = async (e) => {
    const file = e.target.files && e.target.files[0];
    e.target.value = ""; // the same file may be picked again
    if (!file) return;
    try {
      apply(JSON.parse(await file.text()));
    } catch (err) {
      unreadable();
    }
  };
  const fromVeteran = () =>
    fetch(resume.base + "veteran-army.json")
      .then((r) => r.json())
      .then((data) => apply(data, true), unreadable);
  return (
    <div className="ros-settings-group">
      <div className="ros-settings-label">{tr("Resume Episode II")}</div>
      <div className="ros-settings-row">
        <label className="btn-run ros-settings-opt ros-settings-file" htmlFor="ros-army-resume">
          {"⤒ " + tr("Resume from an army file")}
        </label>
        <input id="ros-army-resume" type="file" accept=".json,application/json" hidden onChange={fromFile} />
        <button className="btn-run ros-settings-opt" onClick={fromVeteran}>
          {"♛ " + tr("Resume with the veteran army")}
        </button>
      </div>
      <p className="ros-settings-note">
        {tr(
          "Resume from an army file: every Episode II battle and raid is marked won, your army and collectibles become exactly those in the file (an Episode II army exported above), and the bonus campaigns open. Resume with the veteran army, for testing: every battle of every campaign, the bonus ones included, is marked won and open to replay, with 8 of every unit and collectible. Either replaces your current Episode II save.",
        )}
      </p>
      {status && (
        <p className={"ros-settings-note ros-transfer-status" + (status.ok ? "" : " bad")} role="status">
          {status.text}
        </p>
      )}
    </div>
  );
}

// ---- ⚙ Settings: the game's own language (separate from the site's EN / RU / UA switch), sound and gameplay ----
export function SettingsPanel({
  onClose,
  musicMuted,
  sfxMuted,
  onToggleMusic,
  onToggleSfx,
  transfer = null,
  resume = null,
}) {
  const lang = useGameLang();
  const volume = useVolume();
  const options = useGameOptions();
  const slider = (k, label) => (
    <label className="ros-vol-row" htmlFor={"ros-vol-" + k}>
      <span className="ros-vol-name">{tr(label)}</span>
      <input
        id={"ros-vol-" + k}
        type="range"
        min="0"
        max="100"
        step="5"
        value={volume[k]}
        onChange={(e) => setVolume({ [k]: +e.target.value })}
      />
      <span className="ros-vol-val">{volume[k]}%</span>
    </label>
  );
  return (
    <div className="ros-overlay ros-overlay-fixed ros-overlay-top" onClick={onClose}>
      <div className="ros-overlay-card ros-settings-card" onClick={(e) => e.stopPropagation()}>
        <h2>⚙ {tr("Settings")}</h2>
        {/* the groups scroll between the title and Close, which stay on screen however short it is */}
        <div className="ros-settings-body">
          <div className="ros-settings-group">
            <div className="ros-settings-label">{tr("Language")}</div>
            <div className="ros-settings-row" role="group" aria-label={tr("Language")}>
              {GAME_LANGS.map((l) => (
                <button
                  key={l.code}
                  className={"btn-run ros-settings-opt" + (lang === l.code ? " on" : "")}
                  aria-pressed={lang === l.code}
                  title={l.code === "en" ? tr("Original — recommended") : undefined}
                  onClick={() => setGameLang(l.code)}
                >
                  {l.label}
                  {l.code === "en" ? " ★" : ""}
                </button>
              ))}
            </div>
            <p className="ros-settings-note">
              {tr("Menus, battle controls, unit texts, the Field Manual and the story.")}
            </p>
          </div>
          <div className="ros-settings-group">
            <div className="ros-settings-label">{tr("Sound")}</div>
            <div className="ros-settings-row">
              <button
                className={"btn-run ros-settings-opt" + (musicMuted ? "" : " on")}
                aria-pressed={!musicMuted}
                onClick={onToggleMusic}
              >
                {musicMuted ? "🔕 " + tr("Music off") : "🎵 " + tr("Music on")}
              </button>
              <button
                className={"btn-run ros-settings-opt" + (sfxMuted ? "" : " on")}
                aria-pressed={!sfxMuted}
                onClick={onToggleSfx}
              >
                {sfxMuted ? "🔇 " + tr("Effects off") : "🔊 " + tr("Effects on")}
              </button>
            </div>
            <div className="ros-vol">
              {slider("master", "Master volume")}
              {slider("sfx", "Effects volume")}
              {slider("music", "Music volume")}
            </div>
          </div>
          <div className="ros-settings-group">
            <div className="ros-settings-label">{tr("Gameplay")}</div>
            <div className="ros-settings-row">
              <button
                className={"btn-run ros-settings-opt" + (options.realisticSiege ? " on" : "")}
                aria-pressed={options.realisticSiege}
                onClick={() => setGameOption({ realisticSiege: !options.realisticSiege })}
              >
                {"🏰 " + tr(options.realisticSiege ? "Realistic siege: on" : "Realistic siege: off")}
              </button>
            </div>
            <p className="ros-settings-note">
              {tr(
                "Off — the original: an AI army's archers, musketeers and war engines only shoot at foes near the point their group is marching to. On: they shoot anything in range, so garrisons fire from their walls. Applies from the next battle.",
              )}
            </p>
            <div className="ros-settings-row">
              <button
                className={"btn-run ros-settings-opt" + (options.autoCharge !== false ? " on" : "")}
                aria-pressed={options.autoCharge !== false}
                onClick={() => setGameOption({ autoCharge: options.autoCharge === false })}
              >
                {"⚡ " + tr(options.autoCharge !== false ? "Auto-charge: on" : "Auto-charge: off")}
              </button>
            </div>
            <p className="ros-settings-note">
              {tr(
                "On: your riders charge whenever they gallop 2+ tiles in a straight line and then strike the foe ahead. Off — the original: they charge only when you tap the foe at the end of the lane, and the gallop and the strike are one action. The AI always charges as in the original. Online battles keep it on. Applies at once.",
              )}
            </p>
          </div>
          {transfer && <ArmyTransfer transfer={transfer} />}
          {resume && <ResumeEpisode resume={resume} />}
          <ReportBugGroup />
        </div>
        <div className="ros-over-btns">
          <button className="btn btn-primary" onClick={onClose}>
            {tr("Close")}
          </button>
        </div>
      </div>
    </div>
  );
}
