;==========================================================
; システム初期化 - ゲーム開始時に必ず呼ぶ
;==========================================================
*init

;--- ステータス ---
[eval exp="f.hp=100"]              ; 体力 (0で戦闘不能)
[eval exp="f.inmaku=0"]            ; 淫紋フラグ: 0=なし / 1=刻まれている
[eval exp="f.seishi=50"]           ; 精液充填量 0-100

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
; 5F（ボスフロア）
[eval exp="f.f5_sr_succubus=0"]

;--- 搾精記録 (エンディング分岐用) ---
[eval exp="f.squeeze_total=0"]     ; 搾精された合計回数
[eval exp="f.resist_count=0"]      ; 抵抗成功回数
[eval exp="f.surrender_count=0"]   ; 自ら従った回数

;--- イベントフラグ ---
[eval exp="f.maou_met=0"]
[eval exp="f.goddess_power=1"]
[eval exp="f.witch_info=0"]        ; 魔女から情報入手済み

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
