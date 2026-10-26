"""自堕落シリーズ #2：30代独身男、ひとりで極楽湯のサウナにハマる（jidaraku.py・10/24 参考動画の作り）。約7分。

python3 catmeme/jidaraku_02_sauna.py → out/jidaraku_02_sauna.mp4
- 流れ：疲れた土曜 → 極楽湯へ → サウナ・水風呂・外気浴で「ととのう」→ 調子に乗って何セットも → のぼせる →
  休憩所でオロポとサ飯と生ビール → 寝落ち → 帰りにぐったり → 次の日、また水風呂を思い出す
- 具体名（10/26 ユーザー指定）：極楽湯、オートロウリュ、アウフグース（熱波師）、ととのい椅子、外気浴、オロポ（オロナミンC＋ポカリ）、
  サ飯、サウナイキタイ（サ活の記録サイト）、12分計。温度などは店によって違うので「90度くらい」とぼかす
- 主人公は「俺」。猫1匹だけ。語りは「〜だ。」、声に出すのは「」。「にゃ」なし。単語の途中で改行しない
- 背景はユーザーが別途くれる画像を backgrounds/jidaraku/02_sauna/ に入れる。届くまでは手もちの背景で代わりにする
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "02_sauna"))
ROOM, FRONT, LOBBY, BATH, SAUNA, MIZU, GAIKI, REST, FOOD, TRAIN, ROOM_N, ROOM_M = (
    "s01_room", "s02_front", "s03_lobby", "s04_bath", "s05_sauna", "s06_mizuburo", "s07_gaikiyoku", "s08_rest_area",
    "s09_food", "s10_train", "s11_room_night", "s12_room_morning")
J.STANDIN.update({ROOM: "bg02_room", FRONT: "bg51_night_street", LOBBY: "bg55_ryokan", BATH: "bg61_snow_onsen",
                  SAUNA: "bg55_ryokan", MIZU: "bg61_snow_onsen", GAIKI: "bg61_snow_onsen", REST: "bg100_lounge_night",
                  FOOD: "bg98_izakaya_night", TRAIN: "bg53_shinkansen", ROOM_N: "bg14_home_night", ROOM_M: "bg02_room"})
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
CATLIFE = os.path.join(L.BGM, "nc102462_Cat_life.mp3")
LETTER = os.path.join(L.BGM, "手紙のさよなら.mp3")


def cuts():
    s = J.line
    return [
        # ---- 家 ----
        s(ROOM, "sleep_sleeping_cat", "土曜の昼。\nやっと起きた。", bgm={"file": L.NORA, "gain": -12}),
        s(ROOM, "sulk_hungry_cat", "今週は\n残業つづきだった。"),
        s(ROOM, "blank_black_cat_zoning_out", "肩が重い。\n腰も重い。"),
        s(ROOM, "slack_nail_filing_cat", "なんとなく\nスマホを見る。"),
        s(ROOM, "stare_big_eyes_tabby_kitten", "「ととのった」と書かれた\nサウナの投稿が流れてきた。"),
        s(ROOM, "think_bike_front_seat_cat", "ととのう……？\nよくわからない。"),
        s(ROOM, "read_book_orange_kitten", "サウナイキタイで\n近くの店を調べてみる。"),
        s(ROOM, "surprise_big_pupils_cat", "車で15分。\n極楽湯がある。"),
        s(ROOM, "peek_what_happen_cat", "口コミには\n「オートロウリュ最高」の声。"),
        s(ROOM, "realize_wet_cat_stare", "俺は30代、独身。\n土曜の予定はゼロだ。"),
        s(ROOM, "excited_hodomoe_city_cat", "「行ってみるか、\nサウナ。」", se="pikon"),
        s(ROOM, "dance_tabby_standing_cat", "タオルだけ持って\n家を出た。"),
        # ---- 店へ ----
        s(FRONT, "drive_driving_cat", "というわけで\n午後2時。"),
        s(FRONT, "showoff_gojo_cosplay_cat", "極楽湯に到着。"),
        s(FRONT, "peek_what_happen_cat", "駐車場は\nけっこう埋まっている。"),
        s(LOBBY, "stare_interviewer_cat", "入口で靴を脱いで\n靴箱に入れる。"),
        s(LOBBY, "money_counting_orange_cat", "券売機で\n入館券を買う。"),
        s(LOBBY, "rizz_cat_rizz", "館内着とタオルの\nセットもつけた。"),
        s(LOBBY, "cocky_dj_cat", "形から入る。\nそれが俺のやり方だ。"),
        s(LOBBY, "blank_black_cat_zoning_out", "まわりは家族連れと\nおじいちゃんたち。"),
        s(LOBBY, "calmdown_dancing_cat", "でも気にしない。\n今日は俺がととのう日だ。"),
        # ---- 1セット目 ----
        s(BATH, "think_bike_front_seat_cat", "まずは体を洗う。\nこれはマナーだ。", bgm={"file": LOFI, "gain": -14, "fade": 1.0}),
        s(BATH, "sleepy_old_memories_cat", "炭酸泉に入る。\nぬるくて気持ちいい。"),
        s(BATH, "realize_wet_cat_stare", "いよいよ\nサウナ室へ。"),
        s(SAUNA, "stare_tabby_wide_eyes_cat", "ドアを開けた瞬間、\n熱気が顔にぶつかる。", se="whoosh_shu"),
        s(SAUNA, "surprise_big_pupils_cat", "温度計は\n90度くらい。"),
        s(SAUNA, "sulk_hungry_cat", "サウナマットに座る。\nいちばん下の段だ。"),
        s(SAUNA, "think_bike_front_seat_cat", "12分計をにらむ。"),
        s(SAUNA, "confused_i_dont_know_cat", "3分。\nもう熱い。"),
        s(SAUNA, "despair_dramatic_kitten", "5分。\n肌がピリピリする。"),
        s(SAUNA, "angry_aiming_cat", "となりのおじいちゃんは\n涼しい顔で座っている。"),
        s(SAUNA, "rage_talking_cat", "負けてたまるか。"),
        s(SAUNA, "sad_banana_cat_cry", "8分。\nもう限界だ。"),
        s(MIZU, "leave_cat_leaves_home", "サウナを出て\nかけ湯で汗を流す。"),
        s(MIZU, "stare_tabby_wide_eyes_cat", "そして水風呂へ。"),
        s(MIZU, "surprise_big_pupils_cat", "「つめたっ！！」", se="freeze_kochiin"),
        s(MIZU, "blank_black_cat_zoning_out", "……でも1分たつと\n体のまわりに膜ができる。"),
        s(MIZU, "realize_wet_cat_stare", "これが\n「羽衣」というやつか。"),
        s(GAIKI, "sleepy_sleepy_cat", "外気浴スペースの\nととのい椅子に座る。"),
        s(GAIKI, "sleepy_old_memories_cat", "風が冷たい。\n空が青い。"),
        s(GAIKI, "calm_black_face_sheep", "手足がじんわりする。\n頭がふわっとする。", se="sparkle_kirakira_01"),
        s(GAIKI, "realize_wet_cat_stare", "……これが\n「ととのう」なのか。"),
        s(GAIKI, "happy_hamster_open_arms", "「ととのった……」"),
        # ---- 調子に乗る ----
        s(GAIKI, "dance_koto_nai_cat", "ここで俺の\nスイッチが入った。", bgm={"file": L.PURPLE, "gain": -12, "fade": 0.8}),
        s(SAUNA, "showoff_gojo_cosplay_cat", "2セット目。\n今度はいちばん上の段だ。"),
        s(SAUNA, "rizz_cat_rizz", "上の段は\n下より10度くらい熱い。"),
        s(SAUNA, "cocky_dj_cat", "「俺はもう\nサウナーだ。」"),
        s(SAUNA, "stare_big_eyes_tabby_kitten", "そこへ放送が流れた。", se="chime_announce"),
        s(SAUNA, "peek_what_happen_cat", "「まもなく\nオートロウリュが始まります」"),
        s(SAUNA, "excited_hodomoe_city_cat", "天井から\n熱いストーンに水が落ちる。", se="explosion_doon"),
        s(SAUNA, "fight_cat_fight", "ジュワーッ！！\n熱い蒸気が降ってくる。"),
        s(SAUNA, "despair_dramatic_kitten", "「あつい！あつい！\nでも気持ちいい！」"),
        s(MIZU, "dance_three_kittens", "水風呂。\nもう怖くない。"),
        s(GAIKI, "calm_black_face_sheep", "外気浴。\nさっきより深くととのう。"),
        s(SAUNA, "work_dog_staring_computer", "3セット目。\n館内の案内を見る。"),
        s(SAUNA, "stare_tabby_wide_eyes_cat", "夕方から\nアウフグースがあるらしい。"),
        s(SAUNA, "yell_orange_fat_cat", "「熱波師が\nタオルで風を送るやつだ！」"),
        s(SAUNA, "happy_girlfriend_dance_cat", "サウナ室は満員。\nみんな静かに待っている。"),
        s(SAUNA, "dance_maxwell_cat", "熱波師がタオルを回す。\n熱い風が来る。", se="whoosh_shu"),
        s(SAUNA, "laugh_laughing_dog", "「おかわり\nいかがですか？」"),
        s(SAUNA, "showoff_gojo_cosplay_cat", "俺は手を挙げた。"),
        s(SAUNA, "rage_talking_cat", "顔に熱風。\n体じゅうから汗が吹き出す。"),
        s(SAUNA, "happy_chipi_chapa_cat", "まわりから拍手。\n俺も拍手。", se="bravo_applause"),
        s(MIZU, "dance_edm_cat", "水風呂に肩までつかる。\n最高だ。"),
        s(GAIKI, "happy_hamster_open_arms", "4セット目、5セット目。\n止まらない。"),
        s(GAIKI, "cocky_dj_cat", "今日の俺は\nサウナの神だ。"),
        # ---- 異変 ----
        s(SAUNA, "stare_tabby_wide_eyes_cat", "6セット目。", se="pi", bgm={"file": LOFI, "gain": -14, "fade": 1.0}),
        s(SAUNA, "confused_i_dont_know_cat", "あれ……\n頭がぼーっとする。"),
        s(SAUNA, "sulk_hungry_cat", "そういえば\n水を飲んでいない。"),
        s(SAUNA, "despair_dramatic_kitten", "立ち上がると\n目の前がチカチカする。"),
        s(BATH, "sleepy_sleepy_cat", "壁に手をついて\nゆっくり歩く。"),
        s(BATH, "sad_banana_cat_cry", "これは\nととのいではない。"),
        s(BATH, "blank_black_cat_zoning_out", "ただの\nのぼせだ。"),
        s(BATH, "realize_wet_cat_stare", "サウナの注意書きを\n思い出す。"),
        s(BATH, "think_bike_front_seat_cat", "「水分補給を\nわすれずに」"),
        s(BATH, "sad_black_dog", "書いてあった。\nちゃんと書いてあった。"),
        # ---- 休憩所 ----
        s(REST, "peek_what_happen_cat", "なんとか館内着に着がえ\n休憩所へ。"),
        s(REST, "money_counting_orange_cat", "売店で\nオロポを頼む。"),
        s(REST, "stare_big_eyes_tabby_kitten", "オロナミンCを\nポカリでわったやつだ。"),
        s(REST, "eat_pop_cat", "ごくごく飲む。", se="drink_gulp_gokugoku_thirsty_chug"),
        s(REST, "yell_orange_fat_cat", "「オロポうめぇ！！\n体にしみる！」"),
        s(REST, "realize_wet_cat_stare", "少しだけ\n生き返った気がする。"),
        s(FOOD, "stare_tabby_wide_eyes_cat", "そしてサウナのあとは\nサ飯だ。"),
        s(FOOD, "read_book_orange_kitten", "食事処のメニューを開く。"),
        s(FOOD, "rizz_cat_rizz", "唐揚げ定食。\nそれと……"),
        s(FOOD, "showoff_gojo_cosplay_cat", "「生ビール\nください！」", se="jan"),
        s(FOOD, "dance_three_kittens", "風呂上がりのビール。\n反則の組み合わせだ。"),
        s(FOOD, "happy_chipi_chapa_cat", "「くぅ〜〜っ！！」", se="pinpoon_correct"),
        s(FOOD, "eat_crunchy_cat_luna", "唐揚げをかじる。\nご飯をかきこむ。"),
        s(FOOD, "dance_wop_cat", "ビールもう1杯。\nおつまみの枝豆も。"),
        s(FOOD, "cocky_dj_cat", "サウナで出したぶん\n取り返している。"),
        s(FOOD, "blank_black_cat_zoning_out", "……いや、\nそれ以上取り返している。"),
        s(REST, "sleepy_sleepy_cat", "リクライニングチェアに\n横になる。"),
        s(REST, "sleep_sleeping_cat", "目を閉じる。\n5分だけ……"),
        s(REST, "stare_tabby_wide_eyes_cat", "目を開けた。", se="cuckoo_pappo"),
        s(REST, "surprise_big_pupils_cat", "夜9時。\n5時間たっていた。", se="question_mark_pop_confused_huh"),
        s(REST, "despair_dramatic_kitten", "「土曜日が\n終わってる……」"),
        # ---- 帰り ----
        s(LOBBY, "money_counting_orange_cat", "精算機で会計する。",
          bgm={"file": LETTER, "gain": -14, "fade": 1.0}),
        s(LOBBY, "stare_tabby_wide_eyes_cat", "入館料、オロポ、\n定食、ビール2杯。"),
        s(LOBBY, "sad_black_dog", "思っていたより\nずっと高い。"),
        s(FRONT, "think_bike_front_seat_cat", "ビールを飲んだから\n車は置いて帰る。"),
        s(FRONT, "sulk_hungry_cat", "代行を呼ぶか\n迷って、電車にした。"),
        s(TRAIN, "sleepy_sleepy_cat", "夜の電車は\n体がだるい。"),
        s(TRAIN, "blank_black_cat_zoning_out", "せっかくの汗が\n冷えて寒い。"),
        s(TRAIN, "sad_banana_cat_cry", "湯冷めというやつだ。"),
        s(TRAIN, "glare_disgusted_cat", "「サウナは\nしばらくいい……」"),
        s(TRAIN, "realize_wet_cat_stare", "明日は車を\n取りに行かないといけない。"),
        # ---- 家（夜） ----
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nそのまま布団に倒れこむ。"),
        s(ROOM_N, "confused_i_dont_know_cat", "体がぽかぽかして\n逆に眠れない。"),
        s(ROOM_N, "despair_dramatic_kitten", "昼に5時間\n寝たせいもある。"),
        s(ROOM_N, "slack_nail_filing_cat", "スマホで\nサウナイキタイを開く。"),
        s(ROOM_N, "work_typing_cat", "初めてのサ活を\n記録してみる。"),
        s(ROOM_N, "sleepy_old_memories_cat", "「6セット。\nのぼせました。」"),
        s(ROOM_N, "sleepy_sleepy_cat", "そう書いて\n目を閉じた。"),
        # ---- 次の日 ----
        s(ROOM_M, "sleepy_old_memories_cat", "次の日の朝。", se="cuckoo_pappo", bgm={"file": CATLIFE, "gain": -12, "fade": 1.0}),
        s(ROOM_M, "sulk_hungry_cat", "体がだるい。\nのどがカラカラだ。"),
        s(ROOM_M, "eat_pop_cat", "水をがぶ飲みする。"),
        s(ROOM_M, "think_bike_front_seat_cat", "昼すぎ。\n車を取りに極楽湯へ向かう。"),
        s(FRONT, "peek_what_happen_cat", "駐車場の車に乗る。"),
        s(FRONT, "stare_big_eyes_tabby_kitten", "店の入口が\n目に入る。"),
        s(FRONT, "blank_black_cat_zoning_out", "中から\nシャンプーのいい香りがする。"),
        s(FRONT, "sleepy_old_memories_cat", "あの水風呂。\nあの外気浴の風。"),
        s(FRONT, "realize_wet_cat_stare", "昨日の「しばらくいい」は\nどこへ行ったのか。"),
        s(FRONT, "rizz_cat_rizz", "「今日は\n3セットだけにしよう。」"),
        s(FRONT, "excited_hodomoe_city_cat", "「水もちゃんと飲む。」", se="pikon"),
        s(FRONT, "dance_tabby_standing_cat", "俺は車のカギを\nポケットにしまった。", dur=3.4),
        J.end_card(),
    ]


if __name__ == "__main__":
    J.run(cuts(), os.path.join(J.HERE, "out", "jidaraku_02_sauna.mp4"), os.path.join(J.HERE, "out", "jidaraku_02_sauna_preview"))
