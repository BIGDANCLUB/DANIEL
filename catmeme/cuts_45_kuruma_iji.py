"""45_kuruma_iji（車を持つと10年でいくら？ 維持費ぜんぶ足してみた）（11/10 ユーザー指定・長尺候補7番・EV回と同じ作り）。2分ほど。

python3 catmeme/cuts_45_kuruma_iji.py [--charts|--len]
数字はざっくりの目安（コンパクトカー・1000cc前後・2025〜2026年ごろ）。記事の目安とそこからの計算：
  自動車税 年3.05万（1000〜1500cc）／重量税 2年2.46万→年約1.2万／自賠責 2年約1.77万→年約0.9万
  任意保険 年約7万（人によって大きく変わる）／ガソリン 月約1万→年12万／駐車場 月1万→年12万（地方0〜都会3万）
  車検の整備・点検・オイル・タイヤ 年約5万 → 1年 約41万（1か月 約3.4万）→ 10年 約410万
  車の値段 約200万を足すと 10年で約610万（1か月 約5万）。駐車場がいらない地方なら 10年で約490万
原稿のルール：車を持つ人・持たない人をけなさない。保険と駐車場は人によって大きく変わると言う
"""
import compare_long as C
import wide_bars as B

DEALER, GAS, PARK, TOKYO, ROAD, INSPECT = ("bg26_car_dealer", "bg26_gas_station", "bg26_parking_lot", "bg26_tokyo_parking",
                                           "bg26_rural_road", "bg26_car_inspection")
C.setup("45_kuruma_iji", {})
bg, nn, ss, boom, qq, g, fx, chap = C.bg, C.nn, C.ss, C.boom, C.qq, C.g, C.fx, C.chap
CONAN, POON, MONEY = C.CONAN, C.POON, C.MONEY

C.charts({
    "k1_year": B.Chart([("1年の維持費", "orange")],
                       [(0.4, 0, "税金", 4.3, "navy"), (1.0, 0, "自賠責", 0.9, "purple"), (1.6, 0, "任意保険", 7, "teal"),
                        (2.2, 0, "ガソリン", 12, "gold"), (2.8, 0, "駐車場", 12, "red"), (3.4, 0, "車検・点検など", 5, "blue")],
                       45, bg=PARK, head="1年でかかるお金（目安）", total_fmt="約{v}万", result_at=4.2, highlight=0),
    "k2_ten": B.Chart([("維持費だけ", "orange"), ("車の値段もこみ", "red")],
                      [(0.4, 0, "10年", 410, "orange"), (1.4, 1, "10年", 610, "red")], 650, bg=MONEY,
                      head="10年でかかるお金（目安）", total_fmt="約{v}万", result_at=2.4, highlight=1),
    "k3_area": B.Chart([("地方（駐車場0円）", "teal"), ("都会（駐車場 月3万）", "red")],
                       [(0.4, 0, "10年", 490, "teal"), (1.4, 1, "10年", 850, "red")], 900, bg=TOKYO,
                       head="住む場所で変わる 10年のお金（車の値段こみ）", total_fmt="約{v}万", result_at=2.4),
})


def cuts_all():
    return [
        # ---- つかみ ----
        nn("車って\n買ったあとも\nいくらかかるの？", DEALER, se="question_hatena_maou", bgm={"file": C.PURPLE, "gain": -4}),
        ss("ガソリン代くらい\nと思っていると", GAS, se="pi"),
        C.slot(MONEY, "車の値段もこみで\n10年乗ると\n約", 610, "万円", dur=3.6),
        boom("610万!?", MONEY, se=[CONAN]),
        fx(nn("1か月\n5万円くらい\nかかってるの!?", MONEY, se=POON), "swirl"),
        C.title(ROAD, "drive_driving_cat", "money_counting_orange_cat"),
        C.card("e02_premise", "コンパクトカーを10年乗った場合でくらべる", dur=5.2),
        # ---- 税金 ----
        chap("① 毎年かかる税金", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("毎年5月に\n自動車税の\nお知らせが来る", PARK, se="pi"),
        ss("1000ccから1500ccの車で\n年3万500円", PARK, se="kon"),
        ss("車検のときには\n重量税と\n自賠責保険も", INSPECT, se="kon"),
        nn("持っているだけで\n年5万円くらい\nかかるのか", PARK, se="question_hatena_maou"),
        # ---- 保険とガソリン ----
        chap("② 保険とガソリン", se="doon_heavy"),
        ss("任意保険は\n年7万円くらい", DEALER, se="pi"),
        ss("年齢や\n事故歴で\n大きく変わる", DEALER, se="kon"),
        ss("ガソリン代は\n月1万円くらい\n年12万", GAS, se="kon"),
        nn("ガソリンが\n値上がりすると\nさらに増える", GAS, se="pc_warning"),
        # ---- 駐車場とメンテ ----
        chap("③ 駐車場とメンテナンス", se="whoosh_shu", bgm={"file": C.COCOA, "gain": -4, "fade": 0.6}),
        ss("駐車場は\n月1万円なら\n年12万", PARK, se="pi"),
        ss("都会だと\n月3万円以上も", TOKYO, se="kon"),
        ss("車検の整備\nオイル交換\nタイヤ交換", INSPECT, se="kon"),
        g("k1_year", "ぜんぶ足すと\n1年で……", dur=6.6),
        fx(boom("1年で\n約41万!!", MONEY, se=["explosion_dokaan"]), "money"),
        # ---- 10年 ----
        chap("④ 10年乗ると", se="doon_heavy", bgm={"file": C.MIRAI, "gain": -4, "fade": 0.6}),
        ss("維持費だけで\n10年で約410万", MONEY, se="pi"),
        ss("車の値段\n約200万を足すと", DEALER, se="kon"),
        g("k2_ten", "10年で\nかかるお金は……", dur=4.6),
        qq(MONEY, "anime_conan_hirameki_remix_b"),
        fx(boom("約610万!!", MONEY, se=["explosion_chudoon"]), "money"),
        fx(nn("1か月\n約5万円の\nサブスクみたいなもの!?", MONEY, se="tv_professional_poon_remix_a"), "swirl"),
        # ---- 住む場所 ----
        chap("⑤ 住む場所で変わる", se="quiz_question_01"),
        ss("地方は\n駐車場が\nタダのことも多い", ROAD, se="pi"),
        ss("都会は\n駐車場だけで\n10年で360万", TOKYO, se="kon"),
        g("k3_area", "地方と都会で\nこんなに違う", dur=4.6),
        boom("差は\n約360万!!", TOKYO, se=["explosion_dokaan"]),
        nn("都会は\n車がなくても\n暮らしやすい", TOKYO, se="pikon"),
        ss("地方は\n車がないと\n買い物も行けない", ROAD, se="kon"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        C.card("e07_points", "車は1か月約5万円 住む場所で大きく変わる", dur=5.6),
        nn("車は\n便利さを\n買っている", ROAD, se="kon"),
        ss("乗る回数が少ないなら\nカーシェアや\nレンタカーも考えよう", PARK, se="pc_warning"),
        C.ending(ROAD)[0],
        C.end_today(ROAD, (("drive_driving_cat", 220, 560), ("money_counting_orange_cat", 640, 560), ("think_chin_paw_orange_cat", 1000, 560),
                           ("drive_monkey_golf_cart", 1360, 560), ("dance_cute_dog", 1720, 600))),
    ]


if __name__ == "__main__":
    C.main("45_kuruma_iji", cuts_all, ["k1_year", "k2_ten", "k3_area"])
