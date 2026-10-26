"""自堕落シリーズのサムネ（横 1280x720）。make_thumb_long_ref.py の部品を使う。

python3 catmeme/make_thumb_jidaraku.py → thumbs/jidaraku_01_yakiniku_thumb.png
"""
import os

from PIL import Image, ImageDraw

import make_thumb_long_ref as T
import make_thumb_short_ref as S

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "jidaraku", "01_yakiniku"))


def yakiniku():
    """網の上のきんぐカルビの写真いっぱい＋驚く猫。上に黒い帯、下に黄色い大きな文字（参考 C 型）。"""
    img = T.fill_photo("j05_grill", T.W, T.H, zoom=1.05)
    T.put_cat(img, "stare_tabby_wide_eyes_cat", 0.6, 1010, 600, 520, True)
    T.put_cat(img, "despair_dramatic_kitten", 0.8, 230, 640, 380, False)
    shade = Image.new("RGBA", (T.W, T.H))
    sd = ImageDraw.Draw(shade)
    for y in range(T.H):
        sd.line((0, y, T.W, y), fill=(0, 0, 0, int(170 * max(0, (y - 380) / 340))))
    img.alpha_composite(shade)
    t = T.runs([("30代独身　ひとり焼肉きんぐで調子に乗った結果", (T.YELLOW, T.BLACK))], 58, 6, T.W - 30)
    ImageDraw.Draw(img).rectangle((0, 0, T.W, t.height + 22), fill=T.BLACK + (255,))
    img.alpha_composite(t, ((T.W - t.width) // 2, 11))
    T.scribble(img, "きんぐカルビ", 600, 200, 80, T.YELLOW, -6)
    T.scribble(img, "デカすぎ!!", 640, 300, 96, T.RED, -6)
    b = T.runs([("食べすぎた…", (T.YELLOW, T.BLACK))], 210, 12, 1040, grad=((255, 250, 210), (245, 200, 30)))
    img.alpha_composite(b, ((T.W - b.width) // 2 - 60, T.H - b.height - 30))
    T.save(img, "jidaraku_01_yakiniku_thumb.png")


if __name__ == "__main__":
    yakiniku()
