"""ショート133：日本vs世界　スマホの電池残量への反応（world_short.py・段階でくらべる型・11/22 ユーザー指定：候補12番）。59.9秒。

python3 catmeme/short_133_denchi.py → out/short_133_denchi.mp4
- 段階ごとに「札だけ → 右の猫（世界）→ 左の猫（日本）」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルの全タイトル（ほのぼの248・40代独身229・おひとりさま7）と被らないことを確認ずみ（11/22）
- 概要欄の注意：※よくあるイメージです（国や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg51_night_street'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('100%', 'calm_black_face_sheep', '気にしない', 'happy_hamster_open_arms', '安心'),
        ('80%', 'cocky_dj_cat', '充電？\nしない', 'smug_squint_bicolor_cat', 'モバイル\nバッテリーも\n持ってる'),
        ('50%', 'dance_cute_dog', 'まだ半分', 'stare_tabby_wide_eyes_cat', 'もう半分'),
        ('30%', 'listen_dancing_dog', '余裕', 'think_chin_paw_orange_cat', '低電力モード'),
        ('20%', 'rizz_cat_rizz', '動画を見る', 'work_typing_cat', '画面を\n暗くする'),
        ('10%', 'dance_edm_cat', '音楽を流す', 'scream_phone_orange_cat', 'コンビニで\n充電器を買う'),
        ('5%', 'happy_girlfriend_dance_cat', '誰かに\n借りる', 'sad_looking_away_tabby', 'カフェで\nコンセント探し'),
        ('1%', 'showoff_gojo_cosplay_cat', '自撮りする', 'sad_banana_cat_cry', '家族に\n最後のLINE'),
        ('0%', 'dance_filmed_by_gray_cat', '自由だ', 'blank_black_cat_zoning_out', '絶望'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}スマホの電池残量への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_133_denchi.mp4"), os.path.join(Wd.HERE, "out", "short_133_denchi_preview"))
