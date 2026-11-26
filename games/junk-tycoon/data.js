// Junk Lot Tycoon - all game data and balance numbers in one place (prototype v0.1)
// Part shapes: box | cyl | sph | cone | tor.  P(shape, sx, sy, sz, x, y, z, color)
// y is measured from the item's bottom (items stand on y = 0).
const P = (s, sx, sy, sz, x, y, z, c) => ({ s, sx, sy, sz, x, y, z, c });

export const ITEMS = {
  // ---------- Tier 1: Grandma's Garage ----------
  teaset:   { name: "Tea Set (1974)", value: 35, tier: 1, w: 10, parts: [
    P("box", .7, .04, .45, 0, .02, 0, 0xc9b28a), P("sph", .18, .16, .18, -.15, .18, 0, 0xf2efe6),
    P("cyl", .07, .08, .07, .18, .08, .1, 0xf2efe6), P("cyl", .07, .08, .07, .18, .08, -.1, 0xf2efe6), P("cone", .05, .08, .05, -.32, .2, 0, 0xf2efe6)] },
  mower:    { name: "Lawnmower (Barely Used, Allegedly)", value: 60, tier: 1, w: 6, parts: [
    P("box", .6, .25, .5, 0, .22, 0, 0xd94f3d), P("cyl", .1, .06, .1, .25, .1, .25, 0x222222), P("cyl", .1, .06, .1, -.25, .1, .25, 0x222222),
    P("cyl", .1, .06, .1, .25, .1, -.25, 0x222222), P("cyl", .1, .06, .1, -.25, .1, -.25, 0x222222), P("box", .05, .7, .05, 0, .6, .35, 0x777777)] },
  toaster:  { name: "Toaster (Toasts One Side)", value: 20, tier: 1, w: 10, parts: [
    P("box", .35, .25, .22, 0, .125, 0, 0xb8c4cc), P("box", .25, .02, .04, 0, .255, .05, 0x333333), P("box", .25, .02, .04, 0, .255, -.05, 0x333333)] },
  cassettes:{ name: "Box of Mixtapes", value: 15, tier: 1, w: 10, parts: [
    P("box", .4, .2, .3, 0, .1, 0, 0x8a6a45), P("box", .38, .04, .28, 0, .22, 0, 0x2b2b2b)] },
  gnome:    { name: "Garden Gnome (Judging You)", value: 25, tier: 1, w: 9, parts: [
    P("cyl", .12, .25, .12, 0, .125, 0, 0x3b6fd9), P("sph", .1, .1, .1, 0, .31, 0, 0xf1c9a5), P("cone", .1, .22, .1, 0, .5, 0, 0xd93030), P("cone", .09, .12, .09, 0, .25, .06, 0xffffff)] },
  chair:    { name: "Rocking Chair", value: 45, tier: 1, w: 6, parts: [
    P("box", .5, .05, .5, 0, .45, 0, 0x8b5a2b), P("box", .5, .6, .05, 0, .78, -.23, 0x8b5a2b),
    P("box", .05, .45, .05, .22, .22, .22, 0x6b4421), P("box", .05, .45, .05, -.22, .22, .22, 0x6b4421), P("box", .05, .45, .05, .22, .22, -.22, 0x6b4421), P("box", .05, .45, .05, -.22, .22, -.22, 0x6b4421)] },
  lamp:     { name: "Table Lamp", value: 18, tier: 1, w: 10, parts: [
    P("cyl", .12, .04, .12, 0, .02, 0, 0x555555), P("cyl", .02, .35, .02, 0, .2, 0, 0x999999), P("cone", .2, .2, .2, 0, .42, 0, 0xf0d58a)] },
  vinyl:    { name: "Crate of Vinyl Records", value: 40, tier: 1, w: 7, parts: [
    P("box", .45, .3, .45, 0, .15, 0, 0xa07a4a), P("cyl", .2, .01, .2, 0, .31, 0, 0x111111)] },
  sewing:   { name: "Sewing Machine", value: 55, tier: 1, w: 5, parts: [
    P("box", .5, .08, .25, 0, .04, 0, 0x2f2f2f), P("box", .08, .3, .2, .2, .23, 0, 0x2f2f2f), P("box", .45, .08, .18, 0, .4, 0, 0x2f2f2f), P("box", .03, .12, .03, -.18, .3, 0, 0xc0c0c0)] },
  painting: { name: "Painting (Probably Nothing)", value: 30, tier: 1, w: 6, rare: { chance: .12, value: 600, name: "Painting (SIGNED! Wait, really?)" }, parts: [
    P("box", .6, .45, .05, 0, .225, 0, 0x9c7a3c), P("box", .5, .35, .02, 0, .225, .03, 0x4f7f5f)] },
  bike:     { name: "Old Bicycle", value: 50, tier: 1, w: 5, parts: [
    P("tor", .25, .25, .03, .35, .25, 0, 0x222222), P("tor", .25, .25, .03, -.35, .25, 0, 0x222222), P("box", .7, .04, .04, 0, .4, 0, 0x2e8b57), P("box", .04, .3, .04, -.3, .55, 0, 0x2e8b57), P("box", .2, .04, .08, -.3, .7, 0, 0x333333)] },
  sock:     { name: "A Single Sock", value: 0, tier: 1, w: 7, junk: true, parts: [P("box", .12, .04, .3, 0, .02, 0, 0xd8d8d8)] },
  bags:     { name: "Bag Full of Bags", value: 0, tier: 1, w: 7, junk: true, parts: [P("sph", .3, .25, .3, 0, .15, 0, 0xe8e0c8)] },
  umbrella: { name: "Umbrella (Inside-Out)", value: 0, tier: 1, w: 5, junk: true, parts: [P("cone", .35, .3, .35, 0, .5, 0, 0x5a3d8a), P("cyl", .015, .6, .015, 0, .3, 0, 0x333333)] },
  // ---------- Tier 2: Student Storage ----------
  guitar:   { name: "Guitar (3 Strings Left)", value: 70, tier: 2, w: 8, parts: [
    P("sph", .3, .08, .38, 0, .04, 0, 0xc9772f), P("box", .07, .03, .55, 0, .05, .45, 0x5a3a1a), P("cyl", .07, .02, .07, 0, .09, 0, 0x222222)] },
  fridge:   { name: "Mini Fridge (Smells Brave)", value: 90, tier: 2, w: 6, parts: [
    P("box", .5, .7, .5, 0, .35, 0, 0xeeeeee), P("box", .03, .2, .03, .2, .45, .26, 0x888888)] },
  gchair:   { name: "Gaming Chair (RGB Not Included)", value: 110, tier: 2, w: 5, parts: [
    P("box", .55, .1, .55, 0, .5, 0, 0x202020), P("box", .55, .75, .1, 0, .9, -.25, 0xc02040), P("cyl", .05, .45, .05, 0, .23, 0, 0x555555), P("cyl", .3, .04, .3, 0, .03, 0, 0x333333)] },
  cans:     { name: "Can Pyramid (400 Cans)", value: 30, tier: 2, w: 7, parts: [
    P("cone", .45, .7, .45, 0, .35, 0, 0xbfc7cf)] },
  sofa:     { name: "Suspiciously New Sofa", value: 180, tier: 2, w: 3, parts: [
    P("box", 1.4, .4, .7, 0, .2, 0, 0x3a6ea5), P("box", 1.4, .45, .15, 0, .6, -.28, 0x3a6ea5), P("box", .15, .25, .7, .63, .52, 0, 0x30598a), P("box", .15, .25, .7, -.63, .52, 0, 0x30598a)] },
  lavalamp: { name: "Lava Lamp (Still Lava-ing)", value: 35, tier: 2, w: 8, parts: [
    P("cone", .12, .12, .12, 0, .06, 0, 0x777777), P("cyl", .08, .35, .08, 0, .29, 0, 0xff5a8a)] },
  skate:    { name: "Skateboard", value: 45, tier: 2, w: 8, parts: [
    P("box", .2, .03, .8, 0, .09, 0, 0x2c2c2c), P("cyl", .03, .04, .03, .07, .03, .3, 0xffffff), P("cyl", .03, .04, .03, -.07, .03, .3, 0xffffff), P("cyl", .03, .04, .03, .07, .03, -.3, 0xffffff), P("cyl", .03, .04, .03, -.07, .03, -.3, 0xffffff)] },
  console:  { name: "Retro Console (Blow on It)", value: 140, tier: 2, w: 4, rare: { chance: .1, value: 900, name: "Retro Console (SEALED Prototype!)" }, parts: [
    P("box", .45, .1, .3, 0, .05, 0, 0x9a9aa8), P("box", .12, .03, .08, -.1, .11, .08, 0x333333)] },
  pizza:    { name: "Empty Pizza Box (Hope Dies)", value: 0, tier: 2, w: 8, junk: true, parts: [P("box", .45, .05, .45, 0, .025, 0, 0xd8b98a)] },
  noodles:  { name: "Ancient Instant Noodles", value: 0, tier: 2, w: 6, junk: true, parts: [P("cyl", .12, .12, .12, 0, .06, 0, 0xf4f0e0)] },
};

export const LOTS = [
  { id: "grandma", name: "Grandma's Garage", price: 40, tier: 1, count: [6, 8], hint: "Smells like lavender and motor oil." },
  { id: "student", name: "Student Storage Unit", price: 260, tier: 2, count: [6, 9], hint: "Something in here is still alive. Probably the fridge.", needs: "van" },
];

export const UPGRADES = [
  { id: "sponge", name: "Sponge", desc: "Clean 2x faster.", price: 60 },
  { id: "washer", name: "Pressure Washer", desc: "Clean 4x faster (stacks). Very loud.", price: 320, needs: "sponge" },
  { id: "table2", name: "Second Table", desc: "+4 shop slots.", price: 160 },
  { id: "sign", name: "Shop Sign", desc: "Customers come 2x more often.", price: 220 },
  { id: "van", name: "Bigger Van", desc: "Unlocks Student Storage lots.", price: 400 },
];

export const ACHIEVEMENTS = [
  { id: "first_lot", name: "First Junk", desc: "Buy your first lot." },
  { id: "shiny", name: "Shiny!", desc: "Restore an item to 100%." },
  { id: "first_sale", name: "First Sale", desc: "Sell an item in your shop." },
  { id: "trash10", name: "Trash Talk", desc: "Throw away 10 junk items." },
  { id: "tool_up", name: "Tool Up", desc: "Buy your first upgrade." },
  { id: "grand", name: "A Grand Idea", desc: "Earn $1,000 in total." },
  { id: "student", name: "Student Life", desc: "Buy a Student Storage lot." },
  { id: "full_shop", name: "Fully Stocked", desc: "Fill every shop slot." },
  { id: "jackpot", name: "Hidden Jackpot", desc: "Discover a rare item while cleaning.", secret: true },
];

export const BALANCE = {
  dirtyFloor: 0.3,        // price at 0% condition = value * 0.3 ... at 100% = value * 1.0
  startCondition: [0.08, 0.45],
  scrubPerPixel: 0.0016,  // condition gained per pixel of mouse movement while scrubbing (x tool multiplier)
  junkScrap: 1,           // $ per junk item thrown away
  customerEvery: 7,       // seconds between customers (sign halves it)
  startMoney: 60,
};

export function itemPrice(item) {
  const c = item.condition, v = item.value;
  return Math.max(1, Math.round(v * (BALANCE.dirtyFloor + (1 - BALANCE.dirtyFloor) * c)));
}

export function rollLot(lot, rnd = Math.random) {
  const pool = Object.entries(ITEMS).filter(([, d]) => d.tier === lot.tier);
  const total = pool.reduce((s, [, d]) => s + d.w, 0);
  const n = lot.count[0] + Math.floor(rnd() * (lot.count[1] - lot.count[0] + 1));
  const out = [];
  for (let i = 0; i < n; i++) {
    let r = rnd() * total;
    for (const [id, d] of pool) { r -= d.w; if (r <= 0) { out.push(id); break; } }
  }
  return out;
}
