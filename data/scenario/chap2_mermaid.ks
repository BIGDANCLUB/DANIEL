;==========================================================
; chap2_mermaid.ks - B1F「マーメイド」
;==========================================================
*mermaid_start

; [bg storage="bg_underground_lake.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
水路の先に、地下湖が広がっていた。向こう岸へ渡らなければならない。[p]

[nm t="ナレーション"]
水面が揺れ、そこから上半身だけが現れた。長い水色の髪、魚の尾——マーメイドだ。[p]

; [chara_show name="mermaid" storage="chara/mermaid_normal.png" pos="center" time="500"]

[nm t="マーメイド" color="#88ccff"]
「……旅人。向こう岸へ行きたいの？」[l]

[nm t="マーメイド" color="#88ccff"]
「渡してあげてもいいけど……お礼が欲しいな」[p]

[select text="どう対処する？"
  option="「お礼とは？」→ 交渉する" target="*mermaid_negotiate"
  option="泳いで渡ろうとする" target="*mermaid_swim"
  option="「わかった」→ お礼を渡す" target="*mermaid_offer"
]

*mermaid_negotiate

[nm t="マーメイド" color="#88ccff"]
「うーん……あなたのいい匂いが欲しい。ちょっとだけ」[l]

[nm t="マーメイド" color="#88ccff"]
「勇者の精力って、私たちにとって滋養強壮なの。海が荒れてて最近食事できてなくて……」[p]

[nm t="勇者" color="#aaddff"]
「（困った顔をしている……）」[p]

[select text="どうする？"
  option="「……少しだけなら」→ 同意" target="*mermaid_offer"
  option="「嫌だ」→ 別の方法を探す" target="*mermaid_swim"
]

*mermaid_swim

[nm t="ナレーション"]
水に飛び込んだ——瞬間、マーメイドの手が足首を掴んだ。[p]

[nm t="マーメイド" color="#88ccff"]
「ダメダメ。この湖は私の縄張りよ」[p]

[jump target="*mermaid_captured"]

*mermaid_offer

[set f.surrender_count=f.surrender_count+1]

[nm t="マーメイド" color="#88ccff"]
「ありがとう……じゃあ、遠慮なく」[p]

[nm t="ナレーション"]
マーメイドが水から上半身を乗り出し、勇者に近づいてくる。[p]

; ====【Hシーン：マーメイド・水際搾精】====
; [cutin storage="event/mermaid_h_offer01.jpg"]

[nm t="ナレーション"]
マーメイドが岸に腰掛けるように上半身を乗り上げ、目の前に座った。[l]

[nm t="マーメイド" color="#88ccff"]
「じゃあ……おとなしくしていて。私がするから」[p]

[nm t="ナレーション"]
水で濡れたマーメイドの手が、服の上から触れてくる。ひんやりとしているが、不快ではなく——むしろ、熱くなった身体に心地よかった。[p]

[nm t="マーメイド" color="#88ccff"]
「……やっぱりいい匂い。もっと近くで嗅ぎたい」[l]

[nm t="ナレーション"]
顔を近づけてくるマーメイド。水色の髪が頬に触れた。[l]

[nm t="ナレーション"]
魚の尾が水中で揺れ、さざ波が立つ。涼しい風と水音の中、マーメイドの手技は驚くほど巧みだった。[p]

[nm t="勇者" color="#aaddff"]
「……っ、うまい……な……」[l]

[nm t="マーメイド" color="#88ccff"]
「うふふ……褒めても何も出ないよ？ ……あ、でも、これは出てきそう」[p]

[nm t="ナレーション"]
耳元で笑う声。水音のBGMの中、勇者は静かに限界を迎えた。[p]
; ==========================================

[nm t="マーメイド" color="#88ccff"]
「……美味しかった。約束通り、渡してあげる」[l]

[nm t="マーメイド" color="#88ccff"]
「またいつでも来てね？」[p]

[call storage="system/init.ks" target="*squeeze_event"]

[jump target="*mermaid_clear"]

*mermaid_captured

[nm t="ナレーション"]
水中へ引き込まれた。しかし溺れることはない——マーメイドの魔法で水中でも呼吸できる。[p]

; ====【Hシーン：マーメイド・水中搾精】====
; [cutin storage="event/mermaid_h_force01.jpg"]

[nm t="ナレーション"]
水中。息ができないはずなのに——マーメイドの魔法のせいか、不思議と苦しくない。[l]

[nm t="ナレーション"]
周囲は静かな水の揺らめき。水面から差し込む光が揺れている。[p]

[nm t="マーメイド" color="#88ccff"]
「……暴れないで。溺れさせたくないから」[l]

[nm t="ナレーション"]
マーメイドの尾が腰に絡みついた。水中でも動じない。水流そのものを操るような動きで、じわりと圧をかけてくる。[p]

[nm t="ナレーション"]
水の抵抗がすべての動きを緩やかにする。逃げようとするほどに水が押し返し、マーメイドの腕の中へ戻っていく。[p]

[nm t="勇者" color="#aaddff"]
「……っ……（水中で声が出せない）」[l]

[nm t="マーメイド" color="#88ccff"]
「……いい顔してる」[p]

[nm t="ナレーション"]
静寂と浮遊感の中——やがて、身体が限界を告げた。[p]
; ==========================================

[nm t="ナレーション"]
満足したマーメイドは、勇者を対岸に送り届けた。[p]

[call storage="system/init.ks" target="*squeeze_event"]

*mermaid_clear

[set f.b1f_mermaid=1]

[nm t="ナレーション"]
——地下湖を渡った。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_b1f"]
