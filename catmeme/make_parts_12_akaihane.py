"""12_akaihane（赤い羽根募金、2.5億円が消えた）の解説画面を書き出す。原稿 scripts/12_akaihane.md（v1）。

python3 catmeme/make_parts_12_akaihane.py → catmeme/parts/12_akaihane/*.png（＋ preview/）
"""
import os

from PIL import Image

import parts as P
from make_parts_04_leak import table3
from make_parts_11_fukiso import nattoku

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "12_akaihane")
PREV = os.path.join(OUT, "preview")

ITEMS = {
    "e00_notice": P.message(["※元事務局長は「着服の疑い」の段階で", "刑事手続きで確定したものではありません",
                             "※金額は北海道共同募金会の発表・報道（2026年10月時点）", "※ネットの声は架空の要約です　※猫は演出です",
                             "※今日は編集中にカップ麺を3回のばしました"],   # 最後の行は今日の一言（指定がないのでこちらで考えた）
                            opaque=True, size=54),
    "e01_title": P.message(["赤い羽根募金、2.5億円が消えた", "善意はどこへ行った？"], sub="2026年　北海道共同募金会の使途不明金", size=96),
    "e02_flow": P.flow("赤い羽根募金　お金の流れ", hsize=56, ssize=46, steps=[
        ("みんなが募金", "街頭・コンビニ\n学校・町内会"),
        ("共同募金会", "都道府県ごとに\n集める"),
        ("地域の福祉へ", "お弁当配り\n見守り\n子ども食堂など"),
    ]),
    "e03_timeline": table3("何が起きたのか（報道より）", ("いつ", "何があった", "ポイント"), [
        ("2010年ごろ", "事務局の男性が　実質1人で会計を担当", "とされる"),
        ("2020年ごろ", "無断で現金を引き出し始めた", "とみられる"),
        ("2022年", "その男性が事務局長に", ""),
        ("2026年2月", "札幌国税局が査察（所得税法違反の疑い）", ("ここで発覚", True)),
        ("2026年6月", "会見で謝罪", "1.8億円以上不足"),
        ("2026年7月", "事務局長（58）を懲戒解雇", ""),
        ("2026年9月", "さらに約7,000万円の不明", ("総額 約2.5億円", True)),
    ], widths=(240, 820), size=44),
    "e04_holes": P.bullets("すり抜けの仕組み（報道より）", [
        "① 通帳も印鑑も　1人で管理",
        "② 足りなくなった分は　年度末に借金して穴埋め",
        "③ 監査は「決算の日の残高」だけ → その日だけ合えば通る",
        "④ 理事会が承認していない議事録で　約1億9,000万円を借りた疑い",
    ], size=50),
    "e05_genba": P.bullets("いま起きていること（報道より）", [
        "今年度の福祉団体への助成金は　予定額の約5割",
        "札幌の街頭ボランティアは　例年の8割減",
        "町内会や企業も　協力を見送るところが続出",
        "置いてくれるお店が見つからず　送れない募金箱も",
    ], size=52),
    "e07_choose": P.bullets("寄付先の選び方（一般論）", [
        "決算や使い道を　公開しているか",
        "お金を扱う人が1人じゃないか（チェックの仕組み）",
        "支援したい団体に　直接寄付する手もある",
        "ふるさと納税・クラファンで　使い道を指定する手もある",
    ], size=54),
    "e09a_known": P.bullets("分かっていること", [
        "北海道共同募金会で　約2億5,000万円が使途不明",
        "会計は事務局長が　1人で管理していた",
        "国税の査察で発覚",
        "元事務局長は懲戒解雇・刑事告訴を検討",
        "今年度の助成金は　予定の約5割",
    ], size=54),
    "e09b_unknown": P.bullets("まだ分かっていないこと", [
        "お金は　どこへ行ったのか",
        "戻ってくるのか",
        "刑事告訴は　するのか",
        "第三者委員会の結論",
    ], size=62),
    "e10_ending": P.message(["あなたは　今年の赤い羽根募金", "する？　しない？", "コメントで教えて！"], size=92),
    "yuruseru": nattoku("これ、許せますか？"),
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
