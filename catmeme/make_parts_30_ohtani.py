"""30_ohtani（大谷翔平 メジャー直行宣言から日本ハム入団まで）の解説画面を書き出す（10/29）。

python3 catmeme/make_parts_30_ohtani.py → catmeme/parts/30_ohtani/*.png（＋ preview/）
"""
import os

from PIL import Image, ImageDraw

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "30_ohtani")
PREV = os.path.join(OUT, "preview")
TODAY = "※デコピンの方が自分より良い暮らししています"   # 今日の一言（10/30 ユーザー指定）

ITEMS = {
    "e01_title": P.message(["メジャー直行宣言から", "日本ハム入団まで"], sub="2012年　大谷翔平と「強行指名」の舞台裏", size=92),
    "e10_ending": P.message(["夢への道は", "ひとつじゃない"], size=100),
}


def notice():
    """注意書き：白い太字＋黒いふちだけ（箱なし）。動く背景を半分暗くした上に重ねる。"""
    lines = ["※内容は報道・球団の発表をもとにした要旨です", "※セリフは流れをわかりやすくするための再現です",
             "※猫は演出です　※背景の一部はAIで作っています", TODAY]
    img = Image.new("RGBA", (P.W, P.H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = P.font("black", 64)
    y = (P.H - len(lines) * 100) // 2
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text(((P.W - w) / 2, y), ln, font=f, fill=(255, 255, 255), stroke_width=7, stroke_fill=(0, 0, 0))
        y += 100
    return img


ITEMS["e00_notice"] = notice()


def main():
    os.makedirs(PREV, exist_ok=True)
    for name, img in ITEMS.items():
        img.save(os.path.join(OUT, name + ".png"))
        bg = P.placeholder_bg("背景")
        bg.alpha_composite(img)
        bg.convert("RGB").save(os.path.join(PREV, name + ".jpg"), quality=85)
    print(f"{len(ITEMS)} parts -> {OUT}")


if __name__ == "__main__":
    main()
