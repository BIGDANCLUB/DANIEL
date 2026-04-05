;==========================================================
; assets.ks - アセット挿入マクロ集
;
; 【使い方一覧】
;
;  ■ CG（Hシーン差分・枚数は任意）
;    [cg f="slime_h1_01"]          → cg/slime_h1_01.jpg を表示（300ms fade）
;    [cg f="slime_h1_02"]          → 次の差分（02, 03, 04... と連番で何枚でも）
;    [cg f="slime_h1_02" t="0"]    → 瞬間切り替え
;    [cg f="slime_h1_03" t="500"]  → ゆっくりfade
;
;    ※ 枚数はシーンごとに自由。多い場合は _01〜_08 等、連番で追加してください。
;
;  ■ 背景（探索・バトル画面）
;    [bg_set f="dungeon_b1f"]       → bg/dungeon_b1f.jpg
;    [bg_set f="throne_room" t="800"]
;
;  ■ イベントCG（プロローグ等の一枚絵）
;    [ev f="prologue_seal"]          → ev/prologue_seal.jpg
;
;  ■ キャラクタースプライト
;    [ch_show e="slime" p="normal"]  → chara/slime_normal.png 中央配置
;    [ch_show e="maou" p="angry" pos="right"]
;    [ch_hide e="slime"]
;    [ch_all_hide]
;
;  ■ BGM
;    [bgm_on f="battle_b1f"]        → bgm/bgm_battle_b1f.ogg をloop再生
;    [bgm_on f="h_scene" v="70"]    → 音量70で再生
;    [bgm_off]                       → 1500msでフェードアウト停止
;    [bgm_off t="0"]                 → 即停止
;
;  ■ SE
;    [se_on f="chain_break"]        → sound/se_chain_break.ogg を1回再生
;    [se_on f="slime_move" v="60"]
;
;  ■ 動画
;    [mv f="opening"]               → video/mv_opening.mp4 を再生
;
; 【ファイル命名規則】
;   CG差分  : data/bgimage/cg/  → {敵名}_h{n}_{フレーム2桁}.jpg
;             例: slime_h1_01.jpg 〜 slime_h1_06.jpg（枚数自由）
;                 slime_h2_01.jpg 〜 slime_h2_04.jpg（シーンごとに枚数が違ってOK）
;   背景    : data/bgimage/bg/  → {場所名}.jpg
;             例: dungeon_b1f.jpg / throne_room.jpg / prison_cell.jpg
;   イベントCG: data/bgimage/ev/ → {シーンID}.jpg
;             例: prologue_seal.jpg / maou_defeat.jpg
;   スプライト: data/chara/      → {キャラ名}_{ポーズ}.png
;             例: slime_normal.png / maou_angry.png / megami_smile.png
;   BGM     : data/bgm/         → bgm_{名前}.ogg
;             例: bgm_battle_b1f.ogg / bgm_h_scene.ogg / bgm_title.ogg
;   SE      : data/sound/       → se_{名前}.ogg
;             例: se_chain_break.ogg / se_slime_move.ogg
;   動画    : data/video/       → mv_{名前}.mp4
;             例: mv_opening.mp4
;==========================================================

; ---- CG差分（Hシーン内の細かい差分切り替え用）----
; 例: [cg f="slime_h1_01"]  または  [cg f="slime_h1_01" t="0"]
[macro name="cg"]
[bg storage="cg/%f%.jpg" time="%t|300"]
[endmacro]

; ---- 背景（バトル・探索マップ等）----
; 例: [bg_set f="dungeon_b1f"]
[macro name="bg_set"]
[bg storage="bg/%f%.jpg" time="%t|500"]
[endmacro]

; ---- イベントCG（プロローグ・エンディング等の一枚絵）----
; 例: [ev f="prologue_seal"]
[macro name="ev"]
[bg storage="ev/%f%.jpg" time="%t|600"]
[endmacro]

; ---- キャラクタースプライト 表示 ----
; 例: [ch_show e="slime" p="normal"]
; 例: [ch_show e="maou" p="angry" pos="right"]
[macro name="ch_show"]
[chara_show name="%e%" storage="chara/%e%_%p%.png" pos="%pos|center" time="%t|400"]
[endmacro]

; ---- キャラクタースプライト 非表示 ----
; 例: [ch_hide e="slime"]
[macro name="ch_hide"]
[chara_hide name="%e%" time="%t|300"]
[endmacro]

; ---- キャラクタースプライト 全非表示 ----
[macro name="ch_all_hide"]
[chara_hide_all time="%t|300"]
[endmacro]

; ---- BGM 再生 ----
; 例: [bgm_on f="battle_b1f"]
; 例: [bgm_on f="h_scene" v="70"]
[macro name="bgm_on"]
[bgm storage="bgm_%f%.ogg" loop=true volume="%v|80"]
[endmacro]

; ---- BGM 停止 ----
; 例: [bgm_off]        → 1500msフェードアウト
; 例: [bgm_off t="0"]  → 即停止
[macro name="bgm_off"]
[bgmopt time="%t|1500"]
[stopbgm]
[endmacro]

; ---- SE 再生 ----
; 例: [se_on f="chain_break"]
; 例: [se_on f="slime_move" v="60"]
[macro name="se_on"]
[playse storage="se_%f%.ogg" volume="%v|80"]
[endmacro]

; ---- 動画再生 ----
; 例: [mv f="opening"]
[macro name="mv"]
[movie storage="video/mv_%f%.mp4"]
[endmacro]

[return]
