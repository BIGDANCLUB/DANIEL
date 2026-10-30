"""ショート51：年収300万・500万・1000万 税金と社会保険でいくら引かれる？（bars_auto.py・東京大阪地方⑤と同じ作り・10/30 ユーザー指定）。59.9秒。
会社員・ひとり暮らし・扶養なしのざっくりの目安（2026年ごろ）：
- 社会保険（健康保険・厚生年金・雇用保険）：約45万／約75万／約145万
- 所得税：約6万／約15万／約85万（年収が上がるほど税率が上がる：5%→10%→33%）
- 住民税：約12万／約25万／約60万
→ 手取り 約237万／約385万／約710万
BGM なし
"""
import bars_auto as A

SPEC = dict(
    bg="bg25_office_desk",
    title=("年収300万・500万・1000万", "税金でいくら引かれる？"),
    incomes=(300, 500, 1000),
    cards=[("年収", "300万", "会社員"), ("年収", "500万", "会社員"), ("年収", "1000万", "会社員")],
    card_cols=[(0, 150, 60), (0, 120, 200), (200, 30, 30)],
    items=[("社会保険", "purple"), ("所得税", "orange"), ("住民税", "green")],
    values={"社会保険": (45, 75, 145), "所得税": (6, 15, 85), "住民税": (12, 25, 60)},
    take_word="手取り",
    style="bright",
)


def cuts():
    M = "dance_three_kittens"
    cs = A.build(SPEC, [
        (2.9, None, (M, M, M), (0, 1, 2)),
        (3.0, "年収1000万なら\n勝ち組でしょ！", ("sleepy_old_memories_cat", "think_chin_paw_orange_cat", "showoff_gojo_cosplay_cat"), 2),
        (2.6, "……手取りは\nいくらだと思う？", ("stare_interviewer_cat", "talk_orange_white_sitting_cat", "huh_huh_cat"), 1),
    ], [
        [(2.8, "まずは社会保険\n健康保険と年金", ("sulk_hungry_cat", "read_book_orange_kitten", "stare_tabby_wide_eyes_cat"), 1),
         (2.4, "1000万だと\n年145万！？", ("blank_black_cat_zoning_out", "eat_chips_cat", "despair_dramatic_kitten"), 2)],
        [(2.8, "所得税は年収が上がるほど\n税率も上がる", ("talk_orange_white_sitting_cat", "think_bike_front_seat_cat", "scream_phone_orange_cat"), 0),
         (2.4, "1000万は\n税率33%の段階も", ("calmdown_dancing_cat", "realize_wet_cat_stare", "sad_banana_cat_cry"), 2)],
        [(2.8, "住民税は\nだいたい一律10%", ("eat_pop_cat", "money_counting_orange_cat", "sad_looking_away_tabby"), 1)],
    ], [
        (2.8, "年収1000万の手取りは\n約710万……", ("happy_chipi_chapa_cat", "realize_wet_cat_stare", "despair_dramatic_kitten"), 2),
        (2.6, "年収が3倍でも\n手取りは3倍にならない", ("think_chin_paw_orange_cat", "stare_interviewer_cat", "sulk_hungry_cat"), 1),
        (2.4, "みんなも\n手取りで考えよう", ("talk_orange_white_sitting_cat", "happy_hamster_open_arms", "dance_happy_banana_cat"), 0),
    ], ("1000万は 毎年 −290万円", "税金と社会保険だけで…", ("dance_happy_banana_cat", "think_chin_paw_orange_cat", "despair_dramatic_kitten")))
    cs[0]["callout"] = ("年収が上がると", "税金はどれだけふえる？")
    return cs


if __name__ == "__main__":
    A.run(SPEC, cuts(), "short_51_zeikin")
