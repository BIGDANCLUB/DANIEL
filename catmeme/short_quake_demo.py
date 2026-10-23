"""お試し3：震度で違う　揺れたときのリアル（income_short.py・参考「地震反応の違い」の作りをまねる）。59.9秒ちょうど。

python3 catmeme/short_quake_demo.py → out/short_quake_demo.mp4
- 台本・帯は参考と変える。区切りの頭のひとことは気象庁の震度の説明（要約）をもとにする
- 地震で亡くなった方・被災した方がいる話題なので、強い揺れ（6強・7）の場面は笑いにしない。最後は備え（家具の固定）で締める
- BGM なし（10/23 ルール）。会話は作り話
"""
import os

import income_short as I

ROOM, HOME, OFFICE = "bg02_room", "bg14_home_night", "bg25_office_desk"
FAM = "家族"


def cuts():
    t = lambda *a, **k: I.talk(*a, label=k.pop("label", FAM), **k)
    return [
        # ---- 震度1 ----
        I.intro(ROOM, "震度1", "気づく人はわずか", "sleepy_sleepy_cat"),
        t(ROOM, "震度1", "今ちょっと\n揺れなかった？", "peek_what_happen_cat", "sleepy_sleepy_cat", who="L"),
        t(ROOM, "震度1", "気のせい\n気のせい", "peek_what_happen_cat", "sleep_sleeping_cat"),
        t(ROOM, "震度1", "……スマホの速報\n出てないね", "think_bike_front_seat_cat", "sleep_sleeping_cat", who="L"),
        # ---- 震度3 ----
        I.intro(ROOM, "震度3", "ほとんどの人が気づく", "stare_tabby_wide_eyes_cat"),
        t(ROOM, "震度3", "あ、揺れてる\n揺れてる", "surprise_big_pupils_cat", "stare_tabby_wide_eyes_cat"),
        t(ROOM, "震度3", "テレビつけて！\n速報まだ？", "surprise_big_pupils_cat", "work_typing_cat", who="L"),
        t(ROOM, "震度3", "震度3だって\nとりあえずセーフ", "calm_black_face_sheep", "work_typing_cat"),
        # ---- 震度4 ----
        I.intro(HOME, "震度4", "ほとんどの人が驚く", "stare_big_eyes_tabby_kitten"),
        t(HOME, "震度4", "電気のかさが\nめっちゃ揺れてる！", "huh_huh_cat", "stare_big_eyes_tabby_kitten", who="L"),
        t(HOME, "震度4", "ドア開けて！\n出口つくっとこ", "huh_huh_cat", "talk_orange_white_sitting_cat"),
        t(HOME, "震度4", "……止まった？\n心臓がバクバク", "realize_wet_cat_stare", "talk_orange_white_sitting_cat", who="L"),
        # ---- 震度5強 ----
        I.intro(HOME, "震度5強", "つかまらないと歩けない", "despair_dramatic_kitten"),
        t(HOME, "震度5強", "棚の食器が\n落ちてくる！", "stare_tabby_wide_eyes_cat", "despair_dramatic_kitten", who="L"),
        t(HOME, "震度5強", "テーブルの下へ！\n頭を守って！", "stare_tabby_wide_eyes_cat", "stare_interviewer_cat"),
        t(HOME, "震度5強", "割れたガラスで\nケガしないようにスリッパ", "calm_black_face_sheep", "stare_interviewer_cat", who="L"),
        # ---- 震度6強 ----
        I.intro(OFFICE, "震度6強", "はわないと動けない", "realize_wet_cat_stare"),
        t(OFFICE, "震度6強", "固定してない家具は\nほとんど倒れる", "calm_black_face_sheep", "realize_wet_cat_stare", who="L"),
        t(OFFICE, "震度6強", "揺れがおさまるまで\n動かないで", "calm_black_face_sheep", "stare_interviewer_cat"),
        t(OFFICE, "震度6強", "おさまったら\n火の元と出口を確認", "meow_gray_white_kitten", "stare_interviewer_cat", who="L"),
        # ---- 震度7 ----
        I.intro(ROOM, "震度7", "いちばん強い揺れ", "stare_interviewer_cat"),
        t(ROOM, "震度7", "家具の固定\nしておけばよかった…", "sad_black_dog", "stare_interviewer_cat", who="L"),
        t(ROOM, "震度7", "だから\n今日やろう", "sad_black_dog", "talk_orange_white_sitting_cat"),
        t(ROOM, "震度7", "水と食料\n3日分もね", "meow_gray_white_kitten", "talk_orange_white_sitting_cat", who="L"),
    ]


if __name__ == "__main__":
    I.run(cuts(), "震度で違う", "揺れたときのリアル", os.path.join(I.HERE, "out", "short_quake_demo.mp4"),
          os.path.join(I.HERE, "out", "short_quake_demo_preview"))
