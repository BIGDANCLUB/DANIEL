// 指標グラフ。粒子だけ見せても8分もたないので、必ず何かのグラフを併走させる。

import { C, F, wealthColor } from './theme.js';
import { text, roundRect, hLine, clamp } from './render.js';

// ジニ係数（0=完全平等, 1=完全独占）。負の値を含む場合は最小値だけ持ち上げて計算する。
export function gini(values) {
  const n = values.length;
  if (n === 0) return 0;
  let arr = Array.from(values);
  const min = Math.min(...arr);
  if (min < 0) arr = arr.map((v) => v - min);
  arr.sort((a, b) => a - b);
  let sum = 0;
  let weighted = 0;
  for (let i = 0; i < n; i++) {
    sum += arr[i];
    weighted += (i + 1) * arr[i];
  }
  if (sum === 0) return 0;
  return (2 * weighted) / (n * sum) - (n + 1) / n;
}

// 上位x%が全体の何%を持つか
export function topShare(values, frac) {
  const arr = Array.from(values).sort((a, b) => b - a);
  const k = Math.max(1, Math.round(arr.length * frac));
  const total = arr.reduce((a, b) => a + b, 0);
  if (total <= 0) return 0;
  let t = 0;
  for (let i = 0; i < k; i++) t += arr[i];
  return t / total;
}

export function histogram(values, binCount, lo, hi) {
  const bins = new Array(binCount).fill(0);
  const span = hi - lo;
  for (let i = 0; i < values.length; i++) {
    let b = Math.floor(((values[i] - lo) / span) * binCount);
    b = clamp(b, 0, binCount - 1);
    bins[b]++;
  }
  return bins;
}

// 資産分布のヒストグラム。この動画の主役。
export function drawHistogram(ctx, values, box, opts = {}) {
  const {
    lo = 0, hi = 400, binCount = 40, title = '資産の分布',
    maxCount = null, alpha = 1, refWealth = 100, xLabel = '一人あたりの資産',
  } = opts;
  const { x, y, w, h } = box;
  if (alpha <= 0) return;

  ctx.save();
  ctx.globalAlpha = alpha;

  const padL = 70, padB = 70, padT = 64, padR = 24;
  const plotX = x + padL, plotY = y + padT;
  const plotW = w - padL - padR, plotH = h - padT - padB;

  text(ctx, title, x + 24, y + 30, { font: F.bold(28), color: C.fg, baseline: 'middle' });

  const bins = histogram(values, binCount, lo, hi);
  const peak = maxCount ?? Math.max(1, ...bins);

  // 横罫線
  for (let i = 0; i <= 4; i++) {
    const gy = plotY + (plotH * i) / 4;
    hLine(ctx, plotX, plotX + plotW, gy, C.grid, 1);
  }

  const bw = plotW / binCount;
  for (let i = 0; i < binCount; i++) {
    const bh = (bins[i] / peak) * plotH;
    if (bh < 0.6) continue;
    const bx = plotX + i * bw;
    const center = lo + ((i + 0.5) / binCount) * (hi - lo);
    ctx.fillStyle = wealthColor(center, refWealth);
    roundRect(ctx, bx + 1.5, plotY + plotH - bh, Math.max(1, bw - 3), bh, Math.min(4, bw / 3));
    ctx.fill();
  }

  // 軸
  hLine(ctx, plotX, plotX + plotW, plotY + plotH, C.fgFaint, 2);
  for (let i = 0; i <= 4; i++) {
    const v = lo + ((hi - lo) * i) / 4;
    const gx = plotX + (plotW * i) / 4;
    text(ctx, `¥${Math.round(v)}`, gx, plotY + plotH + 14, {
      font: F.body(20), color: C.fgDim, align: 'center', baseline: 'top',
    });
  }
  text(ctx, xLabel, plotX + plotW / 2, y + h - 18, {
    font: F.body(20), color: C.fgFaint, align: 'center', baseline: 'bottom',
  });

  // 初期値の位置に基準線
  if (refWealth >= lo && refWealth <= hi) {
    const rx = plotX + ((refWealth - lo) / (hi - lo)) * plotW;
    ctx.save();
    ctx.strokeStyle = C.fgDim;
    ctx.setLineDash([6, 6]);
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(rx, plotY);
    ctx.lineTo(rx, plotY + plotH);
    ctx.stroke();
    ctx.restore();
    text(ctx, 'スタート地点', rx + 8, plotY + 6, { font: F.body(18), color: C.fgDim, baseline: 'top' });
  }

  ctx.restore();
}

// 時系列（ジニ係数の推移など）
export class Series {
  constructor(maxPoints = 900) {
    this.pts = [];
    this.maxPoints = maxPoints;
  }
  reset() { this.pts = []; }
  push(v) {
    this.pts.push(v);
    if (this.pts.length > this.maxPoints) this.pts.shift();
  }
}

export function drawSeries(ctx, series, box, opts = {}) {
  const {
    lo = 0, hi = 1, title = '', color = C.accent, alpha = 1,
    valueLabel = null, guides = [],
  } = opts;
  const { x, y, w, h } = box;
  if (alpha <= 0) return;

  ctx.save();
  ctx.globalAlpha = alpha;

  const padL = 70, padB = 34, padT = 56, padR = 24;
  const plotX = x + padL, plotY = y + padT;
  const plotW = w - padL - padR, plotH = h - padT - padB;

  if (title) text(ctx, title, x + 24, y + 28, { font: F.bold(26), color: C.fg, baseline: 'middle' });

  for (let i = 0; i <= 3; i++) {
    const gy = plotY + (plotH * i) / 3;
    hLine(ctx, plotX, plotX + plotW, gy, C.grid, 1);
    const v = hi - ((hi - lo) * i) / 3;
    text(ctx, v.toFixed(2), plotX - 12, gy, {
      font: F.body(18), color: C.fgDim, align: 'right', baseline: 'middle',
    });
  }

  for (const g of guides) {
    const gy = plotY + plotH - ((g.v - lo) / (hi - lo)) * plotH;
    hLine(ctx, plotX, plotX + plotW, gy, g.color || C.fgFaint, 2, [8, 8]);
    if (g.label) {
      text(ctx, g.label, plotX + plotW - 8, gy - 8, {
        font: F.body(18), color: g.color || C.fgFaint, align: 'right', baseline: 'bottom',
      });
    }
  }

  const pts = series.pts;
  if (pts.length > 1) {
    ctx.beginPath();
    for (let i = 0; i < pts.length; i++) {
      const px = plotX + (i / (series.maxPoints - 1)) * plotW;
      const py = plotY + plotH - ((clamp(pts[i], lo, hi) - lo) / (hi - lo)) * plotH;
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.strokeStyle = color;
    ctx.lineWidth = 4;
    ctx.lineJoin = 'round';
    ctx.stroke();

    const last = pts[pts.length - 1];
    const lx = plotX + ((pts.length - 1) / (series.maxPoints - 1)) * plotW;
    const ly = plotY + plotH - ((clamp(last, lo, hi) - lo) / (hi - lo)) * plotH;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(lx, ly, 7, 0, Math.PI * 2);
    ctx.fill();

    if (valueLabel) {
      text(ctx, valueLabel(last), x + w - 24, y + 28, {
        font: F.num(34), color, align: 'right', baseline: 'middle',
      });
    }
  }

  ctx.restore();
}
