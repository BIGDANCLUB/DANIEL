"""ショート32：家賃でわかる 同じ手取りでいくら残る？（10/27 ユーザー指定：⑤ short_33_chiiki と同じルールで作り直し。RULES_bars_short.md）。59.9秒。
冒頭は踊りまわる猫3匹（マクスウェル猫）。
数字は手取り月26万・ひとり暮らしのざっくりの目安。家賃4万は郊外の古いアパート（通勤が遠い・すきま風で光熱費高め）、
家賃8万は23区のワンルーム、家賃15万は駅直結のタワマン（まわりのお店が高い）。BGM なし"""
import bars_auto as A

SPEC = dict(
    bg="bg57_tokyo_skyline",
    title=("家賃でわかる", "同じ手取りでいくら残る？"),
    incomes=(26, 26, 26),
    cards=[("家賃4万", "郊外アパート", "手取り26万"), ("家賃8万", "23区1K", "手取り26万"), ("家賃15万", "タワマン", "手取り26万")],
    card_cols=[(0, 150, 60), (0, 120, 200), (200, 30, 30)],
    items=[("家賃", "green"), ("通勤・交通", "purple"), ("食費", "orange"), ("光熱費・スマホ", "dark")],
    values={"家賃": (4.0, 8.0, 15.0), "通勤・交通": (1.5, 0.5, 0.2), "食費": (4.0, 4.5, 6.0), "光熱費・スマホ": (1.6, 1.2, 1.3)},
    take_word="残り",
    style="bright",
    wlabel={"通勤・交通": "通勤\n交通費", "光熱費・スマホ": "光熱費\nスマホ"},
)


def cuts():
    D = "dance_maxwell_cat"   # 冒頭は踊りまわる猫3匹（10/27 ユーザー指定）
    cs = A.build(SPEC, [
        (2.9, None, (D, D, D), (0, 1, 2)),
        (3.0, "家賃はバラバラでも\n手取りはみんな26万！", ("sleepy_old_memories_cat", "cocky_dj_cat", "showoff_gojo_cosplay_cat"), 2),
        (2.6, "家賃が安いほうが\n勝ちに決まってるでしょ？", ("happy_hamster_open_arms", "stare_big_eyes_tabby_kitten", "rizz_cat_rizz"), 0),
        (2.2, "……本当に？", ("sleepy_sleepy_cat", "huh_huh_cat", "sleepy_sleepy_cat"), 1),
    ], [
        [(2.8, "タワマンの家賃\n15万！？", ("dance_tabby_standing_cat", "stare_interviewer_cat", "despair_dramatic_kitten"), 2),
         (2.6, "郊外は\nたった4万！", ("happy_girlfriend_dance_cat", "talk_orange_white_sitting_cat", "sad_banana_cat_cry"), 0)],
        [(2.8, "郊外は会社まで\n電車で1時間半", ("stare_tabby_wide_eyes_cat", "think_bike_front_seat_cat", "peek_what_happen_cat"), 0),
         (2.6, "タワマンは\n駅直結で歩いて1分", ("sulk_hungry_cat", "eat_chips_cat", "showoff_gojo_cosplay_cat"), 2)],
        [(2.8, "タワマンのまわりは\nスーパーが高い", ("realize_wet_cat_stare", "calmdown_dancing_cat", "stare_tabby_wide_eyes_cat"), 2),
         (2.6, "コンビニも\n高級スーパーしかない…", ("eat_pop_cat", "read_book_orange_kitten", "despair_dramatic_kitten"), 2)],
        [(2.8, "古いアパートは\nすきま風で暖房代が高い", ("glare_disgusted_cat", "stare_interviewer_cat", "blank_black_cat_zoning_out"), (0, 1))],
    ], [
        (2.8, "いちばん残るのは\n家賃4万！", ("dance_orange_gray_cats", "blank_black_cat_zoning_out", "sad_banana_cat_cry"), 0),
        (2.6, "でも通勤で\n毎日3時間…", ("sleepy_old_memories_cat", "realize_wet_cat_stare", "eat_chips_cat"), 0),
        (2.4, "タワマンは家賃が\nぜんぶ持っていく…", ("think_bike_front_seat_cat", "stare_interviewer_cat", "despair_dramatic_kitten"), 2),
    ], ("タワマンは 毎月 −11.4万円", "郊外より1年で −137万円…", ("happy_hamster_open_arms", "stare_tabby_wide_eyes_cat", "sad_banana_cat_cry")))
    cs[0]["se"] = "silly"   # マクスウェル猫は曲の権利の都合で音を出せないので、楽しい効果音をのせる
    cs[0]["callout"] = ("どの部屋がいちばんおトク？", "家賃3番勝負")   # タイトルコール（上の帯とはちがう言葉）
    return cs


if __name__ == "__main__":
    A.run(SPEC, cuts(), "short_32_yachin")
