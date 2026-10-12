"""ダメ人間の猫ミーム #4「遅刻の言い訳が雑すぎる」（台本：scripts/dame_04_late.md）。作りは short_dame_template.py と同じ。

python3 catmeme/short_dame_late.py → out/short_dame_late.mp4
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M
from short_dame_payday import they
from short_dame_rent import one, two

HERE = M.HERE
NAME = "short_dame_late"
TITLE = ("とあるダメ人間", "遅刻の言い訳が雑すぎる")
NORA = os.path.join(S.BGM, "野良猫は宇宙を目指した.mp3")
LOFI = os.path.join(S.BGM, "2_23_AM.mp3")
SPOT, HOME, OUT_, OFFICE = "bg06_spotlight", "bg14_home_night", "bg01_campus", "bg25_office_desk"

# 登場人物（主人公以外。生き物だけ）
JOUSHI = ("stare_standing_marmot", 950)   # 上司（無言の圧）
DOURYOU = ("laugh_laughing_dog", 1000)     # 同僚（笑ってくる）
SAD = ("sad_black_dog", 950)
HUH = ("confused_i_dont_know_cat", 1000)


def cuts():
    return [
        one(SPOT, "遅刻を*電車*のせいにしたら\n俺、*自転車通勤*だった。", "confused_i_dont_know_cat", 3.4, size=100, shake=True,
            se=["jan", "explosion_chudoon"], bgm={"file": NORA, "gain": -6}),
        one(HOME, "……ん？", "sleep_sleeping_cat", 1.6, size=200, se="cuckoo_pappo"),
        one(HOME, "*9時始業*……。", "surprise_big_pupils_cat", 1.8, size=150),
        one(HOME, "あと*10分*！？", "despair_dramatic_kitten", 2.0, size=160, shake=True, se="explosion_dokaan"),
        one(HOME, "無理無理無理！", "leave_cat_leaves_home", 1.8, size=140, se="run_away_zazaza_fast"),
        one(OUT_, "とりあえず出発！", "ride_kitten_bike", 2.0, size=130, se="dash_super_fast"),
        one(OUT_, "……言い訳、\n考えないと。", "think_bike_front_seat_cat", 2.2, se="thinking_time"),
        one(OUT_, "*電車遅延*でいっか。", "flip_emo_cat_hair", 2.0, size=130, se="shine_kira_01"),
        two(OFFICE, "すいません！\n*電車*が遅れて……。", SAD, JOUSHI, 2.6, "上司", bgm={"file": LOFI, "gain": -6, "fade": 0.3}),
        they(OFFICE, "……。", SAD, JOUSHI, 1.4, "上司", size=200),
        they(OFFICE, "お前、\n*自転車通勤*だよな？", SAD, JOUSHI, 2.4, "上司", size=120, se="game_aceattorney_desk_slam"),
        two(OFFICE, "……。", ("blank_black_cat_zoning_out", 1000), JOUSHI, 1.4, "上司", size=200),
        two(OFFICE, "あ、*自転車*が\n遅れて……。", HUH, JOUSHI, 2.4, "上司", size=120, se="boing_fail"),
        they(OFFICE, "自転車は\n遅れない。", HUH, JOUSHI, 2.0, "上司", size=130, se="buzzer_wrong"),
        they(OFFICE, "ヘルメット、\nかぶったままだし。", HUH, DOURYOU, 2.4, "同僚"),
        they(OFFICE, "*寝ぐせ*も\nついてるし。", HUH, DOURYOU, 2.2, "同僚", size=120, se="silly"),
        two(OFFICE, "……すいません、\n*寝坊*です。", SAD, JOUSHI, 2.4, "上司", se="tear_drop"),
        they(OFFICE, "最初から\nそう言え。", SAD, JOUSHI, 2.0, "上司", size=130, se="kon"),
        one(OFFICE, "はい……。", "sulk_hungry_cat", 1.6, size=160, se="deflate_hyororo"),
        one(HOME, "よし、明日は\n*目覚まし5個*。", "showoff_gojo_cosplay_cat", 2.4, size=120, se="sword_shakiin",
            bgm={"file": NORA, "gain": -6, "fade": 0.3}),
        one(HOME, "……ん？", "sleep_sleeping_cat", 1.6, size=200, se="cuckoo_pappo"),
        one(HOME, "*9時15分*。", "surprise_big_pupils_cat", 1.8, size=170, shake=True, se="explosion_dokaan"),
        one(HOME, "……言い訳、\nなんにしよ。", "realize_wet_cat_stare", 2.4, se="tv_dokkiri_tettere"),
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
