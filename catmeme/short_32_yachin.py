"""ショート32：家賃でわかる ひとり暮らし事情（income_short.py・年収別ショートと同じ作り）。59.9秒。

python3 catmeme/short_32_yachin.py → out/short_32_yachin.mp4
- 区切り：家賃3万・6万・9万・15万・25万、オチは家賃0円（社員寮）
- 会話は作り話。実在の人は出さない。「にゃ」なし。BGM なし（10/23 ルール）
"""
import os

import income_short as I
import world_short as Wd

I.BGS.insert(0, os.path.join(I.HERE, "backgrounds", "jidaraku", "01_yakiniku"))
OLD, ROOM, NIGHT, TOWER, ROPPONGI, DORM = ("j01_room", "bg02_room", "bg14_home_night", "bg57_tokyo_skyline", "bg76_roppongi_night",
                                           "bg55_ryokan")


def cuts():
    t = I.talk
    return [
        # ---- 3万 ----
        I.intro(OLD, "家賃3万", "築45年 駅から徒歩25分！", "meow_ragdoll_chubby_cat"),
        t(OLD, "家賃3万", "家賃3万って\nめっちゃ安くない？", "excited_hodomoe_city_cat", "meow_ragdoll_chubby_cat", who="L"),
        t(OLD, "家賃3万", "その代わり\n壁がうすすぎる", "excited_hodomoe_city_cat", "sulk_hungry_cat"),
        t(OLD, "家賃3万", "となりのくしゃみに\n「お大事に」って返した", "huh_huh_cat", "blank_black_cat_zoning_out"),
        # ---- 6万 ----
        I.intro(ROOM, "家賃6万", "ワンルーム 駅10分！", "happy_hamster_open_arms"),
        t(ROOM, "家賃6万", "ふつうに\n住みやすそう！", "dance_trending_cat", "happy_hamster_open_arms", who="L"),
        t(ROOM, "家賃6万", "うん でも\nキッチンがコンロ1口", "dance_trending_cat", "talk_orange_white_sitting_cat"),
        t(ROOM, "家賃6万", "料理は\nレンジで全部やる", "cocky_dj_cat", "think_bike_front_seat_cat"),
        # ---- 9万 ----
        I.intro(NIGHT, "家賃9万", "1LDK オートロック！", "dance_tabby_standing_cat"),
        t(NIGHT, "家賃9万", "部屋が2つあるの\nうらやましい！", "surprise_big_pupils_cat", "dance_tabby_standing_cat", who="L"),
        t(NIGHT, "家賃9万", "でも1部屋は\n洗濯物の部屋", "surprise_big_pupils_cat", "showoff_gojo_cosplay_cat"),
        t(NIGHT, "家賃9万", "家賃のために\n働いてる気がする…", "glare_disgusted_cat", "sad_banana_cat_cry"),
        # ---- 15万 ----
        I.intro(TOWER, "家賃15万", "駅直結のタワマン！", "money_counting_orange_cat"),
        t(TOWER, "家賃15万", "夜景すごっ！\n勝ち組じゃん！", "stare_big_eyes_tabby_kitten", "money_counting_orange_cat", who="L"),
        t(TOWER, "家賃15万", "でも朝のエレベーターが\n10分待ち", "stare_big_eyes_tabby_kitten", "rizz_cat_rizz"),
        t(TOWER, "家賃15万", "夜景は\n最初の1週間だけ見た", "stare_tabby_wide_eyes_cat", "sleepy_old_memories_cat"),
        # ---- 25万 ----
        I.intro(ROPPONGI, "家賃25万", "港区 コンシェルジュつき！", "happy_girlfriend_dance_cat"),
        t(ROPPONGI, "家賃25万", "コンシェルジュって\n何してくれるの？", "peek_what_happen_cat", "happy_girlfriend_dance_cat", who="L"),
        t(ROPPONGI, "家賃25万", "あいさつ\nしてくれる", "peek_what_happen_cat", "slack_nail_filing_cat"),
        t(ROPPONGI, "家賃25万", "近くのスーパーが\n高すぎて買えない…", "eat_pop_cat", "despair_dramatic_kitten"),
        # ---- オチ：家賃0円（会社の寮）10/27 ユーザー指定：寮ならではの面白エピソードで強く ----
        I.intro(DORM, "家賃0円", "会社の寮！", "sleepy_sleepy_cat"),
        t(DORM, "家賃0円", "家賃タダは\n最強じゃん！", "excited_hodomoe_city_cat", "sleepy_sleepy_cat", who="L"),
        t(DORM, "家賃0円", "朝6時に寮長の\nラジオ体操で起こされる", "excited_hodomoe_city_cat", "despair_dramatic_kitten"),
        t(DORM, "家賃0円", "大浴場に入ったら\n社長と2人きり", "stare_tabby_wide_eyes_cat", "blank_black_cat_zoning_out"),
        t(DORM, "家賃0円", "風邪で休んだら\n上司がおかゆ持ってきた", "huh_huh_cat", "sad_banana_cat_cry"),
        t(DORM, "家賃0円", "……家賃より\n高いものを払ってる", "realize_wet_cat_stare", "sad_black_dog", who="R"),
    ]


def fit(cs):
    k = I.TOTAL / sum(c["dur"] for c in cs)   # 59.9秒ちょうどに
    for c in cs:
        c["dur"] *= k
    return cs


if __name__ == "__main__":
    I.run(fit(Wd.dedupe(cuts())), "家賃でわかる", "ひとり暮らし事情", os.path.join(I.HERE, "out", "short_32_yachin.mp4"),
          os.path.join(I.HERE, "out", "short_32_yachin_preview"))
