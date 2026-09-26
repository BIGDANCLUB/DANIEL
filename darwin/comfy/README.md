# 映像生成（MiniMax H3）の仕組み

`tools/comfy_h3.py` は、水無瀬（ugoira）の **`h3.py` をそのまま読み込んで** `h3.render()` を呼びます。
ワークフロー、トンネル越しのアップロード（524 のときの縮小再送）、映像と音声の別取り、
真っ黒検知、DNS の回避策などは、すべて ugoira 側の実装が使われます。ugoira を直せば darwin にも効きます。

## 必要なもの
- ugoira フォルダ（既定：`C:\Users\genji\OneDrive\デスクトップ\ugoira`）
  - 場所が違う場合は `config.json` の `comfy.ugoira_dir`、または環境変数 `UGOIRA_DIR`
- Colab で `colab_h3_drive.ipynb` の「起動」セルを実行し、出た URL を
  `$env:UGOIRA_COMFY_URL = "https://....trycloudflare.com"`

## darwin 向けに変えている点（h3.render に渡す引数）
| 引数 | 値 | 理由 |
|---|---|---|
| width × height | 768 × 1344 | 縦 9:16（h3.py の V_W / V_H と同じ） |
| length | ナレーションを覆う最小の有効フレーム数（`(n-5)%17==0`、上限 15.2 秒 = 362） | 尺はナレーションで決まる |
| soundscape | episode.json の各【】の `soundscape` | H3 が作る環境音。結合時に薄く敷く |
| music | `N/A` | BGM は結合時にオチだけ入れる |
| chest / expressive | False | ugoira のキャラクター向け常設指示なので使わない |
| add_style | False | 定型文（Subtle motion / 構図固定）を付けず、プロンプトで書き切る |
| upscale | False | 1080×1920 への拡大は assemble.py が行う |
| lora / steps | `config.json` の `comfy.lora`（既定 lightx2v）/ `comfy.steps`（null＝プリセット既定） | 水無瀬と同じ |

H3 には negative プロンプトがありません（h3.py の冒頭の注記どおり）。
