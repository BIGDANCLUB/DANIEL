"""34_bike（車vs125ccバイク 1年でかかるお金）の解説画面を書き出す（10/28）。

python3 catmeme/make_parts_34_bike.py → catmeme/parts/34_bike/*.png（＋ preview/）
"""
import os

from PIL import Image, ImageDraw

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "34_bike")
PREV = os.path.join(OUT, "preview")
TODAY = "※雨の日はカッパが本体"   # 今日の一言（仮・ユーザーの指定があれば差しかえる）

ITEMS = {
    "e01_title": P.message(["車と125ccバイク", "1年でいくら違う？"], sub="車体・税金・保険・車検・ガソリン・駐車場\nぜんぶ足してみた", size=92),
    "e02_premise": P.bullets("今回の計算の前提（目安）", [
        "地方に住む会社員・年8000km走る",
        "車：コンパクトカー新車250万円・5年ローン（金利3%）",
        "バイク：125cc（原付二種）新車35万円を5年で割る",
        "ガソリン170円/L　燃費　車16km/L・バイク50km/L",
        "駐車場　車 月6000円・バイク 月2000円",
    ], size=50),
    "e07_points": P.bullets("今回のポイント", [
        "車は年 約89万円　125ccバイクは年 約18万円",
        "バイクは車検なし・重量税なし・税金は年2400円",
        "ただし雨・寒さ・荷物・高速道路に乗れない",
        "通勤だけならバイク　家族や遠出なら車",
    ], size=52),
    "e10_ending": P.message(["自分の暮らしに合う", "乗り物をえらぼう"], size=96),
}


def notice():
    """注意書き：白い太字＋黒いふちだけ（箱なし）。動く背景を半分暗くした上に重ねる。"""
    lines = ["※金額は2026年時点のざっくりの目安です", "※地方・コンパクトカーと125ccバイクで計算",
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
