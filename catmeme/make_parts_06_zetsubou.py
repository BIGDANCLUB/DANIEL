"""06_zetsubou（「絶望ライン工」の結婚炎上）の解説画面を書き出す。

python3 catmeme/make_parts_06_zetsubou.py → catmeme/parts/06_zetsubou/*.png（＋ preview/）
"""
import os

from PIL import Image

import parts as P
from make_parts_04_leak import glossary, table3

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "06_zetsubou")
PREV = os.path.join(OUT, "preview")

ITEMS = {
    "e00_notice": P.message(["※実在の人物の言葉は、報道・本人の動画をもとにした要旨です", "※ご家族を批判・詮索する動画ではありません",
                             "※猫は演出です"], opaque=True, size=62),
    "e01_title": P.message(["「年収240万・独身」の人気YouTuber", "実は結婚していた件"], sub="2026年9〜10月　「絶望ライン工」の炎上と活動休止",
                           size=96),
    "e02_channel": P.bullets("どんなチャンネルだった？", [
        "工場勤務・寮暮らし",
        "柴犬との暮らし・婚活",
        "給与明細の公開",
        "「質素な独身の暮らし」を発信",
        "登録者　約68万人",
    ], size=58),
    "e03_works": table3("“独身”を売りにした作品も", ("いつ", "作品", "ポイント"), [
        ("2026年1月", "書籍『独身獄中記』", "「刊行時43歳独身」"),
        ("連載", "ダ・ヴィンチWeb", ""),
        ("8月31日", "アルバム『独身漂流記』", ("結婚報告の約1か月前", True)),
    ], widths=(260, 650), size=50),
    "e04_timeline": table3("炎上までの流れ", ("いつ", "出来事", ""), [
        ("9/17", "ショート「年収240万円『質素な暮らし』」", ""),
        ("9/24", "「43歳独身の休日」", ""),
        ("9/28", "結婚と子どもの誕生を報告", ("4日後", True)),
        ("10/5", "説明動画・活動休止を発表", ""),
    ], widths=(180, 900), size=48),
    "e05_anger": glossary("怒りのポイントはどこ？", [
        ("結婚したこと", "× ここではない"),
        ("独身を売り続けた", "本・アルバム・動画を\n出し続けたこと"),
        ("コメント欄", "閉じたことで\n批判がさらに広がった"),
    ]),
    "e06_subs": P.bars("登録者の数（報道）", [
        ("炎上前", 68.4, False, ""),
        ("10/7時点", 67.3, True, "約1.1万人減"),
    ], unit="万人", note="思ったほど減っていない、という見方も"),
    "e07_reactions": glossary("ネットの反応は大きく3つ", [
        ("批判", "今の看板は下ろさないと\n違和感がある"),
        ("擁護", "あなたが幸せなら\nそれでいい"),
        ("考察", "余裕のない社会の\n反映では"),
    ]),
    "e08_setting": P.bullets("“設定”を売るチャンネルのむずかしさ", [
        "キャラ（設定）が　人気の理由になる",
        "現実が変わったとき　設定をどう畳むか",
        "説明が遅れるほど「隠していた」に見える",
        "家族を守る事情との　両立もむずかしい",
    ], size=54),
    "e09_matome": P.bullets("まとめ", [
        "結婚・出産を伏せたまま“独身”の動画を出していた",
        "怒りの中心は「独身を売り続けた」「コメント欄を閉じた」",
        "本人は「嘘をついていた」と認め　活動休止",
        "家族を守るためだった、という説明もあった",
    ], size=50),
    "e10_ending": P.message(["あなたは許せる？　許せない？", "コメントで教えて！"], size=92),
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
