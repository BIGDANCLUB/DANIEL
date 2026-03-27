;==========================================================
; chap2_sr_succubus.ks - 5F「上級サキュバス」ボス
; ※クリア必須エンカウント
;==========================================================
*sr_succubus_start

; [bg storage="bg_top_floor_boss.jpg" time="800"]
; [bgm storage="bgm_miniboss.ogg" loop=true]

[fadein time="800"]

[nm t="女神" color="#ffffaa"]
「……強い魔力を感じる。気をつけて」[p]

[nm t="ナレーション"]
5Fの扉を開けると——豪華な部屋に、一人の女性が待っていた。[l]

[nm t="ナレーション"]
通常のサキュバスとは纏う魔力が違う。格が上——上級サキュバスだ。[p]

; [chara_show name="sr_succubus" storage="chara/sr_succubus_normal.png" pos="center" time="600"]

[nm t="上級サキュバス" color="#ff44aa"]
「……よく来たわね、勇者。私がここの門番よ」[l]

[nm t="上級サキュバス" color="#ff44aa"]
「サキュバス族の中でも上位に位置する私が相手よ。覚悟はいい？」[p]

[nm t="勇者" color="#aaddff"]
「……通してもらう」[l]

[nm t="上級サキュバス" color="#ff44aa"]
「フフ……強がりね。でも、嫌いじゃない」[l]

[nm t="上級サキュバス" color="#ff44aa"]
「条件を提示するわ。私を満足させることができれば、通してあげる」[l]

[nm t="上級サキュバス" color="#ff44aa"]
「拒否するなら……力ずくよ」[p]

[select text="どう対処する？"
  option="「力ずくで突破する」→ 戦う" target="*sr_battle"
  option="「……条件を聞こう」→ 交渉" target="*sr_negotiate"
]

;==========================================================
; 戦闘ルート
;==========================================================
*sr_battle

[nm t="ナレーション"]
上級サキュバスの魅了魔法が炸裂した。通常のサキュバスの比ではない。[l]

[nm t="ナレーション"]
全身に甘い痺れが走る——しかし女神の加護が後押しする。[p]

[nm t="女神" color="#ffffaa"]
「……全力で守る！」[l]

[nm t="ナレーション"]
激しい攻防の末——[p]

; 搾精総数が多いと苦戦
[if exp="f.squeeze_total>=8"]
  [jump target="*sr_battle_hard"]
[else]
  [jump target="*sr_battle_win"]
[endif]

*sr_battle_win

[nm t="ナレーション"]
女神の加護を全開にした一撃が、上級サキュバスを打ち抜いた。[p]

[nm t="上級サキュバス" color="#ff44aa"]
「……ッ！ 本当に勇者ね」[l]

[nm t="上級サキュバス" color="#ff44aa"]
「……わかった、約束通り通してあげる。でも——」[l]

[nm t="上級サキュバス" color="#ff44aa"]
「せめて、私のこれだけ受け取って」[p]

[jump target="*sr_h_scene"]

*sr_battle_hard

[nm t="ナレーション"]
疲弊した身体では魅了に抗いきれない——意識が遠のいていく。[p]

[nm t="上級サキュバス" color="#ff44aa"]
「……思ったより消耗しているのね。仕方ない、特別に楽にしてあげる」[p]

[jump target="*sr_h_scene"]

;==========================================================
; 交渉ルート
;==========================================================
*sr_negotiate

[nm t="上級サキュバス" color="#ff44aa"]
「条件は一つ。私に、あなたの全力を一度見せて」[l]

[nm t="上級サキュバス" color="#ff44aa"]
「戦いでも……別の意味でも、ね」[p]

[set f.surrender_count=f.surrender_count+1]

;==========================================================
; Hシーン（共通）
;==========================================================
*sr_h_scene

; ====【Hシーン：上級サキュバス・上位搾精】====
; (ここにHシーン本文・CG挿入 ※メインHシーンの一つ)
; [cutin storage="event/sr_succubus_h01.jpg"]
; [cutin storage="event/sr_succubus_h02.jpg"]
; ==============================================

[nm t="上級サキュバス" color="#ff44aa"]
「……素晴らしかった。女神の加護の精、格が違うわ」[l]

[nm t="上級サキュバス" color="#ff44aa"]
「……約束よ。玉座への扉は開けておく。行きなさい」[p]

[call storage="system/init.ks" target="*squeeze_event"]

[set f.f5_sr_succubus=1]

[nm t="ナレーション"]
——上級サキュバスを突破した。玉座への道が開いた。[p]

[fadeout time="1500" color="0x000000"]
[wait time=500]

[jump storage="chap2_explore.ks" target="*floor_select"]
