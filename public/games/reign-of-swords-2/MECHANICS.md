# Reign of Swords — Mechanics & Decompilation Reference

This is the complete account of how the recreation works and where every rule comes from. Each finding cites the
original code it was read from: a C++ symbol and address in the iOS binaries (`ros_ep2` = _Reign of Swords Episode II_
1.0.11, 2009; `ros_ep1` = _Reign of Swords_ 1.2, 2008 — addresses are `ros_ep2` unless marked Ep1), a resource id in
the `.dat` archive, or a string id from the 5004 text table. Where a rule is ours rather than the original's, it says
so. The decoder scripts named here live in the project's `tools/ros/` folder and everything they read is in the
download.

## 1. Sources and tools

- **iOS binaries** — Mach-O armv6 Thumb with full C++ symbol tables (unencrypted). Read with `tools/ros/rosbin.py`
  (annotated disassembly of any symbol; `--all` dumps everything) and `tools/ros/rosrange.py` (an address range, for
  the static helpers that carry no symbol, e.g. the unit-AI handlers at 0x7c6e2–0x7d6f2).
- **`reignofswords.dat`** — the packed resource archive: `u32 count`, then per record `{id, packed type/offset, len}`;
  type 1 payloads are zlib. Reader: `tools/ros/rosdat.py`.
- **Resource families** — 5004 strings (unit/ability names, help, tutorial and menu text); 5009 dialogue screens
  (34-byte records, field[2] speaker, field[7] string); 5010 the unit table + weapon×armour damage matrix + terrain
  rows; 5017 the in-battle animation list; 5064 the quicksand whirlpool strip; 6201–6209 heraldic fields, 6301–6366
  charges, 6401–6409 frames; 5006 dialogue portraits (Ep1) — Ep2 portraits are 5017 frames 52–87; scenario records
  (mapId − 100) per mission; map grids per mapId.
- **`audio.dat`** — `u32 count (LE)`, then `count × {id, offset, len}`; offsets are relative to the end of the table.
  Entry N is sound id N exactly as `Context::play(id)` uses it.
- **Decoder toolkit** — `scenario.py` (mission grammar = `Mission::load*`, every record consumes exactly),
  `campaign.py` (kingdoms + unlock graph from `MenuScreen::selectKingdom`), `units.py` (5010 audit), `anim.py` (5017),
  `dialogue.py`, `audit.py`, `atlas.py` (the visual atlas at `/ros-atlas/`), `export_levels.py` (regenerates
  `levels.json`, `waves.json`, `battle_events.json`, `scripts.json`, `scripts_ai.json`, `group_heraldry.json`,
  `rewards.json`, `campaign.json`).
- **Android build** — the older notes came from the Android `classes.dex` (damage code `La/q`, turn cycle `La/g`).
  Where the two disagree the iOS binaries win; the Android reading of the shield (×0.75) and of the unit AI were both
  wrong and have been replaced.
- **Archive reader** — verified against `ResourceManager::read` in both binaries (u32 LE count, `{id, type/offset, len}`
  records, zlib for type 1).
- **Resource ids by slot** (`Context::deleteAllSaves` literal ranges, `MenuScreen::onMenuEvent` @0x5cd42): story map =
  5400 + 3·kingdom + slot, raid = 5600 + 3·kingdom + slot, skirmish = 5200 + 4·kingdom + slot, tutorial = 5800 + slot;
  scenario record = map id − 100. Names come from a per-kingdom block of 11 strings (`Context::getKingdomName`,
  `Context::getMapName`: +0 "Kingdom of X", +1..3 story, +4..6 raids, +7..10 skirmishes).

## 2. Units — the 5010 table

- Each unit record is 15 bytes `B[0..14]` + 3 lists + 6 upgrade slots, then a weapon table with header
  `[minRange, maxRange, ability, ability]` — ref: `Unit::readTypeInfo` @0x6482a, decoded by `tools/ros/units.py`.
- **B[0]** move points · **B[2]** armour id · **B[3]** weapon · **B[4]** second weapon (side-arm: the archer's short
  sword, the cannon's Grapeshot) · **B[5], B[6]** ability ids · **B[7]** COURAGE tier (stored at Unit+0x188, what
  `getCourage` switches on) · **B[8]** ATTACK rating tier (Unit+0x18c, what `getSkill` uses) · `lists[0][0]` the
  deployment cost the game shows as POW.
- **Rating tiers** 0..5 → attack skill 45/60/75/90/100/115 (`Unit::getSkill`) and courage 35/50/65/85/100/125
  (`Unit::getCourage` @0x66e90).
- **Weapons** 1 Staff · 2 Talon · 3 Spear · 4 Antlers · 5 Sword · 6 Mace · 7 Wand · 8 Short Sword · 9 Paw · 10 Halberd ·
  11 Flail · 12 Pike · 13 Greatsword · 14 Scythe · 15 Lance · 16 Longbow · 17 Crossbow · 18 Musket · 19 Short Bow ·
  20 Rock · 21 Boulder · 22 Pitch · 23 Cannonball · 24 Grapeshot · 25 Fireball · 26 Lightning · 27 Bolt; Episode II adds
  29 Hammer Throw, 30 Mallet, 31 Conjured Blade and the Ballistae's Piercing Bolt.
- **Armour** 0 None · 1 Padded · 2 Robes · 3 Light · 4 Nature's Cloak · 5 Breastplate · 6 Light & Shield · 7 Hide ·
  8 Heavy · 9 Holy Vestment · 10 Heavy & Shield · 11 Nature's Shield · 12 War Engine · 13 wood and 14 stone are the
  structure "armours" (see §6) · 15 Relic Armour.
- **Abilities** (5004 string order): 1 First Strike · 2 Last Strike · 3 Blast Area · 4 Fearless (no unit carries it) ·
  5 Formation · 6 Spot · 7 Move or Shoot · 8 Shoot and Move · 9 Fire Arrows · 10 Flammable · 11 Battle Standard ·
  12 Awaken Spirits · 13 Burst · 14 Fear · 15 Charge · 16 Stealth · 17 Ambush · 18/22 Magic · 19/23 Prayer ·
  20/21 Greater Shapeshift · 24 Siege · 25 Barrage · 26 Low Arc · 27 Pike Wall · 28 Spirit Shroud · 29 Arc · Episode II
  30 Leashing · 31 Build · 32 Repair · 33 Siege Armor · 34 Conjure · 35 Absorb · 36 Detonate · 37 Quicksand ·
  38 Life Steal. (An older table had the siege names off by one.)
- **Episode II units** — Craftsmen (type 29, rating 2), Ballistae (30, rating 3), Conjurer (31, rating 2), Sapper
  (rating 0, conjured), Bodyguard (rating 4, conjured), Dune Sirens (34, rating 2), Blood Gorgers (35). Their rating
  tiers were once read from the wrong byte and are now from B[8].
- The recreation's `data/combat-data.js` is generated from this table (0 mismatches on Ep1, ranges compared on the ranged
  weapon only). `kind` (spear/melee/cavalry/ranged/siege/hero) is OUR grouping for icons and AI, not a table field.

## 3. Combat — `Unit::calculateAttackDamage` @0x6af20 and friends

- **Damage is weapon-versus-armour.** `base = WEAPON_DMG[weapon−1][armour]` from the 5010 matrix; there is no
  weapon triangle. The original keeps HP on a 256 scale (100 HP = 256, Unit+0x190) and shows `HP·100 >> 8`; the
  recreation keeps whole HP (§13).
  Combat is deterministic apart from courage, deviation and the Lightning Storm's start.
- **Distance is Manhattan everywhere** — `Unit::getDistance(u, false, true)` → `getUnitMoveCost(.., true)` = |dx|+|dy|.
  Melee is 4-directional; the "diagonal ×0.8" branch in calculateAttackDamage is unreachable.
- **Attack rating** (`Unit::getSkill`): tier 45/60/75/90/100/115, +15 with a friendly Battle Standard or Spirit Shroud
  within 4 (not for the Hero himself), −15 with an enemy Spirit Shroud within 4, +30 per PINCER ally
  (`Unit::calcFlankBonuses`: a friendly unit adjacent to the target directly opposite the attacker) for melee, +15 for
  the team holding the capture points (Mission+0x260, written by `GameScreen::updateCapturePoints` = the team with
  STRICTLY the most units on the capture tiles).
- **Courage** (`Unit::getCourage` @0x66e90): tier 35/50/65/85/100/125, +15 friendly Standard/Shroud within 4 (the Hero
  included — only getSkill leaves him out), −15 enemy Shroud, +15 for the capture-point holder. A unit attacking a
  Fear-causer rolls `(random(1000)·256/1000) ≤ courage·256/100` and balks on failure (`Unit::attack`, sound 44); Fear
  units and Fearless units skip it (no unit is Fearless).
- **Charge** +30 (flag @0xb4): a mounted unit whose foe is more than 2 tiles (Manhattan) from its START tile and
  within its move, along a straight or diagonal lane of empty, affordable tiles — ref: `Unit::createChargeTargetList`
  (Ep1 @0x6037a, Ep2 @0x70d78), `Unit::isValidChargePath` @0x68d38 (Griffon/Great Eagle skip terrain). So it gallops
  two tiles and strikes the third. The foot unit behind the target is trampled with the same blow; a charge that kills
  its target carries the rider onto the cleared tile, and on to the trampled unit's tile if that one died too
  (`Unit::charge` @0x6bfe6 builds the run as a path; the two-kill landing is user-confirmed from play). Episode II
  adds one rule: no charge out of quicksand (`createChargeTargetList` @0x70bd2 lists no target while the rider's own
  tile is quicksand). Otherwise both episodes run the same charge code, bar Episode I's Pike Wall +30 vs a charge.
- **Pike Wall / First & Last Strike** (`Unit::isFirstStrike` @0x66fb4): pikemen always strike first against a mounted
  attacker (class 3 cavalry or Griffon Riders) unless it is the Hero; a braced wall strikes first against everyone but
  the Hero; Ep1 adds +30 to a braced pike's hit on a unit that is CHARGING (its state 3/4, @0x59902) — Ep2's damage
  code has no such +30 (see §13 for how the recreation applies it). A First Strike defender does not pre-empt a First Strike attacker; a Last Strike attacker
  still swings first against another Last Strike unit and against Cannon / Ballistae.
- **Formation**: −10 defence per adjacent Formation ally, skipped for Boulder (21) and Cannonball (23).
- **Cover**: terrain defence from the 5010 terrain row (`Map::getTileDefense`); Boulder and Cannonball half-ignore it
  (`def ≤ 80 → def += (100−def)/2`) and deal 0 to a FLYING target.
- **Shield** (`Map::isUnitShielded` @0x3b3ca): the map keeps a per-team list of priests who INVOKED Shield; a unit
  within Manhattan 2 of one (the priest included) takes ranged damage `>> 1` — it halves. It is a cast, not a passive
  aura, and expires at the team's next turn start.
- **Retribution** adds a smite to the counter. The prayer pushes the priest's tile on a per-group list (Map+0x158);
  `GameScreen::startTurn` clears that group's list. A unit within Manhattan 2 of a mark of its side
  (`Map::isUnitRetributioned` @0x3af88) is guarded: when an enemy's own MELEE blow lands on it on that enemy's turn
  (a shot never — a bow, musket or hammer goes straight to its projectile state, whose landing has no Retribution
  test; nor an area attack — exactly the help's "increase the counter attack strength of nearby allies"), it first goes to state 14 — `applyDamageRaw(25)` on the striker (@0x77846): 25 of
  256, about 10 HP, armour ignored, even if the guarded unit fell; the sword of light (#8) comes down on the striker and
  the read-out shows "10" — and then state 14's end decides the counter (@0x77a84): only if the striker had the
  initiative (`Unit::isFirstStrike(striker, guarded)`) and stands next to it (or the guarded unit has First Strike
  itself) — with no weapon that reaches (a Horse Bowman's bow at point blank) that counter is a bare swing for 0.
  A charge instead counts
  the guarded units it hits (Unit+0xc8, @0x78828) and is smitten for 25 per unit, +25 while its target stands, when it
  ends (`Unit::doFinishMoving` @0x774b2); that smite runs the same end, so a surviving target may then counter the
  rider — the only counter a charge ever meets. A slain priest takes its marks with it (`GameScreen::onEvent`, the
  unit-died event, deletes the positions on its tile); Shield's marks (Map+0x130) work the same way.
- **Siege Armor** (`Map::isSiegedAmor` @0x3ac3c): Ballistae always; other war engines when a friendly Ballistae is
  within the 5×5 square (Chebyshev 2). Melee damage ×8/10.
- **Absorb** (help 585, flag @0x384): an invoked one-hit shield on the Conjurer, laid by sacrificing a Bodyguard;
  `Unit::applyWeaponDamage` consumes it (target type 31 → damage 0, flag cleared; `calculateAttackDamage` returns 0 at
  @0x6af38).
- **Life Steal**: `Unit::applyDamage` @0x6b406 stores the Blood Gorgers' bite damage; `Unit::onTick` @0x780ac heals
  3/2 of it, capped at full health.
- **Flammable** ×2 from a fire WEAPON (`Unit::isFireWeapon` @0x80214: tag 9 Fire Arrows or 13, or the Fireball) — the
  weapon used, so an Archer's Short Sword is no fire. The binaries also have a BURNING tile overlay (5017 #41,
  `Map::renderBurning`, visual only) that the recreation does not draw.
- **Deviation** (`Unit::_executeAction`, `Unit::getDeviationChance` @0x665fa): a Barrage weapon (the Catapult's Rock)
  drifts on a flat 35 %; Arc weapons (Boulder) 15 % on cover / 100 % on a flier / 65 % vs cavalry and wizards / 25 % vs
  engines / 45 % otherwise; Low Arc and every Cannon shot 10/100/50/20/35; the Ballistae never. A drifting shot moves
  one tile in one of eight directions — off the board too, where it hits nobody.
- **Kills and score**: `applyWeaponDamage` adds the victim's point value (@0x194) to the killer's team for mission
  types 1–3. Units that die simply leave the field — there is no death sound in the original.
- **Villages and keeps** heal the shown HP by the terrain row's `heal` (20) at the start of the unit's turn; a
  Priest's Heal and a Craftsman's repair of a war engine add 51 of 256 (+20 here, in whole HP).
- **Pincer detail** — `Unit::calcFlankBonuses` @0x6ac50 is called by `getSkill` for a melee blow only: the axis is
  attacker → target (east-west or north-south) and every other friendly unit adjacent to the target on that axis adds
  +30.
- **Charge cost** — each lane step costs `Map::getMoveCost`, counted twice on a diagonal (`createChargeTargetList`
  @0x70ee0), and the whole run must fit the mount's move.
- **Destructible structures** — byte-faithful to `Map::applyDamage` @0x7ffa0: every cell starts at 256 structure HP
  (`Map::loadMap`); a blow of weapon w on a cell of material m (`Map::getTileArmorType`: 13 wood / 14 stone) removes
  `((HP256 · getSkill256) >> 8) · (w[m]·256/100 · share) >> 8`, where HP256 is the attacker's strength on the 256 scale,
  getSkill its attack rating with auras, and share the blast share of that cell (100 % at the centre). The cell drops
  ONE damage stage (`Map::getTransitionTile`, the tile is redrawn by `Map::tag`) when it was untouched and the blow did
  any damage, or when HP falls below 0; HP is not reset by a stage change, so a pristine house is damaged by the first
  real hit and destroyed once 256 damage has accumulated. Open ground loses HP too (material 0) and a village later
  built on it inherits that. The struck cell takes the blow whenever a unit sheltering there is hit
  (`Unit::onTick` → `Map::applyDamage`) and when a shot is aimed at the empty building.
- **Repair** — `Map::applyRepair` @0x80088 (called from `onTick` with 20): +20 structure HP and the cell steps back one
  stage; a Craftsman may mend an adjacent cell that some earlier stage transitions into (`Unit::canRepair` →
  `Map::isStructureRepairable`, `getPreTransitionTile != −1`) or an adjacent damaged war engine (+51 of 256 through
  `Unit::heal`, the same step as a priest's Heal).
- **Build** — `Map::applyBuildVillage` @0x3f744 replaces open ground (`Map::isBuildable`: terrain types 2, 3, 18, 26)
  with a village tile drawn from the cell's own tileset: tileset 3 → 249 if sub-index > 51 else 185; tileset 4 → 249 if
  sub-index − 7 in 0..27 else 185; tileset 6 → 249 if sub-index ≤ 3 else 3; any other → 3 (3 = wooden house on
  grass, 185 = desert house on sand, 249 = desert house on paving). The new hamlet heals, gives cover and burns like any
  house; Craftsmen build once per battle.

## 4. Abilities in play

- **Prayer** (strings 639/640/641): Heal +20 with the sparkle strip (5017 #3) and a glow on the ally (#40); Shield
  (the dome, #6, sound 22) as above; Retribution (#9 angel, sound 10).
- **Magic**: Fireball (weapon 25, strip #26, sound 14, burst 13), Ice Shard/Ice Field (18, overlay #7), Lightning Storm
  (26, bolts only, the one true 3×3). The player's wizard starts with no spell chosen; AI wizards default to Fireball.
- **Battle Standard / Spirit Shroud** are the two +15 auras above. Shroud is INVOKED at the end of turn (`Unit::curse`
  sets flag @0x45, sound 17); the spear-spirit strip (#4/#5) rises over each Shaman.
- **Greater Shapeshift** (druids): strip #0, sound 11. The form stays: nothing turns a shifted druid back (the saved
  type Unit+0x278 is read only by Undo), so it acts and waits out the enemy's turn as the beast. A Druid and each of
  its forms may shapeshift once a turn before acting — a beast back to the Druid or into one of the other two — and
  Undo right after takes the shift back. Not over water or cliffs: the option is greyed out where a Formation unit
  couldn't stand (`Map::getMoveCost(2, tile) > 4`, Ep1 `GameScreen::initMenuState` @0x1b670), and the AI keeps its
  form there too. The AI druid (`Unit::aiConsiderAction` state 2) is offered a shift twice a turn: before it moves
  (a Stag charge that scores → Stag; a foe within 5 → no change yet; else a Great Eagle, or the form that keeps its
  group's pace, back to the Druid for a foot group) and — as the move step takes the state back off its tried list
  (`mlib_Vector::removeElement`, iOS Ep2 0x31c2c / Ep1 0x28f26 / Android) — again after a plain move if it hasn't
  shifted: then a foe within 5 → **Guardian Bear** (the Bear test needs the moved flag Unit+0x112), which may still
  strike from where it stands.
- **Stealth / Ambush / Spot**: hidden units (`Unit::setIsHidden` @0x656b0, `Unit::canHide` @0x65fd8: own tile
  defence ≤ 90 and no enemy adjacent). A Stealth unit hides at battle start or when spawned, and at the end of its
  own turn if it did not attack. It is revealed when it attacks, when it is damaged, or when an enemy with Spot starts
  its turn within 4. A move that steps next to a hidden foe stops there; the foe is revealed and strikes once, and the
  mover's attack is spent (`Unit::onTick` @0x7839c, `doFinishMoving` @0x770ca). The original's "Ambush" menu command
  (hide in place, charge `Unit+0x288` = 3, which also lets Stealth hide after a move) needs ability 17, which no unit
  carries in either episode, so it never appears there either.
- **Move or Shoot / Shoot and Move**: Craftsmen carry Move or Shoot through the Hammer Throw (weapon 29): after moving
  they cannot attack at all, melee included — that is the data.
- **Siege**: Barrage (Catapult) bursts in a + cross, full on the tile, half on the four edge-neighbours, may drift one
  tile; Cannon fires one tile (Low Arc) and at point-blank rakes a Grapeshot cone (weapon 24, sound 9, pellets #25);
  Trebuchet's Boulder is one tile (Arc, dark round shot #28); Ballistae's Piercing Bolt flies on through three tiles
  (#29, sounds 51/52). Low Arc / Arc never gate gameplay in the binary — they are trajectory labels.
- **Episode II**: Build (Craftsmen raise a village stage, strip #13 + #12, sound 53) and Repair (restore a structure
  one stage); Quicksand (Dune Sirens: `Map::setQuickSandTile(x, y, turns)` writes a countdown layer at map+0x50, drawn
  as resource 5064 (a 4×40×40 strip built in `MenuScreen::loadStep`, laid over each tile by
  `Map::redrawTileInBuffer`) with frame = tick/100, sand skull #14, sound 22; it bites its occupants each turn); Conjure (the
  Conjurer raises a Sapper or Bodyguard, max two minions, pentagram #11, sound 55; minions farther than 8 from a living
  Conjurer die at the side's turn end — Leashing, help 592); Detonate (the Sapper's blast, sound 56); Absorb and Life
  Steal as in §3; Teleport (wizard, strip #1, sounds 58/59).
- **Leashing, the other half** — when a Conjurer falls, every unit it conjured is unsummoned at once
  (`killConjurerChild` @0x7fdcc).
- **Wizard Teleport** — `Unit::createMoveDestinations`' wizard branch @0x6e5f6 (type 21): every EMPTY tile within
  Manhattan distance ≤ move is a destination if its own move cost for a foot unit is ≤ move; nothing in between
  matters (the blink is a straight hop), but the landing tile must be ground a foot soldier can stand on. The help's
  "ignoring all terrain but water" describes the path, not the landing.
- **Retribution** rings the Heal chime (sound 10, `Unit::retribution`) and shows the angel (#9).

## 5. Turn order, sides and heraldry

- **Turn cycle** — the round cycles over the mission's GROUPS in ascending scenario order (Android `La/g` cycles
  `aQ = (aQ ± 1) % J` over `J` groups; iOS `GameScreen::startTurn` @0x276e8 rebuilds the point-concentration layers per
  team each turn). Group 0 is always an enemy, so every campaign map is enemy-first while the player sits at a
  variable index (0 on most maps, 1 on 5402/5405, 2 on 5417). `levels.json` carries `groupOrder` and `playerGroup`.
- **Teams and factions** — the binary's "faction" owns the gold budget (`factions[0]` is the human, `.b` = its team
  index, `.gold` = the deploy budget, `.ab` = the objective string); its "team" is a named army with heraldry
  (`Mission::loadTeams` @0x5dbc6).
- **Team record** — the 6 bytes after the name: `[faction, symbolColour, fieldColour, device, field, banner]`
  (0xff = 0). Verified arms: Carrone `[2,3,26,-,2]` = Or eagle on Gules, frame 2; the Emperor `[8,4,26,-,8]` = Argent
  eagle on Purpure, gold frame 8; Duke Pellus `[2,1,54,-,7]` = Or axe on Azure, frame 7.
- **Tinctures** — ten 3-shade ramps at `ros_ep2` @0x91d54: 0 vert, 1 azure, 2 or, 3 gules, 4 purpure, 5 sable,
  6 tenne, 7 rose (#d485b8/#cf6bac/#c9519f), 8 argent, 9 cyan (#a3faff/#5fc1c7/#1a878f). The player's picker offers
  the classic eight; rose and cyan are NPC colours (the Wizard's Palace Guard, the Caladrin Defenders).
- **Charges** 6301–6366 (66); the last seven (6360–6366) are pre-coloured faction crests (Sangsoleil's red fire,
  Aguilleon's black eagle, the Rebel gold fleur, Bordavia's three swords, Marsur's scythe…) and are never
  palette-swapped. **Frames** 6401–6409 in this order: plain, crossed swords, banner+swords, spears+drape,
  helm+drape, helm ornate, winged helm, winged helm+laurel, gold crown — the team's banner byte IS the frame index.
- **Rendering** — `Context::renderHeraldry(GL, x, y, frame, field, …)` palette-swaps the monochrome masks
  (`getPaletteColor` / `replacePaletteIndex`) — the FRAME too: its key greens take the symbol colour (the Emperor's
  gems → Argent, white → lavender → periwinkle) and its key blues the field colour (Carrone's drape → Gules); in battle `GameScreen::renderDecoporateMenu` draws the acting team's
  arms in the turn-start states 0x23/0x24 — so the original shows every army's crest at its turn, as we do.
- **Colours on units** — the unit's tabard tint is the group's banner colour; the HP number uses the "unit strength
  colour" (help 659): player green, allies blue/cyan, enemies red/orange/yellow by turn order.
- **Facing** — `GameScreen::createUnitAt` @0x292bc sets unit byte 0x14f = (x < cols/2): a new unit looks toward the
  map's centre line whichever side it is on; moving and attacking turn it (`Unit::changeState`, `moveAttack`).
- **The player's heraldry and rank titles** (Squire → Warden of Carrone) are ours.

## 6. Maps, scenarios and scripts

- **Map grid** — a tile index per cell into the tileset (Ep1 124 tiles at 40 px, Ep2 the same indices at 55 px plus
  more); `Map::getTileType` maps a tile to one of the 5010 terrain types, whose rows give defence %, heal and the
  per-class move cost `[fly, skirmish, formation, cavalry, engine]` (`Map::getMoveCost`; 0 → 1, 100 = impassable) and
  the only neighbouring types a ground unit may step between (`Map::isMoveAllowed`) — exported as `movement.json`.
- **Destructible structures** — `structures.json` from 5010: which tiles are wood (armour 13) or stone (14)
  (`Map::getTileArmorType` = terrain field 0xe, a column of the damage matrix), the next damage stage of each tile
  (`Map::getTransitionTile`), the stage Repair restores (`Map::getPreTransitionTile`), and the real terrain row of
  every razed end tile. Siege shots, fire arrows, magic and bolts knock a wall down one stage; Craftsmen repair it.
- **Scenario record** (`scenario.py`, grammar = `Mission::Mission` @0x62026 → `Mission::loadFactions`, `Mission::loadTeams`,
  `Mission::loadUnits`, `Mission::loadTriggers`, `Mission::loadActions`, `Mission::loadMarkers` @0x60050): header `[i = mission type, turnLimit, …, rewards p/q]`;
  factions; teams; unit templates `(type, team)`; per side (0 = the campaign perspective, 1 = raid defence) a trigger
  table and an action list; then the marker sections.
- **Mission type** `i`: 0 destroy the army, 1 hold one area, 2 hold areas by points (kills add the victim's point
  value), 3 escape/escort (the goal-area tiles; a player unit ending there leaves the field — tag 9 `[n, ?, cmd]`
  fires on the n-th escape; escort maps use the escort markers and tag 11 `[required, cmd]`).
- **Triggers** (tags): 1 deploy stage, 2 battle start, 0 round `[round, team, cmd]` (Ep2 `[round, team, counter,
value, cmd]`), 6 tile reached `[x, y, cmd]` / Ep2 `[x, y, counter, count, team, cmd]`
  (`GameScreen::checkLocationTriggers`), 7 unit lost, 8 counter, 4 victory chain, 5 defeat chain.
- **Actions** (opcodes, `Mission::performAction` @0x60b44): 0 SPAWN `[x, y, template, aiControlled, …, next]`
  (`GameScreen::createUnitAt` with group −1 → the marker lookup), 1 SCREEN (dialogue), 2 CAMERA, 3 MOVE, 4 HIDE,
  5 ATTACK, 6 SHOW, 7 TAG, 8 REMOVE (a fleeing hero leaves the map), 9 COUNTER, 10 SETFLAG, 11 AIMODE (see §7).
  Unit ids in MOVE/REMOVE/AIMODE = `10 × team + spawn index within the team`.
- **Markers** — section A `(group, team, x, y)` are the deployment blocks AND the AI group table
  (`Mission::getLocationGroup` @0x5f660); B warp portals (Ep2); C objective areas `flag; n × (points, tiles)`; D and E
  point lists; F the escort operation (Ep2). Exported as `levels[].markers = [x, y, group, team]`.
- **Waves and events** — round-triggered spawns and lines come from the trigger tables (`waves.json`,
  `battle_events.json`); kill-, tile- and counter-gated spawns, HIDE/SHOW, REMOVE and the escort rule run through the
  script runner from `scripts.json`. Victory is withheld while waves are pending, ambushers hidden or an escort en
  route.
- **Rewards** — `GameScreen::createRewardsMenu` (Ep1 @0x192b4, Ep2 @0x1e08a): the header list holds reward tokens;
  token < 100 = a unit of that 5010 type joins the army, token ≥ 100 = collectible token−100 (0 Medal, 1 Armor,
  2 Weapons, 3 Beasts, 4 Spirit, 5 Lore, 6 Flight); `q` draws p tokens at random. Exported as `rewards.json`.
- **Special win rules** pinned by the objective strings (ours, from the text): 5406 hold the line to the turn limit,
  5412/5413 escape with more than half the force, 5416 lose fewer than three war engines.
- **Episode II world** — `MenuScreen::selectKingdom` has hit-rects only for Zayandi, Sabbi Amar and Abbisin; the
  eight Episode I kingdoms are kept on the map by the user's decision (flagged "Episode I"). Episode II opens with
  Zayandi Shores (map 5424, record 5324); see the correction on record 5400 below. Ep2 Carrone 1 (record 5703) is Ep1's Carrone 1 with every coordinate shifted; the layout is taken
  from the Ep1 record 5300 because footage of the original shows it.
- **Placeholders** hidden from the lists: 5626/5629/5632 "Raid 3" (no start trigger) and 5235/5239/5243 "Server 4".
- **Move cost** — `Map::getMoveCost` @0x3ba3a (same table in Ep1): the cell's terrain type (`getTileType`; none →
  impassable) indexes the 5010 cost rows by the unit's movement class; 0 costs 1, 90+ (the data uses 100) is
  impassable; ground units must also obey `Map::isMoveAllowed` on the step they take; a type-16 cell held by the
  unit's own side costs 1. Not ported: the original also blocks the two bottom corner cells in one screen mode where
  the iPhone soft keys sit. Episode II only: a tile an enemy stands on blocks the step, except for Griffon Riders,
  Great Eagles and Dune Sirens, which fly / glide over enemy units (never stopping on one). Episode I's move search
  (`Unit::checkLocation` @0x58920) stops at any visible enemy for every unit, so its flyers go round them.
- **Warp portals** (Episode II) — `Mission::getSourcePortal` / `Mission::getDestPortal` / `Mission::canUsePortal`, `Unit::onTick`
  post-move, `Unit::getPortalOutput`: each portal is ONE-WAY source → destination with a list of the scenario groups
  allowed through (empty = everyone; a two-way gate is two records). `getMoveCost` makes an exit-only pad (90) and a
  gate the team may not use (100) impassable. The exit tile is searched outward from the destination pad in the
  order of the `gWarpPositionX/Y` tables (@0x95c38 / @0x95ba8, 72 offsets: the four axis cells at distance r, then the
  off-axis cells at Manhattan r+1 clockwise from the top-right, r = 1..8); the first cell the unit may stand on that
  touches the pad or paths back to it wins, and the camera follows (`GameScreen::moveViewport`).
- **Tile-reached triggers** are checked by `GameScreen::checkLocationTriggers` @0x272c8 from `GameScreen::onTick`
  against the player side's list (faction 0), team −1 meaning any of that side's units.
- **Sides of a script** — `Mission::getActionSequence` indexes the trigger table by the play side (Mission+0x90), so
  only side 0 is the campaign; side 1 is the raid-defence perspective. Tag-1 sequences run in the deploy stage
  (`GameScreen::isLoadingMap`), tag-2 at battle start (`GameScreen::activateGameState`); both spawn the fixed forces.
- **Correction on the Episode II prologue** — `MenuScreen::onMenuEvent` @0x5cd42 loads story map 5400 + 3·kingdom +
  slot, so Zayandi (kingdom 8) plays 5424/5425/5426 and record 5400 is only ever reached as Carrone's first slot.
  Record 5400 is an OLDER, unused copy of Zayandi Shores with placeholder unit templates (types 29–35) — the Craftsmen /
  Blood Gorgers / Conjurer roster it appears to field is that placeholder data, not a real army. The genuine opener is
  5424 "Zayandi Shores", whose Carrone force is Knights, Cavalry, Archers, Pikemen, Swordsmen and Militiamen. 5400 (and
  the 5800 copy with all-Gorger templates) stay in the data for the atlas, hidden from the campaign. The tutorial in
  slot 5805 has no title string in the table (the names end at "Combat Training").

## 7. The AI — `GroupLogic` and `Unit::aiConsiderAction`

- **Groups come from the marker table.** A unit spawned ON a marker joins its team's group number `marker.group`;
  the team's `GroupLogic[groupId]` is created on demand with the team byte (`GameScreen::createUnitAt` @0x29188,
  `Mission::getLocationGroup`). A unit spawned off any marker has NO group and uses only the per-unit rules.
  `Mission::setGroupId` (8-neighbour flood fill) is used by head-to-head raids only; `Mission::readRaidSide` builds the
  same per-marker groups for raid maps. So on Marsur 2 the militia block is group 0 and each musketeer pair and cannon
  its own group; on Bordavia 1 the gate block and the archer posts are four groups.
- **Modes** (`GroupLogic::determineTarget` @0x38bec, `GroupLogic::updateGroup` @0x38c5e). Mode 0 (default) = ADVANCE: the
  target is `Map::getBestPointConcentration(centre, 1 − teamByte)` @0x3eeb8 = the tile maximising `layer·6 ÷ (manhattan + 5)`
  in integers (the first of equal values wins), where layer t (`Map::updatePointConcentration` @0x3ae66, rebuilt each
  turn in `startTurn`) is every unit of team byte t — for the enemy that is the player's side, ALLIED armies included
  (they are team 0) — by (hp·256 × value) >> 8 under a diamond kernel, plus +100 on every capture tile that team does
  not own. An allied group (team 0) reads layer 1, the enemy's, the same way; only a third team (byte > 1, none in
  either episode) keeps `determineTarget`'s closest enemy. Value = Unit+0x198 = (cost − 50)·50 ÷ 450 + 50, integer. Mode 2 = HOLD (script op 11 AIMODE(unit, 1): `mode = 2, flag7 = 0`,
  `Mission::performAction` @0x60f7c): the target is `dest`, fixed at the first update to the group's initial centre.
- **March** — path = `Map::calcShortestPath(centre → target, leader)` @0x3b470; NEXT = the path point the group's
  pace reaches (min move over members; druids count 10); a formation width from the group size; each member takes a
  SLOT from the sixteen offset tables C.142–C.157 (`GroupLogic::getGroupPositionOffset` @0x38534 — facing = NEXT −
  centre, horizontal / vertical / diagonal layouts); `GroupLogic::getMoveOrder` @0x38794 = NEXT + offset. There is no "arrived" state: a group keeps re-forming on
  NEXT each round.
- **Release** — `applyDamage` sets group flags 0x50/0x51; a HOLD group hit one round and not the next drops to mode 0
  (flag 0x52 chain at the top of `updateGroup`). (The "drop the path once an enemy is within min(pace, 4)" rule
  touches only a scripted static path, which no record sets — it never fires.)
- **Per-unit AI** — `Unit::aiConsiderAction` @0x7bb1c switches on the unit's PENDING ACTION id (unit+0x2a8, written by
  `prepareAction`/`_executeAction`/`cleanUpAction`), not on a state; values 8/9/default reach the generic path at
  0x7d4ea: closest enemy (`Unit::getClosestEnemy` @0x65ef8) → group order → `createChargeTargetList` (charge at
  once when a lane reaches a foe and `calcDamageRatio` @0x70054 is positive) → otherwise advance on the foe
  (`createMoveDestinations` @0x6e450, `getBestMoveLocation` @0x7d6f2). The "closest foe within 9 or wait" test exists
  only inside pending-action 10's handler (0x7ce06); an idle unit is never passive. Ep2 abilities have their own
  handlers (Quicksand `considerQuickSand` @0x685ca, Build/Repair, Conjure, the ranged `createSortedTargetList`
  @0x7ac98).
- **The state chooser and the move** — `GameScreen::aiUpdate` (Ep2 @0x31088, phase table @0x310d4) gives each unit a
  pending action from a fixed order (phase 3): charge (13, not once moved) → druid shift (2) → Priest prayer (6) and
  heal (3) → Wizard standoff (9, not once moved) → siege point (15, the player's side; Episode I's case does nothing)
  → area attack (10) → Episode II's Sapper (30), Bodyguard (29), Conjure (28), Craftsmen Repair (27) and Build (26),
  Dune Sirens' Quicksand (31) → then its target list: none → move (phase 4), else the attack step (phase 6: move to
  the attack tile, then strike). A state that fails goes on the unit's TRIED list; the move step takes states
  14/10/5/3/6/2 back off it (`mlib_Vector::removeElement`; the attack step also 27/26/31), so once it has moved
  (Unit+0x112) the chooser runs again before anything else: a druid that hasn't shifted may turn Bear, a Priest prays
  or heals an adjacent ally — and a moved Priest that has tried both is given Shield anyway (action 6 executed where it
  stands, Ep2 0x317fc / Ep1 0x28c6a; a Priest always takes the move step, so every AI Priest turn ends in a prayer or
  a heal) — a Wizard re-judges its spells, and on the attack step Craftsmen repair or build and
  Dune Sirens lay quicksand from where they stand — only then the strike. States 4 and 5 exist but are never offered.
- **The battle-start prayer** — between the battle-start staging (`activateGameState`'s tag-2 sequence) and the first
  turn, `GameScreen::gameStateUpdate` state 2 (iOS Ep2 @0x1fc3a; Android `aW == 2`) has every Priest outside group 0
  (Unit+0x14c — the player's own Priests too when their group isn't 0) pray where it stands: the AI's prayer choice,
  else Shield. Its side's first turn start clears the mark, as for any prayer.
- **Data check** — Marsur 2 (5307) flags the musketeers, cannons and hero to HOLD and leaves the militia block to
  advance in formation; Bordavia 1 (5309) flags every group, so the pike block holds the gate. Fields of Vuldyne's foes
  sit on no markers and simply advance.
- **Ours, not the original's**: the order the choice is made in. The original first asks from where the unit
  stands (`createSortedTargetList`), else moves and asks again from where it lands; here one pass weighs every tile
  it can reach, with the same scores (`calcDamageRatio`; a grouped melee unit's attack tile within half its move of
  its slot; Move-or-Shoot weapons out once moved) — so the choices match, and only the tie-break between two equally
  good options may fall differently. After a move the unit still looks again from where it stands, as in the
  original: a foe the move brought next to it (through a portal, or one its slot rule ruled out before) is struck.
  The reachable-tile list (`createMoveDestinations` / `Unit::checkLocation` @0x6967c), formation ranks and widths (`GroupLogic::updateGroup`),
  the movers (`getBestMoveLocation` and its Ranged / Horse Bowmen / Charge / Priest / Wizard variants), the Wizard's
  spell choice and the absence of any retreat follow the binary. The original's tactics for the PLAYER's deployment groups (Tactics Path / Set Tactics,
  strings 98–100 and 106–107: "Advance to Destination", "Defend Destination", "Hold in Reserve", "Hold Turns";
  `GameScreen::repositionTactics` → control state 0x35 "- SET THE PATH -") are not reproduced yet.

## 8. Economy and campaign

- **No starting army.** A new game zeroes the roster (Android `La/r.e()`); the only non-zero seed is a debug cheat.
  Units come from mission rewards (§6), the Merchant and Upgrade-Army conversions; the force a mission issues fights
  that battle only (`createRewardsMenu` adds the reward list to the stored army and nothing else).
- **Deploy budget** — `factions[0].gold`; each unit costs its POW (`lists[0][0]`: Militiamen 50 … Knights 300); the
  ELITE cap is budget / 1000 slots (`UnitSelector` constructor); only units you muster count against caps and type
  limits — allies and the record's pre-placed core do not. Starting with 100 or more points left asks "You have not
  fully utilized your deployment points. Victory will certainly be more challenging. Continue?" (Ep1
  `GameScreen::onMenuEvent` @0x2409e, string 103; Ep2 `GameScreen::onSendRaidClicked` @0x29646, 117); starting with
  nothing placed is refused with "ARMY SIZE TOO SMALL" (Ep1 746, Ep2 825). (Ep2's online raid also refused a muster
  that left more than 30 % unspent; there are no online raids here.)
- **Repeat the last setup** — when a muster is complete, the units you placed are kept per map (type, tile, facing;
  `GameScreen::saveRaidSetup` / `captureDeployData`, file `setup<map><side>.sav`); the next muster of that map asks
  "Previous Setup Found — Do you want to repeat the last battle setup for this map?" and sets them down again
  (`loadRaidSetup`), warning "Missing Units" when some are no longer in the army. It is asked as the muster opens,
  before the map's opening sequence (camera, the enemy's arrival, its lines), which waits for the answer: no script
  runs while a popup is up (`activateNextMenu` sets GameScreen+0x1d0, `onTick` skips `updateScriptSequencing`). The
  record's issued force and allies are not part of it; here the Hero's tile is kept too. Not offered in hot-seat, online or Battle Lab runs.
- **Upgrade tree** — the 5010 upgrade slots: Militiamen are the only recruit; every other unit is reached by spending
  a collectible (Armor / Weapons / Beasts / Spirit / Lore / Medal — the string "Medal - Major Victory" heads the
  seven-collectible enum in 5004). Episode II adds Craftsmen, Dune Sirens and Conjurer off the first column, Blood Gorgers
  off Halberdiers, Ballistae off Trebuchet; Sapper and Bodyguard are conjured, never bought. Those five open with the
  Eastern campaign (`UnitSelector::createUnitInfoMenu` @0x8376e and `MenuScreen::onMenuEvent` @0x5d2c2 test the save's
  story bytes): Ballistae after The Wizard's Palace (Zayandi 3), Craftsmen after Warning Caladrin (Sabbi Amar 2), Dune
  Sirens after Caladrin Defense (Sabbi Amar 3), Blood Gorgers after Dune with a View (Abbisin 1), Conjurer after
  Secrets in the Sands (Abbisin 2). Until then the upgrade is listed but refused ("You have not completed the campaign
  mission required to unlock this unit upgrade", 124); the first win shows "Congratulations! The ability to upgrade
  units to … has been unlocked" (800–804). Episode I offers none of them. An upgrade takes any number at once ("Confirm
  the number of units to upgrade", 454; `MenuScreen::handlePopUpEvent` popup 62), one collectible per unit; here one
  tap upgrades one unit (§13). The old
  "weekly levies" were an invention and are gone.
- **The Merchant** (popup 61 "Confirm Purchase", iOS Ep1 @0x3ed2a / Ep2 @0x4ab1c, Android `a_m`) — a collectible costs
  three of one other kind, the player choosing which (a Medal pays too; a Medal can't be bought); a Militiaman costs
  one Armor, one Weapons and one Lore. Any number at once.
- **500 of a kind** — an upgrade or a purchase that would take a unit type or a collectible past 500 is refused:
  "There is a maximum of 500 for units and collectibles." (string 64; Android's port caps at 200).
- **No losses** — the army after a campaign battle or raid is the saved army plus that battle's rewards:
  `GameScreen::createRewardsMenu` (Ep1 @0x192b4 / Ep2 @0x1e08a) reloads the stored counts (`UnitSelector::loadUserArmy`)
  and only adds; `UnitSelector::deleteUnit` is called by Upgrade Army alone. Units slain in battle are lost for good
  only in online battles (help 751 "UNITS LOST"). (The `.mry` file is the player profile that Reset Player deletes.)
- **Kingdoms and unlocks** — `campaign.py` reads `MenuScreen::selectKingdom`: each kingdom has one prerequisite
  (Merovin and Bordavia ← Carrone, Marsur and Sangsoleil ← Merovin, Aguilleon ← Marsur, Hunewold ← Sangsoleil,
  Rukiev ← Hunewold; the same table in Android `a_m.k`). Episode II keeps those rules for the old kingdoms, opens
  Zayandi at start, then Sabbi Amar and Abbisin in sequence (user decision). A kingdom opens once its prerequisite's
  third story battle is won: winning story battle *s* (= 3·kingdom + slot) sets byte *s* of a table in the save
  (`GameScreen::initMenuState` @0x1c8d2 in Episode I, `Context` +0x1c4; Episode II +0x258), and the story battles go
  in order (battle *i* waits on battle *i* − 1).
- **Raids** — they open as the story advances, not one after another (`MenuScreen::initMenuState`, Ep1 @0x45d7e, Ep2
  @0x51ea6 / @0x5201c; Android `a_m`): raid *i* once story battle *i* is won; Carrone's single raid once its third
  story battle is won; in Episode II's Eastern kingdoms raid *i* once story battle *i* + 1 is won. The original hides
  a raid until then; the world map here lists it locked, with the battle that opens it.
- **Training** — Episode I's optional drills (Movement 5800, Combat 5801, Deployment 5802) and Episode II's (Combat,
  Deployment, Combat Training, Advanced Training); Episode II ships no movement drill, so it borrows Episode I's as
  map 5806. Tutorial forces and lines come from the tutorial scenario records 5700–5703; only the reactive "tap here"
  hints are not reproduced. The two drills with a muster bring their own army (`GameScreen::startGameModeCampaign`):
  Deployment two Militiamen, two Footmen and a Pikeman (its 400 points exactly), Episode II's Combat Training part 2
  (5805, the siege half) two Catapults and three Trebuchets. Episode I's unlisted "Tutorial 4" (5803) puts you at the
  head of the Carrone Army (the record's team 1) against the Rebel Army. The Movement drill is the record's goal trigger (tag 9 [7, area 0, cmd 10],
  `checkLocationTriggers`' goal triggers): march the squad from its starting rows into the 3×3 green objective area —
  seven standing in it plays Sir Anston's address, whose last screen leaves the battle; out of its 5 turns, his
  "Perhaps your days as a squire…" (the record's victory sequence) ends it instead.
- **Saves** — progress, upgrade deltas and spoils are kept per episode (the originals are separate apps);
  the player's name and heraldry are shared.
- **Elite units** are exactly the types `UnitSelector::placeCurrent` @0x8154a tests before spending an elite slot:
  Wizards (21), Hero (8), Griffon Riders (9), Cannon (25), Ballistae (30), Conjurer (31) — help 826 "TOO MANY ELITES:
  You may only deploy 1 Elite unit per 1000 deployment points". Catapults, trebuchets, knights, cavalry, rangers,
  druids and priests are not elite. A unit type is capped at 500 (help 64).
- **No Hero for hire** — `UnitSelector::loadUserArmy` copies the saved unit counts and adds nothing, so a Hero is
  fielded only when owned (a reward such as Carrone 3 or The Wizard's Palace, or the Knights → Hero Medal upgrade in
  5010); Heroes stack like any unit — there is no one-Hero cap.
- **Kingdom prerequisites** (`MenuScreen::selectKingdom` switch table, kingdom → required kingdom): Episode I
  1←0, 2←1, 3←0, 4←1, 5←2, 6←4, 7←6, kingdom 0 always open; Episode II gates Rukiev (7) on Zayandi (8) in the binary and
  adds 9←8, 10←9 with 0 and 8 always open — the recreation keeps Ep1's rule for Rukiev by the user's decision.
  `selectKingdom` loops 8 hit-rects in Ep1 and 11 in Ep2.

## 9. Sound and music

- **Clips** — all 62 archive entries ship as `audio/orig/snd_NN.mp3`, id-numbered (ids 7–60 are the RIFF WAVs; 0/1/3/4/
  5/6/61 and 36/38 are MP3 loops and stings). Battle music loop = id 6 (`Context::loop(6)`), menu music = id 3; the
  extra ambient tracks after it are ours.
- **Interface** — cursor / unit pick 41 (Ep1 39), menu button and popup 37, deploy place 39 / take back 40, menu
  close 43, turn start 38 (`GameScreen::startTurn`), victory 36, defeat 24 (`activateGameState`).
- **Movement** (`Unit::playMovingSound` @0x64f78, by class): flying 12, foot 19/20 alternating, cavalry 15/16
  alternating, war engine 42, Blood Gorgers 45, Conjurer 46, stag / mount whinny 34; charge start 12 (Griffon) / 15.
  Movement clips are faded out when a short hop ends (ours — the originals are 1–3 s).
- **Melee** — by the weapon struck with (`Unit::changeState`'s weapon switch @0x6b84c): Spear, Pike and Druid Lance
  cycle 27→28→29, every other blade alternates 30/31 (one counter drives both, Context+5160), a Bodyguard's blow 48
  (@0x6bb82), the Blood Gorgers' Bite 47, the Craftsmen's Mallet 49.
- **Shooting** — bow 35 (Fire Arrows too; 23 is the "unit leaves the field" clip `Unit::_executeAction` plays after
  `Map::removeUnit`), musket 21, cannonball 8 + 13 on impact, Grapeshot 9, catapult / trebuchet launch 33, the
  Catapult's rocks land with 25 and the Trebuchet's boulder with 32 (`onTick` @0x781a8, unit type 24), ballista 51 +
  bolt hit 52, hammer throw 50. A direct shot (arrow, musket ball, hammer) lands without a clip.
- **Magic and casts** — Fireball 14 (+13), Ice Shard 18, Lightning Storm 26, spell cast 22 (dome, sand skull,
  Absorb), Heal and Retribution 10, Fear balk 44 (`Unit::attack`), Spirit Shroud 17 (`Unit::curse`), Build/Repair 53,
  Conjure 55, unsummon 54, Sapper blast 56, Teleport out 58 / in 59 (`onTick` states 0x20/0x21), Quicksand 22 + 57
  (`_executeAction` @0x7f750).
- Unassigned ids: 7 (probably the Ice Shard shatter), 60. There is no death sound.

## 10. Animations and effects — resource 5017

- The in-battle animation list (`DataLoader::loadAnimationList`, loaded by `GameScreen::loadStep2` via
  `loadAnimationImages(5017)`): `u16 count; count × u32 len; count × {u16 frameW, u16 frameH, png}`. 88 entries:
  0–51 effects and projectiles, 52–87 dialogue portraits. `tools/ros/anim.py` prints and extracts it.
- Strips are reached through unit+0x2f4 (`[.., #8]`, `#idx × 4`); the cast dispatcher in `Unit::changeState`
  @0x6bd80 stores each strip at unit+0x17a. Ep1 indices = Ep2 − 6 from #16 on and − 9 from #34 on.
- **Unit overlay slots** (set by `changeState`, drawn by `renderOverlay` / `renderDamage`): +0x2fc the projectile,
  +0x300 the impact (drawn on every cell of a blast), +0x304 the mark on a struck unit (drawn with its damage read-out,
  350 ms), +0x308 the state's overlay, +0x30c a second one, +0x2f8 the attacker's own swoosh.
- **Projectiles** #22/#23 arrows — the flaming #23 only when a Fire Arrows unit shoots a Flammable unit, a building or
  the ground (@0x6b8f8) — #24 bullet, #20/#21 hammer, #25 the Catapult's rocks, #27 the Trebuchet's Boulder (the same
  grey rock, startAreaAttack @0x72e70), #28 the Cannonball, #26 Fireball (and the unused Pitch), #29 piercing bolt.
  Ice Field and Lightning Storm fly nothing (state 5).
- **Marks on the struck unit** — a melee blow only: #30 slash for every blade, #32/#33 blood burst (by facing) for the
  Spear, Pike and Druid Lance, nothing for the Mallet and the Bite. A shot leaves no mark (+0x304 is cleared as it
  lands, @0x6b538); a blast puts the slash on the unit it was aimed at.
- **Impacts** (startAreaAttack) — Rocks #34 earth burst, Boulder #36 rock burst, Cannonball #37 fire burst, Fireball and
  Pitch #35 explosion, Piercing Bolt #38; the Grapeshot's muzzle blast #42–#45 by direction; Lightning #47 bolts. A
  structure an area attack brings down raises #12 the dust ring once the impact is over (Map+0x190, @0x79056).
- **Casts and states** #0 shapeshift, #1 teleport, #2 the Fear skull, #3 sparkles — on the HEALED unit for a Heal
  (state 18 is drawn at Map+0x1c, the target) and over a Blood Gorger draining (state 29) — #4/#5 Spirit Shroud spirit,
  #6 dome, #7 Ice Field, #8 sword of light (the Retribution smite), #9 angel, #10 unsummon, #11 pentagram, #12 dust
  ring, #13 debris, #14 sand skull, #15 Absorb flash, #40 the glow on the cells of an aimed Boulder or Cannonball
  (state 7). #30 also plays over a unit that steps into quicksand.
- **Never seen in battle**: #16–#19 the attackers' swooshes (set on every melee blow and charge, but drawn only by the
  army screen's unit preview, `UnitSelector::render`); #41 the burning unit and #39 the burning tiles
  (`Map::burnLocation` waits on Unit+0x80, which neither binary ever sets); #46 swirl. Three Android-only strips (dark
  dome, frost ring, small angel) have no iOS counterpart and are left out.
- **Animations atlas** — every 5017 strip of both episodes, the engine's effect table, the unit attack and walk sheets,
  and every multi-frame sheet of the raw extraction play live at `/ros-atlas/anim.html` (data by
  `tools/ros/animatlas.py`), each labelled with its use and source. The UNUSED ones are flagged: the Android-only dark
  dome (z_005), small frost ring (z_008) and small angel (z_010), the small Android effect strips z_013/z_017/z_029,
  the aim glow z_027 (5017 #40 — the recreation draws its own aim markers), the Android terrain animations and the iOS terrain strips 001/000 whose purpose was never located,
  the six small Android unit strips 000–005, and 5017 #46 (the swirl, referenced by neither binary).
- Unit walk/attack sheets are the Android sheets; idle poses come from the roster atlas (frame = sprite index). Frame
  counts and hit-frame timing are ours.

## 11. Original interface features and where we stand

- **Formation Order** (manual, string 739 "Hold down on a unit you control to issue a Formation order"): the whole
  deployment group moves and attacks by itself — reproduced as the Formation button on all un-moved units.
- **Tactics Path / Set Tactics** per deployment group before battle — in the original, not yet reproduced (a loose
  army-wide version was removed).
- **Help** — the original's 32-section manual ("Tap here for help") is shown verbatim in the Field Manual, in the
  menu and in battle.
- **Two-finger group selection**, the reactive tutorial hints, and online battles (mobilebattles.com) are not
  reproduced.

## 12. Data versus authored — the honest split

- **Real, from the data or binaries**: every unit stat, weapon, armour, ability set, rating and cost; the damage
  matrix and the combat rules of §3; all maps at true size with armies, deploy blocks, marker groups, objectives,
  portals, waves, triggered spawns and lines; mission types and rewards; the campaign structure and unlock graph;
  dialogue text, speakers and portraits; team heraldry bytes, tinctures, charges and frames; the group AI of §7; every
  sound id of §9 and every effect strip of §10; the tutorial battles and their lines.
- **Ours**: the AI's one-pass choice over the tiles a unit can reach and its tie-breaks (§7); frame timings and projectile visuals; the parchment UI, camera and ambient playlist;
  the special win rules pinned from objective text; the kind grouping and ability description prose; the player's
  heraldry ranks; the Ep2 world map keeping the Episode I kingdoms; the two bonus campaigns of Tilicia and Isoluccia,
  with their maps, story, six units and unit art (§13).
- **Open**: the original's wall pathing bound (9999) in `calcShortestPath`. Every deliberate difference from the
  original is listed in §13.

## 13. Deviations from the original

Everything below plays, looks or works differently from the shipped game, on purpose, or is not reproduced. Anything
not on this list is meant to match the binaries — a difference that is not listed here is a bug, please report it.

### Rules that play differently

- **Whole-number HP** (user decision). The original keeps hit points on a 256 scale (Unit+0x190, 100 HP = 256) and
  shows them rounded down, so its badge and its numbers drift a point apart — a +20 heal from 50 lands on 69,
  quicksand reads 5 while the badge drops 4. Here HP is kept in whole points: a blow is the original's damage chain
  (the attacker's HP taken as HP256) rounded to whole HP, at least 1 when it does anything; a Heal or a repair is
  +20, quicksand 5, a Retribution smite 10 (a charge's 20, 29 …), Life Steal 3/2 of the bite rounded. A unit can
  live or die by a point where the original would not.
- **Warning Caladrin's town garrison** (map 5428). The allies a script spawns away from a group marker get no
  GroupLogic and, in the original, march on the nearest foe at once — the town empties long before the escort arrives.
  Here they stay inside the fort (striking a foe at its wall) until one of your units comes out of the last gates.
- **⚙ Realistic siege** (a setting, OFF by default = the original). The original leashes every AI army's units to
  targets within 8 tiles of the point their group marches on (`Unit::isValidFormationTarget`), shooters included: a
  garrison's musketeers and cannons hold fire on what is not near that point (El Acclazar's march out of the south
  gate), and the allied trebuchets there step sideways instead of shooting. With the setting on, an AI shooter —
  allied or enemy — takes any target in range. It makes walled maps far harder: in the map runner El Acclazar falls
  from 12 of 18 Autopilot wins to 0, Siege of Corbeau from 5 to 0; campaign wins overall drop by about a tenth.
- **A walled-off nearest foe.** `getClosestEnemy` is straight-line, so a melee unit beside an impassable wall picks a foe
  on the far side and stands pinned (The Wizard's Palace). Here a melee walker that cannot walk to it takes the foe
  nearest by real travel, through the portal its walk needs.
- **No rocking behind rocks.** Where the original's A* (bounded at 2 × move) leaves a unit stepping back and forth beside
  a rock ring or a corridor, the reachable tile nearest by real travel is taken; on open ground nothing changes.
- **An allied group whose target cannot be reached** marches on the reachable tile nearest it, instead of the end of
  A*'s partial path (which can lead away and freeze the group).
- **Online battles are ours** (user decision). The original's head-to-head ran on Punch Entertainment's servers, long
  gone. Here two signed-in players meet in a lobby (optional password) on a skirmish map and fight the hot-seat battle
  across two devices: each musters only their own army, every move is shown live on the other screen, each turn has a
  clock (out of time, the turn ends by itself; a player who has left can be beaten on time), and the result moves a
  per-episode Elo rating (the leaderboard). The battle's creator sets the gold (the map's, one amount, or each side's
  own points and Medals) and who moves first (coin toss, either player, or the map's order), as in hot-seat.
- **Armies travel between the episodes** (user decision). The originals are separate apps; here ⚙ Settings exports an
  army and its collectibles to a file the other episode imports — up to 6 of each unit and 30 in all, 3 of each
  collectible and 1 Medal, Episode II's own units reaching Episode I as the unit they upgrade from. Battles won stay
  behind, and a new import replaces the last.
- **Episode II opens on Episode I's intro** (user decision). Entering its campaign plays the "Much of the known world"
  intro its archive still carries; its own intro plays before the first battle of the Eastern Kingdoms.
- **No shapeshifting over water or cliffs in Episode II either** (user decision). Episode I's menu and both
  episodes' AI refuse a shift there; Episode II's rebuilt player menu shows no such check, so it may have let a Great
  Eagle turn into a Druid standing on water.
- **Both diagonals line up a charge** (user decision). The AI's charge staging (`Unit::isValidChargePath`) accepts a
  diagonal lane only when dx = dy, refusing the other diagonal — a slip for |dx| = |dy| (the charge itself takes
  both). Here the AI lines up along either diagonal.
- **⚡ Auto-charge** (a setting, ON by default — user decision; OFF = the original). In the original the charge bonus
  (+30, no counter, riding on through the foot it cuts down) comes only from the Charge action: `Unit::charge`
  (@0x6bfe6) is the one place that sets the charging flag (Unit+0xb4, read by `calculateAttackDamage`), and only
  `_executeAction`'s action 13 calls it — given by the AI's charge state 13 or the player's Charge menu entry; an
  ordinary move or attack clears the flag. With the setting on, a player's rider that has galloped 2+ tiles in a
  straight line charges the foe directly ahead with whatever strike comes next — moving first and striking after,
  or a tap on the foe, which gallops to the launch tile by itself. With it off, a tap on a foe is an ordinary approach
  and blow, and the ⚡ Charge button on the unit card (the original's Charge entry: offered before the rider moves,
  while some foe has a clear lane) highlights the foes it can charge — a tap on one gallops and strikes as one action.
  The setting applies at once; an online battle always plays it on. The AI (enemies, allies, the Autopilot, scripted
  moves) always charges as in the original, by its own charge choice only.
- **A newly built village starts whole.** The original keeps the cell's worn structure HP, so a hamlet raised on ground
  fought over earlier falls to two blows.
- **Story missions reward their first win only.** The original computes the first-win flag and `createRewardsMenu`
  ignores it, paying every win; raids still pay every win here.
- **The bottom-left and bottom-right corner tiles are passable.** `Map::getMoveCost` blocks them outside one screen mode
  — the iPhone's softkeys sit there.
- **Episode I Pike Wall +30.** Given when a braced pikeman strikes a cavalry or war-engine attacker; the original gives it
  when the struck unit is charging.
- **Dice.** The recreation rolls its own seeded generator, not `mlib_Random::getRandom`: every chance matches (courage,
  deviation, the Lightning Storm's start), the sequence of rolls does not. Each battle and each retry gets a fresh seed
  (online battles share theirs, Battle Lab runs keep theirs), and only the rules draw from it — the look-only effects
  (bursts, smoke, a bolt's zigzag, a unit's idle bob) don't, so the dice never depend on what is drawn.

### On screen, not in the original

- Damage forecasts on every target and area cell (the original shows the damage of the one tapped target), the odds of
  keeping one's nerve against a Fear unit, "may deviate X %" warnings, structure HP bars, the charge banner, the
  "Courage!" cue on a passed roll, fast-forward.
- **One upgrade per tap** (user decision). The original's Upgrade asks for the number of units first (popup 62, "Confirm
  the number of units to upgrade"); here each tap of an upgrade turns one unit, for one collectible — three taps, three
  units. The Merchant keeps its number picker.
- A unit struck by a shot (arrow, bolt, ball, hammer) or caught in a blast shows the blood burst; the original marks
  only melee blows (and puts its slash on the unit a blast was aimed at).
- The musket's muzzle flash (the original keeps that blast for the Grapeshot), the blue sparkle as a Wizard casts, the
  bolt that carries an Ice Field (the frost simply appears on the target in the original), and the flames a Fireball
  leaves behind.
- The prose of unit, status and ability descriptions; the kind grouping; the parchment interface and its phone layout;
  the camera; the ambient playlist; Russian and Ukrainian translations; frame timings and projectile visuals; the
  higher-resolution Android sprite sheets where both sets exist.

### Added modes and content

- **Hot-seat** — two players on one device, in place of the original's online head-to-head; it plays the original rules
  (for instance only the map's player side conquers areas).
- **Battle Lab** — batch simulations, autopilot strategies and same-seed replays.
- Raid medal tracking on the world map; the raid titles (the original names them only "Hunewold Raid 1"…); the
  player's heraldry ranks; the Story Codex, the downloads and the map and animation atlases.

### The bonus campaigns: thirteen regions after Episode II (Episode II only)

Thirteen fan-made campaigns, entirely ours (user decision). Nothing in this section comes from the original games; it is
kept apart from the original data so that everything else stays checkable against the binaries.

- **Where it lives.** `bonus.json` (built by `tools/ros/bonus/build_bonus.py` from the hand-written level files
  beside it) holds the thirteen regions, their 39 story battles and 28 raids (map ids 5964-5968 Thalassar, 5973-5977 Brasshaven,
  5984-5988 the Amber Reach — see "The three factions" below — and 5902-5913 Tilicia, 5914-5918 Jarnheim,
  5924-5933 Isoluccia, 5934-5938 Khemret, 5941-5952 Mare Nostra, 5944-5948 Moananui, 5954-5958 Coatlan, 5961-5972
  Satoshi, 5981-5992 the Mirror Sea, 5994-5998 Tezcal), rewards, hold tiles and heraldry, in the same record shapes as the exported files. It is loaded beside
  `levels.json`, `campaign.json` and `rewards.json`, which are not edited. The units are in
  `src/reign-of-swords/data/bonus-units.js`, merged into the unit tables at load; their rules are marked `BONUS` in
  the code. Their sprites are cut from art sheets supplied for this project
  (`tools/ros/bonus/art/`, sliced and given team colours by `import_sheet.py`); the six ability icons were drawn
  for it (`draw_units.py`).
- **Story.** They follow Episode II's last line (the letters naming Tilicia, Isoluccia and the "Battlemage"). The
  maps reuse the Episode II tileset, the speakers reuse its portraits, and every battle runs on the original scenario
  script (round, kill, tile, escape and escort triggers), with no new script commands.
- **Opening.** The kingdoms appear on the Episode II world map, marked "Bonus campaign", once Oasis Standoff is won.
  Tilicia opens first, then Isoluccia, then Mare Nostra (the five ship battles first built as "the Mirror Sea";
  renamed by user decision, its marker in Mare Nostra); Satoshi (the top-right corner) and the Mirror Sea (a second
  naval campaign, its marker on the northern sea under the map's own "Mirror Sea" label) both open after Mare Nostra. Until then nothing of them shows: not the kingdoms, the units, their
  Field Manual entries or their upgrade branches. Episode I never has them, and no bonus unit appears in an original
  battle, raid or battlefield.
- **Twenty-four units** (and the Hounds and Imps two of them call), each on the damage row of an original weapon and an original armour column (§2), so the real
  weapon x armour table prices them:

  | Unit | Move | Weapon (row) | Armour column | Rating | Cost | Abilities |
  |---|---|---|---|---|---|---|
  | Cragsmen | 4, skirmish | Javelin 2-3 (Spear), Spear | Light | 2 | 175 | Climb, Shoot and Move |
  | Spellwardens | 3, formation | Mace (Sword) | Heavy & Shield | 3 | 225 | Nullify, Mending Runes, Formation |
  | Stone Sentinel | 4, formation | Stone Fist (Greatsword) | Heavy & Shield, shown as Living Stone | 4 | 300 | Bulwark, Unyielding, Fear, Fearless |
  | Marines | 4, skirmish | Boarding Musket 2-3 (Musket), Sword | Light & Shield | 3 | 150 | Amphibious, Grapple, Breach, Move or Shoot |
  | Pavisiers | 4, formation | Crossbow, Short Sword | Breastplate | 2 | 200 | Pavise, Formation, Move or Shoot |
  | Battlemage | 4, teleport | Chain Lightning 2-7 (Fireball), Runesword | Relic | 3 | 750, elite | Chain Lightning, Teleport, Shoot and Move, First Strike, Battle Standard, Fear |
  | Gladiators | 4, skirmish | Gladius (Sword) | Heavy & Shield (-10 taken) | 3 | 175 | Whirl |
  | Samurai | 4, formation | Katana (Sword, +10) | Heavy (-10 taken) | 3 | 250 | Lesser Shroud, Pike Wall |
  | Dragon Riders | 8, flying | Dragonfire 2-8 (Cannonball), Lance | Relic | 5 | 750, elite | Dragonfire, Fire and Lance, First Strike, Fear, Charge |
  | Beast Master | 4, formation | Whip (Spear) | Shield | 1 | 250 | Call Hounds |
  | Hounds (called) | 7, skirmish | Fangs (Antlers) | Nature's Cloak | 2 | - | leashed, as the Conjurer's minions |
  | Sohei | 4, formation | Naginata (Halberd, +5) | Holy Vestment | 4 | 175 | Sutra, Fearless |
  | Shinobi | 5, skirmish | Shuriken 2-3 (Spear), Ninjato | Light | 3 | 225 | Shadow, Stealth |
  | Oni | 3, formation | Kanabo (Greatsword) | Heavy, shown as Oni Hide | 4 | 350 | Earthshaker, Fear, Fearless |
  | Tengu | 7, flying | Gale Blade (Sword, +20) | Feathered Hide (-10 taken) | 5 | 325 | Gale |
  | Alchemist | 4, formation | Acid Flask 2-6 (Fireball), Dagger | Holy Vestment | 3 | 250 | Acid Flask, Elixir, Summon Imp |
  | Imp (summoned) | 6, flying | Claws (Short Sword) | Minor Ward | 2 | - | leashed, as the Conjurer's minions |
  | Golem | 3, formation | Rune Fists (Greatsword) | Heavy & Shield, shown as Rune Stone | 4 | 400 | Stoneskin, Unyielding, Fear, Fearless |
  | Unicorn | 7, flying | Starlight 2-4 (Lightning Storm), Antlers | Feathered Hide | 3 | 275 | Purity |
  | Efreet | 5, flying | Flame Jet 2-4 (Fireball, with its + cross), Burning Hands | Feathered Hide (-10 taken), shown as Living Flame | 5 | 350 | Burning Aura (20), Fear |
  | Naga | 5, skirmish | Twin Scimitars (Sword, +10) | Heavy & Shield (-10 taken) | 5 | 300 | Constrict, Whirl, Amphibious |
  | Skeletons | 4, formation | Rusted Sword (Sword, +10) | Heavy & Shield (-10 taken) | 5 | 500 | Rise Again (at full HP), Fearless |
  | Jaguar Warriors | 5, skirmish | Macuahuitl (Sword) | Light & Shield (-5 taken) | 3 | 150 | Jungle Stride, Pounce |
  | Eagle Warriors | 5, skirmish | Atlatl Dart 2-3 (Spear), Macuahuitl | Light | 2 | 175 | Jungle Stride, Eagle Eye, Shoot and Move |
  | Sun Priest | 4, formation | Sunbeam 2-7 (Fireball, +30), Obsidian Knife | Holy Vestment | 4 | 400, elite | Sun Magic |
  | Feathered Serpent | 7, flying | Gale 2-4 (Lightning Storm, +10), Fangs | Feathered Hide | 4 | 300 | Tailwind, Shoot and Move |

- **Four more cultures, eight tokens and the Primal Warden** (the fifth wave; all art supplied by the user).
  *Regions.* Jarnheim (Norse; map ids 5914-5918), Khemret (Egyptian; 5934-5938), Moananui (Polynesian; 5944-5948)
  and Coatlan (a second Aztec region; 5954-5958), three story battles and two raids each. All four open with the
  bonus campaigns (the rule Tilicia has) and are nobody's prerequisite. Markers: Jarnheim in the northern range
  between Hunewold and Rukiev, Khemret on the east bank of the south-east river, Moananui on the island chain west of
  Mare Nostra, Coatlan in the eastern mountains south-east of Tilicia. That makes ten bonus regions, 30 story battles
  and 22 raids.
  *Units* (cost; ability): Berserkers 175 (Rage: +1 on the cell per 2 HP lost; Fearless), Shieldmaidens 200 (Shield
  Wall: a friend beside one takes a quarter less hand to hand), Einherjar 275 (Chosen of the Slain: +50 HP for each
  foe struck down), Jotunn 425 (Frost Slam: its target and the foes beside it move at half pace until their next turn
  ends; Fear); Medjay 175 (Composite Bow 2-7; Desert Stride: terrain types 3, 22, 27, 28 cost 1), Khopesh Warriors
  175 (Shield Hook: the target's armour column is read without its shield, 1 to 0, 6 to 3, 10 to 8), Anubis Priest
  275 (Soulfire 2-6, +1 on the cell per 3 HP the target has lost; magic), Ammit 275 (Devourer: a bite that leaves a
  foe at 20 HP or fewer kills it, war engines excepted; Fear); Toa Warriors 150 (First Thrust: +20 at a foe at full
  health; shallows cost 1), Tahuanui Riders 250 (flier; Sky Hunter: +25 against war engines and units with a ranged
  weapon), Tohunga 250 (Spirit Wisps 2-5; Karakia: at the start of its side's turn the most wounded friend within 3
  tiles mends 15 HP), Taniwha 375 (deep water and shallows cost 1 and it attacks from them; +20 from water; Fear);
  Coatecpatl Warriors 200 (Serpent Venom: the flask's acid, 5 HP for 3 turns; Jungle Stride), Ahuizotl 175
  (Drowning Grasp: the foe it strikes has no targets on its next turn; Amphibious), Cuahchic Chieftain 275 (war
  darts 2-4, Shoot and Move, Battle Standard; Vanguard: a friend beside it counts as having First Strike),
  Tzitzimitl 250 (flier; Starfire 2-5, half its damage returns as health; Fear; magic).
  *The Primal Warden* (a design supplied by the user; 400, elite): Druids + Void. A healer (20 HP at 2 tiles, which
  also lifts acid, chill, blindness and holds) with a Prism Bolt (2-4), that shapeshifts by the Druid's rule (one
  shift a turn, HP kept, not over water or cliffs) into the Storm-Stalker Panther (move 8; Static Arc 2-3, Shoot and
  Move), the Volcanic Siege-Tortoise (move 2; Magma Mortar 2-5 on the 3 x 3 around its target at 100% / 60%, friend
  or foe, never at a tile beside it, where it has only a Bite; everything but magic does half damage to it) or the
  Astral Manta (flier; Void Beam 1-4, which goes on through three tiles beyond its target at full strength, friend
  or foe). The computer picks the Panther where a Druid would take the Stag, the Tortoise for the Bear, the Manta for
  the Eagle.
  *Tokens.* Eight new collectibles, one per culture: Glacial Bloodstone (Jarnheim), Scarab of the Duat (Khemret),
  Smoldering Obsidian (Coatlan), Carved Whalebone (Moananui), Triton's Anchor (Mare Nostra and the Mirror Sea),
  Tsuba of the Shogunate (Satoshi), Sacred Jade Jaguar (Tezcal) and Void Rift Crystal (Tilicia and Isoluccia). Every
  battle and raid of a region rewards 2 of its token (The Harbour Chain also 2 Anchors and The Admiral's Deck 1 Void
  Crystal, for the units they open). They are spent like any collectible, one a unit, but the Merchant does not
  trade them, and the camp shows them once the bonus campaigns are open. Upgrades paid in tokens: Anchor: Militia
  to Marines, Footmen to Gladiators, Raiders to Beast Master. Tsuba: Shamans to Sohei, Footmen to Samurai, Archers to
  Shinobi, Samurai to Oni, Beast Master to Tengu. Void: Griffon Riders to Dragon Riders, Priests to Alchemist, Stone
  Sentinel to Golem, Druids to Primal Warden. Jade: Militia to Jaguar Warriors, Archers to Eagle Warriors, Cavalry to
  Feathered Serpent, Shamans to Sun Priest. Bloodstone: Militia to Berserkers, Footmen to Shieldmaidens,
  Shieldmaidens to Einherjar, Berserkers to Jotunn. Scarab: Archers to Medjay, Militia to Khopesh Warriors, Priests
  to Anubis Priest, Blood Gorgers to Ammit. Whalebone: Militia to Toa, Raiders to Tahuanui Riders, Shamans to
  Tohunga, Dune Sirens to Taniwha. Obsidian: Jaguar Warriors to Coatecpatl, Blood Gorgers to Ahuizotl, Eagle
  Warriors to Cuahchic Chieftain, Shamans to Tzitzimitl. Cragsmen, Spellwardens, Stone Sentinel, Pavisiers and the
  Battlemage keep the original collectibles. The tokens give a unit a branch per culture beside its six original
  slots, start each culture from the Militia or another early unit, and exist only after Episode II is won, so no
  bonus unit can be taken back into the original campaigns before they are finished. (Paths written elsewhere in
  this section with original collectibles for these units are superseded by this list.)
  *Balance.* `docs/unit-balance.md` holds the arena's present numbers for every unit, original ones included; its
  "original finals" test (the last battle of each original kingdom fought with an army of the unit) was added to
  catch units that would steamroll the original game, and the Battlemage (range 2-6, +5 on its bolts), Gladiators,
  Tengu, Tohunga, Medjay and the Chieftain were reduced after it.
- **Tilicia and Isoluccia are three battles each** (user decision; they were built with six). Every battle of
  the two regions is now fought with an army the player deploys: the fixed-force battles (The Tolm Road, The Sleepers
  Wake, Landfall, Free Company) are gone, with The Sealed Vale and The Causeway. Tilicia is Ostrak's Bargain,
  Frostgate, The Empty Tomb (5902, 5904, 5906); Isoluccia is The Harbour Chain, The Arsenal, Reign of the Battlemage
  (5924-5926). The Marines' upgrade now opens after The Harbour Chain and the Golem's after the Quarry of Giants raid.
  With three battles and three raids, a bonus region's last raid opens with its last battle (`raidGate`; the
  original kingdoms keep the original rule).
- **Hidden for now** (user decision): the Unicorn, Efreet, Naga and Skeletons. Their data, rules, art and tests
  stay (`BONUS_HIDDEN` in `data/bonus-units.js`), but the game offers none of them: no camp or Field Manual card, no
  upgrade branch, no reward, no place in any battle or in the veteran army. What is written of them below describes
  the units as built.
- **Tezcal and the upgrade rule** (the fourth wave; art supplied by the user). A sixth region, the Jungles of
  Tezcal (map ids 5994-5998: three story battles, two raids), opens after the Mirror Sea; its marker is east of the
  Mirror Sea, between Satoshi and Tilicia. *Jungle Stride* (Jaguar and Eagle Warriors): woods (terrain types 4, 28)
  cost 1. *Pounce* (Jaguar): +20 on the cell of a blow struck from woods, tall grass, scrub or rocks (types 3, 4, 22,
  27, 28). *Eagle Eye*: an Eagle Warrior's dart counts its target's tile cover as none. *Sun Magic* (Sun Priest, the
  Wizard's counterpart): Sunbeam, its attack, is the Fireball's row +30 on one target and burns on through the two
  tiles beyond it (60% then 35%, the Dragonfire's line), and Nullify stops it; Dawn mends every friend within 2 tiles
  by 15 HP (not war engines or Stone Sentinels); Eclipse blinds a foe within 5 tiles, halving every blow it deals
  until its own next turn ends. The computer casts only Sunbeam. *Tailwind* (Feathered Serpent): a friend beside it
  has 1 more movement. Upgrades: Pikemen + Beasts to Jaguar Warriors (Tezcal 1), Archers + Lore to Eagle Warriors
  (Tezcal 2), Cavalry + Spirit to Feathered Serpent and Priests + Medal to Sun Priest (Tezcal 3).
  *The Beast Master's tree* (user decision): Unicorn (Lore), Efreet (Weapons), Naga (Beasts) and Skeletons (Armor)
  are now upgraded from the Beast Master, beside the Tengu (Spirit); their unlock battles are unchanged.
  *An upgrade beats its base* (user decision): six of a unit must beat six of the unit it is upgraded from, one for
  one (the arena's `upgrade` duel, the mean of both sides and two dice seeds). To pass it Marines, Skeletons, Naga,
  Efreet, Tengu, Jaguar Warriors, the Feathered Serpent and Sohei were strengthened and re-priced (the table above
  has their present numbers); the four made from a Beast Master had to outfight a master and its two packs of Hounds,
  which is why Skeletons are now a 500-point unit that rises at full health.
- **Stone Sentinel and Pavisiers, improved** (user decision, from the arena's battle types). The Sentinel no
  longer strikes last and has *Bulwark* (the Golem too): a charge adds nothing against it, the flank bonus is not
  applied against it, and a Tengu's Gale does not move it; it costs 300. A planted *Pavise* now also takes a quarter
  off every blow hand to hand (not with Siege Armor), and the Pavisiers' own shots from a planted pavise add 10 to
  the Crossbow's cell.
- **The laboratory and its creatures** (the third wave; art supplied by the user, its Gryphon Rider row unused).
  *Acid Flask* (Alchemist): a Fireball in everything but colour, the same + cross at 100% / 60% on friend and foe,
  flying and bursting green; every unit it burns (not war engines) carries acid, 5 HP at the start of each of its
  side's next 3 turns, a fresh flask restarting the count. Point-blank the Alchemist uses its Dagger, with no burst.
  *Elixir*: the Priest's Heal with its own numbers, 30 HP on the shown HP at up to 2 tiles. *Summon Imp*: the
  Conjurer's Conjure with one summon, as the Beast Master's Hounds. *Stoneskin* (Golem): a blow's damage is capped at
  20 HP after every other rule. *Purity* (Unicorn): a unit within 2 tiles of a friendly Unicorn passes every Fear
  check and loses its acid at the start of its turn. *Burning Aura* (Efreet): a unit that begins its side's turn
  beside an enemy Efreet loses 10 HP. *Constrict* (Naga): the unit it strikes hand to hand (not a war engine) has a
  move of 0 until its own next turn ends. *Rise Again* (Skeletons): the first time its HP reaches 0 it is set to 40
  instead. Upgrades: Priests + Lore to Alchemist (after Isoluccia 2), Stone Sentinel + Armor to Golem (the Quarry of Giants raid),
  Knights + Spirit to Unicorn (Satoshi's first raid), Dune Sirens + Lore to Efreet (the Mirror Sea 3), Marines +
  Beasts to Naga (the Mirror Sea 1), Conjurer + Spirit to Skeletons (hidden); each of those battles fields the
  creature and rewards one.
- **More abilities** (added with the later units). *Grapple* (Marines): once a battle, in place of the move, a swing
  to any free tile within 6 that the Marines could stand on (no step rule, so a rampart will do; not deep water),
  played as the Wizard's blink; it cannot be undone and the computer does not use it. *Breach* (Marines): the tile
  cover of a fortification (terrain types 6, 8, 10, 12, 14, 16) counts as none against their blows and shots. *Call
  Hounds* (Beast Master): the Conjurer's Conjure with one summon, Hounds; the cap of two, the 8-tile leash, the turn
  of arrival and the death of the pack with its master are the Conjurer's rules unchanged. Upgrade: Militia + Medal,
  after the Mirror Sea's second battle. *Sutra* (Sohei): at the start of its side's turn every friendly unit
  orthogonally beside a Sohei mends 10 HP with the village heal (not war engines or Stone Sentinels). *Shadow*
  (Shinobi): Stealth that hides on any ground, not only in cover; a turn begun in hiding makes its blows that turn an
  ambush, +30 on the weapon x armour cell. *Earthshaker* (Oni): every other enemy adjacent to its melee target takes
  half the blow. *Gale* (Tengu): its melee target is moved one tile straight back if that tile is free and ground it
  could stand on (war engines never), before the counter-attack is judged, so a thrown foe does not strike back.
  Gladiators now wear the Heavy & Shield column with a further 10 off every cell (the Samurai's rule), at 175.
  Upgrades of the Satoshi four: Shamans + Armor to Sohei, Rangers + Lore to Shinobi, Greatswordsmen + Spirit to
  Oni, and Beast Master + Spirit to Tengu (the only bonus unit upgraded from another bonus unit).
  DELIBERATE FIX found with the Shinobi: a move cut short beside a hidden foe no longer stops on a tile another unit
  holds (a flier over a friend); it stops on the next free tile.
- **Eight abilities.** *Whirl* (Gladiators): after its blow lands on an adjacent target, every other enemy adjacent
  to the Gladiators takes 3/4 of the same blow. *Lesser Shroud* (Samurai): the Shaman's Spirit Shroud with a reach of
  2 tiles instead of 4, raised the same way. *Mending Runes* (Spellwardens): +10 HP at the start of each of their
  turns, with the village heal. The *Boarding Musket* reaches 3 tiles, but only 2 when the Marines stand in woods,
  tall grass, scrub, rocky ground or shallows (terrain types 3, 4, 5, 22, 27, 28). *Master Swordsman* (Samurai): +10
  on the weapon x armour cell of every blow dealt, -10 on every blow taken (never below 1). *Dragonfire*: a fire weapon on the Cannonball's row that also reaches fliers, at 2-8 tiles, drawn as
  a fireball; it obeys cover like any shot, unlike the Cannonball, and burns on through the two tiles beyond its
  target (60% then 35%, friend or foe, structures too) along the line the Ballistae's bolt would take. *Fire and
  Lance*: each turn the Dragon Rider has one breath, one lance blow and its move, in any order. A tap on a foe it can
  reach flies in and strikes with the lance (a charge when the lane allows); the Dragonfire button breathes instead.
  The computer treats it as a melee unit, so it closes in, and follows one attack with the other when a foe is in reach of it. The Battlemage's Teleport is the Wizard's. *Climb*: cliffs (terrain type 21) cost 2. *Amphibious*: deep water (type 19) costs 2, and no
  attack from a deep-water tile. *Nullify*: a unit within 2 tiles (Manhattan) of a living Spellwarden of its side
  takes 0 from enemy Fireball, Lightning Storm, Ice Field and Chain Lightning, is not slowed by an enemy Ice Field,
  ignores an enemy Spirit Shroud and is not stopped or hurt by quicksand. *Unyielding*: no Heal from a Priest, immune
  to quicksand, mended by Craftsmen like a war engine. *Pavise*: Pavisiers that end a turn without moving are planted
  (as are those that have not had a turn yet); while planted, they and a friendly unit next to them and farther from
  the shooter take half ranged damage, the same halving as a Priest's Shield, and the two do not stack. *Chain
  Lightning*: the bolt and every leap add 10 to the Fireball row's cell. After the bolt lands it leaps up to four
  times, each leap from the unit last struck to the nearest enemy not yet struck within 2 tiles of it (the weakest on
  a tie; hidden units and friends are passed over), at 50%, 40%, 30% and 20% of a full bolt on that unit. (First
  built as two leaps at half strength onto enemies beside the target; lengthened and strengthened by user decision.
  In the unit arena this puts the Battlemage well above every other unit for its points.)
  The AI needs no new behaviour: all six act through the movement costs, target lists and damage it already reads.
- **Upgrades.** Each unit hangs off an original unit in a collectible slot that unit leaves empty, and waits on a
  bonus battle like Episode II's own units: Archers to Cragsmen (Armor, Ostrak's Bargain), Swordsmen to Spellwardens
  (Lore, Frostgate), Craftsmen to Stone Sentinel (Spirit, The Empty Tomb), Footmen to Marines (Spirit, The Harbour Chain),
  Crossbowmen to Pavisiers (Armor, The Harbour Chain), Wizards to Battlemage (Medal, Reign of the Battlemage),
  Halberdiers to Gladiators (Weapons, The Lashed Convoy), Swordsmen to Samurai (Spirit, Ishiro's Hill), Griffon
  Riders to Dragon Riders (Medal, The Admiral's Deck).
- **Ships.** The Mirror Sea's battles are fought on hulls lashed together. There is no ship art: a hull is the
  Episode II paving tiles laid on open sea, the obelisk as a mast and the house as a cabin, joined by gangplanks. Where a deck meets the sea it carries a
  wooden bulwark (the sand set's timber wall, by user decision): troops man it from the deck and are covered there
  as on any rampart, horse and war engines keep to the planking, and Marines climb it straight out of the water
  (Amphibious waives the wall-walk step rule). Gangplanks and the stem stay open deck.
- **Unit arena and stress run** (`npm run e2e:arena`, `npm run e2e:stress`). Balance tools, not game content: the
  arena fights equal-points squads of each unit against a basket of fourteen original units on an emptied Open
  Field, from both sides and over several dice seeds, and scores the share of points left. It also fights three
  battle types with a 1500-point squad of the unit: the open field against a mounted army, holding the west castle
  of the Obbsin battlefield against a storming party with Catapults (Autopilot "Hold the fort"), and standing behind a
  rank of Pikemen with Archers behind it while the block advances on a mixed army (Autopilot "Advance as one"); the stress run plays the
  bonus battles at random with the player's army swapped for the bonus units, under the fuzzer's invariants.
  The bonus units' costs and the Battlemage's rating were set from the arena so that each scores near the original
  unit it sits beside (Battlemage and Dragon Rider near the Hero).
- **Resume Episode II** (Settings, Episode II only). *From an army file*: reads an Episode II army file back in
  without the transfer limits, marks every original Episode II battle and raid won, and replaces the army and
  collectibles with the file's. *With the veteran army* (for testing): marks every battle of every campaign won, the
  bonus ones included, so all are open to replay, with 8 of every unit and collectible.
- **The website offers Episode II only** (user decision). The page boots straight into Episode II: there is no
  episode switch, an address that still names an episode (`#reign-of-swords`, `#reign-of-swords-2`) lands on
  Episode II and the hash is dropped, and the page's search metadata describes Episode II alone. Episode I is hidden,
  not removed: its data, rules and tests stay in the repository (Episode II draws its sprites and sounds from
  Episode I's folder), and its saves are neither read nor deleted. In Episode II's Settings the Army transfer group
  is the export alone ("Army file", the file Resume Episode II reads back); importing an Episode I army is no longer
  offered there.
- **The page.** The standalone site gives the game the whole window: the page never scrolls, the campaign screen's
  map and army panel scroll on their own. On a desktop window the battle is two columns as tall as the window: the
  battlefield on the left, as large as the window allows, and the mission bar, controls and unit card (or the
  muster roster) in a side column on the right. Phones keep their own layout.

### The three factions and the bonus terrain tiles (Episode II only)

Three more regions, twelve units, three upgrade tokens and nineteen kinds of ground, all ours (designs and art
supplied by the user). Where a design asked for something the engine does not have, the user chose how it plays;
those choices are marked.

- **Where it lives.** The regions are `tools/ros/bonus/thalassar.py`, `brasshaven.py` and `amber_reach.py` (three
  story battles and two raids each, opening with the bonus campaigns beside Tilicia). The units are in
  `data/bonus-units.js` with the rest; their blows are `_factionStrike` and its neighbours in `rules/combat.js`,
  their skills in `rules/abilities.js`. The tiles are `rules/tiles.js`; `tools/ros/bonus/import_tiles.py` cuts their
  art and writes their tables. Tests: `faction-units.test.js`, `bonus-tiles.test.js`.
- **Tokens with a gift.** Abyssal Pearl, Overclocked Mainspring and Amber Catalyst are collectibles like the other
  culture tokens: won two at a time in their region's battles, spent one per unit to make that faction's units, kept
  off the Merchant's counter. Each also names a gift, and every unit made with the token carries it (user decision:
  the faction's own units, not a second upgrade tier):
  - *Crush Depth* (the Trench Brood): the foe a Trench unit strikes is Snared — no movement on its next turn. It is
    the Naga's hold (`_held`), so it ends with the victim's own turn, a blow landed during the victim's turn holds
    nothing, and a Cleansing Touch or a Zen Sand Garden lifts it. War engines and the Immovable are not held.
  - *Overdrive* (the Clockwork Syndicate): a skill armed before the unit acts. When its action ends it takes a
    second full action (move and attack again); when that ends it loses 25 HP, straight off its health. Armed and
    then let down before acting, it costs nothing; a second action never finished is still paid for as the turn
    ends. The computer winds up a unit above half health that has a foe it can strike this turn.
  - *Apex Roar* (the Saurian Exiles): when a Saurian strikes a foe down, every friend within 2 tiles gains +15 on
    its attack rating until the end of its next turn.
- **Twelve units**, each on an original weapon row and armour column like the rest:

  | Unit | Move | Weapon (row) | Armour column | Rating | Cost | Abilities |
  |---|---|---|---|---|---|---|
  | Carapace Scuttler | 3, skirmish | Crusher Claw (Spear) | Heavy & Shield, shown as Carapace | 3 | 225 | Carapace, Amphibious, Crush Depth |
  | Siren Channeler | 5, skirmish | Coral Trident (Spear) | Holy Vestment | 4 | 225 | Lure, Wayfinder, Crush Depth |
  | Brine Hurler | 4, formation | Toxic Coral 3-7 (Rock), Short Sword | Breastplate | 3 | 250 | Flooded Ground, Move or Shoot, Crush Depth |
  | Trench Behemoth | 4, formation | Sweeping Bite (Halberd) | Heavy (-10 taken), shown as Shark Hide | 5 | 500, elite | Sweeping Bite, Immovable, Lurker of the Deep, Fear, Crush Depth |
  | Brass Phalanx | 3, formation | Piston Mace (Sword) | Heavy & Shield | 4 | 225 | Shield Lock, Formation, Overdrive |
  | Arc Caster | 5, skirmish | Arc Bolt 2-4 (Lightning Storm), Short Sword | Breastplate | 4 | 225 | Chain Arc, Shoot and Move, Overdrive |
  | Caltrop Gyrocopter | 8, flies | Caltrops 2-4 (Short Bow) | Feathered Hide | 3 | 175 | Caltrops, Shoot and Move, Overdrive |
  | Volatile Automaton | 5, formation | Ram (Spear) | Light | 2 | 100 | Volatile, Unyielding, Fearless, Overdrive |
  | Raptor Skirmisher | 7, skirmish | Sickle Claws (Wizard Blade) | Light | 4 | 200 | Pack Hunter, Apex Roar |
  | Ankylosaur Juggernaut | 3, formation | Tail Club (Sword) | Heavy & Shield (-10 taken), shown as Spiked Shell | 3 | 325 | Spiked Shell, Apex Roar |
  | Pterosaur Bombardier | 7, flies | Dropped Stone 2-3 (Rock), Talon | Feathered Hide | 4 | 250 | Harvest, Shoot and Move, Apex Roar |
  | Theropod Tyrant | 4, formation | Tyrant Jaws (Greatsword; 120 wood, 90 stone) | Heavy (-15 taken), shown as Tyrant Hide | 5 | 700, elite | Devastation, Fear, Fearless, Apex Roar |

- **Their abilities.**
  - *Carapace* and *Pack Hunter* — **there is no unit facing in the game**, so "the rear" is the original's own
    pincer (user decision): a blow hand to hand while another unit of the attacker's side stands directly opposite
    (the +30 case of the flank bonus). The Scuttler's shell turns 40% of every other blow; a pincered blow at a
    Scuttler, and any pincered blow by a Raptor, reads the weapon's No Armour column and ignores cover, Formation
    and the -N taken. Nothing reaches the underside of a Bulwark.
  - *Lure* (Siren): a skill in place of her attack, at 2-4 tiles on a visible foe. The foe is dragged up to 2 tiles
    towards her — a step at a time along the longer side of the gap first, onto ground it could stand on, stopping at
    anything in the way — and is Snared. No damage. What it is dragged onto does its work (quicksand, caltrops, the
    tiles below). The design gave her no attack at all; she carries a Coral Trident so that a squad of Sirens can
    finish what it drags in (in the arena a Siren with no weapon lost to the Dune Sirens she is made from). The
    computer sings when her trident can reach nobody this turn.
  - *Flooded Ground* (Brine Hurler): the tile its coral lands on — under a foe or on empty ground — is Flooded for
    the rest of the battle: ground units not of the Trench pay double to enter it and take 20% more damage on it.
    Not on deep water or cliffs.
  - **The Behemoth and the Tyrant occupy one tile** (user decision): the designs' 2x2 body would have needed every
    unit-per-tile assumption in the engine rewritten. They are drawn large, and keep the rest: *Immovable* (no
    Gale, Lure or conveyor moves a Behemoth) and *Sweeping Bite* (the target in full, the foes on either side of
    it across the line of the blow at 75%).
  - *Shield Lock*: a Brass Phalanx beside another takes 30% less from every ranged attack (from any side: no
    facing). *Chain Arc*: the bolt leaps at half strength to one foe beside its target — any, if the target stands
    in shallows, deep water or on a Flooded tile; otherwise only one in Heavy, Heavy & Shield, War Engine or Relic
    armour.
  - *Caltrops*: the tile a Gyrocopter shoots at (a foe's, or empty ground) is strewn for the rest of the battle, by
    side. An enemy ground unit that steps on them stops there (a dead end in its reach, as quicksand) and loses 10
    HP. Fliers and the strewer's own side are not troubled. Any ground unit on or beside the enemy's caltrops can
    spend its action to clear those under and beside it; the computer does so with a unit they stopped that has
    nobody to strike. (The design gave it no attack: its caltrops fall on the Short Bow's row so that the computer
    can use them as a shot.)
  - *Volatile*: when an Automaton falls it bursts on the eight tiles around it, friend or foe, structures too —
    a Boiler Blast (the Fireball's row, a fire weapon) priced as fired by the Automaton at full health. One burst
    can set off the next.
  - *Spiked Shell*: whoever strikes an Ankylosaur hand to hand takes back 30% of the damage done.
  - *Harvest* (Pterosaur): an action that lifts caltrops (either side's), quicksand, a Flooded tile or loose
    boulders from its own tile or one beside it. Its next Dropped Stone falls 25 stronger on the cell, bursts at
    60% on the four tiles around its target (friend or foe), and leaves what it carried there. The designs named a
    Sapper's trap; the game's Sappers lay none, so caltrops stand in. The computer does not harvest.
  - *Devastation* (Tyrant): any structure its jaws close on — a wood, a barricade, a wall, a tower, the Jungle
    Ruins — goes straight to its last stage and stays there. It may attack such a tile directly.
- **Nineteen terrain tiles** (tiles 260-284, terrain types 30-48). Their move costs, cover and healing are rows of
  the same tables the original's terrain uses (`movement.json`); what a table cannot say is in `rules/tiles.js`.
  **The game has no miss chance**, so the designs' "evasion" is a share of the damage (user decision).

  | Tile | Enter (skirmish / formation / cavalry / engine) | What it does |
  |---|---|---|
  | Conveyor Belt | 1 / 1 / 1 / 1 | As each round ends, what stands on it is carried a tile the way it runs — a full belt as one. Not fliers, not the Immovable. |
  | Vent Grate | 1 / 1 / 1 / 1 | No shot can be aimed across it (the tiles the straight line passes through). War engines lob over. |
  | Abyssal Muck | 2 / 2 / 2 / 3 | 25% more from every shot ("evasion to 0"). The Trench Brood pays 1 and is not exposed. |
  | Thermal Chimney | 2 / 2 / 3 / no | 30% less from every shot; 8 HP off its occupant as each of its turns begins. |
  | Tar Pit | 2 / 2 / no / no | A unit on foot stops in it, cannot move on its next turn and takes 10% more damage. Saurians pay 1 and are not held. |
  | Giant Fern Canopy | 2 / 2 / 3 / no | Any unit under it hides as an Ambush unit does: untargetable until a foe steps beside it, and then it strikes first. 10% cover. |
  | Black Ice | 1 / 1 / 1 / 1 | A unit that steps on slides on the way it came, across the ice and onto the first ground beyond; a wall or the map's edge stops it short, another unit costs both 5 HP. |
  | Runic Monolith | no | Every unit on the eight tiles around it mends 5 HP a turn. |
  | Quicksand Sinkhole | 1 / 1 / 1 / 1 | A unit that steps in stops. Its next turn is the climb out: one tile, no attack. Fliers and Dune Sirens are immune. |
  | Mirage Sand | 1 / 1 / 1 / 1 | Half damage from every shot ("+50% evasion"); nothing hand to hand. |
  | Sacrificial Altar Steps | 1 / 1 / 2 / no | Whoever strikes a unit down on them is healed 20 HP. |
  | Overgrown Jungle Ruins | no | A structure of two stages that any weapon damages (at least 30 on the table); it falls to rubble. |
  | Razor Coral | 2 / 3 / 3 / no | Shallows; 5 HP for every tile of it a ground unit crosses. Not the units of Moananui, nor the Trench Brood. |
  | Cenote | 2 / 2 / 2 / no | A move ends here. A unit in one can Dive to any other free cenote, once a turn, as the rest of its move — straight after walking in, or on a later turn. The computer does not dive. |
  | Astral Glyph | 1 / 1 / 1 / 1 | +2 to the reach of a ranged weapon fired from it; 25% more from every shot aimed back. |
  | Chinampa | 2 / 2 / 2 / no | Heals 10 HP a turn (the table's own heal field). |
  | Obsidian Spikes | 2 / 2 / 3 / no | 5 HP for every tile crossed; heavy armour shatters: +10 on every blow but magic at it, for the rest of the battle. |
  | Bamboo Thicket | 2 / 2 / no / no | Troops on foot take 40% less from every shot. Any fire weapon burns the tile to open ash and costs whoever is inside 10 HP. |
  | Zen Sand Garden | 1 / 1 / 1 / 1 | Stepping in clears acid, venom, snares, chill, blindness and shattered armour; a unit in it cannot be dragged or thrown. |

  Five of them came without art and are drawn from the game's own tiles (Vent Grate, Thermal Chimney, Mirage Sand,
  Altar Steps, Jungle Ruins). The rest are the supplied isometric drawings squared up: the top face of each block
  becomes the ground, and what stands on it (a monolith, bamboo, fern tops) is cut out and stood back upright.
- **Where the tiles are.** Thalassar has muck, chimneys and coral; Brasshaven belts and vents; the Amber Reach tar
  and ferns. The older regions' existing maps were re-laid with their cultures' tiles (user decision): Jarnheim ice
  and monoliths, Khemret sinkholes and mirage, Moananui coral, Coatlan altar steps, ruins, chinampas and obsidian,
  Satoshi bamboo and zen gardens. There is no Mayan campaign: its two tiles, the Cenote and the Astral Glyph, went
  to Tezcal (user decision). The map runner rates those thirty battles as before; the Raven Pass musters 250 points
  more to stay where it was.
- **What the computer does not do.** It does not harvest, dive, or avoid a tile for what it does: it walks onto ice,
  tar, caltrops and belts as onto any ground it can cross. The Autopilot plays your side the same way.

### Not reproduced

- Online battles, Rivals, challenges, levies and army upload (mobilebattles.com).
- Two-finger group selection.
- By user decision: the battle autosave ("Your progress is automatically saved at the start of every turn", "AutoSave
  Found"); Set Tactics at the muster (Advance to Destination / Defend Destination / Hold in Reserve, the Tactics Path
  and "Hold Turns — Advance to destination after how many turns?", 121); the one-time tutorial tips ("INVALID
  PLACEMENT…", "NOT ENOUGH POINTS…" and the other reactive hints); the Map Key screen.

## 14. Algorithms, step by step

These are the procedures the game runs, written out in order. Each names the function it was read from; where the
recreation does something different, the difference is stated.

### Turn cycle (`GameScreen::startTurn` @0x276e8, `endTurn` @0x2a1b0, Android `La/g`)

1. The mission holds its groups in scenario order; a cursor walks them 0, 1, 2 … and wraps.
2. When the cursor lands on the player's group the player acts; every other group is played by the AI, each as a
   separate army with its own allies and foes.
3. At the top of every group's turn: its units' acted flags reset, Retribution and Shield cast by that team expire,
   villages and keeps heal units standing on them, its round-triggered waves spawn and its lines fire, and the
   point-concentration layers are rebuilt (`Map::updatePointConcentration` for every team).
4. The round counter advances after the last group; past the turn limit the mission ends (defeat, or victory on a
   "survive" map). Victory is checked after every action: the opposing armies gone, the escape or points condition
   met, and no wave, hidden ambusher or escort still pending.

### Damage of one blow (`Unit::calculateAttackDamage` @0x6af20)

1. Take the attacker's weapon (its side-arm if the target is adjacent and the main weapon is ranged) and the
   defender's armour; `base = WEAPON_DMG[weapon−1][armour]`.
2. If the target flies and the weapon is Boulder or Cannonball, damage is 0; stop.
3. Double it for a fire weapon on a Flammable target; add +30 for a charge (and in Ep1 +30 for a braced pike's
   first strike).
4. Attack rating: the tier value (45…115) + 15 per friendly Standard/Shroud within 4 (once) − 15 for an enemy Shroud
   within 4 + 15 if the attacker's team holds the capture points + 30 per pincer ally for a melee blow.
5. Cover: the tile's defence from the terrain row; Boulder and Cannonball halve the gap to 100; every adjacent
   Formation ally of the defender takes 10 more off the defender's exposure.
6. On the 256 scale, each step truncated: `dmg = ((cover·256/100 · base·256/100) >> 8) · ((rating·256/100 · HP256) >> 8)
   > > 8`. It can be 0 — there is no minimum. The recreation turns it into whole HP: rounded, at least 1 when it is
   anything at all (§13).
7. Halve it if the blow comes from range and the defender is within 2 of its side's Shield mark; ×8/10 up close under
   Siege Armor; 0 if the defender carries Absorb (the buff is consumed). An area cell takes `dmg × share·256/100 >> 8`.
8. Apply, then the structure under the defender takes its own blow (§3).

### Attack resolution (`Unit::attack` @0x7666c, `isFirstStrike`, `charge`, `moveAttack`)

1. Fear check: if the target causes Fear and the attacker is not Fearless, roll courage; a failed roll balks
   (sound 44) and the action is spent.
2. Decide who swings first: a braced Pike Wall or a pikeman against a mounted attacker strikes first; a First Strike
   defender strikes first against an ordinary attacker; a Last Strike attacker swings after the defender; otherwise the
   attacker first. The Hero is never pre-empted.
3. The first striker hits; if the blow is melee, the target is guarded by Retribution and it is the striker's own
   turn, the striker is smitten (about 10 HP, armour ignored); then, if both survive and the target is in reach, it counters. A charge also
   tramples the foot unit directly behind the target with the same blow.
4. Kills add the victim's point value to the killer's team on point missions; Life Steal heals the Gorger 3/2 of its
   bite. A charge that kills its target advances onto the cleared tile, and on to the trampled unit's tile if that
   one died too.

### Courage roll (`Unit::getCourage` @0x66e90, `Unit::attack`)

1. courage = tier value (35/50/65/85/100/125) + the four ±15 modifiers of §3.
2. Draw `random(1000)`; the attacker balks when `draw·256/1000 > courage·256/100`.

### Deviation of a lobbed shot (`Unit::getDeviationChance` @0x665fa, `randomizeAttackLocation` @0x67532)

1. A Barrage weapon (the Catapult) drifts on a flat 35 %; otherwise pick the table by trajectory: Arc (Boulder) or Low
   Arc / any Cannon shot. The Ballistae never deviates.
2. Choose the row by what stands on the target: cover 15/10 %, a flier 100 %, cavalry or wizards 65/50 %, an engine
   25/20 %, anything else 45/35 %.
3. On a hit of the chance, move the impact one tile in a random direction (eight ways), off the board too, and resolve
   whatever is there.

### Movement reach (`Unit::createMoveDestinations` @0x6e450, `Map::getMoveCost` @0x3ba3a)

1. Start from the unit's tile with its move points; explore neighbours (4-way) breadth-first by remaining points.
2. Stepping onto a cell costs its terrain row's value for the unit's class (fly / skirmish / formation / cavalry /
   engine); 0 means 1; 90 or more cannot be entered; ground units may only cross between linked terrain types
   (`isMoveAllowed`); occupied cells cannot be ended on.
3. Wizards instead take every empty tile within Manhattan distance ≤ move whose own cost is affordable (the blink).
4. Portals: entering a source pad the unit's team may use ends the move at the pad and the unit is placed on the first
   free exit cell in the warp search order.

### Charge lane (`Unit::createChargeTargetList` @0x70d78, `isValidChargePath` @0x68d38)

1. For every enemy that is neither hidden nor spent: it must be more than 2 tiles (Manhattan) from the mount's start
   tile and within its move.
2. The line from mount to foe must be straight or exactly diagonal; every tile of it must be empty and affordable
   (diagonal steps cost double); Griffon and Great Eagle skip the terrain test.
3. The AI charges the first foe for which `calcDamageRatio` @0x70054 (its damage versus the expected counter) is
   positive; the player charges by simply moving that lane and striking.

### Group AI per round (`Mission::initAttackPhase` @0x5f812 → `GroupLogic::determineTarget` @0x38bec →

`updateGroup` @0x38c5e)

1. For every group of the acting team: clear the hold-release flags; if the group is in HOLD mode and was hit last
   round but not this one, drop it to ADVANCE.
2. Centre = the mean tile of its members; pace = the slowest member's move (druids count 10); with a hero present the
   hero's move is capped to the pace.
3. Target: HOLD → the group's initial centre (fixed at the first update); ADVANCE → the tile maximising
   `concentration·6 ÷ (distance + 5)` over the map, where concentration is the other side's units (allies count with
   the player) by hp × rating under a 4-wide diamond kernel plus 100 per capture tile that side does not own — for
   allied groups too.
4. The "drop the path when an enemy is within min(pace, 4)" rule only touches a scripted static path, which no record
   sets (the Android port's `a.i.a` is only ever cleared) — so it never fires.
5. Otherwise path = shortest path centre → target for the leader; NEXT = the farthest path point within one pace.
6. Width from the group size; facing = NEXT − centre picks one of the eight slot tables (horizontal, vertical, four
   diagonals); slot 0 is the front-centre and slots fill row by row outward.
7. Slots are filled rank by rank from the per-type table (`updateGroup` @0x38d14): Hero 0, Militiamen 1, Pikemen and
   Greatswordsmen 2, the other foot 3, Priests, Shamans and Craftsmen 4, shooters, Sappers, Bodyguards and Dune
   Sirens 5, riders, Druids and Conjurers 6, Wizards and Catapults 7 — each slot goes to the nearest free member of
   the current rank. Trebuchets, Cannons, Ballistae, fliers, Rangers and Horse Bowmen take no slot and head for NEXT
   itself. A member's move order is NEXT + its slot offset.

### Unit AI, the generic path (`Unit::aiConsiderAction` @0x7bb1c → 0x7d4ea)

1. Find the closest enemy (`getClosestEnemy` @0x65ef8); none → do nothing.
2. If the unit has a group, take its move order (NEXT + slot); a scripted MOVE overrides everything.
3. Build the charge list; if a lane reaches a foe with a positive damage ratio, charge now.
4. Otherwise pick the attack with the best damage ratio among the tiles it can reach, preferring to keep formation
   and cover; with no attack, walk toward the move order, or toward the closest enemy when it has none.
   Every attack is scored by `calcDamageRatio` — a catapult's ordinary attack too; its blast's coverage (foes +, its
   own side −3×) counts only in the area attack before it moves (state 10, `totalAreaAttackDamage`). Only the
   Trebuchet and the Cannon score the expected blow of a drifting shot (@0x70106). (Weighing every reachable tile in
   one pass is the recreation's way of asking "from here, else move and ask again" — see §7.)
   Having moved, the unit looks again from where it stands (`createSortedTargetList` with the moved flag): Move or
   Shoot weapons are out, melee reaches an adjacent foe, and the best attack above −3000 is made.
5. Skills come first for their carriers: a priest moves first (toward the threat, or with its group) or walks up to
   heal the most damaged ally in reach, and having moved prays — Shield when enemy shooters lead, Retribution when
   melee does — or heals an adjacent ally, else casts Shield anyway; Craftsmen mend an engine or build near the front; Dune Sirens lay quicksand across an
   approaching column; Conjurers raise a Sapper or Bodyguard up to two; Sappers detonate beside a cluster; Shamans'
   Shroud rises at the side's turn end.

### Structure damage, repair, build (`Map::applyDamage` @0x7ffa0, `applyRepair` @0x80088, `applyBuildVillage` @0x3f744)

1. Every cell begins at 256 HP. A blow subtracts `((HP256 × skill256) >> 8) × (weapon[material] × 256/100 × share) >> 8`.
2. If the cell was untouched and any damage landed, or its HP fell below 0, it drops one stage
   (`getTransitionTile`); the last stage becomes the razed end tile whose own terrain row now governs movement and cover.
3. Repair adds 20 HP and steps the tile back one stage; Build swaps open ground for the village tile matching the
   ground's tileset.

### Warp exit search (`Unit::getPortalOutput`, `gWarpPositionX/Y` @0x95c38/@0x95ba8)

1. Walk the 72 offsets from the destination pad: the four axis cells at distance 1, the off-axis cells at Manhattan 2
   clockwise from the top-right, then distance 2, 3 … up to 8.
2. The first cell the unit may stand on (`isTileDeployable`) that touches the pad, or from which a path leads back to
   the pad, is the exit; the camera pans there.

### Scenario execution (`Mission::performAction` @0x60b44, `getActionSequence`, `GameScreen::checkLocationTriggers` @0x272c8)

1. Load: factions, teams, unit templates, the side-0 trigger table and action list, markers.
2. Deploy stage: run the tag-1 chain (spawns the fixed forces, camera, lines).
3. Battle start: run the tag-2 chain; then each round, for every round trigger whose round (and counter, in Ep2)
   matches, follow its action chain: spawns join the trigger's team at the top of that team's phase, SCREEN shows a
   line and pauses, MOVE walks a unit, HIDE/SHOW toggle ambushers, REMOVE takes a unit off, COUNTER and SETFLAG update
   state, AIMODE sets a group to hold.
4. After every move check the tile-reached triggers; after every death the unit-lost triggers; on a counter change the
   counter-branch triggers (tag 8). A round trigger gated on a counter (Ep2 `[−1, −1, counter, value, cmd]`) is only
   looked at when a turn begins — `Mission::getSequenceOnTurn`, asked as the "Player Turn Start" / "CPU Turn Start"
   banner closes (`GameScreen::hideCurrentMenu`) — so Zayandi Shores' second ambush comes at the next turn start, not
   the moment the first squad falls.
5. On the end conditions run the tag-4 (victory) or tag-5 (defeat) chain and, on victory, draw the rewards.

### Deployment (`UnitSelector` ctor, `placeCurrent` @0x8154a, `loadUserArmy`)

1. The muster lists the units you own, at their POW cost; the budget is the mission's gold; elite slots = budget / 1000.
2. Placing a unit on a yellow block checks: enough points, the type's count and the 500 cap, and for an elite type a
   free elite slot; placing on your own unit replaces it and refunds its cost.
3. Holding a placed unit repositions it (or, in the original, opens the tactics path for its block); starting with
   100 or more points unspent asks for confirmation (string 103 / 117), starting with nothing placed is refused
   ("ARMY SIZE TOO SMALL"), and the muster is kept for the next battle on that map ("Previous Setup Found").

### Rewards (`GameScreen::createRewardsMenu`, Ep1 @0x192b4 / Ep2 @0x1e08a)

1. Read the record's reward list; if the random flag is set, draw p entries from it at random, else take them all.
2. A token under 100 adds a unit of that 5010 type to the roster; a token of 100 or more adds collectible token−100.

### Quicksand (`Map::setQuickSandTile`, `Unit::considerQuickSand` @0x685ca)

1. The Siren marks the three tiles of the row or column on the chosen side; each gets a countdown of 4 turns.
2. Every turn a unit standing on a marked tile takes the quicksand damage read-out; the countdown decays and the
   whirlpool art (5064) shows while it is above 0.

### Sounds of a fight (`Unit::changeState` @0x6b4e0, `playMovingSound` @0x64f78)

1. Movement plays the class clip and alternates between its two variants on successive moves.
2. A melee strike plays the state's clip: one attack state cycles 27, 28, 29 by a per-context counter; the other
   alternates 30 and 31 (Bodyguard 48); ranged states play their launch clip and the impact clip when the shot lands.
