"""15_vambi（ヴァンビの経歴と、2026年10月の逮捕報道・事務所退所）のカット割り。原稿 scripts/15_vambi.md。作りは 14本目と同じ。

python3 catmeme/cuts_15_vambi.py          → out/15_vambi_full.mp4
python3 catmeme/cuts_15_vambi.py --audio  → 音だけ作り直す

原稿のルール（必ず守る）：
- 逮捕は容疑の段階。「〜した疑い」「〜とみられる」。有罪のように言わない（推定無罪）
- 被害を訴えた女性を笑いにしない・詮索しない。確認できない噂（夜遊び・過去の告発など）は使わない
- 実在の人（ヴァンビさん・ゆんさんほか）は猫で演じない。本人の発言は報道どおりの要約だけ。からかわない
- 報道・事務所の発表・本人の説明を分けて言う
- 主語になる団体（太田プロダクション・警視庁）は団体名の札つきの猫で出し、その場面にはニュース猫・博識な猫は出さない
- 全動画共通：今日の一言・単語の途中で改行しない・最後はチャンネル登録の画面・過去の動画にはふれない
"""
import os
import sys

import cuts_04_leak as L
import render as R

HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("15_vambi", "14_japan", "02_october", "01_todai", "04_leak")]
L.PT = os.path.join(HERE, "parts", "15_vambi")
R.PAN_DIRS = tuple(R.PAN_DIRS) + ("14_japan", "15_vambi")
pt, cat, duo, solo, close, dia, expl, chap, net, nn, ss = L.pt, L.cat, L.duo, L.solo, L.close, L.dia, L.expl, L.chap, L.net, L.nn, L.ss
bg = L.bg
N, S = L.N, L.S
PURPLE, COCOA, MIRAI, KAMI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.KAMI, L.NORA
AM223 = os.path.join(L.BGM, "2_23_AM.mp3")
LETTER = os.path.join(L.BGM, "手紙のさよなら.mp3")

L.POOLS["react"] += ["stare_standing_marmot", "flip_emo_cat_hair"]
L.POOLS["calm"] += ["lick_talking_goat", "eat_chips_cat", "stand_real_sheep"]

ORG_COLOR = (90, 60, 150)
ORG_CAT = {"太田プロダクション": "work_typing_cat", "警視庁": "stare_standing_marmot"}
for _o in ORG_CAT:
    L.ROLE[_o] = ORG_COLOR

STAGE, STUDIO, CHAPEL, LIVE, SHORTS, WORLD, SEMINAR, ROPPONGI, POLICE_ST, AGENCY, TIMELINE, COUNTER = (
    "bg69_vkei_stage", "bg70_youtube_studio", "bg71_wedding_chapel", "bg72_live_stream", "bg73_shorts_phone",
    "bg74_world_viewers", "bg75_seminar_hall", "bg76_roppongi_night", "bg77_police_station", "bg78_agency_office",
    "bg79_timeline", "bg80_counter_rocket")
ROOM, BOARD = "bg02_room", "bg03_blackboard"
V_NIGHT, V_POLICE, V_HANDS, V_PHONE, V_PHONE_W, V_HAND, V_MEET, V_CHART, V_SHIBUYA, V_TYPE = (
    "v05_city_night_river", "v16_police_car_lights", "v20_smartphone_hands", "v04_smartphone_man_coat",
    "v18_smartphone_woman", "v22_smartphone_hand", "v14_business_meeting", "v11_stock_chart_blue",
    "v09_shibuya_crossing_aerial", "v02_typing_keyboard_closeup")
STING = {"file": KAMI, "len": 3.5, "gain": -14}


def two(b, sub, **kw):
    return dict(bg=bg(b), cats=[cat("@react", "ニュース猫", 500, h=700), cat("@calm", "博識な猫", 1430, h=700)], say=sub,
                text_top=True, **kw)


def ex(b, text, **kw):
    return expl(b, [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "", text, dur=kw.pop("dur", 3.6), **kw)


def org(b, who, sub, **kw):
    """団体の猫だけをまん中に置く（10/14 ユーザー指定）。"""
    return dict(bg=bg(b), cats=[cat(ORG_CAT[who], who, 960, h=720)], say=sub, text_top=True, **kw)


def card(c, sub, b=BOARD, **kw):
    return dia(c, sub, b, right=S, dur=kw.pop("dur", 5.0), se=kw.pop("se", "card_flip"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=5.0, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- 1. 登録者1,000万人のYouTuberが逮捕（0:00〜0:40）----
        nn("登録者1,000万人の\nYouTuberが\n逮捕……！？", V_POLICE, se=["jan", "explosion_chudoon"], sting={"file": KAMI, "len": 4.0, "gain": -14}),
        ss("2026年10月1日\nヴァンビさんこと\n白井竜樹容疑者（36）", V_POLICE, se="doon_movie", bgm={"file": AM223, "gain": -4}),
        ex(ROPPONGI, "東京・六本木のクラブで\n20代女性の下半身を触った疑い\n東京都迷惑防止条例違反の疑いで現行犯逮捕（報道）", dur=4.6,
           se="pinpon_notice", explain_size=80),
        ss("酒に酔っていたとみられる\nと報じられている", ROPPONGI, se="pi"),
        org(AGENCY, "太田プロダクション", "10月13日\n所属事務所の\n太田プロダクションを退所", se="page_turn_02"),
        dict(bg=bg(TIMELINE), card=pt("e01_title"), dur=3.6, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        ss("まず大前提\n逮捕は“疑い”の段階\n有罪が決まったわけじゃない", se="kon"),
        nn("でも\nなんでそんなに\n大ニュースに？", COUNTER, se="question_mark_pop_confused_huh"),
        ss("“ヴァンゆん”で大ブレイク\n個人で登録者1,000万人を\n日本人最速で達成した人だから", COUNTER, se="pikon"),
        nn("成功した人に\n何があったのか……", COUNTER, se="shock_piano"),
        ss("最初から\n順番に見ていこう", TIMELINE, se="tv_professional_poon"),
        # ---- 2. ヴィジュアル系バンドからYouTuberへ（0:40〜1:35）----
        chap("ヴィジュアル系バンドから\nYouTuberへ", se="doon_heavy", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        card("e02_profile", "本名は白井竜樹さん　2026年10月時点で36歳", b=STAGE),
        two(STAGE, "もともとは\nヴィジュアル系バンド\n「LOG-ログ-」で活動", se="jan"),
        nn("バンドマン\nだったの！？", STAGE, se=["explosion_chudoon"]),
        ss("2019年のイベントでは\nLOG-ログ-が\n一日限定で復活した", STAGE, se="pi"),
        nn("今のイメージから\n全然想像できない", STAGE, se="question_hatena_maou"),
        two(STUDIO, "バンドのあと\nYouTubeの道へ", se="pikon"),
        ss("2018年7月\n女性YouTuberのゆんさんと\nコンビ「ヴァンゆん」を結成", STUDIO, se="jan"),
        nn("ここから\n快進撃が\n始まる……", STUDIO, se="idea_newtype_01"),
        # ---- 3. ヴァンゆんが大ブレイク（1:35〜2:30）----
        chap("ヴァンゆんが\n大ブレイク", se="doon_heavy", bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        two(STUDIO, "ドッキリ・大食い\nデート企画・日常の動画", se="pikon"),
        ss("男女コンビの\nカップルみたいな距離感が\n人気を集めた", STUDIO, se="pi"),
        nn("でも\n付き合ってたの？", STUDIO, se="question_mark_pop_confused_huh"),
        ss("2人は\n“交際はしていない”と\n説明していた", STUDIO, se="kon"),
        nn("付き合ってないのに\nこの距離感……\nそりゃ気になる", STUDIO, se="question_hatena_maou"),
        card("e03_vanyun", "2019年3月に100万人　8月に150万人", b=COUNTER),
        org(AGENCY, "太田プロダクション", "2019年9月\nヴァンゆんが\n太田プロダクションに所属", se="page_turn_01"),
        card("e03_vanyun", "登録者100万人超えのクリエイターの所属は太田プロで初", b=AGENCY, se="card_place"),
        ss("YouTuberが\n芸能事務所に入った\n“第1号”とも言われた", AGENCY, se="pi"),
        nn("YouTuberが\n芸能界の\n仲間入り……", AGENCY, se="idea_newtype_01"),
        ss("その後\n登録者は200万人を超え\nテレビにも出るように", COUNTER, se="pikon"),
        ss("2021年2月には\nYouTubeの公式番組で\nヴァンゆんのドキュメンタリーも決定", V_HANDS, se="pi"),
        nn("YouTube公式にまで\n取り上げられる\nトップ人気……", V_HANDS, se="idea_newtype_01"),
        ss("でも\nその年の暮れに\n大きな騒動が起きる", V_HANDS, se="kon"),
        # ---- 4. 2021年の結婚企画で大炎上（2:30〜3:45）----
        chap("2021年の結婚企画で\n大炎上", se="doon_heavy", bgm={"file": AM223, "gain": -2, "fade": 0.6}),
        two(LIVE, "2021年12月25日\nクリスマスの生配信", se="jan"),
        card("e04_marriage", "企画は「登録者250万人に届いたら結婚」", b=LIVE),
        nn("結婚を\n登録者数で\n決めるの！？", LIVE, se=["explosion_chudoon"]),
        ss("始まった時点は\n約226万人\n約24万人の上積みが必要", LIVE, se="pi"),
        card("e04_marriage", "ゆんさんは「プレゼント企画」と聞いていた（報道）", b=LIVE, se="card_place"),
        nn("本人が\nよく知らないまま\n始まったの……", LIVE, se="shock_piano"),
        two(CHAPEL, "しかも\n結婚式場まで\n押さえていた", se="pc_warning"),
        ss("配信では\nゆんさんが戸惑う様子も\n伝えられた", CHAPEL, se="kon"),
        ss("ネットでは\n“女性の気持ちを考えていない”\nと批判が広がった（報道）", CHAPEL, se="pi"),
        nn("ドッキリの\nノリで済む話\nじゃない……", CHAPEL, se="deflate_hyororo"),
        card("e04_marriage", "結果は約228万人　約1万4,000人増で終了", b=CHAPEL),
        nn("250万人には\n届かなかった", CHAPEL, se="chin_bell_failure_sad_ending"),
        card("e04_after", "翌26日　ヴァンビさんが謝罪の動画", b=STUDIO),
        ss("“全ての責任の所在は僕にある”\nと説明した（報道）", STUDIO, se="kon"),
        card("e04_after", "2022年1月　2人で話し合い　仲直りを報告", b=STUDIO, se="card_place"),
        ss("炎上した理由は\n“相手の気持ちより\n企画が先”に見えたこと", STUDIO, se="pi"),
        nn("数字のための企画が\n裏目に出た……", STUDIO, se="deflate_hyororo"),
        # ---- 5. ヴァンゆん活動休止とゆんの結婚（3:45〜4:30）----
        chap("ヴァンゆん\n活動休止へ", se="whoosh_shu", bgm={"file": LETTER, "gain": -4, "fade": 0.6}),
        two(TIMELINE, "2022年12月1日\nヴァンゆんが\n無期限の活動休止を発表", se="page_turn_01"),
        ss("12月31日で\nコンビとしては休止\nそれぞれ個人の活動へ", TIMELINE, se="pi"),
        two(TIMELINE, "2023年5月\nゆんさんが\nFischer'sのシルクロードさんと結婚を発表", se="jan"),
        ss("過去の結婚企画が\nまた話題になった", TIMELINE, se="kon"),
        ss("2023年9月\nヴァンゆんは\n正式に解散", TIMELINE, se="hyoshigi_01"),
        nn("ここで\n終わり……\nかと思いきや", TIMELINE, se="shock_piano"),
        card("e05_timeline", "スパイダーメーン開設は2022年7月10日　休止の発表より前", b=TIMELINE, dur=5.4),
        nn("休止の前から\nもう新しい\nチャンネルを！？", TIMELINE, se=["explosion_chudoon"]),
        # ---- 6. スパイダーメーンで1,000万人（4:30〜5:55）----
        chap("スパイダーメーンで\n登録者1,000万人", se="doon_heavy", bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        two(SHORTS, "チャンネル名は\n「spider-maaaaaaan」\n（スパイダーメーン）", se="jan"),
        ss("スパイダーマンのような\nコスチュームで\n正体を隠して活動", SHORTS, se="pi"),
        ss("中心は\nショート動画", SHORTS, se="pikon"),
        card("e06_spider", "2023年7月19日　登録者1,000万人　開設から374日", b=COUNTER),
        nn("1年ちょっとで\n1,000万人……！？", COUNTER, se=["explosion_dokaan"]),
        card("e06_spider", "当時の日本最速　それまでの記録は394日", b=COUNTER, se="card_place"),
        two(COUNTER, "そして\n2023年8月5日", se="jan"),
        ss("生配信で\n“正体はヴァンビ”\nと公表", COUNTER, se="doon_movie"),
        ss("“日本一のYouTuberになります”\nと宣言した（報道）", COUNTER, se="pikon"),
        ss("人気YouTuberのヒカルさんとの\nコラボ動画も公開され\n大きな反響に", COUNTER, se="pi"),
        nn("炎上した人が\n覆面で\n日本一に……", COUNTER, se="shock_piano"),
        ss("なぜ\nここまで伸びたのか\n5つに分けて見てみよう", BOARD, se="kon"),
        card("e06_why", "① 言葉がいらないショート動画", b=SHORTS),
        ss("見ただけで分かるから\n日本語が分からない人にも\n伝わる", SHORTS, se="pi"),
        card("e06_why", "② 海外の視聴者にも届く", b=WORLD, se="card_place"),
        ss("視聴者が\n日本だけじゃなく\n世界に広がる", WORLD, se="pikon"),
        card("e06_why", "③ ショートは広がるのが速い", b=SHORTS),
        ss("スマホで次々に流れてくるから\n登録してない人にも\n見つけてもらえる", SHORTS, se="pi"),
        card("e06_why", "④ 覆面で「だれ？」と話題に", b=SHORTS, se="card_place"),
        card("e06_why", "⑤ ヴァンゆん時代とは　まったく別のスタイル", b=STUDIO),
        ss("しゃべりと企画のコンビから\n言葉のいらない\n一人の短い動画へ", STUDIO, se="kon"),
        nn("やり方を\nまるごと\n変えたんだ", STUDIO, se="idea_newtype_01"),
        ss("2023年11月には\nチャンネル名も\n改められた", SHORTS, se="pi"),
        ss("その後\n340日で達成する人が現れて\n記録は更新された", COUNTER, se="pi"),
        # ---- 7. 実業家へ転身（5:55〜6:35）----
        chap("実業家へ\nHERO'ZZを設立", se="whoosh_shu", bgm={"file": MIRAI, "gain": -4, "fade": 0.6}),
        card("e07_heroz", "2024年1月　株式会社HERO'ZZ 設立", b=SEMINAR),
        ss("2024年3月26日に\n新会社とサービスの\n記者会見を開いた", SEMINAR, se="pi"),
        card("e07_heroz", "発信する人を育てる学校　学長はヴァンビさん", b=SEMINAR, se="card_place"),
        ss("登録者を増やすノウハウを\n教える学校", SEMINAR, se="pi"),
        nn("1,000万人の経験を\n教える側に……", SEMINAR, se="idea_newtype_01"),
        ss("受講生は\n累計2,000人以上と\n運営が発表している", SEMINAR, se="pikon"),
        ss("2024年7月には\n大学のオープンキャンパスで\n高校生向けの特別講義も", SEMINAR, se="pi"),
        ss("2026年5月には\n開校3年目に入った\nと発表していた", SEMINAR, se="kon"),
        nn("順調に見えた\nその5か月後……", V_NIGHT, se="shock_piano"),
        ss("動画をつくる人から\n会社を経営する人へ\n活動を広げていった", V_MEET, se="kon"),
        # ---- 8. 2026年10月、六本木で現行犯逮捕（6:35〜7:45）----
        chap("2026年10月\n六本木で現行犯逮捕", se="doon_heavy", bgm={"file": AM223, "gain": -2, "fade": 0.6}),
        card("e08_arrest", "10月1日の午前4時前　東京・六本木のクラブ", b=ROPPONGI),
        card("e08_arrest", "20代女性の下半身を触った疑い　東京都迷惑防止条例違反", b=ROPPONGI, se="card_place"),
        org(POLICE_ST, "警視庁", "110番通報を受けて\n駆けつけた警察官が\nその場で現行犯逮捕（報道）", se="siren_police"),
        org(POLICE_ST, "警視庁", "酒に酔っていたとみられる\n認否は\n明らかにしていない", se="page_turn_02"),
        nn("認めているかどうかも\nまだ分からない", V_POLICE, se="question_hatena_maou"),
        org(AGENCY, "太田プロダクション", "事務所は当初\n“報道を見て知った\n事実関係を確認中”", se="page_turn_01"),
        ss("人気YouTuberの逮捕として\n一気に報道が広がった", V_PHONE, se="pi"),
        nn("1,000万人が\n見ていた人だから\n影響も大きい", V_PHONE, se="deflate_hyororo"),
        card("e08_presume", "逮捕は「疑い」の段階　有罪が決まったわけではない", b=BOARD),
        card("e08_presume", "起訴・不起訴などは発表されていない（10月14日時点）", b=BOARD, se="card_place"),
        ss("それに\n被害を訴えた女性を\n詮索したり責めたりしない", BOARD, se="kon"),
        ss("確認できないうわさも\n事実のように\n広めないこと", BOARD, se="pi"),
        nn("報道で分かってることと\nうわさは\n分けて見る", BOARD, se="tv_professional_poon"),
        # ---- 9. 太田プロダクション退所（7:45〜8:30）----
        chap("太田プロダクション\n退所", se="doon_heavy", bgm={"file": LETTER, "gain": -4, "fade": 0.6}),
        org(AGENCY, "太田プロダクション", "10月13日\n退所を発表\nその日付で退所", se="page_turn_02"),
        card("e09_ohta", "事態の重大性を深刻に受け止め　本人と面会して協議", b=AGENCY),
        card("e09_ohta", "本人からの申し出もあり　13日付で退所", b=AGENCY, se="card_place"),
        card("e09_ohta", "騒動を改めて謝罪　捜査中のため詳細は控える", b=AGENCY),
        ss("2019年9月の所属から\n約7年の関係が\n終わった", AGENCY, se="kon"),
        nn("YouTuber所属の\n“第1号”が……", AGENCY, se="deflate_hyororo"),
        ss("退所は\n“本人からの申し出もあった”\nと事務所は説明", AGENCY, se="pi"),
        nn("事務所の説明と\n本人の説明は\n分けて見よう", AGENCY, se="kon"),
        ss("YouTubeの活動や\n会社の経営がどうなるかは\nまだ発表されていない", V_HANDS, se="pi"),
        # ---- 10. 経歴を総括（8:30〜9:00）----
        chap("ヴァンビさんの\n経歴をふり返る", se="whoosh_shu", bgm={"file": MIRAI, "gain": -2, "fade": 0.8}),
        card("e10_summary", "バンド→ヴァンゆん→炎上→休止・解散", b=TIMELINE),
        card("e10_summary", "スパイダーメーンで1,000万人→HERO'ZZ設立", b=TIMELINE, se="card_place"),
        card("e10_summary", "そして逮捕（容疑の段階）・事務所退所", b=TIMELINE),
        ss("大成功と騒動を\nくり返してきた経歴", TIMELINE, se="kon"),
        ss("言葉のいらない動画で\n世界に届いた発想力は\n本物だった", COUNTER, se="pi"),
        nn("だからこそ\n今回のニュースの衝撃も\n大きかった", COUNTER, se="deflate_hyororo"),
        nn("今回の件が\nこれからの活動に\nどう影響するのか……", TIMELINE, se="question_hatena_maou"),
        ss("捜査の結果も含めて\n引き続き\n注目されている", V_NIGHT, se="pi"),
        dict(bg=bg(TIMELINE), card=pt("e11_ending"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


def cuts_full():
    return L.apply_fx(L.allocate(cuts_all(), max_use=8))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "15_vambi_full.mp4")
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
