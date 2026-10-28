"""ショート40：ボーナス日の前と後（salary_short.py・「給料日の前と後」と同じ作り）。住民税・ローンのボーナス払いで消える。59.9秒。
札は「○日前／○日後」。引き落としの場面は叫ぶマーモット（1回叫んだら次へ）。
10/28 リモートワークと同じルール：「!?」の場面はコナン、「え…」の場面はポーン。字幕は上まん中・猫はその下に大きく。"""
import salary_short as S
from salary_short import s, t, OFF, ROOM, NIGHT, IZAKAYA

M = "scream_standing_marmot"


def ph(label):
    return [("phone:" + label, 300, 1200, 230)]


cs = [
    s(ROOM, "10日前", "ボーナスで\n*何買おう*", "dance_tabby_standing_cat", lines=True, se="jan"),
    dict(s(ROOM, "7日前", "新しいテレビ\n旅行も行きたい", "laugh_laughing_dog"), props=[("cloud:テレビ\n温泉旅行@R", 300, 1000, 480)]),
    s(ROOM, "3日前", "ネットで\n*カートに入れまくる*", "work_typing_cat"),
    s(NIGHT, "1日前", "明日は\nボーナス日…！", "excited_hodomoe_city_cat"),
    dict(s(OFF, "ボーナス日", "明細が\nきた！", "money_counting_orange_cat", se="pikon"), props=ph("賞与明細")),
    dict(s(OFF, "ボーナス日", "……あれ？\n思ったより少ない", "stare_tabby_wide_eyes_cat"), props=ph("賞与明細")),
    t(OFF, "ボーナス日", "ボーナスからも\n*税金と社会保険料*\n引かれるからね", "talk_orange_white_sitting_cat", "stare_big_eyes_tabby_kitten", who="L",
      ll="先輩"),
    t(OFF, "ボーナス日", "手取りは\n*2割*くらい減るよ", "talk_orange_white_sitting_cat", "despair_dramatic_kitten", who="L", ll="先輩"),
    s(IZAKAYA, "1日後", "でも今日は\n*ボーナス祝い*！", "yell_orange_fat_cat", se="jan"),
    s(IZAKAYA, "1日後", "全員分\n*おごっちゃう*", "showoff_gojo_cosplay_cat"),
    s(ROOM, "2日後", "カートの中身\n*全部ポチ*", "dance_wop_cat", se="pikon"),
    s(ROOM, "5日後", "車のローン\nボーナス払い", M, d=1.3),
    s(ROOM, "6日後", "カードの\nボーナス一括払い", M, d=1.3),
    s(ROOM, "7日後", "家具のローンも\nボーナス払い", M, d=1.3),
    dict(s(ROOM, "10日後", "もう残ってない!?", "surprise_big_pupils_cat"),   # !? の場面はコナン（10/28 ルール）
         props=ph("残高\n3千円")),
    s(ROOM, "10日後", "ボーナスは\n*通りすぎていった*", "sad_banana_cat_cry"),
    s(NIGHT, "10日後", "次のボーナスまで\nあと*半年*…", "sad_black_dog", se="chin_bell_failure_sad_ending"),
    s(NIGHT, "10日後", "みんなも\nボーナス払いは\n*使いすぎに気をつけよう*", "realize_wet_cat_stare"),
]

if __name__ == "__main__":
    S.run("short_40_bonus", "ボーナス日の前と後", "これ自分だけ？", cs)
