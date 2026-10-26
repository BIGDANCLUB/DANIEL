"""ショート28：友人と旅行中 ど深夜に明日仕事だと思い出した結果（world_short.py・10/26 参考「実家帰省中 ど深夜に明日仕事だと
思い出した結果」の作りをまねる）。59.9秒。

python3 catmeme/short_28_ryoko.py → out/short_28_ryoko.mp4
- 10/26 ユーザー指定：「実家帰省中」を「友人と旅行中」に。締め（オチ）も変える
- 作りは、いつものショート風（黒い帯・赤い札に時刻・白い字幕・ステッカーの猫）。台本だけ参考にする（10/26 ユーザー指定）
- 舞台は札幌のホテル（友人4人旅行）。始発の飛行機で帰る → 会社に着いたら今日は創立記念日で休み → 友人から朝の海鮮丼の写真
- 実在の人は出さない。会話は作り話。BGM なし（10/23 ルール）
"""
import os

import world_short as Wd

HOTEL, YELLOW, PURPLE, AIRPORT, PLANE, OFFICE, SEA = ("bg66_hotel_price", "bg120_yellow_rays", "bg121_purple_rays",
                                                      "bg45_airport_arrival", "bg45_airport_arrival", "bg25_office_desk",
                                                      "bg46_sushi_counter")
BLUE_, RED_ = (20, 40, 220), (220, 20, 20)
ME = "イッチ"


def cuts():
    """10/26 ユーザー指定：台本だけ参考にして、作り（黒い帯・赤い札・白い字幕・ステッカーの猫）はいつものショート風にする。"""
    def s(bg, tm, say, cat, me=True, **kw):
        return Wd.solo(bg, tm, say, cat, label=ME if me else None, tag_style="time", **kw)

    def t(bg, tm, say, left, right, who="R", **kw):
        return Wd.talk(bg, tm, say, left, right, who=who, llabel="友人", rlabel=ME, tag_style="time", **kw)

    return [
        s(HOTEL, "深夜1:00", "あれ\n明日仕事じゃね…？", "stare_tabby_wide_eyes_cat", lines=True, se="question_mark_pop_confused_huh"),
        s(HOTEL, "深夜1:00", "ここは札幌のホテル\n会社は東京", "sleepy_old_memories_cat"),
        s(HOTEL, "深夜1:02", "始発の飛行機でも\n着くのは朝9時すぎ", "despair_dramatic_kitten"),
        t(HOTEL, "深夜1:05", "有給使えば\nええやん", "eat_chips_cat", "sad_banana_cat_cry", who="L"),
        t(HOTEL, "深夜1:05", "有給\nもう残ってないんよ…", "laugh_laughing_dog", "sulk_hungry_cat"),
        s(HOTEL, "深夜1:10", "間に合わん\nずる休みの理由考えろ！", "rizz_cat_rizz", me=False, se="jan"),
        t(HOTEL, "深夜1:12", "親戚が\n急に倒れたとか？", "talk_orange_white_sitting_cat", "glare_disgusted_cat", who="L"),
        t(HOTEL, "深夜1:12", "それ今年\nもう3回使った", "cocky_dj_cat", "blank_black_cat_zoning_out"),
        t(HOTEL, "深夜1:15", "じゃあ飛行機が\n欠航したことにしよ", "dance_wop_cat", "stare_big_eyes_tabby_kitten", who="L"),
        t(HOTEL, "深夜1:15", "札幌 明日\n快晴なんよ", "eat_pop_cat", "sleepy_sleepy_cat"),
        t(HOTEL, "深夜1:20", "始発の便\nまだ空いてるで", "work_dog_staring_computer", "peek_what_happen_cat", who="L", se="pikon"),
        t(HOTEL, "深夜1:20", "これええやん\n昼前には出社できる！", "money_counting_orange_cat", "happy_hamster_open_arms"),
        s(HOTEL, "深夜1:25", "上司に「少し遅れます」\nってLINE送っとこ", "call_customer_service_cat"),
        t(HOTEL, "深夜1:30", "空港までのタクシー\n朝5時に呼んどいたで", "showoff_gojo_cosplay_cat", "dance_tabby_standing_cat", who="L"),
        t(HOTEL, "深夜1:30", "お前ら\n最高かよ…", "happy_girlfriend_dance_cat", "sad_black_dog"),
        s(HOTEL, "朝5:00", "友人は\n全員寝ている", "sleep_sleeping_cat", me=False, se="cuckoo_pappo"),
        s(AIRPORT, "朝6:30", "なんとか\n始発の便に乗れた", "leave_cat_leaves_home"),
        s(AIRPORT, "朝9:10", "羽田から\nそのまま会社へダッシュ", "ride_kitten_bike", se="dash_super_fast"),
        s(OFFICE, "朝10:00", "……あれ？\n会社が真っ暗", "surprise_big_pupils_cat"),
        s(OFFICE, "朝10:00", "上司から返信\n「今日は創立記念日で\n休みだよ？」", "stare_interviewer_cat", me=False, se="pinpon_notice"),
        s(OFFICE, "朝10:01", "始発で帰ってきたのに…", "sad_black_dog"),
        s(OFFICE, "朝10:01", "……は？", "huh_huh_cat", big_say=True, dur=2.2, se="question_mark_pop_confused_huh"),
        t(SEA, "朝10:05", "朝から海鮮丼\nうまいww", "dance_three_kittens", "despair_dramatic_kitten", who="L", se="pikon"),
        t(SEA, "朝10:05", "グッバイ\nイッチww", "laugh_laughing_dog", "sad_banana_cat_cry", who="L", dur=2.6),
    ]


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{r}友人と旅行中", 140, Wd.WHITE, 300), ("{y}明日仕事を思い出した結果", 96, Wd.BLACK, 440)], *Wd.I.BAND),
           os.path.join(Wd.HERE, "out", "short_28_ryoko.mp4"), os.path.join(Wd.HERE, "out", "short_28_ryoko_preview"))
