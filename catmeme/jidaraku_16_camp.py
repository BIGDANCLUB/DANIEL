"""自堕落シリーズ #16：30代独身男、ひとりでソロキャンプ（11/12 ユーザー指定：候補4番・仕事の理不尽の回想を入れる）。約8分。

python3 catmeme/jidaraku_16_camp.py → out/jidaraku_16_camp.mp4
- 流れ：金曜の会社でいろいろあった → 週末はひとりで山へ → テント設営に1時間 → 回想（上司の無茶ぶり・事務の人からの急なお願い・
  後輩が指示を聞かずに独自のやり方でミス）→ たき火を見つめて全部燃やす気持ちに → ひとりメシ（焼き肉・ラーメン）→ 夜の物音にびびる →
  朝のコーヒー → 帰り道・月曜日へ
- ソロキャンプの一般的な話：キャンプ場は予約制のところが多い／たき火は直火禁止の所が多く、たき火台を使う／
  ペグ（くい）を打ってテントを立てる／夜は思ったより冷える。キャンプ場の名前は出さない
- 回想の人物は「上司」「事務の人」「後輩」。性別や見た目でからかわない（理不尽なのは頼み方・やり方）。実在の会社や人ではない
- ベンチマーク3チャンネルにキャンプの回はない（11/12 確認）
- 写真は backgrounds/jidaraku/16_camp に置く。届くまでは手もちのイラストで仮に（ほかの店の写真は使わない）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "16_camp"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku", "01_yakiniku")]
ROOM, ROOM_N, ROAD, OFFICE, SITE, SITE_N, FIRE = ("j01_room", "j07_room_night", "bg26_rural_road", "bg25_office_desk",
                                                  "cp01_site", "cp02_site_night", "cp03_fire")
# 背景 cp01_site・cp02_site_night・cp03_fire はユーザー提供（11/12）
J.HOLD = 4
J.LOOPS = 1
J.SUB_STYLE = "glow"
MORNING = os.path.join(L.BGM, "Morning.mp3")
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
TENT, TAKIBI, MEAT, RAMEN, COFFEE = "f_tent", "f_takibi", "f_meat", "f_ramen", "f_coffee"


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 金曜日の会社 ----
        s(OFFICE, "work_typing_cat", "金曜日の夕方5時", bgm={"file": LOFI, "gain": -12}),
        s(OFFICE, "stare_tabby_wide_eyes_cat", "あと1時間で\n週末だ"),
        s(OFFICE, "stare_interviewer_cat", "ちょっといいかな", se="pi"),
        s(OFFICE, "surprise_big_pupils_cat", "上司だ"),
        s(OFFICE, "talk_orange_white_sitting_cat", "月曜の朝イチの会議\n資料100ページ\nよろしくね"),
        s(OFFICE, "scream_standing_marmot", "今\n金曜の夕方ですけど", se="explosion_chudoon"),
        s(OFFICE, "stare_interviewer_cat", "君なら\nできると思って"),
        s(OFFICE, "despair_dramatic_kitten", "その信頼\nいらない"),
        s(OFFICE, "calm_black_face_sheep", "結局\n夜10時まで残った"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nベッドに倒れこむ", se="whoosh_shu"),
        s(ROOM_N, "scream_phone_orange_cat", "スマホを見る"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "たき火の動画"),
        s(ROOM_N, "sleepy_old_memories_cat", "パチパチと\n燃える音"),
        s(ROOM_N, "realize_wet_cat_stare", "なぜか\n涙が出そうになる"),
        s(ROOM_N, "think_chin_paw_orange_cat", "誰もいない山で"),
        s(ROOM_N, "angry_aiming_cat", "火を見つめたい"),
        s(ROOM_N, "excited_hodomoe_city_cat", "ソロキャンプだ", se="shine_kiraan_maou"),
        s(ROOM_N, "work_typing_cat", "近くのキャンプ場を\n予約する"),
        s(ROOM_N, "money_counting_orange_cat", "テント\nたき火台\nいす"),
        s(ROOM_N, "angry_aiming_cat", "渋沢を\n大量に\n生贄に捧げ", se="explosion_chudoon"),
        s(ROOM_N, "showoff_gojo_cosplay_cat", "いでよ\nキャンプ道具……", se="gong_dora_jaan"),
        s(ROOM_N, "sad_black_dog", "渋沢たちは\n帰ってこなかった"),
        s(ROOM_N, "rizz_cat_rizz", "これは\n心の治療費だ"),
        # ---- 出発 ----
        s(ROAD, "drive_driving_cat", "土曜日の朝\n山へ向かう", se="whoosh_shu", bgm={"file": MORNING, "gain": -12, "fade": 0.8}),
        s(ROAD, "sleepy_old_memories_cat", "窓をあけると\n空気がおいしい"),
        s(ROAD, "stare_tabby_wide_eyes_cat", "スマホの電波が\n1本になる"),
        s(ROAD, "joy_happy_happy_happy_cat", "上司からの連絡が\n届かない場所", se="pikon"),
        s(ROAD, "happy_hamster_open_arms", "最高だ"),
        s(ROAD, "scream_phone_orange_cat", "と思ったら\n電波が1本で\n電話が鳴る", se="pi"),
        s(ROAD, "stare_interviewer_cat", "休みの日に\nごめんね\nあの資料のファイル\nどこだっけ"),
        s(ROAD, "despair_dramatic_kitten", "共有フォルダの\n一番上です"),
        s(ROAD, "stare_interviewer_cat", "フォルダって\nどうやって開くの"),
        s(ROAD, "blank_black_cat_zoning_out", "そこからか"),
        s(ROAD, "call_customer_service_cat", "運転を止めて\n15分説明した"),
        s(ROAD, "sad_black_dog", "山の上で\nパソコン教室"),
        s(ROAD, "calmdown_dancing_cat", "電波が\n0本になった", se="pikon"),
        s(ROAD, "think_chin_paw_orange_cat", "そういえば\n山登りが趣味の\nお医者さんも\n多いらしい"),
        s(ROAD, "stare_tabby_wide_eyes_cat", "運動不足の\n解消かと思いきや"),
        s(ROAD, "read_book_orange_kitten", "電波が届かないから\n呼び出しが\nこないかららしい"),
        s(ROAD, "surprise_big_pupils_cat", "なるほど"),
        s(ROAD, "rizz_cat_rizz", "毎日\n誰かの命を救う人は"),
        s(ROAD, "smug_squint_bicolor_cat", "自分の命を救うことにも\n余念がない"),
        s(ROAD, "happy_hamster_open_arms", "俺も\n自分の命を\n救いに来た"),
        s(ROAD, "happy_hamster_open_arms", "今度こそ\n最高だ"),
        s(SITE, "leave_cat_leaves_home", "キャンプ場に到着", se="gong_dora_jaan", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(SITE, "surprise_big_pupils_cat", "木もれ日の\n林の中のサイト"),
        s(SITE, "peek_what_happen_cat", "まわりは\n家族づれと\nキャンプ仲間"),
        s(SITE, "stare_lying_tabby_cat", "となりのサイトでは\nベテランが\nもうコーヒーを飲んでいる"),
        s(SITE, "angry_aiming_cat", "俺も\nいくぞ"),
        # ---- テント設営 ----
        s(SITE, "work_typing_cat", "テントを\n袋から出す", item=TENT),
        s(SITE, "huh_huh_cat", "部品が\n思ったより多い", item=TENT, se="question_mark_pop_confused_huh"),
        s(SITE, "read_book_orange_kitten", "説明書を読む", item=TENT),
        s(SITE, "confused_i_dont_know_cat", "絵が\n小さすぎて\nわからない", item=TENT),
        s(SITE, "think_chin_paw_orange_cat", "この長い棒は\nどこに通すんだ", item=TENT),
        s(SITE, "despair_dramatic_kitten", "テントが\n風で飛んでいく", item=TENT, se="explosion_chudoon"),
        s(SITE, "scream_standing_marmot", "待ってくれ", item=TENT),
        s(SITE, "sad_looking_away_tabby", "追いかけて\n10メートル走る", item=TENT),
        s(SITE, "read_book_orange_kitten", "先にペグを\n打つらしい", item=TENT),
        s(SITE, "angry_shooting_cat", "カン\nカン\nカン", item=TENT, se="pi"),
        s(SITE, "stare_tabby_wide_eyes_cat", "ふと\n思い出す", item=TENT),
        # ---- 回想1 上司 ----
        s(OFFICE, "sleepy_old_memories_cat", "そういえば\n先月も", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(OFFICE, "stare_interviewer_cat", "この企画\n明日までに\n3案ね"),
        s(OFFICE, "surprise_big_pupils_cat", "明日!?"),
        s(OFFICE, "stare_interviewer_cat", "あ\nやっぱり\n今日の夕方まで"),
        s(OFFICE, "scream_standing_marmot", "早まった!?", se="explosion_chudoon"),
        s(OFFICE, "work_typing_cat", "必死で\n3案つくる"),
        s(OFFICE, "stare_interviewer_cat", "うーん\n全部ちがうかな\n最初の方向に\nもどして"),
        s(OFFICE, "blank_black_cat_zoning_out", "最初の方向って\nどれですか"),
        s(OFFICE, "sad_black_dog", "上司も\nわかっていなかった"),
        s(SITE, "angry_shooting_cat", "カンッ", item=TENT, se="explosion_dokaan"),
        s(SITE, "smug_squint_bicolor_cat", "ペグが\nいつもより\n深く入った", item=TENT),
        # ---- 回想2 事務の人 ----
        s(SITE, "think_chin_paw_orange_cat", "2本目のペグ", item=TENT),
        s(OFFICE, "sleepy_old_memories_cat", "そういえば\n先週も"),
        s(OFFICE, "talk_orange_white_sitting_cat", "すみませーん\nこの経費の書類\n今日中に\n出しなおしてください"),
        s(OFFICE, "surprise_big_pupils_cat", "先月\n出したやつですよね"),
        s(OFFICE, "talk_orange_white_sitting_cat", "ハンコの位置が\n2ミリずれてます"),
        s(OFFICE, "huh_huh_cat", "2ミリ", se="question_mark_pop_confused_huh"),
        s(OFFICE, "talk_orange_white_sitting_cat", "あと\n日付は\n和暦でお願いします"),
        s(OFFICE, "despair_dramatic_kitten", "前は西暦で\nって言われました"),
        s(OFFICE, "talk_orange_white_sitting_cat", "今月から\n変わりました"),
        s(OFFICE, "calm_black_face_sheep", "決まりは\n毎月変わる"),
        s(SITE, "angry_shooting_cat", "カンッ", item=TENT, se="explosion_dokaan"),
        s(SITE, "smug_squint_bicolor_cat", "2ミリも\nずれずに\n入った", item=TENT),
        # ---- 回想3 後輩 ----
        s(SITE, "think_chin_paw_orange_cat", "3本目のペグ", item=TENT),
        s(OFFICE, "sleepy_old_memories_cat", "そういえば\nおととい"),
        s(OFFICE, "work_typing_cat", "後輩に\nていねいに\nやり方を教えた"),
        s(OFFICE, "stare_interviewer_cat", "わかりました！"),
        s(OFFICE, "joy_happy_happy_happy_cat", "いい返事だ"),
        s(OFFICE, "peek_what_happen_cat", "1時間後"),
        s(OFFICE, "stare_interviewer_cat", "こっちのほうが\n早いと思って\n自分のやり方で\nやりました！"),
        s(OFFICE, "surprise_big_pupils_cat", "聞いてなかった", se="explosion_chudoon"),
        s(OFFICE, "scream_phone_orange_cat", "お客さんに\n間違った資料が\n届いていた"),
        s(OFFICE, "call_customer_service_cat", "謝りの電話は\n俺がかけた"),
        s(OFFICE, "stare_interviewer_cat", "すみません\n次から気をつけます！"),
        s(OFFICE, "blank_black_cat_zoning_out", "その返事も\nいい返事だった"),
        s(SITE, "angry_shooting_cat", "カンッ\nカンッ\nカンッ", item=TENT, se="explosion_dokaan"),
        s(SITE, "think_chin_paw_orange_cat", "4本目のペグ", item=TENT),
        s(OFFICE, "sleepy_old_memories_cat", "そういえば\n先週の午後"),
        s(OFFICE, "stare_interviewer_cat", "君ねえ\nだいたい\n考えが甘いんだよ"),
        s(OFFICE, "sad_looking_away_tabby", "上司のお説教が\n30分つづく"),
        s(OFFICE, "surprise_big_pupils_cat", "すみません\nこのあと\nお客さんとの\nアポがありまして"),
        s(OFFICE, "stare_interviewer_cat", "話の途中で\n抜けるなんて\n甘えたこと言うな！", se="explosion_chudoon"),
        s(OFFICE, "despair_dramatic_kitten", "お説教は\n最後まで\nつづいた"),
        s(OFFICE, "scream_standing_marmot", "当然\nアポに遅れる"),
        s(OFFICE, "call_customer_service_cat", "お客さんに\n小言を言われる"),
        s(OFFICE, "sleepy_old_memories_cat", "会社にもどると"),
        s(OFFICE, "stare_interviewer_cat", "アポには\nちゃんと\n間に合ったのか？"),
        s(OFFICE, "sad_black_dog", "……遅れました"),
        s(OFFICE, "stare_interviewer_cat", "お客さんに\n迷惑かけやがって！\nまだ甘えた考えを\n持ってるんだな！", se="explosion_dokaan"),
        s(OFFICE, "blank_black_cat_zoning_out", "止めたのは\nあなたです"),
        s(SITE, "angry_shooting_cat", "カンッ！！", item=TENT, se="explosion_dokaan"),
        s(SITE, "despair_dramatic_kitten", "気がつけば\n1時間", item=TENT),
        s(SITE, "showoff_gojo_cosplay_cat", "テント\n完成", item=TENT, se="gong_dora_jaan"),
        s(SITE, "stare_tabby_wide_eyes_cat", "となりのベテランが\nこっちを見ている", item=TENT),
        s(SITE, "stare_interviewer_cat", "ペグ\nめちゃくちゃ\n深いですね", item=TENT),
        s(SITE, "sad_looking_away_tabby", "いろいろ\nあったので", item=TENT),
        # ---- たき火 ----
        s(FIRE, "work_typing_cat", "日が落ちてきた", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(FIRE, "read_book_orange_kitten", "ここは\n地面で直接\nたき火をしては\nいけない", item=TAKIBI),
        s(FIRE, "think_chin_paw_orange_cat", "たき火台の上で\n火をおこす", item=TAKIBI),
        s(FIRE, "despair_dramatic_kitten", "つかない", item=TAKIBI),
        s(FIRE, "sad_black_dog", "マッチ10本目", item=TAKIBI),
        s(FIRE, "read_book_orange_kitten", "細い枝から\n少しずつ\nらしい", item=TAKIBI),
        s(FIRE, "angry_aiming_cat", "ふーっ", item=TAKIBI),
        s(FIRE, "surprise_big_pupils_cat", "ついた", item=TAKIBI, se="shine_kiraan_maou"),
        s(FIRE, "happy_hamster_open_arms", "パチパチ\nパチパチ", item=TAKIBI),
        s(FIRE, "sleepy_old_memories_cat", "動画で見た\nあの音だ", item=TAKIBI),
        s(FIRE, "stare_lying_tabby_cat", "火を見つめる", item=TAKIBI),
        s(FIRE, "think_chin_paw_orange_cat", "100ページの資料", item=TAKIBI),
        s(FIRE, "calm_black_face_sheep", "2ミリずれたハンコ", item=TAKIBI),
        s(FIRE, "blank_black_cat_zoning_out", "いい返事の後輩", item=TAKIBI),
        s(FIRE, "realize_wet_cat_stare", "全部\nこの火に\nくべていく", item=TAKIBI),
        s(FIRE, "sad_banana_cat_cry", "燃えろ\n燃えてしまえ", item=TAKIBI),
        s(FIRE, "happy_girlfriend_dance_cat", "炎が\n少し大きくなった", item=TAKIBI),
        s(FIRE, "rizz_cat_rizz", "たき火は\n大人の\nストレス焼却炉だ", item=TAKIBI),
        # ---- ひとりメシ ----
        s(FIRE, "sulk_hungry_cat", "腹が減った", se="pi"),
        s(FIRE, "money_counting_orange_cat", "スーパーで買った\nちょっといい肉", item=MEAT),
        s(FIRE, "work_typing_cat", "網の上で焼く", item=MEAT),
        s(FIRE, "eat_crunchy_cat_luna", "ジューッ", item=MEAT, se="pikon"),
        s(FIRE, "surprise_big_pupils_cat", "煙の香りが\nうつっている", item=MEAT),
        s(FIRE, "happy_girlfriend_dance_cat", "うまい", item=MEAT),
        s(FIRE, "eat_pop_cat", "家で焼くのと\n同じ肉なのに", item=MEAT),
        s(FIRE, "happy_hamster_open_arms", "外で食べると\n3倍うまい", item=MEAT),
        s(FIRE, "eat_crunchy_cat_luna", "缶ビールを\nプシュッ", item=MEAT, se="drink_gulp_gokugoku_thirsty_chug"),
        s(FIRE, "sleepy_sleepy_cat", "誰にも\n気をつかわない\n乾杯", item=MEAT),
        s(FIRE, "think_chin_paw_orange_cat", "しめは\nカップラーメン", item=RAMEN),
        s(FIRE, "eat_pop_cat", "ズズッ", item=RAMEN, se="drink_gulp_gokugoku_thirsty_chug"),
        s(FIRE, "realize_wet_cat_stare", "寒い夜の\nカップラーメンは\n反則だ", item=RAMEN),
        s(FIRE, "stare_lying_tabby_cat", "ふと\nたき火に\n細い枝を足す", item=TAKIBI),
        s(FIRE, "think_chin_paw_orange_cat", "細い枝といえば", item=TAKIBI),
        s(OFFICE, "sleepy_old_memories_cat", "事務の人に\nまた呼ばれた日", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(OFFICE, "talk_orange_white_sitting_cat", "すみませーん\nコピー機の紙が\nなくなりました"),
        s(OFFICE, "huh_huh_cat", "俺\n総務じゃないです", se="question_mark_pop_confused_huh"),
        s(OFFICE, "talk_orange_white_sitting_cat", "でも\n席が一番近いので"),
        s(OFFICE, "work_typing_cat", "紙の箱を\n倉庫から運ぶ"),
        s(OFFICE, "talk_orange_white_sitting_cat", "あと\nついでに\n電球も\nお願いします"),
        s(OFFICE, "despair_dramatic_kitten", "ついでの\nはばが広い"),
        s(OFFICE, "calm_black_face_sheep", "結局\n全部やった"),
        s(OFFICE, "sleepy_old_memories_cat", "そして\n来週の飲み会"),
        s(OFFICE, "work_typing_cat", "幹事は\n後輩の予定だった"),
        s(OFFICE, "stare_tabby_wide_eyes_cat", "2日前"),
        s(OFFICE, "surprise_big_pupils_cat", "お店\nどこにした？"),
        s(OFFICE, "stare_interviewer_cat", "まだ\n何も\n決めてません！"),
        s(OFFICE, "scream_standing_marmot", "2日前だぞ", se="explosion_chudoon"),
        s(OFFICE, "work_typing_cat", "俺が\n巻き取る"),
        s(OFFICE, "despair_dramatic_kitten", "いい店は\nもう\nどこも満席"),
        s(OFFICE, "sad_black_dog", "空いていたのは\n駅から遠い\nせまい店"),
        s(OFFICE, "sleepy_old_memories_cat", "そして\n飲み会の当日"),
        s(OFFICE, "stare_interviewer_cat", "なんだこの店は！\n誰が幹事だ！", se="explosion_dokaan"),
        s(OFFICE, "stare_interviewer_cat", "先輩です！"),
        s(OFFICE, "surprise_big_pupils_cat", "後輩が\n元気よく\n俺を売り飛ばした"),
        s(OFFICE, "blank_black_cat_zoning_out", "その日いちばんの\nいい返事だった"),
        s(FIRE, "angry_aiming_cat", "太い薪を\n3本くべる", item=TAKIBI, se="explosion_dokaan"),
        s(FIRE, "happy_girlfriend_dance_cat", "ゴオォッ", item=TAKIBI),
        s(FIRE, "surprise_big_pupils_cat", "火が\n大きくなりすぎた", item=TAKIBI),
        s(FIRE, "scream_standing_marmot", "あつい\nあつい", item=TAKIBI),
        s(FIRE, "smug_squint_bicolor_cat", "ストレスも\n入れすぎは\nよくない", item=TAKIBI),
        # ---- 夜 ----
        s(SITE_N, "stare_tabby_wide_eyes_cat", "夜9時", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(SITE_N, "surprise_big_pupils_cat", "空を見上げる"),
        s(SITE_N, "sleepy_old_memories_cat", "星が\nこわいくらい\n多い"),
        s(SITE_N, "happy_hamster_open_arms", "都会では\n見えなかった"),
        s(SITE_N, "think_chin_paw_orange_cat", "上司も\n事務の人も\n後輩も"),
        s(SITE_N, "calm_black_face_sheep", "この星の下では\nみんな小さい"),
        s(SITE_N, "blank_black_cat_zoning_out", "……寒い"),
        s(SITE_N, "read_book_orange_kitten", "山の夜は\n思ったより冷える"),
        s(SITE_N, "work_typing_cat", "寝袋に入る"),
        s(SITE_N, "stare_lying_tabby_cat", "テントの外で\nガサッ", se="pi"),
        s(SITE_N, "scream_standing_marmot", "なにか\nいる", se="explosion_chudoon"),
        s(SITE_N, "despair_dramatic_kitten", "ガサガサッ"),
        s(SITE_N, "peek_what_happen_cat", "そっと\nのぞく"),
        s(SITE_N, "surprise_big_pupils_cat", "タヌキだった"),
        s(SITE_N, "sad_looking_away_tabby", "肉の残りを\nねらっている"),
        s(SITE_N, "smug_squint_bicolor_cat", "後輩と同じで\n話を聞かない"),
        s(SITE_N, "sleep_sleeping_cat", "ゴミを車にしまって\nテントにもどる"),
        s(SITE_N, "stare_lying_tabby_cat", "寝袋の中で\nじっとする"),
        s(SITE_N, "think_chin_paw_orange_cat", "会社では\nいつも\n誰かに呼ばれる"),
        s(SITE_N, "sleepy_old_memories_cat", "ここでは\n誰も呼ばない"),
        s(SITE_N, "realize_wet_cat_stare", "聞こえるのは\n風と虫の声だけ"),
        s(SITE_N, "sleepy_sleepy_cat", "それが\nこんなに\nありがたいとは"),
        s(SITE_N, "sleep_sleeping_cat", "気がつけば\n眠っていた"),
        # ---- 朝 ----
        s(SITE, "stare_tabby_wide_eyes_cat", "朝6時\n鳥の声で\n目が覚めた", bgm={"file": MORNING, "gain": -12, "fade": 0.8}),
        s(SITE, "surprise_big_pupils_cat", "林に\n朝もやが\nかかっている"),
        s(SITE, "work_typing_cat", "お湯をわかして\nコーヒーを入れる", item=COFFEE),
        s(SITE, "eat_crunchy_cat_luna", "ズズッ", item=COFFEE, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SITE, "happy_girlfriend_dance_cat", "うまい", item=COFFEE),
        s(SITE, "stare_lying_tabby_cat", "となりのベテランと\n同じ景色を見ている", item=COFFEE),
        s(SITE, "stare_interviewer_cat", "ペグ\nぬけますか？", item=TENT),
        s(SITE, "despair_dramatic_kitten", "……ぬけない", item=TENT, se="pi"),
        s(SITE, "sad_black_dog", "昨日の怒りが\n深すぎた", item=TENT),
        s(SITE, "angry_shooting_cat", "全力で\nひっこぬく", item=TENT, se="explosion_dokaan"),
        s(SITE, "joy_happy_happy_happy_cat", "ぬけた", item=TENT),
        s(SITE, "happy_hamster_open_arms", "ベテランが\n拍手してくれた", item=TENT),
        # ---- 帰り道 ----
        s(ROAD, "drive_driving_cat", "帰り道", se="whoosh_shu", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(ROAD, "sleepy_old_memories_cat", "服から\nたき火のにおい"),
        s(ROAD, "happy_hamster_open_arms", "いいにおいだ"),
        s(ROAD, "stare_tabby_wide_eyes_cat", "電波が\nもどってきた"),
        s(ROAD, "scream_phone_orange_cat", "通知が\n12件", se="pi"),
        s(ROAD, "stare_interviewer_cat", "月曜の資料\nやっぱり\n50ページで\nいいよ"),
        s(ROAD, "despair_dramatic_kitten", "もう\n100ページ\n作った"),
        s(ROAD, "blank_black_cat_zoning_out", "……"),
        s(ROAD, "calmdown_dancing_cat", "まあいい"),
        s(ROAD, "rizz_cat_rizz", "またたき火に\nくべればいい"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nベッドに倒れこむ", se="whoosh_shu"),
        s(ROOM_N, "think_chin_paw_orange_cat", "来月も\n予約しよう"),
        s(ROOM_N, "money_counting_orange_cat", "キャンプ道具は\nもうそろっている"),
        s(ROOM_N, "smug_squint_bicolor_cat", "あとは\nストレスを\nためるだけだ"),
        s(ROOM_N, "excited_hodomoe_city_cat", "月曜日も\nなんとか\nがんばれそうだ", se="pikon", dur=3.8),
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_16_camp.mp4"), os.path.join(J.HERE, "out", "jidaraku_16_camp_preview"))
