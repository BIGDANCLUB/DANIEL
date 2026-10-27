"""ショート27：コロナ前と今 同じ月給でどっちが余裕？（10/27 ユーザー指定：⑤ short_33_chiiki と同じルールで作り直し。RULES_bars_short.md）。59.9秒。
列：2019年 月給30万／2026年 月給30万の2つ（賃上げ後の列はなし）。1か月あたりのざっくりの目安（東京でひとり暮らしの会社員）
- 税金・社会保険：約6.2万 → 約6.4万。家賃（23区ワンルーム）：約8.0万 → 約9.5万。光熱費＋スマホ：約1.9万 → 約1.9万。食費：約4.0万 → 約4.8万
BGM なし"""
import bars_auto as A

SPEC = dict(
    bg="bg57_tokyo_skyline",
    title=("コロナ前と今", "同じ月給でどっちが余裕？"),
    incomes=(30, 30),
    cards=[("2019年", "コロナ前", "月給30万"), ("2026年", "今", "月給30万")],
    card_cols=[(0, 120, 200), (200, 30, 30)],
    items=[("税金・社保", "red"), ("家賃", "green"), ("光熱費・スマホ", "purple"), ("食費", "orange")],
    values={"税金・社保": (6.2, 6.4), "家賃": (8.0, 9.5), "光熱費・スマホ": (1.9, 1.9), "食費": (4.0, 4.8)},
    take_word="残り",
    style="bright",
    wlabel={"税金・社保": "税金\n社会保険", "光熱費・スマホ": "光熱費\nスマホ"},
)


def cuts():
    M = "scream_standing_marmot_fast"   # 冒頭は同じ素材を列の数だけ（叫ぶマーモット）
    cs = A.build(SPEC, [
        (2.9, None, (M, M), (0, 1)),
        (3.0, "コロナ前と今\n月給は同じ30万！", ("sleepy_old_memories_cat", "showoff_gojo_cosplay_cat"), 1),
        (2.6, "なら暮らしも\n同じでしょ？", ("stare_big_eyes_tabby_kitten", "cocky_dj_cat"), 1),
        (2.2, "……本当に？", ("sleepy_sleepy_cat", "huh_huh_cat"), 1),
    ], [
        [(2.8, "ここは\nほとんど変わらない", ("calmdown_dancing_cat", "talk_orange_white_sitting_cat"), 1),
         (2.6, "雇用保険料が\nちょっと上がったくらい", ("peek_what_happen_cat", "read_book_orange_kitten"), 1)],
        [(2.8, "同じワンルームで\n1.5万も高い！？", ("sleepy_old_memories_cat", "stare_tabby_wide_eyes_cat"), (0, 1)),
         (2.6, "都心の家賃は\nずっと上がりっぱなし…", ("happy_hamster_open_arms", "sad_banana_cat_cry"), 1)],
        [(2.8, "電気代は上がったけど\nスマホ代は下がった！", ("talk_orange_white_sitting_cat", "happy_girlfriend_dance_cat"), 1),
         (2.4, "ここは\n引き分け！", ("dance_orange_gray_cats", "dance_three_kittens"), 0)],
        [(2.8, "同じものを買っても\n1か月で8000円高い", ("rizz_cat_rizz", "despair_dramatic_kitten"), 1)],
    ], [
        (2.8, "同じ給料なのに\n毎月2.5万も少ない…", ("dance_tabby_standing_cat", "stare_tabby_wide_eyes_cat"), 1),
        (2.6, "給料より\n物の値段が先に上がった", ("realize_wet_cat_stare", "blank_black_cat_zoning_out"), 0),
    ], ("今は 毎月 −2.5万円", "1年で −30万円…", ("happy_chipi_chapa_cat", "sad_banana_cat_cry")))
    cs[0]["callout"] = ("あの頃のほうがマシだった？", "物価高 お財布バトル")   # タイトルコール（上の帯とはちがう言葉）
    return cs


if __name__ == "__main__":
    A.run(SPEC, cuts(), "short_27_corona")
