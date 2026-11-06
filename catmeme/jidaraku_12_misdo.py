"""自堕落シリーズ #12：30代独身男、ミスドのドーナツビュッフェで60分食べ放題（11/6 ユーザー指定：候補9番・ビュッフェの話に変更）。約8分。

python3 catmeme/jidaraku_12_misdo.py → out/jidaraku_12_misdo.mp4
- 流れ：日曜の朝に甘いものが食べたい → スマホでドーナツビュッフェを見つける（イートイン限定・60分・対象のドーナツが食べ放題・
  対象のドリンクはおかわり自由・やっている店は一部・予約が必要な店も）→ 予約して来店 → トレーとトングで山盛り10個 →
  時間とたたかいながら1個ずつ食レポ（ポン・デ・リング／オールドファッション／エンゼルフレンチ／フレンチクルーラー／ゴールデンチョコレート）→
  5個目で限界 → 食べ放題は残さないのがルール → コーヒーのおかわりで最後まで → 残り1分で最後のポン・デ・リング → 帰り道・夜
- 店をけなさない。値段・カロリーの数字は出さない。ビュッフェの決まりは案内の画像に書いてあることだけ言う
- ベンチマーク3チャンネルにミスドの回はない（11/6 確認）
- 写真は backgrounds/jidaraku/12_misdo。ほかの店の写真は使わない（外観・ショーケース・席は届くまで仮のイラスト）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "12_misdo"))
ROOM, FRONT, CASE, SEAT, STREET, ROOM_N = ("j01_room", "m01_front", "m02_showcase", "m03_seat", "bg48_clean_street", "j07_room_night")
J.STANDIN.update({FRONT: "bg48_clean_street", CASE: "bg86_product_shelf", SEAT: "bg20_counter"})
# 仮の背景のある場所（ほかの店の写真は使わない。j01_room は自堕落シリーズの部屋）
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in (os.path.join("jidaraku", "01_yakiniku"), "03_kodomo_nisa", "14_japan", "16_tenchim")]
J.HOLD = 3
J.SUB_STYLE = "glow"
MORNING = os.path.join(L.BGM, "Morning.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
BUFFET, LINEUP = "f_buffet", "f_lineup"   # 11/6 ドーナツビュッフェの案内・ならんだドーナツのアップ
TRAY, PON, OLD, ANGEL, CRULLER, GOLDEN, COFFEE = ("f_tray", "f_ponde", "f_old", "f_angel", "f_cruller", "f_golden", "f_coffee")


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 日曜の朝 ----
        s(ROOM, "sleep_sleeping_cat", "日曜日の朝10時\n目が覚めた", bgm={"file": MORNING, "gain": -12}),
        s(ROOM, "blank_black_cat_zoning_out", "予定はない"),
        s(ROOM, "think_chin_paw_orange_cat", "なんだか\n甘いものが食べたい"),
        s(ROOM, "stare_big_eyes_tabby_kitten", "冷蔵庫を開ける"),
        s(ROOM, "calm_black_face_sheep", "マヨネーズと\n麦茶"),
        s(ROOM, "sad_looking_away_tabby", "甘いものは\nどこにもない"),
        s(ROOM, "sleepy_old_memories_cat", "子どものころ\n日曜日の朝は\nドーナツだった"),
        s(ROOM, "happy_chipi_chapa_cat", "母さんが\n箱で買ってきてくれた"),
        s(ROOM, "think_bike_front_seat_cat", "でも1人1個までと\n決まっていた"),
        s(ROOM, "sad_black_dog", "もっと食べたいと\n言えなかった"),
        s(ROOM, "scream_phone_orange_cat", "ベッドの上で\nスマホを見る"),
        s(ROOM, "stare_tabby_wide_eyes_cat", "ミスドの\nドーナツビュッフェ", item=BUFFET),
        s(ROOM, "surprise_big_pupils_cat", "対象のドーナツが\n食べ放題", item=BUFFET, se="explosion_chudoon"),
        s(ROOM, "read_book_orange_kitten", "時間は60分\nお店の中で食べる人だけ", item=BUFFET),
        s(ROOM, "happy_hamster_open_arms", "対象のドリンクは\nおかわり自由", item=BUFFET),
        s(ROOM, "think_chin_paw_orange_cat", "やっている店は\n一部だけ", item=BUFFET),
        s(ROOM, "work_typing_cat", "近くの店を\nさがす", item=BUFFET),
        s(ROOM, "joy_happy_happy_happy_cat", "駅前の店で\nやっていた", item=BUFFET),
        s(ROOM, "read_book_orange_kitten", "予約が必要な店も\nあるらしい", item=BUFFET),
        s(ROOM, "work_typing_cat", "念のため\n予約する", item=BUFFET, se="pi"),
        s(ROOM, "realize_wet_cat_stare", "あのころ\n1個までだった俺が", item=BUFFET),
        s(ROOM, "angry_aiming_cat", "60分\n食べ放題", item=BUFFET),
        s(ROOM, "excited_hodomoe_city_cat", "行くしかない", se="shine_kiraan_maou"),
        s(ROOM, "work_typing_cat", "パーカーをはおる"),
        s(ROOM, "stare_lying_tabby_cat", "顔は洗わない"),
        s(ROOM, "calm_black_face_sheep", "ドーナツは\n顔を見ない"),
        s(ROOM, "leave_cat_leaves_home", "家を出る", se="whoosh_shu"),
        s(STREET, "think_chin_paw_orange_cat", "日曜の朝の道は\n静かだ", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(STREET, "dance_three_kittens", "公園で\n子どもたちが\n走りまわっている"),
        s(STREET, "sleepy_old_memories_cat", "俺にも\nあんな時代があった"),
        s(STREET, "think_bike_front_seat_cat", "作戦を考える"),
        s(STREET, "read_book_orange_kitten", "朝ごはんは\n食べていない"),
        s(STREET, "smug_squint_bicolor_cat", "胃袋は\n空っぽだ"),
        s(STREET, "rizz_cat_rizz", "準備は\nととのった"),
        # ---- 来店 ----
        s(FRONT, "leave_cat_leaves_home", "駅前の\nミスタードーナツ", se="whoosh_shu"),
        s(FRONT, "surprise_big_pupils_cat", "あまい香りが\n外までただよっている"),
        s(FRONT, "happy_hamster_open_arms", "この香りだけで\nごはんが食べられる"),
        s(FRONT, "stare_interviewer_cat", "家族づれ\n学生さん\n近所のおばあちゃん"),
        s(FRONT, "rizz_cat_rizz", "ミスドは\nだれでも入れる店だ"),
        s(FRONT, "yell_orange_fat_cat", "入店", se="gong_match_start"),
        s(CASE, "stare_interviewer_cat", "いらっしゃいませー", se="pinpon_notice", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(CASE, "meow_ragdoll_chubby_cat", "予約した\nビュッフェで……"),
        s(CASE, "stare_interviewer_cat", "ドーナツビュッフェ\nですねー\n60分でーす"),
        s(CASE, "happy_chipi_chapa_cat", "ドリンクは\nおかわりできまーす"),
        s(CASE, "think_bike_front_seat_cat", "ホットコーヒーを\nたのむ", item=COFFEE),
        s(CASE, "cocky_dj_cat", "スマホで\nタイマーを\n60分", se="pi"),
        s(CASE, "angry_shooting_cat", "スタート", se="gong_match_start"),
        # ---- ショーケース ----
        s(CASE, "stare_big_eyes_tabby_kitten", "目の前に\nずらりとならぶ\nドーナツ", item=LINEUP),
        s(CASE, "showoff_gojo_cosplay_cat", "ドーナツの宝石箱だ", se="gong_dora_jaan", item=LINEUP),
        s(CASE, "huh_huh_cat", "パイ\nマフィン\n季節のドーナツ", item=LINEUP),
        s(CASE, "think_chin_paw_orange_cat", "対象のドーナツは\n店ごとにちがう\nらしい", item=LINEUP),
        s(CASE, "stare_lying_tabby_cat", "まずは\n1周して\n全部見る", item=LINEUP),
        s(CASE, "stare_tabby_wide_eyes_cat", "残り58分", se="pi"),
        s(CASE, "read_book_orange_kitten", "トレーとトングを\n持って\n自分で選ぶ"),
        s(CASE, "think_chin_paw_orange_cat", "トングを\nカチカチ\n2回鳴らす", se="pi"),
        s(CASE, "smug_squint_bicolor_cat", "準備はできた"),
        s(CASE, "confused_i_dont_know_cat", "選べない", item=LINEUP),
        s(CASE, "despair_dramatic_kitten", "全部ほしい", se="pi", item=LINEUP),
        s(CASE, "think_bike_front_seat_cat", "落ち着け\n時間は\nかぎられている"),
        s(CASE, "read_book_orange_kitten", "まずは\n定番から攻める"),
        s(CASE, "work_typing_cat", "ポン・デ・リング", item=PON),
        s(CASE, "eat_pop_cat", "のせる", item=PON),
        s(CASE, "stare_big_eyes_tabby_kitten", "オールドファッション", item=OLD),
        s(CASE, "happy_chipi_chapa_cat", "のせる", item=OLD),
        s(CASE, "surprise_big_pupils_cat", "エンゼルフレンチ", item=ANGEL),
        s(CASE, "joy_happy_happy_happy_cat", "のせる", item=ANGEL),
        s(CASE, "think_chin_paw_orange_cat", "フレンチクルーラー", item=CRULLER),
        s(CASE, "dance_wop_cat", "のせる", item=CRULLER),
        s(CASE, "stare_tabby_wide_eyes_cat", "ゴールデンチョコレート", item=GOLDEN),
        s(CASE, "dance_happy_banana_cat", "のせる", item=GOLDEN),
        s(CASE, "huh_goat_talks_to_huh_cat", "となりのやつも\nそのとなりも", item=TRAY),
        s(CASE, "dance_edm_cat", "のせる\nのせる\nのせる", item=TRAY),
        s(CASE, "stare_big_eyes_tabby_kitten", "トレーを見る", item=TRAY),
        s(CASE, "scream_standing_marmot", "10個", item=TRAY, se="explosion_chudoon"),
        s(CASE, "calm_black_face_sheep", "トレーが\n見えない", item=TRAY),
        s(CASE, "peek_what_happen_cat", "となりのお母さんが\n子どもに言っている", item=TRAY),
        s(CASE, "stare_interviewer_cat", "食べられる分だけ\nとろうねー", item=TRAY),
        s(CASE, "sad_black_dog", "俺に\n言われた気がする", item=TRAY),
        s(CASE, "rizz_cat_rizz", "大丈夫だ\n朝ごはんを\nぬいてきた", item=TRAY),
        # ---- 1個目 ポン・デ・リング ----
        s(SEAT, "work_typing_cat", "窓ぎわの席を\n確保"),
        s(SEAT, "stare_tabby_wide_eyes_cat", "残り55分", se="pi"),
        s(SEAT, "calmdown_dancing_cat", "まずは\nポン・デ・リング", item=PON),
        s(SEAT, "read_book_orange_kitten", "1個ずつ\nちぎって食べる派だ", item=PON),
        s(SEAT, "eat_pop_cat", "ちぎっ", item=PON, se="pikon"),
        s(SEAT, "eat_crunchy_cat_luna", "もちっ", item=PON),
        s(SEAT, "surprise_big_pupils_cat", "もちもちが\n口の中ではねる", item=PON),
        s(SEAT, "sleepy_old_memories_cat", "子どものころの\n日曜日の味だ", item=PON),
        s(SEAT, "sad_banana_cat_cry", "母さん\n元気かな", item=PON),
        s(SEAT, "think_chin_paw_orange_cat", "ドーナツの穴は\nなぜあいているのか", item=PON),
        s(SEAT, "read_book_orange_kitten", "まんなかまで\nむらなく\n火を通すためらしい", item=PON),
        s(SEAT, "realize_wet_cat_stare", "俺の休日の\nぽっかりあいた時間にも\nきっと意味がある", item=PON),
        s(SEAT, "calm_black_face_sheep", "たぶん", item=PON),
        s(SEAT, "happy_hamster_open_arms", "1個目\n完食", item=PON),
        # ---- 2個目 オールドファッション ----
        s(SEAT, "stare_tabby_wide_eyes_cat", "残り48分\n2個目\nオールドファッション", item=OLD),
        s(SEAT, "read_book_orange_kitten", "外はザクザク\n中はしっとり", item=OLD),
        s(SEAT, "eat_crunchy_cat_luna", "ザクッ", item=OLD, se="pikon"),
        s(SEAT, "realize_wet_cat_stare", "まわりのザクザクが\nいちばんうまい", item=OLD),
        s(SEAT, "think_chin_paw_orange_cat", "ここで\nコーヒーをひと口", item=COFFEE),
        s(SEAT, "eat_crunchy_cat_luna", "ズズッ", item=COFFEE, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "cocky_dj_cat", "オールドファッションと\nコーヒーは\n名コンビだ", item=OLD),
        s(SEAT, "joy_happy_happy_happy_cat", "2個目\n完食", item=OLD),
        # ---- 3個目 エンゼルフレンチ ----
        s(SEAT, "surprise_big_pupils_cat", "残り42分\n3個目\nエンゼルフレンチ", item=ANGEL),
        s(SEAT, "stare_big_eyes_tabby_kitten", "半分チョコで\n中にクリーム", item=ANGEL),
        s(SEAT, "angry_aiming_cat", "いくぞ", item=ANGEL),
        s(SEAT, "eat_crunchy_cat_luna", "ガブッ", item=ANGEL, se="explosion_chudoon"),
        s(SEAT, "scream_standing_marmot", "クリームが\nうしろから\nはみ出した", item=ANGEL),
        s(SEAT, "despair_dramatic_kitten", "口のまわりが\nクリームまみれ", item=ANGEL),
        s(SEAT, "peek_what_happen_cat", "となりの子どもも\n同じ顔をしている", item=ANGEL),
        s(SEAT, "happy_chipi_chapa_cat", "仲間だ", item=ANGEL),
        s(SEAT, "sleepy_sleepy_cat", "天使が\n口の中で\nとけていく", item=ANGEL),
        s(SEAT, "happy_hamster_open_arms", "3個目\n完食", item=ANGEL),
        # ---- 4個目 フレンチクルーラー ----
        s(SEAT, "think_bike_front_seat_cat", "残り37分\n4個目\nフレンチクルーラー", item=CRULLER),
        s(SEAT, "read_book_orange_kitten", "ふんわりかるい\nうねうねのドーナツ", item=CRULLER),
        s(SEAT, "eat_pop_cat", "ふわっ", item=CRULLER, se="pikon"),
        s(SEAT, "surprise_big_pupils_cat", "消えた", item=CRULLER),
        s(SEAT, "huh_huh_cat", "いま\n食べたよな？", item=CRULLER, se="question_mark_pop_confused_huh"),
        s(SEAT, "smug_squint_bicolor_cat", "かるすぎて\n0個だ", item=CRULLER),
        s(SEAT, "dance_wop_cat", "食べ放題には\nありがたい", item=CRULLER),
        # ---- 5個目 ゴールデンチョコレート ----
        s(SEAT, "stare_tabby_wide_eyes_cat", "残り31分\n5個目\nゴールデンチョコレート", item=GOLDEN),
        s(SEAT, "think_chin_paw_orange_cat", "黄色いツブツブが\nびっしり", item=GOLDEN),
        s(SEAT, "eat_crunchy_cat_luna", "ザクザク", item=GOLDEN, se="pikon"),
        s(SEAT, "sad_looking_away_tabby", "テーブルが\nツブツブだらけ", item=GOLDEN),
        s(SEAT, "meow_ragdoll_chubby_cat", "1粒ずつ\nひろって食べる", item=GOLDEN),
        s(SEAT, "realize_wet_cat_stare", "さっきより\n手がおそい", item=GOLDEN),
        s(SEAT, "sleepy_old_memories_cat", "口の中が\nずっと甘い", item=GOLDEN),
        s(SEAT, "despair_dramatic_kitten", "おなかが\n重い", item=GOLDEN, se="pi"),
        s(SEAT, "blank_black_cat_zoning_out", "5個目で\n手が止まった", item=GOLDEN),
        # ---- 限界 ----
        s(SEAT, "stare_big_eyes_tabby_kitten", "トレーを見る", item=TRAY),
        s(SEAT, "scream_standing_marmot", "まだ\n5個ある", item=TRAY, se="explosion_chudoon"),
        s(SEAT, "stare_tabby_wide_eyes_cat", "残り25分", se="pi"),
        s(SEAT, "sad_black_dog", "食べられる分だけ\nとろうねー", item=TRAY),
        s(SEAT, "despair_dramatic_kitten", "あのお母さんの声が\n頭の中でひびく", item=TRAY),
        s(SEAT, "think_chin_paw_orange_cat", "とったものは\n残さない\nそれが食べ放題の\nマナーだ", item=TRAY),
        s(SEAT, "angry_aiming_cat", "やるしかない", item=TRAY, se="gong_match_start"),
        s(SEAT, "work_typing_cat", "コーヒーを\nおかわり", item=COFFEE, se="pinpon_notice"),
        s(SEAT, "eat_crunchy_cat_luna", "ズズッ", item=COFFEE, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "happy_hamster_open_arms", "苦さが\n口の中を\nもとにもどす", item=COFFEE),
        s(SEAT, "eat_pop_cat", "6個目", item=TRAY),
        s(SEAT, "think_chin_paw_orange_cat", "味を変える作戦", item=TRAY),
        s(SEAT, "read_book_orange_kitten", "甘いのの次は\nシンプルなやつ", item=TRAY),
        s(SEAT, "smug_squint_bicolor_cat", "これで\n舌がリセットされる", item=TRAY),
        s(SEAT, "calm_black_face_sheep", "されない", item=TRAY),
        s(SEAT, "eat_crunchy_cat_luna", "7個目", item=TRAY),
        s(SEAT, "stare_tabby_wide_eyes_cat", "残り15分", se="pi"),
        s(SEAT, "work_typing_cat", "コーヒー\n3杯目", item=COFFEE),
        s(SEAT, "peek_what_happen_cat", "店の中を見わたす", item=COFFEE),
        s(SEAT, "stare_interviewer_cat", "勉強している学生さん", item=COFFEE),
        s(SEAT, "sleepy_old_memories_cat", "新聞を読む\nおじいちゃん", item=COFFEE),
        s(SEAT, "happy_chipi_chapa_cat", "ドーナツを分けあう\nカップル", item=COFFEE),
        s(SEAT, "calm_black_face_sheep", "タイマーと\nにらめっこの俺", item=TRAY),
        s(SEAT, "rizz_cat_rizz", "みんな\nそれぞれの日曜日だ", item=TRAY),
        s(SEAT, "sleepy_sleepy_cat", "8個目", item=TRAY),
        s(SEAT, "despair_dramatic_kitten", "9個目", item=TRAY),
        s(SEAT, "stare_lying_tabby_cat", "窓の外を\nぼんやりながめる", item=COFFEE),
        s(SEAT, "dance_three_kittens", "家族づれが\n箱を持って\n帰っていく", item=COFFEE),
        s(SEAT, "sleepy_old_memories_cat", "母さんも\nあんなふうに\n箱を持って\n帰ってきてくれた", item=COFFEE),
        s(SEAT, "stare_tabby_wide_eyes_cat", "残り5分", se="pi"),
        s(SEAT, "despair_dramatic_kitten", "手がふるえる", item=TRAY),
        s(SEAT, "sad_black_dog", "でも\nあと1個", item=TRAY),
        s(SEAT, "angry_shooting_cat", "コーヒーを\n一気に飲む", item=COFFEE, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "yell_orange_fat_cat", "最後の力を\nふりしぼる", item=TRAY),
        s(SEAT, "stare_tabby_wide_eyes_cat", "残り1分", se="explosion_chudoon"),
        s(SEAT, "stare_big_eyes_tabby_kitten", "最後の1個", item=PON),
        s(SEAT, "surprise_big_pupils_cat", "ポン・デ・リングを\n2個とっていた", item=PON),
        s(SEAT, "eat_pop_cat", "ちぎっ\nもちっ", item=PON),
        s(SEAT, "realize_wet_cat_stare", "いろいろ食べたけど", item=PON),
        s(SEAT, "happy_girlfriend_dance_cat", "結局\nここに帰ってくる", item=PON),
        s(SEAT, "cocky_dj_cat", "ピピピピ", se="pi"),
        s(SEAT, "showoff_gojo_cosplay_cat", "60分\n10個\n完食", item=TRAY, se="gong_dora_jaan"),
        s(SEAT, "sad_banana_cat_cry", "1個までだった\nあのころの俺\n見てるか", item=TRAY),
        # ---- 帰り道 ----
        s(STREET, "leave_cat_leaves_home", "おなかを抱えて\n店を出る", se="whoosh_shu", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(STREET, "think_bike_front_seat_cat", "公園のベンチに座る"),
        s(STREET, "sleepy_sleepy_cat", "おなかが\n重くて\n動けない"),
        s(STREET, "calm_black_face_sheep", "鳩が\nこっちを見ている"),
        s(STREET, "laugh_laughing_dog", "何も持っていないぞ"),
        s(STREET, "work_typing_cat", "母さんにLINEする"),
        s(STREET, "scream_phone_orange_cat", "ミスドの\n食べ放題\n行ってきた"),
        s(STREET, "stare_big_eyes_tabby_kitten", "すぐに返事が来た"),
        s(STREET, "happy_chipi_chapa_cat", "いいね\nポン・デ・リング\n食べた？"),
        s(STREET, "joy_happy_happy_happy_cat", "最初と最後に\n食べた"),
        s(STREET, "happy_hamster_open_arms", "母さんも\nポン・デ・リング派だった"),
        s(STREET, "sleepy_old_memories_cat", "今度の休みは\n実家に\n箱で持って帰ろう"),
        s(STREET, "think_chin_paw_orange_cat", "1人1個までじゃなく\n好きなだけ"),
        # ---- 夜 ----
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\n昼寝", se="whoosh_shu"),
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "夜8時\n目が覚めた"),
        s(ROOM_N, "huh_huh_cat", "晩ごはんを\nどうするか"),
        s(ROOM_N, "calm_black_face_sheep", "まだ\nおなかがいっぱいだ"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "冷蔵庫を開ける"),
        s(ROOM_N, "sad_looking_away_tabby", "マヨネーズと\n麦茶"),
        s(ROOM_N, "realize_wet_cat_stare", "今日は\nこれでいい"),
        s(ROOM_N, "think_chin_paw_orange_cat", "健康診断の\n結果のことは\n今は考えない"),
        s(ROOM_N, "sad_banana_cat_cry", "ドーナツも\n人生も\n原点がいちばんだ", item=PON),
        s(ROOM_N, "excited_hodomoe_city_cat", "来週は\n5個にしよう\nたぶん", se="pikon", dur=3.8),
        J.end_card(),
    ]


def place(cs):
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_12_misdo.mp4"), os.path.join(J.HERE, "out", "jidaraku_12_misdo_preview"))
