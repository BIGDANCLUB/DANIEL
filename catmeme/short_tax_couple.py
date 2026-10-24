"""お試し2：世帯年収1000万、手取りがいちばん多い夫婦は？（bars_short.py・参考「1番損する夫婦年収」の作りをまねる）。59.9秒ちょうど。

python3 catmeme/short_tax_couple.py → out/short_tax_couple.mp4
- 台本・帯は参考と変える（世帯年収1200万→1000万、分け方・差し引く順番・セリフ・締めの文字も別）
- 数字はざっくりの目安（会社員・ボーナスなし・40歳未満・子どもなし・2026年の税の決まりでの概算）。
  社会保険料は健康保険（協会けんぽ 約5%）・厚生年金（9.15%・月65万で上限）・雇用保険（0.55%）。
  所得税は基礎控除（所得に応じて58〜88万）と配偶者控除（38万）、復興特別所得税こみ。住民税は10%＋均等割
- BGM なし（10/23 ルール）
"""
import os

import bars_short as B

SPEC = dict(
    bg="bg25_office_desk",
    title=("世帯年収1000万", "手取りが1番多い夫婦は？"),
    incomes=(1000, 1000, 1000),
    cards=[("年収", "夫1000万", "妻0万"), ("年収", "夫700万", "妻300万"), ("年収", "夫500万", "妻500万")],
    card_cols=[(225, 90, 0), (0, 150, 150), (170, 0, 170)],
    items=[("社会保険料", "gray"), ("所得税", "red"), ("住民税", "dark")],
    values={"社会保険料": (127, 147, 147), "所得税": (75, 32, 24), "住民税": (61, 49, 48)},
)
A, B2, C3 = "夫1000万", "夫700万", "夫500万"


def cut(dur, say=None, cats=(None, None, None), shown=0, grow=False, banner=None, take=False, voice=None, box=False, big=None,
        finish=None, se=None, say_y=640):
    c = dict(dur=dur, say=say, cats3=list(cats), shown=shown, grow=grow, banner=banner, take=take, voice=voice, box=box, big=big,
             finish=finish, say_y=say_y)
    if se:
        c["se"] = se
    return c


def cuts():
    trio = ("stare_big_eyes_tabby_kitten", "happy_hamster_open_arms", "talk_orange_white_sitting_cat")
    same = ("think_bike_front_seat_cat", "stare_interviewer_cat", "meow_gray_white_kitten")
    return [
        # つかみ
        cut(3.4, "世帯年収は\nみんな同じ1000万！", trio, voice=1, se="jan"),
        cut(2.6, "じゃあ手取りも\n同じでしょ？", trio, voice=0, se="pi"),
        cut(2.4, "……本当に？", ("sleepy_sleepy_cat", "huh_huh_cat", "sleepy_sleepy_cat"), voice=1, big=1),
        # 社会保険料
        cut(2.2, None, same, banner=("社会保険料", "社会保険料", "ズシッ!!", "money_counting_orange_cat"), se="explosion_chudoon"),
        cut(2.6, None, same, shown=1, grow=True, se="card_place"),
        cut(2.8, "共働きの2組は\n2人とも払うから\n高くなる", ("blank_black_cat_zoning_out", "sad_banana_cat_cry", "sulk_hungry_cat"),
            shown=1, voice=1),
        cut(2.8, "妻が扶養だと\n妻の分は0円！", ("excited_hodomoe_city_cat", "glare_disgusted_cat", "glare_disgusted_cat"),
            shown=1, voice=0),
        # 所得税
        cut(2.2, None, same, shown=1, banner=("所得税", "所得税", "ドスン!!", "punch_boxing_white_cat"), se="explosion_chudoon"),
        cut(2.6, None, same, shown=2, grow=True, se="card_place"),
        cut(3.0, "ちょっと待って\n1人で稼ぐほうが\n税率が上がるの！？", ("stare_tabby_wide_eyes_cat", "think_bike_front_seat_cat",
                                                    "think_bike_front_seat_cat"), shown=2, voice=0, big=0, box=True),
        cut(2.8, "所得税は\n稼ぐほど率が上がる\nしくみだからね", ("realize_wet_cat_stare", "talk_orange_white_sitting_cat",
                                                 "stare_interviewer_cat"), shown=2, voice=1),
        cut(2.4, "半分ずつの\n私たちが有利！", ("realize_wet_cat_stare", "stare_interviewer_cat", "dance_orange_gray_cats"),
            shown=2, voice=2),
        # 住民税
        cut(2.2, None, same, shown=2, banner=("住民税", "住民税", "ドンッ!!", "angry_aiming_cat"), se="explosion_chudoon"),
        cut(2.6, None, same, shown=3, grow=True, se="card_place"),
        cut(2.8, "住民税は\nだいたい同じくらい\n…と思ったら", ("think_bike_front_seat_cat", "stare_interviewer_cat",
                                               "meow_gray_white_kitten"), shown=3, voice=1),
        cut(2.6, "やっぱり\n1人で稼ぐと多い…", ("despair_dramatic_kitten", "stare_interviewer_cat", "stare_interviewer_cat"),
            shown=3, voice=0),
        # 手取り
        cut(2.2, None, same, shown=3, banner=("手取り", "のこった手取り", "ジャン!!", "dance_tabby_standing_cat"), se="explosion_chudoon"),
        cut(3.0, None, ("sad_banana_cat_cry", "excited_hodomoe_city_cat", "happy_girlfriend_dance_cat"), shown=3, take=True,
            se="price_display"),
        cut(3.0, "同じ1000万なのに\n40万以上も違う…", ("stare_tabby_wide_eyes_cat", None, None), shown=3, take=True, voice=0, big=0,
            box=True, say_y=1000),
        cut(2.8, "共働きのほうが\n手取りは多い！", (None, "excited_hodomoe_city_cat", "happy_girlfriend_dance_cat"), shown=3,
            take=True, voice=1, say_y=1000),
        cut(2.6, "でも家事と子育ても\n2人で分けてね", ("talk_orange_white_sitting_cat", "huh_huh_cat", "huh_huh_cat"), shown=3,
            take=True, voice=0, box=True, say_y=1000),
        cut(2.4, None, ("sad_banana_cat_cry", "excited_hodomoe_city_cat", "happy_girlfriend_dance_cat"), shown=3, take=True, finish="勝負あり!!",
            se="game_smash_finish"),
    ]


if __name__ == "__main__":
    B.run(SPEC, cuts(), os.path.join(B.HERE, "out", "short_tax_couple.mp4"), os.path.join(B.HERE, "out", "short_tax_couple_preview"))
