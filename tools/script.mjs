#!/usr/bin/env node
// 画面字幕からナレーション原稿と字幕ファイル(SRT)を書き出す。
//
// 字幕データが原稿の唯一の出所なので、台本と画面が食い違うことがない。
// 音声は自分で録るか合成する。合成音声を使った場合は YouTube 側で
// 「変更または合成されたコンテンツ」の開示トグルを必ず ON にすること。
//
//   node tools/script.mjs --episode 01-wealth --out out/01-wealth

import { writeFile, mkdir } from 'node:fs/promises';
import { join, dirname, normalize } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = normalize(join(dirname(fileURLToPath(import.meta.url)), '..'));
const args = Object.fromEntries(
  process.argv.slice(2).join(' ').split('--').filter(Boolean)
    .map((s) => s.trim().split(/\s+/)).map(([k, ...v]) => [k, v.length ? v.join(' ') : 'true']),
);
const EPISODE = args.episode ?? '01-wealth';
const OUT = args.out ?? `out/${EPISODE}`;

const mod = await import(pathToFileURL(join(ROOT, 'sim/episodes', EPISODE, 'episode.js')).href);
const { tl } = mod.build();

const pad = (n, w = 2) => String(n).padStart(w, '0');
const mmss = (s) => `${Math.floor(s / 60)}:${pad(Math.floor(s % 60))}`;
const srtTime = (s) => {
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60);
  const sec = Math.floor(s % 60), ms = Math.round((s % 1) * 1000);
  return `${pad(h)}:${pad(m)}:${pad(sec)},${pad(ms, 3)}`;
};

// ---- ナレーション原稿(Markdown)
const md = [`# ${EPISODE} ナレーション原稿`, ''];
md.push(`尺: ${mmss(tl.durationSec)} / ${tl.fps}fps / 1920x1080`, '');
let chars = 0;
for (const sc of tl.scenes) {
  md.push(`## ${sc.title}  (${mmss(sc.startSec)} - ${mmss(sc.startSec + sc.dur)})`, '');
  for (const c of sc.captions ?? []) {
    md.push(`- **${mmss(sc.startSec + c.at)}**　${c.text}`);
    chars += c.text.length;
  }
  md.push('');
}
md.push('---', '', `総文字数: ${chars} 字 / ${tl.durationSec} 秒 = ${(chars / tl.durationSec).toFixed(2)} 字/秒`, '');
md.push('※ 数値はすべてシミュレーションの実測値。パラメータを変えたら `npm run verify` で再確認すること。');

// ---- 字幕(SRT)
const cues = [];
for (const sc of tl.scenes) {
  const list = sc.captions ?? [];
  list.forEach((c, i) => {
    const start = sc.startSec + c.at;
    const end = i + 1 < list.length ? sc.startSec + list[i + 1].at : sc.startSec + sc.dur;
    cues.push({ start, end, text: c.text });
  });
}
const srt = cues.map((c, i) =>
  `${i + 1}\n${srtTime(c.start)} --> ${srtTime(c.end)}\n${c.text}\n`).join('\n');

await mkdir(dirname(OUT), { recursive: true });
await writeFile(`${OUT}-script.md`, md.join('\n'));
await writeFile(`${OUT}.srt`, srt);
console.log(`${OUT}-script.md   (${chars}字 / ${cues.length}行)`);
console.log(`${OUT}.srt`);
