"""16本目（てんちむ）のショート2本目「子役から4億円の返金まで」。作りは short_16_tenchim.py と同じ。

python3 catmeme/short_16b_tenchim.py → out/short_16b_tenchim.mp4
金額は「見込み」「本人の説明」をはっきり書く。私生活の未公開情報は使わない。
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M
from short_16_tenchim import (ADSTUDIO, CHILD, COURT, EVENT, FEATHER, MONEY, NEON, PAPERS, POST, SHELF, YOUNG, one, org,
                              side)

HERE = M.HERE
NAME = "short_16b_tenchim"
TITLE = ("元子役てんちむ", "返金の負担は4億円超", M.WHITE, M.YELLOW, M.RED)
COCOA = os.path.join(S.BGM, "星降る夜のホットココア.mp3")


def cuts():
    return [
        side(CHILD, "この子役\n*だれか*分かる？", "stare_big_eyes_tabby_kitten", 2.6, shake=True,
             se=["jan", "explosion_chudoon"], bgm={"file": COCOA, "gain": -6}),
        side(CHILD, "子役時代は\n*橋本甜歌*", "huh_huh_cat", 2.2, se="pi"),
        side(CHILD, "NHK\n「天才てれびくんMAX」\nにも出演", "meow_gray_white_kitten", 2.6, size=90, se="page_turn_01"),
        side(YOUNG, "2016年に\n*YouTube*を始めた", "talk_orange_white_sitting_cat", 2.4, se="pikon"),
        side(NEON, "それが\n*てんちむ*さん", "surprise_big_pupils_cat", 2.2, size=120, se="jan"),
        one(SHELF, "ナイトブラを\nプロデュース・宣伝", "think_bike_front_seat_cat", 2.4, se="page_turn_01"),
        one(ADSTUDIO, "2020年\n*豊胸手術を隠した*\n宣伝が発覚", "glare_disgusted_cat", 2.8, size=90, shake=True,
            se="pc_warning"),
        one(MONEY, "本人が\n*自腹で返金*すると表明", "realize_wet_cat_stare", 2.6, se="kon"),
        one(MONEY, "返金の見込み\n*約3億7,000万円*超\n（本人の発表）", "yell_orange_fat_cat", 2.8, size=90,
            se="price_display"),
        one(MONEY, "会社への賠償の見込みも合わせ\n*約4億3,000万円*\n（本人の説明）", "stare_big_eyes_tabby_kitten", 3.0, size=80,
            shake=True, se=["explosion_dokaan"]),
        one(NEON, "銀座のクラブなどでも\n*働いた*と\n報じられた", "sad_banana_cat_cry", 2.8, size=90, se="tear_drop"),
        one(MONEY, "2021年4月\n約2万人に*3億円以上*\n返金を報告", "punch_tabby_cat_reach", 2.8, size=90, se="pinpoon_correct"),
        org(PAPERS, "販売元", "でも会社とは\n*返金のお金*で対立", "work_typing_cat", 2.6, se="page_turn_02"),
        org(COURT, "東京地裁", "一審は\n*3億8,457万円*の\n支払い命令", "stare_standing_marmot", 2.8, size=90,
            se="buzzer_wrong"),
        org(COURT, "東京高裁", "でも2026年10月\n控訴審で*取り消し*\n（本人の報告）", "showoff_gojo_cosplay_cat", 2.8, size=86,
            shake=True, se=["explosion_chudoon"]),
        one(POST, "6年がかりの\n*大逆転*", "dance_three_kittens", 2.4, size=120, se="game_coin_get_money_gain_happy"),
        one(POST, "広告の“隠しごと”\nいくらかかるか\n*分かった？*", "eat_pop_cat", 2.6, size=96, se="chirin"),
        one(POST, "※金額は本人の発表・説明と報道によるもので、意味がそれぞれ違います\n※控訴審の結果は本人の報告（理由・確定は未確認）",
            "eat_pop_cat", 3.0, size=44, se="pinpon_notice"),
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
