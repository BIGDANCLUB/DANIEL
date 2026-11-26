"""作り方シリーズ「いかだの作り方」の台本（59.9秒）。主人公はレッサーパンダ（ユーザー指定）。最初と最後はドリルを使う場面（ユーザー指定）。
型は「困ったこと → だからこう作る → これが○○です」。ベンチマーク：0秒博士「いかだの作り方」（262万回）。
実話：コンティキ号（ヘイエルダールら6人）。1947年4月28日にペルーを出て、8月7日にツアモツ諸島のラロイア環礁へ。101日、約6980km（約7000km）。
バルサの丸太9本を麻縄でしばり、丸太のすき間に松の板をセンターボードとして差し込んでいた（Wikipedia「Kon-Tiki expedition」ほか）。
声は青山龍星（ユーザー指定）。"""

LINES = [
    # 1) 丸太にドリルで穴 → 縄でしばる → いかだ（最初の5秒は強く動かす）
    dict(text="丸太に ドリルで 穴をあけ", scene="s01_drill"),
    dict(text="縄を通して しばれば", scene="s01_drill"),
    dict(text="それはもう いかだです", scene="s01_drill"),
    dict(text="でも 丸太は 重くて", scene="s01_drill"),
    dict(text="上に乗ると 水びたしです", scene="s01_drill"),
    # 2) 軽い木（バルサ）
    dict(text="そこで とても軽い木 バルサを使います", scene="s02_balsa"),
    dict(text="これで 体が 水の上に出ます", scene="s02_balsa"),
    # 3) 波でひっくり返る → アウトリガー
    dict(text="でも 大きな波が来ると", scene="s03_outrigger"),
    dict(text="ひっくり返ってしまいます", scene="s03_outrigger"),
    dict(text="そこで 横に離して もう1本 丸太を浮かべます", scene="s03_outrigger"),
    dict(text="これが アウトリガーです", scene="s03_outrigger"),
    dict(text="南の島の 小舟にも 付いています", scene="s03_outrigger"),
    # 4) 縄が切れる → 木の棒でつなぐ
    dict(text="でも 縄は 波でこすれて", scene="s04_pegs"),
    dict(text="切れてしまいます", scene="s04_pegs"),
    dict(text="そこで 丸太に 横から穴をあけ", scene="s04_pegs"),
    dict(text="木の棒を通して つなぎます", scene="s04_pegs"),
    # 5) 舵
    dict(text="でも 流れに 流されるままです", scene="s05_rudder"),
    dict(text="そこで うしろに 長い板を付けます", scene="s05_rudder"),
    dict(text="板の向きを変えると 好きな方へ曲がれます", scene="s05_rudder"),
    dict(text="これが 舵です", scene="s05_rudder"),
    # 6) 帆
    dict(text="でも こぎ続けると つかれます", scene="s06_sail"),
    dict(text="そこで 帆を張って", scene="s06_sail"),
    dict(text="風の力で 進みます", scene="s06_sail"),
    # 7) センターボード
    dict(text="でも 横からの風で 流されます", scene="s07_board"),
    dict(text="そこで 丸太のすき間から", scene="s07_board"),
    dict(text="板を 水の中へ 差し込みます", scene="s07_board"),
    dict(text="水の中の板が 横すべりを止めます", scene="s07_board"),
    dict(text="これが センターボードです", scene="s07_board"),
    # 8) 実話：コンティキ号
    dict(text="実際に 1947年", scene="s08_kontiki", over="1947年"),
    dict(text="6人で バルサのいかだに乗り", scene="s08_kontiki"),
    dict(text="太平洋を 101日かけて", scene="s08_kontiki", over="101日"),
    dict(text="約7000km 渡った人たちがいます", scene="s08_kontiki", over="約7000km"),
    # 9) 完成（最後もドリル）
    dict(text="最後に 帆柱を ドリルで とめれば", scene="s09_final"),
    dict(text="いかだの完成です", scene="s09_final"),
]

TOTAL = 59.9
LEAD = 0.25
TAIL = 1.4
GAP = 0.06
SPEAKER = 13         # 青山龍星 ノーマル（ユーザー指定）
PITCH = 0.0
INTONATION = 1.2
