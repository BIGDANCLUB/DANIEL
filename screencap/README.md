# ScreenCap — ホットキーで画面の指定範囲を MP4 録画

## 準備（初回だけ）
1. Python 3.8 以上（python.org 版。標準ライブラリだけで動く）
2. ffmpeg: `winget install Gyan.FFmpeg`（または `ffmpeg.exe` をこのフォルダに置く）

## 使い方
`ScreenCap.bat` をダブルクリック（またはスタートアップに入れておく）。小さな操作ウィンドウが出る。

| キー | 動作 |
|---|---|
| **F9** | 録画開始 / 停止（どのアプリを使っていても効く）。範囲が未設定なら先に範囲選択 |
| **F8** | 録画範囲を選び直す |

範囲選択の画面（全モニターが暗くなる）
- ドラッグで範囲を描く／枠の中をドラッグで移動／四隅・辺の □ で大きさ変更
- 矢印キーで 1px 移動（Shift で 10px）、Ctrl+矢印で大きさ変更
- `F` でマウスのあるモニター全体
- Enter・ダブルクリック・F9 で決定（F9 ならそのまま録画開始）、Esc・右クリックでキャンセル

範囲は保存されるので、次からは F9 を押した瞬間に録画が始まる。録画中は範囲の外側に赤い枠が出る（録画には映らない）。

保存先は既定で `ビデオ\ScreenCap\screencap_YYYYMMDD_HHMMSS.mp4`（H.264 / yuv420p / faststart）。

## 設定 `%APPDATA%\ScreenCap\config.json`
操作ウィンドウの「設定ファイル」ボタンで開ける。変えたら ScreenCap を起動し直す。

- `hotkey_record` / `hotkey_select` … 例 `"F9"`, `"Ctrl+Shift+R"`, `"Alt+PrintScreen"`
- `fps`（30）, `crf`（23。小さいほど高画質）, `preset`（veryfast。重ければ ultrafast）
- `encoder` … `libx264`（既定）/ `h264_nvenc`（NVIDIA）/ `h264_qsv`（Intel）/ `h264_amf`（AMD）
- `audio_device` … 音も録るならデバイス名（`python screencap.py --list-audio` で確認）
- `output_dir`, `filename`（strftime 形式）, `draw_mouse`, `show_border`, `minimize_while_recording`, `sound`, `ffmpeg`

## 困ったとき
- 録画が始まらない → `%APPDATA%\ScreenCap\ffmpeg.log` に ffmpeg のメッセージ
- ホットキー登録失敗の警告 → 他のアプリが同じキーを使っている。config で別のキーに
- 拡大率（125%・150% など）が違うモニターが混ざっていても、範囲は物理ピクセルでそろえてあるのでずれない
