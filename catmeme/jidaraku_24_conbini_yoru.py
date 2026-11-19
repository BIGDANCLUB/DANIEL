"""自堕落シリーズ #24：30代独身男、平日5日間のコンビニ夜ごはん（11/19 ユーザー指定）。8分をこえる長さ。

python3 catmeme/jidaraku_24_conbini_yoru.py → out/jidaraku_24_conbini_yoru.mp4
- 流れ：日曜の夜「今週こそ健康に」→ 月曜はサラダ・サラダチキン・野菜ジュース → 火曜おにぎり2個 → 水曜からあげ弁当 →
  木曜カップ麺 → 金曜ビールとからあげ、23時にアイスも → 土曜の朝、冷蔵庫に残ったサラダチキン → 来週こそ
- #3（金曜のコンビニはしご）とは別の話：平日の5日間で健康の決意がくずれていくようす。店名・値段は出さない
- 11/17 からのルール：場面転換ゆっくり・字幕は1行12字・最大2行・2.5〜3秒・職場の回想なし
- 料理の絵は backgrounds/shorts_pic/pic_cv_*.png（ショート119と同じユーザー提供の8枚）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku")]
ROOM, ROOM_N, STREET_N, SHOP = "j01_room", "j07_room_night", "bg51_night_street", "st03_konbini"
J.HOLD = 6
J.LOOPS = 1
J.TEMPO_K = 1.3
J.SUB_SEC = (2.5, 3.0)
J.SUB_STYLE = "glow"
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
MORNING = os.path.join(L.BGM, "Morning.mp3")
SALAD, CHICKEN, VEG, ONIGIRI, BENTO, CUP, BEER, ICE = ("pic_cv_salad", "pic_cv_chicken", "pic_cv_veggie", "pic_cv_onigiri",
                                                       "pic_cv_bento", "pic_cv_cupmen", "pic_cv_beer", "pic_cv_ice")


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 日曜の夜 ----
        s(ROOM_N, "stare_lying_tabby_cat", "日曜日の夜", bgm={"file": LOFI, "gain": -12}),
        s(ROOM_N, "sad_looking_away_tabby", "体重計に乗る"),
        s(ROOM_N, "surprise_big_pupils_cat", "……見なかったことにしたい", se="pi"),
        s(ROOM_N, "despair_dramatic_kitten", "先週の夜ごはんを思い出す"),
        s(ROOM_N, "calm_black_face_sheep", "全部コンビニだった"),
        s(ROOM_N, "think_chin_paw_orange_cat", "ひとり暮らしの平日"),
        s(ROOM_N, "sleepy_sleepy_cat", "帰ってから料理する元気はない"),
        s(ROOM_N, "read_book_orange_kitten", "でもコンビニにも\n体にいいものはある"),
        s(ROOM_N, "angry_aiming_cat", "決めた"),
        s(ROOM_N, "showoff_gojo_cosplay_cat", "今週こそ健康に生きる", se="gong_dora_jaan"),
        s(ROOM_N, "smug_squint_bicolor_cat", "コンビニで\n健康になってみせる"),
        s(ROOM_N, "read_book_orange_kitten", "ルールを決める"),
        s(ROOM_N, "read_book_orange_kitten", "その1\n揚げものは買わない"),
        s(ROOM_N, "read_book_orange_kitten", "その2\nレジ横は見ない"),
        s(ROOM_N, "read_book_orange_kitten", "その3\n夜11時すぎは\nコンビニに行かない"),
        s(ROOM_N, "rizz_cat_rizz", "完璧な計画だ"),
        s(ROOM_N, "sleep_sleeping_cat", "早めに寝る"),
        # ---- 月曜 ----
        s(STREET_N, "drive_driving_cat", "月曜日の夜8時", se="whoosh_shu", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(STREET_N, "stare_tabby_wide_eyes_cat", "帰り道の\nコンビニの明かり"),
        s(STREET_N, "happy_hamster_open_arms", "いつ見ても安心する"),
        s(SHOP, "leave_cat_leaves_home", "入店", se="pikon"),
        s(SHOP, "angry_aiming_cat", "今日は迷わない"),
        s(SHOP, "work_typing_cat", "まっすぐサラダの棚へ", item=SALAD),
        s(SHOP, "smug_squint_bicolor_cat", "レタスとトマトとコーン", item=SALAD),
        s(SHOP, "rizz_cat_rizz", "野菜を選ぶ俺", item=SALAD),
        s(SHOP, "read_book_orange_kitten", "たんぱく質も大事", item=CHICKEN),
        s(SHOP, "showoff_gojo_cosplay_cat", "サラダチキン", item=CHICKEN, se="shine_kiraan_maou"),
        s(SHOP, "smug_squint_bicolor_cat", "鍛えている人は\nみんなこれを食べている", item=CHICKEN),
        s(SHOP, "think_chin_paw_orange_cat", "飲みものは", item=VEG),
        s(SHOP, "happy_girlfriend_dance_cat", "野菜ジュース", item=VEG),
        s(SHOP, "rizz_cat_rizz", "完璧な組み合わせだ", item=VEG),
        s(SHOP, "peek_what_happen_cat", "レジの横で\nからあげが光っている"),
        s(SHOP, "calm_black_face_sheep", "見ない"),
        s(SHOP, "angry_aiming_cat", "今週の俺は\nちがう"),
        s(SHOP, "stare_interviewer_cat", "袋はご利用ですか？"),
        s(SHOP, "smug_squint_bicolor_cat", "エコバッグがあります"),
        s(SHOP, "rizz_cat_rizz", "今週の俺は\n地球にもやさしい"),
        s(ROOM_N, "work_typing_cat", "家に帰って\nテーブルに並べる", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(ROOM_N, "smug_squint_bicolor_cat", "健康の三種の神器", item=SALAD),
        s(ROOM_N, "eat_crunchy_cat_luna", "シャキシャキ", item=SALAD, se="pikon"),
        s(ROOM_N, "eat_pop_cat", "サラダチキンを\nほぐしてのせる", item=CHICKEN),
        s(ROOM_N, "happy_hamster_open_arms", "体が\nよろこんでいる気がする", item=CHICKEN),
        s(ROOM_N, "eat_crunchy_cat_luna", "野菜ジュースで\nしめる", item=VEG, se="drink_gulp_gokugoku_thirsty_chug"),
        s(ROOM_N, "realize_wet_cat_stare", "なんて健康なんだ", item=VEG),
        s(ROOM_N, "think_chin_paw_orange_cat", "サラダチキンは\nもう1個買ってある", item=CHICKEN),
        s(ROOM_N, "rizz_cat_rizz", "明日のぶんも\n準備ばんたん", item=CHICKEN),
        s(ROOM_N, "sleepy_old_memories_cat", "夜10時"),
        s(ROOM_N, "sulk_hungry_cat", "……おなかがすいた", se="pi"),
        s(ROOM_N, "despair_dramatic_kitten", "サラダは\nすぐ消える"),
        s(ROOM_N, "calm_black_face_sheep", "水を飲んで寝る"),
        s(ROOM_N, "smug_squint_bicolor_cat", "でも\nルールは守った"),
        s(ROOM_N, "happy_hamster_open_arms", "月曜日\n大勝利"),
        # ---- 火曜 ----
        s(STREET_N, "stare_lying_tabby_cat", "火曜日の夜9時", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(STREET_N, "sleepy_sleepy_cat", "今日は少し\n疲れた"),
        s(SHOP, "think_chin_paw_orange_cat", "サラダの棚の前に立つ"),
        s(SHOP, "stare_tabby_wide_eyes_cat", "昨日の夜10時の\n空腹を思い出す"),
        s(SHOP, "read_book_orange_kitten", "人は野菜だけでは\n生きていけない"),
        s(SHOP, "angry_aiming_cat", "お米も大事だ", item=ONIGIRI),
        s(SHOP, "happy_girlfriend_dance_cat", "おにぎり2個", item=ONIGIRI, se="pikon"),
        s(SHOP, "smug_squint_bicolor_cat", "鮭と梅", item=ONIGIRI),
        s(SHOP, "rizz_cat_rizz", "和食だから\n健康", item=ONIGIRI),
        s(SHOP, "peek_what_happen_cat", "となりで\n同じくらいの年の人が\nサラダを買っている"),
        s(SHOP, "sad_looking_away_tabby", "なんだか\n負けた気がする"),
        s(SHOP, "think_chin_paw_orange_cat", "いや\n勝ち負けではない"),
        s(SHOP, "calm_black_face_sheep", "おにぎりも\n立派な食事だ"),
        s(ROOM_N, "eat_pop_cat", "パリッ", item=ONIGIRI, se="pikon"),
        s(ROOM_N, "happy_hamster_open_arms", "のりの音がいい", item=ONIGIRI),
        s(ROOM_N, "eat_crunchy_cat_luna", "お米って\nこんなにうまかったか", item=ONIGIRI),
        s(ROOM_N, "sleepy_old_memories_cat", "冷蔵庫には\n昨日のサラダチキン", item=CHICKEN),
        s(ROOM_N, "calm_black_face_sheep", "あしたでいいか", item=CHICKEN),
        s(ROOM_N, "think_chin_paw_orange_cat", "まだ健康の範囲だ"),
        # ---- 水曜 ----
        s(STREET_N, "work_typing_cat", "水曜日の夜10時", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(STREET_N, "despair_dramatic_kitten", "残業だった"),
        s(STREET_N, "sad_black_dog", "週の真ん中が\nいちばん重い"),
        s(SHOP, "stare_big_eyes_tabby_kitten", "お弁当の棚が\n目に入る"),
        s(SHOP, "surprise_big_pupils_cat", "からあげ弁当", item=BENTO, se="pi"),
        s(SHOP, "think_chin_paw_orange_cat", "サラダが\nついている", item=BENTO),
        s(SHOP, "smug_squint_bicolor_cat", "つまり\nこれも健康", item=BENTO),
        s(SHOP, "rizz_cat_rizz", "残業したから\nセーフ", item=BENTO),
        s(SHOP, "read_book_orange_kitten", "ルールその1\n揚げものは買わない", item=BENTO),
        s(SHOP, "think_chin_paw_orange_cat", "でもこれは\nお弁当", item=BENTO),
        s(SHOP, "smug_squint_bicolor_cat", "揚げものではない\nお弁当だ", item=BENTO),
        s(SHOP, "blank_black_cat_zoning_out", "自分に甘い", item=BENTO),
        s(SHOP, "stare_interviewer_cat", "温めますか？", item=BENTO),
        s(SHOP, "happy_hamster_open_arms", "お願いします", item=BENTO),
        s(ROOM_N, "eat_pop_cat", "ジュワッ", item=BENTO, se="pikon", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(ROOM_N, "happy_girlfriend_dance_cat", "うまい", item=BENTO),
        s(ROOM_N, "eat_crunchy_cat_luna", "からあげと白いご飯", item=BENTO),
        s(ROOM_N, "realize_wet_cat_stare", "この組み合わせを\n考えた人に\nお礼を言いたい", item=BENTO),
        s(ROOM_N, "stare_lying_tabby_cat", "端っこのサラダを\nながめる", item=BENTO),
        s(ROOM_N, "calm_black_face_sheep", "レタス2枚", item=BENTO),
        s(ROOM_N, "sad_looking_away_tabby", "これで健康は\nむりがある", item=BENTO),
        s(ROOM_N, "think_chin_paw_orange_cat", "サラダチキンは\nまだ冷蔵庫", item=CHICKEN),
        # ---- 木曜 ----
        s(STREET_N, "sleepy_sleepy_cat", "木曜日の夜11時", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(STREET_N, "blank_black_cat_zoning_out", "何も考えられない"),
        s(SHOP, "stare_lying_tabby_cat", "気づいたら\nコンビニにいた"),
        s(SHOP, "think_chin_paw_orange_cat", "選ぶ元気がない"),
        s(SHOP, "work_typing_cat", "いちばん近い棚から\n取る", item=CUP),
        s(SHOP, "calm_black_face_sheep", "カップ麺", item=CUP),
        s(ROOM_N, "work_typing_cat", "お湯をそそぐ", item=CUP, se="pi"),
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "3分待つ", item=CUP),
        s(ROOM_N, "sleepy_old_memories_cat", "その3分で\n少し寝た", item=CUP),
        s(ROOM_N, "surprise_big_pupils_cat", "5分たっていた", item=CUP, se="explosion_chudoon"),
        s(ROOM_N, "despair_dramatic_kitten", "麺がのびている", item=CUP),
        s(ROOM_N, "eat_pop_cat", "ズズッ", item=CUP, se="drink_gulp_gokugoku_thirsty_chug"),
        s(ROOM_N, "realize_wet_cat_stare", "のびても\nうまい", item=CUP),
        s(ROOM_N, "think_chin_paw_orange_cat", "スープを\n飲み干すか", item=CUP),
        s(ROOM_N, "calm_black_face_sheep", "半分で\nやめておく", item=CUP),
        s(ROOM_N, "smug_squint_bicolor_cat", "ここが\n最後の健康", item=CUP),
        s(ROOM_N, "sad_black_dog", "健康の文字は\nどこへ行った", item=CUP),
        s(ROOM_N, "think_chin_paw_orange_cat", "サラダチキンの賞味期限を\n見る", item=CHICKEN),
        s(ROOM_N, "smug_squint_bicolor_cat", "まだ大丈夫", item=CHICKEN),
        s(ROOM_N, "read_book_orange_kitten", "ルールその3\n夜11時すぎは\nコンビニに行かない"),
        s(ROOM_N, "despair_dramatic_kitten", "11時5分に\n行っていた"),
        s(ROOM_N, "sad_black_dog", "ルールは\n3つとも\nくずれかけている"),
        # ---- 金曜 ----
        s(STREET_N, "showoff_gojo_cosplay_cat", "金曜日の夜", se="gong_dora_jaan", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(STREET_N, "happy_girlfriend_dance_cat", "1週間よくがんばった"),
        s(STREET_N, "rizz_cat_rizz", "今日は\nごほうびの日だ"),
        s(SHOP, "angry_shooting_cat", "まっすぐビールの冷蔵庫へ", item=BEER, se="pikon"),
        s(SHOP, "peek_what_happen_cat", "そしてレジの横", item=BEER),
        s(SHOP, "stare_big_eyes_tabby_kitten", "月曜に見ないふりをした\nからあげ", item=BEER),
        s(SHOP, "joy_happy_happy_happy_cat", "やっと会えたな", item=BEER),
        s(SHOP, "read_book_orange_kitten", "ルールその2\nレジ横は見ない", item=BEER),
        s(SHOP, "calm_black_face_sheep", "もう\nがっつり見ている", item=BEER),
        s(SHOP, "stare_interviewer_cat", "からあげ\nおひとつですか？", item=BEER),
        s(SHOP, "angry_shooting_cat", "ふたつで", item=BEER, se="explosion_chudoon"),
        s(ROOM_N, "eat_crunchy_cat_luna", "プシュッ", item=BEER, se="drink_gulp_gokugoku_thirsty_chug", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(ROOM_N, "happy_hamster_open_arms", "ゴクッゴクッ", item=BEER),
        s(ROOM_N, "eat_pop_cat", "からあげ", item=BEER, se="pikon"),
        s(ROOM_N, "happy_girlfriend_dance_cat", "ビール", item=BEER),
        s(ROOM_N, "realize_wet_cat_stare", "これが\n1週間の答えだ", item=BEER),
        s(ROOM_N, "sleepy_sleepy_cat", "2本目もあけてしまう", item=BEER),
        s(ROOM_N, "stare_lying_tabby_cat", "夜11時", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(ROOM_N, "think_chin_paw_orange_cat", "なにか\n甘いものがほしい"),
        s(ROOM_N, "angry_aiming_cat", "コンビニは\n歩いて1分"),
        s(SHOP, "leave_cat_leaves_home", "サンダルで出かける", se="whoosh_shu"),
        s(SHOP, "eat_crunchy_cat_luna", "アイスも", item=ICE),
        s(SHOP, "smug_squint_bicolor_cat", "ついでに\nもう1個", item=ICE),
        s(ROOM_N, "happy_hamster_open_arms", "冷たくてあまい", item=ICE),
        s(ROOM_N, "sleepy_old_memories_cat", "幸せだ", item=ICE),
        s(ROOM_N, "sleep_sleeping_cat", "そのまま\nソファで寝る"),
        s(ROOM_N, "stare_lying_tabby_cat", "夢の中で\nサラダチキンが\n手をふっていた"),
        # ---- 土曜の朝 ----
        s(ROOM, "stare_tabby_wide_eyes_cat", "土曜日の朝", bgm={"file": MORNING, "gain": -12, "fade": 0.8}),
        s(ROOM, "sad_looking_away_tabby", "テーブルの上に\n空き缶とアイスのカップ"),
        s(ROOM, "work_typing_cat", "冷蔵庫をあける"),
        s(ROOM, "surprise_big_pupils_cat", "そこには", item=CHICKEN, se="pi"),
        s(ROOM, "showoff_gojo_cosplay_cat", "月曜日のサラダチキン", item=CHICKEN, se="gong_dora_jaan"),
        s(ROOM, "realize_wet_cat_stare", "ずっと\n待っていてくれた", item=CHICKEN),
        s(ROOM, "sad_banana_cat_cry", "ごめん", item=CHICKEN),
        s(ROOM, "eat_pop_cat", "朝ごはんにする", item=CHICKEN),
        s(ROOM, "happy_hamster_open_arms", "うまい", item=CHICKEN),
        s(ROOM, "think_chin_paw_orange_cat", "ふりかえる"),
        s(ROOM, "read_book_orange_kitten", "月曜は\nサラダとチキン", item=SALAD),
        s(ROOM, "read_book_orange_kitten", "火曜は\nおにぎり", item=ONIGIRI),
        s(ROOM, "read_book_orange_kitten", "水曜は\nからあげ弁当", item=BENTO),
        s(ROOM, "read_book_orange_kitten", "木曜は\nのびたカップ麺", item=CUP),
        s(ROOM, "read_book_orange_kitten", "金曜は\nビールとからあげと\nアイス", item=BEER),
        s(ROOM, "calm_black_face_sheep", "きれいな\n下り坂だ"),
        s(ROOM, "smug_squint_bicolor_cat", "でも\n月曜はちゃんと健康だった"),
        s(ROOM, "rizz_cat_rizz", "1日でも\n健康だったら\nえらい"),
        s(ROOM, "think_chin_paw_orange_cat", "そういえば"),
        s(ROOM, "read_book_orange_kitten", "ルールは3つとも\n金曜にやぶった"),
        s(ROOM, "despair_dramatic_kitten", "ルールのほうが\nきびしすぎたのかもしれない"),
        s(ROOM, "smug_squint_bicolor_cat", "来週は\nルールを1つにしよう"),
        s(ROOM, "rizz_cat_rizz", "サラダチキンを\nその日のうちに食べる"),
        s(ROOM, "happy_hamster_open_arms", "それだけでいい"),
        s(ROOM, "sad_looking_away_tabby", "体重計には\n乗らない"),
        s(ROOM, "calm_black_face_sheep", "来週の日曜まで\n乗らない"),
        s(ROOM_N, "stare_lying_tabby_cat", "日曜日の夜", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(ROOM_N, "think_chin_paw_orange_cat", "今週の\n反省をする"),
        s(ROOM_N, "angry_aiming_cat", "決めた"),
        s(ROOM_N, "showoff_gojo_cosplay_cat", "来週こそ\n健康に生きる", se="gong_dora_jaan"),
        s(ROOM_N, "blank_black_cat_zoning_out", "先週も\n同じことを言っていた"),
        s(ROOM_N, "think_chin_paw_orange_cat", "でもいい"),
        s(ROOM_N, "happy_hamster_open_arms", "コンビニは\n今週もずっと\nあいていてくれた"),
        s(ROOM_N, "rizz_cat_rizz", "それだけで\nひとり暮らしは\nなんとかなる"),
        s(ROOM_N, "excited_hodomoe_city_cat", "月曜の俺に\nまかせよう", se="pikon", dur=3.8),
        J.end_card(),
    ]


def place(cs):
    J.diversify(cs)
    J.prefer_long(cs)
    J.reflow(cs)
    J.auto_tempo(cs)
    for c in cs:
        if c.get("text"):
            c["text"] = c["text"].replace("「", "").replace("」", "")
    return cs


if __name__ == "__main__":
    cs = place(cuts())
    if os.environ.get("LEN"):
        print(len(cs), round(sum(c["dur"] for c in cs), 1))
    else:
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_24_conbini_yoru.mp4"), os.path.join(J.HERE, "out", "jidaraku_24_conbini_yoru_preview"))
