/* ============================================================
   Reign of Swords — the BONUS units (Tilicia & Isoluccia).
   NOT from the original games: the two bonus campaigns and their six units are ours (user decision; MECHANICS.md
   §13). Everything here is authored, so it lives apart from the tables transcribed from record 5010
   (data/combat-data.js) and is merged into them at load. Each unit strikes with the damage row of an ORIGINAL weapon
   and wears an ORIGINAL armour column, so it is priced against the real units by the real weapon × armour table.
   Pure literals — no imports (combat-data and game-data both import this file).
   ============================================================ */

// The bonus units, in Field Manual order.
export const BONUS_ORDER = [
  "cragsmen",
  "spellwardens",
  "sentinel",
  "marines",
  "pavisiers",
  "battlemage",
  "gladiator", // Mare Nostra
  "samurai", // Satoshi
  "dragonrider", // Mare Nostra
  "beastmaster", // the Mirror Sea (the second naval campaign)
  "sohei", // Satoshi
  "shinobi",
  "oni",
  "tengu",
  "alchemist", // the laboratory and its creatures (unlocked across the bonus campaigns)
  "golem",
  "unicorn",
  "efreet",
  "naga",
  "skeleton",
  "jaguar", // Tezcal
  "eagle",
  "sunpriest",
  "serpent",
];
// Units a bonus unit calls onto the field: never deployed or owned (the Beast Master's Hounds).
export const BONUS_SUMMONS = ["hounds", "imp"];

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
    range: [2, 7],
    tags: [8], // Shoot and Move
    desc: "Chain Lightning strikes its target, then leaps on through up to four more enemies, each within 2 tiles of the last, weakening as it goes.",
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
    tags: [],
    desc: "A Stone Fist delivers crushing melee damage.",
  },
  39: {
    name: "Boarding Musket",
    row: 18, // Musket
    range: [2, 3],
    tags: [7], // Move or Shoot
    desc: "A Boarding Musket is a short musket for decks and breaches: consistent against all armor types. It reaches 3 tiles from open ground and 2 from woods, scrub, rocks or shallows.",
  },
  40: {
    name: "Gladius",
    row: 5, // Sword
    range: [1, 1],
    tags: [],
    desc: "A Gladius is a short stabbing sword: good damage against all armor types, but less effective against the heaviest armors.",
  },
  41: {
    name: "Katana",
    row: 5, // Sword
    range: [1, 1],
    tags: [],
    desc: "A Katana delivers good damage against all armor types, but is less effective against the heaviest armors.",
  },
  42: {
    name: "Dragonfire",
    row: 23, // Cannonball
    patch: { 7: 35 }, // …but it burns fliers too (the Cannonball's Feathered Hide cell is 0)
    range: [2, 8],
    tags: [13], // Burst (a fire weapon: double damage to Flammable war engines)
    desc: "Dragonfire is a breath of flame: it burns its target, then the two tiles beyond it in a line, and is ruinous to war engines and walls.",
  },
  43: {
    name: "Whip",
    row: 3, // Spear
    range: [1, 1],
    tags: [],
    desc: "A Whip delivers decent damage against all but the heaviest armor.",
  },
  44: {
    name: "Fangs",
    row: 4, // Antlers (the Stag's)
    range: [1, 1],
    tags: [],
    desc: "The Hounds' Fangs tear at lightly armoured troops, and do little to heavy plate.",
  },
  45: {
    name: "Naginata",
    row: 10, // Halberd
    range: [1, 1],
    tags: [],
    desc: "A Naginata is a long curved glaive: it cuts deep into every armor, and deepest into the lightest.",
  },
  46: {
    name: "Shuriken",
    row: 3, // Spear (as the Javelin)
    range: [2, 3],
    tags: [],
    desc: "Shuriken are thrown blades: decent damage at a short distance against all but the heaviest armor.",
  },
  47: {
    name: "Ninjato",
    row: 5, // Sword
    range: [1, 1],
    tags: [],
    desc: "A Ninjato is a short straight sword: good damage against all armor types, but less effective against the heaviest armors.",
  },
  48: {
    name: "Kanabo",
    row: 13, // Greatsword
    range: [1, 1],
    tags: [],
    desc: "A Kanabo is an iron-studded war club as tall as a man. Its blow shakes the ground around its target.",
  },
  49: {
    name: "Gale Blade",
    row: 5, // Sword
    range: [1, 1],
    tags: [],
    desc: "The Tengu's blade strikes with a gust from its fan behind it: the foe is thrown a tile back.",
  },
  // blast: the share of the blow the aimed tile and its four neighbours take (data/combat-data BLAST_SHARE)
  50: {
    name: "Acid Flask",
    row: 25, // Fireball
    range: [2, 6],
    tags: [],
    blast: [100, 60],
    desc: "An Acid Flask bursts like a Fireball, on its target and the four tiles around it, and leaves acid that eats 5 HP a turn for 3 turns.",
  },
  51: {
    name: "Dagger",
    row: 8, // Short Sword
    range: [1, 1],
    tags: [],
    desc: "A Dagger is a last resort: weak against everything but the unarmoured.",
  },
  52: {
    name: "Rune Fists",
    row: 13, // Greatsword
    range: [1, 1],
    tags: [],
    desc: "The Golem's Rune Fists deliver crushing melee damage.",
  },
  53: {
    name: "Claws",
    row: 8, // Short Sword
    range: [1, 1],
    tags: [],
    desc: "An Imp's Claws scratch at the lightly armoured and do little else.",
  },
  54: {
    name: "Starlight",
    row: 26, // Lightning Storm
    range: [2, 4],
    tags: [],
    desc: "Starlight is a bolt from the Unicorn's horn: steady damage against every armor.",
  },
  55: {
    name: "Flame Jet",
    row: 25, // Fireball
    range: [2, 4],
    tags: [13], // a fire weapon: double damage to Flammable war engines
    blast: [100, 60],
    desc: "A Flame Jet is a gout of fire at short range that bursts like a Fireball, ruinous to war engines.",
  },
  56: {
    name: "Burning Hands",
    row: 5, // Sword
    range: [1, 1],
    tags: [13],
    desc: "The Efreet's Burning Hands deliver good damage up close.",
  },
  57: {
    name: "Twin Scimitars",
    row: 5, // Sword
    range: [1, 1],
    tags: [],
    desc: "Twin Scimitars deliver good damage against all armor types, but are less effective against the heaviest armors.",
  },
  58: {
    name: "Rusted Sword",
    row: 5, // Sword
    range: [1, 1],
    tags: [],
    desc: "A Rusted Sword still cuts: good damage against all but the heaviest armors.",
  },
  59: {
    name: "Macuahuitl",
    row: 5, // Sword
    range: [1, 1],
    tags: [],
    desc: "A Macuahuitl is a wooden club edged with obsidian: good damage against all armor types, but less effective against the heaviest armors.",
  },
  60: {
    name: "Atlatl Dart",
    row: 3, // Spear (as the Javelin)
    range: [2, 3],
    tags: [8], // Shoot and Move
    desc: "An Atlatl Dart is flung from a spear-thrower: decent damage at a short distance against all but the heaviest armor, and no cover turns it.",
  },
  61: {
    name: "Sunbeam",
    row: 25, // Fireball
    range: [2, 7],
    tags: [13], // a fire weapon
    desc: "A Sunbeam is a lance of fire: far stronger than a Fireball on its target, and it burns on through the two tiles beyond.",
  },
  62: {
    name: "Obsidian Knife",
    row: 8, // Short Sword
    range: [1, 1],
    tags: [],
    desc: "An Obsidian Knife is a last resort: weak against everything but the unarmoured.",
  },
  63: {
    name: "Gale",
    row: 26, // Lightning Storm
    range: [2, 4],
    tags: [8], // Shoot and Move
    desc: "The Feathered Serpent's Gale is a blast of wind at short range: steady damage against every armor.",
  },
};
// The weapons Nullify stops (the three spells and Chain Lightning).
export const MAGIC_WEAPONS = [25, 26, 27, 36, 61];
// every bonus weapon that is not swung in melee (rules/combat RANGED_WEAPONS)
export const BONUS_RANGED = [35, 36, 39, 42, 46, 50, 54, 55, 60, 61, 63];
// the Alchemist's flask, and the acid it leaves: HP a turn, for how many of the victim's turns
export const FLASK_WEAPON = 50;
export const ACID = { damage: 5, turns: 3 };
export const CHAIN_WEAPON = 36;
// Chain Lightning: added to the weapon x armour cell of every bolt and leap, and the share of the bolt each leap
// carries (four leaps, each from the unit last struck to the nearest unstruck enemy within CHAIN_REACH tiles)
export const CHAIN_BONUS = 10;
export const CHAIN_SHARE = [0.5, 0.4, 0.3, 0.2];
export const CHAIN_REACH = 2;
// Dragonfire, and the share of the blow the first and second tile BEYOND its target take
export const DRAGONFIRE_WEAPON = 42;
// the weapons that burn on in a line beyond their target: Dragonfire and the Sun Priest's Sunbeam
export const BEAM_WEAPONS = [42, 61];
export const BREATH_SHARE = [0.6, 0.35];

// Movement class (0 fly · 1 skirmish · 2 formation · 3 cavalry · 4 war engine), as data/combat-data UNIT_AL.
export const BONUS_AL = {
  cragsmen: 1,
  spellwardens: 2,
  sentinel: 2,
  marines: 1,
  pavisiers: 2,
  battlemage: 2,
  gladiator: 1,
  samurai: 2,
  dragonrider: 0,
  beastmaster: 2,
  hounds: 1,
  sohei: 2,
  shinobi: 1,
  oni: 2,
  tengu: 0,
  alchemist: 2,
  imp: 0,
  golem: 2,
  unicorn: 0,
  efreet: 0,
  naga: 1,
  skeleton: 2,
  jaguar: 1,
  eagle: 1,
  sunpriest: 2,
  serpent: 0,
};

// The combat record of each unit, in the shape of data/combat-data UNIT_COMBAT. rating tier → rf 45/60/75/90/100/115.
// Trait flags: climb · nullify · unyielding · amphibious · pavise · chain (the six bonus abilities, rules/bonus.js).
export const BONUS_COMBAT = {
  cragsmen: { move: 4, weapon: 35, weapon2: 3, armour: 3, rating: 2, rf: 75, abilities: [8], climb: true },
  // regen: the HP it mends by itself at the start of each of its turns
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
    regen: 10,
  },
  // armour 10 = the Heavy Armour & Shield column, shown as "Living Stone"
  sentinel: {
    move: 4,
    weapon: 38,
    weapon2: 0,
    armour: 10,
    rating: 4,
    rf: 100,
    abilities: [14, 4],
    unyielding: true,
    bulwark: true, // a charge gains nothing against it, it cannot be flanked, and nothing throws it back
    armourName: "Living Stone",
  },
  // terrainRange: the musket reaches 3 tiles from open ground, 2 from woods, scrub, rocks or shallows
  marines: {
    move: 4,
    weapon: 39,
    weapon2: 5,
    armour: 6,
    rating: 3,
    rf: 90,
    abilities: [7],
    amphibious: true,
    terrainRange: true,
    grapple: 6, // once a battle: swing to a free tile within this many tiles, in place of its move
    breach: true, // its blows ignore the cover of walls, towers, gates and palisades
  },
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
  // teleport: it moves as the Wizard does; First Strike (1) as the Hero has it; Shoot and Move (8)
  battlemage: {
    move: 4,
    weapon: 36,
    weapon2: 6,
    armour: 15,
    rating: 3,
    rf: 90,
    abilities: [1, 11, 14, 8],
    standard: true,
    chain: true,
    teleport: true,
  },
  // armourBonus: taken off the weapon x armour cell of every blow against it (set in the arena so that Gladiators
  // beat Greatswordsmen point for point)
  gladiator: {
    move: 4,
    weapon: 40,
    weapon2: 0,
    armour: 10,
    rating: 3,
    rf: 90,
    abilities: [],
    whirl: true,
    armourBonus: 10,
  },
  // a swordsman who is also a lesser Shaman: the Spirit Shroud aura (flag `shroud`), reaching 2 tiles instead of 4.
  // dmgBonus / armourBonus: +10 on the weapon x armour cell of every blow it deals, -10 on every blow it takes.
  samurai: {
    move: 4,
    weapon: 41,
    weapon2: 0,
    armour: 8,
    rating: 3,
    rf: 90,
    abilities: [27],
    pikeWall: true,
    shroud: true,
    shroudRange: 2,
    lesserShroud: true,
    keen: true,
    dmgBonus: 10,
    armourBonus: 10,
  },
  // a flier in Relic Armour at the Hero's rating: the Lance (15) up close, Dragonfire at 2-8.
  // twinAttack: each turn it may breathe fire once AND strike with the lance once, in either order, around its move.
  dragonrider: {
    move: 8,
    weapon: 42,
    weapon2: 15,
    armour: 15,
    rating: 5,
    rf: 115,
    abilities: [1, 14, 15],
    charge: true,
    fly: true,
    dragonfire: true,
    twinAttack: true,
  },
  // conjures: what its Conjure calls (in place of the Conjurer's Sapper / Bodyguard) — up to two, leashed as theirs
  beastmaster: {
    move: 4,
    weapon: 43,
    weapon2: 0,
    armour: 1,
    rating: 1,
    rf: 60,
    abilities: [],
    conjure: true,
    conjures: "hounds",
  },
  // the Stag one tier down: a point less movement, a rating tier lower, and no Charge
  hounds: { move: 7, weapon: 44, weapon2: 0, armour: 4, rating: 2, rf: 75, abilities: [], summoned: true },
  // SATOSHI's second wave. sutra: the HP every friend beside it mends at the start of its turn.
  sohei: { move: 4, weapon: 45, weapon2: 0, armour: 9, rating: 4, rf: 100, abilities: [4], sutra: 10, dmgBonus: 5 },
  // shadowStep: hides on ANY ground (not only in cover) when it ends a turn unattacking, and its blows from hiding land
  // as an ambush (+30 on the cell, like a charge)
  shinobi: { move: 5, weapon: 46, weapon2: 47, armour: 3, rating: 3, rf: 90, abilities: [16], shadowStep: true },
  // quake: its blow also shakes every other enemy standing next to its TARGET, at half strength
  oni: {
    move: 3,
    weapon: 48,
    weapon2: 0,
    armour: 8,
    rating: 4,
    rf: 100,
    abilities: [14, 4],
    quake: true,
    armourName: "Oni Hide",
  },
  // gale: the foe it strikes is thrown one tile back (and so cannot strike back), when there is room behind it
  tengu: {
    move: 7,
    weapon: 49,
    weapon2: 0,
    armour: 7,
    rating: 5,
    rf: 115,
    abilities: [],
    fly: true,
    gale: true,
    dmgBonus: 20,
    armourBonus: 10,
  },
  // THE LABORATORY AND ITS CREATURES. The Alchemist throws flasks (flask: a Fireball-shaped burst that leaves acid),
  // heals (the Priest's Heal, 30 HP at 2 tiles) and summons Imps (the Conjurer's rule).
  alchemist: {
    move: 4,
    weapon: 50,
    weapon2: 51,
    armour: 9,
    rating: 3,
    rf: 90,
    abilities: [],
    flask: true,
    conjure: true,
    conjures: "imp",
  },
  imp: { move: 6, weapon: 53, weapon2: 0, armour: 2, rating: 2, rf: 75, abilities: [], fly: true, summoned: true },
  // stoneskin: no single blow takes more than this many HP from it
  golem: {
    move: 3,
    weapon: 52,
    weapon2: 0,
    armour: 10,
    rating: 4,
    rf: 100,
    abilities: [14, 4],
    unyielding: true,
    bulwark: true,
    stoneskin: 20,
    armourName: "Rune Stone",
  },
  // purity: friends within this many tiles feel no Fear and are cleansed of acid
  unicorn: { move: 7, weapon: 54, weapon2: 4, armour: 7, rating: 3, rf: 90, abilities: [], fly: true, purity: 2 },
  // burn: HP every enemy standing beside it loses at the start of that enemy's turn
  efreet: {
    move: 5,
    weapon: 55,
    weapon2: 56,
    armour: 7,
    rating: 5,
    rf: 115,
    abilities: [14],
    fly: true,
    burn: 20,
    armourName: "Living Flame",
    armourBonus: 10,
  },
  // constrict: the foe it strikes cannot move on its next turn
  naga: {
    move: 5,
    weapon: 57,
    weapon2: 0,
    armour: 10,
    rating: 5,
    rf: 115,
    abilities: [],
    amphibious: true,
    constrict: true,
    armourBonus: 10,
    dmgBonus: 10,
    whirl: true,
  },
  // undying: the first time it is struck down it rises again with this many HP
  skeleton: {
    move: 4,
    weapon: 58,
    weapon2: 0,
    armour: 10,
    rating: 5,
    rf: 115,
    abilities: [4],
    undying: 100,
    dmgBonus: 10,
    armourBonus: 10,
  },
  // TEZCAL. forestWalk: woods cost 1 to cross. pounce: +20 on the cell when it strikes from woods, tall grass, scrub
  // or rocks. eagleEye: its darts ignore the cover of the target's tile.
  jaguar: {
    move: 5,
    weapon: 59,
    weapon2: 0,
    armour: 6,
    rating: 3,
    rf: 90,
    abilities: [],
    forestWalk: true,
    pounce: 20,
    armourBonus: 5,
  },
  eagle: {
    move: 5,
    weapon: 60,
    weapon2: 59,
    armour: 3,
    rating: 2,
    rf: 75,
    abilities: [8],
    forestWalk: true,
    eagleEye: true,
  },
  // sunPriest: the caster of Dawn (friends within 2 tiles mend 15) and Eclipse (a foe within 5 strikes at half
  // strength through its next turn); sunbeam: +N on the cell of its Sunbeam
  sunpriest: {
    move: 4,
    weapon: 61,
    weapon2: 62,
    armour: 9,
    rating: 4,
    rf: 100,
    abilities: [],
    sunPriest: true,
    sunbeam: 30,
  },
  // tailwind: friends beside it move this many tiles further
  serpent: {
    move: 7,
    weapon: 63,
    weapon2: 44,
    armour: 7,
    rating: 4,
    rf: 100,
    abilities: [8],
    fly: true,
    tailwind: 1,
    dmgBonus: 10,
  },
};
export const BONUS_COURAGE = {
  cragsmen: 2,
  spellwardens: 3,
  sentinel: 5,
  marines: 2,
  pavisiers: 2,
  battlemage: 5,
  gladiator: 3,
  samurai: 4,
  dragonrider: 5,
  beastmaster: 3,
  hounds: 3,
  sohei: 4,
  shinobi: 3,
  oni: 5,
  tengu: 4,
  alchemist: 3,
  imp: 2,
  golem: 5,
  unicorn: 4,
  efreet: 5,
  naga: 3,
  skeleton: 5,
  jaguar: 3,
  eagle: 3,
  sunpriest: 4,
  serpent: 4,
};
export const BONUS_COST = {
  cragsmen: 175,
  spellwardens: 225,
  sentinel: 300,
  marines: 150,
  pavisiers: 200,
  battlemage: 750,
  gladiator: 175,
  samurai: 250,
  dragonrider: 750,
  beastmaster: 250,
  hounds: 0, // called by the Beast Master, never deployed
  sohei: 175,
  shinobi: 225,
  oni: 350,
  tengu: 325,
  alchemist: 250,
  imp: 0, // summoned by the Alchemist
  golem: 400,
  unicorn: 275,
  efreet: 350,
  naga: 300,
  skeleton: 500,
  jaguar: 150,
  eagle: 175,
  sunpriest: 400,
  serpent: 300,
};
// "You may only deploy 1 Elite unit per 1000 deployment points" — the Battlemage and the Dragon Rider count as elites.
export const BONUS_ELITE = { battlemage: true, dragonrider: true, sunpriest: true };

// Sprite strips: cut from the supplied art sheets by tools/ros/bonus/import_sheet.py — 88 px frames, the whole strip
// one attack (frame 0 a ready pose), `hitFrame` the frame the blow lands or the shot leaves on.
const strip = (frames, hitFrame) => ({ frames, frameW: 88, frameH: 88, hitFrame });
// a unit with a projectile plays the same strip for its shot and for its hand-to-hand blow
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
    ...both(5, 3),
    kind: "ranged",
    projectile: "bolt",
    ability: "Climb — crosses cliffs no other ground unit can. Throws Javelins at 2–3 tiles and may still move.",
  },
  spellwardens: {
    name: "Spellwardens",
    sprite: "spellwardens",
    ...strip(6, 4),
    kind: "melee",
    ability: "Nullify — enemy magic does nothing to units within 2 tiles of a Spellwarden.",
  },
  sentinel: {
    name: "Stone Sentinel",
    sprite: "sentinel",
    ...strip(8, 5),
    kind: "melee",
    ability:
      "Bulwark — charges and flank attacks gain nothing against it. Unyielding — ignores quicksand, cannot be healed by Priests; Craftsmen can repair it. Fear.",
  },
  marines: {
    name: "Marines",
    sprite: "marines",
    ...both(7, 5),
    kind: "ranged",
    projectile: "bullet",
    ability:
      "Amphibious — wades through deep water at double cost; cannot attack while standing in it. Boarding Musket: 2–3 tiles. Grapple — once a battle, swings to a free tile up to 6 away. Breach — ignores the cover of fortifications.",
  },
  pavisiers: {
    name: "Pavisiers",
    sprite: "pavisiers",
    ...both(8, 5),
    kind: "ranged",
    projectile: "arrow",
    ability:
      "Pavise — while it has not moved, it and the ally behind it take half ranged damage, it takes a quarter less in melee, and its own bolts hit harder.",
  },
  battlemage: {
    name: "Battlemage",
    sprite: "battlemage",
    ...strip(8, 3),
    kind: "ranged",
    ability:
      "Chain Lightning — strikes its target, then leaps on through up to four more enemies, weakening as it goes.",
  },
  gladiator: {
    name: "Gladiators",
    sprite: "gladiator",
    ...strip(7, 5),
    kind: "melee",
    ability: "Whirl — its blow spins on through every other enemy standing next to it.",
  },
  samurai: {
    name: "Samurai",
    sprite: "samurai",
    ...strip(6, 4),
    kind: "melee",
    ability:
      "Lesser Shroud — a swordsman with a Shaman's aura: allies within 2 tiles gain +15, enemies within 2 lose 15.",
  },
  // one strip, two attacks: frames 0–2 breathe fire (it leaves on frame 1), frames 3–6 are the lance dive (it lands on 5)
  dragonrider: {
    name: "Dragon Riders",
    sprite: "dragonrider",
    frames: 7,
    frameW: 176,
    frameH: 128,
    rangedFrom: 0,
    rangedTo: 2,
    rangedHit: 1,
    meleeFrom: 3,
    meleeTo: 6,
    hitFrame: 5,
    kind: "cavalry",
    projectile: "ball",
    magic: true, // the shot is drawn and sounds as a fireball, not a cannonball
    ability:
      "Dragonfire — hurls a gout of flame at 3–8 tiles like a cannon shot, and may still move; a flier in Relic Armour.",
  },
  beastmaster: {
    name: "Beast Master",
    sprite: "beastmaster",
    ...strip(5, 3),
    kind: "melee",
    ability:
      "Call Hounds — whistles up to two packs of Hounds to its side, each leashed within range 8. Fights with a Whip.",
  },
  hounds: {
    name: "Hounds",
    sprite: "hounds",
    ...strip(4, 2),
    kind: "melee",
    ability: "Called by a Beast Master: fast, leashed within 8 tiles of it, and gone if it falls.",
  },
  sohei: {
    name: "Sohei",
    sprite: "sohei",
    frames: 4,
    frameW: 128,
    frameH: 88,
    hitFrame: 1,
    kind: "melee",
    ability: "Sutra — friends beside it mend 10 HP at the start of its turn. Fearless.",
  },
  shinobi: {
    name: "Shinobi",
    sprite: "shinobi",
    frames: 6,
    frameW: 104,
    frameH: 88,
    meleeFrom: 0,
    meleeTo: 2,
    hitFrame: 1,
    rangedFrom: 3,
    rangedTo: 5,
    rangedHit: 4,
    kind: "ranged",
    projectile: "bolt",
    ability: "Shadow — hides on any ground; its first blow from hiding is an ambush. Throws Shuriken at 2–3 tiles.",
  },
  oni: {
    name: "Oni",
    sprite: "oni",
    frames: 4,
    frameW: 128,
    frameH: 96,
    hitFrame: 2,
    kind: "melee",
    ability: "Earthshaker — its blow shakes every other enemy beside its target at half strength. Fear, Fearless.",
  },
  tengu: {
    name: "Tengu",
    sprite: "tengu",
    frames: 4,
    frameW: 144,
    frameH: 104,
    hitFrame: 2,
    kind: "cavalry",
    ability: "Gale — the foe it strikes is thrown a tile back and cannot strike back. Flies.",
  },
  // heal / healAmount / healRange: the Priest's Heal with its own numbers. magic + projectile "ball": the flask flies
  // as the Fireball does; greenShot tints it and its burst green. splash: the + cross of a Fireball.
  alchemist: {
    name: "Alchemist",
    sprite: "alchemist",
    ...both(4, 2),
    kind: "ranged",
    projectile: "ball",
    magic: true,
    greenShot: true,
    splash: true,
    heal: true,
    healAmount: 30,
    healRange: 2,
    ability:
      "Throws Acid Flasks that burst like a Fireball and leave acid; heals 30 HP at 2 tiles; summons up to two Imps.",
  },
  imp: {
    name: "Imp",
    sprite: "imp",
    ...strip(4, 2),
    kind: "melee",
    ability: "Summoned by an Alchemist: a small flier, leashed within 8 tiles of it, and gone if it falls.",
  },
  golem: {
    name: "Golem",
    sprite: "golem",
    frames: 4,
    frameW: 104,
    frameH: 104,
    hitFrame: 2,
    kind: "melee",
    ability: "Stoneskin — no single blow takes more than 20 HP from it. Fear, Fearless; only Craftsmen can mend it.",
  },
  // shotSpell: its bolt flies as the Wizard's ice bolt does (a white-blue streak), with no burst of flame
  unicorn: {
    name: "Unicorn",
    sprite: "unicorn",
    frames: 4,
    frameW: 112,
    frameH: 104,
    hitFrame: 1,
    rangedFrom: 0,
    rangedTo: 3,
    rangedHit: 1,
    meleeFrom: 0,
    meleeTo: 3,
    kind: "ranged",
    projectile: "ball",
    magic: true,
    shotSpell: "ice",
    ability: "Purity — friends within 2 tiles feel no Fear and are cleansed of acid. Starlight at 2–4 tiles. Flies.",
  },
  efreet: {
    name: "Efreet",
    sprite: "efreet",
    ...both(4, 2),
    kind: "ranged",
    projectile: "ball",
    magic: true,
    splash: true,
    ability:
      "Burning Aura — enemies beside it lose 20 HP each turn. Flame Jet at 2–4 tiles, bursting like a Fireball. Fear. Flies.",
  },
  naga: {
    name: "Naga",
    sprite: "naga",
    ...strip(4, 2),
    kind: "melee",
    ability: "Constrict — the foe it strikes cannot move on its next turn. Amphibious.",
  },
  skeleton: {
    name: "Skeletons",
    sprite: "skeleton",
    ...strip(4, 2),
    kind: "melee",
    ability: "Rise Again — the first time it is struck down it rises with 40 HP. Fearless.",
  },
  jaguar: {
    name: "Jaguar Warriors",
    sprite: "jaguar",
    frames: 4,
    frameW: 112,
    frameH: 88,
    hitFrame: 2,
    kind: "melee",
    ability:
      "Jungle Stride — crosses woods as open ground. Pounce — strikes harder from woods, tall grass, scrub or rocks.",
  },
  eagle: {
    name: "Eagle Warriors",
    sprite: "eagle",
    frames: 4,
    frameW: 104,
    frameH: 88,
    hitFrame: 1,
    rangedFrom: 0,
    rangedTo: 3,
    rangedHit: 1,
    meleeFrom: 0,
    meleeTo: 3,
    kind: "ranged",
    projectile: "bolt",
    ability:
      "Jungle Stride — crosses woods as open ground. Eagle Eye — its darts ignore cover. Atlatl Darts at 2–3 tiles, and may still move.",
  },
  sunpriest: {
    name: "Sun Priest",
    sprite: "sunpriest",
    frames: 4,
    frameW: 96,
    frameH: 88,
    hitFrame: 2,
    rangedFrom: 0,
    rangedTo: 3,
    rangedHit: 2,
    meleeFrom: 0,
    meleeTo: 3,
    kind: "ranged",
    projectile: "ball",
    magic: true,
    ability:
      "Sun Magic — Sunbeam (a lance of fire on one foe), Dawn (heals friends within 2 tiles), Eclipse (blinds a foe).",
  },
  serpent: {
    name: "Feathered Serpent",
    sprite: "serpent",
    frames: 4,
    frameW: 144,
    frameH: 104,
    hitFrame: 2,
    rangedFrom: 0,
    rangedTo: 3,
    rangedHit: 2,
    meleeFrom: 0,
    meleeTo: 3,
    kind: "ranged",
    projectile: "ball",
    magic: true,
    shotSpell: "ice",
    ability: "Tailwind — friends beside it move 1 further. Gale at 2–4 tiles, and may still move. Flies.",
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
    flag: "bulwark",
    n: "Bulwark",
    icon: "skill_pavise",
    d: "Immovable: a charge gains nothing against it, attacks from its flank or rear gain nothing, and it cannot be thrown back.",
  },
  {
    flag: "unyielding",
    n: "Unyielding",
    icon: "skill_unyielding",
    d: "Living stone: a Priest's Heal does nothing for it and quicksand neither stops nor hurts it. Craftsmen can Repair it like a war engine.",
  },
  {
    flag: "forestWalk",
    n: "Jungle Stride",
    icon: "skill_climb",
    d: "Crosses woods at 1 movement a tile, as if they were open ground.",
  },
  {
    flag: "pounce",
    n: "Pounce",
    icon: "skill_first",
    d: "A blow struck from woods, tall grass, scrub or rocks is 20 stronger on the weapon and armour table.",
  },
  {
    flag: "eagleEye",
    n: "Eagle Eye",
    icon: "skill_chain",
    d: "Its darts ignore the cover of the ground its target stands on: woods, houses, walls and towers protect nobody from them.",
  },
  {
    flag: "sunPriest",
    n: "Sun Magic",
    icon: "skill_nullify",
    d: "Three spells. Sunbeam: a lance of fire at 2 to 7 tiles, 30 stronger than a Fireball's cell, that burns on through the two tiles beyond its target (60% then 35%, friend or foe). Dawn: every friendly unit within 2 tiles mends 15 HP. Eclipse: a foe within 5 tiles is blinded and strikes at half strength until its next turn ends.",
  },
  {
    flag: "tailwind",
    n: "Tailwind",
    icon: "skill_charge",
    d: "Friendly units standing beside it move 1 tile further.",
  },
  {
    flag: "flask",
    n: "Acid Flask",
    icon: "skill_chain",
    d: "Its flask bursts like a Fireball on the target and the four tiles around it (friend or foe), and everyone it burns loses 5 HP at the start of each of their next 3 turns.",
  },
  {
    flag: "healRange",
    n: "Elixir",
    icon: "skill_nullify",
    d: "Heals a friendly unit within 2 tiles for 30 HP, in place of its attack.",
  },
  {
    flag: "stoneskin",
    n: "Stoneskin",
    icon: "skill_unyielding",
    d: "No single blow takes more than 20 HP from it, however strong.",
  },
  {
    flag: "purity",
    n: "Purity",
    icon: "skill_nullify",
    d: "Friendly units within 2 tiles feel no Fear, and acid is washed from them at the start of their turn.",
  },
  {
    flag: "burn",
    n: "Burning Aura",
    icon: "skill_chain",
    d: "Every enemy standing beside it loses 10 HP at the start of that enemy's turn.",
  },
  {
    flag: "constrict",
    n: "Constrict",
    icon: "skill_amphibious",
    d: "The foe it strikes in its own turn is held in its coils: it cannot move on its next turn, though it can still fight.",
  },
  {
    flag: "undying",
    n: "Rise Again",
    icon: "skill_unyielding",
    d: "The first time it is struck down in a battle it rises again at once with 40 HP.",
  },
  {
    flag: "sutra",
    n: "Sutra",
    icon: "skill_nullify",
    d: "At the start of its turn, every friendly unit standing beside it mends 10 HP (war engines and Stone Sentinels do not).",
  },
  {
    flag: "shadowStep",
    n: "Shadow",
    icon: "skill_first",
    d: "Hides on any ground, not only in cover, when it ends a turn without attacking and no enemy stands beside it. A blow or throw from hiding is an ambush: 30 stronger on the weapon and armour table.",
  },
  {
    flag: "quake",
    n: "Earthshaker",
    icon: "skill_unyielding",
    d: "Its blow shakes the ground: every other enemy standing next to its target takes half of it.",
  },
  {
    flag: "gale",
    n: "Gale",
    icon: "skill_charge",
    d: "The foe it strikes is thrown one tile straight back, and so cannot strike back. War engines, and foes with no free ground behind them, stand fast.",
  },
  {
    flag: "grapple",
    n: "Grapple",
    icon: "skill_climb",
    d: "Once a battle, in place of its move, it throws a grapple and swings to any free tile within 6 — over water, walls and enemies, onto a rampart if it likes. It may still strike with its sword afterwards.",
  },
  {
    flag: "breach",
    n: "Breach",
    icon: "skill_amphibious",
    d: "Its blows and shots ignore the cover of fortifications: walls, towers, gates and palisades protect nobody from it.",
  },
  {
    flag: "conjures",
    n: "Call",
    icon: "skill_conjure",
    d: "Calls its creature (a Beast Master's Hounds, an Alchemist's Imp) onto a tile beside it — up to two at once, each leashed within range 8 and unable to act the turn it arrives. They are gone if their master falls.",
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
    d: "Ends a turn without moving and it plants its pavise: until it next moves, it and any friendly unit standing directly behind it take half damage from ranged attacks, it takes a quarter less from blows hand to hand, and its own bolts are 10 stronger on the weapon and armour table.",
  },
  {
    flag: "chain",
    n: "Chain Lightning",
    icon: "skill_chain",
    d: "Its ranged attack (2–5 tiles) hits the target at full strength, then leaps to up to two enemies standing next to the target at half strength.",
  },
  {
    flag: "whirl",
    n: "Whirl",
    icon: "skill_melee",
    d: "It spins as it strikes: after its blow lands on its target, every other enemy standing next to the Gladiators takes three quarters of the same blow.",
  },
  {
    flag: "lesserShroud",
    n: "Lesser Shroud",
    icon: "skill_shroud",
    d: "A Shaman's Spirit Shroud at half the reach: once an enemy has come near, allies within 2 tiles gain +15 attack and courage, and enemies within 2 tiles lose 15.",
  },
  {
    flag: "regen",
    n: "Mending Runes",
    icon: "skill_prayer",
    d: "Mends itself by 10 HP at the start of each of its turns.",
  },
  {
    flag: "terrainRange",
    n: "Boarding Musket",
    icon: "skill_ranged",
    d: "Fires at 2–3 tiles: 3 from open ground, walls and decks, only 2 from woods, tall grass, scrub, rocks or shallows. Up close it draws a Short Sword.",
  },
  {
    flag: "dragonfire",
    n: "Dragonfire",
    icon: "skill_fireball",
    d: "A breath of flame at 2–8 tiles: full damage to the target, then 60% and 35% to whoever stands on the next two tiles in a line beyond it, friend or foe. Double damage to flammable war engines, and it breaks walls.",
  },
  {
    flag: "twinAttack",
    n: "Fire and Lance",
    icon: "skill_charge",
    d: "Each turn it may breathe Dragonfire once and strike with its Lance once, in either order, before or after its move. Tap a foe it can reach and it flies in with the lance; the Dragonfire button breathes instead.",
  },
  {
    flag: "keen",
    n: "Master Swordsman",
    icon: "skill_first",
    d: "Every blow it deals is 10 stronger and every blow it takes is 10 weaker, on the weapon and armour table.",
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
  { from: "halberdiers", to: "gladiator", need: "Weapons", gate: 5942 }, // Mare Nostra 2
  { from: "swordsmen", to: "samurai", need: "Spirit", gate: 5962 }, // Satoshi 2
  { from: "griffon", to: "dragonrider", need: "Medal", gate: 5943 }, // Mare Nostra 3, The Admiral's Deck
  { from: "militiamen", to: "beastmaster", need: "Medal", gate: 5982 }, // the Mirror Sea 2
  { from: "shamans", to: "sohei", need: "Armor", gate: 5961 }, // Satoshi 1 (Armor: the one slot Shamans leave empty)
  { from: "rangers", to: "shinobi", need: "Lore", gate: 5962 }, // Satoshi 2
  { from: "greatswordsmen", to: "oni", need: "Spirit", gate: 5963 }, // Satoshi 3
  { from: "beastmaster", to: "tengu", need: "Spirit", gate: 5963 }, // Satoshi 3
  { from: "priests", to: "alchemist", need: "Lore", gate: 5925 }, // Isoluccia 5, The Arsenal
  { from: "sentinel", to: "golem", need: "Armor", gate: 5905 }, // Tilicia 5, The Sleepers Wake
  // the Beast Master's tree (user decision): its creatures are all made from a Beast Master
  { from: "beastmaster", to: "unicorn", need: "Lore", gate: 5971 }, // Satoshi raid 1, The Shrine Pass
  { from: "beastmaster", to: "efreet", need: "Weapons", gate: 5983 }, // the Mirror Sea 3, The Reaver-King
  { from: "beastmaster", to: "naga", need: "Beasts", gate: 5981 }, // the Mirror Sea 1, The Line of Hulls
  { from: "beastmaster", to: "skeleton", need: "Armor", gate: 5903 }, // Tilicia 3, The Sealed Vale
  { from: "pikemen", to: "jaguar", need: "Beasts", gate: 5994 }, // Tezcal 1
  { from: "archers", to: "eagle", need: "Lore", gate: 5995 }, // Tezcal 2
  { from: "cavalry", to: "serpent", need: "Spirit", gate: 5996 }, // Tezcal 3
  { from: "priests", to: "sunpriest", need: "Medal", gate: 5996 }, // Tezcal 3
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
    kit: "⚔ Boarding Musket / Short Sword · 🛡 Light Armor & Shield",
    note: "Isoluccian marines who wade through deep water to shoot from where no one else can reach. Once a battle they grapple across up to 6 tiles, and no wall gives cover against them.",
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
  gladiator: {
    role: "Arena Fighter",
    kit: "⚔ Gladius · 🛡 Light Armor & Shield",
    note: "Deck-fighters of Mare Nostra, trained in the arenas of the island cities. Surrounded, they are at their best: their blow spins on through every foe beside them.",
  },
  samurai: {
    role: "Spirit Swordsman",
    kit: "⚔ Katana · 🛡 Heavy Armor",
    note: "Warriors of Satoshi who fight as swordsmen and carry their ancestors with them: a lesser Spirit Shroud steadies allies and unnerves foes within 2 tiles.",
  },
  dragonrider: {
    role: "Flying Terror",
    kit: "⚔ Dragonfire / Lance · 🛡 Relic Armor",
    note: "A lancer on a sea-dragon of Mare Nostra. It flies over anything, breathes fire like a cannon shot at long range, and fights in the air like a Hero.",
  },
  beastmaster: {
    role: "Hound Handler",
    kit: "⚔ Whip · 🛡 Light Armor",
    note: "Kennel-masters of the Mirror Sea corsairs. A Beast Master whistles up to two packs of war Hounds to its side — fast, savage, a little less than a Stag — leashed within 8 tiles and gone if their master falls.",
  },
  sohei: {
    role: "Warrior Monk",
    kit: "⚔ Naginata · 🛡 Holy Vestment",
    note: "Monks of the mountain temples of Satoshi, who fight with the naginata and chant as they do. Friends beside a Sohei mend 10 HP each turn, and nothing frightens it.",
  },
  shinobi: {
    role: "Shadow Agent",
    kit: "⚔ Shuriken / Ninjato · 🛡 Light Armor",
    note: "Spies and night-fighters. A Shinobi hides on open ground as others hide in woods, and strikes hardest from hiding.",
  },
  oni: {
    role: "Mountain Ogre",
    kit: "⚔ Kanabo · 🛡 Oni Hide",
    note: "A red ogre of the high passes with an iron club. Slow and terrible: its blow shakes every foe beside the one it lands on.",
  },
  tengu: {
    role: "Wind Spirit",
    kit: "⚔ Gale Blade · 🛡 Feathered Hide",
    note: "Crow-winged spirits of the cedar forests. A Tengu's fan throws the foe it strikes a tile back, out of reach of any reply.",
  },
  alchemist: {
    role: "Battle Chemist",
    kit: "⚔ Acid Flask / Dagger · 🛡 Holy Vestment",
    note: "A priest who left the temple for the laboratory. Its flasks burst like a Fireball and leave acid that eats 5 HP a turn for 3 turns; its elixirs heal 30 HP at 2 tiles; and it keeps up to two Imps on a leash.",
  },
  golem: {
    role: "Rune Construct",
    kit: "⚔ Rune Fists · 🛡 Rune Stone",
    note: "A Stone Sentinel rebuilt with rune-cut armour. Slower still, but no single blow takes more than 20 HP from it.",
  },
  unicorn: {
    role: "Winged Unicorn",
    kit: "⚔ Starlight / Hooves · 🛡 Feathered Hide",
    note: "A winged unicorn that only the truest knights can ride. Friends within 2 tiles feel no Fear and are washed clean of acid; its horn throws Starlight at 2–4 tiles.",
  },
  efreet: {
    role: "Fire Djinn",
    kit: "⚔ Flame Jet / Burning Hands · 🛡 Living Flame",
    note: "A djinn of the deep desert, bound by the Sirens' songs. Enemies who stand beside it burn for 10 HP a turn.",
  },
  naga: {
    role: "Serpent Warrior",
    kit: "⚔ Twin Scimitars · 🛡 Breastplate",
    note: "Serpent warriors of the warm seas. A Naga swims like the Marines, and the foe it strikes is held in its coils for a turn.",
  },
  skeleton: {
    role: "Undead Warrior",
    kit: "⚔ Rusted Sword · 🛡 Shield",
    note: "The dead of old battlefields, raised by a Conjurer. Cheap, fearless, and each one has to be put down twice.",
  },
  jaguar: {
    role: "Jungle Shock Troop",
    kit: "⚔ Macuahuitl · 🛡 Light Armor & Shield",
    note: "Warriors of Tezcal in jaguar skins. They run through woods as others run on a road, and strike hardest out of cover.",
  },
  eagle: {
    role: "Jungle Skirmisher",
    kit: "⚔ Atlatl Dart / Macuahuitl · 🛡 Light Armor",
    note: "Warriors of Tezcal in eagle feathers. Their darts find a foe behind any cover, they move after they throw, and they fight better up close than any other skirmisher.",
  },
  sunpriest: {
    role: "Priest of the Sun",
    kit: "⚔ Sunbeam / Obsidian Knife · 🛡 Minor Ward",
    note: "A high priest of Tezcal, the Wizard's equal with spells of his own: Sunbeam burns one foe, Dawn mends the friends around him, and Eclipse blinds an enemy for a turn.",
  },
  serpent: {
    role: "Winged Serpent",
    kit: "⚔ Gale / Fangs · 🛡 Feathered Hide",
    note: "A feathered serpent of the high temples: the horse-archer of the air. It throws a gale and flies on, and friends beside it are carried a tile further.",
  },
};
// Battle ids of the four bonus regions (Tilicia 5901–5913, Isoluccia 5921–5933, the Mirror Sea 5941–5952, Satoshi
// 5961–5972).
export const isBonusMap = (mapId) => mapId >= 5900 && mapId < 6000;
