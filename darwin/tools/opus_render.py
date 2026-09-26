"""図解・画面（source: opus）と、H3 映像に重ねる文字（overlay）を HTML から mp4 / 透過 mov に書き出す。

  python tools/opus_render.py vs01-kangaroo-ostrich              # 全部（作成済みはスキップ）
  python tools/opus_render.py vs01-kangaroo-ostrich --only o2 r1  # 指定だけ（作り直し）
  python tools/opus_render.py vs01-kangaroo-ostrich --still r1:6  # r1 の 6秒時点を PNG で確認（out/stills/）

episodes/<ep>/graphics/index.html?scene=<ID>&dur=<秒>&overlay=0|1 を Chrome（ヘッドレス）で開き、
window.renderAt(t) で時刻を進めながら 1 コマずつ撮る。追加インストール不要（Chrome と Python 標準ライブラリのみ）。
  source opus   → out/clips/<ID>.mp4
  overlay あり  → out/overlays/<ID>.mov（背景透過。assemble.py が H3 映像の上に重ねる）
"""
import argparse
import base64
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from common import ffmpeg_exe, load_config, load_episode, out_dir

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


class WebSocket:
    """CDP 用の最小限の WebSocket クライアント（テキストフレームのみ）。"""

    def __init__(self, url):
        rest = url.split("://", 1)[1]
        hostport, path = rest.split("/", 1)
        host, port = hostport.split(":")
        self.sock = socket.create_connection((host, int(port)))
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall((f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\n"
                           f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n").encode())
        head = b""
        while b"\r\n\r\n" not in head:
            head += self.sock.recv(1)
        if b" 101 " not in head.split(b"\r\n")[0]:
            raise RuntimeError(f"WebSocket 接続失敗: {head[:200]!r}")

    def _read(self, n):
        buf = bytearray(n)
        view = memoryview(buf)
        got = 0
        while got < n:
            k = self.sock.recv_into(view[got:], n - got)
            if not k:
                raise RuntimeError("WebSocket が切断されました")
            got += k
        return bytes(buf)

    def send(self, text):
        data = text.encode()
        n = len(data)
        head = bytes([0x81])
        if n < 126:
            head += bytes([0x80 | n])
        elif n < 65536:
            head += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            head += bytes([0x80 | 127]) + struct.pack(">Q", n)
        mask = os.urandom(4)
        m = int.from_bytes((mask * (n // 4 + 1))[:n], "big") if n else 0
        body = (int.from_bytes(data, "big") ^ m).to_bytes(n, "big") if n else b""
        self.sock.sendall(head + mask + body)

    def recv(self):
        parts = []
        while True:
            b0, b1 = self._read(2)
            n = b1 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._read(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._read(8))[0]
            payload = self._read(n)
            op = b0 & 0x0F
            if op == 9:  # ping
                self.sock.sendall(bytes([0x8A, 0x80]) + os.urandom(4))
                continue
            if op in (0, 1):
                parts.append(payload)
                if b0 & 0x80:
                    return b"".join(parts).decode()
            if op == 8:
                raise RuntimeError("WebSocket が閉じられました")


class Chrome:
    def __init__(self, width, height):
        exe = next((p for p in CHROME_PATHS if Path(p).exists()), None) or shutil.which("chrome")
        if not exe:
            sys.exit("Chrome / Edge が見つかりません。")
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        s.close()
        self.profile = tempfile.mkdtemp(prefix="opus_render_")
        self.proc = subprocess.Popen([exe, "--headless=new", f"--remote-debugging-port={port}",
                                      f"--user-data-dir={self.profile}", "--no-first-run", "--no-default-browser-check",
                                      "--hide-scrollbars", "--mute-audio", "--force-device-scale-factor=1",
                                      "--allow-file-access-from-files", f"--window-size={width},{height}", "about:blank"],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                pages = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=2))
                page = next(p for p in pages if p["type"] == "page")
                break
            except Exception:
                time.sleep(0.2)
        else:
            sys.exit("Chrome のデバッグ接続に失敗しました。")
        self.ws = WebSocket(page["webSocketDebuggerUrl"])
        self.next_id = 0
        self.call("Page.enable")
        self.call("Emulation.setDeviceMetricsOverride", width=width, height=height, deviceScaleFactor=1, mobile=False)

    def call(self, method, **params):
        self.next_id += 1
        self.ws.send(json.dumps({"id": self.next_id, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.next_id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def eval(self, expr):
        r = self.call("Runtime.evaluate", expression=expr, awaitPromise=True, returnByValue=True)
        if "exceptionDetails" in r:
            raise RuntimeError(f"JS エラー: {r['exceptionDetails'].get('exception', {}).get('description', r)}")
        return r.get("result", {}).get("value")

    def open(self, url, transparent):
        if transparent:
            self.call("Emulation.setDefaultBackgroundColorOverride", color={"r": 0, "g": 0, "b": 0, "a": 0})
        else:
            self.call("Emulation.setDefaultBackgroundColorOverride")
        self.call("Page.navigate", url=url)
        for _ in range(300):
            time.sleep(0.1)
            try:
                state = self.eval("[window.__ready === true, window.__error || null]")
            except RuntimeError:
                continue  # 読み込み中で実行コンテキストがまだ無い
            if state and state[1]:
                raise RuntimeError(f"図解ページのエラー: {state[1]}")
            if state and state[0]:
                return
        raise RuntimeError(f"ページの準備が終わりません: {url}")

    def shot(self, t, fmt):
        self.eval(f"window.renderAt({t:.5f})")
        opts = {"format": fmt, "optimizeForSpeed": True}
        if fmt == "jpeg":
            opts["quality"] = 95
        return base64.b64decode(self.call("Page.captureScreenshot", **opts)["data"])

    def close(self):
        try:
            self.call("Browser.close")
        except Exception:
            pass
        self.proc.wait(timeout=10)
        shutil.rmtree(self.profile, ignore_errors=True)


def render(chrome, url, dur, fps, dest, overlay):
    chrome.open(url, overlay)
    fmt = "png" if overlay else "jpeg"
    if overlay:
        enc = ["-c:v", "png", "-pix_fmt", "rgba"]
    else:
        enc = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p"]
    tmp = dest.with_name(dest.stem + ".tmp" + dest.suffix)
    ff = subprocess.Popen([ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", "-f", "image2pipe",
                           "-framerate", str(fps), "-c:v", "png" if overlay else "mjpeg", "-i", "-", *enc, str(tmp)],
                          stdin=subprocess.PIPE)
    n = int(round(dur * fps))
    t0 = time.time()
    for i in range(n):
        ff.stdin.write(chrome.shot(i / fps, fmt))
        if i % (fps * 2) == 0:
            print(f"\r    {i / fps:5.1f}/{dur:g}秒", end="", flush=True)
    ff.stdin.close()
    if ff.wait() != 0:
        sys.exit(f"ffmpeg の書き出しに失敗しました: {dest}")
    tmp.replace(dest)
    print(f"\r    ✓ {dest.name}（{n}コマ・{time.time() - t0:.0f}秒）")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--only", nargs="*", default=[])
    ap.add_argument("--still", nargs="*", default=[], help="ID:秒 の形で静止画だけ書き出す（確認用）")
    args = ap.parse_args()

    ep_dir, ep = load_episode(args.episode)
    r = {**load_config()["render"], **ep.get("format", {}).get("render", {})}
    W, H, FPS = r["width"], r["height"], r["fps"]
    page = Path(ep_dir, "graphics", "index.html")
    if not page.exists():
        sys.exit(f"図解の HTML がありません: {page}")
    base = page.resolve().as_uri()
    by_id = {s["id"]: s for s in ep["sections"]}

    jobs = []  # (ID, 透過か, 出力先)
    for s in ep["sections"]:
        if s.get("source") == "opus":
            jobs.append((s["id"], False, out_dir(ep_dir, "clips") / f"{s['id']}.mp4"))
        elif s.get("overlay"):
            jobs.append((s["id"], True, out_dir(ep_dir, "overlays") / f"{s['id']}.mov"))

    chrome = Chrome(W, H)
    try:
        if args.still:
            dest_dir = out_dir(ep_dir, "stills")
            for spec in args.still:
                sid, _, t = spec.partition(":")
                overlay = by_id[sid].get("source") != "opus"
                chrome.open(f"{base}?scene={sid}&dur={by_id[sid]['duration']}&overlay={int(overlay)}", overlay)
                dest = dest_dir / f"{sid}_{float(t or 0):05.2f}.png"
                dest.write_bytes(chrome.shot(float(t or 0), "png"))
                print(dest)
            return
        for sid, overlay, dest in jobs:
            if args.only and sid not in args.only:
                continue
            if dest.exists() and not args.only:
                print(f"  skip {sid}（作成済み。作り直すなら --only {sid}）")
                continue
            dur = by_id[sid]["duration"]
            print(f"  {sid}（{'重ね' if overlay else '図解'} {dur}秒）{by_id[sid]['label']}")
            render(chrome, f"{base}?scene={sid}&dur={dur}&overlay={int(overlay)}", dur, FPS, dest, overlay)
    finally:
        chrome.close()


if __name__ == "__main__":
    main()
