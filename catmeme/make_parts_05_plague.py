"""05_plague（ロシアのペスト研究所）の解説画面を書き出す。

python3 catmeme/make_parts_05_plague.py → catmeme/parts/05_plague/*.png（＋ preview/）
"""
import os

from PIL import Image, ImageDraw

import parts as P
from make_parts_04_leak import glossary, table3

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "05_plague")
PREV = os.path.join(OUT, "preview")


def distance_map(title):
    """イルクーツクと日本の位置関係（おおまかな図。直線距離つき）。"""
    img, d, (bx0, by0, bx1, by1) = P.card(title)
    # 経度・緯度をそのまま平面に（おおまかでよい）
    def xy(lat, lon):
        x = bx0 + 80 + (lon - 98) / (146 - 98) * (bx1 - bx0 - 160)
        y = by0 + 40 + (56 - lat) / (56 - 32) * (by1 - by0 - 80)
        return x, y
    # 日本列島（ざっくりした形）
    honshu = [xy(41.5, 140.5), xy(40, 142), xy(37, 141), xy(35, 140.5), xy(34, 136), xy(34, 132), xy(35.5, 133), xy(37, 137),
              xy(38.5, 139.5)]
    hokkaido = [xy(45.4, 141.7), xy(44, 145.5), xy(42.5, 143.5), xy(41.5, 140.5), xy(43, 140.5)]
    kyushu = [xy(33.9, 130.9), xy(33.5, 132), xy(31.2, 131.2), xy(31.3, 130.2), xy(33.2, 129.6)]
    for poly in (honshu, hokkaido, kyushu):
        d.polygon(poly, fill=(205, 225, 205), outline=(120, 150, 120))
    pts = {"イルクーツク": xy(52.3, 104.3), "札幌": xy(43.06, 141.35), "東京": xy(35.68, 139.69)}
    for a, b, label, off in (("イルクーツク", "札幌", "約2,900km", (-40, -60)), ("イルクーツク", "東京", "約3,300km", (-60, 50))):
        (x0, y0), (x1, y1) = pts[a], pts[b]
        n = 28
        for k in range(n):
            if k % 2 == 0:
                d.line((x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n, x0 + (x1 - x0) * (k + 1) / n, y0 + (y1 - y0) * (k + 1) / n),
                       fill=P.ACCENT, width=8)
        mx, my = (x0 + x1) / 2 + off[0], (y0 + y1) / 2 + off[1]
        d.text((mx, my), label, font=P.font("round_b", 60), fill=P.ACCENT, anchor="mm", stroke_width=6, stroke_fill=P.WHITE)
    for name, (x, y) in pts.items():
        r = 22 if name == "イルクーツク" else 16
        d.ellipse((x - r, y - r, x + r, y + r), fill=P.RED_TEXT if name == "イルクーツク" else P.NAVY, outline=P.WHITE, width=5)
        anchor = "lm" if name != "イルクーツク" else "mb"
        tx, ty = (x + 30, y) if name != "イルクーツク" else (x, y - 30)
        d.text((tx, ty), name, font=P.font("round_b", 58), fill=P.INK, anchor=anchor, stroke_width=6, stroke_fill=P.WHITE)
    d.text((pts["イルクーツク"][0], pts["イルクーツク"][1] + 40), "（ロシア・シベリア）", font=P.font("round_b", 42), fill=P.INK,
           anchor="mt", stroke_width=5, stroke_fill=P.WHITE)
    d.text((bx1 - 10, by1 - 10), "※直線距離・おおまかな図", font=P.font("round", 34), fill=(110, 110, 110), anchor="rb")
    return img


ITEMS = {
    "e00_notice": P.message(["※亡くなった方のご冥福をお祈りします", "※ロシア当局は「ペストは確認されていない」と発表しています",
                             "※実在の人物の言葉は、報道をもとにした要旨です", "※猫は演出です"], opaque=True, size=62),
    "e01_title": P.message(["ロシアの「ペスト研究所」で", "何が起きた？"], sub="2026年10月　シベリア・イルクーツク州", size=110),
    "e02_map": distance_map("どこで起きた？"),
    "e03_timeline": table3("何が起きたか（時系列）", ("いつ", "何があった", "ポイント"), [
        ("9月末", "職員（28歳）が体調をくずす", ""),
        ("10/2", "重い肺炎で亡くなる", ""),
        ("同じころ", "接触した人を隔離・観察", ("約200人", True)),
        ("10/5〜6", "当局がWHOに報告", ("ペストは検出されず", True)),
    ], widths=(250, 720), size=52),
    "e04_vs": table3("報道と発表が食い違う", ("", "現地メディアの報道", "ロシア当局の発表"), [
        ("病名", "肺ペストの可能性", ("原因不明の肺炎", True)),
        ("きっかけ", "試験管を割った？（未確認）", "業務の菌は見つからず"),
        ("接触者", "約200人を隔離", "感染者なし→ほぼ解除"),
    ], widths=(220, 620), size=50),
    "e05_plague": P.bullets("そもそも「ペスト」って？", [
        "細菌（ペスト菌）がおこす感染症",
        "ネズミ → ノミ → 人　とうつる",
        "「肺ペスト」は　せきや飛沫で人から人へ",
        "早めに抗生物質で治療すれば　治る",
    ], size=58),
    "e06_types": glossary("ペストの3つの種類", [
        ("腺ペスト", "リンパ節が腫れる\n（いちばん多い）"),
        ("敗血症ペスト", "血液に菌が回る"),
        ("肺ペスト", "肺に感染する\n人から人へうつる"),
    ]),
    "e07_history": P.bullets("ペストの歴史と今", [
        "14世紀　ヨーロッパで「黒死病」が大流行",
        "人口の3分の1〜半分が亡くなったとされる",
        "今も世界で毎年患者が出ている",
        "（マダガスカル・コンゴ民主共和国・ペルーなど）",
        "日本は1926年を最後に　国内での発生なし",
    ], size=54),
    "e08_why": P.bullets("なんでこんなに騒がれた？", [
        "「研究所」で起きた",
        "「隔離」「病院の封鎖」が報道された",
        "発表が遅く　報道と食い違った",
        "→ コロナの始まりを思い出させた",
    ], size=58),
    "e09_matome": P.bullets("まとめ（10月7日時点）", [
        "○ 28歳の研究所職員が亡くなった",
        "○ 約200人を隔離・観察（その後ほぼ解除）",
        "○ 当局「ペストは検出されず・接触者に感染なし」",
        "？ 本当の死因はまだはっきりしない",
        "？ 試験管の話は確認されていない",
    ], size=52),
    "e10_ending": P.message(["このニュース、どう感じた？", "コメントで教えて！"], size=96),
}


def main():
    os.makedirs(PREV, exist_ok=True)
    for name, img in ITEMS.items():
        img.save(os.path.join(OUT, name + ".png"))
        bg = P.placeholder_bg("背景")
        bg.alpha_composite(img)
        bg.convert("RGB").save(os.path.join(PREV, name + ".jpg"), quality=85)
    files = sorted(f for f in os.listdir(PREV) if f.endswith(".jpg") and f != "_contact.jpg")
    cols, tw, th = 4, 480, 270
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), "white")
    for i, fn in enumerate(files):
        sheet.paste(Image.open(os.path.join(PREV, fn)).resize((tw - 8, th - 8)), ((i % cols) * tw + 4, (i // cols) * th + 4))
    sheet.save(os.path.join(PREV, "_contact.jpg"), quality=85)
    print(f"{len(ITEMS)} parts -> {OUT}")


if __name__ == "__main__":
    main()
