"""32_jiro（毎日 二郎系ラーメンを食べ続けるとどうなる？）の解説画面を書き出す（10/30）。

python3 catmeme/make_parts_32_jiro.py → catmeme/parts/32_jiro/*.png（＋ preview/）
"""
import os

from PIL import Image, ImageDraw

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "32_jiro")
PREV = os.path.join(OUT, "preview")
TODAY = "※ヤサイマシマシは野菜の摂取にカウントしたい"   # 今日の一言（仮・ユーザーの指定があれば差しかえる）

ITEMS = {
    "e01_title": P.message(["毎日 二郎系ラーメンを", "食べ続けるとどうなる…？"], sub="1日目・1週間・1か月・半年・1年\n体はこう変わる（計算上の目安）", size=88),
    "e02_premise": P.bullets("今回の計算の前提（目安）", [
        "ふつうの食事のうち　1食を二郎系ラーメンに置きかえる",
        "1杯 約1500〜2000kcal・塩分はスープまで飲むと10g以上も",
        "いつもの1食よりも　1日 約800kcal 多くなるとする",
        "体脂肪1kg＝約7200kcal　（実際は人によって大きくちがう）",
    ], size=48),
    "e07_points": P.bullets("今回のポイント", [
        "1杯で　大人の1日の半分以上のカロリーも",
        "スープを全部飲むと　塩分は1日の目標を大きくこえる",
        "毎日だと　体重・むくみ・健康診断にじわじわ出る",
        "楽しむなら　スープを残す・少なめ・次の食事を軽く",
    ], size=50),
    "e10_ending": P.message(["好きな物こそ", "ほどほどに"], size=100),
}


def notice():
    """注意書き：白い太字＋黒いふちだけ（箱なし）。動く背景を半分暗くした上に重ねる。"""
    lines = ["※カロリー・塩分・体重はざっくりの計算上の目安です", "※体への影響は人によって大きくちがいます",
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
