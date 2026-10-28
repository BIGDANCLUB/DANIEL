"""ショート41：年末調整の時期のリアル（salary_short.py）。保険の控除証明書が見つからない・毎年同じ書類で迷う。59.9秒。"""
import salary_short as S
from salary_short import s, t, OFF, OFF2, ROOM, NIGHT

cs = [
    t(OFF, "11月1日", "年末調整の書類\n*今月中*に出してね", "work_typing_cat", "stare_big_eyes_tabby_kitten", who="L", ll="総務", se="pinpon_notice"),
    t(OFF, "11月1日", "はーい\n（まだ1か月ある）", "work_typing_cat", "slack_nail_filing_cat", ll="総務"),
    s(ROOM, "11月20日", "そろそろ\nやるか…", "think_bike_front_seat_cat", lines=True),
    s(ROOM, "11月20日", "えっと…\n*扶養控除*ってなに？", "confused_i_dont_know_cat", se="question_mark_pop_confused_huh"),
    s(ROOM, "11月20日", "去年も\n同じところで迷った", "sleepy_old_memories_cat"),
    s(ROOM, "11月20日", "生命保険の\n*控除証明書*がいる", "read_book_orange_kitten"),
    s(ROOM, "11月20日", "……どこ？", "huh_huh_cat", big_say=True, d=2.0, se="question_mark_pop_confused_huh"),
    s(ROOM, "11月21日", "郵便物の山を\nぜんぶひっくり返す", "fight_cat_fight", se="explosion_doon"),
    s(ROOM, "11月21日", "チラシ・チラシ\nピザのメニュー", "blank_black_cat_zoning_out"),
    s(ROOM, "11月22日", "まさか\n*捨てた*…？", "despair_dramatic_kitten"),
    t(OFF, "11月28日", "書類まだの人\n*あと2日*です", "rage_talking_cat", "sad_banana_cat_cry", who="L", ll="総務"),
    s(ROOM, "11月28日", "保険会社に電話して\n*再発行*をお願い", "call_customer_service_cat", se="pi"),
    s(ROOM, "11月30日", "とどいた！\n*ギリギリ*間に合う", "happy_chipi_chapa_cat", se="pinpoon_correct"),
    t(OFF2, "11月30日", "はい受け取りました\n…あ ここ*ハンコ*がない", "stare_interviewer_cat", "stare_tabby_wide_eyes_cat", who="L", ll="総務"),
    s(OFF2, "11月30日", "……", "sad_black_dog", d=1.8),
    s(NIGHT, "12月", "引き出しを片づけたら", "peek_what_happen_cat", dark=0.3),
    s(NIGHT, "12月", "*控除証明書*\n出てきた", "surprise_big_pupils_cat", se="question_mark_pop_confused_huh", dark=0.3),
    s(NIGHT, "12月", "みんなも\n大事な書類は\n*1か所にまとめよう*", "realize_wet_cat_stare", dark=0.3),
]

if __name__ == "__main__":
    S.run("short_41_nenmatsu", "年末調整の時期", "会社員のリアル", cs)
