"""42_ev（EVvsガソリン車 10年でいくら違う？）（11/3 ユーザー指定・ガソリンvsハイブリッドと同じ作り）。3分ほど。

python3 catmeme/cuts_42_ev.py [--charts|--len]
数字はざっくりの目安（2026年・同じくらいの大きさのコンパクトカー・家で充電・10年乗って売る）：
  車の値段：EV 400万（国の補助金 約70万→実質330万）／ガソリン車 250万（差 80万）
  燃料代（年8000km）：ガソリン 18km/L・170円/L → 年7.6万（10年76万）／EV 6.5km/kWh・家の電気31円/kWh → 年3.8万（10年38万）
  税金（10年）：自動車税 EV 25万／ガソリン 30.5万。重量税 EV 約5万／ガソリン 約12万
  家の充電器の工事：約15万（EVだけ）。オイル交換など：ガソリン車だけ 10年で約15万
  10年後に売ると：EV 約30万（電池が古くなり安め）／ガソリン車 約40万
  → 年8000km：EV 約383万／ガソリン車 約344万（ガソリン車が約40万安い）
  → 年1万5000km：燃料 EV 72万・ガソリン 142万 → EV 約417万／ガソリン車 約410万（ほぼ同じ）
原稿のルール：実在の車の名前・メーカー名は出さない。今日の一言はエンディング画面・単語の途中で改行しない
"""
import compare_long as C
import wide_bars as B

DEALER, GAS, ROAD, PARK, STREET, NIGHT = ("bg26_car_dealer", "bg26_gas_station", "bg26_rural_road", "bg26_parking_lot",
                                          "bg48_clean_street", "bg14_home_night")
C.setup("42_ev", {})
bg, nn, ss, boom, qq, g, fx, chap = C.bg, C.nn, C.ss, C.boom, C.qq, C.g, C.fx, C.chap
CONAN, POON, MONEY = C.CONAN, C.POON, C.MONEY

VS = [("EV", "teal"), ("ガソリン車", "orange")]
HEAD = "10年でかかるお金（年8000km・目安）"
EV = [("車の値段（補助金のあと）", 330, "teal"), ("電気代", 38, "gold"), ("税金", 30, "navy"), ("充電器の工事", 15, "purple")]
GS = [("車の値段", 250, "orange"), ("ガソリン代", 76, "gold"), ("税金", 42.5, "navy"), ("オイル交換など", 15, "purple")]


def steps(ev, gs, have_ev=(), have_gs=(), t0=0.5, gap=0.9):
    st = [(-1, 0, n, v, c) for n, v, c in EV if n in have_ev] + [(-1, 1, n, v, c) for n, v, c in GS if n in have_gs]
    k = 0
    for side, rows, names in ((0, EV, ev), (1, GS, gs)):
        for n, v, c in rows:
            if n in names:
                st.append((t0 + gap * k, side, n, v, c))
                k += 1
    return st


C.charts({
    "e1_price": B.Chart([("EV（補助金の前）", "teal"), ("EV（補助金のあと）", "blue"), ("ガソリン車", "orange")],
                        [(0.4, 0, "", 400, "teal"), (1.2, 1, "", 330, "blue"), (2.0, 2, "", 250, "orange")], 450, bg=DEALER,
                        head="車の値段（目安）", total_fmt="{v}万", highlight=1),
    "e2_fuel": B.Chart(VS, [(0.4, 0, "家で充電", 3.8, "teal"), (1.4, 1, "18km/L", 7.6, "orange")], 9, bg=GAS,
                       head="1年の燃料代（年8000km）", total_fmt="年{v}万", highlight=0),
    "e3_all": B.Chart(VS, steps(["電気代", "税金", "充電器の工事"], ["ガソリン代", "税金", "オイル交換など"],
                                have_ev=["車の値段（補助金のあと）"], have_gs=["車の値段"]), 450, bg=MONEY, head=HEAD,
                      result_at=6.2, highlight=1),
    "e4_sell": B.Chart(VS, [(0.4, 0, "売った分を引くと", 383, "teal"), (1.4, 1, "売った分を引くと", 344, "orange")], 450, bg=MONEY,
                       head="10年後に売った分を引くと（年8000km）", total_fmt="{v}万", result_at=2.4, highlight=1),
    "e5_15000": B.Chart(VS, [(0.4, 0, "年1万5000km", 417, "teal"), (1.4, 1, "年1万5000km", 410, "orange")], 450, bg=ROAD,
                        head="たくさん走る人の10年（売った分を引く）", total_fmt="{v}万", result_at=2.4),
})


def cuts_all():
    return [
        # ---- つかみ ----
        nn("EVって\n電気で走るから\nめちゃくちゃ安いんでしょ？", DEALER, se="question_hatena_maou", bgm={"file": C.PURPLE, "gain": -4}),
        ss("電気代は\nたしかに\nガソリン代の半分", DEALER, se="pi"),
        C.slot(MONEY, "でも10年でくらべると ガソリン車のほうが 約", 40, "万円安い"),
        boom("ガソリン車の\nほうが安い!?", MONEY, se=[CONAN]),
        fx(nn("え……\nEVって\nお得じゃないの？", MONEY, se=POON), "mono"),
        C.title(STREET, "drive_driving_cat", "money_counting_orange_cat"),
        C.card("e02_premise", "同じくらいの大きさのコンパクトカーでくらべる", dur=5.2),
        # ---- 車の値段 ----
        chap("① 車の値段", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("EVは\n大きな電池を積むので\n値段が高い", DEALER, se="pi"),
        ss("同じくらいの大きさで\nEVは400万\nガソリン車は250万", DEALER, se="kon"),
        ss("でもEVには\n国の補助金がある", DEALER, se="pikon"),
        ss("車によって\n約70万前後\n住む町の補助金もあることも", DEALER, se="kon"),
        g("e1_price", "補助金のあとでも\n80万高い", dur=4.6),
        boom("それでも\n80万の差!?", DEALER, se=["explosion_chudoon"]),
        # ---- 電気代 ----
        chap("② 電気代とガソリン代", se="doon_heavy"),
        ss("ガソリン車は\n年8000km走ると\nガソリン代 年7.6万", GAS, se="pi"),
        ss("EVは家で\n夜に充電すると\n年3.8万", NIGHT, se="kon"),
        g("e2_fuel", "燃料代は\n半分", dur=3.8),
        nn("毎年4万も\n安いじゃん！", GAS, se="pikon"),
        ss("でも外の急速充電は\n高めなので\n家で充電できるかが大事", PARK, se="pc_warning"),
        nn("マンションだと\n充電できないことも\nあるのか", PARK, se="question_hatena_maou"),
        # ---- 税金とメンテ ----
        chap("③ 税金とメンテナンス", se="whoosh_shu", bgm={"file": C.COCOA, "gain": -4, "fade": 0.6}),
        ss("EVは\n自動車税や重量税が\n安い", STREET, se="kon"),
        ss("エンジンがないので\nオイル交換も\nいらない", STREET, se="pikon"),
        ss("そのかわり\n家に充電器をつける\n工事が約15万", NIGHT, se="kon"),
        g("e3_all", "ぜんぶ積むと……", dur=7.2),
        fx(boom("EV413万\nガソリン車384万!!", MONEY, se=["explosion_dokaan"]), "money"),
        # ---- 売る値段 ----
        chap("④ 10年後に売ると", se="doon_heavy", bgm={"file": C.MIRAI, "gain": -4, "fade": 0.6}),
        ss("EVは\n電池が古くなると\n値段が下がりやすい", PARK, se="pi"),
        ss("10年後\nEVは約30万\nガソリン車は約40万", PARK, se="kon"),
        g("e4_sell", "売った分を\n引くと……", dur=4.4),
        qq(MONEY, "anime_conan_hirameki_remix_b"),
        fx(boom("ガソリン車が\n約40万安い!!", MONEY, se=["explosion_chudoon"]), "money"),
        fx(nn("え……\n電気代が安いのに\n負けるの？", MONEY, se="tv_professional_poon_remix_a"), "swirl"),
        # ---- 逆転する人 ----
        chap("⑤ EVが勝つ人", se="quiz_question_01"),
        ss("たくさん走る人は\n燃料代の差が\nどんどん広がる", ROAD, se="pi"),
        g("e5_15000", "年1万5000kmなら\nほぼ同じ", dur=4.4),
        boom("走るほど\nEVが追いつく!?", ROAD, se=["explosion_dokaan"]),
        ss("家に太陽光パネルが\nあれば\n電気代はもっと安い", NIGHT, se="shine_kiraan_maou"),
        ss("停電のときに\n家の電気として\n使える車もある", NIGHT, se="kon"),
        # ---- お金以外 ----
        chap("⑥ お金以外のちがい", se="whoosh_shu", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("EVは静かで\n加速がなめらか", ROAD, se="kon"),
        ss("でも長い旅行は\n充電する場所と\n時間を考える", ROAD, se="kon"),
        nn("ガソリンスタンドより\nコンセントのほうが\n近いかも", NIGHT, se="pikon"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy"),
        C.card("e07_points", "走る量と 家で充電できるかで決めよう", dur=5.6),
        nn("EVは\n使い方しだいで\n得にも損にもなる", NIGHT, se="kon"),
        ss("補助金は毎年変わるので\n買う前に\n確認しよう", NIGHT, se="pc_warning"),
        C.ending(STREET)[0],
        C.end_today(STREET, (("drive_driving_cat", 220, 560), ("dance_three_kittens", 640, 520), ("money_counting_orange_cat", 1000, 560),
                             ("drive_monkey_golf_cart", 1360, 560), ("dance_happy_banana_cat", 1720, 600))),
    ]


if __name__ == "__main__":
    C.main("42_ev", cuts_all, ["e1_price", "e2_fuel", "e3_all", "e4_sell", "e5_15000"])
