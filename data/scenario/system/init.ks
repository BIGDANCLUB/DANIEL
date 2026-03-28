;==========================================================
; システム初期化 - ゲーム開始時に必ず呼ぶ
;==========================================================
*init

;--- ステータス ---
[eval exp="f.hp=100"]
[eval exp="f.inmaku=0"]
[eval exp="f.seishi=50"]

;--- チャプターフラグ ---
[eval exp="f.chapter=0"]
[eval exp="f.prolog_done=0"]
[eval exp="f.chap1_done=0"]

;--- 第2章: フロアクリアフラグ ---
; B1F
[eval exp="f.b1f_slime=0"]
[eval exp="f.b1f_tentacle=0"]
[eval exp="f.b1f_mimic=0"]
[eval exp="f.b1f_mermaid=0"]
; 1F
[eval exp="f.f1_thief=0"]
[eval exp="f.f1_kunoichi=0"]
[eval exp="f.f1_fighter=0"]
; 2F
[eval exp="f.f2_lamia=0"]
[eval exp="f.f2_harpy=0"]
[eval exp="f.f2_succubus=0"]
; 3F
[eval exp="f.f3_alraune=0"]
[eval exp="f.f3_witch=0"]
[eval exp="f.f3_scientist=0"]
[eval exp="f.f3_nurse=0"]
; 4F
[eval exp="f.f4_sister=0"]
[eval exp="f.f4_massage=0"]
[eval exp="f.f4_prostitute=0"]
[eval exp="f.f4_downer=0"]
; 5F
[eval exp="f.f5_sr_succubus=0"]

;--- 搾精記録 ---
[eval exp="f.squeeze_total=0"]
[eval exp="f.resist_count=0"]
[eval exp="f.surrender_count=0"]

;--- イベントフラグ ---
[eval exp="f.maou_met=0"]
[eval exp="f.goddess_power=1"]
[eval exp="f.witch_info=0"]

;--- バトルシステム ---
[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]
[eval exp="f.from_recall=0"]

;--- 回想解放システム ---
[eval exp="f.scene_all_unlocked=0"]
; B1F
[eval exp="f.scene_slime_h1=0"]
[eval exp="f.scene_slime_h2=0"]
[eval exp="f.scene_slime_h3=0"]
[eval exp="f.scene_slime_h4=0"]
[eval exp="f.scene_slime_h5=0"]
[eval exp="f.scene_tentacle_h1=0"]
[eval exp="f.scene_tentacle_h2=0"]
[eval exp="f.scene_tentacle_h3=0"]
[eval exp="f.scene_tentacle_h4=0"]
[eval exp="f.scene_tentacle_h5=0"]
[eval exp="f.scene_mimic_h1=0"]
[eval exp="f.scene_mimic_h2=0"]
[eval exp="f.scene_mimic_h3=0"]
[eval exp="f.scene_mimic_h4=0"]
[eval exp="f.scene_mimic_h5=0"]
[eval exp="f.scene_mermaid_h1=0"]
[eval exp="f.scene_mermaid_h2=0"]
[eval exp="f.scene_mermaid_h3=0"]
[eval exp="f.scene_mermaid_h4=0"]
[eval exp="f.scene_mermaid_h5=0"]
; 1F
[eval exp="f.scene_thief_h1=0"]
[eval exp="f.scene_thief_h2=0"]
[eval exp="f.scene_thief_h3=0"]
[eval exp="f.scene_thief_h4=0"]
[eval exp="f.scene_thief_h5=0"]
[eval exp="f.scene_kunoichi_h1=0"]
[eval exp="f.scene_kunoichi_h2=0"]
[eval exp="f.scene_kunoichi_h3=0"]
[eval exp="f.scene_kunoichi_h4=0"]
[eval exp="f.scene_kunoichi_h5=0"]
[eval exp="f.scene_fighter_h1=0"]
[eval exp="f.scene_fighter_h2=0"]
[eval exp="f.scene_fighter_h3=0"]
[eval exp="f.scene_fighter_h4=0"]
[eval exp="f.scene_fighter_h5=0"]
; 2F
[eval exp="f.scene_lamia_h1=0"]
[eval exp="f.scene_lamia_h2=0"]
[eval exp="f.scene_lamia_h3=0"]
[eval exp="f.scene_lamia_h4=0"]
[eval exp="f.scene_lamia_h5=0"]
[eval exp="f.scene_harpy_h1=0"]
[eval exp="f.scene_harpy_h2=0"]
[eval exp="f.scene_harpy_h3=0"]
[eval exp="f.scene_harpy_h4=0"]
[eval exp="f.scene_harpy_h5=0"]
[eval exp="f.scene_succubus_h1=0"]
[eval exp="f.scene_succubus_h2=0"]
[eval exp="f.scene_succubus_h3=0"]
[eval exp="f.scene_succubus_h4=0"]
[eval exp="f.scene_succubus_h5=0"]
; 3F
[eval exp="f.scene_alraune_h1=0"]
[eval exp="f.scene_alraune_h2=0"]
[eval exp="f.scene_alraune_h3=0"]
[eval exp="f.scene_alraune_h4=0"]
[eval exp="f.scene_alraune_h5=0"]
[eval exp="f.scene_witch_h1=0"]
[eval exp="f.scene_witch_h2=0"]
[eval exp="f.scene_witch_h3=0"]
[eval exp="f.scene_witch_h4=0"]
[eval exp="f.scene_witch_h5=0"]
[eval exp="f.scene_scientist_h1=0"]
[eval exp="f.scene_scientist_h2=0"]
[eval exp="f.scene_scientist_h3=0"]
[eval exp="f.scene_scientist_h4=0"]
[eval exp="f.scene_scientist_h5=0"]
[eval exp="f.scene_nurse_h1=0"]
[eval exp="f.scene_nurse_h2=0"]
[eval exp="f.scene_nurse_h3=0"]
[eval exp="f.scene_nurse_h4=0"]
[eval exp="f.scene_nurse_h5=0"]
; 4F
[eval exp="f.scene_sister_h1=0"]
[eval exp="f.scene_sister_h2=0"]
[eval exp="f.scene_sister_h3=0"]
[eval exp="f.scene_sister_h4=0"]
[eval exp="f.scene_sister_h5=0"]
[eval exp="f.scene_massage_h1=0"]
[eval exp="f.scene_massage_h2=0"]
[eval exp="f.scene_massage_h3=0"]
[eval exp="f.scene_massage_h4=0"]
[eval exp="f.scene_massage_h5=0"]
[eval exp="f.scene_prostitute_h1=0"]
[eval exp="f.scene_prostitute_h2=0"]
[eval exp="f.scene_prostitute_h3=0"]
[eval exp="f.scene_prostitute_h4=0"]
[eval exp="f.scene_prostitute_h5=0"]
[eval exp="f.scene_downer_h1=0"]
[eval exp="f.scene_downer_h2=0"]
[eval exp="f.scene_downer_h3=0"]
[eval exp="f.scene_downer_h4=0"]
[eval exp="f.scene_downer_h5=0"]
; 5F
[eval exp="f.scene_sr_succubus_h1=0"]
[eval exp="f.scene_sr_succubus_h2=0"]
[eval exp="f.scene_sr_succubus_h3=0"]
[eval exp="f.scene_sr_succubus_h4=0"]
[eval exp="f.scene_sr_succubus_h5=0"]
; 魔王
[eval exp="f.scene_maou_h1=0"]
[eval exp="f.scene_maou_h2=0"]
[eval exp="f.scene_maou_h3=0"]

[return]

;==========================================================
; 搾精イベント共通処理
;==========================================================
*squeeze_event

[eval exp="f.squeeze_total=f.squeeze_total+1"]
[eval exp="f.seishi=Math.max(f.seishi-30,0)"]
[eval exp="f.seishi=Math.min(f.seishi+10,100)"]

[return]

;==========================================================
; セーブ画面呼び出し (共通)
;==========================================================
*call_save
[showsave]
[return]
