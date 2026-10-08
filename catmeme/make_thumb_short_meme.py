"""ショート「ニュースから生まれたネット名フレーズ6選」のサムネ（縦 1080x1920）。

python3 catmeme/make_thumb_short_meme.py → thumbs/short_meme_phrases.png
作りは make_thumb_short_05_06.py と同じ（いちばん上に話題の帯／大きなタイトル／真ん中に6個のフレーズ札／下に猫2匹）。
"""
from PIL import Image, ImageDraw

import parts as P
from make_thumb_03 import fit_text
from make_thumb_short_04 import BLACK, NAVY, RED, W, WHITE, YELLOW, base, cats, save, topic_band, words

PHRASES = [("553＞1107", RED), ("古古古米", (200, 120, 20)), ("2億円トイレ", RED), ("ジャンボタニシ農法", (30, 140, 70)),
           ("のり弁", NAVY), ("GoToトラブル", RED)]


def tag(img, text, col, cx, cy, rot):
    f = P.font("black", 64)
    d = ImageDraw.Draw(img)
    tw = int(d.textlength(text, font=f)) + 60
    while tw > 500:
        f = P.font("black", f.size - 4)
        tw = int(d.textlength(text, font=f)) + 60
    t = Image.new("RGBA", (tw, 120), (0, 0, 0, 0))
    td = ImageDraw.Draw(t)
    td.rounded_rectangle((0, 0, tw - 1, 119), 22, fill=WHITE, outline=col, width=9)
    td.text((tw / 2, 60), text, font=f, fill=col, anchor="mm")
    t = t.rotate(rot, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(t, (int(cx - t.width / 2), int(cy - t.height / 2)))


def main():
    img = base("bg06_spotlight", ((255, 60, 60, 150), (255, 210, 0, 130)), bg_dir="01_todai")
    d = ImageDraw.Draw(img)
    topic_band(img, "ネットで生まれた名フレーズ")
    fit_text(d, (W / 2, 320), "ニュースから生まれた", 1000, 110, WHITE, BLACK, double=None)
    fit_text(d, (W / 2, 500), "名フレーズ6選", 1040, 190, YELLOW, BLACK, double=WHITE)
    for i, (text, col) in enumerate(PHRASES):
        cx = 280 if i % 2 == 0 else 800
        cy = 700 + (i // 2) * 150
        tag(img, text, col, cx, cy, -4 if i % 2 == 0 else 4)
    cats(img, ("huh_huh_cat", 1.0, False), ("surprise_big_pupils_cat", 0.6, True))
    words(img, [("全部わかる？", 290, 1250, 78, WHITE, 8), ("どれが好き？", 800, 1260, 84, RED, -8)])
    save(img, "short_meme_phrases")


if __name__ == "__main__":
    main()
