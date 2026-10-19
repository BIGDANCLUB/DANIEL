"""20_sagi（人気YouTuberも次々被害　「郵便局です」から始まる特殊詐欺、1日10億円）のカット割り。
原稿 scripts/draft_sagi.md（v1）。作りは 10〜13本目と同じ（セリフごとに猫ミームを入れ替える）。

python3 catmeme/cuts_20_sagi.py          → out/20_sagi_full.mp4
python3 catmeme/cuts_20_sagi.py --audio  → 音だけ作り直す

原稿のルール（必ず守る）：
- 被害を公表した YouTuber は被害者。笑いにしない・責めない。チャンネル名は出さない（「登録者の多い人気YouTuber」まで）。
  動画の中身（金額・経緯）は本人の動画で確認できた範囲だけ → 確認できていないので、タイトルと再生回数だけ
- 手口は「見抜くため」の説明だけ（警察の注意喚起の範囲）。〔再現〕の場面は右上に「※警察の注意喚起をもとにした再現」の札
- 統計は警察庁の発表どおり。ネットの声は架空の要約。「にゃ」禁止
- 全動画共通：今日の一言・単語の途中で改行しない・最後はチャンネル登録の画面・過去の動画にはふれない
  （原稿の「→ 4本目もどうぞ」は、このルールに合わせて入れていない）
- 使わない BGM：「やる気のないダースベイダーのテーマ」（チャンネルのルール）→ 再現の場面は「神の怒り」を小さく
- AI の背景は使い切ったので（10/19 クレジット切れ）、これまでの背景・動く背景で作る
"""
import os
import sys

import cuts_04_leak as L
import render as R

HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("16_tenchim", "15_vambi", "18_story", "17_imamori", "04_leak", "02_october",
                                                         "01_todai")]
L.PT = os.path.join(HERE, "parts", "20_sagi")
pt, cat, duo, solo, close, dia, expl, chap, net, nn, ss = L.pt, L.cat, L.duo, L.solo, L.close, L.dia, L.expl, L.chap, L.net, L.nn, L.ss
bg = L.bg
N, S = L.N, L.S
PURPLE, COCOA, MIRAI, KAMI = L.PURPLE, L.COCOA, L.MIRAI, L.KAMI
AM223 = os.path.join(L.BGM, "2_23_AM.mp3")
LETTER = os.path.join(L.BGM, "手紙のさよなら.mp3")

L.POOLS["react"] += ["stare_standing_marmot", "flip_emo_cat_hair"]
L.POOLS["calm"] += ["eat_chips_cat", "stand_real_sheep"]
# 詐欺の電話（架空・声だけの役）とお母さん猫（架空・70代）
SCAM, MOM = "詐欺の電話", "お母さん猫"
L.ROLE[SCAM] = (30, 30, 30)
L.ROLE[MOM] = (35, 140, 65)
L.POOLS["scam"] = ["angry_aiming_cat", "cocky_dj_cat", "showoff_gojo_cosplay_cat", "call_customer_service_cat", "work_typing_cat",
                   "stare_standing_marmot"]
L.POOLS["mom"] = ["sleepy_old_memories_cat", "meow_ragdoll_chubby_cat", "talk_orange_white_sitting_cat", "eat_crunchy_cat_luna"]
L.FALLBACK["scam"] = ["calm"]
L.FALLBACK["mom"] = ["calm"]

POST, POLICE, STUDIO, PHONE_POST, HOME, KITCHEN, ROOM, BOARD, SNS, CHAT, PHONE = (
    "bg17_post_office", "bg77_police_station", "bg70_youtube_studio", "bg90_phone_post", "bg14_home_night", "st02_home_kitchen",
    "bg02_room", "bg03_blackboard", "bg09_sns", "bg101_phone_chat", "bg26_phone_alert")
V_CHART, V_POLICE, V_PHONE_M, V_PHONE_W, V_HANDS, V_HAND, V_DARK, V_CASH, V_HOOD, V_SHIBUYA = (
    "v11_stock_chart_blue", "v16_police_car_lights", "v04_smartphone_man_coat", "v18_smartphone_woman", "v20_smartphone_hands",
    "v22_smartphone_hand", "v13_cat_gray_dark", "v06_cash_counting", "v10_hooded_figure_mystery", "v09_shibuya_crossing_aerial")
TAG = pt("tag_reenact")


def sub(b, text, **kw):
    """【字幕】説明の字幕。博識な猫を小さく1匹。"""
    return dict(bg=bg(b), sub=text, cats=[cat("@calm", "博識な猫", 470, h=640)], se=kw.pop("se", "pi"), **kw)


def card(c, text, b=BOARD, **kw):
    if len(text) > 22 and "\n" not in text and "　" in text:   # 長い字幕は区切り（全角スペース）で改行（単語の途中で切らない）
        k = min((i for i, ch in enumerate(text) if ch == "　"), key=lambda i: abs(i - len(text) / 2))
        text = text[:k] + "\n" + text[k + 1:]
    return dia(c, text, b, right=S, dur=kw.pop("dur", 5.0), se=kw.pop("se", "card_flip"), **kw)


def scam(say, b=PHONE, **kw):
    """〔再現〕詐欺の電話（架空）。右上に再現の札。"""
    c = solo(b, "@scam", SCAM, say, side="R", **kw)
    c["layers"] = [TAG]
    return c


def re(c):
    """〔再現〕の間のほかのカットにも札を付ける。"""
    c["layers"] = c.get("layers", []) + [TAG]
    return c


def mom(say, **kw):
    return solo(KITCHEN, "@mom", MOM, say, side="R", se=kw.pop("se", "pi"), **kw)


def ex(b, text, **kw):
    return expl(b, [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "", text, dur=kw.pop("dur", 4.0),
                se=kw.pop("se", "pinpon_notice"), **kw)


def voice(say, **kw):
    return net("@react", say, se=kw.pop("se", "pi"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=5.2, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- 1. つかみ ----
        sub(STUDIO, "10月18日　YouTubeに\nこんなタイトルの動画が並んだ", se="page_turn_01",
            sting={"file": KAMI, "len": 3.5, "gain": -14}),
        dict(bg=bg(STUDIO), inset={"card": pt("e01_titles"), "box": (200, 60, 1720, 860)}, dur=5.6, se="card_flip",
             cats=[cat("@calm", "博識な猫", 1750, h=380, bottom=1060, float=True)], bgm={"file": AM223, "gain": -4}),
        close(STUDIO, "@react", "ニュース猫", "え、全部……\n人気YouTuberの動画？", se=["explosion_chudoon"]),
        sub(PHONE_POST, "どれも　登録者の多い\n人気YouTuberが\n自分の被害を公表した動画", dur=3.8),
        sub(PHONE_POST, "3本あわせて　1日で\n100万回以上　再生された", dur=3.4),
        nn("詐欺って\nお年寄りが狙われるものだと\n思ってた……", V_PHONE_W, se="question_mark_pop_confused_huh"),
        ss("今は　ネットに慣れてる世代でも\nやられてる", V_PHONE_W, se="kon"),
        dict(bg=bg(V_HANDS), card=pt("e01_title"), dur=4.0, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        # ---- 2. 1日10億円 ----
        chap("数字で見ると", se="doon_heavy"),
        card("e02_stats", "被害額は1,816億円　上半期として過去最悪", V_CHART, dur=5.0),
        card("e02_stats", "1日あたり約10億円　件数は2万2,031件（18.3％増）", V_CHART, dur=5.0),
        card("e02_stats", "いちばん多いのはSNS型投資詐欺　2番目はニセ警察詐欺", V_CHART, dur=5.0),
        nn("1日10億円……\n毎日　宝くじの1等が\n消えてるレベル", V_CASH, se="shock_piano"),
        ss("しかも警察庁は\n“危機的な状況”と\n言ってる", V_POLICE, se="kon"),
        # ---- 3. 「郵便局です」から始まる手口（再現） ----
        chap("こうやって、だまされる", se="doon_heavy", bgm={"file": KAMI, "gain": -12, "fade": 0.6}),
        re(sub(HOME, "ステップ1　自動音声", se="page_turn_01")),
        scam("こちらは郵便局です\nお客さまの荷物について\n確認があります", HOME, se="pi"),
        scam("オペレーターに\nつなぐには\n1を押してください", HOME),
        re(nn("（ポチッ）", HOME, se="pi")),
        re(sub(POST, "ステップ2　“郵便局員”が出る", se="page_turn_01")),
        scam("お客さま名義の荷物に\n他人のキャッシュカードが\n入っていました", POST),
        scam("犯罪に関わっている\n可能性があるので\n警察におつなぎします", POST),
        re(nn("え、オレ\n何もしてないけど！？", POST, se="question_mark_pop_confused_huh")),
        re(sub(POLICE, "ステップ3　“警察官”に交代", se="page_turn_01")),
        scam("〇〇警察です\nあなたの口座が\n犯罪に使われている疑いが", POLICE),
        scam("このままだと逮捕になります\nくわしくはビデオ通話で", POLICE),
        re(close(POLICE, "@react", "ニュース猫", "た、逮捕！？", se=["explosion_dokaan"])),
        re(sub(V_HANDS, "ステップ4　“資産を守るため”と言って\nお金を移させる", se="page_turn_01", dur=3.6)),
        scam("無実を証明するために\n資産をいったん\nこちらの口座に移してください", V_HANDS),
        chap("再現ここまで", dur=1.6, bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        nn("……いや　今見ると怪しいけど\n本当に“警察です”って\n言われたら焦る", V_PHONE_M, se="kon"),
        ss("そこが狙い\n“郵便局”“警察”と\nまじめな名前を次々出して", V_PHONE_M, se="pikon"),
        ss("考える時間を\n与えない", V_PHONE_M, se="kon"),
        sub(V_HAND, "ほかにも　電話会社や総務省を名乗ってから\n警察に替わる例もある", dur=3.8),
        sub(V_HOOD, "最近は　警察の公式サイトそっくりの偽サイトで\n「逮捕状」を見せる手口も\nと言われている", dur=4.2),
        # ---- 4. なぜ引っかかるのか ----
        chap("なぜ“慣れてる人”でも\n引っかかる？", se="quiz_question_01"),
        card("e04_trick", "名乗るのは“信用できる所”　「逮捕」「犯罪」でパニックにさせる", dur=5.2),
        card("e04_trick", "「誰にも言わないで」と相談させない　ビデオ通話で本物っぽく見せる", dur=5.2),
        card("e04_trick", "「お金を守るため」と言う　→　だまされている感覚がない", dur=5.0),
        ss("“お金を払え”じゃなくて\n“お金を守れ”\nここが新しい", BOARD, se="pikon"),
        nn("守ってるつもりで\n全部持っていかれるのか……", BOARD, se="deflate_hyororo"),
        sub(V_PHONE_M, "高齢者だけでなく　40〜50代の現役世代が\nネットバンキングで振り込んでしまう例も\n報告されている", dur=4.6),
        close(V_PHONE_M, "@react", "ニュース猫", "オレらの世代も\nど真ん中じゃん", se=["shock_piano"]),
        # ---- 5. 見抜く5つのポイント ----
        chap("これだけ覚えて", se="quiz_question_02", bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        card("e05_points", "郵便局は自動音声で個人情報を聞かない　番号を押させない", dur=5.0, se="pinpoon_correct"),
        card("e05_points", "警察は　電話やSNS・ビデオ通話で\n取り調べをしない", dur=5.0, se="pinpoon_correct"),
        card("e05_points", "警察は捜査のために\n「お金を移せ」「振り込め」と言わない", dur=5.0, se="pinpoon_correct"),
        card("e05_points", "「+1」など知らない国際電話は出ない　止める手続きもある", dur=5.0, se="pinpoon_correct"),
        card("e05_points", "迷ったら　いったん切って　家族か「#9110」（警察の相談電話）へ", dur=5.0, se="pinpoon_correct"),
        nn("⑤の“いったん切る”だけで\nだいぶ防げそう", BOARD, se="idea_newtype_01"),
        ss("詐欺は“今すぐ”を作ってくる\nこっちは“あとで”に\n変えればいい", BOARD, se="tv_professional_poon"),
        # ---- 6. 親を守る ----
        chap("実家に電話しよう", se="chirin", bgm={"file": LETTER, "gain": -6, "fade": 0.6}),
        mom("（実家）……あら\n郵便局から電話？\n荷物の確認ですって"),
        close(KITCHEN, "@react", "ニュース猫", "お母さん\nそれ切って！！", se=["explosion_chudoon"]),
        sub(KITCHEN, "ニセ警察詐欺の被害は\n70代が最多", dur=3.2),
        ss("動画を見た今日\n実家に一本電話するだけで\n違う", KITCHEN, se="kon"),
        card("e06_parents", "固定電話は留守番電話に　「郵便局」「警察」から電話が来たら、まず家族に", KITCHEN, dur=5.4),
        card("e06_parents", "国際電話を止める手続き　「誰にも言わないで」は詐欺の合図", KITCHEN, dur=5.2),
        mom("わかった\nまずあんたに電話するわね"),
        nn("それでいい！", KITCHEN, se="pinpoon_correct"),
        # ---- 7. ネットの声 ----
        chap("ネットの声", se="whoosh_shu", dur=1.4, bgm={"file": MIRAI, "gain": -4, "fade": 0.6}),
        voice("あの人気YouTuberでも\nやられるなら\n誰でもやられる"),
        voice("被害を公表してくれたの\n本当に勇気ある"),
        voice("“お金を守るため”って\n言われたら\nたぶん自分も動いちゃう"),
        voice("郵便局から自動音声\nうちにも来たことある"),
        voice("1日10億円って\nもはや産業"),
        voice("とりあえず\n親の家の電話\n留守電にしてくる"),
        voice("犯人\n早く全員捕まって"),
        # ---- 8. まとめ ----
        dict(bg=bg(BOARD), inset={"card": pt("e08_todo"), "box": (200, 60, 1720, 860)}, dur=6.0,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)], se="chiin_01"),
        ss("だまされた人が\n悪いんじゃない\nだます側が　それだけうまい", V_SHIBUYA, se="kon"),
        nn("次は自分か\n自分の親かもしれない\nだから今日　電話する", V_SHIBUYA, se="chirin"),
        dict(bg=bg(BOARD), card=pt("e10_ending"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


def cuts_full():
    return L.apply_fx(L.allocate(cuts_all(), max_use=4))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "20_sagi_full.mp4")
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
