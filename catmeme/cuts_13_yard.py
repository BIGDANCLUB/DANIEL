"""13_yard（盗難ハイエース300台、塀の中で解体され海外へ）のカット割り。原稿 scripts/13_yard.md（v1）。作りは 10〜12本目と同じ。

python3 catmeme/cuts_13_yard.py          → out/13_yard_full.mp4
python3 catmeme/cuts_13_yard.py --audio  → 音だけ作り直す

原稿のルール（必ず守る）：
- 逮捕された4人は容疑の段階。「〜した疑い」「〜とみられる」。名前・顔は出さない。容疑者を猫で演じない
- 国籍でひとくくりにしない。盗む役は日本人とされていることも入れる。輸出先は「と言われている」
- 「ヤード＝悪」と言わない。手口の詳しいやり方は説明しない
- 全動画共通：冒頭の問いかけ・今日の一言・単語の途中で改行しない・最後はチャンネル登録の画面・簡単なボケは入れない
"""
import os
import sys

import cuts_04_leak as L
import render as R

HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("13_yard", "04_leak", "03_kodomo_nisa", "02_october", "01_todai")]
L.PT = os.path.join(HERE, "parts", "13_yard")
VIC = "車を盗まれた猫"
L.ROLE[VIC] = (35, 140, 65)
pt, cat, duo, solo, close, dia, expl, chap, net, nn, ss = L.pt, L.cat, L.duo, L.solo, L.close, L.dia, L.expl, L.chap, L.net, L.nn, L.ss
bg = L.bg
N, S = L.N, L.S
PURPLE, COCOA, MIRAI, KAMI = L.PURPLE, L.COCOA, L.MIRAI, L.KAMI
AM223 = os.path.join(L.BGM, "2_23_AM.mp3")

L.POOLS["react"] += ["stare_standing_marmot", "flip_emo_cat_hair"]
L.POOLS["calm"] += ["lick_talking_goat", "eat_chips_cat", "stand_real_sheep"]
# 車を盗まれた猫：仕事で使うハイエースを盗まれた職人（架空・被害者側）
L.POOLS["victim"] = ["sad_banana_cat_cry", "sad_black_dog", "despair_dramatic_kitten", "sulk_hungry_cat", "blank_black_cat_zoning_out",
                     "realize_wet_cat_stare", "snore_snoring_dog"]
L.FALLBACK["victim"] = ["react", "calm"]
# 背景（10/13 ユーザー提供の写真：ハイエース3枚・ヤード2枚 → backgrounds/13_yard。港の絵はないので手持ちで代用）
LOT, YARD, PRESS, ROOM, BOARD, SNS, PORT, PHONE = ("bg18_backyard", "bg41_yard_scrap", "bg07_press", "bg02_room", "bg03_blackboard",
                                                   "bg09_sns", "bg20_counter", "bg26_phone_alert")
RAID = "bg42_yard_raid_ai"   # AI生成（看板の店名はぼかし済み・架空）
HIACE_W, HIACE_B, HIACE_C = "bg38_hiace_white_run", "bg39_hiace_black_garage", "bg40_hiace_white_city"
# 動く背景（assets_video/wide）。10/13 ユーザー指定「動画背景をもっと使う」
V_POLICE, V_HOOD, V_CASH, V_CHART, V_DARK, V_DEAL, V_NIGHT, V_MEET = (
    "v16_police_car_lights", "v10_hooded_figure_mystery", "v06_cash_counting", "v11_stock_chart_blue", "v13_cat_gray_dark",
    "v19_handshake_business", "v05_city_night_river", "v14_business_meeting")
V_PHONE_M, V_PHONE_W, V_HANDS, V_HAND, V_FUJI, V_SHIBUYA, V_ROAD, V_CATBW = (
    "v04_smartphone_man_coat", "v18_smartphone_woman", "v20_smartphone_hands", "v22_smartphone_hand", "v07_mt_fuji_clouds",
    "v09_shibuya_crossing_aerial", "v17_cherry_road_aerial", "v21_cat_black_white")
STING = {"file": KAMI, "len": 3.5, "gain": -14}


def vic(say, b=LOT, **kw):
    return solo(b, "@victim", VIC, say, side=kw.pop("side", "L"), **kw)


def one(b, sub, **kw):
    return dict(bg=bg(b), sub=sub, cats=[cat("@calm", "博識な猫", 470, h=640)], **kw)


def two(b, sub, **kw):
    return dict(bg=bg(b), cats=[cat("@react", "ニュース猫", 500, h=700), cat("@calm", "博識な猫", 1430, h=700)], say=sub,
                text_top=True, **kw)


def ex(b, text, **kw):
    return expl(b, [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "", text, dur=kw.pop("dur", 3.6), **kw)


def ask(**kw):
    return dict(card=None, layers=[pt("nattoku")], dur=kw.pop("dur", 2.8), se=kw.pop("se", "doon_heavy"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き・冒頭の問いかけ ----
        dict(card=None, layers=[pt("e00_notice")], dur=5.0, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- 1. つかみ ----（「これ、納得できますか？」は原稿で指定された所だけ。冒頭には入れない：10/13 ユーザー指定）
        vic("朝　仕事に行こうとしたら……\nハイエースが……\nない……", se="tear_drop", sting={"file": KAMI, "len": 4.0, "gain": -14}),
        vic("工具も全部\n積んだままだったのに……", HIACE_B, se="chin_bell_failure_sad_ending", bgm={"file": PURPLE, "gain": -4}),
        one("v17_cherry_road_aerial", "このヤードだけで\n2024年以降\n盗難車300台以上を\n受け取ったとみられる", se="doon_movie"),
        one(YARD, "その多くが　その日のうちに\n茨城県の「ヤード」へ運ばれ", se="car_brake"),
        one(RAID, "塀の中で解体されて\n海外へ輸出された\nとみられる", se="pc_warning"),
        close(RAID, "@react", "ニュース猫", "300台！？\n盗んで　バラして　海外って……\n流れ作業じゃん", se=["explosion_chudoon"]),
        one("v10_hooded_figure_mystery", "自動車の取材を続ける\nジャーナリストは言う", se="page_turn_01"),
        dict(bg=bg(BOARD), card=pt("e01_quote"), dur=4.6, se="doon_heavy", sting=STING,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)]),
        nn("……日本\nナメられてない？", V_DARK, se="shock_piano"),
        dict(bg=bg(BOARD), card=pt("e01_title"), dur=3.4, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        # ---- 2. 何が起きたのか ----
        chap("2026年6月\n4県警がいっせいに", se="doon_heavy"),
        two("v16_police_car_lights", "神奈川・茨城・千葉・埼玉の\n4県警の合同捜査本部が\n4人を逮捕", se="siren_police"),
        dia("e02_roles", "盗む役は日本人の男2人とされる", right=S, dur=4.4, se="card_flip"),
        dia("e02_roles", "受け取ってバラす役は　茨城県鉾田市のヤードの経営者と従業員", right=S, dur=4.6, se="card_place"),
        dia("e02_roles", "部品などにして海外へ（中東などへ、と言われている）", right=S, dur=4.4, se="card_flip"),
        nn("盗むのは日本人で\n受け取るのがヤード……\n完全に分業制じゃん", V_HOOD, se="kon"),
        ss("国籍とか関係なく\n“盗む・隠す・売る”で\n役割を分けてたとみられる", V_DEAL, se="pikon"),
        ex(V_POLICE, "逮捕の容疑：2026年2月　埼玉県川口市で盗まれた\nハイエース1台を　盗難車と知りながら\nヤードで受け取った疑い", dur=4.4, se="pinpon_notice",
           explain_size=80),
        ex(RAID, "警察は　2024年以降に関東一円で盗まれた\n300台以上を受け取り\n解体して輸出したとみている", dur=4.0, se="pinpon_notice"),
        ex(V_PHONE_M, "4人の認否は\n明らかにされていない", se="pinpoon_note"),
        close(RAID, "@react", "ニュース猫", "ちょっと待って\n300台なのに\n容疑は“1台”？", se=["game_pokemon_super_effective_hit_big_damage"]),
        ss("そこ\nあとで話す", V_DARK, se="hyoshigi_01"),
        # ---- 3. ヤードってなに？ ----
        chap("塀の向こう側", se="doon_heavy"),
        dia("e03_yard", "高い鉄の塀で囲まれた　解体や部品の保管をする作業場", YARD, right=S, dur=4.4, se="pinpon_notice"),
        nn("外から中が\n見えないやつか", RAID, se="question_mark_pop_confused_huh"),
        one(YARD, "千葉県だけでも\nヤードは約790か所\n（2025年9月末）", se="page_turn_01"),
        ss("多くのヤードは\nちゃんとルールを守って仕事してる\nそこは誤解しちゃダメ", YARD, se="pinpoon_correct"),
        ss("ただ一部が\n“盗難車の受け皿”になってる\nと言われている", RAID, se="kon"),
        nn("盗まれた車が\n塀の中に入ったら\nもう見えない……", RAID, se="deflate_hyororo"),
        vic("私のハイエースも\nあの塀の中で……", YARD, se="tear_drop"),
        # ---- 4. なぜハイエース？ ----
        chap("なぜ狙われる？", se="quiz_question_01", bgm={"file": COCOA, "gain": -2, "fade": 0.6}),
        two(HIACE_C, "ハイエースやランドクルーザーは\n丈夫で　海外でも人気が高い\nと言われている", se="page_turn_01"),
        two("v06_cash_counting", "まるごとでも　バラした部品でも\n売れる　と言われている", se="price_display"),
        dia("e04_numbers", "2025年の自動車盗難は6,386件　盗難1件あたりの保険金は平均約297.5万円", HIACE_W, right=S, dur=5.0,
            se="card_flip"),
        nn("1台300万円近く……\nそれが300台……", V_CHART, se="shock_piano"),
        ss("単純計算で\n9億円近く", "v06_cash_counting", se="kon"),
        close(V_CASH, "@react", "ニュース猫", "きゅ、9億！？", se=["explosion_dokaan"]),
        ex(V_CHART, "※単純計算\n実際の被害額は発表されていない", se="pinpoon_note"),
        # ---- 5. なぜナメられていると言われるのか ----
        chap("なぜ“大した罪にならない”と\n思われるのか", se="doon_heavy", bgm={"file": AM223, "gain": -2, "fade": 0.6}),
        dia("e05_reasons", "「盗難車だと知っていた」ことの証明が難しい", right=S, dur=4.4, se="card_flip"),
        dia("e05_reasons", "ヤードを取り締まる国の法律がなく　塀の中は見えず　盗まれた人が自分で探すことも", right=S, dur=4.8, se="card_place"),
        ss("①がいちばん大きい\n“知らなかった”と言われると\n受け取った側を罪に問うのが難しい", V_DARK, se="pikon"),
        ex(V_MEET, "「盗難車と知っていた」ことの立証が難しく\n「公訴を維持できない」として\n不起訴になることが多い（ジャーナリスト・報道より）", dur=4.6,
           se="pinpon_notice", explain_size=80),
        close(V_DEAL, "@react", "ニュース猫", "盗んだ車を受け取っても\n“知らなかった”で\n終わっちゃうの！？", se=["explosion_chudoon"]),
        ss("そして③\nヤード（車の解体・保管場所）を\n取り締まる国の法律は　まだない", V_NIGHT, se="kon"),
        ss("ルールは　県ごとの\n「ヤード条例」だけ", YARD, se="pi"),
        dia("e05_jorei", "2016年に千葉県が全国で初めて「ヤード条例」　その後各地に", right=S, dur=4.6, se="card_flip"),
        dia("e05_jorei", "茨城県で違反すると　3か月以下の拘禁刑　または30万円以下の罰金", right=S, dur=4.8, se="card_place"),
        close(V_CASH, "@react", "ニュース猫", "300台で9億円かも\nしれないのに\n条例違反は30万円……！？", se=["explosion_dokaan"], sting=STING),
        ss("もちろん盗みや受け取りは\n別の罪　でも“ヤードのルール違反”\nだけなら　その程度", V_DARK, se="hyoshigi_01"),
        ex(V_POLICE, "ヤードへの踏み込みには\n証拠固めと令状が必要で\n警察にとって面倒な案件　との指摘も（報道より）", dur=4.4, se="pinpon_notice"),
        vic("警察に届けたけど……\n“見つかったら連絡します”\nって……", V_PHONE_M, se="tear_drop"),
        one(V_HANDS, "被害者が\n自分で車を探すケースも多い\nと言われている", se="pi"),
        close(PHONE, "@react", "ニュース猫", "盗まれた方が\n探偵するの！？", se=["game_aceattorney_desk_slam"]),
        one("v10_hooded_figure_mystery", "こうして窃盗団に\n「大した罪にならない」と\n思われている　と言われている", se="doon_movie"),
        nn("そりゃ\nナメられるわ……", V_CATBW, se="deflate_hyororo"),
        ask(),
        # ---- 6. その後 ----
        chap("その後", se="doon_heavy"),
        ex(V_HAND, "4人が起訴されたかどうかは\n10月13日時点で\n報道されていない", se="pinpon_notice"),
        ex(V_POLICE, "経営者ら2人は\n盗難ハイエースの受け取りで\n再逮捕された（報道）", se="page_turn_01"),
        nn("300台の件なのに\n続報が少ない……", V_HANDS, se="question_hatena_maou"),
        ss("逮捕は大ニュース\nでも　その後は静か", V_PHONE_W, se="kon"),
        two(PORT, "一方で\n“出口”で止めた例もある", se="pi"),
        two(PORT, "2026年5月　盗難車のランドクルーザーを\n「ミニバン」と偽って\n横浜港から輸出しようとした疑いで4人逮捕", se="page_turn_02"),
        two(PORT, "見抜いたのは\n税関のコンテナX線検査", se="pinpoon_correct"),
        nn("税関、有能！", PORT, se="game_coin_get_money_gain_happy"),
        two("v16_police_car_lights", "警察庁は2026年4月\nヤードへの立ち入り検査や\n悪質なヤードの取り締まりを強めると表明", se="page_turn_01"),
        two(PRESS, "茨城県は　条例と取り締まりで\n2019年の全国ワースト1位から\n2024年は4位に", se="pinpoon_correct"),
        nn("やればできるじゃん！", V_FUJI, se="idea_newtype_01"),
        one(V_DARK, "ところが……", se="shock_piano"),
        one("v05_city_night_river", "最近　盗難が減っている理由のひとつは\n「ホルムズ海峡が閉鎖されて\n中東に運べないから」と言われている", dur=4.2, se="pc_warning"),
        close(V_NIGHT, "@react", "ニュース猫", "対策じゃなくて\n海峡が閉まったから！？", se=["explosion_chudoon"]),
        ss("海峡が開いたら\nまた増えるかもしれない\nとも", V_CHART, se="kon"),
        nn("日本の防犯\n中東まかせ……", V_SHIBUYA, se="deflate_hyororo"),
        ask(),
        # ---- 7. 自分の車を守るには ----
        chap("じゃあ、どう守る？", se="quiz_question_02", bgm={"file": COCOA, "gain": -2, "fade": 0.6}),
        dia("e07_protect", "ハンドルロックやタイヤロックで「盗るのが面倒な車」に", HIACE_B, right=S, dur=4.6, se="pinpoon_correct"),
        dia("e07_protect", "防犯カメラ・GPS追跡装置・車両保険の補償も確認", HIACE_B, right=S, dur=4.4, se="pinpoon_correct"),
        ss("“盗るのに時間がかかる車”は\n狙われにくい\nと言われている", HIACE_W, se="pikon"),
        vic("全部やっておけば\nよかった……", HIACE_B, se="tear_drop"),
        nn("でも本当は　盗まれた側じゃなくて\n盗む側・受け取る側が困る\n仕組みにしてほしい", HIACE_C, dur=3.6, se="kon"),
        # ---- 8. ネットの声 ----
        chap("ネットの声", se="whoosh_shu", dur=1.4, bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        net("@react", "300台盗まれて\n容疑は1台\nこれが日本", se="boing_01"),
        dict(net("@react", "“知らなかった”で\n済むなら\nやったもん勝ち", se="tsukkomi_bishi"), bg=bg(V_HANDS)),
        net("@react", "条例違反30万円は\nさすがに\n安すぎる", se="buzzer_wrong"),
        net("sleepy_old_memories_cat", "盗まれた人が\n自分で探すの\nおかしいでしょ", se="tear_drop"),
        dict(net("@react", "海峡が閉じて\n盗難が減ったは草\n対策どこ行った", se="silly"), bg=bg(V_PHONE_W)),
        net("@react", "盗む役が日本人なのも\n闇が深い", se="pi"),
        dict(net("@react", "国籍関係なく\n盗む・受け取る・売る\n全員ちゃんと裁け", se="pinpoon_correct"), bg=bg(V_HAND)),
        net("@react", "ヤードを取り締まる\n国の法律を\nまずつくって", se="kon"),
        nn("みんな言ってること\nだいたい同じ", "v09_shibuya_crossing_aerial", se="kon"),
        # ---- 9. まとめ ----
        dict(bg=bg(BOARD), inset={"card": pt("e09a_case"), "box": (200, 60, 1720, 860)}, dur=5.0,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)],
             bgm={"file": MIRAI, "gain": -2, "fade": 0.8}, se="chiin_01"),
        dict(bg=bg(BOARD), inset={"card": pt("e09b_reasons"), "box": (200, 60, 1720, 860)}, dur=4.4,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)], se="card_flip"),
        ss("“大した罪にならない”と\n思わせないこと\nそれが一番の防犯", V_FUJI, se="tv_professional_poon"),
        nn("ヤードの国の法律\n早くつくって……", V_ROAD, se="chirin"),
        dict(bg=bg(BOARD), card=pt("e10_ending"), dur=3.0, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


def cuts_full():
    return L.apply_fx(L.allocate(cuts_all()))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "13_yard_full.mp4")
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
