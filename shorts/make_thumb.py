#!/usr/bin/env python3
"""ショートのサムネイル（1080x1920）を台本から作る。API は使わない。

- 背景: 1行目の画像（場面画像なら crop の位置）を少し暗くして全面に
- 上: 小さなタグ（台本の banner 1行目。例「知らないと大損する」）
- 中央: 大きな見出し（台本の "thumb"。無ければ1行目の字幕）。{黄} <赤> が使える
- 下: チャンネル名

usage:
  python3 make_thumb.py story.json out/xxx_thumb.jpg
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

import gen_images_gemini
from make_short import H, W, font, rich_text

CHANNEL = "日本で生きるということ"
TITLE_SIZE = 190


def background(cfg, base):
    l = cfg["lines"][0]
    if "scene" in l:
        img = Image.open(gen_images_gemini.scene_path(cfg, base, l["scene"])).convert("RGB")
        cx, cy, zoom = l.get("crop", [0.5, 0.5, 1.0])
    else:
        img = Image.open(gen_images_gemini.image_path(cfg, base, 0)).convert("RGB")
        cx, cy, zoom = 0.5, 0.5, 1.0
    w = img.width / zoom
    h = w * H / W
    x = min(max(0, cx * img.width - w / 2), img.width - w)
    y = min(max(0, cy * img.height - h / 2), img.height - h)
    img = img.transform((W, H), Image.EXTENT, (x, y, x + w, y + h), Image.BICUBIC)
    img = ImageEnhance.Brightness(img).enhance(0.62)
    # 文字の周りをさらに暗くして読みやすく（中央に帯状のグラデーション）
    shade = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(shade)
    for yy in range(H):
        t = 1 - min(1, abs(yy - H * 0.47) / (H * 0.30))
        d.line([(0, yy), (W, yy)], fill=int(150 * t))
    img.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), shade.filter(ImageFilter.GaussianBlur(40)))
    return img.convert("RGBA")


def make_thumb(story_path, out):
    cfg = json.load(open(story_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(story_path))
    img = background(cfg, base)

    tag = cfg.get("thumb_tag") or (cfg.get("banner", "").split("\n")[0] or "知らないと大損する")
    tag_img = rich_text(tag, 84, W - 160, base="#ffffff", stroke_ratio=0.0)
    pad = 36
    box = Image.new("RGBA", (tag_img.width + pad * 2, tag_img.height + pad), (215, 20, 20, 255))
    box.alpha_composite(tag_img, (pad, pad // 2))
    img.alpha_composite(box, ((W - box.width) // 2, 260))

    title = cfg.get("thumb") or cfg["lines"][0]["text"]
    t = rich_text(title, TITLE_SIZE, W - 60, base="#ffffff", stroke_ratio=0.16, line_gap=0.02)
    img.alpha_composite(t, ((W - t.width) // 2, int(H * 0.47 - t.height / 2)))

    ch = rich_text(CHANNEL, 60, W - 200, base="#ffffff", stroke_ratio=0.12)
    img.alpha_composite(ch, ((W - ch.width) // 2, H - 360))

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.convert("RGB").save(out, quality=92)
    print("done:", out)


if __name__ == "__main__":
    make_thumb(sys.argv[1], sys.argv[2])
