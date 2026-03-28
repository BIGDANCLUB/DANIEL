;==========================================================
; macro.ks - カスタムマクロ定義
;==========================================================

; [nm t="キャラ名"] → 名前ボックスに名前を表示するマクロ
; TyranoScript V6 では [position] タグで name 属性を設定する
[macro name="nm"]
[position layer="message0" page=fore name="%t"]
[endmacro]

[return]
