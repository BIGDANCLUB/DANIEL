"""02_october_changes（10月1日から変わったこと）のカット割り。原稿 scripts/02_october_changes.md。

python3 catmeme/cuts_02_october.py          → out/02_october_full.mp4
python3 catmeme/cuts_02_october.py --audio  → 音だけ作り直す
python3 catmeme/cuts_02_october.py 0:10     → 先頭10カットだけ
"""
import os
import sys

import render as R


HERE = os.path.dirname(os.path.abspath(__file__))
BG = os.path.join(HERE, "backgrounds", "02_october")
BG01 = os.path.join(HERE, "backgrounds", "01_todai")   # 部屋・黒板・スポットライト・スマホは1本目のを使い回す
PT = os.path.join(HERE, "parts", "02_october")
BGM = os.path.join(HERE, "bgm")

PURPLE = os.path.join(BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")
COCOA = os.path.join(BGM, "星降る夜のホットココア.mp3")
MIRAI = os.path.join(BGM, "未来を創る君たちへ.mp3")
KAMI = os.path.join(BGM, "神の怒り.mp3")


def bg(n):
    p = os.path.join(BG, n + ".png")
    return p if os.path.exists(p) else os.path.join(BG01, n + ".png")


def pt(n):
    return os.path.join(PT, n + ".png")


def news(a, say, b="bg02_room", **kw):
    """ニュース猫（左）のセリフ。"""
    cat = {"a": a, "x": kw.pop("x", 500), "h": kw.pop("h", 760), "bottom": 1010, "flip": kw.pop("flip", False),
           "ss": kw.pop("ss", 0.0), "anchor": kw.pop("anchor", False), "sound": kw.pop("sound", False)}
    return dict(bg=bg(b), cats=[cat], say=say, say_name="ニュース猫", **kw)


def sage(a, say, b="bg02_room", **kw):
    """博識な猫（右）のセリフ。"""
    cat = {"a": a, "x": kw.pop("x", 1420), "h": kw.pop("h", 740), "bottom": 1010, "flip": kw.pop("flip", False),
           "sound": kw.pop("sound", False), "anchor": kw.pop("anchor", False)}
    return dict(bg=bg(b), cats=[cat], say=say, say_name="博識な猫", plate_xy=(1080, 900), **kw)


def beer(a, say, b="bg13_izakaya", **kw):
    """ビール猫（右・ビール派）。"""
    cat = {"a": a, "x": kw.pop("x", 1420), "h": kw.pop("h", 740), "bottom": 1010, "flip": kw.pop("flip", False),
           "sound": kw.pop("sound", False)}
    return dict(bg=bg(b), cats=[cat], say=say, say_name="ビール猫", plate_xy=(1080, 900), **kw)


def third(a, say, b="bg14_home_night", **kw):
    """第三のビール猫（左・毎晩第三のビール）。"""
    cat = {"a": a, "x": kw.pop("x", 500), "h": kw.pop("h", 740), "bottom": 1010, "flip": kw.pop("flip", False),
           "sound": kw.pop("sound", False)}
    return dict(bg=bg(b), cats=[cat], say=say, say_name="第三のビール猫", **kw)


def narr(b, sub, a, **kw):
    """ナレーション（左に猫、右に大きな文字）。"""
    cat = {"a": a, "x": kw.pop("x", 470), "h": kw.pop("h", 640), "bottom": 990, "flip": kw.pop("flip", False),
           "sound": kw.pop("sound", False)}
    return dict(bg=bg(b), cats=[cat], sub=sub, **kw)


def card(c, sub, cat=None, b="bg03_blackboard", **kw):
    """解説カード＋右下の小さい猫＋字幕。"""
    cats = [{"a": cat, "x": 1752, "h": 330, "bottom": 830, "float": True, "small": True,
             "sound": kw.pop("sound", False)}] if cat else []
    return dict(bg=bg(b), card=pt(c), cats=cats, sub=sub, **kw)


def net(a, say, tag, **kw):
    """ネットの声（スマホ背景・左に猫）。"""
    cat = {"a": a, "x": kw.pop("x", 500), "h": kw.pop("h", 720), "bottom": 1010, "flip": kw.pop("flip", False),
           "sound": kw.pop("sound", False)}
    return dict(bg=bg("bg09_sns"), cats=[cat], say=say, say_name=tag, **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=3.2),
        # ---- 1. つかみ ----
        dict(bg=bg("bg12_liquor_shelf"), card=pt("e01_title"), dur=2.4, bgm={"file": PURPLE, "gain": -7},
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        narr("bg12_liquor_shelf", "2026年10月1日\nいろんなものの\n値段が\n一気に変わった", "work_typing_cat"),
        news("peek_what_happen_cat", "え、またなんか\n上がったの？"),
        news("angry_shooting_cat", "ここ最近ずっと\n全部値上げじゃん！", dur=1.9),
        narr("bg06_spotlight", "ビール\n安くなる", "dance_koto_nai_cat", dur=1.8),
        beer("joy_happy_happy_happy_cat", "よっしゃ\nああああ", sound=True),
        narr("bg06_spotlight", "第三のビール\n高くなる", "blank_black_cat_zoning_out", dur=1.8),
        third("huh_goat_talks_to_huh_cat", "……は？"),
        narr("bg06_spotlight", "チューハイも\n高くなる", "slack_nail_filing_cat", dur=1.8),
        third("despair_dramatic_kitten", "はぁぁぁぁぁ!?"),
        news("confused_i_dont_know_cat", "ビールだけ\n得してんの、\nなんで？？", flip=True),
        narr("bg12_liquor_shelf", "ほかにも\n食べ物・たばこ\nゆうパック\nパートの「壁」まで", "call_customer_service_cat"),
        news("spin_spinning_cat", "多い多い多い", dur=1.5),
        sage("itchy_kitten_butt", "じゃ、\nひとつずつ\n見てくか", dur=1.8),
        # ---- 2. 酒税ってなに？ ----
        news("think_bike_front_seat_cat", "酒税って\n詳しく\n知らないんだよなぁ"),
        card("e02_sake", "お酒には　消費税とは別に「酒税」がかかっている", "eat_crunchy_cat_luna", dur=2.6),
        card("e02_sake", "しかも　お酒の種類ごとに　税額がちがう", "eat_crunchy_cat_luna", dur=2.4),
        sage("work_typing_cat", "缶1本ごとに\n決まった額の\n税金が\n入ってんのよ"),
        news("realize_wet_cat_stare", "知らんかった……\n毎回\n払ってたのか"),
        # ---- 3. ビール系の税、ついに同じ額に ----
        card("e03_beer3", "これまで　ビール系は3種類で　税額がバラバラ", "ride_kitten_bike", b="bg12_liquor_shelf",
             dur=2.6),
        card("e03_beer3", "麦芽が少ないほど　税金が安かった", "ride_kitten_bike", b="bg12_liquor_shelf", dur=2.2),
        news("sulk_hungry_cat", "だから\n第三のビールって\n安かったのか"),
        sage("drive_driving_cat", "そう。\nでもそれが\nややこしい話に\nなってさ"),
        card("e03b_itachi", "メーカーが「ビールっぽいけど税金の安いお酒」を次々開発", "excited_hodomoe_city_cat",
             dur=2.8),
        card("e03b_itachi", "国は　そのたびにルールを変えて　税を上げる", "excited_hodomoe_city_cat", dur=2.4),
        news("cocky_dj_cat", "ルールハック\nするヤツと\nそれを修正する\n運営って感じ"),
        sage("calm_black_face_sheep", "国いわく\n「お酒どうしの\n税の公平さ」\nのためだってさ"),
        news("sleepy_old_memories_cat", "公平……\nねぇ……", dur=1.6),
        card("e03c_plan", "そこで2017年に決めた　「3回に分けて　ビール系の税を同じ額にそろえる」", "dance_wop_cat",
             dur=3.0),
        card("e03c_plan", "ちなみに　日本酒とワインは　2023年に先にそろった", "dance_wop_cat", dur=2.4),
        card("e04_beer", "ビールの税金は　少しずつ下がって　今回 54.25円に", "happy_girlfriend_dance_cat", dur=2.8),
        card("e04b_third", "第三のビールは　28円から　54.25円に", "sad_banana_cat_cry", dur=2.6),
        news("surprise_big_pupils_cat", "え、\n第三のビール\n28円から54円！？", se="don"),
        news("rage_talking_cat", "ほぼ2倍\nじゃん！！",
             sting={"file": KAMI, "len": 5.0, "gain": -18}),
        card("e04_beer", "今回の10月で　ビールは1本9.10円の減税", "taunt_cat_and_scared_dog", b="bg12_liquor_shelf",
             dur=2.4),
        card("e04b_third", "第三のビール・発泡酒は　1本7.26円の増税", "taunt_cat_and_scared_dog",
             b="bg12_liquor_shelf", dur=2.4),
        beer("dance_maxwell_cat", "ビール派、\n勝ち〜", sound=True),
        third("sad_banana_cat_cry", "こっちは\n毎日\n飲んでんのよ……"),
        beer("cocky_dj_cat", "まあまあ\nたまには\nビール飲めば？", flip=True),
        third("angry_aiming_cat", "そのたまにが\n高いんだって！"),
        beer("listen_dancing_dog", "……\nなんか\nごめん", dur=1.6),
        sage("slack_nail_filing_cat", "ちなみに\n減った税の分\n値段がそのまま\n下がるとは\n限らんからね", dur=2.6),
        news("glare_disgusted_cat", "え、そこ\n一番大事なとこ", anchor=True),
        # ---- 4. チューハイ・たばこ ----
        card("e05_chuhai", "チューハイなども　1本28円 → 35円（7円の増税）", "eat_pop_cat", b="bg15_convenience",
             dur=2.8),
        third("leave_cat_leaves_home", "チューハイに\n逃げようと\n思ってたのに", b="bg15_convenience"),
        card("e05_chuhai", "加熱式たばこ　4月に続いて2回目の値上げ（1箱20〜40円ほど）", "work_typing_cat",
             b="bg15_convenience", dur=3.0),
        card("e05_chuhai", "紙巻きたばこは　2027年4月から増税の予定", "work_typing_cat", b="bg15_convenience", dur=2.4),
        news("mock_swinging_cat", "年2回値上げって\nなに？\n捕獲レベル並みの\nインフレじゃん", b="bg15_convenience"),
        sage("think_bike_front_seat_cat", "計算の仕方を\n2回に分けて\n変えてんのよ", b="bg15_convenience"),
        # ---- 5. 食べ物・郵便 ----
        card("e06_food", "10月に値上げされる食べ物・飲み物　3,033品目", "call_customer_service_cat", b="bg16_food_aisle",
             dur=2.6, bgm={"file": COCOA, "gain": -7}),
        card("e06_food", "2026年は1〜11月の分だけで　1万9,083品目", "call_customer_service_cat", b="bg16_food_aisle",
             dur=2.6),
        news("blank_black_cat_zoning_out", "1万9千……\nもう数字の感覚\nバグる", b="bg16_food_aisle"),
        card("e07_post", "ゆうパック　平均 約10％の値上げ", "drive_monkey_golf_cart", b="bg17_post_office", dur=2.4),
        card("e07_post", "クリックポストは　185円 → 240円", "drive_monkey_golf_cart", b="bg17_post_office", dur=2.4),
        news("huh_huh_cat", "55円も\n上がってんの！？", b="bg17_post_office"),
        card("e07_post", "ゆうパケットも　厚さ1〜3cmは　360円に統一", "taunt_cat_and_scared_dog", b="bg17_post_office",
             dur=2.6),
        sage("eat_pop_cat", "燃料とか人件費とか\n全部上がってる\nからって説明", b="bg17_post_office"),
        net("calm_black_face_sheep", "フリマで\n売るたびに\n送料で消える\nんだが", "フリマ勢の声"),
        # ---- 6. 106万円の壁 ----
        news("weird_meowing_cat", "お酒とたばこ\n以外も\nあんの？"),
        sage("wakeup_dog_hits_bowl", "パートの人に\nデカい話が\nあんのよ"),
        card("e08_wall", "会社の社会保険に入る条件のうち「月8万8千円以上」がなくなった", "peek_what_happen_cat",
             b="bg18_backyard", dur=3.0),
        sage("fight_cat_fight", "これが\n“106万円の壁”\nね", b="bg18_backyard", dur=1.8),
        card("e08_wall", "これからは　週20時間以上働くかどうかが基準（今は51人以上の会社）", "ride_kitten_bike",
             b="bg18_backyard", dur=3.0),
        news("huh_goat_talks_to_huh_cat", "え、じゃあ\n給料関係なく\n入るってこと？", b="bg18_backyard"),
        card("e08_wall", "対象の会社は　2027年10月から少しずつ広がり　2035年10月には規模の条件もなくなる",
             "drive_monkey_golf_cart", b="bg18_backyard", dur=3.2),
        news("dance_edm_cat", "10年がかり\nかよ", b="bg18_backyard", dur=1.6),
        card("e08b_merit", "入ると　保険料が給料から引かれる → 手取りは減る", "sleepy_sleepy_cat", b="bg18_backyard",
             dur=2.6),
        card("e08b_merit", "そのかわり　将来の年金が増える・病気やケガのときの手当がある", "sleepy_sleepy_cat",
             b="bg18_backyard", dur=2.8),
        news("sulk_hungry_cat", "今の手取り\n減るのは\nキツいって", b="bg18_backyard"),
        sage("tense_two_cats_face_off", "将来の年金と\n今の財布の\n綱引きってやつ", b="bg18_backyard"),
        card("e08b_merit", "なお　家族の扶養に入れるかの「130万円の壁」は　そのまま", "listen_dancing_dog",
             b="bg18_backyard", dur=2.8),
        news("angry_cat_hits_cat", "壁、\nまだあんのかい", b="bg18_backyard", dur=1.8),
        # ---- 7. ネットの声 ----
        narr("bg09_sns", "この10月の変化に\nネットでは\n不満の声が\n目立った", "realize_wet_cat_stare"),
        net("laugh_laughing_dog", "ビール減税、9円？\n1本あたり？\n誤差では？", "減税への声"),
        net("glare_disgusted_cat", "第三のビール勢から\n取って\nビール勢に配るの\n草", "増税への不満"),
        net("rage_talking_cat", "安い酒を作る努力を\nルール変更で\n潰してきた歴史", "増税への不満"),
        net("spit_not_my_taste_cat", "どうせ減税分\n値下げしないで\n終わり", "減税への声"),
        net("angry_aiming_cat", "106万の壁\nなくすなら\n130万の壁も\nなくして", "壁への不満"),
        net("despair_dramatic_kitten", "“将来のため”って\nその将来\nちゃんとある？", "壁への不満"),
        net("sleep_sleeping_cat", "値上げのニュース\n毎月\n同じこと言ってない？", "値上げへの声"),
        net("surprise_big_pupils_cat", "ゆうパケット\n360円統一って\n薄いのも\n高くなるじゃん", "フリマ勢の声"),
        net("fight_cat_fight", "結局\n取れるところから\n取ってるだけ", "値上げへの声"),
        narr("bg09_sns", "一方で", "showoff_gojo_cosplay_cat", dur=1.4),
        net("happy_chipi_chapa_cat", "ビール党の自分\n10月が\n待ち遠しかった", "歓迎する声", sound=True),
        net("dance_trending_cat", "税がそろうなら\n純粋に味で\n選べる", "歓迎する声"),
        news("calmdown_dancing_cat", "まあ、\n得する人と\n損する人が\nハッキリ分かれた\nってことね"),
        # ---- 8. まとめ ----
        dict(bg=bg("bg03_blackboard"), card=pt("e09_matome"), dur=4.2,
             cats=[{"a": "eat_crunchy_cat_luna", "x": 1752, "h": 330, "bottom": 830, "float": True, "small": True}],
             bgm={"file": MIRAI, "gain": -7, "fade": 0.8}),
        sage("showoff_gojo_cosplay_cat", "ビール系の税は\n今回で\n“全部同じ”\n最終回ってわけ"),
        news("excited_hodomoe_city_cat", "で、結局\nうちらは\nどうすりゃいいの？"),
        sage("itchy_kitten_butt", "自分に関係ある\nとこだけでも\nチェックしとけ\nってこと"),
        news("eat_pop_cat", "とりあえず\nレシート\nちゃんと見るわ"),
        dict(bg=bg("bg03_blackboard"), card=pt("e10_ending"), dur=3.0,
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
    ]


# 効果音（catmeme/se/）。セリフ・字幕・カード画像の一部が一致したカットに付ける（上から順に最初の一致）
SE_MAP = [
    ("国いわく", "pinpon_notice"), ("公平……", "mokugyo_pokupoku"), ("日本酒とワインは", "card_place"),
    ("たまには\nビール", "boing_02"), ("そのたまにが", "punch"), ("なんか\nごめん", "deflate_hyororo"),
    ("厚さ1〜3cmは", "card_flip"), ("燃料とか", "cursor_move_01"), ("2035年10月", "whoosh_shu"),
    ("10年がかり", "tsukkomi_bashi"), ("薄いのも", "buzzer_wrong"), ("取れるところから", "kon"),
    ("どうすりゃいい", "question_hatena_maou"), ("チェックしとけ", "pinpoon_note"),
    ("e00_notice", {"f": "chime_announce", "len": 3.0, "gain": -2}), ("e01_title", "chirin"),
    ("一気に変わった", "quiz_question_01"), ("またなんか", "pi"), ("全部値上げ", "explosion_chudoon"),
    ("ビール\n安くなる", "fanfare_pararappara"), ("第三のビール\n高くなる", "doon_heavy"), ("……は？", "question_hatena_maou"),
    ("チューハイも\n高くなる", "doon_movie"), ("はぁぁぁ", "shock_piano"), ("ビールだけ\n得して", "kote"),
    ("ほかにも\n食べ物", "jan"), ("多い多い", "tsukkomi_bishi"), ("ひとつずつ", "taiko_kaka"),
    ("酒税って", "pikon"), ("消費税とは別に", "page_turn_01"), ("種類ごとに", "card_place"),
    ("缶1本ごとに", "idea_newtype_01"), ("知らんかった", "tear_drop"),
    ("3種類で", "xylophone_transition"), ("麦芽が少ないほど", "card_flip"), ("安かったのか", "pinpoon_note"),
    ("ややこしい話", "quiz_den"), ("次々開発", "whoosh_shu"), ("そのたびにルール", "hyoshigi_01"),
    ("ルールハック", "punch"), ("2017年に決めた", "page_turn_02"), ("今回 54.25円", "shine_kira_01"),
    ("28円から　54.25円", "fall_hyuu"), ("28円から54円", "don"), ("ほぼ2倍", "explosion_dokaan"),
    ("9.10円の減税", "pinpoon_correct"), ("7.26円の増税", "buzzer_wrong"), ("ビール派、", None),
    ("毎日\n飲んでんの", "deflate_hyororo"), ("限らんからね", "cymbal_light_maou"), ("一番大事", "car_brake"),
    ("28円 → 35円", "boon"), ("逃げようと", "boing_fail"), ("2回目の値上げ", "pi"), ("紙巻き", "card_place"),
    ("捕獲レベル", "glass_break_01"), ("2回に分けて", "tsukkomi_bashi"),
    ("3,033品目", "button_13"), ("1万9,083", "boon"), ("感覚\nバグる", "silly"),
    ("約10％の値上げ", "button_26"), ("185円 → 240円", "pc_warning"), ("55円も", "voice_uuwaa"), ("送料で消える", "kon"),
    ("以外も\nあんの", "spring_byoin"), ("デカい話", "aura_02"), ("8万8千円以上", "doon_heavy"), ("106万円の壁”", "jan"),
    ("週20時間以上", "card_flip"), ("給料関係なく", "question_hatena_maou"), ("手取りは減る", "fall_hyuu"),
    ("将来の年金が増える", "shine_kiraan_maou"), ("キツいって", "punch"), ("綱引き", "taiko_kaka"),
    ("130万円の壁", "doon_movie"), ("まだあんのかい", "tsukkomi_bishi"),
    ("不満の声", "quiz_question_02"), ("誤差では", "kon"), ("草", "boing_01"), ("潰してきた", "boon"),
    ("値下げしないで", "pi"), ("130万の壁も", "buzzer_wrong"), ("その将来", "shock_piano"), ("毎月", "silly"),
    ("一方で", "whoosh_shu"), ("ビール党", None), ("味で", "pinpoon_correct"), ("ハッキリ分かれた", "taiko_kaka"),
    ("e09_matome", "chiin_01"), ("最終回", "hyoshigi_02"), ("レシート", "pikoon_retro"), ("e10_ending", "chirin"),
]

# 猫ミーム素材を途中で切らずに最後まで流すカット（切る秒は assets/play.json）
FULL = ["よっしゃ", "ビール派、", "ビール党", "はぁぁぁ"]


def apply_se(cuts):
    for c in cuts:
        k = " ".join(str(c.get(x) or "") for x in ("say", "sub"))
        if any(f in k for f in FULL) and c.get("cats"):
            c["cats"][0]["full"] = True
            cfg = R.ASSET_PLAY.get(c["cats"][0]["a"], {})
            if cfg.get("until"):
                c["cats"][0]["until"] = cfg["until"]
    for c in cuts:
        key = " ".join(str(c.get(k) or "") for k in ("say", "sub", "card", "layers"))
        for snip, se in SE_MAP:
            if snip in key:
                if se is not None:
                    c["se"] = se
                break
    return cuts


def cuts_full():
    return apply_se(cuts_all())


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "02_october_full.mp4")
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
