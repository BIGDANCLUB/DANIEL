"""ショート77：日本vs世界 年越しの過ごし方（world_short.py・段階でくらべる型・11/6 ユーザー指定：候補14番）。59.9秒。

python3 catmeme/short_77_toshikoshi.py → out/short_77_toshikoshi.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg14_home_night"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('22時', 'dance_edm_cat', 'パーティーの\n準備', 'eat_pop_cat', '年越しそば'),
        ('23時', 'dance_trending_cat', '街に\n集まる', 'sleepy_old_memories_cat', 'こたつで\n歌番組'),
        ('23時50分', 'cocky_dj_cat', 'カウントダウンの\n準備', 'stare_tabby_wide_eyes_cat', '除夜の鐘を\n聞く'),
        ('23時59分', 'spin_spinning_cat', '10・9・8…', 'think_chin_paw_orange_cat', 'ジャンプの\n準備'),
        ('0時', 'dance_happy_banana_cat', '花火と\nハグ', 'happy_chipi_chapa_cat', '年越しの瞬間\n地球に\nいなかった'),
        ('0時5分', 'dance_wop_cat', '朝まで\nおどる', 'calm_black_face_sheep', 'あけおめ\nLINE'),
        ('1時', 'dance_maxwell_cat', 'まだ\nパーティー', 'sleep_sleeping_cat', '寝る'),
        ('元日の朝', 'sleepy_sleepy_cat', '二日酔い', 'read_book_orange_kitten', '初日の出'),
        ('元日の昼', 'sad_banana_cat_cry', '1月2日から\n仕事', 'eat_crunchy_cat_luna', 'おせちと\nお年玉'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}年越しの過ごし方", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_77_toshikoshi.mp4"), os.path.join(Wd.HERE, "out", "short_77_toshikoshi_preview"))
