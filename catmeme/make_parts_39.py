"""39本目（VTuberの音声ガイド 154万円と経済効果）の解説画面を書き出す（11/2）。

python3 catmeme/make_parts_39.py → catmeme/parts/39_raden/*.png
"""
import os

import make_parts_35_38 as M
import notice_styles as NS
import parts as P

NOTES = ["※金額は報道・県の公開資料をもとにした目安", "※猫は演出です", "※背景の一部はAIで作っています"]

HERE = os.path.dirname(os.path.abspath(__file__))
V = dict(
    today="推しは推せる時に推せ‼",
    notice2="※数字は報道・県の公開資料をもとにした目安",
    title=(["VTuberの音声ガイド", "154万円で何が起きた？"], "県の資料でわかった費用と\n地域の経済効果をくらべてみた"),
    premise=("今回の話", ["静岡県立美術館の音声ガイド", "担当はホロライブの儒烏風亭らでんさん",
                       "2026年1月20日〜3月15日・4つの展示", "スマホで聞ける無料のガイド"]),
    points=("今回のポイント", ["委託料は154万円（収録・制作こみ）", "地域での消費は推計 約3600万円",
                             "費用の約23倍のお金が地域で使われた", "来館者の約34％が発信をきっかけに"]),
    ending=["推しの力は", "地域も動かす"])


def today_only(text):
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (P.W, P.H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = P.font("black", 120)
    w = d.textlength(text, font=f)
    d.text(((P.W - w) / 2, P.H / 2 - 75), text, font=f, fill=(255, 255, 255), stroke_width=10, stroke_fill=(0, 0, 0))
    return img


def main():
    out = os.path.join(HERE, "parts", "39_raden")
    os.makedirs(out, exist_ok=True)
    items = {
        "e00_notice": NS.make("a", V["today"], NOTES),   # 11/2 ユーザー指定：今日のひとこと＋下に小さく注意書き（A案）
        "e01_title": P.message(V["title"][0], sub=V["title"][1], size=88),
        "e02_premise": P.bullets(V["premise"][0], V["premise"][1], size=50),
        "e07_points": P.bullets(V["points"][0], V["points"][1], size=50),
        "e10_ending": P.message(V["ending"], size=96),
        "e11_end_today": NS.make_end("a", V["today"], NOTES),   # 11/2 ユーザー指定：最後のエンディング画面（A案）
    }
    for n, img in items.items():
        img.save(os.path.join(out, n + ".png"))
        print(n)


if __name__ == "__main__":
    main()
