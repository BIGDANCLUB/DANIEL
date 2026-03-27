;==========================================================
; システム初期化 - ゲーム開始時に必ず呼ぶ
;==========================================================
*init

;--- ステータス ---
[set f.hp=100]              ; 体力 (0で戦闘不能)
[set f.inmaku=0]            ; 淫紋フラグ: 0=なし / 1=刻まれている
[set f.seishi=50]           ; 精液充填量 0-100

;--- チャプターフラグ ---
[set f.chapter=0]
[set f.prolog_done=0]
[set f.chap1_done=0]

;--- 第2章: フロアクリアフラグ ---
; B1F
[set f.b1f_slime=0]
[set f.b1f_tentacle=0]
[set f.b1f_mimic=0]
[set f.b1f_mermaid=0]
; 1F
[set f.f1_thief=0]
[set f.f1_kunoichi=0]
[set f.f1_fighter=0]
; 2F
[set f.f2_lamia=0]
[set f.f2_harpy=0]
[set f.f2_succubus=0]
; 3F
[set f.f3_alraune=0]
[set f.f3_witch=0]
[set f.f3_scientist=0]
[set f.f3_nurse=0]
; 4F
[set f.f4_sister=0]
[set f.f4_massage=0]
[set f.f4_prostitute=0]
[set f.f4_downer=0]
; 5F（ボスフロア）
[set f.f5_sr_succubus=0]

;--- 搾精記録 (エンディング分岐用) ---
[set f.squeeze_total=0]     ; 搾精された合計回数
[set f.resist_count=0]      ; 抵抗成功回数
[set f.surrender_count=0]   ; 自ら従った回数

;--- イベントフラグ ---
[set f.maou_met=0]
[set f.goddess_power=1]
[set f.witch_info=0]        ; 魔女から情報入手済み

[return]

;==========================================================
; 搾精イベント共通処理
;==========================================================
*squeeze_event

[set f.squeeze_total=f.squeeze_total+1]
[eval exp="f.seishi = Math.max(f.seishi - 30, 0)"]
[eval exp="f.seishi = Math.min(f.seishi + 10, 100)"]

[return]

;==========================================================
; セーブ画面呼び出し (共通)
;==========================================================
*call_save
[call_save]
[return]
