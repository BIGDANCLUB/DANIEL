"""44_tabako（たばこを吸う人と吸わない人の生涯コスト）（11/6 ユーザー指定・自堕落ではない長尺の候補8番・EV回と同じ作り）。2〜3分。

python3 catmeme/cuts_44_tabako.py [--charts|--len]
数字は目安：
  1箱 580円（紙巻きの人気銘柄・2021年10月の値上げから）。1日1箱 → 1年 約21万（580×365＝21万1700円）
  → 10年 約212万／30年 約635万／半箱なら30年 約318万
  たばこ税は2027年から段階的に上がる予定（紙巻き・加熱式とも値上がりの見込み）→ 数字は今の値段のまま
  ほか：生命保険は「吸わない人のほうが安い」プランがある／賃貸の壁紙のヤニ汚れは退去のとき費用になることも（数字は出さない）
原稿のルール：吸う人をけなさない（どちらを選ぶかは自由）。健康の話は数字を出さない。「たばこ休憩」の話はしない（ほのぼの猫ミームと被る）
"""
import compare_long as C
import wide_bars as B

KONBINI, OFFICE, STREET, NIGHT, ROOM, IZAKAYA = ("bg15_convenience", "bg25_office_desk", "bg51_night_street", "bg14_home_night",
                                                 "bg02_room", "bg98_izakaya_night")
C.setup("44_tabako", {})
bg, nn, ss, boom, qq, g, fx, chap = C.bg, C.nn, C.ss, C.boom, C.qq, C.g, C.fx, C.chap
CONAN, POON, MONEY = C.CONAN, C.POON, C.MONEY
VS = [("1日1箱", "red"), ("吸わない", "teal")]

C.charts({
    "t1_year": B.Chart([("1日1箱", "red")], [(0.4, 0, "1年", 21, "red")], 25, bg=KONBINI,
                       head="たばこ代（1箱580円・1日1箱）", total_fmt="年{v}万", highlight=0),
    "t2_years": B.Chart([("10年", "orange"), ("20年", "red"), ("30年", "purple")],
                        [(0.4, 0, "", 212, "orange"), (1.2, 1, "", 424, "red"), (2.0, 2, "", 635, "purple")], 700, bg=MONEY,
                        head="たばこ代を積み上げると（1日1箱）", total_fmt="{v}万", result_at=3.0, highlight=2),
    "t3_half": B.Chart([("1日1箱", "red"), ("1日半箱", "orange"), ("吸わない", "teal")],
                       [(0.4, 0, "30年", 635, "red"), (1.2, 1, "30年", 318, "orange"), (2.0, 2, "30年", 0, "teal")], 700, bg=MONEY,
                       head="30年でかかるたばこ代", total_fmt="{v}万", result_at=3.0),
})


def cuts_all():
    return [
        # ---- つかみ ----
        nn("たばこを吸う人と\n吸わない人\n一生でいくら違う？", KONBINI, se="question_hatena_maou", bgm={"file": C.PURPLE, "gain": -4}),
        ss("1箱580円\n1日1箱だと", KONBINI, se="pi"),
        C.slot(MONEY, "30年で\nたばこ代だけで\n約", 635, "万円", dur=3.6),
        boom("635万!?", MONEY, se=[CONAN]),
        fx(nn("1日580円が\nそんなに!?", MONEY, se=POON), "swirl"),
        C.title(STREET, "think_chin_paw_orange_cat", "money_counting_orange_cat"),
        C.card("e02_premise", "今の値段のままで計算する", dur=5.2),
        # ---- 1日 ----
        chap("① 1日580円", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("紙巻きたばこの\n人気の銘柄は\n1箱580円ほど", KONBINI, se="pi"),
        ss("1日1箱なら\n1か月で\n約1万7000円", KONBINI, se="kon"),
        g("t1_year", "1年で\n約21万", dur=3.8),
        nn("スマホ代より\n高いかも", KONBINI, se="pikon"),
        ss("昔は1箱\n300円くらいの\n時代もあった", NIGHT, se="kon"),
        ss("税金が上がるたびに\n少しずつ\n値上がりしてきた", NIGHT, se="kon"),
        # ---- 積み上げ ----
        chap("② 積み上げると", se="doon_heavy"),
        ss("20歳から50歳まで\n30年吸うと", MONEY, se="pi"),
        g("t2_years", "10年 20年 30年……", dur=5.2),
        qq(MONEY, "anime_conan_hirameki_remix_b"),
        fx(boom("30年で\n約635万!!", MONEY, se=["explosion_dokaan"]), "money"),
        ss("新車が2台\n海外旅行なら\n20回くらい", MONEY, se="kon"),
        fx(nn("煙と一緒に\n車が2台\n消えていた!?", MONEY, se="tv_professional_poon_remix_a"), "swirl"),
        # ---- 本数 ----
        chap("③ 本数で変わる", se="whoosh_shu", bgm={"file": C.COCOA, "gain": -4, "fade": 0.6}),
        ss("1日半箱なら\nちょうど半分", IZAKAYA, se="pi"),
        g("t3_half", "1日1箱と\n半箱と\n吸わない人", dur=5.0),
        boom("半箱でも\n約318万!!", IZAKAYA, se=["explosion_chudoon"]),
        ss("飲み会の日だけ\n本数が増える人も\n多い", IZAKAYA, se="kon"),
        # ---- たばこ代以外 ----
        chap("④ たばこ代以外のお金", se="doon_heavy", bgm={"file": C.MIRAI, "gain": -4, "fade": 0.6}),
        ss("生命保険は\n吸わない人のほうが\n安いプランがある", OFFICE, se="pi"),
        ss("賃貸の部屋は\n壁紙のヤニ汚れで\n退去のときに\nお金がかかることも", ROOM, se="pc_warning"),
        ss("服や車の\nにおい消しや\nクリーニング", ROOM, se="kon"),
        nn("たばこ代だけじゃ\nなかったのか", ROOM, se="question_hatena_maou"),
        # ---- これから ----
        chap("⑤ これからの値段", se="quiz_question_01"),
        ss("たばこの税金は\n2027年から\n段階的に上がる予定", KONBINI, se="pi"),
        ss("紙巻きも加熱式も\nこれから\n値上がりしそう", KONBINI, se="kon"),
        nn("今の計算より\nもっと\n高くなるかも", KONBINI, se="question_hatena_maou"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        C.card("e07_points", "1日580円は 30年で約635万", dur=5.6),
        ss("吸うか吸わないかは\n自由", NIGHT, se="kon"),
        nn("でも\n一生分の値段は\n知っておきたい", NIGHT, se="pikon"),
        ss("やめた人は\nその分を\n毎月貯金に回すのもあり", NIGHT, se="shine_kiraan_maou"),
        C.ending(STREET)[0],
        C.end_today(STREET, (("think_chin_paw_orange_cat", 220, 560), ("dance_three_kittens", 640, 520), ("money_counting_orange_cat", 1000, 560),
                             ("calm_black_face_sheep", 1360, 560), ("dance_happy_banana_cat", 1720, 600))),
    ]


if __name__ == "__main__":
    C.main("44_tabako", cuts_all, ["t1_year", "t2_years", "t3_half"])
