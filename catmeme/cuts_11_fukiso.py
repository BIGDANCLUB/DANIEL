"""11_fukiso（2,000万円の車を盗んだ疑いでも不起訴）のカット割り。原稿 scripts/11_fukiso.md（v2）。作りは 10本目と同じ。

python3 catmeme/cuts_11_fukiso.py          → out/11_fukiso_full.mp4
python3 catmeme/cuts_11_fukiso.py --audio  → 音だけ作り直す
python3 catmeme/cuts_11_fukiso.py 0:10     → 先頭10カットだけ

原稿のルール（必ず守る）：
- 怒りの矛先は ①事件そのもの ②置き去りにされる被害者 ③理由を説明しない仕組み。外国人全体・特定の国籍への怒りは煽らない
- 字幕の国籍は「ブラジル国籍の男性」「アメリカ国籍の男性」まで（報道で確認できないネットの話は「外国籍の男性」にとどめる）
- 不起訴の人は罪に問われていない：「犯人」と呼ばない・猫で演じない・名前や顔は出さない
- 真偽が分からない話は「と言われている」を付けるだけ
"""
import os
import sys

import cuts_04_leak as L
import render as R

HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("11_fukiso", "04_leak", "03_kodomo_nisa", "02_october", "01_todai")]
L.PT = os.path.join(HERE, "parts", "11_fukiso")
VIC = "被害者の猫"
L.ROLE[VIC] = (35, 140, 65)
pt, cat, duo, solo, close, dia, expl, chap, net, nn, ss = L.pt, L.cat, L.duo, L.solo, L.close, L.dia, L.expl, L.chap, L.net, L.nn, L.ss
bg = L.bg
N, S = L.N, L.S
PURPLE, COCOA, MIRAI, KAMI = L.PURPLE, L.COCOA, L.MIRAI, L.KAMI
AM223 = os.path.join(L.BGM, "2_23_AM.mp3")
LETTER = os.path.join(L.BGM, "手紙のさよなら.mp3")

L.POOLS["react"] += ["stare_standing_marmot", "flip_emo_cat_hair"]
L.POOLS["calm"] += ["lick_talking_goat", "eat_chips_cat", "stand_real_sheep"]
# 被害者の猫：車を盗まれた人・殴られた警備員の気持ちの代弁（架空）
L.POOLS["victim"] = ["sad_banana_cat_cry", "sad_black_dog", "despair_dramatic_kitten", "sulk_hungry_cat", "blank_black_cat_zoning_out",
                     "sleepy_old_memories_cat", "realize_wet_cat_stare", "leave_cat_leaves_home", "snore_snoring_dog"]
L.FALLBACK["victim"] = ["react", "calm"]
HOME, FEST, PRESS, ROOM, BOARD, SNS = "bg18_backyard", "bg13_izakaya", "bg07_press", "bg02_room", "bg03_blackboard", "bg09_sns"
STING = {"file": KAMI, "len": 3.5, "gain": -14}


def vic(say, b=HOME, **kw):
    return solo(b, "@victim", VIC, say, side=kw.pop("side", "L"), **kw)


def one(b, sub, **kw):
    return dict(bg=bg(b), sub=sub, cats=[cat("@calm", "博識な猫", 470, h=640)], **kw)


def two(b, sub, **kw):
    return dict(bg=bg(b), cats=[cat("@react", "ニュース猫", 500, h=700), cat("@calm", "博識な猫", 1430, h=700)], say=sub,
                text_top=True, **kw)


def ex(b, text, **kw):
    return expl(b, [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "", text, dur=kw.pop("dur", 3.6), **kw)


def fk(b, text="結果　→　不起訴", **kw):
    """「不起訴」の瞬間：赤い文字＋集中線＋揺れ＋神の怒り。"""
    return close(b, "@react", "ニュース猫", text, se=kw.pop("se", ["explosion_dokaan"]), sting=STING, **kw)


def ask(**kw):
    """章の終わりの問いかけ「これ、納得できますか？」。"""
    return dict(card=None, layers=[pt(kw.pop("card", "nattoku"))], dur=kw.pop("dur", 2.8), se=kw.pop("se", "doon_heavy"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=4.6, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        ask(),   # 本編の一番最初にも問いかけ（10/12 ユーザー指定）
        # ---- 1. つかみ ----
        one(HOME, "時価2,000万円の\n高級車", se="doon_movie", sting={"file": KAMI, "len": 4.0, "gain": -14}),
        one(HOME, "盗んだ疑いで\nブラジル国籍の男性を逮捕\nほかの高級車とあわせ3件で送検", se="siren_police", bgm={"file": PURPLE, "gain": -4}),
        nn("さすがにこれは\n起訴でしょ", HOME, se="kon"),
        fk(HOME),
        close(HOME, "@react", "ニュース猫", "はあああ！？", se=["game_pokemon_super_effective_hit_big_damage"]),
        one(FEST, "2日後　お祭りで\n警備員を殴った疑いで\nアメリカ国籍の男性を逮捕", se="punch"),
        fk(FEST),
        close(FEST, "@react", "ニュース猫", "また！？", se=["explosion_chudoon"]),
        one(PRESS, "ブラジル国籍と\nアメリカ国籍の男性", se="pi"),
        one(PRESS, "そして　どちらも\nくわしい理由は\n説明されていない", se="pc_warning"),
        net("@react", "日本\n完全に\nナメられてる", se="boing_01"),
        net("@react", "捕まっても\n不起訴なら\nやったもん勝ち", se="kon"),
        net("@react", "被害者のことは\n誰も考えてない", se="tear_drop"),
        ss("……今回は\nオレも\nモヤモヤしてる", ROOM, se="shock_piano"),
        dict(bg=bg(BOARD), card=pt("e01_title"), dur=3.4, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        # ---- 2. 仙台 ----
        chap("10月7日　仙台", se="doon_heavy"),
        one(HOME, "2025年9月\n宮城県名取市", se="page_turn_01"),
        one(HOME, "住宅に止めてあった\n高級SUV（時価約2,000万円）が\n盗まれた", se="car_brake"),
        vic("朝起きたら……\n車が……\nない……", se="tear_drop"),
        dia("e02_sendai", "盗んだ疑いで　ブラジル国籍の男性（28）が逮捕・送検", right=S, dur=4.4, se="card_flip"),
        dia("e02_sendai", "ほかの高級車を盗んだ疑いもあわせて　3件で逮捕・送検", right=S, dur=4.2, se="card_place"),
        nn("3件！\nこれは決まりでしょ", se="pikon"),
        fk(PRESS, "2026年10月7日　仙台地検\n→　不起訴"),
        ex(PRESS, "地検のコメント\n「捜査の結果、公訴を維持するに足りる\n証拠を収集するに至らなかった」", dur=4.0, se="pinpon_notice"),
        nn("日本語でおk", PRESS, se="tsukkomi_bishi"),
        ss("“裁判で有罪にできるだけの\n証拠が集まらなかった”\nってこと", PRESS, se="pikon"),
        close(PRESS, "@react", "ニュース猫", "1年かけて？\n3件も逮捕して？", se=["explosion_chudoon"]),
        vic("じゃあ……\n私の車は……？", se="chin_bell_failure_sad_ending"),
        one(SNS, "ネットでは\n「泥棒天国ジャパン」\nという声", se="pi"),
        one(SNS, "高級車の盗難では\n「通算4度目」の逮捕と\n報じられた別の事件も", se="page_turn_02"),
        nn("4度目って……\n何回捕まえれば\n終わるの", SNS, se="deflate_hyororo"),
        ask(),
        # ---- 3. 横浜 ----
        chap("10月9日　横浜", se="doon_heavy"),
        one(FEST, "9月　横浜・赤レンガ倉庫の\n「オクトーバーフェスト」", se="page_turn_01"),
        one(FEST, "会場を守っていた\n警備員の男性が\n顔を殴られた", se="punch"),
        vic("仕事してた\nだけなのに……", FEST, se="tear_drop"),
        dia("e03_yokohama", "酔って殴るなどした疑いで　アメリカ国籍の男性（27）が逮捕", right=S, dur=4.4, se="card_flip"),
        fk(PRESS, "10月9日　横浜地検\n→　不起訴"),
        ex(PRESS, "地検「犯行後の状況も含めた\n関係証拠の内容を踏まえ\n不起訴処分とした」", dur=4.0, se="pinpon_notice"),
        close(PRESS, "@react", "ニュース猫", "“犯行後の状況”って何！？\n説明それだけ！？", se=["game_aceattorney_desk_slam"]),
        ss("それだけ\nくわしい理由は\n発表されてない", PRESS, se="hyoshigi_01"),
        one(SNS, "ネットでは\n「示談で済ませたのでは」\n「酔ってたら許されるのか」\nと言われている", dur=3.8, se="pi"),
        nn("警備員さん\n殴られ損じゃん", FEST, se="deflate_hyororo"),
        ask(),
        # ---- 4. 被害者は ----
        chap("置き去りにされる被害者", se="doon_heavy", bgm={"file": LETTER, "gain": -4, "fade": 0.6}),
        vic("逮捕された人が\n釈放された", HOME, se="tear_drop"),
        vic("理由は\n教えてもらえない", HOME, se="pi"),
        vic("車も\n戻ってこない", HOME, se="chin_bell_failure_sad_ending"),
        nn("……被害者側からしたら\n地獄じゃん", se="shock_piano"),
        ss("不起訴に納得できないときは\n“検察審査会”に\n申し立てる道はある", se="pikon"),
        dia("e04_kensin", "くじで選ばれた市民が　「その不起訴はおかしくないか」を審査する", right=S, dur=4.4, se="pinpon_notice"),
        nn("でも　被害者が\nそこまでやらなきゃ\nいけないの？", se="question_hatena_maou"),
        ss("……そこなんよ", se="kon"),
        # ---- 5. ネットで広まった話 ----
        chap("ほかにも……", se="doon_heavy", bgm={"file": AM223, "gain": -2, "fade": 0.6}),
        one(SNS, "9月　ネットでは\nこんな話も広まった", se="pi"),
        ex(SNS, "「警察官のふりをして　高齢女性から500万円を\nだまし取った疑いの外国籍の男性が\n不起訴になった」と言われている（まとめサイトなどで話題）",
           dur=4.6, se="pc_warning", explain_size=78),
        close(SNS, "@react", "ニュース猫", "お年寄りの500万……\n老後のお金だよ……", se=["shock_piano"]),
        ex(SNS, "「通訳が来るのを待っている間に\n期限の23日が過ぎて釈放された」\nという話も広まっている", dur=4.2, se="pc_warning"),
        fk(SNS, "通訳待ちで時間切れ！？\nふざけんな！"),
        one(SNS, "こうした話が積み重なって\n「日本は捕まえても裁けない国」\nと受け止められている", dur=3.8, se="doon_movie"),
        # ---- 6. 理由を言わない検察 ----
        chap("なぜ“ナメられている”と\n感じるのか", se="doon_heavy"),
        dia("e06_reasons", "逮捕は速報。不起訴は小さく、いつの間にか終わってる", right=S, dur=4.4, se="card_flip"),
        dia("e06_reasons", "理由はほぼ説明されず　同じような事件が繰り返されているように見える", right=S, dur=4.6, se="card_place"),
        nn("①は本当にそう\n逮捕のときだけ\n大騒ぎ", se="tsukkomi_bishi"),
        ss("しかも“証拠の内容を踏まえ”だけ\n何が足りなかったのか\n誰にも分からない", se="kon"),
        nn("説明しないから\n“外国人だから甘くしたんじゃ？”\nって思われるんだよ", se="tsukkomi_bashi"),
        dia("e06_types", "不起訴には　主に3つの種類がある", right=S, dur=4.6, se="pinpon_notice"),
        nn("どれに当たるのかすら\n教えてくれないの？", se="question_hatena_maou"),
        ss("教えてくれない\n日本人の事件でも\n“プライバシー保護のため”で終わり", se="hyoshigi_01"),
        close(ROOM, "@react", "ニュース猫", "それ、全員に対して\n不親切ってことじゃん！", se=["explosion_chudoon"]),
        ask(),
        # ---- 7. 23日の壁 ----
        chap("時間切れで釈放？", se="doon_heavy"),
        dia("e07_23days", "逮捕から最大23日の間に　起訴か釈放かを決めないといけない", right=S, dur=4.8, se="xylophone_transition"),
        nn("たった23日で\n全部調べろってこと？", se="question_hatena_maou"),
        ss("日本語が通じない人の取り調べには\n通訳が要る\n通訳が足りないと時間との勝負になる\nと言われている", dur=3.8, se="pikon"),
        close(ROOM, "@react", "ニュース猫", "通訳不足で時間切れ……\nそれ、国の準備不足じゃん", se=["explosion_dokaan"]),
        ss("高級車の盗難は\n盗んだ車がすぐ海外へ流され\n証拠集めが難しい\nと言われている", dur=3.8, se="kon"),
        nn("相手はプロ\nこっちは23日……\nそりゃナメられるわ", se="deflate_hyororo"),
        # ---- 8. 数字では ----
        chap("数字で見ると", se="quiz_question_01", bgm={"file": COCOA, "gain": -2, "fade": 0.6}),
        dia("e08_stats", "来日外国人の事件の起訴率は　日本人を含む全体より　刑法犯で2.8ポイント高い", right=S, dur=5.0,
            se="page_turn_01"),
        nn("え、数字だと\nちゃんと起訴されてる\n方なの？", se="question_mark_pop_confused_huh"),
        ss("全体の数字では\nそう", se="kon"),
        nn("じゃあ　なんで\nこんなにムカつくの？", se="question_hatena_maou"),
        ss("目の前の事件が\n理由も説明されずに\n終わっていくから", se="pikon"),
        ss("被害者が納得できないまま\n終わる事件が\n1件でもあったらダメなんよ", dur=3.4, se="tv_professional_poon"),
        close(ROOM, "@react", "ニュース猫", "それ！", se=["explosion_chudoon"]),
        # ---- 9. ネットの声 ----
        chap("ネットの声", se="whoosh_shu", dur=1.4, bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        net("@react", "日本の司法\nナメられすぎ", se="boing_01"),
        net("@react", "2,000万円盗まれて\n“証拠不十分”\n被害者は泣き寝入り", se="tear_drop"),
        net("sleepy_old_memories_cat", "警備員さんが\n殴られ損なのが\n一番つらい", se="chiin_01"),
        net("@react", "逮捕は大きく報道\n不起訴はこっそり\n信用できない", se="pi"),
        net("@react", "理由を言わないから\n全部“外国人だから？”\nって疑われる\n検察の自業自得", se="tsukkomi_bishi"),
        net("@react", "通訳が足りなくて\n時間切れなら\n国の怠慢", se="boing_02"),
        net("@react", "お年寄りの500万の件が\n本当なら\n絶対に許せない", se="kon"),
        net("@react", "国籍関係なく\n悪いことしたら\nちゃんと裁け", se="pinpoon_correct"),
        nn("最後の\nほんとそれ", "bg09_sns", se="kon"),
        # ---- 10. まとめ ----
        dict(bg=bg(BOARD), inset={"card": pt("e10_cases"), "box": (200, 60, 1720, 860)}, dur=5.0,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)],
             bgm={"file": MIRAI, "gain": -2, "fade": 0.8}, se="chiin_01"),
        dict(bg=bg(BOARD), inset={"card": pt("e10_anger"), "box": (200, 60, 1720, 860)}, dur=4.4,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)], se="card_flip"),
        ss("“ナメられてる”と言われないために\n必要なのは　ちゃんと裁くこと\nそして　なぜ不起訴かを説明すること", dur=4.0,
           se="tv_professional_poon"),
        nn("被害者が\n納得できる国で\nあってほしい", se="chirin"),
        ask(card="nattoku_last", dur=3.2, se="doon_heavy"),
        dict(bg=bg(BOARD), card=pt("e11_ending"), dur=3.0, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(chap("→ 4本目「個人情報、盗まれすぎ問題」\n10本目「ハッカーに煽られたクラウド」もどうぞ", dur=3.0), chapter_size=70),
    ]


def cuts_full():
    return L.apply_fx(L.allocate(cuts_all()))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "11_fukiso_full.mp4")
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
