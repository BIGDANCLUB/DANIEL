;==========================================================
; chap2_tentacle.ks - B1F「触手系魔物」
;==========================================================
*tentacle_start

; [bg storage="bg_underground_waterway.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
水路の壁から、無数の触手がにゅるりと伸びてきた。[l]

[nm t="ナレーション"]
触手の先端が勇者の匂いを嗅ぐように揺れる。意思を持った生物——触手系の魔物だ。[p]

どう対処する？[r]
[link target="*tentacle_rush"]剣で切り払いながら突進する[endlink][r]
[link target="*tentacle_observe"]触手の動きを観察してから動く[endlink][r]
[link target="*tentacle_captured"]（触手に捕まってしまった）[endlink][r]
[s]

*tentacle_rush

[nm t="ナレーション"]
剣を振りながら前進する。切っても切っても次々と伸びてくるが——出口が見えた！[p]

[nm t="勇者" color="#aaddff"]
「突き抜ける！」[l]

[nm t="ナレーション"]
全力疾走で触手の群れを抜けた。[p]

[eval exp="f.resist_count=f.resist_count+1"]

[jump target="*tentacle_clear"]

*tentacle_observe

[nm t="ナレーション"]
触手の動きをよく見ると、光に向かって伸びる習性があるようだ。[l]

[nm t="勇者" color="#aaddff"]
「（光源から離れれば……）」[l]

[nm t="ナレーション"]
松明を壁に投げつけ、触手の注意を引きつけてから反対方向へ走り抜けた。[p]

[eval exp="f.resist_count=f.resist_count+1"]

[jump target="*tentacle_clear"]

*tentacle_captured

[nm t="ナレーション"]
気がつくと、足首から触手が巻きついていた。引き倒され、全身を複数の触手に拘束される。[p]

[nm t="ナレーション"]
ぬるりとした感触が全身を這い回り、服の隙間へ入り込んでくる。[p]

; ====【Hシーン：触手・全身拘束搾精】====
; [cutin storage="event/tentacle_h01.jpg"]

[nm t="ナレーション"]
触手が四肢を完全に固定した。手首、足首、胴体、首元まで。どれほど力を込めても、びくともしない。[p]

[nm t="ナレーション"]
ぬるぬるとした粘液が触手の表面に滲んでいる。それが素肌に触れるたびに、摩擦ゼロの滑らかな感触が広がった。[l]

[nm t="ナレーション"]
一本の触手が、服の前を器用にはだけさせた。[p]

[nm t="勇者" color="#aaddff"]
「……やめろ……！ 離せ……！」[l]

[nm t="ナレーション"]
叫んでも、触手は止まらない。むしろ声に反応するように、動きが活発になった。[p]

[nm t="ナレーション"]
細い触手が、一番敏感な部分に絡みついてくる。ゆっくりと、リズムを刻むように動き始めた。[l]

[nm t="ナレーション"]
多数の触手が同時に別々の場所を刺激する——耳元、首筋、脇腹、内腿……そして中心。[p]

[nm t="勇者" color="#aaddff"]
「っ……あ……く……そっ……！」[l]

[nm t="ナレーション"]
淫紋が熱く脈動する。触手はじっくりと、焦らすように、追い詰めていく。逃げ場はない。[p]

[nm t="ナレーション"]
絶頂の瞬間、触手が素早く採取した。[p]
; ========================================

[nm t="ナレーション"]
触手が満足したのか、ゆっくりと離れていった。女神の加護が薄く輝き、道を示す。[p]

[call storage="system/init.ks" target="*squeeze_event"]

[jump target="*tentacle_clear"]

*tentacle_clear

[eval exp="f.b1f_tentacle=1"]

[nm t="ナレーション"]
——触手系魔物の区画を突破した。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_b1f"]
