"""自堕落シリーズ #20：30代独身男、ひとりでサンマルクのパン食べ放題ランチ（11/15 ユーザー指定）。8分をこえる長さ。

python3 catmeme/jidaraku_20_stmarc.py → out/jidaraku_20_stmarc.mp4
- お店はベーカリーレストランサンマルク（サンマルクカフェではない）。ランチのメイン料理を頼むと焼きたてパンが食べ放題
- 口コミより：店員さんがかごに入れた焼きたてパンを席まで持ってきてくれる／パンの種類が多く入れ替わりも早い／
  照明が少し暗めで落ち着いた雰囲気／ドリンクバーの種類は少なめという声も（感想は人それぞれ）
- 値段は出さない（店舗・時期で変わる）。お店・店員さん・ほかのお客さんをけなさない
- 会社の回想（上司の無茶ぶり・後輩が言うことを聞かない）を少し入れる。性別や見た目でからかわない
- 写真は backgrounds/jidaraku/20_stmarc に置く。届くまでは手もちのイラストで仮に（ほかの店の写真は使わない）
- 11/15 ユーザー指定：今後の動画は8分をこえる長さで作る
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "20_stmarc"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku")]
OFFICE, STREET, STREET_E, ROOM_N = "bg25_office_desk", "bg35_suburb_street", "bg51_night_street", "j07_room_night"
FRONT, SEAT = "sm01_front", "sm02_seat"
J.STANDIN.update({SEAT: "bg28_ny_diner"})   # 外観 sm01_front・パン・ハンバーグはユーザー提供（11/15）。f_bread_cheese は塩パンの写真
J.HOLD = 4
J.LOOPS = 1
J.SUB_STYLE = "glow"
MORNING = os.path.join(L.BGM, "Morning.mp3")
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
BASKET, MAIN, SALAD, CHOCO, CHEESE, DESSERT = "f_basket", "f_main", "f_salad", "f_bread_choco", "f_bread_cheese", "f_dessert"


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 平日の会社 ----
        s(OFFICE, "work_typing_cat", "金曜日の昼休み", bgm={"file": LOFI, "gain": -12}),
        s(OFFICE, "eat_pop_cat", "コンビニの\nパンを\nかじる"),
        s(OFFICE, "stare_interviewer_cat", "ちょっといいかな", se="pi"),
        s(OFFICE, "surprise_big_pupils_cat", "上司だ"),
        s(OFFICE, "stare_interviewer_cat", "昼休み中\n悪いんだけど\nこの資料\n今すぐ見て"),
        s(OFFICE, "sad_looking_away_tabby", "パンを\nくわえたまま\n資料を見る"),
        s(OFFICE, "stare_interviewer_cat", "パンくずが\n資料に落ちてるよ"),
        s(OFFICE, "despair_dramatic_kitten", "あなたが\n今来たからです"),
        s(OFFICE, "calm_black_face_sheep", "とは言えない"),
        s(OFFICE, "blank_black_cat_zoning_out", "昼休みは\n10分で終わった"),
        s(OFFICE, "think_chin_paw_orange_cat", "パンくらい\nゆっくり\n食べたい"),
        s(OFFICE, "scream_phone_orange_cat", "スマホで\nパンの店を\n調べる"),
        s(OFFICE, "stare_big_eyes_tabby_kitten", "焼きたてパンが\n食べ放題のランチ"),
        s(OFFICE, "surprise_big_pupils_cat", "ベーカリーレストラン\nサンマルク", se="shine_kiraan_maou"),
        s(OFFICE, "read_book_orange_kitten", "メインの料理を頼むと\nパンが食べ放題\nらしい"),
        s(OFFICE, "angry_aiming_cat", "決めた\n土曜日は\nパンの日だ"),
        # ---- 土曜日 ----
        s(ROOM_N, "sleep_sleeping_cat", "土曜日の朝", bgm={"file": MORNING, "gain": -12, "fade": 0.8}),
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "朝ごはんは\nぬく"),
        s(ROOM_N, "smug_squint_bicolor_cat", "胃袋を\nからっぽにしておく"),
        s(ROOM_N, "rizz_cat_rizz", "パンに対する\n礼儀だ"),
        s(STREET, "drive_driving_cat", "お昼前に\n家を出る", se="whoosh_shu"),
        s(STREET, "happy_hamster_open_arms", "空腹が\nちょうどいい"),
        s(FRONT, "showoff_gojo_cosplay_cat", "到着", se="gong_dora_jaan"),
        s(FRONT, "surprise_big_pupils_cat", "店の前から\nパンのにおい"),
        s(FRONT, "sleepy_old_memories_cat", "このにおいだけで\nごはんが食べられる"),
        s(FRONT, "peek_what_happen_cat", "店の前には\n家族づれと\nカップル"),
        s(FRONT, "sad_looking_away_tabby", "ひとりは\n俺だけか"),
        s(FRONT, "angry_aiming_cat", "パンの前では\nみな平等だ"),
        s(SEAT, "stare_interviewer_cat", "何名様ですか？", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(SEAT, "smug_squint_bicolor_cat", "1名です"),
        s(SEAT, "stare_interviewer_cat", "こちらの\nお席へどうぞ"),
        s(SEAT, "happy_hamster_open_arms", "ふかふかの\nソファ席"),
        s(SEAT, "sleepy_sleepy_cat", "照明は\n少し暗めで\n落ち着く"),
        s(SEAT, "rizz_cat_rizz", "大人の\nパンの時間だ"),
        s(SEAT, "peek_what_happen_cat", "店の奥に\nパンを焼く\nかまどが見える"),
        s(SEAT, "stare_big_eyes_tabby_kitten", "焼き上がるたびに\nいいにおいが\nただよってくる"),
        s(SEAT, "think_chin_paw_orange_cat", "これは\n作戦が必要だ"),
        s(SEAT, "work_typing_cat", "作戦1\nメインは軽めに"),
        s(SEAT, "work_typing_cat", "作戦2\n飲みものでおなかをふくらませない"),
        s(SEAT, "work_typing_cat", "作戦3\n全種類を\n1個ずつ食べる"),
        s(SEAT, "smug_squint_bicolor_cat", "完璧な作戦だ"),
        # ---- 注文 ----
        s(SEAT, "read_book_orange_kitten", "メニューを開く"),
        s(SEAT, "think_chin_paw_orange_cat", "ハンバーグ\nパスタ\nグラタン"),
        s(SEAT, "stare_tabby_wide_eyes_cat", "どれを選んでも\nパンは食べ放題"),
        s(SEAT, "smug_squint_bicolor_cat", "メインは\nパンを食べるための\nチケットだ"),
        s(SEAT, "angry_shooting_cat", "ハンバーグの\nランチで", se="pikon"),
        s(SEAT, "stare_interviewer_cat", "パンは\n順番に\nお持ちしますね"),
        s(SEAT, "surprise_big_pupils_cat", "順番に\n持ってくる？"),
        s(SEAT, "peek_what_happen_cat", "見ると\n店員さんが\nかごを持って\n回っている"),
        s(SEAT, "stare_big_eyes_tabby_kitten", "かごの中には\n焼きたてパン", item=BASKET),
        s(SEAT, "happy_girlfriend_dance_cat", "パンの方から\nやってくる\nシステムだ", item=BASKET),
        s(SEAT, "rizz_cat_rizz", "パンの\n回転ずし", item=BASKET),
        s(SEAT, "think_chin_paw_orange_cat", "ということは", item=BASKET),
        s(SEAT, "stare_tabby_wide_eyes_cat", "かごが来るまで\nパンは\n食べられない", item=BASKET),
        s(SEAT, "surprise_big_pupils_cat", "自分で\n取りに行けない", item=BASKET),
        s(SEAT, "despair_dramatic_kitten", "完全に\n店員さん次第", item=BASKET),
        s(SEAT, "calm_black_face_sheep", "会社と\n同じだ", item=BASKET),
        s(SEAT, "rizz_cat_rizz", "上からの\n配給を待つ", item=BASKET),
        # ---- 1回目のかご ----
        s(SEAT, "stare_lying_tabby_cat", "かごが\n近づいてくる", item=BASKET, bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(SEAT, "stare_interviewer_cat", "焼きたてパン\nいかがですか？", item=BASKET),
        s(SEAT, "surprise_big_pupils_cat", "種類が多い", item=BASKET, se="pi"),
        s(SEAT, "read_book_orange_kitten", "チョコのパン\n塩パン\nくるみのパン", item=BASKET),
        s(SEAT, "think_chin_paw_orange_cat", "最初の1個は\n大事だ", item=BASKET),
        s(SEAT, "angry_aiming_cat", "チョコのパンを\nください", item=CHOCO),
        s(SEAT, "eat_pop_cat", "ふわっ", item=CHOCO, se="pikon"),
        s(SEAT, "happy_girlfriend_dance_cat", "あったかい", item=CHOCO),
        s(SEAT, "eat_crunchy_cat_luna", "中のチョコが\nとろける", item=CHOCO),
        s(SEAT, "realize_wet_cat_stare", "焼きたては\n正義だ", item=CHOCO),
        s(SEAT, "joy_happy_happy_happy_cat", "コンビニのパンと\nは別の食べもの", item=CHOCO),
        s(SEAT, "stare_tabby_wide_eyes_cat", "あっという間に\nなくなった", item=CHOCO),
        s(SEAT, "think_chin_paw_orange_cat", "次のかごは\nまだか", item=CHOCO),
        # ---- サラダとメイン ----
        s(SEAT, "stare_big_eyes_tabby_kitten", "先にサラダが来た", item=SALAD),
        s(SEAT, "smug_squint_bicolor_cat", "野菜を先に食べると\n体にいいらしい", item=SALAD),
        s(SEAT, "eat_crunchy_cat_luna", "シャキシャキ", item=SALAD),
        s(SEAT, "calm_black_face_sheep", "これで\nパンを食べる\n言いわけができた", item=SALAD),
        s(SEAT, "surprise_big_pupils_cat", "ハンバーグが\nやってきた", item=MAIN, se="shine_kiraan_maou"),
        s(SEAT, "happy_hamster_open_arms", "鉄板の上で\nジュージュー", item=MAIN),
        s(SEAT, "eat_pop_cat", "ガブッ", item=MAIN, se="pikon"),
        s(SEAT, "happy_girlfriend_dance_cat", "肉汁が\nあふれる", item=MAIN),
        s(SEAT, "think_chin_paw_orange_cat", "このソース", item=MAIN),
        s(SEAT, "angry_aiming_cat", "パンに\nつけたい", item=MAIN),
        s(SEAT, "stare_lying_tabby_cat", "でも\nパンがない", item=MAIN),
        s(SEAT, "despair_dramatic_kitten", "かごが\n来ない", item=MAIN),
        s(SEAT, "peek_what_happen_cat", "かごは\nとなりの家族の席で\nとまっている", item=BASKET),
        s(SEAT, "sad_looking_away_tabby", "子どもが\n全種類\n選んでいる", item=BASKET),
        s(SEAT, "calm_black_face_sheep", "待とう\n子どもの\nパンの時間は大事だ", item=BASKET),
        # ---- 2回目のかご ----
        s(SEAT, "stare_interviewer_cat", "焼きたてパン\nいかがですか？", item=BASKET, se="pi"),
        s(SEAT, "showoff_gojo_cosplay_cat", "来た", item=BASKET, se="gong_dora_jaan"),
        s(SEAT, "angry_shooting_cat", "塩パンと\nくるみのパンを", item=CHEESE),
        s(SEAT, "work_typing_cat", "ハンバーグのソースを\nパンでぬぐう", item=MAIN),
        s(SEAT, "eat_crunchy_cat_luna", "もぐっ", item=CHEESE, se="pikon"),
        s(SEAT, "realize_wet_cat_stare", "これが\nやりたかった", item=CHEESE),
        s(SEAT, "happy_girlfriend_dance_cat", "皿の上が\nピカピカになる", item=MAIN),
        s(SEAT, "rizz_cat_rizz", "パンは\n最高のスポンジだ", item=CHEESE),
        s(SEAT, "think_chin_paw_orange_cat", "作戦1\nメインは軽めに", item=MAIN),
        s(SEAT, "stare_lying_tabby_cat", "ハンバーグを\n完食している", item=MAIN),
        s(SEAT, "despair_dramatic_kitten", "作戦は\n1つ目から\nくずれた", item=MAIN),
        s(SEAT, "calmdown_dancing_cat", "まあいい", item=MAIN),
        s(SEAT, "eat_pop_cat", "塩パンも\nもっちもち", item=CHEESE),
        s(SEAT, "joy_happy_happy_happy_cat", "これで\n3個", item=CHEESE),
        # ---- 回想：後輩 ----
        s(SEAT, "think_chin_paw_orange_cat", "ちぎって食べると\nふと思い出す", item=CHEESE),
        s(OFFICE, "sleepy_old_memories_cat", "先週の\n後輩", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(OFFICE, "work_typing_cat", "この仕事\n少しずつ\n分けて進めてね"),
        s(OFFICE, "stare_interviewer_cat", "わかりました！"),
        s(OFFICE, "peek_what_happen_cat", "翌日"),
        s(OFFICE, "stare_interviewer_cat", "全部まとめて\n一気にやりました！"),
        s(OFFICE, "surprise_big_pupils_cat", "早いな"),
        s(OFFICE, "stare_interviewer_cat", "でも\n途中で\n全部消えました！"),
        s(OFFICE, "scream_standing_marmot", "保存は？", se="explosion_chudoon"),
        s(OFFICE, "stare_interviewer_cat", "最後に\nまとめて\nしようと思ってました！"),
        s(OFFICE, "blank_black_cat_zoning_out", "その日\nふたりで\n終電まで"),
        s(SEAT, "smug_squint_bicolor_cat", "パンも仕事も", item=CHEESE, bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(SEAT, "rizz_cat_rizz", "少しずつ\nちぎるのが\nいちばんだ", item=CHEESE),
        # ---- 3回目〜 ----
        s(SEAT, "stare_interviewer_cat", "焼きたてパン\nいかがですか？", item=BASKET),
        s(SEAT, "surprise_big_pupils_cat", "また来た", item=BASKET),
        s(SEAT, "think_chin_paw_orange_cat", "おなかは\n少しきつい", item=BASKET),
        s(SEAT, "stare_tabby_wide_eyes_cat", "でも\nかごの中に\n見たことないパン", item=BASKET),
        s(SEAT, "read_book_orange_kitten", "焼きたての\n新しい種類", item=BASKET),
        s(SEAT, "angry_aiming_cat", "断れない", item=BASKET, se="explosion_chudoon"),
        s(SEAT, "eat_pop_cat", "ください", item=BASKET),
        s(SEAT, "happy_hamster_open_arms", "これで\n5個", item=BASKET),
        s(SEAT, "stare_lying_tabby_cat", "かごが\n回ってくるたびに", item=BASKET),
        s(SEAT, "sad_looking_away_tabby", "パンが\n1個ふえる", item=BASKET),
        s(SEAT, "despair_dramatic_kitten", "これは\nわんこそばだ", item=BASKET),
        s(SEAT, "eat_crunchy_cat_luna", "7個", item=BASKET),
        s(SEAT, "sleepy_sleepy_cat", "8個", item=BASKET),
        s(SEAT, "think_chin_paw_orange_cat", "ふと\nまわりを見る", item=BASKET),
        s(SEAT, "peek_what_happen_cat", "となりの\nカップルは\n2個で終わっている", item=BASKET),
        s(SEAT, "calm_black_face_sheep", "店員さんが\n俺の席にだけ\nよく来る気がする", item=BASKET),
        s(SEAT, "rizz_cat_rizz", "常連だと\n思われている", item=BASKET),
        s(SEAT, "blank_black_cat_zoning_out", "今日\n初めて来た", item=BASKET),
        s(SEAT, "work_typing_cat", "ここまでの\nパンランキング", item=BASKET, bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(SEAT, "read_book_orange_kitten", "3位\nくるみのパン\n香ばしい", item=BASKET),
        s(SEAT, "read_book_orange_kitten", "2位\n塩パン\nもっちもち", item=CHEESE),
        s(SEAT, "read_book_orange_kitten", "1位\nチョコのパン\n焼きたてが反則", item=CHOCO),
        s(SEAT, "smug_squint_bicolor_cat", "でも\nランキングは\nかごが来るたびに\n変わる", item=BASKET),
        s(SEAT, "rizz_cat_rizz", "パンの世界は\n下克上だ", item=BASKET),
        # ---- ドリンクバー ----
        s(SEAT, "stare_big_eyes_tabby_kitten", "のどがかわいた", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(SEAT, "work_typing_cat", "ドリンクバーへ"),
        s(SEAT, "think_chin_paw_orange_cat", "種類は\nひかえめ"),
        s(SEAT, "smug_squint_bicolor_cat", "でも\nパンに合う\nコーヒーと紅茶がある"),
        s(SEAT, "eat_crunchy_cat_luna", "ゴクッ", se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "happy_hamster_open_arms", "パンと\nコーヒー"),
        s(SEAT, "rizz_cat_rizz", "これ以上の\n組み合わせはない"),
        s(SEAT, "sleepy_old_memories_cat", "ここで\nもう少し\nゆっくりしよう"),
        # ---- 回想：上司 ----
        s(SEAT, "stare_lying_tabby_cat", "コーヒーを飲みながら\nぼんやりする"),
        s(OFFICE, "sleepy_old_memories_cat", "そういえば\n上司は\nいつも言う", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(OFFICE, "stare_interviewer_cat", "昼は\nサッと食べて\nすぐもどるのが\nできる社員だ"),
        s(OFFICE, "sad_looking_away_tabby", "だから\nいつも10分"),
        s(OFFICE, "peek_what_happen_cat", "その上司は"),
        s(OFFICE, "stare_interviewer_cat", "今日は\n2時間ランチで\n取引先とパスタ\nだったよ"),
        s(OFFICE, "despair_dramatic_kitten", "自分は\nゆっくり食べている", se="explosion_chudoon"),
        s(OFFICE, "blank_black_cat_zoning_out", "できる社員の\n定義とは"),
        s(OFFICE, "sleepy_old_memories_cat", "そういえば\n事務の人にも"),
        s(OFFICE, "talk_orange_white_sitting_cat", "すみませーん\n会議のおかし\n買ってきてください"),
        s(OFFICE, "huh_huh_cat", "俺\n会議に出ないです", se="question_mark_pop_confused_huh"),
        s(OFFICE, "talk_orange_white_sitting_cat", "でも\nパンにくわしそうなので"),
        s(OFFICE, "despair_dramatic_kitten", "昼休みに\nコンビニのパンを\n食べていただけ"),
        s(OFFICE, "work_typing_cat", "結局\n昼休みに\nパン屋さんへ走った"),
        s(OFFICE, "talk_orange_white_sitting_cat", "あ\nやっぱり\nおせんべいで"),
        s(OFFICE, "sad_black_dog", "パン10個\n俺が食べた"),
        s(SEAT, "calmdown_dancing_cat", "今日は\n2時間ランチだ", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(SEAT, "rizz_cat_rizz", "俺も今日は\nできる社員だ"),
        # ---- 最後のかご ----
        s(SEAT, "stare_interviewer_cat", "焼きたてパン\nいかがですか？", item=BASKET, se="pi"),
        s(SEAT, "despair_dramatic_kitten", "おなかは\nもう限界", item=BASKET),
        s(SEAT, "stare_tabby_wide_eyes_cat", "でも\nかごに\nメロンパン", item=BASKET),
        s(SEAT, "surprise_big_pupils_cat", "焼きたての\nメロンパン", item=BASKET),
        s(SEAT, "angry_aiming_cat", "最後の1個だ", item=BASKET),
        s(SEAT, "eat_pop_cat", "サクッ", item=BASKET, se="pikon"),
        s(SEAT, "happy_girlfriend_dance_cat", "外はサクサク\n中はふわふわ", item=BASKET),
        s(SEAT, "realize_wet_cat_stare", "パン人生で\nいちばんの\nメロンパン", item=BASKET),
        s(SEAT, "stare_lying_tabby_cat", "合計\n10個", item=BASKET),
        s(SEAT, "smug_squint_bicolor_cat", "ハンバーグより\nパンを食べた", item=BASKET),
        s(SEAT, "stare_interviewer_cat", "デザートを\nお持ちしました", item=DESSERT),
        s(SEAT, "surprise_big_pupils_cat", "デザートも\nついていた", item=DESSERT, se="shine_kiraan_maou"),
        s(SEAT, "sad_banana_cat_cry", "入る場所が\nない", item=DESSERT),
        s(SEAT, "eat_crunchy_cat_luna", "でも\n甘いものは\n別の胃袋", item=DESSERT),
        s(SEAT, "happy_hamster_open_arms", "ペロリ", item=DESSERT),
        s(SEAT, "sleepy_sleepy_cat", "しあわせな\n満腹", item=DESSERT),
        s(SEAT, "scream_phone_orange_cat", "記念に\n写真をとる", item=DESSERT),
        s(SEAT, "think_chin_paw_orange_cat", "でも\nパンは全部\nおなかの中", item=DESSERT),
        s(SEAT, "sad_looking_away_tabby", "写っているのは\nからっぽのかごと\nデザートの皿", item=DESSERT),
        s(SEAT, "calm_black_face_sheep", "誰にも\n伝わらない", item=DESSERT),
        s(SEAT, "rizz_cat_rizz", "思い出は\n胃袋の中に", item=DESSERT),
        s(SEAT, "despair_dramatic_kitten", "立ち上がろうとする", item=DESSERT),
        s(SEAT, "scream_standing_marmot", "パンの重みで\n立てない", item=DESSERT, se="explosion_chudoon"),
        s(SEAT, "sleepy_old_memories_cat", "あと5分だけ\nソファに\nしずむ", item=DESSERT),
        # ---- 会計・帰り道 ----
        s(SEAT, "money_counting_orange_cat", "お会計", se="pi"),
        s(SEAT, "stare_interviewer_cat", "ありがとうございましたー"),
        s(SEAT, "rizz_cat_rizz", "パン10個で\nこのお値段"),
        s(SEAT, "happy_girlfriend_dance_cat", "パン屋さんで\n10個買うより\nオトク"),
        s(SEAT, "think_chin_paw_orange_cat", "レジの横にも\nパンが\n売っている"),
        s(SEAT, "stare_big_eyes_tabby_kitten", "持ち帰り用の\n焼きたてパン"),
        s(SEAT, "angry_aiming_cat", "おなかは\nいっぱいなのに"),
        s(SEAT, "money_counting_orange_cat", "なぜか\n明日の朝の\nパンを買う"),
        s(SEAT, "smug_squint_bicolor_cat", "明日の俺への\nおみやげだ"),
        s(FRONT, "leave_cat_leaves_home", "満腹で店を出る", se="whoosh_shu", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(STREET, "drive_driving_cat", "帰り道"),
        s(STREET, "sleepy_old_memories_cat", "服から\nパンのにおい"),
        s(STREET, "think_chin_paw_orange_cat", "夜ごはんは\nいらないな"),
        s(STREET, "stare_tabby_wide_eyes_cat", "帰りにパン屋さんが\n見える"),
        s(STREET, "smug_squint_bicolor_cat", "今日は\nもう\n見ないふり"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nソファに沈む", se="whoosh_shu"),
        s(ROOM_N, "sleepy_sleepy_cat", "そのまま\n昼寝"),
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "夜8時\n目が覚める", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(ROOM_N, "sulk_hungry_cat", "……おなかがすいた"),
        s(ROOM_N, "despair_dramatic_kitten", "パン10個\nどこへ消えた"),
        s(ROOM_N, "work_typing_cat", "冷蔵庫を開ける"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "そういえば\n明日の朝のパン"),
        s(ROOM_N, "eat_pop_cat", "明日の俺へのおみやげを\n今の俺が食べる"),
        s(ROOM_N, "happy_hamster_open_arms", "冷めてもうまい"),
        s(ROOM_N, "calm_black_face_sheep", "明日の朝は\nコンビニのパンだ"),
        s(ROOM_N, "sleepy_old_memories_cat", "でも\n今日の俺には\nわかる"),
        s(ROOM_N, "rizz_cat_rizz", "パンは\nどれも\nえらい"),
        s(ROOM_N, "scream_phone_orange_cat", "月曜日の\n予定を見る"),
        s(ROOM_N, "stare_interviewer_cat", "月曜朝イチで\n例の資料よろしく"),
        s(ROOM_N, "blank_black_cat_zoning_out", "……"),
        s(ROOM_N, "smug_squint_bicolor_cat", "少しずつ\nちぎって\nやればいい"),
        s(ROOM_N, "excited_hodomoe_city_cat", "来週も\nパンのために\nがんばろう", se="pikon", dur=3.8),
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_20_stmarc.mp4"), os.path.join(J.HERE, "out", "jidaraku_20_stmarc_preview"))
