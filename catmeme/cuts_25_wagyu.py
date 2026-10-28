"""25_wagyu（和牛を狙った男たち ―― 日本の宝はなぜ守られなかったのか）のカット割り。構成はユーザー指定（10/27）。約7分。作りは 24本目と同じ。

python3 catmeme/cuts_25_wagyu.py          → out/25_wagyu_full.mp4
python3 catmeme/cuts_25_wagyu.py --audio  → 音だけ作り直す

原稿のルール：
- 実在の人（運んだ男・牧場経営者・農家）は猫で演じない・名前も出さない。役所・当局は名札つきの猫（org）だけ
- 事件の当事者をからかわない。笑いは「ストロー1本で運べてしまう」「法律がなかった」などしくみのほうで取る
- 全動画共通：今日の一言・単語の途中で改行しない・最後はチャンネル登録の画面・過去の動画にはふれない
"""
import os
import sys

import cuts_04_leak as L
import render as R

R.TEMPO = getattr(R, "TEMPO", 1.0) * 0.74   # 10/28 ユーザー指定：スピード感・テンポよく4〜5分に
HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("25_wagyu", "25_world", "14_japan", "16_tenchim", "15_vambi", "04_leak", "02_october",
                                                         "01_todai", "jidaraku/01_yakiniku", "18_semicon")]
L.PT = os.path.join(HERE, "parts", "25_wagyu")
pt, cat, close, dia, expl, chap, net, nn, ss = L.pt, L.cat, L.close, L.dia, L.expl, L.chap, L.net, L.nn, L.ss
N, S = L.N, L.S
PURPLE, COCOA, MIRAI, KAMI = L.PURPLE, L.COCOA, L.MIRAI, L.KAMI
AM223 = os.path.join(L.BGM, "2_23_AM.mp3")
NORA = L.NORA
STING = {"file": KAMI, "len": 3.5, "gain": -14}

ORG_COLOR = (90, 60, 150)
ORG_CAT = {"中国の検疫当局": "stare_interviewer_cat", "農林水産省": "work_typing_cat", "警察": "angry_aiming_cat",
           "裁判所": "stare_standing_marmot", "国会": "talk_orange_white_sitting_cat", "アメリカの牧場": "cocky_dj_cat"}
for _o in ORG_CAT:
    L.ROLE[_o] = ORG_COLOR

# 背景（ChatGPT で作る背景が届いたら backgrounds/25_wagyu に同じ名前で置けば差しかわる。指示文 scripts/25_wagyu_bg_prompts.md）
FERRY, RANCH, STEAK, STRAW, US_RANCH, WORLD, POLICE, COURT, DIET, BOARD, SNS, GRILL = (
    "bg25_ferry_port", "bg25_wagyu_ranch", "bg25_wagyu_steak", "bg25_frozen_straws", "bg25_us_ranch", "bg44_world_map",
    "bg77_police_station", "bg85_courtroom", "bg115_japan_diet", "bg03_blackboard", "bg09_sns", "j05_grill")
CUSTOMS = "bg25_customs_gate"
STANDIN = {FERRY: "bg45_airport_arrival", RANCH: "bg63_hokkaido_field", STEAK: "j05_grill", STRAW: "bg03_jp_material_plant",
           US_RANCH: "bg63_hokkaido_field", DIET: "bg84_courthouse", CUSTOMS: "bg45_airport_arrival"}
_bg = L.bg


def bg(n):
    try:
        return _bg(n)
    except FileNotFoundError:
        return _bg(STANDIN[n])


L.bg = bg


def org(b, who, sub, **kw):
    return dict(bg=bg(b), cats=[cat(ORG_CAT[who], who, 960, h=720)], say=sub, text_top=True, **kw)


def card(c, sub, b=BOARD, **kw):
    return dia(c, sub, b, right=S, dur=kw.pop("dur", 5.0), se=kw.pop("se", "card_flip"), **kw)


def ex(b, text, **kw):
    return expl(b, [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "", text, dur=kw.pop("dur", 4.2),
                se=kw.pop("se", "pinpon_notice"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        # 背景で猫ミームが動いている上に、画面を半分暗くして注意書き（音なし・10/28 ユーザー指定）
        dict(bg=bg(STEAK), cats=[{"a": a_, "x": x_, "h": h_, "bottom": 1070, "mute": True} for a_, x_, h_ in (
                ("dance_tabby_standing_cat", 220, 620), ("dance_three_kittens", 640, 520), ("happy_hamster_open_arms", 1000, 560),
                ("dance_orange_gray_cats", 1360, 600), ("happy_girlfriend_dance_cat", 1720, 600))],   # 素材をたくさん（10/28）
             fx=["dim"], layers_top=[pt("e00_notice")], dur=6.0, no_pop=True, notice=True,
             se={"f": "chime_announce", "len": 3.0, "gain": -2}),   # ピンポンパンポーン
        # ---- ① つかみ ----
        ss("2018年6月\n大阪から上海へ向かう\n1隻のフェリー", FERRY, se="page_turn_01", bgm={"file": PURPLE, "gain": -4}),
        nn("フェリーの旅？\nいいねぇ", FERRY, se="pikon"),
        ss("荷物の中から\nあるものが見つかった", FERRY, se="pi"),
        org(STRAW, "中国の検疫当局", "これは……\n和牛の精液と受精卵の\nストロー365本！", se=["explosion_chudoon"], sting=STING),
        close(STRAW, "@react", "ニュース猫", "365本！？\n1年分あるじゃん！", se=["explosion_dokaan"]),
        ss("見つけたのは\n日本じゃなくて\n中国の検疫当局", STRAW, se="kon"),
        nn("え\n日本はスルー\nしちゃったの？", STRAW, se="question_mark_pop_confused_huh"),
        ss("日本の税関は\n気づかなかった\nと報じられている", CUSTOMS, se="kon"),
        nn("ザル……\nいや、言っちゃダメか", STRAW, se="deflate_hyororo"),
        dict(bg=bg(STEAK), card=pt("e01_title"), dur=4.2, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        ss("世界が欲しがる和牛は\nなぜこんなに簡単に\n海を渡りかけたのか", STEAK, se="tv_professional_poon"),
        nn("そもそも\nなんで精液と受精卵\nなんだろう？", STEAK, se="question_hatena_maou"),
        ss("それを順番に\n見ていこう", STEAK, se="tv_professional_poon"),
        # ---- ② 和牛とは何か ----
        chap("そもそも\n和牛って何？", se="quiz_question_01", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        nn("和牛って\n日本の牛なら\nぜんぶ和牛でしょ？", RANCH, se="question_hatena_maou"),
        ss("ちがう\n和牛と呼べるのは\n4品種とその交配種だけ", RANCH, se="tsukkomi_bishi"),
        card("e02_wagyu", "黒毛和種・褐毛和種・日本短角種・無角和種", dur=5.4, b=RANCH),
        nn("国産牛と和牛って\n別物だったの！？", RANCH, se="shock_piano"),
        ss("国産牛は\n日本で育った牛\n品種は問わない", RANCH, se="pi"),
        ss("和牛のほとんどは\n黒毛和種", RANCH, se="kon"),
        nn("黒毛和種……\n名前からして\n強そう", RANCH, se="pikon"),
        ss("全国の和牛の\n9割以上が\n黒毛和種と言われる", RANCH, se="pi"),
        ss("何十年もかけて\n血統を記録して\n少しずつ改良してきた", RANCH, se="page_turn_01"),
        nn("どの牛と\nどの牛をかけ合わせるか\nずっと記録してるのか", RANCH, se="kon"),
        ss("種牛1頭ごとに\n子どもの肉の質まで\n調べてきた", RANCH, se="page_turn_01"),
        nn("牛の家系図が\nずっと続いてるのか", RANCH, se="kon"),
        ss("その一頭一頭が\n地域の宝として\n大切に育てられてる", RANCH, se="sparkle_kirakira_01"),
        ss("そう\nあのサシの入り方は\n農家の努力の結晶", STEAK, se="sparkle_kirakira_01"),
        close(STEAK, "@react", "ニュース猫", "うまそう……\n（よだれ）", red=False, se=["drink_gulp_gokugoku_thirsty_chug"]),
        ss("でもその成果は\n凍らせた精液と受精卵の\nストロー1本で運べてしまう", STRAW, se="pi"),
        close(STRAW, "@react", "ニュース猫", "何十年の努力が\nストロー1本！？", se=["explosion_chudoon"]),
        ss("細さは\nストローとほぼ同じ\nポケットにも入る", STRAW, se="kon"),
        nn("それはヤバい……", STRAW, se="deflate_hyororo"),
        ss("しかも液体窒素で\n凍らせておけば\n何年でも使える", STRAW, se="freeze_kochiin"),
        nn("冷凍保存OKって\nますます危ない……", STRAW, se="kon"),
        # ---- ③ 実はすでに海を渡っていた ----
        chap("実は\nすでに海を\n渡っていた", se="doon_heavy", bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        ss("話は\n1976年にさかのぼる", WORLD, se="page_turn_01"),
        org(US_RANCH, "アメリカの牧場", "研究用に\n和牛の雄牛4頭が\nアメリカへ", se="pi"),
        nn("研究用なら\nまあいいか……", US_RANCH, se="kon"),
        ss("1990年代も\n輸出は続いた", US_RANCH, se="pi"),
        ss("1993年には\n雌牛も\n海を渡った", US_RANCH, se="pi"),
        close(US_RANCH, "@react", "ニュース猫", "雌も！？\nそれ増やせちゃうじゃん！", se=["explosion_dokaan"]),
        card("e03_history", "1997年ごろまでに　200頭あまりが海外へ", dur=5.4, b=WORLD),
        ss("アメリカから\nオーストラリアなどに\n広がっていった", WORLD, se="whoosh_shu"),
        ss("今では世界中で\n「WAGYU」が\n売られている", WORLD, se="pi"),
        ss("オーストラリアは\n今では和牛の\n一大産地", WORLD, se="pi"),
        nn("本家より\nたくさん作ってる\nかもしれない！？", WORLD, se="question_mark_pop_confused_huh"),
        nn("海外のスーパーに\nWAGYUって\n書いてあるのは……", WORLD, se="kon"),
        ss("その子孫や\n交配種のことが\n多い", WORLD, se="pi"),
        close(WORLD, "@react", "ニュース猫", "日本の和牛の\nライバルになってる！？", se=["shock_piano"]),
        ss("日本は1997年に\n生きた牛の輸出を\n止めた", BOARD, se="hyoshigi_01"),
        nn("よかった\nこれでひと安心", BOARD, se="pikon"),
        ss("ところが……", BOARD, se="pi"),
        card("e03_history", "精液と受精卵を止める法律は　なかった", dur=5.0, se="doon_heavy"),
        close(BOARD, "@react", "ニュース猫", "いちばん小さくて\n運びやすいやつが\nノーマーク！？", se=["explosion_chudoon"]),
        ss("牛は止めたけど\nストローは\n止めてなかった", STRAW, se="kon"),
        nn("玄関のカギはかけたのに\n窓が全開だった\nみたいな……", STRAW, se="deflate_hyororo"),
        # ---- ④ 事件の全容 ----
        chap("事件の全容", se="doon_heavy", bgm={"file": AM223, "gain": -4, "fade": 0.6}),
        card("e04_case", "男2人が　365本を検査を受けずに中国へ持ち込もうとした", dur=5.4, b=FERRY),
        ss("日本を出るとき\n本当は検査を\n受けないといけない", CUSTOMS, se="pi"),
        nn("それを受けずに\nフェリーに\n乗っちゃった……", FERRY, se="kon"),
        org(STRAW, "中国の検疫当局", "書類がない\n持ち込みは\n認めません", se="buzzer_wrong"),
        ss("中国の入国検査で\n拒否されて\n日本に戻ってきた", FERRY, se="pi"),
        nn("相手の国に\n止められて\n帰ってきたの……", FERRY, se="deflate_hyororo"),
        ss("中身は\nすべて廃棄された", STRAW, se="glass_break_01"),
        close(STRAW, "@react", "ニュース猫", "365本が\nぜんぶ……", red=False, se=["tear_drop"]),
        card("e04_case", "提供したのは　徳島県の畜産農家", dur=4.6),
        org(POLICE, "警察", "2019年\n牧場経営者らを\n逮捕", se="siren_police"),
        ss("「過去にも\n何度も運んだ」\nという供述もあったとされる", POLICE, se="pi"),
        close(POLICE, "@react", "ニュース猫", "初めてじゃ\nなかったの！？", se=["explosion_dokaan"]),
        nn("じゃあ\nもうとっくに\n流れてたかも……", POLICE, se="kon"),
        ss("それは\n誰にもわからない", POLICE, se="pi"),
        org(COURT, "裁判所", "懲役2年と\n懲役1年2か月\nいずれも執行猶予3年", se="game_aceattorney_desk_slam"),
        ss("2人とも初めての罪で\n反省もしているとして\n執行猶予がついた", COURT, se="pi"),
        nn("執行猶予……\nけっこう軽い？", COURT, se="question_mark_pop_confused_huh"),
        card("e05_charge", "問われたのは　検査を受けずに持ち出したことだけ", dur=5.0, b=COURT),
        ss("遺伝資源を\n持ち出すこと自体を\n禁じる法律はなかった", COURT, se="kon"),
        close(COURT, "@react", "ニュース猫", "和牛を持ち出したことは\n罪じゃなかったの！？", se=["explosion_chudoon"], sting=STING),
        ss("罪になったのは\n“検査の手続き”の\nほうだった", COURT, se="pi"),
        nn("家のカギを持ち出して\n“書類不備”で\n怒られたみたいな……", COURT, se="deflate_hyororo"),
        ss("この事件で\n“和牛の遺伝資源を守る法律が\nない”ことが知れわたった", BOARD, se="kon"),
        nn("みんなが\n「え、なかったの！？」\nってなったわけか", BOARD, se="question_mark_pop_confused_huh"),
        # ---- ⑤ 日本がようやく動いた ----
        chap("日本が\nようやく動いた", se="power_up", bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        org(DIET, "国会", "2020年\n家畜遺伝資源の\n不正競争防止法が成立", se="jan"),
        ss("同じ年の10月から\n動き出した", DIET, se="pi"),
        card("e06_law", "不正な入手・使用・転売を禁止", dur=4.6),
        card("e06_law", "不正に流れたものから生まれた子牛・受精卵も対象", dur=5.0),
        nn("生まれた子牛まで\n追いかけるのか", BOARD, se="kon"),
        ss("国外に持ち出すのも\nもちろんダメ", BOARD, se="buzzer_wrong"),
        ss("農家どうしの\n契約も見直された", BOARD, se="pi"),
        card("e06_law", "個人は懲役10年以下・罰金1000万円以下　法人は罰金3億円以下", dur=5.6, se="doon_heavy"),
        close(BOARD, "@react", "ニュース猫", "執行猶予だったのが\n懲役10年に！？", se=["explosion_dokaan"]),
        card("e06_law", "ストローには　種牛の名前を書くことが義務に", dur=4.8),
        ss("どの種牛のものか\nすぐわかるように\nした", STRAW, se="pinpoon_note"),
        org(STRAW, "農林水産省", "ストロー1本1本に\n名前つき", se="pikon"),
        nn("ストローに\n名札をつけたのか", STRAW, se="pikon"),
        ss("事件があって\nやっと\nルールが追いついた", BOARD, se="kon"),
        nn("でも\n昔出ていった牛は\nもう戻らないよね", WORLD, se="kon"),
        ss("そう\n海外のWAGYUを\n止める方法はない", WORLD, se="pi"),
        ss("だからこそ\n日本の和牛ならではの\n質と信頼で勝負していく", STEAK, se="tv_professional_poon"),
        # ---- ネットの声 ----
        chap("ネットの声", se="whoosh_shu", dur=1.4),
        net("@react", "精液は止めてなかった\nって聞いて\nびっくりした", se="boing_01"),
        net("@react", "見つけたのが\n中国側っていうのが\nなんとも……", se="kon"),
        net("@react", "海外のWAGYUって\nそういうことだったのか", se="pi"),
        net("@react", "農家さんの何十年を\n守る法律が\nできてよかった", se="pinpoon_correct"),
        net("sleepy_old_memories_cat", "今日の晩ごはん\n焼肉にしたくなった", se="tear_drop"),
        # ---- ⑥ 締め ----
        dict(bg=bg(RANCH), inset={"card": pt("e07_points"), "box": (200, 60, 1720, 860)}, dur=6.0,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)],
             bgm={"file": MIRAI, "gain": -2, "fade": 0.8}, se="chiin_01"),
        ss("和牛の価値は\n農家が何十年も\nかけてきた時間そのもの", RANCH, se="tv_professional_poon"),
        ss("一度渡った血統は\n取り戻せない", RANCH, se="kon"),
        nn("だからこそ\n残ったものを\n守る意味があるんだね", RANCH, se="chirin"),
        ss("次に和牛を食べるとき\nその裏の歴史を\n少し思い出してほしい", STEAK, se="chirin"),
        nn("いただきます……\n（しみじみ）", STEAK, se="kon"),
        dict(bg=bg(STEAK), card=pt("e10_ending"), dur=3.6, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


FLASHY = ("explosion", "shock", "dokaan", "desk_slam", "siren", "jan", "power_up", "doon_heavy", "glass_break")


def hype(cuts):
    """派手な演出を、見にくくならない範囲でとにかく多く（10/28 ユーザー指定：もっと派手に・もっと頻繁に）。"""
    for i, c in enumerate(cuts):
        if c.get("notice"):
            continue
        fx = list(c.get("fx", []))
        se = c.get("se")
        ses = " ".join((x if isinstance(x, str) else x.get("f", "")) for x in ([se] if isinstance(se, (str, dict)) else (se or [])))
        big = c.get("say_style") == "red" or any(k in ses for k in FLASHY) or c.get("chapter")
        fx += ["punch"]   # すべてのカット：グッと寄る（上下に流れるキラキラ・紙吹雪はなし・10/28 ユーザー指定）
        if i % 2 == 0:
            fx.append("lines")   # 2カットに1回 集中線
        if i % 4 == 1:
            fx.append("border")   # ときどき光るふち
        if big:
            fx += ["flash", "shake", "lines", "ring", "border"]
        if not big:
            fx.append("zoom")
        c["fx"] = list(dict.fromkeys(f for f in fx if f not in ("spark", "confetti")))
        # SE をもっと（10/28 ユーザー指定）：どのカットにも頭の小さな音、驚きの場面には追加の音
        lst = [] if not se else ([se] if isinstance(se, (str, dict)) else list(se))
        lst.append({"f": POP_SE[i % len(POP_SE)], "gain": -7})
        if big:
            lst.append({"f": BIG_SE[i % len(BIG_SE)], "gain": -4, "at": 0.25})
        c["se"] = lst
    return cuts


POP_SE = ("pikon", "spo", "puni", "kote", "pa", "papa", "peta", "suupo", "button_13", "cursor_move_01")   # 頭の小さな音
BIG_SE = ("voice_uuwaa", "boing_02", "tsukkomi_bashi", "punch", "frying_pan_kaan", "kaan",
          "hit_dogo_maou", "shock_piano")   # 驚きの場面に重ねる音


def cuts_full():
    return hype(L.apply_fx(L.allocate(cuts_all(), max_use=2)))   # 猫ミームの素材を増やす（同じ素材は1本で2回まで）


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "25_wagyu_full.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cuts = cuts_full()
    if sys.argv[1:] == ["--audio"]:
        R.remux_audio(cuts, out, out.replace(".mp4", "_a.mp4"))
        os.replace(out.replace(".mp4", "_a.mp4"), out)
        sys.exit()
    if sys.argv[1:] == ["--len"]:
        print(len(cuts), round(sum(R.cut_dur(c) for c in cuts), 1))
        sys.exit()
    if len(sys.argv) > 1:
        a, b = (int(x) if x else None for x in sys.argv[1].split(":"))
        cuts = cuts[a:b]
    R.render(cuts, out, preview_dir=out.replace(".mp4", "_preview"))
