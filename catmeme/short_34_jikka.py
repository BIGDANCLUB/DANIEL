"""ショート34：実家暮らしvsひとり暮らし 毎月いくら残る？（10/27 ユーザー指定：⑤ short_33_chiiki と同じルールで作り直し。RULES_bars_short.md）。59.9秒。
数字は手取り月22万（20代・年収330万くらい）のざっくりの目安。実家は家に月3万入れる。ひとり暮らしは東京近郊のワンルーム。
BGM なし（10/23 ルール）"""
import bars_auto as A

SPEC = dict(
    bg="bg14_home_night",
    title=("実家暮らしvsひとり暮らし", "毎月いくら残る？"),
    incomes=(22, 22),
    cards=[("実家", "暮らし", "手取り22万"), ("ひとり", "暮らし", "手取り22万")],
    card_cols=[(0, 120, 200), (200, 30, 30)],
    items=[("家に入れるお金", "red"), ("家賃", "green"), ("食費", "orange"), ("光熱費・スマホ", "purple")],
    values={"家に入れるお金": (3.0, 0), "家賃": (0, 7.0), "食費": (1.0, 4.0), "光熱費・スマホ": (0.5, 1.8)},
    take_word="残り",
    style="bright",
    wlabel={"家に入れるお金": "家に\n入れるお金", "光熱費・スマホ": "光熱費\nスマホ"},
)


def cuts():
    D = "dance_three_kittens"   # 冒頭は同じ素材を列の数だけ（3匹で踊る子猫）
    cs = A.build(SPEC, [
        (2.9, None, (D, D), (0, 1)),
        (3.0, "どっちも\n手取りは22万！", ("sleepy_old_memories_cat", "showoff_gojo_cosplay_cat"), 1),
        (2.6, "家に3万入れてるから\nうちも大変なんだよ", ("talk_orange_white_sitting_cat", "cocky_dj_cat"), 0),
        (2.2, "……3万で？", ("sleepy_sleepy_cat", "huh_huh_cat"), 1),
    ], [
        [(2.6, "実家は\n家に3万入れる", ("realize_wet_cat_stare", "stare_interviewer_cat"), 0, "もっと入れろや"),
         (2.4, "ひとり暮らしは\n0円…でも", ("happy_hamster_open_arms", "think_bike_front_seat_cat"), 1)],
        [(2.8, "家賃7万！？\nこれが一番重い", ("laugh_laughing_dog", "stare_tabby_wide_eyes_cat"), (0, 1)),
         (2.6, "実家は\n家賃0円", ("dance_tabby_standing_cat", "despair_dramatic_kitten"), 0)],
        [(2.8, "ご飯が\n勝手に出てくる…", ("eat_pop_cat", "sulk_hungry_cat"), 1),
         (2.6, "ひとり暮らしは\n自炊しても4万", ("happy_girlfriend_dance_cat", "eat_crunchy_cat_luna"), 1)],
        [(2.8, "電気代もネットも\n全部自分で払う", ("yell_orange_fat_cat", "sad_black_dog"), (0, 1)),
         (2.6, "実家はスマホ代だけ", ("cocky_dj_cat", "blank_black_cat_zoning_out"), 0)],
    ], [
        (2.8, "同じ給料なのに\n毎月8万以上ちがう…", ("dance_tabby_standing_cat", "stare_tabby_wide_eyes_cat"), 1),
        (2.6, "その分を貯金にまわせば\n大きな差になる", ("rage_talking_cat", "realize_wet_cat_stare"), 0),
    ], ("実家暮らしは 毎月 +8.3万円", "1年で 約100万円 貯金できる！", ("happy_hamster_open_arms", "sad_banana_cat_cry"), "good"))
    cs[0]["callout"] = ("住むならどっちがおトク？", "親元vsひとり 貯金バトル")   # タイトルコール（上の帯とはちがう言葉）
    return cs


if __name__ == "__main__":
    A.run(SPEC, cuts(), "short_34_jikka")
