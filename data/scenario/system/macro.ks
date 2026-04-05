;==========================================================
; macro.ks - カスタムマクロ定義
;==========================================================

; アセットマクロ（cg / bg_set / bgm_on 等）を読み込む
[call storage="system/assets.ks"]

; [nm t="キャラ名"] → 名前ボックスに名前を表示するマクロ
[macro name="nm"]
[position layer="message0" page=fore name="%t"]
[endmacro]

; [fadeout time=xxx color=xxx] → 暗転（素材なし期間は待機のみ）
[macro name="fadeout"]
[wait time="%time"]
[endmacro]

; [fadein time=xxx] → 明転（素材なし期間は待機のみ）
[macro name="fadein"]
[wait time="%time"]
[endmacro]

[return]
