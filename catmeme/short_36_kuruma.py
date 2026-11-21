"""ショート36：車ありvs車なし 1年でかかるお金（bars_auto.py・ショート27と同じ作り）。59.9秒。
数字は手取り年300万・地方都市・コンパクトカー（250万円を5年ローン）のざっくりの目安。
車本体 約50万/年、保険・税金・車検 約20万/年、ガソリン・駐車場 約17万/年。車なしは電車・バス・タクシー 約15万/年。
BGM なし（10/23 ルール）"""
import bars_auto as A

SPEC = dict(
    bg="bg48_clean_street",
    title=("車ありvs車なし", "1年でかかるお金"),
    incomes=(300, 300),
    cards=[("車あり", "マイカー", "手取り300万"), ("車なし", "電車・バス", "手取り300万")],
    card_cols=[(200, 30, 30), (0, 120, 200)],
    items=[("車のローン", "red"), ("保険・税金・車検", "purple"), ("ガソリン・駐車場", "orange"), ("電車・バス・タクシー", "green")],
    values={"車のローン": (50, 0), "保険・税金・車検": (20, 0), "ガソリン・駐車場": (17, 0), "電車・バス・タクシー": (0, 15)},
    take_word="残り",
)


def cuts():
    return A.build(SPEC, [
        (3.0, "手取りはどっちも\n年300万！", ("drive_driving_cat", "ride_kitten_bike"), 0),
        (2.6, "車は便利だし\n絶対必要でしょ", ("showoff_gojo_cosplay_cat", "stare_big_eyes_tabby_kitten"), 0),
        (2.2, "……いくらかかるか\n知ってる？", ("sleepy_sleepy_cat", "huh_huh_cat"), 1),
    ], [
        [(2.8, "250万の車を\n5年ローンで年50万", ("stare_tabby_wide_eyes_cat", "cocky_dj_cat"), 1),
         (2.4, "払い終わるのは\n5年後…", ("despair_dramatic_kitten", "happy_hamster_open_arms"), 0)],
        [(2.8, "自動車税・保険・車検で\n年20万", ("sulk_hungry_cat", "talk_orange_white_sitting_cat"), 1),
         (2.4, "乗らなくても\nかかるお金", ("sad_banana_cat_cry", "realize_wet_cat_stare"), 1)],
        [(2.8, "ガソリン代と\n駐車場で年17万", ("blank_black_cat_zoning_out", "dance_three_kittens"), 1)],
        [(2.8, "車なしは\n電車とタクシーで年15万", ("glare_disgusted_cat", "read_book_orange_kitten"), 1),
         (2.4, "雨の日は\nちょっと大変", ("laugh_laughing_dog", "sleepy_old_memories_cat"), 1)],
    ], [
        (2.8, "1年で\n70万以上ちがう…", ("stare_tabby_wide_eyes_cat", None), 0),
        (2.6, "でも地方は\n車がないと不便", ("realize_wet_cat_stare", "think_bike_front_seat_cat"), 0),
        (2.4, "必要かどうか\nよく考えよう", ("talk_orange_white_sitting_cat", "happy_girlfriend_dance_cat"), 1),
    ], ("車ありは 1年で −72万円", "10年で −720万円…", ("despair_dramatic_kitten", "dance_tabby_standing_cat")))


if __name__ == "__main__":
    A.run(SPEC, cuts(), "short_36_kuruma")
