"""自堕落シリーズ #17：30代独身男、ひとりで釣り堀（11/12 ユーザー指定：候補5番・仕事の理不尽の回想を入れる）。約8分。

python3 catmeme/jidaraku_17_tsuribori.py → out/jidaraku_17_tsuribori.mp4
- 流れ：月曜の会社で理不尽が重なる → 日曜の朝、ひとりで郊外の釣り堀へ → 竿を借りてエサをつける → 全然釣れない間に回想
  （上司の急な方針変更・事務の人の無茶なお願い・後輩が指示を聞かずに独自のやり方でミス）→ となりの常連さん・子ども連れ →
  ついに大物 → 釣った魚をその場で塩焼き → 夕方、帰り道
- 釣り堀の一般的な話：竿とエサは貸し出しが多い／時間制の料金／釣った魚はその場で焼いてもらえる所もある（店名は出さない）
- 回想の人物は「上司」「事務の人」「後輩」。性別や見た目でからかわない（理不尽なのは頼み方・やり方）。実在の会社や人ではない
- ベンチマーク3チャンネルに釣り堀の回はない（11/12 確認）
- 写真は backgrounds/jidaraku/17_tsuribori に置く。届くまでは手もちのイラストで仮に（ほかの店の写真は使わない）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "17_tsuribori"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku", "01_yakiniku")]
ROOM, ROOM_N, ROAD, OFFICE, GATE, POND, POND_E = ("j01_room", "j07_room_night", "bg26_rural_road", "bg25_office_desk",
                                                  "tb01_gate", "tb02_pond", "tb03_pond_evening")
J.STANDIN.update({GATE: "bg107_lake_shore", POND: "bg106_lake_calm", POND_E: "bg110_lake_sunset"})
J.HOLD = 4
J.LOOPS = 1
J.SUB_STYLE = "glow"
MORNING = os.path.join(L.BGM, "Morning.mp3")
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
ROD, BAIT, FISH, SALT, BEER = "f_rod", "f_bait", "f_fish", "f_shioyaki", "f_beer"


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 平日の会社 ----
        s(OFFICE, "work_typing_cat", "水曜日の午後3時", bgm={"file": LOFI, "gain": -12}),
        s(OFFICE, "stare_tabby_wide_eyes_cat", "先週\n上司に言われた通り\n作った資料"),
        s(OFFICE, "stare_interviewer_cat", "あれ\nなんで青色なの？", se="pi"),
        s(OFFICE, "surprise_big_pupils_cat", "青で\nって言われました"),
        s(OFFICE, "stare_interviewer_cat", "今は赤の\n気分なんだよね"),
        s(OFFICE, "scream_standing_marmot", "気分!?", se="explosion_chudoon"),
        s(OFFICE, "work_typing_cat", "30枚の資料を\n全部赤にする"),
        s(OFFICE, "stare_interviewer_cat", "うーん\nやっぱり\n青のほうがいいかな"),
        s(OFFICE, "blank_black_cat_zoning_out", "元のやつ\nありますけど"),
        s(OFFICE, "stare_interviewer_cat", "じゃあ\n間をとって\n紫で"),
        s(OFFICE, "despair_dramatic_kitten", "間を\nとらないでほしい"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nソファに沈む", se="whoosh_shu"),
        s(ROOM_N, "scream_phone_orange_cat", "スマホを見る"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "釣り堀の動画"),
        s(ROOM_N, "sleepy_old_memories_cat", "おじさんが\n池の前で\nじっと座っている"),
        s(ROOM_N, "realize_wet_cat_stare", "誰にも\n何も言われていない"),
        s(ROOM_N, "think_chin_paw_orange_cat", "うらやましい"),
        s(ROOM_N, "angry_aiming_cat", "俺も\nじっと座りたい"),
        s(ROOM_N, "excited_hodomoe_city_cat", "日曜は\n釣り堀だ", se="shine_kiraan_maou"),
        s(ROOM_N, "work_typing_cat", "竿もエサも\n借りられるらしい"),
        s(ROOM_N, "money_counting_orange_cat", "道具ゼロ円で\nはじめられる"),
        s(ROOM_N, "rizz_cat_rizz", "コスパ最強の\n現実逃避だ"),
        s(OFFICE, "sleepy_old_memories_cat", "金曜日の夕方", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(OFFICE, "stare_interviewer_cat", "日曜\nゴルフの人数が\n1人足りなくてさ"),
        s(OFFICE, "surprise_big_pupils_cat", "日曜は\n予定がありまして"),
        s(OFFICE, "stare_interviewer_cat", "なんの予定？"),
        s(OFFICE, "sad_looking_away_tabby", "……釣り堀です"),
        s(OFFICE, "stare_interviewer_cat", "朝6時のゴルフのあとで\n行けるね"),
        s(OFFICE, "scream_standing_marmot", "行けない", se="explosion_chudoon"),
        s(OFFICE, "call_customer_service_cat", "親戚の用事と\nいうことにした"),
        s(OFFICE, "blank_black_cat_zoning_out", "親戚は\n池にいる魚だ"),
        # ---- 出発・到着 ----
        s(ROAD, "drive_driving_cat", "日曜日の朝\n郊外へ向かう", se="whoosh_shu", bgm={"file": MORNING, "gain": -12, "fade": 0.8}),
        s(ROAD, "sleepy_old_memories_cat", "田んぼの間の\n一本道"),
        s(GATE, "leave_cat_leaves_home", "釣り堀に到着", se="gong_dora_jaan"),
        s(GATE, "surprise_big_pupils_cat", "思ったより\n人がいる"),
        s(GATE, "peek_what_happen_cat", "家族づれ\nカップル\n常連のおじさん"),
        s(GATE, "stare_tabby_wide_eyes_cat", "受付で\nひとり3時間で"),
        s(GATE, "stare_interviewer_cat", "竿とエサ\nおつけしますね"),
        s(GATE, "happy_hamster_open_arms", "店の人が\nやさしい"),
        s(GATE, "joy_happy_happy_happy_cat", "誰にも\n文句を言われない\n3時間", se="pikon"),
        # ---- 釣りはじめ ----
        s(POND, "work_typing_cat", "池のはしに\n座る", item=ROD, bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(POND, "read_book_orange_kitten", "エサの練りエサを\n丸めて\n針につける", item=BAIT),
        s(POND, "huh_huh_cat", "手が\nくさい", item=BAIT, se="question_mark_pop_confused_huh"),
        s(POND, "angry_aiming_cat", "えいっ", item=ROD, se="whoosh_shu"),
        s(POND, "despair_dramatic_kitten", "うしろの木に\nひっかかった", item=ROD, se="explosion_chudoon"),
        s(POND, "sad_looking_away_tabby", "店の人に\nとってもらう", item=ROD),
        s(POND, "angry_aiming_cat", "もう一度\nえいっ", item=ROD),
        s(POND, "smug_squint_bicolor_cat", "ぽちゃん", item=ROD, se="pikon"),
        s(POND, "stare_lying_tabby_cat", "ウキを\n見つめる", item=ROD),
        s(POND, "stare_lying_tabby_cat", "……", item=ROD),
        s(POND, "blank_black_cat_zoning_out", "5分たっても\n動かない", item=ROD),
        s(POND, "think_chin_paw_orange_cat", "動かないウキを\n見ていると", item=ROD),
        s(POND, "sleepy_old_memories_cat", "なぜか\n会社を\n思い出す", item=ROD),
        # ---- 回想1 事務の人 ----
        s(OFFICE, "sleepy_old_memories_cat", "あれは\n月末の夕方", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(OFFICE, "talk_orange_white_sitting_cat", "すみませーん\nこの申請書\n今から30分で\n書きなおしてください"),
        s(OFFICE, "surprise_big_pupils_cat", "どこが\nだめでしたか"),
        s(OFFICE, "talk_orange_white_sitting_cat", "全部\n手書きで\nお願いします"),
        s(OFFICE, "huh_huh_cat", "パソコンで\n出してくださいって\n言われました", se="question_mark_pop_confused_huh"),
        s(OFFICE, "talk_orange_white_sitting_cat", "今月から\n手書きです\n黒のボールペンで"),
        s(OFFICE, "work_typing_cat", "必死で\n手書きする"),
        s(OFFICE, "talk_orange_white_sitting_cat", "あ\n消せるペンは\nだめですよ"),
        s(OFFICE, "despair_dramatic_kitten", "全部\n消せるペンで\n書いてた"),
        s(OFFICE, "calm_black_face_sheep", "もう1枚\n最初から"),
        s(POND, "stare_lying_tabby_cat", "ウキは\nまだ動かない", item=ROD),
        s(POND, "sad_black_dog", "あの日の\n申請書と\n同じくらい\n進まない", item=ROD),
        # ---- 常連さん ----
        s(POND, "peek_what_happen_cat", "となりの常連さんが\nまた釣った", item=ROD),
        s(POND, "stare_tabby_wide_eyes_cat", "これで5匹目", item=ROD),
        s(POND, "stare_interviewer_cat", "兄ちゃん\nエサ\nでかすぎるよ", item=BAIT),
        s(POND, "surprise_big_pupils_cat", "そうなんですか", item=BAIT),
        s(POND, "stare_interviewer_cat", "小豆くらいに\n小さく丸めな", item=BAIT),
        s(POND, "happy_hamster_open_arms", "ていねいな\n指示だ", item=BAIT),
        s(POND, "think_chin_paw_orange_cat", "指示といえば", item=BAIT),
        # ---- 回想2 後輩 ----
        s(OFFICE, "sleepy_old_memories_cat", "後輩に\nお客さんへの\nメールを頼んだ日"),
        s(OFFICE, "work_typing_cat", "この文章を\nそのまま送ってね\nと伝えた"),
        s(OFFICE, "stare_interviewer_cat", "わかりました！"),
        s(OFFICE, "peek_what_happen_cat", "30分後"),
        s(OFFICE, "stare_interviewer_cat", "かたい文章だったので\nちょっと\nやわらかくしました！"),
        s(OFFICE, "surprise_big_pupils_cat", "見せて", se="pi"),
        s(OFFICE, "scream_phone_orange_cat", "お世話になっております\nのあとに\n顔文字"),
        s(OFFICE, "scream_standing_marmot", "相手は\n取引先の社長", se="explosion_chudoon"),
        s(OFFICE, "stare_interviewer_cat", "親しみやすさが\n大事だと思って！"),
        s(OFFICE, "call_customer_service_cat", "おわびの電話は\n俺がかけた"),
        s(OFFICE, "stare_interviewer_cat", "次からは\n絵文字にします！"),
        s(OFFICE, "blank_black_cat_zoning_out", "そういうことじゃない"),
        s(POND, "read_book_orange_kitten", "エサを\n小豆くらいに\n丸める", item=BAIT),
        s(POND, "smug_squint_bicolor_cat", "俺は\n言われた通りに\nやる人間だ", item=BAIT),
        s(POND, "angry_aiming_cat", "ぽちゃん", item=ROD, se="pikon"),
        s(POND, "surprise_big_pupils_cat", "ウキが\nしずんだ", item=ROD, se="shine_kiraan_maou"),
        s(POND, "angry_shooting_cat", "今だ", item=ROD, se="explosion_dokaan"),
        s(POND, "despair_dramatic_kitten", "エサだけ\nとられた", item=ROD),
        s(POND, "read_book_orange_kitten", "もう一度\nエサをつける", item=BAIT),
        s(POND, "despair_dramatic_kitten", "またとられた", item=ROD),
        s(POND, "sad_black_dog", "これで\n4回目", item=ROD),
        s(POND, "sad_banana_cat_cry", "魚にまで\nいいように\n使われている", item=ROD),
        # ---- 子ども ----
        s(POND, "peek_what_happen_cat", "反対どなりに\n親子がきた", item=ROD, bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(POND, "stare_interviewer_cat", "おじさん\n釣れた？", item=ROD),
        s(POND, "sad_looking_away_tabby", "おじさん\nゼロ匹", item=ROD),
        s(POND, "stare_interviewer_cat", "ぼく\nもう3匹", item=ROD),
        s(POND, "blank_black_cat_zoning_out", "負けている", item=ROD),
        s(POND, "think_chin_paw_orange_cat", "負けているといえば", item=ROD),
        # ---- 回想3 上司 ----
        s(OFFICE, "sleepy_old_memories_cat", "上司と\nお客さんの会社へ\n行った日", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(OFFICE, "stare_interviewer_cat", "今日の説明\n全部君にまかせるから"),
        s(OFFICE, "surprise_big_pupils_cat", "聞いてないです"),
        s(OFFICE, "stare_interviewer_cat", "今言った"),
        s(OFFICE, "work_typing_cat", "必死で説明する"),
        s(OFFICE, "joy_happy_happy_happy_cat", "お客さんが\nうなずいてくれた"),
        s(OFFICE, "stare_interviewer_cat", "いやあ\n私が考えた\n企画でして"),
        s(OFFICE, "scream_standing_marmot", "手柄だけ\n持っていかれた", se="explosion_chudoon"),
        s(OFFICE, "sleepy_old_memories_cat", "そして\n帰りの電車"),
        s(OFFICE, "stare_interviewer_cat", "さっきの数字\n1つ間違ってたよ\n君のミスね"),
        s(OFFICE, "despair_dramatic_kitten", "ミスだけ\nこっちに来た"),
        s(OFFICE, "calm_black_face_sheep", "手柄は上司\nミスは俺"),
        # ---- 大物 ----
        s(POND, "stare_lying_tabby_cat", "深呼吸する", item=ROD, bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(POND, "read_book_orange_kitten", "エサは小さく", item=BAIT),
        s(POND, "think_chin_paw_orange_cat", "ウキが\nしずんでも\n一瞬待つ", item=ROD),
        s(POND, "angry_aiming_cat", "ぽちゃん", item=ROD),
        s(POND, "stare_lying_tabby_cat", "……", item=ROD),
        s(POND, "surprise_big_pupils_cat", "ググッ", item=ROD, se="pi"),
        s(POND, "angry_shooting_cat", "今だ", item=ROD, se="explosion_dokaan"),
        s(POND, "scream_standing_marmot", "重い", item=ROD),
        s(POND, "despair_dramatic_kitten", "竿が\nしなる", item=ROD),
        s(POND, "stare_interviewer_cat", "兄ちゃん\nあわてるな", item=ROD),
        s(POND, "stare_interviewer_cat", "おじさん\nがんばれ", item=ROD),
        s(POND, "angry_aiming_cat", "上司の分", item=ROD),
        s(POND, "angry_aiming_cat", "事務の人の分", item=ROD),
        s(POND, "angry_aiming_cat", "後輩の分", item=ROD),
        s(POND, "showoff_gojo_cosplay_cat", "釣れた", item=FISH, se="gong_dora_jaan"),
        s(POND, "surprise_big_pupils_cat", "30センチの\nニジマス", item=FISH),
        s(POND, "happy_girlfriend_dance_cat", "常連さんと\n子どもが\n拍手してくれた", item=FISH),
        s(POND, "realize_wet_cat_stare", "最後に\nほめられたのは\nいつだったか", item=FISH),
        s(POND, "happy_hamster_open_arms", "会社では\n一度もない", item=FISH),
        s(POND, "rizz_cat_rizz", "魚は\n努力を\n裏切らない", item=FISH),
        # ---- 塩焼き ----
        s(POND, "money_counting_orange_cat", "釣った魚は\nその場で\n塩焼きにしてもらえる", item=SALT),
        s(POND, "stare_tabby_wide_eyes_cat", "15分待つ", item=SALT),
        s(POND, "sulk_hungry_cat", "においで\n腹が鳴る", item=SALT, se="pi"),
        s(POND, "surprise_big_pupils_cat", "きた", item=SALT, se="shine_kiraan_maou"),
        s(POND, "eat_crunchy_cat_luna", "パリッ", item=SALT, se="pikon"),
        s(POND, "happy_girlfriend_dance_cat", "うまい", item=SALT),
        s(POND, "eat_pop_cat", "皮がパリパリ\n身がふわふわ", item=SALT),
        s(POND, "happy_hamster_open_arms", "自分で釣ると\n3倍うまい", item=SALT),
        s(POND, "eat_crunchy_cat_luna", "ノンアルビールを\nプシュッ", item=BEER, se="drink_gulp_gokugoku_thirsty_chug"),
        s(POND, "sleepy_sleepy_cat", "車なので\nノンアルだ", item=BEER),
        s(POND, "smug_squint_bicolor_cat", "決まりは守る\n言われた通りに", item=BEER),
        s(POND, "stare_interviewer_cat", "おじさん\nそれ\nぼくのより大きい", item=SALT),
        s(POND, "sad_looking_away_tabby", "しっぽだけ\nわけてあげた", item=SALT),
        s(POND, "joy_happy_happy_happy_cat", "ちゃんと\nお礼を言ってくれた", item=SALT),
        s(POND, "realize_wet_cat_stare", "後輩より\nしっかりしている", item=SALT),
        s(POND, "stare_lying_tabby_cat", "おなかいっぱいで\nぼんやりする", item=ROD),
        s(POND, "think_chin_paw_orange_cat", "来月\n有給をとって\nまた来ようか", item=ROD),
        s(OFFICE, "sleepy_old_memories_cat", "そういえば\n前に有給を\n出したとき", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(OFFICE, "talk_orange_white_sitting_cat", "すみませーん\nその日は\nだめです"),
        s(OFFICE, "surprise_big_pupils_cat", "なにか\nありましたっけ"),
        s(OFFICE, "talk_orange_white_sitting_cat", "わたしが\n休むので"),
        s(OFFICE, "huh_huh_cat", "関係あります？", se="question_mark_pop_confused_huh"),
        s(OFFICE, "talk_orange_white_sitting_cat", "わたしの仕事を\nお願いしたいので"),
        s(OFFICE, "despair_dramatic_kitten", "休むどころか\n仕事が増えた"),
        s(OFFICE, "stare_interviewer_cat", "先輩\nぼくも\nその日休みます！"),
        s(OFFICE, "scream_standing_marmot", "後輩まで\n乗ってきた", se="explosion_chudoon"),
        s(OFFICE, "calm_black_face_sheep", "その日\n席には\n俺ひとり"),
        s(OFFICE, "blank_black_cat_zoning_out", "会社で\nソロキャンプ\nしていた"),
        s(POND, "smug_squint_bicolor_cat", "今日は\n誰の仕事も\nしなくていい", item=ROD),
        s(POND, "happy_hamster_open_arms", "それだけで\nごちそうだ", item=ROD),
        # ---- 夕方 ----
        s(POND_E, "stare_lying_tabby_cat", "夕方になった", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(POND_E, "sleepy_old_memories_cat", "池に\n夕日がうつる"),
        s(POND_E, "think_chin_paw_orange_cat", "3時間\nほぼ座っていただけ"),
        s(POND_E, "calm_black_face_sheep", "なのに\n心が軽い"),
        s(POND_E, "angry_aiming_cat", "最後に\nもう1回だけ", item=ROD),
        s(POND_E, "stare_lying_tabby_cat", "ウキを見つめる", item=ROD),
        s(POND_E, "surprise_big_pupils_cat", "しずんだ", item=ROD, se="pi"),
        s(POND_E, "think_chin_paw_orange_cat", "一瞬\n待つ", item=ROD),
        s(POND_E, "angry_shooting_cat", "今だ", item=ROD, se="explosion_dokaan"),
        s(POND_E, "showoff_gojo_cosplay_cat", "2匹目", item=FISH, se="gong_dora_jaan"),
        s(POND_E, "happy_girlfriend_dance_cat", "もう\n指示は\nいらない", item=FISH),
        s(POND_E, "money_counting_orange_cat", "2匹目は\n持ち帰って\n夜ごはんにする", item=FISH),
        s(POND_E, "stare_interviewer_cat", "兄ちゃん\nまた来なよ"),
        s(POND_E, "happy_hamster_open_arms", "常連さんに\n認められた"),
        s(POND_E, "rizz_cat_rizz", "会社より\nここのほうが\n評価が早い"),
        # ---- 帰り道 ----
        s(ROAD, "drive_driving_cat", "帰り道", se="whoosh_shu", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(ROAD, "sleepy_old_memories_cat", "手から\nまだ\nエサのにおい"),
        s(ROAD, "scream_phone_orange_cat", "スマホが鳴る", se="pi"),
        s(ROAD, "stare_interviewer_cat", "明日の会議\nやっぱり\n緑の資料で"),
        s(ROAD, "blank_black_cat_zoning_out", "……"),
        s(ROAD, "calmdown_dancing_cat", "まあいい"),
        s(ROAD, "smug_squint_bicolor_cat", "ウキを待つのと\n同じだ"),
        s(ROAD, "rizz_cat_rizz", "あわてず\n一瞬待ってから\n動けばいい"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nソファに沈む", se="whoosh_shu"),
        s(ROOM_N, "think_chin_paw_orange_cat", "来週は\n2匹釣りたい"),
        s(ROOM_N, "excited_hodomoe_city_cat", "今週も\nなんとか\nがんばれそうだ", se="pikon", dur=3.8),
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_17_tsuribori.mp4"), os.path.join(J.HERE, "out", "jidaraku_17_tsuribori_preview"))
