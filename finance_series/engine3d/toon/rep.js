// node rep.js "<episode.html?query>" video <out.mp4> <t0> <t1> [fn=renderAt]   -> frames t0..t1 piped to ffmpeg (30 fps)
// node rep.js "<episode.html?query>" stills <out_dir> <t1,t2,...> [fn]          -> jpg per time
// Pages are served from the repo root through Playwright routing (no local server).
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { spawn } = require('child_process');
(async () => {
  const [page, mode, out, a, b, fn0] = process.argv.slice(2);
  const q = new URLSearchParams(page.split('?')[1] || ''); const W = +(q.get('w') || 1920), H = +(q.get('h') || 1080);
  const br = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await br.newPage({ viewport: { width: W, height: H } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const ROOT = path.join(__dirname, '..', '..', '..');
  const TYPES = { '.js': 'text/javascript', '.html': 'text/html', '.ttf': 'font/ttf', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg' };
  await p.route('http://local/**', r => { const f = path.join(ROOT, decodeURIComponent(new URL(r.request().url()).pathname));
    if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) return r.fulfill({ status: 404, body: '' });
    r.fulfill({ status: 200, contentType: TYPES[path.extname(f)] || 'application/octet-stream', body: fs.readFileSync(f) }); });
  await p.goto(`http://local/finance_series/engine3d/toon/${page}`);
  await p.waitForFunction(() => window.ready || window.__err, null, { timeout: 180000 }).catch(e => { console.log('not ready', errs); process.exit(1); });
  const fn = (mode === 'stills' ? b : fn0) || 'renderAt';
  if (process.env.SHORT) await p.evaluate(s => { window.SHORT = JSON.parse(s); }, process.env.SHORT);
  const b64 = d => Buffer.from(d.split(',')[1], 'base64');
  const frame = (t) => p.evaluate(([t, fn]) => window[fn](t), [t, fn]);
  if (mode === 'stills') { fs.mkdirSync(out, { recursive: true }); for (const t of a.split(',').map(Number)) fs.writeFileSync(path.join(out, `f_${t.toFixed(2)}.jpg`), b64(await frame(t))); }
  else {
    const fps = 30, f0 = Math.round(+a * fps), f1 = Math.round(+b * fps), t0 = Date.now();
    const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = f0; f < f1; f++) { const buf = b64(await frame(f / fps)); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if ((f - f0) % 300 === 0) console.log(path.basename(out), f - f0, f1 - f0, ((Date.now() - t0) / 1000).toFixed(0) + 's'); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  if (errs.length) console.log('page errors', JSON.stringify(errs.slice(0, 5)));
  await br.close();
})();
