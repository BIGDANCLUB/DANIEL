// message_controls.js
// L キー: メッセージログ表示/非表示
// A キー: オートモード ON/OFF トグル
(function () {
    'use strict';

    // ===== キー設定 =====
    var BACKLOG_KEY = 'l'; // メッセージログ
    var AUTO_KEY    = 'a'; // オートモード
    // ====================

    // ---- AUTO インジケーター ----
    var indicator = null;

    function getIndicator() {
        if (indicator) return indicator;
        indicator = document.createElement('div');
        indicator.style.cssText = [
            'position:fixed',
            'top:12px',
            'right:16px',
            'background:rgba(0,0,0,0.75)',
            'color:#ffcc44',
            'border:1px solid #ffcc44',
            'border-radius:4px',
            'padding:3px 10px',
            'font:bold 14px sans-serif',
            'letter-spacing:2px',
            'z-index:8000',
            'pointer-events:none',
            'display:none'
        ].join(';');
        indicator.textContent = 'AUTO';
        document.body.appendChild(indicator);
        return indicator;
    }

    function syncIndicator() {
        var on = isAutoOn();
        getIndicator().style.display = on ? 'block' : 'none';
    }

    // ---- AUTO 状態取得 ----
    function isAutoOn() {
        try {
            var kag = TYRANO.kag;
            // TyranoScript V6 は stat.is_auto を使用
            if (kag.stat && kag.stat.is_auto != null) return !!kag.stat.is_auto;
            // フォールバック
            if (kag.tmp && kag.tmp.is_auto != null) return !!kag.tmp.is_auto;
        } catch (e) {}
        return false;
    }

    // ---- AUTO 開始 ----
    function startAuto() {
        try {
            var kag = TYRANO.kag;
            if (kag.menu && typeof kag.menu.startAuto === 'function') {
                kag.menu.startAuto();
            } else {
                // 直接フラグをセット
                if (kag.stat) kag.stat.is_auto = true;
                // 現在テキスト待ち状態なら次へ進める
                kag.ftag && kag.ftag.nextOrder && kag.ftag.nextOrder();
            }
        } catch (e) {}
    }

    // ---- AUTO 停止 ----
    function stopAuto() {
        try {
            var kag = TYRANO.kag;
            if (kag.menu && typeof kag.menu.stopAuto === 'function') {
                kag.menu.stopAuto();
            } else {
                if (kag.stat) kag.stat.is_auto = false;
            }
        } catch (e) {}
    }

    // ---- AUTO トグル ----
    function toggleAuto() {
        if (isAutoOn()) {
            stopAuto();
        } else {
            startAuto();
        }
        // 少し遅らせてインジケーター更新（API が非同期の場合があるため）
        setTimeout(syncIndicator, 80);
    }

    // ---- バックログ表示 ----
    function showBackLog() {
        try {
            var kag = TYRANO.kag;
            // 方法1: menu API
            if (kag.menu && typeof kag.menu.showBackLog === 'function') {
                kag.menu.showBackLog();
                return;
            }
            // 方法2: タグ実行
            if (kag.ftag && typeof kag.ftag.startTag === 'function') {
                kag.ftag.startTag('backlog', {});
                return;
            }
        } catch (e) {}
    }

    // ---- キーイベント ----
    document.addEventListener('keydown', function (e) {
        // 入力フィールド内は無視
        var tag = e.target.tagName;
        if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
        // 回想部屋マップ中は無視（canvas がフォーカス中）
        if (document.querySelector('canvas') &&
            document.querySelector('canvas').style.zIndex >= 9000) return;

        var key = e.key.toLowerCase();

        if (key === BACKLOG_KEY) {
            showBackLog();
            e.preventDefault();
        } else if (key === AUTO_KEY) {
            toggleAuto();
            e.preventDefault();
        }
    });

    // ---- クリックでAUTO解除されたときインジケーターを同期 ----
    document.addEventListener('click', function () {
        setTimeout(syncIndicator, 100);
    });

    // ---- 定期チェック（外部からAUTOが止まった場合も追従） ----
    setInterval(syncIndicator, 500);

    console.log('[message_controls] loaded.  BackLog=' + BACKLOG_KEY.toUpperCase() +
                '  Auto=' + AUTO_KEY.toUpperCase());
})();
