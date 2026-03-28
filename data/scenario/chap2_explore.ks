;==========================================================
; chap2_explore.ks - 第2章「魔王城探索」フロアハブ
;
; 構造:
;   B1F: 地下水路  (スライム, 触手系, ミミック, マーメイド)
;    1F: 中央区画  (女盗賊, くのいち, 女戦士)
;    2F: 上層回廊  (ラミア, ハーピー, サキュバス)
;    3F: 研究棟    (アルラウネ, ウィッチ, 科学者, ナース)
;    4F: 居住区    (シスター, マッサージ師, 娼婦, ダウナー女性)
;    5F: 最上部    (上級サキュバス ※ボス、クリア必須)
;  玉座: 魔王
;
; ルール:
;   - 各フロア内の敵は任意順でOK（全員倒す必要はない）
;   - 各フロアのクリア条件を満たすと次フロアへ
;   - フロアクリア条件: フロア内の敵を1体以上突破
;==========================================================
*chap2_start

[eval exp="f.chapter=2"]
[jump target="*floor_select"]

;==========================================================
; フロア選択ハブ
;==========================================================
*floor_select

; [bg storage="bg_castle_map.jpg" time="500"]
; [bgm storage="bgm_castle_exploration.ogg" loop=true]

[fadein time="800"]

[nm t="女神" color="#ffffaa"]
「玉座は最上部よ。各フロアを突破して上を目指して」[p]

[nm t="ナレーション"]
【現在地: 魔王城内部】[l]
どのフロアへ向かう？[p]

; B1F（常に開放）
[link target="*hub_b1f"]　▼ B1F: 地下水路[endlink][r]

; 1F（常に開放）
[link target="*hub_1f"]　　1F: 中央区画[endlink][r]

; 2F（B1Fか1Fのどちらかをクリアで開放）
[if exp="f.b1f_slime==1 || f.b1f_tentacle==1 || f.b1f_mimic==1 || f.b1f_mermaid==1 || f.f1_thief==1 || f.f1_kunoichi==1 || f.f1_fighter==1"]
  [link target="*hub_2f"]　▲ 2F: 上層回廊[endlink][r]
[else]
  　　2F: 上層回廊 【鍵がかかっている】[r]
[endif]

; 3F（2Fを1体以上クリア）
[if exp="f.f2_lamia==1 || f.f2_harpy==1 || f.f2_succubus==1"]
  [link target="*hub_3f"]　▲ 3F: 研究棟[endlink][r]
[else]
  　　3F: 研究棟 【2Fを突破せよ】[r]
[endif]

; 4F（3Fを1体以上クリア）
[if exp="f.f3_alraune==1 || f.f3_witch==1 || f.f3_scientist==1 || f.f3_nurse==1"]
  [link target="*hub_4f"]　▲ 4F: 居住区[endlink][r]
[else]
  　　4F: 居住区 【3Fを突破せよ】[r]
[endif]

; 5F（4Fを1体以上クリア）
[if exp="f.f4_sister==1 || f.f4_massage==1 || f.f4_prostitute==1 || f.f4_downer==1"]
  [if exp="f.f5_sr_succubus==1"]
    [link target="*goto_chap3"]　▲ 玉座: 魔王【突破可能】[endlink][r]
  [else]
    [link target="*hub_5f"]　▲ 5F: 最上部[endlink][r]
  [endif]
[else]
  　　5F: 最上部 【4Fを突破せよ】[r]
[endif]

[s]

;==========================================================
; B1F: 地下水路
;==========================================================
*hub_b1f

; [bg storage="bg_underground_waterway.jpg" time="500"]

[nm t="ナレーション"]
【B1F: 地下水路】 魔物が潜む湿った通路。[p]

[if exp="f.b1f_slime==0"]
  [link target="*go_slime"]　・スライム[endlink][r]
[else]
  　✓ スライム（突破済み）[r]
[endif]

[if exp="f.b1f_tentacle==0"]
  [link target="*go_tentacle"]　・触手系魔物[endlink][r]
[else]
  　✓ 触手系魔物（突破済み）[r]
[endif]

[if exp="f.b1f_mimic==0"]
  [link target="*go_mimic"]　・ミミック[endlink][r]
[else]
  　✓ ミミック（突破済み）[r]
[endif]

[if exp="f.b1f_mermaid==0"]
  [link target="*go_mermaid"]　・マーメイド[endlink][r]
[else]
  　✓ マーメイド（突破済み）[r]
[endif]

[link target="*floor_select"]　← フロア選択へ戻る[endlink][r]

[s]

*go_slime
[jump storage="chap2_slime.ks"]
*go_tentacle
[jump storage="chap2_tentacle.ks"]
*go_mimic
[jump storage="chap2_mimic.ks"]
*go_mermaid
[jump storage="chap2_mermaid.ks"]

;==========================================================
; 1F: 中央区画
;==========================================================
*hub_1f

; [bg storage="bg_central_hall.jpg" time="500"]

[nm t="ナレーション"]
【1F: 中央区画】 魔王城の主要通路。人型の魔物が巡回している。[p]

[if exp="f.f1_thief==0"]
  [link target="*go_thief"]　・女盗賊[endlink][r]
[else]
  　✓ 女盗賊（突破済み）[r]
[endif]

[if exp="f.f1_kunoichi==0"]
  [link target="*go_kunoichi"]　・くのいち[endlink][r]
[else]
  　✓ くのいち（突破済み）[r]
[endif]

[if exp="f.f1_fighter==0"]
  [link target="*go_fighter"]　・女戦士[endlink][r]
[else]
  　✓ 女戦士（突破済み）[r]
[endif]

[link target="*floor_select"]　← フロア選択へ戻る[endlink][r]

[s]

*go_thief
[jump storage="chap2_thief.ks"]
*go_kunoichi
[jump storage="chap2_kunoichi.ks"]
*go_fighter
[jump storage="chap2_fighter.ks"]

;==========================================================
; 2F: 上層回廊
;==========================================================
*hub_2f

; [bg storage="bg_upper_corridor.jpg" time="500"]

[nm t="ナレーション"]
【2F: 上層回廊】 魔力が漂う薄紫の空間。[p]

[if exp="f.f2_lamia==0"]
  [link target="*go_lamia"]　・ラミア[endlink][r]
[else]
  　✓ ラミア（突破済み）[r]
[endif]

[if exp="f.f2_harpy==0"]
  [link target="*go_harpy"]　・ハーピー[endlink][r]
[else]
  　✓ ハーピー（突破済み）[r]
[endif]

[if exp="f.f2_succubus==0"]
  [link target="*go_succubus"]　・サキュバス[endlink][r]
[else]
  　✓ サキュバス（突破済み）[r]
[endif]

[link target="*floor_select"]　← フロア選択へ戻る[endlink][r]

[s]

*go_lamia
[jump storage="chap2_lamia.ks"]
*go_harpy
[jump storage="chap2_harpy.ks"]
*go_succubus
[jump storage="chap2_succubus.ks"]

;==========================================================
; 3F: 研究棟
;==========================================================
*hub_3f

; [bg storage="bg_research_tower.jpg" time="500"]

[nm t="ナレーション"]
【3F: 研究棟】 奇妙な装置と薬品の匂い。学術系の魔物の領域。[p]

[if exp="f.f3_alraune==0"]
  [link target="*go_alraune"]　・アルラウネ[endlink][r]
[else]
  　✓ アルラウネ（突破済み）[r]
[endif]

[if exp="f.f3_witch==0"]
  [link target="*go_witch"]　・ウィッチ[endlink][r]
[else]
  　✓ ウィッチ（突破済み）[r]
[endif]

[if exp="f.f3_scientist==0"]
  [link target="*go_scientist"]　・科学者[endlink][r]
[else]
  　✓ 科学者（突破済み）[r]
[endif]

[if exp="f.f3_nurse==0"]
  [link target="*go_nurse"]　・ナース[endlink][r]
[else]
  　✓ ナース（突破済み）[r]
[endif]

[link target="*floor_select"]　← フロア選択へ戻る[endlink][r]

[s]

*go_alraune
[jump storage="chap2_alraune.ks"]
*go_witch
[jump storage="chap2_witch.ks"]
*go_scientist
[jump storage="chap2_scientist.ks"]
*go_nurse
[jump storage="chap2_nurse.ks"]

;==========================================================
; 4F: 居住区
;==========================================================
*hub_4f

; [bg storage="bg_residential.jpg" time="500"]

[nm t="ナレーション"]
【4F: 居住区】 魔王城で生活する者たちの区画。様々な職種の女性たちがいる。[p]

[if exp="f.f4_sister==0"]
  [link target="*go_sister"]　・シスター[endlink][r]
[else]
  　✓ シスター（突破済み）[r]
[endif]

[if exp="f.f4_massage==0"]
  [link target="*go_massage"]　・マッサージ師[endlink][r]
[else]
  　✓ マッサージ師（突破済み）[r]
[endif]

[if exp="f.f4_prostitute==0"]
  [link target="*go_prostitute"]　・娼婦[endlink][r]
[else]
  　✓ 娼婦（突破済み）[r]
[endif]

[if exp="f.f4_downer==0"]
  [link target="*go_downer"]　・ダウナー女性[endlink][r]
[else]
  　✓ ダウナー女性（突破済み）[r]
[endif]

[link target="*floor_select"]　← フロア選択へ戻る[endlink][r]

[s]

*go_sister
[jump storage="chap2_sister.ks"]
*go_massage
[jump storage="chap2_massage.ks"]
*go_prostitute
[jump storage="chap2_prostitute.ks"]
*go_downer
[jump storage="chap2_downer.ks"]

;==========================================================
; 5F: 最上部（上級サキュバス・クリア必須）
;==========================================================
*hub_5f

; [bg storage="bg_top_floor.jpg" time="500"]

[nm t="女神" color="#ffffaa"]
「……ここが玉座への最後の関門よ。強力な魔物がいる。気をつけて」[p]

[nm t="ナレーション"]
【5F: 最上部】 玉座への扉を守る番人がいる。[p]

[link target="*go_sr_succubus"]　・上級サキュバス【突破必須】[endlink][r]

[link target="*floor_select"]　← フロア選択へ戻る[endlink][r]

[s]

*go_sr_succubus
[jump storage="chap2_sr_succubus.ks"]

;==========================================================
; 玉座へ
;==========================================================
*goto_chap3

[nm t="ナレーション"]
全ての関門を突破した。魔王城最上部——玉座への扉が目前に迫っている。[p]

[nm t="女神" color="#ffffaa"]
「準備はいい？ 魔王が待っているわ」[p]

; 搾精状況に応じたコメント
[if exp="f.squeeze_total==0"]
  [nm t="女神" color="#ffffaa"]
  「……一度も搾られなかったのね。さすが」[p]
[endif]
[if exp="f.squeeze_total>=10"]
  [nm t="女神" color="#ffffaa"]
  「……随分消耗しているわ。でも、あなたならきっと大丈夫」[p]
[endif]

[nm t="勇者" color="#aaddff"]
「……行きます」[p]

[eval exp="f.chapter=3"]

[fadeout time="2000" color="0x000000"]
[wait time=500]

[jump storage="chap3_maou.ks"]
