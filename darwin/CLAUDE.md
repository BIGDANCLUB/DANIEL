# darwin — ダーウィンが来た風ショート 生成パイプライン（Claude Code 用の作業メモ）

このフォルダでは **Claude がコマンドを実行する**。ユーザーに PowerShell を打たせない。
ユーザーに頼むのは「Colab の起動セルを実行して URL を教えてもらう」「完成物を見て判断してもらう」だけ。

## 環境（Windows / PowerShell）
- 作業フォルダ: `C:\work\daniel\darwin`（git: bigdanclub/daniel, ブランチ `claude/horse-racing-uncle-script-trojcd`）
- Python: `C:\Users\genji\AppData\Local\Programs\Python\Python310\python.exe`（ugoira と同じ。cv2 入り）
- ffmpeg: PATH にあり（8.x）
- ugoira: `C:\Users\genji\OneDrive\デスクトップ\ugoira`（`tools/comfy_h3.py` がここの `h3.py` を import して `h3.render()` を呼ぶ）
- `GEMINI_API_KEY`: ユーザー環境変数に設定済み（Tier 1・前払い）。**値を表示・ログ出力しない**
- Codex で作った画像の置き場（OneDrive）: `C:\Users\genji\OneDrive\ドキュメント\ChatGPT\ダーウィン解説\episodes\<話>\images\`
  → 生成前に `episodes\<話>\images\` へコピーする

## 工程とコマンド（例: 01-keiba）
1. 画像プロンプト: `python tools/image_prompts.py 01-keiba` → `out/image_prompts.md`（ユーザーが Codex で生成）
2. ナレーション（Gemini TTS）: `python tools/tts_gemini.py 01-keiba --lines`
   - 生成済みの文はスキップ。作り直し: `--redo 03_seitai:2` / `--redo all`
   - 声の比較: `--audition A B ...`、全文比較: `--voice X --preview`（本番は変えない）
   - 速度や無音カットは後処理なので API を呼ばずに変更できる（config の `gemini.tempo` など）
3. 映像（Colab の ComfyUI + MiniMax H3）:
   - `$env:UGOIRA_COMFY_URL = "<ユーザーから受け取った trycloudflare URL>"` を同じシェルで設定してから
   - `python tools/comfy_h3.py 01-keiba --plan`（Colab 不要。フレーム数の確認）
   - `python tools/comfy_h3.py 01-keiba --only 02_hakken`（まず1本）→ 全部: 引数なし
   - 撮り直し: `--redo <id> [--seed N]`。1本 A100 80GB で数分。長時間かかるので**バックグラウンド実行して進捗を見る**
4. 結合: `python tools/assemble.py 01-keiba` → `out/final.mp4`, `out/subtitles.srt`
- 動作確認だけ: `python tools/run_all.py 01-keiba --mock`（終わったら `out` を必ず削除。残すと本番でダミーが使われる）

## いま作っているもの：異種対決シリーズ `vs01-kangaroo-ostrich`（2026-09-28〜）
- **01-keiba と 02-pachinko はお蔵入り**（ユーザー判断）。ファイルは残してあるが作業しない
- 16:9・約 8 分 50 秒（530 秒）・54 ショット。1 セクション＝1 ショットで `duration`（再生尺）が決め打ち
  - `source: h3`（32 本・MiniMax H3 1344x768）/ `opus`（17 本・Claude が HTML で作る図解）/ `reuse`（5 本・既存クリップの使い回し）
  - `speed` で区間スロー（0.5〜0.2 倍）、`overlay` は H3 映像に重ねる文字（`out/overlays/<ID>.mov`）
  - 勝者はダチョウ（逃走で決着）。体力ゲージは ⑤ の r1 だけ。効果音なし（動物の音は H3 の音）。試作では BGM なし
  - シリーズ名「ありえない野生対決」は仮
- 手順（`episodes/vs01-kangaroo-ostrich`）
  1. `python tools/image_prompts.py vs01-kangaroo-ostrich` → Codex で 32 枚（横 16:9、まず m2・m3 を作って参照画像に）
  2. `python tools/tts_gemini.py vs01-kangaroo-ostrich --lines`（作成済み。ショットの尺まで無音で埋める）
  3. `python tools/opus_render.py vs01-kangaroo-ostrich`（`graphics/index.html` を Chrome ヘッドレスでコマ撮り。
     `--still r1:6` で静止画確認。r1・m4・c3 は `images/m2,m3,c2.png` があれば写真、無ければシルエット → 画像が揃ったら `--only m4 r1 c3` で作り直す）
  4. `python tools/comfy_h3.py vs01-kangaroo-ostrich`（`gen_seconds` の長さで生成。スローは結合時）
  5. `python tools/assemble.py vs01-kangaroo-ostrich`（スローのコマ補間は config `render.interp`：blend＝速い / minterpolate＝きれいだが遅い。
     `out/clips/<ID>_rife.mp4` があれば優先）。`--only <ID>` でショット単体を `out/work/v_<ID>.mp4` に作って確認できる

## 決定事項（01-keiba）
- 声 `Zubenelgenubi`、速度 1.1 倍、男性ナレーター・やや高めで明るい語り口（config.example.json）
- **H3 は 1 クリップ 12 秒以下が要件**（`comfy.max_seconds: 12` → 最大 277 フレーム＝11.54 秒）。
  13 秒超（328〜362 フレーム）は NaN で真っ黒になることが多かった（03_seitai は 3 回連続）
- 12 秒を超える【】は文の区切りでセクションを分け、後半に `"start_from": "<前半ID>"` を書く
  → 前半クリップが結合で切られる位置のコマを始点に続きを作る（Codex 画像不要）
- クリップは 10 本: 01_basho / 01_basho_b / 02_hakken / 03_seitai / 03_seitai_b / 03_seitai_c /
  04_tenkan / 05_ochimae / 06_ochi / 06_ochi_b（`_b` の3本は start_from）
- セクション ID を変えたら `out/tts/<声>/<ID>_<番号>.wav` も改名すれば TTS を呼び直さずに済む
- H3: 768x1344、lightx2v 4 step、chest/expressive/add_style は False、music は N/A（BGM は結合時）
- 【】の基本構成（今後も固定）: 場所紹介 → 生き物を発見 → 生態の紹介 → 場面転換 → オチ前 → オチ

## 注意
- Colab は接続中ずっと課金。**生成が終わったらユーザーに「接続解除して削除」を促す**
- トンネル URL は第三者に使われうるので、コミット・ログ・config に書かない
- Gemini の 429（回数制限）は自動で待つ。402 は前払い残高切れ → ユーザーに AI Studio でのチャージを頼む
- 1本目の H3 はモデル読み込み（ドライブから約44GB）で遅い。Colab 側で `!tail -n 20 /content/logs/comfy.log` を見てもらうと状況が分かる
