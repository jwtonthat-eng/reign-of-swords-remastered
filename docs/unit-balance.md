# Unit balance: the arena

Written by `tools/ros/arena-report.mjs` from the rows of `npm run e2e:arena` (src/reign-of-swords/e2e/arena.e2e.js).
Every number is a margin: the share of its points one side has left minus the share the other has left, from -1 to
+1, so 0 is an even fight for the price. The original units run the same tests and are the yardstick.

- **Duels**: equal-points squads against each of fourteen original units on an open field, from both sides.
- **Cavalry / Castle / Spear line**: a 1500-point squad against a mounted army; holding a castle against a
  storming party with Catapults; behind six Pikemen with six Archers behind it, advancing on a mixed army.
- **One for one**: six of the unit against six of the unit it is upgraded from. An upgrade must come out ahead.
- **Original finals**: the last battle of each original kingdom of Episode II, fought by the Autopilot with as many
  of the unit as the battle's points and the elite rule allow, Swordsmen and Militiamen for the rest: the share of
  the army kept on a victory, -1 on a defeat, and how many of those battles were won. A new unit far above every
  original unit here would steamroll the original game.

| Unit | New | Points | All | Duels | Cavalry | Castle | Spear line | Upgraded from | Token | One for one | Original finals | Won |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Samurai | yes | 250 | +0.44 | +0.36 | +0.80 | +0.47 | +0.11 | Footmen | Tsuba | +0.87 | -0.45 | 3/8 |
| Battlemage | yes | 750 | +0.43 | +0.49 | -0.19 | +0.94 | +0.48 | Wizards | Medal | +0.58 | +0.43 | 7/8 |
| Footmen |  | 75 | +0.38 | +0.53 | +0.65 | +0.15 | +0.19 |  |  |  | -0.52 | 3/8 |
| Swordsmen |  | 125 | +0.32 | +0.43 | +0.61 | -0.08 | +0.34 |  |  |  | -0.49 | 3/8 |
| Greatswordsmen |  | 150 | +0.28 | +0.28 | +0.27 | +0.21 | +0.34 |  |  |  | -0.53 | 3/8 |
| Dragon Riders | yes | 750 | +0.24 | +0.20 | +0.43 | +0.45 | -0.12 | Griffon Riders | Void | +0.90 | +0.03 | 6/8 |
| Jotunn | yes | 425 | +0.23 | +0.16 | +0.50 | -0.11 | +0.36 | Berserkers | Bloodstone | +0.77 | -0.57 | 2/8 |
| Taniwha | yes | 375 | +0.21 | +0.20 | -0.09 | +0.57 | +0.16 | Dune Sirens | Whalebone | +0.95 | -0.37 | 3/8 |
| Stone Sentinel | yes | 300 | +0.19 | +0.20 | +0.11 | +0.46 | -0.01 | Craftsmen | Spirit | +0.97 | -0.68 | 2/8 |
| Einherjar | yes | 275 | +0.15 | +0.25 | -0.26 | +0.43 | +0.19 | Shieldmaidens | Bloodstone | +0.78 | -0.45 | 3/8 |
| Oni | yes | 350 | +0.15 | +0.16 | +0.17 | -0.36 | +0.63 | Samurai | Tsuba | +0.53 | -0.68 | 2/8 |
| Gladiators | yes | 175 | +0.14 | +0.23 | +0.25 | -0.26 | +0.31 | Footmen | Anchor | +0.79 | -0.50 | 3/8 |
| Halberdiers |  | 125 | +0.10 | +0.27 | +0.54 | -0.27 | -0.12 |  |  |  | -0.67 | 2/8 |
| Berserkers | yes | 175 | +0.10 | +0.18 | +0.35 | +0.10 | -0.22 | Militiamen | Bloodstone | +0.73 | -0.70 | 2/8 |
| Shinobi | yes | 225 | +0.07 | +0.24 | +0.66 | -0.34 | -0.28 | Archers | Tsuba | +0.96 | -0.28 | 4/8 |
| Golem | yes | 400 | +0.05 | +0.16 | +0.53 | -0.41 | -0.07 | Stone Sentinel | Void | +0.69 | -0.57 | 2/8 |
| Hero |  | 500 | +0.02 | +0.34 | +0.55 | -0.43 | -0.38 |  |  |  | -0.66 | 2/8 |
| Pavisiers | yes | 200 | +0.00 | -0.24 | -0.09 | +0.55 | -0.20 | Crossbowmen | Armor | +0.77 | -0.27 | 4/8 |
| Khopesh Warriors | yes | 175 | -0.00 | -0.02 | +0.34 | -0.31 | -0.02 | Militiamen | Scarab | +0.89 | -0.68 | 2/8 |
| Beast Master | yes | 250 | -0.00 | +0.29 | +0.05 | -0.55 | +0.20 | Raiders | Anchor | +0.80 | -0.71 | 2/8 |
| Tengu | yes | 325 | -0.01 | +0.02 | -0.07 | +0.24 | -0.21 | Beast Master | Tsuba | +0.23 | -0.21 | 5/8 |
| Pikemen |  | 150 | -0.01 | +0.14 | +0.64 | -0.51 | -0.31 |  |  |  | -0.82 | 1/8 |
| Shieldmaidens | yes | 200 | -0.03 | +0.09 | +0.16 | -0.15 | -0.20 | Footmen | Bloodstone | +0.80 | -0.67 | 2/8 |
| Eagle Warriors | yes | 175 | -0.04 | +0.05 | -0.11 | +0.22 | -0.31 | Archers | Jade | +0.77 | -0.43 | 4/8 |
| Spellwardens | yes | 225 | -0.05 | +0.04 | +0.58 | -0.51 | -0.31 | Swordsmen | Lore | +0.77 | -0.81 | 1/8 |
| Jaguar Warriors | yes | 150 | -0.06 | +0.08 | +0.28 | -0.37 | -0.22 | Militiamen | Jade | +0.74 | -0.86 | 1/8 |
| Marines | yes | 150 | -0.07 | +0.02 | +0.22 | -0.15 | -0.39 | Militiamen | Anchor | +0.67 | -0.70 | 2/8 |
| Toa Warriors | yes | 150 | -0.08 | +0.07 | +0.42 | -0.36 | -0.45 | Militiamen | Whalebone | +0.69 | -0.83 | 1/8 |
| Tzitzimitl | yes | 250 | -0.09 | -0.02 | -0.61 | +0.75 | -0.47 | Shamans | Obsidian | +0.76 | -0.28 | 3/8 |
| Ammit | yes | 275 | -0.10 | -0.01 | -0.35 | +0.17 | -0.20 | Blood Gorgers | Scarab | +0.90 | -0.88 | 0/8 |
| Cragsmen | yes | 175 | -0.10 | +0.03 | -0.04 | -0.08 | -0.30 | Archers | Armor | +0.97 | -0.74 | 2/8 |
| Alchemist | yes | 250 | -0.11 | +0.01 | +0.13 | -0.32 | -0.27 | Priests | Void | +1.00 | -0.16 | 4/8 |
| Cavalry |  | 200 | -0.13 | +0.21 | +0.57 | -0.67 | -0.61 |  |  |  | -0.84 | 1/8 |
| Feathered Serpent | yes | 300 | -0.15 | +0.04 | -0.30 | +0.12 | -0.45 | Cavalry | Jade | +0.41 | -0.29 | 4/8 |
| Ahuizotl | yes | 175 | -0.15 | -0.02 | +0.15 | -0.48 | -0.24 | Blood Gorgers | Obsidian | +0.87 | -0.85 | 1/8 |
| Sohei | yes | 175 | -0.16 | -0.03 | +0.14 | -0.38 | -0.35 | Shamans | Tsuba | +0.46 | -0.88 | 0/8 |
| Coatecpatl Warriors | yes | 200 | -0.19 | -0.03 | -0.02 | -0.42 | -0.30 | Jaguar Warriors | Obsidian | +0.42 | -0.86 | 1/8 |
| Tahuanui Riders | yes | 250 | -0.21 | -0.06 | -0.27 | -0.32 | -0.19 | Raiders | Whalebone | +0.65 | -0.55 | 3/8 |
| Cuahchic Chieftain | yes | 275 | -0.22 | -0.11 | -0.69 | -0.00 | -0.08 | Eagle Warriors | Obsidian | +0.24 | -0.36 | 3/8 |
| Medjay | yes | 175 | -0.24 | -0.35 | -0.44 | +0.10 | -0.29 | Archers | Scarab | +0.66 | -0.80 | 1/8 |
| Griffon Riders |  | 400 | -0.25 | -0.08 | -0.37 | -0.24 | -0.31 |  |  |  | -0.56 | 3/8 |
| Tohunga | yes | 250 | -0.26 | -0.28 | -0.68 | +0.19 | -0.29 | Shamans | Whalebone | +0.50 | -0.44 | 3/8 |
| Wizards |  | 500 | -0.27 | +0.07 | -0.81 | -0.08 | -0.24 |  |  |  | -0.08 | 5/8 |
| Knights |  | 300 | -0.29 | +0.01 | -0.10 | -0.46 | -0.61 |  |  |  | -0.86 | 1/8 |
| Sun Priest | yes | 400 | -0.32 | -0.13 | -0.40 | -0.44 | -0.32 | Shamans | Jade | +1.00 | -0.14 | 5/8 |
| Archers |  | 100 | -0.34 | -0.32 | -0.46 | -0.15 | -0.44 |  |  |  | -0.82 | 1/8 |
| Anubis Priest | yes | 275 | -0.37 | -0.34 | -0.70 | -0.17 | -0.25 | Priests | Scarab | +1.00 | -0.35 | 4/8 |
| Crossbowmen |  | 125 | -0.40 | -0.51 | -0.61 | -0.05 | -0.41 |  |  |  | -1.00 | 0/8 |
| Primal Warden | yes | 400 | -0.43 | -0.50 | -0.71 | -0.10 | -0.41 | Druids | Void | +0.30 | -0.53 | 3/8 |
| Catapult |  | 300 | -0.61 | -0.63 | -0.80 | -0.54 | -0.48 |  |  |  | -0.88 | 0/8 |
| Musketeers |  | 175 | -0.64 | -0.68 | -0.75 | -0.59 | -0.52 |  |  |  | -0.88 | 0/8 |
