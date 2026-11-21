"""25_wagyu（和牛を狙った男たち）の解説画面を書き出す。原稿はユーザー指定の構成（10/27）。

python3 catmeme/make_parts_25_wagyu.py → catmeme/parts/25_wagyu/*.png（＋ preview/）
"""
import os

from PIL import Image

import parts as P
from make_parts_04_leak import glossary, table3

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "25_wagyu")
PREV = os.path.join(OUT, "preview")
TODAY = "※外国牛の赤身も美味いよね"   # 今日の一言（10/28 ユーザー指定）

ITEMS = {
    "e00_notice": None,   # 下の notice() で作る（半暗転の画面に白い文字だけ）
    "e01_title": P.message(["和牛を狙った男たち", "日本の宝はなぜ守られなかったのか"], sub="2018年　和牛の精液・受精卵 持ち出し事件", size=78),
    "e02_wagyu": glossary("和牛とは？", [
        ("和牛", "次の4品種と\nその交配種だけ"),
        ("4品種", "黒毛和種・褐毛和種\n日本短角種・無角和種"),
        ("黒毛和種", "和牛のほとんど\n何十年も血統を記録して改良"),
    ]),
    "e03_history": table3("和牛が海を渡った歴史", ("いつ", "できごと", "その後"), [
        ("1976年", "研究用に雄牛4頭がアメリカへ", "研究・繁殖に使われる"),
        ("1990年代", "輸出が続く（1993年には雌も）", "数がふえる"),
        ("1997年ごろ", ("約200頭あまりが海外へ", True), "米国→豪州などへ広がる"),
        ("1997年", "生きた牛の輸出を止める", ("精液・受精卵は止められず", True)),
        ("今", "世界中で「WAGYU」が売られる", "豪州は一大産地に"),
    ], widths=(240, 620), size=44),
    "e04_case": table3("事件の流れ（報道・判決より）", ("いつ", "できごと", "ポイント"), [
        ("2018年6月", "大阪→上海のフェリーで運ぶ", "精液と受精卵のストロー365本"),
        ("上海", ("中国の検疫で持ち込み拒否", True), "日本に戻る・中身は廃棄"),
        ("提供", "徳島県の畜産農家", "牧場経営者らがかかわる"),
        ("2019年", "男らを逮捕", "「過去にも何度も運んだ」供述も"),
        ("判決", ("懲役2年／1年2か月", True), "いずれも執行猶予3年"),
    ], widths=(220, 600), size=44),
    "e05_charge": P.bullets("問われたのは何？", [
        "検査を受けずに持ち出したこと",
        "（家畜伝染病予防法違反など）",
        "遺伝資源を海外に持ち出すこと自体を",
        "禁じる法律は　当時なかった",
    ], size=56),
    "e06_law": P.bullets("家畜遺伝資源の不正競争防止法（2020年成立・10月施行）", [
        "不正な入手・使用・転売を禁止",
        "不正に流れたものから生まれた子牛・受精卵も規制の対象",
        "罰則：個人は懲役10年以下・罰金1000万円以下",
        "法人は罰金3億円以下",
        "ストローには種牛の名前を書くことが義務に",
    ], size=50),
    "e07_points": P.bullets("今回のポイント", [
        "和牛の価値は　農家が何十年もかけた改良の結晶",
        "ストロー1本で　その成果を持ち運べてしまう",
        "2018年の事件のあと　ようやく法律ができた",
        "一度渡った血統は　取り戻せない",
    ], size=52),
    "e10_ending": P.message(["次に和牛を食べるとき", "その裏の歴史を少し思い出してほしい"], size=84),
}


def notice():
    """注意書き：白い太字＋黒いふちだけ（箱なし）。動く背景を半分暗くした上に重ねる（10/28 ユーザー指定）。"""
    from PIL import ImageDraw
    lines = ["※事件の内容は報道・判決をもとにした要旨です", "※登場する人物の名前は出しません",
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
