"""20_sagi（「郵便局です」から始まる特殊詐欺、1日10億円）の解説画面を書き出す。原稿 scripts/draft_sagi.md（v1）。

python3 catmeme/make_parts_20_sagi.py → catmeme/parts/20_sagi/*.png（＋ preview/）
被害を公表した YouTuber のチャンネル名は出さない（動画のタイトルだけ）。
"""
import os

from PIL import Image, ImageDraw

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "20_sagi")
PREV = os.path.join(OUT, "preview")


def titles(title, items):
    """YouTube の動画タイトルを3つ並べる（チャンネル名は出さない）。"""
    img, d, (bx0, by0, bx1, by1) = P.card(title, tag="10月18日")
    step = (by1 - by0) / len(items)
    for i, t in enumerate(items):
        y0 = by0 + step * i + 14
        y1 = by0 + step * (i + 1) - 14
        d.rounded_rectangle((bx0, y0, bx1, y1), 22, fill=P.WHITE, outline=(200, 200, 200), width=3)
        d.rounded_rectangle((bx0 + 24, y0 + 24, bx0 + 220, y1 - 24), 14, fill=(60, 60, 60))   # サムネのかわり
        d.polygon([(bx0 + 102, (y0 + y1) / 2 - 26), (bx0 + 102, (y0 + y1) / 2 + 26), (bx0 + 148, (y0 + y1) / 2)], fill=P.WHITE)
        f = P.font("round", 52)
        while d.textlength(t, font=f) > bx1 - bx0 - 300 and f.size > 32:
            f = P.font("round", f.size - 2)
        d.text((bx0 + 260, (y0 + y1) / 2), t, font=f, fill=P.INK, anchor="lm")
    return img


ITEMS = {
    "e00_notice": P.message(["※被害に遭われた方を責める意図はありません", "※手口は警察の注意喚起をもとにした再現です", "※ネットの声は架空の要約です　※猫は演出です",
                             "※今日は実家に電話しました"], opaque=True, size=58),   # 最後の行は今日の一言
    "e01_titles": titles("動画のタイトル", ["「特殊詐欺に遭い、財産のほぼ全てを失いました」", "「郵便局だと思って対応したら特殊詐欺でした」",
                                       "「特殊詐欺被害に遭いました」"]),
    "e01_title": P.message(["人気YouTuberも次々被害", "「郵便局です」から始まる特殊詐欺、1日10億円"], sub="2026年10月", size=74),
    "e02_stats": P.bullets("特殊詐欺（警察庁・2026年1〜6月）", [
        "被害額　1,816億円（上半期として過去最悪）",
        "1日あたり　約10億円",
        "件数　2万2,031件（前年より18.3％増）",
        "いちばん多い手口　SNS型投資詐欺　797億9,000万円",
        "2番目　ニセ警察詐欺　507億9,000万円（被害は70代が最多）",
    ], size=52),
    "e04_trick": P.bullets("だまされる仕組み", [
        "① 名乗るのが「郵便局」「警察」など“信用できる所”",
        "② 「逮捕」「犯罪」で　パニックにさせる",
        "③ 「誰にも言わないで」と　家族や友だちに相談させない",
        "④ ビデオ通話で“本物っぽい”制服や部屋を見せる",
        "⑤ 「お金を守るため」と言う　→　だまされている感覚がない",
    ], size=50),
    "e05_points": P.bullets("これが来たら詐欺（警察の注意喚起より）", [
        "① 郵便局は　自動音声で個人情報を聞かない／番号を押させない",
        "② 警察は　電話やSNS・ビデオ通話で取り調べをしない",
        "③ 警察は　捜査のために「お金を移せ」「振り込め」と言わない",
        "④ 「+1」など　知らない国際電話は出ない（止める手続きもある）",
        "⑤ 迷ったら　いったん切って　家族か「#9110」（警察の相談電話）へ",
    ], size=48),
    "e06_parents": P.bullets("親にやってほしいこと", [
        "固定電話を“留守番電話”にしておく",
        "「郵便局」「警察」から電話が来たら、まず家族に連絡",
        "国際電話を止める手続きをしておく",
        "「誰にも言わないで」と言われたら、それが詐欺の合図",
    ], size=54),
    "e08_todo": P.bullets("今日からやること", [
        "① 「郵便局」「警察」の電話でも　いったん切る",
        "② 「お金を移して」は　100％詐欺",
        "③ 実家に電話して　この動画の話をする",
    ], size=62),
    "e10_ending": P.message(["あなたの家に　怪しい電話、", "来たことある？　コメントで教えて！"], size=86),
}


def reenact_tag():
    """〔再現〕の場面の右上に出す札。"""
    img = Image.new("RGBA", (P.W, P.H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = P.font("round", 40)
    t = "※警察の注意喚起をもとにした再現"
    w = d.textlength(t, font=f)
    box = (P.W - w - 80, 24, P.W - 24, 92)
    d.rounded_rectangle(box, 16, fill=(20, 20, 20, 220), outline=(255, 210, 0, 255), width=3)
    d.text((box[0] + 28, 58), t, font=f, fill=(255, 230, 0), anchor="lm")
    return img


ITEMS["tag_reenact"] = reenact_tag()


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
