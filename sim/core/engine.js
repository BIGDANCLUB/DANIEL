// フレーム駆動タイムライン。
//
// 設計上の要点:
//  - 実時間で録画しない。requestAnimationFrame は一切使わず、frame 番号だけで全状態が決まる。
//    録画マシンが遅くても速くても、出来上がる動画は1フレーム単位で同一になる。
//  - シミュレーションの試行回数はイージングで配分する。序盤はゆっくり見せ、
//    後半で一気に回す = 「時間の圧縮」がこのシリーズの演出の本質。

import { ease } from './render.js';

export class Timeline {
  /**
   * @param {number} fps
   * @param {Array} scenes - { id, dur(秒), steps?(そのシーンで消化する総試行回数),
   *                           rate?(イージング名), enter?(ep), draw(ctx, s) }
   */
  constructor(fps, scenes) {
    this.fps = fps;
    this.scenes = scenes;
    let acc = 0;
    for (const s of scenes) {
      s.startSec = acc;
      s.frames = Math.round(s.dur * fps);
      s.startFrame = Math.round(acc * fps);
      acc += s.dur;
    }
    this.durationSec = acc;
    this.totalFrames = Math.round(acc * fps);
  }

  sceneAt(frame) {
    for (let i = this.scenes.length - 1; i >= 0; i--) {
      if (frame >= this.scenes[i].startFrame) return this.scenes[i];
    }
    return this.scenes[0];
  }

  // そのシーン内で localFrame までに消化しているべき累積試行回数。
  // rampEnd はシーンの何割の時点で試行を打ち切るか。残りは最終結果を見せる「溜め」に使う。
  // これがないと、最後の数字を読み上げている最中にカウンタがまだ動いていて字幕と合わない。
  cumulativeSteps(scene, localFrame) {
    if (!scene.steps) return 0;
    const span = Math.max(1, scene.frames * (scene.rampEnd ?? 0.88));
    const p = Math.min(1, localFrame / span);
    const fn = ease[scene.rate || 'ramp'] || ease.ramp;
    return Math.round(scene.steps * fn(p));
  }
}

export class Runner {
  constructor(timeline, episode) {
    this.tl = timeline;
    this.ep = episode;
    this.cursor = -1;
    this.currentSceneId = null;
    this.sceneCum = 0;
  }

  // frame を1つ進める（描画はしない）。副作用はここだけに閉じる。
  _advanceTo(frame) {
    for (let f = this.cursor + 1; f <= frame; f++) {
      const scene = this.tl.sceneAt(f);
      if (scene.id !== this.currentSceneId) {
        this.currentSceneId = scene.id;
        this.sceneCum = 0;
        if (scene.enter) scene.enter(this.ep);
      }
      const localFrame = f - scene.startFrame;
      const want = this.tl.cumulativeSteps(scene, localFrame);
      const delta = want - this.sceneCum;
      if (delta > 0) {
        this.ep.stepSim(delta, scene);
        this.sceneCum = want;
      }
      if (this.ep.onFrame) this.ep.onFrame(f, scene, localFrame);
    }
    this.cursor = frame;
  }

  // 前方シークのみ高速。後方に戻る場合は先頭から静かに再生し直す（プレビュー用途）。
  renderFrame(ctx, frame) {
    if (frame < this.cursor) {
      this.ep.reset();
      this.cursor = -1;
      this.currentSceneId = null;
      this.sceneCum = 0;
    }
    this._advanceTo(frame);

    const scene = this.tl.sceneAt(frame);
    const localFrame = frame - scene.startFrame;
    const state = {
      frame,
      scene,
      localFrame,
      localT: Math.min(1, localFrame / Math.max(1, scene.frames)),
      localSec: localFrame / this.tl.fps,
      sec: frame / this.tl.fps,
      fps: this.tl.fps,
    };
    scene.draw(ctx, state, this.ep);
    return state;
  }
}

// 字幕リスト [{at: 秒, text}] から、その時刻に出すべき字幕を引く。
// ナレーション原稿と1対1で対応させ、script.md を自動生成する元データにもなる。
export function captionAt(list, localSec, holdTail = 999) {
  let cur = null;
  for (const c of list) {
    if (localSec >= c.at) cur = c;
    else break;
  }
  if (!cur) return { text: '', alpha: 0 };
  const idx = list.indexOf(cur);
  const next = list[idx + 1];
  const end = next ? next.at : cur.at + holdTail;
  if (localSec > end) return { text: '', alpha: 0 };
  const fadeIn = Math.min(1, (localSec - cur.at) / 0.25);
  const fadeOut = Math.min(1, (end - localSec) / 0.25);
  return { text: cur.text, alpha: Math.max(0, Math.min(fadeIn, fadeOut)) };
}
