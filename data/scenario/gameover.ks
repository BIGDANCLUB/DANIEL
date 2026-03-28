;==========================================================
; gameover.ks - ゲームオーバー処理
; (将来的にHP制を実装する場合に使用)
;==========================================================
*gameover

; [bg storage="bg_black.jpg" time="500"]
; [bgm storage="bgm_gameover.ogg" loop=false]

[fadein time="500"]

[nm t="ナレーション"]
勇者は力尽きた……[p]

; [showmessage storage="ui/gameover.png" text="GAME OVER"]

[wait time=2000]

どうする？[r]
[link target="*go_title"]タイトルに戻る[endlink][r]
[link target="*go_load"]ロードする[endlink][r]
[s]

*go_title
[jump storage="first.ks" target="*start"]

*go_load
[call_load]
[s]
