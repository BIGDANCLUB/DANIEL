"""10_idcf（IDCFクラウドのランサムウェア攻撃）の解説画面を書き出す。原稿 scripts/10_idcf.md（v2）。

python3 catmeme/make_parts_10_idcf.py → catmeme/parts/10_idcf/*.png（＋ preview/）
攻撃者のメッセージ画像はそのまま使わず、要旨を「画面ふうのカード」で再現する（原稿のルール）。
"""
import os

from PIL import Image, ImageDraw

import parts as P
from make_parts_04_leak import glossary, table3

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "10_idcf")
PREV = os.path.join(OUT, "preview")
GREEN = (90, 255, 120)


def screen(lines, tag="ハッカーの主張（要旨を再現）", big=0):
    """黒い画面ふうのカード。lines[:big] は大きな緑の文字、残りは白い訳・説明。"""
    img = P.canvas()
    d = ImageDraw.Draw(img)
    box = (150, 70, 1770, 880)
    P.shadow(img, box, 30, offset=12, alpha=90)
    d.rounded_rectangle(box, 30, fill=(12, 14, 16, 245), outline=(70, 75, 80), width=6)
    d.rectangle((box[0] + 3, box[1] + 3, box[2] - 3, box[1] + 70), fill=(45, 48, 52))
    for k, col in enumerate(((235, 90, 80), (240, 190, 60), (90, 200, 90))):
        d.ellipse((box[0] + 40 + k * 50, box[1] + 22, box[0] + 70 + k * 50, box[1] + 52), fill=col)
    tf = P.font("round_b", 36)
    d.text((box[2] - 40, box[1] + 37), tag, font=tf, fill=(255, 210, 90), anchor="rm")
    top, bottom = box[1] + 110, box[3] - 50
    sizes = [118 if i < big else 66 for i in range(len(lines))]
    total = sum(s * 1.45 for s in sizes)
    y = top + (bottom - top - total) / 2
    for i, (ln, s) in enumerate(zip(lines, sizes)):
        f = P.font("black" if i < big else "round_b", s)
        while d.textlength(ln, font=f) > box[2] - box[0] - 140 and f.size > 30:
            f = P.font("black" if i < big else "round_b", f.size - 2)
        d.text((960, y + s * 0.72), ln, font=f, fill=GREEN if i < big else P.WHITE, anchor="mm")
        y += s * 1.45
    return img


SHOT = os.path.join(OUT, "src", "hacker_message.png")


def shot(box, mark=None):
    """実際のメッセージ画像（SNSで広まったもの）の一部を切り出す。
    侵入の手順にあたる下の部分（コマンド・ファイルの場所）は使わない（y=875 より下は切る）。mark=(x0,y0,x1,y1) は赤い枠で囲む所。"""
    im = Image.open(SHOT).convert("RGBA")
    x0, y0, x1, y1 = box
    im = im.crop((x0, y0, x1, min(y1, 875)))
    d = ImageDraw.Draw(im)
    if mark:
        m = (mark[0] - x0, mark[1] - y0, mark[2] - x0, mark[3] - y0)
        d.rounded_rectangle(m, 12, outline=(255, 220, 0), width=6)
    k = 1600 / im.width
    im = im.resize((1600, int(im.height * k)), Image.LANCZOS)
    out = Image.new("RGBA", (im.width + 16, im.height + 76), (60, 60, 60, 255))
    out.paste(im, (8, 68))
    d = ImageDraw.Draw(out)
    d.text((24, 34), "実際に表示されたメッセージ（SNSで拡散・IDCFも同様の画像を確認）　※侵入の手順にあたる部分は隠しています",
           font=P.font("round_b", 30), fill=(255, 220, 0), anchor="lm")
    return out


def badge(text="※ハッカーの主張・言われていることをもとにした再現"):
    """再現パートの間ずっと出す、画面左上の札。"""
    img = P.canvas()
    d = ImageDraw.Draw(img)
    f = P.font("round_b", 38)
    w = d.textlength(text, font=f)
    d.rounded_rectangle((26, 24, 26 + w + 44, 24 + 66), 14, fill=(20, 20, 20, 225), outline=(255, 210, 90), width=4)
    d.text((48, 57), text, font=f, fill=(255, 210, 90), anchor="lm")
    return img


ITEMS = {
    "e00_notice": P.message(["※ハッカーの主張や、ネットで言われていることは", "確認されていないものを含みます",
                             "※会社の発表は2026年10月11日時点のものです", "※再現パートは演出です　※猫は演出です"],
                            opaque=True, size=60),
    "e01_title": P.message(["ハッカーに「7時間気づいてない」と", "煽られたクラウド"],
                           sub="2026年10月　IDCFクラウドのランサムウェア攻撃", size=96),
    "e01_msg": screen(["YOUR CLOUD IS OURS.", "（お前たちのクラウドは　われわれのものだ）"], tag="管理画面のメッセージ（要旨を再現）", big=1),
    "e01_claim": screen(["「お前たちは7時間たっても", "オレのメッセージに", "気づいていない」"]),
    "e02_mansion": glossary("たとえるなら", [
        ("クラウド", "大きなマンション"),
        ("企業・自治体", "部屋を借りている住人"),
        ("今回の攻撃", "管理室ごと乗っ取られ\n部屋にカギをかけられた"),
    ]),
    "e02_affected": P.bullets("影響の例（公表・報道より）", [
        "茨城県・栃木県・小平市・多賀城市のホームページ",
        "ニッスイの物流（17拠点）",
        "NTTドコモ「あんしんフィルター」",
        "京都サンガF.C.／SKE48のファン向けメール",
        "音声認識アプリ「UDトーク」　など",
    ], tag="495の企業・自治体", size=54),
    "e03_tl1": table3("10月7日に何が起きたか（公表された順）", ("時刻", "だれが", "何があった"), [
        ("3:40ごろ", "IDCF", "東日本リージョン1で障害が発生"),
        ("4:50ごろ", "物流会社", "システム障害を確認"),
        ("7:54", "Jリーグのクラブ", "障害を公表"),
        ("8:00ごろ", "茨城県", "「電源が落ちた」と連絡"),
        ("10:22", "茨城県", "「県のホームページが見られません」"),
        ("13:52", "IDCF 第1報", "第三者による不正アクセス"),
        ("20:18", "IDCF 第2報", ("ランサムウェア攻撃", True)),
    ], widths=(260, 420), size=44),
    "e03_ransom": glossary("ことば", [
        ("ランサムウェア", "データに勝手にカギ（暗号）をかけて\n使えなくし「戻してほしければ\n金を払え」と迫るウイルス"),
    ]),
    "e03_tl2": table3("10月8日からの発表", ("日付", "発表", "内容"), [
        ("10/8", "第3報", ("止まった仮想サーバーは再起動できない", True)),
        ("10/8", "第3報", ("4ゾーンのデータは取り出し・復元が困難", True)),
        ("10/8", "第3報", "復元は お客さま自身のバックアップからのみ"),
        ("10/8", "第3報", "警視庁・監督省庁に報告　外部の会社と調査"),
        ("10/9", "第4報", "親会社のソフトバンクと連携して対応"),
    ], widths=(200, 230), size=46),
    "e04_claims": P.bullets("ハッカーが主張する被害", [
        "東日本リージョン1を　たった7分で暗号化",
        "仮想マシンの土台　239台に到達",
        "データの保管庫　225個を暗号化",
        "仮想マシンのディスク　1万6,600超",
        "ストレージ3.6ペタバイト／復元用の記録55万件超",
        "バックアップ41.5ペタバイト分を失わせた",
    ], tag="確認されていない・IDCFは調査中", size=52),
    "e05_claim2": screen(["「仮想マシンをいじってるのに", "まだオレのメッセージを", "見つけていない」", "「ファイルの中の時計は　本物だぞ」"]),
    "e06_meian": P.bullets("バックアップで明暗が分かれた（報道より）", [
        "別のクラウドにバックアップあり → そこから作り直し中",
        "「データの復元は難しい」→ 別の場所で一から作り直し",
        "ホームページが戻った自治体も",
    ], size=54),
    "e06_basic": P.bullets("バックアップの基本（一般論）", [
        "コピーを　複数つくる",
        "ちがう場所に　置く",
        "1つは　書き換えられない形で",
    ], size=66),
    "e07_jr": table3("JR東日本グループの発表（10/9・最大の件数）", ("サービス", "件数", "対象の情報"), [
        ("えきねっと", ("約167万件", True), "メールアドレス"),
        ("大人の休日倶楽部", ("約39万件", True), "メール・会員番号など"),
        ("ビューカード", ("約403万件", True), "メールアドレス（VIEW's NET）"),
        ("合計", ("最大 約609万件", True), "カード番号などは含まれない"),
    ], widths=(380, 330), size=44),
    "e09a_known": P.bullets("分かっていること（公式の発表）", [
        "10/7 午前3時40分ごろ　障害が発生",
        "原因は　ランサムウェア攻撃",
        "495の企業・自治体に影響",
        "仮想サーバーは　再起動できない",
        "データは　自分のバックアップからしか戻せない",
    ], size=56),
    "e09b_claims": P.bullets("ハッカーの主張・言われていること", [
        "7分で暗号化した（ハッカーの主張）",
        "225個のメッセージを置いた（ハッカーの主張）",
        "7時間気づかなかった（ハッカーの主張）",
        "ひたすら再起動していた（と言われている）",
    ], size=56),
    "e09c_unknown": P.bullets("まだ分かっていないこと", [
        "どこから入られたのか（侵入経路）",
        "情報は外に漏れたのか",
        "犯人はだれか",
    ], size=64),
    "e10_ending": P.message(["あなたの会社は　大丈夫？", "コメントで教えて！"], size=96),
    "badge": badge(),
    "r0_full": shot((0, 0, 1330, 875)),
    "r1_top": shot((0, 30, 1330, 445), mark=(20, 235, 520, 280)),
    "r2_stats": shot((0, 280, 1330, 710), mark=(20, 465, 1245, 705)),
    "r3_noc": shot((0, 560, 1330, 875), mark=(20, 730, 1245, 870)),
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
