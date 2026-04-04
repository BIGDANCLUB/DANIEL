// hold_skip.js
// 特定キーを押し続けている間、メッセージを高速スキップする
(function () {
    'use strict';

    // ===== 設定 =====
    // スキップに使うキー（複数指定可）
    // 'Control' = Ctrlキー, 'PageDown' = PageDown, 'Shift' = Shift など
    var SKIP_KEYS = ['Control', 'PageDown'];
    // ================

    var skipActive = false;
    var pressedKeys = {};

    function startSkip() {
        if (skipActive) return;
        skipActive = true;
        try {
            var kag = TYRANO.kag;
            // TyranoScript V6 スキップ開始
            if (kag.menu && typeof kag.menu.startSkip === 'function') {
                kag.menu.startSkip();
            } else if (kag.stat) {
                kag.stat.is_skip = true;
                // テキスト表示中なら即時完了させる
                if (kag.tmp && kag.tmp.chara_ptext) {
                    kag.tmp.chara_ptext.complete && kag.tmp.chara_ptext.complete();
                }
            }
        } catch (e) {}
    }

    function stopSkip() {
        if (!skipActive) return;
        skipActive = false;
        try {
            var kag = TYRANO.kag;
            if (kag.menu && typeof kag.menu.stopSkip === 'function') {
                kag.menu.stopSkip();
            } else if (kag.stat) {
                kag.stat.is_skip = false;
            }
        } catch (e) {}
    }

    function checkKeys() {
        var anyPressed = false;
        for (var k in pressedKeys) {
            if (pressedKeys[k] && SKIP_KEYS.indexOf(k) !== -1) {
                anyPressed = true;
                break;
            }
        }
        if (anyPressed) {
            startSkip();
        } else {
            stopSkip();
        }
    }

    document.addEventListener('keydown', function (e) {
        if (SKIP_KEYS.indexOf(e.key) !== -1) {
            pressedKeys[e.key] = true;
            if (!e.repeat) checkKeys();
            e.preventDefault();
        }
    });

    document.addEventListener('keyup', function (e) {
        if (SKIP_KEYS.indexOf(e.key) !== -1) {
            pressedKeys[e.key] = false;
            checkKeys();
        }
    });

    // フォーカスを外れたらスキップ解除
    window.addEventListener('blur', function () {
        pressedKeys = {};
        stopSkip();
    });

    console.log('[hold_skip] loaded. Skip keys:', SKIP_KEYS.join(', '));
})();
