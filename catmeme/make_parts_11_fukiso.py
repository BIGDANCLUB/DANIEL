"""11_fukiso（2,000万円の車を盗んだ疑いでも不起訴）の解説画面を書き出す。原稿 scripts/11_fukiso.md（v2）。

python3 catmeme/make_parts_11_fukiso.py → catmeme/parts/11_fukiso/*.png（＋ preview/）
"""
import os

from PIL import Image, ImageDraw

import parts as P
from make_parts_04_leak import glossary, table3

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "11_fukiso")
PREV = os.path.join(OUT, "preview")


def nattoku(text="これ、納得できますか？"):
    """章の終わりの問いかけ（黒地に大きな赤い文字）。"""
    img = Image.new("RGBA", (P.W, P.H), (0, 0, 0, 255))
    im = P.big_text(text, (80, 300, P.W - 80, 780), max_size=170, max_lines=2, fill=P.RED_TEXT, stroke=P.WHITE)
    img.alpha_composite(im)
    return img


def wall23():
    """23日の壁：逮捕 → 勾留 → 延長。"""
    img, d, (bx0, by0, bx1, by1) = P.card("「23日の壁」")
    steps = [("逮捕", "最大3日"), ("勾留", "10日"), ("延長", "10日")]
    n, gap = len(steps), 80
    bw = (bx1 - bx0 - 340 - 90 - gap * (n - 1)) / n
    hf, sf = P.font("round", 64), P.font("round_b", 50)
    cy = (by0 + by1) / 2 - 40
    for i, (h, s) in enumerate(steps):
        x0 = bx0 + i * (bw + gap)
        d.rounded_rectangle((x0, cy - 130, x0 + bw, cy + 130), 26, fill=P.WHITE, outline=P.NAVY, width=6)
        d.text((x0 + bw / 2, cy - 40), h, font=hf, fill=P.INK, anchor="mm")
        d.text((x0 + bw / 2, cy + 50), s, font=sf, fill=P.MUTED, anchor="mm")
        if i < n - 1:
            ax = x0 + bw + 14
            d.polygon([(ax, cy - 28), (ax + gap - 28, cy), (ax, cy + 28)], fill=P.NAVY)
    rx = bx1 - 340
    d.text((rx - 45, cy), "＝", font=P.font("round", 80), fill=P.ACCENT, anchor="mm")
    d.rounded_rectangle((rx, cy - 130, bx1, cy + 130), 26, fill=P.ACCENT)
    d.text((rx + 170, cy - 40), "最大", font=P.font("round_b", 50), fill=P.WHITE, anchor="mm")
    d.text((rx + 170, cy + 45), "23日", font=P.font("round", 96), fill=P.WHITE, anchor="mm")
    d.text(((bx0 + bx1) / 2, by1 - 40), "この間に「起訴」か「釈放」かを決めないといけない", font=P.font("round_b", 50), fill=P.INK,
           anchor="mm")
    return img


ITEMS = {
    "e00_notice": P.message(["※「不起訴」になった人は、法律上は罪に問われていません", "※国籍で人をひとくくりにする意図はありません",
                             "※ネットの声は架空の要約です　※猫は演出です"], opaque=True, size=62),
    "e01_title": P.message(["2,000万円の車を盗んだ疑いでも不起訴…", "日本はナメられているのか"],
                           sub="2026年10月　仙台・横浜で続いた「不起訴」", size=86),
    "e02_sendai": table3("仙台の件（報道より）", ("いつ", "何があった", "ポイント"), [
        ("2025年9月", "名取市の住宅で高級SUV盗難", ("時価約2,000万円", True)),
        ("その後", "ブラジル国籍の男性（28）逮捕", "ほか2件とあわせ3件で送検"),
        ("2026/10/7", "仙台地検が判断", ("不起訴", True)),
    ], widths=(250, 700), size=46),
    "e03_yokohama": table3("横浜の件（報道より）", ("いつ", "何があった", "ポイント"), [
        ("2026年9月", "横浜オクトーバーフェスト", "警備員が顔を殴られる"),
        ("その後", "アメリカ国籍の男性（27）逮捕", "酔って殴るなどした疑い"),
        ("2026/10/9", "横浜地検が判断", ("不起訴", True)),
    ], widths=(250, 700), size=46),
    "e04_kensin": glossary("ことば", [
        ("検察審査会", "くじで選ばれた市民が\n「その不起訴はおかしくないか」\nを審査する仕組み"),
    ]),
    "e06_reasons": P.bullets("怒りが収まらない理由", [
        "① 逮捕は速報。不起訴は小さく、いつの間にか終わってる",
        "② 不起訴の理由が　ほぼ説明されない",
        "③ 同じような事件が　何度も繰り返されているように見える",
        "④ 「国に帰ってしまえば終わり」と言われている",
        "⑤ 「日本の刑罰は軽い」と海外で思われている、と言われている",
    ], size=50),
    "e06_types": glossary("不起訴の主な3つ", [
        ("嫌疑なし", "やっていないと分かった"),
        ("嫌疑不十分", "あやしいけど　有罪にできる\nだけの証拠がない"),
        ("起訴猶予", "やったことは認められるが\n事情（示談・反省など）で見送る"),
    ]),
    "e07_23days": wall23(),
    "e08_stats": P.bullets("犯罪白書（法務省・令和7年版）", [
        "2024年　来日外国人の事件の起訴率は",
        "日本人を含む全体より　刑法犯で2.8ポイント高い",
        "（特別法犯でも1.0ポイント高い）",
        "→ 全体の数字では　起訴されていないわけではない",
    ], size=54),
    "e10_cases": P.bullets("今回の事件", [
        "10/7 仙台：高級車3件で逮捕・送検 → 不起訴",
        "　　（「証拠が集まらなかった」）",
        "10/9 横浜：警備員を殴った疑い → 不起訴",
        "　　（くわしい理由は非公表）",
    ], size=56),
    "e10_anger": P.bullets("怒りの正体", [
        "不起訴の理由が　説明されない",
        "被害者が　置き去りにされる",
        "23日で時間切れ、と言われている",
    ], size=64),
    "e11_ending": P.message(["あなたは　この不起訴に", "納得できますか？", "コメントで教えて！"], size=92),
    "nattoku": nattoku(),
    "nattoku_last": nattoku("あなたは　この不起訴に\n納得できますか？"),
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
