// recollection_map.js
// 回想部屋 - キーボード操作マップシステム
(function () {
    'use strict';

    var CANVAS_W = 1280;
    var CANVAS_H = 720;
    var PLAYER_R = 12;
    var NPC_R = 18;
    var BOOK_R = 16;
    var INTERACT_RANGE = 55;
    var MOVE_SPEED = 3;

    // NPC定義（位置・シーン数）
    var NPC_DATA = [
        // B1F エリア（左下）
        { id: 'slime',      name: 'スライム',     x: 80,  y: 630, scenes: 5, area: 'B1F' },
        { id: 'tentacle',   name: '触手系魔物',   x: 160, y: 630, scenes: 5, area: 'B1F' },
        { id: 'mimic',      name: 'ミミック',     x: 240, y: 630, scenes: 5, area: 'B1F' },
        { id: 'mermaid',    name: '人魚',         x: 320, y: 630, scenes: 5, area: 'B1F' },
        // 1F エリア
        { id: 'thief',      name: '女盗賊',       x: 80,  y: 510, scenes: 5, area: '1F' },
        { id: 'kunoichi',   name: 'くのいち',     x: 180, y: 510, scenes: 5, area: '1F' },
        { id: 'fighter',    name: '女戦士',       x: 280, y: 510, scenes: 5, area: '1F' },
        // 2F エリア
        { id: 'lamia',      name: 'ラミア',       x: 80,  y: 390, scenes: 5, area: '2F' },
        { id: 'harpy',      name: 'ハーピー',     x: 180, y: 390, scenes: 5, area: '2F' },
        { id: 'succubus',   name: 'サキュバス',   x: 280, y: 390, scenes: 5, area: '2F' },
        // 3F エリア（中央下）
        { id: 'alraune',    name: 'アルラウネ',   x: 540, y: 630, scenes: 5, area: '3F' },
        { id: 'witch',      name: '魔女',         x: 640, y: 630, scenes: 5, area: '3F' },
        { id: 'scientist',  name: '科学者',       x: 740, y: 630, scenes: 5, area: '3F' },
        { id: 'nurse',      name: 'ナース',       x: 840, y: 630, scenes: 5, area: '3F' },
        // 4F エリア
        { id: 'sister',     name: 'シスター',     x: 540, y: 510, scenes: 5, area: '4F' },
        { id: 'massage',    name: 'マッサージ師', x: 640, y: 510, scenes: 5, area: '4F' },
        { id: 'prostitute', name: '娼婦',         x: 740, y: 510, scenes: 5, area: '4F' },
        { id: 'downer',     name: 'ダウナー',     x: 840, y: 510, scenes: 5, area: '4F' },
        // 5F エリア（右中）
        { id: 'sr_succubus', name: '上級サキュバス', x: 1050, y: 390, scenes: 5, area: '5F' },
        // 魔王
        { id: 'maou',       name: '魔王リリス',   x: 1150, y: 200, scenes: 3, area: '魔王' },
    ];

    // 古い本オブジェ（回想全開放）
    var BOOK = { x: 480, y: 290, label: '古い本' };

    // プレイヤー状態
    var savedX = 0, savedY = 0;
    try {
        savedX = TYRANO.kag.stat.f['recall_return_x'] || 0;
        savedY = TYRANO.kag.stat.f['recall_return_y'] || 0;
        TYRANO.kag.stat.f['recall_return_x'] = 0;
        TYRANO.kag.stat.f['recall_return_y'] = 0;
    } catch (e) {}
    var player = {
        x: savedX > 0 ? savedX : 640,
        y: savedY > 0 ? savedY : 400
    };

    var nearbyNPC = null;
    var nearBook = false;
    var showMenu = false;
    var showBookConfirm = false;
    var bookConfirmIndex = 1; // 0=はい, 1=いいえ (default いいえ)
    var selectedNPC = null;
    var menuIndex = 0;
    var keys = {};
    var animId = null;

    // Canvas作成
    var canvas = document.createElement('canvas');
    canvas.width = CANVAS_W;
    canvas.height = CANVAS_H;
    canvas.style.cssText = [
        'position:fixed', 'top:0', 'left:0',
        'width:100%', 'height:100%',
        'z-index:9999', 'background:#120820'
    ].join(';');
    document.body.appendChild(canvas);
    var ctx = canvas.getContext('2d');

    // TyranoScriptフラグ取得
    function getFlag(name) {
        try { return TYRANO.kag.stat.f[name] || 0; } catch (e) { return 0; }
    }
    // TyranoScriptフラグセット
    function setFlag(name, value) {
        try { TYRANO.kag.stat.f[name] = value; } catch (e) {}
    }

    // シーン解放チェック
    function isUnlocked(npcId, n) {
        if (getFlag('scene_all_unlocked') == 1) return true;
        return getFlag('scene_' + npcId + '_h' + n) == 1;
    }

    // シーン再生
    function playScene(npcId, n) {
        setFlag('from_recall', 1);
        setFlag('recall_return_x', player.x);
        setFlag('recall_return_y', player.y);
        cleanup();
        canvas.remove();
        try {
            TYRANO.kag.ftag.startTag('jump', {
                storage: 'recollection_room.ks',
                target: '*recall_' + npcId + '_h' + n
            });
        } catch (e) { console.error('playScene error:', e); }
    }

    // 全開放
    function unlockAll() {
        setFlag('scene_all_unlocked', 1);
    }

    // タイトルへ戻る
    function exitToTitle() {
        cleanup();
        canvas.remove();
        try {
            TYRANO.kag.ftag.startTag('jump', { storage: 'first.ks', target: '*start' });
        } catch (e) {}
    }

    // キーダウン
    function onKeyDown(e) {
        keys[e.key] = true;

        if (showBookConfirm) {
            if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { bookConfirmIndex = 0; e.preventDefault(); }
            if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { bookConfirmIndex = 1; e.preventDefault(); }
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                if (bookConfirmIndex === 0) { unlockAll(); }
                showBookConfirm = false;
            }
            if (e.key === 'Escape' || e.key === 'x' || e.key === 'X') {
                showBookConfirm = false;
            }
            return;
        }

        if (showMenu) {
            if (e.key === 'ArrowUp') { menuIndex = Math.max(0, menuIndex - 1); e.preventDefault(); }
            if (e.key === 'ArrowDown') { menuIndex = Math.min(selectedNPC.scenes - 1, menuIndex + 1); e.preventDefault(); }
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                var n = menuIndex + 1;
                if (isUnlocked(selectedNPC.id, n)) { playScene(selectedNPC.id, n); }
            }
            if (e.key === 'Escape' || e.key === 'x' || e.key === 'X') { showMenu = false; }
        } else {
            if ((e.key === ' ' || e.key === 'Enter') && nearBook) {
                e.preventDefault();
                showBookConfirm = true;
                bookConfirmIndex = 1;
            } else if ((e.key === ' ' || e.key === 'Enter') && nearbyNPC) {
                e.preventDefault();
                showMenu = true; selectedNPC = nearbyNPC; menuIndex = 0;
            }
            if (e.key === 'Escape') { exitToTitle(); }
        }
    }
    function onKeyUp(e) { keys[e.key] = false; }
    document.addEventListener('keydown', onKeyDown);
    document.addEventListener('keyup', onKeyUp);

    function cleanup() {
        document.removeEventListener('keydown', onKeyDown);
        document.removeEventListener('keyup', onKeyUp);
        if (animId) cancelAnimationFrame(animId);
    }

    // 更新
    function update() {
        if (showMenu || showBookConfirm) return;
        var dx = 0, dy = 0;
        if (keys['ArrowLeft']  || keys['a'] || keys['A']) dx = -MOVE_SPEED;
        if (keys['ArrowRight'] || keys['d'] || keys['D']) dx =  MOVE_SPEED;
        if (keys['ArrowUp']    || keys['w'] || keys['W']) dy = -MOVE_SPEED;
        if (keys['ArrowDown']  || keys['s'] || keys['S']) dy =  MOVE_SPEED;
        if (dx && dy) { dx *= 0.707; dy *= 0.707; }
        player.x = Math.max(PLAYER_R, Math.min(CANVAS_W - PLAYER_R, player.x + dx));
        player.y = Math.max(50 + PLAYER_R, Math.min(CANVAS_H - 40 - PLAYER_R, player.y + dy));

        nearbyNPC = null;
        for (var i = 0; i < NPC_DATA.length; i++) {
            var npc = NPC_DATA[i];
            if (Math.hypot(npc.x - player.x, npc.y - player.y) < INTERACT_RANGE) {
                nearbyNPC = npc; break;
            }
        }

        nearBook = Math.hypot(BOOK.x - player.x, BOOK.y - player.y) < INTERACT_RANGE;
    }

    // ヒントテキスト
    var HINTS = {
        slime:     ['スライム戦①を間違える', 'スライム戦②を間違える', 'スライム戦③を間違える', 'スライム戦④を間違える', 'スライム戦⑤を間違える'],
        tentacle:  ['触手戦①を間違える', '触手戦②を間違える', '触手戦③を間違える', '触手戦④を間違える', '触手戦⑤を間違える'],
        mimic:     ['ミミック戦①を間違える', 'ミミック戦②を間違える', 'ミミック戦③を間違える', 'ミミック戦④を間違える', 'ミミック戦⑤を間違える'],
        mermaid:   ['人魚戦①を間違える', '人魚戦②を間違える', '人魚戦③を間違える', '人魚戦④を間違える', '人魚戦⑤を間違える'],
        thief:     ['女盗賊戦①を間違える', '女盗賊戦②を間違える', '女盗賊戦③を間違える', '女盗賊戦④を間違える', '女盗賊戦⑤を間違える'],
        kunoichi:  ['くのいち戦①を間違える', 'くのいち戦②を間違える', 'くのいち戦③を間違える', 'くのいち戦④を間違える', 'くのいち戦⑤を間違える'],
        fighter:   ['女戦士戦①を間違える', '女戦士戦②を間違える', '女戦士戦③を間違える', '女戦士戦④を間違える', '女戦士戦⑤を間違える'],
        lamia:     ['ラミア戦①を間違える', 'ラミア戦②を間違える', 'ラミア戦③を間違える', 'ラミア戦④を間違える', 'ラミア戦⑤を間違える'],
        harpy:     ['ハーピー戦①を間違える', 'ハーピー戦②を間違える', 'ハーピー戦③を間違える', 'ハーピー戦④を間違える', 'ハーピー戦⑤を間違える'],
        succubus:  ['サキュバス戦①を間違える', 'サキュバス戦②を間違える', 'サキュバス戦③を間違える', 'サキュバス戦④を間違える', 'サキュバス戦⑤を間違える'],
        alraune:   ['アルラウネ戦①を間違える', 'アルラウネ戦②を間違える', 'アルラウネ戦③を間違える', 'アルラウネ戦④を間違える', 'アルラウネ戦⑤を間違える'],
        witch:     ['魔女戦①を間違える', '魔女戦②を間違える', '魔女戦③を間違える', '魔女戦④を間違える', '魔女戦⑤を間違える'],
        scientist: ['科学者戦①を間違える', '科学者戦②を間違える', '科学者戦③を間違える', '科学者戦④を間違える', '科学者戦⑤を間違える'],
        nurse:     ['ナース戦①を間違える', 'ナース戦②を間違える', 'ナース戦③を間違える', 'ナース戦④を間違える', 'ナース戦⑤を間違える'],
        sister:    ['シスター戦①を間違える', 'シスター戦②を間違える', 'シスター戦③を間違える', 'シスター戦④を間違える', 'シスター戦⑤を間違える'],
        massage:   ['マッサージ師戦①を間違える', 'マッサージ師戦②を間違える', 'マッサージ師戦③を間違える', 'マッサージ師戦④を間違える', 'マッサージ師戦⑤を間違える'],
        prostitute:['娼婦戦①を間違える', '娼婦戦②を間違える', '娼婦戦③を間違える', '娼婦戦④を間違える', '娼婦戦⑤を間違える'],
        downer:    ['ダウナー戦①を間違える', 'ダウナー戦②を間違える', 'ダウナー戦③を間違える', 'ダウナー戦④を間違える', 'ダウナー戦⑤を間違える'],
        sr_succubus:['上級サキュバス戦①を間違える', '上級サキュバス戦②を間違える', '上級サキュバス戦③を間違える', '上級サキュバス戦④を間違える', '上級サキュバス戦⑤を間違える'],
        maou:      ['魔王戦①を間違える', '魔王戦②を間違える', '魔王戦③を間違える'],
    };

    // 描画
    function render() {
        ctx.clearRect(0, 0, CANVAS_W, CANVAS_H);

        // 背景
        ctx.fillStyle = '#120820';
        ctx.fillRect(0, 0, CANVAS_W, CANVAS_H);

        // グリッド
        ctx.strokeStyle = '#1e1035';
        ctx.lineWidth = 1;
        for (var gx = 0; gx < CANVAS_W; gx += 64) {
            ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, CANVAS_H); ctx.stroke();
        }
        for (var gy = 50; gy < CANVAS_H; gy += 64) {
            ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(CANVAS_W, gy); ctx.stroke();
        }

        // エリア区切り線
        ctx.strokeStyle = '#332255';
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(420, 50); ctx.lineTo(420, CANVAS_H - 35); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(950, 50); ctx.lineTo(950, CANVAS_H - 35); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, 450); ctx.lineTo(950, 450); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, 570); ctx.lineTo(950, 570); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(950, 320); ctx.lineTo(CANVAS_W, 320); ctx.stroke();

        // エリアラベル
        ctx.font = '13px sans-serif';
        ctx.fillStyle = '#443366';
        ctx.textAlign = 'left';
        ctx.fillText('B1F 地下水路エリア',  20, 668);
        ctx.fillText('1F  中央廊下エリア',  20, 548);
        ctx.fillText('2F  上位廊下エリア',  20, 428);
        ctx.fillText('3F  研究棟エリア',   460, 668);
        ctx.fillText('4F  居住棟エリア',   460, 548);
        ctx.fillText('5F  最上階エリア',   970, 428);
        ctx.fillText('魔王の間',           990, 240);

        // 古い本オブジェを描画
        ctx.beginPath();
        ctx.arc(BOOK.x, BOOK.y, BOOK_R, 0, Math.PI * 2);
        ctx.fillStyle = nearBook ? '#8b6914' : '#5a4010';
        ctx.fill();
        ctx.strokeStyle = nearBook ? '#ffd700' : '#aa8820';
        ctx.lineWidth = nearBook ? 3 : 1.5;
        ctx.stroke();
        ctx.font = '12px sans-serif';
        ctx.fillStyle = '#ffd700';
        ctx.textAlign = 'center';
        ctx.fillText('📖', BOOK.x, BOOK.y + 5);
        ctx.font = '11px sans-serif';
        ctx.fillStyle = '#ccaa44';
        ctx.fillText(BOOK.label, BOOK.x, BOOK.y + BOOK_R + 13);
        if (nearBook && !showBookConfirm) {
            ctx.font = 'bold 13px sans-serif';
            ctx.fillStyle = '#ffff44';
            ctx.fillText('Spaceで調べる', BOOK.x, BOOK.y - BOOK_R - 6);
        }

        // NPCを描画
        for (var i = 0; i < NPC_DATA.length; i++) {
            var npc = NPC_DATA[i];
            var near = (nearbyNPC === npc);
            ctx.beginPath();
            ctx.arc(npc.x, npc.y, NPC_R, 0, Math.PI * 2);
            ctx.fillStyle = near ? '#cc6622' : '#662200';
            ctx.fill();
            ctx.strokeStyle = near ? '#ffcc44' : '#aa4400';
            ctx.lineWidth = near ? 3 : 1.5;
            ctx.stroke();
            ctx.font = '11px sans-serif';
            ctx.fillStyle = '#eeeeee';
            ctx.textAlign = 'center';
            ctx.fillText(npc.name, npc.x, npc.y + NPC_R + 13);
            if (near && !showMenu) {
                ctx.font = 'bold 13px sans-serif';
                ctx.fillStyle = '#ffff44';
                ctx.fillText('Spaceで話す', npc.x, npc.y - NPC_R - 6);
            }
        }

        // プレイヤー
        ctx.beginPath();
        ctx.arc(player.x, player.y, PLAYER_R, 0, Math.PI * 2);
        ctx.fillStyle = '#4499ff';
        ctx.fill();
        ctx.strokeStyle = '#88ccff';
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.font = 'bold 10px sans-serif';
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.fillText('勇者', player.x, player.y + PLAYER_R + 12);

        // タイトルバー
        ctx.fillStyle = 'rgba(0,0,0,0.85)';
        ctx.fillRect(0, 0, CANVAS_W, 48);
        ctx.font = 'bold 20px sans-serif';
        ctx.fillStyle = '#ffddaa';
        ctx.textAlign = 'left';
        ctx.fillText('回想部屋', 20, 32);
        ctx.font = '13px sans-serif';
        ctx.fillStyle = '#888888';
        ctx.fillText('矢印キー/WASD: 移動  Space/Enter: 話す  Esc: タイトルへ', 200, 32);

        // 下部バー
        ctx.fillStyle = 'rgba(0,0,0,0.8)';
        ctx.fillRect(0, CANVAS_H - 32, CANVAS_W, 32);
        ctx.font = '12px sans-serif';
        ctx.fillStyle = '#666666';
        ctx.textAlign = 'center';
        ctx.fillText('キャラクターに近づいてSpaceキーを押すとHシーン回想メニューが開きます', CANVAS_W / 2, CANVAS_H - 10);

        // メニュー
        if (showMenu && selectedNPC) { drawMenu(); }
        if (showBookConfirm) { drawBookConfirm(); }

        ctx.textAlign = 'left';
    }

    function drawMenu() {
        var npc = selectedNPC;
        var W = 620, itemH = 52;
        var totalItems = npc.scenes;
        var H = totalItems * itemH + 80;
        var mx = (CANVAS_W - W) / 2;
        var my = Math.max(60, (CANVAS_H - H) / 2);

        // 背景
        ctx.fillStyle = 'rgba(8,0,20,0.97)';
        ctx.strokeStyle = '#884422';
        ctx.lineWidth = 2;
        ctx.beginPath();
        if (ctx.roundRect) { ctx.roundRect(mx, my, W, H, 10); } else { ctx.rect(mx, my, W, H); }
        ctx.fill(); ctx.stroke();

        // タイトル
        ctx.font = 'bold 19px sans-serif';
        ctx.fillStyle = '#ffddaa';
        ctx.textAlign = 'center';
        ctx.fillText(npc.name + ' ― 回想シーン', mx + W / 2, my + 38);

        // シーン一覧
        for (var i = 0; i < npc.scenes; i++) {
            var n = i + 1;
            var iy = my + 58 + i * itemH;
            var selected = (menuIndex === i);
            var unlocked = isUnlocked(npc.id, n);

            if (selected) {
                ctx.fillStyle = 'rgba(120,60,20,0.6)';
                ctx.fillRect(mx + 8, iy + 2, W - 16, itemH - 4);
            }

            ctx.textAlign = 'left';
            if (unlocked) {
                ctx.font = '16px sans-serif';
                ctx.fillStyle = selected ? '#ffffff' : '#dddddd';
                ctx.fillText(n + '.  Hシーン ' + '①②③④⑤'[i], mx + 28, iy + 24);
            } else {
                ctx.font = '15px sans-serif';
                ctx.fillStyle = '#555555';
                ctx.fillText(n + '.  ????', mx + 28, iy + 16);
                ctx.font = '11px sans-serif';
                ctx.fillStyle = '#666666';
                var hint = (HINTS[npc.id] && HINTS[npc.id][i]) || 'ストーリーを進める';
                ctx.fillText('条件: ' + hint, mx + 48, iy + 34);
            }
        }

        // ヒント
        ctx.font = '12px sans-serif';
        ctx.fillStyle = '#666666';
        ctx.textAlign = 'center';
        ctx.fillText('↑↓: 選択   Enter/Space: 決定   Esc: 閉じる', mx + W / 2, my + H - 12);
    }

    function drawBookConfirm() {
        var W = 480, H = 180;
        var mx = (CANVAS_W - W) / 2;
        var my = (CANVAS_H - H) / 2;

        // 背景
        ctx.fillStyle = 'rgba(8,0,20,0.97)';
        ctx.strokeStyle = '#aa8820';
        ctx.lineWidth = 2;
        ctx.beginPath();
        if (ctx.roundRect) { ctx.roundRect(mx, my, W, H, 10); } else { ctx.rect(mx, my, W, H); }
        ctx.fill(); ctx.stroke();

        // 本のアイコンとタイトル
        ctx.font = 'bold 18px sans-serif';
        ctx.fillStyle = '#ffd700';
        ctx.textAlign = 'center';
        ctx.fillText('古い本', mx + W / 2, my + 36);

        ctx.font = '15px sans-serif';
        ctx.fillStyle = '#dddddd';
        ctx.fillText('回想全開放しますか？', mx + W / 2, my + 72);

        // はい / いいえボタン
        var btnW = 140, btnH = 44;
        var yesX = mx + W / 2 - btnW - 20;
        var noX  = mx + W / 2 + 20;
        var btnY = my + 100;

        // はい
        ctx.fillStyle = bookConfirmIndex === 0 ? 'rgba(20,100,20,0.8)' : 'rgba(20,60,20,0.4)';
        ctx.beginPath();
        if (ctx.roundRect) { ctx.roundRect(yesX, btnY, btnW, btnH, 6); } else { ctx.rect(yesX, btnY, btnW, btnH); }
        ctx.fill();
        ctx.strokeStyle = bookConfirmIndex === 0 ? '#66ff66' : '#336633';
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.font = 'bold 16px sans-serif';
        ctx.fillStyle = bookConfirmIndex === 0 ? '#aaffaa' : '#669966';
        ctx.fillText('はい', yesX + btnW / 2, btnY + 28);

        // いいえ
        ctx.fillStyle = bookConfirmIndex === 1 ? 'rgba(100,20,20,0.8)' : 'rgba(60,20,20,0.4)';
        ctx.beginPath();
        if (ctx.roundRect) { ctx.roundRect(noX, btnY, btnW, btnH, 6); } else { ctx.rect(noX, btnY, btnW, btnH); }
        ctx.fill();
        ctx.strokeStyle = bookConfirmIndex === 1 ? '#ff6666' : '#663333';
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.fillStyle = bookConfirmIndex === 1 ? '#ffaaaa' : '#996666';
        ctx.fillText('いいえ', noX + btnW / 2, btnY + 28);

        ctx.font = '11px sans-serif';
        ctx.fillStyle = '#666666';
        ctx.fillText('←→: 選択   Enter/Space: 決定   Esc: キャンセル', mx + W / 2, my + H - 10);
    }

    // ゲームループ
    function loop() {
        update();
        render();
        animId = requestAnimationFrame(loop);
    }
    loop();

})();
