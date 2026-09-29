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
   - `tone` … その一文の気持ち（例「不安で声が沈む。ゆっくり」）。`tts.style` の人物像・演技指示と合わせて TTS に渡し、抑揚をつける
   - `prompt` … その行の画像の指示（英語推奨・画像内に文字を入れない）
   - `move` … `in` / `out` / `left` / `right` / `up` / `down`（省略時は自動で交互）
   - `se` … その行の頭に効果音（`don` 重い一打 / `coin` チャリン。合成音なので素材不要）
   - 台本トップの `banner` … 画面上部に出し続ける概要帯（`\n` で2行、`{…}` 黄）
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

## その他
- `python3 tts_gemini.py --list-models` … 使える TTS モデル名の確認（モデル名が変わったとき用）
- `story_st003b.json` … 元動画の声と背景を再利用する版（`--source 元動画.mp4` が必要。背景は `extract_plates.py` で作成）
