"""ショート38：リモートワークの1日（salary_short.py）。カメラオフで寝ぐせ → 急に「カメラつけて」。59.9秒。"""
import salary_short as S
from salary_short import s, t, ROOM, NIGHT

cs = [
    # 10/28 ユーザー指定：冒頭に、エフェクト全力で前日深夜まで暴飲暴食＆ゲームしている場面
    s(NIGHT, "前日 23:00", "明日はリモート\n*夜ふかし*し放題！", "dance_edm_cat", lines=True, hype=True, se=["air_horn"]),
    s(NIGHT, "前日 0:30", "ピザ・ポテチ・コーラ\n*暴飲暴食*", "eat_crunchy_cat_luna", lines=True, hype=True,
      se=["eat_paku", {"f": "drink_gulp_gokugoku_thirsty_chug", "at": 0.8}]),
    s(NIGHT, "前日 2:00", "ゲームも\n*あと1戦だけ*", "angry_shooting_cat", lines=True, hype=True, se=["boot_game_like"]),
    s(NIGHT, "前日 4:00", "気づけば\n*朝の4時*", "stare_big_eyes_tabby_kitten", lines=True, hype=True, se=["shock_piano"]),
    s(ROOM, "8:58", "始業2分前に\n*起床*", "sleep_sleeping_cat", lines=True, se="cuckoo_pappo"),
    s(ROOM, "8:59", "パジャマのまま\nパソコンを開く", "work_typing_cat"),
    s(ROOM, "9:00", "朝会は\n*カメラオフ*で参加", "slack_nail_filing_cat", se="pikon"),
    t(ROOM, "9:00", "みなさん\nおはようございます", "stare_interviewer_cat", "sleepy_sleepy_cat", who="L", ll="上司"),
    t(ROOM, "9:00", "おはようございま〜す\n（布団の中から）", "stare_interviewer_cat", "sleepy_old_memories_cat", ll="上司"),
    s(ROOM, "10:30", "洗濯機を回しながら\n資料づくり", "work_dog_staring_computer"),
    s(ROOM, "11:00", "チャットの返事は\n*スマホ*で", "call_customer_service_cat"),
    s(ROOM, "12:00", "お昼は冷凍パスタ\n*移動0歩*", "eat_pop_cat", se="eat_paku"),
    s(ROOM, "13:00", "ちょっとだけ\n横になろう…", "sleepy_sleepy_cat"),
    s(ROOM, "13:40", "*40分*\nたってた", "stare_tabby_wide_eyes_cat", se="question_mark_pop_confused_huh"),
    t(ROOM, "14:00", "取引先との会議\n入ります", "talk_orange_white_sitting_cat", "think_bike_front_seat_cat", who="L", ll="上司"),
    t(ROOM, "14:00", "（今日も\nカメラオフでいける）", "talk_orange_white_sitting_cat", "showoff_gojo_cosplay_cat", ll="上司"),
    t(ROOM, "14:05", "あ 今日は先方がいるから\n全員*カメラつけて*", "rage_talking_cat", "stare_big_eyes_tabby_kitten", who="L", ll="上司",
      se="pinpon_notice"),
    s(ROOM, "14:05", "……え", "huh_huh_cat", big_say=True, d=2.0, se="question_mark_pop_confused_huh"),
    s(ROOM, "14:05", "寝ぐせ\n*爆発中*", "despair_dramatic_kitten", se="explosion_doon"),
    s(ROOM, "14:06", "うしろに\n*洗濯物の山*", "surprise_big_pupils_cat"),
    s(ROOM, "14:06", "急いで\nパーカーをかぶる", "leave_cat_leaves_home", se="dash_super_fast"),
    s(ROOM, "14:06", "背景を\n*ぼかし*にする", "work_typing_cat", se="pikon"),
    t(ROOM, "14:07", "……すみません\n遅れました", "stare_interviewer_cat", "blank_black_cat_zoning_out", ll="上司"),
    t(ROOM, "14:07", "なんで\nフードかぶってるの？", "glare_disgusted_cat", "blank_black_cat_zoning_out", who="L", ll="上司"),
    t(ROOM, "14:07", "……寒くて", "glare_disgusted_cat", "sad_banana_cat_cry", ll="上司", d=2.0),
    s(NIGHT, "18:00", "明日から\n*ちゃんと着がえよう*", "realize_wet_cat_stare"),
    s(ROOM, "翌朝 8:58", "始業2分前に\n*起床*", "sleep_sleeping_cat", se="cuckoo_pappo"),
]

if __name__ == "__main__":
    S.run("short_38_remote", "カメラオフの油断", "リモートワークの1日", cs)
