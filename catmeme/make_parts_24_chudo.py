"""24_chudo（議員1人の政党に交付金5.8億円）の解説画面を書き出す。原稿 scripts/24_chudo.md。

python3 catmeme/make_parts_24_chudo.py → catmeme/parts/24_chudo/*.png（＋ preview/）
"""
import os

from PIL import Image

import parts as P
from make_parts_04_leak import glossary, table3

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "24_chudo")
PREV = os.path.join(OUT, "preview")

ITEMS = {
    "e00_notice": P.message(["※発言は報道をもとにした要旨です", "※特定の政党を応援・批判する意図はありません",
                             "※ネットの声は架空の要約です　※猫は演出です",
                             "※今日は自販機で当たりが出ました"], opaque=True, size=58),   # 最後の行は今日の一言
    "e01_title": P.message(["議員1人の政党に交付金5.8億円", "中道改革連合の政党交付金、何が問題？"], sub="2026年10月20日　総務省が交付", size=72),
    "e02_timeline": table3("中道改革連合の1年（報道より）", ("いつ", "できごと", "ポイント"), [
        ("2026年1月", "立憲民主党と公明党が合流", "新党「中道改革連合」"),
        ("2月8日", "衆院選", ("49議席に", True)),
        ("2月", "代表選", "小川淳也氏が代表に"),
        ("9月", "合流が決裂・事実上解体", ("48人が離党", True)),
        ("9月16日", "渡辺創氏が新代表に", ("議員は1人だけ", True)),
        ("10月20日", "政党交付金を受け取る", ("約5億8470万円", True)),
    ], widths=(250, 600), size=44),
    "e03_rules": P.bullets("政党交付金のしくみ（総務省）", [
        "国民1人あたり250円ぶんの税金が、政党に配られる",
        "対象は　国会議員5人以上の政党など",
        "毎年1月1日の時点で、1年分の金額が決まる",
        "4月・7月・10月・12月の年4回に分けて交付",
    ], size=54),
    "e03_split": glossary("ことば", [
        ("分派", "党を解散せずに残し\n議員が外に出ていく形\n（党は1人でも続く）"),
    ]),
    "e04_money": table3("中道改革連合の2026年分の交付金（報道より）", ("いつ", "金額", "ようす"), [
        ("1年分", "約23億3881万円", "1月1日の議員数などで決まった"),
        ("4月・7月", "約11億6940万円", "交付ずみ"),
        ("10月20日", ("約5億8470万円", True), ("議員1人で受け取り", True)),
        ("12月", "約5億8千万円", "交付される見込み"),
    ], widths=(260, 460), size=46),
    "e05_reason": P.bullets("党の説明（小川淳也前代表・9月の報道より）", [
        "衆院選の経費のうち、交付金で払う分は約20億円",
        "民間の業者に、分割で払う契約になっている",
        "支払いは「半分も終わっていない」",
        "後継の新党には、交付金は入らない",
    ], size=54),
    "e06_voices": table3("各党・専門家の声（報道の要旨）", ("だれ", "立場", "言ったこと"), [
        ("民主改革の会", "階猛 幹事長", "負い目はない／批判は甘んじて受ける"),
        ("公明党", "西田 幹事長", "国民の血税。使い道をしっかり示して"),
        ("日本維新の会", "吉村 代表", "1人しか残っていないのに受け取るべきでない"),
        ("与党", "（報道）", "「論理のすり替えだ」との声"),
        ("政治学者", "岩井奉信 氏", "相当、使い道を説明する必要がある"),
    ], widths=(290, 270), size=42),
    "e07_poll": P.bars("中道の交付金受け取りに納得できる？", [("納得できない", 74.0, True, ""), ("それ以外", 26.0, False, "")],
                       note="産経新聞・FNN 世論調査（10月17・18日）", unit="%"),
    "e08_points": P.bullets("今回のポイント", [
        "議員は1人。それでも交付金は約5億8470万円",
        "理由は、衆院選の経費の支払い（党の説明）",
        "使い道の説明と、制度の見直しが求められている",
        "12月分も交付される見込み",
    ], size=52),
    "e10_ending": P.message(["あなたは　納得できる？", "コメントで教えて！"], size=96),
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
