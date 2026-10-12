"""12_akaihane（赤い羽根募金、2.5億円が消えた）のカット割り。原稿 scripts/12_akaihane.md（v1）。作りは 10・11本目と同じ。

python3 catmeme/cuts_12_akaihane.py          → out/12_akaihane_full.mp4
python3 catmeme/cuts_12_akaihane.py --audio  → 音だけ作り直す
python3 catmeme/cuts_12_akaihane.py 0:10     → 先頭10カットだけ

原稿のルール（必ず守る）：
- 元事務局長は「着服の疑い」の段階。「着服した」「横領犯」と言い切らない。名前・顔は出さない。猫で演じない
- 怒りの矛先は「消えた善意」「1人に任せきりだった仕組み」「止められなかった役員・監査」。募金した人・ボランティア・福祉の現場は被害者側
- 「募金するな」とは言わない。「どう寄付先を選ぶか」で締める
- わざと知らないふりをする簡単なボケは入れない（10/11 ユーザー指定）→ 原稿の「羽根、品切れ？」は外した
"""
import os
import sys

import cuts_04_leak as L
import render as R

HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("12_akaihane", "04_leak", "03_kodomo_nisa", "02_october", "01_todai")]
L.PT = os.path.join(HERE, "parts", "12_akaihane")
DON, GEN = "募金した猫", "福祉の現場の猫"
L.ROLE[DON] = (35, 140, 65)
L.ROLE[GEN] = (205, 150, 0)
pt, cat, duo, solo, close, dia, expl, chap, net, nn, ss = L.pt, L.cat, L.duo, L.solo, L.close, L.dia, L.expl, L.chap, L.net, L.nn, L.ss
bg = L.bg
N, S = L.N, L.S
PURPLE, COCOA, MIRAI, KAMI = L.PURPLE, L.COCOA, L.MIRAI, L.KAMI
AM223 = os.path.join(L.BGM, "2_23_AM.mp3")
LETTER = os.path.join(L.BGM, "手紙のさよなら.mp3")

L.POOLS["react"] += ["stare_standing_marmot", "flip_emo_cat_hair"]
L.POOLS["calm"] += ["lick_talking_goat", "eat_chips_cat", "stand_real_sheep"]
# 募金した猫（毎年コンビニのレジで募金していた人）・福祉の現場の猫（配食や見守りの団体の人）。どちらも被害者側
L.POOLS["donor"] = ["sad_banana_cat_cry", "sad_black_dog", "sulk_hungry_cat", "realize_wet_cat_stare", "sleepy_old_memories_cat",
                    "blank_black_cat_zoning_out", "snore_snoring_dog"]
L.POOLS["genba"] = ["work_typing_cat", "call_customer_service_cat", "wakeup_dog_hits_bowl", "work_dog_staring_computer",
                    "think_bike_front_seat_cat", "despair_dramatic_kitten", "leave_cat_leaves_home"]
L.FALLBACK["donor"] = ["react", "calm"]
L.FALLBACK["genba"] = ["calm", "react"]
CONV, PRESS, OFFICE, BANK, SCHOOL, ROOM, BOARD, SNS, MEET = ("bg15_convenience", "bg07_press", "bg25_office_desk", "bg20_counter",
                                                            "bg21_school_gate", "bg02_room", "bg03_blackboard", "bg09_sns",
                                                            "bg05_meeting")
STING = {"file": KAMI, "len": 3.5, "gain": -14}


def don(say, b=CONV, **kw):
    return solo(b, "@donor", DON, say, side=kw.pop("side", "L"), **kw)


def gen(say, b=OFFICE, **kw):
    return solo(b, "@genba", GEN, say, side=kw.pop("side", "R"), **kw)


def one(b, sub, **kw):
    return dict(bg=bg(b), sub=sub, cats=[cat("@calm", "博識な猫", 470, h=640)], **kw)


def two(b, sub, **kw):
    return dict(bg=bg(b), cats=[cat("@react", "ニュース猫", 500, h=700), cat("@calm", "博識な猫", 1430, h=700)], say=sub,
                text_top=True, **kw)


def ex(b, text, **kw):
    return expl(b, [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "", text, dur=kw.pop("dur", 3.6), **kw)


def ask(**kw):
    return dict(card=None, layers=[pt("yuruseru")], dur=kw.pop("dur", 2.8), se=kw.pop("se", "doon_heavy"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=5.0, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        ask(),   # 本編の一番最初にも問いかけ（10/12 ユーザー指定）
        # ---- 1. つかみ ----
        one(CONV, "毎年10月1日から始まる\n「赤い羽根共同募金」", se="doon_movie", sting={"file": KAMI, "len": 4.0, "gain": -14}),
        one(PRESS, "大臣たちが　胸に赤い羽根をつけて\nテレビに映る\nおなじみの季節", se="page_turn_01", bgm={"file": PURPLE, "gain": -4}),
        one(PRESS, "……ところが今年は\n誰もつけていない", se="shock_piano"),
        nn("え、なんで？", PRESS, se="question_mark_pop_confused_huh"),
        one(PRESS, "政府は今年\n閣僚らの赤い羽根の着用を\n控えている（官房長官の説明）", se="pi"),
        nn("政府ごと\n“つけない”って……\n何があったの", PRESS, se="question_hatena_maou"),
        close(OFFICE, "@react", "ニュース猫", "集めた募金など\n約2億5,000万円が\n使い道の分からないお金に", se=["explosion_dokaan"], sting=STING),
        close(OFFICE, "@react", "ニュース猫", "にっ……\n2億5,000万円！？", se=["game_pokemon_super_effective_hit_big_damage"]),
        don("毎年　コンビニの\nお釣りを\n入れてたのに……", se="tear_drop"),
        dict(bg=bg(BOARD), card=pt("e01_title"), dur=3.4, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        # ---- 2. 赤い羽根って？ ----
        chap("そもそも赤い羽根って？", se="quiz_question_01", bgm={"file": COCOA, "gain": -2, "fade": 0.6}),
        ex(CONV, "赤い羽根共同募金 ＝ 都道府県ごとの\n「共同募金会」が集めて\nその地域の福祉活動に配る募金", dur=4.0, se="pinpon_notice"),
        dia("e02_flow", "集めたお金は　その地域のお年寄りへのお弁当配り・見守り・子ども食堂などへ", right=S, dur=4.8, se="card_flip"),
        ss("北海道で集めたお金は\n北海道の福祉に使われる\n“地元のための募金”なんよ", se="pikon"),
        two(CONV, "北海道では　年末の\n「歳末たすけあい」と合わせて\n毎年6億〜7億円が集まっていた", se="price_display"),
        nn("そのうち2.5億円が\n……消えた？", se="shock_piano"),
        ss("“使い道が分からない”\nまだ“どこに行ったか”も\n全部は分かってない", se="kon"),
        # ---- 3. 何が起きたのか ----
        chap("何が起きたのか", se="doon_heavy", bgm={"file": AM223, "gain": -2, "fade": 0.6}),
        dia("e03_timeline", "2010年ごろから　事務局の男性が　実質1人で会計を担当していたとされる", right=S, dur=4.6, se="xylophone_transition"),
        dia("e03_timeline", "2020年ごろから　無断で現金を引き出し始めたとみられる", right=S, dur=4.4, se="card_flip"),
        dia("e03_timeline", "2026年2月　札幌国税局が　所得税法違反の疑いで査察 → ここで発覚", right=S, dur=4.6, se="pc_warning"),
        dia("e03_timeline", "7月に事務局長を懲戒解雇　9月にさらに約7,000万円の不明 → 総額 約2億5,000万円", right=S, dur=5.0,
            se="card_place", sting=STING),
        close(ROOM, "@react", "ニュース猫", "国税が来て　初めてバレたの！？\n内部じゃ誰も\n気づいてないの！？", se=["explosion_chudoon"]),
        ss("そう\nきっかけは税務署側", se="hyoshigi_01"),
        two(PRESS, "共同募金会は\n「元事務局長が　繰り返し着服していた\n疑いがある」として　刑事告訴を検討", se="page_turn_01"),
        two(PRESS, "元事務局長とは\n連絡が取れていない\nとされる", se="pi"),
        nn("しかも\n連絡つかないの……", PRESS, se="deflate_hyororo"),
        ask(),
        # ---- 4. なぜバレなかったのか ----
        chap("なぜ何年もバレなかったのか", se="doon_heavy"),
        dia("e04_holes", "通帳も印鑑も　1人で管理していた", right=S, dur=4.2, se="card_flip"),
        dia("e04_holes", "足りなくなった分は　年度末に金融機関から借りて穴埋め　監査は決算の日の残高だけ", right=S, dur=5.0,
            se="card_place"),
        nn("夏休みの宿題を\n最終日だけ友だちに借りて\n提出してたみたいな……", se="silly"),
        ss("スケールが\n2.5億円の宿題な", se="tsukkomi_bishi"),
        dia("e04_holes", "理事会が承認していない議事録で　約1億9,000万円を借りていた疑いも", right=S, dur=4.6, se="pc_warning"),
        close(ROOM, "@react", "ニュース猫", "議事録まで……", se=["explosion_chudoon"]),
        ss("外部の監査も何回も入ってたのに\n止められなかった\n役員も　監事も", se="kon"),
        two(MEET, "全国の共同募金会を緊急点検\nほかの都府県は「お金を出す人」と\n「OKを出す人」を分けていた", se="page_turn_02"),
        two(MEET, "北海道の\n「1人に任せきり」は\n突出していた　と指摘されている", se="doon_movie"),
        nn("ほかの県はダブルチェック\nしてたのに　北海道だけ\n“1人で全部”……", MEET, se="deflate_hyororo"),
        close(MEET, "@calm", "博識な猫", "“いい人だから任せる”が\nいちばん危ない", se=["tv_hissatsu_slash_finishing_blow_kill"]),
        # ---- 5. 誰が困ったのか ----
        chap("困っているのは誰？", se="doon_heavy", bgm={"file": LETTER, "gain": -4, "fade": 0.6}),
        dia("e05_genba", "今年度　福祉団体への助成金は　予定額の約5割", OFFICE, right=S, dur=4.4, se="chin_bell_failure_sad_ending"),
        gen("お年寄りに配る\nお弁当の予算が……\n半分……", se="tear_drop"),
        gen("見守りの車の\nガソリン代\nどうしよう……", se="deflate_hyororo"),
        nn("いちばん困ってるの\n現場の人たち\nじゃん……", OFFICE, se="shock_piano"),
        two(CONV, "10月1日　今年の募金がスタート\n出発式は　ボランティアへの\n謝罪から始まった", se="page_turn_01"),
        dia("e05_genba", "札幌の街頭ボランティアは例年の8割減　町内会や企業も協力の見送りが続出", CONV, right=S, dur=5.0, se="card_flip"),
        dia("e05_genba", "置いてくれるお店が見つからず　送れない募金箱も", CONV, right=S, dur=4.2, se="card_place"),
        don("募金したくても\nどこに入れたらいいのか……", se="tear_drop"),
        close(CONV, "@calm", "博識な猫", "1人の“疑い”で\n何千人の善意と\n何千人の支援が止まってる", red=False, se=["shock_piano"]),
        ask(),
        # ---- 6. 全国への影響 ----
        chap("北海道だけの話じゃない", se="doon_heavy", bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        two(PRESS, "政府は今年\n閣僚らの赤い羽根の着用を控えた\n（厚生労働省から各府省に依頼）", se="pi"),
        nn("毎年の“赤い羽根つけてます”の\nニュースが今年ないの\nそういうことか", PRESS, se="idea_newtype_01"),
        two(MEET, "中央共同募金会は　全国に\n「内部通報窓口」をつくるなどの\n再発防止策をまとめている", se="page_turn_01"),
        two(MEET, "札幌市は特別監査を行い\n「会計の責任者」と「印鑑を持つ人」を\n分けるよう指導", se="page_turn_02"),
        ss("今さら？って思うけど\nこれが“ふつう”なんよ", se="kon"),
        # ---- 7. 募金はどうする？ ----
        chap("じゃあ、募金はどうする？", se="quiz_question_02"),
        two(CONV, "北海道新聞の調査では\n例年募金していた人の約4割が\n「今年はしない」", se="pc_warning"),
        two(CONV, "帯広市の町内会では\n「改善が確認できるまで出さない」が\n8割を超えた例も", se="pi"),
        two(SCHOOL, "小学校で羽根を配る\n習慣にも\n反発の声", se="page_turn_01"),
        nn("そりゃ\nそうなるよね……", SCHOOL, se="deflate_hyororo"),
        gen("でも　募金が減ったら\n困るのは……", se="tear_drop"),
        nn("……現場、か", OFFICE, se="shock_piano"),
        ss("“募金しない”も“募金する”も\nどっちも正解\n大事なのは“どこに・どう使われるか”\nを見ること", dur=4.0, se="pikon"),
        dia("e07_choose", "決算や使い道を公開しているか　お金を扱う人が1人じゃないか", right=S, dur=4.6, se="pinpoon_correct"),
        dia("e07_choose", "支援したい団体に直接寄付したり　使い道を指定したりする手もある", right=S, dur=4.6, se="pinpoon_correct"),
        nn("“なんとなく募金”から\n“選んで寄付”の\n時代か", se="idea_newtype_01"),
        # ---- 8. ネットの声 ----
        chap("ネットの声", se="whoosh_shu", dur=1.4, bgm={"file": AM223, "gain": -2, "fade": 0.6}),
        net("@react", "善意を2.5億円も……\n怒りしかない", se="boing_01"),
        net("@react", "国税が来るまで\n誰も気づかないの\n組織として終わってる", se="tsukkomi_bishi"),
        net("@react", "監査って\n何のために\nあるの？", se="question_hatena_maou"),
        net("@react", "通帳と印鑑を\n1人に持たせた時点で\nアウト", se="buzzer_wrong"),
        net("@react", "大臣が羽根つけないの\nむしろ正直でいい", se="kon"),
        net("@react", "募金したいけど\n今年は直接\n団体に送る", se="pikon"),
        net("sleepy_old_memories_cat", "一番かわいそうなのは\n助成が半分になった\n福祉の現場", se="chiin_01"),
        net("@react", "小学生に羽根を\n配らせるの\nもうやめてあげて", se="tear_drop"),
        nn("怒りと　現場への心配と\n半々って感じ", SNS, se="kon"),
        # ---- 9. まとめ ----
        dict(bg=bg(BOARD), inset={"card": pt("e09a_known"), "box": (200, 60, 1720, 860)}, dur=5.0,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)],
             bgm={"file": MIRAI, "gain": -2, "fade": 0.8}, se="chiin_01"),
        dict(bg=bg(BOARD), inset={"card": pt("e09b_unknown"), "box": (200, 60, 1720, 860)}, dur=4.4,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)], se="card_flip"),
        ss("善意は\n仕組みがないと\n守れない", se="tv_professional_poon"),
        nn("募金した人も　現場の人も\n悪くない\n悪いのは……", se="kon"),
        ss("それは　これから\n調べで明らかになる", se="hyoshigi_01"),
        dict(bg=bg(BOARD), card=pt("e10_ending"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(chap("→ 10本目「ハッカーに煽られたクラウド」\n11本目「2,000万円の車を盗んだ疑いでも不起訴」もどうぞ", dur=3.0), chapter_size=66),
    ]


def cuts_full():
    return L.apply_fx(L.allocate(cuts_all()))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "12_akaihane_full.mp4")
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
