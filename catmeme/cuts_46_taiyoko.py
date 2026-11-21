"""46_taiyoko（太陽光パネルは何年で元が取れる？）（11/10 ユーザー指定・長尺候補14番・EV回と同じ作り）。2分ほど。

python3 catmeme/cuts_46_taiyoko.py [--charts|--len]
数字はざっくりの目安（一戸建て・4kW・2025〜2026年ごろ）。記事の目安とそこからの計算：
  設置費用 1kWあたり約28.6万→4kWで約115万（記事では4kWで100〜130万）
  発電量 1kWで年約1100kWh→4kWで年約4400kWh（一般的な目安）
  家で使う分 3割（1320kWh）×電気代31円＝年約4.1万の節約／売る分 7割（3080kWh）×15円＝年約4.6万 → 年約8.7万
  → 115万÷8.7万＝約13年で元が取れる計算（記事では条件がよければ7年ほど）。売る値段は10年たつと大きく下がる
  国の補助金は終わっている。東京都など町の補助金がある所も
原稿のルール：つける人・つけない人をけなさない。発電量・電気代・売る値段で大きく変わると言う
"""
import compare_long as C
import wide_bars as B

HOUSE, STREET, NIGHT, SUN = ("bg35_house", "bg35_suburb_street", "bg14_home_night", "bg120_yellow_rays")
C.setup("46_taiyoko", {})
bg, nn, ss, boom, qq, g, fx, chap = C.bg, C.nn, C.ss, C.boom, C.qq, C.g, C.fx, C.chap
CONAN, POON, MONEY = C.CONAN, C.POON, C.MONEY

C.charts({
    "s1_cost": B.Chart([("設置費用", "red")], [(0.4, 0, "4kW", 115, "red")], 130, bg=HOUSE,
                       head="つけるお金（目安）", total_fmt="約{v}万", highlight=0),
    "s2_year": B.Chart([("1年でうくお金", "teal")],
                       [(0.4, 0, "家で使う分", 4.1, "teal"), (1.2, 0, "売る分", 4.6, "gold")], 10, bg=SUN,
                       head="1年でうくお金（目安）", total_fmt="約{v}万", result_at=2.0, highlight=0),
    "s3_payback": B.Chart([("つけたお金", "red"), ("ういたお金（13年）", "teal")],
                          [(0.4, 0, "", 115, "red")] + [(0.8 + 0.18 * k, 1, "", 8.7, ("teal", "gold")[k % 2]) for k in range(13)],
                          130, bg=MONEY, head="何年で元が取れる？", total_fmt="約{v}万", result_at=3.4, highlight=1),
})


def cuts_all():
    return [
        # ---- つかみ ----
        nn("太陽光パネルって\nつけたほうが\n得なの？", HOUSE, se="question_hatena_maou", bgm={"file": C.PURPLE, "gain": -4}),
        ss("電気代が\nどんどん上がる中", NIGHT, se="pi"),
        C.slot(MONEY, "4kWのパネルで\n元が取れるまで\n約", 13, "年", dur=3.6),
        boom("13年!?", MONEY, se=[CONAN]),
        fx(nn("意外と\nかかるのか", MONEY, se=POON), "swirl"),
        C.title(HOUSE, "think_chin_paw_orange_cat", "money_counting_orange_cat"),
        C.card("e02_premise", "一戸建てに4kWのパネルをつけた場合で計算", dur=5.2),
        # ---- つけるお金 ----
        chap("① つけるお金", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("一戸建ての屋根なら\n4kWくらいが\nよくある大きさ", HOUSE, se="pi"),
        ss("1kWあたり\n約28万円", HOUSE, se="kon"),
        g("s1_cost", "4kWだと……", dur=3.8),
        boom("約115万!!", HOUSE, se=["explosion_chudoon"]),
        ss("国の補助金は\nもう終わっている", STREET, se="kon"),
        ss("でも東京都など\n町の補助金が\nある所もある", STREET, se="pikon"),
        # ---- 1年でうくお金 ----
        chap("② 1年でうくお金", se="doon_heavy"),
        ss("4kWのパネルで\n1年に\n約4400kWh発電", SUN, se="pi"),
        ss("昼に家で使えば\nその分\n電気を買わなくていい", SUN, se="kon"),
        ss("使いきれない分は\n電力会社に\n売れる", SUN, se="kon"),
        g("s2_year", "ぜんぶ合わせると\n1年で……", dur=4.6),
        boom("年約8.7万!!", MONEY, se=["explosion_dokaan"]),
        nn("毎月7000円くらい\nうくのか", NIGHT, se="pikon"),
        # ---- 元が取れる ----
        chap("③ 何年で元が取れる？", se="whoosh_shu", bgm={"file": C.COCOA, "gain": -4, "fade": 0.6}),
        ss("115万円を\n年8.7万円で\n取りもどすと", MONEY, se="pi"),
        g("s3_payback", "何年かかる？", dur=6.4),
        qq(MONEY, "anime_conan_hirameki_remix_b"),
        fx(boom("約13年!!", MONEY, se=["explosion_chudoon"]), "money"),
        ss("記事によっては\n条件がよければ\n7年ほどという計算も", MONEY, se="kon"),
        nn("家で使う電気が\n多いほど\n早く取りもどせる", SUN, se="pikon"),
        # ---- 気をつけること ----
        chap("④ 気をつけたいこと", se="doon_heavy", bgm={"file": C.MIRAI, "gain": -4, "fade": 0.6}),
        ss("電気を売る値段は\n10年たつと\n大きく下がる", MONEY, se="pc_warning"),
        ss("屋根の向きや\n日当たりで\n発電量が変わる", HOUSE, se="kon"),
        ss("途中で\n機械の交換が\n必要になることも", HOUSE, se="kon"),
        nn("つける前に\nいくつか\n見積もりを取ろう", STREET, se="pikon"),
        # ---- 得する人 ----
        chap("⑤ 得しやすい人", se="quiz_question_01"),
        ss("昼に家にいる時間が\n長い人", NIGHT, se="pi"),
        ss("南向きの\n日当たりのいい屋根", HOUSE, se="kon"),
        ss("EVや蓄電池と\nいっしょに使う人", NIGHT, se="kon"),
        nn("停電のときに\n電気が使えるのも\nうれしい", NIGHT, se="shine_kiraan_maou"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        C.card("e07_points", "元が取れるのは7〜13年 家で使うほど得", dur=5.6),
        nn("太陽光は\n長く住む家ほど\n向いている", HOUSE, se="kon"),
        ss("町の補助金は\n毎年変わるので\n調べてから決めよう", STREET, se="pc_warning"),
        C.ending(HOUSE)[0],
        C.end_today(HOUSE, (("think_chin_paw_orange_cat", 220, 560), ("money_counting_orange_cat", 640, 560), ("happy_hamster_open_arms", 1000, 560),
                            ("sleep_sleeping_cat", 1360, 560), ("dance_cute_dog", 1720, 600))),
    ]


if __name__ == "__main__":
    C.main("46_taiyoko", cuts_all, ["s1_cost", "s2_year", "s3_payback"])
