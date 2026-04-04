;==========================================================
; first.ks - ゲームエントリーポイント・タイトル画面
;==========================================================
*start

[call storage="system/macro.ks"]

[iscript]
(function() {
    if (document.getElementById('hold_skip_loaded')) return;
    var s = document.createElement('script');
    s.id = 'hold_skip_loaded';
    s.src = 'data/js/hold_skip.js?' + Date.now();
    document.head.appendChild(s);
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
