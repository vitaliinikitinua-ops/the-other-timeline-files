// node rtoon.js <page.html> sheet <out_dir>          -> sheet_0.jpg, sheet_1.jpg
// node rtoon.js <page.html> video <out.mp4> <secs>    -> frames piped to ffmpeg
// Files are served from the repo by Playwright routing (no local server needed).
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { spawn } = require('child_process');
(async () => {
  const [page, mode, out, secs] = process.argv.slice(2);
  const br = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const ROOT = path.join(__dirname, '..', '..', '..');
  const TYPES = { '.js': 'text/javascript', '.html': 'text/html', '.ttf': 'font/ttf', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg' };
  await p.route('http://local/**', r => { const f = path.join(ROOT, decodeURIComponent(new URL(r.request().url()).pathname));
    if (!f.startsWith(ROOT) || !fs.existsSync(f)) return r.fulfill({ status: 404, body: '' });
    r.fulfill({ status: 200, contentType: TYPES[path.extname(f)] || 'application/octet-stream', body: fs.readFileSync(f) }); });
  await p.goto(`http://local/finance_series/engine3d/toon/${page}`); await p.waitForFunction(() => window.ready, null, { timeout: 120000 });
  const b64 = d => Buffer.from(d.split(',')[1], 'base64');
  if (mode === 'sheet') { fs.mkdirSync(out, { recursive: true }); for (const i of [0, 1]) fs.writeFileSync(path.join(out, `sheet_${i}.jpg`), b64(await p.evaluate(i => window.renderSheet(i), i))); }
  else {
    const fps = 30, n = Math.round(+secs * fps), t0 = Date.now();
    const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = 0; f < n; f++) { const buf = b64(await p.evaluate(t => window.renderAt(t), f / fps)); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if (f % 60 === 0) console.log(f, n, ((Date.now() - t0) / 1000).toFixed(0) + 's'); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  if (errs.length) console.log('page errors', JSON.stringify(errs.slice(0, 5)));
  await br.close();
})();
