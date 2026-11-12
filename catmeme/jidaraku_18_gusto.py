"""自堕落シリーズ #18：30代独身男、ひとりでガスト飲み（11/12 ユーザー指定：ユーザーの流れ＋口コミを参考に）。8-10分。

python3 catmeme/jidaraku_18_gusto.py → out/jidaraku_18_gusto.mp4
- 流れ（ユーザー指定）：サイゼのひとり飲みは有名 → だがガストも負けていない → 甘くないレモンサワー・ウーロンハイが200円ちょっと →
  18時前に入ってハッピーアワーのビール → その後ほかのドリンク（クレバーな自分に酔う）→ おつまみ（ほうれん草ベーコン・野菜グリル・
  手羽中・ハムとモッツァレラ）→ 小エビのサラダも捨てがたい → ボトルワイン1000円以下・無敵感 → から好しの唐揚げ（胡麻にんにくダレ）→
  ミラノ風ドリアが恋しくなる → サイゼもガストもバーミヤンも捨てがたい → 18時前から飲んでいるから夜は長い
- 口コミより：平日の夕方は空いていてひとりでも入りやすい／ハッピーアワーは平日の18時まで（店舗・時期で変わる）／
  注文はタブレット／ネコ型の配膳ロボットが運んでくる
- 値段は「ちょっと」「くらい」でぼかす。「店舗や時期で変わります」を1回出す。ほかの店をけなさない
- 写真は backgrounds/jidaraku/18_gusto（ユーザー提供の料理5枚）。お店の外観・店内は手もちのイラストで仮に（ほかの店の写真は使わない）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "18_gusto"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku")]
OFFICE, STREET, FRONT, SEAT, ROOM_N = ("bg25_office_desk", "bg51_night_street", "gs01_front", "gs02_seat", "j07_room_night")
J.STANDIN.update({SEAT: "bg28_ny_diner"})   # 外観 gs01_front・ワイン f_wine はユーザー提供（11/12）
J.HOLD = 4
J.LOOPS = 1
J.SUB_STYLE = "glow"
MORNING = os.path.join(L.BGM, "Morning.mp3")
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
BEER, HORENSO, GRILL, TEBA, HAM, KARA, WINE = "f_beer", "f_horenso", "f_grill", "f_tebanaka", "f_ham", "f_karaage", "f_wine"


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 会社 ----
        s(OFFICE, "work_typing_cat", "平日の午後5時", bgm={"file": LOFI, "gain": -12}),
        s(OFFICE, "stare_tabby_wide_eyes_cat", "今日は\n定時で帰る"),
        s(OFFICE, "think_chin_paw_orange_cat", "なぜなら\n行く場所が\n決まっているからだ"),
        s(OFFICE, "smug_squint_bicolor_cat", "ひとり飲みの\n聖地といえば"),
        s(OFFICE, "excited_hodomoe_city_cat", "サイゼリヤ", se="pi"),
        s(OFFICE, "money_counting_orange_cat", "デカンタワインが\nとにかく安い"),
        s(OFFICE, "happy_hamster_open_arms", "それは\nみんな知っている"),
        s(OFFICE, "rizz_cat_rizz", "だが\n俺は知っている"),
        s(OFFICE, "angry_aiming_cat", "ガストも\n負けず劣らず\nオトクだということを", se="shine_kiraan_maou"),
        s(OFFICE, "stare_interviewer_cat", "ちょっといいかな", se="pi"),
        s(OFFICE, "surprise_big_pupils_cat", "上司だ"),
        s(OFFICE, "stare_interviewer_cat", "あした\n時間ある？"),
        s(OFFICE, "calmdown_dancing_cat", "あしたなら\nいくらでも"),
        s(OFFICE, "leave_cat_leaves_home", "お先に\n失礼します", se="whoosh_shu"),
        # ---- 18時前に入る ----
        s(STREET, "drive_driving_cat", "時計を見る\n5時45分", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(STREET, "read_book_orange_kitten", "ガストには\nハッピーアワーがある"),
        s(STREET, "think_chin_paw_orange_cat", "平日の18時前は\nビールが安くなる"),
        s(STREET, "calm_black_face_sheep", "※時間や値段は\n店舗や時期で\n変わります"),
        s(STREET, "angry_aiming_cat", "つまり\n勝負は\n18時前"),
        s(STREET, "scream_standing_marmot", "急げ", se="explosion_chudoon"),
        s(FRONT, "surprise_big_pupils_cat", "赤い看板が\n見えてきた"),
        s(FRONT, "happy_hamster_open_arms", "いつ見ても\n安心する赤だ"),
        s(FRONT, "sleepy_old_memories_cat", "子どものころは\n家族で来た店"),
        s(FRONT, "rizz_cat_rizz", "今は\nひとりで\n飲みに来る店"),
        s(FRONT, "showoff_gojo_cosplay_cat", "5時52分\n入店", se="gong_dora_jaan"),
        s(FRONT, "stare_interviewer_cat", "何名様ですか？"),
        s(FRONT, "smug_squint_bicolor_cat", "1名です\n（キリッ）"),
        s(SEAT, "happy_hamster_open_arms", "平日の夕方は\n空いている", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(SEAT, "peek_what_happen_cat", "となりは\n勉強中の学生"),
        s(SEAT, "peek_what_happen_cat", "その向こうは\nパソコンを開いた\nサラリーマン"),
        s(SEAT, "sleepy_old_memories_cat", "誰も\nこっちを見ていない"),
        s(SEAT, "rizz_cat_rizz", "ひとり客に\nやさしい世界"),
        s(SEAT, "sleepy_old_memories_cat", "思い出すのは\n先月の\n会社の飲み会"),
        s(OFFICE, "stare_interviewer_cat", "とりあえず\n全員ビールで\nいいよね？", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(OFFICE, "sad_looking_away_tabby", "レモンサワーが\n飲みたかった"),
        s(OFFICE, "work_typing_cat", "上司のグラスが\n空かないか\nずっと見張る"),
        s(OFFICE, "stare_interviewer_cat", "君の話\nもっと聞かせてよ"),
        s(OFFICE, "blank_black_cat_zoning_out", "と言いながら\n2時間\n上司の昔話"),
        s(OFFICE, "talk_orange_white_sitting_cat", "すみませーん\n会費5000円\n集めてまーす"),
        s(OFFICE, "despair_dramatic_kitten", "唐揚げ\n2個しか\n食べてない"),
        s(OFFICE, "calm_black_face_sheep", "1個2500円の\n唐揚げだった"),
        s(SEAT, "happy_hamster_open_arms", "今日は\n好きなものを\n好きなだけ", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(SEAT, "joy_happy_happy_happy_cat", "誰の\nグラスも\n見張らなくていい"),
        s(SEAT, "work_typing_cat", "注文は\nタブレット"),
        s(SEAT, "stare_tabby_wide_eyes_cat", "店員さんを\n呼ばなくていい"),
        s(SEAT, "joy_happy_happy_happy_cat", "誰とも\n話さずに\n飲みが始められる"),
        s(SEAT, "angry_shooting_cat", "まずは\nハッピーアワーの\nビール", item=BEER, se="pikon"),
        s(SEAT, "stare_big_eyes_tabby_kitten", "5時54分\n注文完了", item=BEER),
        s(SEAT, "smug_squint_bicolor_cat", "間に合った", item=BEER),
        # ---- ネコ型ロボット ----
        s(SEAT, "surprise_big_pupils_cat", "向こうから\n何か来る", se="pi"),
        s(SEAT, "stare_lying_tabby_cat", "ネコの顔をした\n配膳ロボットだ"),
        s(SEAT, "happy_girlfriend_dance_cat", "ビールを\n運んできてくれた", item=BEER),
        s(SEAT, "realize_wet_cat_stare", "ロボットにまで\nやさしくされる", item=BEER),
        s(SEAT, "eat_crunchy_cat_luna", "ゴクッ\nゴクッ", item=BEER, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "happy_hamster_open_arms", "うまい", item=BEER),
        s(SEAT, "sleepy_sleepy_cat", "定時で帰って\n明るいうちに飲む\nビール", item=BEER),
        s(SEAT, "rizz_cat_rizz", "これを\n幸せと呼ぶ", item=BEER),
        # ---- 18時以降の作戦 ----
        s(SEAT, "stare_tabby_wide_eyes_cat", "18時になった", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(SEAT, "think_chin_paw_orange_cat", "ここからは\n作戦を変える"),
        s(SEAT, "read_book_orange_kitten", "甘くない\nレモンサワー"),
        s(SEAT, "read_book_orange_kitten", "ウーロンハイ"),
        s(SEAT, "money_counting_orange_cat", "どちらも\n200円ちょっと"),
        s(SEAT, "surprise_big_pupils_cat", "安すぎる", se="explosion_chudoon"),
        s(SEAT, "smug_squint_bicolor_cat", "18時前は\nハッピーアワーで\nビール"),
        s(SEAT, "smug_squint_bicolor_cat", "18時からは\n安いサワーで攻める"),
        s(SEAT, "rizz_cat_rizz", "このクレバーな\n立ち回り"),
        s(SEAT, "happy_girlfriend_dance_cat", "酒より先に\n自分に酔える"),
        s(SEAT, "eat_crunchy_cat_luna", "甘くないレモンサワー\nゴクッ", se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "happy_hamster_open_arms", "本当に\n甘くない"),
        s(SEAT, "calm_black_face_sheep", "おつまみに\n合う味だ"),
        s(SEAT, "think_chin_paw_orange_cat", "さらに\nドリンクバーも\n頼んでおく"),
        s(SEAT, "smug_squint_bicolor_cat", "お酒の合間に\nお茶や炭酸水"),
        s(SEAT, "read_book_orange_kitten", "チェイサーが\n飲み放題"),
        s(SEAT, "rizz_cat_rizz", "これで\n明日に残らない"),
        s(SEAT, "sleepy_old_memories_cat", "……はずだ"),
        s(SEAT, "eat_crunchy_cat_luna", "ホットの\n烏龍茶をはさむ", se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "happy_hamster_open_arms", "胃が\nととのう"),
        # ---- おつまみ ----
        s(SEAT, "think_chin_paw_orange_cat", "そして\nガストの強みは\nおつまみの多さ"),
        s(SEAT, "angry_aiming_cat", "まずは\nほうれん草と\nベーコン", item=HORENSO, se="pikon"),
        s(SEAT, "surprise_big_pupils_cat", "鉄板の上で\nバターがとけていく", item=HORENSO),
        s(SEAT, "eat_pop_cat", "シャキッ", item=HORENSO),
        s(SEAT, "happy_girlfriend_dance_cat", "うまい", item=HORENSO),
        s(SEAT, "think_chin_paw_orange_cat", "サイゼにも\nほうれん草はある", item=HORENSO),
        s(SEAT, "smug_squint_bicolor_cat", "でも\nこれは\nガストのほうが好きだ", item=HORENSO),
        s(SEAT, "rizz_cat_rizz", "異論は\n認める", item=HORENSO),
        s(SEAT, "angry_aiming_cat", "つぎは\n野菜のグリル", item=GRILL),
        s(SEAT, "surprise_big_pupils_cat", "ヤングコーン\nブロッコリー\nトマトにきのこ", item=GRILL),
        s(SEAT, "eat_crunchy_cat_luna", "アツッ", item=GRILL, se="pi"),
        s(SEAT, "happy_hamster_open_arms", "野菜の甘みが\nすごい", item=GRILL),
        s(SEAT, "money_counting_orange_cat", "これは\nサイゼにはない\n一品", item=GRILL),
        s(SEAT, "showoff_gojo_cosplay_cat", "野菜は\nガストに\n軍配があがる", item=GRILL, se="gong_dora_jaan"),
        s(SEAT, "sleepy_old_memories_cat", "……と\n言いたいが", item=GRILL),
        s(SEAT, "realize_wet_cat_stare", "サイゼの\n小エビのサラダも\nうまいんだよなあ", item=GRILL),
        s(SEAT, "confused_i_dont_know_cat", "甲乙つけがたい", item=GRILL),
        s(SEAT, "angry_aiming_cat", "手羽中の唐揚げ", item=TEBA),
        s(SEAT, "eat_pop_cat", "カリッ", item=TEBA, se="pikon"),
        s(SEAT, "happy_girlfriend_dance_cat", "甘辛いタレが\nたまらない", item=TEBA),
        s(SEAT, "eat_crunchy_cat_luna", "タレの濃さが\nおつまみに\nちょうどいい", item=TEBA),
        s(SEAT, "work_typing_cat", "骨のまわりまで\nしゃぶる", item=TEBA),
        s(SEAT, "sad_looking_away_tabby", "ひとりだから\n誰にも\n見られていない", item=TEBA),
        s(SEAT, "angry_aiming_cat", "口なおしに\nハムとモッツァレラ", item=HAM),
        s(SEAT, "stare_big_eyes_tabby_kitten", "トマトに\nレモンまで\nついている", item=HAM),
        s(SEAT, "rizz_cat_rizz", "急に\nおしゃれな店に\n来た気分", item=HAM),
        s(SEAT, "smug_squint_bicolor_cat", "ファミレスで\nイタリアンバル", item=HAM),
        s(SEAT, "joy_happy_happy_happy_cat", "テーブルが\nにぎやかになってきた", item=HAM),
        # ---- ボトルワイン ----
        s(SEAT, "stare_tabby_wide_eyes_cat", "おっと", se="pi"),
        s(SEAT, "despair_dramatic_kitten", "サワーが\nもうない"),
        s(SEAT, "think_chin_paw_orange_cat", "格安ワインは\nサイゼだけのものだと\n思ったか"),
        s(SEAT, "smug_squint_bicolor_cat", "ガストにもある"),
        s(SEAT, "money_counting_orange_cat", "ボトルで\n1000円しない\nワインが", se="shine_kiraan_maou", item=WINE),
        s(SEAT, "angry_shooting_cat", "注文", se="pikon"),
        s(SEAT, "stare_lying_tabby_cat", "ネコのロボットが\nボトルを運んでくる", item=WINE),
        s(SEAT, "surprise_big_pupils_cat", "ドンッ", se="explosion_dokaan", item=WINE),
        s(SEAT, "happy_girlfriend_dance_cat", "ボトルが\n自分のテーブルに\n置かれたときの\nこの高揚感", item=WINE),
        s(SEAT, "showoff_gojo_cosplay_cat", "無敵感", se="gong_dora_jaan", item=WINE),
        s(SEAT, "rizz_cat_rizz", "ひとりなのに\n1本まるごと\n俺のもの", item=WINE),
        s(SEAT, "stare_big_eyes_tabby_kitten", "イタリアの\n赤ワイン", item=WINE),
        s(SEAT, "read_book_orange_kitten", "ラベルには\nぶどうと\n古いおうちの絵", item=WINE),
        s(SEAT, "smug_squint_bicolor_cat", "気分は\nイタリアの田舎", item=WINE),
        s(SEAT, "calm_black_face_sheep", "実際は\n国道ぞいの\nファミレス", item=WINE),
        s(SEAT, "eat_crunchy_cat_luna", "トクトクトク", se="drink_gulp_gokugoku_thirsty_chug", item=WINE),
        s(SEAT, "happy_hamster_open_arms", "今宵も\nこのテーブルの上は"),
        s(SEAT, "happy_chipi_chapa_cat", "お祭り騒ぎだ"),
        s(SEAT, "eat_crunchy_cat_luna", "ひとくち", se="drink_gulp_gokugoku_thirsty_chug", item=WINE),
        s(SEAT, "surprise_big_pupils_cat", "ちゃんと\nワインの味がする", item=WINE),
        s(SEAT, "think_chin_paw_orange_cat", "高いワインとの\n違いは", item=WINE),
        s(SEAT, "confused_i_dont_know_cat", "正直\nわからない", item=WINE),
        s(SEAT, "smug_squint_bicolor_cat", "わからない舌で\nよかった", item=WINE),
        s(SEAT, "rizz_cat_rizz", "安く幸せになれる\n才能だ", item=WINE),
        # ---- から好しの唐揚げ ----
        s(SEAT, "stare_tabby_wide_eyes_cat", "そして", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(SEAT, "surprise_big_pupils_cat", "……きた", se="pi"),
        s(SEAT, "rizz_cat_rizz", "これが\nガスト飲みの価値を\n1ランク上げている", item=KARA),
        s(SEAT, "showoff_gojo_cosplay_cat", "から好しの\n唐揚げだ", item=KARA, se="gong_dora_jaan"),
        s(SEAT, "read_book_orange_kitten", "メニューには\n大きく\n金賞の文字", item=KARA),
        s(SEAT, "calm_black_face_sheep", "だが\n賞なんて\nどうでもいい", item=KARA),
        s(SEAT, "smug_squint_bicolor_cat", "食べれば\nわかる", item=KARA),
        s(SEAT, "eat_pop_cat", "ジュワッ", item=KARA, se="pikon"),
        s(SEAT, "surprise_big_pupils_cat", "やわらかい", item=KARA),
        s(SEAT, "happy_girlfriend_dance_cat", "うまくないわけが\nない", item=KARA),
        s(SEAT, "think_chin_paw_orange_cat", "今日は\n胡麻にんにくダレ", item=KARA),
        s(SEAT, "read_book_orange_kitten", "いつもこれか\nハニーマスタード", item=KARA),
        s(SEAT, "eat_crunchy_cat_luna", "この濃い味に\nこのやわらかさ", item=KARA),
        s(SEAT, "angry_aiming_cat", "反則だ", item=KARA, se="explosion_chudoon"),
        s(SEAT, "rizz_cat_rizz", "ペナルティとして\nグラスのワインを\n飲み干す", item=KARA),
        s(SEAT, "eat_crunchy_cat_luna", "ゴクッ", item=KARA, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "joy_happy_happy_happy_cat", "反則がつづく", item=KARA),
        s(SEAT, "eat_pop_cat", "もう1個", item=KARA),
        s(SEAT, "rizz_cat_rizz", "ペナルティ\nもう1杯", item=KARA),
        s(SEAT, "sleepy_sleepy_cat", "審判は\nいない", item=KARA),
        # ---- ドリアが恋しい ----
        s(SEAT, "stare_lying_tabby_cat", "ワインも\n半分飲んだ", bgm={"file": LOFI, "gain": -12, "fade": 0.8}, item=WINE),
        s(SEAT, "sleepy_old_memories_cat", "ここまでくると\nあれが恋しくなる"),
        s(SEAT, "realize_wet_cat_stare", "そう"),
        s(SEAT, "stare_big_eyes_tabby_kitten", "サイゼの\nミラノ風ドリア"),
        s(SEAT, "happy_hamster_open_arms", "温玉トッピングで"),
        s(SEAT, "think_chin_paw_orange_cat", "ワインで酔うと\nあれが\n恋しくならんか"),
        s(SEAT, "sleepy_old_memories_cat", "あれ"),
        s(SEAT, "angry_aiming_cat", "あれも\n反則のたぐいだ"),
        s(SEAT, "smug_squint_bicolor_cat", "サイゼのひとり飲みを\n1ランク上げる\n一品"),
        s(SEAT, "confused_i_dont_know_cat", "ここは\nガストなのに"),
        s(SEAT, "despair_dramatic_kitten", "頭の中は\nサイゼ"),
        s(SEAT, "calm_black_face_sheep", "これだから\nサイゼもガストも\n捨てがたい"),
        s(SEAT, "think_chin_paw_orange_cat", "あと\n焼酎ボトルが安いから\nバーミヤンも\n捨てがたい"),
        s(SEAT, "rizz_cat_rizz", "ファミレス\n三国志だ"),
        s(SEAT, "think_chin_paw_orange_cat", "ワインのサイゼ"),
        s(SEAT, "think_chin_paw_orange_cat", "おつまみのガスト"),
        s(SEAT, "think_chin_paw_orange_cat", "焼酎のバーミヤン"),
        s(SEAT, "confused_i_dont_know_cat", "どこにつくかは\nその日の気分"),
        s(SEAT, "smug_squint_bicolor_cat", "天下統一は\nしなくていい"),
        s(SEAT, "rizz_cat_rizz", "全部の国に\n通えばいい"),
        # ---- 時計 ----
        s(SEAT, "stare_tabby_wide_eyes_cat", "ふと\n時計を見る", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(SEAT, "surprise_big_pupils_cat", "まだ\n19時半", se="pi"),
        s(SEAT, "happy_girlfriend_dance_cat", "18時前から\n飲みはじめているから"),
        s(SEAT, "joy_happy_happy_happy_cat", "夜が長い"),
        s(SEAT, "peek_what_happen_cat", "店内は\n家族づれで\nにぎやかになってきた"),
        s(SEAT, "stare_lying_tabby_cat", "子どもが\nネコのロボットに\n手をふっている"),
        s(SEAT, "sleepy_old_memories_cat", "その横で\nボトルワインを\n抱える俺"),
        s(SEAT, "realize_wet_cat_stare", "同じ店で\nそれぞれの\n幸せがある"),
        s(SEAT, "rizz_cat_rizz", "ファミレスは\nみんなのものだ"),
        s(SEAT, "scream_phone_orange_cat", "スマホが光る", se="pi"),
        s(SEAT, "stare_interviewer_cat", "先輩\nあしたの資料\n自分なりに\nアレンジしておきました！"),
        s(SEAT, "surprise_big_pupils_cat", "後輩だ"),
        s(SEAT, "despair_dramatic_kitten", "アレンジは\nたのんでいない"),
        s(SEAT, "think_chin_paw_orange_cat", "今すぐ\n返事をするか"),
        s(SEAT, "calmdown_dancing_cat", "スマホを\nふせる"),
        s(SEAT, "rizz_cat_rizz", "あしたの俺に\nまかせよう"),
        s(SEAT, "eat_crunchy_cat_luna", "ワインを\nもう1杯", se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "work_typing_cat", "しめに\nもう1品"),
        s(SEAT, "think_chin_paw_orange_cat", "ドリアは\nサイゼにとっておく"),
        s(SEAT, "eat_pop_cat", "から好しを\nもう1皿", item=KARA, se="pikon"),
        s(SEAT, "smug_squint_bicolor_cat", "今度は\nハニーマスタードで", item=KARA),
        s(SEAT, "happy_girlfriend_dance_cat", "反則の\nおかわり", item=KARA),
        s(SEAT, "sleepy_sleepy_cat", "ボトルが\n空になった", item=WINE),
        # ---- 会計・帰り道 ----
        s(SEAT, "money_counting_orange_cat", "お会計", se="pi"),
        s(SEAT, "surprise_big_pupils_cat", "ボトルワインまで\n飲んだのに"),
        s(SEAT, "happy_hamster_open_arms", "居酒屋の\n半分くらい"),
        s(SEAT, "rizz_cat_rizz", "財布にも\nやさしい"),
        s(STREET, "leave_cat_leaves_home", "店を出る", se="whoosh_shu", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(STREET, "stare_tabby_wide_eyes_cat", "まだ\n夜8時半"),
        s(STREET, "sleepy_old_memories_cat", "ほろよいで\n夜風が気持ちいい"),
        s(STREET, "think_chin_paw_orange_cat", "帰り道に\nサイゼの看板が\n光っている"),
        s(STREET, "stare_big_eyes_tabby_kitten", "ミラノ風ドリア"),
        s(STREET, "despair_dramatic_kitten", "いや\nさすがに\n入らない"),
        s(STREET, "calmdown_dancing_cat", "今日は\nここまでだ"),
        s(STREET, "smug_squint_bicolor_cat", "あしたは\nサイゼで飲もう"),
        s(STREET, "rizz_cat_rizz", "あさっては\nバーミヤン"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nベッドに倒れこむ", se="whoosh_shu"),
        s(ROOM_N, "scream_phone_orange_cat", "スマホを見る", se="pi"),
        s(ROOM_N, "stare_interviewer_cat", "あした\n残業たのめる？"),
        s(ROOM_N, "blank_black_cat_zoning_out", "……"),
        s(ROOM_N, "sad_black_dog", "サイゼのドリアは\nまた今度だ"),
        s(ROOM_N, "excited_hodomoe_city_cat", "それでも\nファミレスがある限り\n俺は\nがんばれる", se="pikon", dur=3.8),
        J.end_card(),
    ]


def place(cs):
    J.diversify(cs)
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_18_gusto.mp4"), os.path.join(J.HERE, "out", "jidaraku_18_gusto_preview"))
