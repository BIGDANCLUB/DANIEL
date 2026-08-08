// エピソード#1 のシミュレーション本体。
//
// ルール:
//   全員が同額 (¥100) からスタートし、毎回ランダムに2人を選んで ¥1 を渡す。
//   実力差なし、運の偏りなし、搾取なし。それでも格差は生まれるのか？

import { Rng } from '../../core/rng.js';

export class WealthWorld {
  constructor(opts = {}) {
    this.n = opts.n ?? 100;
    this.start = opts.start ?? 100;
    // 1回あたりの送金額。平衡（指数分布）に達するには 1人あたり (start/unit)^2 の
    // 数十倍の取引が必要で、unit=1 では100万回ではまったく足りない。実測で unit=5 に決定。
    this.unit = opts.unit ?? 5;
    this.allowDebt = opts.allowDebt ?? false;
    this.taxEvery = opts.taxEvery ?? 0;   // 0 = 再分配なし
    this.taxRate = opts.taxRate ?? 0;     // 平均超過分に対する課税率
    this.seed = opts.seed ?? 12345;

    this.rng = new Rng(this.seed);
    this.wealth = new Float64Array(this.n).fill(this.start);
    this.trades = 0;
    this.blocked = 0;          // 所持金ゼロで渡せなかった回数
    this.lastFrom = -1;
    this.lastTo = -1;
    this.taxCount = 0;
  }

  reset() {
    this.rng = new Rng(this.seed);
    this.wealth.fill(this.start);
    this.trades = 0;
    this.blocked = 0;
    this.lastFrom = -1;
    this.lastTo = -1;
    this.taxCount = 0;
  }

  // 1回の取引。
  step() {
    const n = this.n;
    const from = this.rng.int(n);
    let to = this.rng.int(n);
    if (to === from) to = (to + 1) % n;

    // 借金を許さない場合、払える分しか渡せない（この判定が結果を決定的に変える）
    const amount = this.allowDebt ? this.unit : Math.min(this.unit, Math.max(0, this.wealth[from]));
    if (amount <= 0) {
      this.blocked++;
    } else {
      this.wealth[from] -= amount;
      this.wealth[to] += amount;
      this.lastFrom = from;
      this.lastTo = to;
    }
    this.trades++;

    if (this.taxEvery > 0 && this.trades % this.taxEvery === 0) this.redistribute();
  }

  // 平均を超えた分に課税し、全員に等分して配る
  redistribute() {
    const n = this.n;
    let mean = 0;
    for (let i = 0; i < n; i++) mean += this.wealth[i];
    mean /= n;
    let pot = 0;
    for (let i = 0; i < n; i++) {
      if (this.wealth[i] > mean) {
        const t = (this.wealth[i] - mean) * this.taxRate;
        this.wealth[i] -= t;
        pot += t;
      }
    }
    const share = pot / n;
    for (let i = 0; i < n; i++) this.wealth[i] += share;
    this.taxCount++;
  }

  run(steps) {
    for (let i = 0; i < steps; i++) this.step();
  }

  stats() {
    const n = this.n;
    let min = Infinity, max = -Infinity, sum = 0, broke = 0;
    for (let i = 0; i < n; i++) {
      const v = this.wealth[i];
      if (v < min) min = v;
      if (v > max) max = v;
      sum += v;
      if (v <= 0) broke++;
    }
    const mean = sum / n;
    let sq = 0;
    for (let i = 0; i < n; i++) sq += (this.wealth[i] - mean) ** 2;
    return { min, max, mean, total: sum, broke, sd: Math.sqrt(sq / n) };
  }

  // 資産順に並べた配列（可視化用。元配列は壊さない）
  sorted() {
    return Array.from(this.wealth).sort((a, b) => b - a);
  }
}
