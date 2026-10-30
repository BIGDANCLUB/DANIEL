"""ショート53：4人の飲み会でオールしたら 朝に向けてだんだんおかしくなっていく（salary_short.py・10/30 ユーザー指定）。59.9秒。
4人（先輩・同期・後輩・幹事）がそろう場面は4匹ならべる。時刻の札は 19:00 → 翌朝 6:00。
「!?」はコナン、「え…」はポーン（ショートのルールで自動）。最後は「みんなも飲みすぎに気をつけよう」で締める。BGM なし
"""
import world_short as Wd
import salary_short as S
from salary_short import s, t

IZA, LOUNGE, STREET, NIGHT_ST, STATION = "bg98_izakaya_night", "bg100_lounge_night", "bg76_roppongi_night", "bg51_night_street", \
    "bg54_station_crowd_map"
M = "scream_standing_marmot"


def g4(bg, tag, say, cats, se=None, voice=0, **kw):
    """4人そろう場面：4匹を横にならべて、名札をつける。voice の猫だけ鳴らす。"""
    c = s(bg, tag, say, cats[0], se=se, **kw)
    # 横1列に4匹（字幕の下・名札は猫の足もと）
    c["cats"] = [Wd._cat(a, x, 620, 268, 1600, lab, mute=k != voice)
                 for k, (a, x, lab) in enumerate(zip(cats, (138, 406, 674, 942), ("先輩", "同期", "後輩", "幹事")))]
    return c


cs = [
    g4(IZA, "19:00", "4人で\n*かんぱーい!!*", ("happy_hamster_open_arms", "dance_tabby_standing_cat", "dance_happy_banana_cat",
                                             "happy_chipi_chapa_cat"), se="jan", lines=True),
    t(IZA, "20:30", "今日は\n*終電で帰ろうね*", "talk_orange_white_sitting_cat", "stare_big_eyes_tabby_kitten", who="L", ll="幹事", rl="後輩"),
    s(IZA, "23:50", "*終電*\nもう出てた!?", "stare_tabby_wide_eyes_cat", label="同期"),
    g4(LOUNGE, "0:30", "じゃあ\n*朝までカラオケ!!*", ("dance_edm_cat", "dance_wop_cat", "dance_three_kittens", "dance_orange_gray_cats"),
       se="air_horn", voice=3, lines=True),
    s(LOUNGE, "1:30", "先輩が\n*同じ歌を4回目*", "yell_orange_fat_cat", label="先輩"),
    s(LOUNGE, "2:30", "同期が\n*急に泣きだす*", "sad_banana_cat_cry", label="同期"),
    s(LOUNGE, "3:00", "後輩が\n*タンバリンで踊りだす*", "spin_spinning_cat", label="後輩", se="boing_02"),
    s(LOUNGE, "3:30", "幹事は\n*ソファで爆睡*", "sleep_sleeping_cat", label="幹事"),
    g4(LOUNGE, "4:00", "なぜか\n*4人で円陣*", ("dance_three_kittens", "happy_hamster_open_arms", "dance_tabby_standing_cat", "dance_happy_banana_cat"),
       se="cheer_applause", lines=True),
    s(NIGHT_ST, "4:30", "外に出て\n*朝日に叫ぶ*", M, d=1.3),
    g4(NIGHT_ST, "5:00", "*ラーメン*で\nしめよう!!", ("eat_pop_cat", "eat_chips_cat", "eat_crunchy_cat_luna", "money_counting_orange_cat"),
       se="eat_paku", voice=2),
    s(STATION, "5:30", "始発で\n*全員爆睡*", "sleepy_sleepy_cat"),
    s(STATION, "6:00", "……え\nここ終点？", "sad_looking_away_tabby", label="後輩"),
    s(STREET, "6:30", "今日\n*月曜日*!?", "scream_phone_orange_cat", label="同期"),
    s(STREET, "6:30", "みんなも\n*飲みすぎに気をつけよう*", "realize_wet_cat_stare"),
]

if __name__ == "__main__":
    S.run("short_53_nomikai", "飲み会でオール", "朝までの4人のようす", cs)
