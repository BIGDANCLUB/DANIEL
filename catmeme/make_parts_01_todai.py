"""01_todai_president（東大総長）の解説画面・字幕枠などを書き出す。

python3 catmeme/make_parts_01_todai.py
→ catmeme/parts/01_todai/*.png（本番用・透過PNG）
→ catmeme/parts/01_todai/preview/*.jpg（仮背景に重ねた確認用）
"""
import os

from PIL import Image

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "01_todai")
PREV = os.path.join(OUT, "preview")

ITEMS = {
    # 共通の枠
    "frame_subtitle": P.subtitle(),
    # 冒頭
    "e00_notice": P.message(["※実在の人物の言葉は、報道をもとにした要旨です", "※猫は再現のための演出です"],
                            opaque=True, size=58),
    "e01_title": P.message(["東大の新しい総長", "投票2位の人が選ばれた件"], sub="2026年9月28日　東京大学"),
    # 2 総長ってだれ？
    "e02_soucho": P.bullets("総長ってだれ？", [
        "大学のいちばん上の人（ふつうは「学長」）",
        "東大では昔から「総長」と呼ぶ",
        "次の総長の任期：2027年4月から6年間",
    ]),
    # 3 候補者
    "e03_candidates": P.bullets("候補者は5人", [
        "大越慎一さん", "菅野暁さん", "染谷隆夫さん", "藤垣裕子さん", "山本隆司さん",
    ], size=54),
    # 4〜5 選び方
    "e04_flow": P.flow("総長の決まり方", [
        ("候補者を\n5人にしぼる", "書類や推薦をもとに"),
        ("学内で投票", "「意向投票」\nあくまで参考"),
        ("16人の会議が\n決める", "総長選考・監察会議\n学外の人も参加"),
    ]),
    "e05_votes": P.bars("意向投票の結果（2回目）", [
        ("染谷隆夫さん", 1107, False, "51.0%"),
        ("藤垣裕子さん", 553, False, "25.5%"),
        ("山本隆司さん", 451, False, "20.8%"),
    ]),
    "e05b_votes_selected": P.bars("意向投票の結果（2回目）", [
        ("染谷隆夫さん", 1107, False, "1位"),
        ("藤垣裕子さん", 553, True, "選ばれた"),
        ("山本隆司さん", 451, False, ""),
    ], note="投票2位の藤垣さんが　次の総長に"),
    "e05c_reveal": P.message(["次の総長は", "藤垣裕子さん"], size=110),
    # 6 藤垣さん
    "e06_profile": P.bullets("藤垣裕子さんってどんな人？", [
        "1962年生まれ",
        "専門：科学技術社会論",
        "＝科学と社会がどう付き合うかの研究",
        "2021年から5年間、東大の副学長",
    ]),
    # 7 選んだ理由
    "e07_reasons": P.bullets("会議が挙げた　選んだ理由", [
        "文系と理系をつなぐ力",
        "大学を外にひらく力",
        "科学を社会にわかりやすく伝える力",
        "学問への信頼を取り戻す力",
        "分断を乗りこえる力",
    ], size=54),
    # 9 世の中の反応
    "e09_reactions": P.flow("ネットの反応は大きく3つ", [
        ("歓迎", "150年で初の\n女性総長"),
        ("投票の意味は？", "過半数の1位を\n選ばないなんて"),
        ("説明が足りない", "1位を選ばなかった\n理由が見えない"),
    ]),
    # 10 ほかの大学
    "e10_kyoto": P.bars("京都大学（2026年夏）", [
        ("1位の候補", 478, False, ""),
        ("2位の候補", 301, False, ""),
        ("立川康人さん", 299, True, "3位→学長に"),
    ], tag="6人中3位", note="立川さんは10月1日に就任"),
    "e10b_tsukuba": P.bars("筑波大学（2020年）", [
        ("対立候補", 951, False, ""),
        ("現職の学長", 584, True, "再任"),
    ], tag="意見を聞く投票", note="同時に　任期の上限と教職員の投票をなくした"),
    "e10c_policy": P.bullets("背景：国の方針", [
        "2014年ごろから見直し",
        "「学長は会議が主体的に選ぶように」",
        "投票の順位どおりにならない例が増えている",
    ]),
    # 11 まとめ・締め
    "e11_matome": P.message(["投票はあくまで参考", "でも1位を選ばないなら　理由の説明がカギ"], size=72),
    "e12_ending": P.message(["あなたはどう思う？", "コメントで教えて！"], size=90),
}

# 名前テロップ（候補者紹介・投票結果の場面で猫の足元に出す）
TAGS = {
    "tag_someya": ("染谷隆夫さん", "候補者"),
    "tag_fujigaki": ("藤垣裕子さん", "候補者・次の総長"),
    "tag_yamamoto": ("山本隆司さん", "候補者"),
    "tag_ookoshi": ("大越慎一さん", "候補者"),
    "tag_kanno": ("菅野暁さん", "候補者"),
    "tag_chair": ("選考会議の議長", "総長選考・監察会議"),
    "tag_tachikawa": ("立川康人さん", "京都大学の新しい学長"),
}


def save(name, img):
    img.save(os.path.join(OUT, name + ".png"))


def preview(name, layers, label):
    bg = P.placeholder_bg(label)
    for ly in layers:
        bg.alpha_composite(ly)
    bg.convert("RGB").save(os.path.join(PREV, name + ".jpg"), quality=85)


def main():
    os.makedirs(PREV, exist_ok=True)
    for name, img in ITEMS.items():
        save(name, img)
    for name, (n, s) in TAGS.items():
        save(name, P.name_tag(n, s))

    # 確認用：解説カード＋右下の小さい猫＋字幕
    for name, img in ITEMS.items():
        if name in ("frame_subtitle", "e00_notice"):
            continue
        layers = [img]
        if name.startswith("e") and name not in ("e01_title", "e05c_reveal", "e11_matome", "e12_ending"):
            cat = P.canvas()
            P.placeholder_cat(cat, P.CAT_SLOT, "小さい猫")
            layers.insert(0, cat)
        preview(name, layers, "黒板など")
    preview("e00_notice", [ITEMS["e00_notice"]], "")

    # 確認用：会話シーン（猫＋吹き出し＋字幕）
    cat = P.canvas()
    P.placeholder_cat(cat, (760, 430, 1160, 1000), "ニュース猫")
    preview("scene_news_cat", [cat, P.bubble("2位の倍よ倍！ はい優勝！ 解散！", name="ニュース猫", cat_x=960, top=180),
                               P.subtitle("1位　染谷隆夫さん　1,107票（51.0%）")], "リビング bg02")
    cat = P.canvas()
    P.placeholder_cat(cat, (1150, 430, 1550, 1000), "藤垣さん猫")
    preview("scene_fujigaki", [cat, P.bubble("ようやく初の女性ってことで、\nこれはかなりメッセージ性あると思うんですよね",
                                             name="藤垣さん（再現）", cat_x=1350, top=120, color=P.NAVY),
                               P.subtitle("翌29日　藤垣さんが会見")], "会見場 bg07")
    cat = P.canvas()
    P.placeholder_cat(cat, (760, 300, 1160, 690), "染谷さん猫")
    preview("scene_nametag", [cat, P.name_tag("染谷隆夫さん", "候補者", y=700),
                              P.subtitle("1位　染谷隆夫さん　1,107票（51.0%）")], "キャンパス bg01")

    # 一覧
    files = sorted(f for f in os.listdir(PREV) if f.endswith(".jpg") and f != "_contact.jpg")
    cols, tw, th = 4, 480, 270
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), "white")
    for i, fn in enumerate(files):
        im = Image.open(os.path.join(PREV, fn)).resize((tw - 8, th - 8))
        sheet.paste(im, ((i % cols) * tw + 4, (i // cols) * th + 4))
    sheet.save(os.path.join(PREV, "_contact.jpg"), quality=85)
    print(f"{len(ITEMS) + len(TAGS)} parts, {len(files)} previews -> {OUT}")


if __name__ == "__main__":
    main()
