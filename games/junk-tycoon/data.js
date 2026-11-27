// Junk Lot Tycoon - all game data and balance numbers in one place (v0.3)
// 3D models: Poly Haven (CC0) in models/<model>.glb. keepX keeps only sub-objects whose centre x is in range (for multi-object sets);
// rot lays an item down [x, y, z] in radians; scale multiplies the real-world size.
const M = (model, name, value, tier, w, extra = {}) => ({ model, name, value, tier, w, ...extra });
const MYSTERY = (tier) => M("treasure_chest", "Locked Mystery Chest", 0, tier, 3, { mystery: true, scale: .55 });
const FLAT = [-Math.PI / 2, 0, 0];

export const ITEMS = {
  // ---------- Tier 1: Grandma's Garage ----------
  teaset:   M("tea_set_01", "Tea Set (1974)", 35, 1, 10),
  rocker:   M("Rockingchair_01", "Rocking Chair", 45, 1, 6),
  gnome:    M("garden_gnome", "Garden Gnome (Judging You)", 25, 1, 9),
  kettle:   M("vintage_electric_kettle", "Electric Kettle (Whistles Jazz)", 22, 1, 9),
  mantel:   M("mantel_clock_01", "Mantel Clock", 40, 1, 7, { rare: { chance: .12, value: 650, name: "Mantel Clock (Antique, 1890!)" } }),
  basket:   M("wicker_basket_01", "Wicker Basket", 12, 1, 9),
  suitcase: M("vintage_suitcase", "Vintage Suitcase", 30, 1, 8, { keepX: [0, 2] }),
  spinning: M("spinning_wheel_01", "Spinning Wheel", 70, 1, 4),
  vase:     M("ceramic_vase_01", "Ceramic Vase", 20, 1, 9),
  oillamp:  M("vintage_oil_lamp", "Oil Lamp", 28, 1, 8),
  wcan:     M("watering_can_metal_01", "Watering Can", 15, 1, 9),
  painting: M("fancy_picture_frame_01", "Painting (Probably Nothing)", 30, 1, 6, { rot: FLAT, rare: { chance: .12, value: 600, name: "Painting (SIGNED! Wait, really?)" } }),
  trashbag: M("trashbag", "Bag of... Something", 0, 1, 7, { junk: true }),
  rustcan:  M("can_rusted", "Rusty Can", 0, 1, 7, { junk: true }),
  tyre:     M("old_tyre", "Bald Tyre", 0, 1, 5, { junk: true, rot: FLAT }),
  mystery1: MYSTERY(1),
  // ---------- Tier 2: Student Storage ----------
  boombox:  M("boombox", "Boombox (Bass Boosted)", 60, 2, 8),
  tv:       M("Television_01", "CRT Television", 45, 2, 8),
  console:  M("gaming_console", "Game Console (Blow on It)", 90, 2, 5, { rare: { chance: .1, value: 900, name: "Game Console (SEALED Prototype!)" } }),
  cassette: M("portable_cassette_player", "Cassette Walkman", 35, 2, 8),
  ukulele:  M("Ukulele_01", "Ukulele (3 Strings Left)", 40, 2, 7),
  duck:     M("rubber_duck_toy", "Rubber Duck", 8, 2, 8, { rare: { chance: .15, value: 500, name: "Rubber Duck (Limited Gold Edition!)" } }),
  armchair: M("ArmChair_01", "Armchair (Suspiciously Comfy)", 80, 2, 5),
  desklamp: M("desk_lamp_arm_01", "Desk Lamp", 30, 2, 8),
  laptop:   M("classic_laptop", "Retro Laptop", 110, 2, 5),
  plchair:  M("plastic_monobloc_chair_01", "Plastic Chair", 10, 2, 7),
  gallon:   M("plastic_bottle_gallon", "Empty Gallon Jug", 0, 2, 7, { junk: true }),
  foodcans: M("russian_food_cans_01", "Expired Canned Food", 0, 2, 6, { junk: true }),
  cardbox:  M("cardboard_box_01", "Box of Instant Noodle Wrappers", 0, 2, 7, { junk: true }),
  mystery2: MYSTERY(2),
  // ---------- Tier 3: Old Repair Shop ----------
  toolchest:M("metal_tool_chest", "Rolling Tool Chest", 220, 3, 6),
  drillpress:M("drill_press_01", "Drill Press", 300, 3, 5),
  vice:     M("bench_vice_01", "Bench Vice", 90, 3, 8),
  generator:M("portable_generator", "Generator (Coughs Twice)", 380, 3, 4),
  handdrill:M("vintage_hand_drill", "Vintage Hand Drill", 110, 3, 7),
  sledge:   M("sledgehammer_01", "Sledgehammer", 60, 3, 8, { rot: [0, 0, Math.PI / 2] }),
  multimeter:M("retro_multimeter", "Retro Multimeter", 140, 3, 7),
  toolbox:  M("metal_toolbox", "Metal Toolbox", 120, 3, 8),
  microscope:M("vintage_microscope", "Brass Microscope", 180, 3, 5, { rare: { chance: .1, value: 2400, name: "Brass Microscope (Museum Piece!)" } }),
  blowtorch:M("brass_blowtorch", "Brass Blowtorch", 95, 3, 7),
  oiltin:   M("oil_tin", "Leaky Oil Tin", 0, 3, 6, { junk: true }),
  jerrycan: M("metal_jerrycan", "Dented Jerrycan", 0, 3, 6, { junk: true }),
  rim:      M("rusted_wheel_rim_01", "Rusted Wheel Rim", 0, 3, 5, { junk: true, rot: FLAT }),
  mystery3: MYSTERY(3),
  // ---------- Tier 4: Mansion Cellar ----------
  grandclock:M("vintage_grandfather_clock_01", "Grandfather Clock", 900, 4, 4),
  bust:     M("marble_bust_01", "Marble Bust", 650, 4, 5, { rare: { chance: .1, value: 5000, name: "Marble Bust (Lost Roman Original!)" } }),
  horse:    M("horse_statue_01", "Bronze Horse Statue", 300, 4, 7),
  chandelier:M("Chandelier_01", "Crystal Chandelier", 700, 4, 5),
  katana:   M("antique_katana_01", "Antique Katana", 800, 4, 5, { rot: [0, 0, Math.PI / 2] }),
  chess:    M("chess_set", "Marble Chess Set", 350, 4, 6),
  brassvase:M("brass_vase_01", "Brass Vase", 250, 4, 7),
  shield:   M("kite_shield", "Knight's Shield", 500, 4, 5, { rot: FLAT }),
  mirror:   M("ornate_mirror_01", "Ornate Mirror", 450, 4, 6, { rot: FLAT }),
  watch:    M("pocket_watch", "Pocket Watch", 380, 4, 6, { rare: { chance: .12, value: 3200, name: "Pocket Watch (Belonged to a Count!)" } }),
  wine:     M("wine_bottles_01", "Empty Wine Bottles", 0, 4, 6, { junk: true }),
  bucket:   M("wooden_bucket_01", "Bucket With a Hole", 0, 4, 6, { junk: true }),
  mystery4: MYSTERY(4),
};

export const LOTS = [
  { id: "grandma", name: "Grandma's Garage", price: 40, tier: 1, count: [6, 8], hint: "Smells like lavender and motor oil." },
  { id: "student", name: "Student Storage Unit", price: 260, tier: 2, count: [6, 9], hint: "Something in here is still alive. Probably the fridge.", needs: "van" },
  { id: "workshop", name: "Old Repair Shop", price: 700, tier: 3, count: [6, 8], hint: "Closed in 1998. The coffee is still in the mug.", needs: "truck" },
  { id: "mansion", name: "Mansion Cellar", price: 1900, tier: 4, count: [6, 8], hint: "The butler says nothing. The butler is a statue.", needs: "bigtruck" },
];

// fx: clean (x), price (x), cust (x customer rate), junk ($ per junk), rare (x chance), walk (x speed), tables (+), baths (+), bathSpeed (x), xp (x), online (+ listing spots), onlineSpeed (x)
export const UPGRADES = [
  { id: "sponge",   cat: "Cleaning", name: "Sponge",              desc: "Scrub 2x faster.",                         price: 60,    lvl: 1, fx: { clean: 2 } },
  { id: "brush",    cat: "Cleaning", name: "Wire Brush",          desc: "Scrub 1.5x faster.",                       price: 220,   lvl: 2, needs: "sponge", fx: { clean: 1.5 } },
  { id: "washer",   cat: "Cleaning", name: "Pressure Washer",     desc: "Scrub 2.5x faster. Very loud.",            price: 650,   lvl: 3, needs: "brush", fx: { clean: 2.5 } },
  { id: "steam",    cat: "Cleaning", name: "Steam Cleaner",       desc: "Scrub 2x faster. Grandma approves.",       price: 2200,  lvl: 5, needs: "washer", fx: { clean: 2 } },
  { id: "laser",    cat: "Cleaning", name: "Laser Cleaner",       desc: "Scrub 3x faster. Pew pew.",                price: 7500,  lvl: 7, needs: "steam", fx: { clean: 3 } },
  { id: "bath1",    cat: "Automation", name: "Ultrasonic Bath",    desc: "Put an item in, it cleans itself.",        price: 700,   lvl: 3, fx: { baths: 1 } },
  { id: "bath2",    cat: "Automation", name: "Second Bath",        desc: "Another self-cleaning bath.",              price: 2600,  lvl: 5, needs: "bath1", fx: { baths: 1 } },
  { id: "turbo",    cat: "Automation", name: "Turbo Bubbles",      desc: "Baths clean 2.5x faster.",                 price: 4200,  lvl: 6, needs: "bath1", fx: { bathSpeed: 2.5 } },
  { id: "camera",   cat: "Online", name: "Photo Camera",          desc: "Unlocks the JunkBay photo table: sell online for +30%.", price: 350, lvl: 2, fx: { online: 1 } },
  { id: "camera2",  cat: "Online", name: "Second Photo Table",    desc: "List two items online at once.",          price: 1500,  lvl: 4, needs: "camera", fx: { online: 1 } },
  { id: "seo",      cat: "Online", name: "Clickbait Titles",      desc: "Online offers arrive 2x faster.",         price: 1100,  lvl: 4, needs: "camera", fx: { onlineSpeed: 2 } },
  { id: "flyers",   cat: "Shop", name: "Flyers on Every Lamppost", desc: "Customers come 1.25x more often.",         price: 90,    lvl: 1, fx: { cust: 1.25 } },
  { id: "table2",   cat: "Shop", name: "Second Table",           desc: "+4 shop slots.",                            price: 160,   lvl: 1, fx: { tables: 1 } },
  { id: "sign",     cat: "Shop", name: "Shop Sign",              desc: "Customers come 1.6x more often.",          price: 260,   lvl: 2, fx: { cust: 1.6 } },
  { id: "tags",     cat: "Shop", name: "Fancy Price Tags",       desc: "Everything sells for 10% more.",           price: 380,   lvl: 2, fx: { price: 1.1 } },
  { id: "table3",   cat: "Shop", name: "Third Table",            desc: "+4 shop slots.",                            price: 1300,  lvl: 4, needs: "table2", fx: { tables: 1 } },
  { id: "lights",   cat: "Shop", name: "Showroom Lights",        desc: "Everything sells for 15% more.",           price: 1900,  lvl: 4, needs: "tags", fx: { price: 1.15 } },
  { id: "billboard",cat: "Shop", name: "Highway Billboard",      desc: "Customers come 1.6x more often.",          price: 3200,  lvl: 6, needs: "sign", fx: { cust: 1.6 } },
  { id: "van",      cat: "Lots", name: "Bigger Van",             desc: "Unlocks Student Storage lots.",            price: 400,   lvl: 2, fx: {} },
  { id: "truck",    cat: "Lots", name: "Box Truck",              desc: "Unlocks Old Repair Shop lots.",            price: 1600,  lvl: 4, needs: "van", fx: {} },
  { id: "bigtruck", cat: "Lots", name: "Semi Truck",             desc: "Unlocks Mansion Cellar lots.",             price: 5200,  lvl: 6, needs: "truck", fx: {} },
  { id: "paddle",   cat: "Lots", name: "Auction Paddle",         desc: "Unlocks storage auctions on the LOTS board.", price: 450, lvl: 3, fx: {} },
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
  { id: "workshop",  name: "Grease Monkey",       desc: "Buy an Old Repair Shop lot." },
  { id: "mansion",   name: "Old Money",           desc: "Buy a Mansion Cellar lot." },
  { id: "full_shop", name: "Fully Stocked",       desc: "Fill every shop slot." },
  { id: "automation",name: "Let the Bubbles Work",desc: "Clean an item in an Ultrasonic Bath." },
  { id: "online",    name: "Going Viral",         desc: "Sell an item online on JunkBay." },
  { id: "auction",   name: "Going Once, Going Twice", desc: "Win a storage auction." },
  { id: "streak5",   name: "On Fire",             desc: "Reach a x5 sales streak." },
  { id: "sold50",    name: "Shopkeeper",          desc: "Sell 50 items." },
  { id: "jackpot",   name: "Hidden Jackpot",      desc: "Discover a rare item while cleaning.", secret: true },
  { id: "mystery",   name: "What's in the Chest?", desc: "Open a Locked Mystery Chest.", secret: true },
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
  onlineBonus: 1.3,       // JunkBay pays 30% more than the shop
  onlineWait: [25, 60],   // seconds until an online offer arrives (divided by onlineSpeed)
  xpForLevel: (lvl) => Math.round(100 * Math.pow(1.55, lvl - 1)),
};

export function rollLot(lot, rnd = Math.random, extra = 0) {
  const pool = Object.entries(ITEMS).filter(([, d]) => d.tier === lot.tier);
  const total = pool.reduce((s, [, d]) => s + d.w, 0);
  const n = lot.count[0] + Math.floor(rnd() * (lot.count[1] - lot.count[0] + 1)) + extra;
  const out = [];
  for (let i = 0; i < n; i++) {
    let r = rnd() * total;
    for (const [id, d] of pool) { r -= d.w; if (r <= 0) { out.push(id); break; } }
  }
  return out;
}

export const TUTORIAL = [
  { text: "Welcome to your yard! Walk to the <b>LOTS</b> chalkboard and buy <b>Grandma's Garage</b>.", target: "board", reward: 0 },
  { text: "The shutter is open! Walk in and <b>pick up an item</b> with <b>E</b> (or click).", target: "garage", reward: 10 },
  { text: "Carry it to the <b>WORKBENCH</b> and press <b>E</b> to put it down.", target: "bench", reward: 10 },
  { text: "<b>Hold the mouse button and move the mouse</b> to scrub off the grime. Get it to <b>100%</b>!", target: "bench", reward: 15 },
  { text: "Clean = expensive. Pick it up and put it on a <b>shop table</b>.", target: "table", reward: 10 },
  { text: "Wait for a customer to buy it. Meanwhile, clean the next item!", target: "table", reward: 20 },
  { text: "Open the <b>COMPUTER</b> and check the <b>Requests</b> tab: people pay extra for special orders.", target: "computer", reward: 15 },
  { text: "Buy your <b>first upgrade</b> on the computer. Tip: the <b>Sponge</b> doubles your scrubbing speed.", target: "computer", reward: 30 },
];
