#!/usr/bin/env node
// フレーム単位のオフスクリーン録画。
//
// 実時間で画面を録画するのではなく、SIM.renderFrame(i) を i=0..N-1 で呼び、
// 1枚ずつ PNG を ffmpeg の標準入力に流し込む。
//   - マシンの速度が結果に影響しない（何度回しても1フレーム単位で同一の動画）
//   - 中間ファイルをディスクに置かないので、10分尺でも数GBを消費しない
//
// 使い方:
//   node tools/capture.mjs --episode 01-wealth --out out/01-wealth.mp4
//   node tools/capture.mjs --episode 01-wealth --to 300 --out out/smoke.mp4   # 冒頭10秒だけ

import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { mkdirSync, existsSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { extname, join, normalize, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const ROOT = normalize(join(dirname(fileURLToPath(import.meta.url)), '..'));

const args = Object.fromEntries(
  process.argv.slice(2).join(' ').split('--').filter(Boolean)
    .map((s) => s.trim().split(/\s+/))
    .map(([k, ...v]) => [k, v.length ? v.join(' ') : 'true']),
);

const EPISODE = args.episode ?? '01-wealth';
const OUT = args.out ?? `out/${EPISODE}.mp4`;
const FROM = args.from ? parseInt(args.from, 10) : 0;
const TO = args.to ? parseInt(args.to, 10) : null;
const CRF = args.crf ?? '16';
const PRESET = args.preset ?? 'medium';
const FFMPEG = args.ffmpeg ?? 'ffmpeg';

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json',
};

// ---- ローカル静的サーバ（file:// だと ES module が CORS で読めないため）
const server = createServer(async (req, res) => {
  try {
    const path = normalize(join(ROOT, decodeURIComponent(req.url.split('?')[0])));
    if (!path.startsWith(ROOT)) { res.writeHead(403).end(); return; }
    const body = await readFile(path);
    res.writeHead(200, { 'Content-Type': MIME[extname(path)] ?? 'application/octet-stream' });
    res.end(body);
  } catch {
    res.writeHead(404).end('not found');
  }
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;
const url = `http://127.0.0.1:${port}/sim/episodes/${EPISODE}/index.html`;

// ---- ブラウザ
// 環境に用意済みの Chromium を使う（playwright install は走らせない）。
const PRESET_CHROME = '/opt/pw-browsers/chromium';
const launchOpts = {
  args: ['--force-device-scale-factor=1', '--hide-scrollbars', '--disable-lcd-text'],
};
if (args.chrome) launchOpts.executablePath = args.chrome;
else if (existsSync(PRESET_CHROME)) launchOpts.executablePath = PRESET_CHROME;
const browser = await chromium.launch(launchOpts);
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
// 描画を壊すのは JS 例外だけ。favicon の 404 のような読み込み失敗で録画を止めない。
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => {
  if (m.type() !== 'error') return;
  const t = m.text();
  if (/Failed to load resource/i.test(t)) return;
  errors.push(t);
});

await page.goto(url, { waitUntil: 'load' });
await page.waitForFunction(() => window.SIM_READY === true, null, { timeout: 60_000 });
if (errors.length) {
  console.error('ページ内エラー:\n' + errors.join('\n'));
  await browser.close(); server.close(); process.exit(1);
}
await page.evaluate(() => window.SIM.captureMode());

const meta = await page.evaluate(() => ({
  fps: window.SIM.fps,
  totalFrames: window.SIM.totalFrames,
  durationSec: window.SIM.durationSec,
  scenes: window.SIM.scenes,
}));

const start = FROM;
const end = TO !== null ? Math.min(TO, meta.totalFrames) : meta.totalFrames;
const count = end - start;

console.log(`エピソード : ${EPISODE}`);
console.log(`尺         : ${(meta.durationSec / 60).toFixed(2)} 分 / ${meta.fps}fps / 全 ${meta.totalFrames} フレーム`);
console.log(`書き出し   : フレーム ${start} - ${end - 1} (${count} 枚)`);
console.log(`出力       : ${OUT}\n`);

if (!existsSync(dirname(OUT))) mkdirSync(dirname(OUT), { recursive: true });

// ---- ffmpeg
const ff = spawn(FFMPEG, [
  '-y', '-hide_banner', '-loglevel', 'error',
  '-f', 'image2pipe', '-framerate', String(meta.fps), '-c:v', 'png', '-i', '-',
  '-c:v', 'libx264', '-preset', PRESET, '-crf', CRF,
  '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
  '-r', String(meta.fps),
  OUT,
]);
ff.stderr.on('data', (d) => process.stderr.write(d));

// エラー監視は1回だけ張る（フレームごとに once を足すとリスナーが1万個溜まる）
let ffError = null;
ff.stdin.on('error', (e) => { ffError = e; });

const write = (buf) => new Promise((res, rej) => {
  if (ffError) return rej(ffError);
  if (ff.stdin.write(buf)) res();
  else ff.stdin.once('drain', res);
});

const t0 = Date.now();
for (let i = start; i < end; i++) {
  const dataUrl = await page.evaluate((f) => {
    window.SIM.renderFrame(f);
    return window.SIM.png();
  }, i);
  await write(Buffer.from(dataUrl.slice('data:image/png;base64,'.length), 'base64'));

  const done = i - start + 1;
  if (done % 60 === 0 || done === count) {
    const el = (Date.now() - t0) / 1000;
    const rate = done / el;
    const eta = (count - done) / rate;
    const sc = meta.scenes.filter((s) => i / meta.fps >= s.startSec).pop();
    process.stdout.write(
      `\r  ${done}/${count}  ${(done / count * 100).toFixed(1)}%  ` +
      `${rate.toFixed(1)} fps  残り ${(eta / 60).toFixed(1)}分  [${sc ? sc.title : ''}]        `,
    );
  }
}
process.stdout.write('\n');

ff.stdin.end();
await new Promise((res, rej) => {
  ff.on('close', (code) => (code === 0 ? res() : rej(new Error(`ffmpeg exit ${code}`))));
});

await browser.close();
server.close();

if (errors.length) console.error('\n描画中のエラー:\n' + errors.join('\n'));
console.log(`\n完成: ${OUT}  (${((Date.now() - t0) / 60000).toFixed(1)} 分で書き出し)`);
