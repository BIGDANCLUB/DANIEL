"""自堕落シリーズ #1：30代独身男、ひとりで焼肉きんぐに行く（jidaraku.py・10/24 参考動画3本の作りをまねる）。

python3 catmeme/jidaraku_01_yakiniku.py → out/jidaraku_01_yakiniku.mp4
- 流れ：家でCMを見る → 店へ → いちばん高いコースで調子に乗る → 食べすぎて後悔 → 帰って苦しむ → 次の日、また行きたくなる
- 主人公は「俺」（30代・独身・会社員）。猫1匹だけ、セリフごとに猫を差しかえる。語りは「〜だ。」、声に出すのは「」
- 値段・品数は書かない（店やコースで変わるため）。「にゃ」なし。単語の途中で改行しない
- 背景はユーザーが別途くれる画像を backgrounds/jidaraku/01_yakiniku/ に入れる。届くまでは手もちの背景で代わりにする
"""
import os

import cuts_04_leak as L
import jidaraku as J

ROOM, FRONT, WAIT, TABLE, GRILL, DESSERT, REGI, ROAD, ROOM_N, ROOM_M = (
    "j01_room", "j02_store_front", "j03_entrance", "j04_table", "j05_grill", "j06_dessert", "j07_register", "j08_night_road",
    "j09_room_night", "j10_room_morning")
J.STANDIN.update({ROOM: "bg02_room", FRONT: "bg51_night_street", WAIT: "bg13_izakaya", TABLE: "bg22_yakiniku",
                  GRILL: "bg22_yakiniku", DESSERT: "bg22_yakiniku", REGI: "bg15_convenience", ROAD: "bg51_night_street",
                  ROOM_N: "bg14_home_night", ROOM_M: "bg02_room"})
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
CATLIFE = os.path.join(L.BGM, "nc102462_Cat_life.mp3")


def cuts():
    s = J.line
    return [
        # ---- 家 ----
        s(ROOM, "think_bike_front_seat_cat", "土曜の昼。\nやることがない。", bgm={"file": L.NORA, "gain": -12}),
        s(ROOM, "slack_nail_filing_cat", "スマホを見ていたら\n焼肉の動画が流れてきた。"),
        s(ROOM, "stare_big_eyes_tabby_kitten", "ジュウジュウ焼ける肉。\n山盛りのご飯。"),
        s(ROOM, "eat_pop_cat", "……腹が鳴った。"),
        s(ROOM, "sleepy_old_memories_cat", "そういえば最近\nコンビニ弁当ばかりだ。"),
        s(ROOM, "realize_wet_cat_stare", "俺は30代、独身。\n誰にも遠慮はいらない。"),
        s(ROOM, "excited_hodomoe_city_cat", "「焼肉きんぐ、\nひとりで行くか。」", se="pikon"),
        s(ROOM, "dance_tabby_standing_cat", "決めたら早い。\n上着だけ羽織る。"),
        # ---- 店へ ----
        s(FRONT, "drive_driving_cat", "というわけで\n夕方5時。"),
        s(FRONT, "showoff_gojo_cosplay_cat", "焼肉きんぐに到着。"),
        s(FRONT, "peek_what_happen_cat", "駐車場は\nもう車でいっぱいだ。"),
        s(WAIT, "stare_interviewer_cat", "入口には\n家族連れが並んでいる。"),
        s(WAIT, "blank_black_cat_zoning_out", "ひとりなのは\nたぶん俺だけ。"),
        s(WAIT, "calmdown_dancing_cat", "でも気にしない。\n今日は肉が主役だ。"),
        s(WAIT, "meow_gray_white_kitten", "「1名で\nお願いします。」"),
        s(WAIT, "surprise_big_pupils_cat", "意外とすぐ\n席に案内された。"),
        # ---- コース選び ----
        s(TABLE, "read_book_orange_kitten", "席に着いて\nメニューを開く。"),
        s(TABLE, "think_bike_front_seat_cat", "コースは\nいくつかある。"),
        s(TABLE, "money_counting_orange_cat", "いつもなら\nいちばん安いコースだ。"),
        s(TABLE, "rizz_cat_rizz", "でも今日は\n自分へのごほうびだ。"),
        s(TABLE, "yell_orange_fat_cat", "「いちばん上のコースで！」", se="jan"),
        s(TABLE, "cocky_dj_cat", "言ってしまった。\nもう後には引けない。"),
        s(TABLE, "work_typing_cat", "注文は\nタッチパネルでする。"),
        s(TABLE, "stare_tabby_wide_eyes_cat", "制限時間は100分。\n勝負の始まりだ。", se="game_smash_ready_go"),
        # ---- 食べる（調子に乗る） ----
        s(TABLE, "work_dog_staring_computer", "まずは定番。\nカルビ、ハラミ、タン。",
          bgm={"file": L.PURPLE, "gain": -12, "fade": 0.8}),
        s(TABLE, "dance_three_kittens", "ついでに\nご飯の大盛り。"),
        s(GRILL, "happy_hamster_open_arms", "肉が届いた。\n網にのせる。", se="card_place"),
        s(GRILL, "peek_what_happen_cat", "ジュウ……\nいい音だ。"),
        s(GRILL, "eat_crunchy_cat_luna", "タレにつけて\nご飯にバウンド。"),
        s(GRILL, "yell_orange_fat_cat", "「うまっ！！」", se="pinpoon_correct"),
        s(GRILL, "dance_koto_nai_cat", "ここで俺の\nスイッチが入った。"),
        s(TABLE, "work_typing_cat", "タッチパネルを\n連打する。"),
        s(TABLE, "cocky_dj_cat", "上カルビ、厚切りタン、\nホルモン、ステーキ。"),
        s(TABLE, "dance_wop_cat", "食べ放題だから\nいくら頼んでもいい。"),
        s(TABLE, "showoff_gojo_cosplay_cat", "「俺はまだ\n20代の胃袋だ。」"),
        s(GRILL, "happy_girlfriend_dance_cat", "次々と肉が届く。\nテーブルが埋まっていく。"),
        s(GRILL, "eat_pop_cat", "焼いては食べ、\n焼いては食べる。"),
        s(GRILL, "dance_edm_cat", "ビビンバも頼む。\n冷麺も頼む。"),
        s(GRILL, "laugh_laughing_dog", "唐揚げとポテトも。\n焼肉屋なのに。"),
        s(GRILL, "dance_maxwell_cat", "楽しい。\n今日の俺は無敵だ。"),
        # ---- 異変 ----
        s(GRILL, "stare_tabby_wide_eyes_cat", "40分がたった。", se="pi", bgm={"file": LOFI, "gain": -14, "fade": 1.0}),
        s(GRILL, "confused_i_dont_know_cat", "あれ……\nお腹が重い。"),
        s(GRILL, "sulk_hungry_cat", "まだ網の上には\nホルモンがある。"),
        s(GRILL, "peek_what_happen_cat", "そこへ店員さんが来た。"),
        s(GRILL, "surprise_big_pupils_cat", "「ご注文の上カルビ\n3皿です！」", se="card_place"),
        s(GRILL, "despair_dramatic_kitten", "……3皿？", se="question_mark_pop_confused_huh"),
        s(GRILL, "blank_black_cat_zoning_out", "調子に乗って\n押した俺がいた。"),
        s(GRILL, "realize_wet_cat_stare", "頼んだものは\n残さず食べる。"),
        s(GRILL, "angry_aiming_cat", "それが俺の\n焼肉の流儀だ。"),
        s(GRILL, "eat_crunchy_cat_luna", "ひと切れずつ\nゆっくり口に運ぶ。"),
        s(GRILL, "sad_banana_cat_cry", "さっきまで\nあんなにうまかったのに。"),
        s(GRILL, "sleepy_sleepy_cat", "脂が、重い。"),
        s(GRILL, "stare_interviewer_cat", "となりの家族の\n子どもと目が合った。"),
        s(GRILL, "glare_disgusted_cat", "ひとりで肉と\n戦っている大人を見ている。"),
        s(GRILL, "think_bike_front_seat_cat", "最後の1枚を\nご飯なしで飲みこむ。"),
        s(GRILL, "realize_wet_cat_stare", "……勝った。", se="chiin_01"),
        # ---- デザート ----
        s(DESSERT, "stare_big_eyes_tabby_kitten", "ふとメニューの\nデザートが目に入る。"),
        s(DESSERT, "rizz_cat_rizz", "「甘いものは\n別腹って言うしな。」"),
        s(DESSERT, "happy_chipi_chapa_cat", "ソフトクリームを\n頼んでしまった。", se="pikon"),
        s(DESSERT, "eat_pop_cat", "冷たくて甘い。\n口の中がさっぱりする。"),
        s(DESSERT, "sleepy_old_memories_cat", "でも胃袋は\nさっぱりしない。"),
        s(DESSERT, "call_customer_service_cat", "「ラストオーダーの\nお時間です。」", se="chime_announce"),
        s(DESSERT, "sad_black_dog", "もう何も\n頼めない体だ。"),
        # ---- 会計 ----
        s(REGI, "money_counting_orange_cat", "会計をすませる。",
          bgm={"file": os.path.join(L.BGM, "手紙のさよなら.mp3"), "gain": -14, "fade": 1.0}),
        s(REGI, "stare_tabby_wide_eyes_cat", "ひとりで払うには\nなかなかの金額だ。"),
        s(REGI, "meow_gray_white_kitten", "「ごちそうさまでした……」"),
        # ---- 帰り道 ----
        s(ROAD, "leave_cat_leaves_home", "外はもう暗い。", se="whoosh_shu"),
        s(ROAD, "sleepy_sleepy_cat", "ベルトの穴を\nひとつゆるめる。"),
        s(ROAD, "sulk_hungry_cat", "歩くたびに\nお腹がゆれる。"),
        s(ROAD, "despair_dramatic_kitten", "「なんであんなに\n頼んだんだ……」"),
        s(ROAD, "sleepy_old_memories_cat", "20代のころは\nもっと食べられた。"),
        s(ROAD, "realize_wet_cat_stare", "でも今の俺は30代だ。\n胃袋は正直だ。"),
        s(ROAD, "glare_disgusted_cat", "「もう焼肉は\nしばらくいい。」"),
        # ---- 家（夜） ----
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nそのまま横になる。"),
        s(ROOM_N, "blank_black_cat_zoning_out", "胃薬を飲む。"),
        s(ROOM_N, "sad_banana_cat_cry", "寝返りをうつたび\nカルビがよみがえる。"),
        s(ROOM_N, "confused_i_dont_know_cat", "服から\n焼肉のにおいがする。"),
        s(ROOM_N, "despair_dramatic_kitten", "「二度と調子に乗らない。」"),
        s(ROOM_N, "sleepy_sleepy_cat", "そう誓って\n目を閉じた。"),
        # ---- 次の日 ----
        s(ROOM_M, "sleepy_old_memories_cat", "次の日の朝。", se="cuckoo_pappo", bgm={"file": CATLIFE, "gain": -12, "fade": 1.0}),
        s(ROOM_M, "sulk_hungry_cat", "まだ胃が重い。\n朝ごはんはいらない。"),
        s(ROOM_M, "think_bike_front_seat_cat", "昼すぎ。\nだんだん楽になってきた。"),
        s(ROOM_M, "slack_nail_filing_cat", "なんとなく\nスマホを見る。"),
        s(ROOM_M, "stare_big_eyes_tabby_kitten", "また焼肉の動画が\n流れてきた。"),
        s(ROOM_M, "peek_what_happen_cat", "ジュウジュウ焼ける肉。"),
        s(ROOM_M, "eat_pop_cat", "……腹が鳴った。"),
        s(ROOM_M, "realize_wet_cat_stare", "昨日の誓いは\nどこへ行ったのか。"),
        s(ROOM_M, "excited_hodomoe_city_cat", "「今日は\nふつうのコースにしよう。」", se="pikon"),
        s(ROOM_M, "dance_tabby_standing_cat", "俺は上着を羽織った。", dur=3.2),
        J.end_card(),
    ]


if __name__ == "__main__":
    J.run(cuts(), os.path.join(J.HERE, "out", "jidaraku_01_yakiniku.mp4"), os.path.join(J.HERE, "out", "jidaraku_01_yakiniku_preview"))
