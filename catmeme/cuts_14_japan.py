"""14_japan（日本が「世界で最も魅力的な国」4年連続1位）のカット割り。原稿 scripts/14_japan.md。作りは 13本目と同じ。

python3 catmeme/cuts_14_japan.py          → out/14_japan_full.mp4
python3 catmeme/cuts_14_japan.py --audio  → 音だけ作り直す

原稿のルール（必ず守る）：
- 海外の反応は、確認できた記事・調査だけ。セリフや反応を作らない（猫が言うのは要約・感想）
- ランキング・統計は「調べた団体」と「年」を必ず出す。投票の結果と、SNSや旅行者の声は分ける
- 日本を持ち上げるだけにしない。不満・課題（混雑・言葉・ゴミ箱・二重価格・犯罪はゼロではない）も出す
- 主語になる団体（観光局・雑誌・警視庁など）は団体名の札つきの猫で出し、その場面にはニュース猫・博識な猫は出さない
- 全動画共通：今日の一言・単語の途中で改行しない・最後はチャンネル登録の画面・過去の動画にはふれない
"""
import os
import sys

import cuts_04_leak as L
import render as R

HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("14_japan", "02_october", "01_todai", "04_leak", "03_kodomo_nisa")]
L.PT = os.path.join(HERE, "parts", "14_japan")
R.PAN_DIRS = tuple(R.PAN_DIRS) + ("14_japan",)   # AIで作った写真ふうの背景もゆっくり動かす
pt, cat, duo, solo, close, dia, expl, chap, net, nn, ss = L.pt, L.cat, L.duo, L.solo, L.close, L.dia, L.expl, L.chap, L.net, L.nn, L.ss
bg = L.bg
N, S = L.N, L.S
PURPLE, COCOA, MIRAI, KAMI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.KAMI, L.NORA
AM223 = os.path.join(L.BGM, "2_23_AM.mp3")

L.POOLS["react"] += ["stare_standing_marmot", "flip_emo_cat_hair"]
L.POOLS["calm"] += ["lick_talking_goat", "eat_chips_cat", "stand_real_sheep"]
# 海外の旅行者（調査・記事の回答を要約して言う役。特定の人を演じない）
TRA = "海外の旅行者"
L.ROLE[TRA] = (205, 150, 0)
L.POOLS["traveler"] = ["excited_hodomoe_city_cat", "peek_what_happen_cat", "happy_girlfriend_dance_cat", "eat_pop_cat",
                       "huh_huh_cat", "joy_happy_happy_happy_cat", "happy_chipi_chapa_cat", "sulk_hungry_cat"]
L.FALLBACK["traveler"] = ["react", "calm"]

# 主語になる団体は猫にして登場させる（10/14 ユーザー指定）
ORG_COLOR = (90, 60, 150)
ORG_CAT = {"コンデナスト・トラベラー": "flip_emo_cat_hair", "日本政府観光局": "work_typing_cat", "観光庁": "call_customer_service_cat",
           "警視庁": "stare_standing_marmot", "警察庁": "showoff_gojo_cosplay_cat", "JR東海": "drive_driving_cat",
           "京都市": "think_bike_front_seat_cat", "姫路市": "angry_aiming_cat", "スカイトラックス": "peek_what_happen_cat",
           "タイムアウト": "cocky_dj_cat", "電通": "work_dog_staring_computer", "ロンリープラネット": "ride_kitten_bike",
           "山梨県・静岡県": "leave_cat_leaves_home", "富士河口湖町": "stand_real_sheep", "米NPR": "listen_dancing_dog",
           "ミシュラン": "eat_crunchy_cat_luna"}
for _o in ORG_CAT:
    L.ROLE[_o] = ORG_COLOR

# 背景（14_japan は Gemini で作ったイラスト＝AI生成。概要欄に書く）
STAGE, MAP, AIRPORT, SUSHI, RAMEN, STREET, TOILET, CLASS = ("bg43_award_stage", "bg44_world_map", "bg45_airport_arrival",
                                                           "bg46_sushi_counter", "bg47_ramen_shop", "bg48_clean_street",
                                                           "bg49_public_toilet", "bg50_classroom_cleaning")
NIGHT, KOBAN, SHINK, ROUTE, RYOKAN, TEMPLE, SKY, AKIBA = ("bg51_night_street", "bg52_koban", "bg53_shinkansen",
                                                         "bg54_station_crowd_map", "bg55_ryokan", "bg56_kyoto_temple",
                                                         "bg57_tokyo_skyline", "bg58_akihabara")
SAKURA, MOMIJI, ONSEN, OKINAWA, HOKKAIDO, VENDING, CROWD, HOTEL, SAMPLE, LOCKER = (
    "bg59_sakura_park", "bg60_autumn_leaves", "bg61_snow_onsen", "bg62_okinawa_beach", "bg63_hokkaido_field",
    "bg64_vending_machines", "bg65_crowded_kyoto", "bg66_hotel_price", "bg67_food_sample", "bg68_coin_lockers")
KONBINI, AISLE, IZAKAYA, YAKINIKU, KYOTO, ROOM, BOARD, PRESS, SNS = (
    "bg15_convenience", "bg16_food_aisle", "bg13_izakaya", "bg22_yakiniku", "bg10_kyoto", "bg02_room", "bg03_blackboard",
    "bg07_press", "bg09_sns")
# 動く背景（assets_video/wide）
V_FUJI, V_SHIBUYA, V_NIGHT, V_ROAD, V_CAT, V_CHART, V_CASH, V_PHONE, V_HANDS, V_POLICE, V_MEET, V_PARK, V_CATBW, V_SLEEP = (
    "v07_mt_fuji_clouds", "v09_shibuya_crossing_aerial", "v05_city_night_river", "v17_cherry_road_aerial",
    "v08_cat_orange_walking", "v11_stock_chart_blue", "v06_cash_counting", "v04_smartphone_man_coat", "v20_smartphone_hands",
    "v16_police_car_lights", "v14_business_meeting", "v12_students_park_laptop", "v21_cat_black_white", "v03_cat_sleeping_bed")
STING = {"file": KAMI, "len": 3.5, "gain": -14}


def one(b, sub, **kw):
    return dict(bg=bg(b), sub=sub, cats=[cat("@calm", "博識な猫", 470, h=640)], **kw)


def two(b, sub, **kw):
    return dict(bg=bg(b), cats=[cat("@react", "ニュース猫", 500, h=700), cat("@calm", "博識な猫", 1430, h=700)], say=sub,
                text_top=True, **kw)


def ex(b, text, **kw):
    return expl(b, [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "", text, dur=kw.pop("dur", 3.6), **kw)


def org(b, who, sub, **kw):
    """団体の猫だけをまん中に置く。第三者が出る場面にはニュース猫・博識な猫は出さない（10/14 ユーザー指定）。"""
    return dict(bg=bg(b), cats=[cat(ORG_CAT[who], who, 960, h=720)], say=sub, text_top=True, **kw)


def tra(b, say, **kw):
    """海外の旅行者（調査・記事の内容を要約して言う）。猫は1匹だけ。"""
    return solo(b, "@traveler", TRA, say, side=kw.pop("side", "L"), **kw)


def card(c, sub, b=BOARD, **kw):
    return dia(c, sub, b, right=S, dur=kw.pop("dur", 5.0), se=kw.pop("se", "card_flip"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=5.0, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- 1. 世界1位！4年連続（0:00〜2:00）----
        nn("速報！\n日本が　また\n世界1位！", V_FUJI, se=["jan", "explosion_chudoon"], bgm={"file": PURPLE, "gain": -4}),
        ss("“世界で最も\n魅力的な国”\nしかも4年連続", V_FUJI, se="doon_movie"),
        org(STAGE, "コンデナスト・トラベラー", "アメリカの旅行雑誌\nコンデナスト・トラベラーの\n読者投票で", se="page_turn_01"),
        dict(bg=bg(STAGE), card=pt("e01_title"), dur=3.6, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        org(STAGE, "コンデナスト・トラベラー", "発表は\n2026年10月6日\n（アメリカ東部時間）", se="pi"),
        nn("4年連続って\nもう殿堂入りでは？", STAGE, se="question_mark_pop_confused_huh"),
        card("e01_us", "米国版の1位は日本　スコアは95.52", se="card_flip"),
        card("e01_us", "2位イタリアとの差は　わずか0.72", se="card_place"),
        two(MAP, "イタリア・スペイン・フランス\n観光大国が\nずらっと並ぶ中で1位", se="kon"),
        nn("ピザとパスタの国に\n勝っちゃった……", MAP, se="shock_piano"),
        ss("2024年の米国版も\n1位は日本\n2位イタリア・3位ギリシャ", MAP, se="pi"),
        nn("ずっと\nイタリアと\nトップ争い……", MAP, se="kon"),
        ss("ただし\n英国版もある", MAP, se="hyoshigi_01"),
        card("e01_uk", "英国版の1位はギリシャ　日本は2位", se="card_flip"),
        nn("イギリスでは\n惜しくも2位！", se="deflate_hyororo"),
        ss("英国版は29回目\nギリシャとの差は\n約1.1点", se="pi"),
        ss("読む人の国が違うと\n結果も変わる", se="pikon"),
        card("e01_how", "読者が旅の体験を採点するランキング", dur=4.4),
        card("e01_how", "米国版は39回目　約79万9,000票", dur=4.4, se="card_place"),
        two(SKY, "都市の部門では\n東京が2位\n京都が10位", se="pinpon_notice"),
        nn("東京と京都\nどっちもランクイン！", SKY, se="idea_newtype_01"),
        ss("大事なのは\nこれは“読者の投票”\nということ", se="kon"),
        ss("SNSの声や\n旅行者の感想とは\n別ものとして見る", se="pi"),
        org(AIRPORT, "日本政府観光局", "実際に\n日本に来る人も\n増え続けている", se="page_turn_01"),
        card("e01_visitors", "2025年の訪日外国人は約4,268万人で過去最高", b=AIRPORT),
        card("e01_visitors", "初めて4,000万人を超えた", b=AIRPORT, se="card_place"),
        nn("4,268万人って\n日本の人口の\n3分の1くらい！？", AIRPORT, se=["explosion_chudoon"]),
        ss("のべ人数だから\n同じ人が何回も\n来ていることもある", AIRPORT, se="pikon"),
        ss("旅行で使ったお金も\n約9.5兆円で過去最高\n前の年より17%増", V_CASH, se="price_display"),
        nn("9.5兆円……\n想像できない", V_CASH, se="shock_piano"),
        ss("円安で\n日本の旅が\n割安になったことも大きい", V_CHART, se="kon"),
        ss("一方で\n2025年12月は中国からの客が\n前年より約45%減った", V_CHART, se="pi"),
        nn("国どうしの関係でも\n旅行者の数は\n変わるんだね", V_CHART, se="question_hatena_maou"),
        org(AIRPORT, "日本政府観光局", "今回の結果は\n“おもてなし”と“安全”が\n評価されたと発表", se="pinpon_notice"),
        close(V_SHIBUYA, "@react", "ニュース猫", "でも　なんで\nそこまで\n日本なの？", red=False, se=["game_aceattorney_desk_slam"]),
        ss("今日は\n海外の目で\n日本を見てみよう", V_SHIBUYA, se="tv_professional_poon"),
        # ---- 2. 日本食（2:00〜3:30）----
        ss("まずは\nいちばん期待されている\nあれから", V_FUJI, se="kon"),
        chap("日本食が\n外国人を虜にする理由", se="doon_heavy", bgm={"file": COCOA, "gain": -2, "fade": 0.6}),
        org(SUSHI, "観光庁", "訪日客に聞いた\n“日本に来る前に\nいちばん楽しみだったこと”", se="page_turn_01"),
        card("e02_food", "「日本食を食べること」が82.2%で1位", b=SUSHI),
        card("e02_food", "食べた人の満足度は96.9%", b=SUSHI, se="card_place"),
        nn("期待されて\nちゃんと応えてる！", SUSHI, se="pinpoon_correct"),
        two(SUSHI, "寿司・ラーメン・和牛\n天ぷら・うどん", se="pikon"),
        ss("農林中央金庫の調査（2023年）では\n人気の料理の1位は　寿司", SUSHI, se="pi"),
        ss("“本場の日本食は\n自分の国で食べるのと違う”\nと答えた人が多かった", SUSHI, se="kon"),
        nn("海外の寿司と\n何が違うんだろう", SUSHI, se="question_mark_pop_confused_huh"),
        ss("ネタの鮮度と\n職人の技　と\nよく言われる", SUSHI, se="pi"),
        org(SUSHI, "ミシュラン", "そして\nミシュランの星", se="jan"),
        card("e02_michelin", "東京の星つきの店は183軒（2024年版）", b=SUSHI),
        card("e02_michelin", "2023年版は200軒で「世界最多の都市」", b=SUSHI, se="card_place"),
        nn("パリより\n星が多い街……", SUSHI, se="shock_piano"),
        two(RAMEN, "しかも\n高級店だけじゃない", se="kon"),
        ss("1,000円前後のラーメンや\n定食が　ちゃんとおいしい", RAMEN, se="pikon"),
        nn("街の定食屋が\n実はすごかった", RAMEN, se="idea_newtype_01"),
        two(KONBINI, "そして\n外国人に大人気なのが\nコンビニ", se="jan"),
        org(KONBINI, "米NPR", "アメリカの公共ラジオNPRは\n2025年9月\n「日本型コンビニがアメリカへ」と報道", se="page_turn_02"),
        card("e02_konbini", "全国に約2万2,000店　24時間営業", b=KONBINI),
        card("e02_konbini", "食べ物が1日に何回も届く　チケットや荷物の発送も", b=KONBINI, se="card_place"),
        nn("コンビニが\n“ちょっと便利な店”\nじゃなかった", KONBINI, se="shock_piano"),
        ss("もともとコンビニは\nアメリカ生まれ\n日本で形を変えて広まった", KONBINI, se="pi"),
        nn("アメリカ生まれが\n日本で進化して\nアメリカへ帰る……", KONBINI, se="idea_newtype_01"),
        ss("おにぎり・たまごサンド・\nからあげ\n海外の旅行記の定番", KONBINI, se="pi"),
        ss("記事では\n「アメリカで受け入れられるかは\nまだ分からない」という声も", KONBINI, se="kon"),
        two(AISLE, "地域ごとの味も\n強み", se="pikon"),
        ss("北海道の海鮮\n大阪の粉もの\n沖縄のそば", AISLE, se="pi"),
        nn("全部\n食べに行きたい……", AISLE, se="tear_drop"),
        ss("ただし\n“期待外れ”の声もある", AISLE, se="hyoshigi_01"),
        ss("観光庁の調査では\n“店員と言葉が通じなかった”が\n15.2%", IZAKAYA, se="kon"),
        nn("メニューが\n読めないと\n注文も大変……", IZAKAYA, se="deflate_hyororo"),
        ss("それに\n人気店は行列\n予約が取れない店も多い", IZAKAYA, se="pi"),
        nn("おいしいのは\n分かったけど\nたどり着けない……", IZAKAYA, se="question_hatena_maou"),
        # ---- 3. 清潔さ（3:30〜5:00）----
        ss("次は\n外国人がいちばん\n困っていることの話", IZAKAYA, se="kon"),
        chap("なぜ日本の街は\nこんなに清潔なのか", se="doon_heavy"),
        two(STREET, "外国人がよく驚くのが\n“ゴミ箱がないのに\nゴミが落ちてない”", se="jan"),
        org(AIRPORT, "観光庁", "帰国する外国人\n4,000人以上に\n空港で聞き取り", se="page_turn_01"),
        card("e03_trash", "困ったことの1位は「ゴミ箱が少ない」21.9%", b=AIRPORT),
        card("e03_trash", "それでも約7割がゴミを持ち帰った", b=AIRPORT, se="card_place"),
        nn("困るけど\nちゃんと持って帰ってる！", AIRPORT, se="pinpoon_correct"),
        ss("“困ったことはない”も\n51.1%で半分以上", AIRPORT, se="pi"),
        nn("ゴミ箱が少ないのは\nなんで？", STREET, se="question_mark_pop_confused_huh"),
        ss("1995年の地下鉄サリン事件のあと\n安全のために\n駅のゴミ箱が減ったと言われる", STREET, se="kon"),
        ss("それで\n“ゴミは持ち帰る”が\n当たり前になった", STREET, se="pikon"),
        two(CLASS, "もうひとつ\n海外から見て\n不思議な習慣", se="pi"),
        ss("日本の学校は\n子どもが自分で\n教室を掃除する", CLASS, se="pikon"),
        nn("え　当たり前じゃ\nないの？", CLASS, se="question_mark_pop_confused_huh"),
        ss("海外では\n清掃の人がやる国も多い", CLASS, se="kon"),
        nn("“自分で汚したら\n自分できれいに”が\n小さいころから……", CLASS, se="idea_newtype_01"),
        two(TOILET, "そしてトイレ", se="jan"),
        org(AIRPORT, "スカイトラックス", "空港の世界ランキング\n利用者のアンケートで決まる", se="page_turn_01"),
        card("e03_haneda", "世界で最もきれいな空港は羽田　10年連続1位", b=AIRPORT),
        nn("10年連続！？", AIRPORT, se=["explosion_chudoon"]),
        ss("トイレ・座席・\n保安検査場まで\n評価されている", AIRPORT, se="pi"),
        ss("羽田は\n“世界の最高の空港”部門でも\n3位（2025年）", AIRPORT, se="pikon"),
        nn("きれいなだけじゃ\nなかった", AIRPORT, se="pinpoon_correct"),
        two(TOILET, "温水洗浄便座は\nおみやげに買って帰る人も\nいると言われる", se="pikon"),
        nn("トイレを\nおみやげに……", TOILET, se="question_hatena_maou"),
        ss("ただ　海外とは\n電圧や配管が違うので\n取り付けに注意", TOILET, se="kon"),
        nn("きれいな街は\nみんなで守ってる\nってことか", STREET, se="kon"),
        # ---- 4. 治安（5:00〜6:20）----
        ss("きれいな街は\n安心な街でもある？", STREET, se="kon"),
        chap("外国人が驚く\n日本の治安", se="doon_heavy", bgm={"file": AM223, "gain": -2, "fade": 0.6}),
        two(NIGHT, "夜に一人で歩ける\nスマホを机に置いて\n席を取れる", se="pi"),
        nn("それ\n海外だと\nやらないの？", NIGHT, se="question_mark_pop_confused_huh"),
        ss("国によっては\n“すぐ盗まれる”と\n注意されている行動", NIGHT, se="kon"),
        card("e04_safety", "人口10万人あたりの殺人　日本は0.23（2023年）", b=NIGHT),
        card("e04_safety", "アメリカは5.76　日本の約25倍", b=NIGHT, se="card_place"),
        nn("けた違い……", NIGHT, se="shock_piano"),
        ss("世界平和度指数の1位は\nアイスランド\n日本はアジアでも上位", NIGHT, se="pi"),
        ss("世界平和度指数2025でも\n日本は163の国と地域の中で\n12位", NIGHT, se="pi"),
        two(KOBAN, "そして\n落とし物が戻ってくる国", se="jan"),
        org(KOBAN, "警視庁", "東京で2025年に\n届けられた現金は\n約45億円", se="page_turn_01"),
        card("e04_lost", "そのうち約32億円が落とし主に戻った", b=KOBAN),
        nn("32億円！？\n落とした人も多いけど\n届ける人も多い！", KOBAN, se=["explosion_chudoon"]),
        ss("2003年のアメリカの法学者の実験では\n東京で落とした財布20個のうち\n17個が現金ごと戻った", KOBAN, se="pi"),
        ss("交番があって\n届けるのが当たり前\nという仕組みも大きい", KOBAN, se="pikon"),
        ss("交番は\n全国に約6,000か所以上\n道案内もしてくれる", KOBAN, se="pi"),
        ss("拾った人は\nお礼を受け取る権利があるけど\n断る人も多いと言われる", KOBAN, se="kon"),
        nn("お礼より\n“戻ってよかった”\nの方がうれしい……", KOBAN, se="tear_drop"),
        two(V_PHONE, "電車の中の静かさや\n行列にきちんと並ぶのも\nよく驚かれる", se="pi"),
        nn("いつもの通勤が\n海外では\n“すごい”らしい", V_PHONE, se="idea_newtype_01"),
        ss("でも\n日本でも犯罪は起きる", se="hyoshigi_01"),
        org(V_POLICE, "警察庁", "2025年の刑法犯は\n77万4,142件\n4年連続で増加", se="page_turn_02"),
        card("e04_crime", "特殊詐欺の被害額は1,414億円で過去最多", b=V_POLICE),
        nn("安全な国でも\n油断はダメ……", V_POLICE, se="deflate_hyororo"),
        ss("旅行者も\nスリや詐欺には\n気をつけてほしい", V_POLICE, se="kon"),
        # ---- 5. 交通（6:20〜7:40）----
        ss("安心して\nどこへでも行ける\nその足は……", V_POLICE, se="kon"),
        chap("日本の交通は\n世界的に見てすごい？", se="quiz_question_01", bgm={"file": COCOA, "gain": -2, "fade": 0.6}),
        two(SHINK, "東京から大阪まで\n新幹線で\n約2時間半", se="pikon"),
        org(SHINK, "JR東海", "東海道新幹線の\n1本あたりの平均の遅れは\n約1分半（2024年度・報道より）", se="page_turn_01"),
        card("e05_train", "台風や地震などの災害も含めた数字", b=SHINK),
        card("e05_train", "1日に350本以上が走る", b=SHINK, se="card_place"),
        nn("災害込みで\n1分半！？", SHINK, se=["explosion_chudoon"]),
        ss("2008年度は\n平均36秒だった\nという記録もある", SHINK, se="pi"),
        nn("秒で数える\n遅れ……", SHINK, se="shock_piano"),
        ss("遅れが出ると\n“遅延証明書”まで\nもらえる", SHINK, se="pikon"),
        nn("遅れた証明書を\n会社に出す国……", SHINK, se="question_hatena_maou"),
        ss("ホームには\n乗る位置まで\n線で書いてある", SHINK, se="pi"),
        nn("並ぶ場所まで\n決まってるのか", SHINK, se="question_mark_pop_confused_huh"),
        two(V_HANDS, "Suicaなどの\nICカード1枚で\n電車もバスもコンビニも", se="pikon"),
        ss("最近は\nスマホにも入れられる", V_HANDS, se="pi"),
        two(KYOTO, "電車とバスだけで\n京都も奈良も日光も\n回れる", se="pi"),
        nn("車がなくても\n観光できる国", KYOTO, se="idea_newtype_01"),
        ss("でも\n弱点もある", ROUTE, se="hyoshigi_01"),
        two(ROUTE, "東京の路線図は\n会社も線も多くて\n“迷路”と言われがち", se="kon"),
        nn("日本人でも\n乗り換えで\n迷う……", ROUTE, se="deflate_hyororo"),
        ss("朝のラッシュの満員電車も\n海外の旅行者には\nびっくりされる", ROUTE, se="pi"),
        ss("地方に行くと\nバスが1日数本\nということもある", ROUTE, se="kon"),
        nn("都会と地方で\n便利さが全然違う", ROUTE, se="deflate_hyororo"),
        # ---- 6. おもてなし（7:40〜9:00）----
        ss("移動の次は\n人の話", ROUTE, se="kon"),
        chap("世界を感動させる\n日本のおもてなし", se="doon_heavy"),
        card("e06_omotenashi", "日本政府観光局「おもてなしと安全が評価された」", b=RYOKAN),
        two(RYOKAN, "店に入ると\n“いらっしゃいませ”\n水とおしぼりが無料", se="pi"),
        nn("それも\n海外では\n当たり前じゃない？", RYOKAN, se="question_mark_pop_confused_huh"),
        ss("アメリカなどでは\nチップを払う文化\n日本はチップなし", RYOKAN, se="kon"),
        nn("チップなしで\nこの接客……", RYOKAN, se="shock_piano"),
        two(RYOKAN, "旅館では\n部屋係の人が\n食事や布団まで世話をする", se="pikon"),
        org(RYOKAN, "ロンリープラネット", "旅行ガイドの\nロンリープラネット", se="page_turn_01"),
        card("e07_ryokan", "世界の体験25の中で　日本の旅館に泊まるが4位", b=RYOKAN),
        nn("旅館そのものが\n“体験”として\n評価されてる！", RYOKAN, se="idea_newtype_01"),
        ss("相手が言う前に\n気づいて動く\nそれが“おもてなし”", RYOKAN, se="pi"),
        two(HOTEL, "でも\nいつも完ぺき\nではない", se="hyoshigi_01"),
        ss("日本語が話せない客への\n対応が冷たかった\nという話も報じられている", HOTEL, se="kon"),
        ss("英語での案内が\n足りないのは\nまだ課題", HOTEL, se="pi"),
        nn("おもてなしにも\n“言葉の壁”が\nあるんだね", HOTEL, se="deflate_hyororo"),
        # ---- 7. 伝統と未来（9:00〜10:20）----
        ss("人の次は\n街そのものの魅力", HOTEL, se="kon"),
        chap("伝統と未来が\n共存する日本", se="whoosh_shu", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        two(TEMPLE, "京都や奈良には\n何百年も前の\nお寺や町並み", se="pi"),
        two(SKY, "電車で少し移動すると\n高層ビルとネオンの\n東京", se="pikon"),
        nn("昔と未来が\n電車1本で\nつながってる", SKY, se="idea_newtype_01"),
        two(AKIBA, "アニメ・マンガ・ゲームも\n日本に来る\n大きな理由", se="jan"),
        ss("作品の舞台を\nめぐる“聖地巡礼”も\n人気", AKIBA, se="pi"),
        nn("好きな作品の\n景色を\n自分の目で……", AKIBA, se="tear_drop"),
        ss("職人の伝統工芸も\n包丁や器が\nおみやげとして人気", TEMPLE, se="pikon"),
        org(V_SHIBUYA, "タイムアウト", "世界の都市ランキング\nタイムアウト\n“世界の最高の都市”", se="page_turn_01"),
        card("e07_tokyo", "東京は2025年の31位から　2026年は10位へ", b=V_SHIBUYA),
        nn("一気に\nトップ10に復帰！", V_SHIBUYA, se="pinpoon_correct"),
        ss("150都市・2万4,000人以上の\n住民の声と\n専門家の投票で決まる", V_SHIBUYA, se="pi"),
        ss("2025年の都の調査では\n外国人観光客が\nいちばん行ったのは渋谷", V_SHIBUYA, se="pi"),
        ss("でも　ネットの英語の掲示板では\n“渋谷は思ったほどじゃない”\nという声もあった", V_SHIBUYA, se="kon"),
        nn("人気の場所ほど\n好みが分かれる", V_SHIBUYA, se="question_hatena_maou"),
        # ---- 8. 自然と四季（10:20〜11:20）----
        ss("街を出ると\nまた別の顔", V_SHIBUYA, se="kon"),
        chap("日本の自然と\n四季の魅力", se="doon_heavy", bgm={"file": COCOA, "gain": -2, "fade": 0.6}),
        two(SAKURA, "春は桜", se="jan"),
        org(SAKURA, "日本政府観光局", "2025年4月の訪日客は\n約391万人\n1か月として過去最高", se="page_turn_01"),
        card("e08_sakura", "桜の季節と海外のイースター休みが重なった", b=SAKURA),
        ss("東京の目黒川の\n桜のクルーズは\n乗客の45%が外国人（2025年3月）", SAKURA, se="pi"),
        ss("2025年の花見の経済効果は\n約1.39兆円と予測された", SAKURA, se="price_display"),
        nn("桜を見に\n海を越えて\n来てるんだ", SAKURA, se="idea_newtype_01"),
        ss("アジアの旅行者は桜\n欧米の旅行者は\n日本庭園や歴史に興味が強いという調査も", SAKURA, se="pi"),
        two(MOMIJI, "秋は紅葉", se="pikon"),
        two(ONSEN, "冬は雪と温泉", se="pikon"),
        ss("雪の中の露天風呂は\n海外では\nめずらしい体験", ONSEN, se="pi"),
        two(V_FUJI, "そして富士山", se="jan"),
        org(V_FUJI, "山梨県・静岡県", "2025年夏から\n入山料は\n1人4,000円", se="page_turn_02"),
        card("e08_fuji", "夜に登るなら山小屋の予約が必要", b=V_FUJI),
        nn("人気すぎて\nルールが\nできたんだね", V_FUJI, se="kon"),
        two(HOKKAIDO, "北の北海道から", se="pi"),
        two(OKINAWA, "南の沖縄まで\n景色が全然違う", se="pikon"),
        nn("ひとつの国で\n雪と南の海……", OKINAWA, se="shock_piano"),
        ss("最近は\n地方の自然や温泉に\n行く旅行者も増えている", HOKKAIDO, se="pi"),
        # ---- 9. 意外な日常（11:20〜12:30）----
        ss("景色の次は\nもっと身近なもの", HOKKAIDO, se="kon"),
        chap("外国人が驚いた\n意外な日常", se="quiz_question_02", bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        two(VENDING, "自動販売機が\nどこにでもある", se="pi"),
        ss("外に置いても\n壊されない\nというのも驚かれる", VENDING, se="pikon"),
        two(SAMPLE, "店の前の\n食品サンプル", se="pi"),
        nn("言葉が分からなくても\n指させば注文できる！", SAMPLE, se="idea_newtype_01"),
        ss("食品サンプルは\nおみやげとしても人気\n作る体験ができる店も", SAMPLE, se="pikon"),
        two(LOCKER, "駅のコインロッカー", se="pi"),
        ss("荷物を預けて\n手ぶらで観光", LOCKER, se="pikon"),
        two(TOILET, "温水洗浄便座と\nボタンだらけのトイレ", se="pi"),
        nn("ボタンが多すぎて\n押すのが怖い\nという人も……", TOILET, se="question_hatena_maou"),
        two(V_PHONE, "電車の中で\n電話しない\n静かな車内", se="pi"),
        two(ROUTE, "駅の案内表示は\n英語・中国語・韓国語も", se="pi"),
        ss("でも\n観光庁の調査では\n“案内の文字が読めない”の声も", ROUTE, se="kon"),
        nn("便利だけど\nまだまだ\n改善の余地あり", ROUTE, se="deflate_hyororo"),
        # ---- 10. 不満もある（12:30〜14:00）----
        ss("ここまで\nいいことばかり\n……でも", ROUTE, se="kon"),
        chap("日本を絶賛する\n外国人にも不満はある", se="doon_heavy", bgm={"file": AM223, "gain": -2, "fade": 0.6}),
        card("e03_trash", "困ったこと　ゴミ箱・言葉・混雑", b=CROWD),
        two(CROWD, "京都は\n2024年に外国人観光客が\n約1,088万人", se="jan"),
        nn("人気の通りは\n歩けないくらい……", CROWD, se="shock_piano"),
        ss("東山の調査では\n日本人の観光客が12%減って\n外国人が66%増えた（2023→2024年）", CROWD, se="pi"),
        nn("日本人が\n京都から離れてる……", CROWD, se="deflate_hyororo"),
        ss("祇園の私道には\n“無断で入ると1万円”の\n看板も立った（2024年）", CROWD, se="kon"),
        ss("市バスに\n観光客と地元の人が\n乗れないことも", CROWD, se="kon"),
        org(CROWD, "京都市", "2026年3月から\n宿泊税を引き上げ\n最大で1人1泊1万円", se="page_turn_02"),
        nn("1泊1万円の\n税金！？", CROWD, se=["explosion_dokaan"]),
        ss("安い宿は\n200円のまま\n高級な宿ほど高い", CROWD, se="pi"),
        org(TEMPLE, "姫路市", "姫路城は2026年3月から\n市民1,000円\n市民以外2,500円", se="page_turn_01"),
        ss("“外国人だけ高くする”案には\n海外から“差別的”だという\n批判も出た", TEMPLE, se="kon"),
        ss("最終的には\n“市民かどうか”で\n分ける形になった", TEMPLE, se="pi"),
        ss("始まった最初の月は\n入場者が約17%減って\n入城料の収入は約2倍と報じられた", TEMPLE, se="price_display"),
        nn("人はへって\nお金はふえた……", TEMPLE, se="question_hatena_maou"),
        org(V_FUJI, "富士河口湖町", "2024年\n富士山の撮影スポットに\n黒い幕を設置", se="page_turn_02"),
        ss("理由は　道路への飛び出しや\nゴミに困った住民の声\n幕は　のちに撤去された", V_FUJI, se="kon"),
        nn("人気が出すぎて\n住む人が\n困ってる……", V_FUJI, se="deflate_hyororo"),
        two(HOTEL, "ホテル代の高さも\nよく聞く不満", se="pi"),
        ss("円安で\n海外の人には安く感じても\n日本人には高い", HOTEL, se="kon"),
        nn("日本人が\n京都に泊まれない……", HOTEL, se="tear_drop"),
        ss("お店で\n外国人の値段を\n高くする“二重価格”も議論に", HOTEL, se="pi"),
        ss("海外の旅行者からは\n“差別だ”という声も\n日本の中では賛成も多い", HOTEL, se="kon"),
        nn("むずかしい\n問題……", HOTEL, se="deflate_hyororo"),
        ss("観光の仕事は\n人手不足\nサービスを保てるかも課題", HOTEL, se="kon"),
        ss("世界旅行ツーリズム協議会は\n2035年に観光の働き手が\n約29%足りなくなると予測", V_MEET, se="pi"),
        nn("ほめられるだけじゃ\nなかった……", HOTEL, se="deflate_hyororo"),
        # ---- 11. なぜ何度も来たくなる？（14:00〜16:00）----
        ss("それでも\n人気は止まらない", HOTEL, se="kon"),
        chap("なぜ外国人は\n何度も日本に来たくなるのか", se="doon_heavy", bgm={"file": MIRAI, "gain": -2, "fade": 0.8}),
        org(V_MEET, "電通", "20の国と地域の\n1万2,400人に聞いた\nジャパンブランド調査2025", se="page_turn_01"),
        card("e11_repeat", "「日本にまた行きたい」52.7%で1位", b=V_MEET),
        nn("2人に1人が\n“また来たい”！", V_MEET, se="pinpoon_correct"),
        ss("2024年の34.6%から\n大きく上がった", V_MEET, se="pi"),
        two(AIRPORT, "オーストラリアからは\n2025年に初めて\n100万人を超えた", se="pikon"),
        ss("アメリカからは\n約330万人\n前の年より21%増", AIRPORT, se="pi"),
        nn("遠い国からも\nどんどん来てる", AIRPORT, se="idea_newtype_01"),
        ss("ヨーロッパ・アメリカ・オーストラリアから\nまとめて見ても\n前の年より22%増（2025年）", AIRPORT, se="pi"),
        card("e11_reasons", "安くておいしい食事　清潔さと安全", b=BOARD, dur=4.4),
        card("e11_reasons", "時間どおりの交通　伝統と最先端　四季の自然", b=BOARD, dur=4.4, se="card_place"),
        ss("どれも\n日本人には\n“当たり前”のもの", se="kon"),
        nn("当たり前が\n海外では\n特別……", V_CAT, se="idea_newtype_01"),
        card("e11_issues", "混雑・言葉の壁・ホテル代・地方への分散", b=BOARD, dur=4.6),
        ss("人気を続けるには\n観光客と住む人が\nどちらも困らない工夫", se="pi"),
        two(V_ROAD, "旅を地方に分散すれば\n混雑もへって\n地方も元気になる", se="pikon"),
        nn("4年連続1位は\nゴールじゃなくて\nスタートかも", V_FUJI, se="tv_professional_poon"),
        ss("ごみを持ち帰る　並ぶ　静かにする\nいつもの暮らしが\n世界の評価につながっている", V_FUJI, se="kon"),
        dict(bg=bg(BOARD), card=pt("e12_ending"), dur=3.2, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


def cuts_full():
    return L.apply_fx(L.allocate(cuts_all(), max_use=10))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "14_japan_full.mp4")
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
