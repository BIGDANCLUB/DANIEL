"""個人情報流出（4本目）のショート2本（縦 1080x1920・60秒以内）。

python3 catmeme/short_04_leak.py a   → out/short_04a_license.mp4（免許証が漏れると…）
python3 catmeme/short_04_leak.py b   → out/short_04b_coupon.mp4（お詫びクーポンのワナ）
画面の作りは short_03_kodomo_nisa.py と同じ（上：タイトル帯／中：場面かパネル／下：大きな字幕）。
"""
import os
import sys

from PIL import Image, ImageDraw

import short_01_todai as T
import short_03_kodomo_nisa as S

HERE = S.HERE
BGM = S.BGM
PURPLE = os.path.join(BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")
NORA = os.path.join(BGM, "野良猫は宇宙を目指した.mp3")
COCOA = os.path.join(BGM, "星降る夜のホットココア.mp3")
SW = S.SW
NEWS, SAGE, HACK = S.NEWS, S.SAGE, (30, 30, 30)
YELLOW, RED, WHITE, BLACK, NAVY, ORANGE = S.YELLOW, S.RED, S.WHITE, S.BLACK, S.NAVY, S.ORANGE
text_img, ptext, base, items, big = S.text_img, T.ptext, T.base, T.items, T.big
BGS = [os.path.join(HERE, "backgrounds", d) for d in ("04_leak", "03_kodomo_nisa", "02_october", "01_todai")]


def bg(n):
    for d in BGS:
        p = os.path.join(d, n + ".png")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(n)


def title_band(top, main):
    img = Image.new("RGBA", (SW, 400), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, SW, 400), fill=NAVY)
    d.polygon([(0, 330), (SW, 300), (SW, 400), (0, 400)], fill=RED)
    img.alpha_composite(text_img(top, SW, 150, 104, fill=WHITE), (0, 40))
    img.alpha_composite(text_img(main, SW, 170, 140, fill=YELLOW), (0, 170))
    return img


def flow(head, steps, note=""):
    """上から下への流れ図。steps=[(大, 小, 強調)]。段数に合わせて高さを決める。"""
    img, d = base(head)
    n = len(steps)
    gap = 32
    box_h = (640 - gap * (n - 1)) / n
    y = 190
    for k, (h, s, hi) in enumerate(steps):
        col = RED if hi else NAVY
        d.rounded_rectangle((60, y, SW - 60, y + box_h), 24, fill=WHITE, outline=col, width=8)
        img.alpha_composite(ptext(h, 460, int(box_h), 60, fill=col), (70, int(y)))
        img.alpha_composite(ptext(s, 470, int(box_h), 44, fill=(60, 60, 60)), (540, int(y)))
        if k < n - 1:
            d.polygon([(SW / 2 - 30, y + box_h + 4), (SW / 2 + 30, y + box_h + 4), (SW / 2, y + box_h + gap - 2)], fill=RED)
        y += box_h + gap
    if note:
        img.alpha_composite(ptext(note, SW - 80, 100, 40, fill=(70, 70, 70)), (40, 840 - 70))
    return img


def cat(a, role, x, color, h=820, flip=False, mute=False):
    return S.cat(a, role, x, color, h=h, flip=flip, mute=mute)


def one(b, a, role, color, cap, **kw):
    """1匹アップ。"""
    return dict(kind="scene", bg=bg(b), cats=[cat(a, role, 960, color, h=kw.pop("h", 900), flip=kw.pop("flip", False))],
                cap=cap, **kw)


def two(b, left, right, cap, who="L", until=None, **kw):
    """2匹で掛け合い（左＝ニュース猫、右＝博識な猫）。しゃべらない方の音は消す。until で素材を途中で切る。"""
    cats = [cat(left, "ニュース猫", 520, NEWS, mute=who != "L"), cat(right, "博識な猫", 1430, SAGE, mute=who != "R")]
    if until:
        for c in cats:
            c["until"] = until
    return dict(kind="scene", bg=bg(b), cats=cats, cap=cap, **kw)


def panel(img, cap, **kw):
    return dict(kind="panel", img=img, cap=cap, **kw)


# ---- A：免許証が漏れると… ----
def cuts_a():
    return [
        one("bg20_counter", "surprise_big_pupils_cat", "ニュース猫", NEWS, "レンタカー予約で\n免許証まで！？", cap_col=RED,
            dur=2.6, fx=["lines", "shake"], se=["jan", "explosion_chudoon"], bgm={"file": PURPLE, "gain": -4}),
        panel(big("タイムズカー（9/28発表）", "約660万件が\n漏えいのおそれ", col=NAVY,
                  note="名前・住所・生年月日・電話・メール"), "不正アクセスで\n約660万件", dur=3.0, se="pc_warning"),
        panel(big("そのうち", "約160万件は\n免許証などの\n本人確認書類", note="※件数はタイムズカーの発表"),
              "免許証の情報まで", cap_col=RED, dur=3.2, se="doon_heavy"),
        two("bg20_counter", "glare_disgusted_cat", "eat_pop_cat", "免許証って\n名前・住所・生年月日\n顔写真まで載ってるからな",
            who="R", dur=3.2, se="hyoshigi_02"),
        one("bg20_counter", "peek_what_happen_cat", "ニュース猫", NEWS, "それ悪用されたら\nどうなるの？", dur=2.4,
            se="question_hatena_maou"),
        panel(flow("悪用されると…（最悪のケース）", [
            ("なりすまし", "名前を使って\nクレカを作られる", False),
            ("勝手に借金", "知らぬ間に\nキャッシング", False),
            ("信用に傷", "延滞の記録\n＝いわゆるブラック", False),
            ("ローン不可", "家・車のローンが\n組めない", True)]),
            "最悪こうなる", cap_col=RED, dur=4.2, se="game_dq_miss", bgm={"file": NORA, "gain": -4}),
        one("bg23_hacker_room", "weird_meowing_cat", "ニュース猫", NEWS, "知らないうちに\nブラックリスト入り！？",
            cap_col=RED, dur=2.6, fx=["lines", "shake"], se="game_mgs_alert"),
        one("bg23_hacker_room", "cocky_dj_cat", "ハッカー猫", HACK, "ローンの審査？\nお気の毒さま〜", dur=2.4,
            se="anime_shinchan_taraan"),
        one("bg20_counter", "confused_i_dont_know_cat", "ニュース猫", NEWS, "じゃあ\nどうすればいいの？", dur=2.2, se="boing_fail"),
        two("bg20_counter", "huh_huh_cat", "think_bike_front_seat_cat", "実際は審査で\n電話や口座の確認もある\n必ず通るわけじゃない",
            who="R", dur=3.2, se="pinpon_notice"),
        panel(items("免許証が漏れたかも…と思ったら", [
            "信用情報機関に「本人申告」", "（CIC・JICC・全銀協）", "なりすましの契約を防ぎやすく",
            "開示して　身に覚えのない契約をチェック"]),
            "今すぐできる対策", cap_col=YELLOW, dur=4.0, se="pinpoon_correct"),
        two("bg20_counter", "spin_spinning_cat", "eat_pop_cat", "信用情報って\n自分で見られるのか", who="L", dur=2.4, se="pikon"),
        two("bg20_counter", "spin_spinning_cat", "eat_pop_cat", "開示を申し込めば\n見られるぞ\n身に覚えのない契約がないかチェックな",
            who="R", dur=3.0, se="idea_newtype_01"),
        one("bg03_blackboard", "wave_waving_cat", "ニュース猫", NEWS, "なぜ漏えいが連発？\n本編で解説！", cap_col=YELLOW,
            h=760, dur=3.0, se="chirin", bgm={"file": COCOA, "gain": -6, "fade": 0.8}),
    ]


# ---- B：お詫びクーポンのワナ ----
def cuts_b():
    return [
        panel(items("9月末から　漏えいの発表が連発", [
            "焼肉きんぐ　約1,078万件", "Gyazo　約2,362万件", "タイムズカー　約660万件", "デジタル庁　約24.6万件"],
            note="件数は各社の発表（漏えいのおそれを含む）"), "漏えいが\n止まらない", dur=3.4, se=["jan", "doon_heavy"],
            bgm={"file": PURPLE, "gain": -4}),
        one("bg22_yakiniku", "dance_koto_nai_cat", "ニュース猫", NEWS, "多すぎて\nもう何がなんだか", dur=2.4,
            se="spring_byoin"),
        one("bg26_phone_alert", "taunt_cat_and_scared_dog", "ハッカー猫", HACK, "お詫びの\nクーポンです〜（偽）", dur=2.6,
            se="shine_kira_01"),
        two("bg26_phone_alert", "joy_happy_happy_happy_cat", "glare_disgusted_cat", "え、クーポン？\nラッキー♪", who="L", dur=2.4, until=2.8,
            se="game_mario_1up"),
        two("bg26_phone_alert", "joy_happy_happy_happy_cat", "glare_disgusted_cat", "待て\nそれが一番あやしい", who="R", dur=2.4, until=2.8,
            se="tsukkomi_bishi"),
        one("bg23_hacker_room", "angry_aiming_cat", "ハッカー猫", HACK, "ポチッと押してくれれば\nこっちのもん", dur=2.6,
            se="game_zelda_item_get"),
        panel(flow("お詫びクーポンのワナ", [
            ("偽のお詫びが届く", "漏えいの\nニュースに便乗", False),
            ("リンクを押す", "本物そっくりの\n偽サイトへ", False),
            ("入力させられる", "ログイン情報・\nカード番号", False),
            ("盗まれる", "不正ログイン・\nカードの不正利用", True)]),
            "押すと…", cap_col=RED, dur=4.2, se="buzzer_wrong", bgm={"file": NORA, "gain": -4}),
        one("bg26_phone_alert", "surprise_big_pupils_cat", "ニュース猫", NEWS, "カード番号まで！？", cap_col=RED, dur=2.2,
            fx=["lines", "shake"], se="explosion_chudoon"),
        two("bg26_phone_alert", "surprise_big_pupils_cat", "eat_pop_cat", "本物のお詫びでも\nメールのリンクじゃなく\n公式アプリで確かめる",
            who="R", dur=3.2, se="pinpon_notice"),
        two("bg02_room", "peek_what_happen_cat", "eat_pop_cat", "パスワードを使い回してると\nほかのサービスにも\n次々ログインされる",
            who="R", dur=3.4, se="pc_warning"),
        two("bg02_room", "sad_banana_cat_cry", "eat_pop_cat", "……全部\n同じパスワードだわ", who="L", dur=2.6, se="tear_drop"),
        panel(items("今日からできる対策", [
            "「お詫び」のリンクは押さない", "公式アプリ・公式サイトから確認", "パスワードを使い回さない", "二段階認証を入れる"]),
            "これだけは\nやっておこう", cap_col=YELLOW, dur=4.0, se="pinpoon_correct"),
        two("bg02_room", "sleepy_sleepy_cat", "drive_driving_cat", "持ってるだけで漏れるから\n使ってないアカウントは\n退会しとこう",
            who="R", dur=3.2, se="page_turn_01"),
        one("bg23_hacker_room", "blank_black_cat_zoning_out", "ハッカー猫", HACK, "二段階認証……\nだと……", dur=2.4,
            se="deflate_hyororo"),
        one("bg03_blackboard", "wave_waving_cat", "ニュース猫", NEWS, "なぜ漏えいが連発？\n本編で解説！", cap_col=YELLOW,
            h=760, dur=3.0, se="chirin", bgm={"file": COCOA, "gain": -6, "fade": 0.8}),
    ]


SHORTS = {
    "a": (cuts_a, ("レンタカー予約で", "免許証まで⁉"), "short_04a_license"),
    "b": (cuts_b, ("その「お詫びクーポン」", "押しちゃダメ⁉"), "short_04b_coupon"),
}


def main():
    for key in sys.argv[1:] or ["a", "b"]:
        fn, title, name = SHORTS[key]
        S.run(fn(), title_band(*title), os.path.join(HERE, "out", name + ".mp4"), os.path.join(HERE, "out", name + "_preview"))


if __name__ == "__main__":
    main()
