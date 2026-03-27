;==========================================================
; ending_good.ks - グッドエンディング群
;==========================================================

;==========================================================
; エンド A: 平和の誓い（通常ルート）
;==========================================================
*ending_peace

[set f.chapter=99]

; [bg storage="bg_throne_room_dawn.jpg" time="2000"]
; [bgm storage="bgm_ending_peaceful.ogg" loop=true]

[fadein time="1500"]

[nm t="ナレーション"]
魔王と勇者は、長い夜をかけて話し合った。[l]

[nm t="ナレーション"]
魔物たちの居住区域。人間との交易路。争いのない世界への道筋。[p]

[nm t="魔王" color="#ff4444"]
「……あなた、名前は？」[l]

[nm t="勇者" color="#aaddff"]
「……レン。勇者レン」[l]

[nm t="魔王" color="#ff4444"]
「私はリリス。……よろしく、レン」[p]

[nm t="ナレーション"]
窓の外が白み始めた。夜明けだ。[p]

[nm t="女神" color="#ffffaa"]
「……これが、私が願っていた結末よ。よくやったわ、レン」[p]

[nm t="ナレーション"]
淫紋が——静かに消えていった。[l]

[nm t="ナレーション"]
それはまるで、この出来事全てを承認するかのように。[p]

[nm t="ナレーション"]
勇者レンとリリスは、新たな冒険へ踏み出した。[l]

[nm t="ナレーション"]
今度は、剣ではなく言葉を武器に。[p]

; エンドテキスト表示
; [showmessage storage="ui/ending_title.png" text="END A: 平和の誓い"]

[jump target="*ending_credits"]

;==========================================================
; エンド B: 絆ルート（魔物たちと心通わせた場合）
;==========================================================
*ending_friendship

[set f.chapter=99]

; [bg storage="bg_castle_garden.jpg" time="2000"]
; [bgm storage="bgm_ending_warm.ogg" loop=true]

[fadein time="1500"]

[nm t="ナレーション"]
魔王城の庭に、不思議な光景が広がっていた。[p]

[nm t="ナレーション"]
スライムが嬉しそうに弾んでいる。サキュバスが笑っている。魔女が照れくさそうに目を逸らしている。[p]

[nm t="サキュバス" color="#ff88cc"]
「勇者くん……また来てくれたのね」[l]

[nm t="勇者" color="#aaddff"]
「……約束したからな」[p]

[nm t="魔女" color="#cc88ff"]
「……共存魔法薬、完成したわよ。あなたのサンプルのおかげ」[l]

[nm t="魔女" color="#cc88ff"]
「……感謝するわ（小声）」[p]

[nm t="スライム"]
「ぷるぷる……また来た！ うれしい！」[p]

[nm t="魔王" color="#ff4444"]
「……あなたはおかしな勇者ね。敵を仲間にして」[l]

[nm t="勇者" color="#aaddff"]
「仲間じゃなくて、友達だ」[p]

[nm t="魔王" color="#ff4444"]
「……友達」[l]

[nm t="ナレーション"]
魔王リリスが——珍しく、柔らかく笑った。[p]

[nm t="女神" color="#ffffaa"]
「……これが真の勇気ね。戦うだけじゃない、繋がる勇気」[p]

[nm t="ナレーション"]
淫紋は消えた。しかし勇者の身体に残る記憶は——消えなかった。[p]

[nm t="ナレーション"]
それもまた、かけがえのない旅の証だった。[p]

; [showmessage storage="ui/ending_title.png" text="END B: 絆の冒険"]

[jump target="*ending_credits"]

;==========================================================
; エンドロール（共通）
;==========================================================
*ending_credits

[fadeout time="3000" color="0x000000"]
[wait time=1000]

; [bg storage="bg_black.jpg"]
; [bgm storage="bgm_credits.ogg" loop=false]

[fadein time="2000"]

; クレジット表示
; [credit ...]

[nm t="ナレーション"]
——END——[p]

[wait time=2000]

[fadeout time="2000" color="0x000000"]
[wait time=1000]

; タイトルへ戻る
[jump storage="first.ks" target="*start"]
