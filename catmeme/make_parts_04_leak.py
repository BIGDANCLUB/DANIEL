"""04_leak（個人情報、盗まれすぎ問題）の解説画面を書き出す。

python3 catmeme/make_parts_04_leak.py → catmeme/parts/04_leak/*.png（＋ preview/）
"""
import os

from PIL import Image

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "04_leak")
PREV = os.path.join(OUT, "preview")


def table3(title, head, rows, widths=(240, 620), tag="", size=48):
    """3列の表。head=(列1,列2,列3)、rows=[(…)]。3列目の重要な行は (文字, True) で赤く。"""
    img, d, (bx0, by0, bx1, by1) = P.card(title, tag)
    hf, cf = P.font("round", size + 4), P.font("round_b", size)
    w0, w1 = widths
    col_w = [w0, w1, (bx1 - bx0) - w0 - w1]
    xs = [bx0, bx0 + w0, bx0 + w0 + w1]
    row_h = (by1 - by0) / (len(rows) + 1)
    for j, h in enumerate(head):
        x0 = xs[j] + 6
        d.rounded_rectangle((x0, by0, x0 + col_w[j] - 12, by0 + row_h - 10), 16, fill=P.NAVY)
        d.text((x0 + (col_w[j] - 12) / 2, by0 + (row_h - 10) / 2), h, font=hf, fill=P.WHITE, anchor="mm")
    for i, r in enumerate(rows):
        y = by0 + row_h * (i + 1)
        d.line((bx0, y, bx1, y), fill=P.NEUTRAL, width=2)
        for j, cell in enumerate(r):
            hi = isinstance(cell, tuple) and cell[1]
            text = cell[0] if isinstance(cell, tuple) else cell
            f = cf
            while d.textlength(text, font=f) > col_w[j] - 20 and f.size > 26:
                f = P.font("round_b", f.size - 2)
            d.text((xs[j] + 14, y + row_h / 2), text, font=f, fill=P.ACCENT if hi else P.INK, anchor="lm")
    return img


ITEMS = {
    "e00_notice": P.message(["※件数は各社の発表どおりです", "（「漏えいのおそれ」を含みます）",
                             "※被害を受けた会社を責める動画ではありません", "※猫は演出です"], opaque=True, size=72),
    "e01_title": P.message(["個人情報、", "盗まれすぎ問題"], sub="2026年9月末〜10月の連続漏えいを解説", size=120),
    "e02_list": table3("9月末から　ほぼ毎日…（1）", ("発表", "どこ", "件数（おそれ含む）"), [
        ("10/5", "焼肉きんぐ", ("約1,078万件", True)),
        ("10/1", "佐川急便", "約100日分の宛先"),
        ("9/29", "セイコーマート", "約57万件"),
        ("9/28", "タイムズカー", ("約660万件", True)),
    ], widths=(200, 560), size=58),
    "e02b_list": table3("9月末から　ほぼ毎日…（2）", ("発表", "どこ", "件数（おそれ含む）"), [
        ("9/27", "OZmall", "最大約44万件"),
        ("9/25", "Gyazo", ("約2,362万件", True)),
        ("9/15", "ムラウチドットコム", "約771万件"),
        ("9/11", "デジタル庁", "約24.6万件"),
    ], widths=(200, 560), size=58),
    "e02c_times": P.bullets("タイムズカーの件（9/28発表）", [
        "不正アクセスで　約660万件が漏えいのおそれ",
        "名前・住所・生年月日・電話・メール",
        "うち約160万件は　運転免許証などの本人確認書類",
        "※レンタカー・カーシェアは　登録時に免許証の確認が必要",
    ], size=56),
    "e03_cause": P.bars("9月に原因まで公表された10件", [
        ("機器やシステムの弱点", 6, True, "いちばん多い"),
        ("設定の不備", 1, False, ""),
        ("フィッシング", 1, False, ""),
        ("人のうっかり", 2, False, "誤送付・誤入力"),
    ], unit="件", note="※うっかりの例はほかにも（紙の紛失・8年間の誤掲載など）"),
    "e03b_words": P.flow("ことばの意味（たとえ）", [
        ("VPN", "社員用の\n通用口"),
        ("脆弱性", "壊れた\n裏口の鍵"),
        ("ランサム\nウェア", "データを人質に\n身代金"),
    ], hsize=58, ssize=46),
    "e04_ransom": P.bars("ランサムウェアの被害（上半期・警察庁）", [
        ("2022年", 114, False, ""),
        ("2023年", 103, False, ""),
        ("2024年", 114, False, ""),
        ("2025年", 116, False, ""),
        ("2026年", 123, True, "半期として最多"),
    ], unit="件", note="侵入口の約5割は　VPN機器"),
    "e04b_big": P.bars("上場企業の漏えい（東京商工リサーチ）", [
        ("100万人超の大型（前の年）", 2, False, ""),
        ("100万人超の大型（2025年）", 6, True, "3倍"),
    ], unit="件", note="件数全体は2025年に減った。でも大型が増えた"),
    "e05_risk": P.flow("盗まれると　この先どうなる？", [
        ("名前・電話\nメール", "本物っぽい\n偽SMS・偽メール"),
        ("送り主\n届け先", "荷物を頼んだ人を\nねらう詐欺"),
        ("免許証の\n画像", "なりすまし\n（口座・契約）"),
    ], hsize=52, ssize=44),
    "e05b_license": P.flow("免許証の画像が悪用されると…（最悪のケース）", [
        ("なりすまし", "名前を使って\nクレカ作成"),
        ("勝手に借金", "知らぬ間に\nキャッシング"),
        ("信用に傷", "延滞の記録\n＝ブラック"),
        ("ローン不可", "家・車の\nローンが\n組めない"),
    ], hsize=44, ssize=36),
    "e06_todo": P.bullets("今日からできる　6つの対策", [
        "①「お詫び」メールのリンクは踏まない",
        "② 使い回しのパスワードを変える",
        "③ 二段階認証・パスキーを入れる",
        "④ 荷物のSMS・お詫びクーポンは疑う",
        "⑤ 使っていないアカウントは退会",
        "⑥ 身に覚えのない契約・郵便に注意",
    ], size=56),
    "e07_matome": P.bullets("まとめ", [
        "9月末から　漏えいの発表が連発",
        "原因：システムの弱点・設定ミス・フィッシング・うっかり",
        "AIで攻撃が　安く・早くなった",
        "悪用はこれから → 偽メール・偽SMSに注意",
        "リンクを踏まない・使い回さない・二段階認証",
    ], size=54),
    "e08_ending": P.message(["あなたは何個のサービスに", "登録してる？", "コメントで教えて！"], size=96),
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
