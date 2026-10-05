#!/usr/bin/env python3
"""ショートのサムネイル（1080x1920）を台本から作る。API は使わない。

台本に "thumb_top"（"1行目\\n2行目"）があれば参考フォーマット:
  上の黒帯に2行の大見出し（1行目 黄・2行目 赤）、下に写真、写真の上に "thumb_teaser" を色の板（座布団）に載せて
  "thumb_teaser_style": "yellow"（既定）/ "red"
無ければ従来の形:

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
from make_short import H, W, font, parse_runs, plain, rich_text

CHANNEL = "日本で生きるということ"
TITLE_SIZE = 190


def background(cfg, base, dark=True):
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
    if not dark:
        return ImageEnhance.Brightness(img).enhance(0.92).convert("RGBA")
    img = ImageEnhance.Brightness(img).enhance(0.62)
    # 文字の周りをさらに暗くして読みやすく（中央に帯状のグラデーション）
    shade = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(shade)
    for yy in range(H):
        t = 1 - min(1, abs(yy - H * 0.47) / (H * 0.30))
        d.line([(0, yy), (W, yy)], fill=int(150 * t))
    img.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), shade.filter(ImageFilter.GaussianBlur(40)))
    return img.convert("RGBA")


def fit_line(text, color, max_w, max_size=150):
    """1行を横幅いっぱいの大きさで描く（長ければ自動で縮む）。"""
    return rich_text(text, max_size, max_w, base=color, stroke_ratio=0.10, line_gap=0.0)


def make_thumb(story_path, out):
    """参考フォーマット: 上に黒帯の2行見出し（1行目 黄・2行目 赤）、下に写真、写真の上に黄色のあおり文。"""
    cfg = json.load(open(story_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(story_path))
    top = cfg.get("thumb_top")
    if not top:
        return make_thumb_classic(cfg, base, out)
    l1, l2 = top.split("\n")
    a = fit_line(l1, "#ffe600", W - 50)
    b = fit_line(l2, "#ff2626", W - 50)
    gap, pad = 18, 40
    band_h = pad + a.height + gap + b.height + pad
    img = background(cfg, base, dark=False)
    band = Image.new("RGBA", (W, band_h), (0, 0, 0, 255))
    band.alpha_composite(a, ((W - a.width) // 2, pad))
    band.alpha_composite(b, ((W - b.width) // 2, pad + a.height + gap))
    img.alpha_composite(band, (0, 0))
    teaser = cfg.get("thumb_teaser")
    if teaser:
        board = teaser_board(teaser, cfg.get("thumb_teaser_style", "yellow"))
        img.alpha_composite(board, (0, int(H * 0.70 - board.height / 2)))
    save(img, out)


TEASER_STYLES = {
    # 板の色, 文字の色, 縁の色, 強調の記号（{…} 黄 / <…> 赤。板と同じ色にならない方へそろえる）
    "red": ((206, 18, 24), "#ffffff", "#000000", "{}"),
    "yellow": ((255, 222, 0), "#111111", "#ffffff", "<>"),
}


TRACK = -0.06    # あおり文の字間（文字の幅に対する割合。少し詰めて大きく見せる）


def tracked(f, s):
    """字間を詰めたときの文字列の幅。"""
    return sum(f.getlength(ch) * (1 + TRACK) for ch in s) - f.getlength(s[-1:]) * TRACK if s else 0


def teaser_board(text, style="yellow"):
    """ニュースのテロップのような帯（画面の端から端までの色の板）に、あおり文を大きく載せる。
    文字は二重の縁取り（内側 白・外側 黒）、帯の上下は黒と白の太い線で締める。"""
    fill, color, edge, (o, c) = TEASER_STYLES[style]
    text = text.translate(str.maketrans("{}<>", o + c + o + c))
    lines = text.split("\n")
    bw, sh = 18, 18                       # 上下の枠の太さ・影の高さ
    size = 200
    while True:
        f = font("thumb", size)
        s_out, s_in = int(size * 0.12), int(size * 0.065)   # 外側（黒）・内側（白）の縁
        widths = [tracked(f, plain(l)) for l in lines]
        if max(widths) + 2 * s_out + 24 <= W or size <= 60:
            break
        size -= 4
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * 1.0)
    py = 18
    bhei = lh * len(lines) + 2 * s_out + py * 2
    canvas = Image.new("RGBA", (W, bhei + 2 * bw + sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    y0 = bw
    # 影 → 枠（黒の外側・白の内側）→ 板
    d.rectangle([0, sh, W, bhei + 2 * bw + sh], fill=(0, 0, 0, 170))
    d.rectangle([0, 0, W, bhei + 2 * bw], fill="#000000")
    d.rectangle([0, bw // 2, W, bhei + bw + bw // 2], fill=edge)
    d.rectangle([0, y0, W, y0 + bhei], fill=fill)
    # 文字：外側の黒縁 → 内側の白縁 → 文字色の順に、1字ずつ詰めて重ねる
    for stroke, stroke_col in ((s_out, "#000000"), (s_in, "#ffffff"), (0, None)):
        for li, l in enumerate(lines):
            x = (W - widths[li]) / 2
            y = y0 + py + s_out + li * lh
            for seg, col in parse_runs(l, color):
                for ch in seg:
                    fc = col if stroke_col is None else stroke_col
                    d.text((x, y), ch, font=f, fill=fc, stroke_width=stroke, stroke_fill=stroke_col or fc)
                    x += f.getlength(ch) * (1 + TRACK)
    return canvas


def save(img, out):
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.convert("RGB").save(out, quality=92)
    print("done:", out)


def make_thumb_classic(cfg, base, out):
    """暗くした写真の中央に大見出しを置く形（thumb_top が無い台本用）。"""
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

    save(img, out)




if __name__ == "__main__":
    make_thumb(sys.argv[1], sys.argv[2])
