"""04_leak（個人情報、盗まれすぎ問題）のカット割り。原稿 scripts/04_leak.md。作りは 03 と同じ。

v2: 参考動画（ニャースインフォ）ふうの作り
  - 猫は2匹ずつ並べて掛け合い。足元に色つきの役名札（ニュース猫=赤、博識な猫=青、パパ猫=緑、ネットの声=紫）
  - セリフは画面上に白い縁取り文字。強調は赤い文字＋集中線＋画面の揺れ
  - 図は画面の真ん中に差し込み、両側に猫。下に説明の字幕
  - 事実の説明は「説明モード」（画面を灰色の小窓に縮めて、黒地に説明文）
  - 場面の区切りは黒い画面に小さな文字（「本題に入るその前に…」など）
  - 場面転換は白飛びなしのパッと切り替え＋シュッという音。BGMは前より大きめ

python3 catmeme/cuts_04_leak.py          → out/04_leak_full.mp4
python3 catmeme/cuts_04_leak.py --audio  → 音だけ作り直す
python3 catmeme/cuts_04_leak.py 0:10     → 先頭10カットだけ
"""
import os
import sys

import render as R

R.NYAS_STYLE = True     # 文字がポンと飛び出す
R.WHITE_DIP = 0.0       # 白飛びの転換はしない（パッと切り替え）
R.FG_DUCK = -9          # 猫の音・SEが鳴っている間のBGMの下げ幅（前は -20。参考動画はBGMが大きめ）

HERE = os.path.dirname(os.path.abspath(__file__))
BGS = [os.path.join(HERE, "backgrounds", d) for d in ("04_leak", "03_kodomo_nisa", "02_october", "01_todai")]   # 前の動画の背景も使い回す
PT = os.path.join(HERE, "parts", "04_leak")
BGM = os.path.join(HERE, "bgm")

PURPLE = os.path.join(BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")
COCOA = os.path.join(BGM, "星降る夜のホットココア.mp3")
MIRAI = os.path.join(BGM, "未来を創る君たちへ.mp3")
KAMI = os.path.join(BGM, "神の怒り.mp3")

NORA = os.path.join(BGM, "野良猫は宇宙を目指した.mp3")
NEWS, SAGE, PAPA, NET = (215, 35, 35), (40, 90, 200), (35, 140, 65), (120, 50, 170)
HACK = (30, 30, 30)
ROLE = {"ニュース猫": NEWS, "博識な猫": SAGE, "パパ猫": PAPA, "ネットの声": NET, "ハッカー猫": HACK}


def bg(n):
    for d in BGS:
        p = os.path.join(d, n + ".png")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(n)


def pt(n):
    return os.path.join(PT, n + ".png")


def cat(a, role, x, h=640, bottom=1010, **kw):
    return dict(a=a, x=x, h=h, bottom=bottom, label=role, label_color=ROLE[role], label_size=kw.pop("label_size", 66), **kw)


def duo(b, left, right, say, who="L", **kw):
    """2匹並べての掛け合い。left/right = (素材, 役名)。who はしゃべる側（L/R）。しゃべっていない方の猫の音は消す。"""
    cats = [cat(left[0], left[1], 500, h=760, bottom=1040, flip=kw.pop("lflip", False), mute=who != "L"),
            cat(right[0], right[1], 1430, h=760, bottom=1040, flip=kw.pop("rflip", False), mute=who != "R")]
    return dict(bg=bg(b), cats=cats, say=say, text_top=True, **kw)


def solo(b, a, role, say, side="L", **kw):
    """1匹だけ。セリフは猫の反対側。"""
    x = 500 if side == "L" else 1420
    return dict(bg=bg(b), cats=[cat(a, role, x, h=kw.pop("h", 720), flip=kw.pop("flip", False))], say=say, **kw)


def close(b, a, role, say, red=True, **kw):
    """驚きのアップ。赤い文字＋集中線＋揺れ。"""
    c = cat(a, role, kw.pop("x", 960), h=kw.pop("h", 760), bottom=1060, float=True, flip=kw.pop("flip", False))
    return dict(bg=bg(b), cats=[c], say=say, text_top=True, say_style="red" if red else None,
                fx=["lines", "shake"], **kw)


def dia(c, sub, b="bg03_blackboard", left=None, right=None, **kw):
    """図を大きく差し込み、右下に小さめの猫1匹、下に説明の字幕。"""
    who = right or left
    cats = [cat(who[0], who[1], 1790, h=400, bottom=1060, float=True, label_size=54)] if who else []
    return dict(bg=bg(b), inset={"card": pt(c), "box": (40, 15, 1660, 815)}, cats=cats, sub=sub,
                sub_box=(60, 820, 1600, 1070), sub_size=70, **kw)


def expl(b, cats, say, text, **kw):
    """説明モード：直前の場面を灰色の小窓にして、黒地に説明文。"""
    return dict(bg=bg(b), cats=cats, say=say, text_top=True, explain=text, no_pop=True, **kw)


def chap(text, **kw):
    return dict(bg=None, chapter=text, chapter_size=140, dur=kw.pop("dur", 1.8), se=kw.pop("se", "whoosh_shu"), **kw)


def place(b, text, **kw):
    return dict(bg=bg(b), place=text, dur=kw.pop("dur", 1.4), fx=["zoom"], **kw)


def net(a, say, tag="ネットの声", **kw):
    c = cat(a, "ネットの声", 500, h=700)
    c["label"] = tag
    return dict(bg=bg("bg09_sns"), cats=[c], say=say, **kw)


def pops(*items):
    """時間差で出る文字。items = (秒, 文字, (x0,y0,x1,y1)[, "red"])。それぞれポンの音つき。"""
    out = []
    for it in items:
        out.append({"t": it[0], "text": it[1], "box": it[2], "dur": 9, "size": 100, "style": it[3] if len(it) > 3 else None,
                    "align": "left"})
    return out


def pop_se(*ts, f="pop"):
    return [{"f": f, "at": t, "gain": -6} for t in ts]


# 掛け合いの組み合わせ（同じ素材が続けて出すぎないよう、場面ごとに猫を変える）
N, S, H_ = ("@react", "ニュース猫"), ("@calm", "博識な猫"), ("@hack", "ハッカー猫")


def nn(say, b="bg02_room", **kw):
    """ニュース猫がしゃべる（左）、博識な猫が聞く（右）。"""
    return duo(b, N, S, say, who="L", **kw)


def ss(say, b="bg02_room", **kw):
    """博識な猫がしゃべる（右）。"""
    return duo(b, N, S, say, who="R", **kw)


def hk(say, **kw):
    """ハッカー猫のひとり語り（暗い部屋）。"""
    return solo(kw.pop("b", "bg23_hacker_room"), "@hack", "ハッカー猫", say, side=kw.pop("side", "R"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=3.6, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- 1. 何が起きているか ----
        dict(bg=bg("bg26_phone_alert"), card=pt("e01_title"), dur=2.6, bgm={"file": PURPLE, "gain": -2}, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        chap("話は2026年10月5日…"),
        dict(bg=bg("bg22_yakiniku"), sub="焼肉きんぐの公式アプリで\n約1,078万件の会員情報が\n漏えいのおそれ",
             cats=[cat("@calm", "博識な猫", 470, h=640)], se="doon_movie", fx=["lines"]),
        close("bg22_yakiniku", "@react", "ニュース猫", "1,000万件！？", se=["explosion_chudoon"]),
        ss("会員番号・名前・\nメール・電話番号な", "bg22_yakiniku", se="page_turn_01"),
        expl("bg22_yakiniku", [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "",
             "パスワード・生年月日・カード情報は\n漏れていないと発表されています", dur=3.2, se="pinpon_notice"),
        nn("焼肉食べたかった\nだけなのに……", "bg22_yakiniku", se="tear_drop"),
        ss("しかもこれ\n最近ずっと続いてんのよ", se="quiz_den"),
        chap("9月末から　ほぼ毎日…", se="doon_heavy"),
        dia("e02_list", "10月だけでも　焼肉きんぐ・佐川急便", right=S, se="xylophone_transition"),
        dia("e02_list", "タイムズカーは　免許証などの書類も約160万件　漏えいのおそれ", right=S, se="pc_warning"),
        dia("e02b_list", "9月にも　大きな発表が続いた", right=S, se="card_flip"),
        dia("e02b_list", "（京王電鉄はランサムウェア被害。情報の漏えいは確認されていない）", right=S, se="card_place"),
        close("bg24_server_room", "@react", "ニュース猫", "ちょっと待って\nデジタル庁も！？", se=["explosion_chudoon"]),
        close("bg24_server_room", "@react", "ニュース猫", "日本のデジタル戦略を\n担うところが！？", flip=True,
              se=["game_aceattorney_desk_slam"]),
        dict(bg=bg("bg24_server_room"), sub="デジタル庁が運用する「GSS」\n（省庁の職員が使う共通のIT環境）で\n約24.6万件　漏えいのおそれ",
             cats=[cat("@calm", "博識な猫", 470, h=640)], se="pc_warning"),
        ss("国の機関だって\n例外じゃない\nってことな", "bg24_server_room", se="hyoshigi_01"),
        nn("多すぎて\nもう何がなんだか", se="spring_byoin"),
        nn("全部足したら\n日本の人口超えるんじゃ……", se="question_hatena_maou"),
        ss("同じ人が何社にも\n登録してるから\n足しちゃダメなやつな", se="tsukkomi_bishi"),
        close("bg20_counter", "@react", "ニュース猫", "レンタカー予約しただけで\n免許証まで！？", se=["game_mgs_alert"]),
        dia("e02c_times", "タイムズカーで　何が漏れたかもしれないのか", "bg20_counter", right=S, se="page_turn_01"),
        dia("e02c_times", "約160万件は　運転免許証などの“本人確認書類”の情報", "bg20_counter", right=S, se="pc_warning"),
        ss("免許証には\n名前・住所・生年月日・\n顔写真まで載ってるからな", "bg20_counter", se="hyoshigi_02"),
        # ---- 2. なぜ起きているか ----
        chap("なんでこんなに　盗まれるの？", se="quiz_question_01", bgm={"file": NORA, "gain": -2}),
        hk("ふっふっふ……\n入口なんて\nいくらでもあるのよ", se="anime_broly_dedeen"),
        dia("e03_cause", "9月に原因まで公表された10件を見ると", "bg24_server_room", right=S, se="xylophone_transition"),
        dia("e03_cause", "いちばん多いのは　ネットにつながった機器やシステムの「弱点」をつかれたケース", "bg24_server_room", right=S, se="doon_heavy"),
        dia("e03c_weak", "弱点＝プログラムのミスや古い設定など　“直っていない欠陥”", "bg24_server_room", right=S, se="page_turn_02"),
        dia("e03d_weak_ex", "9月の発表では　こんな所の弱点がねらわれた", "bg24_server_room", right=S, se="card_flip"),
        dia("e03b_words", "むずかしい言葉は　こう考えるとわかりやすい", "bg24_server_room", right=S, se="idea_newtype_01"),
        nn("つまり会社の出入り口に\nスキマがあって\nそこから入られたってことか", "bg24_server_room", se="kon"),
        ss("偽のログイン画面に誘う\n「フィッシング」で\nメールを乗っ取られた例も", "bg24_server_room", se="pi"),
        hk("ポチッと押してくれれば\nこっちのもん", se="game_zelda_item_get"),
        expl("bg25_office_desk", [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "",
             "実は　攻撃者がいない漏えいもある", dur=2.6, se="doon_movie"),
        dia("e03_cause", "TOPPAN　損保ジャパン契約者17万7,426名分を　ドラッグ&ドロップの誤りで同業他社へ送付", "bg25_office_desk",
            right=S, se="glass_break_01"),
        dia("e03_cause", "RIZAP　約2万人分を外部の生成AIに入力／愛知県のサイトで8年間まちがって掲載", "bg25_office_desk",
            right=S, se="boing_fail"),
        close("bg25_office_desk", "@react", "ニュース猫", "ハッキングより\nドラッグ&ドロップのほうが怖い", se=["shock_piano"]),
        ss("人間のうっかりは\nどこにでもあるからな", "bg25_office_desk", se="taiko_kaka"),
        # ---- 3. なぜ今 連発しているのか ----
        chap("なんで今　こんなに連発？", se="quiz_question_02"),
        dia("e04_ransom", "2026年上半期は123件　前の年より増えて　半期として過去最多（警察庁）", right=S,
            se="doon_heavy"),
        dia("e04_ransom", "ランサムウェアの侵入口は　約5割がVPN機器", right=S, se="pc_warning"),
        ss("ランサムウェアは\n“貸し出し”もされてて\n技術がなくても攻撃できる", se="cursor_move_01"),
        close("bg02_room", "@react", "ニュース猫", "悪いことの\nサブスク！？", se=["game_smash_challenger"]),
        ss("IPAの「10大脅威」に\nAIをめぐるリスクが\n初めて入った", se="page_turn_01"),
        expl("bg23_hacker_room", [cat("@hack", "ハッカー猫", 960, h=700)], "",
             "9月10〜15日の5日間　人間が指揮したAIが\nほぼ自動で100以上の組織を攻撃し　30以上に侵入\n"
             "（海外の報告。日本の件と同じ犯人という根拠はない）", dur=4.6, se="game_undertale_encounter"),
        close("bg23_hacker_room", "@react", "ニュース猫", "AIが\nハッカーやってんの！？",
              se=["explosion_dokaan"], sting={"file": KAMI, "len": 4.0, "gain": -16}),
        dict(bg=bg("bg23_hacker_room"), sub="かかった費用は\n約8,000ドル", cats=[cat("@calm", "博識な猫", 470, h=640)],
             se="cymbal_light_maou"),
        hk("安い！\n早い！\nうまい！", se="game_mario_1up"),
        ss("ただ“件数が\nめちゃくちゃ増えた”とは\n言い切れないんだよな", se="hyoshigi_01"),
        dia("e04b_big", "上場企業の漏えい事故は　2025年に減った　でも100万人超の大型は　2件→6件", right=S,
            se="card_flip"),
        dia("e04b_big", "法律が変わり「漏えいのおそれ」でも報告が義務に　→　発表が増えて見える面も", right=S,
            se="pinpoon_note"),
        nn("大きいのが増えて\n目立ってるってことか", se="pikon"),
        chap("ネットでは　こんな声も…\n（根拠は未確認）", se="whoosh_shu", dur=2.2),
        net("@react", "AIで誰でも\n大量に攻撃\nできるように\nなったから", "ネットの声", se="pi"),
        net("@react", "日本企業は\nセキュリティに\nお金をかけない", "ネットの声", se="boon"),
        net("@react", "古いシステムと\nITに弱い経営陣", "ネットの声", se="kote"),
        net("@react", "もう全員の情報\n漏れ済み\n今さら", "ネットの声", se="silly"),
        ss("どれも“という声”な\n証拠はまだない", se="tsukkomi_bashi"),
        # ---- 4. 盗まれると何が起きるのか ----
        chap("盗まれると　何が起きる？", se="doon_heavy", bgm={"file": COCOA, "gain": -2}),
        dict(bg=bg("bg26_phone_alert"), sub="今のところ多くの会社が\n「悪用は確認されていない」\nと発表",
             cats=[cat("@calm", "博識な猫", 470, h=640)], se="pinpon_notice"),
        nn("じゃあ\nセーフ？", "bg26_phone_alert", se="question_hatena_maou"),
        ss("心配なのは\nこの先な", "bg26_phone_alert", se="shock_piano"),
        dia("e05_risk", "名前・電話・メールがそろうと　本物っぽい偽SMS・偽メールが届く", "bg26_phone_alert", right=S,
            se="xylophone_transition"),
        dia("e05_risk", "送り主・届け先や　免許証の画像は　詐欺やなりすましに使われるおそれ", "bg26_phone_alert", right=S,
            se="pc_warning"),
        chap("特にこわいのが　免許証の画像", se="doon_heavy"),
        dia("e05b_license", "免許証の画像があれば　あなたになりすまして　クレカやローンを申し込めてしまうおそれ", "bg20_counter",
            right=S, se="pc_warning"),
        dia("e05b_license", "知らないうちにキャッシング　→　返されずに延滞　→　信用情報に記録", "bg20_counter",
            right=S, se="doon_movie"),
        close("bg20_counter", "@react", "ニュース猫", "知らないうちに\n借金して\nブラックリスト入り！？",
              se=["explosion_dokaan"]),
        dia("e05b_license", "そうなると　家や車のローン・クレカの審査に　通らなくなることも", "bg20_counter", right=S,
            se="game_dq_miss"),
        hk("ローンの審査？\nお気の毒さま〜", b="bg23_hacker_room", se="anime_shinchan_taraan"),
        ss("実際は　審査で\n電話や口座の確認もあるから\n画像だけで必ず通る\nわけじゃない", "bg20_counter", se="pinpon_notice"),
        expl("bg20_counter", [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "",
             "免許証が漏れたかもしれない時は　信用情報機関（CIC・JICC・全銀協）に\n"
             "「本人申告」を登録すると　なりすましの契約を防ぎやすくなります", dur=4.6, se="pinpoon_correct"),
        nn("信用情報って\n自分で\n見られるのか", "bg20_counter", se="pikon"),
        ss("開示を申し込めば\n見られるぞ\n身に覚えのない契約が\nないかチェックな", "bg20_counter", se="idea_newtype_01"),
        hk("お荷物の\nお届けに\nあがりました〜（偽）", b="bg26_phone_alert", se="cursor_move_02"),
        hk("お詫びの\nクーポンです〜（偽）", b="bg26_phone_alert", side="L", se="shine_kira_01"),
        close("bg26_phone_alert", "@react", "ニュース猫", "お詫びクーポンが来たら\nそれが一番あやしい！",
              se=["tv_gakitsuka_dedeen"]),
        ss("パスワードの使い回しは\n別のサービスにも\n次々ログインされる", se="pi"),
        nn("……全部\n同じパスワードだわ", se="tv_dokkiri_tettere"),
        close("bg02_room", "@calm", "博識な猫", "それ一番\nやばいやつ", se=["game_aceattorney_desk_slam"]),
        # ---- 5. 対策 ----
        chap("じゃあ　どうすればいい？", se="quiz_question_01"),
        dia("e06_todo", "「お詫び」メールのリンクは踏まない　公式アプリ・ブックマークから確認", right=S,
            se="pinpoon_correct"),
        dia("e06_todo", "使い回しのパスワードを変える　二段階認証・パスキーを入れる", right=S, se="pinpoon_correct"),
        dia("e06_todo", "使っていないアカウントは退会　身に覚えのない契約・郵便に注意", right=S, se="pinpoon_correct"),
        nn("使ってないアカウント\nめっちゃある……", se="deflate_hyororo"),
        ss("持ってるだけで\n漏れる可能性\nあるからな", se="hyoshigi_02"),
        hk("二段階認証……\nだと……", se="game_dq_miss"),
        # ---- 6. ネットの声 ----
        chap("ネットの声", dur=1.4),
        net("@react", "漏れてない\n個人情報のほうが\nレア", "ネットの声", se="kon"),
        net("@react", "焼肉食べに行った\nだけで\nメアドと電話番号が", "ネットの声", se="tear_drop"),
        net("@react", "“二次被害は\n確認されていません”\n聞き飽きた", "ネットの声", se="silly"),
        net("@react", "AIで攻撃し放題なのに\n守る側はまだ\n紙とハンコ", "ネットの声", se="boing_01"),
        net("@react", "補償なし・\nメール1通で終わり？", "ネットの声", se="buzzer_wrong"),
        # ---- 7. まとめ ----
        dict(bg=bg("bg03_blackboard"), inset={"card": pt("e07_matome"), "box": (200, 60, 1720, 860)}, dur=4.6,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)],
             bgm={"file": MIRAI, "gain": -2, "fade": 0.8}, se="chiin_01"),
        ss("“漏れない”じゃなくて\n“漏れても被害にならない”\nように守るのが今のやり方", dur=3.6, se="tv_professional_poon"),
        nn("とりあえず\nパスワード\n変えてくるわ", se="pikoon_retro"),
        dict(bg=bg("bg03_blackboard"), card=pt("e08_ending"), dur=3.0, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
    ]


# 猫ミーム素材を途中で切らずに最後まで流すカット（切る秒は assets/play.json）
FULL = []


def apply_fx(cuts):
    for c in cuts:
        k = " ".join(str(c.get(x) or "") for x in ("say", "sub"))
        if any(f in k for f in FULL) and c.get("cats"):
            c["cats"][0]["full"] = True
            cfg = R.ASSET_PLAY.get(c["cats"][0]["a"], {})
            if cfg.get("until"):
                c["cats"][0]["until"] = cfg["until"]
    # 図が飛び出すのは、その図が動画で初めて出る時だけ（同じ表がポンポン出直さないように）
    seen = set()
    for c in cuts:
        card = (c.get("inset") or {}).get("card")
        if card:
            if card in seen:
                c["inset_still"] = True
            seen.add(card)
    # 場所（背景）が変わるカットの頭にシュッという音（すでに付いている音とは重ねる）
    prev = None
    for c in cuts:
        if c.get("bg") != prev and prev is not None:
            se = c.get("se")
            lst = [] if not se else ([se] if isinstance(se, (str, dict)) else list(se))
            if not any((s if isinstance(s, str) else s.get("f")) == "whoosh_shu" for s in lst):
                lst = [{"f": "whoosh_shu", "gain": -10}] + lst
            c["se"] = lst
        prev = c.get("bg")
    return cuts


# 猫ミームの自動の割り当て（"@react" などの所）。役名はそのままで、セリフごとに素材を入れ替える。
# 同じ素材は1本で3回まで、前後2場面には同じ素材を出さない。曲つき・長さ指定の素材は自動では選ばない
POOLS = {
    "react": ["surprise_big_pupils_cat", "huh_huh_cat", "realize_wet_cat_stare", "peek_what_happen_cat", "weird_meowing_cat",
              "blank_black_cat_zoning_out", "glare_disgusted_cat", "spit_not_my_taste_cat", "sulk_hungry_cat",
              "angry_cat_hits_cat", "fight_cat_fight", "rage_talking_cat", "leave_cat_leaves_home", "sad_banana_cat_cry",
              "spin_spinning_cat", "mock_swinging_cat", "sleepy_sleepy_cat", "sleep_sleeping_cat", "angry_aiming_cat",
              "tense_two_cats_face_off"],
    "calm": ["itchy_kitten_butt", "calm_black_face_sheep", "work_typing_cat", "think_bike_front_seat_cat",
             "call_customer_service_cat", "cocky_dj_cat", "showoff_gojo_cosplay_cat", "drive_driving_cat",
             "drive_monkey_golf_cart", "ride_kitten_bike", "slack_nail_filing_cat", "eat_crunchy_cat_luna", "eat_pop_cat",
             "taunt_cat_and_scared_dog", "wakeup_dog_hits_bowl", "sleepy_old_memories_cat", "listen_dancing_dog",
             "excited_hodomoe_city_cat"],
    "papa": ["shady_dancing_man", "dance_wild_dog", "dance_edm_cat", "calmdown_dancing_cat", "dance_trending_cat",
             "dance_wop_cat", "happy_girlfriend_dance_cat", "laugh_laughing_dog", "dance_koto_nai_cat"],
}
POOLS["hack"] = ["angry_aiming_cat", "angry_shooting_cat", "cocky_dj_cat", "taunt_cat_and_scared_dog", "shady_dancing_man",
                 "showoff_gojo_cosplay_cat", "dance_wild_dog", "laugh_laughing_dog", "dance_edm_cat"]
FALLBACK = {"react": ["papa", "calm"], "calm": ["papa", "react"], "papa": ["calm", "react"], "hack": ["papa", "calm"]}


def allocate(cuts, max_use=3, gap=2):
    count, last = {}, {}
    for i, c in enumerate(cuts):   # 指定ずみの素材を先に数える
        for k in c.get("cats", []):
            if not k["a"].startswith("@"):
                count[k["a"]] = count.get(k["a"], 0) + 1
    fixed_at = {}
    for i, c in enumerate(cuts):
        for k in c.get("cats", []):
            if not k["a"].startswith("@"):
                fixed_at.setdefault(k["a"], []).append(i)
    for i, c in enumerate(cuts):
        here = {k["a"] for k in c.get("cats", [])}
        for k in c.get("cats", []):
            if not k["a"].startswith("@"):
                last[k["a"]] = i
                continue
            pool = k["a"][1:]
            def ok(a):
                near_fixed = any(abs(j - i) <= gap for j in fixed_at.get(a, []))
                return (count.get(a, 0) < max_use and a not in here and i - last.get(a, -99) > gap and not near_fixed)
            for name in [pool] + FALLBACK[pool]:
                cands = [a for a in POOLS[name] if ok(a)]
                if cands:
                    break
            else:
                raise RuntimeError(f"cut {i}: 猫ミームが足りない")
            a = min(cands, key=lambda a: (count.get(a, 0), last.get(a, -99)))
            k["a"] = a
            count[a] = count.get(a, 0) + 1
            last[a] = i
            here.add(a)
    return cuts


def cuts_full():
    return apply_fx(allocate(cuts_all()))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "04_leak_full.mp4")
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

