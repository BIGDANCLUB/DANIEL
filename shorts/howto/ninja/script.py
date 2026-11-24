"""作り方シリーズ「忍者屋敷の作り方」の台本（59.9秒）。姫路城と同じ「敵がこう攻める → だからこう作る → これが○○です」の型。
モデル：甲賀流忍術屋敷（滋賀県甲賀市、望月出雲守の旧宅、元禄年間の建築。外見はふつうの家、中は3層。どんでん返し・隠し梯子と隠し部屋・落とし穴・縄ばしご）。
刀隠しは伊賀流忍者博物館の忍者屋敷にもある仕掛け。読む速さは参考元と同じ（1秒に約8.8モーラ）。声は青山龍星（ユーザー指定）。"""

LINES = [
    # 1) 家と忍者（最初の5秒は強く動かす）
    dict(text="家を建てて 忍者が住めば", scene="n01_house"),
    dict(text="それはもう忍者屋敷です", scene="n01_house"),
    dict(text="でも敵の忍者が", scene="n01_house"),
    dict(text="屋敷に忍び込んできます", scene="n01_house"),
    # 2) どんでん返し
    dict(text="そこで", scene="n02_donden"),
    dict(text="壁の板の真ん中に 軸を通して", scene="n02_donden"),
    dict(text="くるっと回るようにします", scene="n02_donden"),
    dict(text="敵が来たら 壁を押して", scene="n02_donden"),
    dict(text="一瞬で 隣の部屋へ", scene="n02_donden"),
    dict(text="これがどんでん返しです", scene="n02_donden"),
    # 3) 隠し梯子と隠し部屋
    dict(text="でも敵は 回る壁に気づいて", scene="n03_ladder"),
    dict(text="追いかけてきます", scene="n03_ladder"),
    dict(text="だから天井の板を外して", scene="n03_ladder"),
    dict(text="隠し梯子を下ろします", scene="n03_ladder"),
    dict(text="上がったら梯子を引き上げて", scene="n03_ladder"),
    dict(text="板を閉じれば", scene="n03_ladder"),
    dict(text="そこは隠し部屋です", scene="n03_ladder"),
    # 4) 外から見るとふつうの家
    dict(text="外から見ると ふつうの家", scene="n04_floors"),
    dict(text="でも中は 3階建てです", scene="n04_floors"),
    # 5) 落とし穴
    dict(text="敵が 隠し部屋の入り口を探して", scene="n05_pit"),
    dict(text="部屋を歩き回ると", scene="n05_pit"),
    dict(text="床板が抜けて", scene="n05_pit", kana="ユカイタガ'/ヌケテ'"),
    dict(text="下の穴へ真っ逆さま", scene="n05_pit"),
    dict(text="これが落とし穴です", scene="n05_pit"),
    # 6) 刀隠し
    dict(text="でも寝ているところを", scene="n06_katana"),
    dict(text="襲われたら？", scene="n06_katana"),
    dict(text="だから床板の下に", scene="n06_katana", kana="ダ'カラ/ユカイタノ'/シタニ'"),
    dict(text="刀を隠しておきます", scene="n06_katana"),
    dict(text="これが刀隠しです", scene="n06_katana"),
    # 7) からくり窓
    dict(text="今度は 外から窓を破ろうとします", scene="n07_window"),
    dict(text="でもこの窓は 開け方を知らないと", scene="n07_window"),
    dict(text="どうやっても開きません", scene="n07_window"),
    dict(text="これがからくり窓です", scene="n07_window"),
    # 8) 縄ばしご
    dict(text="それでも 囲まれてしまったら", scene="n08_rope"),
    dict(text="3階から縄ばしごを下ろして", scene="n08_rope"),
    dict(text="一気に1階へ逃げます", scene="n08_rope"),
    # 9) 完成
    dict(text="この屋敷は 約330年前に建てられ", scene="n09_final", over="約330年前"),
    dict(text="今も滋賀県の甲賀に 残っています", scene="n09_final", over="滋賀県甲賀市", kana="イマモ'/シガ'ケンノ/コ'ウカニ、ノコ'ッテ/イマ'_ス"),
    dict(text="おめでとう", scene="n09_final"),
    dict(text="忍者屋敷の完成です", scene="n09_final"),
]

TOTAL = 59.9
LEAD = 0.25          # 最初の声までの間
TAIL = 1.4           # 最後の声のあと（BGM で締める）
GAP = 0.06           # 句と句の間
SPEAKER = 13         # 青山龍星 ノーマル（ユーザー指定）
PITCH = 0.0
INTONATION = 1.2
