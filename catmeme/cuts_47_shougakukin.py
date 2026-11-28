"""47_shougakukin（奨学金を借りた人と借りなかった人）（11/10 ユーザー指定・長尺候補15番・EV回と同じ作り）。2分ほど。

python3 catmeme/cuts_47_shougakukin.py [--charts|--len]
数字は調査の平均（中央労福協のアンケート）：
  借りた総額の平均 約310万（2022年の調査）・毎月の返済 約1万5000円（同）・返す期間の平均 約15年（2018年の調査 14.7年）
  返済中の人の約7割が、これからの返済に不安（2024年の調査）
  22歳から返しはじめると 約37歳まで。借りなかった人が同じ月1万5000円を15年貯金すると 約270万
  返さなくていい「給付型」もある（世帯の収入などの条件あり）
原稿のルール：借りた人・借りなかった人・親をけなさない。奨学金は進学を助ける制度だと言う。利息の数字は出さない（人と時期で変わる）
"""
import compare_long as C
import wide_bars as B

CAMPUS, CLASS, OFFICE, NIGHT, CHAPEL, KIDS = ("bg01_campus", "bg30_classroom_desk", "bg25_office_desk", "bg14_home_night",
                                             "bg71_wedding_chapel", "bg19_kids_room")
C.setup("47_shougakukin", {})
bg, nn, ss, boom, qq, g, fx, chap = C.bg, C.nn, C.ss, C.boom, C.qq, C.g, C.fx, C.chap
CONAN, POON, MONEY = C.CONAN, C.POON, C.MONEY

C.charts({
    "g1_total": B.Chart([("借りたお金（平均）", "red")], [(0.4, 0, "4年間", 310, "red")], 350, bg=CAMPUS,
                        head="奨学金を借りた総額（調査の平均）", total_fmt="約{v}万", highlight=0),
    "g2_age": B.Chart([("返す期間", "orange")], [(0.4, 0, "", 15, "orange")], 18, bg=OFFICE,
                      head="返し終わるまで（調査の平均）", total_fmt="約{v}年", highlight=0),
    "g3_save": B.Chart([("借りた人：返済", "red"), ("借りなかった人：貯金", "teal")],
                       [(0.4, 0, "15年", 270, "red"), (1.4, 1, "15年", 270, "teal")], 300, bg=MONEY,
                       head="月1万5000円を15年（37歳まで）", total_fmt="約{v}万", result_at=2.4),
})


def cuts_all():
    return [
        # ---- つかみ ----
        nn("奨学金を\n借りた人と\n借りなかった人", CAMPUS, se="question_hatena_maou", bgm={"file": C.PURPLE, "gain": -4}),
        ss("大学を出たあと\n何が違う？", OFFICE, se="pi"),
        C.slot(MONEY, "借りた人の\n平均は\n約", 310, "万円", dur=3.6),
        boom("310万!?", MONEY, se=[CONAN]),
        fx(nn("社会人の\nスタートが\nマイナスから!?", MONEY, se=POON), "swirl"),
        C.title(CAMPUS, "read_book_orange_kitten", "money_counting_orange_cat"),
        C.card("e02_premise", "アンケートの平均で 借りた人と借りなかった人をくらべる", dur=5.2),
        # ---- 借りた額 ----
        chap("① いくら借りている？", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("奨学金は\n大学に行くための\nお金を借りる制度", CAMPUS, se="pi"),
        ss("毎月\n決まった額を\n4年間借りる", CLASS, se="kon"),
        g("g1_total", "借りた総額は\n平均で……", dur=3.8),
        boom("約310万!!", CAMPUS, se=["explosion_chudoon"]),
        nn("学費と\nひとり暮らしの\n生活費に使う人も", CLASS, se="kon"),
        # ---- 返済 ----
        chap("② 何年で返す？", se="doon_heavy"),
        ss("卒業して\n半年後くらいから\n返しはじめる", OFFICE, se="pi"),
        ss("毎月の返済は\n平均で\n約1万5000円", OFFICE, se="kon"),
        g("g2_age", "返し終わるまで\n平均で……", dur=3.8),
        boom("約15年!!", OFFICE, se=["explosion_dokaan"]),
        nn("22歳から返すと\n37歳まで\n続くのか", NIGHT, se="question_hatena_maou"),
        # ---- 人生の時期 ----
        chap("③ 人生のイベントと重なる", se="whoosh_shu", bgm={"file": C.COCOA, "gain": -4, "fade": 0.6}),
        ss("返している間に\n結婚する人も", CHAPEL, se="pi"),
        ss("子どもが生まれる人も", KIDS, se="kon"),
        ss("家を買う人も", NIGHT, se="kon"),
        ss("返済中の人の\n約7割が\nこれからの返済に\n不安を感じている", OFFICE, se="pc_warning"),
        nn("毎月の1万5000円が\nずっと続くのは\n重い", NIGHT, se="kon"),
        # ---- くらべる ----
        chap("④ 借りなかった人とくらべると", se="doon_heavy", bgm={"file": C.MIRAI, "gain": -4, "fade": 0.6}),
        ss("借りなかった人が\n同じ1万5000円を\n15年貯金すると", MONEY, se="pi"),
        g("g3_save", "15年で\nその差は……", dur=4.6),
        qq(MONEY, "anime_conan_hirameki_remix_b"),
        fx(boom("約270万!!", MONEY, se=["explosion_chudoon"]), "money"),
        fx(nn("37歳の時点で\n270万円の\n差がつく!?", MONEY, se="tv_professional_poon_remix_a"), "swirl"),
        ss("でも\n奨学金がなければ\n大学に行けなかった人もいる", CAMPUS, se="kon"),
        nn("大学で\n得たものは\nお金だけじゃない", CAMPUS, se="shine_kiraan_maou"),
        # ---- 知っておきたいこと ----
        chap("⑤ 知っておきたいこと", se="quiz_question_01"),
        ss("返さなくていい\n給付型の奨学金も\nある", CLASS, se="pi"),
        ss("世帯の収入などの\n条件がある", CLASS, se="kon"),
        ss("返すのが苦しいときは\n返済を待ってもらう\nしくみもある", OFFICE, se="kon"),
        nn("借りる前に\n親子で\n話しておきたい", KIDS, se="pikon"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        C.card("e07_points", "平均約310万を約15年で返す", dur=5.6),
        nn("奨学金は\n未来の自分からの\n借金", NIGHT, se="kon"),
        ss("給付型や\n返済を待つしくみも\n調べておこう", NIGHT, se="pc_warning"),
        C.ending(CAMPUS)[0],
        C.end_today(CAMPUS, (("read_book_orange_kitten", 220, 560), ("money_counting_orange_cat", 640, 560), ("work_typing_cat", 1000, 560),
                             ("sleep_sleeping_cat", 1360, 560), ("dance_cute_dog", 1720, 600))),
    ]


if __name__ == "__main__":
    C.main("47_shougakukin", cuts_all, ["g1_total", "g2_age", "g3_save"])
