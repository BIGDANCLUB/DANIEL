"""17_imamori（元戦隊ヒロイン・今森茉耶の経歴と、2026年10月のSNS騒動・発信休止）のカット割り。原稿 scripts/17_imamori.md。

python3 catmeme/cuts_17_imamori.py          → out/17_imamori_full.mp4
python3 catmeme/cuts_17_imamori.py --audio  → 音だけ作り直す

原稿のルール（必ず守る）：
- 公式発表（事務所・テレビ朝日）／週刊誌の報道（疑惑）／本人のSNS・動画の発言を分けて言う
- 不倫・交際は「疑惑」。相手の名前は出さない（一般の人・確認できない人）
- 降板の公式の理由は「20歳未満の飲酒」。不倫疑惑ではない
- 妊娠の経緯・結果は推測しない。妊娠の経験そのものを不祥事として扱わない。LINE の関係者は推測しない・個人情報は出さない
- 本人のつらさを笑いにしない：8〜10章は落ち着いた猫と静かな効果音だけ（驚き・爆発の演出はしない）
- 実在の人は猫で演じない。写真も使わない（背景はAIのイラスト）
- 主語になる団体（事務所・テレビ朝日・東映・週刊誌）は団体名の札つきの猫だけで出す
- 全動画共通：今日の一言・単語の途中で改行しない・最後はチャンネル登録の画面・過去の動画にはふれない
"""
import os
import sys

import cuts_04_leak as L
import render as R

HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("17_imamori", "16_tenchim", "15_vambi", "14_japan", "02_october", "01_todai")]
L.PT = os.path.join(HERE, "parts", "17_imamori")
R.PAN_DIRS = tuple(R.PAN_DIRS) + ("14_japan", "15_vambi", "16_tenchim", "17_imamori")
pt, cat, duo, solo, close, dia, expl, chap, net, nn, ss = L.pt, L.cat, L.duo, L.solo, L.close, L.dia, L.expl, L.chap, L.net, L.nn, L.ss
bg = L.bg
N, S = L.N, L.S
PURPLE, COCOA, MIRAI, KAMI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.KAMI, L.NORA
AM223 = os.path.join(L.BGM, "2_23_AM.mp3")
LETTER = os.path.join(L.BGM, "手紙のさよなら.mp3")

L.POOLS["react"] += ["stare_standing_marmot", "flip_emo_cat_hair"]
L.POOLS["calm"] += ["lick_talking_goat", "eat_chips_cat", "stand_real_sheep"]
# 本人がつらい話をする章で使う、落ち着いた猫（ふざけた動き・叫ぶ猫は入れない）
L.POOLS["quietN"] = ["sulk_hungry_cat", "sad_black_dog", "realize_wet_cat_stare", "blank_black_cat_zoning_out",
                     "sleepy_old_memories_cat", "think_bike_front_seat_cat", "stare_big_eyes_tabby_kitten"]
L.POOLS["quietS"] = ["calm_black_face_sheep", "stare_interviewer_cat", "work_typing_cat", "talk_orange_white_sitting_cat",
                     "stand_real_sheep", "listen_dancing_dog"]
L.FALLBACK["quietN"] = ["calm"]
L.FALLBACK["quietS"] = ["calm"]
QN, QS = ("@quietN", "ニュース猫"), ("@quietS", "博識な猫")

ORG_COLOR = (90, 60, 150)
ORG_CAT = {"事務所 seju": "work_typing_cat", "テレビ朝日": "call_customer_service_cat", "東映": "stare_standing_marmot",
           "週刊文春": "peek_what_happen_cat"}
for _o in ORG_CAT:
    L.ROLE[_o] = ORG_COLOR

MAG, HERO, TOYS, TABLOID, IZAKAYA, TVSTA, LOUNGE, CHAT, QUIET, TL = (
    "bg94_magazine_stand", "bg95_hero_studio", "bg96_hero_toys", "bg97_tabloid_desk", "bg98_izakaya_night", "bg99_tv_station",
    "bg100_lounge_night", "bg101_phone_chat", "bg102_quiet_room", "bg103_timeline2")
STUDIO, POST, BOARD = "bg70_youtube_studio", "bg90_phone_post", "bg03_blackboard"
V_PHONE_W, V_HANDS, V_HAND, V_NIGHT, V_SHIBUYA, V_TYPE, V_SLEEP = (
    "v18_smartphone_woman", "v20_smartphone_hands", "v22_smartphone_hand", "v05_city_night_river", "v09_shibuya_crossing_aerial",
    "v02_typing_keyboard_closeup", "v03_cat_sleeping_bed")


def two(b, sub, **kw):
    return dict(bg=bg(b), cats=[cat("@react", "ニュース猫", 500, h=700), cat("@calm", "博識な猫", 1430, h=700)], say=sub,
                text_top=True, **kw)


def org(b, who, sub, **kw):
    """団体の猫だけをまん中に置く（10/14 ユーザー指定）。"""
    return dict(bg=bg(b), cats=[cat(ORG_CAT[who], who, 960, h=720)], say=sub, text_top=True, **kw)


def card(c, sub, b=BOARD, **kw):
    return dia(c, sub, b, right=S, dur=kw.pop("dur", 5.8), se=kw.pop("se", "card_flip"), **kw)


def qn(say, b=QUIET, **kw):
    """落ち着いた場面：ニュース猫（静かな猫）がしゃべる。"""
    return duo(b, QN, QS, say, who="L", **kw)


def qs(say, b=QUIET, **kw):
    """落ち着いた場面：博識な猫（静かな猫）がしゃべる。"""
    return duo(b, QN, QS, say, who="R", **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=5.0, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- 1. 再出発からわずか6日で発信休止（0:00〜0:40）----
        nn("元戦隊ヒロインが\nYouTubeで再出発……\nわずか6日で発信休止！？", HERO, se=["jan", "explosion_chudoon"], bgm={"file": AM223, "gain": -4}),
        ss("2025年\n『ナンバーワン戦隊ゴジュウジャー』の\nヒロインだった今森茉耶さん", HERO, se="doon_movie"),
        ss("週刊誌の不倫疑惑\nそして20歳未満の飲酒で\n番組を降板", HERO, se="pi"),
        ss("2026年10月8日\nYouTubeに初投稿\n10月14日　すべての発信を休止と表明", V_HANDS, se="pi"),
        nn("降板から\n約1年での再出発\nだったのに……", V_HANDS, se="shock_piano"),
        dict(bg=bg(TL), card=pt("e01_title"), dur=3.8, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        nn("再出発したばかりで\nなぜまた騒動に？", TL, se="question_mark_pop_confused_huh"),
        ss("公式の発表・週刊誌の報道・\n本人の発言を分けながら\n順番に見ていこう", TL, se="tv_professional_poon"),
        # ---- 2. 経歴（0:40〜1:25）----
        chap("今森茉耶って\nどんな人？", se="doon_heavy", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        card("e02_profile", "2006年3月26日生まれ　宮崎県出身", b=MAG),
        ss("中学生のころから\nTikTokで活動していた", V_PHONE_W, se="pi"),
        card("e02_profile", "2022年に芸能事務所 seju と契約　2023年にグラビアデビュー", b=MAG, se="card_place"),
        two(MAG, "そして\n「ミスマガジン2023」で\nグランプリ", se="jan"),
        nn("デビューの年に\nいきなりグランプリ！？", MAG, se=["explosion_chudoon"]),
        ss("ミスマガジンは\n多くの人気女優を生んだ\n講談社のオーディション", MAG, se="pi"),
        ss("雑誌やCMにも出て\n知名度が一気に上がった", MAG, se="pikon"),
        ss("写真集は\n地元の宮崎と\nフィリピンのセブ島で撮影（報道）", MAG, se="pi"),
        nn("TikTokから\nグラビア　そして……", MAG, se="idea_newtype_01"),
        ss("次に決まったのが\nあの有名シリーズの\nヒロインだった", MAG, se="kon"),
        # ---- 3. 戦隊初の女性ブラック（1:25〜2:15）----
        ss("グランプリの先に\n待っていたのは……", MAG, se="kon"),
        chap("戦隊シリーズ初の\n女性ブラック", se="doon_heavy", bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        card("e03_sentai", "2025年2月放送開始　一河角乃／ゴジュウユニコーン役", b=HERO),
        nn("シリーズ初の\n女性ブラック！？", HERO, se=["explosion_chudoon"]),
        ss("ブラックは\nこれまで男性の戦士が\n続いてきた色", HERO, se="pi"),
        ss("しかも放送開始時は18歳\nスーパー戦隊50周年の\n記念作品のヒロイン", HERO, se="pi"),
        card("e03_sentai", "戦隊シリーズは若手俳優の登竜門と言われる", b=TOYS, se="card_place"),
        ss("戦隊出身から\n人気俳優になった人は多い", TOYS, se="pikon"),
        nn("将来を期待される\nスタートだった", TOYS, se="idea_newtype_01"),
        ss("ところが\n放送中に\n大きく変わっていく", TOYS, se="kon"),
        # ---- 4. 2025年9月の不倫疑惑報道（2:15〜3:05）----
        ss("順調に見えた放送中\n週刊誌が動いた", HERO, se="kon"),
        chap("2025年9月\n週刊誌の疑惑報道", se="doon_heavy", bgm={"file": AM223, "gain": -2, "fade": 0.6}),
        org(TABLOID, "週刊文春", "9月10日発売の週刊文春が\n共演していたスーツアクターとの\n不倫疑惑を報道", se="page_turn_02"),
        card("e04_bunshun", "相手とされたのは既婚のスーツアクター（報道）", b=TABLOID),
        card("e04_bunshun", "9月18日発売の号では　プロサッカー選手との交際疑惑も", b=TABLOID, se="card_place"),
        org(TABLOID, "東映", "制作の東映は\nプライバシーを理由に\n回答しなかった", se="page_turn_01"),
        ss("東映はこの報道の前の9月1日\nそのスーツアクターの降板を\n持病の悪化として発表していた", HERO, se="pi"),
        ss("報道では\n撮影のスケジュールが\n一時見直されたとも伝えられた", HERO, se="pi"),
        ss("本人は\nこの報道について\n何も話さなかった", V_PHONE_W, se="kon"),
        ss("大事なのは\nどちらも週刊誌の報道で\n確定した事実ではないこと", BOARD, se="kon"),
        ss("相手とされる人の名前も\nこの動画では出さない", BOARD, se="pi"),
        nn("特撮ファンの間では\n大きな話題に\nなったけど……", V_HANDS, se="question_hatena_maou"),
        ss("そして\n番組を降りた公式の理由は\nこの疑惑ではない", BOARD, se="hyoshigi_01"),
        # ---- 5. 20歳未満の飲酒で契約解除・降板（3:05〜4:10）----
        ss("その2か月後\n事態はもっと大きくなる", TABLOID, se="kon"),
        chap("20歳未満の飲酒で\n契約解除・降板", se="doon_heavy"),
        org(TVSTA, "事務所 seju", "2025年11月8日\n“20歳未満で飲酒していた\n事実を確認”として契約解除", se="page_turn_02"),
        card("e05_cancel", "テレビ朝日も降板を発表　理由は20歳未満の飲酒", b=TVSTA),
        org(TVSTA, "テレビ朝日", "番組サイトで\n降板の申し入れに\n同意したと発表", se="page_turn_01"),
        ss("本人もInstagramで\n“非常に恥ずべき行為”と\n謝罪した", V_PHONE_W, se="kon"),
        nn("ヒロインが\n放送の途中で\nいなくなる……", HERO, se="shock_piano"),
        ss("当時は19歳\n20歳の誕生日まで\nあと4か月ほどだった", IZAKAYA, se="pi"),
        nn("ここが\n公式の理由なんだね", BOARD, se="pikon"),
        card("e05_age", "成人は18歳から　でもお酒は20歳から", b=IZAKAYA),
        nn("19歳は\n大人なのに\nお酒はダメ……", IZAKAYA, se="question_mark_pop_confused_huh"),
        ss("2022年に成人年齢は\n18歳になったけど\nお酒とたばこは20歳のまま", IZAKAYA, se="pi"),
        ss("出演の契約では\n法律を守ることは大前提\n子ども向け番組ならなおさら", HERO, se="kon"),
        org(TVSTA, "テレビ朝日", "11月25日の会見で社長は\n“子供向け番組で\n申し訳ない”と謝罪", se="page_turn_02"),
        ss("本人への損害賠償は\n“検討していない”と\n説明した", TVSTA, se="pi"),
        # ---- 6. 番組の異例の対応（4:10〜4:55）----
        ss("では番組は\nどうしたのか", TVSTA, se="kon"),
        chap("番組の\n異例の対応", se="whoosh_shu", bgm={"file": COCOA, "gain": -2, "fade": 0.6}),
        card("e06_swap", "降板直後の放送は　出演シーンをカット・編集", b=HERO),
        ss("顔の映る場面を\n減らすなどして\n物語を続けた", HERO, se="pi"),
        ss("変身したあとの\nヒーローの姿は\n登場を続けた", HERO, se="pi"),
        card("e06_swap", "11月30日の第40話から　志田こはくさんが同じ役で出演", b=HERO, se="card_place"),
        nn("放送の途中で\n同じ役の人が\n入れ替わった！？", HERO, se=["explosion_chudoon"]),
        org(TVSTA, "東映", "起用の発表は\n降板から1週間後の\n11月15日", se="page_turn_01"),
        ss("物語の中では\n“顔と声が変わった”という\n設定で引き継いだと紹介された", HERO, se="kon"),
        nn("むちゃな設定……\nでも番組を\n止めないための工夫か", HERO, se="question_hatena_maou"),
        ss("志田さんは\n『暴太郎戦隊ドンブラザーズ』で\nヒロインを演じた経験者", HERO, se="pikon"),
        ss("撮り直しや脚本の調整など\n制作の現場には\n大きな負担になったとみられる", HERO, se="kon"),
        nn("一人の行動が\n番組全体に\n影響したんだね", TOYS, se="deflate_hyororo"),
        # ---- 7. YouTubeで再出発（4:55〜5:45）----
        ss("それから\n約11か月", TL, se="kon"),
        chap("2026年10月\nYouTubeで再出発", se="doon_heavy", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        card("e07_youtube", "10月8日にYouTubeへ初投稿（本人の動画・報道）", b=STUDIO),
        card("e07_youtube", "約4か月ラウンジで働いたと説明　パパ活の疑いは否定", b=LOUNGE, se="card_place"),
        ss("芸能界には\n戻らない考えを\n示したと報じられた", STUDIO, se="pi"),
        ss("Instagramでは\n降板のころのことには\n今後触れられないと説明していた（報道）", V_PHONE_W, se="kon"),
        ss("事務所に入らず\n個人で発信できるのが\nYouTubeの場所", STUDIO, se="pikon"),
        ss("2026年3月の\n20歳の誕生日のころにも\nSNSの投稿が賛否を呼んでいた（報道）", V_PHONE_W, se="pi"),
        ss("別のYouTuberの動画では\nいじめや不登校の過去も\n話したと報じられた", STUDIO, se="kon"),
        nn("一からの\n再スタート……", STUDIO, se="idea_newtype_01"),
        ss("ただ　ネットで\n“交際相手”などの\nうわさも出たけど", V_HANDS, se="kon"),
        ss("確認できない話なので\nこの動画では\n扱わない", BOARD, se="pi"),
        # ---- 8. 対談動画での発言（5:45〜6:40）※落ち着いた演出 ----
        ss("再出発から\n4日後", TL, se="kon"),
        chap("対談動画での\n発言が拡散", se="whoosh_shu", bgm={"file": LETTER, "gain": -6, "fade": 0.8}),
        qs("10月12日\nYouTuberの中町JPさんとの\n対談動画が公開された", STUDIO, se="pi"),
        qs("恋愛や結婚\n将来の子どものことなどを\n話す中で", STUDIO, se="pi"),
        qs("高校1年生のころに\n妊娠した経験があると\n本人が話した", QUIET, se="kon"),
        qs("この発言の一部が\nSNSで切り取られて\n広まった", V_HANDS, se="pi"),
        qs("動画のタイトルや\n切り抜きを通じて\n批判の声も集まった", V_HANDS, se="kon"),
        qn("その後どうなったのかは\n公表されていない", QUIET, se="kon"),
        qs("だからこの動画でも\n経緯や結果を\n推測しない", BOARD, se="pi"),
        qn("経験そのものは\n責められることじゃない\nってことだね", QUIET, se="kon"),
        # ---- 9. LINE画像の投稿（6:40〜7:20）----
        chap("LINE画像の投稿と削除", se="whoosh_shu"),
        qs("10月14日未明\n本人がXに\nLINEのやり取りとみられる画像を投稿", CHAT, se="pi"),
        qs("過去の飲酒の問題に\n関係するとみられる\n内容だった（報道）", CHAT, se="kon"),
        qs("画像はすぐに削除されたが\nスクリーンショットが\nネットで広まった", V_HANDS, se="pi"),
        qn("関係者について\nいろいろな憶測も\n出ているけど……", CHAT, se="question_hatena_maou"),
        qs("ほかの人の関わりや\n隠していたことは\n確認されていない", BOARD, se="kon"),
        qs("画像にあった\n個人の情報も\nここでは出さない", BOARD, se="pi"),
        # ---- 10. 謝罪と発信休止（7:20〜8:10）----
        chap("本人が謝罪\nすべての発信を休止", se="whoosh_shu"),
        card("e10_timeline", "10月8日の初投稿から　14日の発信休止まで　わずか6日", b=TL, se="card_place"),
        card("e10_apology", "妊娠の発言について説明・謝罪　その後のことは話せないとした", b=QUIET),
        card("e10_apology", "LINE画像の投稿についても謝罪　しばらくすべての発信をやめると表明", b=QUIET, se="card_place"),
        qs("文書では\n“心がもたず”と\n追い詰められていた気持ちも明かした", QUIET, se="kon"),
        qs("発言については\n“責任感のない発言をしてしまった”と\n反省を述べた（報道）", QUIET, se="pi"),
        qs("投稿はその後\n削除されたと\n報じられている", QUIET, se="pi"),
        qs("YouTube初投稿から\nわずか6日での\n発信休止だった", TL, se="kon"),
        qn("これからの活動が\nいつ再開するかは\n分からない", QUIET, se="kon"),
        # ---- 11. まとめ（8:10〜8:45）----
        chap("まとめ", se="whoosh_shu", bgm={"file": MIRAI, "gain": -4, "fade": 0.8}),
        card("e11_summary", "ミスマガジン2023グランプリ→戦隊ヒロイン→疑惑報道", b=TL),
        card("e11_summary", "飲酒で契約解除・降板→YouTube→発信休止", b=TL, se="card_place"),
        card("e11_note", "20歳未満の飲酒は本人の責任　でも疑惑や私生活の詮索・中傷は別の問題", b=BOARD, dur=5.8),
        qs("責任をとることと\nネットでたたかれ続けることは\n同じじゃない", V_SHIBUYA, se="kon"),
        qn("書きこむ前に\n一度考えたいね", V_SHIBUYA, se="pi"),
        qs("公式の発表か　週刊誌の疑惑か\n本人の発言か\n確かめて見ることも大事", BOARD, se="pikon"),
        qs("ネットに広まった言葉や画像は\n消しても\n完全には消えない", V_HANDS, se="kon"),
        qs("つらいときは\nひとりで抱えず\n相談窓口を頼ってほしい", QUIET, se="pi"),
        qs("厚生労働省の\n「まもろうよ こころ」に\n電話やSNSの窓口がまとめてある", QUIET, se="pi"),
        dict(bg=bg(TL), card=pt("e12_ending"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


def cuts_full():
    return L.apply_fx(L.allocate(cuts_all(), max_use=8))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "17_imamori_full.mp4")
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
