"""自堕落シリーズ #23：30代独身男、ひとりで吉野家の牛すき鍋膳（11/18 ユーザー指定）。5〜6分でよい。

python3 catmeme/jidaraku_23_yoshinoya.py → out/jidaraku_23_yoshinoya.mp4
- 流れ（ユーザー指定）：吉野家にひとりで行き、牛すき鍋膳をたのむ → このメニューの歴史を語る →
  「ご飯のおかわりは無料なのか？」が毎年まぎらわしい
- 歴史（吉野家の発表・ニュースより）：2013年12月に登場 → 2014年に熟成肉でパワーアップして再登場 → 毎年冬の定番 →
  2023年11月に累計1億食 → 2026年で14年目・累計1億2000万食。11/10〜11/24 は「牛すき祭」で100円引き
- ご飯のおかわり：11/18 調べた範囲（2026年版の記事・吉野家の発表）では、店内なら増量・おかわり無料（テイクアウトは増量のみ・
  一部対象外の店あり）。ユーザーは「できない」と書いていたので、どちらで落とすかユーザーに確認中（台本は「できる」で仮）
- 11/17 からのルール：場面転換ゆっくり（TEMPO_K 1.3・HOLD 6・prefer_long）・字幕は1行12字・最大2行・2.5〜3秒・職場の回想なし
- 写真は backgrounds/jidaraku/23_yoshinoya に置く。届くまでは手もちのイラストで仮に（ほかの店の写真は使わない）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "23_yoshinoya"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku")]
ROOM_N, STREET_N = "j07_room_night", "bg51_night_street"
FRONT, SEAT = "yo01_front", "yo02_seat"
J.STANDIN.update({FRONT: "bg51_night_street", SEAT: "bg20_counter"})
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
NABE, RICE, EGG, POSTER = "f_nabe", "f_rice", "f_egg", "f_poster"


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 寒い夜 ----
        s(STREET_N, "stare_lying_tabby_cat", "11月の夜", bgm={"file": LOFI, "gain": -12}),
        s(STREET_N, "sad_looking_away_tabby", "急に寒くなった"),
        s(STREET_N, "think_chin_paw_orange_cat", "こんな夜は\nあったかい鍋が食べたい"),
        s(STREET_N, "calm_black_face_sheep", "でも\nひとり鍋は\n白菜が余る"),
        s(STREET_N, "stare_tabby_wide_eyes_cat", "そこに見えてきた\nオレンジの看板", se="pi"),
        s(FRONT, "showoff_gojo_cosplay_cat", "吉野家だ", se="gong_dora_jaan"),
        s(FRONT, "surprise_big_pupils_cat", "入り口に\nあのポスター", item=POSTER, se="shine_kiraan_maou"),
        s(FRONT, "happy_hamster_open_arms", "牛すき鍋膳", item=POSTER),
        s(FRONT, "realize_wet_cat_stare", "今年も\nこの季節が来たか", item=POSTER),
        s(FRONT, "rizz_cat_rizz", "吉野家の\n冬の風物詩だ", item=POSTER),
        # ---- 注文 ----
        s(SEAT, "work_typing_cat", "カウンターに座る", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(SEAT, "peek_what_happen_cat", "まわりも\nひとり客ばかり"),
        s(SEAT, "happy_hamster_open_arms", "吉野家は\nひとり客の味方だ"),
        s(SEAT, "angry_shooting_cat", "牛すき鍋膳を\nください", se="pikon"),
        s(SEAT, "stare_interviewer_cat", "牛すき鍋膳ですね"),
        s(SEAT, "smug_squint_bicolor_cat", "迷いはない"),
        # ---- 歴史 ----
        s(SEAT, "think_chin_paw_orange_cat", "待っているあいだに\n少し語らせてほしい", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(SEAT, "read_book_orange_kitten", "牛すき鍋膳が\n登場したのは\n2013年の冬"),
        s(SEAT, "stare_big_eyes_tabby_kitten", "牛丼の店で\n鍋が出てくる"),
        s(SEAT, "surprise_big_pupils_cat", "当時は\nけっこうな\n事件だった"),
        s(SEAT, "read_book_orange_kitten", "次の年には\n熟成肉を使って\nパワーアップして\n再登場"),
        s(SEAT, "happy_girlfriend_dance_cat", "そこから\n毎年冬になると\n帰ってくる"),
        s(SEAT, "rizz_cat_rizz", "冬の定番に\nなった"),
        s(SEAT, "money_counting_orange_cat", "2023年には\n累計1億食を突破"),
        s(SEAT, "scream_standing_marmot", "1億食", se="explosion_chudoon"),
        s(SEAT, "think_chin_paw_orange_cat", "日本人ひとりあたり\nほぼ1食"),
        s(SEAT, "read_book_orange_kitten", "そして今年で\n14年目"),
        s(SEAT, "stare_tabby_wide_eyes_cat", "累計は\n1億2000万食"),
        s(SEAT, "sleepy_old_memories_cat", "14年といえば\n俺が\n若手社員だったころ"),
        s(SEAT, "calm_black_face_sheep", "今は30代独身"),
        s(SEAT, "rizz_cat_rizz", "牛すき鍋膳だけが\n毎年かわらず\nそばにいる"),
        s(SEAT, "read_book_orange_kitten", "ちなみに今は\n牛すき祭で\n100円引き"),
        s(SEAT, "joy_happy_happy_happy_cat", "ありがたい"),
        # ---- 到着・実食 ----
        s(SEAT, "stare_interviewer_cat", "お待たせしました", item=NABE, se="pi", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(SEAT, "surprise_big_pupils_cat", "ぐつぐつ", item=NABE, se="shine_kiraan_maou"),
        s(SEAT, "happy_hamster_open_arms", "牛肉\nねぎ\n白菜\n豆腐", item=NABE),
        s(SEAT, "stare_big_eyes_tabby_kitten", "そして\n生たまご", item=EGG),
        s(SEAT, "work_typing_cat", "たまごを\nよくといて", item=EGG),
        s(SEAT, "eat_pop_cat", "牛肉を\nくぐらせる", item=NABE, se="pikon"),
        s(SEAT, "happy_girlfriend_dance_cat", "うまい", item=NABE),
        s(SEAT, "eat_crunchy_cat_luna", "甘いわりしたが\nしみている", item=NABE),
        s(SEAT, "realize_wet_cat_stare", "体のしんから\nあったまる", item=NABE),
        s(SEAT, "eat_pop_cat", "そして\nご飯", item=RICE),
        s(SEAT, "rizz_cat_rizz", "すき焼きと白いご飯", item=RICE),
        s(SEAT, "joy_happy_happy_happy_cat", "反則の組み合わせ", item=RICE),
        s(SEAT, "stare_tabby_wide_eyes_cat", "ご飯が\nみるみる減っていく", item=RICE),
        # ---- おかわり問題 ----
        s(SEAT, "stare_lying_tabby_cat", "そして\n毎年ここで\n悩む", item=RICE, bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(SEAT, "think_chin_paw_orange_cat", "このご飯\nおかわりできるのか？", item=RICE),
        s(SEAT, "read_book_orange_kitten", "吉野家の定食は\nご飯のおかわりが\n無料", item=RICE),
        s(SEAT, "huh_huh_cat", "でも\n牛すき鍋膳は\n定食なのか？", item=RICE, se="question_mark_pop_confused_huh"),
        s(SEAT, "confused_i_dont_know_cat", "名前は\n鍋膳", item=RICE),
        s(SEAT, "despair_dramatic_kitten", "毎年\nまぎらわしい", item=RICE),
        s(SEAT, "sad_looking_away_tabby", "去年の俺も\n悩んでいた", item=RICE),
        s(SEAT, "sleepy_old_memories_cat", "おととしの俺も\n悩んでいた", item=RICE),
        s(SEAT, "calm_black_face_sheep", "毎年調べて\n毎年忘れる", item=RICE),
        s(SEAT, "angry_aiming_cat", "今年こそ\nはっきりさせる", item=RICE),
        s(SEAT, "stare_interviewer_cat", "店内でしたら\nおかわり無料です", item=RICE, se="pi"),
        s(SEAT, "showoff_gojo_cosplay_cat", "できる", item=RICE, se="gong_dora_jaan"),
        s(SEAT, "read_book_orange_kitten", "持ち帰りは\n増量だけで\nおかわりはなし", item=RICE),
        s(SEAT, "read_book_orange_kitten", "※一部\n対象外のお店も\nあるらしい", item=RICE),
        s(SEAT, "happy_girlfriend_dance_cat", "おかわり\nください", item=RICE, se="pikon"),
        s(SEAT, "eat_crunchy_cat_luna", "2杯目も\nすき焼きと", item=RICE),
        s(SEAT, "sleepy_sleepy_cat", "しあわせな満腹", item=NABE),
        s(SEAT, "rizz_cat_rizz", "今年の答えは\nメモしておく", item=NABE),
        # ---- 帰り道 ----
        s(STREET_N, "leave_cat_leaves_home", "店を出る", se="whoosh_shu", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(STREET_N, "happy_hamster_open_arms", "外は寒いのに\n体はぽかぽか"),
        s(STREET_N, "think_chin_paw_orange_cat", "鍋は\nひとりで食べても\nあったかい"),
        s(STREET_N, "sleepy_old_memories_cat", "来年の冬も\nきっと来る"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nベッドに倒れこむ", se="whoosh_shu"),
        s(ROOM_N, "scream_phone_orange_cat", "スマホのメモを\n見返す"),
        s(ROOM_N, "read_book_orange_kitten", "去年のメモにも\n同じことが\n書いてあった"),
        s(ROOM_N, "blank_black_cat_zoning_out", "……"),
        s(ROOM_N, "excited_hodomoe_city_cat", "来年の俺も\nたぶん悩む", se="pikon", dur=3.8),
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_23_yoshinoya.mp4"), os.path.join(J.HERE, "out", "jidaraku_23_yoshinoya_preview"))
