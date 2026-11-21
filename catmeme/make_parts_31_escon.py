"""31_escon（札幌ドームを出て日本ハムがエスコンを建てた話）の解説画面を書き出す（10/30）。

python3 catmeme/make_parts_31_escon.py → catmeme/parts/31_escon/*.png（＋ preview/）
"""
import os

from PIL import Image, ImageDraw

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "31_escon")
PREV = os.path.join(OUT, "preview")
TODAY = "※球場で温泉に入れる時代"   # 今日の一言（仮・ユーザーの指定があれば差しかえる）

ITEMS = {
    "e01_title": P.message(["家賃が高すぎて", "球場ごと建てた球団"], sub="札幌ドームからエスコンフィールドへ\n日本ハムの大移動", size=92),
    "e02_compare": P.bullets("札幌ドームとエスコン（目安）", [
        "持ち主　札幌ドーム＝札幌市　エスコン＝球団の会社",
        "屋根　札幌ドーム＝閉じたまま　エスコン＝開け閉めできる",
        "芝　札幌ドーム＝人工芝（野球）　エスコン＝天然芝",
        "看板・飲食のお金　札幌ドーム＝おもにドーム側　エスコン＝球団に",
    ], size=48),
    "e07_points": P.bullets("今回のポイント", [
        "札幌ドームは使うだけで　年に20億円以上とも",
        "看板や飲食のお金が　球団に入りにくかった",
        "自分たちの球場を　北広島市に約600億円で建てた",
        "温泉・ホテル・ビール工房つきの　ボールパークに",
    ], size=50),
    "e10_ending": P.message(["借りるより", "自分で建てた"], size=100),
}


def notice():
    """注意書き：白い太字＋黒いふちだけ（箱なし）。動く背景を半分暗くした上に重ねる。"""
    lines = ["※内容は報道・球団や市の発表をもとにした要旨です", "※金額はざっくりの目安です　※セリフは再現です",
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
