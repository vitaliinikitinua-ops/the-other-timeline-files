// Junk Lot Tycoon - all game data and balance numbers in one place (prototype v0.2)
// Part shapes: box | cyl | sph | cone | tor.  P(shape, sx, sy, sz, x, y, z, color)  (y = centre height above the item's bottom)
const P = (s, sx, sy, sz, x, y, z, c) => ({ s, sx, sy, sz, x, y, z, c });
const MYSTERY = (tier) => ({ name: "Locked Mystery Box", value: 0, tier, w: 3, mystery: true, parts: [
  P("box", .45, .4, .45, 0, .2, 0, 0x6a4b8c), P("box", .47, .06, .47, 0, .36, 0, 0xd9b44a), P("box", .08, .12, .03, 0, .25, .24, 0xd9b44a)] });

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
  mystery1: MYSTERY(1),
  // ---------- Tier 2: Student Storage ----------
  guitar:   { name: "Guitar (3 Strings Left)", value: 70, tier: 2, w: 8, parts: [
    P("sph", .3, .08, .38, 0, .04, 0, 0xc9772f), P("box", .07, .03, .55, 0, .05, .45, 0x5a3a1a), P("cyl", .07, .02, .07, 0, .09, 0, 0x222222)] },
  fridge:   { name: "Mini Fridge (Smells Brave)", value: 90, tier: 2, w: 6, parts: [
    P("box", .5, .7, .5, 0, .35, 0, 0xeeeeee), P("box", .03, .2, .03, .2, .45, .26, 0x888888)] },
  gchair:   { name: "Gaming Chair (RGB Not Included)", value: 110, tier: 2, w: 5, parts: [
    P("box", .55, .1, .55, 0, .5, 0, 0x202020), P("box", .55, .75, .1, 0, .9, -.25, 0xc02040), P("cyl", .05, .45, .05, 0, .23, 0, 0x555555), P("cyl", .3, .04, .3, 0, .03, 0, 0x333333)] },
  cans:     { name: "Can Pyramid (400 Cans)", value: 30, tier: 2, w: 7, parts: [P("cone", .45, .7, .45, 0, .35, 0, 0xbfc7cf)] },
  sofa:     { name: "Suspiciously New Sofa", value: 180, tier: 2, w: 3, parts: [
    P("box", 1.4, .4, .7, 0, .2, 0, 0x3a6ea5), P("box", 1.4, .45, .15, 0, .6, -.28, 0x3a6ea5), P("box", .15, .25, .7, .63, .52, 0, 0x30598a), P("box", .15, .25, .7, -.63, .52, 0, 0x30598a)] },
  lavalamp: { name: "Lava Lamp (Still Lava-ing)", value: 35, tier: 2, w: 8, parts: [P("cone", .12, .12, .12, 0, .06, 0, 0x777777), P("cyl", .08, .35, .08, 0, .29, 0, 0xff5a8a)] },
  skate:    { name: "Skateboard", value: 45, tier: 2, w: 8, parts: [
    P("box", .2, .03, .8, 0, .09, 0, 0x2c2c2c), P("cyl", .03, .04, .03, .07, .03, .3, 0xffffff), P("cyl", .03, .04, .03, -.07, .03, .3, 0xffffff), P("cyl", .03, .04, .03, .07, .03, -.3, 0xffffff), P("cyl", .03, .04, .03, -.07, .03, -.3, 0xffffff)] },
  console:  { name: "Retro Console (Blow on It)", value: 140, tier: 2, w: 4, rare: { chance: .1, value: 900, name: "Retro Console (SEALED Prototype!)" }, parts: [
    P("box", .45, .1, .3, 0, .05, 0, 0x9a9aa8), P("box", .12, .03, .08, -.1, .11, .08, 0x333333)] },
  pizza:    { name: "Empty Pizza Box (Hope Dies)", value: 0, tier: 2, w: 8, junk: true, parts: [P("box", .45, .05, .45, 0, .025, 0, 0xd8b98a)] },
  noodles:  { name: "Ancient Instant Noodles", value: 0, tier: 2, w: 6, junk: true, parts: [P("cyl", .12, .12, .12, 0, .06, 0, 0xf4f0e0)] },
  mystery2: MYSTERY(2),
  // ---------- Tier 3: Closed Pizzeria ----------
  oven:     { name: "Pizza Oven (Still Warm?!)", value: 260, tier: 3, w: 5, parts: [
    P("box", .9, .6, .7, 0, .3, 0, 0x8a3b2b), P("sph", .35, .3, .3, 0, .75, 0, 0x8a3b2b), P("box", .4, .2, .05, 0, .35, .36, 0x111111)] },
  arcade:   { name: "Arcade Cabinet (Insert Coin)", value: 380, tier: 3, w: 4, rare: { chance: .1, value: 2400, name: "Arcade Cabinet (World Record Inside!)" }, parts: [
    P("box", .7, 1.6, .6, 0, .8, 0, 0x2a2a6a), P("box", .55, .4, .05, 0, 1.15, .31, 0x40e0ff), P("box", .6, .1, .3, 0, .8, .35, 0x1a1a1a)] },
  neon:     { name: "Neon 'OPEN' Sign (Mostly 'OPE')", value: 140, tier: 3, w: 7, parts: [P("box", .9, .4, .06, 0, .2, 0, 0x222222), P("box", .75, .08, .07, 0, .2, 0, 0xff3aa0)] },
  bigpizza: { name: "Giant Wooden Pizza", value: 110, tier: 3, w: 7, parts: [P("cyl", .55, .06, .55, 0, .03, 0, 0xe0a050), P("cyl", .45, .02, .45, 0, .07, 0, 0xc0392b)] },
  mixer:    { name: "Industrial Dough Mixer", value: 190, tier: 3, w: 5, parts: [P("cyl", .3, .5, .3, 0, .25, 0, 0xbbbbbb), P("box", .2, .5, .2, 0, .75, -.2, 0x999999)] },
  jukebox:  { name: "Jukebox (Plays Only Polka)", value: 320, tier: 3, w: 4, parts: [P("box", .7, 1.2, .5, 0, .6, 0, 0xb5651d), P("sph", .35, .2, .25, 0, 1.25, 0, 0xffd27a)] },
  redchair: { name: "Red Diner Chair", value: 55, tier: 3, w: 9, parts: [P("cyl", .22, .06, .22, 0, .48, 0, 0xd62828), P("cyl", .03, .45, .03, 0, .23, 0, 0xcccccc), P("box", .4, .35, .05, 0, .7, -.2, 0xd62828)] },
  crust:    { name: "Fossilized Crust", value: 0, tier: 3, w: 6, junk: true, parts: [P("tor", .15, .15, .04, 0, .05, 0, 0xc49a5a)] },
  sauce:    { name: "Mystery Sauce Bucket", value: 0, tier: 3, w: 6, junk: true, parts: [P("cyl", .18, .3, .18, 0, .15, 0, 0x8a1c1c)] },
  mystery3: MYSTERY(3),
  // ---------- Tier 4: Circus Wagon ----------
  unicycle: { name: "World's Tallest Unicycle", value: 420, tier: 4, w: 6, parts: [P("tor", .25, .25, .04, 0, .25, 0, 0x222222), P("cyl", .03, 1.5, .03, 0, 1.0, 0, 0xd0d0d0), P("box", .3, .06, .12, 0, 1.75, 0, 0xd62828)] },
  cannon:   { name: "Human Cannon (Used Once)", value: 1300, tier: 4, w: 3, parts: [P("cyl", .3, 1.6, .3, 0, .9, 0, 0xd62828), P("tor", .32, .32, .06, 0, 1.7, 0, 0xffd700), P("box", .9, .3, .6, 0, .15, 0, 0x2c3e8c)] },
  pins:     { name: "Juggling Pins (One Is Haunted)", value: 120, tier: 4, w: 8, parts: [P("cone", .06, .45, .06, -.1, .22, 0, 0xffffff), P("cone", .06, .45, .06, .1, .22, 0, 0xd62828), P("cone", .06, .45, .06, 0, .22, .1, 0x2c7be5)] },
  hat:      { name: "Ringmaster Top Hat", value: 260, tier: 4, w: 7, rare: { chance: .12, value: 3500, name: "Ringmaster Top Hat (Has a Real Rabbit!)" }, parts: [P("cyl", .25, .03, .25, 0, .015, 0, 0x111111), P("cyl", .15, .3, .15, 0, .18, 0, 0x111111), P("cyl", .155, .05, .155, 0, .08, 0, 0xc0392b)] },
  tinybike: { name: "Tiny Clown Bicycle", value: 300, tier: 4, w: 6, parts: [P("tor", .1, .1, .02, .15, .1, 0, 0x222222), P("tor", .1, .1, .02, -.15, .1, 0, 0x222222), P("box", .32, .03, .03, 0, .18, 0, 0xff7ac8)] },
  stool:    { name: "Lion Tamer's Stool", value: 160, tier: 4, w: 8, parts: [P("cyl", .3, .05, .3, 0, .6, 0, 0xffd700), P("cyl", .25, .58, .25, 0, .29, 0, 0xd62828)] },
  horn:     { name: "Clown Car Horn (HONK)", value: 90, tier: 4, w: 8, parts: [P("sph", .1, .1, .1, -.15, .1, 0, 0xd62828), P("cone", .1, .25, .1, .05, .1, 0, 0xffd700)] },
  confetti: { name: "Used Confetti", value: 0, tier: 4, w: 6, junk: true, parts: [P("sph", .25, .1, .25, 0, .05, 0, 0xff66cc)] },
  elephant: { name: "Something That Smells Like Elephant", value: 0, tier: 4, w: 5, junk: true, parts: [P("sph", .3, .3, .3, 0, .3, 0, 0x7a7a7a)] },
  mystery4: MYSTERY(4),
};

export const LOTS = [
  { id: "grandma", name: "Grandma's Garage", price: 40, tier: 1, count: [6, 8], hint: "Smells like lavender and motor oil." },
  { id: "student", name: "Student Storage Unit", price: 260, tier: 2, count: [6, 9], hint: "Something in here is still alive. Probably the fridge.", needs: "van" },
  { id: "pizzeria", name: "Closed Pizzeria", price: 700, tier: 3, count: [6, 8], hint: "Closed in 1998. The cheese is still there.", needs: "truck" },
  { id: "circus", name: "Abandoned Circus Wagon", price: 1900, tier: 4, count: [6, 8], hint: "Do NOT open the small door. (You will open the small door.)", needs: "bigtruck" },
];

// fx: clean (x), price (x), cust (x customer rate), junk ($ per junk), rare (x chance), walk (x speed), tables (+), baths (+), bathSpeed (x), xp (x)
export const UPGRADES = [
  { id: "sponge",   cat: "Cleaning", name: "Sponge",              desc: "Scrub 2x faster.",                         price: 60,    lvl: 1, fx: { clean: 2 } },
  { id: "brush",    cat: "Cleaning", name: "Wire Brush",          desc: "Scrub 1.5x faster.",                       price: 220,   lvl: 2, needs: "sponge", fx: { clean: 1.5 } },
  { id: "washer",   cat: "Cleaning", name: "Pressure Washer",     desc: "Scrub 2.5x faster. Very loud.",            price: 650,   lvl: 3, needs: "brush", fx: { clean: 2.5 } },
  { id: "steam",    cat: "Cleaning", name: "Steam Cleaner",       desc: "Scrub 2x faster. Grandma approves.",       price: 2200,  lvl: 5, needs: "washer", fx: { clean: 2 } },
  { id: "laser",    cat: "Cleaning", name: "Laser Cleaner",       desc: "Scrub 3x faster. Pew pew.",                price: 7500,  lvl: 7, needs: "steam", fx: { clean: 3 } },
  { id: "bath1",    cat: "Automation", name: "Ultrasonic Bath",    desc: "Put an item in, it cleans itself.",        price: 700,   lvl: 3, fx: { baths: 1 } },
  { id: "bath2",    cat: "Automation", name: "Second Bath",        desc: "Another self-cleaning bath.",              price: 2600,  lvl: 5, needs: "bath1", fx: { baths: 1 } },
  { id: "turbo",    cat: "Automation", name: "Turbo Bubbles",      desc: "Baths clean 2.5x faster.",                 price: 4200,  lvl: 6, needs: "bath1", fx: { bathSpeed: 2.5 } },
  { id: "flyers",   cat: "Shop", name: "Flyers on Every Lamppost", desc: "Customers come 1.25x more often.",         price: 90,    lvl: 1, fx: { cust: 1.25 } },
  { id: "table2",   cat: "Shop", name: "Second Table",           desc: "+4 shop slots.",                            price: 160,   lvl: 1, fx: { tables: 1 } },
  { id: "sign",     cat: "Shop", name: "Shop Sign",              desc: "Customers come 1.6x more often.",          price: 260,   lvl: 2, fx: { cust: 1.6 } },
  { id: "tags",     cat: "Shop", name: "Fancy Price Tags",       desc: "Everything sells for 10% more.",           price: 380,   lvl: 2, fx: { price: 1.1 } },
  { id: "table3",   cat: "Shop", name: "Third Table",            desc: "+4 shop slots.",                            price: 1300,  lvl: 4, needs: "table2", fx: { tables: 1 } },
  { id: "lights",   cat: "Shop", name: "Showroom Lights",        desc: "Everything sells for 15% more.",           price: 1900,  lvl: 4, needs: "tags", fx: { price: 1.15 } },
  { id: "billboard",cat: "Shop", name: "Highway Billboard",      desc: "Customers come 1.6x more often.",          price: 3200,  lvl: 6, needs: "sign", fx: { cust: 1.6 } },
  { id: "van",      cat: "Lots", name: "Bigger Van",             desc: "Unlocks Student Storage lots.",            price: 400,   lvl: 2, fx: {} },
  { id: "truck",    cat: "Lots", name: "Box Truck",              desc: "Unlocks Closed Pizzeria lots.",            price: 1600,  lvl: 4, needs: "van", fx: {} },
  { id: "bigtruck", cat: "Lots", name: "Semi Truck",             desc: "Unlocks Circus Wagon lots.",               price: 5200,  lvl: 6, needs: "truck", fx: {} },
  { id: "coffee",   cat: "Perks", name: "Coffee Machine",        desc: "Walk 25% faster.",                         price: 120,   lvl: 1, fx: { walk: 1.25 } },
  { id: "recycle",  cat: "Perks", name: "Recycling Contract",    desc: "Junk pays $5 instead of $1.",              price: 300,   lvl: 2, fx: { junk: 5 } },
  { id: "magnifier",cat: "Perks", name: "Appraiser's Magnifier", desc: "Rare items appear 1.5x more often.",       price: 500,   lvl: 3, fx: { rare: 1.5 } },
  { id: "gloves",   cat: "Perks", name: "Lucky Gloves",          desc: "Rare items appear 1.5x more often again.", price: 2400,  lvl: 5, needs: "magnifier", fx: { rare: 1.5 } },
  { id: "notebook", cat: "Perks", name: "Business Notebook",     desc: "+25% XP from everything.",                 price: 800,   lvl: 3, fx: { xp: 1.25 } },
];

export const ACHIEVEMENTS = [
  { id: "tutorial",  name: "Junk 101",            desc: "Finish the tutorial." },
  { id: "first_lot", name: "First Junk",          desc: "Buy your first lot." },
  { id: "shiny",     name: "Shiny!",              desc: "Restore an item to 100%." },
  { id: "first_sale",name: "First Sale",          desc: "Sell an item in your shop." },
  { id: "trash10",   name: "Trash Talk",          desc: "Recycle 10 junk items." },
  { id: "tool_up",   name: "Tool Up",             desc: "Buy your first upgrade." },
  { id: "request1",  name: "At Your Service",     desc: "Complete a request." },
  { id: "request10", name: "Busy Bee",            desc: "Complete 10 requests." },
  { id: "lvl5",      name: "Junk Apprentice",     desc: "Reach level 5." },
  { id: "lvl10",     name: "Junk Lord",           desc: "Reach level 10." },
  { id: "grand",     name: "A Grand Idea",        desc: "Earn $1,000 in total." },
  { id: "rich",      name: "Five Figures",        desc: "Earn $10,000 in total." },
  { id: "student",   name: "Student Life",        desc: "Buy a Student Storage lot." },
  { id: "pizza",     name: "Pizza Time",          desc: "Buy a Closed Pizzeria lot." },
  { id: "circus",    name: "Under the Big Top",   desc: "Buy a Circus Wagon lot." },
  { id: "full_shop", name: "Fully Stocked",       desc: "Fill every shop slot." },
  { id: "automation",name: "Let the Bubbles Work",desc: "Clean an item in an Ultrasonic Bath." },
  { id: "streak5",   name: "On Fire",             desc: "Reach a x5 sales streak." },
  { id: "sold50",    name: "Shopkeeper",          desc: "Sell 50 items." },
  { id: "jackpot",   name: "Hidden Jackpot",      desc: "Discover a rare item while cleaning.", secret: true },
  { id: "mystery",   name: "What's in the Box?",  desc: "Open a Locked Mystery Box.", secret: true },
  { id: "whale",     name: "Big Ticket",          desc: "Sell a single item for $1,000 or more." },
  { id: "allup",     name: "Fully Loaded",        desc: "Buy every upgrade." },
];

export const BALANCE = {
  dirtyFloor: 0.3,        // price at 0% condition = value * 0.3 ... at 100% = value * 1.0
  startCondition: [0.08, 0.45],
  scrubPerPixel: 0.0016,  // condition per pixel of mouse movement while scrubbing (x tool multiplier)
  bathRate: 0.025,        // condition per second in an ultrasonic bath (x bathSpeed)
  customerEvery: 7,       // seconds between customers (divided by cust multipliers)
  startMoney: 60,
  streakWindow: 18,       // seconds between sales to keep the streak
  streakBonus: 0.05,      // +5% price per streak step (max x5)
  levelPriceBonus: 0.02,  // +2% sale price per level above 1
  xpForLevel: (lvl) => Math.round(100 * Math.pow(1.55, lvl - 1)),
};

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

// Tutorial steps. done(S, G) is checked every frame; target names a world spot for the arrow.
export const TUTORIAL = [
  { text: "Welcome to your yard! Walk to the <b>LOTS FOR SALE</b> board and buy <b>Grandma's Garage</b>.", target: "board", reward: 0 },
  { text: "The garage is open! Walk in and <b>pick up an item</b> with <b>E</b> (or click).", target: "garage", reward: 10 },
  { text: "Carry it to the <b>WORKBENCH</b> and press <b>E</b> to put it down.", target: "bench", reward: 10 },
  { text: "<b>Hold the mouse button and move the mouse</b> to scrub it. Get it to <b>100%</b>!", target: "bench", reward: 15 },
  { text: "Clean = expensive. Pick it up and put it on a <b>shop table</b>.", target: "table", reward: 10 },
  { text: "Wait for a customer to buy it. Meanwhile, clean the next item!", target: "table", reward: 20 },
  { text: "Open the <b>COMPUTER</b> and check the <b>Requests</b> tab: people pay extra for special orders.", target: "computer", reward: 15 },
  { text: "Buy your <b>first upgrade</b> on the computer. Tip: the <b>Sponge</b> doubles your scrubbing speed.", target: "computer", reward: 30 },
];
