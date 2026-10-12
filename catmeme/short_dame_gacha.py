"""ダメ人間の猫ミーム #5「生活費でガチャ回した」（台本：scripts/dame_05_gacha.md）。作りは short_dame_template.py と同じ。

python3 catmeme/short_dame_gacha.py → out/short_dame_gacha.mp4
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M
from short_dame_payday import they
from short_dame_rent import one, two

HERE = M.HERE
NAME = "short_dame_gacha"
TITLE = ("とあるダメ人間", "生活費でガチャ回した")
NORA = os.path.join(S.BGM, "野良猫は宇宙を目指した.mp3")
LOFI = os.path.join(S.BGM, "2_23_AM.mp3")
PURPLE = os.path.join(S.BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")
SPOT, HOME, PHONE = "bg06_spotlight", "bg14_home_night", "bg26_phone_alert"

# 登場人物（主人公以外。生き物だけ）
TOMO = ("lick_talking_goat", 880)             # 友だち（ツッコミ）
PC = ("work_dog_staring_computer", 1000)      # スマホを見つめる主人公


def cuts():
    return [
        one(SPOT, "生活費でガチャ回して\n*推し*は出なかった。", "blank_black_cat_zoning_out", 3.2, size=110, shake=True,
            se=["jan", "explosion_chudoon"], bgm={"file": NORA, "gain": -6}),
        one(HOME, "……いや、*1回*だけの\nつもりだったんだよ。", "sulk_hungry_cat", 2.6, se="whoosh_shu"),
        one(PHONE, "推しの*限定*、\n今日まで！？", "excited_hodomoe_city_cat", 2.2, size=120, se="pikon",
            bgm={"file": PURPLE, "gain": -8, "fade": 0.3}),
        one(PHONE, "*1回*だけ。\n1回だけなら。", "happy_girlfriend_dance_cat", 2.2, se="button_13"),
        one(PHONE, "……ハズレ。", "huh_huh_cat", 1.6, size=160, se="buzzer_wrong"),
        one(PHONE, "*10連*なら\n出るでしょ。", "cocky_dj_cat", 2.2, size=120, se="drumroll"),
        one(PHONE, "……ハズレ。", "glare_disgusted_cat", 1.6, size=160, se="game_dq_miss"),
        they(HOME, "おい、\n*何回*回してんの？", PC, TOMO, 2.4, "友だち", size=120, bgm={"file": LOFI, "gain": -6, "fade": 0.3}),
        two(HOME, "まだ*3万*しか\n入れてない。", PC, TOMO, 2.4, "友だち", size=120, se="price_display"),
        they(HOME, "*しか*？", PC, TOMO, 1.6, "友だち", size=200, se="question_hatena_maou"),
        two(HOME, "天井まで\nあと*少し*なんだよ。", PC, TOMO, 2.4, "友だち"),
        they(HOME, "それ、\n*生活費*じゃない？", PC, TOMO, 2.4, "友だち", size=120),
        one(HOME, "……推しは\n生活より*大事*。", "flip_emo_cat_hair", 2.2, size=120, se="shine_kira_01"),
        one(SPOT, "キター！！\n*推し*！！", "joy_happy_happy_happy_cat", 2.0, size=140, shake=True, se="fanfare_pararappara",
            bgm={"file": PURPLE, "gain": -8, "fade": 0.2}),
        one(SPOT, "……え？", "peek_what_happen_cat", 1.4, size=180),
        one(PHONE, "欲しかったの\n*限定衣装*の方……。", "realize_wet_cat_stare", 2.4, se="shock_piano",
            bgm={"file": LOFI, "gain": -6, "fade": 0.3}),
        one(PHONE, "……。", "blank_black_cat_zoning_out", 1.2, size=200),
        they(HOME, "で、\n*残高*いくら？", ("sad_black_dog", 950), TOMO, 2.0, "友だち", size=120),
        two(HOME, "*512円*。", ("despair_dramatic_kitten", 1000), TOMO, 1.8, "友だち", size=180, shake=True, se="explosion_dokaan"),
        they(HOME, "……飯、\nおごってやるよ。", ("despair_dramatic_kitten", 1000), TOMO, 2.4, "友だち", se="chirin",
             bgm={"file": NORA, "gain": -6, "fade": 0.3}),
        two(HOME, "マジで！？\n*神*！！", ("dance_cute_dog", 950), TOMO, 2.0, "友だち", size=130, se="jan"),
        two(HOME, "……じゃあ浮いたお金で\nもう1回……。", ("cocky_dj_cat", 1000), TOMO, 2.2, "友だち"),
        they(HOME, "*回すな*。", ("cocky_dj_cat", 1000), TOMO, 1.8, "友だち", size=220, shake=True, se="tsukkomi_bishi"),
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
