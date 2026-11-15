"""自堕落シリーズ #21：30代独身男、ひとりでケンタッキーの食べ放題（11/15 ユーザー指定）。8分をこえる長さ。

python3 catmeme/jidaraku_21_kfc.py → out/jidaraku_21_kfc.mp4
- 流れ（ユーザー指定）：始まる前「ケンタのチキンの衣うますぎない？衣だけのメニューがほしい」→
  「何個食べれば元が取れるんだ。元は取りたい。それが我々“放題スト”の使命」→
  後半かなり苦しくなり「やはり衣だけの食べ放題がほしい…」
- 食べ放題はビュッフェ形式の KFC のレストラン（昼は80分制）。値段・店名は出さない（店舗・時期で変わる）
- 口コミ・記事より：オリジナルチキンのほかにビスケット・ポテト・サラダ・パスタやカレーなど・デザートも並ぶ／
  ビスケットにはちみつ／骨が皿にたまっていく／手が油でテカテカ
- 会社の回想を少し入れる（上司・後輩）。性別や見た目でからかわない。お店・ほかのお客さんをけなさない
- 写真は backgrounds/jidaraku/21_kfc に置く。届くまでは手もちのイラストで仮に（ほかの店の写真は使わない）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "21_kfc"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku")]
OFFICE, STREET, STREET_N, ROOM_N = "bg25_office_desk", "bg35_suburb_street", "bg51_night_street", "j07_room_night"
FRONT, SEAT, BUFFET = "kf01_front", "kf02_seat", "kf03_buffet"
# 写真はユーザー提供（11/15）。骨の皿・デザートの写真はないので、その場面は写真なし。チキンの皿 f_plate はパスタ・カレーの場面では出さない（11/15 ユーザー指定）
J.HOLD = 4
J.LOOPS = 1
J.SUB_STYLE = "glow"
MORNING = os.path.join(L.BGM, "Morning.mp3")
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
CHICKEN, PLATE, BISCUIT, POTATO, BONES, DESSERT = "f_chicken", "f_plate", "f_biscuit", "f_potato", "f_bones", "f_dessert"


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 衣の話 ----
        s(ROOM_N, "stare_lying_tabby_cat", "金曜日の夜", bgm={"file": LOFI, "gain": -12}),
        s(ROOM_N, "eat_pop_cat", "仕事帰りに買った\nケンタッキー", item=CHICKEN),
        s(ROOM_N, "eat_crunchy_cat_luna", "ザクッ", item=CHICKEN, se="pikon"),
        s(ROOM_N, "happy_girlfriend_dance_cat", "うまい", item=CHICKEN),
        s(ROOM_N, "think_chin_paw_orange_cat", "いつも思う", item=CHICKEN),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "ケンタのチキンの\n衣", item=CHICKEN),
        s(ROOM_N, "surprise_big_pupils_cat", "うますぎない？", item=CHICKEN, se="pi"),
        s(ROOM_N, "read_book_orange_kitten", "11種類のハーブと\nスパイスの\n秘密の味", item=CHICKEN),
        s(ROOM_N, "eat_pop_cat", "気づけば\n衣から食べている", item=CHICKEN),
        s(ROOM_N, "smug_squint_bicolor_cat", "肉は\n衣をのせるための\nお皿だ", item=CHICKEN),
        s(ROOM_N, "angry_aiming_cat", "衣だけの\nメニューがほしい", item=CHICKEN, se="explosion_chudoon"),
        s(ROOM_N, "rizz_cat_rizz", "衣バケツ\n衣パック\n衣セット", item=CHICKEN),
        s(ROOM_N, "calm_black_face_sheep", "そんなものは\nない", item=CHICKEN),
        s(ROOM_N, "sad_looking_away_tabby", "1ピースで\nおなかいっぱい", item=CHICKEN),
        s(ROOM_N, "think_chin_paw_orange_cat", "もっと\n衣を食べたい"),
        s(ROOM_N, "scream_phone_orange_cat", "スマホで調べる"),
        s(ROOM_N, "surprise_big_pupils_cat", "ケンタッキーの\n食べ放題が\nあるらしい", se="shine_kiraan_maou"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "昼は80分の\nビュッフェ形式"),
        s(ROOM_N, "read_book_orange_kitten", "オリジナルチキンも\nサイドメニューも\nデザートも"),
        s(ROOM_N, "showoff_gojo_cosplay_cat", "明日は\n衣の日だ", se="gong_dora_jaan"),
        # ---- 元を取る計算 ----
        s(ROOM_N, "work_typing_cat", "その前に\n計算しておく", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(ROOM_N, "money_counting_orange_cat", "チキン1ピースは\nだいたい\n300円ちょっと"),
        s(ROOM_N, "think_chin_paw_orange_cat", "ということは\n8ピース食べれば\n元が取れる"),
        s(ROOM_N, "surprise_big_pupils_cat", "8ピース", se="pi"),
        s(ROOM_N, "despair_dramatic_kitten", "ふだん\n2ピースで\nもう満足なのに"),
        s(ROOM_N, "angry_aiming_cat", "だが\n元は取りたい"),
        s(ROOM_N, "smug_squint_bicolor_cat", "それが\n我々\n放題ストの使命"),
        s(ROOM_N, "rizz_cat_rizz", "食べ放題に\n行く者は\nみな放題ストだ"),
        s(ROOM_N, "read_book_orange_kitten", "放題ストの掟\nその1\n朝ごはんは食べない"),
        s(ROOM_N, "read_book_orange_kitten", "放題ストの掟\nその2\nジュースで\nおなかをふくらませない"),
        s(ROOM_N, "read_book_orange_kitten", "放題ストの掟\nその3\nポテトは\n後半にまわす"),
        s(ROOM_N, "sleep_sleeping_cat", "胃袋を休ませるため\n早く寝る"),
        # ---- 当日 ----
        s(STREET, "drive_driving_cat", "土曜日の昼", se="whoosh_shu", bgm={"file": MORNING, "gain": -12, "fade": 0.8}),
        s(STREET, "sulk_hungry_cat", "朝ごはんは\nぬいた"),
        s(STREET, "happy_hamster_open_arms", "空腹は\n最高のスパイス"),
        s(STREET, "smug_squint_bicolor_cat", "12種類目の\nスパイスだ"),
        s(FRONT, "showoff_gojo_cosplay_cat", "到着", se="gong_dora_jaan"),
        s(FRONT, "peek_what_happen_cat", "おなじみの\nおじさんの看板"),
        s(FRONT, "stare_big_eyes_tabby_kitten", "やさしい笑顔で\n迎えてくれる"),
        s(FRONT, "angry_aiming_cat", "今日は\nその笑顔に\n勝ちに来た"),
        s(SEAT, "stare_interviewer_cat", "何名様ですか？", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(SEAT, "smug_squint_bicolor_cat", "1名です"),
        s(SEAT, "stare_interviewer_cat", "80分の\n食べ放題ですね"),
        s(SEAT, "peek_what_happen_cat", "まわりは\n家族づれと\nカップル"),
        s(SEAT, "sad_looking_away_tabby", "ひとりは\n俺だけか"),
        s(SEAT, "rizz_cat_rizz", "放題ストは\nいつだって\n孤独な戦士だ"),
        s(SEAT, "work_typing_cat", "タイマーを\n80分に\nセットする"),
        s(SEAT, "think_chin_paw_orange_cat", "作戦を\nおさらいする"),
        s(SEAT, "read_book_orange_kitten", "目標\nチキン8ピース"),
        s(SEAT, "smug_squint_bicolor_cat", "1ピース10分で\n80分\n計算はあっている"),
        s(SEAT, "stare_tabby_wide_eyes_cat", "おしぼりを\n3枚もらっておく"),
        s(SEAT, "rizz_cat_rizz", "放題ストは\n準備をおこたらない"),
        s(BUFFET, "showoff_gojo_cosplay_cat", "スタート", se="gong_dora_jaan"),
        # ---- 1皿目 ----
        s(BUFFET, "surprise_big_pupils_cat", "ずらりと並ぶ\nオリジナルチキン", item=CHICKEN, se="shine_kiraan_maou"),
        s(BUFFET, "happy_girlfriend_dance_cat", "チキンの山だ", item=CHICKEN),
        s(BUFFET, "read_book_orange_kitten", "ほかにも\nビスケット\nポテト\nサラダ", item=PLATE),
        s(BUFFET, "think_chin_paw_orange_cat", "でも\n掟を守る", item=PLATE),
        s(BUFFET, "angry_aiming_cat", "まずは\nチキン3ピース", item=PLATE),
        s(SEAT, "eat_crunchy_cat_luna", "ザクッ", item=CHICKEN, se="pikon"),
        s(SEAT, "realize_wet_cat_stare", "揚げたての衣", item=CHICKEN),
        s(SEAT, "happy_hamster_open_arms", "テイクアウトの\n100倍うまい", item=CHICKEN),
        s(SEAT, "eat_pop_cat", "ジュワッと\n肉汁", item=CHICKEN),
        s(SEAT, "joy_happy_happy_happy_cat", "1ピース目\nクリア", item=CHICKEN),
        s(SEAT, "eat_crunchy_cat_luna", "2ピース目", item=CHICKEN),
        s(SEAT, "eat_pop_cat", "3ピース目", item=CHICKEN),
        s(SEAT, "smug_squint_bicolor_cat", "順調だ", item=CHICKEN),
        s(SEAT, "stare_lying_tabby_cat", "皿の上に\n骨がたまっていく", item=BONES),
        s(SEAT, "rizz_cat_rizz", "これは\n戦いの記録だ", item=BONES),
        s(SEAT, "stare_tabby_wide_eyes_cat", "手は\n油でテカテカ", item=BONES),
        s(SEAT, "calm_black_face_sheep", "スマホは\nさわれない", item=BONES),
        s(SEAT, "eat_pop_cat", "指についた衣も\nのがさない", item=BONES),
        s(SEAT, "realize_wet_cat_stare", "指まで\nおいしい", item=BONES),
        s(SEAT, "work_typing_cat", "おしぼりで\nふく", item=BONES),
        s(SEAT, "smug_squint_bicolor_cat", "3枚もらって\n正解だった", item=BONES),
        s(SEAT, "happy_girlfriend_dance_cat", "誰からの連絡も\n見なくていい", item=BONES),
        s(SEAT, "think_chin_paw_orange_cat", "ここで\n放題ストの知識", item=CHICKEN),
        s(SEAT, "read_book_orange_kitten", "オリジナルチキンには\n5つの部位がある", item=CHICKEN),
        s(SEAT, "read_book_orange_kitten", "キール\nドラム\nリブ\nサイ\nウイング", item=CHICKEN),
        s(SEAT, "smug_squint_bicolor_cat", "衣の面積が\nいちばん広いのは", item=CHICKEN),
        s(SEAT, "angry_aiming_cat", "サイだ", item=CHICKEN, se="explosion_chudoon"),
        s(SEAT, "stare_tabby_wide_eyes_cat", "※個人の感想です", item=CHICKEN),
        s(SEAT, "rizz_cat_rizz", "次は\nサイを\nねらい撃ちだ", item=CHICKEN),
        # ---- 2皿目 ----
        s(BUFFET, "work_typing_cat", "2皿目へ", item=PLATE, bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(BUFFET, "angry_aiming_cat", "チキン\nもう3ピース", item=CHICKEN),
        s(BUFFET, "stare_big_eyes_tabby_kitten", "トレーをのぞくと\nサイがない", item=CHICKEN),
        s(BUFFET, "despair_dramatic_kitten", "みんな\n知っていたのか", item=CHICKEN),
        s(BUFFET, "stare_interviewer_cat", "揚げたて\n入りまーす", item=CHICKEN, se="pi"),
        s(BUFFET, "surprise_big_pupils_cat", "揚げたての\nチキンが\n追加された", item=CHICKEN, se="shine_kiraan_maou"),
        s(BUFFET, "peek_what_happen_cat", "まわりの放題ストたちが\n静かに立ち上がる", item=CHICKEN),
        s(BUFFET, "angry_shooting_cat", "トングの\n静かな戦い", item=CHICKEN, se="explosion_dokaan"),
        s(BUFFET, "showoff_gojo_cosplay_cat", "サイ\nゲット", item=CHICKEN, se="gong_dora_jaan"),
        s(BUFFET, "calm_black_face_sheep", "譲りあいの心も\n忘れない", item=CHICKEN),
        s(BUFFET, "stare_big_eyes_tabby_kitten", "ビスケットが\n目に入る", item=BISCUIT),
        s(BUFFET, "think_chin_paw_orange_cat", "炭水化物は\n掟違反では", item=BISCUIT),
        s(BUFFET, "smug_squint_bicolor_cat", "1個だけなら\n味見だ", item=BISCUIT),
        s(SEAT, "eat_pop_cat", "ビスケットに\nはちみつ", item=BISCUIT, se="pikon"),
        s(SEAT, "surprise_big_pupils_cat", "あまい", item=BISCUIT),
        s(SEAT, "happy_hamster_open_arms", "しょっぱいチキンと\nあまいビスケット", item=BISCUIT),
        s(SEAT, "rizz_cat_rizz", "無限ループの\n入り口だ", item=BISCUIT),
        s(SEAT, "eat_crunchy_cat_luna", "チキン", item=CHICKEN),
        s(SEAT, "eat_pop_cat", "ビスケット", item=BISCUIT),
        s(SEAT, "eat_crunchy_cat_luna", "チキン", item=CHICKEN),
        s(SEAT, "despair_dramatic_kitten", "ビスケット\n3個目", item=BISCUIT),
        s(SEAT, "sad_looking_away_tabby", "掟は\n2皿目で\nやぶられた", item=BISCUIT),
        s(SEAT, "work_typing_cat", "ここで\n途中計算", item=BONES),
        s(SEAT, "money_counting_orange_cat", "チキン6ピース", item=BONES),
        s(SEAT, "think_chin_paw_orange_cat", "元を取るまで\nあと2ピース", item=BONES),
        s(SEAT, "angry_aiming_cat", "いける", item=BONES),
        # ---- 回想 ----
        s(SEAT, "stare_lying_tabby_cat", "骨を見つめていると\nふと思い出す", item=BONES),
        s(OFFICE, "sleepy_old_memories_cat", "先週の会議", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(OFFICE, "stare_interviewer_cat", "この企画は\n骨組みだけ\nあればいいから"),
        s(OFFICE, "work_typing_cat", "骨組みだけ作る"),
        s(OFFICE, "stare_interviewer_cat", "中身がスカスカだな"),
        s(OFFICE, "despair_dramatic_kitten", "骨組みだけって\n言いました", se="explosion_chudoon"),
        s(OFFICE, "stare_interviewer_cat", "肉付けまでが\n骨組みだよ"),
        s(OFFICE, "blank_black_cat_zoning_out", "それは\nもう\nチキンです"),
        s(OFFICE, "sleepy_old_memories_cat", "さらに後輩"),
        s(OFFICE, "stare_interviewer_cat", "先輩\n肉付けは\nやっておきました！"),
        s(OFFICE, "surprise_big_pupils_cat", "ありがたい"),
        s(OFFICE, "stare_interviewer_cat", "骨組みは\nじゃまだったので\n消しました！"),
        s(OFFICE, "scream_standing_marmot", "骨を\n消すな", se="explosion_dokaan"),
        s(OFFICE, "sleepy_old_memories_cat", "そして\n事務の人"),
        s(OFFICE, "talk_orange_white_sitting_cat", "すみませーん\n交通費の書類\nレシートの\n原本ください"),
        s(OFFICE, "work_typing_cat", "レシートを\n探す"),
        s(OFFICE, "despair_dramatic_kitten", "チキンの油で\nとうめいになっていた"),
        s(OFFICE, "talk_orange_white_sitting_cat", "読めないので\n再発行してください"),
        s(OFFICE, "calm_black_face_sheep", "その日の夜は\nチキンが\nのどを通らなかった"),
        s(SEAT, "calmdown_dancing_cat", "今は\n骨のことは忘れよう", item=BONES, bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        # ---- 3皿目 ----
        s(BUFFET, "angry_aiming_cat", "3皿目", item=CHICKEN),
        s(BUFFET, "read_book_orange_kitten", "パスタや\nカレーまで\nある"),
        s(BUFFET, "think_chin_paw_orange_cat", "ケンタッキーで\nカレー"),
        s(BUFFET, "smug_squint_bicolor_cat", "これは\n味見しないと\n失礼だ"),
        s(SEAT, "eat_pop_cat", "カレーの上に\nチキンをのせる", se="pikon"),
        s(SEAT, "happy_girlfriend_dance_cat", "チキンカレーの\n完成"),
        s(SEAT, "rizz_cat_rizz", "ここだけの\n裏メニューだ"),
        s(SEAT, "eat_crunchy_cat_luna", "7ピース目", item=CHICKEN),
        s(SEAT, "stare_tabby_wide_eyes_cat", "……", item=CHICKEN),
        s(SEAT, "sleepy_sleepy_cat", "少し\nペースが落ちてきた", item=CHICKEN),
        s(SEAT, "work_typing_cat", "タイマーを見る\n残り40分", item=BONES),
        s(SEAT, "smug_squint_bicolor_cat", "まだ半分", item=BONES),
        s(SEAT, "calm_black_face_sheep", "まだ半分……", item=BONES),
        s(SEAT, "stare_lying_tabby_cat", "ドリンクバーで\nひと休み", item=BONES),
        s(SEAT, "think_chin_paw_orange_cat", "掟その2\nジュースで\nおなかをふくらませない", item=BONES),
        s(SEAT, "smug_squint_bicolor_cat", "なので\nウーロン茶", item=BONES),
        s(SEAT, "eat_crunchy_cat_luna", "ゴクッ", item=BONES, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "happy_hamster_open_arms", "油が\nリセットされる", item=BONES),
        s(SEAT, "rizz_cat_rizz", "ウーロン茶は\n放題ストの\n味方だ", item=BONES),
        s(SEAT, "stare_tabby_wide_eyes_cat", "ふと\n骨の皿を見る", item=BONES),
        s(SEAT, "surprise_big_pupils_cat", "骨が\nタワーになっている", item=BONES),
        s(SEAT, "peek_what_happen_cat", "となりの家族が\nちらっと見た", item=BONES),
        s(SEAT, "sad_looking_away_tabby", "そっと\n骨の皿を\n下げてもらう", item=BONES),
        # ---- 苦しくなる ----
        s(SEAT, "stare_lying_tabby_cat", "8ピース目", item=CHICKEN, bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(SEAT, "despair_dramatic_kitten", "手が\nのびない", item=CHICKEN),
        s(SEAT, "sad_black_dog", "チキンが\n重い", item=CHICKEN),
        s(SEAT, "think_chin_paw_orange_cat", "衣は\nまだ食べたい", item=CHICKEN),
        s(SEAT, "sad_looking_away_tabby", "でも\n中の肉が\nついてくる", item=CHICKEN),
        s(SEAT, "realize_wet_cat_stare", "肉よ\n今は\nおまえじゃない", item=CHICKEN),
        s(SEAT, "work_typing_cat", "衣だけ食べて\n肉を残すのは\nマナー違反", item=CHICKEN),
        s(SEAT, "despair_dramatic_kitten", "放題ストの\n誇りが許さない", item=CHICKEN),
        s(SEAT, "eat_pop_cat", "ゆっくり\nかみしめる", item=CHICKEN),
        s(SEAT, "stare_tabby_wide_eyes_cat", "…………", item=CHICKEN),
        s(SEAT, "showoff_gojo_cosplay_cat", "8ピース\n完食", item=BONES, se="gong_dora_jaan"),
        s(SEAT, "joy_happy_happy_happy_cat", "元が取れた", item=BONES),
        s(SEAT, "sleepy_sleepy_cat", "でも\n喜ぶ元気が\nない", item=BONES),
        s(SEAT, "peek_what_happen_cat", "となりの子どもが\nソフトクリームを\n食べている", item=DESSERT),
        s(SEAT, "sad_looking_away_tabby", "あんなに\n軽やかに", item=DESSERT),
        s(SEAT, "realize_wet_cat_stare", "子どもは\nペース配分の天才だ", item=DESSERT),
        s(SEAT, "despair_dramatic_kitten", "ポテトを\n後半にまわした\n過去の俺", item=POTATO),
        s(SEAT, "sad_black_dog", "後半の俺に\n入る場所はない", item=POTATO),
        s(SEAT, "scream_standing_marmot", "掟その3が\n牙をむく", item=POTATO, se="explosion_chudoon"),
        s(SEAT, "eat_crunchy_cat_luna", "ポテトを\n1本だけ", item=POTATO),
        s(SEAT, "calm_black_face_sheep", "ポテトにも\n礼儀はつくした", item=POTATO),
        s(SEAT, "stare_lying_tabby_cat", "そして\n思う", item=BONES),
        s(SEAT, "sad_banana_cat_cry", "やはり\n衣だけの\n食べ放題がほしい", item=CHICKEN, se="explosion_dokaan"),
        s(SEAT, "rizz_cat_rizz", "衣だけなら\nまだ\n10ピースいける", item=CHICKEN),
        s(SEAT, "think_chin_paw_orange_cat", "衣バイキング\n衣ビュッフェ\n衣放題", item=CHICKEN),
        s(SEAT, "calm_black_face_sheep", "店員さんに\n言う勇気はない", item=CHICKEN),
        s(SEAT, "think_chin_paw_orange_cat", "でも\n想像してみる", item=CHICKEN),
        s(SEAT, "happy_girlfriend_dance_cat", "皿いっぱいの\n衣だけ", item=CHICKEN),
        s(SEAT, "eat_crunchy_cat_luna", "ザクザク\nザクザク", item=CHICKEN),
        s(SEAT, "stare_tabby_wide_eyes_cat", "……", item=CHICKEN),
        s(SEAT, "sad_black_dog", "それは\nそれで\n胃もたれしそうだ", item=CHICKEN),
        s(SEAT, "calm_black_face_sheep", "肉があるから\n衣は輝く", item=CHICKEN),
        s(SEAT, "realize_wet_cat_stare", "衣と肉は\n名コンビだった", item=CHICKEN),
        # ---- デザート ----
        s(BUFFET, "work_typing_cat", "残り10分", item=DESSERT, bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(BUFFET, "stare_big_eyes_tabby_kitten", "デザートコーナー", item=DESSERT),
        s(BUFFET, "think_chin_paw_orange_cat", "入らない", item=DESSERT),
        s(BUFFET, "eat_crunchy_cat_luna", "でも\n甘いものは\n別の胃袋", item=DESSERT),
        s(SEAT, "eat_pop_cat", "ペロリ", item=DESSERT),
        s(SEAT, "happy_hamster_open_arms", "冷たくて\n生き返る", item=DESSERT),
        s(SEAT, "sleepy_sleepy_cat", "しあわせな\n満腹", item=DESSERT),
        s(SEAT, "work_typing_cat", "タイマーが鳴る", se="pi"),
        s(SEAT, "showoff_gojo_cosplay_cat", "80分\n完走", se="gong_dora_jaan"),
        s(SEAT, "money_counting_orange_cat", "最終結果\nチキン8ピース\nビスケット3個\nカレー1皿", item=BONES),
        s(SEAT, "rizz_cat_rizz", "元は\nたしかに取れた", item=BONES),
        s(SEAT, "sad_looking_away_tabby", "胃袋の元は\n取れていない", item=BONES),
        # ---- 帰り ----
        s(FRONT, "leave_cat_leaves_home", "店を出る", se="whoosh_shu", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(FRONT, "peek_what_happen_cat", "おじさんの看板が\n見送ってくれる"),
        s(FRONT, "stare_big_eyes_tabby_kitten", "来たときより\n笑顔に見える"),
        s(FRONT, "calm_black_face_sheep", "完敗だ"),
        s(STREET, "drive_driving_cat", "帰り道"),
        s(STREET, "sleepy_old_memories_cat", "服から\nスパイスのにおい"),
        s(STREET, "think_chin_paw_orange_cat", "12種類目の\nスパイスは\n空腹だった"),
        s(STREET, "smug_squint_bicolor_cat", "もう\nどこにもない"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nベッドに倒れこむ", se="whoosh_shu"),
        s(ROOM_N, "sleepy_sleepy_cat", "今日は\nもう\n何も食べない"),
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "夜10時", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(ROOM_N, "scream_phone_orange_cat", "スマホに\nケンタッキーの\nクーポン", se="pi"),
        s(ROOM_N, "think_chin_paw_orange_cat", "……"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "あの衣"),
        s(ROOM_N, "angry_aiming_cat", "もう\n食べたくなっている"),
        s(ROOM_N, "realize_wet_cat_stare", "放題ストの胃袋は\nすぐ忘れる"),
        s(ROOM_N, "work_typing_cat", "今日の反省を\nメモする"),
        s(ROOM_N, "read_book_orange_kitten", "1\nビスケットは\n最後に"),
        s(ROOM_N, "read_book_orange_kitten", "2\nポテトは\n最初に"),
        s(ROOM_N, "read_book_orange_kitten", "3\nサイは\n揚げたてを待て"),
        s(ROOM_N, "smug_squint_bicolor_cat", "次の放題ストへの\n申し送りだ"),
        s(ROOM_N, "rizz_cat_rizz", "ケンタッキーさん"),
        s(ROOM_N, "excited_hodomoe_city_cat", "いつか\n衣だけの食べ放題を\nお願いします", se="pikon", dur=3.8),
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_21_kfc.mp4"), os.path.join(J.HERE, "out", "jidaraku_21_kfc_preview"))
