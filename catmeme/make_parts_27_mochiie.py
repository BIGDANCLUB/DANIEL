"""27_mochiie（持ち家vs賃貸 一生でかかるお金）の解説画面を書き出す（10/29）。

python3 catmeme/make_parts_27_mochiie.py → catmeme/parts/27_mochiie/*.png（＋ preview/）
"""
import os

from PIL import Image, ImageDraw

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "27_mochiie")
PREV = os.path.join(OUT, "preview")
TODAY = "※住めば都"   # 今日の一言（仮・ユーザーの指定があれば差しかえる）

ITEMS = {
    "e01_title": P.message(["持ち家vs賃貸", "一生でかかるお金"], sub="頭金・ローン・家賃・税金・修繕・更新料　ぜんぶ足してみた", size=96),
    "e02_premise": P.bullets("今回の計算の前提（目安）", [
        "30歳の夫婦・郊外の3LDK",
        "持ち家：4500万円の戸建て　頭金450万・35年ローン（金利1%）",
        "賃貸：同じくらいの広さで家賃 月13万円",
        "35年後（65歳）と　90歳まで　の2つでくらべる",
    ], size=54),
    "e07_points": P.bullets("今回のポイント", [
        "毎月だけなら　ローンのほうが家賃より安いことも",
        "持ち家は税金・修繕で　35年に約1170万円",
        "35年だけなら賃貸が安い　90歳までなら持ち家が安い",
        "金利・災害・転勤・老後の借りにくさも考えて選ぶ",
    ], size=52),
    "e10_ending": P.message(["どっちが正解かは", "暮らし方しだい"], size=96),
}


def notice():
    """注意書き：白い太字＋黒いふちだけ（箱なし）。動く背景を半分暗くした上に重ねる。"""
    lines = ["※金額は2026年時点のざっくりの目安です", "※地域・物件・金利によって大きく変わります",
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
