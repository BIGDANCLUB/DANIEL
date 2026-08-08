#!/usr/bin/env node
// 指定秒数の静止画を書き出す。構図の確認とサムネイル候補の抽出に使う。
//   node tools/stills.mjs --episode 01-wealth --at 20,60,150,300,480,560,590 --out out/stills

import { createServer } from 'node:http';
import { readFile, writeFile } from 'node:fs/promises';
import { mkdirSync, existsSync } from 'node:fs';
import { extname, join, normalize, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const ROOT = normalize(join(dirname(fileURLToPath(import.meta.url)), '..'));
const args = Object.fromEntries(
  process.argv.slice(2).join(' ').split('--').filter(Boolean)
    .map((s) => s.trim().split(/\s+/)).map(([k, ...v]) => [k, v.length ? v.join(' ') : 'true']),
);

const EPISODE = args.episode ?? '01-wealth';
const OUTDIR = args.out ?? 'out/stills';
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8' };

const server = createServer(async (req, res) => {
  try {
    const p = normalize(join(ROOT, decodeURIComponent(req.url.split('?')[0])));
    if (!p.startsWith(ROOT)) return res.writeHead(403).end();
    const body = await readFile(p);
    res.writeHead(200, { 'Content-Type': MIME[extname(p)] ?? 'application/octet-stream' });
    res.end(body);
  } catch { res.writeHead(404).end(); }
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));

const browser = await chromium.launch({
  executablePath: existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined,
  args: ['--force-device-scale-factor=1', '--hide-scrollbars'],
});
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
const errs = [];
page.on('pageerror', (e) => errs.push(String(e)));
page.on('console', (m) => { if (m.type() === 'error' && !/Failed to load resource/i.test(m.text())) errs.push(m.text()); });
await page.goto(`http://127.0.0.1:${server.address().port}/sim/episodes/${EPISODE}/index.html`, { waitUntil: 'load' });
await page.waitForFunction(() => window.SIM_READY === true, null, { timeout: 60_000 });
await page.evaluate(() => window.SIM.captureMode());

const meta = await page.evaluate(() => ({ fps: window.SIM.fps, scenes: window.SIM.scenes, totalFrames: window.SIM.totalFrames }));
// --at 未指定なら各シーンの中央を撮る
const secs = args.at
  ? args.at.split(',').map(Number)
  : meta.scenes.map((s) => s.startSec + s.dur * 0.6);

if (!existsSync(OUTDIR)) mkdirSync(OUTDIR, { recursive: true });
for (const sec of secs.sort((a, b) => a - b)) {
  const f = Math.min(meta.totalFrames - 1, Math.round(sec * meta.fps));
  const dataUrl = await page.evaluate((i) => { window.SIM.renderFrame(i); return window.SIM.png(); }, f);
  const name = join(OUTDIR, `${String(Math.round(sec)).padStart(4, '0')}s.png`);
  await writeFile(name, Buffer.from(dataUrl.slice(22), 'base64'));
  console.log(`${name}  (${Math.floor(sec / 60)}:${String(Math.round(sec % 60)).padStart(2, '0')})`);
}

if (errs.length) console.error('エラー:\n' + errs.join('\n'));
await browser.close();
server.close();
