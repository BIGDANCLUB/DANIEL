"""ショート42：残業時間でわかる 会社員の顔つき（income_short.py・年収別ショートと同じ作り）。59.9秒。
区切り：残業0時間・20時間・45時間・80時間、最後は「みんなも働きすぎに気をつけよう」。
45時間は36協定の上限の原則、80時間は過労死ラインと呼ばれる目安。"""
import os

import income_short as I
import world_short as Wd

OFF, NIGHT, ROOM, IZA = "bg25_office_desk", "bg14_home_night", "bg02_room", "bg13_izakaya"


def cuts():
    t = I.talk
    return [
        I.intro(IZA, "残業0時間", "定時ダッシュ！", "dance_tabby_standing_cat"),
        t(IZA, "残業0時間", "仕事終わりに\nジム行こうぜ！", "excited_hodomoe_city_cat", "dance_tabby_standing_cat", who="L", label="同僚"),
        t(IZA, "残業0時間", "そのあと\n飲みにも行こう！", "excited_hodomoe_city_cat", "happy_girlfriend_dance_cat"),
        t(IZA, "残業0時間", "肌ツヤ\n最高", "happy_hamster_open_arms", "showoff_gojo_cosplay_cat"),
        I.intro(OFF, "残業20時間", "ちょっと疲れてきた", "think_bike_front_seat_cat"),
        t(OFF, "残業20時間", "週末なにする？", "talk_orange_white_sitting_cat", "think_bike_front_seat_cat", who="L", label="同僚"),
        t(OFF, "残業20時間", "土曜は\n寝て終わる", "talk_orange_white_sitting_cat", "sleepy_sleepy_cat"),
        t(OFF, "残業20時間", "でもまだ\n平気", "stare_interviewer_cat", "calmdown_dancing_cat"),
        I.intro(OFF, "残業45時間", "上限ギリギリ", "blank_black_cat_zoning_out"),
        t(OFF, "残業45時間", "今日のお昼\n何食べた？", "peek_what_happen_cat", "blank_black_cat_zoning_out", who="L", label="同僚"),
        t(OFF, "残業45時間", "……え\n食べたっけ", "peek_what_happen_cat", "confused_i_dont_know_cat"),
        t(OFF, "残業45時間", "目の下の\nクマがすごい", "surprise_big_pupils_cat", "sleepy_old_memories_cat", who="L", label="同僚"),
        I.intro(NIGHT, "残業80時間", "危険ライン", "despair_dramatic_kitten", se="explosion_doon"),
        t(NIGHT, "残業80時間", "家に帰っても\n寝るだけ", "stare_tabby_wide_eyes_cat", "sleep_sleeping_cat"),
        t(NIGHT, "残業80時間", "休みの日も\n仕事の夢を見る", "stare_tabby_wide_eyes_cat", "sad_banana_cat_cry"),
        t(NIGHT, "残業80時間", "顔色悪いよ\n休んで！", "rage_talking_cat", "sad_black_dog", who="L", label="同僚"),
        I.intro(ROOM, "まとめ", "体がいちばん大事", "realize_wet_cat_stare", se="pinpoon_correct"),
        t(ROOM, "まとめ", "しんどい時は\nだれかに相談しよう", "talk_orange_white_sitting_cat", "stare_interviewer_cat", who="L", label="同僚"),
        t(ROOM, "まとめ", "みんなも\n働きすぎに気をつけよう", "happy_hamster_open_arms", "dance_three_kittens"),
    ]


def fit(cs):
    k = I.TOTAL / sum(c["dur"] for c in cs)
    for c in cs:
        c["dur"] *= k
    return cs


if __name__ == "__main__":
    I.run(fit(Wd.dedupe(cuts())), "残業時間でわかる", "会社員の顔つき", os.path.join(I.HERE, "out", "short_42_zangyo_jikan.mp4"),
          os.path.join(I.HERE, "out", "short_42_zangyo_jikan_preview"))
