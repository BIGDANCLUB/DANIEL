"""36_chiho（東京vs地方移住 1年でいくら残る？ 家賃・車・給料までふくめて）（11/1 ユーザー指定・車ありvs車なしと同じ作り）。3分ほど。

python3 catmeme/cuts_36_chiho.py [--charts|--len]
数字はざっくりの目安（2026年・30代・ひとり暮らしの会社員・地方は県庁所在地くらいの町）：
  手取り：東京 年収500万→約390万／地方 年収420万→約335万
  1年の生活費：家賃 東京 月9万＝108万／地方 月5万＝60万
               車 東京 0（電車・定期は会社もち）／地方 軽自動車 年 約40万（ローン・税金・保険・ガソリン・車検）
               食費 東京48万／地方42万　光熱費 東京12万／地方15万（冬の暖房・プロパンガス）
               遊び・交際 東京30万／地方20万　通信 どちらも6万
               → 東京 約204万／地方 約183万
  残るお金：東京 約186万／地方 約152万 → 家賃は安いのに、東京のほうが年34万多く残る（給料の差が大きい）
  ただし：地方で東京と同じ給料なら（リモートワークなど）年 約207万残る。国の移住支援金（東京23区などから・条件あり）は最大100万円
原稿のルール：実在の人・会社・自治体名は出さない。どの地域もけなさない。今日の一言・単語の途中で改行しない・最後はチャンネル登録
"""
import compare_long as C
import wide_bars as B

TOKYO, LOCAL, ROOM, LROOM, ROAD, STATION, OFFICE = ("bg57_tokyo_skyline", "bg36_local_town", "bg02_room", "bg36_local_room",
                                                    "bg26_rural_road", "bg54_station_crowd_map", "bg25_office_desk")
C.setup("36_chiho", {LOCAL: "bg63_hokkaido_field", LROOM: "bg19_kids_room"}, tempo=1.1)
bg, nn, ss, boom, qq, g, fx, chap = C.bg, C.nn, C.ss, C.boom, C.qq, C.g, C.fx, C.chap
CONAN, POON, MONEY = C.CONAN, C.POON, C.MONEY

VS = [("東京", "red"), ("地方", "teal")]
HEAD = "1年の生活費（ひとり暮らし・目安）"
TK = [("家賃", 108, "red"), ("食費", 48, "orange"), ("光熱費", 12, "gold"), ("遊び・交際", 30, "pink"), ("通信", 6, "navy")]
LC = [("家賃", 60, "teal"), ("車", 40, "purple"), ("食費", 42, "orange"), ("光熱費", 15, "gold"), ("遊び・交際", 20, "pink"),
      ("通信", 6, "navy")]


def steps(tk, lc, have_tk=(), have_lc=(), t0=0.5, gap=0.9):
    st = [(-1, 0, n, v, c) for n, v, c in TK if n in have_tk] + [(-1, 1, n, v, c) for n, v, c in LC if n in have_lc]
    k = 0
    for side, rows, names in ((0, TK, tk), (1, LC, lc)):
        for n, v, c in rows:
            if n in names:
                st.append((t0 + gap * k, side, n, v, c))
                k += 1
    return st


C.charts({
    "c0_rent": B.Chart(VS, steps(["家賃"], ["家賃"]), 220, bg=TOKYO, head=HEAD, highlight=1),
    "c1_car": B.Chart(VS, steps([], ["車"], have_tk=["家賃"], have_lc=["家賃"]), 220, bg=ROAD, head=HEAD),
    "c2_life": B.Chart(VS, steps(["食費", "光熱費", "遊び・交際", "通信"], ["食費", "光熱費", "遊び・交際", "通信"],
                                 have_tk=["家賃"], have_lc=["家賃", "車"]), 220, bg=MONEY, head=HEAD, result_at=7.0, highlight=1),
    "c3_pay": B.Chart(VS, [(0.4, 0, "年収500万", 390, "red"), (1.4, 1, "年収420万", 335, "teal")], 420, bg=OFFICE,
                      head="1年の手取り（目安）", total_fmt="{v}万", highlight=0),
    "c4_left": B.Chart(VS, [(0.4, 0, "手取り−生活費", 186, "red"), (1.5, 1, "手取り−生活費", 152, "teal")], 260, bg=MONEY,
                       head="1年で残るお金（目安）", total_fmt="{v}万", result_at=2.5, highlight=0),
    "c5_remote": B.Chart([("東京で働く", "red"), ("地方で働く", "teal"), ("地方で東京の給料", "gold")],
                         [(0.4, 0, "", 186, "red"), (1.2, 1, "", 152, "teal"), (2.0, 2, "リモートなど", 207, "gold")], 260,
                         bg=LOCAL, head="1年で残るお金（目安）", total_fmt="{v}万", result_at=3.0, highlight=2),
})


def cuts_all():
    return [
        C.notice(LOCAL, (("ride_kitten_bike", 220, 560), ("dance_three_kittens", 640, 520), ("calm_black_face_sheep", 1000, 560),
                         ("walk_white_duck", 1360, 520), ("dance_happy_banana_cat", 1720, 600))),
        # ---- つかみ ----
        nn("地方に移住したら\n家賃が安くて\nお金が貯まるよね？", LOCAL, se="question_hatena_maou", bgm={"file": C.PURPLE, "gain": -4}),
        ss("家賃だけ見ると\nそうだけど……", LOCAL, se="pi"),
        C.slot(TOKYO, "残るお金 東京のほうが 年", 34, "万多い"),
        C.hatena(TOKYO),
        boom("東京のほうが\n貯まる!?", TOKYO, se=[CONAN]),
        fx(nn("え……\n家賃は高いのに？", MONEY, se=POON), "mono"),
        C.title(LOCAL, "ride_kitten_bike", "talk_orange_white_sitting_cat"),
        C.card("e02_premise", "30代・ひとり暮らしの会社員の場合", dur=5.2),
        # ---- 家賃 ----
        chap("① 家賃", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("東京のワンルームは\n月9万くらい", ROOM, se="pi"),
        ss("地方なら\n広い1LDKでも\n月5万くらい", LROOM, se="pikon"),
        g("c0_rent", "1年で\n48万の差", dur=3.8),
        nn("地方の圧勝\nじゃん！", LROOM, se="pikon"),
        ss("駐車場つきの\n家もふつう", LROOM, se="pikon"),
        # ---- 車 ----
        chap("② 車", se="doon_heavy"),
        ss("でも地方は\n車がないと\n生活しにくい", ROAD, se="pi"),
        ss("スーパーも病院も\n車で行く", ROAD, se="kon"),
        ss("軽自動車でも\nローン・税金・保険\nガソリンで年40万", ROAD, se="kon"),
        g("c1_car", "家賃の差が\nほとんど消える", dur=3.8),
        fx(boom("車で\n40万!?", ROAD, se=["explosion_chudoon", {"f": "glass_break_01", "gain": -4}]), "crack"),
        ss("東京は電車で\n定期代は\n会社が出すことが多い", STATION, se="pi"),
        ss("家族で住むなら\n車が2台いる\nことも", ROAD, se="pc_warning"),
        boom("2台で\n年80万!?", ROAD, se=["explosion_dokaan"]),
        # ---- 生活費 ----
        chap("③ 食費・光熱費・遊び", se="whoosh_shu", bgm={"file": C.COCOA, "gain": -4, "fade": 0.6}),
        ss("食費は\n地方が少し安い\n野菜や魚が安いことも", LOCAL, se="pi"),
        ss("でも光熱費は\n地方のほうが\n高いことがある", LROOM, se="kon"),
        nn("なんで？", LROOM, se="question_hatena_maou"),
        ss("冬の暖房\nそれにプロパンガスの\n地域も多い", LROOM, se="freeze_kochiin"),
        ss("遊びやお出かけは\n東京のほうが\nお金を使いがち", TOKYO, se="kon"),
        g("c2_life", "ぜんぶ積むと……", dur=7.4),
        fx(boom("東京204万\n地方183万", MONEY, se=["explosion_dokaan"]), "money"),
        nn("差は\nたった21万!?", MONEY, red=True, se=["anime_conan_hirameki_remix_a"]),
        # ---- 給料 ----
        chap("④ 給料", se="doon_heavy", bgm={"file": C.MIRAI, "gain": -4, "fade": 0.6}),
        ss("ここが\nいちばん大事", OFFICE, se="pi"),
        ss("同じ仕事でも\n地方は給料が\n低めのことが多い", OFFICE, se="kon"),
        ss("求人の数も\n東京のほうが多い", OFFICE, se="kon"),
        nn("転職しやすさも\nちがうのか", OFFICE, se="question_hatena_maou"),
        g("c3_pay", "手取りで\n55万の差", dur=3.6),
        boom("給料の差のほうが\n大きい!?", OFFICE, se=["explosion_dokaan"]),
        g("c4_left", "1年で\n残るお金は……", dur=4.4),
        qq(MONEY, "anime_conan_hirameki_remix_b"),
        fx(boom("東京のほうが\n年34万\n多く残る!!", TOKYO, se=["explosion_chudoon"]), "money"),
        fx(nn("え……\n移住したら\n貯まると思ってた", MONEY, se="tv_professional_poon_remix_a"), "swirl"),
        # ---- 逆転する人 ----
        chap("⑤ 地方が勝つ人", se="quiz_question_01"),
        ss("でも地方で\n東京と同じ給料を\nもらえたら？", LOCAL, se="pi"),
        nn("そんなことある？", LOCAL, se="question_hatena_maou"),
        ss("リモートワーク\n東京の会社に\n勤めたまま移住", LOCAL, se="pikon"),
        g("c5_remote", "これなら\n地方が圧勝", dur=4.8),
        boom("年207万\n残る!?", LOCAL, se=["explosion_dokaan"]),
        ss("国の移住支援金も\n条件しだいで\n最大100万円", LOCAL, se="shine_kiraan_maou"),
        ss("家族がいると\n子どもの分の\n加算もある", LOCAL, se="kon"),
        # ---- お金以外 ----
        chap("⑥ お金以外のちがい", se="whoosh_shu", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("地方は\n広い家・静か\n自然がいっぱい", LOCAL, se="kon"),
        ss("東京は\n仕事もお店も多い\n終電まで遊べる", TOKYO, se="kon"),
        nn("雪かきは\nいい運動……", LOCAL, se="deflate_hyororo"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy"),
        C.card("e07_points", "家賃だけでなく 給料と車まで見よう", dur=5.6),
        nn("移住は\n給料しだい\nなんだね", LOCAL, se="kon"),
        ss("東京の給料のまま\n移住できたら\n最強", LOCAL, se="kon"),
    ] + C.ending(LOCAL)


if __name__ == "__main__":
    C.main("36_chiho", cuts_all, ["c0_rent", "c1_car", "c2_life", "c3_pay", "c4_left", "c5_remote"])
