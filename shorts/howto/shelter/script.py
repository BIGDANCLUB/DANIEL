"""作り方シリーズ「核シェルターの作り方」の台本（59.9秒）。姫路城と同じ「困ったこと → だからこう作る → これが○○です」の型。
参考元（0秒博士「シェルターを作る方法」）とは言い回しと順番を変えて、核ならではのしかけ（死の灰・放射線・曲がった入口・2週間）を中心にする。
数字の出どころ：土の遮へい（土の半価層 約8〜9cm → 約1mで約1000分の1）、7:10の法則（7時間で1/10、49時間で1/100、約2週間で1/1000。爆発1時間後との比、目安）。
読む速さは参考元と同じ（1秒に約8.8モーラ）。声は青山龍星（ユーザー指定）。"""

LINES = [
    # 1) 穴と部屋（最初の5秒は強く動かす）
    dict(text="地面に穴を掘って", scene="s01_hole"),
    dict(text="部屋を埋めれば", scene="s01_hole"),
    dict(text="それはもう 核シェルターです", scene="s01_hole"),
    dict(text="でも近くに 核ミサイルが落ちると", scene="s01_hole"),
    # 2) 爆風 → 鉄筋コンクリートと防爆扉
    dict(text="まず すさまじい爆風が", scene="s02_blast"),
    dict(text="地面の上を 吹き抜けます", scene="s02_blast"),
    dict(text="そこで 部屋を分厚い鉄筋コンクリートで作り", scene="s02_blast"),
    dict(text="入口には 鋼鉄の扉を付けます", scene="s02_blast"),
    dict(text="これが防爆扉です", scene="s02_blast", kana="コレガ'/ボウバクト'ビラデス"),
    # 3) 死の灰 → 1mの土
    dict(text="次に 空から死の灰が降ってきます", scene="s03_soil"),
    dict(text="灰が出す放射線は", scene="s03_soil"),
    dict(text="コンクリートの屋根も 通り抜けます", scene="s03_soil"),
    dict(text="そこで 屋根の上に 1mの土をかぶせます", scene="s03_soil", kana="ソコデ'、ヤネノ'/ウエニ'、イチメ'エトルノ/ツチ'オ/カブセマ'_ス"),
    dict(text="これで放射線は 約1000分の1", scene="s03_soil", over="約1/1000"),
    # 4) 曲がった入口
    dict(text="でも入口からは", scene="s04_entrance"),
    dict(text="放射線が まっすぐ入ってきます", scene="s04_entrance"),
    dict(text="だから入口の通路を 直角に曲げます", scene="s04_entrance"),
    dict(text="放射線は 曲がり角で 大きく弱まります", scene="s04_entrance"),
    # 5) 換気フィルター
    dict(text="こもっていると 空気がなくなります", scene="s05_air"),
    dict(text="でも外の空気には 死の灰がまざっています", scene="s05_air"),
    dict(text="だから ファンで吸い込んで", scene="s05_air"),
    dict(text="フィルターで 灰を取りのぞいてから", scene="s05_air"),
    dict(text="部屋に送ります", scene="s05_air"),
    dict(text="これが換気フィルターです", scene="s05_air"),
    # 6) 2週間
    dict(text="では いつまで隠れればいい？", scene="s06_days"),
    dict(text="放射線は 7時間で10分の1", scene="s06_days", over="7時間", kana="ホオシャセンワ'、ナナジ'カンデ/ジュウブンノ'イチ"),
    dict(text="2日で100分の1", scene="s06_days", over="2日", kana="フツカデ'/ヒャクブンノ'イチ"),
    dict(text="2週間で 約1000分の1に減ります", scene="s06_days", over="2週間", kana="ニシュ'ウカンデ、ヤク'/センブンノ'イチニ/ヘリマ'_ス"),
    dict(text="だから 2週間分の水と食料を備えます", scene="s06_days"),
    # 7) 完成
    dict(text="最後に ベッドとトイレを置けば", scene="s07_final"),
    dict(text="核シェルターの完成です", scene="s07_final"),
]

TOTAL = 59.9
LEAD = 0.25
TAIL = 1.4
GAP = 0.06
SPEAKER = 13         # 青山龍星 ノーマル（ユーザー指定）
PITCH = 0.0
INTONATION = 1.2
