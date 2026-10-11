"""10_idcf（IDCFクラウドのランサムウェア攻撃）のカット割り。原稿 scripts/10_idcf.md（v2）。作りは 04〜06 と同じ。

python3 catmeme/cuts_10_idcf.py          → out/10_idcf_full.mp4
python3 catmeme/cuts_10_idcf.py --audio  → 音だけ作り直す
python3 catmeme/cuts_10_idcf.py 0:10     → 先頭10カットだけ

原稿のルール：
- 真偽が分からない話（7時間気づかなかった・ひたすら再起動・被害の数字）は「ハッカーは主張している／と言われている」を付けるだけ
- 被害を受けた会社・自治体・運用担当者をバカにしない（運用の猫は「深夜に呼び出されて必死な人」）。笑いはハッカーの上から目線とニュース猫のリアクション
- 攻撃のやり方は説明しない。攻撃者のメッセージ画像は使わず、要旨をカードで再現
- 再現パートの間は、画面のすみに「※ハッカーの主張・言われていることをもとにした再現」の札
"""
import os
import sys

import cuts_04_leak as L
import render as R

HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("10_idcf", "04_leak", "03_kodomo_nisa", "02_october", "01_todai")]
L.PT = os.path.join(HERE, "parts", "10_idcf")
OPS = "運用の猫"
L.ROLE[OPS] = (35, 140, 65)
pt, cat, duo, solo, close, dia, expl, chap, net, nn, ss = L.pt, L.cat, L.duo, L.solo, L.close, L.dia, L.expl, L.chap, L.net, L.nn, L.ss
bg = L.bg
N, S, HK = L.N, L.S, L.H_
O = ("@ops", OPS)
PURPLE, COCOA, MIRAI, KAMI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.KAMI, L.NORA
# 原稿の BGM 表は 4〜5 に「やる気のないダースベイダーのテーマ」だが、市販曲で使用不可（bgm/README.md）なので「野良猫は宇宙を目指した」に差し替え
AM223 = os.path.join(L.BGM, "2_23_AM.mp3")

# 後から追加した素材も使う（10/11 追加分）
L.POOLS["react"] += ["stare_standing_marmot", "flip_emo_cat_hair"]
L.POOLS["calm"] += ["lick_talking_goat", "eat_chips_cat", "stand_real_sheep"]
L.POOLS["hack"] += ["rizz_cat_rizz", "dance_white_dog"]
# 運用の猫：深夜に呼び出されて必死に対応している人（バカにしない）
L.POOLS["ops"] = ["work_typing_cat", "work_dog_staring_computer", "call_customer_service_cat", "sad_black_dog",
                  "sleepy_sleepy_cat", "wakeup_dog_hits_bowl", "blank_black_cat_zoning_out", "think_bike_front_seat_cat"]
L.FALLBACK["ops"] = ["calm", "react"]
SERVER, HACKER = "bg24_server_room", "bg23_hacker_room"


def re(c):
    """再現パートの札を付ける。"""
    c["layers"] = c.get("layers", []) + [pt("badge")]
    return c


def hk(say, **kw):
    return re(L.solo(kw.pop("b", HACKER), "@hack", "ハッカー猫", say, side=kw.pop("side", "R"), **kw))


def op(say, **kw):
    return re(L.solo(kw.pop("b", SERVER), "@ops", OPS, say, side=kw.pop("side", "L"), **kw))


def vs(say, who, **kw):
    """運用の猫（左）とハッカー猫（右）。who=L なら運用の猫、R ならハッカー猫がしゃべる。"""
    return re(duo(kw.pop("b", SERVER), O, HK, say, who=who, **kw))


def two(b, sub, **kw):
    """2匹を並べて、上に説明の字幕。"""
    return dict(bg=bg(b), cats=[cat("@react", "ニュース猫", 500, h=700), cat("@calm", "博識な猫", 1430, h=700)], say=sub,
                text_top=True, **kw)


def one(b, sub, **kw):
    return dict(bg=bg(b), sub=sub, cats=[cat("@calm", "博識な猫", 470, h=640)], **kw)


def ex(b, text, **kw):
    return expl(b, [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "", text, dur=kw.pop("dur", 3.4), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=4.6, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- 1. つかみ ----
        dict(bg=bg(SERVER), sub="2026年10月7日\n午前3時40分ごろ", cats=[cat("@calm", "博識な猫", 470, h=640)], se="doon_movie",
             sting={"file": KAMI, "len": 4.0, "gain": -14}),
        one(SERVER, "ある「クラウド」が\n止まった", se="pc_warning"),
        one(SERVER, "影響を受けたのは\n495の企業と自治体", se="doon_heavy"),
        close(SERVER, "@react", "ニュース猫", "よんひゃく……\nきゅうじゅうご！？", se=["explosion_chudoon"]),
        one("bg26_phone_alert", "県のホームページ\n会社の物流システム\nスマホの見守りサービス……", se="pi"),
        one(HACKER, "そして管理画面には\nハッカーのメッセージが\n表示されていた", se="rumble_gogogo",
            bgm={"file": PURPLE, "gain": -4}),
        dia("e01_msg", "管理画面に出たメッセージ（要旨を再現）", HACKER, right=N, dur=4.4, se="anime_yugioh_summon_powerful_appearance"),
        nn("映画でしか\n聞いたことない\nセリフ！", HACKER, se="boing_01"),
        one(HACKER, "ハッカーは\nこう主張している", se="kon"),
        dia("e01_claim", "ハッカーの主張（確認されていない）", HACKER, right=N, dur=4.4, se="game_persona5_cutin_dramatic_entrance"),
        one(SERVER, "その間　運用チームは\nひたすらサーバーの再起動を\n繰り返していた　と言われている", dur=4.0, se="click_tap_select_button"),
        close(SERVER, "@react", "ニュース猫", "ハッカーに\n煽られながら\n再起動……！？", se=["explosion_dokaan"]),
        ss("ハッカー側からすると\n見られてないメッセージを\n置いてずっと待ってた\nことになる", SERVER, se="pikon"),
        nn("地獄の\n放置プレイじゃん", SERVER, se="tsukkomi_bishi"),
        dict(bg=bg("bg03_blackboard"), card=pt("e01_title"), dur=3.4, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        # ---- 2. そもそも「IDCFクラウド」って？ ----
        chap("そもそも何が止まったのか", se="doon_heavy"),
        two("bg25_office_desk", "IDCFクラウド\n＝ソフトバンクの子会社\n「IDCフロンティア」のクラウド", se="page_turn_01"),
        nn("クラウドって\nあのフワフワした\nやつでしょ", "bg25_office_desk", se="boing_02"),
        ss("フワフワしてない\n中身はデータセンターにある\n本物のサーバーだ", SERVER, se="tsukkomi_bishi"),
        dia("e02_mansion", "クラウド＝大きなマンション　企業や自治体＝部屋を借りている住人", right=S, se="card_flip"),
        ss("自分でサーバーを買うかわりに\n部屋を借りて\nホームページやシステムを置いてる", se="pikon"),
        nn("で、今回は？", se="question_mark_pop_confused_huh"),
        dia("e02_mansion", "管理室ごと乗っ取られて　部屋にカギをかけられた", right=S, se="doon_movie"),
        close("bg02_room", "@react", "ニュース猫", "住人ぜんぶ\n締め出し！？", se=["explosion_chudoon"]),
        dia("e02_affected", "影響を受けたのは　495の企業と自治体", right=N, dur=5.0, se="card_place"),
        nn("アイドルの\nメールまで\n止まってる……", se="chin_bell_failure_sad_ending"),
        # ---- 3. 何が起きたか（公式の発表） ----
        chap("7日に何が起きたのか…", se="doon_heavy"),
        dia("e03_tl1", "午前3時40分ごろ　東日本リージョン1で障害が発生", right=S, dur=4.4, se="xylophone_transition"),
        dia("e03_tl1", "朝には物流会社やJリーグのクラブ、茨城県にも影響が広がった", right=S, dur=4.4, se="card_flip"),
        dia("e03_tl1", "午後に第1報「不正アクセス」　夜に第2報「ランサムウェア攻撃」", right=S, dur=4.4, se="card_place"),
        nn("朝3時40分から\n夜8時まで……", se="tear_drop"),
        ss("“ランサムウェア”と\n発表されたのは夜\nそれまでは“障害”\n“不正アクセス”だった", se="pikon"),
        dia("e03_ransom", "データを人質にとって　身代金を要求するウイルス", right=S, se="pinpon_notice"),
        nn("データを人質にとる\n誘拐犯みたいな\nもんか", se="kon"),
        ss("そう\n4本目でもやったやつ", se="tv_professional_poon"),
        dia("e03_tl2", "8日の第3報：止まった仮想サーバーは　再起動できない", right=S, dur=4.4, se="xylophone_transition"),
        dia("e03_tl2", "4ゾーンのデータは取り出し・復元が困難　戻せるのは自分のバックアップからだけ", right=S, dur=4.8,
            se="pc_warning"),
        dia("e03_tl2", "警視庁と監督省庁に報告　9日の第4報ではソフトバンクと連携", right=S, dur=4.2, se="card_flip"),
        close("bg02_room", "@react", "ニュース猫", "え、データ\n戻らないの！？", se=["game_pokemon_super_effective_hit_big_damage"]),
        ss("そこが一番ヤバい\nあとで詳しくやる", se="hyoshigi_01"),
        # ---- 4. ハッカーのメッセージ ----
        chap("ハッカーは何と言っているのか", se="doon_heavy", bgm={"file": NORA, "gain": -4, "fade": 0.4}),
        one(HACKER, "SNSで広まった\n管理画面の画像", se="pi"),
        one(HACKER, "IDCFも\n「同じような画像を複数確認」\nと回答（内容は調査中）", se="page_turn_01"),
        hk("YOUR CLOUD\nIS OURS.", se="anime_yugioh_summon_powerful_appearance"),
        hk("東日本リージョン1を\n暗号化した\nかかった時間は\nたった7分", se="shine_kiraan_maou"),
        re(dia("e04_claims", "ハッカーが主張する被害（確認されていない）", HACKER, right=HK, dur=5.0, se="card_flip")),
        re(nn("ペタってなに？\nギガの上の上の……？", HACKER, se="question_hatena_maou")),
        re(ss("128ギガのスマホでいうと\nだいたい数万台分", HACKER, se="pikon")),
        re(close(HACKER, "@react", "ニュース猫", "スケールが\nでかすぎる", se=["explosion_dokaan"])),
        ex(HACKER, "数字はすべて　ハッカーの主張\nIDCFは「調査中」としている", se="pinpon_notice"),
        # ---- 5. 「7時間気づいていない」 ----
        chap("そして、あの煽り", se="doon_heavy"),
        hk("午前3時から\nすべての保管庫に\n“回復のご案内”を\n225個置いてやった", se="cursor_move_01"),
        hk("お前たちが\n異変に気づいたのは\n4時25分だな", se="shine_kira_01"),
        re(one(SERVER, "午前3時40分ごろ\n障害発生（公式の発表）", se="pinpon_notice")),
        op("（深夜に電話で起こされて）\nサーバーが……\n止まってる……", se="aircon_beep"),
        op("とりあえず\n再起動……", se="click_tap_select_button"),
        op("……動かない\nもう一回……", se="click_tap_select_button"),
        re(one(SERVER, "運用チームは\nひたすら再起動を繰り返していた\nと言われている", se="pi")),
        vs("いや、\nメッセージ見て？", "R", se="question_mark_pop_confused_huh"),
        vs("再起動……", "L", se="click_tap_select_button"),
        vs("いや、\n見て？？", "R", se="tsukkomi_bashi", fx=["shake"]),
        re(one(HACKER, "そして\nハッカーは主張する", se="kon")),
        hk("それから7時間\n仮想マシンをいじってるのに\nまだオレのメッセージを\n見つけていない", dur=3.6, se="game_yoshi_detteiu_so_what_bored"),
        hk("ファイルの中の時計は\n本物だぞ", se="cuckoo_clock"),
        re(dia("e05_claim2", "ハッカーの主張（確認されていない）", HACKER, right=N, dur=4.0, se="card_place")),
        nn("ハッカーの方が\nしびれ切らしてるの草", se="silly"),
        nn("てか“時計”って\n期限ってこと？", se="question_hatena_maou"),
        ss("そう読める\nただ身代金の額や払い方は\n公開された画像には\n書かれていない", se="pikon"),
        ss("ちなみに会社の発表では\n止まったサーバーは\n“再起動できない”状態", SERVER, se="page_turn_01"),
        nn("カギかけられてるんだもん\nそりゃ動かないよね……", SERVER, se="deflate_hyororo"),
        ss("深夜3時に呼び出されて\n止まったサーバーを前にしたら\nまず再起動を試すのは\n自然な動きではある", SERVER, se="kon"),
        nn("運用の人\nほんとお疲れさまです……", SERVER, se="chirin"),
        ex(SERVER, "IDCFは「3時40分に検知し\n決められた手順で対応した」\nと説明している（報道の要旨）", se="pinpoon_note"),
        ex(HACKER, "ハッカーにとって煽りは“作戦”でもある\n→ 相手を焦らせて払わせるための\n心理戦　と言われている", dur=3.8, se="pc_warning"),
        nn("煽り性能まで\n武器なのか……", HACKER, se="game_touhou_pichuun_miss_defeat"),
        # ---- 6. データが戻らない ----
        chap("本当にヤバいのはここ", se="doon_heavy", bgm={"file": COCOA, "gain": -2, "fade": 0.6}),
        two(SERVER, "対象の4ゾーンのデータは\n取り出し・復元が困難\n（公式の発表）", se="doon_movie"),
        two(SERVER, "「復元できるのは\nお客さま自身が持っている\nバックアップからのみ」", se="page_turn_01"),
        close("bg02_room", "@react", "ニュース猫", "クラウドに預けてたら\n安心じゃないの！？", se=["scream_woman_shock_horror"]),
        ss("預けたデータの“コピー”を\n自分でも別の場所に\n持ってたかどうかで\n明暗が分かれた", se="pikon"),
        dia("e06_meian", "別のクラウドにバックアップがあった会社は　そこから作り直し中", right=S, dur=4.4, se="card_flip"),
        dia("e06_meian", "バックアップがなかった所は　別の場所で一から作り直し", right=S, dur=4.2, se="card_place"),
        ex(SERVER, "IDCFのバックアップサービスにも\n書き換えられない保存の選択肢はあるが\n今は管理の仕組みを止めていて使えない", dur=4.0,
           se="pinpon_notice"),
        ex(SERVER, "データ自体は残っているとされる\n（報道の要旨）", se="pinpoon_note"),
        nn("マンションの金庫に\nしまったカギが\nマンションごと\n封鎖されてる感じ……", se="chin_bell_failure_sad_ending"),
        ss("だから\n“バックアップは別の場所に”\nが鉄則", se="tv_professional_poon"),
        dia("e06_basic", "コピーを複数　ちがう場所に　1つは書き換えられない形で", right=S, dur=4.4, se="pinpoon_correct"),
        # ---- 7. 情報は漏れた？ ----
        chap("情報は漏れたの？", se="quiz_question_01", bgm={"file": AM223, "gain": -2, "fade": 0.6}),
        two("bg26_phone_alert", "IDCF：個人情報の流出は\n「確認中」", se="pi"),
        two("bg26_phone_alert", "利用していたJR東日本は10月9日\nメールアドレスなどが\n漏れた可能性を発表", se="pc_warning"),
        dia("e07_jr", "えきねっと・大人の休日倶楽部・ビューカード　合わせて最大約609万件", "bg26_phone_alert", right=S, dur=5.0,
            se="card_flip"),
        close("bg26_phone_alert", "@react", "ニュース猫", "600万！？", se=["explosion_chudoon"]),
        ss("“可能性”の最大の数な\n漏れたと決まった\nわけじゃない", "bg26_phone_alert", se="hyoshigi_01"),
        dia("e07_jr", "氏名・住所・カード番号・パスワードは　含まれないとしている", "bg26_phone_alert", right=S, se="pinpoon_note"),
        ss("こういう時は　便乗した\n偽の“お詫びメール”に注意\n（4本目でもやった）", "bg26_phone_alert", se="pc_warning"),
        ss("“カギをかける（暗号化）”と\n“盗む（流出）”は\n別の話", se="pikon"),
        ss("ただ　中身に触れられた以上\n“漏れてない”と言い切るのも\n難しい", se="kon"),
        nn("どこから\n入られたの？", se="question_mark_pop_confused_huh"),
        ex("bg02_room", "侵入経路：10月11日時点で\nまだ公表されていない", se="pinpon_notice"),
        nn("そこが一番\n知りたいのに", se="deflate_hyororo"),
        ex("bg02_room", "同じ週に日本で捕まったハッカー集団（9本目）と\n同じ犯人かどうかは\n分かっていない", dur=3.8, se="pinpoon_note"),
        # ---- 8. ネットの声 ----
        chap("ネットの声", se="whoosh_shu", dur=1.4),
        net("@react", "“YOUR CLOUD\nIS OURS”\n悔しいけど\nかっこいい", se="kon"),
        net("@react", "ハッカーに\n“まだ気づかないの？”\nって言われるの\n屈辱すぎる", se="boing_01"),
        net("@react", "7時間再起動してたって\n話がほんとなら\n現場は地獄", se="pi"),
        net("sleepy_old_memories_cat", "深夜3時に\n呼び出された\n担当の人が\n一番かわいそう", se="chiin_01"),
        net("@react", "県のホームページが\n見られないの\n地味に怖い", se="question_hatena_maou"),
        net("@react", "バックアップ\n取ってた会社が\n勝ち組すぎる", se="game_coin_get_money_gain_happy"),
        net("@react", "クラウドに預けたら\n安心、じゃ\nなかったのか……", se="deflate_hyororo"),
        net("@react", "“時計は本物だ”\nってセリフ\n悪役すぎる", se="cuckoo_clock"),
        nn("みんな\nハッカーのセリフ回しに\n持っていかれてる", "bg09_sns", se="silly"),
        # ---- 9. まとめ ----
        dict(bg=bg("bg03_blackboard"), inset={"card": pt("e09a_known"), "box": (200, 60, 1720, 860)}, dur=5.0,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)],
             bgm={"file": MIRAI, "gain": -2, "fade": 0.8}, se="chiin_01"),
        dict(bg=bg("bg03_blackboard"), inset={"card": pt("e09b_claims"), "box": (200, 60, 1720, 860)}, dur=5.0,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)], se="card_flip"),
        dict(bg=bg("bg03_blackboard"), inset={"card": pt("e09c_unknown"), "box": (200, 60, 1720, 860)}, dur=4.2,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)], se="card_place"),
        ss("クラウドでも\n預けっぱなしは危ない\n自分のデータは\n自分でもコピーを持っとく", dur=3.4, se="tv_professional_poon"),
        nn("とりあえず\nスマホの写真の\nバックアップしてくる", se="dash_super_fast"),
        nn("続報が出たら\nまたやります", se="pikoon_retro"),
        dict(bg=bg("bg03_blackboard"), card=pt("e10_ending"), dur=3.0, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(chap("→ 4本目「個人情報、盗まれすぎ問題」\n9本目「ハッカー集団の中心メンバー拘束」もどうぞ", dur=3.0), chapter_size=70),
    ]


def cuts_full():
    return L.apply_fx(L.allocate(cuts_all()))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "10_idcf_full.mp4")
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
