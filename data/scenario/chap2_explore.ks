;==========================================================
; chap2_explore.ks - 第2章「魔王城探索」ハブ
; 3つのエンカウントをクリアしたら第3章へ
;==========================================================
*chap2_hub

[set f.chapter=2]

; [bg storage="bg_castle_corridor.jpg" time="800"]
; [bgm storage="bgm_castle_exploration.ogg" loop=true]

[fadein time="1000"]

[nm t="ナレーション"]
魔王城の回廊。松明の炎が揺れ、石造りの廊下が奥へと続いている。[p]

[nm t="女神" color="#ffffaa"]
「玉座は城の最上部よ。だけど……この城には3つの区画がある」[l]

[nm t="女神" color="#ffffaa"]
「どこも魔物が守っているわ。突破しないと先へは進めない」[p]

; クリア済みチェック後のメッセージ
[if exp="f.chap2_slime==1 && f.chap2_succubus==1 && f.chap2_witch==1"]
  [jump target="*chap2_all_clear"]
[endif]

[nm t="ナレーション"]
分岐路の前に立つ。道標には文字が刻まれている。[p]

; 選択肢（クリア済みの場所はグレーアウトする仕様にする）
[nm t="ナレーション"]
【どの区画へ向かう？】[l]

[if exp="f.chap2_slime==0"]
  [link target="*go_slime"]　→ 地下水路（スライムの巣）[endlink][r]
[else]
  　　　地下水路 ✓ クリア済み[r]
[endif]

[if exp="f.chap2_succubus==0"]
  [link target="*go_succubus"]　→ 上層回廊（サキュバスの回廊）[endlink][r]
[else]
  　　　上層回廊 ✓ クリア済み[r]
[endif]

[if exp="f.chap2_witch==0"]
  [link target="*go_witch"]　→ 東の塔（魔女の実験室）[endlink][r]
[else]
  　　　東の塔 ✓ クリア済み[r]
[endif]

[s]

;==========================================================
; 各エリアへの移動
;==========================================================

*go_slime
[jump storage="chap2_slime.ks"]

*go_succubus
[jump storage="chap2_succubus.ks"]

*go_witch
[jump storage="chap2_witch.ks"]

;==========================================================
; 全エリアクリア → 第3章へ
;==========================================================
*chap2_all_clear

[nm t="ナレーション"]
三つの区画を突破した。魔王城の最深部——玉座への道が開かれた。[p]

[nm t="女神" color="#ffffaa"]
「よくやったわ、勇者……でも淫紋の影響は？ 大丈夫？」[l]

; 淫紋レベルに応じたメッセージ
[if exp="f.inmaku<=1"]
  [nm t="勇者" color="#aaddff"]
  「なんとか……耐えました。行けます」[p]
[endif]
[if exp="f.inmaku==2"]
  [nm t="勇者" color="#aaddff"]
  「……正直、きつかったです。でも、まだ戦えます」[p]
[endif]
[if exp="f.inmaku>=3"]
  [nm t="勇者" color="#aaddff"]
  「（身体が……熱い。でも魔王を倒さないと）……行きます」[p]
[endif]

[nm t="女神" color="#ffffaa"]
「……わかった。気をつけて。私がついているわ」[p]

[set f.chapter=3]

[fadeout time="2000" color="0x000000"]
[wait time=500]

[jump storage="chap3_maou.ks"]
