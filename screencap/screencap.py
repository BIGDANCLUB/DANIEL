"""ScreenCap — ホットキー一発で画面の指定範囲を MP4 に録画する Windows 用ツール。

  python screencap.py                 # 起動（小さな操作ウィンドウが出る）
  python screencap.py --select        # 起動してすぐ範囲選択
  python screencap.py --list-audio    # 録音に使えるマイク等のデバイス名を表示

既定のホットキー（どのアプリを使っていても効く）
  F9 … 録画開始 / 停止（範囲が未設定なら先に範囲選択）
  F8 … 録画範囲をマウスで選び直す

範囲選択の操作
  ドラッグ          … 新しく範囲を描く
  枠の中をドラッグ  … 範囲を移動
  四隅・辺の□      … ドラッグで大きさを変える
  矢印キー          … 1px 移動（Shift で 10px）／ Ctrl+矢印 で大きさを変える
  F                 … マウスがあるモニター全体を選ぶ
  Enter / ダブルクリック … 決定　　Esc / 右クリック … キャンセル

必要なもの: Python 3.8 以上（標準ライブラリだけ）と ffmpeg（gdigrab 入り。公式ビルドなら入っている）。
設定は %APPDATA%\\ScreenCap\\config.json（初回起動時に作られる。ホットキー・fps・画質・保存先など）。

座標について: このプロセスは Per-Monitor DPI Aware（v2）で動くので、Tk のウィンドウ座標・
GetSystemMetrics の仮想スクリーン座標・gdigrab の -offset_x/-offset_y はすべて物理ピクセルで一致する
（拡大率の違うモニターを並べていても範囲がずれない）。
"""
import argparse
import ctypes
import datetime as _dt
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
import traceback
from pathlib import Path

IS_WIN = sys.platform == "win32"
APP = "ScreenCap"
SCRIPT_DIR = Path(__file__).resolve().parent

if IS_WIN:
    from ctypes import wintypes

# ---------------------------------------------------------------------------
# 設定
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = {
    "hotkey_record": "F9",          # 録画開始/停止
    "hotkey_select": "F8",          # 範囲選択
    "output_dir": "",               # 空なら ~/Videos/ScreenCap
    "filename": "screencap_%Y%m%d_%H%M%S.mp4",
    "fps": 30,
    "draw_mouse": True,             # マウスカーソルも録る
    "encoder": "libx264",           # libx264 / h264_nvenc / h264_qsv / h264_amf
    "crf": 23,                      # libx264 の画質（小さいほど高画質・大きいファイル。18〜28 くらい）
    "preset": "veryfast",           # libx264 の速さ（ultrafast〜medium。重いときは ultrafast）
    "audio_device": "",             # 録音するなら dshow のデバイス名（--list-audio で確認）。空なら無音
    "show_border": True,            # 録画中、範囲の外側に赤い枠を出す（枠は録画には映らない）
    "minimize_while_recording": False,
    "sound": True,                  # 開始・停止で効果音
    "ffmpeg": "",                   # ffmpeg.exe のパス。空なら同じフォルダ → PATH の順に探す
    "region": None,                 # [x, y, w, h]（物理ピクセル・仮想スクリーン座標）。範囲選択で保存される
}


def config_dir():
    base = os.environ.get("APPDATA") if IS_WIN else os.environ.get("XDG_CONFIG_HOME")
    base = Path(base) if base else Path.home() / (".config" if not IS_WIN else "AppData/Roaming")
    return base / APP


def load_config():
    path = config_dir() / "config.json"
    cfg = dict(DEFAULT_CONFIG)
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            cfg.update({k: v for k, v in data.items() if k in DEFAULT_CONFIG})
        except (OSError, ValueError) as e:
            print(f"設定ファイルを読めませんでした（既定値で起動）: {path}: {e}", file=sys.stderr)
    return cfg


def save_config(cfg):
    path = config_dir() / "config.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def output_dir(cfg):
    d = Path(os.path.expandvars(os.path.expanduser(cfg["output_dir"]))) if cfg["output_dir"] \
        else Path.home() / "Videos" / APP
    d.mkdir(parents=True, exist_ok=True)
    return d


def find_ffmpeg(cfg):
    cands = []
    if cfg.get("ffmpeg"):
        cands.append(Path(os.path.expandvars(os.path.expanduser(cfg["ffmpeg"]))))
    exe = "ffmpeg.exe" if IS_WIN else "ffmpeg"
    cands += [SCRIPT_DIR / exe, SCRIPT_DIR / "bin" / exe]
    for c in cands:
        if c.is_file():
            return str(c)
    return shutil.which("ffmpeg")


# ---------------------------------------------------------------------------
# Win32: DPI・画面情報・グローバルホットキー
# ---------------------------------------------------------------------------

def enable_dpi_awareness():
    """Tk のウィンドウを作る前に呼ぶ。座標を物理ピクセルにそろえる。"""
    if not IS_WIN:
        return "n/a"
    try:  # Windows 10 1703+
        if ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4)):
            return "per-monitor-v2"
    except (AttributeError, OSError):
        pass
    try:  # Windows 8.1+
        if ctypes.windll.shcore.SetProcessDpiAwareness(2) == 0:
            return "per-monitor"
    except (AttributeError, OSError):
        pass
    try:
        ctypes.windll.user32.SetProcessDPIAware()
        return "system"
    except (AttributeError, OSError):
        return "unaware"


def virtual_screen():
    """全モニターを合わせた矩形 (x, y, w, h)。左や上にモニターがあると x, y は負になる。"""
    if not IS_WIN:
        return (0, 0, 1920, 1080)
    gsm = ctypes.windll.user32.GetSystemMetrics
    return (gsm(76), gsm(77), gsm(78), gsm(79))


def monitor_at(x, y):
    """点 (x, y) があるモニターの矩形 (x, y, w, h)。"""
    if not IS_WIN:
        return virtual_screen()

    class MONITORINFO(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", wintypes.RECT),
                    ("rcWork", wintypes.RECT), ("dwFlags", wintypes.DWORD)]

    user32 = ctypes.windll.user32
    user32.MonitorFromPoint.restype = wintypes.HMONITOR
    user32.MonitorFromPoint.argtypes = [wintypes.POINT, wintypes.DWORD]
    user32.GetMonitorInfoW.argtypes = [wintypes.HMONITOR, ctypes.POINTER(MONITORINFO)]
    hmon = user32.MonitorFromPoint(wintypes.POINT(int(x), int(y)), 2)  # MONITOR_DEFAULTTONEAREST
    mi = MONITORINFO()
    mi.cbSize = ctypes.sizeof(MONITORINFO)
    if not user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
        return virtual_screen()
    r = mi.rcMonitor
    return (r.left, r.top, r.right - r.left, r.bottom - r.top)


def cursor_pos():
    if not IS_WIN:
        return (0, 0)
    pt = wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return (pt.x, pt.y)


MOD_ALT, MOD_CONTROL, MOD_SHIFT, MOD_WIN, MOD_NOREPEAT = 0x1, 0x2, 0x4, 0x8, 0x4000
_MODS = {"alt": MOD_ALT, "ctrl": MOD_CONTROL, "control": MOD_CONTROL, "shift": MOD_SHIFT,
         "win": MOD_WIN, "windows": MOD_WIN}
_VK = {"space": 0x20, "pageup": 0x21, "pgup": 0x21, "pagedown": 0x22, "pgdn": 0x22, "end": 0x23,
       "home": 0x24, "left": 0x25, "up": 0x26, "right": 0x27, "down": 0x28,
       "printscreen": 0x2C, "prtsc": 0x2C, "insert": 0x2D, "ins": 0x2D, "delete": 0x2E, "del": 0x2E,
       "pause": 0x13, "scrolllock": 0x91, "tab": 0x09, "enter": 0x0D, "backspace": 0x08}
_VK.update({f"f{i}": 0x6F + i for i in range(1, 25)})
_VK.update({f"numpad{i}": 0x60 + i for i in range(10)})
_VK.update({chr(c).lower(): c for c in range(ord("A"), ord("Z") + 1)})
_VK.update({str(i): 0x30 + i for i in range(10)})


def parse_hotkey(text):
    """'Ctrl+Shift+R' → (mods, vk)。不正なら ValueError。"""
    parts = [p.strip().lower() for p in str(text).replace("-", "+").split("+") if p.strip()]
    if not parts:
        raise ValueError(f"ホットキーが空です: {text!r}")
    mods, key = 0, None
    for p in parts:
        if p in _MODS:
            mods |= _MODS[p]
        elif p in _VK and key is None:
            key = _VK[p]
        else:
            raise ValueError(f"ホットキーを解釈できません: {text!r}（{p!r}）")
    if key is None:
        raise ValueError(f"ホットキーにキーがありません（修飾キーだけ）: {text!r}")
    return mods, key


class HotkeyThread(threading.Thread):
    """RegisterHotKey は登録したスレッドのメッセージキューに WM_HOTKEY が届くので、専用スレッドで回す。"""
    WM_HOTKEY, WM_QUIT = 0x0312, 0x0012

    def __init__(self, bindings, callback):
        super().__init__(daemon=True)
        self.bindings = bindings          # {名前: "F9"}
        self.callback = callback          # callback(名前) ※このスレッドから呼ばれる
        self.failed = {}                  # {名前: 理由}
        self.ready = threading.Event()
        self._tid = None

    def run(self):
        user32, kernel32 = ctypes.windll.user32, ctypes.windll.kernel32
        user32.RegisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.UINT, wintypes.UINT]
        user32.UnregisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int]
        user32.GetMessageW.argtypes = [ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]
        self._tid = kernel32.GetCurrentThreadId()
        ids = {}
        for i, (name, text) in enumerate(self.bindings.items(), start=1):
            try:
                mods, vk = parse_hotkey(text)
            except ValueError as e:
                self.failed[name] = str(e)
                continue
            if user32.RegisterHotKey(None, i, mods | MOD_NOREPEAT, vk):
                ids[i] = name
            else:
                self.failed[name] = f"{text} は他のアプリが使っています"
        self.ready.set()
        msg = wintypes.MSG()
        try:
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
                if msg.message == self.WM_HOTKEY and msg.wParam in ids:
                    self.callback(ids[msg.wParam])
        finally:
            for i in ids:
                user32.UnregisterHotKey(None, i)

    def stop(self):
        if self._tid:
            ctypes.windll.user32.PostThreadMessageW.argtypes = [wintypes.DWORD, wintypes.UINT,
                                                                wintypes.WPARAM, wintypes.LPARAM]
            ctypes.windll.user32.PostThreadMessageW(self._tid, self.WM_QUIT, 0, 0)


def play_sound(kind):
    if not IS_WIN:
        return
    try:
        import winsound
        winsound.MessageBeep(winsound.MB_OK if kind == "start" else winsound.MB_ICONASTERISK)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# 範囲の正規化・ffmpeg
# ---------------------------------------------------------------------------

MIN_SIZE = 16


def normalize_region(region, bounds=None):
    """仮想スクリーン内に収め、幅・高さを偶数にする（yuv420p の H.264 は奇数サイズ不可）。不正なら None。"""
    if not region or len(region) != 4:
        return None
    bx, by, bw, bh = bounds or virtual_screen()
    x, y, w, h = (int(round(v)) for v in region)
    x1, y1 = max(x, bx), max(y, by)
    x2, y2 = min(x + w, bx + bw), min(y + h, by + bh)
    w, h = x2 - x1, y2 - y1
    w -= w % 2
    h -= h % 2
    if w < MIN_SIZE or h < MIN_SIZE:
        return None
    return [x1, y1, w, h]


def build_ffmpeg_cmd(ffmpeg, region, out_path, cfg, video_input=None):
    """video_input を渡すと gdigrab の代わりに使う（動作確認用）。"""
    x, y, w, h = region
    fps = str(cfg["fps"])
    cmd = [ffmpeg, "-hide_banner", "-y"]
    if video_input is None:
        cmd += ["-f", "gdigrab", "-thread_queue_size", "1024", "-framerate", fps,
                "-draw_mouse", "1" if cfg["draw_mouse"] else "0",
                "-offset_x", str(x), "-offset_y", str(y), "-video_size", f"{w}x{h}", "-i", "desktop"]
    else:
        cmd += video_input
    if cfg.get("audio_device"):
        cmd += ["-f", "dshow", "-thread_queue_size", "1024", "-i", f"audio={cfg['audio_device']}"]
    enc = cfg["encoder"]
    cmd += ["-map", "0:v:0"]
    if cfg.get("audio_device"):
        cmd += ["-map", "1:a:0", "-c:a", "aac", "-b:a", "160k"]
    cmd += ["-c:v", enc]
    if enc == "libx264":
        cmd += ["-preset", cfg["preset"], "-crf", str(cfg["crf"])]
    elif enc == "h264_nvenc":
        cmd += ["-preset", "p4", "-rc", "vbr", "-cq", str(cfg["crf"]), "-b:v", "0"]
    elif enc == "h264_qsv":
        cmd += ["-global_quality", str(cfg["crf"])]
    elif enc == "h264_amf":
        cmd += ["-rc", "cqp", "-qp_i", str(cfg["crf"]), "-qp_p", str(cfg["crf"])]
    cmd += ["-pix_fmt", "yuv420p", "-r", fps, "-movflags", "+faststart", str(out_path)]
    return cmd


class Recorder:
    def __init__(self, ffmpeg, cfg):
        self.ffmpeg, self.cfg = ffmpeg, cfg
        self.proc = None
        self.path = None
        self.started_at = None
        self._log = None
        self.log_path = config_dir() / "ffmpeg.log"

    @property
    def active(self):
        return self.proc is not None

    def start(self, region, video_input=None):
        out = output_dir(self.cfg) / _dt.datetime.now().strftime(self.cfg["filename"])
        if not out.suffix:
            out = out.with_suffix(".mp4")
        cmd = build_ffmpeg_cmd(self.ffmpeg, region, out, self.cfg, video_input)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._log = open(self.log_path, "w", encoding="utf-8", errors="replace")
        self._log.write(" ".join(f'"{c}"' if " " in c else c for c in cmd) + "\n\n")
        self._log.flush()
        flags = 0x08000000 if IS_WIN else 0  # CREATE_NO_WINDOW
        self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                                     stderr=self._log, creationflags=flags)
        self.path, self.started_at = out, time.monotonic()
        # 起動直後に落ちる（範囲外・エンコーダ無しなど）ならすぐ分かるように少し待つ
        try:
            self.proc.wait(timeout=0.6)
        except subprocess.TimeoutExpired:
            return out
        err = self._finish()
        raise RuntimeError("ffmpeg がすぐに終了しました。\n\n" + err)

    def stop(self):
        """'q' を送ってきれいに終わらせる（moov が書かれて再生できる mp4 になる）。"""
        if not self.proc:
            return None
        try:
            self.proc.stdin.write(b"q")
            self.proc.stdin.flush()
            self.proc.stdin.close()
        except OSError:
            pass
        try:
            self.proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        path = self.path
        self._finish()
        return path

    def died(self):
        """録画中に ffmpeg が勝手に終わったら、そのログ末尾を返す。"""
        if self.proc and self.proc.poll() is not None:
            return self._finish()
        return None

    def elapsed(self):
        return time.monotonic() - self.started_at if self.started_at else 0.0

    def _finish(self):
        code = self.proc.returncode if self.proc else None
        self.proc = None
        self.started_at = None
        if self._log:
            self._log.close()
            self._log = None
        try:
            tail = self.log_path.read_text(encoding="utf-8", errors="replace").strip().splitlines()[-12:]
        except OSError:
            tail = []
        return f"(終了コード {code})\n" + "\n".join(tail)


# ---------------------------------------------------------------------------
# 範囲選択オーバーレイ
# ---------------------------------------------------------------------------

class RegionSelector:
    HANDLE = 6   # □ の半径（px）
    COLOR = "#ff3b30"

    def __init__(self, root, initial, on_done):
        import tkinter as tk
        self.tk = tk
        self.root, self.on_done = root, on_done
        self.vx, self.vy, self.vw, self.vh = virtual_screen()
        self.win = tk.Toplevel(root)
        self.win.overrideredirect(True)
        self.win.geometry(f"{self.vw}x{self.vh}+{self.vx}+{self.vy}")
        self.win.attributes("-topmost", True)
        try:
            self.win.attributes("-alpha", 0.45)
        except tk.TclError:
            pass
        self.cv = tk.Canvas(self.win, bg="black", highlightthickness=0, cursor="crosshair")
        self.cv.pack(fill="both", expand=True)

        self.rect = None   # canvas 座標 [x1, y1, x2, y2]
        if initial:
            x, y, w, h = initial
            self.rect = [x - self.vx, y - self.vy, x - self.vx + w, y - self.vy + h]
        self.mode = None
        self.anchor = None
        self.orig = None

        cv = self.cv
        cv.bind("<ButtonPress-1>", self._press)
        cv.bind("<B1-Motion>", self._drag)
        cv.bind("<ButtonRelease-1>", self._release)
        cv.bind("<Double-Button-1>", lambda e: self._confirm())
        cv.bind("<Motion>", self._hover)
        cv.bind("<ButtonPress-3>", lambda e: self._cancel())
        w = self.win
        w.bind("<Return>", lambda e: self._confirm())
        w.bind("<KP_Enter>", lambda e: self._confirm())
        w.bind("<Escape>", lambda e: self._cancel())
        w.bind("<Key-f>", lambda e: self._full_monitor())
        w.bind("<Key-F>", lambda e: self._full_monitor())
        for key, d in (("Left", (-1, 0)), ("Right", (1, 0)), ("Up", (0, -1)), ("Down", (0, 1))):
            w.bind(f"<{key}>", lambda e, d=d: self._nudge(d, 1, False))
            w.bind(f"<Shift-{key}>", lambda e, d=d: self._nudge(d, 10, False))
            w.bind(f"<Control-{key}>", lambda e, d=d: self._nudge(d, 1, True))
            w.bind(f"<Control-Shift-{key}>", lambda e, d=d: self._nudge(d, 10, True))

        # 拡大率の違うモニターをまたぐと Windows が大きさを変えてくることがあるので、少し後に念押し
        self.win.after(150, lambda: self.win.geometry(f"{self.vw}x{self.vh}+{self.vx}+{self.vy}"))
        self.win.after(10, self._grab_focus)
        self._redraw()

    # -- 座標 --
    def _origin(self):
        """canvas の (0,0) が画面上のどこか。geometry どおりのはずだが実測を優先する。"""
        try:
            return self.cv.winfo_rootx(), self.cv.winfo_rooty()
        except self.tk.TclError:
            return self.vx, self.vy

    def _norm(self):
        x1, y1, x2, y2 = self.rect
        return [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]

    def _handles(self):
        x1, y1, x2, y2 = self._norm()
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        return {"nw": (x1, y1), "n": (mx, y1), "ne": (x2, y1), "e": (x2, my),
                "se": (x2, y2), "s": (mx, y2), "sw": (x1, y2), "w": (x1, my)}

    def _hit(self, x, y):
        if not self.rect:
            return None
        r = self.HANDLE + 3
        for name, (hx, hy) in self._handles().items():
            if abs(x - hx) <= r and abs(y - hy) <= r:
                return name
        x1, y1, x2, y2 = self._norm()
        if x1 < x < x2 and y1 < y < y2:
            return "move"
        return None

    # -- マウス --
    _CURSORS = {"nw": "size_nw_se", "se": "size_nw_se", "ne": "size_ne_sw", "sw": "size_ne_sw",
                "n": "sb_v_double_arrow", "s": "sb_v_double_arrow",
                "e": "sb_h_double_arrow", "w": "sb_h_double_arrow", "move": "fleur", None: "crosshair"}

    def _hover(self, e):
        try:
            self.cv.configure(cursor=self._CURSORS[self._hit(e.x, e.y)])
        except self.tk.TclError:
            self.cv.configure(cursor="crosshair")

    def _press(self, e):
        hit = self._hit(e.x, e.y)
        if hit is None:
            self.mode = "new"
            self.rect = [e.x, e.y, e.x, e.y]
        else:
            self.mode = hit
            self.rect = self._norm()
        self.anchor = (e.x, e.y)
        self.orig = list(self.rect)
        self._redraw()

    def _drag(self, e):
        if not self.mode:
            return
        x = min(max(e.x, 0), self.vw)
        y = min(max(e.y, 0), self.vh)
        dx, dy = x - self.anchor[0], y - self.anchor[1]
        x1, y1, x2, y2 = self.orig
        if self.mode == "new":
            self.rect = [x1, y1, x, y]
        elif self.mode == "move":
            dx = min(max(dx, -x1), self.vw - x2)
            dy = min(max(dy, -y1), self.vh - y2)
            self.rect = [x1 + dx, y1 + dy, x2 + dx, y2 + dy]
        else:
            if "w" in self.mode:
                x1 += dx
            if "e" in self.mode:
                x2 += dx
            if "n" in self.mode:
                y1 += dy
            if "s" in self.mode:
                y2 += dy
            self.rect = [x1, y1, x2, y2]
        self._redraw()

    def _release(self, e):
        if self.rect:
            self.rect = self._norm()
            x1, y1, x2, y2 = self.rect
            if x2 - x1 < 4 and y2 - y1 < 4:   # ただのクリックは範囲にしない
                self.rect = None if self.mode == "new" else self.orig
        self.mode = None
        self._redraw()

    # -- キーボード --
    def _nudge(self, d, step, resize):
        if not self.rect:
            return
        x1, y1, x2, y2 = self._norm()
        dx, dy = d[0] * step, d[1] * step
        if resize:
            x2 = max(x1 + MIN_SIZE, min(self.vw, x2 + dx))
            y2 = max(y1 + MIN_SIZE, min(self.vh, y2 + dy))
        else:
            dx = min(max(dx, -x1), self.vw - x2)
            dy = min(max(dy, -y1), self.vh - y2)
            x1, x2, y1, y2 = x1 + dx, x2 + dx, y1 + dy, y2 + dy
        self.rect = [x1, y1, x2, y2]
        self._redraw()

    def _full_monitor(self):
        ox, oy = self._origin()
        mx, my, mw, mh = monitor_at(*cursor_pos())
        self.rect = [mx - ox, my - oy, mx - ox + mw, my - oy + mh]
        self._redraw()

    # -- 描画 --
    def _redraw(self):
        cv = self.cv
        cv.delete("all")
        ox, oy = self._origin()
        # 操作説明はマウスのあるモニターの上部中央に
        mx, my, mw, _ = monitor_at(*cursor_pos())
        tx, ty = mx - ox + mw / 2, my - oy + 40
        help_text = ("ドラッグで範囲を選択　│　枠内ドラッグ＝移動　□＝大きさ変更　矢印キー＝微調整（Ctrl で大きさ）"
                     "\nF＝モニター全体　│　Enter / ダブルクリック＝決定　│　Esc / 右クリック＝キャンセル")
        cv.create_rectangle(tx - 430, ty - 26, tx + 430, ty + 26, fill="#202020", outline="")
        cv.create_text(tx, ty, text=help_text, fill="white", font=("Yu Gothic UI", 11), justify="center")
        if not self.rect:
            return
        x1, y1, x2, y2 = self._norm()
        cv.create_rectangle(x1, y1, x2, y2, fill="#7a7a7a", outline="")
        cv.create_rectangle(x1, y1, x2, y2, outline=self.COLOR, width=2)
        h = self.HANDLE
        for hx, hy in self._handles().values():
            cv.create_rectangle(hx - h, hy - h, hx + h, hy + h, fill="white", outline=self.COLOR, width=2)
        reg = self._region()
        label = f"{reg[2]} × {reg[3]}   ({reg[0]}, {reg[1]})" if reg else "小さすぎます"
        ly = y1 - 16 if y1 > 30 else y2 + 16
        cv.create_rectangle(x1, ly - 12, x1 + 9 * len(label) + 16, ly + 12, fill=self.COLOR, outline="")
        cv.create_text(x1 + 8, ly, text=label, fill="white", anchor="w", font=("Consolas", 11, "bold"))

    def _region(self):
        if not self.rect:
            return None
        ox, oy = self._origin()
        x1, y1, x2, y2 = self._norm()
        return normalize_region([x1 + ox, y1 + oy, x2 - x1, y2 - y1])

    def _grab_focus(self):
        try:
            self.win.lift()
            self.win.focus_force()
            self.cv.focus_set()
        except self.tk.TclError:
            pass

    # -- 終了 --
    def _confirm(self):
        reg = self._region()
        if not reg:
            return
        self._close(reg)

    def _cancel(self):
        self._close(None)

    def _close(self, result):
        try:
            self.win.destroy()
        except self.tk.TclError:
            pass
        self.on_done(result)


# ---------------------------------------------------------------------------
# 録画中の枠（範囲の外側に 4 本の細いウィンドウ。範囲の中には入らないので録画に映らない）
# ---------------------------------------------------------------------------

class Border:
    def __init__(self, root, region, color="#ff3b30", thick=3, gap=1):
        import tkinter as tk
        x, y, w, h = region
        t, g = thick, gap
        rects = [(x - t - g, y - t - g, w + 2 * (t + g), t),   # 上
                 (x - t - g, y + h + g, w + 2 * (t + g), t),   # 下
                 (x - t - g, y - g, t, h + 2 * g),             # 左
                 (x + w + g, y - g, t, h + 2 * g)]             # 右
        self.wins = []
        for rx, ry, rw, rh in rects:
            win = tk.Toplevel(root)
            win.overrideredirect(True)
            win.attributes("-topmost", True)
            win.configure(bg=color)
            win.geometry(f"{rw}x{rh}+{rx}+{ry}")
            self.wins.append(win)

    def destroy(self):
        for w in self.wins:
            try:
                w.destroy()
            except Exception:
                pass
        self.wins = []


# ---------------------------------------------------------------------------
# 操作ウィンドウ
# ---------------------------------------------------------------------------

class App:
    def __init__(self, cfg, ffmpeg, dpi_mode, select_on_start=False):
        import tkinter as tk
        from tkinter import messagebox
        self.tk, self.messagebox = tk, messagebox
        self.cfg, self.ffmpeg = cfg, ffmpeg
        self.region = normalize_region(cfg.get("region"))
        self.recorder = Recorder(ffmpeg, cfg)
        self.selector = None
        self.border = None
        self.events = queue.Queue()
        self.last_file = None
        self.video_input = None   # テスト用（gdigrab の代わり）

        root = self.root = tk.Tk()
        root.title(APP)
        root.resizable(False, False)
        root.report_callback_exception = self._on_tk_error
        root.protocol("WM_DELETE_WINDOW", self.quit)

        pad = {"padx": 10, "pady": 3}
        self.status = tk.StringVar(value="待機中")
        self.region_text = tk.StringVar()
        self.file_text = tk.StringVar(value="")
        self.status_lbl = tk.Label(root, textvariable=self.status, font=("Yu Gothic UI", 14, "bold"), anchor="w")
        self.status_lbl.pack(fill="x", **pad)
        tk.Label(root, textvariable=self.region_text, anchor="w", font=("Yu Gothic UI", 10)).pack(fill="x", **pad)
        self.hotkey_lbl = tk.Label(root, anchor="w", justify="left", fg="#555", font=("Yu Gothic UI", 9))
        self.hotkey_lbl.pack(fill="x", **pad)

        row = tk.Frame(root)
        row.pack(fill="x", padx=10, pady=(6, 3))
        self.btn_rec = tk.Button(row, text="● 録画開始", width=12, command=self.toggle_record)
        self.btn_rec.pack(side="left")
        self.btn_sel = tk.Button(row, text="範囲を選択", width=12, command=self.select_region)
        self.btn_sel.pack(side="left", padx=6)
        tk.Button(row, text="保存先を開く", width=12, command=self.open_folder).pack(side="left")

        row2 = tk.Frame(root)
        row2.pack(fill="x", padx=10, pady=(0, 8))
        tk.Label(row2, textvariable=self.file_text, anchor="w", fg="#555", font=("Yu Gothic UI", 9)).pack(side="left")
        self.btn_play = tk.Button(row2, text="再生", command=self.play_last, state="disabled")
        self.btn_play.pack(side="right")
        tk.Button(row2, text="設定ファイル", command=self.open_config).pack(side="right", padx=6)

        self._update_region_text()
        self.hotkeys = None
        if IS_WIN:
            self.hotkeys = HotkeyThread({"record": cfg["hotkey_record"], "select": cfg["hotkey_select"]},
                                        self.events.put)
            self.hotkeys.start()
            self.hotkeys.ready.wait(2)
        self._update_hotkey_text()
        if self.hotkeys and self.hotkeys.failed:
            messagebox.showwarning(APP, "ホットキーを登録できませんでした:\n\n" +
                                   "\n".join(self.hotkeys.failed.values()) +
                                   f"\n\n{config_dir() / 'config.json'} で別のキーにしてください。"
                                   "\n（ボタンからは操作できます）")
        if dpi_mode not in ("per-monitor-v2", "per-monitor", "n/a"):
            print(f"注意: DPI 設定が {dpi_mode} です。拡大率の違うモニターでは範囲がずれることがあります。",
                  file=sys.stderr)
        root.after(50, self._poll)
        if select_on_start:
            root.after(200, self.select_region)

    # -- 表示 --
    def _update_region_text(self):
        if self.region:
            x, y, w, h = self.region
            self.region_text.set(f"範囲: {w} × {h}  位置 ({x}, {y})")
        else:
            self.region_text.set("範囲: 未設定（録画開始で選択します）")

    def _update_hotkey_text(self):
        def show(name, key):
            if self.hotkeys and name in self.hotkeys.failed:
                return f"{key}（登録失敗）"
            return key if IS_WIN else f"{key}（Windows のみ）"
        self.hotkey_lbl.configure(text=f"{show('record', self.cfg['hotkey_record'])} … 録画開始 / 停止　　"
                                       f"{show('select', self.cfg['hotkey_select'])} … 範囲選択")

    def _set_recording_ui(self, on):
        if on:
            self.btn_rec.configure(text="■ 録画停止")
            self.btn_sel.configure(state="disabled")
            self.status_lbl.configure(fg="#d70015")
            self.root.title(f"● REC - {APP}")
        else:
            self.btn_rec.configure(text="● 録画開始")
            self.btn_sel.configure(state="normal")
            self.status_lbl.configure(fg="black")
            self.status.set("待機中")
            self.root.title(APP)

    # -- 操作 --
    def toggle_record(self):
        if self.recorder.active:
            self.stop_record()
        else:
            self.start_record()

    def start_record(self):
        if self.recorder.active or self.selector:
            return
        if not self.region:
            self.select_region(then_record=True)
            return
        region = normalize_region(self.region)   # モニター構成が変わっていてもはみ出さないように
        if not region:
            self.region = None
            self._update_region_text()
            self.select_region(then_record=True)
            return
        try:
            self.recorder.start(region, self.video_input)
        except Exception as e:
            self.messagebox.showerror(APP, f"録画を開始できませんでした。\n\n{e}\n\nログ: {self.recorder.log_path}")
            return
        if self.cfg["sound"]:
            play_sound("start")
        if self.cfg["show_border"]:
            self.border = Border(self.root, region)
        if self.cfg["minimize_while_recording"]:
            self.root.iconify()
        self._set_recording_ui(True)

    def stop_record(self):
        if not self.recorder.active:
            return
        self.status.set("保存中…")
        self.root.update_idletasks()
        if self.border:
            self.border.destroy()
            self.border = None
        path = self.recorder.stop()
        self._set_recording_ui(False)
        if self.cfg["sound"]:
            play_sound("stop")
        if path and path.exists() and path.stat().st_size > 0:
            self.last_file = path
            self.file_text.set(f"保存: {path.name}")
            self.btn_play.configure(state="normal")
        else:
            self.messagebox.showerror(APP, f"ファイルが作られませんでした。\nログ: {self.recorder.log_path}")
        if self.cfg["minimize_while_recording"]:
            self.root.deiconify()

    def select_region(self, then_record=False):
        if self.recorder.active or self.selector:
            return

        def done(region):
            self.selector = None
            if region:
                self.region = region
                self.cfg["region"] = region
                try:
                    save_config(self.cfg)
                except OSError as e:
                    print(f"設定を保存できませんでした: {e}", file=sys.stderr)
                self._update_region_text()
                if then_record:
                    # オーバーレイが消えきってから録り始める（暗い画面が 1 コマ目に入らないように）
                    self.root.after(150, self.start_record)
        self.selector = RegionSelector(self.root, self.region, done)

    def open_folder(self):
        self._open(output_dir(self.cfg))

    def open_config(self):
        path = config_dir() / "config.json"
        if not path.exists():
            save_config(self.cfg)
        self._open(path)

    def play_last(self):
        if self.last_file and self.last_file.exists():
            self._open(self.last_file)

    def _open(self, path):
        try:
            if IS_WIN:
                os.startfile(str(path))
            else:
                subprocess.Popen(["xdg-open", str(path)])
        except OSError as e:
            self.messagebox.showerror(APP, f"開けませんでした: {path}\n{e}")

    # -- ループ --
    def _poll(self):
        try:
            while True:
                name = self.events.get_nowait()
                if name == "record":
                    if self.selector:
                        self.selector._confirm()   # 選択中に録画キー → その範囲で決定して録画
                        if not self.selector and self.region:
                            self.root.after(150, self.start_record)
                    else:
                        self.toggle_record()
                elif name == "select":
                    self.select_region()
        except queue.Empty:
            pass
        if self.recorder.active:
            err = self.recorder.died()
            if err is not None:
                if self.border:
                    self.border.destroy()
                    self.border = None
                self._set_recording_ui(False)
                self.messagebox.showerror(APP, "録画が途中で止まりました。\n\n" + err)
            else:
                s = int(self.recorder.elapsed())
                self.status.set(f"● 録画中  {s // 3600:d}:{s // 60 % 60:02d}:{s % 60:02d}")
        self.root.after(50, self._poll)

    def _on_tk_error(self, exc, val, tb):
        text = "".join(traceback.format_exception(exc, val, tb))
        _write_crash(text)
        self.messagebox.showerror(APP, f"エラーが起きました:\n\n{val}\n\n詳細: {config_dir() / 'error.log'}")

    def quit(self):
        if self.recorder.active:
            self.stop_record()
        if self.hotkeys:
            self.hotkeys.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def _write_crash(text):
    try:
        config_dir().mkdir(parents=True, exist_ok=True)
        with open(config_dir() / "error.log", "a", encoding="utf-8") as f:
            f.write(f"--- {_dt.datetime.now().isoformat(timespec='seconds')}\n{text}\n")
    except OSError:
        pass
    print(text, file=sys.stderr)


def list_audio_devices(ffmpeg):
    r = subprocess.run([ffmpeg, "-hide_banner", "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    names = [line.split('"')[1] for line in r.stderr.splitlines() if "(audio)" in line and '"' in line]
    if not names:
        print(r.stderr)
        return
    print("録音デバイス（config.json の audio_device にそのまま書く）:")
    for n in names:
        print(f"  {n}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="ホットキーで画面の指定範囲を MP4 に録画する")
    ap.add_argument("--select", action="store_true", help="起動してすぐ範囲選択")
    ap.add_argument("--record", action="store_true", help="起動してすぐ録画（範囲が未設定なら先に選択）")
    ap.add_argument("--fps", type=int, help="フレームレート（設定ファイルより優先）")
    ap.add_argument("--out", help="保存先フォルダ（設定ファイルより優先）")
    ap.add_argument("--list-audio", action="store_true", help="録音デバイス名を表示して終了")
    args = ap.parse_args(argv)

    cfg = load_config()
    if not (config_dir() / "config.json").exists():
        try:
            save_config(cfg)
        except OSError:
            pass
    if args.fps:
        cfg["fps"] = args.fps
    if args.out:
        cfg["output_dir"] = args.out

    ffmpeg = find_ffmpeg(cfg)
    if args.list_audio:
        if not ffmpeg:
            sys.exit("ffmpeg が見つかりません")
        list_audio_devices(ffmpeg)
        return

    dpi_mode = enable_dpi_awareness()   # ← Tk を作る前に
    if not ffmpeg:
        import tkinter as tk
        from tkinter import messagebox
        r = tk.Tk()
        r.withdraw()
        messagebox.showerror(APP, "ffmpeg が見つかりません。\n\n"
                                  "・winget install Gyan.FFmpeg でインストールする\n"
                                  "・または ffmpeg.exe を screencap.py と同じフォルダに置く\n"
                                  f"・または {config_dir() / 'config.json'} の \"ffmpeg\" にパスを書く")
        sys.exit(1)
    if not IS_WIN:
        print("注意: 録画（gdigrab）とホットキーは Windows 専用です。", file=sys.stderr)

    app = App(cfg, ffmpeg, dpi_mode, select_on_start=args.select)
    if args.record:
        app.root.after(300, app.start_record)
    app.run()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        _write_crash(traceback.format_exc())
        raise
