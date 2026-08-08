# シミュレーション動画生成基盤

シリーズA「シミュレーション検証」の共通基盤。1本目 `01-wealth` が実装済みで、
2本目以降はルールとナレーションを書くだけで作れる。

企画の全体像は [`docs/series-a-simulation-plan.md`](../docs/series-a-simulation-plan.md)、
チャンネル方針は [`docs/youtube-series-ideas.md`](../docs/youtube-series-ideas.md) を参照。

## 使い方

```bash
npm install                # playwright のみ

npm run verify             # 字幕の数値と実測値を突き合わせる（台本を直したら必ず）
npm run stills             # 各シーンの静止画を出して構図を確認
npm run smoke              # 冒頭10秒だけ書き出してパイプラインを確認
npm run render             # 本編 10分 を書き出す（約30分）
npm run script             # ナレーション原稿(.md)と字幕(.srt)を書き出す
```

ブラウザで `sim/episodes/01-wealth/index.html` を直接開けば、
再生・シーク・シーンジャンプができるプレビューになる（要ローカルサーバ）。

## 設計上の約束ごと

この4つを守らないと、10分尺の動画づくりは編集段階で破綻する。

**1. 実時間で録画しない。**
`requestAnimationFrame` は録画経路で一切使わない。`SIM.renderFrame(i)` に
フレーム番号を渡すと、そのフレームの絵が決まる。マシンが遅くても速くても、
出来上がる動画は1フレーム単位で同一になる。

**2. 乱数は必ずシード付き。**
`Math.random()` を使うと「さっきの結果をもう一度」が再現できず、
ナレーションの数字と画面が永久に合わなくなる。`core/rng.js` 経由でのみ引く。

**3. 試行回数はイージングで配分する。**
`scene.steps` に総試行回数、`scene.rate` に加速カーブを指定すると、
序盤はゆっくり見せて後半で一気に回る。**時間の圧縮がこのシリーズの演出の本質**で、
100万回を実時間で見せる必要はどこにもない。
`scene.rampEnd`（既定 0.88）でシーンの終盤に「結果を見せる溜め」を残す。
これがないと、最後の数字を読み上げている最中にカウンタがまだ動いている。

**4. 指標グラフを常時併走させる。**
粒子や棒が動くだけでは8分もたない。ジニ係数や標準偏差が伸びるグラフと、
回り続けるカウンタを画面に置くと、それだけで滞在時間が変わる。

## 台本の数値は実測から書く

この型の動画は「実測を見せる」ことが価値の全て。ナレーションの数字が
画面のカウンタとズレたら、その時点で動画が嘘になる。

```bash
npm run verify
```

各字幕の時点で画面に出ている実際の取引回数・ジニ係数・最大値を印字するので、
**先に数値を見てから台本を書く**。パラメータや尺を変えたら必ず再実行する。

1本目の制作でも、これで「1000人×100万回では指数分布に到達していない」
「借金を許すと格差は縮むどころか発散する」という2つの誤りが見つかっている。

## 構成

```
sim/
  core/
    rng.js       シード付き乱数
    theme.js     配色・フォント（チャンネルの見た目はここだけで決まる）
    render.js    Canvas2D プリミティブ、字幕、カウンタ、イージング
    charts.js    ヒストグラム、時系列、ジニ係数、上位シェア
    engine.js    タイムライン、フレーム駆動ランナー、字幕引き
  episodes/
    01-wealth/
      model.js    シミュレーション本体（ルールだけ書く）
      episode.js  シーン定義と字幕＝ナレーション原稿
      index.html  プレビュー兼、録画用インターフェース
tools/
  capture.mjs  フレームを PNG で ffmpeg に流して mp4 にする
  stills.mjs   構図確認用の静止画
  verify.mjs   字幕と実測値の突き合わせ
  script.mjs   ナレーション原稿と SRT の書き出し
```

## 新しいエピソードの作り方

1. `sim/episodes/NN-name/model.js` にルールを書く（`step()` と `stats()` だけ）
2. `episode.js` にシーンと字幕を書く。レイアウト定数と描画部品は 01 からコピーでよい
3. `npm run verify -- --episode NN-name` で実測値を見る
4. **実測値に合わせて字幕を書き直す**
5. `npm run stills` で構図を確認
6. `npm run render` で書き出す

## 環境メモ

- Chromium は `/opt/pw-browsers/chromium` を使う（`playwright install` は実行しない）
- 日本語表示には `fonts-noto-cjk` が必要
- ffmpeg は libx264 が入っているものを使う
