const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const out = process.argv[2], dur = +process.argv[3] || 15, fps = 30; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'] });
  const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8790/finance_series/engine3d/demo.html'); await p.waitForFunction(() => window.ready, null, { timeout: 60000 });
  const n = Math.round(dur * fps), t0 = Date.now();
  for (let i = 0; i < n; i++) { const d = await p.evaluate((t) => window.renderDemo(t), i / fps); fs.writeFileSync(`${out}/f_${String(i).padStart(4,'0')}.jpg`, Buffer.from(d.split(',')[1], 'base64')); if (i % 90 === 0) console.log(i, ((Date.now()-t0)/1000).toFixed(0)+'s'); }
  console.log('done', n, 'errors', JSON.stringify(errs.slice(0,5)));
  await b.close();
})();
