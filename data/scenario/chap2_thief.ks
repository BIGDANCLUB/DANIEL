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

どう対処する？[r]
[link target="*thief_negotiate"]「いくら欲しい？」→ 交渉する[endlink][r]
[link target="*thief_counter"]隙を突いて反撃する[endlink][r]
[link target="*thief_captured"]（短剣を押しつけられ、抵抗できない）[endlink][r]
[s]

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

どうする？[r]
[link target="*thief_offer"]「……わかった」→ 同意[endlink][r]
[link target="*thief_counter"]「断る」→ 力ずくで突破[endlink][r]
[s]

*thief_counter

[nm t="ナレーション"]
短剣の動きが一瞬止んだ瞬間——素早く手首を掴み、短剣を弾き飛ばす！[p]

[nm t="女盗賊" color="#aaaaff"]
「っ……！」[l]

[nm t="ナレーション"]
驚いた女盗賊が後退した隙に、通路を駆け抜けた。[p]

[eval exp="f.resist_count=f.resist_count+1"]
[jump target="*thief_clear"]

*thief_offer

[eval exp="f.surrender_count=f.surrender_count+1"]

; ====【Hシーン：女盗賊・取引搾精】====
; [cutin storage="event/thief_h_deal01.jpg"]

[nm t="女盗賊" color="#aaaaff"]
「……じゃあ、さっさと済ませようか。私も時間を無駄にしたくない」[l]

[nm t="ナレーション"]
女盗賊が勇者の前に座り、手を伸ばしてきた。その動きに一切の迷いがない。仕事として割り切っているのが伝わってくる。[p]

[nm t="女盗賊" color="#aaaaff"]
「……へえ、噂通りだね。これは確かに値打ちがある」[l]

[nm t="勇者" color="#aaddff"]
「……黙っていてくれると助かる」[l]

[nm t="女盗賊" color="#aaaaff"]
「フン、細かいことを言う子だ」[p]

[nm t="ナレーション"]
プロの手際。無駄がなく、的確で、必要な場所だけを刺激する。感情を乗せない分、かえって純粋な快感だけが残った。[p]

[nm t="勇者" color="#aaddff"]
「……っ、待、もう少し……」[l]

[nm t="女盗賊" color="#aaaaff"]
「待てない。こっちが主導権だよ」[p]

[nm t="ナレーション"]
抗議する間もなく、追い詰められた。[p]
; ========================================

[nm t="女盗賊" color="#aaaaff"]
「……フン。まあ、許してやるよ。行きな」[p]

[call storage="system/init.ks" target="*squeeze_event"]
[jump target="*thief_clear"]

*thief_captured

[nm t="ナレーション"]
身動きが取れない状態で、女盗賊が近づいてくる。[p]

; ====【Hシーン：女盗賊・強制搾精】====
; [cutin storage="event/thief_h_force01.jpg"]

[nm t="女盗賊" color="#aaaaff"]
「……動くな。抵抗するとこっちも手加減できない」[p]

[nm t="ナレーション"]
短剣を首元に当てたまま、もう片方の手が器用に動く。[l]

[nm t="ナレーション"]
盗賊の手際は確かだった。ロープを使わずに相手を動けなくする術を知っている。[p]

[nm t="勇者" color="#aaddff"]
「……くっ……！」[l]

[nm t="女盗賊" color="#aaaaff"]
「おとなしくしな。悪いようにはしない……まあ、気持ちよくしてやるくらいのことはするけど」[p]

[nm t="ナレーション"]
淡々と、しかし確実に——目的を達成するまで止まらなかった。[p]
; ========================================

[call storage="system/init.ks" target="*squeeze_event"]

*thief_clear

[eval exp="f.f1_thief=1"]
[nm t="ナレーション"]
——女盗賊を突破した。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_1f"]
