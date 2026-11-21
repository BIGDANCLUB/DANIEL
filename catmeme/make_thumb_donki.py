"""自堕落シリーズ #25 ドン・キホーテのサムネ案（11/21）。吉野家・競馬回と同じ形：
写真を全面・左に猫・右上に白ふちの商品写真・黄色い角丸の帯に赤い太字・帯の上に白地の札。

python3 catmeme/make_thumb_donki.py → thumbs/jidaraku_25_donki_thumb_c1〜c3.png
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S
import make_thumb_yoshinoya as Y

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "jidaraku", "25_donki"))


def main():
    Y.one("jidaraku_25_donki_thumb_c1.png", "dk01_front", "surprise_big_pupils_cat", "歯ブラシだけのはずが", tag="30代独身　休日の夜", item="dk06_basket")
    Y.one("jidaraku_25_donki_thumb_c2.png", "dk02_aisle", "happy_hamster_open_arms", "ドンキは大人の遊園地", tag="30代独身　予定なし", item="f_blanket")
    Y.one("jidaraku_25_donki_thumb_c3.png", "dk01_front", "stare_tabby_wide_eyes_cat", "予定がない夜はドンキ", tag="30代独身", item="f_karaage")


if __name__ == "__main__":
    main()


def final():
    """11/21 ユーザー指定：吉野家の決定版（final3）と同じ作り。ドンキの外観を全面・着る毛布の猫（ユーザー提供 t_cat_blanket）を
    上半身アップで真ん中・白い札「30代独身 休日の夜」・黄色い角丸の帯に赤い太字「夜のドンキは大人の宝物庫！」。"""
    from PIL import Image, ImageDraw
    img = T.fill_photo("dk01_front", T.W, T.H, cy=0.4)
    cat = Image.open(os.path.join(T.HERE, "backgrounds", "jidaraku", "25_donki", "t_cat_blanket.png")).convert("RGBA")
    cat = cat.crop((0, 0, cat.width, int(cat.height * 0.55)))
    k = 880 / cat.width
    cat = cat.resize((880, int(cat.height * k)), Image.LANCZOS)
    img.alpha_composite(cat, ((T.W - cat.width) // 2, T.H - cat.height - 40))
    big = T.runs([("夜の", T.RED), ("ドンキ", T.BLUE), ("は大人の宝物庫", T.RED)], 170, 10, T.W - 220)   # 11/21：ドンキは青・！なし
    bh = big.height + 40
    by = T.H - bh - 18
    ImageDraw.Draw(img).rounded_rectangle((60, by, T.W - 60, by + bh), 36, fill=(255, 245, 60, 255))
    img.alpha_composite(big, ((T.W - big.width) // 2, by + 20))
    t = T.runs([("30代独身　休日の夜", (T.RED, T.WHITE))], 60, 2, 900)
    box = Image.new("RGBA", (t.width + 56, t.height + 34), T.WHITE + (255,))
    box.alpha_composite(t, (28, 17))
    img.alpha_composite(box, ((T.W - box.width) // 2, by - box.height + 12))
    T.save(img, "jidaraku_25_donki_thumb_final.png")
