"""37_hitori（ひとり暮らしvs実家暮らし 1年でかかるお金）（11/1 ユーザー指定・車ありvs車なしと同じ作り）。3分ほど。

python3 catmeme/cuts_37_hitori.py [--charts|--len]
数字はざっくりの目安（2026年・20代の会社員・都市部）。実家暮らしも「家に入れるお金」などはかかる、としてくらべる：
  ひとり暮らし：家賃 月7.5万＝90万／光熱費12万／食費45万／日用品6万／家具家電（30万を5年で）6万／通信6万／遊び・交際30万 → 年 約195万
  実家：家に入れるお金 月4万＝48万／自分の食費（外食・ランチ）12万／日用品2万／通信6万／遊び・交際30万 → 年 約98万
  → 1年で約97万の差。5年で約485万
  ひとり暮らしの最初：敷金・礼金・仲介手数料・引っ越し・家具家電で 約60万
  実家の見えないコスト：通勤時間（往復で1日1時間多い→年 約240時間）／自由・家事の力／親の手伝い
原稿のルール：実家暮らしをバカにしない。今日の一言・単語の途中で改行しない・最後はチャンネル登録・過去の動画にはふれない
"""
import compare_long as C
import wide_bars as B

ROOM, HOME, KITCHEN, STATION, MOVE, NIGHT = ("bg02_room", "bg37_family_home", "st02_home_kitchen", "bg54_station_crowd_map",
                                            "bg37_moving_boxes", "bg14_home_night")
C.setup("37_hitori", {HOME: "bg19_kids_room", MOVE: "bg02_room"})
bg, nn, ss, boom, qq, g, fx, chap = C.bg, C.nn, C.ss, C.boom, C.qq, C.g, C.fx, C.chap
CONAN, POON, MONEY = C.CONAN, C.POON, C.MONEY

VS = [("ひとり暮らし", "red"), ("実家暮らし", "teal")]
HEAD = "1年でかかるお金（20代会社員・目安）"
HT = [("家賃", 90, "red"), ("光熱費", 12, "gold"), ("食費", 45, "orange"), ("日用品", 6, "pink"), ("家具家電", 6, "purple"),
      ("通信", 6, "navy"), ("遊び・交際", 30, "coral")]
JK = [("家に入れるお金", 48, "teal"), ("食費（外食）", 12, "orange"), ("日用品", 2, "pink"), ("通信", 6, "navy"),
      ("遊び・交際", 30, "coral")]


def steps(ht, jk, have_ht=(), have_jk=(), t0=0.5, gap=0.8):
    st = [(-1, 0, n, v, c) for n, v, c in HT if n in have_ht] + [(-1, 1, n, v, c) for n, v, c in JK if n in have_jk]
    k = 0
    for side, rows, names in ((0, HT, ht), (1, JK, jk)):
        for n, v, c in rows:
            if n in names:
                st.append((t0 + gap * k, side, n, v, c))
                k += 1
    return st


C.charts({
    "h0_preview": B.Chart(VS, [(0.3 + 0.25 * k, 0, n, v, c) for k, (n, v, c) in enumerate(HT)]
                          + [(2.4 + 0.3 * k, 1, n, v, c) for k, (n, v, c) in enumerate(JK)], 210, bg=ROOM, head=HEAD, highlight=1),
    "h1_rent": B.Chart(VS, steps(["家賃"], ["家に入れるお金"]), 210, bg=ROOM, head=HEAD),
    "h2_food": B.Chart(VS, steps(["光熱費", "食費"], ["食費（外食）"], have_ht=["家賃"], have_jk=["家に入れるお金"]), 210,
                       bg=KITCHEN, head=HEAD),
    "h3_all": B.Chart(VS, steps(["日用品", "家具家電", "通信", "遊び・交際"], ["日用品", "通信", "遊び・交際"],
                                have_ht=["家賃", "光熱費", "食費"], have_jk=["家に入れるお金", "食費（外食）"]), 210, bg=MONEY,
                      head=HEAD, result_at=6.0, highlight=1),
    "h4_5y": B.Chart(VS, [(0.4, 0, "最初の60万＋5年分", 1035, "red"), (1.5, 1, "5年分", 490, "teal")], 1150, bg=MONEY,
                     head="5年でかかるお金（目安）", total_fmt="{v}万", result_at=2.6, highlight=1),
    "h5_time": B.Chart(VS, [(0.4, 0, "会社の近く", 120, "red"), (1.4, 1, "1日1時間多い", 360, "teal")], 400, bg=STATION,
                       head="1年の通勤時間（目安）", total_fmt="{v}時間", highlight=0),
})


def cuts_all():
    return [
        C.notice(ROOM, (("sleep_sleeping_cat", 220, 560), ("eat_pop_cat", 640, 520), ("happy_hamster_open_arms", 1000, 560),
                        ("money_counting_orange_cat", 1360, 560), ("dance_happy_banana_cat", 1720, 600))),
        # ---- つかみ ----
        nn("実家暮らしって\nお金かからないん\nでしょ？", HOME, se="question_hatena_maou", bgm={"file": C.PURPLE, "gain": -4}),
        ss("家にお金を入れたり\n外で食べたり\nけっこうかかるよ", HOME, se="pi"),
        C.slot(ROOM, "それでも差は 年 約", 97, "万円"),
        boom("年97万!?", ROOM, se=[CONAN]),
        g("h0_preview", "ぜんぶ積み上げると\nこうなる", dur=5.4),
        fx(nn("え……\n実家ってそんなに\n強いの？", MONEY, se=POON), "mono"),
        C.title(HOME, "sleep_sleeping_cat", "happy_hamster_open_arms"),
        C.card("e02_premise", "20代・都市部の会社員の場合", dur=5.2),
        # ---- 住むお金 ----
        chap("① 住むお金", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("ひとり暮らしの家賃は\n月7.5万くらい", ROOM, se="pi"),
        ss("家賃の目安は\n手取りの3分の1まで", ROOM, se="kon"),
        nn("手取り20万なら\n6.6万……", ROOM, se="deflate_hyororo"),
        ss("実家暮らしは\n家にお金を入れる人が多い\n月3万〜5万", HOME, se="kon"),
        g("h1_rent", "ここで\n42万の差", dur=3.8),
        nn("家に入れるお金も\nけっこう大きいね", HOME, se="pikon"),
        ss("でも親は\nそのお金を\nこっそり貯めてくれていることも", HOME, se="sparkle_kirakira_01"),
        # ---- 食費・光熱費 ----
        chap("② 食費と光熱費", se="whoosh_shu"),
        ss("ひとり暮らしは\n電気・ガス・水道を\nぜんぶ自分ではらう", ROOM, se="pi"),
        ss("食費は自炊しても\n月3.5万くらい\nコンビニが多いともっと", KITCHEN, se="kon"),
        nn("実家は\nごはんが出てくる……", KITCHEN, se="pikon"),
        ss("ひとり分の料理は\n食材が余りがち", KITCHEN, se="kon"),
        nn("キャベツ1玉\n使いきれない……", KITCHEN, se="deflate_hyororo"),
        ss("会社のランチや\n友だちとの外食は\n自分ではらう", KITCHEN, se="pi"),
        g("h2_food", "食費と光熱費でも\nこの差", dur=4.4),
        boom("お母さんの\nごはんの価値!?", KITCHEN, se=["explosion_dokaan"]),
        # ---- 日用品・家具 ----
        chap("③ 見えないお金", se="doon_heavy", bgm={"file": C.COCOA, "gain": -4, "fade": 0.6}),
        ss("トイレットペーパー\n洗剤・シャンプー\nぜんぶ自分で買う", ROOM, se="pi"),
        nn("ティッシュって\nこんなに\nすぐなくなるの!?", ROOM, red=True, se=["explosion_dokaan"]),
        ss("冷蔵庫・洗濯機\nベッドも\nそろえる", MOVE, se="kon"),
        ss("最初の引っ越しで\n敷金・礼金・家具家電\n約60万", MOVE, se="pc_warning"),
        ss("NHKの受信料や\nインターネットの工事も\n自分で手続き", ROOM, se="pi"),
        ss("更新料も\n2年ごとに\n家賃1か月分", ROOM, se="kon"),
        fx(boom("住む前に\n60万!?", MOVE, se=["explosion_chudoon", {"f": "glass_break_01", "gain": -4}]), "crack"),
        g("h3_all", "ぜんぶ積むと……", dur=6.6),
        fx(boom("ひとり暮らし195万\n実家98万!!", MONEY, se=["explosion_dokaan"]), "money"),
        g("h4_5y", "5年で\nくらべると……", dur=4.6),
        qq(MONEY, "anime_conan_hirameki_remix_b"),
        fx(boom("5年で\n500万以上の差!?", MONEY, se=["explosion_chudoon"]), "money"),
        # ---- 実家のコスト ----
        chap("④ 実家にもコストはある", se="quiz_question_01", bgm={"file": C.MIRAI, "gain": -4, "fade": 0.6}),
        ss("実家が\n会社から遠いと\n通勤時間が長い", STATION, se="pi"),
        g("h5_time", "1日1時間多いと\n年240時間", dur=3.8),
        boom("10日分も\n電車に\n乗ってる!?", STATION, se=["explosion_dokaan"]),
        ss("門限や\n家族の目もある", HOME, se="kon"),
        fx(nn("え……\n夜中にラーメン\n食べにいけない？", HOME, se="tv_professional_poon_remix_a"), "swirl"),
        ss("家事の力が\nなかなか身につかない\nことも", HOME, se="kon"),
        ss("親が年をとると\n家のことを手伝う\n時間もふえる", HOME, se="kon"),
        ss("それは\nお金にかえられない\n大事な時間でもある", HOME, se="sparkle_kirakira_01"),
        # ---- ひとり暮らしのよさ ----
        chap("⑤ ひとり暮らしのよさ", se="whoosh_shu"),
        ss("会社の近くに住めば\n朝ゆっくり寝られる", ROOM, se="pikon"),
        ss("料理・洗濯・お金の管理\n全部自分でできるようになる", ROOM, se="kon"),
        ss("友だちを\n気軽に呼べる", NIGHT, se="pikon"),
        ss("会社の近くなら\n通勤時間を\n自分の時間にできる", ROOM, se="kon"),
        nn("時間を\nお金で買うって\nこういうことか", ROOM, se="pikon"),
        nn("自由は\nお金で買う\nものなのか", NIGHT, se="kon"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        C.card("e07_points", "実家にいるあいだに しっかり貯めよう", dur=5.6),
        nn("実家にいる間は\n貯めるチャンス\nなんだね", HOME, se="kon"),
        ss("家に入れるお金は\nちゃんとはらって\n感謝も忘れずに", HOME, se="kon"),
        ss("ひとり暮らしは\n自由と経験を\nお金で買っている", ROOM, se="kon"),
    ] + C.ending(HOME)


if __name__ == "__main__":
    C.main("37_hitori", cuts_all, ["h0_preview", "h1_rent", "h2_food", "h3_all", "h4_5y", "h5_time"])
