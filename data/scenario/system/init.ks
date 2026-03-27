;==========================================================
; システム初期化 - ゲーム開始時に必ず呼ぶ
;==========================================================
*init

;--- ステータス ---
[set f.hp=100]              ; 体力 (0で戦闘不能)
[set f.inmaku=0]            ; 淫紋レベル 0-3 (高いほど快楽に弱い)
[set f.seishi=50]           ; 精液充填量 0-100 (高いほど搾りやすい)
[set f.resistance=100]      ; 快楽耐性 (inmakuで低下: 100-inmaku*25)

;--- チャプターフラグ ---
[set f.chapter=0]
[set f.prolog_done=0]
[set f.chap1_done=0]
[set f.chap2_slime=0]
[set f.chap2_succubus=0]
[set f.chap2_witch=0]
[set f.chap3_done=0]

;--- 搾精記録 (エンディング分岐用) ---
[set f.squeeze_total=0]     ; 搾精された合計回数
[set f.resist_count=0]      ; 抵抗成功回数
[set f.surrender_count=0]   ; 自ら従った回数

;--- イベントフラグ ---
[set f.maou_met=0]          ; 魔王と接触済み
[set f.goddess_power=1]     ; 女神の加護レベル (脱出に使用)

[return]

;==========================================================
; 淫紋レベルアップ処理
;==========================================================
*inmaku_up

[if exp="f.inmaku < 3"]
  [set f.inmaku=f.inmaku+1]
  [set f.resistance=100-(f.inmaku*25)]
  [if exp="f.inmaku==1"]
    [nm t="システム"]
    淫紋が脈動する……快楽への感度がわずかに上がった気がする。[p]
  [endif]
  [if exp="f.inmaku==2"]
    [nm t="システム"]
    淫紋の輝きが増す……身体が熱い。少し触れられただけでも反応してしまいそうだ。[p]
  [endif]
  [if exp="f.inmaku==3"]
    [nm t="システム"]
    淫紋が激しく脈動する……もはや快楽への耐性はほぼ失われた。[p]
  [endif]
[endif]

[return]

;==========================================================
; 搾精イベント共通処理
;==========================================================
*squeeze_event

[set f.squeeze_total=f.squeeze_total+1]
[set f.seishi=f.seishi-30]
[if exp="f.seishi < 0"]
  [set f.seishi=0]
[endif]
; 搾られた後は少し充填される
[eval exp="f.seishi = Math.min(f.seishi+10, 100)"]

[return]

;==========================================================
; セーブ画面呼び出し (共通)
;==========================================================
*call_save
[call_save]
[return]
