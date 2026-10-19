"""19_inawashiro（猪苗代湖ボート事故、6年目の逆転有罪）の解説画面を書き出す。原稿 scripts/draft_inawashiro.md（v1）。

python3 catmeme/make_parts_19_inawashiro.py → catmeme/parts/19_inawashiro/*.png（＋ preview/）
人が亡くなっている事故なので、図は事実だけ。事故の様子は描かない。
"""
import os

from PIL import Image

import parts as P
from make_parts_04_leak import table3

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "19_inawashiro")
PREV = os.path.join(OUT, "preview")


def lake_map(title):
    """猪苗代湖と、事故があった中田浜の沖（おおまかな図）。"""
    img, d, (bx0, by0, bx1, by1) = P.card(title, tag="福島県")
    cx, cy = (bx0 + bx1) / 2 + 40, (by0 + by1) / 2 + 10
    # 湖（ざっくりした形：南北に少し長い丸）
    lake = [(-260, -200), (-120, -250), (60, -240), (230, -170), (290, -20), (250, 140), (120, 230), (-60, 240), (-220, 170),
            (-300, 20)]
    lake = [(x * 0.85, y * 0.85) for x, y in lake]
    d.polygon([(cx + x, cy + y) for x, y in lake], fill=(170, 205, 235), outline=(90, 130, 180))
    d.text((cx, cy - 10), "猪苗代湖", font=P.font("round", 70), fill=(40, 70, 120), anchor="mm")
    # 中田浜の沖（湖の南西側）
    px, py = cx - 195, cy + 128
    d.ellipse((px - 22, py - 22, px + 22, py + 22), fill=P.RED_TEXT, outline=P.WHITE, width=5)
    d.text((px - 40, py + 40), "中田浜の沖", font=P.font("round", 56), fill=P.INK, anchor="rt", stroke_width=6,
           stroke_fill=P.WHITE)
    d.text((cx - 380, cy + 10), "会津若松市", font=P.font("round_b", 50), fill=P.MUTED, anchor="rm")
    d.text((cx + 20, cy - 262), "猪苗代町", font=P.font("round_b", 50), fill=P.MUTED, anchor="mm")
    d.text((bx1 - 10, by1 - 10), "※おおまかな図", font=P.font("round", 34), fill=(110, 110, 110), anchor="rb")
    return img


ITEMS = {
    "e00_notice": P.message(["※この事故で亡くなられた方のご冥福をお祈りします", "※裁判の内容は報道をもとにした要旨です", "※猫は演出です",
                             "※今日は家族に「ありがとう」を言いました"], opaque=True, size=58),   # 最後の行は今日の一言
    "e01_title": P.message(["「見えたはず」か「見えなかった」か", "猪苗代湖ボート事故、6年目の逆転有罪"], sub="2026年10月16日　最高裁判所",
                           size=74),
    "e02_map": lake_map("どこで起きた？"),
    "e03_trial": table3("裁判の流れ（報道の要旨）", ("裁判", "判断", "理由"), [
        ("一審・福島地裁（2023年）", ("有罪（禁錮2年の実刑）", True), "約223メートル手前で見つけられたはず"),
        ("二審・仙台高裁（2024年）", "無罪", "確実に見つけられたとは認めがたい"),
        ("最高裁（2026年10月16日）", ("有罪（禁錮2年が確定へ）", True), "二審の判断は「著しく正義に反する」"),
    ], widths=(440, 380), size=38),
    "e06_safety": P.bullets("水辺で気をつけたいこと（一般的な注意）", [
        "泳ぐ・浮かぶのは　決められた遊泳区域で",
        "目立つ色のライフジャケット・帽子",
        "ボートを運転する側は　スピードを落とし、見張りを置く",
        "子どもからは　目を離さない",
    ], size=56),
    "e08_points": P.bullets("今回のポイント", [
        "2020年　湖に浮かんでいた4人にボートが突っ込み、8歳の男の子が亡くなった",
        "一審 有罪 → 二審 無罪 → 最高裁 有罪（禁錮2年が確定へ）",
        "争点は「衝突の前に、被害者を見つけられたか」",
    ], size=52),
}


def main():
    os.makedirs(PREV, exist_ok=True)
    for name, img in ITEMS.items():
        img.save(os.path.join(OUT, name + ".png"))
        bg = P.placeholder_bg("背景")
        bg.alpha_composite(img)
        bg.convert("RGB").save(os.path.join(PREV, name + ".jpg"), quality=85)
    files = sorted(f for f in os.listdir(PREV) if f.endswith(".jpg") and f != "_contact.jpg")
    cols, tw, th = 3, 640, 360
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), "white")
    for i, fn in enumerate(files):
        sheet.paste(Image.open(os.path.join(PREV, fn)).resize((tw - 8, th - 8)), ((i % cols) * tw + 4, (i // cols) * th + 4))
    sheet.save(os.path.join(PREV, "_contact.jpg"), quality=85)
    print(f"{len(ITEMS)} parts -> {OUT}")


if __name__ == "__main__":
    main()
