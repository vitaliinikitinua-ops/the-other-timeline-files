// node render_ep.js epNN <worker> <workers>   -> build3d/chunk_<worker>.mp4 (frames piped to ffmpeg)
// node render_ep.js epNN stills t1,t2,...    -> build3d/stills/s_000.jpg ...
// Same Chromium flags as render_demo.js (software WebGL in the container).
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { spawn } = require('child_process');
(async () => {
  const [ep, a, b] = process.argv.slice(2);
  const bd = path.join(__dirname, '..', ep, 'build3d'); const tl = JSON.parse(fs.readFileSync(path.join(bd, 'timeline.json')));
  const br = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await br.newPage({ viewport: { width: 1920, height: 1080 } }); const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto(`http://localhost:8790/finance_series/engine3d/episode.html?ep=${ep}`);
  await p.waitForFunction(() => window.ready, null, { timeout: 120000 });
  if (process.argv[5] === 'clean') await p.evaluate(() => { window.CLEAN = true; });
  const grab = async (t) => Buffer.from((await p.evaluate((t) => window.renderAt(t), t)).split(',')[1], 'base64');
  if (a === 'stills') {
    fs.mkdirSync(path.join(bd, 'clean'), { recursive: true }); fs.mkdirSync(path.join(bd, 'stills'), { recursive: true }); const ts = b.split(',').map(Number);
    for (let i = 0; i < ts.length; i++) fs.writeFileSync(path.join(bd, process.argv[5] === 'clean' ? 'clean' : 'stills', `s_${String(i).padStart(3, '0')}.jpg`), await grab(ts[i]));
  } else {
    const wi = +a, wn = +b, n = Math.ceil(tl.total * tl.fps), f0 = Math.floor(n * wi / wn), f1 = Math.floor(n * (wi + 1) / wn);
    const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(tl.fps), '-i', '-',
      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', path.join(bd, `chunk_${wi}.mp4`)], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let f = f0; f < f1; f++) {
      const buf = await grab(f / tl.fps); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if ((f - f0) % 300 === 0) console.log(`w${wi} ${f - f0}/${f1 - f0} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  if (errs.length) console.log('page errors', JSON.stringify(errs.slice(0, 5)));
  await br.close();
})();
