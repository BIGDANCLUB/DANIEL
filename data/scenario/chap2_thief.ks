;==========================================================
; chap2_thief.ks - 1F「女盗賊」
;==========================================================
*thief_start

; [bg storage="bg_central_hall.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
回廊の角を曲がった瞬間——首元に短剣が当てられた。[p]

; [chara_show name="thief" storage="chara/thief_normal.png" pos="right" time="300"]

[nm t="女盗賊" color="#aaaaff"]
「動くな。……その匂い、勇者だね？」[l]

[nm t="女盗賊" color="#aaaaff"]
「ちょうどいい。魔王様から、勇者を捕まえたら報酬をもらえるって聞いてたんだよね」[p]

[nm t="勇者" color="#aaddff"]
「……金で動く、か」[p]

[select text="どう対処する？"
  option="「いくら欲しい？」→ 交渉する" target="*thief_negotiate"
  option="隙を突いて反撃する" target="*thief_counter"
  option="（短剣を押しつけられ、抵抗できない）" target="*thief_captured"
]

*thief_negotiate

[nm t="勇者" color="#aaddff"]
「俺を捕まえるより、もっと割のいい仕事がある」[p]

[nm t="女盗賊" color="#aaaaff"]
「……ほう。聞かせてもらおうか」[p]

[nm t="勇者" color="#aaddff"]
「魔王を倒して平和が戻れば、盗賊稼業も稼ぎにくくなるだろう？ 今のうちに俺と組め」[l]

[nm t="勇者" color="#aaddff"]
「俺が魔王を倒した後、正式なルートで報酬を出す」[p]

[nm t="女盗賊" color="#aaaaff"]
「……面白い提案だ。でも保証は？」[l]

[nm t="女盗賊" color="#aaaaff"]
「まずは……担保を置いてもらおうか。あなたの身体で」[p]

[select text="どうする？"
  option="「……わかった」→ 同意" target="*thief_offer"
  option="「断る」→ 力ずくで突破" target="*thief_counter"
]

*thief_counter

[nm t="ナレーション"]
短剣の動きが一瞬止んだ瞬間——素早く手首を掴み、短剣を弾き飛ばす！[p]

[nm t="女盗賊" color="#aaaaff"]
「っ……！」[l]

[nm t="ナレーション"]
驚いた女盗賊が後退した隙に、通路を駆け抜けた。[p]

[set f.resist_count=f.resist_count+1]
[jump target="*thief_clear"]

*thief_offer

[set f.surrender_count=f.surrender_count+1]

; ====【Hシーン：女盗賊・取引搾精】====
; (ここにHシーン本文・CG挿入)
; [cutin storage="event/thief_h_deal01.jpg"]
; =======================================

[nm t="女盗賊" color="#aaaaff"]
「……フン。まあ、許してやるよ。行きな」[p]

[call storage="system/init.ks" target="*squeeze_event"]
[jump target="*thief_clear"]

*thief_captured

[nm t="ナレーション"]
身動きが取れない状態で、女盗賊が近づいてくる。[p]

; ====【Hシーン：女盗賊・強制搾精】====
; (ここにHシーン本文・CG挿入)
; [cutin storage="event/thief_h_force01.jpg"]
; =======================================

[call storage="system/init.ks" target="*squeeze_event"]

*thief_clear

[set f.f1_thief=1]
[nm t="ナレーション"]
——女盗賊を突破した。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_1f"]
