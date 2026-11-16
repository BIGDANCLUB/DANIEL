"""ショート111：東京vs地方　飲み会1回の金額（world_short.py・段階でくらべる型・11/16 ユーザー指定：お金の候補）。59.9秒。

python3 catmeme/short_111_nomikai_chiho.py → out/short_111_nomikai_chiho.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・地域・人もけなさない
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/16 一覧で確認）
- 概要欄の注意：※目安です（よくあるイメージで、実際の金額は店や地域で変わります）※お酒は20歳になってから・飲んだら運転しない。BGM なし
"""
import os

import world_short as Wd

ST = 'bg13_izakaya'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1次会', 'happy_hamster_open_arms', '飲み放題\n3000円', 'eat_crunchy_cat_luna', '飲み放題\n5000円'),
        ('2次会', 'cocky_dj_cat', 'スナック\n2000円', 'work_typing_cat', 'バー\n4000円'),
        ('カラオケ', 'dance_cute_dog', '1人\n500円', 'listen_dancing_dog', '1人\n2000円'),
        ('ラーメン', 'rizz_cat_rizz', 'ラーメン\n700円', 'think_chin_paw_orange_cat', 'ラーメン\n1200円'),
        ('終電', 'stare_aloha_gray_cat', '電車が\nない', 'stare_tabby_wide_eyes_cat', '終電\nダッシュ'),
        ('帰り', 'smug_squint_bicolor_cat', '運転代行\n4000円', 'scream_phone_orange_cat', 'タクシー\n6000円'),
        ('翌朝', 'calm_black_face_sheep', '車を\n取りに行く', 'sleepy_sleepy_cat', '二日酔いで\n出社'),
        ('合計', 'money_counting_orange_cat', '1万円\nちょっと', 'despair_dramatic_kitten', '2万円\nこえ'),
        ('結局', 'happy_chipi_chapa_cat', '家飲みが\nいちばん', 'dance_filmed_by_gray_cat', '家飲みが\nいちばん'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('東京', '地方'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}東京vs地方", 96, Wd.BLACK, 95), ("{y}飲み会1回の金額", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_111_nomikai_chiho.mp4"), os.path.join(Wd.HERE, "out", "short_111_nomikai_chiho_preview"))
