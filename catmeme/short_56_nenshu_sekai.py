"""ショート56：アメリカ・韓国・日本 平均年収と手取りはいくら？（bars_auto.py・税金のショートと同じ作り・10/31 ユーザー指定）。59.9秒。
ざっくりの目安（会社員の平均・円換算は為替や計算方法で大きく変わる）：
- 平均年収：アメリカ 約1100万（OECD のドル建て平均賃金を円にした目安）／韓国 約540万（2024年・常用労働者 4917万ウォン）／日本 約460万（2023年）
- 税金（所得税・住民税など）：約180万／約30万／約35万
- 社会保険：約85万／約50万／約68万
→ 手取り 約835万／約460万／約357万
BGM なし
"""
import bars_auto as A

SPEC = dict(
    bg="bg44_world_map",
    title=("アメリカ・韓国・日本", "平均年収と手取りは？"),
    incomes=(1100, 540, 460),
    cards=[("アメリカ", "平均年収", "約1100万"), ("韓国", "平均年収", "約540万"), ("日本", "平均年収", "約460万")],
    card_cols=[(222, 92, 8), (0, 148, 152), (166, 8, 172)],
    items=[("社会保険", "gray"), ("税金", "red")],
    values={"社会保険": (85, 50, 68), "税金": (180, 30, 35)},
    take_word="手取り",
    style="classic",
)


def cuts():
    M = "dance_three_kittens"
    cs = A.build(SPEC, [
        (2.9, None, (M, M, M), (0, 1, 2)),
        (3.0, "日本の給料って\n世界ではどのくらい？", ("think_chin_paw_orange_cat", "talk_orange_white_sitting_cat", "stare_big_eyes_tabby_kitten"), 2),
        (2.6, "……韓国にも\nぬかれてる？", ("stare_interviewer_cat", "huh_huh_cat", "despair_dramatic_kitten"), -1),   # 11/1：泣いている猫の音
    ], [
        [(2.8, "まずは社会保険\n年金と健康保険", ("sulk_hungry_cat", "read_book_orange_kitten", "stare_tabby_wide_eyes_cat"), 0),
         (2.4, "日本は\n年68万", ("blank_black_cat_zoning_out", "eat_chips_cat", "sad_looking_away_tabby"), 2)],
        [(2.8, "アメリカは税金が\n州によってちがう", ("talk_orange_white_sitting_cat", "think_bike_front_seat_cat", "scream_phone_orange_cat"), 0),
         (2.4, "それでも手取りは\n日本の2倍以上！？", ("cocky_dj_cat", "realize_wet_cat_stare", "stare_tabby_wide_eyes_cat"), 0)],
    ], [
        (2.8, "日本の手取りは\n約357万……", ("happy_chipi_chapa_cat", "realize_wet_cat_stare", "despair_dramatic_kitten"), 2),
        (2.6, "アメリカは物価も高い\n家賃もランチも", ("calm_black_face_sheep", "think_chin_paw_orange_cat", "sulk_hungry_cat"), 0),
        (2.4, "みんなはこの金額\nどう思いますか？", ("talk_orange_white_sitting_cat", "happy_hamster_open_arms", "dance_happy_banana_cat"), 0),
    ], ("アメリカとの差 年 −478万円", "手取りで比べても…", ("cocky_dj_cat", "think_chin_paw_orange_cat", "despair_dramatic_kitten")))
    for c in cs:   # 11/1：「韓国にもぬかれてる？」は泣いている猫の音（猫の声のかわり）
        if (c.get("say") or "").startswith("……韓国にも"):
            c["se"] = [{"f": "cat_crying_sad", "gain": 0}]
            c["no_huh"] = True
    cs[0]["callout"] = ("日本の給料は", "世界で何番目？")
    cs[0]["callout_style"] = "b"
    cs[0]["se"] = ["whoosh_shu", {"f": "explosion_chudoon", "at": 0.22}, {"f": "shine_kiraan_maou", "at": 0.45}]
    return cs


if __name__ == "__main__":
    A.run(SPEC, cuts(), "short_56_nenshu_sekai")
