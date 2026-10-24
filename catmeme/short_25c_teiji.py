"""ショート25c：絶対定時で帰る日 サラリーマンの1日（world_short.py・10/24 参考「定時で帰る予定 会社員の1日」を1カットずつまねる）。59.9秒。

python3 catmeme/short_25c_teiji.py → out/short_25c_teiji.mp4
- 10/24 ユーザー指定「口調や素材の使い方をもっと厳密に」：時刻の札・カットの順番と長さの比率・役名の札（私は札なし、
  相手だけ「同僚」「上司」「取引先」「友達」）・スマホを持つ猫・友達とのトーク画面・夕方の仕事チャット・最後の「帰れねええ」まで参考どおり。
  予定は映画ではなく「焼肉」、打ち合わせは「15分」ではなく「10分」。文は書きかえる
- 実在のアプリの画面やロゴは出さない（仕事チャットは緑の枠のふきだしだけ）
- BGM なし（10/23 ルール）
"""
import os

import world_short as Wd

OFF, OFF2, YAKI = "bg25_office_desk", "bg78_agency_office", "bg22_yakiniku"
K = 59.9 / 66.5   # 参考の長さ（66.5秒）→ 59.9秒


def cuts():
    def s(tm, d, say, cat, bg=OFF, **kw):
        return Wd.solo(bg, tm, say, cat, dur=d * K, tag_style="time", **kw)

    def t(tm, d, say, left, right, rl, bg=OFF, ll=None, **kw):
        return Wd.talk(bg, tm, say, left, right, dur=d * K, llabel=ll, rlabel=rl, tag_style="time", **kw)

    def ph(d, msgs, cat=None, say=None):
        c = Wd.phone(OFF, "友達", msgs, cat=cat, say=say, dur=d * K, friend_icon="dance_tabby_standing_cat",
                     me_icon="spit_not_my_taste_cat", se="pikon" if not cat else None)
        return c

    m1 = ("friend", "今日の焼肉\n間に合いそ？", "15時30分")
    m2 = ("me", "けっこうピンチだけど\nたぶん行ける！！", "15時40分")
    night = dict(dark=0.3)
    return [
        s("09:00", 2.5, "今日はなにがあっても\n*定時*で帰る！", "mock_swinging_cat", lines=True, se="don_hit"),
        t("10:00", 2.5, "今日なにか\n予定あるの？", "mock_swinging_cat", "talk_orange_white_sitting_cat", "同僚"),
        t("10:00", 3.0, "19時から\n*焼肉*行くんだ！！！", "yell_orange_fat_cat", "talk_orange_white_sitting_cat", "同僚", who="L"),
        t("10:00", 2.5, "いいね～\n間に合うといいね", "yell_orange_fat_cat", "rage_talking_cat", "同僚"),
        s("11:30", 2.5, "午前の仕事\nもう*ほとんど*片づいた！", "work_dog_staring_computer"),
        t("11:30", 3.0, "今日*絶好調*\nじゃん！！", "realize_wet_cat_stare", "happy_chipi_chapa_cat", "同僚"),
        t("13:00", 3.0, "ごめん、この資料\n*今日中*に頼む", "rage_talking_cat", "work_typing_cat", None, ll="上司", who="L"),
        t("13:00", 3.0, "了解です！\nすぐやります！", "rage_talking_cat", "happy_girlfriend_dance_cat", None, ll="上司", who="R"),
        t("13:00", 3.4, "仕事ふえたけど\n間に合いそう？", "work_typing_cat", "stare_big_eyes_tabby_kitten", "同僚"),
        t("13:00", 2.6, "早めにふってくれたから\n*よゆう*！！", "dance_wop_cat", "stare_big_eyes_tabby_kitten", "同僚", who="L"),
        t("13:00", 3.4, "午後の仕事も\n予定どおり進めるぞ！！", "stand_real_sheep", "stare_big_eyes_tabby_kitten", "同僚", who="L"),
        t("13:30", 2.6, "ちょっと*10分*だけ\n相談いい？", "glare_disgusted_cat", "work_typing_cat", None, ll="上司", who="L"),
        t("13:30", 2.0, "10分なら！！", "glare_disgusted_cat", "laugh_laughing_dog", None, ll="上司", who="R"),
        t("14:30", 2.0, "…ってことだから\n対応よろしく～", "stare_interviewer_cat", "sleepy_sleepy_cat", None, ll="上司", bg=OFF2, who="L"),
        t("14:30", 2.5, "……*10分*の話じゃ\nなかったっけ", "stare_interviewer_cat", "stare_big_eyes_tabby_kitten", None, ll="上司", bg=OFF2, who="R"),
        s("15:00", 2.5, "げっ電話だ…\nいやな予感しかしない", "call_customer_service_cat", se="pinpon_notice",
          props=[("phone", 700, 1180, 200)]),
        t("15:00", 3.4, "明日の納品、\n*午前中*にできる？", "confused_i_dont_know_cat", "meow_ragdoll_chubby_cat", "取引先"),
        t("15:00", 2.5, "い、今から\nですか……？", "blank_black_cat_zoning_out", "meow_ragdoll_chubby_cat", "取引先", who="L"),
        ph(4.4, [m1], cat="sulk_hungry_cat", say="あと3時間半か…"),
        ph(3.0, [m1], cat="eat_pop_cat", say="いや…いける\n本気出せばいけるぞ！！"),
        ph(3.0, [m1, m2]),
        dict(s("17:00", 2.0, None, "work_typing_cat", se="pikon",
               bubbles=[("@メンション\nお疲れさまです。", 640, 900, 0.0), ("ちょっといいですか？", 640, 1060, 0.9)]), **night),
        dict(s("17:00", 1.6, "あ、終わった", "work_typing_cat", big_say=True, se="chin_bell_failure_sad_ending"), **night),
        t("19:00", 2.0, "もう焼肉\n始まってるけど？", None, "talk_orange_white_sitting_cat", "友達", bg=YAKI, who="R"),
        t("19:00", 1.6, "帰れねええ", "sad_banana_cat_cry", "talk_orange_white_sitting_cat", "友達", bg=YAKI, who="L"),
    ]


def fix(cs):
    """talk の None（だれもいない側）を取りのぞく。帯は参考どおり少し上（140〜450）。"""
    for c in cs:
        c["cats"] = [q for q in c["cats"] if q.get("a")]
        c.update(band_y=140, tag_y=520)
        c.setdefault("say_y", 600)
    return cs


if __name__ == "__main__":
    Wd.run(fix(cuts()), Wd.rich_band([("{y}絶対定時で帰る日", 140, Wd.BLACK, 245), ("{r}サラリーマンの1日", 120, Wd.WHITE, 380)], 140, 450),
           os.path.join(Wd.HERE, "out", "short_25c_teiji.mp4"), os.path.join(Wd.HERE, "out", "short_25c_teiji_preview"))
