#!/usr/bin/env node
// 字幕の数値と実際のシミュレーション結果を突き合わせる。
//
// この型の動画は「実測を見せる」ことが価値の全てなので、ナレーションの数字が
// 画面のカウンタとズレていたら成立しない。パラメータや尺を変えたら必ず実行し、
// 各字幕の時点で画面に出ている実際の値を確認してから台本を直すこと。
//
//   node tools/verify.mjs --episode 01-wealth

import { join, dirname, normalize } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { gini, topShare } from '../sim/core/charts.js';

const ROOT = normalize(join(dirname(fileURLToPath(import.meta.url)), '..'));
const args = Object.fromEntries(
  process.argv.slice(2).join(' ').split('--').filter(Boolean)
    .map((s) => s.trim().split(/\s+/)).map(([k, ...v]) => [k, v.length ? v.join(' ') : 'true']),
);
const EPISODE = args.episode ?? '01-wealth';

const mod = await import(pathToFileURL(join(ROOT, 'sim/episodes', EPISODE, 'episode.js')).href);
const { ep, tl, runner } = mod.build();

console.log(`エピソード: ${EPISODE}`);
console.log(`尺: ${(tl.durationSec / 60).toFixed(2)} 分 (${tl.durationSec}秒) / ${tl.fps}fps / ${tl.totalFrames} フレーム\n`);

const mmss = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;

for (const scene of tl.scenes) {
  console.log(`── ${scene.title}  [${mmss(scene.startSec)} - ${mmss(scene.startSec + scene.dur)}]  ${scene.steps ? scene.steps.toLocaleString() + '回' : '—'}`);
  for (const c of scene.captions ?? []) {
    const frame = Math.round((scene.startSec + c.at) * tl.fps);
    runner._advanceTo(frame);
    const w = ep.world;
    const st = w.stats();
    const metric = w.allowDebt
      ? `sd=¥${st.sd.toFixed(0)} min=¥${Math.round(st.min)} max=¥${Math.round(st.max)} 借金=${st.broke}人`
      : `gini=${gini(w.wealth).toFixed(3)} top10%=${(topShare(w.wealth, 0.1) * 100).toFixed(1)}% max=¥${Math.round(st.max)} 無一文=${st.broke}人`;
    console.log(`  ${mmss(scene.startSec + c.at)}  ${String(w.trades).padStart(9)}回  ${metric}`);
    console.log(`         「${c.text}」`);
  }
  console.log('');
}

// ナレーション総文字数から、話速が現実的かを見る（日本語ナレーションは約6文字/秒）
let chars = 0;
for (const s of tl.scenes) for (const c of s.captions ?? []) chars += c.text.length;
console.log(`ナレーション総文字数: ${chars} 字 / ${tl.durationSec}秒 = ${(chars / tl.durationSec).toFixed(2)} 字/秒`);
console.log('（日本語の聞き取りやすい話速は 5〜7 字/秒。3未満なら間が多すぎ、8超なら早口）');
