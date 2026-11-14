"""ショート95：年代別 自販機で買うもの（平日と休日）（world_short.py・段階でくらべる型・11/12 ユーザー指定：候補26番）。59.9秒。

python3 catmeme/short_95_jihanki.py → out/short_95_jihanki.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg64_vending_machines"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('10代', 'dance_cute_dog', '炭酸', 'happy_hamster_open_arms', '当たりが\n出るまで\n買う'),
        ('20代', 'cocky_dj_cat', 'エナジー\nドリンク', 'dance_white_dog', '炭酸'),
        ('30代', 'work_typing_cat', '缶コーヒー', 'eat_chips_cat', 'ジュースで\n若返り'),
        ('40代', 'stare_lying_tabby_cat', 'ブラック\nコーヒー', 'sleepy_old_memories_cat', 'お茶'),
        ('50代', 'calm_black_face_sheep', 'トクホの\nお茶', 'sad_looking_away_tabby', 'あったか〜い\nおしるこ'),
        ('60代', 'stare_aloha_gray_cat', '健康飲料', 'blank_black_cat_zoning_out', '水'),
        ('70代', 'sleep_sleeping_cat', '水', 'huh_huh_cat', 'スマホで\n払えない'),
        ('80代', 'talk_orange_white_sitting_cat', '家から\n水筒を持参', 'happy_chipi_chapa_cat', '家から\n水筒を持参'),
        ('100歳', 'showoff_gojo_cosplay_cat', 'いちごミルク', 'dance_filmed_by_gray_cat', 'コーラ'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('休日', '平日'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}年代別", 96, Wd.BLACK, 95), ("{y}自販機で買うもの", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_95_jihanki.mp4"), os.path.join(Wd.HERE, "out", "short_95_jihanki_preview"))
