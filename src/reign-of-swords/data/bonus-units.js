/* ============================================================
   Reign of Swords — the BONUS units (Tilicia & Isoluccia).
   NOT from the original games: the two bonus campaigns and their six units are ours (user decision; MECHANICS.md
   §13). Everything here is authored, so it lives apart from the tables transcribed from record 5010
   (data/combat-data.js) and is merged into them at load. Each unit strikes with the damage row of an ORIGINAL weapon
   and wears an ORIGINAL armour column, so it is priced against the real units by the real weapon × armour table.
   Pure literals — no imports (combat-data and game-data both import this file).
   ============================================================ */

// The six bonus units, in Field Manual order.
export const BONUS_ORDER = ["cragsmen", "spellwardens", "sentinel", "marines", "pavisiers", "battlemage"];

// New weapon ids (the originals end at 34). `row` = the ORIGINAL weapon whose damage row it copies.
export const BONUS_WEAPONS = {
  35: {
    name: "Javelin",
    row: 3, // Spear
    range: [2, 3],
    tags: [8], // Shoot and Move
    desc: "A Javelin is a thrown spear: decent damage at a short distance against all but the heaviest armor.",
  },
  36: {
    name: "Chain Lightning",
    row: 25, // Fireball
    range: [2, 5],
    tags: [7], // Move or Shoot
    desc: "Chain Lightning strikes its target, then leaps to up to two enemies standing next to it at half strength.",
  },
  37: {
    name: "Mace",
    row: 5, // Sword
    range: [1, 1],
    tags: [],
    desc: "A Mace delivers good damage against all armor types, but is less effective against the heaviest armors.",
  },
  38: {
    name: "Stone Fist",
    row: 13, // Greatsword
    range: [1, 1],
    tags: [2], // Last Strike
    desc: "A Stone Fist delivers crushing melee damage, but the Sentinel is slow and strikes last.",
  },
  39: {
    name: "Cutlass",
    row: 5, // Sword
    range: [1, 1],
    tags: [],
    desc: "A Cutlass delivers good damage against all armor types, but is less effective against the heaviest armors.",
  },
};
// The weapons Nullify stops (the three spells and Chain Lightning).
export const MAGIC_WEAPONS = [25, 26, 27, 36];
export const CHAIN_WEAPON = 36;

// Movement class (0 fly · 1 skirmish · 2 formation · 3 cavalry · 4 war engine), as data/combat-data UNIT_AL.
export const BONUS_AL = { cragsmen: 1, spellwardens: 2, sentinel: 2, marines: 1, pavisiers: 2, battlemage: 2 };

// The combat record of each unit, in the shape of data/combat-data UNIT_COMBAT. rating tier → rf 45/60/75/90/100/115.
// Trait flags: climb · nullify · unyielding · amphibious · pavise · chain (the six bonus abilities, rules/bonus.js).
export const BONUS_COMBAT = {
  cragsmen: { move: 4, weapon: 35, weapon2: 3, armour: 3, rating: 2, rf: 75, abilities: [8], climb: true },
  spellwardens: {
    move: 3,
    weapon: 37,
    weapon2: 0,
    armour: 10,
    rating: 3,
    rf: 90,
    abilities: [5],
    formation: true,
    nullify: true,
  },
  // armour 8 = the Heavy Armour column, shown as "Living Stone"
  sentinel: {
    move: 3,
    weapon: 38,
    weapon2: 0,
    armour: 8,
    rating: 3,
    rf: 90,
    abilities: [14, 2, 4],
    lastStrike: true,
    unyielding: true,
    armourName: "Living Stone",
  },
  marines: { move: 4, weapon: 39, weapon2: 0, armour: 6, rating: 2, rf: 75, abilities: [], amphibious: true },
  pavisiers: {
    move: 4,
    weapon: 17,
    weapon2: 8,
    armour: 5,
    rating: 2,
    rf: 75,
    abilities: [5, 7],
    formation: true,
    pavise: true,
  },
  battlemage: {
    move: 4,
    weapon: 36,
    weapon2: 6,
    armour: 15,
    rating: 4,
    rf: 100,
    abilities: [1, 11, 14, 7],
    standard: true,
    chain: true,
  },
};
export const BONUS_COURAGE = { cragsmen: 2, spellwardens: 3, sentinel: 5, marines: 2, pavisiers: 2, battlemage: 5 };
export const BONUS_COST = {
  cragsmen: 150,
  spellwardens: 225,
  sentinel: 350,
  marines: 125,
  pavisiers: 200,
  battlemage: 600,
};
// "You may only deploy 1 Elite unit per 1000 deployment points" — the two heavyweights count as elites.
export const BONUS_ELITE = { sentinel: true, battlemage: true };

// Sprite strips (drawn for this project — tools/ros/bonus/draw_units.py) and the display fallbacks, in the shape of
// data/game-data UNIT_TYPES. A unit with a projectile plays its whole strip for both the shot and the hand-to-hand blow.
const strip = (frames, hitFrame) => ({ frames, frameW: 72, frameH: 72, hitFrame });
const both = (frames, hitFrame) => ({
  ...strip(frames, hitFrame),
  rangedFrom: 0,
  rangedTo: frames - 1,
  rangedHit: hitFrame,
  meleeFrom: 0,
  meleeTo: frames - 1,
});
export const BONUS_TYPES = {
  cragsmen: {
    name: "Cragsmen",
    sprite: "cragsmen",
    ...both(7, 4),
    kind: "ranged",
    projectile: "bolt",
    ability: "Climb — crosses cliffs no other ground unit can. Throws Javelins at 2–3 tiles and may still move.",
  },
  spellwardens: {
    name: "Spellwardens",
    sprite: "spellwardens",
    ...strip(7, 4),
    kind: "melee",
    ability: "Nullify — enemy magic does nothing to units within 2 tiles of a Spellwarden.",
  },
  sentinel: {
    name: "Stone Sentinel",
    sprite: "sentinel",
    ...strip(8, 5),
    kind: "melee",
    ability: "Unyielding — feels no Fear, ignores quicksand, cannot be healed by Priests; Craftsmen can repair it.",
  },
  marines: {
    name: "Marines",
    sprite: "marines",
    ...strip(7, 4),
    kind: "melee",
    ability: "Amphibious — wades through deep water at double cost; cannot attack while standing in it.",
  },
  pavisiers: {
    name: "Pavisiers",
    sprite: "pavisiers",
    ...both(8, 3),
    kind: "ranged",
    projectile: "arrow",
    ability: "Pavise — while it has not moved, it and the ally behind it take half ranged damage.",
  },
  battlemage: {
    name: "Battlemage",
    sprite: "battlemage",
    ...strip(7, 4),
    kind: "ranged",
    ability: "Chain Lightning — strikes its target, then leaps to up to two adjacent enemies at half strength.",
  },
};

// The six bonus abilities as Field Manual / unit-card skills: the trait flag, the name, the description, the icon.
export const BONUS_SKILLS = [
  {
    flag: "climb",
    n: "Climb",
    icon: "skill_climb",
    d: "Moves across cliffs that stop every other ground unit, at 2 movement a tile — and can fight from them.",
  },
  {
    flag: "nullify",
    n: "Nullify",
    icon: "skill_nullify",
    d: "Enemy magic does nothing to any friendly unit within 2 tiles (the Spellwarden included): Fireball, Lightning Storm, Ice Field and Chain Lightning deal no damage and do not slow, an enemy Spirit Shroud saps nothing, and quicksand neither stops nor hurts.",
  },
  {
    flag: "unyielding",
    n: "Unyielding",
    icon: "skill_unyielding",
    d: "Living stone: a Priest's Heal does nothing for it and quicksand neither stops nor hurts it. Craftsmen can Repair it like a war engine.",
  },
  {
    flag: "amphibious",
    n: "Amphibious",
    icon: "skill_amphibious",
    d: "Wades through deep water, at 2 movement a tile. It cannot attack while it stands in deep water.",
  },
  {
    flag: "pavise",
    n: "Pavise",
    icon: "skill_pavise",
    d: "Ends a turn without moving and it plants its pavise: until it next moves, it and any friendly unit standing directly behind it take half damage from ranged attacks.",
  },
  {
    flag: "chain",
    n: "Chain Lightning",
    icon: "skill_chain",
    d: "Its ranged attack (2–5 tiles) hits the target at full strength, then leaps to up to two enemies standing next to the target at half strength.",
  },
];

// UPGRADE ARMY — each bonus unit hangs off an original unit, in a collectible slot that unit leaves empty, and waits
// on a bonus battle (the map id) the way Episode II's own units wait on theirs.
export const BONUS_UPGRADES = [
  { from: "archers", to: "cragsmen", need: "Armor", gate: 5902 }, // Tilicia 2, Ostrak's Bargain
  { from: "swordsmen", to: "spellwardens", need: "Lore", gate: 5904 }, // Tilicia 4, Frostgate
  { from: "craftsmen", to: "sentinel", need: "Spirit", gate: 5906 }, // Tilicia 6, The Empty Tomb
  { from: "footmen", to: "marines", need: "Spirit", gate: 5923 }, // Isoluccia 3, Free Company
  { from: "crossbowmen", to: "pavisiers", need: "Armor", gate: 5924 }, // Isoluccia 4, The Harbour Chain
  { from: "wizards", to: "battlemage", need: "Medal", gate: 5926 }, // Isoluccia 6, Reign of the Battlemage
];

// Camp / Field Manual cards, in the shape of data/shell-data UNIT_META.
export const BONUS_META = {
  cragsmen: {
    role: "Mountain Skirmisher",
    kit: "⚔ Javelin / Spear · 🛡 Light Armor",
    note: "Tilician clansmen who climb cliffs no other soldier can, and throw Javelins from the heights.",
  },
  spellwardens: {
    role: "Anti-magic Infantry",
    kit: "⚔ Mace · 🛡 Heavy Armor & Shield",
    note: "Rune-shielded wardens of the Tilician tombs. Enemy magic does nothing within 2 tiles of them.",
  },
  sentinel: {
    role: "Archaic Construct",
    kit: "⚔ Stone Fist · 🛡 Living Stone",
    note: "A guardian of living stone, raised by archaic magic. Slow and fearsome; it strikes last, and only Craftsmen can mend it.",
  },
  marines: {
    role: "Shore Raider",
    kit: "⚔ Cutlass · 🛡 Light Armor & Shield",
    note: "Isoluccian marines who wade through deep water to strike where no one else can reach.",
  },
  pavisiers: {
    role: "Shielded Crossbow",
    kit: "⚔ Crossbow / Short Sword · 🛡 Breastplate",
    note: "Crossbowmen behind tall pavise shields. Planted, they and the rank behind them shrug off half of all ranged fire.",
  },
  battlemage: {
    role: "War-Sorcerer",
    kit: "⚔ Chain Lightning / Runesword · 🛡 Relic Armor",
    note: "The archaic weapon itself: a war-sorcerer in relic armour whose lightning leaps from foe to foe, and whose presence steadies an army.",
  },
};
// Battle ids of the two bonus kingdoms (story 5901–5906 / 5921–5926, raids 5911–5913 / 5931–5933).
export const isBonusMap = (mapId) => mapId >= 5900 && mapId < 6000;
