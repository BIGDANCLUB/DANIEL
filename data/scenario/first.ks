;==========================================================
; first.ks - ゲームエントリーポイント・タイトル画面
;==========================================================
*start

[call storage="system/macro.ks"]

[iscript]
(function() {
    if (!document.getElementById('hold_skip_loaded')) {
        var s1 = document.createElement('script');
        s1.id = 'hold_skip_loaded';
        s1.src = 'data/js/hold_skip.js?' + Date.now();
        document.head.appendChild(s1);
    }
    if (!document.getElementById('msg_controls_loaded')) {
        var s2 = document.createElement('script');
        s2.id = 'msg_controls_loaded';
        s2.src = 'data/js/message_controls.js?' + Date.now();
        document.head.appendChild(s2);
    }
})();
[endscript]

[wait time=300]

; タイトルBGM
; [bgm storage="title.ogg" loop=true]

; タイトル背景
; [bg storage="title_bg.jpg" time="1000"]

; ---- カスタムタイトルメニュー ----
[nm t=""]

[r]
[r]
[r]
[r]
[r]
[r]
勇者と魔王城の淫紋[r]
[r]
[link target="*newgame"]　　►  ニューゲーム[endlink][r]
[link target="*load"]　　►  ロード[endlink][r]
[link target="*config"]　　►  設定[endlink][r]
[link target="*recollection"]　　►  回想部屋[endlink][r]
[s]

;==========================================================
; ニューゲーム開始
;==========================================================
*newgame

[call storage="system/init.ks" target="*init"]
[jump storage="prologue.ks"]

;==========================================================
; ロード
;==========================================================
*load

[showload]
[jump storage="first.ks" target="*start"]

;==========================================================
; コンフィグ
;==========================================================
*config

[showconfig]
[jump storage="first.ks" target="*start"]

;==========================================================
; 回想部屋
;==========================================================
*recollection

[jump storage="recollection_room.ks" target="*recollection_start"]
