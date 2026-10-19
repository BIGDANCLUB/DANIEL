#!/bin/bash
# VOICEVOX エンジン（Linux CPU 版）をダウンロード・展開して起動する。起動済みなら何もしない。
# 使い方: bash shorts/tools/voicevox_setup.sh
set -e
V=${VOICEVOX_VERSION:-0.25.2}
DIR=${VOICEVOX_DIR:-/home/user/vv}
PORT=${VOICEVOX_PORT:-50021}
if curl -s "http://127.0.0.1:$PORT/version" >/dev/null 2>&1; then echo "VOICEVOX は起動済み"; exit 0; fi
mkdir -p "$DIR"
if [ ! -x "$DIR/linux-cpu-x64/run" ] && [ -z "$(find "$DIR" -maxdepth 3 -name run -type f 2>/dev/null)" ]; then
  if [ ! -f "$DIR/engine.7z" ]; then
    echo "ダウンロード中（約1.8GB）…"
    curl -sSL --retry 3 -o "$DIR/engine.7z" \
      "https://github.com/VOICEVOX/voicevox_engine/releases/download/$V/voicevox_engine-linux-cpu-x64-$V.7z.001"
  fi
  echo "展開中…"
  python3 -m pip install -q py7zr
  python3 -c "import py7zr,sys; py7zr.SevenZipFile(sys.argv[1]).extractall(sys.argv[2])" "$DIR/engine.7z" "$DIR"
  rm -f "$DIR/engine.7z"
fi
RUN=$(find "$DIR" -maxdepth 3 -name run -type f | head -1)
chmod +x "$RUN"
echo "起動中… ($RUN)"
nohup "$RUN" --host 127.0.0.1 --port "$PORT" > "$DIR/engine.log" 2>&1 &
for i in $(seq 1 120); do
  if curl -s "http://127.0.0.1:$PORT/version" >/dev/null 2>&1; then echo "起動しました"; exit 0; fi
  sleep 2
done
echo "起動に失敗しました（$DIR/engine.log を確認）"; exit 1
