"""35_tower（タワマンvs郊外の一戸建て 30年でかかるお金）（11/1 ユーザー指定・車ありvs車なしと同じ作り）。3分ほど。

python3 catmeme/cuts_35_tower.py [--charts|--len]
数字はざっくりの目安（2026年・首都圏・同じ6500万円で買った場合・30年）。ローンの返済は同じなので「家を持つためのお金」だけくらべる：
  タワマン（湾岸・70㎡）：管理費 月2.5万＝年30万／修繕積立金 月1.5万→上がって平均 月2.5万＝年30万／駐車場 月3万＝年36万／
    固定資産税 年20万／保険 年1万 → 年 約117万 → 30年 約3500万
  郊外の一戸建て（4LDK）：管理費・駐車場 0／修繕（屋根・外壁・給湯器・水回り）30年で約800万＝年27万／固定資産税 年15万／
    火災・地震保険 年4万／庭・外まわり 年2万 → 年 約48万 → 30年 約1440万
  売るとき：タワマンは値下がりしにくい場所が多い（30年後 約4500万の目安）／一戸建ては建物の価値が下がり、土地の分（約2000万）が中心
  → 住み続けるなら一戸建てが安い。売るならタワマンが取り戻しやすいことも
原稿のルール：実在の人・会社・マンション名は出さない。今日の一言・単語の途中で改行しない・最後はチャンネル登録・過去の動画にはふれない
"""
import compare_long as C
import wide_bars as B

TOWER, HOUSE, LOBBY, PARK, ROOF, STREET = ("bg35_tower", "bg35_house", "bg35_tower_lobby", "bg35_tower_parking", "bg35_house_repair",
                                           "bg35_suburb_street")
C.setup("35_tower", {TOWER: "bg76_roppongi_night", HOUSE: "bg48_clean_street", LOBBY: "bg78_agency_office",
                     PARK: "bg26_parking_lot", ROOF: "bg26_car_inspection", STREET: "bg59_sakura_park"})
bg, nn, ss, boom, qq, g, fx, chap = C.bg, C.nn, C.ss, C.boom, C.qq, C.g, C.fx, C.chap
CONAN, POON, MONEY = C.CONAN, C.POON, C.MONEY

VS = [("タワマン", "purple"), ("郊外の一戸建て", "teal")]
HEAD = "1年でかかるお金（ローンの返済はのぞく・目安）"
TW = [("管理費", 30, "purple"), ("修繕積立金", 30, "navy"), ("駐車場", 36, "red"), ("固定資産税", 20, "orange"), ("保険", 1, "pink")]
HS = [("修繕（自分で）", 27, "teal"), ("固定資産税", 15, "orange"), ("火災・地震保険", 4, "pink"), ("庭・外まわり", 2, "green")]


def steps(tw, hs, have_tw=(), have_hs=(), t0=0.5, gap=0.9):
    st = [(-1, 0, n, v, c) for n, v, c in TW if n in have_tw] + [(-1, 1, n, v, c) for n, v, c in HS if n in have_hs]
    k = 0
    for n, v, c in TW:
        if n in tw:
            st.append((t0 + gap * k, 0, n, v, c))
            k += 1
    for n, v, c in HS:
        if n in hs:
            st.append((t0 + gap * k, 1, n, v, c))
            k += 1
    return st


AT, AH = [n for n, _, _ in TW], [n for n, _, _ in HS]
C.charts({
    "t0_preview": B.Chart(VS, [(0.3 + 0.3 * k, 0, n, v, c) for k, (n, v, c) in enumerate(TW)]
                          + [(2.2 + 0.35 * k, 1, n, v, c) for k, (n, v, c) in enumerate(HS)], 125, bg=TOWER, head=HEAD, highlight=1),
    "t1_kanri": B.Chart(VS, steps(["管理費", "修繕積立金"], []), 125, bg=LOBBY, head=HEAD),
    "t2_park": B.Chart(VS, steps(["駐車場"], [], have_tw=["管理費", "修繕積立金"]), 125, bg=PARK, head=HEAD),
    "t3_repair": B.Chart(VS, steps([], ["修繕（自分で）"], have_tw=["管理費", "修繕積立金", "駐車場"]), 125, bg=ROOF, head=HEAD),
    "t4_all": B.Chart(VS, steps(["固定資産税", "保険"], ["固定資産税", "火災・地震保険", "庭・外まわり"],
                                have_tw=["管理費", "修繕積立金", "駐車場"], have_hs=["修繕（自分で）"]), 125, bg=MONEY, head=HEAD,
                      result_at=5.0, highlight=1),
    "t5_shuzen": B.Chart([("10年目", "navy"), ("20年目", "purple"), ("30年目", "red")],
                         [(0.4, 0, "", 1.5, "navy"), (1.2, 1, "", 2.5, "purple"), (2.0, 2, "", 3.5, "red")], 4,
                         bg=LOBBY, head="タワマンの修繕積立金（月・目安）", total_fmt="月{v}万", highlight=2),
    "t6_30y": B.Chart(VS, [(0.4, 0, "30年分", 3510, "purple"), (1.6, 1, "30年分", 1440, "teal")], 3800, bg=MONEY,
                      head="30年でかかるお金（ローンの返済はのぞく）", total_fmt="{v}万", result_at=2.6, highlight=1),
    "t7_sell": B.Chart(VS, [(0.4, 0, "30年後に売ると", 4500, "purple"), (1.6, 1, "30年後に売ると", 2000, "teal")], 5000, bg=STREET,
                       head="30年後に売ったときの値段（目安）", total_fmt="{v}万", result_at=2.6, highlight=0),
})


# 11/1 ユーザー指定：つかみのグラフは左（タワマン）の最後を1UP、右（一戸建て）の最後をパフではなく気の抜けたゲームの音に。
# 「30年後に売ったら」の結果はゴマダレ
C.K.STEP_SE["t0_preview"] = C.K.GAME_STEP[:len(TW) - 1] + ["game_mario_1up"]
C.K.DROP_SE["t0_preview"] = {1: ["pafu"] * (len(HS) - 1) + ["game_dq_miss"]}
C.K.RESULT_SE["t7_sell"] = "game_zelda_item_get"


def cuts_all():
    return [
        C.notice(TOWER, (("cocky_dj_cat", 220, 600), ("dance_three_kittens", 640, 520), ("happy_hamster_open_arms", 1000, 560),
                         ("money_counting_orange_cat", 1360, 560), ("dance_happy_banana_cat", 1720, 600))),
        # ---- つかみ ----
        nn("同じ6500万円なら\nタワマンと一戸建て\nどっちがいい？", TOWER, se="question_hatena_maou", bgm={"file": C.PURPLE, "gain": -4}),
        ss("ローンの返済は同じ\nでも住むだけで\nかかるお金がちがう", TOWER, se="pi"),
        C.slot(TOWER, "タワマン 年 約", 117, "万円"),
        boom("住むだけで\n年117万!?", TOWER, se=[CONAN]),
        g("t0_preview", "一戸建ては\n年 約48万", dur=5.6),
        fx(nn("え……\n2倍以上\nちがうの？", MONEY, se=POON), "mono"),
        C.title(TOWER, "cocky_dj_cat", "happy_hamster_open_arms"),
        C.card("e02_premise", "首都圏・同じ6500万円で買った場合", dur=5.2),
        # ---- 管理費・修繕積立金 ----
        chap("① 管理費と修繕積立金", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("マンションは\n毎月 管理費をはらう", LOBBY, se="pi"),
        nn("何に使うお金？", LOBBY, se="question_hatena_maou"),
        ss("コンシェルジュ\nジムやラウンジ\nエレベーターの電気代", LOBBY, se="kon"),
        ss("タワマンは\n共用の設備が豪華なぶん\n月2.5万くらい", LOBBY, se="pi"),
        ss("さらに\n修繕積立金", LOBBY, se="pi"),
        nn("それは\n何のお金？", LOBBY, se="question_hatena_maou"),
        ss("将来の大規模修繕の\nためにみんなで\n積み立てるお金", LOBBY, se="kon"),
        g("t1_kanri", "この2つで\n年60万", dur=3.8),
        g("t5_shuzen", "しかも修繕積立金は\nだんだん上がる\nことが多い", dur=3.8),
        boom("30年目には\n月3.5万!?", LOBBY, se=["explosion_chudoon"]),
        ss("タワマンの修繕は\n足場が組めないので\n費用が高くなりやすい", LOBBY, se="pc_warning"),
        # ---- 駐車場 ----
        chap("② 駐車場", se="whoosh_shu"),
        ss("タワマンの駐車場は\n機械式が多い", PARK, se="pi"),
        ss("都心に近いと\n月3万円以上も", PARK, se="kon"),
        g("t2_park", "駐車場だけで\n年36万", dur=3.6),
        fx(boom("駐車場代で\n軽自動車が\n買える!?", PARK, se=["explosion_chudoon", {"f": "glass_break_01", "gain": -4}]), "crack"),
        nn("一戸建ては？", HOUSE, se="question_hatena_maou"),
        ss("家の前に\nとめれば\n0円", HOUSE, se="pikon"),
        # ---- 一戸建ての修繕 ----
        chap("③ 一戸建ての修繕", se="doon_heavy", bgm={"file": C.COCOA, "gain": -4, "fade": 0.6}),
        nn("一戸建ては\n管理費0円！\n最強じゃん", HOUSE, se="pikon"),
        ss("でも修繕は\n自分でやる", ROOF, se="pi"),
        ss("屋根と外壁は\n15年ごとに\n100万〜200万", ROOF, se="kon"),
        ss("給湯器\nお風呂・キッチン\nトイレも交換", ROOF, se="kon"),
        boom("30年で\n約800万!?", ROOF, se=["explosion_dokaan"]),
        g("t3_repair", "1年あたり\n27万", dur=3.6),
        ss("しかも一度に\nまとめてかかる", ROOF, se="pc_warning"),
        fx(nn("え……\n積み立ててないと\nピンチ？", ROOF, se="tv_professional_poon_remix_a"), "swirl"),
        ss("自分で\nコツコツ貯めておく\nのがおすすめ", ROOF, se="pi"),
        # ---- 税金・保険 ----
        chap("④ 税金と保険", se="whoosh_shu"),
        ss("固定資産税は\nどちらも毎年かかる", STREET, se="pi"),
        ss("タワマンは\n年20万くらい\n一戸建ては15万くらい", STREET, se="kon"),
        ss("火災保険は\n一戸建てのほうが\n高め", STREET, se="kon"),
        g("t4_all", "ぜんぶ積むと……", dur=6.0),
        fx(boom("タワマン117万\n一戸建て48万!!", MONEY, se=["explosion_dokaan"]), "money"),
        g("t6_30y", "30年で\nくらべると……", dur=4.6),
        qq(MONEY, "anime_conan_hirameki_remix_b"),
        fx(boom("30年で\n2000万以上の差!?", MONEY, se=["explosion_chudoon"]), "money"),
        # ---- 売るとき ----
        chap("⑤ でも売るときは？", se="quiz_question_01", bgm={"file": C.MIRAI, "gain": -4, "fade": 0.6}),
        ss("タワマンは\n人気の場所なら\n値下がりしにくい", TOWER, se="pi"),
        ss("一戸建ては\n建物の価値が下がって\n土地の値段が中心", HOUSE, se="kon"),
        g("t7_sell", "30年後に\n売ったら……", dur=4.6),
        boom("売る値段は\nタワマンが\n2500万高い!?", TOWER, se=["explosion_dokaan"]),
        fx(nn("え……\nじゃあ結局\nどっちが得？", MONEY, se=POON), "mono"),
        ss("住み続けるなら\n一戸建て", HOUSE, se="pikon"),
        ss("いつか売るなら\nタワマンが\n取り戻しやすいことも", TOWER, se="pikon"),
        # ---- ほかのちがい ----
        chap("⑥ お金以外のちがい", se="whoosh_shu"),
        ss("タワマンは駅近\n眺めがいい\nセキュリティも安心", TOWER, se="kon"),
        ss("でも朝は\nエレベーター待ち", TOWER, se="cuckoo_pappo"),
        nn("地震で止まったら\n階段で30階!?", TOWER, red=True, se=["explosion_dokaan"]),
        ss("一戸建ては\n広い・静か\n庭で遊べる", HOUSE, se="kon"),
        ss("でも駅から遠くて\n車が必要なことも", HOUSE, se="pi"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        C.card("e07_points", "買うときは毎月の維持費まで見よう", dur=5.6),
        nn("値段だけで\nえらんじゃダメだね", STREET, se="kon"),
        ss("住み続けるか\n売るか\nで答えが変わる", STREET, se="kon"),
    ] + C.ending(STREET)


if __name__ == "__main__":
    C.main("35_tower", cuts_all, ["t0_preview", "t1_kanri", "t2_park", "t3_repair", "t4_all", "t5_shuzen", "t6_30y", "t7_sell"])
