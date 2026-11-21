"""38_hybrid（ガソリン車vsハイブリッド車 どっちが安い？）（11/1 ユーザー指定・車ありvs車なしと同じ作り）。3分ほど。

python3 catmeme/cuts_38_hybrid.py [--charts|--len]
数字はざっくりの目安（2026年・同じくらいの大きさのコンパクトカー・ガソリン170円/L）：
  車の値段：ガソリン車 約200万／ハイブリッド 約260万（差 約60万）
  実際の燃費：ガソリン車 約18km/L／ハイブリッド 約30km/L
  1年のガソリン代：年8000km → ガソリン車 約7.6万／ハイブリッド 約4.5万（差 約3.1万）
                   年1万km → 差 約3.8万／年2万km → 差 約7.6万
  60万の差を取り戻すには：年8000km → 約19年／年1万km → 約16年／年2万km → 約8年
  税金：自動車税はどちらも排気量で決まる（1.5Lなら年30,500円）。ハイブリッドはエコカー減税で最初の重量税などが安くなることがある（数万円）
  10年後に売ると：ハイブリッドのほうが高く売れやすい（目安 +20万）→ 年8000km・10年で ガソリン車 約256万／ハイブリッド 約265万（ほぼ同じ）
原稿のルール：実在の車の名前・メーカー名は出さない。今日の一言・単語の途中で改行しない・最後はチャンネル登録・過去の動画にはふれない
"""
import compare_long as C
import wide_bars as B

DEALER, GAS, ROAD, CITY, STREET = "bg26_car_dealer", "bg26_gas_station", "bg26_rural_road", "bg38_city_traffic", "bg48_clean_street"
C.setup("38_hybrid", {CITY: "bg57_tokyo_skyline"})
bg, nn, ss, boom, qq, g, fx, chap = C.bg, C.nn, C.ss, C.boom, C.qq, C.g, C.fx, C.chap
CONAN, POON, MONEY = C.CONAN, C.POON, C.MONEY

VS = [("ガソリン車", "orange"), ("ハイブリッド車", "teal")]
C.charts({
    "y1_price": B.Chart(VS, [(0.4, 0, "", 200, "orange"), (1.4, 1, "", 260, "teal")], 300, bg=DEALER, head="車の値段（目安）",
                        total_fmt="{v}万", highlight=0),
    "y2_gas": B.Chart(VS, [(0.4, 0, "18km/L", 7.6, "orange"), (1.4, 1, "30km/L", 4.5, "teal")], 9, bg=GAS,
                      head="1年のガソリン代（年8000km・170円/L）", total_fmt="年{v}万", highlight=1),
    "y3_km": B.Chart([("年8000km", "teal"), ("年1万km", "blue"), ("年2万km", "red")],
                     [(0.4, 0, "", 19, "teal"), (1.2, 1, "", 16, "blue"), (2.0, 2, "", 8, "red")], 21, bg=ROAD,
                     head="60万の差を取り戻すまで", total_fmt="{v}年", highlight=2),
    "y4_10y": B.Chart(VS, [(0.3, 0, "車の値段", 200, "orange"), (1.0, 0, "ガソリン10年", 76, "gold"),
                           (1.8, 1, "車の値段", 260, "teal"), (2.5, 1, "ガソリン10年", 45, "gold")], 340, bg=MONEY,
                      head="10年でかかるお金（年8000km）", total_fmt="{v}万", result_at=3.4, highlight=0),
    "y5_sell": B.Chart(VS, [(0.4, 0, "売ったお金を引くと", 256, "orange"), (1.4, 1, "売ったお金を引くと", 265, "teal")], 300,
                       bg=MONEY, head="10年後に売った分を引くと（目安）", total_fmt="{v}万", result_at=2.4),
    "y6_2man": B.Chart(VS, [(0.4, 0, "年2万km・10年", 389, "orange"), (1.4, 1, "年2万km・10年", 351, "teal")], 420, bg=ROAD,
                       head="たくさん走る人の10年（売ったお金を引く）", total_fmt="{v}万", result_at=2.4, highlight=1),
})


def cuts_all():
    return [
        C.notice(STREET, (("drive_driving_cat", 220, 600), ("dance_three_kittens", 640, 520), ("money_counting_orange_cat", 1000, 560),
                          ("drive_monkey_golf_cart", 1360, 560), ("dance_happy_banana_cat", 1720, 600))),
        # ---- つかみ ----
        nn("車を買うなら\nハイブリッドが\nお得でしょ？", DEALER, se="question_hatena_maou", bgm={"file": C.PURPLE, "gain": -4}),
        ss("ガソリン代は\nたしかに安い\nでも……", DEALER, se="pi"),
        C.slot(DEALER, "車の値段の差を取り戻すまで 約", 19, "年"),
        boom("19年!?\nその前に\n車を買いかえる!?", DEALER, se=[CONAN]),
        fx(nn("え……\nハイブリッドって\n得じゃないの？", MONEY, se=POON), "mono"),
        C.title(STREET, "drive_driving_cat", "money_counting_orange_cat"),
        C.card("e02_premise", "同じくらいの大きさのコンパクトカーでくらべる", dur=5.2),
        # ---- 車の値段 ----
        chap("① 車の値段", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("同じくらいの大きさでも\nハイブリッドは\n値段が高い", DEALER, se="pi"),
        g("y1_price", "その差\n約60万", dur=3.6),
        boom("最初から\n60万高い!?", DEALER, se=["explosion_chudoon"]),
        nn("でもガソリン代で\n取り戻せるん\nでしょ？", DEALER, se="question_hatena_maou"),
        ss("ハイブリッドは\nモーターとエンジンの\n2つを積んでいる", DEALER, se="kon"),
        ss("そのぶん部品が多くて\n値段が上がる", DEALER, se="pi"),
        # ---- ガソリン代 ----
        chap("② ガソリン代", se="whoosh_shu"),
        ss("実際の燃費は\nガソリン車 18km\nハイブリッド 30km", GAS, se="pi"),
        ss("年8000km走ると\nガソリン代は……", GAS, se="kon"),
        g("y2_gas", "1年の差は\n約3万円", dur=3.6),
        fx(boom("1年で\nたった3万!?", GAS, se=["explosion_chudoon", {"f": "glass_break_01", "gain": -4}]), "crack"),
        nn("60万を取り戻すには\n……20年？", GAS, se="deflate_hyororo"),
        ss("ガソリンが200円に\nなったら？", GAS, se="question_hatena_maou"),
        ss("それでも差は\n年3.6万くらい", GAS, se="kon"),
        boom("17年かかる!?", GAS, se=["explosion_dokaan"]),
        ss("ふつうは10年くらいで\n買いかえる人が多い", GAS, se="pi"),
        # ---- 走る距離しだい ----
        chap("③ 走る距離しだい", se="doon_heavy", bgm={"file": C.COCOA, "gain": -4, "fade": 0.6}),
        ss("たくさん走る人ほど\nハイブリッドが\n得になる", ROAD, se="pi"),
        g("y3_km", "年2万km走るなら\n8年で取り戻せる", dur=4.4),
        ss("通勤で毎日\n長い距離を走る人\n営業の人", ROAD, se="kon"),
        nn("近所の買い物だけ\nだと？", CITY, se="question_hatena_maou"),
        ss("ガソリン車のほうが\n安くすむことが\n多い", CITY, se="pikon"),
        ss("ただし街中の\nストップ＆ゴーは\nハイブリッドが得意", CITY, se="kon"),
        ss("止まったり走ったりで\nモーターが働いて\n燃費がよくなる", CITY, se="kon"),
        ss("逆に高速道路を\nずっと走ると\n差は小さくなる", ROAD, se="pi"),
        nn("乗り方で\nこんなに変わるの？", ROAD, se="question_hatena_maou"),
        # ---- 税金・下取り ----
        chap("④ 税金と売るとき", se="whoosh_shu"),
        ss("自動車税は\nどちらも\nエンジンの大きさで決まる", STREET, se="pi"),
        ss("ハイブリッドは\nエコカー減税で\n最初に数万円安くなることも", STREET, se="kon"),
        ss("車検の費用は\nどちらも\nあまり変わらない", STREET, se="pi"),
        ss("保険料も\n車の値段が高いぶん\n少し上がることも", STREET, se="kon"),
        ss("そして\n売るときは\nハイブリッドが高く売れやすい", DEALER, se="shine_kiraan_maou"),
        g("y4_10y", "10年でくらべると……", dur=4.6),
        g("y5_sell", "売ったお金を\n引くと……", dur=4.2),
        qq(MONEY, "anime_conan_hirameki_remix_b"),
        fx(boom("ほぼ\n同じ!?", MONEY, se=["explosion_chudoon"]), "money"),
        fx(nn("え……\n迷ったぶん\n損した気分", MONEY, se="tv_professional_poon_remix_a"), "swirl"),
        g("y6_2man", "たくさん走る人は\nハイブリッドの勝ち", dur=4.2),
        boom("10年で\n38万お得!?", ROAD, se=["explosion_dokaan"]),
        # ---- お金以外 ----
        chap("⑤ お金以外のちがい", se="quiz_question_01", bgm={"file": C.MIRAI, "gain": -4, "fade": 0.6}),
        ss("ハイブリッドは\n静かで\nなめらかに走る", CITY, se="kon"),
        ss("給油の回数が少ない\nのもうれしい", GAS, se="pikon"),
        ss("ガソリン車は\nしくみがシンプルで\n修理が安いことも", STREET, se="kon"),
        nn("電池の交換が\n心配……", STREET, se="question_hatena_maou"),
        ss("最近は長持ちで\n保証も長いことが\n多い", STREET, se="pi"),
        ss("中古車なら\nハイブリッドとの値段の差は\nもっと小さいことも", DEALER, se="pikon"),
        boom("中古ハイブリッドが\nいちばんお得!?", DEALER, se=["explosion_dokaan"]),
        ss("ただし電池の\n残りの元気は\nしっかり確認", DEALER, se="pc_warning"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        C.card("e07_points", "1年に走る距離で えらぼう", dur=5.6),
        nn("あまり走らないなら\nガソリン車で\nいいんだね", STREET, se="kon"),
        ss("たくさん走るなら\nハイブリッド\n距離で決めよう", STREET, se="kon"),
    ] + C.ending(STREET)


if __name__ == "__main__":
    C.main("38_hybrid", cuts_all, ["y1_price", "y2_gas", "y3_km", "y4_10y", "y5_sell", "y6_2man"])
