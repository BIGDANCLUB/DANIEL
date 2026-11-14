# 汎用SEのファイル名を英語にする（濁点の分かれ方・半角カナの違いがあっても見つける）
$dir = "C:\Users\genji\OneDrive\デスクトップ\動画素材\汎用\SE\Github"
$map = @'
FF カーソル音.wav|game_ff_cursor.wav
Switch 指パッチン.wav|game_switch_snap.wav
うぅーわー.mp3|voice_uuwaa.mp3
きらきら輝く1.mp3|sparkle_kirakira_01.mp3
ごまだれ.wav|game_zelda_item_get.wav
ざざざっ　素早い逃走音.wav|run_away_zazaza_fast.wav
ちょこん可愛く座る.mp3|sit_cute_chokon.mp3
てってれー　ドッキリ.mp3|tv_dokkiri_tettere.mp3
ひびが入る.mp3|crack.mp3
ひらめく1 ニュータイプ.mp3|idea_newtype_01.mp3
ぷにょっ.wav|puni.wav
むわぁぁぁ.wav|voice_muwaaa.wav
アンダーテイル　エンカウント.mp3|game_undertale_encounter.mp3
アンダーテイル　魔法のやり　ポワァ.mp3|game_undertale_spear.mp3
インム　台パン.wav|meme_inmu_desk_slam.wav
エアコン　ピッ.wav|aircon_beep.wav
エアライド　クリアチェッカー.mp3|game_airride_checker.mp3
エアーホーン.mp3|air_horn.mp3
オコリザル鳴き声.mp3|game_pokemon_mankey_cry.mp3
オーラ2.mp3|aura_02.mp3
カン　マイクラ金床.wav|game_minecraft_anvil.wav
カンコーン　遊戯王.wav|anime_yugioh_kankon.wav
カーソル移動1.mp3|cursor_move_01.mp3
カーソル移動2.mp3|cursor_move_02.mp3
カードをめくる.mp3|card_flip.mp3
カードを台の上に出す.mp3|card_place.mp3
カーン.mp3|kaan.mp3
カーーッ　ビブラスラップ.mp3|vibraslap.mp3
ガキ使　デデーン.mp3|tv_gakitsuka_dedeen.mp3
ガラスが割れる1.mp3|glass_break_01.mp3
キラッ1.mp3|shine_kira_01.mp3
キラーン　魔王魂 効果音 システム46.mp3|shine_kiraan_maou.mp3
クイズ出題1.mp3|quiz_question_01.mp3
クイズ出題音.mp3|quiz_question_02.mp3
クレシン　げんこつ.wav|anime_shinchan_genkotsu.wav
クレシン　💦たらーん.wav|anime_shinchan_taraan.wav
グギッ.wav|gugi.wav
ゲームボーイスタート音.mp3|game_gameboy_start.mp3
ゲーム起動音風.wav|boot_game_like.wav
コテッ.mp3|kote.mp3
コナン　閃き.wav|anime_conan_idea.wav
コンッ.mp3|kon.mp3
ゴゴゴゴ.mp3|rumble_gogogo.mp3
ゴング　カーン.wav|gong_kaan.wav
サイレン・パトカー.mp3|siren_police.mp3
サイレン・救急車01.mp3|siren_ambulance.mp3
ザザザザッ　逃走音.wav|run_away_zazaza.wav
シャキーン1.mp3|shakiin_01.mp3
シュッ.wav|whoosh_shu.wav
ショック2　ピアノ.mp3|shock_piano.mp3
シンキングタイム.mp3|thinking_time.mp3
シンバル　軽い魔王魂  ドラム1-シンバル.mp3|cymbal_light_maou.mp3
シンバル　魔王魂  ドラム2-シンバル.mp3|cymbal_maou.mp3
ジャンプの着地.mp3|jump_landing.mp3
ジャンプ音　低め.wav|jump_low.wav
ジャン！.mp3|jan.mp3
ジャーン銅鑼.mp3|gong_dora_jaan.mp3
ジングルベル単発魔王魂 効果音 物音15.mp3|jingle_bell_maou.mp3
スイッチを押す.mp3|switch_press.mp3
ステンバーイ.wav|meme_standby.wav
スネア　単発魔王魂  ドラム2-スネア.mp3|snare_maou.mp3
スポッ.mp3|spo.mp3
スマブラX　ジャスガ.wav|game_smash_x_just_guard.wav
スマブラ　GAMESET.wav|game_smash_gameset.wav
スマブラ　Ready Go.wav|game_smash_ready_go.wav
スマブラ　とどめ演出.wav|game_smash_finish.wav
スマブラ　ジャスガ.wav|game_smash_just_guard.wav
スマブラ　参戦.wav|game_smash_challenger.wav
スマブラ　残念だったな.wav|game_smash_zannen.wav
スーポッ.mp3|suupo.mp3
チャン　軽高.mp3|chan_light_high.mp3
チリン.mp3|chirin.mp3
チーン1.mp3|chiin_01.mp3
テーレッテレー.mp3|tereterere.mp3
ディスコード　切断音.wav|app_discord_disconnect.wav
デデドン　インム.mp3|meme_inmu_dededon.mp3
デンッ　クイズ・出題04.mp3|quiz_den.mp3
ドカーン.wav|explosion_dokaan.wav
ドゴッ魔王魂  戦闘12.mp3|hit_dogo_maou.mp3
ドラえもん秘密道具.wav|anime_doraemon_gadget.wav
ドラクエ　レベルアップ.mp3|game_dq_level_up.mp3
ドラクエ　味方攻撃.wav|game_dq_attack_ally.wav
ドラクエ　宿屋.wav|game_dq_inn.wav
ドラクエ　攻撃ミス.wav|game_dq_miss.wav
ドラクエ　敵攻撃.wav|game_dq_attack_enemy.wav
ドラゴンボール 打撃音.wav|anime_dbz_punch.wav
ドラゴンボール　瞬間移動.wav|anime_dbz_teleport.wav
ドラムロール.mp3|drumroll.mp3
ドンっ.mp3|don_hit.mp3
ドーン　銃声.wav|gunshot_doon.wav
ドーン重い演出.mp3|doon_heavy.mp3
ドーン（映画風）.mp3|doon_movie.mp3
ニュータイプ風.mp3|newtype_like.mp3
ハイタム　魔王魂  ドラム2-タム3.mp3|tom_high_maou.mp3
ハテナ？　魔王魂 効果音 ワンポイント26.mp3|question_hatena_maou.mp3
バキューン魔王魂  銃03.mp3|gunshot_bakyuun_maou.mp3
バシッとツッコミ3.mp3|tsukkomi_bashi.mp3
バネ・びょい～ん03.mp3|spring_byoin.mp3
バーン　爆発.mp3|explosion_baan.mp3
パソコン警告音.wav|pc_warning.wav
パッ.mp3|pa.mp3
パッポー　鳩時計.mp3|cuckoo_pappo.mp3
パパッ.mp3|papa.mp3
パフ.mp3|pafu.mp3
パワーアップ・強化・上昇.mp3|power_up.mp3
ヒョロロー脱力.mp3|deflate_hyororo.mp3
ヒーローの決めポーズ.mp3|hero_pose.mp3
ビシッとツッコミ2.mp3|tsukkomi_bishi.mp3
ビヨォン.mp3|boing_01.mp3
ビヨヨヨーン.mp3|boing_02.mp3
ビヨーン　失敗しちゃった.mp3|boing_fail.mp3
ビローン〈ボヨーン〉.wav|boing_03.wav
ピコン　起動音風.wav|pikon_boot.wav
ピコン！.mp3|pikon.mp3
ピコーン　ファミコン風.wav|pikoon_retro.wav
ピッ.wav|pi_beep.wav
ピュピュピュピュピュピューン.wav|run_away_pyupyupyun.wav
ピュピュピュ逃げる音.wav|run_away_pyupyu.wav
ピューンと逃げる.mp3|run_away_pyuun.mp3
ピンポン　注意書き.mp3|pinpon_notice.mp3
ピンポンパンポン.wav|chime_announce.wav
ピンポーン(補足).mp3|pinpoon_note.mp3
ピンポーン.wav|pinpoon_correct.wav
ピー音　短.wav|bleep_short_01.wav
ピー音　短い2.mp3|bleep_short_02.mp3
ピー音・モザイクや放送禁止.mp3|bleep_censor.mp3
ピ！.mp3|pi.mp3
フライパン　カーン.mp3|frying_pan_kaan.mp3
ブッピガン.mp3|meme_buppigan.mp3
ブブー.mp3|buzzer_wrong.mp3
ブラボー拍手付.mp3|bravo_applause.mp3
ブロリー　デデーン.wav|anime_broly_dedeen.wav
プロフェ　ポーン.mp3|tv_professional_poon.mp3
ベベン.mp3|beben.mp3
ペタッ.mp3|peta.mp3
ホームランバット.wav|game_smash_homerun_bat.wav
ボカーン.mp3|explosion_bokaan.mp3
ボーン.mp3|boon.mp3
ボーン　小さめ.mp3|boon_small.mp3
マリオ　1UP.wav|game_mario_1up.wav
マリオ　ジャンプ.mp3|game_mario_jump.mp3
マリオ　ジャンプ　バオ.mp3|game_mario_jump_bao.mp3
メタルギア　アラート.wav|game_mgs_alert.wav
モンハン　クエスト出発.wav|game_monhun_quest_start.wav
凍る・コチーン.mp3|freeze_kochiin.mp3
剣　シャキーン.wav|sword_shakiin.wav
剣で斬る3.mp3|sword_slash.mp3
剣を抜く.mp3|sword_draw.mp3
和太鼓　ドドン.mp3|taiko_dodon_01.mp3
和太鼓　ドン.wav|taiko_don.wav
和太鼓でカカッ.mp3|taiko_kaka.mp3
和太鼓でドドン.mp3|taiko_dodon_02.mp3
岩が真っ二つに割れる.mp3|rock_split.mp3
幻想殺し.mp3|anime_imagine_breaker.mp3
拍子木1.mp3|hyoshigi_01.mp3
拍子木2.mp3|hyoshigi_02.mp3
拳銃 ばきゅん.mp3|gunshot_bakyun.mp3
木琴シーン切り替え1.mp3|xylophone_transition.mp3
木魚ポク・ポク・ポク.mp3|mokugyo_pokupoku.mp3
本をめくる音.mp3|page_turn_01.mp3
本をめくる音.wav|page_turn_02.wav
歓声と拍手.mp3|cheer_applause.mp3
殴り音.wav|punch.wav
決定、ボタン押下13.mp3|button_13.mp3
決定、ボタン押下17.mp3|button_17.mp3
決定、ボタン押下22.mp3|button_22.mp3
決定、ボタン押下26.mp3|button_26.mp3
決定、ボタン押下3.mp3|button_03.mp3
決定、ボタン押下39.mp3|button_39.mp3
決定、ボタン押下42.mp3|button_42.mp3
決定、ボタン押下9.mp3|button_09.mp3
涙のしずく.mp3|tear_drop.mp3
熱盛.wav|tv_atsumori.wav
爆発2.mp3|explosion_02.mp3
男衆「オウ！」.mp3|voice_men_ou.mp3
盾で防御.mp3|shield_block.mp3
落ちる音　ひゅー.mp3|fall_hyuu.mp3
試合終了のゴング.mp3|gong_match_end.mp3
試合開始のゴング.mp3|gong_match_start.mp3
豊田　このハゲー.wav|news_toyota_konohage.wav
豊田　ちがうだろ.wav|news_toyota_chigaudaro.wav
超高速ダッシュ.mp3|dash_super_fast.mp3
車・急ブレーキ01.mp3|car_brake.mp3
逆転裁判　ピーン.wav|game_aceattorney_ping.wav
逆転裁判　机をたたく音.wav|game_aceattorney_desk_slam.wav
金額表示.mp3|price_display.mp3
鈴を鳴らす.mp3|bell_ring.mp3
銅鑼の音.wav|gong_dora.wav
間抜け3.mp3|silly.mp3
食べ物をパクッ.mp3|eat_paku.mp3
魔の時計塔の鐘　ゴーン.mp3|bell_tower_goon.mp3
鳩時計1.mp3|cuckoo_clock.mp3
ﾁｭﾄﾞｰﾝ　爆発1.mp3|explosion_chudoon.mp3
ﾄﾞｰﾝ　爆発2.mp3|explosion_doon.mp3
ﾊﾟﾗﾗﾗｯﾊﾟﾗｰ.mp3|fanfare_pararappara.mp3
'@
$files = Get-ChildItem -LiteralPath $dir -File
$log = @()
$miss = 0
foreach ($line in $map -split "`r?`n") {
  if (-not $line.Trim()) { continue }
  $old, $new = $line -split '\|', 2
  $want = $old.Normalize([Text.NormalizationForm]::FormKC)
  $file = $files | Where-Object { $_.Name.Normalize([Text.NormalizationForm]::FormKC) -eq $want } | Select-Object -First 1
  if ($file) {
    Rename-Item -LiteralPath $file.FullName -NewName $new
    $log += [pscustomobject]@{old = $old; new = $new}
  } else {
    Write-Host "見つからない: $old" -ForegroundColor Yellow
    $miss++
  }
}
$log | Export-Csv (Join-Path $dir "rename_log.csv") -NoTypeInformation -Encoding UTF8
Write-Host "$($log.Count) 件の名前を変えました（見つからない: $miss 件）" -ForegroundColor Green
