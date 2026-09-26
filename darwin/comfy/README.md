# ComfyUI（MiniMax H3 i2v）の接続設定

`tools/comfy_h3.py` は、あなたが普段使っている H3 の i2v ワークフロー（水無瀬で使っているもの）を
そのまま使い、**画像・プロンプト・秒数・シード**の4か所だけを書き換えて ComfyUI に投げます。

## 1. ワークフローを API 形式で保存
1. ComfyUI で H3 の i2v ワークフローを開き、1回手動で生成が通ることを確認する
2. メニュー → Workflow → **Export (API)**（旧UIなら設定で Dev mode を有効にして「Save (API Format)」）
3. 保存した JSON を `darwin/comfy/h3_i2v_api.json` に置く

動画の保存ノード（`VHS_VideoCombine` / `SaveVideo` など）が mp4 を出力するようにしておいてください。

## 2. ノード ID を config.json に書く
`config.example.json` を `config.json` にコピーし、`comfy.nodes` の `REPLACE_ME` を埋めます。
API 形式 JSON のキー（`"12": {"class_type": "LoadImage", ...}` の `"12"`）がノード ID です。

| キー | 対象ノード | input 名の例 |
|---|---|---|
| image | LoadImage | `image` |
| prompt | 正プロンプトのテキストノード | `text` |
| negative | 負プロンプト（無ければ `"node": ""` で省略可） | `text` |
| duration | 尺を決めるノード | `length`（フレーム数）/ `duration`（秒） |
| seed | サンプラー等 | `seed` / `noise_seed` |

- 尺がフレーム数なら `"unit": "frames"`。H3 の有効な長さ `(length-5) % 17 == 0` のうち、秒×24 を覆う最小値を自動で選びます（8秒→192）。
- 尺が秒指定なら `"unit": "seconds"`。
- 縦長にするため `comfy.width`/`comfy.height`（既定 736×1280）を解像度ノードに流す場合は `nodes.width` / `nodes.height` を設定。
- ComfyUI の URL は環境変数 `DARWIN_COMFY_URL`（または `UGOIRA_COMFY_URL`）で渡します。

ノード ID の一覧はこれで確認できます：
```
python -c "import json;[print(k,v['class_type'],list(v['inputs'])) for k,v in json.load(open('comfy/h3_i2v_api.json',encoding='utf-8')).items()]"
```
