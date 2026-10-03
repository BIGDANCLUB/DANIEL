"""01_todai_president（東大総長）のカット割り。原稿 scripts/01_todai_president.md の 1〜5 章。

python3 catmeme/cuts_01_todai.py            → out/01_todai_trial.mp4（試作：冒頭〜「選ばれたのは」）
"""
import os
import sys

import parts as P
import render as R

HERE = os.path.dirname(os.path.abspath(__file__))
BG = os.path.join(HERE, "backgrounds", "01_todai")
PT = os.path.join(HERE, "parts", "01_todai")
BGM = os.path.join(HERE, "bgm")


def bg(n):
    return os.path.join(BG, n + ".png")


def pt(n):
    return os.path.join(PT, n + ".png")


def news(a, say, **kw):
    """ニュース猫（リビング・中央）のセリフ。"""
    cat = {"a": a, "x": kw.pop("x", 500), "h": kw.pop("h", 760), "bottom": 1010, "flip": kw.pop("flip", False),
           "ss": kw.pop("ss", 0.0), "anchor": kw.pop("anchor", False),
           "sound": kw.pop("sound", False)}
    return dict(bg=bg("bg02_room"), cats=[cat], say=say, say_name="ニュース猫", **kw)


def friend(a, say, **kw):
    """物知り猫（リビング・右側）のセリフ。ニュース猫に説明する役。"""
    cat = {"a": a, "x": kw.pop("x", 1420), "h": kw.pop("h", 740), "bottom": 1010, "flip": kw.pop("flip", False),
           "sound": kw.pop("sound", False), "anchor": kw.pop("anchor", False)}
    return dict(bg=bg("bg02_room"), cats=[cat], say=say, say_name="物知り猫", plate_xy=(1080, 900), **kw)


def card(c, sub, cat=None, b="bg03_blackboard", **kw):
    """解説カード＋右下の小さい猫＋字幕。"""
    cats = [{"a": cat, "x": 1752, "h": 330, "bottom": 830, "float": True, "small": True,
             "sound": kw.pop("sound", False)}] if cat else []
    return dict(bg=bg(b), card=pt(c), cats=cats, sub=sub, **kw)


CANDS = [("大越慎一さん", "ride_kitten_bike"), ("菅野暁さん", "dance_wop_cat"),
         ("染谷隆夫さん", "spit_not_my_taste_cat"), ("藤垣裕子さん", "sleepy_old_memories_cat"),
         ("山本隆司さん", "sleepy_sleepy_cat")]
CAND_X = [250, 605, 960, 1315, 1670]


def candidates():
    cats, tags = [], []
    for (name, a), x in zip(CANDS, CAND_X):
        cats.append({"a": a, "x": x, "h": 360, "bottom": 690, "still": True, "float": True})
        tags.append(P.name_plate(name, int(x - (len(name) * 40 + 26) / 2), 705, size=40))
    return cats, tags


TEACHERS = [{"a": "think_bike_front_seat_cat", "x": 560, "h": 420, "bottom": 840, "float": True},
            {"a": "work_typing_cat", "x": 960, "h": 470, "bottom": 850, "float": True},
            {"a": "blank_black_cat_zoning_out", "x": 1380, "h": 430, "bottom": 850, "flip": True}]
MEETING = [{"a": "scold_talking_cats", "x": 700, "h": 520, "bottom": 900},
           {"a": "tense_two_cats_face_off", "x": 1300, "h": 500, "bottom": 900, "flip": True}]


def narr(b, sub, a, **kw):
    """ナレーション（出来事の説明）。左に猫、右に大きな文字。"""
    cat = {"a": a, "x": kw.pop("x", 470), "h": kw.pop("h", 640), "bottom": 990, "flip": kw.pop("flip", False),
           "sound": kw.pop("sound", False)}
    return dict(bg=bg(b), cats=[cat], sub=sub, **kw)


PURPLE = os.path.join(BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")


def cuts_trial():
    cand_cats, cand_tags = candidates()
    return [
        # ---- 1. つかみ ----
        dict(card=None, layers=[pt("e00_notice")], dur=2.6),
        dict(bg=bg("bg01_campus"), card=pt("e01_title"), dur=2.4, se="chime", bgm={"file": PURPLE, "gain": -7},
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        narr("bg01_campus", "2026年9月28日\n東大の次の「総長」が\n決まった", "work_typing_cat"),
        news("slack_nail_filing_cat", "ほーん、\n東大のボス\n決まったんだ"),
        friend("taunt_cat_and_scared_dog", "いやそれがさ\nマジで\n事件なんだって"),
        narr("bg01_campus", "選ばれたのは\n投票で2位だった人", "peek_what_happen_cat", se="don"),
        news("blank_black_cat_zoning_out", "……は？", dur=1.3),
        news("huh_huh_cat", "いやいやいや\n待って待って"),
        news("confused_i_dont_know_cat", "2位？\n1位じゃなくて？\nなんで？？"),
        narr("bg01_campus", "しかも\n東大150年の歴史で\n初めての女性の総長", "call_customer_service_cat", se="don"),
        news("despair_dramatic_kitten", "ちょ、\n情報量\nバグってんだけど"),
        friend("leave_cat_leaves_home", "まあ落ち着けって\n順番に話すわ", dur=1.8),
        news("drive_monkey_golf_cart", "たのむわ", dur=1.3),
        # ---- 2. 総長ってだれ？ ----
        news("weird_meowing_cat", "てか総長って\nなに？\n暴走族のアタマ？"),
        friend("fight_cat_fight", "ちげーよ", dur=1.3),
        card("e02_soucho", "総長＝大学のいちばん上の人（ふつうは「学長」）", "work_typing_cat", dur=2.4),
        news("glare_disgusted_cat", "呼び方つっよ", dur=1.4, anchor=True),
        card("e02_soucho", "次の総長の任期は　2027年4月から6年間", "sulk_hungry_cat", dur=2.2),
        news("surprise_big_pupils_cat", "6年！？\nなっが", dur=1.5, se="don"),
        friend("wakeup_dog_hits_bowl", "長いよな\nだから選び方\nガチで大事なんよ"),
        # ---- 3. 候補者は5人 ----
        dict(bg=bg("bg01_campus"), sub="候補者は5人", cats=cand_cats, layers=cand_tags, dur=2.2, se="pop"),
        news("showoff_gojo_cosplay_cat", "うわ、\n全員つよそう", dur=1.6),
        friend("eat_crunchy_cat_luna", "副学長とか理事とか\n東大の中の\nえらい人ばっか"),
        news("cocky_dj_cat", "で、どうやって\n選ぶん？", se="pop"),
        # ---- 4. 先生たちの投票 ----
        dict(bg=bg("bg04_voting"), sub="学内の先生たちが投票\n「意向投票」", cats=TEACHERS, dur=2.2),
        dict(bg=bg("bg04_voting"), cats=TEACHERS, say="どれにしよ〜\nまあこの人っしょ", say_name="先生たち",
             plate_xy=(60, 900), dur=2.0),
        news("dance_maxwell_cat", "結果\nはよ", dur=1.3, se="pop"),
        narr("bg06_spotlight", "2回目の投票の\n結果は……", "dance_koto_nai_cat", se="drum", dur=2.2),
        card("e05_votes", "染谷さんが過半数でダントツ1位", "happy_chipi_chapa_cat", dur=2.6, se="don", sound=True),
        news("realize_wet_cat_stare", "え、1位の人、\n半分以上\n取ってんじゃん"),
        news("joy_happy_happy_happy_cat", "2位の倍よ倍！\nはい優勝！\n解散！", sound=True),
        friend("mock_swinging_cat", "それがさ……\n解散しねーのよ", dur=1.8),
        news("glare_disgusted_cat", "は？", dur=1.2, anchor=True),
        # ---- 5. 最後に決めるのは会議 ----
        narr("bg05_meeting", "ところが\n最後に決めるのは\n投票じゃない", "sleepy_sleepy_cat", se="don",
             ),
        card("e04_flow", "最後は「総長選考・監察会議」（16人）が決める", "call_customer_service_cat",
             b="bg05_meeting", dur=2.6),
        news("blank_black_cat_zoning_out", "……ん？", dur=1.2, flip=True),
        dict(bg=bg("bg05_meeting"), cats=[dict(MEETING[0], full=True), MEETING[1]],
             say="はーい、\nじゃ会議はじめまーす", say_name="会議の猫たち",
             pops=[{"t": t, "text": "はい", "box": (790, 600, 1050, 780), "size": 130} for t in (3.08, 8.88, 10.83)],
             plate_xy=(60, 900)),
        card("e04_flow", "投票は「参考にする材料の一つ」　書類や面接も合わせて決める", "slack_nail_filing_cat",
             b="bg05_meeting", dur=2.8),
        news("huh_goat_talks_to_huh_cat", "え、投票って\nただのアンケート\n的なやつ？"),
        friend("itchy_kitten_butt", "いや\nルールで「参考」って\n決まってんのよ"),
        news("sulk_hungry_cat", "ふーん……", dur=1.3),
        dict(bg=bg("bg05_meeting"), cats=MEETING, say="うーん……", say_name="会議の猫たち", plate_xy=(60, 900),
             dur=1.6, bgm={"file": None, "fade": 0.8}),
        news("sleep_sleeping_cat", "なげーよ", dur=1.3),
        dict(bg=bg("bg06_spotlight"), sub="そして選ばれたのは——", dur=2.0, se="drum"),
        dict(bg=bg("bg06_spotlight"), card=pt("e05c_reveal"), dur=2.8, se="don",
             cats=[{"a": "sleepy_old_memories_cat", "x": 960, "h": 300, "bottom": 1000, "float": True, "still": True}],
             sting={"file": os.path.join(BGM, "神の怒り.mp3"), "len": 6.0, "gain": -18}),
        # 発表後のリアクション（驚き → 戸惑い → 絶望）
        news("surprise_big_pupils_cat", "えええええ！？", dur=1.3, se="don"),
        news("weird_meowing_cat", "2位の人\nきたーーー！？", dur=1.5, flip=True),
        news("confused_i_dont_know_cat", "ちょ待って\n1位の人は？\nどこいったの？", flip=True),
        news("huh_huh_cat", "……は？\n半分以上\n取ってたよね？"),
        news("despair_dramatic_kitten", "投票の意味\nとは……", dur=1.6),
        news("sad_banana_cat_cry", "オレの予想\n外れたんだけど", dur=1.6),
        news("tense_two_cats_face_off", "マジかよ\n逆転じゃん", dur=1.8),
    ]


def person(b, a, say=None, name="", sub=None, **kw):
    """実在の人の再現（右に猫、左に大きな文字）。"""
    cat = {"a": a, "x": kw.pop("x", 1420), "h": kw.pop("h", 720), "bottom": 1010, "flip": kw.pop("flip", False)}
    d = dict(bg=bg(b), cats=[cat], **kw)
    if say:
        d.update(say=say, say_name=name, plate_xy=kw.get("plate_xy") or (1060, 900))
    if sub:
        d["sub"] = sub
    return d


def net(a, say, tag, **kw):
    """ネットの声（SNS背景・左に猫）。"""
    cat = {"a": a, "x": kw.pop("x", 500), "h": kw.pop("h", 720), "bottom": 1010, "flip": kw.pop("flip", False),
           "sound": kw.pop("sound", False)}
    return dict(bg=bg("bg09_sns"), cats=[cat], say=say, say_name=tag, **kw)


FUJI = "sleepy_old_memories_cat"
CHAIR = "listen_dancing_dog"
MIRAI = os.path.join(BGM, "未来を創る君たちへ.mp3")


def cuts_rest():
    """原稿 6〜11 章（藤垣さんの紹介 〜 まとめ）。"""
    return [
        # ---- 6. 藤垣さんってどんな人？ ----
        card("e06_profile", "藤垣裕子さん　1962年生まれ", "think_bike_front_seat_cat", b="bg08_study",
             bgm={"file": PURPLE, "gain": -7, "from": 40}),
        card("e06_profile", "専門は「科学技術社会論」", "think_bike_front_seat_cat", b="bg08_study", dur=2.0),
        news("huh_goat_talks_to_huh_cat", "かがくぎじゅつ\nしゃかいろん……？\nえ、呪文？"),
        card("e06_profile", "ざっくり言うと「科学と社会がどう付き合っていくか」の研究", "leave_cat_leaves_home",
             b="bg08_study", dur=2.8),
        card("e06_profile", "2021年から5年間　東大の副学長も務めた", "leave_cat_leaves_home", b="bg08_study", dur=2.4),
        news("showoff_gojo_cosplay_cat", "あー、中の人ってことね\nガチ勢じゃん"),
        friend("calm_black_face_sheep", "大学の中のこと\n知り尽くしてる人\nってわけ"),
        # ---- 7. 会議の言い分 ----
        card("e07_reasons", "会議が挙げた　選んだ理由", "angry_aiming_cat", b="bg05_meeting", dur=3.4),
        news("glare_disgusted_cat", "なんか、\nふわっとしてない？", anchor=True),
        friend("ride_kitten_bike", "まあ\n「総長に求める力」\nってやつな"),
        person("bg07_press", CHAIR, sub="会見で　議長は", dur=1.6),
        person("bg07_press", CHAIR, "いろんな資料とか\n面接とかをもとに\n何回もマジメに\n話し合ったんですよ",
               "議長（再現）", dur=3.2),
        person("bg07_press", CHAIR, "投票とズレたのは\nそんなに大きな\n問題じゃないと\n思ってます", "議長（再現）", dur=2.8),
        news("angry_shooting_cat", "言い切ったーーー", dur=1.6),
        news("sulk_hungry_cat", "いやまあ\nルール上は\nそうなんだろう\nけどさぁ"),
        # ---- 8. 藤垣さんの会見 ----
        person("bg07_press", FUJI, sub="翌29日　藤垣さんが会見", dur=1.8),
        person("bg07_press", FUJI, "ようやく初の女性\nこれはかなり\nメッセージ性\nあると思うんです",
               "藤垣さん（再現）", dur=3.2),
        person("bg07_press", "eat_crunchy_cat_luna", "研究者を目指す\n女の人が\nもっと増えたら\nうれしいなって", "藤垣さん（再現）", dur=2.8),
        person("bg07_press", "call_customer_service_cat", "アメリカの大学の\nお金の集め方は\n参考にしたいんです", "藤垣さん（再現）", dur=2.6),
        person("bg07_press", "realize_wet_cat_stare", "でも学問への\n信頼が落ちてる所は\nまねしちゃダメ\nだと思ってて",
               "藤垣さん（再現）", dur=3.0),
        person("bg07_press", "showoff_gojo_cosplay_cat", "今の総長の改革は\nちゃんと引き継いで\n広げていきます", "藤垣さん（再現）", dur=2.8),
        news("dance_trending_cat", "女性初は\nたしかに\nデカいよな", dur=1.6, se="pop"),
        news("angry_aiming_cat", "信頼の話は\nわかりみ", dur=1.4),
        news("wave_waving_cat", "お、\nふつうに\nしっかりしてるやん"),
        # ---- 9. 世の中の反応 ----
        narr("bg09_sns", "このニュースに\nネットでは\nさまざまな声が", "slack_nail_filing_cat"),
        net("joy_happy_happy_happy_cat", "150年で初！？\nおそすぎでしょ、\nでもおめ！", "歓迎する声", sound=True),
        net("mock_swinging_cat", "歴史\nうごいたぁぁ", "歓迎する声", dur=1.6),
        net("angry_cat_hits_cat", "過半数とった1位\n落とすなら\n投票いらなくね？", "投票の意味を問う声"),
        net("peek_what_happen_cat", "これ\n総長選の女子枠\nってこと？", "投票の意味を問う声"),
        news("spit_not_my_taste_cat", "うわー\nそれ言うやつ\n絶対いると思った"),
        friend("drive_driving_cat", "いろんな意見\n出まくってんのよ"),
        net("rage_talking_cat", "藤垣さん選んだ\n理由はわかったよ？", "説明が足りないという声"),
        net("huh_huh_cat", "で、染谷さんじゃ\nダメな理由は？\nどこ？\n書いてなくね？", "説明が足りないという声"),
        narr("bg03_blackboard", "選んだ人の\n良いところだけでは\n比べたかどうか\nわからない",
             "realize_wet_cat_stare"),
        news("sleepy_sleepy_cat", "あー、藤垣さんが\nダメとかじゃなくて"),
        news("drive_driving_cat", "決め方が\nブラックボックス\nなのがモヤる\nってことね"),
        # ---- 10. ほかの大学でも ----
        news("itchy_kitten_butt", "てかこういうの\n東大だけ？"),
        narr("bg10_kyoto", "実は\n投票の順位どおりに\nならなかった例は\nほかにもある", "eat_pop_cat"),
        card("e10_kyoto", "教職員の投票で6人中3位だった立川康人さんが学長に", "eat_pop_cat", b="bg10_kyoto", dur=2.8),
        news("weird_meowing_cat", "3位！？\n下剋上レベル\n上がってんだけど"),
        friend("rage_talking_cat", "京大で投票の結果が\n覆ったのは\n初めてらしいぞ"),
        card("e10_kyoto", "選考会議は「国際卓越研究大学」をめざす体制づくりなどをふまえたと説明", "confused_i_dont_know_cat",
             b="bg10_kyoto", dur=3.0),
        card("e10_kyoto", "教職員の組合は「教職員の意思を反映していない」と批判", "confused_i_dont_know_cat",
             b="bg10_kyoto", dur=2.8),
        card("e10b_tsukuba", "教職員の投票では対立候補が上回ったが　現職の学長が再任", "ride_kitten_bike", b="bg11_tsukuba",
             dur=3.0),
        card("e10b_tsukuba", "同時に　学長の任期の上限と　教職員の投票をなくした", "ride_kitten_bike", b="bg11_tsukuba",
             dur=2.6),
        news("spin_spinning_cat", "え、\nなにそれ", dur=1.3, se="pop"),
        news("angry_shooting_cat", "投票ごと\n消したの！？\n強すぎん！？",
             sting={"file": os.path.join(BGM, "神の怒り.mp3"), "len": 3.0, "gain": -18}),
        card("e10c_policy", "2014年ごろから　国が「学長は会議が主体的に選ぶように」と見直した", "calm_black_face_sheep",
             dur=3.0),
        news("laugh_laughing_dog", "あー、だから最近\nこういうの\n増えてんのか"),
        # ---- 11. まとめ ----
        dict(bg=bg("bg03_blackboard"), card=pt("e11_matome"), dur=3.0,
             cats=[{"a": "despair_dramatic_kitten", "x": 1700, "h": 380, "bottom": 1060, "float": True, "small": True}],
             bgm={"file": MIRAI, "gain": -7, "fade": 0.8}),
        news("think_bike_front_seat_cat", "ルール違反じゃないけど、\nモヤるのは\nしゃーないってことね"),
        friend("eat_pop_cat", "決めるのは会議\nでも説明は\nちゃんとしろって話"),
        news("excited_hodomoe_city_cat", "それな", dur=1.3, se="pop"),
        dict(bg=bg("bg03_blackboard"), card=pt("e12_ending"), dur=3.0, se="chime",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
    ]


# 効果音（catmeme/se/）。セリフ・字幕・カード画像の一部が一致したカットに付ける（上から順に最初の一致）
SE_MAP = [
    ("e00_notice", {"f": "chime_announce", "len": 3.0, "gain": -2}), ("e01_title", "chirin"), ("半分以上\n取ってたよね", "crack"), ("2026年9月28日", "quiz_question_01"), ("いやそれがさ", "quiz_den"),
    ("選ばれたのは\n投票で2位", "doon_heavy"), ("……は？", "question_hatena_maou"), ("いやいやいや", "tsukkomi_bishi"),
    ("2位？\n1位じゃなくて", "kote"), ("しかも\n東大150年", "jan"), ("ちょ、\n情報量", "explosion_chudoon"),
    ("まあ落ち着けって", "taiko_kaka"), ("たのむわ", "papa"),
    ("てか総長って", "pikon"), ("ちげーよ", "tsukkomi_bashi"), ("総長＝大学の", "page_turn_01"),
    ("呼び方つっよ", "punch"), ("次の総長の任期", "card_place"), ("6年！？", "taiko_dodon_01"),
    ("候補者は5人", "game_smash_challenger"), ("全員つよそう", "aura_02"), ("副学長とか理事とか", "shine_kira_01"),
    ("どうやって\n選ぶん", "cursor_move_01"),
    ("学内の先生たちが投票", "button_13"), ("どれにしよ", {"f": "thinking_time", "gain": -8}), ("結果\nはよ", "spo"),
    ("2回目の投票の", "drumroll"), ("染谷さんが過半数", "fanfare_pararappara"), ("え、1位の人", "kon"),
    ("解散しねーのよ", "deflate_hyororo"), ("e05_votes", None),
    ("ところが\n最後に", "doon_movie"), ("最後は「総長選考", "page_turn_02"), ("……ん？", "pi"),
    ("じゃ会議はじめまーす", "gong_match_start"), ("投票は「参考に", "card_flip"), ("え、投票って", "boing_fail"),
    ("ルールで「参考」", "hyoshigi_01"), ("ふーん……", "silly"), ("うーん……", {"f": "mokugyo_pokupoku", "gain": -6}),
    ("なげーよ", "tsukkomi_bashi"), ("そして選ばれたのは", "drumroll"), ("e05c_reveal", "taiko_dodon_02"),
    ("えええええ！？", "voice_uuwaa"), ("きたーーー！？", "tv_gakitsuka_dedeen"), ("ちょ待って\n1位の人は", "car_brake"),
    ("投票の意味\nとは", "shock_piano"), ("オレの予想", "tear_drop"),
    ("マジかよ\n逆転", "glass_break_01"),
    ("藤垣裕子さん　1962年", "xylophone_transition"), ("専門は「科学技術", "page_turn_01"),
    ("かがくぎじゅつ", "question_hatena_maou"), ("ざっくり言うと", "idea_newtype_01"), ("2021年から5年間", "card_place"),
    ("中の人ってことね", "shine_kiraan_maou"),
    ("会議が挙げた", "pinpoon_note"), ("ふわっとしてない", "puni"), ("会見で　議長は", "cymbal_light_maou"),
    ("言い切ったーーー", "game_aceattorney_desk_slam"), ("ルール上は\nそうなんだろう", "kote"),
    ("翌29日", "button_39"), ("女性初は", "bell_ring"),
    ("しっかりしてるやん", {"f": "cheer_applause", "gain": -8}),
    ("このニュースに", "button_26"), ("歴史\nうごいた", "game_dq_level_up"), ("過半数とった1位", "buzzer_wrong"),
    ("総長選の女子枠", "kon"), ("それ言うやつ", "fall_hyuu"), ("藤垣さん選んだ", "cursor_move_02"),
    ("で、染谷さんじゃ", "anime_shinchan_taraan"), ("良いところだけでは", "pinpon_notice"),
    ("ブラックボックス", "pc_warning"),
    ("てかこういうの", "spring_byoin"), ("投票の順位どおりに", "quiz_den"), ("6人中3位だった", "hyoshigi_02"),
    ("下剋上レベル", "explosion_dokaan"), ("「国際卓越研究大学」", "page_turn_02"), ("教職員の組合", "pi"),
    ("対立候補が上回った", "whoosh_shu"), ("同時に　学長の任期", "doon_heavy"), ("え、\nなにそれ", "boing_02"),
    ("2014年ごろから", "card_flip"), ("だから最近", "pikoon_retro"),
    ("e11_matome", "chiin_01"), ("ちゃんとしろって話", "taiko_kaka"), ("それな", "tsukkomi_bishi"),
    ("e12_ending", "chirin"),
]


# 猫ミーム素材を途中で切らずに最後まで流すカット
FULL = ["2位？\n1位じゃなくて", "情報量\nバグってんだけど", "結果\nはよ", "染谷さんが過半数", "2位の倍よ倍"]


def apply_se(cuts):
    for c in cuts:
        k = " ".join(str(c.get(x) or "") for x in ("say", "sub"))
        if any(f in k for f in FULL) and c.get("cats"):
            c["cats"][0]["full"] = True
    for c in cuts:
        key = " ".join(str(c.get(k) or "") for k in ("say", "sub", "card", "layers"))
        for snip, se in SE_MAP:
            if snip in key:
                if se is None:
                    break
                c["se"] = se
                break
    return cuts


def cuts_full():
    return apply_se(cuts_trial() + cuts_rest())



if __name__ == "__main__":
    full = "--trial" not in sys.argv
    sys.argv = [a for a in sys.argv if a != "--trial"]
    out = os.path.join(HERE, "out", "01_todai_full.mp4" if full else "01_todai_trial.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cuts = cuts_full() if full else cuts_trial()
    if sys.argv[1:] == ["--audio"]:   # 音だけ作り直す
        R.remux_audio(cuts, out, out.replace(".mp4", "_a.mp4"))
        os.replace(out.replace(".mp4", "_a.mp4"), out)
        sys.exit()
    if len(sys.argv) > 1:   # 例: python3 cuts_01_todai.py 0:5 → 先頭5カットだけ
        a, b = (int(x) if x else None for x in sys.argv[1].split(":"))
        cuts = cuts[a:b]
    R.render(cuts, out, preview_dir=out.replace(".mp4", "_preview"))
