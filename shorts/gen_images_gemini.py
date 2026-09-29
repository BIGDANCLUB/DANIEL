#!/usr/bin/env python3
"""Gemini API（Imagen / Gemini 画像モデル）で台本の各行の画像を作る。

- 行に "prompt" があるものだけ生成し、image_dir/NN.png に保存
- プロンプト・モデル・共通スタイルが同じなら再生成しない
- 気に入らない行は --only 3,7 のように指定して作り直せる

usage:
  python3 gen_images_gemini.py story.json
  python3 gen_images_gemini.py story.json --only 3,7
"""
import base64
import hashlib
import io
import json
import os
import sys

from PIL import Image

from tts_gemini import _request

DEFAULTS = {
    "model": "gemini-3.1-flash-image",
    "style": ("Photorealistic vertical photo taken in Japan, natural light, subtle film grain, "
              "lived-in everyday atmosphere, muted colors. No text, no letters, no signs with writing, "
              "no logos, no watermark. If people appear, show them from behind or only their hands."),
    "image_dir": "images",
}
W, H = 1080, 1920


def image_config(cfg):
    return {**DEFAULTS, **cfg.get("image_gen", {})}


def image_path(cfg, base, i):
    return os.path.join(base, image_config(cfg)["image_dir"], f"{i + 1:02d}.png")


def _key(ic, prompt):
    return hashlib.sha1(json.dumps([ic["model"], ic["style"], prompt]).encode()).hexdigest()


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
    for i, line in enumerate(cfg["lines"]):
        if not line.get("prompt"):
            continue
        out = image_path(cfg, base, i)
        k = _key(ic, line["prompt"])
        name = os.path.basename(out)
        forced = only is not None and (i + 1) in only
        if only is not None and not forced:
            continue
        # 手で置いた画像（manifest に無い）はそのまま使う
        if os.path.exists(out) and not forced and manifest.get(name, k) == k:
            continue
        print(f"[{i + 1:02d}] {line['prompt'][:70]}", flush=True)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        generate(ic, line["prompt"]).save(out)
        manifest[name] = k
        json.dump(manifest, open(manifest_path, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    only = None
    if "--only" in sys.argv:
        only = {int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")}
    ensure_images(sys.argv[1], only)
