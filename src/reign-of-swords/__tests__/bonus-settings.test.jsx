// ⚙ Settings → Resume Episode II (ours): the panel's own part — pick an army file or the built-in veteran army,
// confirm, and say what happened. (What a resume does to the save is in bonus-shell.test.js.)
import { describe, it, expect, vi, afterEach } from "vitest";
import { render, screen, fireEvent, act, cleanup } from "@testing-library/react";
import { SettingsPanel } from "../ui/shell/SettingsPanel.jsx";

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});
const panel = (resume) =>
  render(<SettingsPanel onClose={() => {}} musicMuted={false} sfxMuted={false} resume={resume} />);
const settle = () => act(async () => await new Promise((r) => setTimeout(r, 20)));

describe("Settings: Resume Episode II", () => {
  it("is offered only when the shell hands it over (Episode II, outside a battle)", () => {
    panel(null);
    expect(screen.queryByText("Resume Episode II")).toBeNull();
  });
  it("the veteran army: asks first, then resumes with the built-in file and reports the army", async () => {
    const onResume = vi.fn(() => ({ units: { footmen: 10, king: 2 }, spoils: { Medal: 4 } }));
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(false);
    panel({ base: "/games/reign-of-swords-2/", onResume });
    fireEvent.click(screen.getByRole("button", { name: /Resume with the veteran army/ }));
    await settle();
    expect(confirm).toHaveBeenCalled();
    expect(onResume).not.toHaveBeenCalled(); // declined: nothing changes
    confirm.mockReturnValue(true);
    fireEvent.click(screen.getByRole("button", { name: /Resume with the veteran army/ }));
    await settle();
    expect(onResume).toHaveBeenCalledTimes(1);
    expect(onResume.mock.calls[0][0]).toMatchObject({ kind: "reign-of-swords-army", episode: 2 });
    expect(screen.getByRole("status").textContent).toMatch(/12 units and 4 collectibles.*bonus campaigns are open/);
  });
  it("an army file: a wrong or unreadable file is refused with the reason", async () => {
    const onResume = vi.fn(() => {
      throw new Error("This is not a Reign of Swords army file.");
    });
    vi.spyOn(window, "confirm").mockReturnValue(true);
    const { container } = panel({ base: "/games/reign-of-swords-2/", onResume });
    const pick = async (text) => {
      const file = new File([text], "army.json", { type: "application/json" });
      fireEvent.change(container.querySelector("#ros-army-resume"), { target: { files: [file] } });
      await settle();
      return screen.getByRole("status");
    };
    const refused = await pick("{}");
    expect(refused.textContent).toBe("This is not a Reign of Swords army file.");
    expect(refused.className).toContain("bad");
    expect((await pick("not json")).textContent).toBe("This file could not be read.");
  });
});
