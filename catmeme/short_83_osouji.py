"""ショート83：大掃除の理想と現実（world_short.py・段階でくらべる型・11/7 ユーザー指定：候補16番）。59.9秒。

python3 catmeme/short_83_osouji.py → out/short_83_osouji.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
- 11/8 ユーザー指定：14時の理想は別の素材・16時「何も終わっていない」・18時「何もしてないけど疲れた」・夜の理想「綺麗な部屋で心機一転」・翌日は理想の素材を変えて現実「年末の自分に託す」（踊る猫をスマホで撮る猫）
"""
import os

import world_short as Wd

ST = "bg02_room"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('朝9時', 'showoff_gojo_cosplay_cat', '窓から\nピカピカに', 'sleep_sleeping_cat', 'まだ寝ている'),
        ('10時', 'work_typing_cat', 'いらない物を\n捨てる', 'scream_phone_orange_cat', '掃除のやり方を\n動画で見る'),
        ('11時', 'cocky_dj_cat', '台所の\n油よごれ', 'sleepy_old_memories_cat', '昔のアルバムを\n見つける'),
        ('12時', 'happy_hamster_open_arms', 'お昼も\nさっと', 'eat_pop_cat', 'アルバムを\n見ながら\nお昼'),
        ('14時', 'calmdown_dancing_cat', '押し入れを\n整理', 'read_book_orange_kitten', '昔のマンガを\n読みはじめる'),
        ('16時', 'joy_happy_happy_happy_cat', 'ほぼ終わり', 'despair_dramatic_kitten', '何も\n終わっていない'),
        ('18時', 'dance_three_kittens', 'ピカピカの部屋で\nごほうび', 'sulk_hungry_cat', '何もしてないけど\n疲れた'),
        ('夜', 'happy_girlfriend_dance_cat', '綺麗な\n部屋で\n心機一転', 'calm_black_face_sheep', '窓だけ\n1枚ふいた'),
        ('翌日', 'happy_hamster_open_arms', 'きれいを\nキープ', 'dance_filmed_by_gray_cat', '年末の\n自分に\n託す'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('現実', '理想'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}大掃除の", 96, Wd.BLACK, 95), ("{y}理想と現実", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_83_osouji.mp4"), os.path.join(Wd.HERE, "out", "short_83_osouji_preview"))
