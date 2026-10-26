"""ショート27：コロナ前と今 同じ月給でどっちが余裕？（bars_short.py・10/26 参考「2000年vs2026年 どっちが裕福？」の趣旨。
比べる相手は「コロナ前（2019年）」にする（10/26 ユーザー指定）。演出は short_tax_couple とほぼ同じ）。59.9秒。

python3 catmeme/short_27_corona.py → out/short_27_corona.mp4
- 列：2019年 月給30万／2026年 月給30万の2つだけ（10/26 ユーザー指定：賃上げ後の列はいらない）。1か月あたりの、ざっくりの目安（東京でひとり暮らしの会社員）
- 税金・社会保険（所得税・住民税・健康保険・厚生年金・雇用保険）：2019年 約6.2万／2026年 約6.4万（雇用保険料の引き上げなど）
- 家賃（23区ワンルーム）：約8.0万 → 約9.5万。光熱費＋スマホ：約1.9万 → 約1.9万（光熱費は上がったが、スマホ代は格安プランで下がった）
- 食費：約4.0万 → 約4.8万（食べ物の値上がり）
- 数字は概要欄に「ざっくりの目安」と書く。BGM なし（10/23 ルール）
"""
import os

import bars_short as B

SPEC = dict(
    bg="bg57_tokyo_skyline",
    title=("コロナ前と今", "同じ月給でどっちが余裕？"),
    incomes=(30, 30),
    cards=[("2019年", "コロナ前", "月給30万"), ("2026年", "今", "月給30万")],
    card_cols=[(0, 120, 200), (200, 30, 30)],
    items=[("税金・社保", "red"), ("家賃", "green"), ("光熱費・スマホ", "purple"), ("食費", "orange")],
    values={"税金・社保": (6.2, 6.4), "家賃": (8.0, 9.5), "光熱費・スマホ": (1.9, 1.9), "食費": (4.0, 4.8)},
    take_word="残り",
)


def cut(dur, say=None, cats=(None, None, None), shown=0, grow=False, banner=None, take=False, voice=None, box=False, big=None,
        finish=None, se=None, say_y=640, finish_word=None):
    c = dict(dur=dur, say=say, cats3=list(cats), shown=shown, grow=grow, banner=banner, take=take, voice=voice, box=box, big=big,
             finish=finish, say_y=say_y, finish_word=finish_word or "1位")
    if se:
        c["se"] = se
    return c


def cuts():
    return [
        # つかみ
        cut(3.0, "コロナ前と今\n月給は同じ30万！", ("sleepy_old_memories_cat", "showoff_gojo_cosplay_cat"), voice=1, se="jan"),
        cut(2.6, "なら暮らしも\n同じでしょ？", ("stare_big_eyes_tabby_kitten", "cocky_dj_cat"), voice=1, se="pi"),
        cut(2.2, "……本当に？", ("sleepy_sleepy_cat", "huh_huh_cat"), voice=1, big=1),
        # 税金・社保
        cut(2.0, None, ("think_bike_front_seat_cat", "stare_interviewer_cat"),
            banner=("税金・社保", "税金・社保", "ズシッ!!", "money_counting_orange_cat"), se="explosion_chudoon"),
        cut(2.4, None, ("realize_wet_cat_stare", "meow_ragdoll_chubby_cat"), shown=1, grow=True, se="card_place"),
        cut(2.8, "ここは\nほとんど変わらない", ("calmdown_dancing_cat", "talk_orange_white_sitting_cat"), shown=1, voice=1),
        cut(2.6, "雇用保険料が\nちょっと上がったくらい", ("peek_what_happen_cat", "read_book_orange_kitten"), shown=1, voice=1),
        # 家賃
        cut(2.0, None, ("think_bike_front_seat_cat", "stare_interviewer_cat"),
            banner=("家賃", "家賃", "ドスン!!", "punch_boxing_white_cat"), se="explosion_chudoon"),
        cut(2.4, None, ("eat_chips_cat", "glare_disgusted_cat"), shown=2, grow=True, se="card_place"),
        cut(2.8, "同じワンルームで\n1.5万も高い！？", ("sleepy_old_memories_cat", "stare_tabby_wide_eyes_cat"), shown=2, voice=1, big=1,
            box=True),
        cut(2.6, "都心の家賃は\nずっと上がりっぱなし…", ("happy_hamster_open_arms", "sad_banana_cat_cry"), shown=2, voice=1),
        # 光熱費・スマホ
        cut(2.0, None, ("think_bike_front_seat_cat", "stare_interviewer_cat"),
            banner=("光熱費・スマホ", "光熱費・スマホ", "ドンッ!!", "angry_aiming_cat"), se="explosion_chudoon"),
        cut(2.4, None, ("realize_wet_cat_stare", "confused_i_dont_know_cat"), shown=3, grow=True, se="card_place"),
        cut(2.8, "電気代は上がったけど\nスマホ代は下がった！", ("talk_orange_white_sitting_cat", "happy_girlfriend_dance_cat"),
            shown=3, voice=1),
        cut(2.6, "格安プランに\n変えたからね", ("sulk_hungry_cat", "work_typing_cat"), shown=3, voice=1),
        cut(2.2, "ここは\n引き分け！", ("dance_orange_gray_cats", "dance_three_kittens"), shown=3, voice=0),
        # 食費
        cut(2.0, None, ("think_bike_front_seat_cat", "stare_interviewer_cat"),
            banner=("食費", "食費", "ズドン!!", "eat_pop_cat"), se="explosion_chudoon"),
        cut(2.4, None, ("eat_crunchy_cat_luna", "blank_black_cat_zoning_out"), shown=4, grow=True, se="card_place"),
        cut(2.8, "同じものを買っても\n1か月で8000円高い", ("rizz_cat_rizz", "despair_dramatic_kitten"), shown=4, voice=1),
        # 残り
        cut(2.0, None, ("think_bike_front_seat_cat", "stare_interviewer_cat"),
            banner=("残り", "のこったお金", "ジャン!!", "dance_tabby_standing_cat"), se="explosion_chudoon"),
        cut(2.8, None, ("happy_chipi_chapa_cat", "sad_black_dog"), shown=4, take=True, se="price_display"),
        cut(2.8, "同じ給料なのに\n毎月2.5万も少ない…", (None, "stare_tabby_wide_eyes_cat"), shown=4, take=True, voice=1, big=1,
            box=True, say_y=420),
        cut(2.6, "給料より\n物の値段が先に上がった", ("realize_wet_cat_stare", "sulk_hungry_cat"), shown=4, take=True, voice=0,
            say_y=420),
        dict(cut(3.0, None, ("sad_banana_cat_cry", "despair_dramatic_kitten"), shown=4, take=True, se="explosion_chudoon"),
             minus=("毎月 −2.5万円", "1年で −30万円…")),
    ]


if __name__ == "__main__":
    B.run(SPEC, cuts(), os.path.join(B.HERE, "out", "short_27_corona.mp4"), os.path.join(B.HERE, "out", "short_27_corona_preview"))
