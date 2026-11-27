const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const out = process.argv[2]; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'] });
  const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  await p.goto('http://localhost:8790/finance_series/engine3d/sheet.html'); await p.waitForFunction(() => window.ready, null, { timeout: 60000 });
  const jobs = [];
  const poses = ['idle','no','cheer','point','shrug','facepalm','thumbsup','panic','slump','hold','jump'];
  const emos = ['neutral','happy','shock','smug','sad','panic','money','laugh','angry'];
  for (const who of ['you','max','grandma','banker']) jobs.push([who,'idle','neutral']);
  poses.forEach((po,i) => jobs.push(['you', po, ['happy','smug','money','neutral','smug','sad','happy','panic','sad','happy','laugh'][i]]));
  emos.forEach(e => jobs.push(['max','idle',e]));
  jobs.push(['grandma','thumbsup','happy'],['banker','point','smug'],['max','facepalm','sad'],['max','panic','panic']);
  let i = 0;
  for (const [who,pose,emo] of jobs) { const d = await p.evaluate(([w,po,e]) => window.renderSheet(w,po,e), [who,pose,emo]); fs.writeFileSync(`${out}/${String(i).padStart(2,'0')}_${who}_${pose}_${emo}.jpg`, Buffer.from(d.split(',')[1],'base64')); i++; }
  console.log('frames', i, 'errors', JSON.stringify(errs));
  await b.close();
})();
