"""26_kuruma（車ありvs車なし 1年でかかるお金）の解説画面を書き出す（10/28）。

python3 catmeme/make_parts_26_kuruma.py → catmeme/parts/26_kuruma/*.png（＋ preview/）
"""
import os

from PIL import Image, ImageDraw

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "26_kuruma")
PREV = os.path.join(OUT, "preview")
TODAY = "※自転車は最強の乗り物"   # 今日の一言（仮・ユーザーの指定があれば差しかえる）

ITEMS = {
    "e01_title": P.message(["車を持つと", "1年でいくら消える？"], sub="ローン・税金・保険・ガソリン・駐車場　ぜんぶ足してみた", size=92),
    "e02_premise": P.bullets("今回の計算の前提（目安）", [
        "地方に住む会社員",
        "コンパクトカー　新車250万円",
        "5年ローン（金利3%）",
        "年8000km走る（燃費16km/L・ガソリン160円/L）",
        "月極駐車場　月6000円",
    ], size=58),
    "e07_points": P.bullets("今回のポイント", [
        "車は1年で約89万円（月 約7.4万円）",
        "乗らなくても　税金・保険・車検・駐車場はかかる",
        "ローンが終わっても　年35万円くらいは続く",
        "軽自動車・保険の見直し・カーシェアで減らせる",
    ], size=54),
    "e10_ending": P.message(["車は便利。だからこそ", "1年の合計を知っておこう"], size=88),
}


def notice():
    """注意書き：白い太字＋黒いふちだけ（箱なし）。動く背景を半分暗くした上に重ねる。"""
    lines = ["※金額は2026年時点のざっくりの目安です", "※地方・コンパクトカー・5年ローンの場合で計算",
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
