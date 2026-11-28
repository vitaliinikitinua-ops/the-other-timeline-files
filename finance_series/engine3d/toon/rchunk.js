// node rchunk.js "<page?query>" <out.mp4> <t0> <t1>  | node rchunk.js "<page?query>" events <out.json>
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { spawn } = require('child_process');
(async () => {
  const [page, a, b, c] = process.argv.slice(2);
  const br = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const ROOT = path.join(__dirname, '..', '..', '..');
  const TYPES = { '.js': 'text/javascript', '.html': 'text/html', '.ttf': 'font/ttf', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg' };
  await p.route('http://local/**', r => { const f = path.join(ROOT, decodeURIComponent(new URL(r.request().url()).pathname));
    if (!f.startsWith(ROOT) || !fs.existsSync(f)) return r.fulfill({ status: 404, body: '' });
    r.fulfill({ status: 200, contentType: TYPES[path.extname(f)] || 'application/octet-stream', body: fs.readFileSync(f) }); });
  await p.goto(`http://local/finance_series/engine3d/toon/${page}`);
  try { await p.waitForFunction(() => window.ready, null, { timeout: 180000 }); } catch (e) { console.log('NOT READY', JSON.stringify(errs)); process.exit(1); }
  if (a === 'events') { fs.writeFileSync(b, JSON.stringify(await p.evaluate(() => window.eventsList()))); await br.close(); return; }
  if (a === 'stills') { fs.mkdirSync(b, { recursive: true }); for (const t of c.split(',')) { let d; try { d = await p.evaluate(t => window.renderAt(t), +t); } catch (e) { console.log('ERR at', t, e.message.slice(0, 300)); continue; } fs.writeFileSync(path.join(b, `s_${(+t).toFixed(2)}.jpg`), Buffer.from(d.split(',')[1], 'base64')); } if (errs.length) console.log('errors', JSON.stringify(errs.slice(0, 5))); await br.close(); return; }
  const fps = 30, f0 = Math.round(+b * fps), f1 = Math.round(+c * fps), t0 = Date.now();
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', a], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = f0; f < f1; f++) { const buf = Buffer.from((await p.evaluate(t => window.renderAt(t), f / fps)).split(',')[1], 'base64'); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if ((f - f0) % 300 === 0) console.log(a, f - f0, f1 - f0, ((Date.now() - t0) / 1000).toFixed(0) + 's'); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  if (errs.length) console.log('page errors', JSON.stringify(errs.slice(0, 5)));
  await br.close();
})();
