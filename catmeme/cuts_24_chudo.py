"""24_chudo（議員1人の政党に交付金5.8億円　中道改革連合の政党交付金）のカット割り。原稿 scripts/24_chudo.md。作りは 10〜13本目と同じ。

python3 catmeme/cuts_24_chudo.py          → out/24_chudo_full.mp4
python3 catmeme/cuts_24_chudo.py --audio  → 音だけ作り直す

原稿のルール（必ず守る）：
- 実在の政治家は猫で演じない。発言は報道の要旨をカード・字幕で。党・役所は名札つきの猫（org）だけで出す
- 党の説明と批判の両方を出す。悪口・あだ名は使わない。数字は報道どおり（差があるものは幅で）
- 全動画共通：今日の一言・単語の途中で改行しない・最後はチャンネル登録の画面・過去の動画にはふれない
- 「これ、納得できますか？」は原稿で指定がないので使わない
"""
import os
import sys

import cuts_04_leak as L
import render as R

R.TEMPO = getattr(R, "TEMPO", 1.0) * 1.12   # 8分くらいに（10/22 ユーザー指定）。1カットを少しゆっくり

HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("24_chudo", "15_vambi", "16_tenchim", "17_imamori", "13_yard", "14_japan",
                                                         "04_leak", "02_october", "01_todai")]
L.PT = os.path.join(HERE, "parts", "24_chudo")
pt, cat, duo, solo, close, dia, expl, chap, net, nn, ss = L.pt, L.cat, L.duo, L.solo, L.close, L.dia, L.expl, L.chap, L.net, L.nn, L.ss
bg = L.bg
N, S = L.N, L.S
PURPLE, COCOA, MIRAI, KAMI = L.PURPLE, L.COCOA, L.MIRAI, L.KAMI
AM223 = os.path.join(L.BGM, "2_23_AM.mp3")
NORA = L.NORA
STING = {"file": KAMI, "len": 3.5, "gain": -14}

L.POOLS["react"] += ["stare_standing_marmot", "flip_emo_cat_hair"]
L.POOLS["calm"] += ["lick_talking_goat", "eat_chips_cat", "stand_real_sheep"]

# 主語になる党・役所は名札つきの猫で（10/14 ユーザー指定）。実在の人は猫で演じない
ORG_COLOR = (90, 60, 150)
ORG_CAT = {"中道改革連合": "meow_gray_white_kitten", "総務省": "work_typing_cat", "民主改革の会": "talk_orange_white_sitting_cat",
           "公明党": "stare_interviewer_cat", "日本維新の会": "angry_aiming_cat", "与党": "showoff_gojo_cosplay_cat",
           "世論調査": "call_customer_service_cat"}
for _o in ORG_CAT:
    L.ROLE[_o] = ORG_COLOR

# 背景（手持ち。ChatGPT で作った背景が届いたら backgrounds/24_chudo に同じ名前で置けば差しかわる）
DIET, OFFICE1, PRESS, VOTE, MONEY, PAPERS, MEETING, HALL, TL, BOARD, SNS, AGENCY = (
    "bg24_diet_building", "bg24_one_desk_office", "bg07_press", "bg04_voting", "bg87_refund_money", "bg88_contract_papers",
    "bg05_meeting", "bg75_seminar_hall", "bg103_timeline2", "bg03_blackboard", "bg09_sns", "bg78_agency_office")
STANDIN = {DIET: "bg57_tokyo_skyline", OFFICE1: "bg25_office_desk"}
_bg = L.bg


def bg(n):
    try:
        return _bg(n)
    except FileNotFoundError:
        return _bg(STANDIN[n])


L.bg = bg
V_CASH, V_CHART, V_MEET, V_DEAL, V_PHONE_W, V_HANDS, V_DARK, V_NIGHT, V_SHIBUYA, V_TYPE = (
    "v06_cash_counting", "v11_stock_chart_blue", "v14_business_meeting", "v19_handshake_business", "v18_smartphone_woman",
    "v20_smartphone_hands", "v13_cat_gray_dark", "v05_city_night_river", "v09_shibuya_crossing_aerial", "v02_typing_keyboard_closeup")


def org(b, who, sub, **kw):
    """党・役所の猫だけをまん中に（第三者の場面にはニュース猫・博識な猫は出さない）。"""
    return dict(bg=bg(b), cats=[cat(ORG_CAT[who], who, 960, h=720)], say=sub, text_top=True, **kw)


PH = os.path.join(HERE, "backgrounds", "24_chudo", "photos")   # ユーザー提供の報道写真（別のセッションで用意したもの・10/22）。
# 笑顔の写真は批判の言葉と並べない（からかっているように見えないように）


def pic(name, text, b=PRESS, **kw):
    """ユーザー提供の写真を上に枠つきで大きく、説明は下の帯。猫は右に小さく（写真の人の顔にかけない）。"""
    return dict(bg=bg(b), inset={"card": os.path.join(PH, name + "_framed.png"), "box": (140, 16, 1640, 672)}, say="",
                explain=text, no_pop=True, text_top=True, dur=kw.pop("dur", 4.4),
                cats=[cat("@calm", "博識な猫", 1760, h=380, bottom=660, float=True)], **kw)


def card(c, sub, b=BOARD, **kw):
    return dia(c, sub, b, right=S, dur=kw.pop("dur", 5.0), se=kw.pop("se", "card_flip"), **kw)


def ex(b, text, **kw):
    return expl(b, [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "", text, dur=kw.pop("dur", 4.2),
                se=kw.pop("se", "pinpon_notice"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=5.2, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- 1. つかみ ----
        org(AGENCY, "総務省", "2026年10月20日\n政党交付金を\n11の党に交付", se="page_turn_01", bgm={"file": PURPLE, "gain": -4}),
        org(MONEY, "中道改革連合", "そのうち\n所属議員1人の党に\n約5億8470万円", se=["explosion_chudoon"], sting=STING),
        close(MONEY, "@react", "ニュース猫", "議員1人で\n5億8000万円！？", se=["explosion_dokaan"]),
        ss("しかも\n12月にも\nあと約5億8000万円", MONEY, se="pi"),
        nn("1人あたり\nいくらになるの……", V_CASH, se="question_mark_pop_confused_huh"),
        ss("議員の給料じゃなくて\n“党”に入るお金な\nそこは分けて考えよう", V_CASH, se="tsukkomi_bishi"),
        dict(bg=bg(DIET), card=pt("e01_title"), dur=4.0, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        nn("なんで議員1人の党に\nそんな大金が？", TL, se="question_hatena_maou"),
        ss("党の説明と批判\n両方を\n順番に見ていこう", TL, se="tv_professional_poon"),
        # ---- 2. 中道改革連合ってどんな党？ ----
        chap("中道改革連合って\nどんな党？", se="doon_heavy", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        pic("p1_party_handshake", "中道改革連合の会見（2026年）", dur=4.0),
        card("e02_timeline", "2026年1月　立憲民主党と公明党が合流してできた新党", dur=5.4),
        nn("立憲と公明が\nひとつの党に！？", TL, se="pikon"),
        ss("“中道”を掲げて\n衆院選に挑んだ", VOTE, se="page_turn_01"),
        card("e02_timeline", "2月8日の衆院選で49議席　公示前は160議席をこえていた", dur=5.4, se="doon_heavy"),
        close(VOTE, "@react", "ニュース猫", "160から49！？", se=["shock_piano"]),
        ss("自民党は316議席\n衆院の3分の2をこえた", VOTE, se="pi"),
        card("e02_timeline", "選挙のあと　代表選で小川淳也氏が代表に", dur=4.6),
        ex(PRESS, "代表選は\n小川淳也氏27票・階猛氏22票\n（報道）", dur=3.8),
        nn("立て直しを\nめざしたんだね", MEETING, se="kon"),
        card("e02_timeline", "ところが9月　合流が決裂し、党は事実上解体", dur=5.0, se="glass_break_01"),
        close(MEETING, "@react", "ニュース猫", "解体！？\n7か月で！？", se=["explosion_chudoon"]),
        ss("立憲出身の議員は\n新党「民主改革の会」へ", MEETING, se="pi"),
        ss("公明出身の議員は\n公明党に戻った", MEETING, se="pi"),
        card("e02_timeline", "9月16日　48人の離党を承認　渡辺創氏が新代表に", dur=5.0),
        nn("49人のうち\n48人が出ていって……", OFFICE1, se="deflate_hyororo"),
        ss("残ったのは\n渡辺創衆院議員\nただ1人", OFFICE1, se="kon"),
        ex(OFFICE1, "小川前代表は渡辺氏を\n「1人しんがり」と表現した\n（報道）", dur=3.8),
        nn("しんがり……\n最後に残る役か", OFFICE1, se="kon"),
        # ---- 3. 政党交付金ってなに？ ----
        chap("政党交付金って\nなに？", se="quiz_question_01", bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        card("e03_rules", "国民1人あたり250円ぶんの税金が政党に配られる", dur=5.0),
        nn("え、税金なの？", BOARD, se="question_mark_pop_confused_huh"),
        ss("そう\n政治にかかるお金を\n税金で助ける制度", BOARD, se="pikon"),
        card("e03_rules", "対象は　国会議員5人以上の政党など", dur=4.6),
        card("e03_rules", "毎年1月1日の時点で　1年分の金額が決まる", dur=4.8),
        card("e03_rules", "4月・7月・10月・12月の年4回に分けて交付", dur=4.8),
        nn("1月1日の時点で\n決まるってことは……", BOARD, se="kon"),
        ss("1月1日に中道は\nまだ大きな党だった", BOARD, se="pi"),
        ss("だから1年分は\n約23億3881万円", MONEY, se="price_display"),
        close(MONEY, "@react", "ニュース猫", "23億！？", se=["explosion_dokaan"]),
        card("e04_money", "4月・7月で　約11億6940万円が交付ずみ", dur=4.8, b=MONEY),
        card("e04_money", "のこり　10月・12月で　約11億6940万円", dur=4.8, b=MONEY),
        # ---- 3b. そもそもなぜ税金で？ ----
        nn("そもそも\nなんで政党に\n税金を配るの？", HALL, se="question_hatena_maou"),
        ss("始まりは1990年代の\n政治とお金の\n事件がきっかけ", HALL, se="page_turn_01"),
        ss("企業のお金に\n頼りすぎない政治に\nしようとした", HALL, se="pi"),
        ex(HALL, "1994年の政治改革関連法で\n政党助成制度ができ\n1995年から交付が始まった", dur=4.4),
        ss("金額は\n国勢調査の人口 × 250円", MONEY, se="price_display"),
        ss("2025年分は\n10の党に\nあわせて約315億円", MONEY, se="pi"),
        close(MONEY, "@react", "ニュース猫", "毎年300億円以上！？", se=["explosion_chudoon"]),
        ss("ちなみに共産党は\n“制度に反対”として\n受け取っていない", HALL, se="kon"),
        nn("受け取らない党も\nあるんだ……", HALL, se="pikon"),
        ss("税金だからこそ\n使い道は毎年\n報告書で公開される", PAPERS, se="pinpoon_note"),
        # ---- 4. なぜ1人で受け取れる？ ----
        chap("なぜ1人で\n受け取れる？", se="doon_heavy"),
        nn("みんな離党したなら\n新しい党に\nお金も移せば？", TL, se="question_hatena_maou"),
        ss("それができない\n離党した議員は\nのこりの交付金を持っていけない", TL, se="hyoshigi_01"),
        ss("新しい党は\n1月1日にはなかった\nだから今年は交付金ゼロ", TL, se="pi"),
        card("e03_split", "分派＝党を解散せずに残し、議員が外に出ていく形", dur=5.0),
        nn("党を1人で残せば\n交付金は止まらない\nってこと？", OFFICE1, se="kon"),
        ss("報道では\nそういう形だと\n説明されている", OFFICE1, se="pi"),
        close(OFFICE1, "@react", "ニュース猫", "そんなこと\nできるの！？", se=["game_aceattorney_desk_slam"]),
        ss("今のルールでは\n違法ではない", OFFICE1, se="kon"),
        ss("ただ\n“議員1人の党に億単位”は\n多くの人が想定していなかった", OFFICE1, se="pi"),
        # ---- 5. 党の説明 ----
        chap("党の説明", se="page_turn_02", bgm={"file": AM223, "gain": -4, "fade": 0.6}),
        card("e05_reason", "衆院選の経費のうち　交付金で払う分は約20億円", dur=5.0, b=PAPERS),
        card("e05_reason", "民間の業者に　分割で払う契約になっている", dur=4.8, b=PAPERS),
        card("e05_reason", "支払いは「半分も終わっていない」", dur=4.6, b=PAPERS),
        card("e05_reason", "後継の新党には　交付金は入らない", dur=4.6, b=PAPERS),
        nn("選挙で使ったお金の\nツケが残ってる\nってこと？", PAPERS, se="kon"),
        ss("党の説明はそう\nポスターや広告などを\n作った業者がいる", PAPERS, se="pi"),
        nn("業者さんに\n払わないわけには\nいかないか……", PAPERS, se="kon"),
        ss("そこは\n筋が通っている\nという見方もある", PAPERS, se="pikon"),
        nn("でもさ\n選挙で負けたのに\nそんなに使ってたの？", PAPERS, se="question_mark_pop_confused_huh"),
        ss("選挙の経費は\n勝っても負けても\nかかる", PAPERS, se="kon"),
        ss("候補者が多い党ほど\nポスターや宣伝の\nお金もふくらむ", PAPERS, se="pi"),
        pic("p3_hashina_pose", "中道で幹事長を務めた　階猛氏（いまは民主改革の会の幹事長）", dur=4.2, se="page_turn_01"),
        pic("p2_hashina_talk", "階氏（要旨）「残務整理を進めるうえで必要」\n「負い目を感じなくてはいけないものではない」", dur=5.0),
        pic("p2_hashina_talk", "「最善策だったと考えているが\n批判は甘んじて受けざるを得ない」（要旨）", dur=5.0, se="page_turn_01"),
        # ---- 6. 批判の声 ----
        chap("批判の声", se="doon_heavy", bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        org(MEETING, "公明党", "西田 幹事長（要旨）\n“国民の血税\n使い道をしっかり示して”", se="page_turn_01", dur=4.4),
        org(MEETING, "日本維新の会", "吉村 代表（要旨）\n“1人しか残っていないのに\n受け取るべきではない”", se="page_turn_01", dur=4.4),
        org(MEETING, "与党", "与党からは\n“論理のすり替えだ”\nとの声も（報道）", se="page_turn_02", dur=4.0),
        nn("元の仲間の公明党も\n注文をつけてる……", MEETING, se="kon"),
        card("e06_voices", "政治学者の岩井奉信氏は「相当、使い道を説明する必要がある」と指摘", dur=5.4),
        org(V_PHONE_W, "世論調査", "産経・FNN世論調査\n（10月17・18日）", se="page_turn_01", dur=3.4),
        card("e07_poll", "中道の交付金の受け取りに「納得できない」74.0%", dur=5.4, se="doon_heavy"),
        close(V_HANDS, "@react", "ニュース猫", "4人に3人が\n納得できない！", se=["explosion_chudoon"]),
        ss("“党が解体したのに\n税金を受け取る”\nそこに違和感がある", V_HANDS, se="pi"),
        nn("ほかの党を\n“お金の問題”で批判してた\nのに……って声もある", V_HANDS, se="kon"),
        ss("それはSNSの声な\n事実と意見は\n分けて見よう", V_HANDS, se="tsukkomi_bishi"),
        # ---- 7. 何が問題？ ----
        chap("何が問題？", se="quiz_question_02", bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        ss("ポイントは3つ", BOARD, se="pikon"),
        ss("①　1月1日で1年分が\n決まってしまうルール\n途中で党が消えても止まらない", BOARD, se="pi"),
        ss("②　使い道が\n本当に選挙の支払いだけか\n外から見えにくい", BOARD, se="pi"),
        ss("③　議員1人で\n億単位のお金を\n管理すること", BOARD, se="pi"),
        nn("ルールの穴って\nこと？", BOARD, se="question_mark_pop_confused_huh"),
        ss("“想定外の使われ方”\nとも言える\n制度の見直しを求める声も出てる", BOARD, se="kon"),
        nn("じゃあ\n12月分も……？", MONEY, se="kon"),
        ss("今のルールのままなら\n12月分も\n交付される見込み", MONEY, se="pi"),
        close(MONEY, "@react", "ニュース猫", "合わせて\n約11億7000万円！？", se=["explosion_dokaan"], sting=STING),
        ss("だからこそ\n何に使ったかを\n細かく示すことが大事", PAPERS, se="tv_professional_poon"),
        ex(PAPERS, "政党交付金の使い道は\n毎年 報告書で公開される\n（使途等報告書）", dur=4.0),
        nn("報告書が出たら\nちゃんと見られる\nってことか", PAPERS, se="pikon"),
        # ---- 8. ネットの声 ----
        chap("ネットの声", se="whoosh_shu", dur=1.4, bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        net("@react", "議員1人で\n5億8000万円は\nさすがに無理がある", se="boing_01"),
        net("@react", "業者への支払いは\n払わないと\n業者がかわいそう", se="pi"),
        net("@react", "なら全部の支払い先と\n金額を\n公開してほしい", se="kon"),
        net("@react", "ルール上OKでも\n気持ちとしては\n納得できない", se="buzzer_wrong"),
        net("@react", "1月1日で1年分\nっていうルール自体を\n見直すべき", se="pi"),
        net("@react", "余ったら\nちゃんと国に\n返してほしい", se="kon"),
        net("sleepy_old_memories_cat", "結局いちばん損してるのは\n税金を払ってる\nわたしたち", se="tear_drop"),
        nn("みんな\n“説明して”って\n言ってるね", V_SHIBUYA, se="kon"),
        # ---- 9. まとめ ----
        dict(bg=bg(BOARD), inset={"card": pt("e08_points"), "box": (200, 60, 1720, 860)}, dur=6.0,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)],
             bgm={"file": MIRAI, "gain": -2, "fade": 0.8}, se="chiin_01"),
        ss("ルール上は受け取れる\nでも 納得してもらえるかは\n説明しだい", V_NIGHT, se="tv_professional_poon"),
        nn("12月の交付と\n使い道の報告\nちゃんと見ていこう", V_NIGHT, se="chirin"),
        dict(bg=bg(BOARD), card=pt("e10_ending"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


def cuts_full():
    return L.apply_fx(L.allocate(cuts_all(), max_use=4))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "24_chudo_full.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cuts = cuts_full()
    if sys.argv[1:] == ["--audio"]:
        R.remux_audio(cuts, out, out.replace(".mp4", "_a.mp4"))
        os.replace(out.replace(".mp4", "_a.mp4"), out)
        sys.exit()
    if len(sys.argv) > 1:
        a, b = (int(x) if x else None for x in sys.argv[1].split(":"))
        cuts = cuts[a:b]
    R.render(cuts, out, preview_dir=out.replace(".mp4", "_preview"))
