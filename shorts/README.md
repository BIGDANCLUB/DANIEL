# ショート動画ジェネレーター

縦型ショート（1080x1920・45〜55秒）を台本JSONから作ります。
全面画像を1行ごとに切り替え、画面中央に縁取り字幕（`{黄}` `<赤>`）を出す形式です。BGMは入れません。

## 準備
- 環境変数 `GEMINI_API_KEY` に Gemini API キーを登録（音声・画像の自動生成に使用）
- `pip install -r shorts/requirements.txt`

## 流れ
1. 台本 `story_xxx.json` を書く（`story_st003b_ai.json` が見本）
   - `text` … 字幕。`\n` で改行、`{…}` 黄、`<…>` 赤。`"hook": true` で大きい黄色のフック
   - `say` … 読み上げ文（省略時は `text` から自動）。読み間違いの修正にも使う
   - フィクションなので具体的な人名は出さない（「私は〇〇、72歳です」のような名乗りは入れない。年齢や立場は「72歳の私」「定年して」などで伝える）
   - 声（`tts.voice`）は語り手（登場人物）の性別に合わせる（視聴ターゲットの性別ではない）。男性語りの見本は `story_st004_ai.json`（Algenib）
   - `tone` … その一文の気持ち（例「不安で声が沈む。ゆっくり」）。`tts.style` の人物像・演技指示と合わせて TTS に渡し、抑揚をつける
   - `prompt` … その行の画像の指示（英語推奨・画像内に文字を入れない）
   - 画像を安くするなら行ごとの `prompt` の代わりに場面で指定する（1枚を2行ほどで使い回すと画像代は約半分）
     - 台本トップの `scenes` … `{"病室": {"prompt": "..."}}`、またはライブラリの画像をそのまま使う `{"病室": {"library": "st004_ai_06"}}`（生成しないので無料）
     - 行の `scene` … 使う場面名。`crop` … `[中心x, 中心y, 拡大率]`（x,y は0〜1、拡大率1で全体。1.8程度まで）
     - 場面の変わり目（危機→制度→解決）は別の画像にすると単調にならない
   - `move` … `in` / `out` / `left` / `right` / `up` / `down`（省略時は自動で交互）
   - `se` … その行の頭に効果音（`coin` チャリン などの合成音、または `se/` に置いたファイル名）
   - 冒頭SE … 全動画の0秒目に `se/チリン.mp3` を固定で鳴らす（1行目の `se` より優先）。台本トップの `intro_se` で別のファイル名、`"none"` で無し。`intro_se_volume` で音量（dB、既定 -3）
   - 台本トップの `banner` … 画面上部に出し続ける概要帯（`\n` で2行、`{…}` 黄）
   - BGM … `bgm/` に置いた曲から動画ごとにランダムで1曲選び、全編に流す（冒頭0.8秒フェードイン、最後2秒フェードアウト、声の間は自動で音量を下げる）
     - 台本トップの `bgm` … 省略で全曲からランダム、`"random:スカッと"` で `bgm/スカッと/` の中から、`"曲名.mp3"` で指定、`"none"` でなし
     - `bgm_volume` … BGMの音量（dB、既定 -10。声より約10dB小さくなる。大きい/小さいときはここで調整）
     - 選ばれた曲は `out/xxx_work/bgm_choice.txt` に記録され、作り直しても同じ曲になる（変えたいときはこのファイルを消す）
   - 赤字 `<…>` は表示直後にもう一度ポンと弾む
2. `python3 make_short.py story_xxx.json out/xxx.mp4`
   - 足りない音声（Gemini TTS）と画像（Gemini 画像モデル）を生成してから動画を書き出す
   - 生成物は `tts.voice_dir` / `image_gen.image_dir` に保存され、次回は再利用
3. 直したいとき
   - 画像だけ作り直す: `python3 gen_images_gemini.py story_xxx.json --only 3,7`
   - 声を全部作り直す: `python3 tts_gemini.py story_xxx.json --force`
   - 手で用意した音声・画像は `NN.wav` / `NN.png` として同じフォルダに置けばそれを使う
   - 尺が45〜55秒から外れると、合わせるための `tempo` の目安を表示する
   - 感情をこめた読みは行の途中に長い間が入りやすい。台本トップの `max_pause`（秒、既定0.3）より長い間は自動で詰める

## 画像ライブラリ（作品をまたいだ使い回し）
- 生成した画像は `library/` に JPEG で登録される。同じプロンプト・モデル・スタイルの画像があれば生成せずにコピーする
- `python3 gen_images_gemini.py --library 病院` … キーワードで一覧（名前とプロンプト）
- `python3 gen_images_gemini.py story_xxx.json --seed-library` … 生成済みの画像をまとめて登録
- 画像モデルの既定は `gemini-3.1-flash-lite-image`（通常版と画像トークン数は同じで、画質もほぼ同等）

## サムネイル
- `python3 make_thumb.py story_xxx.json out/xxx_thumb.jpg` … 1080x1920 のサムネイル（API不要）
- 背景は1行目の画像、見出しは台本トップの `thumb`（`\n` で改行、`{黄}` `<赤>`）。タグは `thumb_tag`（省略時は banner の1行目）

## その他
- `python3 tts_gemini.py --list-models` … 使える TTS モデル名の確認（モデル名が変わったとき用）
- `story_st003b.json` … 元動画の声と背景を再利用する版（`--source 元動画.mp4` が必要。背景は `extract_plates.py` で作成）
