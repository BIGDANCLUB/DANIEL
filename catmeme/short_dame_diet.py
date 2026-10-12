"""ダメ人間の猫ミーム #3「明日から本気でやせる」（台本：scripts/dame_03_diet.md）。作りは short_dame_template.py と同じ。

python3 catmeme/short_dame_diet.py → out/short_dame_diet.mp4
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M
from short_dame_payday import they
from short_dame_rent import one, two

HERE = M.HERE
NAME = "short_dame_diet"
TITLE = ("とあるダメ人間", "明日から本気でやせる")
NORA = os.path.join(S.BGM, "野良猫は宇宙を目指した.mp3")
PURPLE = os.path.join(S.BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")
SPOT, HOME, OFFICE, RAMEN = "bg06_spotlight", "bg14_home_night", "bg25_office_desk", "bg13_izakaya"

# 登場人物（主人公以外。生き物だけ）
TOMO = ("lick_talking_goat", 1000)          # 友だち（ツッコミ）
DOURYOU = ("stare_standing_marmot", 950)    # 同僚（無言の圧）
TENSHU = ("rizz_cat_rizz", 1050)            # ラーメン屋の店主（誘惑）
GOJO = ("showoff_gojo_cosplay_cat", 1000)   # 強がる主人公


def cuts():
    return [
        one(SPOT, "ダイエット3日目の夜に\n*ラーメン大盛り*。", "eat_crunchy_cat_luna", 3.0, size=110, shake=True,
            se=["jan", "explosion_chudoon"], bgm={"file": NORA, "gain": -6}),
        one(HOME, "……いや、ちゃんと\n頑張ってたんだって。", "confused_i_dont_know_cat", 2.6, se="whoosh_shu"),
        one(HOME, "体重計……*+5キロ*？", "surprise_big_pupils_cat", 2.2, size=120, shake=True, se="explosion_dokaan"),
        one(HOME, "は？", "huh_huh_cat", 1.6, size=230, se="question_hatena_maou"),
        one(HOME, "よし、*明日から*\n本気出す。", GOJO[0], 2.2, size=120, se="sword_shakiin"),
        they(HOME, "明日から？", GOJO, TOMO, 2.0, "友だち", size=150, se="boing_01"),
        two(HOME, "今日はもう夜だし。", GOJO, TOMO, 2.0, "友だち", size=120),
        one(HOME, "1日目。\n*サラダだけ*！", "joy_happy_happy_happy_cat", 2.2, size=120, se="pikon"),
        one(HOME, "意外と*いける*わ。", "flip_emo_cat_hair", 2.0, size=130, se="shine_kira_01"),
        one(OFFICE, "2日目。\n……お腹鳴りすぎ。", "sulk_hungry_cat", 2.4, se="gugi"),
        they(OFFICE, "お前の腹の音、\n*会議中*に響いてたぞ", ("sulk_hungry_cat", 1000), DOURYOU, 2.6, "同僚"),
        two(OFFICE, "……すいません。", ("sulk_hungry_cat", 1000), DOURYOU, 1.8, "同僚", size=140, se="tear_drop"),
        one(RAMEN, "3日目の夜。\n……いい匂い。", "peek_what_happen_cat", 2.4, bgm={"file": PURPLE, "gain": -8, "fade": 0.3}),
        they(RAMEN, "いらっしゃい！\n大盛り*無料*だよ！", ("peek_what_happen_cat", 1000), TENSHU, 2.4, "店主", size=110,
             se="anime_shinchan_taraan"),
        two(RAMEN, "……*無料*なら\n食べないと損か。", ("realize_wet_cat_stare", 1000), TENSHU, 2.4, "店主", se="idea_newtype_01"),
        they(RAMEN, "チャーシューも\nのせとく？", ("realize_wet_cat_stare", 1000), TENSHU, 2.2, "店主"),
        one(RAMEN, "のせて*ください*！！", "excited_hodomoe_city_cat", 2.0, size=130, shake=True, se="jan"),
        one(RAMEN, "……。", "eat_crunchy_cat_luna", 1.6, size=200, se="eat_paku"),
        one(HOME, "うますぎた……。", "sleepy_old_memories_cat", 2.0, size=140, se="chirin", bgm={"file": NORA, "gain": -6, "fade": 0.3}),
        they(HOME, "お前、*明日から*って\n言ってなかった？", ("sleepy_old_memories_cat", 1000), TOMO, 2.6, "友だち"),
        two(HOME, "うん。\nだから*明日から*。", GOJO, TOMO, 2.2, "友だち", size=120, se="sword_shakiin"),
        they(HOME, "……で、明日の夜は？", GOJO, TOMO, 1.8, "友だち"),
        one(HOME, "*焼肉*。", "cocky_dj_cat", 1.8, size=230, shake=True, se="tv_dokkiri_tettere"),
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
