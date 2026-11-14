"""29_kome（お米が消えた夏 お米の値段はなぜ上がった？）の解説画面を書き出す（10/29）。

python3 catmeme/make_parts_29_kome.py → catmeme/parts/29_kome/*.png（＋ preview/）
"""
import os

from PIL import Image, ImageDraw

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "29_kome")
PREV = os.path.join(OUT, "preview")
TODAY = "※炊きたてのごはんは最強"   # 今日の一言（仮・ユーザーの指定があれば差しかえる）

ITEMS = {
    "e01_title": P.message(["お米が消えた夏", "お米の値段はなぜ上がった？"], sub="2024〜2025年　スーパーの棚が空っぽになったわけ", size=92),
    "e07_points": P.bullets("今回のポイント", [
        "2024年夏　スーパーの棚からお米が消えた",
        "5kgの値段は　約2000円 → 4000円超えに",
        "猛暑・需要の増加・作る量・流通が重なった",
        "国は備蓄米を放出　家計のお米代は約2倍に",
    ], size=54),
    "e10_ending": P.message(["毎日のごはん", "大事に食べよう"], size=100),
}


def notice():
    """注意書き：白い太字＋黒いふちだけ（箱なし）。動く背景を半分暗くした上に重ねる。"""
    lines = ["※内容は報道・国の発表をもとにした要旨です", "※値段はスーパーの平均などのざっくりの目安です",
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
