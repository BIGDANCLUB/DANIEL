"""40_mansion（新築マンションvs中古マンション＋リノベ 30年でいくら違う？）（11/3 ユーザー指定・タワマンと同じ作り）。3分ほど。

python3 catmeme/cuts_40_mansion.py [--charts|--len]
数字はざっくりの目安（2026年・首都圏・同じエリアの70平米・35年ローン金利0.8%・30年住んで売る）：
  買う値段：新築 6500万／中古（築20年）4000万＋リノベ800万＝4800万（差 1700万）
  買うときの諸費用：新築 約250万／中古 約350万（仲介手数料がかかる）
  ローンの利息（30年ぶん）：新築 約900万／中古 約650万
  修繕積立金（30年）：新築 約790万（最初は安くて段階的に上がる）／中古 約900万（すでに高い）
  固定資産税（30年）：新築 約540万（最初の5年は軽減）／中古 約390万
  30年後に売ると：新築（築30年）約3500万／中古（築50年）約1800万
  → 実際にかかるお金：新築 約5480万／中古 約5290万（差 約190万・中古が少し安い）
  管理費はどちらも同じくらいなので入れない
原稿のルール：実在のマンション・会社の名前は出さない。今日の一言はエンディング画面・単語の途中で改行しない・過去の動画にはふれない
"""
import compare_long as C
import wide_bars as B

TOWER, LOBBY, ROOM, OFFICE, STREET, NIGHT = ("bg35_tower", "bg35_tower_lobby", "bg02_room", "bg78_agency_office",
                                             "bg35_suburb_street", "bg14_home_night")
C.setup("40_mansion", {})
bg, nn, ss, boom, qq, g, fx, chap = C.bg, C.nn, C.ss, C.boom, C.qq, C.g, C.fx, C.chap
CONAN, POON, MONEY = C.CONAN, C.POON, C.MONEY

VS = [("新築", "red"), ("中古＋リノベ", "teal")]
HEAD = "30年でかかるお金（目安）"
NW = [("買う値段", 6500, "red"), ("諸費用", 250, "orange"), ("ローン利息", 900, "gold"), ("修繕積立金", 790, "purple"),
      ("固定資産税", 540, "navy")]
CH = [("買う値段＋リノベ", 4800, "teal"), ("諸費用", 350, "orange"), ("ローン利息", 650, "gold"), ("修繕積立金", 900, "purple"),
      ("固定資産税", 390, "navy")]


def steps(nw, ch, have_nw=(), have_ch=(), t0=0.5, gap=0.9):
    st = [(-1, 0, n, v, c) for n, v, c in NW if n in have_nw] + [(-1, 1, n, v, c) for n, v, c in CH if n in have_ch]
    k = 0
    for side, rows, names in ((0, NW, nw), (1, CH, ch)):
        for n, v, c in rows:
            if n in names:
                st.append((t0 + gap * k, side, n, v, c))
                k += 1
    return st


C.charts({
    "m1_price": B.Chart(VS, steps(["買う値段"], ["買う値段＋リノベ"]), 9500, bg=TOWER, head=HEAD, highlight=1),
    "m2_loan": B.Chart(VS, steps(["諸費用", "ローン利息"], ["諸費用", "ローン利息"], have_nw=["買う値段"], have_ch=["買う値段＋リノベ"]),
                       9500, bg=OFFICE, head=HEAD),
    "m3_keep": B.Chart(VS, steps(["修繕積立金", "固定資産税"], ["修繕積立金", "固定資産税"],
                                 have_nw=["買う値段", "諸費用", "ローン利息"], have_ch=["買う値段＋リノベ", "諸費用", "ローン利息"]),
                       9500, bg=LOBBY, head=HEAD, result_at=4.3, highlight=1),
    "m4_sell": B.Chart([("新築（築30年）", "red"), ("中古（築50年）", "teal")],
                       [(0.4, 0, "", 3500, "red"), (1.4, 1, "", 1800, "teal")], 4000, bg=STREET,
                       head="30年後に売ると（目安）", total_fmt="{v}万", highlight=0),
    "m5_total": B.Chart(VS, [(0.4, 0, "売った分を引くと", 5480, "red"), (1.5, 1, "売った分を引くと", 5290, "teal")], 6200, bg=MONEY,
                        head="30年で実際にかかったお金（目安）", total_fmt="{v}万", result_at=2.6, highlight=1),
})


def cuts_all():
    return [
        # ---- つかみ ----
        nn("中古マンションを\nリノベしたら\nめちゃくちゃ得でしょ？", ROOM, se="question_hatena_maou", bgm={"file": C.PURPLE, "gain": -4}),
        dict(ss("買う値段は\nたしかに\n1700万安い", ROOM, se="pi"), layers_top=[C.pt("e03_basis")]),   # 11/3：根拠を小さく
        C.slot(MONEY, "でも30年でくらべると 差は 約", 190, "万円", dur=3.6),
        boom("たった190万!?", MONEY, se=[CONAN]),
        fx(nn("え……\n1700万は\nどこへ消えたの？", MONEY, se=POON), "mono"),
        C.title(TOWER, "showoff_gojo_cosplay_cat", "money_counting_orange_cat"),
        C.card("e02_premise", "首都圏・同じエリアの70平米でくらべる", dur=5.2),
        # ---- 買う値段 ----
        chap("① 買う値段", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("首都圏の新築マンションは\n70平米で\n6500万くらい", TOWER, se="pi"),
        ss("同じエリアの\n築20年の中古なら\n4000万くらい", STREET, se="kon"),
        ss("中古はキッチンや\nお風呂をリノベして\n800万", ROOM, se="kon"),
        nn("新品みたいに\nなるなら\n中古で十分じゃん", ROOM, se="pikon"),
        g("m1_price", "ここで\n1700万の差", dur=3.8),
        boom("1700万も\n安い!?", MONEY, se=["explosion_chudoon"]),
        ss("間取りも\n自分の好きに\n変えられる", ROOM, se="pikon"),
        # ---- ローン ----
        chap("② 諸費用とローン", se="doon_heavy"),
        ss("買うときには\n登記や手数料などの\n諸費用がかかる", OFFICE, se="pi"),
        ss("中古は\n不動産屋さんへの\n仲介手数料がかかる", OFFICE, se="kon"),
        nn("中古のほうが\n諸費用は高いの？", OFFICE, se="question_hatena_maou"),
        ss("でも借りるお金が\n少ないぶん\nローンの利息は少ない", OFFICE, se="kon"),
        g("m2_loan", "借りる額が\n小さいほど\n利息も小さい", dur=4.4),
        ss("中古はリノベ代を\nいっしょにローンに\nできないこともある", OFFICE, se="pc_warning"),
        # ---- 住んでからのお金 ----
        chap("③ 住んでからのお金", se="whoosh_shu", bgm={"file": C.COCOA, "gain": -4, "fade": 0.6}),
        ss("マンションは\n毎月の修繕積立金が\nかかる", LOBBY, se="pi"),
        ss("新築は最初が安くて\n5年ごとに\nどんどん上がる", LOBBY, se="kon"),
        nn("最初が安いのは\nわなだったのか", LOBBY, se="deflate_hyororo"),
        ss("築20年の中古は\nもう高くなっている", LOBBY, se="kon"),
        ss("固定資産税は\n建物が新しいほど高い", OFFICE, se="kon"),
        ss("新築は最初の5年だけ\n税金が安くなる", OFFICE, se="pikon"),
        g("m3_keep", "ぜんぶ積むと……", dur=6.0),
        fx(boom("新築9000万\n中古7100万!!", MONEY, se=["explosion_dokaan"]), "money"),
        nn("まだ1900万も\n中古が安いじゃん", MONEY, se="pikon"),
        # ---- 売る値段 ----
        chap("④ 30年後に売ると", se="doon_heavy", bgm={"file": C.MIRAI, "gain": -4, "fade": 0.6}),
        ss("ここが\nいちばん大事", STREET, se="pi"),
        ss("30年後\n新築は築30年\n中古は築50年", STREET, se="kon"),
        ss("築50年の\nマンションは\n買う人が少ない", STREET, se="kon"),
        g("m4_sell", "売る値段が\nぜんぜん違う", dur=3.8),
        boom("1700万の差が\n売る時に\n戻ってくる!?", STREET, se=["explosion_chudoon"]),
        g("m5_total", "売った分を\n引くと……", dur=4.6),
        qq(MONEY, "anime_conan_hirameki_remix_b"),
        fx(boom("差は\nたった190万!!", MONEY, se=["explosion_chudoon"]), "money"),
        fx(nn("え……\nほとんど同じ!?", MONEY, se="tv_professional_poon_remix_a"), "swirl"),
        # ---- 気をつけること ----
        chap("⑤ 中古で気をつけること", se="quiz_question_01"),
        ss("古いマンションは\n耐震の基準を\n確認しよう", STREET, se="pi"),
        ss("1981年6月より前の\n建物は\n古い基準のことがある", STREET, se="pc_warning"),
        ss("建て替えの話が出ると\n大きなお金が\nかかることも", LOBBY, se="kon"),
        ss("修繕積立金が\nちゃんと貯まっているかも\n大事", LOBBY, se="kon"),
        nn("中古は\n建物の健康診断が\n大事なんだね", LOBBY, se="pikon"),
        # ---- 新築のよさ ----
        chap("⑥ 新築のよさ", se="whoosh_shu", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("最新の設備\n断熱がよくて\n光熱費が安い", TOWER, se="kon"),
        ss("住宅ローン控除も\n新築のほうが\n有利なことが多い", OFFICE, se="kon"),
        nn("新築の香りは\n最高……", TOWER, se="sparkle_kirakira_01"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy"),
        C.card("e07_points", "値段だけでなく 売る時と建物の年れいまで", dur=5.6),
        nn("安く買っても\n安く売ることに\nなるんだね", NIGHT, se="kon"),
        ss("30年で見ると\nほとんど同じ\n好きなほうを選ぼう", NIGHT, se="kon"),
        C.ending(TOWER)[0],
        C.end_today(TOWER, (("read_book_orange_kitten", 220, 560), ("dance_three_kittens", 640, 520), ("calm_black_face_sheep", 1000, 560),
                            ("money_counting_orange_cat", 1360, 560), ("dance_happy_banana_cat", 1720, 600))),
    ]


if __name__ == "__main__":
    C.main("40_mansion", cuts_all, ["m1_price", "m2_loan", "m3_keep", "m4_sell", "m5_total"])
