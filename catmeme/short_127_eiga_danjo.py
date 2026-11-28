"""ショート127：彼氏vs彼女　映画を選ぶ時（world_short.py・段階でくらべる型・11/21 ユーザー指定：男女型候補10番）。59.9秒。

python3 catmeme/short_127_eiga_danjo.py → out/short_127_eiga_danjo.mp4
- ベンチマークで伸びている「男女の比べっこ」型（11/20 調査）。ほのぼのにある題材とは被らないものを選んだ
- 11/21 修正：札は「選び始め」「○分後」・再生の段は彼女スマホでショート／彼氏 開始5分で爆睡
- 札は選び始めてからの時間。右＝彼女、左＝彼氏
- 段階ごとに「札だけ → 右の猫（彼女）→ 左の猫（彼氏）」の3段。どちらもけなさない、よくあるイメージ。BGM なし
"""
import os

import world_short as Wd

ST = 'bg14_home_night'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫＝彼女, 右の説明, 左の猫＝彼氏, 左の説明)
    rows = [
        ('選び始め', 'dance_cute_dog', '何見る？', 'calm_black_face_sheep', 'なんでも\nいい'),
        ('5分後', 'happy_hamster_open_arms', 'これ\n面白そう', 'work_typing_cat', '予告編を\n全部見る'),
        ('10分後', 'think_chin_paw_orange_cat', 'やっぱり\nこっち', 'stare_tabby_wide_eyes_cat', 'レビューを\n読み込む'),
        ('20分後', 'listen_dancing_dog', 'あらすじ\n読む', 'smug_squint_bicolor_cat', '星3.8は\n微妙'),
        ('30分後', 'stare_interviewer_cat', 'おすすめ\n教えて', 'confused_i_dont_know_cat', '結局\n昔の名作？'),
        ('45分後', 'cocky_dj_cat', 'お菓子\n準備完了', 'blank_black_cat_zoning_out', 'まだ\n決まらない'),
        ('1時間後', 'glare_disgusted_cat', 'もう\n何でもいい', 'sad_looking_away_tabby', 'スクロール\nし続ける'),
        ('1時間半後', 'stare_lying_tabby_cat', '眠く\nなってきた', 'rizz_cat_rizz', 'これに\n決めた！'),
        ('再生', 'calm_black_face_sheep', 'スマホで\nショート\n見てる', 'sleep_sleeping_cat', '開始5分で\n爆睡'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('彼氏', '彼女'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}彼氏vs彼女", 96, Wd.BLACK, 95), ("{y}映画を選ぶ時", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_127_eiga_danjo.mp4"), os.path.join(Wd.HERE, "out", "short_127_eiga_danjo_preview"))
