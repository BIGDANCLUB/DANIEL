"""06_zetsubou（「絶望ライン工」の結婚炎上）のカット割り。原稿 scripts/06_zetsubou.md。作りは 04 と同じ（部品は cuts_04_leak を使い回す）。

python3 catmeme/cuts_06_zetsubou.py          → out/06_zetsubou_full.mp4
python3 catmeme/cuts_06_zetsubou.py --audio  → 音だけ作り直す
python3 catmeme/cuts_06_zetsubou.py 0:10     → 先頭10カットだけ

注意（指示書より）：本人の言葉は報道・説明動画の要旨だけ。本人をバカにしない（本人役は落ち着いた猫だけ）。
奥さん・お子さんはいじらない。噂の数字は出さない。
"""
import os
import sys

import cuts_04_leak as L
import render as R

HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("06_zetsubou", "04_leak", "03_kodomo_nisa", "02_october", "01_todai")]
L.PT = os.path.join(HERE, "parts", "06_zetsubou")
HONNIN = "本人（再現）"
L.ROLE[HONNIN] = (35, 140, 65)
# 新しい背景が届くまでの仮の背景
STANDIN = {"bg31_factory_line": "bg25_office_desk", "bg32_simple_room": "bg14_home_night", "bg33_wedding": "bg19_kids_room"}
_bg = L.bg


def bg(n):
    try:
        return _bg(n)
    except FileNotFoundError:
        print(f"（仮）{n} → {STANDIN[n]}")
        return _bg(STANDIN[n])


L.bg = bg
pt, cat, duo, solo, close, dia, expl, chap, net, nn, ss = L.pt, L.cat, L.duo, L.solo, L.close, L.dia, L.expl, L.chap, L.net, L.nn, L.ss
N, S = L.N, L.S
PURPLE, COCOA, MIRAI, KAMI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.KAMI, L.NORA
CALM_HONNIN = ["sleepy_old_memories_cat", "calm_black_face_sheep", "think_bike_front_seat_cat", "work_typing_cat",
               "call_customer_service_cat"]
# 本人役の猫は、ほかの役（博識な猫など）には使わない（同じ猫が別の人に見えないように）
L.POOLS = {k: [a for a in v if a not in CALM_HONNIN] for k, v in L.POOLS.items()}


def two(b, sub, **kw):
    """2匹を並べて、上に説明の字幕（出来事の説明）。"""
    return dict(bg=bg(b), cats=[cat("@react", "ニュース猫", 500, h=700), cat("@calm", "博識な猫", 1430, h=700)], say=sub,
                text_top=True, **kw)


def honnin(k, say, **kw):
    """本人（再現）。落ち着いた猫だけを使い、セリフは要旨。"""
    return solo("bg32_simple_room", CALM_HONNIN[k % len(CALM_HONNIN)], HONNIN, say, side="R", **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=3.8, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- 1. つかみ ----
        dict(bg=bg("bg31_factory_line"), card=pt("e01_title"), dur=2.8, bgm={"file": PURPLE, "gain": -2}, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=bg("bg31_factory_line"), sub="「年収240万円・43歳独身・\n非正規・工場勤務」", cats=[cat("@calm", "博識な猫", 470, h=640)],
             se="doon_movie"),
        dict(bg=bg("bg31_factory_line"), sub="このキャラで　登録者68万人の\n人気YouTuber「絶望ライン工」",
             cats=[cat("@calm", "博識な猫", 470, h=640)], se="pc_warning"),
        dict(bg=bg("bg33_wedding"), sub="9月28日\n結婚と　子どもの誕生を報告", cats=[cat("@calm", "博識な猫", 470, h=640)],
             se="chiin_01"),
        nn("え、\nおめでたいじゃん！", "bg33_wedding", se="game_mario_1up"),
        chap("ところが…", se="doon_heavy"),
        close("bg06_spotlight", "@react", "ニュース猫", "大炎上！？\nなんで！？", se=["explosion_chudoon"]),
        ss("“独身”そのものが\n売りだったからな", "bg06_spotlight", se="kon"),
        # ---- 2. どんなチャンネルだったか ----
        chap("どんなチャンネルだった？", se="quiz_question_01"),
        dia("e02_channel", "工場勤務・寮暮らし・柴犬・婚活・給与明細", "bg31_factory_line", right=S, se="page_turn_01"),
        nn("給与明細まで\n出してたのか", "bg31_factory_line", se="question_hatena_maou"),
        ss("“等身大の独身男性”として\n共感を集めてたんだ", "bg31_factory_line", se="pikon"),
        nn("わかる\n疲れた日に見ると\n落ち着くやつ", "bg32_simple_room", se="chiin_01"),
        ss("“自分と同じだ”って\n思える人が多かったんだろうな", "bg32_simple_room", se="kon"),
        dia("e03_works", "本・連載・アルバムも　“独身”が売り", right=S, se="card_flip"),
        nn("本もアルバムも\n“独身”推しだ", se="boing_01"),
        dia("e03_works", "アルバムの発売は　結婚報告の約1か月前", right=S, se="doon_heavy"),
        # ---- 3. なぜ炎上したのか ----
        chap("なんで炎上したの？", se="quiz_question_02", bgm={"file": NORA, "gain": -2}),
        dia("e04_timeline", "9月17日・24日にも“独身”の動画を公開", right=S, se="xylophone_transition"),
        dia("e04_timeline", "「独身の休日」を出した　4日後に　結婚と子どもの報告", right=S, se="doon_heavy"),
        close("bg06_spotlight", "@react", "ニュース猫", "4日後！？\n時空ゆがんでない！？", se=["explosion_dokaan"],
              sting={"file": KAMI, "len": 4.0, "gain": -16}),
        ss("家族がいる間も\n“独身”の動画を\n出してたことになる", se="hyoshigi_01"),
        two("bg09_sns", "「独身を売りにした本やアルバムは？」\n「キャラは商品だったのか」\nと批判が集まった", se="pc_warning"),
        two("bg09_sns", "さらに　コメント欄を\nオフにしたことでも\n批判が広がった", se="buzzer_wrong"),
        nn("閉じたら\n余計に燃えるやつ", "bg09_sns", se="spring_byoin"),
        ss("視聴者が怒ったのは\n“結婚”じゃないんだよな", se="kon"),
        dia("e05_anger", "怒りの中心は「独身を売り続けた」「コメント欄を閉じた」", right=S, se="card_flip"),
        # ---- 4. 本人の説明 ----
        chap("10月5日　本人が説明", se="whoosh_shu", bgm={"file": COCOA, "gain": -4}),
        dict(bg=bg("bg32_simple_room"), sub="ここからの本人の言葉は\n報道・説明動画の要旨です", cats=[cat("@calm", "博識な猫", 470, h=640)],
             se="pinpon_notice"),
        honnin(0, "配偶者がいることと\n妊娠を伏せていました\n私は嘘をついておりました", dur=3.6, se="pi"),
        honnin(1, "職種が変わったあとも\n“ライン工”の設定を\n使い続けました\n極めて悪質でした", dur=3.8, se="pi"),
        honnin(2, "“弱者ビジネス”と\n思われても仕方のない\n運営でした\n人気への過信がありました", dur=3.8, se="pi"),
        honnin(3, "コメント欄を閉じたこと\n報告のタイミングを誤り\n視聴者を裏切りました", dur=3.6, se="pi"),
        expl("bg32_simple_room", [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "",
             "家族を伏せていた理由（本人の説明の要旨）\n危害をほのめかす連絡や　イベント出演のキャンセルなど\n実害から家族を守るため", dur=4.4,
             se="pinpon_notice"),
        expl("bg32_simple_room", [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "",
             "もうひとつの理由（本人の説明の要旨）\n妊娠・出産を　軽々しく発表するリスクを考えた", dur=3.6, se="pinpon_notice"),
        honnin(4, "批判は　欲に目が眩んだ\n自分の愚かさが招いた\n結果として受け止めます", dur=3.6, se="pi"),
        two("bg32_simple_room", "今は育児に向き合っている\nと説明", se="page_turn_01"),
        two("bg09_sns", "同じ日　Xで\nチャンネルの活動休止を発表", se="doon_movie"),
        dia("e06_subs", "登録者は　約1万1,000人減（10/7時点の報道）", right=S, se="card_place"),
        nn("思ったより\n減ってない……？", se="question_hatena_maou"),
        ss("それだけ\n応援してる人も\n多いってことだな", se="pikon"),
        # ---- 5. ネットの反応 ----
        chap("ネットの反応は？", se="quiz_den"),
        dia("e07_reactions", "報道で紹介された声は　批判・擁護・考察の3つ", right=S, se="xylophone_transition"),
        two("bg09_sns", "批判：「少なくとも\n今の看板は下ろさないと\n違和感しかない」（趣旨）", se="buzzer_wrong"),
        two("bg09_sns", "擁護：「あなたが幸せなら\nそれでいい」\n「ただただ幸せになってくれ」（趣旨）", se="chiin_01"),
        two("bg09_sns", "「犬を大事にして」\nという声も（趣旨）", se="pikon"),
        two("bg09_sns", "考察：「今は昔ほど\n余裕のない社会に\nなっているのでは」（趣旨）", se="page_turn_01"),
        nn("批判も応援も\nどっちもあるんだな", "bg09_sns", se="kon"),
        chap("ネットでは　こんな声も…", se="whoosh_shu"),
        net("@react", "独身の休日を出した\n4日後に子ども、は\n時空が歪んでる", se="kon"),
        net("@react", "年収240万は\n本業の話でしょ？\n動画の収入は別って\nみんな薄々わかってた", se="silly"),
        net("@react", "貧乏を“見せる”のが\n一番稼げる時代", se="boing_01"),
        net("@react", "“弱者ビジネス”って\n自分で言っちゃうの\n正直すぎる", se="tsukkomi_bishi"),
        net("@calm", "家族を守るために\n隠したなら\nそれは責められない", se="chiin_01"),
        net("@calm", "結婚して子どもが\nできたのに叩かれる\n世界線", se="tear_drop"),
        net("@react", "看板変えて\n“既婚ライン工”で\n再出発してほしい", se="pikon"),
        two("bg09_sns", "「本当は年収○○万」「やらせ」\nなどの噂は\n根拠が確認されていません", se="pinpon_notice"),
        ss("噂の数字は\n信じないようにな", "bg09_sns", se="hyoshigi_02"),
        # ---- 6. この件から見えること ----
        chap("この件から見えること", se="bell_tower_goon", bgm={"file": MIRAI, "gain": -2, "fade": 0.8}),
        dia("e08_setting", "“設定”を売るチャンネルの　むずかしさ", right=S, se="page_turn_01"),
        ss("“設定”を売るなら\n変わったときの畳み方が\n一番むずかしい", dur=3.2, se="tv_professional_poon"),
        nn("早めに言ってたら\nここまで燃えなかった\nのかもね", se="kon"),
        ss("応援してた人ほど\n“言ってほしかった”\nって気持ちなんだろうな", se="chiin_01"),
        ss("とはいえ\n家族を守る事情もあった\nそこは難しいところだな", dur=3.2, se="hyoshigi_01"),
        dict(bg=bg("bg03_blackboard"), inset={"card": pt("e09_matome"), "box": (200, 60, 1720, 860)}, dur=5.0,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)], se="chiin_01"),
        nn("おめでたいことが\n炎上になるの\nなんか切ないね", "bg33_wedding", se="tear_drop"),
        dict(bg=bg("bg03_blackboard"), card=pt("e10_ending"), dur=3.0, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
    ]


def cuts_full():
    return L.apply_fx(L.allocate(cuts_all()))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "06_zetsubou_full.mp4")
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
