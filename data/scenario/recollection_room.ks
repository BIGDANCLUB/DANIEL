;==========================================================
; recollection_room.ks - 回想部屋
; タイトル画面から呼び出される
;==========================================================
*recollection_start

[call storage="system/macro.ks"]

; JavaScript マップを読み込む
[iscript]
(function() {
    var s = document.createElement('script');
    s.src = 'data/js/recollection_map.js?' + Date.now();
    document.head.appendChild(s);
})();
[endscript]

; JSがCanvas制御を引き継ぐので停止
[s]

;==========================================================
; スライム 回想シーン
;==========================================================
*recall_slime_h1
[call storage="system/macro.ks"]
[jump storage="chap2_slime.ks" target="*slime_h1"]

*recall_slime_h2
[call storage="system/macro.ks"]
[jump storage="chap2_slime.ks" target="*slime_h2"]

*recall_slime_h3
[call storage="system/macro.ks"]
[jump storage="chap2_slime.ks" target="*slime_h3"]

*recall_slime_h4
[call storage="system/macro.ks"]
[jump storage="chap2_slime.ks" target="*slime_h4"]

*recall_slime_h5
[call storage="system/macro.ks"]
[jump storage="chap2_slime.ks" target="*slime_h5"]

;==========================================================
; 触手系 回想
;==========================================================
*recall_tentacle_h1
[call storage="system/macro.ks"]
[jump storage="chap2_tentacle.ks" target="*tentacle_h1"]

*recall_tentacle_h2
[call storage="system/macro.ks"]
[jump storage="chap2_tentacle.ks" target="*tentacle_h2"]

*recall_tentacle_h3
[call storage="system/macro.ks"]
[jump storage="chap2_tentacle.ks" target="*tentacle_h3"]

*recall_tentacle_h4
[call storage="system/macro.ks"]
[jump storage="chap2_tentacle.ks" target="*tentacle_h4"]

*recall_tentacle_h5
[call storage="system/macro.ks"]
[jump storage="chap2_tentacle.ks" target="*tentacle_h5"]

;==========================================================
; ミミック 回想
;==========================================================
*recall_mimic_h1
[call storage="system/macro.ks"]
[jump storage="chap2_mimic.ks" target="*mimic_h1"]

*recall_mimic_h2
[call storage="system/macro.ks"]
[jump storage="chap2_mimic.ks" target="*mimic_h2"]

*recall_mimic_h3
[call storage="system/macro.ks"]
[jump storage="chap2_mimic.ks" target="*mimic_h3"]

*recall_mimic_h4
[call storage="system/macro.ks"]
[jump storage="chap2_mimic.ks" target="*mimic_h4"]

*recall_mimic_h5
[call storage="system/macro.ks"]
[jump storage="chap2_mimic.ks" target="*mimic_h5"]

;==========================================================
; 人魚 回想
;==========================================================
*recall_mermaid_h1
[call storage="system/macro.ks"]
[jump storage="chap2_mermaid.ks" target="*mermaid_h1"]

*recall_mermaid_h2
[call storage="system/macro.ks"]
[jump storage="chap2_mermaid.ks" target="*mermaid_h2"]

*recall_mermaid_h3
[call storage="system/macro.ks"]
[jump storage="chap2_mermaid.ks" target="*mermaid_h3"]

*recall_mermaid_h4
[call storage="system/macro.ks"]
[jump storage="chap2_mermaid.ks" target="*mermaid_h4"]

*recall_mermaid_h5
[call storage="system/macro.ks"]
[jump storage="chap2_mermaid.ks" target="*mermaid_h5"]

;==========================================================
; 女盗賊 回想
;==========================================================
*recall_thief_h1
[call storage="system/macro.ks"]
[jump storage="chap2_thief.ks" target="*thief_h1"]

*recall_thief_h2
[call storage="system/macro.ks"]
[jump storage="chap2_thief.ks" target="*thief_h2"]

*recall_thief_h3
[call storage="system/macro.ks"]
[jump storage="chap2_thief.ks" target="*thief_h3"]

*recall_thief_h4
[call storage="system/macro.ks"]
[jump storage="chap2_thief.ks" target="*thief_h4"]

*recall_thief_h5
[call storage="system/macro.ks"]
[jump storage="chap2_thief.ks" target="*thief_h5"]

;==========================================================
; くのいち 回想
;==========================================================
*recall_kunoichi_h1
[call storage="system/macro.ks"]
[jump storage="chap2_kunoichi.ks" target="*kunoichi_h1"]

*recall_kunoichi_h2
[call storage="system/macro.ks"]
[jump storage="chap2_kunoichi.ks" target="*kunoichi_h2"]

*recall_kunoichi_h3
[call storage="system/macro.ks"]
[jump storage="chap2_kunoichi.ks" target="*kunoichi_h3"]

*recall_kunoichi_h4
[call storage="system/macro.ks"]
[jump storage="chap2_kunoichi.ks" target="*kunoichi_h4"]

*recall_kunoichi_h5
[call storage="system/macro.ks"]
[jump storage="chap2_kunoichi.ks" target="*kunoichi_h5"]

;==========================================================
; 女戦士 回想
;==========================================================
*recall_fighter_h1
[call storage="system/macro.ks"]
[jump storage="chap2_fighter.ks" target="*fighter_h1"]

*recall_fighter_h2
[call storage="system/macro.ks"]
[jump storage="chap2_fighter.ks" target="*fighter_h2"]

*recall_fighter_h3
[call storage="system/macro.ks"]
[jump storage="chap2_fighter.ks" target="*fighter_h3"]

*recall_fighter_h4
[call storage="system/macro.ks"]
[jump storage="chap2_fighter.ks" target="*fighter_h4"]

*recall_fighter_h5
[call storage="system/macro.ks"]
[jump storage="chap2_fighter.ks" target="*fighter_h5"]

;==========================================================
; ラミア 回想
;==========================================================
*recall_lamia_h1
[call storage="system/macro.ks"]
[jump storage="chap2_lamia.ks" target="*lamia_h1"]

*recall_lamia_h2
[call storage="system/macro.ks"]
[jump storage="chap2_lamia.ks" target="*lamia_h2"]

*recall_lamia_h3
[call storage="system/macro.ks"]
[jump storage="chap2_lamia.ks" target="*lamia_h3"]

*recall_lamia_h4
[call storage="system/macro.ks"]
[jump storage="chap2_lamia.ks" target="*lamia_h4"]

*recall_lamia_h5
[call storage="system/macro.ks"]
[jump storage="chap2_lamia.ks" target="*lamia_h5"]

;==========================================================
; ハーピー 回想
;==========================================================
*recall_harpy_h1
[call storage="system/macro.ks"]
[jump storage="chap2_harpy.ks" target="*harpy_h1"]

*recall_harpy_h2
[call storage="system/macro.ks"]
[jump storage="chap2_harpy.ks" target="*harpy_h2"]

*recall_harpy_h3
[call storage="system/macro.ks"]
[jump storage="chap2_harpy.ks" target="*harpy_h3"]

*recall_harpy_h4
[call storage="system/macro.ks"]
[jump storage="chap2_harpy.ks" target="*harpy_h4"]

*recall_harpy_h5
[call storage="system/macro.ks"]
[jump storage="chap2_harpy.ks" target="*harpy_h5"]

;==========================================================
; サキュバス 回想
;==========================================================
*recall_succubus_h1
[call storage="system/macro.ks"]
[jump storage="chap2_succubus.ks" target="*succubus_h1"]

*recall_succubus_h2
[call storage="system/macro.ks"]
[jump storage="chap2_succubus.ks" target="*succubus_h2"]

*recall_succubus_h3
[call storage="system/macro.ks"]
[jump storage="chap2_succubus.ks" target="*succubus_h3"]

*recall_succubus_h4
[call storage="system/macro.ks"]
[jump storage="chap2_succubus.ks" target="*succubus_h4"]

*recall_succubus_h5
[call storage="system/macro.ks"]
[jump storage="chap2_succubus.ks" target="*succubus_h5"]

;==========================================================
; アルラウネ 回想
;==========================================================
*recall_alraune_h1
[call storage="system/macro.ks"]
[jump storage="chap2_alraune.ks" target="*alraune_h1"]

*recall_alraune_h2
[call storage="system/macro.ks"]
[jump storage="chap2_alraune.ks" target="*alraune_h2"]

*recall_alraune_h3
[call storage="system/macro.ks"]
[jump storage="chap2_alraune.ks" target="*alraune_h3"]

*recall_alraune_h4
[call storage="system/macro.ks"]
[jump storage="chap2_alraune.ks" target="*alraune_h4"]

*recall_alraune_h5
[call storage="system/macro.ks"]
[jump storage="chap2_alraune.ks" target="*alraune_h5"]

;==========================================================
; 魔女 回想
;==========================================================
*recall_witch_h1
[call storage="system/macro.ks"]
[jump storage="chap2_witch.ks" target="*witch_h1"]

*recall_witch_h2
[call storage="system/macro.ks"]
[jump storage="chap2_witch.ks" target="*witch_h2"]

*recall_witch_h3
[call storage="system/macro.ks"]
[jump storage="chap2_witch.ks" target="*witch_h3"]

*recall_witch_h4
[call storage="system/macro.ks"]
[jump storage="chap2_witch.ks" target="*witch_h4"]

*recall_witch_h5
[call storage="system/macro.ks"]
[jump storage="chap2_witch.ks" target="*witch_h5"]

;==========================================================
; 科学者 回想
;==========================================================
*recall_scientist_h1
[call storage="system/macro.ks"]
[jump storage="chap2_scientist.ks" target="*scientist_h1"]

*recall_scientist_h2
[call storage="system/macro.ks"]
[jump storage="chap2_scientist.ks" target="*scientist_h2"]

*recall_scientist_h3
[call storage="system/macro.ks"]
[jump storage="chap2_scientist.ks" target="*scientist_h3"]

*recall_scientist_h4
[call storage="system/macro.ks"]
[jump storage="chap2_scientist.ks" target="*scientist_h4"]

*recall_scientist_h5
[call storage="system/macro.ks"]
[jump storage="chap2_scientist.ks" target="*scientist_h5"]

;==========================================================
; ナース 回想
;==========================================================
*recall_nurse_h1
[call storage="system/macro.ks"]
[jump storage="chap2_nurse.ks" target="*nurse_h1"]

*recall_nurse_h2
[call storage="system/macro.ks"]
[jump storage="chap2_nurse.ks" target="*nurse_h2"]

*recall_nurse_h3
[call storage="system/macro.ks"]
[jump storage="chap2_nurse.ks" target="*nurse_h3"]

*recall_nurse_h4
[call storage="system/macro.ks"]
[jump storage="chap2_nurse.ks" target="*nurse_h4"]

*recall_nurse_h5
[call storage="system/macro.ks"]
[jump storage="chap2_nurse.ks" target="*nurse_h5"]

;==========================================================
; シスター 回想
;==========================================================
*recall_sister_h1
[call storage="system/macro.ks"]
[jump storage="chap2_sister.ks" target="*sister_h1"]

*recall_sister_h2
[call storage="system/macro.ks"]
[jump storage="chap2_sister.ks" target="*sister_h2"]

*recall_sister_h3
[call storage="system/macro.ks"]
[jump storage="chap2_sister.ks" target="*sister_h3"]

*recall_sister_h4
[call storage="system/macro.ks"]
[jump storage="chap2_sister.ks" target="*sister_h4"]

*recall_sister_h5
[call storage="system/macro.ks"]
[jump storage="chap2_sister.ks" target="*sister_h5"]

;==========================================================
; マッサージ師 回想
;==========================================================
*recall_massage_h1
[call storage="system/macro.ks"]
[jump storage="chap2_massage.ks" target="*massage_h1"]

*recall_massage_h2
[call storage="system/macro.ks"]
[jump storage="chap2_massage.ks" target="*massage_h2"]

*recall_massage_h3
[call storage="system/macro.ks"]
[jump storage="chap2_massage.ks" target="*massage_h3"]

*recall_massage_h4
[call storage="system/macro.ks"]
[jump storage="chap2_massage.ks" target="*massage_h4"]

*recall_massage_h5
[call storage="system/macro.ks"]
[jump storage="chap2_massage.ks" target="*massage_h5"]

;==========================================================
; 娼婦 回想
;==========================================================
*recall_prostitute_h1
[call storage="system/macro.ks"]
[jump storage="chap2_prostitute.ks" target="*prostitute_h1"]

*recall_prostitute_h2
[call storage="system/macro.ks"]
[jump storage="chap2_prostitute.ks" target="*prostitute_h2"]

*recall_prostitute_h3
[call storage="system/macro.ks"]
[jump storage="chap2_prostitute.ks" target="*prostitute_h3"]

*recall_prostitute_h4
[call storage="system/macro.ks"]
[jump storage="chap2_prostitute.ks" target="*prostitute_h4"]

*recall_prostitute_h5
[call storage="system/macro.ks"]
[jump storage="chap2_prostitute.ks" target="*prostitute_h5"]

;==========================================================
; ダウナー 回想
;==========================================================
*recall_downer_h1
[call storage="system/macro.ks"]
[jump storage="chap2_downer.ks" target="*downer_h1"]

*recall_downer_h2
[call storage="system/macro.ks"]
[jump storage="chap2_downer.ks" target="*downer_h2"]

*recall_downer_h3
[call storage="system/macro.ks"]
[jump storage="chap2_downer.ks" target="*downer_h3"]

*recall_downer_h4
[call storage="system/macro.ks"]
[jump storage="chap2_downer.ks" target="*downer_h4"]

*recall_downer_h5
[call storage="system/macro.ks"]
[jump storage="chap2_downer.ks" target="*downer_h5"]

;==========================================================
; 上級サキュバス 回想
;==========================================================
*recall_sr_succubus_h1
[call storage="system/macro.ks"]
[jump storage="chap2_sr_succubus.ks" target="*sr_succubus_h1"]

*recall_sr_succubus_h2
[call storage="system/macro.ks"]
[jump storage="chap2_sr_succubus.ks" target="*sr_succubus_h2"]

*recall_sr_succubus_h3
[call storage="system/macro.ks"]
[jump storage="chap2_sr_succubus.ks" target="*sr_succubus_h3"]

*recall_sr_succubus_h4
[call storage="system/macro.ks"]
[jump storage="chap2_sr_succubus.ks" target="*sr_succubus_h4"]

*recall_sr_succubus_h5
[call storage="system/macro.ks"]
[jump storage="chap2_sr_succubus.ks" target="*sr_succubus_h5"]

;==========================================================
; 魔王リリス 回想
;==========================================================
*recall_maou_h1
[call storage="system/macro.ks"]
[jump storage="chap3_maou.ks" target="*maou_h1"]

*recall_maou_h2
[call storage="system/macro.ks"]
[jump storage="chap3_maou.ks" target="*maou_h2"]

*recall_maou_h3
[call storage="system/macro.ks"]
[jump storage="chap3_maou.ks" target="*maou_h3"]
