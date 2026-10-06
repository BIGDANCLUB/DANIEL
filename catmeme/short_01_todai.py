"""東大総長のショート（縦 1080x1920・60秒以内）。「投票2位が総長に⁉」をざっくり。

python3 catmeme/short_01_todai.py → out/short_01_todai.mp4
画面の作りは short_03_kodomo_nisa.py と同じ（上：タイトル帯／中：場面かパネル／下：大きな字幕）。
"""
import os

from PIL import Image, ImageDraw

import parts as P
import short_03_kodomo_nisa as S

HERE = S.HERE
BG = os.path.join(HERE, "backgrounds", "01_todai")
BGM = S.BGM
PURPLE = os.path.join(BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")
KAMI = os.path.join(BGM, "神の怒り.mp3")
MIRAI = os.path.join(BGM, "未来を創る君たちへ.mp3")
OUT = os.path.join(HERE, "out", "short_01_todai.mp4")

SW = S.SW
NEWS, SAGE, NET = S.NEWS, S.SAGE, (120, 50, 170)
YELLOW, RED, WHITE, BLACK, NAVY, ORANGE = S.YELLOW, S.RED, S.WHITE, S.BLACK, S.NAVY, S.ORANGE
GRAY = (150, 150, 150)
text_img = S.text_img


def ptext(text, w, h, size, fill=BLACK, stroke=None, sw=None):
    """パネル用の文字（白地の上なので縁取りなし。入らなければ小さくする）。"""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lines = text.split("\n")
    while True:
        f = P.font("black", size)
        if (max(d.textlength(ln, font=f) for ln in lines) <= w - 20 and size * 1.2 * len(lines) <= h) or size < 30:
            break
        size -= 2
    y = h / 2 - size * 1.2 * len(lines) / 2 + size * 0.6
    for ln in lines:
        d.text((w / 2, y), ln, font=f, fill=fill, anchor="mm")
        y += size * 1.2
    return img


def bg(n):
    return os.path.join(BG, n + ".png")


def title_band():
    img = Image.new("RGBA", (SW, 400), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, SW, 400), fill=NAVY)
    d.polygon([(0, 330), (SW, 300), (SW, 400), (0, 400)], fill=RED)
    img.alpha_composite(text_img("東大の総長選", SW, 150, 110, fill=WHITE), (0, 40))
    img.alpha_composite(text_img("2位が勝った⁉", SW, 170, 150, fill=YELLOW), (0, 170))
    return img


def base(head):
    img = Image.new("RGBA", (SW, 880), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((24, 10, SW - 24, 870), 40, fill=(252, 250, 244), outline=BLACK, width=7)
    img.alpha_composite(ptext(head, SW - 60, 150, 90, fill=BLACK, stroke=WHITE, sw=4), (30, 30))
    return img, d


def votes(head, rows, note=""):
    """横棒グラフ。rows=[(名前, 票, 色, 右の文字)]。"""
    img, d = base(head)
    top = max(v for _, v, _, _ in rows)
    y = 230
    step = 520 / len(rows)
    for name, v, col, tag in rows:
        d.text((60, y + 30), name, font=P.font("black", 54), fill=BLACK, anchor="lm")
        w = int(560 * v / top)
        d.rounded_rectangle((60, y + 75, 60 + w, y + 145), 16, fill=col)
        d.text((80 + w, y + 110), f"{v:,}票", font=P.font("black", 60), fill=col if col != GRAY else (90, 90, 90), anchor="lm")
        if tag:
            d.text((SW - 60, y + 30), tag, font=P.font("black", 52), fill=RED if col == ORANGE else NAVY, anchor="rm")
        y += step
    if note:
        img.alpha_composite(ptext(note, SW - 80, 120, 48, fill=(70, 70, 70), stroke=WHITE, sw=2), (40, 735))
    return img


def big(head, text, col=RED, note=""):
    img, d = base(head)
    img.alpha_composite(ptext(text, SW - 100, 520, 150, fill=col, stroke=WHITE, sw=4), (50, 190))
    if note:
        img.alpha_composite(ptext(note, SW - 80, 120, 48, fill=(70, 70, 70), stroke=WHITE, sw=2), (40, 735))
    return img


def items(head, lines, note=""):
    img, d = base(head)
    y = 230
    for ln in lines:
        d.rounded_rectangle((60, y, SW - 60, y + 92), 22, fill=(235, 240, 250))
        img.alpha_composite(ptext(ln, SW - 160, 92, 58, fill=NAVY, stroke=WHITE, sw=2), (80, y))
        y += 108
    if note:
        img.alpha_composite(ptext(note, SW - 80, 120, 48, fill=(70, 70, 70), stroke=WHITE, sw=2), (40, 735))
    return img


def flow(head, steps, note=""):
    """上から下への流れ図。steps=[(大, 小, 強調)]。"""
    img, d = base(head)
    y = 210
    for k, (h, s, hi) in enumerate(steps):
        col = ORANGE if hi else NAVY
        d.rounded_rectangle((70, y, SW - 70, y + 140), 26, fill=WHITE, outline=col, width=8)
        img.alpha_composite(ptext(h, 520, 140, 64, fill=col, stroke=WHITE, sw=2), (80, y))
        img.alpha_composite(ptext(s, 420, 140, 46, fill=(60, 60, 60), stroke=WHITE, sw=2), (580, y))
        if k < len(steps) - 1:
            d.polygon([(SW / 2 - 34, y + 150), (SW / 2 + 34, y + 150), (SW / 2, y + 190)], fill=RED)
        y += 200
    if note:
        img.alpha_composite(ptext(note, SW - 80, 120, 48, fill=(70, 70, 70), stroke=WHITE, sw=2), (40, 735))
    return img


def cat(a, role, x, color, h=820, flip=False, mute=False):
    return S.cat(a, role, x, color, h=h, flip=flip, mute=mute)


def cuts():
    return [
        dict(kind="scene", bg=bg("bg01_campus"), cats=[cat("slack_nail_filing_cat", "ニュース猫", 960, NEWS, h=900)],
             cap="東大の次の総長\n決まったんだ〜", dur=2.4, se="chirin", bgm={"file": PURPLE, "gain": -5}),
        dict(kind="panel", img=votes("学内の投票（決選投票）", [
            ("染谷隆夫さん", 1107, NAVY, "1位・51%"), ("藤垣裕子さん", 553, GRAY, "2位"), ("山本隆司さん", 451, GRAY, "3位")]),
             cap="1位は\n半分以上の票", dur=3.2, se="card_flip"),
        dict(kind="scene", bg=bg("bg02_room"), cats=[dict(cat("joy_happy_happy_happy_cat", "ニュース猫", 960, NEWS, h=900), until=3.0)],
             cap="2位の倍よ倍！\nはい優勝！", cap_col=YELLOW, dur=2.4, se="game_mario_1up"),
        dict(kind="scene", bg=bg("bg06_spotlight"), cats=[cat("dance_koto_nai_cat", "ニュース猫", 960, NEWS, h=760, mute=True)],
             cap="選ばれたのは……", dur=2.0, se="drumroll", bgm={"file": None, "fade": 0.6}),
        dict(kind="panel", img=votes("次の総長に選ばれたのは", [
            ("染谷隆夫さん", 1107, GRAY, "1位"), ("藤垣裕子さん", 553, ORANGE, "選ばれた！"), ("山本隆司さん", 451, GRAY, "")],
            note="東大150年で　初めての女性の総長"),
             cap="2位の\n藤垣裕子さん！", cap_col=RED, dur=3.2, se=["jan", "explosion_chudoon"], bgm={"file": KAMI, "gain": -4}),
        dict(kind="scene", bg=bg("bg02_room"), cats=[cat("surprise_big_pupils_cat", "ニュース猫", 960, NEWS, h=900)],
             cap="えええ！？\n1位の人は！？", cap_col=RED, dur=2.4, fx=["lines", "shake"], se="anime_broly_dedeen"),
        dict(kind="panel", img=flow("東大の総長の決まり方", [
            ("候補者5人", "書類や推薦で\nしぼる", False), ("学内で投票", "あくまで\n参考の一つ", False),
            ("16人の会議", "最後はここが\n決める", True)]),
             cap="最後に決めるのは\n16人の会議", dur=3.4, se="xylophone_transition",
             bgm={"file": PURPLE, "gain": -7, "from": 40, "fade": 0.8}),
        dict(kind="scene", bg=bg("bg02_room"),
             cats=[cat("huh_goat_talks_to_huh_cat", "ニュース猫", 520, NEWS), cat("eat_pop_cat", "博識な猫", 1430, SAGE, mute=True)],
             cap="投票って\nただのアンケート？", dur=2.6, se="question_hatena_maou"),
        dict(kind="panel", img=items("会議が挙げた　選んだ理由", [
            "文系と理系をつなぐ力", "大学を外にひらく力", "科学をわかりやすく伝える力", "分断を乗りこえる力"], note="※理由の一部"),
             cap="会議は\n「この力を評価」", dur=3.4, se="page_turn_01"),
        dict(kind="scene", bg=bg("bg09_sns"), cats=[cat("angry_cat_hits_cat", "ネットの声", 960, NET, h=900)],
             cap="1位を落とすなら\n投票いらなくね？", cap_col=RED, dur=2.8, fx=["lines", "shake"], se="game_aceattorney_desk_slam"),
        dict(kind="scene", bg=bg("bg09_sns"), cats=[cat("huh_huh_cat", "ネットの声", 960, NET, h=900)],
             cap="1位じゃダメな理由\nどこに書いてある？", dur=2.8, se="tsukkomi_bishi"),
        dict(kind="panel", img=big("実は　京都大学でも（2026年）", "投票3位が\n学長に", note="教職員の組合は「意思を反映していない」と批判"),
             cap="京大でも\n下剋上", dur=3.2, se="doon_heavy"),
        dict(kind="panel", img=big("筑波大学では（2020年）", "教職員の\n投票ごと廃止", note="投票で負けた現職の学長が　再任"),
             cap="筑波大は\n投票ごと消した", cap_col=RED, dur=3.2, se="buzzer_wrong"),
        dict(kind="scene", bg=bg("bg02_room"), cats=[cat("spin_spinning_cat", "ニュース猫", 960, NEWS, h=900)],
             cap="強すぎん！？", cap_col=RED, dur=1.8, fx=["lines", "shake"], se="boing_fail"),
        dict(kind="scene", bg=bg("bg02_room"),
             cats=[cat("think_bike_front_seat_cat", "ニュース猫", 520, NEWS, mute=True), cat("eat_pop_cat", "博識な猫", 1430, SAGE)],
             cap="ルール違反じゃない\nでも説明が\nいちばん大事", dur=3.4, se="idea_newtype_01",
             bgm={"file": MIRAI, "gain": -5, "fade": 0.8}),
        dict(kind="scene", bg=bg("bg03_blackboard"), cats=[cat("wave_waving_cat", "ニュース猫", 960, NEWS, h=760)],
             cap="くわしい理由・会見は\n本編で解説！", cap_col=YELLOW, dur=3.0, se="chirin"),
    ]


def main():
    S.run(cuts(), title_band(), OUT, os.path.join(HERE, "out", "short_01_preview"))


if __name__ == "__main__":
    main()
