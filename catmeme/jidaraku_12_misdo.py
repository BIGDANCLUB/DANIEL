"""自堕落シリーズ #12：30代独身男、ミスタードーナツで好きなだけドーナツ（11/6 ユーザー指定：候補9番）。約8分。

python3 catmeme/jidaraku_12_misdo.py → out/jidaraku_12_misdo.mp4
- 流れ：日曜の朝に甘いものが食べたい → ミスドのショーケース → トレーとトングで選ぶ → 定番・期間限定で迷う → トレーに山盛り →
  店内で1個ずつ食レポ（ポン・デ・リング／オールドファッション／エンゼルフレンチ／フレンチクルーラー／ゴールデンチョコレート）→
  5個目で限界 → コーヒーをおかわり → 残りは持ち帰り → 結局ポン・デ・リングに戻る
- 店をけなさない。値段・カロリーの数字は出さない。コーヒーのおかわりは「できる店が多い」とぼかす
- ベンチマーク3チャンネルにミスドの回はない（11/6 確認）
- 写真がない場面は字幕だけ（写真が届いたら backgrounds/jidaraku/12_misdo に置く）。ほかの店の写真は使わない
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
LINEUP = "f_lineup"   # 11/6 ならんだドーナツのアップ（ショーケースの最初）
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
        s(ROOM, "think_bike_front_seat_cat", "あの箱を\n開ける瞬間が\n好きだった"),
        s(ROOM, "realize_wet_cat_stare", "今の俺は\n30代独身"),
        s(ROOM, "money_counting_orange_cat", "自分のお金で\n好きなだけ\n買える"),
        s(ROOM, "angry_aiming_cat", "大人の\nドーナツ食べ放題だ"),
        s(ROOM, "excited_hodomoe_city_cat", "ミスドだ", se="shine_kiraan_maou"),
        s(ROOM, "work_typing_cat", "パーカーをはおる"),
        s(ROOM, "stare_lying_tabby_cat", "顔は洗わない"),
        s(ROOM, "calm_black_face_sheep", "ドーナツは\n顔を見ない"),
        s(ROOM, "leave_cat_leaves_home", "家を出る", se="whoosh_shu"),
        s(STREET, "think_chin_paw_orange_cat", "日曜の朝の道は\n静かだ"),
        s(STREET, "dance_three_kittens", "公園で\n子どもたちが\n走りまわっている"),
        s(STREET, "sleepy_old_memories_cat", "俺にも\nあんな時代があった"),
        s(STREET, "think_bike_front_seat_cat", "あのころは\nドーナツ1個で\nしあわせだった"),
        s(STREET, "rizz_cat_rizz", "今日の俺は\n10個で\nしあわせになる"),
        # ---- 来店 ----
        s(FRONT, "leave_cat_leaves_home", "駅前の\nミスタードーナツ", se="whoosh_shu", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(FRONT, "surprise_big_pupils_cat", "あまい香りが\n外までただよっている"),
        s(FRONT, "happy_hamster_open_arms", "この香りだけで\nごはんが食べられる"),
        s(FRONT, "stare_interviewer_cat", "家族づれ\n学生さん\n近所のおばあちゃん"),
        s(FRONT, "rizz_cat_rizz", "ミスドは\nだれでも入れる店だ"),
        s(FRONT, "joy_happy_happy_happy_cat", "30代独身男も\n例外ではない"),
        s(FRONT, "yell_orange_fat_cat", "入店", se="gong_match_start"),
        # ---- ショーケース ----
        s(CASE, "stare_big_eyes_tabby_kitten", "目の前に\nずらりとならぶ\nドーナツ", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}, item=LINEUP),
        s(CASE, "showoff_gojo_cosplay_cat", "ドーナツの宝石箱だ", se="gong_dora_jaan", item=LINEUP),
        s(CASE, "read_book_orange_kitten", "トレーとトングを\n持って\n自分で選ぶ", item=TRAY),
        s(CASE, "think_chin_paw_orange_cat", "トングを\nカチカチ\n2回鳴らす", item=TRAY, se="pi"),
        s(CASE, "smug_squint_bicolor_cat", "準備はできた", item=TRAY),
        s(CASE, "stare_tabby_wide_eyes_cat", "定番のドーナツ"),
        s(CASE, "surprise_big_pupils_cat", "期間限定のドーナツ"),
        s(CASE, "huh_huh_cat", "パイ\nマフィン\n飲茶まである"),
        s(CASE, "confused_i_dont_know_cat", "選べない"),
        s(CASE, "despair_dramatic_kitten", "全部ほしい", se="pi"),
        s(CASE, "think_bike_front_seat_cat", "落ち着け"),
        s(CASE, "read_book_orange_kitten", "まずは\n定番から攻める"),
        s(CASE, "work_typing_cat", "ポン・デ・リング", item=PON),
        s(CASE, "eat_pop_cat", "トレーにのせる", item=PON),
        s(CASE, "stare_big_eyes_tabby_kitten", "オールドファッション", item=OLD),
        s(CASE, "happy_chipi_chapa_cat", "のせる", item=OLD),
        s(CASE, "surprise_big_pupils_cat", "エンゼルフレンチ", item=ANGEL),
        s(CASE, "joy_happy_happy_happy_cat", "のせる", item=ANGEL),
        s(CASE, "think_chin_paw_orange_cat", "フレンチクルーラー", item=CRULLER),
        s(CASE, "dance_wop_cat", "のせる", item=CRULLER),
        s(CASE, "stare_tabby_wide_eyes_cat", "ゴールデンチョコレート", item=GOLDEN),
        s(CASE, "dance_happy_banana_cat", "のせる", item=GOLDEN),
        s(CASE, "peek_what_happen_cat", "期間限定のやつも", item=TRAY),
        s(CASE, "cocky_dj_cat", "のせる", item=TRAY),
        s(CASE, "huh_goat_talks_to_huh_cat", "となりのやつも", item=TRAY),
        s(CASE, "dance_edm_cat", "のせる", item=TRAY),
        s(CASE, "peek_what_happen_cat", "となりのお母さんが\n子どもに聞いている", item=TRAY),
        s(CASE, "stare_interviewer_cat", "どれにするー？\n1個だけねー", item=TRAY),
        s(CASE, "sad_black_dog", "1個だけ……", item=TRAY),
        s(CASE, "smug_squint_bicolor_cat", "俺には\n止める人がいない", item=TRAY),
        s(CASE, "happy_hamster_open_arms", "これが\n独身の自由だ", item=TRAY),
        s(CASE, "think_chin_paw_orange_cat", "いや\n止めてくれる人が\nいないだけだ", item=TRAY),
        s(CASE, "stare_big_eyes_tabby_kitten", "トレーを見る", item=TRAY),
        s(CASE, "scream_standing_marmot", "10個", item=TRAY, se="explosion_chudoon"),
        s(CASE, "calm_black_face_sheep", "トレーが\n見えない", item=TRAY),
        s(CASE, "think_chin_paw_orange_cat", "1人で10個は\n多いだろうか", item=TRAY),
        s(CASE, "rizz_cat_rizz", "いや\nこれは大人の\n食べ放題だ", item=TRAY),
        # ---- レジ ----
        s(CASE, "stare_interviewer_cat", "お次の方\nどうぞー", se="pinpon_notice", item=TRAY),
        s(CASE, "meow_ragdoll_chubby_cat", "トレーを\nそっと置く", item=TRAY),
        s(CASE, "stare_interviewer_cat", "お持ち帰りですかー？", item=TRAY),
        s(CASE, "sad_black_dog", "10個あれば\nそう思うよな", item=TRAY),
        s(CASE, "angry_shooting_cat", "店内で", item=TRAY, se="explosion_dokaan"),
        s(CASE, "stare_interviewer_cat", "かしこまりましたー", item=TRAY),
        s(CASE, "joy_happy_happy_happy_cat", "店員さんは\n笑顔のまま", item=TRAY),
        s(CASE, "happy_hamster_open_arms", "さすがプロだ", item=TRAY),
        s(CASE, "think_bike_front_seat_cat", "ホットコーヒーも\nたのむ", item=COFFEE),
        s(CASE, "read_book_orange_kitten", "おかわりが\nできる店も多い", item=COFFEE),
        s(CASE, "smug_squint_bicolor_cat", "長期戦の\n準備はできた", item=COFFEE),
        # ---- 1個目 ポン・デ・リング ----
        s(SEAT, "work_typing_cat", "窓ぎわの席を\n確保", bgm={"file": PASTEL, "gain": -12}),
        s(SEAT, "stare_big_eyes_tabby_kitten", "10個のドーナツと\n向きあう", item=TRAY),
        s(SEAT, "calmdown_dancing_cat", "まずは\nポン・デ・リング", item=PON),
        s(SEAT, "think_chin_paw_orange_cat", "丸い玉が\n輪になって\nつながっている", item=PON),
        s(SEAT, "read_book_orange_kitten", "1個ずつ\nちぎって食べる派だ", item=PON),
        s(SEAT, "eat_pop_cat", "ちぎっ", item=PON, se="pikon"),
        s(SEAT, "eat_crunchy_cat_luna", "もちっ", item=PON),
        s(SEAT, "surprise_big_pupils_cat", "もちもちが\n口の中ではねる", item=PON),
        s(SEAT, "happy_girlfriend_dance_cat", "この食感\n変わっていない", item=PON),
        s(SEAT, "sleepy_old_memories_cat", "子どものころの\n日曜日の味だ", item=PON),
        s(SEAT, "sad_banana_cat_cry", "母さん\n元気かな", item=PON),
        s(SEAT, "think_bike_front_seat_cat", "あとで\nLINEしよう", item=PON),
        s(SEAT, "eat_pop_cat", "ちぎっ\nもちっ", item=PON),
        s(SEAT, "happy_hamster_open_arms", "1個目\n完食", item=PON),
        s(SEAT, "stare_tabby_wide_eyes_cat", "ふと思う", item=PON),
        s(SEAT, "think_chin_paw_orange_cat", "ドーナツの穴は\nなぜあいているのか", item=PON),
        s(SEAT, "read_book_orange_kitten", "まんなかまで\nむらなく\n火を通すためらしい", item=PON),
        s(SEAT, "huh_huh_cat", "穴にも\n意味があった", item=PON),
        s(SEAT, "realize_wet_cat_stare", "俺の休日の\nぽっかりあいた時間にも\nきっと意味がある", item=PON),
        s(SEAT, "calm_black_face_sheep", "たぶん", item=PON),
        # ---- 2個目 オールドファッション ----
        s(SEAT, "stare_tabby_wide_eyes_cat", "2個目\nオールドファッション", item=OLD),
        s(SEAT, "read_book_orange_kitten", "外はザクザク\n中はしっとり", item=OLD),
        s(SEAT, "eat_crunchy_cat_luna", "ザクッ", item=OLD, se="pikon"),
        s(SEAT, "realize_wet_cat_stare", "まわりのザクザクが\nいちばんうまい", item=OLD),
        s(SEAT, "think_chin_paw_orange_cat", "ここで\nコーヒーをひと口", item=COFFEE),
        s(SEAT, "eat_crunchy_cat_luna", "ズズッ", item=COFFEE, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "happy_girlfriend_dance_cat", "合う", item=COFFEE),
        s(SEAT, "cocky_dj_cat", "オールドファッションと\nコーヒーは\n名コンビだ", item=OLD),
        s(SEAT, "rizz_cat_rizz", "大人の\nドーナツの食べ方", item=OLD),
        s(SEAT, "joy_happy_happy_happy_cat", "2個目\n完食", item=OLD),
        # ---- 3個目 エンゼルフレンチ ----
        s(SEAT, "surprise_big_pupils_cat", "3個目\nエンゼルフレンチ", item=ANGEL),
        s(SEAT, "stare_big_eyes_tabby_kitten", "ふわふわの生地に\nクリームがたっぷり", item=ANGEL),
        s(SEAT, "think_chin_paw_orange_cat", "これは\n食べ方がむずかしい", item=ANGEL),
        s(SEAT, "angry_aiming_cat", "いくぞ", item=ANGEL),
        s(SEAT, "eat_crunchy_cat_luna", "ガブッ", item=ANGEL, se="explosion_chudoon"),
        s(SEAT, "scream_standing_marmot", "クリームが\nうしろから\nはみ出した", item=ANGEL),
        s(SEAT, "despair_dramatic_kitten", "口のまわりが\nクリームまみれ", item=ANGEL),
        s(SEAT, "peek_what_happen_cat", "となりの子どもが\nこっちを見ている", item=ANGEL),
        s(SEAT, "laugh_laughing_dog", "同じ顔をしている", item=ANGEL),
        s(SEAT, "happy_chipi_chapa_cat", "仲間だ", item=ANGEL),
        s(SEAT, "realize_wet_cat_stare", "でも\nクリームがやさしい", item=ANGEL),
        s(SEAT, "sleepy_sleepy_cat", "天使が\n口の中で\nとけていく", item=ANGEL),
        s(SEAT, "happy_hamster_open_arms", "3個目\n完食", item=ANGEL),
        # ---- 4個目 フレンチクルーラー ----
        s(SEAT, "think_bike_front_seat_cat", "4個目\nフレンチクルーラー", item=CRULLER),
        s(SEAT, "read_book_orange_kitten", "ふんわりかるい\nうねうねのドーナツ", item=CRULLER),
        s(SEAT, "eat_pop_cat", "ふわっ", item=CRULLER, se="pikon"),
        s(SEAT, "surprise_big_pupils_cat", "消えた", item=CRULLER),
        s(SEAT, "huh_huh_cat", "いま\n食べたよな？", item=CRULLER, se="question_mark_pop_confused_huh"),
        s(SEAT, "calm_black_face_sheep", "かるすぎて\n食べた気がしない", item=CRULLER),
        s(SEAT, "smug_squint_bicolor_cat", "つまり\n0個だ", item=CRULLER),
        s(SEAT, "dance_wop_cat", "4個目は\nなかったことにする", item=CRULLER),
        # ---- 5個目 ゴールデンチョコレート ----
        s(SEAT, "stare_tabby_wide_eyes_cat", "5個目\nゴールデンチョコレート", item=GOLDEN),
        s(SEAT, "think_chin_paw_orange_cat", "黄色いツブツブが\nびっしり", item=GOLDEN),
        s(SEAT, "eat_crunchy_cat_luna", "ザクザク", item=GOLDEN, se="pikon"),
        s(SEAT, "happy_girlfriend_dance_cat", "ツブツブが\n楽しい", item=GOLDEN),
        s(SEAT, "stare_big_eyes_tabby_kitten", "……あれ", item=GOLDEN),
        s(SEAT, "sad_looking_away_tabby", "テーブルが\nツブツブだらけ", item=GOLDEN),
        s(SEAT, "meow_ragdoll_chubby_cat", "1粒ずつ\nひろって食べる", item=GOLDEN),
        s(SEAT, "realize_wet_cat_stare", "さっきより\n手がおそい", item=GOLDEN),
        s(SEAT, "sleepy_old_memories_cat", "口の中が\nずっと甘い", item=GOLDEN),
        s(SEAT, "despair_dramatic_kitten", "おなかが\n重い", item=GOLDEN, se="pi"),
        s(SEAT, "blank_black_cat_zoning_out", "5個目で\n手が止まった", item=GOLDEN),
        s(SEAT, "peek_what_happen_cat", "店の中を見わたす", item=COFFEE),
        s(SEAT, "stare_interviewer_cat", "勉強している学生さん", item=COFFEE),
        s(SEAT, "sleepy_old_memories_cat", "新聞を読む\nおじいちゃん", item=COFFEE),
        s(SEAT, "happy_chipi_chapa_cat", "ドーナツを分けあう\nカップル", item=COFFEE),
        s(SEAT, "calm_black_face_sheep", "ドーナツ10個と\n向きあう俺", item=TRAY),
        s(SEAT, "rizz_cat_rizz", "みんな\nそれぞれの日曜日だ", item=TRAY),
        # ---- 限界 ----
        s(SEAT, "stare_big_eyes_tabby_kitten", "トレーを見る", item=TRAY),
        s(SEAT, "scream_standing_marmot", "まだ\n5個ある", item=TRAY, se="explosion_chudoon"),
        s(SEAT, "sad_black_dog", "大人の食べ放題は\n胃袋が\n子どものままだった", item=TRAY),
        s(SEAT, "think_chin_paw_orange_cat", "コーヒーで\nリセットする", item=COFFEE),
        s(SEAT, "work_typing_cat", "おかわり\nおねがいします", item=COFFEE, se="pinpon_notice"),
        s(SEAT, "stare_interviewer_cat", "どうぞー", item=COFFEE),
        s(SEAT, "eat_crunchy_cat_luna", "ズズッ", item=COFFEE, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "happy_hamster_open_arms", "苦さが\n口の中を\nもとにもどす", item=COFFEE),
        s(SEAT, "angry_aiming_cat", "6個目\nいけるか", item=TRAY),
        s(SEAT, "calm_black_face_sheep", "……いけない", item=TRAY),
        s(SEAT, "sleepy_sleepy_cat", "コーヒーだけ\n3杯目", item=COFFEE),
        s(SEAT, "stare_lying_tabby_cat", "窓の外を\nぼんやりながめる", item=COFFEE),
        s(SEAT, "dance_three_kittens", "家族づれが\n箱を持って\n帰っていく", item=COFFEE),
        s(SEAT, "realize_wet_cat_stare", "そうか", item=COFFEE),
        s(SEAT, "think_bike_front_seat_cat", "ドーナツは\n持って帰るという\n手があった", item=TRAY),
        s(SEAT, "joy_happy_happy_happy_cat", "すみません\n箱をください", item=TRAY, se="pinpon_notice"),
        s(SEAT, "stare_interviewer_cat", "はーい", item=TRAY),
        s(SEAT, "happy_chipi_chapa_cat", "子どものころの\nあの箱だ", item=TRAY),
        # ---- 帰り道 ----
        s(STREET, "leave_cat_leaves_home", "箱を持って\n店を出る", se="whoosh_shu", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(STREET, "happy_hamster_open_arms", "箱が\nずっしり重い"),
        s(STREET, "sleepy_old_memories_cat", "母さんは\nいつも\nこれを持って帰ってきたのか"),
        s(STREET, "sad_banana_cat_cry", "今になって\nわかる"),
        s(STREET, "work_typing_cat", "母さんにLINEする"),
        s(STREET, "scream_phone_orange_cat", "ミスド行ってきた"),
        s(STREET, "stare_big_eyes_tabby_kitten", "すぐに返事が来た"),
        s(STREET, "happy_chipi_chapa_cat", "いいね\nポン・デ・リング\n食べた？"),
        s(STREET, "joy_happy_happy_happy_cat", "母さんも\nポン・デ・リング派だった"),
        s(STREET, "stare_big_eyes_tabby_kitten", "公園の前を通る"),
        s(STREET, "dance_three_kittens", "朝の子どもたちが\nまだ走っている"),
        s(STREET, "think_bike_front_seat_cat", "ベンチに座る"),
        s(STREET, "sleepy_sleepy_cat", "おなかが\n重くて\n動けない"),
        s(STREET, "calm_black_face_sheep", "鳩が\n箱を見ている"),
        s(STREET, "angry_aiming_cat", "あげないぞ"),
        s(STREET, "leave_cat_leaves_home", "箱を抱えて\n歩き出す"),
        s(STREET, "think_chin_paw_orange_cat", "今度の休みは\n実家に箱で\n持って帰ろう"),
        # ---- 夜 ----
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\n昼寝", se="whoosh_shu"),
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "夜8時\n目が覚めた"),
        s(ROOM_N, "huh_huh_cat", "晩ごはんを\nどうするか"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "テーブルの上に\nあの箱", item=TRAY),
        s(ROOM_N, "smug_squint_bicolor_cat", "晩ごはんは\nドーナツだ", item=TRAY),
        s(ROOM_N, "think_chin_paw_orange_cat", "1日に\nドーナツ10個", item=TRAY),
        s(ROOM_N, "calm_black_face_sheep", "健康診断の\n結果のことは\n今は考えない", item=TRAY),
        s(ROOM_N, "eat_crunchy_cat_luna", "6個目\n7個目", item=TRAY),
        s(ROOM_N, "sleepy_sleepy_cat", "8個目\n9個目", item=TRAY),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "最後の1個", item=PON),
        s(ROOM_N, "surprise_big_pupils_cat", "ポン・デ・リングを\n2個買っていた", item=PON),
        s(ROOM_N, "eat_pop_cat", "ちぎっ\nもちっ", item=PON),
        s(ROOM_N, "realize_wet_cat_stare", "いろいろ食べたけど", item=PON),
        s(ROOM_N, "happy_girlfriend_dance_cat", "結局\nここに帰ってくる", item=PON),
        s(ROOM_N, "sad_banana_cat_cry", "ドーナツも\n人生も\n原点がいちばんだ", item=PON),
        s(ROOM_N, "excited_hodomoe_city_cat", "来週は\n2個にしよう\nたぶん", se="pikon", dur=3.8),
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
