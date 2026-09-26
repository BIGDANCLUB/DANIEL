# ダーウィンが来た風ショート 生成パイプライン

| 工程 | 担当 | 実行場所 |
|---|---|---|
| 原稿・クリップ設計（`episodes/<id>/episode.json`） | Claude Code | — |
| 画像（【】ごとに1枚） | Codex（imagegen） | `tools/image_prompts.py` でプロンプトを出力 |
| ① ナレーション | Gemini 3.8 Flash TTS | `tools/tts_gemini.py` |
| ② 映像（【】ごとに1クリップ） | MiniMax H3（Colab・水無瀬の h3.py を利用） | `tools/comfy_h3.py` |
| ③ 結合（環境音・SE・BGM・字幕） | ffmpeg | `tools/assemble.py` |

**尺はナレーションの実測で決まります。** ①で実際の音声の長さを計り、②はその長さを覆う秒数（4〜15秒）で生成します。15秒を超える【】は③でスロー再生して埋めます。

## GPU（Colab）との接続
水無瀬と同じです。Colab で `colab_h3_drive.ipynb` の「起動」セルを実行し、最後に出る URL を PC で設定します。
```powershell
$env:UGOIRA_COMFY_URL = "https://....trycloudflare.com"
```
映像生成は ugoira フォルダの `h3.py` をそのまま使います（→ [comfy/README.md](comfy/README.md)）。
URL を知っていれば誰でもその ComfyUI を使えるので、config.json やチャットには書かないこと。

## セットアップ（PC で・初回のみ）
- 水無瀬（ugoira）が動いている PC であること（Python・ffmpeg・ugoira の依存が入っている前提）
- 環境変数 `GEMINI_API_KEY`
- ugoira フォルダが `C:\Users\genji\OneDrive\デスクトップ\ugoira` 以外なら、`config.example.json` を `config.json` にコピーして `comfy.ugoira_dir` を変更

## 手順
```bash
cd darwin
python tools/image_prompts.py 01-keiba          # Codex 用プロンプト → episodes/01-keiba/out/image_prompts.md
#   Codex で画像を作り episodes/01-keiba/images/01_basho.png … 06_ochi.png として保存
python tools/tts_gemini.py 01-keiba       # ① ナレーション（実測の尺を表示）
python tools/comfy_h3.py 01-keiba --plan  #    生成フレーム数の計画を確認（Colab 不要）
python tools/comfy_h3.py 01-keiba         # ② 映像
python tools/assemble.py 01-keiba         # ③ → episodes/01-keiba/out/final.mp4
```
撮り直し：`tts_gemini.py 01-keiba --redo 03_seitai:2`（文単位）／`comfy_h3.py 01-keiba --redo 06_ochi --seed 42`（クリップ単位）
→ その後 `assemble.py` だけ再実行。

動作確認（API・ComfyUI なし）：`python tools/run_all.py 01-keiba --mock`

## 素材（任意）
無いものは警告を出してスキップします。
- `assets/ambience/racecourse_crowd.wav`, `concourse.wav` … 環境音（無ければ H3 が soundscape から生成した音を敷く。通常はこちらで十分）
- `assets/sfx/discover.wav`（発見）, `sting_low.wav`（落胆）, `timpani_roll.wav`（場面転換）, `machine.wav`, `error_beep.wav`（オチ）
- `assets/bgm/ochi.wav` … 「なんと無駄な足掻き」から最後まで流れる

## 新しいエピソードの作り方
`episodes/01-keiba/episode.json` をコピーして書き換えます。【】の構成（場所紹介 → 生き物を発見 → 生態の紹介 → 場面転換 → オチ前 → オチ）は固定です。
- `lines[].emotion` … 感情タグ。Gemini TTS への話し方の指示は `config.json` の `gemini.emotions` で調整
- `lines[].cues` … SE / BGM を入れるタイミング（その文の頭からの秒数）
- `image_prompt` / `video_prompt` / `soundscape` … Codex 用 / H3 の映像 / H3 の環境音（英語）
