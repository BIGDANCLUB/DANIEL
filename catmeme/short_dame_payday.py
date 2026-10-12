"""ダメ人間の猫ミーム #2「給料日から3日で金がない」（台本：scripts/dame_02_payday.md）。作りは short_dame_template.py と同じ。

python3 catmeme/short_dame_payday.py → out/short_dame_payday.mp4
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M
from short_dame_rent import one, two

HERE = M.HERE
NAME = "short_dame_payday"
TITLE = ("とあるダメ人間", "給料日から3日で金がない")
LIME = M.LIME
NORA = os.path.join(S.BGM, "野良猫は宇宙を目指した.mp3")
LOFI = os.path.join(S.BGM, "2_23_AM.mp3")
SPOT, HOME, YAKI, CONV, PHONE = "bg06_spotlight", "bg14_home_night", "bg22_yakiniku", "bg15_convenience", "bg26_phone_alert"

# 登場人物（主人公以外。生き物だけ）
KOUHAI = ("dance_cute_dog", 950)              # 後輩（浮かれる）
TENIN = ("call_customer_service_cat", 1000)   # 店員
HAHA = ("stare_standing_marmot", 950)         # 母ちゃん（無言の圧）
GOJO = ("showoff_gojo_cosplay_cat", 1000)     # 後輩の前でカッコつける主人公


def they(bg, say, me, other, dur, label, **kw):
    """相手役がしゃべるカット（黄緑の文字・相手の音を鳴らす）。"""
    return two(bg, say, me, other, dur, label, speaker=1, col=LIME, **kw)


def cuts():
    return [
        one(SPOT, "給料日から*3日*で\n*残高ゼロ*。", "despair_dramatic_kitten", 3.0, size=120, shake=True,
            se=["jan", "explosion_chudoon"], bgm={"file": NORA, "gain": -6}),
        one(HOME, "……いや、ちゃんと\n計画はあったんだよ。", "sad_black_dog", 2.6, se="whoosh_shu"),
        one(HOME, "給料日！！\n今月こそ*貯金*するぞ！", "joy_happy_happy_happy_cat", 2.4, se="fanfare_pararappara"),
        they(YAKI, "先輩、今日\n焼肉っすよね？", GOJO, KOUHAI, 2.4, "後輩", se="pikon"),
        two(YAKI, "おう、*全部おごり*だ！", GOJO, KOUHAI, 2.2, "後輩", size=120, se="shine_kira_01"),
        they(YAKI, "先輩マジ神っす！", GOJO, KOUHAI, 2.0, "後輩", size=120),
        they(YAKI, "お会計\n*3万8千円*です", GOJO, TENIN, 2.4, "店員", size=120, se="price_display"),
        two(YAKI, "……カードで。", GOJO, TENIN, 1.8, "店員", size=150),
        one(CONV, "2日目。\nちょっとだけコンビニ。", "happy_girlfriend_dance_cat", 2.2, se="store_famima_entry_chime_arrive_welcome"),
        one(CONV, "新作スイーツ、新作ポテチ、\n*新作全部*。", "eat_pop_cat", 2.4, se="eat_paku"),
        they(CONV, "お会計\n*4千2百円*です", ("eat_pop_cat", 1000), TENIN, 2.2, "店員", size=120, se="price_display"),
        one(PHONE, "3日目。\n……スマホ代の引き落とし。", "peek_what_happen_cat", 2.4, se="pc_warning"),
        one(PHONE, "残高 *82円*", "surprise_big_pupils_cat", 2.0, size=160, shake=True, se="explosion_dokaan",
            bgm={"file": LOFI, "gain": -6, "fade": 0.3}),
        one(HOME, "は？", "huh_huh_cat", 1.6, size=230, se="question_hatena_maou"),
        one(HOME, "ちょっと母ちゃんに\n電話しよ……。", "confused_i_dont_know_cat", 2.2, se="button_09"),
        they(HOME, "あんた、給料日って\n*3日前*じゃなかった？", ("confused_i_dont_know_cat", 1000), HAHA, 2.6, "母ちゃん"),
        two(HOME, "……3日*後*です。", ("sad_black_dog", 950), HAHA, 2.0, "母ちゃん", size=140, se="tear_drop"),
        they(HOME, "自分で\nなんとかしなさい。", ("sad_black_dog", 950), HAHA, 2.2, "母ちゃん", se="kon"),
        one(HOME, "……。", "blank_black_cat_zoning_out", 1.2, size=200),
        one(HOME, "残り27日、\n*もやし*でいける。", "flip_emo_cat_hair", 2.4, se="sword_shakiin"),
        they(HOME, "先輩！給料日、\nまた焼肉っすよね！", ("cocky_dj_cat", 1000), KOUHAI, 2.4, "後輩", se="pikon",
             bgm={"file": NORA, "gain": -6, "fade": 0.3}),
        two(HOME, "おう、*全部おごり*だ！", ("cocky_dj_cat", 1000), KOUHAI, 2.4, "後輩", size=120, shake=True, se="tv_dokkiri_tettere"),
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
