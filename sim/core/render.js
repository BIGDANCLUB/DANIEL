// Canvas2D 描画プリミティブ。エピソード側は極力ここの関数だけで絵を作る。

import { C, F, W, H } from './theme.js';

export const clamp = (v, lo, hi) => (v < lo ? lo : v > hi ? hi : v);
export const lerp = (a, b, t) => a + (b - a) * t;

export const ease = {
  linear: (t) => t,
  inOut: (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2),
  out: (t) => 1 - Math.pow(1 - t, 3),
  in: (t) => t * t * t,
  // 試行回数の加速に使う。序盤ゆっくり見せて後半一気に回す。
  ramp: (t) => Math.pow(t, 3.2),
};

// 0->1 のフェード窓。t が [a,b] の間だけ 1 になる台形。
export function window01(t, fadeIn0, fadeIn1, fadeOut0, fadeOut1) {
  if (t < fadeIn0 || t > fadeOut1) return 0;
  if (t < fadeIn1) return ease.out((t - fadeIn0) / Math.max(1e-6, fadeIn1 - fadeIn0));
  if (t < fadeOut0) return 1;
  return 1 - ease.in((t - fadeOut0) / Math.max(1e-6, fadeOut1 - fadeOut0));
}

export function clear(ctx) {
  ctx.fillStyle = C.bg;
  ctx.fillRect(0, 0, W, H);
}

export function roundRect(ctx, x, y, w, h, r) {
  const rr = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + rr, y);
  ctx.arcTo(x + w, y, x + w, y + h, rr);
  ctx.arcTo(x + w, y + h, x, y + h, rr);
  ctx.arcTo(x, y + h, x, y, rr);
  ctx.arcTo(x, y, x + w, y, rr);
  ctx.closePath();
}

export function panel(ctx, x, y, w, h, alpha = 1) {
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.fillStyle = C.bgPanel;
  roundRect(ctx, x, y, w, h, 16);
  ctx.fill();
  ctx.strokeStyle = C.grid;
  ctx.lineWidth = 2;
  ctx.stroke();
  ctx.restore();
}

export function text(ctx, str, x, y, { font = F.body(32), color = C.fg, align = 'left', baseline = 'alphabetic', alpha = 1, maxWidth } = {}) {
  if (alpha <= 0) return;
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.font = font;
  ctx.fillStyle = color;
  ctx.textAlign = align;
  ctx.textBaseline = baseline;
  if (maxWidth) ctx.fillText(str, x, y, maxWidth);
  else ctx.fillText(str, x, y);
  ctx.restore();
}

// 画面下部の字幕。ナレーション原稿と1対1で対応させる。
export function caption(ctx, str, alpha = 1) {
  if (!str || alpha <= 0) return;
  const lines = String(str).split('\n');
  const fs = 40;
  const lh = 58;
  const boxH = lines.length * lh + 36;
  const y = H - 60 - boxH;

  ctx.save();
  ctx.globalAlpha = alpha * 0.82;
  ctx.fillStyle = '#00040d';
  roundRect(ctx, 140, y, W - 280, boxH, 14);
  ctx.fill();
  ctx.restore();

  lines.forEach((ln, i) => {
    text(ctx, ln, W / 2, y + 18 + lh * i + lh / 2, {
      font: F.body(fs), color: C.fg, align: 'center', baseline: 'middle', alpha,
    });
  });
}

// 常時表示のカウンタ。回り続けるだけで滞在時間が伸びる。
export function counter(ctx, label, value, x, y, { alpha = 1, color = C.accent, size = 64 } = {}) {
  text(ctx, label, x, y, { font: F.body(24), color: C.fgDim, alpha, baseline: 'top' });
  text(ctx, value, x, y + 34, { font: F.num(size), color, alpha, baseline: 'top' });
}

export function hLine(ctx, x0, x1, y, color = C.grid, width = 2, dash = null) {
  ctx.save();
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  if (dash) ctx.setLineDash(dash);
  ctx.beginPath();
  ctx.moveTo(x0, y);
  ctx.lineTo(x1, y);
  ctx.stroke();
  ctx.restore();
}

export function formatInt(n) {
  return Math.floor(n).toLocaleString('en-US');
}

export function formatYen(n) {
  const s = Math.round(n).toLocaleString('en-US');
  return `¥${s}`;
}
