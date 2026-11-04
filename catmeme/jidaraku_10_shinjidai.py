"""自堕落シリーズ #10：30代独身男、ひとりで新時代（11/4 ユーザー指定の流れ・鳥貴族と同じ作り）。約8分。

python3 catmeme/jidaraku_10_shinjidai.py → out/jidaraku_10_shinjidai.mp4
- 流れ（ユーザー指定）：安く飲み食いできる店で知られる → にぎやかな店だが実は1人飲みにやさしい（カウンター席がある店舗が多い）→
  最初は生ビールでもいいがメガジョッキも（種類が多くてコスパがいい）→ 名物の伝串（外はパリパリ・中はモチモチ・何本でも飽きない・すぐ来る・
  困るのはドリンクがすぐなくなること）→ メガジョッキ出陣 → カニカニランド（ふざけた名前だが油断するな・紛れもなくカニ・
  カリッと揚がった小さなカニが皿に群生・大ジョッキ片手にこの遊園地で遊べるのは新時代くらい）
- 口コミ・店の案内（2026年ごろ）：伝串は「揚げ皮串の発祥」・特許庁に認められた商品とうたう／高麗人参を使ったタレに、テーブルのスパイスをかける店舗も／
  焼きそば・ポテトサラダ・鶏旨タレユッケも好評／手ごろな値段・学生も多い／1人でも入りやすいという声。値段の数字は出さない
- ベンチマーク3チャンネルに新時代の回はない（11/4 確認）
- 写真がない料理は字幕だけ（写真が届いたら backgrounds/jidaraku/10_shinjidai に置く）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "10_shinjidai"))
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku", d) for d in ("04_sushiro", "05_gokurakuyu", "06_bronco", "07_ikea", "08_torikizoku")]
OFFICE, FRONT, IN, COUNTER, ROAD, ROOM_N = ("bg25_office_desk", "n01_front", "n02_inside", "n03_counter", "b06_road_night", "j07_room_night")
J.STANDIN.update({FRONT: "bg51_night_street", IN: "bg98_izakaya_night", COUNTER: "bg13_izakaya"})
NIGHT = {OFFICE: 0.85}
J.HOLD = 3   # 11/4：1つの素材を2〜3文つづけて使う
J.SUB_STYLE = "glow"   # 11/4 ユーザー指定：黒い文字＋淡い黄緑の光
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
NAMA, MEGA, DEN, KANI, YAKISOBA, POTESARA, YUKKE = (
    "f_nama", "f_mega", "f_denkushi", "f_kanikani", "f_yakisoba", "f_potesara", "f_yukke")


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 仕事帰り ----
        s(OFFICE, "work_typing_cat", "水曜日の夜8時", bgm={"file": LOFI, "gain": -12}),
        s(OFFICE, "blank_black_cat_zoning_out", "週のまん中\nいちばん疲れる日だ"),
        s(OFFICE, "think_chin_paw_orange_cat", "月曜は鳥貴族で\nがんばった"),
        s(OFFICE, "sad_looking_away_tabby", "でもその元気は\nもう使いきった"),
        s(OFFICE, "stare_tabby_wide_eyes_cat", "今日も\n飲んで帰りたい"),
        s(OFFICE, "sleepy_old_memories_cat", "できれば安くて\nうまい店がいい"),
        s(OFFICE, "sad_black_dog", "給料日まで\nあと10日"),
        s(OFFICE, "money_counting_orange_cat", "財布の中身は\n千円札が数枚"),
        s(OFFICE, "think_bike_front_seat_cat", "でも\n飲みたい"),
        s(OFFICE, "angry_aiming_cat", "安くて\nうまくて\nひとりで入れる店"),
        s(OFFICE, "excited_hodomoe_city_cat", "……あそこだ", se="shine_kiraan_maou"),
        # ---- 来店 ----
        s(FRONT, "leave_cat_leaves_home", "駅前の\n大きな看板", se="whoosh_shu", bgm={"file": L.PURPLE, "gain": -12, "fade": 0.8}),
        s(FRONT, "showoff_gojo_cosplay_cat", "新時代", se="gong_dora_jaan"),
        s(FRONT, "stare_big_eyes_tabby_kitten", "店の名前が\nもう強い"),
        s(FRONT, "huh_huh_cat", "新しい時代を\n作る気でいる"),
        s(FRONT, "calm_black_face_sheep", "俺の時代は\nまだ来ていない"),
        s(FRONT, "read_book_orange_kitten", "ここも\n安く飲み食いできる店で\n知られている"),
        s(FRONT, "peek_what_happen_cat", "店の中から\nにぎやかな声"),
        s(FRONT, "stare_interviewer_cat", "大学生のグループ\n会社の飲み会"),
        s(FRONT, "sad_black_dog", "ひとりで入るには\n勇気がいる"),
        s(FRONT, "stare_lying_tabby_cat", "入口の前で\n3往復する"),
        s(FRONT, "ignore_orange_cat_sniffed", "通りがかりの人に\n見られている気がする"),
        s(FRONT, "rizz_cat_rizz", "だが\n俺は知っている"),
        s(FRONT, "shady_dancing_man", "ここは意外と\n1人飲みにもやさしい店\nなのだ"),
        s(IN, "stare_interviewer_cat", "いらっしゃいませー！\nおひとりさまですかー！", se="pinpon_notice"),
        s(IN, "surprise_big_pupils_cat", "元気がいい"),
        s(IN, "happy_chipi_chapa_cat", "店員さんの声で\nこっちまで\n元気になる"),
        s(IN, "think_bike_front_seat_cat", "カウンターのお席\nどうぞー！"),
        s(IN, "stare_big_eyes_tabby_kitten", "カウンター席が\nあるのか"),
        s(IN, "joy_happy_happy_happy_cat", "助かった"),
        s(COUNTER, "think_bike_front_seat_cat", "この新時代"),
        s(COUNTER, "read_book_orange_kitten", "なんと\n1人飲みがしやすい\nカウンター席がある店舗が多い"),
        s(COUNTER, "calmdown_dancing_cat", "にぎやかな店の中に\n1人用の\n安全地帯"),
        s(COUNTER, "happy_hamster_open_arms", "ここは\n独身のシェルターだ"),
        s(COUNTER, "think_bike_front_seat_cat", "うしろの席では\n大学生が\nゲームをしている"),
        s(COUNTER, "stare_tabby_wide_eyes_cat", "負けた人が\n一気飲み"),
        s(COUNTER, "calm_black_face_sheep", "俺の前では\n平和な時間が\n流れている"),
        s(COUNTER, "stare_lying_tabby_cat", "となりも\nひとり客"),
        s(COUNTER, "meow_gray_white_kitten", "無言でうなずき合う"),
        s(COUNTER, "think_chin_paw_orange_cat", "ひとり客は\nみんな同じ顔をしている"),
        s(COUNTER, "sleepy_old_memories_cat", "がんばった1日の\n顔だ"),
        s(COUNTER, "happy_hamster_open_arms", "今日はここが\n俺たちの家だ"),
        # ---- ドリンク ----
        s(COUNTER, "work_typing_cat", "タッチパネルを開く"),
        s(COUNTER, "read_book_orange_kitten", "メニューの写真が\nどれもでかい"),
        s(COUNTER, "huh_goat_talks_to_huh_cat", "名前が\nどれも独特だ"),
        s(COUNTER, "stare_tabby_wide_eyes_cat", "メニューを読むだけで\n楽しい"),
        s(COUNTER, "think_chin_paw_orange_cat", "ドリンクは\n最初は生ビールでも\nいいが", item=NAMA),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "メガジョッキという\n選択肢もある", item=MEGA, se="pikon"),
        s(COUNTER, "read_book_orange_kitten", "ここはメガジョッキの\n種類が豊富で", item=MEGA),
        s(COUNTER, "money_counting_orange_cat", "コスパもいいのだ", item=MEGA),
        s(COUNTER, "think_chin_paw_orange_cat", "ふつうのジョッキの\n約2杯分", item=MEGA),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "おかわりを頼む回数が\n半分になる", item=MEGA),
        s(COUNTER, "happy_chipi_chapa_cat", "店員さんを呼ぶのが\n苦手な人にもやさしい", item=MEGA),
        s(COUNTER, "confused_i_dont_know_cat", "ハイボール\nレモンサワー\nウーロンハイ", item=MEGA),
        s(COUNTER, "huh_huh_cat", "全部\nメガ", item=MEGA),
        s(COUNTER, "angry_aiming_cat", "……まずは\n生ビールで\n様子を見る", item=NAMA),
        s(COUNTER, "eat_crunchy_cat_luna", "ゴクッ……\nくぅ〜！", item=NAMA, se="drink_gulp_gokugoku_thirsty_chug"),
        s(COUNTER, "happy_girlfriend_dance_cat", "水曜日の疲れに\n泡がしみる", item=NAMA),
        s(COUNTER, "sleepy_sleepy_cat", "上司の\nもうちょっとがんばろうか\nが溶けていく", item=NAMA),
        s(COUNTER, "dance_white_dog", "明日のことは\n明日の俺にまかせる", item=NAMA),
        # ---- 伝串 ----
        s(COUNTER, "showoff_gojo_cosplay_cat", "ここの名物といえば\nやはり"),
        s(COUNTER, "excited_hodomoe_city_cat", "伝串", item=DEN, se="explosion_dokaan"),
        s(COUNTER, "read_book_orange_kitten", "揚げ皮串の\n発祥の店だと\nうたっている", item=DEN),
        s(COUNTER, "surprise_big_pupils_cat", "特許庁にも\n認められた串らしい", item=DEN),
        s(COUNTER, "huh_goat_talks_to_huh_cat", "串が\n特許!?", item=DEN, se="question_mark_pop_confused_huh"),
        s(COUNTER, "stare_interviewer_cat", "しかも頼んでから\nすぐ来る", item=DEN, se="pinpon_notice"),
        s(COUNTER, "happy_chipi_chapa_cat", "意外と\nポイントが高い", item=DEN),
        s(COUNTER, "think_chin_paw_orange_cat", "テーブルのスパイスを\nふりかける", item=DEN),
        s(COUNTER, "eat_crunchy_cat_luna", "パリッ", item=DEN, se="pikon"),
        s(COUNTER, "surprise_big_pupils_cat", "外はパリパリ", item=DEN),
        s(COUNTER, "eat_pop_cat", "中はモチモチ", item=DEN),
        s(COUNTER, "realize_wet_cat_stare", "鶏皮って\nこんなにモチモチだったか", item=DEN),
        s(COUNTER, "sleepy_old_memories_cat", "子どものころ\n鶏皮が苦手だった", item=DEN),
        s(COUNTER, "sad_banana_cat_cry", "あのころの俺に\n食べさせたい", item=DEN),
        s(COUNTER, "happy_hamster_open_arms", "鶏皮なのに\n食感が2つある", item=DEN),
        s(COUNTER, "realize_wet_cat_stare", "甘めのタレに\nスパイスのピリッ", item=DEN),
        s(COUNTER, "eat_crunchy_cat_luna", "2本目", item=DEN),
        s(COUNTER, "eat_pop_cat", "3本目", item=DEN),
        s(COUNTER, "dance_wop_cat", "4本目", item=DEN),
        s(COUNTER, "rizz_cat_rizz", "何本食べても\n飽きることはない", item=DEN),
        s(COUNTER, "weird_meowing_cat", "鶏皮は\n脂の宝石だ", item=DEN),
        s(COUNTER, "talk_orange_white_sitting_cat", "健康診断の\n結果のことは\n今は考えない", item=DEN),
        s(COUNTER, "snore_snoring_dog", "コレステロールという\n言葉を\n忘れることにした", item=DEN),
        s(COUNTER, "stare_tabby_wide_eyes_cat", "コイツを食べて\n困るのは", item=DEN),
        s(COUNTER, "sad_looking_away_tabby", "ドリンクが\nすぐなくなることくらいだ", item=NAMA),
        s(COUNTER, "despair_dramatic_kitten", "生ビールが\nもう空", item=NAMA, se="pi"),
        s(COUNTER, "huh_huh_cat", "いつ飲んだ？", item=NAMA),
        s(COUNTER, "blank_black_cat_zoning_out", "伝串を食べるたびに\n手が勝手に\nジョッキへのびていた", item=NAMA),
        # ---- メガジョッキ ----
        s(COUNTER, "angry_shooting_cat", "メガジョッキ", item=MEGA),
        s(COUNTER, "yell_orange_fat_cat", "出陣", item=MEGA, se="gong_match_start"),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "来た\n両手で持つ重さ", item=MEGA),
        s(COUNTER, "scream_standing_marmot", "顔より\nでかい", item=MEGA),
        s(COUNTER, "eat_crunchy_cat_luna", "ゴクゴクゴク……", item=MEGA, se="drink_gulp_gokugoku_thirsty_chug"),
        s(COUNTER, "happy_girlfriend_dance_cat", "伝串の脂を\nハイボールが\n流していく", item=MEGA),
        s(COUNTER, "calm_black_face_sheep", "これで\n伝串があと10本\nいける", item=MEGA),
        s(COUNTER, "peek_what_happen_cat", "となりの大学生も\nメガジョッキ", item=MEGA),
        s(COUNTER, "stare_interviewer_cat", "かんぱーい！", item=MEGA),
        s(COUNTER, "meow_ragdoll_chubby_cat", "俺も小さく\nかんぱい", item=MEGA),
        s(COUNTER, "laugh_laughing_dog", "誰にも\n聞こえていない", item=MEGA),
        s(COUNTER, "work_typing_cat", "伝串を\nおかわり", item=DEN, se="pi"),
        s(COUNTER, "stare_interviewer_cat", "お待たせしましたー！", item=DEN),
        s(COUNTER, "surprise_big_pupils_cat", "はやい", item=DEN),
        s(COUNTER, "eat_crunchy_cat_luna", "パリッ\nモチッ", item=DEN),
        s(COUNTER, "happy_girlfriend_dance_cat", "この2つの食感の\n往復が\nたまらない", item=DEN),
        s(COUNTER, "rizz_cat_rizz", "伝串と\nメガジョッキの\n無限ループに入る", item=DEN),
        # ---- サイドメニュー ----
        s(COUNTER, "think_bike_front_seat_cat", "口コミで評判の\nほかのメニューも\n頼んでみる"),
        s(COUNTER, "work_typing_cat", "ポテトサラダ", item=POTESARA, se="pikon"),
        s(COUNTER, "eat_pop_cat", "居酒屋のポテサラは\nなぜこんなに\nうまいのか", item=POTESARA),
        s(COUNTER, "talk_orange_white_sitting_cat", "家で作ると\nこうならない", item=POTESARA),
        s(COUNTER, "think_chin_paw_orange_cat", "マヨネーズの量が\n家とはちがうのだろう", item=POTESARA),
        s(COUNTER, "calm_black_face_sheep", "知らないほうが\n幸せなこともある", item=POTESARA),
        s(COUNTER, "surprise_big_pupils_cat", "鶏旨タレユッケ", item=YUKKE, se="pikon"),
        s(COUNTER, "happy_chipi_chapa_cat", "卵黄をくずして\nからめる", item=YUKKE),
        s(COUNTER, "yell_orange_fat_cat", "メガジョッキが\n減る減る", item=MEGA),
        s(COUNTER, "think_chin_paw_orange_cat", "ほかにも\nメニューがたくさんある"),
        s(COUNTER, "confused_i_dont_know_cat", "唐揚げ\nだし巻き\nもつ煮"),
        s(COUNTER, "despair_dramatic_kitten", "胃袋が\nひとつしかないのが\nくやしい"),
        s(COUNTER, "rizz_cat_rizz", "今日の主役は\n伝串とカニだ"),
        # ---- カニカニランド ----
        s(COUNTER, "sleepy_old_memories_cat", "俺が好きなメニューは\nもうひとつある", bgm={"file": PASTEL, "gain": -15, "fade": 0.8}),
        s(COUNTER, "excited_hodomoe_city_cat", "それがこの", se="pi"),
        s(COUNTER, "surprise_big_pupils_cat", "カニカニランド", item=KANI, se="explosion_dokaan"),
        s(COUNTER, "huh_huh_cat", "ふざけた名前だ", item=KANI),
        s(COUNTER, "glare_disgusted_cat", "だが\n油断するな", item=KANI),
        s(COUNTER, "angry_aiming_cat", "コイツは\nまぎれもなく\nカニだ", item=KANI, se="explosion_chudoon"),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "カリッと揚げられた\n小さなカニが", item=KANI),
        s(COUNTER, "stare_tabby_wide_eyes_cat", "皿の上に\n群生している", item=KANI),
        s(COUNTER, "huh_huh_cat", "1匹\n2匹\n3匹……", item=KANI),
        s(COUNTER, "despair_dramatic_kitten", "数えきれない", item=KANI),
        s(COUNTER, "sleepy_old_memories_cat", "子どものころ\n海でカニを\n追いかけていた", item=KANI),
        s(COUNTER, "rizz_cat_rizz", "今は\n食べる側だ", item=KANI),
        s(COUNTER, "dance_three_kittens", "まさに\nカニカニランド", item=KANI),
        s(COUNTER, "eat_crunchy_cat_luna", "ひとつつまんで\nまるごと", item=KANI),
        s(COUNTER, "happy_hamster_open_arms", "バリッ\n香ばしい", item=KANI),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "塩気が\nちょうどいい", item=KANI),
        s(COUNTER, "cocky_dj_cat", "これは\nメガジョッキを\n呼ぶ味だ", item=KANI),
        s(COUNTER, "yell_orange_fat_cat", "メガジョッキ\nおかわり", item=MEGA),
        s(COUNTER, "realize_wet_cat_stare", "殻ごと食べられる\nカニのせんべいだ", item=KANI),
        s(COUNTER, "cocky_dj_cat", "大ジョッキ片手に", item=MEGA),
        s(COUNTER, "dance_happy_banana_cat", "この遊園地で\n遊べるのは", item=KANI),
        s(COUNTER, "rizz_cat_rizz", "新時代くらいだろう", item=KANI, se="shine_kiraan_maou"),
        s(COUNTER, "sleepy_sleepy_cat", "入場料は\n伝串1本分くらい", item=KANI),
        s(COUNTER, "calm_black_face_sheep", "ジェットコースターはないが\nカニはいる", item=KANI),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "カニの顔と\n目が合う", item=KANI),
        s(COUNTER, "sad_looking_away_tabby", "……ごめん", item=KANI),
        s(COUNTER, "eat_crunchy_cat_luna", "バリッ", item=KANI),
        s(COUNTER, "happy_chipi_chapa_cat", "うまい", item=KANI),
        s(COUNTER, "blank_black_cat_zoning_out", "罪悪感と\n香ばしさは\n両立する", item=KANI),
        # ---- しめ ----
        s(COUNTER, "think_chin_paw_orange_cat", "しめは\n焼きそば", item=YAKISOBA, se="pikon", bgm={"file": HIRU, "gain": -6, "fade": 0.8}),
        s(COUNTER, "read_book_orange_kitten", "口コミでも\n焼きそばがうまいという声が\n多い", item=YAKISOBA),
        s(COUNTER, "eat_pop_cat", "ソースの香り", item=YAKISOBA),
        s(COUNTER, "happy_girlfriend_dance_cat", "居酒屋の焼きそばは\n酒に合うように\nできている", item=YAKISOBA),
        s(COUNTER, "eat_crunchy_cat_luna", "伝串を\n焼きそばに\nのせてみる", item=YAKISOBA),
        s(COUNTER, "surprise_big_pupils_cat", "……うまい", item=YAKISOBA),
        s(COUNTER, "rizz_cat_rizz", "これが\n新時代の\n焼きそばだ", item=YAKISOBA),
        s(COUNTER, "glare_disgusted_cat", "だれにも\nおすすめはしない", item=YAKISOBA),
        s(COUNTER, "happy_chipi_chapa_cat", "でも\n俺は好きだ", item=YAKISOBA),
        s(COUNTER, "stare_interviewer_cat", "2杯目の\nメガジョッキ", item=MEGA),
        s(COUNTER, "eat_crunchy_cat_luna", "伝串", item=DEN),
        s(COUNTER, "happy_girlfriend_dance_cat", "メガ", item=MEGA),
        s(COUNTER, "eat_pop_cat", "カニ", item=KANI),
        s(COUNTER, "happy_girlfriend_dance_cat", "メガ", item=MEGA),
        s(COUNTER, "eat_crunchy_cat_luna", "伝串", item=DEN),
        s(COUNTER, "dance_maxwell_cat", "メガ", item=MEGA),
        s(COUNTER, "spin_spinning_cat", "頭が\nくるくるしてきた"),
        s(COUNTER, "stare_lying_tabby_cat", "カウンターに\nほおづえをつく"),
        s(COUNTER, "sleepy_old_memories_cat", "学生のころは\nこういう店で\n朝まで飲んでいた"),
        s(COUNTER, "realize_wet_cat_stare", "今は\n終電を気にしている"),
        s(COUNTER, "calm_black_face_sheep", "それも\n大人になったということだ"),
        # ---- 満腹・会計 ----
        s(COUNTER, "sulk_hungry_cat", "満腹だ", se="chiin_01",
          bgm={"file": os.path.join(L.BGM, "手紙のさよなら.mp3"), "gain": -14, "fade": 1.0}),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "目の前には\n伝串の串の山"),
        s(COUNTER, "huh_goat_talks_to_huh_cat", "串入れの筒が\nいっぱいだ"),
        s(COUNTER, "stare_lying_tabby_cat", "となりのひとり客の\n串入れも\nいっぱいだ"),
        s(COUNTER, "meow_gray_white_kitten", "また\nうなずき合う"),
        s(COUNTER, "blank_black_cat_zoning_out", "数えるのを\nやめた"),
        s(COUNTER, "think_bike_front_seat_cat", "まわりのテーブルは\nまだまだ盛り上がっている"),
        s(COUNTER, "happy_hamster_open_arms", "にぎやかな声を聞きながら\n1人で飲むのも\n悪くない"),
        s(IN, "money_counting_orange_cat", "お会計"),
        s(IN, "stare_interviewer_cat", "レジの横に\n伝串のポスター"),
        s(IN, "sad_looking_away_tabby", "最後まで\n誘惑してくる"),
        s(IN, "surprise_big_pupils_cat", "……安い", se="explosion_dokaan"),
        s(IN, "joy_happy_happy_happy_cat", "メガジョッキ2杯と\n伝串と\nカニの遊園地で"),
        s(IN, "rizz_cat_rizz", "この値段"),
        s(IN, "happy_hamster_open_arms", "財布の千円札が\nちゃんと残っている"),
        s(IN, "dance_cute_dog", "新時代\nありがとう"),
        s(IN, "stare_interviewer_cat", "ありがとうございましたー！"),
        # ---- 帰り道 ----
        s(ROAD, "leave_cat_leaves_home", "夜風が気持ちいい", se="whoosh_shu"),
        s(ROAD, "sleepy_old_memories_cat", "月曜は鳥貴族\n水曜は新時代"),
        s(ROAD, "think_chin_paw_orange_cat", "安い店のおかげで\n平日を生きのびている"),
        s(ROAD, "sleepy_sleepy_cat", "安い店は\n独身のライフライン"),
        s(ROAD, "happy_hamster_open_arms", "明日もなんとか\nがんばれそうだ"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nベッドに倒れこむ", se="whoosh_shu"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "服から\n伝串のにおい"),
        s(ROOM_N, "happy_hamster_open_arms", "いいにおいだ"),
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "まぶたの裏に\nカニが群生している"),
        s(ROOM_N, "think_chin_paw_orange_cat", "金曜日は\nどこに行こう"),
        s(ROOM_N, "despair_dramatic_kitten", "……いや\n給料日まであと10日だ"),
        s(ROOM_N, "sad_banana_cat_cry", "金曜日は\n家で自炊だ"),
        s(ROOM_N, "excited_hodomoe_city_cat", "また行こう\nカニカニランド", se="pikon", dur=3.8),
        J.end_card(),
    ]


def place(cs):
    J.auto_tempo(cs)
    for c in cs:
        if c.get("text"):
            c["text"] = c["text"].replace("「", "").replace("」", "")
        if c.get("bg") in NIGHT:
            c["dark"] = NIGHT[c["bg"]]
    return cs


if __name__ == "__main__":
    cs = place(cuts())
    if os.environ.get("LEN"):
        print(len(cs), round(sum(c["dur"] for c in cs), 1))
    else:
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_10_shinjidai.mp4"), os.path.join(J.HERE, "out", "jidaraku_10_shinjidai_preview"))
