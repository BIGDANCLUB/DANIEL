"""41_gakuhi（中学から私立vs大学まで国公立 学費はいくら違う？）（11/3 ユーザー指定・くらべる長尺と同じ作り）。3分ほど。

python3 catmeme/cuts_41_gakuhi.py [--charts|--len]
数字はざっくりの目安（2026年・子ども1人・家から通う・文部科学省「子供の学習費調査」などをもとに）：
  1年でかかるお金（塾・習い事などの学校外の費用もふくむ）：公立中 約54万／私立中 約156万／公立高 約60万／私立高 約103万
  中学受験の塾（小4〜小6の3年）：約250万
  大学4年：国立 約243万（入学金28.2万＋授業料53.6万×4）／私立文系 約400万
  私立高校の授業料支援（2026年度から拡充・年45.7万まで）：3年で約137万 → 私立高は 約309万−137万＝約172万
  → 中学から私立：250＋468＋172＋400＝約1290万／大学まで国公立：162＋180＋243＝約585万（差 約705万）
  大学受験の塾・予備校はどちらも同じくらいとして入れない
原稿のルール：実在の学校名は出さない。どちらの道もけなさない。今日の一言はエンディング画面・単語の途中で改行しない
"""
import compare_long as C
import wide_bars as B

STUDY, KIDS, GATE, CLASS, CAMPUS, NIGHT = ("bg08_study", "bg19_kids_room", "bg21_school_gate", "bg30_classroom_desk",
                                           "bg01_campus", "bg14_home_night")
C.setup("41_gakuhi", {})
bg, nn, ss, boom, qq, g, fx, chap = C.bg, C.nn, C.ss, C.boom, C.qq, C.g, C.fx, C.chap
CONAN, POON, MONEY = C.CONAN, C.POON, C.MONEY

VS = [("中学から私立", "red"), ("大学まで国公立", "teal")]
HEAD = "中学から大学までの学費（1人・目安）"
PV = [("中学受験の塾", 250, "orange"), ("私立中 3年", 468, "red"), ("私立高 3年", 172, "pink"), ("私立大 4年", 400, "purple")]
PB = [("公立中 3年", 162, "teal"), ("公立高 3年", 180, "navy"), ("国立大 4年", 243, "gold")]


def steps(pv, pb, have_pv=(), have_pb=(), t0=0.5, gap=0.9):
    st = [(-1, 0, n, v, c) for n, v, c in PV if n in have_pv] + [(-1, 1, n, v, c) for n, v, c in PB if n in have_pb]
    k = 0
    for side, rows, names in ((0, PV, pv), (1, PB, pb)):
        for n, v, c in rows:
            if n in names:
                st.append((t0 + gap * k, side, n, v, c))
                k += 1
    return st


C.charts({
    "g1_juku": B.Chart(VS, steps(["中学受験の塾"], []), 1400, bg=KIDS, head=HEAD, highlight=0),
    "g2_chu": B.Chart(VS, steps(["私立中 3年"], ["公立中 3年"], have_pv=["中学受験の塾"]), 1400, bg=CLASS, head=HEAD),
    "g3_kou": B.Chart(VS, steps(["私立高 3年"], ["公立高 3年"], have_pv=["中学受験の塾", "私立中 3年"], have_pb=["公立中 3年"]),
                      1400, bg=GATE, head=HEAD),
    "g4_dai": B.Chart(VS, steps(["私立大 4年"], ["国立大 4年"], have_pv=["中学受験の塾", "私立中 3年", "私立高 3年"],
                                have_pb=["公立中 3年", "公立高 3年"]), 1400, bg=CAMPUS, head=HEAD, result_at=2.6, highlight=0),
    "g5_year": B.Chart([("公立中", "teal"), ("私立中", "red"), ("公立高", "navy"), ("私立高", "pink")],
                       [(0.4, 0, "", 54, "teal"), (1.0, 1, "", 156, "red"), (1.6, 2, "", 60, "navy"), (2.2, 3, "", 103, "pink")], 180,
                       bg=CLASS, head="1年でかかるお金（塾などもふくむ・目安）", total_fmt="年{v}万", highlight=1),
})


def cuts_all():
    return [
        # ---- つかみ ----
        nn("中学から私立って\nやっぱり\nお金かかるの？", KIDS, se="question_hatena_maou", bgm={"file": C.PURPLE, "gain": -4}),
        ss("塾から大学まで\nぜんぶ足すと……", KIDS, se="pi"),
        C.slot(MONEY, "大学まで国公立とくらべて 差は 約", 700, "万円", dur=3.6),
        boom("700万!?", MONEY, se=[CONAN]),
        fx(nn("え……\n家の頭金が\n払えるじゃん", MONEY, se=POON), "mono"),
        C.title(GATE, "read_book_orange_kitten", "money_counting_orange_cat"),
        C.card("e02_premise", "子ども1人・家から通う場合でくらべる", dur=5.2),
        # ---- 中学受験 ----
        chap("① 中学受験の塾", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("私立中学を受けるなら\n小学4年生から\n塾に通うことが多い", KIDS, se="pi"),
        ss("夏期講習・冬期講習\n模試に特訓", KIDS, se="kon"),
        ss("3年間で\n約250万", KIDS, se="kon"),
        g("g1_juku", "中学に入る前から\n250万", dur=3.6),
        boom("小学生で\n250万!?", KIDS, se=["explosion_chudoon"]),
        nn("小学生の夏休みが\n塾で消える……", KIDS, se="deflate_hyororo"),
        # ---- 中学 ----
        chap("② 中学の3年間", se="doon_heavy"),
        ss("公立中学は\n授業料がかからない", CLASS, se="pi"),
        ss("それでも給食費・部活・塾で\n1年に約54万", CLASS, se="kon"),
        ss("私立中学は\n授業料や施設費で\n1年に約156万", CLASS, se="kon"),
        g("g5_year", "1年でこんなに\nちがう", dur=4.4),
        nn("私立は\n公立の約3倍!?", CLASS, red=True, se=["explosion_dokaan"]),
        g("g2_chu", "中学3年間で\n300万以上の差", dur=4.0),
        ss("そのかわり\n高校受験がない\n中高一貫校も多い", CLASS, se="pikon"),
        # ---- 高校 ----
        chap("③ 高校の3年間", se="whoosh_shu", bgm={"file": C.COCOA, "gain": -4, "fade": 0.6}),
        ss("公立高校は\n授業料の支援があって\n実質0円", GATE, se="pi"),
        ss("私立高校も\n2026年度から\n支援が広がった", GATE, se="pikon"),
        ss("授業料を\n1年に45.7万まで\n国が出してくれる", GATE, se="kon"),
        nn("私立高校も\nかなり安くなったんだ", GATE, se="pikon"),
        ss("でも施設費や\n修学旅行は\n自分ではらう", GATE, se="kon"),
        g("g3_kou", "高校は\n差がちぢむ", dur=4.0),
        # ---- 大学 ----
        chap("④ 大学の4年間", se="doon_heavy", bgm={"file": C.MIRAI, "gain": -4, "fade": 0.6}),
        ss("国立大学は\n入学金と授業料で\n4年で約243万", CAMPUS, se="pi"),
        ss("最近は授業料を\n上げる国立大学も\n出てきた", CAMPUS, se="pc_warning"),
        ss("私立大学の文系は\n4年で約400万", CAMPUS, se="kon"),
        ss("理系や医学部は\nもっとかかる", CAMPUS, se="kon"),
        g("g4_dai", "ぜんぶ積むと……", dur=5.4),
        qq(MONEY, "tv_professional_poon_remix_a"),   # 11/3 ユーザー指定：ポーン連打
        fx(boom("1290万\nvs\n585万!!", MONEY, se=["explosion_chudoon"]), "money"),
        fx(nn("差は\n約700万……", MONEY, se="tv_professional_poon_remix_a"), "swirl"),
        nn("子ども2人なら\n1400万!?", MONEY, red=True, se=["explosion_dokaan"]),
        # ---- お金以外 ----
        chap("⑤ お金以外のちがい", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("私立は\n設備や行事が\n充実していることが多い", GATE, se="kon"),
        ss("中高一貫なら\n6年間\n同じ友だちと過ごせる", CLASS, se="pikon"),
        ss("公立は\nいろいろな人と\n出会える", CLASS, se="kon"),
        ss("国公立の大学に入るには\n高校で\nしっかり勉強が必要", STUDY, se="pi"),
        nn("結局どっちも\n勉強は\nがんばるんだね", STUDY, se="deflate_hyororo"),
        # ---- 備え ----
        chap("⑥ どう備える？", se="whoosh_shu"),
        ss("中学から私立なら\n小学生のうちから\n毎月の積み立てを", NIGHT, se="kon"),
        ss("高校・大学の\n支援制度は\n毎年変わるので確認を", NIGHT, se="pc_warning"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy"),
        C.card("e07_points", "中学から私立は 約700万多くかかる", dur=5.6),
        nn("お金と\n子どもの気持ち\nどっちも大事だね", NIGHT, se="kon"),
        ss("早めに知っておけば\n準備はできる", NIGHT, se="kon"),
        C.ending(GATE)[0],
        C.end_today(GATE, (("read_book_orange_kitten", 220, 560), ("dance_three_kittens", 640, 520), ("calm_black_face_sheep", 1000, 560),
                           ("money_counting_orange_cat", 1360, 560), ("dance_happy_banana_cat", 1720, 600))),
    ]


if __name__ == "__main__":
    C.main("41_gakuhi", cuts_all, ["g1_juku", "g2_chu", "g3_kou", "g4_dai", "g5_year"])
