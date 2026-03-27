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

[select text="どう対処する？"
  option="剣で切り払いながら突進する" target="*tentacle_rush"
  option="触手の動きを観察してから動く" target="*tentacle_observe"
  option="（触手に捕まってしまった）" target="*tentacle_captured"
]

*tentacle_rush

[nm t="ナレーション"]
剣を振りながら前進する。切っても切っても次々と伸びてくるが——出口が見えた！[p]

[nm t="勇者" color="#aaddff"]
「突き抜ける！」[l]

[nm t="ナレーション"]
全力疾走で触手の群れを抜けた。[p]

[set f.resist_count=f.resist_count+1]

[jump target="*tentacle_clear"]

*tentacle_observe

[nm t="ナレーション"]
触手の動きをよく見ると、光に向かって伸びる習性があるようだ。[l]

[nm t="勇者" color="#aaddff"]
「（光源から離れれば……）」[l]

[nm t="ナレーション"]
松明を壁に投げつけ、触手の注意を引きつけてから反対方向へ走り抜けた。[p]

[set f.resist_count=f.resist_count+1]

[jump target="*tentacle_clear"]

*tentacle_captured

[nm t="ナレーション"]
気がつくと、足首から触手が巻きついていた。引き倒され、全身を複数の触手に拘束される。[p]

[nm t="ナレーション"]
ぬるりとした感触が全身を這い回り、服の隙間へ入り込んでくる。[p]

; ====【Hシーン：触手・全身拘束搾精】====
; (ここにHシーン本文・CG挿入)
; [cutin storage="event/tentacle_h01.jpg"]
; =======================================

[nm t="ナレーション"]
触手が満足したのか、ゆっくりと離れていった。女神の加護が薄く輝き、道を示す。[p]

[call storage="system/init.ks" target="*squeeze_event"]

[jump target="*tentacle_clear"]

*tentacle_clear

[set f.b1f_tentacle=1]

[nm t="ナレーション"]
——触手系魔物の区画を突破した。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_b1f"]
