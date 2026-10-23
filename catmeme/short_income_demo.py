"""お試し：年収別 リアルな生活の違い（income_short.py・参考動画3本の作りをまねる）。59.9秒ちょうど。

python3 catmeme/short_income_demo.py → out/short_income_demo.mp4
- 原稿は参考動画と変える（10/23 ユーザー指定）。オチは「年収0円」（飼い猫）
- 手取りは独身・会社員・ボーナスなしのざっくりした目安（概要欄の「ご注意」に書く。動画には注釈を入れない）
- 実在の人は出さない。会話は作り話。「にゃ」なし。単語の途中で改行しない
"""
import os

import income_short as I

# BGM は入れない（10/23 ユーザー指定：ショートは猫の音と効果音だけ）
SUPER, IZAKAYA, RAMEN, ROOM, OFFICE, HOME = ("bg16_food_aisle", "bg13_izakaya", "bg47_ramen_shop", "bg02_room", "bg25_office_desk",
                                             "bg14_home_night")


def cuts():
    t = I.talk
    return [
        # ---- 300万 ----
        I.intro(SUPER, "300万", "手取り約20万！", "meow_ragdoll_chubby_cat"),
        t(SUPER, "300万", "今日パフェ\n食べに行こ！", "excited_hodomoe_city_cat", "meow_ragdoll_chubby_cat", who="L"),
        t(SUPER, "300万", "いや、半額シール\n待ってるから…", "excited_hodomoe_city_cat", "sulk_hungry_cat"),
        t(SUPER, "300万", "7時に2割引、\n8時に半額なんよ", "huh_huh_cat", "think_bike_front_seat_cat"),
        # ---- 500万 ----
        I.intro(IZAKAYA, "500万", "手取り約32万！", "happy_hamster_open_arms"),
        t(IZAKAYA, "500万", "週末キャンプ\n行こうぜ！", "dance_trending_cat", "happy_hamster_open_arms", who="L"),
        t(IZAKAYA, "500万", "いいね！\n道具はレンタルで", "dance_trending_cat", "talk_orange_white_sitting_cat"),
        t(IZAKAYA, "500万", "奨学金の返済が\nまだ残ってて…", "cocky_dj_cat", "sad_banana_cat_cry"),
        # ---- 700万 ----
        I.intro(RAMEN, "700万", "手取り約44万！", "dance_tabby_standing_cat"),
        t(RAMEN, "700万", "それ最新の\nスマホじゃん！", "surprise_big_pupils_cat", "cocky_dj_cat", who="L"),
        t(RAMEN, "700万", "そう！\n24回払いだけど", "surprise_big_pupils_cat", "showoff_gojo_cosplay_cat"),
        t(RAMEN, "700万", "家のローンと\n保育料で消えるんよ…", "glare_disgusted_cat", "realize_wet_cat_stare"),
        # ---- 1000万 ----
        I.intro(ROOM, "1000万", "手取り約60万！", "money_counting_orange_cat"),
        t(ROOM, "1000万", "勝ち組じゃん！\nうらやましい！", "stare_big_eyes_tabby_kitten", "money_counting_orange_cat", who="L"),
        t(ROOM, "1000万", "税金と保険料で\n年280万くらい引かれる", "stare_big_eyes_tabby_kitten", "blank_black_cat_zoning_out"),
        t(ROOM, "1000万", "給料明細、\n見るのが怖い…", "stare_tabby_wide_eyes_cat", "despair_dramatic_kitten"),
        # ---- 1500万 ----
        I.intro(OFFICE, "1500万", "手取り約86万！", "happy_girlfriend_dance_cat"),
        t(OFFICE, "1500万", "タワマン住んでるって\nホント？", "peek_what_happen_cat", "happy_girlfriend_dance_cat", who="L"),
        t(OFFICE, "1500万", "ホント！\n家賃で半分消えるけど", "peek_what_happen_cat", "slack_nail_filing_cat"),
        t(OFFICE, "1500万", "実家暮らしのお前のほうが\nお金残ってる説…", "eat_pop_cat", "sulk_hungry_cat"),
        # ---- オチ：年収0円 ----
        I.intro(HOME, "年収0円", "手取り0円！", "sleepy_sleepy_cat"),
        t(HOME, "年収0円", "ご飯は毎日\n勝手に出てくる", "huh_huh_cat", "sleepy_sleepy_cat"),
        t(HOME, "年収0円", "家賃も税金も\n払ったことない", "huh_huh_cat", "sleep_sleeping_cat"),
        t(HOME, "年収0円", "……飼い猫が\nいちばん勝ち組", "realize_wet_cat_stare", "sleep_sleeping_cat", who="L", label="飼い主"),
    ]


if __name__ == "__main__":
    I.run(cuts(), "年収別", "リアルな生活の違い", os.path.join(I.HERE, "out", "short_income_demo.mp4"),
          os.path.join(I.HERE, "out", "short_income_demo_preview"))
