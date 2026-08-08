// シード付き擬似乱数。全シミュレーションはこれ経由でのみ乱数を引くこと。
// Math.random() を使うと同じ結果を二度と再現できず、編集で詰む。

export class Rng {
  constructor(seed = 1) {
    this.seed = seed >>> 0;
    this.s = this.seed;
  }

  reset() {
    this.s = this.seed;
  }

  // mulberry32
  next() {
    this.s = (this.s + 0x6d2b79f5) >>> 0;
    let t = this.s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  }

  // [0, n) の整数
  int(n) {
    return (this.next() * n) | 0;
  }

  range(lo, hi) {
    return lo + this.next() * (hi - lo);
  }

  pick(arr) {
    return arr[this.int(arr.length)];
  }
}
