"""26本目（車ありvs車なし 1年でかかるお金）のサムネ候補3つ（10/29）。横 1280x720。
和牛のドパガキ向け（虹色・金色・猫多め・キラキラなし・爆発の吹き出し）と同じ作り。人は描かない。

python3 catmeme/make_thumb_kuruma.py → thumbs/26_kuruma_a.png / _b / _c
"""
import os

from PIL import Image, ImageDraw

import make_thumb_long_ref as T
import make_thumb_short_ref as S
import make_thumb_wagyu_dopa as D

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "26_kuruma"))
W, H = T.W, T.H
RED, YEL, WHITE, BLACK = D.RED, D.YEL, D.WHITE, D.BLACK


def a():
    """販売店の車＋「車を持つと1年で 89万!?」＋下の帯「月7万4000円が消える」"""
    img = D.punchy("bg26_car_dealer", zoom=1.05)
    D.rainbow_rays(img, 640, 300, alpha=130)
    D.rainbow_band(img, H - 190, 190)
    for c_ in [("stare_tabby_wide_eyes_cat", 0.6, 1100, 535, 540, True), ("despair_dramatic_kitten", 0.8, 170, 545, 420, False),
               ("scream_phone_orange_cat", 1.0, 420, 535, 300, False), ("money_counting_orange_cat", 1.0, 850, 535, 280, True)]:
        T.put_cat(img, *c_)
    ex = D.explosion2([("車を持つと1年で", 92), ("89万!?", 200)], 720, 440, angle=5)
    D.put(img, D.glow(ex, (255, 255, 255), r=22), 620, 230)
    l1 = T.runs([("毎月", (WHITE, BLACK))], 96, 14, 300, shadow=True)
    l2 = D.gold_text("7万4000円", 128, 640)
    l3 = T.runs([("が消える", (WHITE, BLACK))], 96, 14, 420, shadow=True)
    x0 = (W - (l1.width + l2.width + l3.width - 20)) // 2
    y = H - 95
    img.alpha_composite(l1, (x0, y - l1.height // 2))
    img.alpha_composite(l2, (x0 + l1.width - 10, y - l2.height // 2))
    img.alpha_composite(l3, (x0 + l1.width + l2.width - 20, y - l3.height // 2))
    T.save(img, "26_kuruma_a.png")


def b():
    """左右くらべ：左「車あり」（販売店）・右「車なし」（駅）＋まん中に虹色の「差は年74万!?」"""
    left = D.punchy("bg26_car_dealer", zoom=1.0)
    right = D.punchy("bg54_station_crowd_map", zoom=1.0)
    img = Image.new("RGBA", (W, H))
    img.alpha_composite(left.crop((W // 4, 0, W // 4 + W // 2, H)), (0, 0))
    img.alpha_composite(right.crop((W // 4, 0, W // 4 + W // 2, H)), (W // 2, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((W // 2 - 8, 0, W // 2 + 8, H), fill=BLACK)
    d.rectangle((W // 2 - 3, 0, W // 2 + 3, H), fill=WHITE)
    D.put(img, D.big_text([("車あり", RED)], 120, 560, -4), 320, 90)
    D.put(img, D.big_text([("車なし", (40, 140, 255))], 120, 560, 4), 960, 90)
    T.put_cat(img, "despair_dramatic_kitten", 0.8, 300, 560, 420, False)
    T.put_cat(img, "sad_banana_cat_cry", 1.0, 520, 545, 260, False)
    T.put_cat(img, "dance_happy_banana_cat", 0.5, 980, 560, 400, True)
    T.put_cat(img, "dance_three_kittens", 0.8, 1170, 545, 250, True)
    D.rainbow_band(img, H - 190, 190)
    l1 = T.runs([("1年の差", (WHITE, BLACK))], 120, 16, 500, shadow=True)
    l2 = D.rainbow_text("74万円!?", 160, 700)
    x0 = (W - (l1.width + l2.width - 10)) // 2
    img.alpha_composite(l1, (x0, H - 95 - l1.height // 2))
    img.alpha_composite(l2, (x0 + l1.width - 10, H - 95 - l2.height // 2))
    D.put(img, D.explosion("VS", 200, 170, size=96, angle=-8), W // 2, 250)
    T.save(img, "26_kuruma_b.png")


def c():
    """東京の駐車場＋金色の「10年で470万」＋爆発「新車もう1台!?」"""
    img = D.punchy("bg26_tokyo_parking", zoom=1.08)
    D.rainbow_rays(img, 640, 330, alpha=120, rot=0.05)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 60))
    img.alpha_composite(shade)
    for c_ in [("huh_huh_cat", 1.0, 1110, 730, 520, True), ("stare_tabby_wide_eyes_cat", 0.6, 170, 730, 420, False),
               ("scream_phone_orange_cat", 1.0, 440, 730, 330, False)]:
        T.put_cat(img, *c_)
    D.put(img, D.big_text([("車を10年持つと", WHITE)], 110, 1000, -3), 600, 95)
    D.put(img, D.glow(D.gold_text("470万円", 230, 1100), (255, 220, 80), r=20), 620, 270)
    D.put(img, D.explosion2([("新車", 90), ("もう1台!?", 120)], 520, 340, angle=-6), 820, 540)
    T.save(img, "26_kuruma_c.png")


if __name__ == "__main__":
    a()
    b()
    c()
