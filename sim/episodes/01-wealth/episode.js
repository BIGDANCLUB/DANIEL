// エピソード#1「全員が同じ金額から始めたら、格差は生まれるか」
//
// 尺: 10分00秒 / 30fps / 1920x1080
// 構成: フック → ルール提示 → 100人でゆっくり → 1000人で100万回 →
//       条件変更1(下限の壁を外す) → 条件変更2(再分配) → 結論
//
// 台本中の数値はすべて実測値。パラメータを変えたら tools/verify.mjs を回して
// キャプションの数字を必ず更新すること（ここがズレると動画が嘘になる）。

import { W, H, C, F, wealthColor } from '../../core/theme.js';
import {
  clear, panel, text, caption, counter, roundRect, formatInt, formatYen,
  clamp, window01,
} from '../../core/render.js';
import { drawHistogram, drawSeries, Series, gini, topShare } from '../../core/charts.js';
import { Timeline, Runner, captionAt } from '../../core/engine.js';
import { WealthWorld } from './model.js';

export const FPS = 30;

const LEFT = { x: 60, y: 130, w: 900, h: 640 };
const HIST = { x: 990, y: 130, w: 870, h: 400 };
const SER = { x: 990, y: 550, w: 870, h: 220 };
const COUNT_Y = 792;

const SEED_MAIN = 777;

// ---------------------------------------------------------------- 描画部品

function header(ctx, title, sub, alpha = 1) {
  text(ctx, title, 60, 58, { font: F.title(46), color: C.fg, baseline: 'middle', alpha });
  if (sub) {
    text(ctx, sub, W - 60, 58, {
      font: F.body(28), color: C.fgDim, align: 'right', baseline: 'middle', alpha,
    });
  }
}

// 個人を格子で描く（「ランダムな人々」の絵）
function drawGrid(ctx, world, box, opts = {}) {
  const { cols, alpha = 1, highlight = null, refWealth = 100, label = '' } = opts;
  if (alpha <= 0) return;
  panel(ctx, box.x, box.y, box.w, box.h, alpha);

  const n = world.n;
  const rows = Math.ceil(n / cols);
  const padX = 24, padY = 58;
  const cw = (box.w - padX * 2) / cols;
  const ch = (box.h - padY - 24) / rows;

  if (label) text(ctx, label, box.x + 24, box.y + 30, { font: F.bold(26), color: C.fg, baseline: 'middle', alpha });

  ctx.save();
  ctx.globalAlpha = alpha;
  for (let i = 0; i < n; i++) {
    const r = (i / cols) | 0;
    const c = i % cols;
    const x = box.x + padX + c * cw;
    const y = box.y + padY + r * ch;
    const w = cw - Math.min(4, cw * 0.15);
    const h = ch - Math.min(4, ch * 0.15);

    ctx.fillStyle = '#0a0f1e';
    roundRect(ctx, x, y, w, h, Math.min(5, w / 5));
    ctx.fill();

    const v = world.wealth[i];
    const fill = clamp(v / (refWealth * 4), 0, 1);
    if (fill > 0.01) {
      ctx.fillStyle = wealthColor(v, refWealth);
      const fh = h * fill;
      roundRect(ctx, x, y + h - fh, w, fh, Math.min(5, w / 5));
      ctx.fill();
    }
    if (v <= 0) {
      ctx.strokeStyle = C.bad;
      ctx.lineWidth = 1.5;
      roundRect(ctx, x, y, w, h, Math.min(5, w / 5));
      ctx.stroke();
    }
  }

  if (highlight && highlight.from >= 0 && cw > 20) {
    for (const [idx, col] of [[highlight.from, C.bad], [highlight.to, C.good]]) {
      const r = (idx / cols) | 0;
      const c = idx % cols;
      ctx.strokeStyle = col;
      ctx.lineWidth = 3;
      roundRect(ctx, box.x + padX + c * cw - 2, box.y + padY + r * ch - 2,
        cw - Math.min(4, cw * 0.15) + 4, ch - Math.min(4, ch * 0.15) + 4, 6);
      ctx.stroke();
    }
  }
  ctx.restore();
}

// 資産順に並べた棒グラフ。格差の形がそのまま出る。負の資産にも対応。
function drawSortedBars(ctx, world, box, opts = {}) {
  const { alpha = 1, refWealth = 100, label = '', hiScale = 750, loScale = 0 } = opts;
  if (alpha <= 0) return;
  panel(ctx, box.x, box.y, box.w, box.h, alpha);
  if (label) text(ctx, label, box.x + 24, box.y + 30, { font: F.bold(26), color: C.fg, baseline: 'middle', alpha });

  const arr = world.sorted();
  const n = arr.length;
  const padX = 24, padT = 58, padB = 46;
  const plotX = box.x + padX, plotY = box.y + padT;
  const plotW = box.w - padX * 2, plotH = box.h - padT - padB;
  const span = hiScale - loScale;
  const toY = (v) => plotY + plotH * ((hiScale - clamp(v, loScale, hiScale)) / span);
  const zeroY = toY(0);
  const bw = plotW / n;

  ctx.save();
  ctx.globalAlpha = alpha;
  for (let i = 0; i < n; i++) {
    const v = arr[i];
    const y = toY(v);
    ctx.fillStyle = v < 0 ? C.bad : wealthColor(v, refWealth);
    const top = Math.min(y, zeroY);
    const h = Math.abs(y - zeroY);
    if (h >= 0.3) ctx.fillRect(plotX + i * bw, top, Math.max(0.7, bw - 0.4), h);
  }

  // ゼロ線（負の値が出る条件でのみ意味を持つ）
  if (loScale < 0) {
    ctx.strokeStyle = C.fgFaint;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(plotX, zeroY);
    ctx.lineTo(plotX + plotW, zeroY);
    ctx.stroke();
    text(ctx, '¥0', plotX + plotW - 8, zeroY + 6, {
      font: F.body(20), color: C.fgFaint, align: 'right', baseline: 'top', alpha,
    });
  }

  // スタート水準
  const ry = toY(refWealth);
  ctx.strokeStyle = C.fgDim;
  ctx.setLineDash([8, 8]);
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(plotX, ry);
  ctx.lineTo(plotX + plotW, ry);
  ctx.stroke();
  ctx.setLineDash([]);
  text(ctx, '全員のスタート地点 ¥100', plotX + 8, ry - 8, {
    font: F.body(20), color: C.fgDim, baseline: 'bottom', alpha,
  });
  text(ctx, '←  資産が多い人                                                 資産が少ない人  →',
    plotX + plotW / 2, box.y + box.h - 14, {
      font: F.body(20), color: C.fgFaint, align: 'center', baseline: 'bottom', alpha,
    });
  ctx.restore();
}

// 画面下の指標。借金ありの条件ではジニ係数が比較可能でなくなるので指標を差し替える。
function statRow(ctx, ep, alpha = 1) {
  if (alpha <= 0) return;
  const w = ep.world;
  const st = w.stats();
  const items = w.allowDebt
    ? [
      ['取引回数', formatInt(w.trades), C.accent],
      ['標準偏差（散らばり）', formatYen(st.sd), C.warn],
      ['最も多い人', formatYen(st.max), C.richest],
      ['最も少ない人', formatYen(st.min), C.bad],
      ['借金を抱えた人', `${st.broke}人`, C.bad],
    ]
    : [
      ['取引回数', formatInt(w.trades), C.accent],
      ['ジニ係数', gini(w.wealth).toFixed(3), gini(w.wealth) > 0.4 ? C.warn : C.good],
      ['上位10%の取り分', `${(topShare(w.wealth, 0.1) * 100).toFixed(1)}%`, C.rich],
      ['最も多い人', formatYen(st.max), C.richest],
      ['無一文の人', `${st.broke}人`, st.broke > 0 ? C.bad : C.good],
    ];
  const gap = (W - 120) / items.length;
  items.forEach(([label, value, col], i) => {
    counter(ctx, label, value, 60 + gap * i, COUNT_Y, { alpha, color: col, size: 44 });
  });
}

// 画面下部の帯。グラフを隠さずに一言だけ強調したいときに使う。
function banner(ctx, str, alpha, y = 878, size = 58, color = C.accent) {
  if (alpha <= 0) return;
  ctx.save();
  ctx.globalAlpha = alpha * 0.92;
  ctx.fillStyle = '#00040d';
  ctx.fillRect(0, y - 56, W, 112);
  ctx.restore();
  text(ctx, str, W / 2, y, { font: F.title(size), color, align: 'center', baseline: 'middle', alpha });
}

// 結論のカード。シーンの最後に全画面で挟む。
// グラフの上に半透明で重ねるとヒストグラムが読めなくなるので、覆うなら完全に覆う。
function statementCard(ctx, lines, alpha, y = H / 2) {
  if (alpha <= 0) return;
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.fillStyle = '#00040d';
  ctx.fillRect(0, 0, W, H);
  ctx.restore();
  lines.forEach((ln, i) => {
    text(ctx, ln.t, W / 2, y - (lines.length - 1) * 52 + i * 104, {
      font: F.title(ln.size || 64), color: ln.color || C.fg, align: 'center', baseline: 'middle', alpha,
    });
  });
}

// ---------------------------------------------------------------- エピソード

export class Episode {
  constructor() {
    this.reset();
    // フックで見せる「結末」を先に計算しておく（本編とは別シード）
    const pre = new WealthWorld({ n: 1000, seed: 999 });
    pre.run(1_000_000);
    this.preview = pre;
  }

  reset() {
    this.world = new WealthWorld({ n: 100, seed: 12345 });
    this.series = new Series(600);
    this.snapshots = {};
  }

  stepSim(steps) {
    this.world.run(steps);
  }

  onFrame(frame, scene) {
    if (!scene.steps) return;
    // 借金ありの回は発散を見せたいので、ジニではなく標準偏差を追う
    this.series.push(this.world.allowDebt ? this.world.stats().sd : gini(this.world.wealth));
  }
}

// ---------------------------------------------------------------- シーン
// captions は画面字幕であると同時にナレーション原稿。tools/script.mjs がこれを読む。

const S_HOOK = {
  id: 'hook',
  dur: 45,
  title: 'フック',
  captions: [
    { at: 0, text: 'このグラフを見てください。' },
    { at: 4, text: '1000人が持っているお金を、多い順に並べたものです。' },
    { at: 11, text: '左端の数人が突出し、右端の40人は無一文になっています。' },
    { at: 18, text: 'では、この1000人のスタート地点はどうだったか。' },
    { at: 25, text: '全員、まったく同じ ¥100 でした。' },
    { at: 31, text: '能力の差もなければ、運の偏りも、搾取も存在しません。' },
    { at: 38, text: 'ランダムに ¥5 を渡し合っただけです。' },
    { at: 42, text: 'なぜ、こうなるのか。' },
  ],
  draw(ctx, s, ep) {
    clear(ctx);
    const a = window01(s.localSec, 0, 0.8, 44.2, 45);
    header(ctx, '全員が同じ金額から始めたら、格差は生まれるか', 'シミュレーション #01', a);

    drawSortedBars(ctx, ep.preview, { x: 60, y: 150, w: W - 120, h: 460 }, {
      alpha: a * clamp(s.localSec / 5, 0, 1), label: '100万回の取引を終えた1000人の資産', hiScale: 600,
    });
    drawHistogram(ctx, ep.preview.wealth, { x: 60, y: 630, w: 900, h: 310 }, {
      lo: 0, hi: 600, binCount: 40, title: '同じデータの分布',
      alpha: a * window01(s.localSec, 8, 9.5, 44.2, 45),
    });

    const ba = a * window01(s.localSec, 12, 13.5, 44.2, 45);
    const st = ep.preview.stats();
    counter(ctx, 'ジニ係数', gini(ep.preview.wealth).toFixed(3), 1030, 690, { alpha: ba, color: C.warn, size: 72 });
    counter(ctx, '上位10%の取り分', `${(topShare(ep.preview.wealth, 0.1) * 100).toFixed(1)}%`, 1030, 815, { alpha: ba, color: C.rich, size: 72 });
    counter(ctx, '無一文になった人', `${st.broke}人`, 1470, 690, { alpha: ba, color: C.bad, size: 72 });
    counter(ctx, 'スタート時のジニ係数', '0.000', 1470, 815, { alpha: ba, color: C.good, size: 72 });

    const c = captionAt(this.captions, s.localSec);
    caption(ctx, c.text, c.alpha * a);
  },
};

const S_RULES = {
  id: 'rules',
  dur: 75,
  title: 'ルール提示',
  captions: [
    { at: 0, text: 'ルールを組み立てます。' },
    { at: 4, text: 'まず100人を用意します。全員の所持金は ¥100。' },
    { at: 11, text: '毎回、ランダムに2人を選びます。' },
    { at: 17, text: '片方がもう片方に ¥5 を渡す。それだけです。' },
    { at: 24, text: '渡す人も受け取る人も、完全にランダムに決まります。' },
    { at: 31, text: '強い人も、賢い人も、ズルをする人もいません。' },
    { at: 38, text: '制約はひとつだけ。持っている額を超えては渡せません。' },
    { at: 46, text: '所持金 ¥0 の人は、誰にも渡せないということです。' },
    { at: 53, text: 'この一行が、後で決定的な意味を持ちます。' },
    { at: 60, text: 'ここで予想してみてください。' },
    { at: 65, text: '10万回繰り返したあと、この100人はどうなっているか。' },
  ],
  enter(ep) {
    ep.world = new WealthWorld({ n: 100, seed: 12345 });
    ep.series.reset();
  },
  draw(ctx, s, ep) {
    clear(ctx);
    header(ctx, 'ルール', 'シミュレーション #01');
    const pa = window01(s.localSec, 3, 4.5, 999, 1000);

    drawGrid(ctx, ep.world, LEFT, { cols: 10, alpha: pa, label: '100人（全員 ¥100 スタート）' });

    const rules = [
      { at: 4, t: '1.  100人。全員の所持金は ¥100' },
      { at: 11, t: '2.  毎回ランダムに2人を選ぶ' },
      { at: 17, t: '3.  片方がもう片方に ¥5 を渡す' },
      { at: 38, t: '4.  持っている額を超えては渡せない', c: C.warn },
    ];
    panel(ctx, HIST.x, HIST.y, HIST.w, HIST.h, pa);
    text(ctx, 'ルール', HIST.x + 24, HIST.y + 42, { font: F.bold(30), color: C.fg, baseline: 'middle', alpha: pa });
    rules.forEach((r, i) => {
      text(ctx, r.t, HIST.x + 24, HIST.y + 120 + i * 68, {
        font: F.body(34), color: r.c || C.fg, baseline: 'middle',
        alpha: window01(s.localSec, r.at, r.at + 0.6, 999, 1000),
      });
    });

    // 「存在しないもの」を明示し、格差の原因が構造側にあることを先に封じておく
    const na = window01(s.localSec, 31, 32.5, 999, 1000);
    panel(ctx, SER.x, SER.y, SER.w, SER.h, na);
    text(ctx, 'このシミュレーションに存在しないもの', SER.x + 24, SER.y + 36, {
      font: F.bold(26), color: C.fgDim, baseline: 'middle', alpha: na,
    });
    ['能力の差', '運の偏り', '搾取・詐欺', '利子・投資'].forEach((t, i) => {
      text(ctx, `×  ${t}`, SER.x + 30 + (i % 2) * 420, SER.y + 100 + ((i / 2) | 0) * 58, {
        font: F.body(32), color: C.fgFaint, baseline: 'middle',
        alpha: window01(s.localSec, 32 + i * 1.1, 33 + i * 1.1, 999, 1000),
      });
    });

    const qa = window01(s.localSec, 60, 61.5, 999, 1000);
    if (qa > 0) banner(ctx, '10万回後、この100人はどうなる？', qa);

    const c = captionAt(this.captions, s.localSec);
    caption(ctx, c.text, c.alpha);
  },
};

// steps は ramp(t^3.2) で配分される。以下の字幕の回数はその配分に合わせた実測値。
const S_RUN1 = {
  id: 'run1',
  dur: 120,
  steps: 100_000,
  rate: 'ramp',
  title: '第1回実行（100人）',
  captions: [
    { at: 0, text: 'では始めます。まずはゆっくり、1回ずつ。' },
    { at: 8, text: '赤が渡した人、緑が受け取った人です。' },
    { at: 16, text: '200回ほど進みました。まだ誰にも差はついていません。' },
    { at: 26, text: '速度を上げます。' },
    { at: 34, text: '右のヒストグラムに注目してください。' },
    { at: 42, text: '最初は ¥100 のところに全員が集まった、一本の柱でした。' },
    { at: 52, text: 'それが崩れて、左に潰れながら右へ長い尾を引いていきます。' },
    { at: 62, text: '1万8千回。ジニ係数はもう0.4を超えました。' },
    { at: 71, text: '0が完全な平等、1が一人による独占を意味する指標です。' },
    { at: 82, text: '4万回。伸びは鈍ってきましたが、下がりはしません。' },
    { at: 92, text: '6万回でジニ係数0.5。格差を戻す力はどこにも働いていません。' },
    { at: 102, text: '9万回。ここから先は0.5前後で揺れるだけになります。' },
    { at: 111, text: '10万回。最終的にジニ係数0.52、上位10%が全体の3分の1です。' },
    { at: 116, text: 'では人数を10倍にして、100万回やってみます。' },
  ],
  enter(ep) {
    ep.world = new WealthWorld({ n: 100, seed: 12345 });
    ep.series = new Series(120 * FPS);
  },
  draw(ctx, s, ep) {
    clear(ctx);
    header(ctx, '第1回：100人 / 10万回', `${formatInt(ep.world.trades)} 回`);
    drawGrid(ctx, ep.world, LEFT, {
      cols: 10, label: '100人の資産',
      highlight: s.localSec < 26 ? { from: ep.world.lastFrom, to: ep.world.lastTo } : null,
    });
    drawHistogram(ctx, ep.world.wealth, HIST, { lo: 0, hi: 500, binCount: 40, title: '資産の分布', maxCount: 16 });
    drawSeries(ctx, ep.series, SER, {
      lo: 0, hi: 0.7, title: 'ジニ係数（格差の指標）', color: C.warn,
      valueLabel: (v) => v.toFixed(3),
      guides: [{ v: 0, label: '完全な平等', color: C.good }],
    });
    statRow(ctx, ep);
    const c = captionAt(this.captions, s.localSec);
    caption(ctx, c.text, c.alpha);
  },
};

const S_SCALE = {
  id: 'scale',
  dur: 150,
  steps: 1_000_000,
  rate: 'ramp',
  title: 'スケールアップ（1000人・100万回）',
  captions: [
    { at: 0, text: '1000人にして、100万回の取引を回します。' },
    { at: 9, text: '今度は資産の多い順に並べて表示します。' },
    { at: 18, text: '最初は全員が同じ高さの、きれいな長方形です。' },
    { at: 28, text: '崩れ始めました。' },
    { at: 38, text: '2万回。すでに右肩下がりの曲線ができています。' },
    { at: 50, text: '4万回。左端の数人が上へ突き抜けていきます。' },
    { at: 62, text: 'この曲線には名前があります。指数分布です。' },
    { at: 74, text: '統計力学で、気体分子のエネルギー分布として現れる形と同じものです。' },
    { at: 88, text: 'ランダムにやりとりされる保存量は、必ずこの形に落ち着きます。' },
    { at: 100, text: 'つまりこれは経済の話である前に、統計の必然です。' },
    { at: 112, text: '60万回。ジニ係数は0.49まで来て、そこから動かなくなりました。' },
    { at: 122, text: '増えているのは取引回数だけで、格差の形はもう変わりません。' },
    { at: 134, text: '100万回に到達。ジニ係数0.50は、指数分布の理論値とぴったり一致します。' },
    { at: 143, text: 'では、ルールをたった一行だけ変えてみます。' },
  ],
  enter(ep) {
    ep.world = new WealthWorld({ n: 1000, seed: SEED_MAIN });
    ep.series = new Series(150 * FPS);
  },
  draw(ctx, s, ep) {
    clear(ctx);
    header(ctx, '1000人 / 100万回', `${formatInt(ep.world.trades)} 回`);
    drawSortedBars(ctx, ep.world, LEFT, { label: '1000人の資産（多い順）', hiScale: 750 });
    drawHistogram(ctx, ep.world.wealth, HIST, { lo: 0, hi: 700, binCount: 40, title: '資産の分布', maxCount: 200 });
    drawSeries(ctx, ep.series, SER, {
      lo: 0, hi: 0.7, title: 'ジニ係数', color: C.warn,
      valueLabel: (v) => v.toFixed(3),
      guides: [{ v: 0.5, label: '指数分布の理論値 0.500', color: C.fgFaint }],
    });
    statRow(ctx, ep);

    const ea = window01(s.localSec, 145, 146.2, 149.2, 150);
    if (ea > 0) {
      statementCard(ctx, [
        { t: 'ランダムに配るだけで', size: 52 },
        { t: '必ず指数分布に落ち着く', size: 68, color: C.accent },
      ], ea);
    }

    const c = captionAt(this.captions, s.localSec);
    caption(ctx, c.text, c.alpha);
  },
};

const S_DEBT = {
  id: 'debt',
  dur: 90,
  steps: 1_000_000,
  rate: 'ramp',
  title: '条件変更1：下限の壁を外す',
  captions: [
    { at: 0, text: '変えるのは一行だけ。「持っている額を超えても渡せる」にします。' },
    { at: 9, text: 'つまりマイナスまで払える。借金を許すということです。' },
    { at: 17, text: '同じ1000人、同じ100万回、乱数の種も同じです。' },
    { at: 24, text: 'これで格差はなくなるでしょうか。' },
    { at: 30, text: '分布の形は確かに変わりました。指数分布ではなく、左右対称の釣鐘型です。' },
    { at: 41, text: 'ランダムウォークそのものの形です。' },
    { at: 48, text: 'ところが、散らばりの大きさを見てください。まだ伸び続けています。' },
    { at: 55, text: '壁があったときは標準偏差 ¥99 で止まりました。今はもう ¥128 です。' },
    { at: 64, text: '格差は縮むどころか広がっています。しかも止まりません。' },
    { at: 72, text: '取引回数の平方根に比例して、永久に発散し続けます。' },
    { at: 80, text: '100万回で標準偏差 ¥224。1000人のうち330人が借金を抱えました。' },
  ],
  enter(ep) {
    ep.snapshots.baseline = Float64Array.from(ep.world.wealth);
    ep.world = new WealthWorld({ n: 1000, seed: SEED_MAIN, allowDebt: true });
    ep.series = new Series(90 * FPS);
  },
  draw(ctx, s, ep) {
    clear(ctx);
    header(ctx, '条件変更 1：¥0 の壁を外すと？', `${formatInt(ep.world.trades)} 回`);
    drawSortedBars(ctx, ep.world, LEFT, {
      label: '1000人の資産（多い順）／借金あり', hiScale: 900, loScale: -600,
    });
    drawHistogram(ctx, ep.world.wealth, HIST, {
      lo: -600, hi: 900, binCount: 40, title: '資産の分布（借金あり）', maxCount: 90,
    });
    drawSeries(ctx, ep.series, SER, {
      lo: 0, hi: 260, title: '標準偏差（散らばりの大きさ）', color: C.bad,
      valueLabel: (v) => `¥${v.toFixed(0)}`,
      guides: [{ v: 99, label: '壁があったとき ¥99', color: C.fgFaint }],
    });
    statRow(ctx, ep);

    const ea = window01(s.localSec, 85, 86.2, 89.2, 90);
    if (ea > 0) {
      statementCard(ctx, [
        { t: '¥0 の壁は格差の原因ではなく', size: 52 },
        { t: '発散を止めるブレーキだった', size: 68, color: C.accent },
      ], ea);
    }

    const c = captionAt(this.captions, s.localSec);
    caption(ctx, c.text, c.alpha);
  },
};

const S_TAX = {
  id: 'tax',
  dur: 75,
  steps: 1_000_000,
  rate: 'ramp',
  title: '条件変更2：再分配',
  captions: [
    { at: 0, text: 'もう一度、元のルールに戻します。' },
    { at: 6, text: 'そこに再分配だけを足します。' },
    { at: 12, text: '1万回に1度、平均を超えた分の30%を集めて、全員に等分する。' },
    { at: 23, text: '100万回のあいだに、たった100回だけ実行されます。' },
    { at: 31, text: 'ジニ係数を見てください。0.5まで上がりません。' },
    { at: 40, text: '0.2前後で頭打ちになりました。' },
    { at: 50, text: '上位10%の取り分も、33%から15%に下がっています。' },
    { at: 57, text: '取引のルール自体は、何ひとつ変えていないのに、です。' },
    { at: 66, text: '最終的にジニ係数0.20。無一文の人はひとりも残りませんでした。' },
  ],
  enter(ep) {
    ep.snapshots.debt = Float64Array.from(ep.world.wealth);
    ep.world = new WealthWorld({ n: 1000, seed: SEED_MAIN, taxEvery: 10_000, taxRate: 0.3 });
    ep.series = new Series(75 * FPS);
  },
  draw(ctx, s, ep) {
    clear(ctx);
    header(ctx, '条件変更 2：1万回ごとに30%だけ再分配', `${formatInt(ep.world.trades)} 回`);
    drawSortedBars(ctx, ep.world, LEFT, { label: '1000人の資産（多い順）／再分配あり', hiScale: 750 });
    drawHistogram(ctx, ep.world.wealth, HIST, { lo: 0, hi: 700, binCount: 40, title: '資産の分布（再分配あり）', maxCount: 200 });
    drawSeries(ctx, ep.series, SER, {
      lo: 0, hi: 0.7, title: 'ジニ係数', color: C.good,
      valueLabel: (v) => v.toFixed(3),
      guides: [{ v: 0.5, label: '再分配なしの収束先 0.50', color: C.warn }],
    });
    statRow(ctx, ep);
    const c = captionAt(this.captions, s.localSec);
    caption(ctx, c.text, c.alpha);
  },
};

const S_OUTRO = {
  id: 'outro',
  dur: 45,
  title: '結論',
  captions: [
    { at: 0, text: '3つの結果を並べます。' },
    { at: 5, text: '人数も回数も乱数も同じ。違うのはルールの一行だけです。' },
    { at: 14, text: '全員が同じ額から始め、全員が対等に振る舞っても、格差は生まれます。' },
    { at: 23, text: 'これは避けられません。ランダムであることの必然だからです。' },
    { at: 31, text: 'ただし、どこまで開くかは設計の側で決まります。' },
    { at: 38, text: '次回は、この1000人に「働いて稼ぐ」を足したらどうなるかを試します。' },
  ],
  enter(ep) {
    ep.snapshots.tax = Float64Array.from(ep.world.wealth);
  },
  draw(ctx, s, ep) {
    clear(ctx);
    header(ctx, '結論', 'シミュレーション #01');

    const boxes = [
      { key: 'baseline', title: '① 元のルール', metric: (d) => ['ジニ係数', gini(d).toFixed(3)], color: C.warn },
      { key: 'debt', title: '② ¥0 の壁を外す', metric: (d) => ['標準偏差', `¥${sd(d).toFixed(0)}`], color: C.bad },
      { key: 'tax', title: '③ 再分配あり', metric: (d) => ['ジニ係数', gini(d).toFixed(3)], color: C.good },
    ];
    boxes.forEach((b, i) => {
      const data = ep.snapshots[b.key];
      if (!data) return;
      const a = window01(s.localSec, 1 + i * 1.5, 2.2 + i * 1.5, 999, 1000);
      const x = 60 + i * 610;
      drawHistogram(ctx, data, { x, y: 140, w: 580, h: 340 }, {
        lo: -600, hi: 900, binCount: 34, title: b.title, alpha: a,
      });
      const [label, value] = b.metric(data);
      counter(ctx, label, value, x + 24, 496, { alpha: a, color: b.color, size: 52 });
    });

    // 結論だけは3枚のグラフを残したまま下部に出す（比較しながら聞かせたいため）
    const ma = window01(s.localSec, 14, 16, 999, 1000);
    if (ma > 0) {
      ctx.save();
      ctx.globalAlpha = ma * 0.92;
      ctx.fillStyle = '#00040d';
      ctx.fillRect(0, 596, W, 190);
      ctx.restore();
      text(ctx, '格差が生まれること自体は避けられない', W / 2, 648, {
        font: F.title(44), color: C.fg, align: 'center', baseline: 'middle', alpha: ma,
      });
      text(ctx, '決められるのは、どこまで開くか', W / 2, 730, {
        font: F.title(58), color: C.accent, align: 'center', baseline: 'middle', alpha: ma,
      });
    }

    text(ctx, '次回：働いて稼ぐ人を混ぜたら、格差はどうなるか', W / 2, 900, {
      font: F.bold(38), color: C.fgDim, align: 'center', baseline: 'middle',
      alpha: window01(s.localSec, 38, 39.5, 999, 1000),
    });

    const c = captionAt(this.captions, s.localSec);
    caption(ctx, c.text, c.alpha);
  },
};

function sd(arr) {
  let m = 0;
  for (let i = 0; i < arr.length; i++) m += arr[i];
  m /= arr.length;
  let q = 0;
  for (let i = 0; i < arr.length; i++) q += (arr[i] - m) ** 2;
  return Math.sqrt(q / arr.length);
}

export const SCENES = [S_HOOK, S_RULES, S_RUN1, S_SCALE, S_DEBT, S_TAX, S_OUTRO];

export function build() {
  const ep = new Episode();
  const tl = new Timeline(FPS, SCENES);
  const runner = new Runner(tl, ep);
  return { ep, tl, runner };
}
