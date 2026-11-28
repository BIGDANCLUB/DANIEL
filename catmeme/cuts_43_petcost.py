"""43_petcost（犬と猫、一生でいくらかかる？）（11/6 ユーザー指定・自堕落ではない長尺の候補1番・EV回と同じ作り）。2〜3分。

python3 catmeme/cuts_43_petcost.py [--charts|--len]
数字は目安（調査の平均）：
  1年の支出：犬 41万3416円／猫 19万5427円（アニコム損保「ペットにかける年間支出調査」2025年・契約者アンケート）
  治療費（1年）：犬 8万9120円／猫 4万7130円（猫は前年の約1.45倍）
  平均寿命：犬 14.82歳／猫 16.00歳（ペットフード協会「全国犬猫飼育実態調査」2025年）。超小型犬 15.28歳・中型大型犬 13.63歳
  → 一生（1年×寿命）：犬 約612万（41.3×14.82）／猫 約313万（19.5×16.00）→ 犬は猫の約2倍
原稿のルール：犬も猫もけなさない。調査は「保険の契約者のアンケート」なので目安と言う。今日の一言はエンディング画面
"""
import compare_long as C
import wide_bars as B

ROOM, KIDS, PARK, CLINIC, NIGHT = ("bg02_room", "bg19_kids_room", "bg59_sakura_park", "bg28_jp_clinic", "bg14_home_night")
C.setup("43_petcost", {})
bg, nn, ss, boom, qq, g, fx, chap = C.bg, C.nn, C.ss, C.boom, C.qq, C.g, C.fx, C.chap
CONAN, POON, MONEY = C.CONAN, C.POON, C.MONEY
VS = [("犬", "orange"), ("猫", "teal")]

C.charts({
    "p1_year": B.Chart(VS, [(0.4, 0, "1年", 41.3, "orange"), (1.4, 1, "1年", 19.5, "teal")], 45, bg=ROOM,
                       head="1年にかかるお金（平均・目安）", total_fmt="{v}万", highlight=1),
    "p2_care": B.Chart(VS, [(0.4, 0, "治療費", 8.9, "orange"), (1.4, 1, "治療費", 4.7, "teal")], 10, bg=CLINIC,
                       head="1年の治療費（平均・目安）", total_fmt="{v}万", highlight=1),
    "p3_life": B.Chart(VS, [(0.4, 0, "寿命", 14.82, "orange"), (1.4, 1, "寿命", 16.0, "teal")], 18, bg=PARK,
                       head="平均寿命", total_fmt="{v}歳", highlight=1),
    "p4_total": B.Chart(VS, [(0.4, 0, "一生", 612, "orange"), (1.6, 1, "一生", 313, "teal")], 650, bg=MONEY,
                        head="一生でかかるお金（1年×寿命・目安）", total_fmt="約{v}万", result_at=2.8, highlight=1),
})


def cuts_all():
    return [
        # ---- つかみ ----
        nn("犬と猫\n一生でかかるお金は\nどっちが多い？", ROOM, se="question_hatena_maou", bgm={"file": C.PURPLE, "gain": -4}),
        ss("毎月のエサ代くらい\nと思っていると", ROOM, se="pi"),
        C.slot(MONEY, "一生でかかるお金は\n犬なら\n約", 610, "万円", dur=3.6),
        boom("610万!?", MONEY, se=[CONAN]),
        fx(nn("猫だと\nいくらなの？", MONEY, se=POON), "swirl"),
        C.title(ROOM, "dance_cute_dog", "meow_gray_white_kitten"),
        C.card("e02_premise", "ペット保険のアンケートの平均でくらべる", dur=5.2),
        # ---- 1年 ----
        chap("① 1年でいくら？", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("ペット保険の会社が\n毎年 飼い主に\n聞いている調査がある", ROOM, se="pi"),
        ss("1年にかかるお金は\n犬が約41万\n猫が約20万", ROOM, se="kon"),
        g("p1_year", "犬は猫の\n約2倍", dur=4.2),
        boom("1年で\n41万!?", ROOM, se=["explosion_chudoon"]),
        ss("フード\nおやつ\nトイレ用品", KIDS, se="kon"),
        ss("犬はさらに\nトリミングや\nしつけ教室も", PARK, se="pikon"),
        ss("旅行のときの\nペットホテルも\nかかる", PARK, se="kon"),
        nn("猫は\n散歩もトリミングも\nいらないことが多い", ROOM, se="pikon"),
        # ---- 病院 ----
        chap("② 病院のお金", se="doon_heavy"),
        ss("ケガや病気の\n治療費は\n1年で", CLINIC, se="pi"),
        g("p2_care", "犬が約9万\n猫が約5万", dur=4.2),
        ss("でも猫の治療費は\n前の年の\n約1.5倍に増えた", CLINIC, se="pc_warning"),
        nn("猫も\n病院代は\nあなどれない", CLINIC, se="question_hatena_maou"),
        ss("ペットには\n人間の健康保険がない\n病院代はぜんぶ自分で", CLINIC, se="kon"),
        ss("だから\nペット保険に入る人も\n多い", CLINIC, se="pikon"),
        # ---- 寿命 ----
        chap("③ 何年いっしょにいられる？", se="whoosh_shu", bgm={"file": C.COCOA, "gain": -4, "fade": 0.6}),
        ss("平均寿命は\n犬が約14.8歳\n猫が約16歳", PARK, se="pi"),
        g("p3_life", "猫のほうが\n少し長生き", dur=4.0),
        ss("犬は体が小さいほど\n長生きの傾向\n小さい犬は約15.3歳", PARK, se="kon"),
        nn("15年以上\nいっしょにいられるのは\nうれしい", PARK, se="shine_kiraan_maou"),
        # ---- 一生 ----
        chap("④ 一生でいくら？", se="doon_heavy", bgm={"file": C.MIRAI, "gain": -4, "fade": 0.6}),
        ss("1年のお金×寿命で\nざっくり計算すると", MONEY, se="pi"),
        g("p4_total", "一生で\nかかるお金は……", dur=5.0),
        qq(MONEY, "anime_conan_hirameki_remix_b"),
        fx(boom("犬 約610万\n猫 約310万!!", MONEY, se=["explosion_dokaan"]), "money"),
        fx(nn("犬は\n新車が\n買えるくらい!?", MONEY, se="tv_professional_poon_remix_a"), "swirl"),
        ss("年をとると\n病院に行く回数が\n増えることも多い", CLINIC, se="kon"),
        ss("お金は\n後半ほど\nかかりやすい", CLINIC, se="pi"),
        # ---- お金以外 ----
        chap("⑤ お金以外のちがい", se="whoosh_shu", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("犬は毎日の散歩で\n飼い主も\n歩くようになる", PARK, se="kon"),
        ss("猫は\nひとり暮らしでも\n飼いやすい", NIGHT, se="kon"),
        nn("どっちも\n家族が1人\nふえるのと同じ", NIGHT, se="pikon"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy"),
        C.card("e07_points", "一生のお金を知ってから迎えよう", dur=5.6),
        nn("かわいさは\nプライスレス", NIGHT, se="shine_kiraan_maou"),
        ss("迎える前に\n一生分のお金を\n考えておこう", NIGHT, se="pc_warning"),
        C.ending(ROOM)[0],
        C.end_today(ROOM, (("dance_cute_dog", 220, 560), ("meow_gray_white_kitten", 640, 560), ("money_counting_orange_cat", 1000, 560),
                           ("dance_white_dog", 1360, 560), ("dance_happy_banana_cat", 1720, 600))),
    ]


if __name__ == "__main__":
    C.main("43_petcost", cuts_all, ["p1_year", "p2_care", "p3_life", "p4_total"])
