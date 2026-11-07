"""ショート52：ブラック企業 連勤がふえるとこうなる（salary_short.py・リモートワークと同じ作り・10/30 ユーザー指定）。59.9秒。
14連勤まではどんどん疲れていく → 30・60・100連勤になると逆にハイになって元気に奇行に走る、を連勤の札ごとに見せる。
実在の会社名は出さない。最後は「みんなも休もう」で締める（ショートの締めのルール）。マーモットは叫ぶ場面だけ・1.3秒
"""
import salary_short as S
from salary_short import s, OFF, NIGHT

M = "scream_standing_marmot"

cs = [
    s(OFF, "1連勤目", "今日も\n*がんばるぞ！*", "talk_orange_white_sitting_cat", lines=True, se="jan"),
    s(OFF, "3連勤目", "ちょっとだけ\n眠い", "work_typing_cat"),
    s(OFF, "5連勤目", "週末が\n*待ち遠しい*", "sleepy_sleepy_cat"),
    s(OFF, "7連勤目", "あれ\n*土日*ってなんだっけ", "sleepy_old_memories_cat", se="question_mark_pop_confused_huh"),
    s(OFF, "10連勤目", "コーヒー\n*5杯目*", "blank_black_cat_zoning_out", se="drink_gulp_gokugoku_thirsty_chug"),
    s(NIGHT, "14連勤目", "もう\n*限界*……", "despair_dramatic_kitten", se="chin_bell_failure_sad_ending", dark=0.3),
    s(OFF, "30連勤目", "なんか\n*楽しくなってきた!!*", "dance_filmed_by_gray_cat", lines=True, se="explosion_chudoon"),
    s(OFF, "30連勤目", "コピー機に\n*話しかける*", "spin_spinning_cat", se="boing_02"),
    s(OFF, "60連勤目", "会議中に\n*踊りだす*", "dance_edm_cat", lines=True, se="air_horn"),
    s(OFF, "60連勤目", "上司に\n*ハイタッチ*", "happy_hamster_open_arms", se="tsukkomi_bashi"),
    s(NIGHT, "100連勤目", "夜中のオフィスで", M, d=1.3),
    s(NIGHT, "100連勤目", "*100連勤*\nおめでとう自分!!", "dance_three_kittens", lines=True, se="fanfare_pararappara"),
    s(NIGHT, "100連勤目", "体はとっくに\n*限界をこえている*", "realize_wet_cat_stare", dark=0.3),
    s(NIGHT, "101日目", "みんなも\n*休めるときは休もう*", "sleep_sleeping_cat", dark=0.3),
]

if __name__ == "__main__":
    S.run("short_52_renkin", "ブラック企業", "連勤がふえるとこうなる", cs)
