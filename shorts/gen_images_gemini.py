#!/usr/bin/env python3
"""Gemini API（Imagen / Gemini 画像モデル）で台本の画像を作る。

画像の指定は2通り:
  - 行ごと: 行に "prompt" → image_dir/NN.png
  - 場面ごと（安く済む）: 台本トップの "scenes" に場面を定義し、行は "scene" と "crop" で参照。
    1枚を複数行で切り出して使い回せる。scenes の値は {"prompt": ...} か、
    共有ライブラリの画像をそのまま使う {"library": "名前"}（生成しないので無料）
  - プロンプト・モデル・共通スタイルが同じ画像がライブラリにあれば、生成せずにコピーする
  - 生成した画像は library/ に JPEG で登録し、次の作品で使い回す

usage:
  python3 gen_images_gemini.py story.json
  python3 gen_images_gemini.py story.json --only 3,7          # 行番号 or 場面名（例 --only 3,hospital_room）
  python3 gen_images_gemini.py --library [キーワード]          # ライブラリの一覧
  python3 gen_images_gemini.py story.json --seed-library      # 生成済みの画像をライブラリに登録
"""
import base64
import hashlib
import io
import json
import os
import shutil
import sys

from PIL import Image

from tts_gemini import _request

DEFAULTS = {
    "model": "gemini-3.1-flash-lite-image",
    "style": ("Photorealistic vertical photo taken in Japan, natural light, subtle film grain, "
              "lived-in everyday atmosphere, muted colors. No text, no letters, no signs with writing, "
              "no logos, no watermark. If people appear, show them from behind or only their hands."),
    "image_dir": "images",
}
W, H = 1080, 1920
LIB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library")
LIB_INDEX = os.path.join(LIB_DIR, "index.json")


def image_config(cfg):
    return {**DEFAULTS, **cfg.get("image_gen", {})}


def image_path(cfg, base, i):
    return os.path.join(base, image_config(cfg)["image_dir"], f"{i + 1:02d}.png")


def _key(ic, prompt):
    return hashlib.sha1(json.dumps([ic["model"], ic["style"], prompt]).encode()).hexdigest()


def scene_path(cfg, base, name):
    return os.path.join(base, image_config(cfg)["image_dir"], f"scene_{name}.png")


# --- 共有ライブラリ（作品をまたいで画像を使い回す） ---
def load_library():
    return json.load(open(LIB_INDEX, encoding="utf-8")) if os.path.exists(LIB_INDEX) else {}


def save_library(lib):
    os.makedirs(LIB_DIR, exist_ok=True)
    json.dump(lib, open(LIB_INDEX, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)


def add_to_library(img_path, name, prompt, model, key):
    lib = load_library()
    if any(e["key"] == key for e in lib.values()):
        return
    os.makedirs(LIB_DIR, exist_ok=True)
    Image.open(img_path).convert("RGB").save(os.path.join(LIB_DIR, f"{name}.jpg"), quality=88)
    lib[name] = {"file": f"{name}.jpg", "prompt": prompt, "model": model, "key": key}
    save_library(lib)


def from_library(out, name=None, key=None):
    """ライブラリの画像を out にコピー。name 指定か、同じ key（同じプロンプト・モデル・スタイル）で探す。"""
    lib = load_library()
    entry = lib.get(name) if name else next((e for e in lib.values() if e["key"] == key), None)
    if not entry:
        if name:
            sys.exit(f"ライブラリに {name} がありません（python3 gen_images_gemini.py --library で一覧）")
        return False
    os.makedirs(os.path.dirname(out), exist_ok=True)
    Image.open(os.path.join(LIB_DIR, entry["file"])).convert("RGB").save(out)
    return True


def list_library(word=None):
    for name, e in sorted(load_library().items()):
        if not word or word.lower() in (name + e["prompt"]).lower():
            print(f"{name:28s} {e['prompt'][:90]}")


def _make(ic, prompt, out, key, lib_name, forced):
    """ライブラリに同じ画像があればコピー、無ければ生成してライブラリに登録。"""
    if not forced and from_library(out, key=key):
        print(f"  ライブラリから再利用: {os.path.basename(out)}", flush=True)
        return
    print(f"[{lib_name}] {prompt[:70]}", flush=True)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    generate(ic, prompt).save(out)
    add_to_library(out, lib_name, prompt, ic["model"], key)


def generate(ic, prompt):
    full = f"{prompt}\n\n{ic['style']}"
    if ic["model"].startswith("imagen"):
        res = _request(f"models/{ic['model']}:predict", {
            "instances": [{"prompt": full}],
            "parameters": {"sampleCount": 1, "aspectRatio": "9:16"},
        })
        data = res["predictions"][0]["bytesBase64Encoded"]
    else:
        res = _request(f"models/{ic['model']}:generateContent", {
            "contents": [{"parts": [{"text": full}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "9:16"}},
        })
        parts = res["candidates"][0]["content"]["parts"]
        data = next(p["inlineData"]["data"] for p in parts if "inlineData" in p)
    img = Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB")
    # 9:16 に合わせて中央を切り出し、1080x1920 以上に揃える
    iw, ih = img.size
    if iw / ih > W / H:
        nw = int(ih * W / H)
        img = img.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
    else:
        nh = int(iw * H / W)
        img = img.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))
    if img.width < W:
        img = img.resize((W, H), Image.LANCZOS)
    return img


def ensure_images(story_path, only=None):
    cfg = json.load(open(story_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(story_path))
    ic = image_config(cfg)
    manifest_path = os.path.join(base, ic["image_dir"], "manifest.json")
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}
    stem = os.path.splitext(os.path.basename(story_path))[0].replace("story_", "")
    jobs = []   # (出力先, プロンプト or None, ライブラリ名の指定, 登録名, --only の対象か)
    for i, line in enumerate(cfg["lines"]):
        if line.get("prompt"):
            jobs.append((image_path(cfg, base, i), line["prompt"], None, f"{stem}_{i + 1:02d}",
                         only is not None and (i + 1) in only))
    for sname, sc in cfg.get("scenes", {}).items():
        jobs.append((scene_path(cfg, base, sname), sc.get("prompt"), sc.get("library"), f"{stem}_{sname}",
                     only is not None and sname in only))
    for out, prompt, lib_name, reg_name, forced in jobs:
        name = os.path.basename(out)
        if only is not None and not forced:
            continue
        if lib_name:            # ライブラリの画像をそのまま使う（生成しない）
            if not os.path.exists(out) or manifest.get(name) != "lib:" + lib_name:
                from_library(out, name=lib_name)
                manifest[name] = "lib:" + lib_name
        else:
            k = _key(ic, prompt)
            # 手で置いた画像（manifest に無い）はそのまま使う
            if os.path.exists(out) and not forced and manifest.get(name, k) == k:
                continue
            _make(ic, prompt, out, k, reg_name, forced)
            manifest[name] = k
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        json.dump(manifest, open(manifest_path, "w"), ensure_ascii=False, indent=1)


def seed_library(story_path):
    """生成済みの行画像をライブラリに登録する（既存作品の画像を次の作品で使えるように）。"""
    cfg = json.load(open(story_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(story_path))
    ic = image_config(cfg)
    stem = os.path.splitext(os.path.basename(story_path))[0].replace("story_", "")
    for i, line in enumerate(cfg["lines"]):
        path = image_path(cfg, base, i)
        if line.get("prompt") and os.path.exists(path):
            add_to_library(path, f"{stem}_{i + 1:02d}", line["prompt"], ic["model"], _key(ic, line["prompt"]))
    for sname, sc in cfg.get("scenes", {}).items():
        path = scene_path(cfg, base, sname)
        if sc.get("prompt") and os.path.exists(path):
            add_to_library(path, f"{stem}_{sname}", sc["prompt"], ic["model"], _key(ic, sc["prompt"]))


if __name__ == "__main__":
    if sys.argv[1] == "--library":
        list_library(sys.argv[2] if len(sys.argv) > 2 else None)
    elif "--seed-library" in sys.argv:
        seed_library(sys.argv[1])
    else:
        only = None
        if "--only" in sys.argv:
            only = {int(x) if x.isdigit() else x for x in sys.argv[sys.argv.index("--only") + 1].split(",")}
        ensure_images(sys.argv[1], only)
