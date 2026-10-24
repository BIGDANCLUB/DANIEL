"""ショート25c：今日こそ定時退社 ある会社員の1日（world_short.py・10/24 参考「定時で帰る予定 会社員の1日」の作りをまねる）。59.9秒。

python3 catmeme/short_25c_teiji.py → out/short_25c_teiji.mp4
- 作り（時刻の札・同僚／上司／取引先／友達・スマホのトーク画面・最後に予定の場所で「帰れない」）は参考どおり
- 予定は映画ではなく「友達と焼肉」。帯・セリフは参考と変える。会話は作り話
- BGM なし（10/23 ルール）
"""
import os

import world_short as Wd

OFF, YAKI = "bg25_office_desk", "bg22_yakiniku"


def cuts():
    t, s = Wd.talk, Wd.solo

    def tm(x):
        return dict(tag=x, tag_style="time")

    night = dict(dark=0.35)
    cs = [
        s(OFF, say="今日こそ\n*定時*で帰る！", cat="dance_tabby_standing_cat", lines=True, se="don_hit", **tm("09:00")),
        t(OFF, say="気合い入ってるね\n何かあるの？", left="meow_gray_white_kitten", right="stare_interviewer_cat", who="R",
          rlabel="同僚", **tm("09:00")),
        t(OFF, say="19時から\n友達と*焼肉*！", left="yell_orange_fat_cat", right="stare_interviewer_cat", who="L", rlabel="同僚",
          **tm("10:00")),
        t(OFF, say="いいなぁ！\nそれは絶対帰らなきゃ", left="yell_orange_fat_cat", right="happy_girlfriend_dance_cat", who="R",
          rlabel="同僚", **tm("10:00")),
        s(OFF, say="午前の仕事\nもう*ほぼ終わり*！", cat="work_typing_cat", **tm("11:30")),
        t(OFF, say="今日めちゃくちゃ\n調子いいじゃん", left="showoff_gojo_cosplay_cat", right="happy_girlfriend_dance_cat", who="R",
          rlabel="同僚", **tm("12:30")),
        t(OFF, say="ごめん、この資料\n*今日中*にお願い", left="stare_tabby_wide_eyes_cat", right="rizz_cat_rizz", who="R",
          rlabel="上司", **tm("13:00")),
        t(OFF, say="…了解です！\nすぐやります", left="calmdown_dancing_cat", right="rizz_cat_rizz", who="L", rlabel="上司",
          **tm("13:00")),
        t(OFF, say="仕事ふえたけど\n間に合う？", left="calmdown_dancing_cat", right="peek_what_happen_cat", who="R", rlabel="同僚",
          **tm("13:30")),
        t(OFF, say="午前に*貯金*あるから\nまだ余裕！", left="showoff_gojo_cosplay_cat", right="peek_what_happen_cat", who="L",
          rlabel="同僚", **tm("13:30")),
        t(OFF, say="*5分*だけ\n相談いいかな？", left="meow_gray_white_kitten", right="talk_orange_white_sitting_cat", who="R",
          rlabel="上司", **tm("14:00")),
        t(OFF, say="5分なら！", left="laugh_laughing_dog", right="talk_orange_white_sitting_cat", who="L", rlabel="上司",
          **tm("14:00")),
        t(OFF, say="……というわけで\nよろしくね", left="blank_black_cat_zoning_out", right="talk_orange_white_sitting_cat", who="R",
          rlabel="上司", **tm("15:00")),
        t(OFF, say="5分じゃなくて\n*1時間*たってる…", left="stare_big_eyes_tabby_kitten", right="talk_orange_white_sitting_cat",
          who="L", rlabel="上司", **tm("15:00")),
        s(OFF, say="電話だ…\nいやな予感", cat="call_customer_service_cat", se="pinpon_notice", **tm("15:30")),
        t(OFF, say="納品、*明日の朝*に\n早められます？", left="confused_i_dont_know_cat", right="meow_ragdoll_chubby_cat", who="R",
          rlabel="取引先", **tm("15:30")),
        t(OFF, say="い、今から\nですか……？", left="despair_dramatic_kitten", right="meow_ragdoll_chubby_cat", who="L",
          rlabel="取引先", **tm("15:30")),
        Wd.phone(OFF, "友達", [("friend", "焼肉\n間に合いそう？", "16:00")], friend_icon="eat_pop_cat", cat="stare_tabby_wide_eyes_cat", dur=2.6),
        Wd.phone(OFF, "友達", [("friend", "焼肉\n間に合いそう？", "16:00"), ("me", "ちょっとピンチ\nでも行ける！！", "16:05")], friend_icon="eat_pop_cat",
                 cat="showoff_gojo_cosplay_cat", dur=2.8),
        t(OFF, say="まだ帰らないの？\nお先に〜", left="sulk_hungry_cat", right="leave_cat_leaves_home", who="R", rlabel="同僚",
          **tm("17:30")),
        s(OFF, say="あと少し…\nあと少しだけ…", cat="work_dog_staring_computer", dur=2.2, **tm("18:00")),
        s(OFF, say="よし……\n*終わった*！", cat="work_typing_cat", dur=2.4, se="pinpoon_correct", **tm("18:40")),
        s(YAKI, say="もう*乾杯*\nしちゃったよ？", cat="eat_pop_cat", label="友達", dur=2.6, se="pikon", **tm("19:00")),
        t(YAKI, say="帰れなぁぁい！", left="sad_banana_cat_cry", right="eat_pop_cat", who="L", rlabel="友達", dur=3.0, lscale=1.25, rscale=0.8,
          se="chin_bell_failure_sad_ending", **tm("19:00")),
    ]
    for c in cs[-5:]:   # 夕方からは少し暗く
        if c["bg"] == OFF:
            c.update(night)
    return cs


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}今日こそ定時退社", 140, Wd.BLACK, 300), ("{r}ある会社員の1日", 120, Wd.WHITE, 440)], 206, 516),
           os.path.join(Wd.HERE, "out", "short_25c_teiji.mp4"), os.path.join(Wd.HERE, "out", "short_25c_teiji_preview"))
