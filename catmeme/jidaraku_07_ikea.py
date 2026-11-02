"""自堕落シリーズ #7：30代独身男、ひとりでIKEAに行く（11/2 ユーザー指定・焼肉きんぐ/スシロー/ブロンコビリーと同じ作り）。約8分。

python3 catmeme/jidaraku_07_ikea.py → out/jidaraku_07_ikea.mp4
- 流れ（ユーザー指定）：普段忙しいからこそ丁寧な暮らしがしたい → 家具をオシャレにしたい でもダラダラ見て回りたい → そうだIKEAだ →
  ルートに沿って進むだけで一周できる分かりやすい構造 → コンセプトごとの部屋で生活がイメージしやすい → 他で見ない生活雑貨 →
  一周に何時間かかるんだ → 腹が減ってレストランで肉団子（ミートボール）→ 物色再開 → 良いものが多すぎて何も買えず一周 →
  意を決してマットレスを買う → 最後にソフトクリーム 50円にびっくり 普通に美味しい → 周りは家族連ればかり →
  こんな独り身でも受け入れてくれるIKEAはいい場所（泣きながら帰る）
- 口コミ・記事の声：ソフトクリームは50円（2023年秋から豆乳のプラントベース・値段はそのまま）／
  ミートボールはマッシュポテトとクリームソース・リンゴンベリージャム添え。そのほかの値段は書かない
- 実在の人の名前は出さない。字幕にカギかっこ・句読点なし。「にゃ」なし。単語の途中で改行しない
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "07_ikea"))
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku", d) for d in ("04_sushiro", "05_gokurakuyu", "06_bronco")]
ROOM, FRONT, LIVING, KITCHEN, BEDROOM, MARKET, REST, WARE, BISTRO, ROAD, ROOM_N = (
    "j01_room", "i01_front", "i02_living", "i03_kitchen", "i04_bedroom", "i05_market", "i06_restaurant", "i07_warehouse",
    "i08_bistro", "b06_road_night", "j07_room_night")
# 絵が届くまでの代わり
J.STANDIN.update({FRONT: "g01_front", LIVING: "bg02_room", KITCHEN: "st02_home_kitchen", BEDROOM: "bg02_room",
                  MARKET: "s02_inside", REST: "g06_dining", WARE: "bg24_server_room", BISTRO: "b03_inside"})
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
CATLIFE = os.path.join(L.BGM, "nc102462_Cat_life.mp3")
# 写真（届いた順に backgrounds/jidaraku/07_ikea に置く）
MEATBALL, SOFT, SHARK, GOODS, MATTRESS, BAG = ("f_meatball", "f_softcream", "f_shark", "f_goods", "f_mattress", "f_bluebag")


def cuts():
    def s(*a, **k):   # 1つの字幕は3.4秒（8分前後にする）
        k.setdefault("dur", 3.4)
        return J.line(*a, **k)
    return [
        # ---- 丁寧な暮らしがしたい ----
        s(ROOM, "sleep_sleeping_cat", "日曜の朝10時\n目が覚めた", bgm={"file": L.NORA, "gain": -12}),
        s(ROOM, "blank_black_cat_zoning_out", "部屋を見わたす"),
        s(ROOM, "sulk_hungry_cat", "脱ぎっぱなしの服\nコンビニの袋"),
        s(ROOM, "despair_dramatic_kitten", "学生のころから使っている\nぺたんこの布団"),
        s(ROOM, "think_chin_paw_orange_cat", "普段忙しいからこそ"),
        s(ROOM, "sleepy_old_memories_cat", "休みの日くらいは\n丁寧な暮らしがしたい"),
        s(ROOM, "read_book_orange_kitten", "朝はコーヒーを豆からいれて\n観葉植物に水をやる"),
        s(ROOM, "happy_hamster_open_arms", "そんな部屋に\n住みたい"),
        s(ROOM, "showoff_gojo_cosplay_cat", "家具を\nオシャレにしたい"),
        s(ROOM, "slack_nail_filing_cat", "でも\n店員さんに話しかけられず"),
        s(ROOM, "sleepy_sleepy_cat", "ダラダラ\n見て回りたい"),
        s(ROOM, "stare_tabby_wide_eyes_cat", "……そうだ", se="question_hatena_maou"),
        s(ROOM, "rizz_cat_rizz", "IKEAだ", se="shine_kiraan_maou"),
        # ---- 到着 ----
        s(FRONT, "ride_kitten_bike", "電車とバスを乗りついで\nIKEAに到着", se="whoosh_shu", bgm={"file": L.PURPLE, "gain": -12, "fade": 0.8}),
        s(FRONT, "surprise_big_pupils_cat", "青くて大きい……", se="gong_dora_jaan"),
        s(FRONT, "peek_what_happen_cat", "駐車場には\n家族連れの車がずらり"),
        s(FRONT, "angry_aiming_cat", "大きな青い袋を\n肩にかけて"),
        s(FRONT, "excited_hodomoe_city_cat", "いざ\n入店", item=BAG),
        s(LIVING, "stare_interviewer_cat", "エスカレーターを上がると\nショールーム"),
        s(LIVING, "read_book_orange_kitten", "床には\n矢印が書いてある"),
        s(LIVING, "think_bike_front_seat_cat", "この矢印の\nルートに沿って進むだけで"),
        s(LIVING, "showoff_gojo_cosplay_cat", "建物を\nぐるっと一周できる"),
        s(LIVING, "happy_chipi_chapa_cat", "分かりやすい\n構造だ"),
        s(LIVING, "rizz_cat_rizz", "迷子にならない\nひとり客にやさしい"),
        # ---- ショールーム ----
        s(LIVING, "calmdown_dancing_cat", "部屋が\nコンセプトごとに\n細かく分けられている"),
        s(LIVING, "stare_big_eyes_tabby_kitten", "25平米の\nひとり暮らしの部屋"),
        s(LIVING, "surprise_big_pupils_cat", "……俺の部屋より\n広く見える"),
        s(LIVING, "think_chin_paw_orange_cat", "棚の置き方ひとつで\nこんなに変わるのか"),
        s(LIVING, "sleepy_old_memories_cat", "ソファに座ってみる"),
        s(LIVING, "happy_hamster_open_arms", "……住める"),
        s(LIVING, "realize_wet_cat_stare", "ここで休日に\n本を読む自分が見える"),
        s(LIVING, "read_book_orange_kitten", "家具が飾られているから\n生活がイメージしやすい"),
        s(KITCHEN, "work_typing_cat", "次はキッチンの部屋"),
        s(KITCHEN, "stare_tabby_wide_eyes_cat", "壁に鍋とフライパンが\nきれいにかけてある"),
        s(KITCHEN, "eat_pop_cat", "ここで\nパスタをゆでる俺"),
        s(KITCHEN, "glare_disgusted_cat", "……いや\n家の鍋は1つしかない"),
        s(KITCHEN, "confused_i_dont_know_cat", "しかも\nカップ麺用のお湯しか\nわかしていない"),
        s(BEDROOM, "peek_what_happen_cat", "続いて寝室の部屋"),
        s(BEDROOM, "sleep_sleeping_cat", "ふかふかのベッド"),
        s(BEDROOM, "think_chin_paw_orange_cat", "マットレスの\n寝ごこちを試せるコーナー"),
        s(BEDROOM, "sleepy_sleepy_cat", "寝ころんでみる"),
        s(BEDROOM, "sad_banana_cat_cry", "……ぺたんこの布団とは\n別の世界だ"),
        s(BEDROOM, "stare_interviewer_cat", "となりで子どもが\nベッドで跳ねている"),
        s(BEDROOM, "blank_black_cat_zoning_out", "そっと起き上がる"),
        s(LIVING, "dance_three_kittens", "子ども部屋\nワンルーム\nダイニング"),
        s(LIVING, "stare_tabby_wide_eyes_cat", "部屋がまだまだ続く"),
        s(LIVING, "confused_i_dont_know_cat", "……一周するのに\n何時間かかるんだ", se="cuckoo_pappo"),
        # ---- 腹が減る ----
        s(LIVING, "sulk_hungry_cat", "ダメだ\n回っている最中に\n腹が減った", se="pi", bgm={"file": CATLIFE, "gain": -12, "fade": 0.8}),
        s(LIVING, "think_bike_front_seat_cat", "ショールームの途中に\nレストランがある"),
        s(REST, "leave_cat_leaves_home", "レストランに行こう", se="whoosh_shu"),
        s(REST, "peek_what_happen_cat", "大きな食堂に\n家族連れがいっぱい"),
        s(REST, "work_typing_cat", "トレーを持って\n列に並ぶ"),
        s(REST, "showoff_gojo_cosplay_cat", "頼むのは\nもちろん肉団子", item=MEATBALL),
        s(REST, "stare_big_eyes_tabby_kitten", "スウェーデン風の\nミートボール", item=MEATBALL),
        s(REST, "think_chin_paw_orange_cat", "マッシュポテトと\nクリームソース", item=MEATBALL),
        s(REST, "confused_i_dont_know_cat", "そして\n赤いジャム……？", item=MEATBALL, se="question_mark_pop_confused_huh"),
        s(REST, "read_book_orange_kitten", "リンゴンベリーという\n木の実のジャムらしい", item=MEATBALL),
        s(REST, "glare_disgusted_cat", "肉に\nジャム……", item=MEATBALL),
        s(REST, "eat_crunchy_cat_luna", "ひと口", item=MEATBALL),
        s(REST, "surprise_big_pupils_cat", "……合う", item=MEATBALL, se="pinpoon_correct"),
        s(REST, "happy_girlfriend_dance_cat", "甘ずっぱさが\nクリームソースの\nこってりを消してくれる", item=MEATBALL),
        s(REST, "eat_pop_cat", "マッシュポテトが\nなめらか", item=MEATBALL),
        s(REST, "happy_hamster_open_arms", "肉団子定食\n最高だ", item=MEATBALL),
        s(REST, "sleepy_old_memories_cat", "窓の外をながめながら\nゆっくり食べる"),
        s(REST, "realize_wet_cat_stare", "これが\n丁寧な暮らしか"),
        s(REST, "stare_interviewer_cat", "となりのテーブルでは\n家族が子どもの机を相談している"),
        s(REST, "blank_black_cat_zoning_out", "俺は\nミートボールを数えている"),
        # ---- 物色再開 ----
        s(MARKET, "cocky_dj_cat", "物色\n再開", se="gong_match_start"),
        s(MARKET, "stare_tabby_wide_eyes_cat", "1階は\n生活雑貨の売り場"),
        s(MARKET, "surprise_big_pupils_cat", "他の店では\n見ないようなものが多い", item=GOODS),
        s(MARKET, "read_book_orange_kitten", "キャンドル\n保存容器\nカラフルなまな板", item=GOODS),
        s(MARKET, "think_chin_paw_orange_cat", "名前が全部\n読めない", item=GOODS),
        s(MARKET, "showoff_gojo_cosplay_cat", "この保存容器\n丁寧な暮らしっぽい", item=GOODS),
        s(MARKET, "glare_disgusted_cat", "……でも入れるものがない"),
        s(MARKET, "peek_what_happen_cat", "そして\n山積みの大きなサメ", item=SHARK),
        s(MARKET, "stare_big_eyes_tabby_kitten", "サメのぬいぐるみが\nこっちを見ている", item=SHARK),
        s(MARKET, "happy_chipi_chapa_cat", "……かわいい", item=SHARK),
        s(MARKET, "sad_looking_away_tabby", "30代独身男が\nサメを抱いて帰るのか", item=SHARK),
        s(MARKET, "think_chin_paw_orange_cat", "……そっと戻す", item=SHARK),
        s(MARKET, "dance_koto_nai_cat", "クッション\nラグ\n照明"),
        s(MARKET, "confused_i_dont_know_cat", "どれも良い\nどれも良すぎる"),
        s(MARKET, "despair_dramatic_kitten", "良いものが多すぎて\n選べない"),
        s(MARKET, "sleepy_old_memories_cat", "手に取っては戻す\nまた手に取っては戻す"),
        s(WARE, "stare_tabby_wide_eyes_cat", "気づけば\n巨大な倉庫に出た", se="whoosh_shu"),
        s(WARE, "surprise_big_pupils_cat", "天井まで\n箱が積み上がっている"),
        s(WARE, "read_book_orange_kitten", "ショールームで\nメモした家具を\nここで自分で取るらしい"),
        s(WARE, "blank_black_cat_zoning_out", "……メモ\nしていない"),
        s(WARE, "sulk_hungry_cat", "青い袋は\nからっぽのまま"),
        s(WARE, "despair_dramatic_kitten", "何も買えず\n一周してしまった", se="chin_bell_failure_sad_ending"),
        s(WARE, "sad_banana_cat_cry", "3時間歩いて\nミートボールを食べただけ"),
        # ---- マットレス ----
        s(WARE, "think_chin_paw_orange_cat", "……このままでは\n帰れない", bgm={"file": LOFI, "gain": -12, "fade": 1.0}),
        s(WARE, "sleepy_old_memories_cat", "ぺたんこの布団を\n思い出す"),
        s(WARE, "realize_wet_cat_stare", "丁寧な暮らしは\nまず よく眠ることから"),
        s(WARE, "angry_aiming_cat", "意を決して", se="explosion_dokaan"),
        s(BEDROOM, "leave_cat_leaves_home", "寝室のコーナーまで\n逆走する", se="whoosh_shu"),
        s(BEDROOM, "sleep_sleeping_cat", "マットレスを\nもう一度ぜんぶ試す"),
        s(BEDROOM, "think_bike_front_seat_cat", "かため\nやわらかめ\nふつう"),
        s(BEDROOM, "stare_interviewer_cat", "店員さんに\nはじめて話しかける"),
        s(BEDROOM, "showoff_gojo_cosplay_cat", "このマットレス\nください", item=MATTRESS, se="explosion_dokaan"),
        s(WARE, "happy_hamster_open_arms", "くるくる丸められた\nマットレスを\nカートにのせる", item=MATTRESS),
        s(WARE, "dance_three_kittens", "やっと\n買い物ができた", item=MATTRESS),
        s(WARE, "money_counting_orange_cat", "セルフレジで\nお会計", se="pi"),
        s(WARE, "rizz_cat_rizz", "今夜から\n俺は丁寧に眠る"),
        # ---- ソフトクリーム ----
        s(BISTRO, "stare_tabby_wide_eyes_cat", "レジを出ると\n小さなカフェスペース", se="whoosh_shu", bgm={"file": L.PURPLE, "gain": -12, "fade": 0.8}),
        s(BISTRO, "peek_what_happen_cat", "みんな\nソフトクリームを持っている", item=SOFT),
        s(BISTRO, "think_chin_paw_orange_cat", "1つ買ってみるか", item=SOFT),
        s(BISTRO, "surprise_big_pupils_cat", "……50円!?", item=SOFT, se="explosion_dokaan"),
        s(BISTRO, "confused_i_dont_know_cat", "自販機のジュースより\n安い", item=SOFT),
        s(BISTRO, "read_book_orange_kitten", "今は豆乳でつくった\nプラントベースらしい", item=SOFT),
        s(BISTRO, "eat_pop_cat", "ペロッ", item=SOFT),
        s(BISTRO, "happy_girlfriend_dance_cat", "……普通に\n美味しい", item=SOFT, se="pinpoon_correct"),
        s(BISTRO, "happy_chipi_chapa_cat", "50円でこれは\n反則だろ", item=SOFT),
        s(BISTRO, "sleepy_old_memories_cat", "ベンチに座って\nゆっくり食べる"),
        s(BISTRO, "realize_wet_cat_stare", "食べ終わって\nふと顔を上げる"),
        s(BISTRO, "stare_interviewer_cat", "周りは\n家族連ればかり"),
        s(BISTRO, "peek_what_happen_cat", "子どもが\nサメのぬいぐるみを抱いている"),
        s(BISTRO, "stare_big_eyes_tabby_kitten", "お父さんが\n大きな箱をカートで運んでいる"),
        s(BISTRO, "blank_black_cat_zoning_out", "俺は\nマットレス1枚"),
        s(BISTRO, "sad_looking_away_tabby", "……"),
        s(BISTRO, "think_chin_paw_orange_cat", "でも\nだれも俺を変な目で見ない"),
        s(BISTRO, "sleepy_old_memories_cat", "ひとりでも\nゆっくり見て回れて"),
        s(BISTRO, "happy_hamster_open_arms", "50円で\nソフトクリームが食べられる"),
        s(BISTRO, "sad_banana_cat_cry", "こんな独り身でも\n受け入れてくれる", se="sparkle_kirakira_01",
          bgm={"file": os.path.join(L.BGM, "手紙のさよなら.mp3"), "gain": -14, "fade": 1.0}),
        s(BISTRO, "sad_banana_cat_cry", "IKEAは\nいい場所だ"),
        # ---- 帰り道 ----
        s(ROAD, "leave_cat_leaves_home", "マットレスを抱えて\n帰り道", se="whoosh_shu"),
        s(ROAD, "despair_dramatic_kitten", "……重い"),
        s(ROAD, "sad_banana_cat_cry", "なぜか\n涙が止まらない"),
        s(ROAD, "sad_looking_away_tabby", "重いからなのか\nそれとも"),
        s(ROAD, "blank_black_cat_zoning_out", "考えるのを\nやめた"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nマットレスを広げる", se="whoosh_shu"),
        s(ROOM_N, "happy_hamster_open_arms", "……ふかふかだ"),
        s(ROOM_N, "sleepy_old_memories_cat", "丁寧な暮らしの\n第一歩"),
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "まわりには\n脱ぎっぱなしの服と\nコンビニの袋"),
        s(ROOM_N, "realize_wet_cat_stare", "……次は\n収納を買いに行こう"),
        s(ROOM_N, "excited_hodomoe_city_cat", "またミートボールと\n50円のソフトクリームを\n食べに", se="pikon", dur=3.8),
        J.end_card(),
    ]


def place(cs):
    for c in cs:
        if c.get("text"):   # スシローと同じ：字幕にカギかっこはつけない
            c["text"] = c["text"].replace("「", "").replace("」", "")
    return cs


if __name__ == "__main__":
    cs = place(cuts())
    if os.environ.get("LEN"):
        print(len(cs), round(sum(c["dur"] for c in cs), 1))
    else:
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_07_ikea.mp4"), os.path.join(J.HERE, "out", "jidaraku_07_ikea_preview"))
