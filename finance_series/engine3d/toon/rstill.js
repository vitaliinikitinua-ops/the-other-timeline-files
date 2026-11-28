// node rstill.js <page.html> <out_dir> <t1,t2,...>  -> still_<t>.jpg  (Playwright routing, no server)
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [page, out, ts] = process.argv.slice(2);
  const br = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const ROOT = path.join(__dirname, '..', '..', '..');
  const TYPES = { '.js': 'text/javascript', '.html': 'text/html', '.ttf': 'font/ttf', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg' };
  await p.route('http://local/**', r => { const f = path.join(ROOT, decodeURIComponent(new URL(r.request().url()).pathname));
    if (!f.startsWith(ROOT) || !fs.existsSync(f)) return r.fulfill({ status: 404, body: '' });
    r.fulfill({ status: 200, contentType: TYPES[path.extname(f)] || 'application/octet-stream', body: fs.readFileSync(f) }); });
  await p.goto(`http://local/finance_series/engine3d/toon/${page}`);
  try { await p.waitForFunction(() => window.ready, null, { timeout: 120000 }); } catch (e) { console.log('NOT READY', errs); process.exit(1); }
  fs.mkdirSync(out, { recursive: true });
  for (const t of ts.split(',')) { const d = await p.evaluate(t => window.renderAt(t), +t); fs.writeFileSync(path.join(out, `still_${t}.jpg`), Buffer.from(d.split(',')[1], 'base64')); }
  if (errs.length) console.log('page errors', JSON.stringify(errs.slice(0, 5)));
  await br.close();
})();
