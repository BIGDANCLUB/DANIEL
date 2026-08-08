// 全エピソード共通のビジュアル定義。チャンネルの見た目はここだけで決まる。

export const W = 1920;
export const H = 1080;

export const C = {
  bg: '#0b1020',
  bgPanel: '#121a2e',
  grid: '#1e2a45',
  fg: '#e8edf7',
  fgDim: '#8b9ab5',
  fgFaint: '#4a5872',

  // 富の少ない→多い のスケール（分布とエージェント両方で共有）
  poor: '#3b82f6',
  mid: '#22d3ee',
  rich: '#fbbf24',
  richest: '#f97316',

  accent: '#22d3ee',
  warn: '#f97316',
  good: '#34d399',
  bad: '#f43f5e',
};

const JP = '"Noto Sans CJK JP", "IPAGothic", sans-serif';
const MONO = '"Noto Sans Mono CJK JP", monospace';

export const F = {
  title: (px) => `700 ${px}px ${JP}`,
  body: (px) => `400 ${px}px ${JP}`,
  bold: (px) => `700 ${px}px ${JP}`,
  num: (px) => `700 ${px}px ${MONO}`,
};

// 資産額 -> 色。全シーンで同じスケールを使うことで比較可能にする。
export function wealthColor(v, ref = 100) {
  const r = v / ref;
  if (r < 0) return C.bad;
  if (r < 0.5) return C.poor;
  if (r < 1.5) return C.mid;
  if (r < 3) return C.rich;
  return C.richest;
}
