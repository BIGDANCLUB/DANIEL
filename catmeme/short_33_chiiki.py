"""ショート33：東京・大阪・地方 同じ手取りでいくら残る？（bars_auto.py・ショート27と同じ作り）。59.9秒。
数字は手取り月26万（年収400万くらい・ひとり暮らし）のざっくりの目安。家賃はワンルーム、地方は車が必要として車の費用を入れる。
BGM なし（10/23 ルール）"""
import bars_auto as A

SPEC = dict(
    bg="bg57_tokyo_skyline",
    title=("東京・大阪・地方", "同じ手取りでいくら残る？"),
    incomes=(26, 26, 26),
    cards=[("東京", "23区", "手取り26万"), ("大阪", "市内", "手取り26万"), ("地方", "車あり", "手取り26万")],
    card_cols=[(200, 30, 30), (0, 120, 200), (0, 150, 60)],
    items=[("家賃", "green"), ("車・交通", "purple"), ("食費", "orange"), ("光熱費・スマホ", "dark")],
    values={"家賃": (9.5, 6.5, 4.5), "車・交通": (1.0, 1.0, 4.0), "食費": (4.8, 4.3, 4.0), "光熱費・スマホ": (1.2, 1.2, 1.5)},
    take_word="残り",
    style="bright",   # 明るい配色（10/27 ユーザー指定）
    wlabel={"車・交通": "自動車\n交通費"},   # 重りの文字は2行（10/27 ユーザー指定）
)


def cuts():
    M = "scream_standing_marmot_fast"   # 冒頭は3匹ともマーモットで高速に「オイ！オイ！オイ！」（10/27 ユーザー指定）
    cs = A.build(SPEC, [
        (2.9, None, (M, M, M), (0, 1, 2)),   # 字幕なし（10/27）・3匹とも鳴く
        (3.0, "東京・大阪・地方\n手取りはみんな26万！", ("cocky_dj_cat", "happy_hamster_open_arms", "sleepy_old_memories_cat"), 0),
        (2.6, "地方は家賃が安いから\n勝ちでしょ？", ("stare_big_eyes_tabby_kitten", "dance_three_kittens", "showoff_gojo_cosplay_cat"), 2),
        (2.2, "……本当に？", ("sleepy_sleepy_cat", "huh_huh_cat", "sleepy_sleepy_cat"), 1),
    ], [
        [(2.8, "東京のワンルームは\n大阪の1.5倍", ("despair_dramatic_kitten", "talk_orange_white_sitting_cat", "dance_tabby_standing_cat"), 0),   # 地方は踊る
         (2.6, "地方は\n半分以下！", ("sad_banana_cat_cry", "read_book_orange_kitten", "dance_wop_cat"), 2)],
        [(2.8, "地方は車がないと\n生活できない", ("stare_interviewer_cat", "think_bike_front_seat_cat", "stare_tabby_wide_eyes_cat"), 2),
         (2.6, "ローン・ガソリン・保険で\n月4万！？", ("eat_chips_cat", "calmdown_dancing_cat", "despair_dramatic_kitten"), 2)],
        [(2.8, "東京は外食も\nスーパーも高め", ("sulk_hungry_cat", "laugh_laughing_dog", "realize_wet_cat_stare"), 0),
         (2.6, "大阪は安いお店が\nいっぱい！", ("blank_black_cat_zoning_out", "happy_girlfriend_dance_cat", "realize_wet_cat_stare"), 1)],
        [(2.8, "地方は冬の暖房代が\nちょっと高い", ("talk_orange_white_sitting_cat", "stare_interviewer_cat", "sad_black_dog"), 2)],
    ], [
        (2.8, "いちばん残るのは\nまさかの大阪！", ("sad_banana_cat_cry", "dance_orange_gray_cats", "blank_black_cat_zoning_out"), 1),   # 地方はぼーっと
        (2.6, "地方は車で\n家賃の安さが消える", ("realize_wet_cat_stare", None, "sulk_hungry_cat"), 2),
        (2.4, "東京は家賃が\nぜんぶ持っていく…", ("despair_dramatic_kitten", None, None), 0),
    ], ("東京は 毎月 −3.5万円", "大阪より1年で −42万円…", ("sad_banana_cat_cry", "happy_hamster_open_arms", "stare_tabby_wide_eyes_cat")))
    cs[0]["callout"] = ("住むならどこがおトク？", "都会vs地方 お金バトル")   # タイトルコール（10/27）
    return cs


if __name__ == "__main__":
    A.run(SPEC, cuts(), "short_33_chiiki")
