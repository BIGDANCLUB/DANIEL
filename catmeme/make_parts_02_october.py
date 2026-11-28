"""02_october_changes（10月1日から変わったこと）の解説画面を書き出す。

python3 catmeme/make_parts_02_october.py
→ catmeme/parts/02_october/*.png（本番用・透過PNG）
→ catmeme/parts/02_october/preview/*.jpg（仮背景に重ねた確認用）
"""
import os

from PIL import Image

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "02_october")
PREV = os.path.join(OUT, "preview")

ITEMS = {
    # 冒頭
    "e00_notice": P.message(["※金額は350ml缶1本あたりの「税金」の変化です",
                             "※お店の値段はメーカー・お店ごとに変わります", "※猫は演出です"],
                            opaque=True, size=54),
    "e01_title": P.message(["10月1日から", "いろいろ変わった件"], sub="お酒・たばこ・食べ物・郵便・パート"),
    # 2〜3 酒税
    "e02_sake": P.bullets("そもそも「酒税」ってなに？", [
        "お酒には　消費税とは別に「酒税」がかかる",
        "缶1本ごとに　決まった額の税金が入っている",
        "お酒の種類ごとに　税額がちがう",
    ]),
    "e03_beer3": P.bullets("ビール系は3種類", [
        "ビール",
        "発泡酒（麦芽が少なめ）",
        "第三のビール（新ジャンル）",
        "税金：ビール ＞ 発泡酒 ＞ 第三のビール",
    ]),
    "e03b_itachi": P.flow("税金をめぐる　いたちごっこ", [
        ("メーカー", "税金の安い\nビールっぽいお酒を\n開発"),
        ("国", "ルールを変えて\n税を上げる"),
        ("メーカー", "また別の\nお酒を開発……"),
    ]),
    "e03c_plan": P.flow("2017年に決めたこと", [
        ("2020年10月", "1回目の見直し"),
        ("2023年10月", "2回目の見直し"),
        ("2026年10月", "ビール系の税が\nぜんぶ同じ額に"),
    ]),
    "e04_beer": P.bars("350ml缶1本の税金（ビール）", [
        ("〜2020年9月", 77, False, ""),
        ("2020年10月", 70, False, ""),
        ("2023年10月", 63.35, False, ""),
        ("2026年10月", 54.25, True, "−9.10円"),
    ], unit="円"),
    "e04b_third": P.bars("350ml缶1本の税金（第三のビール）", [
        ("〜2020年9月", 28, False, ""),
        ("2020年10月", 37.8, False, ""),
        ("2023年10月", 46.99, False, ""),
        ("2026年10月", 54.25, True, "＋7.26円"),
    ], unit="円", note="発泡酒（麦芽25％未満）も　今回 7.26円の増税"),
    # 4 チューハイ・たばこ
    "e05_chuhai": P.bullets("チューハイ・たばこも", [
        "チューハイなど：1本28円 → 35円（7円の増税）",
        "加熱式たばこ：4月に続き2回目の値上げ",
        "1箱あたり20〜40円ほど上がる",
        "紙巻きたばこ：2027年4月から増税の予定",
    ], size=54),
    # 5 食べ物・郵便
    "e06_food": P.bullets("食べ物・飲み物も値上げ", [
        "10月に値上げ：3,033品目（8月末時点）",
        "調味料・加工食品が中心",
        "2026年の合計：1万9,083品目（1〜11月分）",
    ], tag="帝国データバンク調べ"),
    "e07_post": P.bullets("郵便も値上げ", [
        "ゆうパック：平均 約10％値上げ",
        "クリックポスト：185円 → 240円",
        "ゆうパケット：360円に統一（厚さ1〜3cm）",
    ]),
    # 6 106万円の壁
    "e08_wall": P.flow("「106万円の壁」がなくなる", [
        ("これまで", "月8万8千円以上\n（年収 約106万円）\nかつ 週20時間以上"),
        ("10月1日から", "給料の条件はなし\n週20時間以上なら\n社会保険に入る"),
        ("対象の会社", "今は51人以上\n2027年10月から\n少しずつ広がる"),
    ]),
    "e08b_merit": P.bullets("社会保険に入ると", [
        "保険料が引かれる → 手取りは減る",
        "将来もらえる年金が増える",
        "病気・ケガで休んだときの手当がある",
        "扶養の「130万円の壁」はそのまま",
    ]),
    # 8 まとめ・締め
    "e09_matome": P.bullets("10月1日から変わったこと", [
        "ビール：1本9.10円の減税",
        "第三のビール・発泡酒：7.26円の増税",
        "チューハイ：7円の増税／加熱式たばこ：値上げ",
        "食べ物・飲み物：約3,000品目の値上げ",
        "ゆうパック：平均 約10％の値上げ",
        "パートの「106万円の壁」：廃止",
    ], size=48),
    "e10_ending": P.message(["あなたは得した？ 損した？", "コメントで教えて！"], size=88),
}


def main():
    os.makedirs(PREV, exist_ok=True)
    for name, img in ITEMS.items():
        img.save(os.path.join(OUT, name + ".png"))
        bg = P.placeholder_bg("背景")
        if name not in ("e00_notice", "e01_title", "e10_ending"):
            cat = P.canvas()
            P.placeholder_cat(cat, P.CAT_SLOT, "小さい猫")
            bg.alpha_composite(cat)
        bg.alpha_composite(img)
        bg.convert("RGB").save(os.path.join(PREV, name + ".jpg"), quality=85)
    files = sorted(f for f in os.listdir(PREV) if f.endswith(".jpg") and f != "_contact.jpg")
    cols, tw, th = 4, 480, 270
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), "white")
    for i, fn in enumerate(files):
        im = Image.open(os.path.join(PREV, fn)).resize((tw - 8, th - 8))
        sheet.paste(im, ((i % cols) * tw + 4, (i // cols) * th + 4))
    sheet.save(os.path.join(PREV, "_contact.jpg"), quality=85)
    print(f"{len(ITEMS)} parts -> {OUT}")


if __name__ == "__main__":
    main()
