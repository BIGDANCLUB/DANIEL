"""28_nihon_sekai（日本で高い物・安い物 世界とくらべてみた）の解説画面を書き出す（10/29）。

python3 catmeme/make_parts_28_nihon_sekai.py → catmeme/parts/28_nihon_sekai/*.png（＋ preview/）
"""
import os

from PIL import Image, ImageDraw

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "28_nihon_sekai")
PREV = os.path.join(OUT, "preview")
TODAY = "※日本のコンビニは世界一"   # 今日の一言（仮・ユーザーの指定があれば差しかえる）

ITEMS = {
    "e01_title": P.message(["日本で高い物・安い物", "世界とくらべてみた"], sub="ビッグマック・ランチ・電車・病院・ガソリン・高速道路", size=92),
    "e02_premise": P.bullets("今回の計算の前提（目安）", [
        "1ドル＝155円・1ポンド＝195円で計算",
        "「世界」はおもにアメリカ（ニューヨークなど）",
        "値段は2026年ごろのざっくりの目安",
        "お店・地域・時期によって大きく変わります",
    ], size=56),
    "e07_points": P.bullets("今回のポイント", [
        "外食・電車・病院は　日本がかなり安い",
        "ガソリン・高速道路・果物は　日本が高め",
        "円安と　給料があまり上がらないことが大きい",
        "観光客には安い国　日本人には海外旅行が高い国",
    ], size=52),
    "e10_ending": P.message(["安いのは", "うれしいけど……"], size=100),
}


def notice():
    """注意書き：白い太字＋黒いふちだけ（箱なし）。動く背景を半分暗くした上に重ねる。"""
    lines = ["※値段は2026年ごろのざっくりの目安です", "※為替・お店・地域で大きく変わります",
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
