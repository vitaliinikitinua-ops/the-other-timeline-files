// CHARACTER BIBLE - The Other Timeline (3D, rounded "clay" style). Reuse these in every video; add new ones here.
// Fields: name/role (for the writer), skin, top (main clothing colour), accent, pants, shoes,
//   outfit: hoodie | tee | shirt | suit | blazer | cardigan | coat | apron | labcoat | vest | dress
//   hair: {style, color}  styles: none, short, side (bald top), long, ponytail, bob, curly, spiky, bun, slick, cap, capback, fedora, hood
//   face: overlays drawn on the face: glasses, sunglasses, mustache, beard, freckles, lashes
//   acc: 3D extras: tie(color), chain, earrings, badge, stethoscope, headphones, phone, keys, nametag
//   height: 1 = adult (kid 0.72, teen 0.9), belly: 0..1
export const CAST = {
  // ---- core cast (since EP01)
  you:        { name: "Karl", role: "MAIN HERO of every video (user decision 28.11.2026): Karl = the viewer's avatar, main hero of every timeline", skin: 0xf6ead2, top: 0xffb02e, accent: 0xe8962f, pants: 0x3a4a6b, outfit: "hoodie", hair: { style: "hood", color: 0xe8962f } },
  max:        { name: "Max", role: "friend, bad influence, impulsive spender, bad timing", skin: 0xf0cdaa, top: 0xff6b5b, pants: 0x2f3542, outfit: "tee", hair: { style: "spiky", color: 0x3c281e } },
  grandma:    { name: "Grandma", role: "wise saver, 'compound interest' voice", skin: 0xf5dec8, top: 0x9a6edc, pants: 0x5b4a7a, outfit: "cardigan", hair: { style: "bun", color: 0xe6e6ee }, face: ["glasses"] },
  banker:     { name: "Banker", role: "bank, loans, credit cards, mortgages", skin: 0xa06e4b, top: 0x28375a, pants: 0x19233c, outfit: "suit", hair: { style: "short", color: 0x1e1919 }, acc: ["tie:0x38c6b4"] },
  // ---- 15 added 28.11.2026
  dad:        { name: "Dad", role: "family budget, salary, mortgage, 'back in my day'", skin: 0xf0c8a0, top: 0x4a7fc1, pants: 0xb59a6a, outfit: "shirt", hair: { style: "short", color: 0x6b4a2e }, face: ["mustache"], belly: 0.35 },
  mom:        { name: "Mom", role: "family budget, groceries, kids' savings", skin: 0xf3d2b3, top: 0x3fa874, pants: 0x2e3a55, outfit: "shirt", hair: { style: "ponytail", color: 0x7a4a2a }, face: ["lashes"], acc: ["earrings"] },
  boss:       { name: "The Boss", role: "employer, raises, layoffs, overtime", skin: 0xf2c9a6, top: 0x5c6370, pants: 0x3a3f48, outfit: "suit", hair: { style: "side", color: 0x8a8a8a }, face: ["glasses"], acc: ["tie:0xd94848"], belly: 0.5 },
  coworker:   { name: "Coworker Sam", role: "office life, side hustles, comparisons", skin: 0x8d5a3b, top: 0x9fd0f0, pants: 0x34405a, outfit: "shirt", hair: { style: "curly", color: 0x1c1410 }, acc: ["badge"] },
  landlord:   { name: "Landlord", role: "rent, deposits, rent increases", skin: 0xe8b996, top: 0x7a5a3a, pants: 0x4a4038, outfit: "vest", hair: { style: "none", color: 0x000000 }, face: ["beard"], acc: ["keys"], belly: 0.8 },
  realtor:    { name: "Realtor", role: "buying/selling houses, 'prices only go up'", skin: 0xf7d7bf, top: 0xd94a8c, pants: 0x2b2b3a, outfit: "blazer", hair: { style: "bob", color: 0xf0c85a }, face: ["lashes"], acc: ["earrings"] },
  car_dealer: { name: "Car Dealer", role: "car loans, upsells, 'only $499 a month'", skin: 0xf0c49c, top: 0xc0392b, pants: 0x222a35, outfit: "blazer", hair: { style: "slick", color: 0x2a1a10 }, face: ["sunglasses"], acc: ["chain"] },
  crypto_bro: { name: "Crypto Bro", role: "crypto hype, FOMO, 'to the moon'", skin: 0xf2cfae, top: 0x22252e, pants: 0x3a3f4a, outfit: "hoodie", hair: { style: "capback", color: 0x1e88e5 }, face: ["sunglasses"], acc: ["chain"] },
  scammer:    { name: "Scammer", role: "too-good-to-be-true offers, fraud warnings", skin: 0xd9b08c, top: 0x3a3a46, pants: 0x26262e, outfit: "coat", hair: { style: "fedora", color: 0x2a2a2a }, face: ["mustache"] },
  kid:        { name: "Kid Leo", role: "kids & money, piggy bank, allowance, 'from birth' accounts", skin: 0xf7dcc4, top: 0x5ac85a, pants: 0x3a5a9a, outfit: "tee", hair: { style: "cap", color: 0xe03c3c }, face: ["freckles"], height: 0.72 },
  teen:       { name: "Teen Mia", role: "first job, first card, student loans, saving at 16", skin: 0xe9c09b, top: 0x8e5bd8, pants: 0x2c2c3c, outfit: "hoodie", hair: { style: "long", color: 0x2a1a14 }, acc: ["headphones"], height: 0.9 },
  grandpa:    { name: "Grandpa", role: "pension, 'a dollar bought more', old prices", skin: 0xf2d4bb, top: 0x8a6a4a, pants: 0x4a4a52, outfit: "cardigan", hair: { style: "side", color: 0xeeeeee }, face: ["glasses", "mustache"] },
  cashier:    { name: "Cashier", role: "shopping, prices, inflation at the till", skin: 0xc68e62, top: 0xf2f2f2, accent: 0xd93c3c, pants: 0x2e2e3a, outfit: "apron", hair: { style: "cap", color: 0xd93c3c }, acc: ["nametag"] },
  doctor:     { name: "Doctor", role: "health costs, insurance, emergency funds", skin: 0xf3d0b0, top: 0xf7f7f7, accent: 0x5ab3e0, pants: 0x3a5f8a, outfit: "labcoat", hair: { style: "short", color: 0x9a9a9a }, acc: ["stethoscope"] },
  influencer: { name: "Influencer", role: "lifestyle creep, buy-now-pay-later, 'link in bio'", skin: 0xf6d6c0, top: 0xff8ac6, pants: 0xf0f0f5, outfit: "tee", hair: { style: "long", color: 0xf3d77a }, face: ["lashes", "sunglasses_up"], acc: ["phone"] },
};
