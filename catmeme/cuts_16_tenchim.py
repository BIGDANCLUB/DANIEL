"""16_tenchim（てんちむ ナイトブラ「モテフィット」裁判の逆転勝訴）のカット割り。原稿 scripts/16_tenchim.md。作りは 15本目と同じ。

python3 catmeme/cuts_16_tenchim.py          → out/16_tenchim_full.mp4
python3 catmeme/cuts_16_tenchim.py --audio  → 音だけ作り直す

原稿のルール（必ず守る）：
- 控訴審の結果は本人の報告と報道。高裁の判決理由は推測しない。上告・確定は「未確認」と言う
- 金額は意味を分ける（返金の見込み／返金した額／会社の請求額／裁判所が命じた額）
- 本人の主張と会社（YUIKU）の主張を公平に分ける
- 逆転勝訴を「宣伝のやり方に問題がなかった証明」として描かない
- 実在の人は猫で演じない（ユーザー提供の写真は背景に使う）。私生活の未公開情報・憶測は使わない
- 主語になる団体（YUIKU・東京地裁・東京高裁）は団体名の札つきの猫で出し、その場面にはニュース猫・博識な猫は出さない
- 全動画共通：今日の一言・単語の途中で改行しない・最後はチャンネル登録の画面・過去の動画にはふれない
"""
import os
import sys

import cuts_04_leak as L
import render as R

HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("16_tenchim", "15_vambi", "14_japan", "02_october", "01_todai", "04_leak")]
L.PT = os.path.join(HERE, "parts", "16_tenchim")
R.PAN_DIRS = tuple(R.PAN_DIRS) + ("14_japan", "15_vambi", "16_tenchim")
pt, cat, duo, solo, close, dia, expl, chap, net, nn, ss = L.pt, L.cat, L.duo, L.solo, L.close, L.dia, L.expl, L.chap, L.net, L.nn, L.ss
bg = L.bg
N, S = L.N, L.S
PURPLE, COCOA, MIRAI, KAMI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.KAMI, L.NORA
AM223 = os.path.join(L.BGM, "2_23_AM.mp3")
LETTER = os.path.join(L.BGM, "手紙のさよなら.mp3")

L.POOLS["react"] += ["stare_standing_marmot", "flip_emo_cat_hair"]
L.POOLS["calm"] += ["lick_talking_goat", "eat_chips_cat", "stand_real_sheep"]

ORG_COLOR = (90, 60, 150)
ORG_CAT = {"YUIKU（販売元）": "work_typing_cat", "東京地裁": "stare_standing_marmot", "東京高裁": "showoff_gojo_cosplay_cat"}
for _o in ORG_CAT:
    L.ROLE[_o] = ORG_COLOR

# ユーザー提供の写真（本人）＋ AI で作った背景
NEON, FEATHER, EVENT = "bg81_tenchim_neon", "bg82_tenchim_feather", "bg83_tenchim_event"
CHILD, YOUNG = "bg92_tenchim_child", "bg93_tenchim_young"   # 子役時代・若い頃（10/14 ユーザー提供）
COURT, ROOMC, SHELF, MONEY, PAPERS, ADSTUDIO, POST, KIDS = (
    "bg84_courthouse", "bg85_courtroom", "bg86_product_shelf", "bg87_refund_money", "bg88_contract_papers", "bg89_ad_studio",
    "bg90_phone_post", "bg91_tv_studio_kids")
STUDIO, TIMELINE, AGENCY, SEMINAR, COUNTER = "bg70_youtube_studio", "bg79_timeline", "bg78_agency_office", "bg75_seminar_hall", \
    "bg80_counter_rocket"
ROOM, BOARD = "bg02_room", "bg03_blackboard"
V_CASH, V_HANDS, V_PHONE_W, V_HAND, V_MEET, V_CHART, V_NIGHT, V_SHIBUYA = (
    "v06_cash_counting", "v20_smartphone_hands", "v18_smartphone_woman", "v22_smartphone_hand", "v14_business_meeting",
    "v11_stock_chart_blue", "v05_city_night_river", "v09_shibuya_crossing_aerial")


def two(b, sub, **kw):
    return dict(bg=bg(b), cats=[cat("@react", "ニュース猫", 500, h=700), cat("@calm", "博識な猫", 1430, h=700)], say=sub,
                text_top=True, **kw)


def ex(b, text, **kw):
    return expl(b, [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "", text, dur=kw.pop("dur", 3.6), **kw)


def org(b, who, sub, **kw):
    """団体の猫だけをまん中に置く（10/14 ユーザー指定）。"""
    return dict(bg=bg(b), cats=[cat(ORG_CAT[who], who, 960, h=720)], say=sub, text_top=True, **kw)


def photo(b, sub, **kw):
    """本人の写真の背景。顔に字幕がかからないよう、字幕は下の帯（説明モード）で出し、猫は右下に小さく。"""
    return dict(bg=bg(b), cats=[cat("@react", "ニュース猫", 1750, h=360, bottom=650, float=True)], say="", text_top=True,
                explain=sub, no_pop=True, dur=kw.pop("dur", 4.6), **kw)


def card(c, sub, b=BOARD, **kw):
    return dia(c, sub, b, right=S, dur=kw.pop("dur", 5.4), se=kw.pop("se", "card_flip"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=5.0, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- 1. 3億8,000万円の賠償命令が取り消し（0:00〜0:40）----
        nn("3億8,000万円の\n支払い命令が……\n0円に！？", V_CASH, se=["jan", "explosion_chudoon"], bgm={"file": PURPLE, "gain": -4}),
        photo(NEON, "2026年10月14日　人気YouTuberのてんちむさんが\nナイトブラ「モテフィット」裁判の控訴審の結果を報告", se="doon_movie"),
        ss("2024年の一審では\n約3億8,457万円の\n支払いを命じられていた", COURT, se="pi"),
        org(COURT, "東京高裁", "控訴審では\nその支払い命令が\nすべて取り消し（本人の報告）", se="page_turn_02"),
        ss("さらに\n会社側に約224万円の\n支払い命令が出たという", COURT, se="pikon"),
        dict(bg=bg(COURT), card=pt("e01_title"), dur=3.6, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        nn("負けてたのが\n逆に払ってもらう側に……", COURT, se="shock_piano"),
        ss("差し引きで見ると\n約3億8,000万円の\n大逆転", V_CASH, se="price_display"),
        nn("宝くじの1等より\n大きい……", V_CASH, se="question_hatena_maou"),
        ss("この話\nお金の数字がたくさん出てくる\n最初に整理しよう", BOARD, se="kon"),
        card("e01_money", "金額は4種類　全部べつもの", dur=5.6),
        ss("約6年間の騒動を\n順番に見ていこう", TIMELINE, se="tv_professional_poon"),
        # ---- 2. てんちむの経歴（0:40〜1:30）----
        chap("てんちむって\nどんな人？", se="doon_heavy", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        card("e02_profile", "1993年生まれ　子役時代は橋本甜歌の名前で活動", b=KIDS),
        photo(CHILD, "子役時代は「橋本甜歌」の名前で活動\nNHK「天才てれびくんMAX」にも出演していた", se="jan"),
        nn("子役\nだったの！？", KIDS, se=["explosion_chudoon"]),
        ss("その後は\nギャル系雑誌の\nモデルとしても活躍", ADSTUDIO, se="pi"),
        photo(YOUNG, "2016年に　YouTubeチャンネルを開設", se="pikon"),
        ss("美容・ファッション\n日常の動画で\n人気を集めた", STUDIO, se="pi"),
        ss("2024年5月の時点で\nチャンネル登録者は\n約165万人", STUDIO, se="pikon"),
        nn("子役→モデル→YouTuber\n芸歴がめちゃくちゃ長い", STUDIO, se="idea_newtype_01"),
        ss("人気が出ると\n商品のプロデュースにも\n活動を広げた", ADSTUDIO, se="kon"),
        nn("ここで出てくるのが\n問題のナイトブラ……", SHELF, se="question_hatena_maou"),
        # ---- 3. 2020年の豊胸隠し騒動（1:30〜2:40）----
        ss("順調だった人気に\nある日\n大きな落とし穴", ADSTUDIO, se="kon"),
        chap("2020年\n豊胸隠し騒動", se="doon_heavy", bgm={"file": AM223, "gain": -2, "fade": 0.6}),
        card("e03_who", "てんちむさんはプロデュースと宣伝　売っていたのはYUIKU株式会社", b=SHELF),
        nn("てんちむさんが\n自分で売ってた\nわけじゃないんだ", SHELF, se="question_mark_pop_confused_huh"),
        ss("つくって売るのは会社\nてんちむさんは\n“広告塔”の立場", SHELF, se="pi"),
        card("e03_who", "過去の豊胸手術を公表しないまま　バストケアの商品を宣伝", b=SHELF, se="card_place"),
        ss("ナイトブラのほかに\nサプリの宣伝も\n問題になった", SHELF, se="pi"),
        two(V_PHONE_W, "2020年\nこのことが明らかになり\n大炎上", se="pc_warning"),
        ss("“効果を信じて買ったのに”\nと宣伝の内容に\n疑問や批判が集まった", V_PHONE_W, se="kon"),
        ss("本人は謝罪し\n購入した人に\n自分のお金で返金すると表明", V_PHONE_W, se="pi"),
        nn("自腹で\n返金……！？", V_PHONE_W, se=["explosion_dokaan"]),
        ss("ふつう返金は\n売った会社がやるもの\n宣伝した人が払うのは異例", V_PHONE_W, se="kon"),
        ss("インフルエンサーの宣伝は\n“この人が使ってるなら”\nという信頼で売れる", ADSTUDIO, se="pikon"),
        nn("だから\n隠しごとがあると\n信頼が一気に崩れる", ADSTUDIO, se="deflate_hyororo"),
        photo(EVENT, "本人は当時の宣伝について　ファンや購入者の信頼を裏切ったと謝罪している", se="kon"),
        # ---- 4. 返金負担は推定4億3,000万円（2:40〜3:35）----
        ss("では返金に\nいくらかかったのか", MONEY, se="kon"),
        chap("返金の負担は\n推定4億3,000万円", se="doon_heavy"),
        card("e04_money", "2020年11月の発表　返金の見込みは約3億7,000万円超", b=MONEY),
        ss("本人確認や返品の確認が取れた\n約3万件の購入者への\n返金を進めると説明", MONEY, se="pi"),
        ss("この金額には\n販売元への手数料30%も\n入っていた", MONEY, se="kon"),
        nn("返金するのに\n手数料まで……", MONEY, se="question_hatena_maou"),
        card("e04_money", "賠償の見込みも合わせ約4億3,000万円（本人の説明）", b=MONEY, se="card_place"),
        nn("4億3,000万円……\n個人で！？", MONEY, se=["explosion_chudoon"]),
        card("e04_money", "会社には総額約2億2,000万円を送金", b=MONEY),
        ss("大事なのは\nこれは当時の“負担の見込み”\n後の裁判の賠償命令とは別", MONEY, se="kon"),
        ss("お金が足りず\n銀座のクラブなどでも\n働いたと報じられた", "bg76_roppongi_night", se="pi"),
        ss("六本木のショーレストランで\nダンサーとしても\n働いたと報じられた", "bg76_roppongi_night", se="pi"),
        nn("YouTuberが\n返金のために\n夜の仕事まで……", "bg76_roppongi_night", se="tear_drop"),
        # ---- 5. 返金完了後にメーカーと対立（3:35〜4:25）----
        ss("返金が終わっても\n話は終わらなかった", PAPERS, se="kon"),
        chap("返金のあと\n会社と対立", se="whoosh_shu", bgm={"file": LETTER, "gain": -4, "fade": 0.6}),
        two(V_HANDS, "2021年4月\n約2万人への返金完了を\n報告（3億円以上）", se="pinpoon_correct"),
        nn("これで\n一件落着……\nじゃなかった", V_HANDS, se="shock_piano"),
        ss("送ったお金が\nちゃんと返金に使われたのか\nで言い分がぶつかった", PAPERS, se="kon"),
        card("e05_conflict", "てんちむ側「振込の明細が示されていない」", b=PAPERS),
        org(PAPERS, "YUIKU（販売元）", "会社側は\n“返金の数字は\n報告していた”と反論", se="page_turn_01"),
        card("e05_conflict", "YUIKU側「1月25日時点で対象23,142件・完了12,321件と伝えていた」", b=PAPERS, se="card_place"),
        ss("返金の窓口だった法律事務所は\n“会社から受け取ったリストに\n不備があった”と告知", PAPERS, se="kon"),
        ss("リストでは返金済みなのに\n実際は返金されていない\nという問い合わせもあった", PAPERS, se="pi"),
        nn("返金したはずの人に\n返金されてない……！？", PAPERS, se="shock_piano"),
        ss("売上や利益の数字でも\n両方の言い分は\n大きく食い違った", V_CHART, se="pi"),
        ss("てんちむ側は\n売上を37億円（争いあり）とみて\n会社が負担すべきと主張", V_CHART, se="kon"),
        org(V_CHART, "YUIKU（販売元）", "会社側は\n2020年の時点の利益は\n337万円にすぎないと主張", se="page_turn_02"),
        nn("37億円と\n337万円……\n桁がちがいすぎる", V_CHART, se=["explosion_chudoon"]),
        nn("どっちが正しいかは\n裁判へ……", V_CHART, se="question_hatena_maou"),
        # ---- 6. 約5億円の賠償請求と一審敗訴（4:25〜5:25）----
        ss("そしてついに\n法廷へ", ROOMC, se="kon"),
        chap("約5億円の請求と\n一審敗訴", se="doon_heavy", bgm={"file": AM223, "gain": -2, "fade": 0.6}),
        card("e06_counter", "2021年3月　てんちむ側がお金の使い道の説明を求めて提訴", b=ROOMC),
        card("e06_counter", "会社側は「反訴」で約5億円を請求", b=ROOMC, se="card_place"),
        nn("反訴って\nなに？", ROOMC, se="question_mark_pop_confused_huh"),
        ss("訴えられた側が\n同じ裁判の中で\n逆に訴え返すこと", ROOMC, se="pi"),
        ss("会社側は\n“豊胸のことを説明しなかった\n説明義務違反”などを主張", ROOMC, se="kon"),
        org(COURT, "東京地裁", "2024年12月16日\n一審の判決", se="jan"),
        card("e06_ruling1", "てんちむ側の請求は退けられ　3億8,457万4,504円の支払い命令", b=COURT),
        nn("ほぼ\n会社の言い分どおり……", COURT, se="deflate_hyororo"),
        org(COURT, "YUIKU（販売元）", "会社側も\n“当社の勝訴”と\n発表した", se="page_turn_01"),
        ss("弁護士の解説では\n“勝訴しても\n回収できないこともある”という指摘も", ROOMC, se="pi"),
        ss("返金の取り決めを\n書面で交わしていなかったことも\n争点になったと報じられた", PAPERS, se="kon"),
        ss("本人は\n“厳しい結果”として\n受け止めた", PAPERS, se="pi"),
        # ---- 7. 子育てと裁判、仕事への復帰（5:25〜6:15）----
        ss("敗訴の少し前\n本人の生活も\n大きく変わっていた", STUDIO, se="kon"),
        chap("子育てと裁判\nそして復帰", se="whoosh_shu", bgm={"file": COCOA, "gain": -2, "fade": 0.6}),
        card("e07_life", "2023年8月に無期限の活動休止を発表", b=STUDIO),
        card("e07_life", "2024年4月に出産を報告　5月にYouTubeを含む活動の再開を発表", b=STUDIO, se="card_place"),
        ss("復帰の理由のひとつは\n巨額の賠償を\n払う可能性だったと説明", STUDIO, se="pi"),
        ss("“2億とか3億とか\nそんなやさしい額じゃない”\nと話していた（報道）", STUDIO, se="kon"),
        ss("“今から普通の会社員として\n働くのは難しい”とも\n語っていた（報道）", STUDIO, se="pi"),
        ss("一時は\n自己破産の可能性にも\nふれていた", V_NIGHT, se="pi"),
        nn("子育てしながら\n数億円の裁判……", V_NIGHT, se="tear_drop"),
        ss("2025年1月\n控訴すると報告", COURT, se="jan"),
        # ---- 8. 2026年10月14日の大逆転（6:15〜7:10）----
        ss("そして迎えた\n控訴審の判決", COURT, se="kon"),
        chap("2026年10月14日\n大逆転", se="doon_heavy", bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        org(COURT, "東京高裁", "控訴審の結果\n一審の約3億8,000万円の\n支払い命令は取り消し", se=["jan", "explosion_chudoon"]),
        card("e08_appeal", "本人の説明では支払いは0円　会社側に約224万円の支払い命令", b=COURT),
        nn("3億8,000万円が\n0円に！？", COURT, se=["explosion_dokaan"]),
        photo(FEATHER, "本人は「諦めずに闘い続けてきて本当によかった」と\n喜びとファンへの感謝をつづった（報道）", se="pinpoon_correct"),
        ss("SNSでは\n驚きや祝福の声が\n広がった", POST, se="pi"),
        ss("“大逆転だな”\n“圧倒的勝訴”などの声が\n紹介された（報道より）", POST, se="pikon"),
        nn("でも\nなんで逆転したの？", COURT, se="question_mark_pop_confused_huh"),
        card("e08_appeal", "判決の理由・確定したかは　10月14日時点で未確認", b=COURT, se="card_place"),
        ss("理由について\nいろいろな推測が出ているけど\nここでは決めつけない", COURT, se="kon"),
        ss("会社側が\n最高裁に上告するかどうかも\nまだ分からない", COURT, se="pi"),
        nn("まだ\n終わりとは\n限らないのか", COURT, se="question_hatena_maou"),
        # ---- 9. 裁判に勝っても消えない問題（7:10〜8:05）----
        ss("ここで\n大事な話をしておこう", BOARD, se="kon"),
        chap("裁判に勝っても\n消えない問題", se="doon_heavy", bgm={"file": LETTER, "gain": -4, "fade": 0.6}),
        card("e09_issue", "本人は　ファンの信頼を裏切ったと認めている", b=ADSTUDIO),
        card("e09_issue", "裁判の勝ち負けと　宣伝のやり方が正しかったかは　別の話", b=ADSTUDIO, se="card_place"),
        nn("勝訴したから\n全部OK\nではないんだね", ADSTUDIO, se="kon"),
        ss("裁判で争われたのは\n“だれがいくら負担するか”\nというお金の分け方", ADSTUDIO, se="pi"),
        ss("広告塔は\n宣伝の中身に責任\n会社は商品と売り方に責任", SHELF, se="pikon"),
        ss("2023年10月からは\n広告なのに広告と言わない\n“ステマ”が法律で禁止に", ADSTUDIO, se="pi"),
        nn("宣伝のルールは\nどんどん厳しく\nなってる", ADSTUDIO, se="kon"),
        nn("だから\nどっちがどれだけ払うかで\n争いになった", SHELF, se="idea_newtype_01"),
        ss("見る側も\n“広告”かどうかを\n気にするのが大事", V_HAND, se="pi"),
        nn("“好きな人が使ってるから”だけで\n買わない方がいい\nってことか", V_HAND, se="idea_newtype_01"),
        ss("宣伝する側も\n言っていないことが\nないか気をつける時代", V_HAND, se="kon"),
        # ---- 10. まとめ（8:05〜8:50）----
        ss("最後に\n6年間を\nふり返ろう", TIMELINE, se="kon"),
        chap("まとめ", se="whoosh_shu", bgm={"file": MIRAI, "gain": -2, "fade": 0.8}),
        card("e10_summary", "2020年 発覚・返金→2021年 返金完了・裁判へ", b=TIMELINE),
        card("e10_summary", "2024年 一審で約3億8,457万円→2026年10月 控訴審で取り消し", b=TIMELINE, se="card_place"),
        ss("この先\n上告されるか\n判決が確定するかに注目", TIMELINE, se="pi"),
        nn("数億円の返金から\n逆転まで\n6年がかり……", TIMELINE, se="shock_piano"),
        ss("返金した額・会社の請求・\n裁判の命令　どれも\n意味のちがうお金だった", MONEY, se="kon"),
        nn("数字だけ見て\n判断しちゃダメ\nってことだね", MONEY, se="idea_newtype_01"),
        ss("インフルエンサーの宣伝と\n信頼のあり方を\n考えさせられる騒動だった", V_SHIBUYA, se="tv_professional_poon"),
        dict(bg=bg(TIMELINE), card=pt("e11_ending"), dur=3.2, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


def cuts_full():
    return L.apply_fx(L.allocate(cuts_all(), max_use=8))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "16_tenchim_full.mp4")
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
