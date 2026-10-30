"""ショート49：ディズニーvsUSJ 1日で使うお金（bars_auto.py・東京大阪地方⑤と同じ作り・10/30 ユーザー指定）。59.9秒。
予算3万円を持って1人で1日遊んだら、いくら残る？（2026年ごろのざっくりの目安・大人1人・土日）
- チケット：ディズニー 約9400円／USJ 約9800円（日によって変わる）
- 食事（昼・夜・おやつ）：どちらも 約4000円。おみやげ：どちらも 約5000円
- 待ち時間を短くするパス：ディズニー（2アトラクション）約3000円／USJ 約1万円〜
→ 残り ディズニー 約8600円／USJ 約1200円
実在の施設の名前は「くらべる目安」としてだけ出す。ロゴ・キャラクターは出さない。BGM なし
"""
import bars_auto as A

SPEC = dict(
    bg="bg57_tokyo_skyline",
    title=("ディズニーvsUSJ", "1日で使うお金"),
    incomes=(30000, 30000),
    unit="円",
    cards=[("ディズニー", "東京", "予算3万円"), ("USJ", "大阪", "予算3万円")],
    card_cols=[(0, 120, 200), (200, 30, 30)],
    items=[("チケット", "red"), ("ごはん", "orange"), ("おみやげ", "purple"), ("待ち時間パス", "green")],
    values={"チケット": (9400, 9800), "ごはん": (4000, 4000), "おみやげ": (5000, 5000), "待ち時間パス": (3000, 10000)},
    take_word="残り",
    style="bright",
    wlabel={"待ち時間パス": "待ち時間\nパス"},
)


def cuts():
    M = "dance_three_kittens"
    cs = A.build(SPEC, [
        (2.9, None, (M, M), (0, 1)),
        (3.0, "予算3万円で\n1日遊びたい！", ("happy_chipi_chapa_cat", "dance_happy_banana_cat"), 1),
        (2.6, "ディズニーとUSJ\nどっちが安い？", ("think_chin_paw_orange_cat", "stare_big_eyes_tabby_kitten"), 0),
    ], [
        [(2.8, "チケットは\nほぼ同じくらい", ("talk_orange_white_sitting_cat", "read_book_orange_kitten"), 0),
         (2.4, "日によって\n値段が変わるよ", ("slack_nail_filing_cat", "think_bike_front_seat_cat"), 1)],
        [(2.8, "パークのごはんは\nちょっと高め", ("eat_pop_cat", "eat_chips_cat"), 0)],
        [(2.8, "おみやげで\n一気に減る！", ("money_counting_orange_cat", "despair_dramatic_kitten"), 1),
         (2.4, "お菓子とぬいぐるみで\nあっという間", ("scream_phone_orange_cat", "sad_looking_away_tabby"), 0)],
        [(2.8, "USJの待ち時間パスは\n1万円以上も！？", ("dance_tabby_standing_cat", "stare_tabby_wide_eyes_cat"), 1),
         (2.4, "人気のアトラクションを\nぜんぶ乗りたいなら……", ("calmdown_dancing_cat", "sulk_hungry_cat"), 1)],
    ], [
        (2.8, "USJは\n残り1200円……", (None, "sad_banana_cat_cry"), 1),
        (2.6, "パスを買わなければ\nほぼ同じくらい", ("realize_wet_cat_stare", "think_chin_paw_orange_cat"), 0),
        (2.4, "みんなも\n使いすぎに気をつけよう", ("talk_orange_white_sitting_cat", "happy_hamster_open_arms"), 0),
    ], ("USJは 残り −7400円", "パスを買うと差が広がる", ("dance_happy_banana_cat", "despair_dramatic_kitten")))
    cs[0]["callout"] = ("夢の国と映画の国", "1日でいくら消える？")
    return cs


if __name__ == "__main__":
    A.run(SPEC, cuts(), "short_49_park")
