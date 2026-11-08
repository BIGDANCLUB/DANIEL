"""自堕落シリーズ #15：30代独身男、ひとりで潮干狩り（11/8 ユーザー指定の流れ・8分ほど）。

python3 catmeme/jidaraku_15_shiohigari.py → out/jidaraku_15_shiohigari.mp4
- 流れ（ユーザー指定）：プロ級の腕前で貝を拾っていく → 大量に拾うが食べきれる量じゃない → 最後は近くの子どもに分ける →
  良いことをしたと満足感 → でも独り身のむなしさ → しかし貝の酒蒸しがうますぎて、酒がむなしさを洗い流す
- 潮干狩りの一般的な話（場所で変わるので数字はぼかす）：潮が大きく引く日の、干潮の前後がねらい目／熊手で砂を浅くかく／
  有料の潮干狩り場は、入場料で網の袋をもらい、その袋に入る分を持ち帰れるところが多い／小さい貝は逃がす／
  持ち帰ったら海水くらいの塩水で砂抜き。暗くして数時間
- ベンチマーク3チャンネルに潮干狩りの回はない（11/8 確認）。子どもや家族をからかわない
- 写真は backgrounds/jidaraku/15_shiohigari に置く。届くまでは手もちのイラストで仮に（ほかの店の写真は使わない）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "15_shiohigari"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku", "01_yakiniku")]
ROOM, ROOM_N, ROAD, BEACH, FLAT = ("j01_room", "j07_room_night", "bg26_rural_road", "sh01_beach", "sh02_flat")
J.STANDIN.update({BEACH: "bg107_lake_shore", FLAT: "bg107_lake_shore"})
J.HOLD = 4
J.LOOPS = 2
J.SUB_STYLE = "glow"
MORNING = os.path.join(L.BGM, "Morning.mp3")
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
KUMADE, ASARI, NET, SAKAMUSHI = "f_kumade", "f_asari", "f_net", "f_sakamushi"


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 決意 ----
        s(ROOM, "sleepy_old_memories_cat", "金曜日の夜\n居酒屋のメニューを\n思い出す", bgm={"file": LOFI, "gain": -12}),
        s(ROOM, "stare_big_eyes_tabby_kitten", "あさりの酒蒸し", item=SAKAMUSHI),
        s(ROOM, "happy_girlfriend_dance_cat", "あれは\nうまかった", item=SAKAMUSHI),
        s(ROOM, "think_chin_paw_orange_cat", "でも\n1皿の貝の数は\nちょっとだけ", item=SAKAMUSHI),
        s(ROOM, "sad_looking_away_tabby", "あさりを\nおなかいっぱい\n食べてみたい", item=SAKAMUSHI),
        s(ROOM, "realize_wet_cat_stare", "……とればいいのか"),
        s(ROOM, "excited_hodomoe_city_cat", "潮干狩りだ", se="shine_kiraan_maou"),
        s(ROOM, "work_typing_cat", "スマホで\n潮見表を調べる"),
        s(ROOM, "read_book_orange_kitten", "潮が大きく引く日の\n干潮の前後が\nねらい目らしい"),
        s(ROOM, "stare_tabby_wide_eyes_cat", "明日の朝が\nちょうどいい"),
        s(ROOM, "money_counting_orange_cat", "ホームセンターで\n熊手と長靴を買う", item=KUMADE),
        s(ROOM, "showoff_gojo_cosplay_cat", "熊手を\n天にかかげる", item=KUMADE, se="gong_dora_jaan"),
        s(ROOM, "sleepy_old_memories_cat", "子どものころ\n家族で\n潮干狩りに行った", item=KUMADE),
        s(ROOM, "happy_chipi_chapa_cat", "父さんは\n貝を見つける\n天才だった", item=KUMADE),
        s(ROOM, "rizz_cat_rizz", "その血が\n俺にも流れている\nはずだ", item=KUMADE),
        s(ROOM, "calm_black_face_sheep", "たぶん", item=KUMADE),
        s(ROOM, "stare_lying_tabby_cat", "クーラーボックスを\n押し入れから出す"),
        s(ROOM, "surprise_big_pupils_cat", "中から\n去年のレシート"),
        s(ROOM, "sad_black_dog", "去年は\n一度も\n使わなかった"),
        s(ROOM, "angry_shooting_cat", "今年は\n使い倒す"),
        s(ROOM, "read_book_orange_kitten", "日焼け止め\n帽子\nタオル"),
        s(ROOM, "think_chin_paw_orange_cat", "あさりを入れる\n海水用の\nペットボトルも"),
        s(ROOM, "calm_black_face_sheep", "準備だけは\nプロ級だ"),
        s(ROOM_N, "sleep_sleeping_cat", "早めに寝る"),
        # ---- 海へ ----
        s(ROAD, "drive_driving_cat", "土曜日の朝\n海へ向かう", se="whoosh_shu", bgm={"file": MORNING, "gain": -12, "fade": 0.8}),
        s(ROAD, "stare_big_eyes_tabby_kitten", "窓をあけると\n潮の香り"),
        s(ROAD, "sleepy_old_memories_cat", "海が\n見えてきた"),
        s(ROAD, "happy_chipi_chapa_cat", "海を見ると\nなぜか\nテンションが上がる"),
        s(ROAD, "stare_tabby_wide_eyes_cat", "駐車場は\nもういっぱい"),
        s(ROAD, "despair_dramatic_kitten", "遠くの駐車場から\n10分歩く"),
        s(BEACH, "leave_cat_leaves_home", "潮干狩り場に到着", se="gong_dora_jaan"),
        s(BEACH, "surprise_big_pupils_cat", "潮が引いて\n海がずっと\n遠くにある"),
        s(BEACH, "stare_interviewer_cat", "家族づれが\nいっぱい"),
        s(BEACH, "peek_what_happen_cat", "子どもたちが\nバケツを持って\n走りまわっている"),
        s(BEACH, "sad_black_dog", "30代の男1人は\n俺だけだ"),
        s(BEACH, "money_counting_orange_cat", "受付で\n入場料を払う", item=NET),
        s(BEACH, "read_book_orange_kitten", "網の袋をもらって\nこの袋に入る分だけ\n持って帰れる", item=NET),
        s(BEACH, "think_chin_paw_orange_cat", "小さい貝は\n逃がしてあげる\nのがルール", item=NET),
        s(BEACH, "stare_big_eyes_tabby_kitten", "長靴にはきかえる", item=NET),
        s(BEACH, "think_chin_paw_orange_cat", "ズボンの\nすそをまくる", item=NET),
        s(BEACH, "calm_black_face_sheep", "すねが\n真っ白だ", item=NET),
        s(BEACH, "sad_looking_away_tabby", "日に当たって\nいなかった証拠だ", item=NET),
        s(BEACH, "angry_aiming_cat", "この袋を\nいっぱいにする", item=NET, se="gong_match_start"),
        # ---- 開始 ----
        s(FLAT, "walk_approaching_orange_cat", "干潟に出る", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(FLAT, "stare_tabby_wide_eyes_cat", "まわりの人は\nしゃがんで\nあちこち掘っている"),
        s(FLAT, "think_chin_paw_orange_cat", "俺は\nすぐには掘らない"),
        s(FLAT, "read_book_orange_kitten", "砂の表面を見る"),
        s(FLAT, "stare_big_eyes_tabby_kitten", "小さな穴が\n2つならんでいる"),
        s(FLAT, "smug_squint_bicolor_cat", "貝が\n息をしているあとだ"),
        s(FLAT, "showoff_gojo_cosplay_cat", "ここだ", se="explosion_chudoon"),
        s(FLAT, "work_typing_cat", "熊手で\n浅くかく", item=KUMADE),
        s(FLAT, "eat_pop_cat", "カチッ", item=ASARI, se="pikon"),
        s(FLAT, "surprise_big_pupils_cat", "あさりだ", item=ASARI),
        s(FLAT, "happy_hamster_open_arms", "1発目で\n当てた", item=ASARI),
        s(FLAT, "rizz_cat_rizz", "やはり\n父さんの血だ", item=ASARI),
        s(FLAT, "stare_tabby_wide_eyes_cat", "まわりを見る", item=ASARI),
        s(FLAT, "peek_what_happen_cat", "家族は\nまだ1個も\nとれていない", item=ASARI),
        s(FLAT, "smug_squint_bicolor_cat", "ふっ", item=ASARI),
        s(FLAT, "showoff_gojo_cosplay_cat", "ここからは\nプロの時間だ", item=ASARI, se="gong_match_start"),
        # ---- プロ級 ----
        s(FLAT, "cocky_dj_cat", "カチッ\nカチッ", item=ASARI, se="pikon"),
        s(FLAT, "dance_wop_cat", "掘るたびに\n出てくる", item=ASARI),
        s(FLAT, "read_book_orange_kitten", "あさりは\nかたまって\nいることが多い", item=ASARI),
        s(FLAT, "smug_squint_bicolor_cat", "1個見つけたら\nそのまわりを\nていねいに", item=ASARI),
        s(FLAT, "angry_shooting_cat", "熊手さばきが\n止まらない", item=KUMADE),
        s(FLAT, "dance_edm_cat", "カチッ\nカチッ\nカチッ", item=ASARI),
        s(FLAT, "peek_what_happen_cat", "となりの家族が\nこっちを見ている", item=ASARI),
        s(FLAT, "stare_interviewer_cat", "あのおじさん\nすごい", item=ASARI),
        s(FLAT, "sad_looking_away_tabby", "おじさん……", item=ASARI),
        s(FLAT, "calmdown_dancing_cat", "だが\n今は職人だ", item=ASARI),
        s(FLAT, "think_chin_paw_orange_cat", "小さいのは\nそっと\n砂にもどす", item=ASARI),
        s(FLAT, "happy_chipi_chapa_cat", "大きくなって\nまた会おう", item=ASARI),
        s(FLAT, "showoff_gojo_cosplay_cat", "プロは\n未来も\n考えている", item=ASARI),
        s(FLAT, "despair_dramatic_kitten", "腰が\n痛い", se="pi"),
        s(FLAT, "sleepy_sleepy_cat", "ずっと\nしゃがんでいるからだ"),
        s(FLAT, "stare_lying_tabby_cat", "1回立って\n腰をのばす"),
        s(FLAT, "joy_happy_happy_happy_cat", "見わたすと\n水平線と\n干潟", se="shine_kiraan_maou"),
        s(FLAT, "sleepy_old_memories_cat", "風が気持ちいい"),
        s(FLAT, "angry_aiming_cat", "職人に\n休みはない", se="gong_match_start"),
        s(FLAT, "eat_crunchy_cat_luna", "カチッ\nカチッ", item=ASARI),
        s(FLAT, "surprise_big_pupils_cat", "大きいハマグリまで\n出てきた", item=ASARI, se="explosion_chudoon"),
        s(FLAT, "happy_girlfriend_dance_cat", "今日は\n大漁だ", item=ASARI),
        s(FLAT, "stare_tabby_wide_eyes_cat", "砂の中から\nカニが出てきた"),
        s(FLAT, "surprise_big_pupils_cat", "横歩きで\n逃げていく"),
        s(FLAT, "happy_chipi_chapa_cat", "カニにも\n休日がある"),
        s(FLAT, "peek_what_happen_cat", "ヤドカリもいる"),
        s(FLAT, "sleepy_old_memories_cat", "家を背負って\n歩いている"),
        s(FLAT, "sad_black_dog", "俺は\n家のローンもない\n家もない"),
        s(FLAT, "rizz_cat_rizz", "……掘ろう"),
        s(FLAT, "despair_dramatic_kitten", "長靴に\n水が入った", se="pi"),
        s(FLAT, "sad_looking_away_tabby", "歩くたびに\nぐちゅっ"),
        s(FLAT, "calmdown_dancing_cat", "職人は\n気にしない"),
        # ---- 大量 ----
        s(FLAT, "stare_lying_tabby_cat", "気がつけば\n2時間", item=ASARI),
        s(FLAT, "sulk_hungry_cat", "腹が減った", item=ASARI),
        s(FLAT, "eat_pop_cat", "コンビニの\nおにぎりを\n干潟で食べる", item=ASARI),
        s(FLAT, "happy_girlfriend_dance_cat", "潮風で\nしょっぱさが\nちょうどいい", item=ASARI),
        s(FLAT, "angry_aiming_cat", "後半戦だ", item=ASARI, se="gong_match_start"),
        s(FLAT, "dance_edm_cat", "カチッ\nカチッ\nカチッ", item=ASARI),
        s(FLAT, "stare_big_eyes_tabby_kitten", "網の袋を見る", item=NET),
        s(FLAT, "scream_standing_marmot", "パンパン", item=NET, se="explosion_dokaan"),
        s(FLAT, "showoff_gojo_cosplay_cat", "袋が\nはち切れそうだ", item=NET),
        s(FLAT, "money_counting_orange_cat", "持ってみる", item=NET),
        s(FLAT, "despair_dramatic_kitten", "重い", item=NET),
        s(FLAT, "think_chin_paw_orange_cat", "……ちょっと待て", item=NET),
        s(FLAT, "realize_wet_cat_stare", "これを\n1人で\n食べるのか", item=NET),
        s(FLAT, "read_book_orange_kitten", "あさりは\n日持ちしない", item=NET),
        s(FLAT, "sad_looking_away_tabby", "冷凍庫には\n氷とアイスしか\n入らない", item=NET),
        s(FLAT, "blank_black_cat_zoning_out", "どう考えても\n食べきれない量だ", item=NET),
        s(FLAT, "sad_black_dog", "取りすぎた", item=NET),
        s(FLAT, "huh_huh_cat", "プロは\n引き際を\n知らなかった", item=NET),
        # ---- 子どもに分ける ----
        s(FLAT, "think_chin_paw_orange_cat", "袋から\n少し出すか"),
        s(FLAT, "stare_lying_tabby_cat", "でも\nせっかくとったのに\n海にもどすのも\nもったいない"),
        s(FLAT, "blank_black_cat_zoning_out", "どうしよう"),
        s(FLAT, "peek_what_happen_cat", "となりで\n小さな男の子が\n掘っている"),
        s(FLAT, "stare_interviewer_cat", "1個も\nとれないよー"),
        s(FLAT, "sleepy_old_memories_cat", "バケツは\n空っぽだ"),
        s(FLAT, "think_bike_front_seat_cat", "子どものころの\n俺を思い出す"),
        s(FLAT, "happy_chipi_chapa_cat", "あのとき\n父さんが\n貝を分けてくれた"),
        s(FLAT, "rizz_cat_rizz", "今度は\n俺の番だ"),
        s(FLAT, "meow_ragdoll_chubby_cat", "よかったら\nこれ\nどうぞ", item=NET),
        s(FLAT, "surprise_big_pupils_cat", "男の子の目が\nかがやく", item=ASARI),
        s(FLAT, "stare_interviewer_cat", "いいの!?\nありがとう！", item=ASARI),
        s(FLAT, "joy_happy_happy_happy_cat", "お母さんも\n何度も\n頭を下げてくれた", item=ASARI),
        s(FLAT, "happy_hamster_open_arms", "コツも\n教えてあげる", item=ASARI),
        s(FLAT, "read_book_orange_kitten", "穴が2つ\nならんでいるところを\n浅くかくんだよ", item=KUMADE),
        s(FLAT, "eat_pop_cat", "カチッ", item=ASARI, se="pikon"),
        s(FLAT, "stare_interviewer_cat", "とれたー！", item=ASARI),
        s(FLAT, "dance_three_kittens", "男の子が\nとびはねている", item=ASARI),
        s(FLAT, "happy_girlfriend_dance_cat", "いいことをした", se="shine_kiraan_maou"),
        s(FLAT, "joy_happy_happy_happy_cat", "胸のあたりが\nあたたかい"),
        s(FLAT, "showoff_gojo_cosplay_cat", "今日の俺は\nヒーローだ"),
        s(FLAT, "stare_interviewer_cat", "おじさん\nありがとう！\nバイバーイ！"),
        s(FLAT, "wave_waving_cat", "手をふる"),
        s(FLAT, "sleepy_old_memories_cat", "父さんも\nこんな気持ち\nだったのかな"),
        s(FLAT, "sad_banana_cat_cry", "今度\n父さんに\n電話しよう"),
        # ---- むなしさ ----
        s(FLAT, "stare_big_eyes_tabby_kitten", "家族が\n帰っていく", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(FLAT, "peek_what_happen_cat", "お父さんが\n男の子を\n肩車している"),
        s(FLAT, "sleepy_old_memories_cat", "お母さんが\nバケツを持っている"),
        s(FLAT, "think_chin_paw_orange_cat", "俺には\n肩車する子どもも\nバケツを持つ人も\nいない"),
        s(FLAT, "sad_looking_away_tabby", "潮が\n満ちてくる"),
        s(FLAT, "blank_black_cat_zoning_out", "夕日の干潟に\n1人"),
        s(FLAT, "sad_banana_cat_cry", "独り身の\nむなしさが\n押し寄せてくる", se="pi"),
        s(FLAT, "calm_black_face_sheep", "潮といっしょに"),
        s(FLAT, "stare_lying_tabby_cat", "網の袋を見る", item=NET),
        s(FLAT, "think_bike_front_seat_cat", "まだ\n半分残っている", item=NET),
        s(FLAT, "rizz_cat_rizz", "……帰ろう\nあさりが待っている", item=NET),
        s(FLAT, "despair_dramatic_kitten", "潮が\nもうひざまで来た", se="pi"),
        s(FLAT, "scream_standing_marmot", "あわてて\n岸にもどる"),
        s(BEACH, "sleepy_sleepy_cat", "水道で\n長靴の砂を落とす"),
        s(BEACH, "stare_lying_tabby_cat", "砂が\nどこまでも\n出てくる"),
        # ---- 帰宅・砂抜き ----
        s(ROAD, "drive_driving_cat", "帰りの車", se="whoosh_shu", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(ROAD, "sleepy_sleepy_cat", "腰が\n座席に\nくっついている"),
        s(ROOM, "work_typing_cat", "家に着いて\nすぐに砂抜き", item=ASARI),
        s(ROOM, "read_book_orange_kitten", "海水くらいの\n塩水につけて\n暗くして\n数時間", item=ASARI),
        s(ROOM, "stare_big_eyes_tabby_kitten", "新聞紙を\nかぶせる", item=ASARI),
        s(ROOM, "peek_what_happen_cat", "そっと\nのぞく", item=ASARI),
        s(ROOM, "surprise_big_pupils_cat", "あさりが\n舌を出している", item=ASARI),
        s(ROOM, "happy_chipi_chapa_cat", "ピュッと\n水をふいた", item=ASARI, se="pikon"),
        s(ROOM, "joy_happy_happy_happy_cat", "生きている", item=ASARI),
        s(ROOM, "sad_black_dog", "家に\n話し相手ができた", item=ASARI),
        s(ROOM, "calm_black_face_sheep", "数時間後に\n食べるけど", item=ASARI),
        s(ROOM, "work_typing_cat", "スマホで\n酒蒸しの\n作り方を調べる"),
        s(ROOM, "read_book_orange_kitten", "あさり\n酒\nにんにく\nバター"),
        s(ROOM, "stare_big_eyes_tabby_kitten", "冷蔵庫を見る"),
        s(ROOM, "joy_happy_happy_happy_cat", "日本酒は\nいつでもある"),
        s(ROOM, "sad_black_dog", "それが\n独身の\n冷蔵庫だ"),
        s(ROOM, "sleep_sleeping_cat", "待っているあいだに\nうたた寝"),
        # ---- 酒蒸し ----
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "夜7時\n目が覚めた", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(ROOM_N, "angry_aiming_cat", "酒蒸しを作る", item=SAKAMUSHI, se="gong_match_start"),
        s(ROOM_N, "work_typing_cat", "フライパンに\nあさりと\nにんにく", item=SAKAMUSHI),
        s(ROOM_N, "cocky_dj_cat", "日本酒を\nどぼどぼ", item=SAKAMUSHI),
        s(ROOM_N, "think_chin_paw_orange_cat", "ふたをして\n待つ", item=SAKAMUSHI),
        s(ROOM_N, "surprise_big_pupils_cat", "パカッ\nパカッ", item=SAKAMUSHI, se="pikon"),
        s(ROOM_N, "happy_girlfriend_dance_cat", "貝が\n次々と\n口を開ける", item=SAKAMUSHI),
        s(ROOM_N, "smug_squint_bicolor_cat", "仕上げに\nバターと\nしょうゆを少し", item=SAKAMUSHI),
        s(ROOM_N, "showoff_gojo_cosplay_cat", "あさりの酒蒸し\n完成", item=SAKAMUSHI, se="gong_dora_jaan"),
        s(ROOM_N, "stare_lying_tabby_cat", "大きなお皿に\nあさりの山", item=SAKAMUSHI),
        s(ROOM_N, "sad_black_dog", "写真を撮る", item=SAKAMUSHI),
        s(ROOM_N, "calm_black_face_sheep", "送る相手は\nいない", item=SAKAMUSHI),
        s(ROOM_N, "think_chin_paw_orange_cat", "冷めないうちに\n食べよう", item=SAKAMUSHI),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "ひと口", item=SAKAMUSHI),
        s(ROOM_N, "eat_crunchy_cat_luna", "ちゅるっ", item=SAKAMUSHI, se="pikon"),
        s(ROOM_N, "scream_standing_marmot", "うますぎる", item=SAKAMUSHI, se="explosion_dokaan"),
        s(ROOM_N, "realize_wet_cat_stare", "ぷりぷりで\n居酒屋の\n何倍も大きい", item=SAKAMUSHI),
        s(ROOM_N, "happy_hamster_open_arms", "自分でとった貝は\nこんなに\nうまいのか", item=SAKAMUSHI),
        s(ROOM_N, "think_chin_paw_orange_cat", "そして\n残ったスープ", item=SAKAMUSHI),
        s(ROOM_N, "cocky_dj_cat", "あさりのだしが\n全部とけている", item=SAKAMUSHI),
        s(ROOM_N, "eat_pop_cat", "日本酒を\nひと口", item=SAKAMUSHI, se="drink_gulp_gokugoku_thirsty_chug"),
        s(ROOM_N, "happy_girlfriend_dance_cat", "合う", item=SAKAMUSHI),
        s(ROOM_N, "dance_wop_cat", "合いすぎる", item=SAKAMUSHI),
        s(ROOM_N, "sleepy_old_memories_cat", "干潟で\n押し寄せてきた\nむなしさ", item=SAKAMUSHI),
        s(ROOM_N, "calmdown_dancing_cat", "酒が\nむなしさを\n洗い流していく", item=SAKAMUSHI, se="shine_kiraan_maou"),
        s(ROOM_N, "sad_banana_cat_cry", "ああ\n満ち潮みたいに", item=SAKAMUSHI),
        s(ROOM_N, "stare_lying_tabby_cat", "あの男の子も\n今ごろ\nあさりを食べているだろうか", item=SAKAMUSHI),
        s(ROOM_N, "joy_happy_happy_happy_cat", "きっと\nうまいと言っている", item=SAKAMUSHI),
        s(ROOM_N, "rizz_cat_rizz", "1人で食べても\nうまいものは\nうまい", item=SAKAMUSHI),
        s(ROOM_N, "scream_phone_orange_cat", "父さんに電話する"),
        s(ROOM_N, "stare_interviewer_cat", "潮干狩り？\n懐かしいな\nとれたか？"),
        s(ROOM_N, "showoff_gojo_cosplay_cat", "袋いっぱい"),
        s(ROOM_N, "stare_interviewer_cat", "さすが\n俺の息子だ"),
        s(ROOM_N, "sad_banana_cat_cry", "子どもに\n半分あげた\nとは言わなかった"),
        s(ROOM_N, "happy_hamster_open_arms", "それは\n俺だけの\nいい話にしておく"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "残りのあさりで\nあさりごはんも作る"),
        s(ROOM_N, "happy_hamster_open_arms", "明日の朝は\nあさりの味噌汁"),
        s(ROOM_N, "think_chin_paw_orange_cat", "腰は\nまだ痛い"),
        s(ROOM_N, "calm_black_face_sheep", "酒が\n腰の痛みまでは\n洗い流してくれない"),
        s(ROOM_N, "excited_hodomoe_city_cat", "次の大潮も\n行こう", se="pikon", dur=3.8),
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_15_shiohigari.mp4"), os.path.join(J.HERE, "out", "jidaraku_15_shiohigari_preview"))
