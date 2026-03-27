;==========================================================
; chap2_alraune.ks - 3F「アルラウネ」
;==========================================================
*alraune_start

; [bg storage="bg_greenhouse.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
研究棟の一室——温室のようになっている。甘い花の香りが充満していた。[l]

[nm t="ナレーション"]
部屋の中央に、大きな花が咲いている。その中から、女性の上半身が現れた——アルラウネだ。[p]

; [chara_show name="alraune" storage="chara/alraune_normal.png" pos="center" time="600"]

[nm t="アルラウネ" color="#ffaaff"]
「……いらっしゃい。私の花粉で、眠くなってきたでしょう？」[l]

[nm t="アルラウネ" color="#ffaaff"]
「大丈夫。ゆっくり休んでいって。……あなたの栄養を少し分けてもらいながら」[p]

[select text="どう対処する？"
  option="息を止めて走り抜ける" target="*alraune_rush"
  option="「花粉の解毒を教えてくれ」と交渉する" target="*alraune_negotiate"
  option="（花粉で意識が……）" target="*alraune_sleep"
]

*alraune_rush

[nm t="ナレーション"]
息を止め、一気に走り抜ける！[l]

[nm t="ナレーション"]
花粉の中を駆け抜け、出口へ——！ 意識が朦朧とするが、なんとか抜け出た。[p]

[nm t="勇者" color="#aaddff"]
「はあ……はあ……抜けた」[l]

[nm t="ナレーション"]
新鮮な空気を吸い込む。花粉の影響が薄れていく。[p]

[set f.resist_count=f.resist_count+1]
[jump target="*alraune_clear"]

*alraune_negotiate

[nm t="勇者" color="#aaddff"]
「……花粉の毒を消す方法を教えてくれ。その代わり、俺に何か手伝えることがあれば」[p]

[nm t="アルラウネ" color="#ffaaff"]
「……手伝う？」[l]

[nm t="アルラウネ" color="#ffaaff"]
「じゃあ……受粉の手伝いをしてほしいの。人型の雄の力が必要で」[p]

; ====【Hシーン：アルラウネ・受粉搾精】====
; (ここにHシーン本文・CG挿入)
; [cutin storage="event/alraune_h_deal01.jpg"]
; ==========================================

[nm t="アルラウネ" color="#ffaaff"]
「……ありがとう。これが解毒の花粉よ」[l]

[nm t="アルラウネ" color="#ffaaff"]
「この先も安全に通れるようにしてあげる」[p]

[call storage="system/init.ks" target="*squeeze_event"]
[set f.surrender_count=f.surrender_count+1]
[jump target="*alraune_clear"]

*alraune_sleep

[nm t="ナレーション"]
花粉が肺に入り込む。甘い匂いが頭を満たし、意識が遠くなっていく……[p]

[nm t="アルラウネ" color="#ffaaff"]
「いい子……そのまま眠って。夢を見ているみたいに気持ちよくしてあげる」[p]

; ====【Hシーン：アルラウネ・睡眠搾精】====
; (ここにHシーン本文・CG挿入)
; [cutin storage="event/alraune_h_sleep01.jpg"]
; ==========================================

[nm t="ナレーション"]
目が覚めると部屋の出口前に横たわっていた。アルラウネは根を伸ばして道を示している。[p]

[call storage="system/init.ks" target="*squeeze_event"]

*alraune_clear

[set f.f3_alraune=1]
[nm t="ナレーション"]
——アルラウネの温室を突破した。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_3f"]
