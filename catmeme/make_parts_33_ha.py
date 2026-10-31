"""33_ha（歯をみがかない・歯医者に行かないとどうなる？）の解説画面を書き出す（10/30）。

python3 catmeme/make_parts_33_ha.py → catmeme/parts/33_ha/*.png（＋ preview/）
"""
import os

from PIL import Image, ImageDraw

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "33_ha")
PREV = os.path.join(OUT, "preview")
TODAY = "※歯は一度失うと生えてこない"   # 今日の一言（仮・ユーザーの指定があれば差しかえる）

ITEMS = {
    "e01_title": P.message(["歯をみがかない・歯医者に", "ずっと行かないとどうなる…？"], sub="1日目・1週間・1か月・1年・10年\n口の中はこう変わる（一般的な目安）", size=84),
    "e03_mushiba": P.bullets("むし歯の進み方（目安）", [
        "C1　表面のエナメル質がとける　（痛みはほぼない）",
        "C2　中の象牙質まで　（冷たい物がしみる）",
        "C3　神経まで　（ズキズキ激痛・根の治療に）",
        "C4　歯の根だけ残る　（抜くことが多い）",
    ], size=52),
    "e07_points": P.bullets("今回のポイント", [
        "みがかないと　数日〜2週間ほどで歯石に",
        "むし歯は　自然には治らない",
        "歯を失う原因のいちばんは　歯周病",
        "歯医者は　痛くなる前に　3〜6か月に1回",
    ], size=52),
    "e10_ending": P.message(["痛くなる前に", "歯医者へ"], size=100),
}


def notice():
    """注意書き：白い太字＋黒いふちだけ（箱なし）。動く背景を半分暗くした上に重ねる。"""
    lines = ["※内容は一般的な目安です　医療の判断は歯科医院で", "※進み方や費用は人によって大きくちがいます",
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
