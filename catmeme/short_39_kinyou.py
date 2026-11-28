"""ショート39：金曜日の会社員の1日（salary_short.py）。朝からうきうき → 夕方に急ぎの仕事。59.9秒。"""
import salary_short as S
from salary_short import s, t, OFF, OFF2, TRAIN, IZAKAYA

cs = [
    s(TRAIN, "7:30", "今日は\n*金曜日*！", "dance_tabby_standing_cat", lines=True, se="jan"),
    s(TRAIN, "7:40", "満員電車も\nなぜか平気", "happy_hamster_open_arms"),
    t(OFF, "9:00", "おはよう\n今日元気だね", "stare_big_eyes_tabby_kitten", "happy_girlfriend_dance_cat", who="L", ll="同僚"),
    t(OFF, "9:00", "*金曜日*だからね！", "stare_big_eyes_tabby_kitten", "dance_wop_cat", ll="同僚"),
    s(OFF, "10:00", "メールの返事も\n*秒*で終わる", "work_typing_cat"),
    s(OFF, "12:00", "お昼は\nちょっといいランチ", "eat_pop_cat", se="eat_paku"),
    t(OFF, "13:00", "今夜飲みに\n行かない？", "talk_orange_white_sitting_cat", "excited_hodomoe_city_cat", who="L", ll="同僚"),
    t(OFF, "13:00", "行く！！\n*19時*ね！", "talk_orange_white_sitting_cat", "yell_orange_fat_cat", ll="同僚", se="pikon"),
    s(OFF, "15:00", "今週の仕事\nもう*ほぼ終わり*", "showoff_gojo_cosplay_cat"),
    s(OFF, "16:00", "あと1時間で\n週末…", "calmdown_dancing_cat"),
    s(OFF, "16:30", "時計ばかり\n見てしまう", "peek_what_happen_cat"),
    t(OFF2, "16:55", "ちょっといい？", "rizz_cat_rizz", "stare_tabby_wide_eyes_cat", who="L", ll="上司", se="pinpon_notice"),
    s(OFF2, "16:55", "いやな予感…", "blank_black_cat_zoning_out", d=2.0),
    t(OFF2, "16:56", "取引先から\n*急ぎの修正*がきた", "rizz_cat_rizz", "surprise_big_pupils_cat", who="L", ll="上司"),
    t(OFF2, "16:56", "*月曜の朝*までに\nお願いできる？", "stare_interviewer_cat", "despair_dramatic_kitten", who="L", ll="上司"),
    s(OFF2, "16:57", "……月曜の朝って\nことは", "think_bike_front_seat_cat"),
    s(OFF2, "16:57", "*今日*やるしかない", "sad_banana_cat_cry", se="chin_bell_failure_sad_ending"),
    t(OFF, "18:50", "まだ終わらない？\n先に行ってるね", "leave_cat_leaves_home", "work_dog_staring_computer", who="L", ll="同僚"),
    s(OFF, "21:00", "やっと\n*終わった*…", "sleepy_old_memories_cat", dark=0.3),
    s(IZAKAYA, "21:30", "みんな\nもう帰ってた", "sad_black_dog", dark=0.2),
    s(IZAKAYA, "21:31", "金曜日の\n*うきうき*返して…", "despair_dramatic_kitten", big_say=False),
]

if __name__ == "__main__":
    S.run("short_39_kinyou", "うきうきの金曜日", "会社員の1日", cs)
