"""自堕落シリーズ #27：30代独身、平日休みに1人でドトールのモーニング（11/23 ユーザー指定）。約5分。ドンキ・焼肉ライクと同じ作り。

python3 catmeme/jidaraku_27_doutor.py → out/jidaraku_27_doutor.mp4
- 11/23 ユーザー指定：「安く行ける」ことを前面に。地域限定は調べたが見つからず、「店舗限定のモーニングがある」に留める
- 調べた内容（11/23）：モーニングは開店〜10:30（土日祝も・一部店舗は違う）・セットA 480円〜・セットB 520円〜・
  ホットモーニング 540円〜・ドリンクとセットで合計から50円引き。値段や時間は店で違うので「500円前後」「店によって違う」と言う
- 流れ：平日休みの朝 → 500円で朝ごはん → 10:30 に間に合うか → レジ（ワンコイン前後・50円引き）→ ホットサンド → コーヒー →
  窓の外の通勤の人 → 店舗限定もあるらしい → 休日の朝を500円で買えた
- 写真はユーザー提供（11/23）backgrounds/jidaraku/27_doutor
- 11/17 からのルール：場面転換ゆっくり・字幕は1行12字・最大2行・2.5〜3秒・職場の回想なし
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "27_doutor"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku")]
ROOM_N, STREET_N = "j07_room_night", "bg51_night_street"
FRONT, INSIDE, WINDOW = "dt01_front", "dt02_inside", "dt03_window"
MORNING, COFFEE = "f_morning", "f_coffee"
ROOM_D = "j01_room"
STREET_D = "bg48_clean_street"   # 朝の道（夜の道は使わない）
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


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 平日休みの朝 ----
        s(ROOM_D, "sleepy_sleepy_cat", "平日の朝7時", bgm={"file": LOFI, "gain": -12}),
        s(ROOM_D, "stare_lying_tabby_cat", "今日は\n平日休み"),
        s(ROOM_D, "think_chin_paw_orange_cat", "みんなが\n会社に行く時間"),
        s(ROOM_D, "smug_squint_bicolor_cat", "自分だけ\n休み"),
        s(ROOM_D, "happy_hamster_open_arms", "この感じが\nたまらない"),
        s(ROOM_D, "money_counting_orange_cat", "でも\n給料日前で\nお金はない"),
        s(ROOM_D, "think_chin_paw_orange_cat", "500円で\nちゃんとした\n朝ごはん"),
        s(ROOM_D, "angry_aiming_cat", "あそこだ"),
        s(ROOM_D, "sleepy_old_memories_cat", "いつもの休日は\n昼まで寝てしまう"),
        s(ROOM_D, "sad_looking_away_tabby", "起きたら\n夕方のこともある"),
        s(ROOM_D, "angry_shooting_cat", "今日は\nちゃんと\n朝から動く"),
        s(ROOM_D, "work_typing_cat", "顔を洗って\n着替える"),
        s(STREET_D, "walk_approaching_orange_cat", "上着をはおって\n朝の道を歩く"),
        s(STREET_D, "stare_tabby_wide_eyes_cat", "黄色い看板が\n見えてきた", se="pi"),
        s(FRONT, "showoff_gojo_cosplay_cat", "ドトール", se="gong_dora_jaan"),
        s(FRONT, "read_book_orange_kitten", "モーニングは\n10時30分まで"),
        s(FRONT, "surprise_big_pupils_cat", "今は\n9時すぎ"),
        s(FRONT, "happy_hamster_open_arms", "間に合った"),
        s(FRONT, "rizz_cat_rizz", "平日休みの\n特権だ"),
        # ---- 注文 ----
        s(INSIDE, "work_typing_cat", "店内に入る", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(INSIDE, "peek_what_happen_cat", "朝のドトールは\n静か"),
        s(INSIDE, "think_chin_paw_orange_cat", "スーツの人が\n急いで\nコーヒーを買っていく"),
        s(INSIDE, "smug_squint_bicolor_cat", "こちらは\n急がない"),
        s(INSIDE, "read_book_orange_kitten", "レジの横に\nモーニングの\nメニュー"),
        s(INSIDE, "stare_big_eyes_tabby_kitten", "写真が\nどれもおいしそう"),
        s(INSIDE, "read_book_orange_kitten", "モーニングは\nパンと\nドリンクのセット"),
        s(INSIDE, "money_counting_orange_cat", "値段は\n500円前後"),
        s(INSIDE, "surprise_big_pupils_cat", "ほぼ\nワンコイン", se="shine_kiraan_maou"),
        s(INSIDE, "read_book_orange_kitten", "ドリンクと\nセットにすると\n50円引き"),
        s(INSIDE, "joy_happy_happy_happy_cat", "ありがたい"),
        s(INSIDE, "think_chin_paw_orange_cat", "メニューで\n少し迷う"),
        s(INSIDE, "angry_shooting_cat", "あたたかい\nサンドに\nしよう", se="pikon"),
        s(INSIDE, "happy_hamster_open_arms", "ブレンドを\n添えて"),
        s(INSIDE, "money_counting_orange_cat", "お会計"),
        s(INSIDE, "surprise_big_pupils_cat", "財布が\nほとんど\n減っていない", se="price_display"),
        # ---- 実食 ----
        s(WINDOW, "work_typing_cat", "窓ぎわの席に座る", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(WINDOW, "stare_tabby_wide_eyes_cat", "朝の光が\nまぶしい"),
        s(WINDOW, "surprise_big_pupils_cat", "来た", item=MORNING, se="shine_kiraan_maou"),
        s(WINDOW, "stare_big_eyes_tabby_kitten", "こんがり\nトースト", item=MORNING),
        s(WINDOW, "happy_girlfriend_dance_cat", "ゆでたまごと\nベーコンと\nチーズ", item=MORNING),
        s(WINDOW, "think_chin_paw_orange_cat", "これで\n500円前後？", item=MORNING),
        s(WINDOW, "eat_pop_cat", "ひと口", item=MORNING, se="eat_paku"),
        s(WINDOW, "realize_wet_cat_stare", "…あったかい", item=MORNING),
        s(WINDOW, "eat_crunchy_cat_luna", "外はサクサク\n中はとろっと", item=MORNING),
        s(WINDOW, "rizz_cat_rizz", "朝からこれは\n反則だ", item=MORNING),
        s(WINDOW, "happy_hamster_open_arms", "コーヒーを\nひと口", item=COFFEE),
        s(WINDOW, "calm_black_face_sheep", "ほっとする", item=COFFEE),
        s(WINDOW, "smug_squint_bicolor_cat", "パンと\nコーヒーの\n往復", item=MORNING),
        s(WINDOW, "eat_pop_cat", "これが\nいちばん\nおいしい食べ方", item=COFFEE),
        s(WINDOW, "eat_crunchy_cat_luna", "たまごが\nほくほく", item=MORNING),
        s(WINDOW, "think_chin_paw_orange_cat", "ベーコンの\n塩気がいい", item=MORNING),
        s(WINDOW, "smug_squint_bicolor_cat", "黒こしょうが\nきいている", item=MORNING),
        s(WINDOW, "happy_girlfriend_dance_cat", "最後のひと口まで\nあたたかい", item=MORNING),
        s(WINDOW, "realize_wet_cat_stare", "…ごちそうさま", item=MORNING),
        # ---- 窓の外 ----
        s(WINDOW, "peek_what_happen_cat", "窓の外を見る", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(WINDOW, "stare_tabby_wide_eyes_cat", "駅へ急ぐ人たち"),
        s(WINDOW, "sad_looking_away_tabby", "いつもは\nあっち側"),
        s(WINDOW, "think_chin_paw_orange_cat", "ちょっとだけ\n申し訳ない"),
        s(WINDOW, "smug_squint_bicolor_cat", "でも\nちょっとだけ\nうれしい"),
        s(WINDOW, "rizz_cat_rizz", "今日だけは\nゆっくりしていい", item=COFFEE),
        s(WINDOW, "read_book_orange_kitten", "スマホで\nモーニングを\n調べてみる"),
        s(WINDOW, "surprise_big_pupils_cat", "店舗限定の\nモーニングも\nあるらしい"),
        s(WINDOW, "think_chin_paw_orange_cat", "置いている店は\n限られている"),
        s(WINDOW, "angry_aiming_cat", "次の平日休みは\nそれを探しに行く"),
        s(WINDOW, "happy_hamster_open_arms", "500円前後の\n小さな冒険だ"),
        s(WINDOW, "calm_black_face_sheep", "コーヒーが\nなくなった", item=COFFEE),
        s(WINDOW, "stare_lying_tabby_cat", "もう少し\nだけ座っていよう"),
        s(WINDOW, "read_book_orange_kitten", "家から\n本を持ってきた"),
        s(WINDOW, "calm_black_face_sheep", "ページを\nめくる音だけ"),
        s(WINDOW, "sleepy_sleepy_cat", "少し\nうとうと"),
        s(WINDOW, "stare_tabby_wide_eyes_cat", "気づけば\nお店も\n少し混んできた"),
        s(WINDOW, "smug_squint_bicolor_cat", "そろそろ\n席をゆずろう"),
        # ---- 帰り道と家 ----
        s(FRONT, "walk_approaching_orange_cat", "お店を出る", bgm={"file": JITAKU, "gain": -10, "fade": 1.0}),
        s(STREET_D, "smug_squint_bicolor_cat", "朝の空気が\n気持ちいい"),
        s(STREET_D, "money_counting_orange_cat", "使ったのは\n500円前後"),
        s(STREET_D, "think_chin_paw_orange_cat", "それなのに\nこの満足感"),
        s(STREET_D, "happy_hamster_open_arms", "まだ\n朝10時"),
        s(STREET_D, "rizz_cat_rizz", "一日が\nまるごと残っている"),
        s(STREET_D, "walk_white_duck", "少し\n遠回りして帰る"),
        s(STREET_D, "peek_what_happen_cat", "平日の昼前の街は\n人が少ない"),
        s(STREET_D, "happy_hamster_open_arms", "公園のベンチで\nひなたぼっこ"),
        s(STREET_D, "calm_black_face_sheep", "誰にも\n急かされない"),
        s(ROOM_D, "dance_tabby_standing_cat", "家に帰って\nのんびり"),
        s(ROOM_D, "sleepy_sleepy_cat", "お腹がいっぱいで\n少し眠い"),
        s(ROOM_D, "sleep_sleeping_cat", "二度寝"),
        s(ROOM_D, "stare_lying_tabby_cat", "起きたら\nお昼"),
        s(ROOM_D, "happy_hamster_open_arms", "それでもいい\n平日休みだから"),
        s(ROOM_D, "think_chin_paw_orange_cat", "休日の朝を\n500円で買えた"),
        s(ROOM_D, "excited_hodomoe_city_cat", "次の平日休みも\nドトールで", se="pikon", dur=3.8),
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_27_doutor.mp4"), os.path.join(J.HERE, "out", "jidaraku_27_doutor_preview"))
