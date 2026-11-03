"""ショート68：日本vs世界 誕生日の祝い方（world_short.py・段階でくらべる型・11/3 ユーザー指定：候補17番）。59.9秒。

python3 catmeme/short_68_tanjoubi.py → out/short_68_tanjoubi.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- 「ほのぼの猫ミーム」と強く被るテーマは使わない（research/honobono_overlap_20261103.md）
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
        ('1歳', 'dance_happy_banana_cat', '盛大な\nパーティー', 'happy_hamster_open_arms', '一升餅を\nせおう'),
        ('10歳', 'dance_three_kittens', '友だちを\n30人呼ぶ', 'eat_pop_cat', '家族で\nケーキ'),
        ('18歳', 'cocky_dj_cat', '大人の\n仲間入り', 'read_book_orange_kitten', '受験勉強'),
        ('20歳', 'dance_edm_cat', '朝まで\nパーティー', 'dance_filmed_by_gray_cat', '朝まで\n飲み明かす'),
        ('30歳', 'happy_chipi_chapa_cat', 'サプライズ\nパーティー', 'sad_looking_away_tabby', 'ひとりで\nコンビニケーキ'),
        ('40歳', 'calm_black_face_sheep', '盛大に\n祝う', 'blank_black_cat_zoning_out', '気づいたら\n過ぎていた'),
        ('50歳', 'showoff_gojo_cosplay_cat', '大きな\nパーティー', 'work_typing_cat', 'ふつうに\n仕事'),
        ('60歳', 'money_counting_orange_cat', 'まだまだ\n若い', 'happy_girlfriend_dance_cat', '赤い\nちゃんちゃんこ'),
        ('100歳', 'surprise_big_pupils_cat', 'ニュースに\nなる', 'scream_phone_orange_cat', '国から\nお祝いが届く'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('日本', '世界'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}誕生日の祝い方", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_68_tanjoubi.mp4"), os.path.join(Wd.HERE, "out", "short_68_tanjoubi_preview"))
