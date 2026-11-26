"""作り方シリーズ「立体駐車場の作り方」の台本（59.9秒）。主人公はレッサーパンダ（ユーザー指定）。最初と最後はドリルを使う場面（ユーザー指定）。
型は姫路城・忍者屋敷と同じ「困ったこと → だからこう作る → これが○○です」。ベンチマーク：0秒博士「立体駐車場の作り方」（320万回）。
数字の出どころ：車路の傾斜部の勾配は17%まで（駐車場法施行令の技術的基準、各自治体の資料）。1階の高さ約3m ÷ 0.17 ≒ 約18m。
エレベーター方式・ターンテーブル・人を検知するセンサー（国土交通省「機械式駐車設備の安全対策」）。車1台 約1.5トン（目安）。
声は青山龍星（ユーザー指定）。"""

LINES = [
    # 1) ドリルで地面に穴 → 白い線 → 駐車場（最初の5秒は強く動かす）
    dict(text="ドリルで 地面に穴をあけて", scene="s01_drill"),
    dict(text="白い線を引けば", scene="s01_drill"),
    dict(text="それはもう 駐車場です", scene="s01_drill"),
    dict(text="でも 駅前の土地は せまくて", scene="s01_drill"),
    dict(text="車が10台しか 止められません", scene="s01_drill"),
    # 2) 鉄骨の床を重ねる
    dict(text="そこで 鉄骨の柱を立てて", scene="s02_floors"),
    dict(text="床を 上へ重ねます", scene="s02_floors"),
    dict(text="これが 立体駐車場です", scene="s02_floors"),
    # 3) 坂道（17%・18m）→ 自走式
    dict(text="でも 車は 2階へ上がれません", scene="s03_ramp"),
    dict(text="そこで 坂道を付けます", scene="s03_ramp"),
    dict(text="でも 坂が急すぎると", scene="s03_ramp"),
    dict(text="車の底を こすってしまいます", scene="s03_ramp"),
    dict(text="だから 坂は 17%まで", scene="s03_ramp", over="17%"),
    dict(text="1階上がるのに 約18mの坂が いります", scene="s03_ramp", over="約18m",
         kana="イッカイ'/アガル'ノニ、ヤ'ク/ジュウハチメ'エトルノ/サカ'ガ、イリマ'_ス"),
    dict(text="これが 自走式です", scene="s03_ramp"),
    # 4) 坂をやめてエレベーター → タワーパーキング
    dict(text="でも 坂道が 土地を半分も使います", scene="s04_tower"),
    dict(text="そこで 坂をやめて", scene="s04_tower"),
    dict(text="車ごと持ち上げる エレベーターを付けます", scene="s04_tower"),
    dict(text="これが タワーパーキングです", scene="s04_tower"),
    # 5) ターンテーブル
    dict(text="でも 奥まで入った車は", scene="s05_turn"),
    dict(text="バックで 出ないといけません", scene="s05_turn"),
    dict(text="そこで 床を ぐるっと回します", scene="s05_turn"),
    dict(text="これが ターンテーブルです", scene="s05_turn"),
    # 6) 重さ → 三角に組む
    dict(text="車は 1台 約1.5トン", scene="s06_truss", over="約1.5トン"),
    dict(text="50台なら 75トンです", scene="s06_truss", over="75トン"),
    dict(text="そこで 鉄骨を 三角に組みます", scene="s06_truss"),
    dict(text="三角は 押されても 形がくずれません", scene="s06_truss"),
    # 7) 人を見はるセンサー
    dict(text="でも 中に人が 残ったまま動くと", scene="s07_sensor"),
    dict(text="はさまれてしまいます", scene="s07_sensor"),
    dict(text="そこで 光のセンサーで 人を見はります", scene="s07_sensor"),
    dict(text="人がいれば 動きません", scene="s07_sensor"),
    # 8) 完成（最後もドリル）
    dict(text="最後に 料金所と 看板を付けて", scene="s08_final"),
    dict(text="ボルトを ドリルで締めれば", scene="s08_final"),
    dict(text="立体駐車場の完成です", scene="s08_final"),
]

TOTAL = 59.9
LEAD = 0.25
TAIL = 1.4
GAP = 0.06
SPEAKER = 13         # 青山龍星 ノーマル（ユーザー指定）
PITCH = 0.0
INTONATION = 1.2
