"""作り方シリーズ「姫路城の作り方」の台本（59.9秒）。参考元（熊本城の作り方）と同じ「敵がこう攻める → だからこう作る → これが○○です」の型。
読む速さは参考元と同じ（1秒に約8.5〜9モーラ）。言い回しもできるだけ参考元に合わせる（2026-11-22）。
1行 = 字幕1つ = 読み上げ1つ。scene は 3D の場面名、over は画面の上に大きく出す文字（年など）。kana は読みを直すときの VOICEVOX のカナ。"""

LINES = [
    # 1) 家と塀（最初の5秒は強く動かす）
    dict(text="家を高い塀で囲めば", scene="h01_house"),
    dict(text="それはもう城です", scene="h01_house"),
    dict(text="でも敵は梯子をかけて", scene="h01_house"),
    dict(text="塀を乗り越えてきます", scene="h01_house"),
    # 2) 石垣
    dict(text="そこで", scene="h02_stone"),
    dict(text="塀の下に石を積み上げて", scene="h02_stone"),
    dict(text="土台にします", scene="h02_stone"),
    dict(text="下はゆるい坂", scene="h03_curve"),
    dict(text="上へ行くほど反り返り", scene="h03_curve"),
    dict(text="てっぺんはほぼ垂直", scene="h03_curve"),
    dict(text="これが扇の勾配です", scene="h03_curve"),
    dict(text="登るほど体が外へ反り", scene="h04_fall"),
    dict(text="そのまま落ちていきます", scene="h04_fall"),
    # 3) 石落とし（参考元と同じ言い回し）
    dict(text="すると敵は石垣の角に集まって", scene="h05_corner", kana="スルト'/テキワ'/イシガキノ'/カ'ドニ/アツマ'ッテ"),
    dict(text="必死に登り始めます", scene="h05_corner"),
    dict(text="だから角の真上に", scene="h05_corner", kana="ダ'カラ/カ'ドノ/マウエ'ニ"),
    dict(text="床が外へ張り出した櫓を建てます", scene="h05_corner", kana="ユカガ'/ソ'トエ/ハリダ'_シタ/ヤグラオ'/タテマ'_ス"),
    dict(text="床の蓋を開ければ", scene="h05_corner"),
    dict(text="真下へ石を落とせます", scene="h05_corner"),
    dict(text="これが石落としです", scene="h05_corner"),
    # 4) 門
    dict(text="登るのをあきらめた敵は", scene="h06_gate"),
    dict(text="門へ押し寄せます", scene="h06_gate"),
    dict(text="だから門はせまく", scene="h06_gate"),
    dict(text="二人通るのがやっと", scene="h06_gate"),
    dict(text="そこへ上の櫓から", scene="h06_gate", kana="ソコエ'/ウエノ'/ヤグラカラ'"),
    dict(text="一斉攻撃", scene="h06_gate"),
    # 5) 狭間
    dict(text="それでも敵は鉄砲で", scene="h07_sama"),
    dict(text="壁の上の兵を撃ち落としてきます", scene="h07_sama"),
    dict(text="今度は壁に小さな穴を開けます", scene="h07_sama"),
    dict(text="穴は内側が広く外側が狭い", scene="h08_cone"),
    dict(text="外からはほとんど当たらず", scene="h08_cone"),
    dict(text="逆に中からは広く狙えます", scene="h08_cone"),
    dict(text="これが狭間 その数997", scene="h08_cone", kana="コレガ'/サマ'、ソノカズ'/キュ'ウヒャク/キュウジュウナ'ナ"),
    # 6) 白漆喰（姫路城ならでは）
    dict(text="最後に敵は火矢を放ちます", scene="h09_fire"),
    dict(text="だから壁を白い漆喰で塗りこめ", scene="h09_fire"),
    dict(text="燃えにくくします", scene="h09_fire"),
    # 7) 完成
    dict(text="この城は完成から400年以上", scene="h10_final", over="1609年"),
    dict(text="1945年の空襲でも", scene="h10_final", over="1945年"),
    dict(text="焼け残りました", scene="h10_final", over="2026年"),
    dict(text="おめでとう", scene="h10_final"),
    dict(text="姫路城の完成です", scene="h10_final"),
]

TOTAL = 59.9
LEAD = 0.25          # 最初の声までの間
TAIL = 1.4           # 最後の声のあと（BGM で締める）
GAP = 0.06           # 句と句の間
SPEAKER = 11         # 玄野武宏 ノーマル
PITCH = 0.08         # 声の高さ：参考元の声（中央値 約174Hz）に合わせる（0 だと約136Hz → 0.08 で約175Hz）
INTONATION = 1.25    # 抑揚を少し強く（参考元の元気な語り）
