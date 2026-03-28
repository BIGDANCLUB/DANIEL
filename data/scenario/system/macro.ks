;==========================================================
; macro.ks - カスタムマクロ定義
;==========================================================

; [nm t="キャラ名"] → 名前ボックスに名前を表示するマクロ
[macro name="nm"]
[position layer="message0" page=fore name="%t"]
[endmacro]

; [fadeout time=xxx color=xxx] → 暗転マクロ
[macro name="fadeout"]
[layeropt layer="base" opacity=0]
[wait time="%time"]
[endmacro]

; [fadein time=xxx] → 明転マクロ
[macro name="fadein"]
[layeropt layer="base" opacity=255]
[wait time="%time"]
[endmacro]

[return]
