"""ショート110：日本vs世界　結婚式に呼ばれたときの出費（world_short.py・段階でくらべる型・11/16 ユーザー指定：お金の候補）。59.9秒。

python3 catmeme/short_110_goshugi.py → out/short_110_goshugi.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・地域・人もけなさない
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/16 一覧で確認）
- 概要欄の注意：※目安です（よくあるイメージで、実際の統計ではありません）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg71_wedding_chapel'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('招待状', 'dance_cute_dog', 'おめでとう！', 'think_chin_paw_orange_cat', 'まず\n口座残高を\n見る'),
        ('服', 'cocky_dj_cat', '手持ちの服', 'money_counting_orange_cat', 'スーツと\nネクタイ\n新調'),
        ('友だち', 'happy_hamster_open_arms', 'プレゼント\n1つ', 'work_typing_cat', 'ご祝儀\n3万円'),
        ('同僚', 'listen_dancing_dog', 'カードで\nお祝い', 'stare_lying_tabby_cat', 'ご祝儀\n3万円'),
        ('上司', 'rizz_cat_rizz', 'ハグ', 'sad_looking_away_tabby', 'ご祝儀\n3万円と\n気づかい'),
        ('2次会', 'smug_squint_bicolor_cat', 'そのまま\n踊る', 'stare_tabby_wide_eyes_cat', '会費\n7000円'),
        ('交通費', 'stare_aloha_gray_cat', '近所', 'scream_phone_orange_cat', '新幹線で\n往復2万円'),
        ('3人目', 'happy_chipi_chapa_cat', 'パーティー\n最高', 'despair_dramatic_kitten', 'Nine\n渋沢’s'),
        ('本番', 'dance_filmed_by_gray_cat', '{fancy}Congratulations', 'dance_filmed_by_gray_cat', 'ウェーイｗ'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}結婚式に呼ばれたら", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_110_goshugi.mp4"), os.path.join(Wd.HERE, "out", "short_110_goshugi_preview"))
