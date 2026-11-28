"""ショート35：10年前と今 5000円でおつりはいくら？（bars_auto.py・ショート27と同じ作り）。59.9秒。
同じ買い物かご（米5kg・卵10個・牛乳1L・食パン）。値段はスーパーのざっくりの目安。
2016年：米 約2000円・卵 約220円・牛乳 約200円・食パン 約160円。2026年：米 約4000円・卵 約300円・牛乳 約260円・食パン 約200円。
BGM なし（10/23 ルール）"""
import bars_auto as A

SPEC = dict(
    bg="bg16_food_aisle",
    title=("10年前と今", "5000円でおつりはいくら？"),
    incomes=(5000, 5000),
    cards=[("2016年", "10年前", "5000円"), ("2026年", "今", "5000円")],
    card_cols=[(0, 120, 200), (200, 30, 30)],
    items=[("お米5kg", "green"), ("卵10個", "orange"), ("牛乳1L", "purple"), ("食パン", "dark")],
    values={"お米5kg": (2000, 4000), "卵10個": (220, 300), "牛乳1L": (200, 260), "食パン": (160, 200)},
    unit="円", take_word="おつり", left_word="のこったおつり",
)


def cuts():
    return A.build(SPEC, [
        (3.0, "同じ買い物かごに\n5000円を持っていく！", ("sleepy_old_memories_cat", "showoff_gojo_cosplay_cat"), 1),
        (2.6, "お米と卵と牛乳と\nパンだけだし余裕でしょ", ("stare_big_eyes_tabby_kitten", "cocky_dj_cat"), 1),
        (2.2, "……本当に？", ("sleepy_sleepy_cat", "huh_huh_cat"), 1),
    ], [
        [(2.8, "お米が\n2倍になってる！？", ("realize_wet_cat_stare", "stare_tabby_wide_eyes_cat"), 1),
         (2.6, "これだけで\n4000円…", ("sleepy_old_memories_cat", "despair_dramatic_kitten"), 1)],
        [(2.8, "卵も\nじわじわ値上がり", ("talk_orange_white_sitting_cat", "sulk_hungry_cat"), 1)],
        [(2.8, "牛乳も\n60円アップ", ("happy_hamster_open_arms", "blank_black_cat_zoning_out"), 1),
         (2.6, "ひとつひとつは\n少しなのに…", ("dance_three_kittens", "sad_black_dog"), 1)],
        [(2.8, "食パンは\n少し小さくなった気も", ("eat_pop_cat", "peek_what_happen_cat"), 1),
         (2.6, "ステルス値上げって\nやつだね", ("read_book_orange_kitten", "glare_disgusted_cat"), 0)],
    ], [
        (2.8, "同じかごなのに\nおつりが2000円以上ちがう", (None, "stare_tabby_wide_eyes_cat"), 1),
        (2.6, "10年前は\nおつりで外食できた", ("happy_girlfriend_dance_cat", "sulk_hungry_cat"), 0),
        (2.4, "今はおつりで\nジュース1本…", ("realize_wet_cat_stare", "despair_dramatic_kitten"), 1),
    ], ("おつり −2180円", "同じかごが10年で1.8倍…", ("dance_tabby_standing_cat", "sad_banana_cat_cry")))


if __name__ == "__main__":
    A.run(SPEC, cuts(), "short_35_kago")
