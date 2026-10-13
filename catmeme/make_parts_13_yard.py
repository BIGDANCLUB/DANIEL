"""13_yard（盗難ハイエース300台、塀の中で解体され海外へ）の解説画面を書き出す。原稿 scripts/13_yard.md（v1）。

python3 catmeme/make_parts_13_yard.py → catmeme/parts/13_yard/*.png（＋ preview/）
"""
import os

from PIL import Image

import parts as P
from make_parts_04_leak import glossary, table3
from make_parts_11_fukiso import nattoku

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "13_yard")
PREV = os.path.join(OUT, "preview")

ITEMS = {
    "e00_notice": P.message(["※逮捕された人は容疑の段階で、有罪が確定したものではありません", "※国籍で人をひとくくりにする意図はありません",
                             "※ネットの声は架空の要約です　※猫は演出です",
                             "※今日は駐車場でハンドルロックを3回確認しました"], opaque=True, size=56),   # 最後の行は今日の一言
    "e01_title": P.message(["盗難ハイエース300台、塀の中で解体され海外へ", "日本は“盗難天国”なのか"], sub="2026年　茨城県のヤードで4人逮捕", size=74),
    "e01_quote": P.message(["窃盗団には「自動車窃盗は", "大した罪にならない」という", "意識があるのではないか"], sub="自動車の取材を続けるジャーナリスト（報道より）", size=86),
    "e02_roles": table3("役割分担（警察の見立て）", ("役割", "だれ", "ポイント"), [
        ("盗む", "日本人の男2人（42・41歳）", "とされる"),
        ("受け取り・解体", "ヤードの経営者（ウガンダ国籍）", "茨城県鉾田市"),
        ("", "従業員（ナイジェリア国籍）", ""),
        ("輸出", "部品などにして海外へ", ("中東などと言われる", True)),
    ], widths=(290, 700), size=48),
    "e03_yard": glossary("ことば", [
        ("ヤード", "高い鉄の塀で囲まれた\n自動車の解体・部品の保管\nコンテナ詰めをする作業場"),
    ]),
    "e04_numbers": P.bullets("数字で見る自動車盗難（2025年）", [
        "自動車盗難（警察が把握した件数）　6,386件",
        "いちばん盗まれた車種　ランドクルーザー 1,177台",
        "盗難1件あたりの保険金の平均　約297.5万円",
        "（警察庁・日本損害保険協会）",
    ], size=56),
    "e05_reasons": P.bullets("ナメられていると言われる5つの理由", [
        "① 「盗難車だと知っていた」の証明が難しい",
        "② 証明できたのは“1台”。300台は「とみられる」",
        "③ ヤードを取り締まる国の法律がない（県の条例だけ）",
        "④ 塀の中は見えない。踏み込むには証拠と令状",
        "⑤ 盗まれた人が　自分で車を探すことも多い",
    ], size=52),
    "e05_jorei": P.bullets("ヤード条例", [
        "2016年　千葉県が全国で初めて",
        "その後　茨城・埼玉・群馬・愛知などに広がる",
        "届け出・相手の身元確認・取引記録・盗難車の申告",
        "茨城県で違反すると　3か月以下の拘禁刑",
        "または　30万円以下の罰金",
    ], size=54),
    "e07_protect": P.bullets("盗難対策（一般的な方法）", [
        "ハンドルロック・タイヤロックで「面倒な車」に",
        "純正だけに頼らず　後付けの盗難防止装置",
        "防犯カメラ・センサーライト",
        "GPS追跡装置",
        "車両保険の補償を確認",
    ], size=54),
    "e09a_case": P.bullets("今回の事件", [
        "2026年6月　4県警が4人を逮捕（容疑の段階）",
        "盗む・受け取って解体・輸出の分業とみられる",
        "関東一円の300台以上に関わったとみられる",
        "起訴の報道は　まだない",
    ], size=56),
    "e09b_reasons": P.bullets("ナメられていると言われる理由", [
        "「知らなかった」の壁",
        "ヤードを取り締まる国の法律がない",
        "塀の中が見えない",
        "盗まれた側が探す",
    ], size=64),
    "e10_ending": P.message(["あなたの車は　大丈夫？", "コメントで教えて！"], size=96),
    "nattoku": nattoku(),
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
