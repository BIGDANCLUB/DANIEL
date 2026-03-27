;==========================================================
; assets.ks - 素材一覧（Phase 3: 素材挿入用リファレンス）
; このファイルは実行されません。素材名の管理用です。
;==========================================================

;==========================================================
; 【背景画像】 data/image/bg/ に配置 (.jpg or .png, 1280x720)
;==========================================================

; --- 魔王城・外観 ---
; bg_maou_castle_front.jpg     魔王城正面・嵐の夜
; bg_throne_room.jpg           玉座の間・通常
; bg_throne_room_battle.jpg    玉座の間・戦闘エフェクトあり
; bg_throne_room_damaged.jpg   玉座の間・戦闘後・壊れた石
; bg_throne_room_dawn.jpg      玉座の間・夜明けの光

; --- 城内・共通 ---
; bg_castle_corridor.jpg       メイン回廊
; bg_castle_map.jpg            城の見取り図風（第2章ハブ）
; bg_prison_cell.jpg           牢獄・暗い石造り

; --- B1F ---
; bg_underground_waterway.jpg  地下水路・暗い・水滴
; bg_underground_lake.jpg      地下湖・薄い光
; bg_underground_storage.jpg   地下倉庫・宝箱が並ぶ

; --- 1F ---
; bg_central_hall.jpg          中央大広間・石造り
; bg_central_hall_shadow.jpg   中央大広間・影多め（くのいち用）
; bg_training_hall.jpg         訓練場・武器が並ぶ

; --- 2F ---
; bg_upper_corridor.jpg        上層回廊・紫の光
; bg_upper_corridor_sky.jpg    上層吹き抜け回廊・空が見える（ハーピー用）
; bg_upper_corridor_lamia.jpg  上層回廊・蛇の鱗の模様

; --- 3F ---
; bg_research_tower.jpg        研究棟・外観
; bg_greenhouse.jpg            温室・花と植物（アルラウネ用）
; bg_witch_lab.jpg             魔女実験室・フラスコ多数
; bg_laboratory.jpg            科学者実験室・機械と薬品
; bg_infirmary.jpg             医務室・白い内装

; --- 4F ---
; bg_residential.jpg           居住区・廊下
; bg_chapel.jpg                礼拝堂・蝋燭の光（シスター用）
; bg_massage_room.jpg          マッサージ室・アロマ雰囲気
; bg_tavern_room.jpg           個室・ソファ・暖色（娼婦用）
; bg_dark_room.jpg             薄暗い部屋・窓の光のみ（ダウナー用）

; --- 5F ---
; bg_top_floor_boss.jpg        最上部・豪華な空間（上級サキュバス）

; --- エンディング ---
; bg_castle_garden.jpg         魔王城の庭・昼間
; bg_black.jpg                 真っ黒（クレジット用）

;==========================================================
; 【立ち絵】 data/image/chara/ に配置 (.png, 透過, 縦長)
; 推奨サイズ: 幅400-600px × 高さ700-1000px
;==========================================================

; maou_normal.png              魔王リリス・通常
; maou_throne.png              魔王・玉座に座った状態
; maou_kneel.png               魔王・膝をついた敗北後
; maou_surprised.png           魔王・驚き
; maou_smile.png               魔王・珍しく笑顔

; megami_spirit.png            女神・半透明の霊体

; slime_normal.png             スライム・全体像
; tentacle_normal.png          触手系魔物

; mermaid_normal.png           マーメイド・上半身
; mimic_closed.png             ミミック・宝箱状態
; mimic_open.png               ミミック・開いた状態

; thief_normal.png             女盗賊・通常
; kunoichi_normal.png          くのいち・通常
; fighter_normal.png           女戦士・鎧あり
; fighter_armor_off.png        女戦士・鎧なし（Hシーン用）

; lamia_normal.png             ラミア・通常
; harpy_normal.png             ハーピー・翼広げ
; succubus_normal.png          サキュバス・通常
; sr_succubus_normal.png       上級サキュバス・通常

; alraune_normal.png           アルラウネ・花の中
; witch_normal.png             ウィッチ・通常（眼鏡あり）
; scientist_normal.png         科学者・白衣
; nurse_normal.png             ナース・制服

; sister_normal.png            シスター・修道服
; massage_normal.png           マッサージ師・施術着
; prostitute_normal.png        娼婦・豪華な服
; downer_normal.png            ダウナー女性・暗めの服

;==========================================================
; 【イベントCG】 data/image/event/ に配置 (.jpg, 1280x720)
; ※Hシーン用。各キャラ1〜3枚構成
;==========================================================

; inmaku_carve.jpg             プロローグ・淫紋刻印シーン

; slime_h01.jpg                スライム・搾精シーン
; slime_h02.jpg                スライム・（差分）

; tentacle_h01.jpg             触手・全身拘束

; mimic_h01.jpg                ミミック・箱内

; mermaid_h_offer01.jpg        マーメイド・水際（合意）
; mermaid_h_force01.jpg        マーメイド・水中（強制）

; thief_h_deal01.jpg           女盗賊・取引
; thief_h_force01.jpg          女盗賊・強制

; kunoichi_h01.jpg             くのいち・麻痺

; fighter_h_offer01.jpg        女戦士・同意

; lamia_h01.jpg                ラミア・催眠拘束

; harpy_h01.jpg                ハーピー・翼拘束

; succubus_h_consent01.jpg     サキュバス・合意
; succubus_h_force01.jpg       サキュバス・強制

; alraune_h_deal01.jpg         アルラウネ・受粉
; alraune_h_sleep01.jpg        アルラウネ・睡眠

; witch_h_deal01.jpg           ウィッチ・取引
; witch_h_bind01.jpg           ウィッチ・拘束

; scientist_h01.jpg            科学者・実験

; nurse_h01.jpg                ナース・医療

; sister_h01.jpg               シスター・儀式

; massage_h01.jpg              マッサージ師・施術

; prostitute_h01.jpg           娼婦・サービス

; downer_h01.jpg               ダウナー女性・静か

; sr_succubus_h01.jpg          上級サキュバス・1枚目
; sr_succubus_h02.jpg          上級サキュバス・絶頂

; maou_h01.jpg                 魔王リリス・和解の夜・1枚目
; maou_h02.jpg                 魔王リリス・2枚目
; maou_h03.jpg                 魔王リリス・絶頂差分

;==========================================================
; 【UI画像】 data/image/ui/ に配置
;==========================================================

; title_bg.jpg                 タイトル画面背景 (1280x720)
; title_logo.png               ゲームタイトルロゴ (透過PNG)
; chapter_title.png            章タイトル枠
; textwindow.png               テキストウィンドウ (透過PNG)
; namebox.png                  名前欄
; ending_a.png                 END A テキスト
; ending_b.png                 END B テキスト
; gameover.png                 GAME OVER テキスト

;==========================================================
; 【BGM】 data/sound/bgm/ に配置 (.ogg 推奨)
;==========================================================

; title.ogg                    タイトル画面
; bgm_castle_exploration.ogg   城内探索（メイン）
; bgm_dungeon_ambient.ogg      地下水路・不気味
; bgm_dungeon_eerie.ogg        地下・暗め
; bgm_seductive.ogg            上層回廊・魅惑的
; bgm_mysterious.ogg           研究棟・不思議
; bgm_residential.ogg          居住区・日常感
; bgm_battle_serious.ogg       戦闘・シリアス
; bgm_miniboss.ogg             上級サキュバス戦
; bgm_maou_theme.ogg           魔王テーマ
; bgm_final_approach.ogg       玉座への道
; bgm_ending_peaceful.ogg      END A エンディング
; bgm_ending_warm.ogg          END B エンディング
; bgm_credits.ogg              クレジット
; bgm_gameover.ogg             ゲームオーバー

;==========================================================
; 【SE】 data/sound/se/ に配置 (.ogg 推奨)
;==========================================================

; se_explosion.ogg             爆発・魔法
; se_heavenly_bell.ogg         女神登場
; se_chain_break.ogg           枷が砕ける
; se_lock_open.ogg             錠前が開く
; se_battle_start.ogg          戦闘開始
; se_battle_start_boss.ogg     ボス戦開始
; se_wing_flap.ogg             翼・羽ばたき
; se_smoke_bomb.ogg            煙幕
; se_magic_circle.ogg          魔法陣
; se_seal_break.ogg            封印破壊
; se_goddess_shield.ogg        女神の盾
; se_goddess_power_up.ogg      女神の力解放
; se_mimic_appear.ogg          ミミック出現
; se_heavenly_bell.ogg         女神の鈴

[s]
