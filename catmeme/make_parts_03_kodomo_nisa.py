"""03_kodomo_nisa（こどもNISA）の解説画面を書き出す。

python3 catmeme/make_parts_03_kodomo_nisa.py
→ catmeme/parts/03_kodomo_nisa/*.png（本番用・透過PNG）
→ catmeme/parts/03_kodomo_nisa/preview/*.jpg（仮背景に重ねた確認用）
"""
import os

from PIL import Image

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "03_kodomo_nisa")
PREV = os.path.join(OUT, "preview")


def table(title, head, rows, hi_col=2, tag=""):
    """比べる表。head = (空, 列1, 列2)、rows = [(項目, 列1, 列2)]。hi_col の列を強調色にする。"""
    img, d, (bx0, by0, bx1, by1) = P.card(title, tag)
    hf, cf = P.font("round", 56), P.font("round_b", 52)
    col_w = [330, (bx1 - bx0 - 330) / 2, (bx1 - bx0 - 330) / 2]
    xs = [bx0, bx0 + col_w[0], bx0 + col_w[0] + col_w[1]]
    row_h = (by1 - by0) / (len(rows) + 1)
    # 見出し行
    for j, h in enumerate(head):
        if not h:
            continue
        x0 = xs[j] + 8
        d.rounded_rectangle((x0, by0, x0 + col_w[j] - 16, by0 + row_h - 12), 18,
                            fill=P.ACCENT if j == hi_col else P.NAVY)
        d.text((x0 + (col_w[j] - 16) / 2, by0 + (row_h - 12) / 2), h, font=hf, fill=P.WHITE, anchor="mm")
    for i, r in enumerate(rows):
        y = by0 + row_h * (i + 1)
        d.line((bx0, y, bx1, y), fill=P.NEUTRAL, width=2)
        for j, cell in enumerate(r):
            f = hf if j == 0 else cf
            col = P.INK if j != hi_col else P.ACCENT
            d.text((xs[j] + col_w[j] / 2 if j else xs[j] + 10, y + row_h / 2), cell, font=f, fill=col,
                   anchor="mm" if j else "lm")
    return img


ITEMS = {
    # 冒頭
    "e00_notice": P.message(["※この動画は制度の紹介です。投資をすすめるものではありません",
                             "※投資は元本割れすることがあります", "※猫は演出です"], opaque=True, size=50),
    "e01_title": P.message(["こどもNISAって", "結局お得？"], sub="違い・お得・イマイチを解説"),
    "e01b_theme": P.flow("今日のテーマ", [
        ("NISAと\nどう違う？", "使える人\n枠・引き出し"),
        ("どこが\nお得？", "非課税の枠・\n長く運用できる"),
        ("どこが\nイマイチ？", "世間の反応"),
    ], hsize=58, ssize=46),
    # 2 きほん
    "e02_basic": P.bullets("こどもNISAのきほん", [
        "0〜17歳の子どもの名前で作るNISA",
        "1年に60万円まで　合計600万円まで",
        "増えた分に税金がかからない（ふつうは約20％）",
        "買えるのは「積立向けの投資信託」だけ",
        "お金を出して運用するのは　親など",
    ], size=64),
    # 3 違い
    "e03_compare": table("ふつうのNISAと比べると", ("", "ふつうのNISA", "こどもNISA"), [
        ("使える人", "18歳以上", "0〜17歳"),
        ("1年の上限", "360万円", "60万円"),
        ("合計の上限", "1,800万円", "600万円"),
        ("買えるもの", "投資信託・株など", "積立向け投資信託"),
        ("引き出し", "いつでもOK", "12歳までは原則NG"),
    ]),
    "e03b_withdraw": P.flow("引き出しのルール", [
        ("12歳未満", "原則NG\n（災害など\nだけ例外）"),
        ("12歳から", "子のための\n出費はOK\n（同意と書類）"),
        ("18歳で", "大人のNISAに\n自動で引っ越し"),
    ], hsize=58, ssize=46),
    "e03c_1800": P.bars("大人になってからの枠", [
        ("大人のNISAの合計", 1800, False, ""),
        ("こどもNISAで使った分", 600, True, "ここに含まれる"),
        ("18歳から使える残り", 1200, False, ""),
    ], unit="万円", note="こどもNISAで使った枠は　大人の1,800万円に含まれる"),
    # 4 お得
    "e04_merit": P.bullets("お得なところ", [
        "① 家族の非課税の枠が増える",
        "② 0歳から始めると　18年も運用できる",
        "③ 12歳から教育費に使える・非課税は無期限",
        "④ 祖父母からの援助の受け皿になる",
    ], size=64),
    "e04b_sim": P.bars("月1万円を0歳から18年つみたてたら（仮の計算）", [
        ("入れたお金", 216, False, ""),
        ("年3％で増えたら", 286, True, "＋約70万円"),
    ], unit="万円", note="※仮の計算です。増えるとは限らず、減ることもあります"),
    "e04c_junior": table("前の制度（ジュニアNISA）の反省", ("", "ジュニアNISA", "こどもNISA"), [
        ("1年の上限", "80万円", "60万円"),
        ("合計の上限", "400万円", "600万円"),
        ("非課税の期間", "5年", "無期限"),
        ("引き出し", "18歳まで原則NG", "12歳から条件つきOK"),
    ]),
    # 5 イマイチ
    "e05_demerit": P.bullets("イマイチと言われているところ", [
        "① まず親のNISAを埋めるのが先",
        "② お金に余裕のある家しか使えない",
        "③ 引き出しのルールがめんどう",
        "④ 18歳で子どものお金になる",
        "⑤ 投資だから減ることもある",
        "⑥ どうせまた制度が変わりそう",
    ], size=64),
    # 6 向いている家
    "e06_fit": P.flow("どんな家に向いてる？", [
        ("向いている", "親の枠が\n埋まりそう\n祖父母の援助"),
        ("向いている", "12歳以降の\n教育費に\n使いたい"),
        ("向いていない", "親の枠が\nまだ空き\nすぐ使うお金"),
    ], hsize=58, ssize=46),
    # 7 まとめ・締め
    "e07_matome": P.bullets("まとめ", [
        "こどもNISA：0〜17歳・年60万円・合計600万円",
        "お得：家族の非課税枠が増える・長く運用できる",
        "お得：12歳から教育費に使える",
        "イマイチ：引き出しに条件・18歳で子のお金に",
        "イマイチ：大人の枠に含まれる・減ることもある",
    ], size=64),
    "e08_ending": P.message(["あなたの家は使う？ 使わない？", "コメントで教えて！"], size=84),
}


def main():
    os.makedirs(PREV, exist_ok=True)
    for name, img in ITEMS.items():
        img.save(os.path.join(OUT, name + ".png"))
        bg = P.placeholder_bg("背景")
        if name not in ("e00_notice", "e01_title", "e08_ending"):
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
