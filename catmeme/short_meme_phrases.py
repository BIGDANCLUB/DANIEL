"""ショート「ニュースから生まれたネット名フレーズ6選」（縦 1080x1920・45〜58秒の1本）。
ニュースへのネットの反応から生まれて広まったフレーズを、1本の中で6個つづけて紹介する。

python3 catmeme/short_meme_phrases.py → out/short_meme_phrases.mp4
画面の作りは short_04_leak.py と同じ（上：話題の札つきタイトル帯／中：場面かパネル／下：大きな字幕）。

ルール：笑うのは「言葉の面白さ」と「出来事のおかしさ」まで。実在の人の発言は使わない・個人をバカにしない。
賛否が分かれた話（2億円トイレ）は反論もひとこと入れる。
"""
import os

from PIL import Image, ImageDraw

import parts as P
import short_03_kodomo_nisa as S
import short_04_leak as Q

HERE = S.HERE
PURPLE, COCOA = Q.PURPLE, Q.COCOA
MIRAI = os.path.join(S.BGM, "未来を創る君たちへ.mp3")
NEWS, NET = S.NEWS, (120, 50, 170)
YELLOW, RED, NAVY, BLACK, WHITE = S.YELLOW, S.RED, S.NAVY, S.BLACK, S.WHITE
SW = S.SW
ptext = Q.ptext
OUT = os.path.join(HERE, "out", "short_meme_phrases.mp4")


def card(no, origin, phrase, lines, col=RED):
    """フレーズのパネル：番号と元のニュース／大きなフレーズ／2〜3行の説明。"""
    img = Image.new("RGBA", (SW, 880), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((24, 10, SW - 24, 870), 40, fill=(252, 250, 244), outline=BLACK, width=7)
    d.ellipse((50, 34, 160, 144), fill=col)
    d.text((105, 89), str(no), font=P.font("black", 76), fill=WHITE, anchor="mm")
    img.alpha_composite(ptext(origin, SW - 230, 110, 58, fill=NAVY), (180, 34))
    img.alpha_composite(ptext(phrase, SW - 80, 300, 190, fill=col), (40, 170))
    y = 500
    for ln in lines:
        d.rounded_rectangle((60, y, SW - 60, y + 100), 22, fill=(235, 240, 250))
        img.alpha_composite(ptext(ln, SW - 160, 100, 56, fill=BLACK), (80, y))
        y += 116
    return img


def react(b, a, cap, **kw):
    return dict(kind="scene", bg=Q.bg(b), cats=[Q.cat(a, "ネットの声", 960, NET, h=860)], cap=cap, **kw)


def cuts(hook=True):
    """hook=True で、最初の5秒を A＋D のつかみ（短い時間でフレーズ連打→猫ミーム乱入→「6連発!!」）にする。"""
    if hook:
        import short_hooks as H   # short_hooks がこのファイルを読むので、ここで読む
        first = [H.hook_cut_AD(H.PHRASES, bgm={"file": PURPLE, "gain": -4})]
    else:
        first = [Q.one("bg06_spotlight", "surprise_big_pupils_cat", "ニュース猫", NEWS, "ニュースから生まれた\nネットの名フレーズ\n6連発！",
                       cap_col=YELLOW, dur=2.8, fx=["lines", "shake"], se=["jan", "doon_heavy"], bgm={"file": PURPLE, "gain": -6})]
    return first + [
        # ① 553＞1107
        Q.panel(card(1, "東大の総長選（2026年）", "553＞1107", ["553票の2位が　総長に選ばれた", "算数ではありえない“不等式”に"]),
                "票が少ないほうが\n勝った！？", dur=4.4, se="card_flip"),
        react("bg09_sns", "huh_huh_cat", "不等式の向き\n逆じゃない？", dur=2.4, se="boing_01"),
        # ② 古古古米
        Q.panel(card(2, "令和の米騒動（2025年）", "古古古米", ["放出された備蓄米は　2021年産＝古古古米", "2020年産は「古古古古米」"], col=(200, 120, 20)),
                "“古”が増えていく", dur=4.4, se="card_flip"),
        react("bg16_food_aisle", "weird_meowing_cat", "早口言葉か！\n味は普通らしい", dur=2.4, se="kon"),
        # ③ 2億円トイレ
        Q.panel(card(3, "大阪・関西万博（2024年）", "2億円トイレ", ["「トイレ1か所に約2億円」と報道", "実は便器46基・見直し後は約1.5億円"]),
                "反論もあった", dur=4.6, se="card_flip"),
        react("bg09_sns", "surprise_big_pupils_cat", "1個じゃ\nなかったのか！", dur=2.4, se="pikon"),
        # ④ ジャンボタニシ農法
        Q.panel(card(4, "SNSで拡散（2024年）", "ジャンボ\nタニシ農法", ["「雑草を食べる生きた除草剤」と拡散", "農水省が「放すのはやめて」と呼びかけ"],
                     col=(30, 140, 70)), "国が止めた！？", dur=4.6, se="card_flip", bgm={"file": COCOA, "gain": -6}),
        react("bg18_backyard", "glare_disgusted_cat", "“農法”って付けると\nそれっぽく見える", dur=2.6, se="boing_01"),
        # ⑤ のり弁
        Q.panel(card(5, "黒塗りの公文書", "のり弁", ["情報公開で出た書類が　ほぼ真っ黒", "海苔を敷き詰めたお弁当にそっくり"], col=NAVY),
                "国の書類が\n真っ黒！？", dur=4.4, se="card_flip"),
        react("bg15_convenience", "huh_huh_cat", "おかずも\n入れてほしい", dur=2.4, se="kon"),
        # ⑥ GoToトラブル
        Q.panel(card(6, "GoToトラベル（2020年）", "GoTo\nトラブル", ["前倒し→東京は対象外→地域ごとに停止", "→全国で一時停止…と変更が続いた"]),
                "1文字ちがい", dur=4.6, se="card_flip"),
        react("bg20_counter", "weird_meowing_cat", "トラベルじゃなくて\nトラブル！", dur=2.4, se="pikon"),
        Q.one("bg03_blackboard", "wave_waving_cat", "ニュース猫", NEWS, "どれが好き？\nほかに知ってたら\nコメントで！", cap_col=YELLOW, h=760,
              dur=3.2, se="chirin", bgm={"file": MIRAI, "gain": -8, "fade": 0.8}),
    ]


def main():
    S.run(cuts(), Q.title_band("ニュースから生まれた", "ネット名フレーズ6選", label="ネットで生まれた名フレーズ"), OUT,
          os.path.join(HERE, "out", "short_meme_phrases_preview"))


if __name__ == "__main__":
    main()
