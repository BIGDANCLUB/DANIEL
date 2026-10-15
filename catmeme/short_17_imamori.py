"""17本目（今森茉耶）のショート1本目「再出発からわずか6日」。作りは short_16_tenchim.py と同じ。60秒ちょうど（10/15 ルール）。

python3 catmeme/short_17_imamori.py → out/short_17_imamori.mp4
- 週刊誌は「疑惑」。降板の公式の理由は20歳未満の飲酒
- 妊娠の発言の中身・経緯にはふれない（ショートでは「対談動画の発言が拡散」まで）。LINE の関係者・中身は推測しない
- 本人のつらさを笑いにしない：後半は落ち着いた猫・静かな効果音
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M

HERE = M.HERE
NAME = "short_17_imamori"
TITLE = ("元戦隊ヒロイン", "再出発からわずか6日", M.WHITE, M.YELLOW, M.RED)
C = M.C
NORA = os.path.join(S.BGM, "野良猫は宇宙を目指した.mp3")
LETTER = os.path.join(S.BGM, "手紙のさよなら.mp3")
M.BGS[:0] = [os.path.join(HERE, "backgrounds", d) for d in ("17_imamori", "17_imamori/photos", "16_tenchim", "15_vambi")]
MAG, HERO, IZAKAYA, TVSTA, LOUNGE, CHAT, QUIET, TL = ("bg94_magazine_stand", "bg95_hero_studio", "bg98_izakaya_night",
                                                     "bg99_tv_station", "bg100_lounge_night", "bg101_phone_chat",
                                                     "bg102_quiet_room", "bg103_timeline2")
STUDIO = "bg70_youtube_studio"


def one(bg, say, a, dur, h=1100, **kw):
    return M.cut(bg, say, [(a, C, h, kw.pop("flip", False))], dur, **kw)


def photo_img(name, w=1000):
    from PIL import Image, ImageOps
    im = Image.open(M.bg_path(name)).convert("RGB")
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    return ImageOps.expand(im, border=10, fill=(255, 255, 255)).convert("RGBA")


def side(name, say, a, dur, **kw):
    """写真をセリフの下に枠つきで見せ、猫は右下に小さく（顔にも字幕にもかけない）。"""
    c = M.cut(TL, say, [(a, 900, 520, False)], dur, **kw)
    c["img"], c["img_y"] = photo_img(name), 1380
    return c


def org(bg, who, say, a, dur, **kw):
    return M.cut(bg, say, [(a, C, 1100, False)], dur, label=who, label_x=540, **kw)


def cuts():
    return [
        side("p5_event_smile", "元戦隊ヒロインが\n再出発から\n*わずか6日*で発信休止", "stare_big_eyes_tabby_kitten", 3.0, shake=True,
             se=["jan", "explosion_chudoon"], bgm={"file": NORA, "gain": -6}),
        side("p2_missmagazine_gp", "2023年\n*ミスマガジン*グランプリ", "surprise_big_pupils_cat", 2.6, se="pi"),
        side("p1_cast_and_hero", "2025年\n戦隊シリーズ初の\n*女性ブラック*に", "excited_hodomoe_city_cat", 2.8, se="pikon"),
        one(TL, "2006年 宮崎県生まれ\n中学生のころから\n*TikTok*で活動", "meow_gray_white_kitten", 2.8, size=96, se="pi"),
        one(HERO, "ところが\n週刊誌が\n*不倫疑惑*を報道", "peek_what_happen_cat", 2.8, se="page_turn_02"),
        one(HERO, "※あくまで\n週刊誌の*疑惑*", "stare_interviewer_cat", 2.2, size=110, se="kon"),
        org(TVSTA, "事務所", "2025年11月\n*20歳未満の飲酒*で\n契約解除", "work_typing_cat", 3.0, size=96, shake=True,
            se=["explosion_dokaan"]),
        one(QUIET, "本人もInstagramで\n“*非常に恥ずべき行為*”と\n謝罪", "realize_wet_cat_stare", 2.8, size=96, se="kon"),
        one(IZAKAYA, "当時は*19歳*\n20歳の誕生日まで\nあと4か月ほど", "think_bike_front_seat_cat", 2.6, size=100, se="pi"),
        one(HERO, "番組も\n*途中で降板*", "despair_dramatic_kitten", 2.4, size=120, se="chin_bell_failure_sad_ending"),
        one(IZAKAYA, "降板の公式の理由は\n*飲酒*のほう", "think_bike_front_seat_cat", 2.6, size=100, se="pi"),
        one(LOUNGE, "その後\n約4か月\n*ラウンジで働いた*と説明", "talk_orange_white_sitting_cat", 2.8, size=96, se="kon"),
        one(STUDIO, "そして\n2026年10月8日\n*YouTubeで再出発*", "meow_gray_white_kitten", 2.8, se="pikon",
            bgm={"file": LETTER, "gain": -8, "fade": 0.6}),
        one(STUDIO, "4日後\n対談動画での発言が\n*SNSで拡散*", "sulk_hungry_cat", 2.8, size=96, se="pi"),
        one(CHAT, "14日未明\nLINEとみられる画像を投稿\n*すぐ削除*", "blank_black_cat_zoning_out", 3.0, size=90, se="kon"),
        one(CHAT, "関係者などは\n*確認されていない*", "calm_black_face_sheep", 2.4, size=110, se="pi"),
        one(QUIET, "14日\n本人が謝罪\n*すべての発信を休止*", "realize_wet_cat_stare", 3.0, size=100, se="kon"),
        one(QUIET, "“心がもたず”と\n*追い詰められた*心境も", "sad_black_dog", 2.8, size=100, se="pi"),
        one(TL, "再出発から\n*6日*の出来事", "stare_interviewer_cat", 2.4, size=120, se="kon"),
        one(QUIET, "責任と\n*誹謗中傷*は\n別の問題", "calm_black_face_sheep", 2.6, size=110, se="pikon"),
        one(QUIET, "※週刊誌の報道は疑惑で、確定した事実ではありません\n※本人・関係者への誹謗中傷・詮索はやめてください\n"
                   "※背景イラストの一部はAIで作っています", "calm_black_face_sheep", 3.0, size=44, se="pinpon_notice"),
    ]


def main():
    cs = M.keep_going(cuts())
    title = M.title_band(*TITLE)
    for c in cs:
        c["draw"] = M.make_draw(c, title)
    print(f"{len(cs)} カット・{sum(R.cut_dur(c) for c in cs):.1f}秒")
    S.run(cs, title, os.path.join(HERE, "out", NAME + ".mp4"), os.path.join(HERE, "out", NAME + "_preview"))


if __name__ == "__main__":
    main()
