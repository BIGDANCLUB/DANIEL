"""共通ユーティリティ（設定読み込み・ffmpeg・音声/動画の長さ計測）。標準ライブラリのみ。"""
import json
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA_EXTS = (".wav", ".mp3", ".m4a", ".ogg", ".flac")


def load_json(path):
    # メモ帳で保存すると先頭に BOM が付くことがあるので utf-8-sig で読む
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _merge(base, over):
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _merge(base[k], v)
        else:
            base[k] = v
    return base


def load_config():
    """config.example.json をベースに、config.json（ローカル専用・git管理外）で上書きする。"""
    cfg = load_json(ROOT / "config.example.json")
    local = ROOT / "config.json"
    if local.exists():
        text = local.read_text(encoding="utf-8-sig").strip()
        if not text:
            print("※ config.json が空なので無視します（不要なら削除してください）")
            return cfg
        try:
            _merge(cfg, json.loads(text))
        except json.JSONDecodeError as e:
            sys.exit(f"config.json の書き方が正しくありません（{e.lineno}行目 {e.colno}文字目）: {e.msg}\n"
                     "  直すか、いったん削除してください:  Remove-Item config.json")
    return cfg


def load_episode(ep):
    ep_dir = Path(ep)
    if not ep_dir.is_absolute() and not ep_dir.exists():
        ep_dir = ROOT / "episodes" / ep
    ep_dir = ep_dir.resolve()
    return ep_dir, load_json(ep_dir / "episode.json")


def out_dir(ep_dir, *parts):
    d = Path(ep_dir, "out", *parts)
    d.mkdir(parents=True, exist_ok=True)
    return d


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg が見つかりません。ffmpeg をインストールするか `pip install imageio-ffmpeg` を実行してください。")


def run_ffmpeg(args):
    cmd = [ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", *map(str, args)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"ffmpeg 失敗:\n  {' '.join(cmd)}\n{res.stderr}")


def probe(path):
    """ffprobe を使わず ffmpeg -i の出力から長さと音声トラック有無を取る。"""
    res = subprocess.run([ffmpeg_exe(), "-hide_banner", "-i", str(path)], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", res.stderr)
    if not m:
        sys.exit(f"長さを取得できません: {path}\n{res.stderr}")
    h, mi, s = m.groups()
    return {"duration": int(h) * 3600 + int(mi) * 60 + float(s), "has_audio": "Audio:" in res.stderr}


def wav_duration(path):
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


def find_asset(folder, name):
    """assets/<folder>/<name>.(wav|mp3|...) を探す。なければ None。"""
    for ext in MEDIA_EXTS:
        p = ROOT / "assets" / folder / f"{name}{ext}"
        if p.exists():
            return p
    return None


def find_image(ep_dir, section_id):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = Path(ep_dir, "images", section_id + ext)
        if p.exists():
            return p
    return None
