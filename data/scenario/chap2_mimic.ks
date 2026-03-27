;==========================================================
; chap2_mimic.ks - B1F「ミミック」
;==========================================================
*mimic_start

; [bg storage="bg_underground_storage.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
倉庫らしき部屋に、古い宝箱が一つ置かれていた。[p]

[nm t="勇者" color="#aaddff"]
「（宝箱……中に武器か回復薬があれば）」[p]

[select text="どう対処する？"
  option="宝箱を開ける" target="*mimic_open"
  option="様子を見てから近づく" target="*mimic_cautious"
  option="無視して通り過ぎる" target="*mimic_ignore"
]

*mimic_open

[nm t="ナレーション"]
宝箱に手をかけた瞬間——蓋が開き、中から舌が伸びてきた！[p]

; [se storage="se_mimic_appear.ogg"]
; [chara_show name="mimic" storage="chara/mimic_open.png" pos="center" time="300"]

[nm t="ミミック" color="#cc8833"]
「……捕まえた♪」[p]

[jump target="*mimic_captured"]

*mimic_cautious

[nm t="ナレーション"]
少し離れた場所から眺めていると——宝箱がわずかに動いた。[l]

[nm t="勇者" color="#aaddff"]
「ミミックか！」[l]

[nm t="ナレーション"]
身構えた瞬間、宝箱が跳び上がり、蓋が大きく開く。[p]

[jump target="*mimic_captured"]

*mimic_ignore

[nm t="ナレーション"]
宝箱には近づかず、部屋の端を伝って通り過ぎようとした。[l]

[nm t="ナレーション"]
しかし——ドスン、と宝箱が勇者の前に飛び込んできた。[p]

[nm t="ミミック" color="#cc8833"]
「……逃がさない」[p]

[jump target="*mimic_captured"]

*mimic_captured

[nm t="ナレーション"]
宝箱の内側は——不思議な空間になっていた。柔らかく、温かく、粘度のある何かに包まれる。[p]

[nm t="ミミック" color="#cc8833"]
「……いいにおい。ゆっくり、食べる」[p]

; ====【Hシーン：ミミック・箱内搾精】====
; [cutin storage="event/mimic_h01.jpg"]

[nm t="ナレーション"]
宝箱の内部は——外観からは想像できない広い空間だった。[l]

[nm t="ナレーション"]
壁も床も天井も、柔らかく湿った何かで覆われている。触れると吸い付くような粘着性。暗いが、ぼんやりと発光している。[p]

[nm t="ミミック" color="#cc8833"]
「……ゆっくり、食べる。逃げられない」[l]

[nm t="ナレーション"]
内壁が蠢き、無数の突起が伸びてきた。人の手のような形をしているものも混じっている。[p]

[nm t="勇者" color="#aaddff"]
「……っ……！」[l]

[nm t="ナレーション"]
複数の"手"が同時に動いた。服を器用に脱がせ、全身をくまなく探るように撫で回す。どこへ逃げようとしても、内壁が追いかけてくる。[p]

[nm t="ミミック" color="#cc8833"]
「……いいにおい。もっと、でてきて」[l]

[nm t="ナレーション"]
暗闇と密室の閉塞感。しかしミミックの"手"は意外なほど繊細で——焦らすように、じわじわと追い詰めていく。[p]

[nm t="勇者" color="#aaddff"]
「……く……あ……っ、もう……」[l]

[nm t="ナレーション"]
抗いきれずに達した。ミミックが満足げに震えた。[p]
; =========================================

[nm t="ナレーション"]
ミミックが満足すると、外へ放り出された。[p]

[call storage="system/init.ks" target="*squeeze_event"]

*mimic_clear

[set f.b1f_mimic=1]

[nm t="ナレーション"]
——ミミックの部屋を突破した。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_b1f"]
