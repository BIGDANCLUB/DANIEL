"""ショート87：日本vs世界 電車の混み具合（world_short.py・段階でくらべる型・11/9 ユーザー指定：候補5番）。59.9秒。

python3 catmeme/short_87_manin.py → out/short_87_manin.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg53_shinkansen"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('50%', 'happy_chipi_chapa_cat', '座れる', 'read_book_orange_kitten', '座って\n読書'),
        ('80%', 'stare_interviewer_cat', 'ふつう', 'work_typing_cat', '立って\nスマホ'),
        ('100%', 'glare_disgusted_cat', '混んでる', 'calm_black_face_sheep', 'ふつう'),
        ('120%', 'leave_cat_leaves_home', '次の電車に\nする', 'think_chin_paw_orange_cat', 'ドアの前で\n深呼吸'),
        ('150%', 'fight_cat_fight', '大さわぎ', 'stare_lying_tabby_cat', 'カバンを\n前に抱える'),
        ('180%', 'scream_standing_marmot', '乗れない', 'sleepy_old_memories_cat', '押されながら\nスマホ'),
        ('200%', 'call_customer_service_cat', 'タクシーで\n行く', 'despair_dramatic_kitten', '駅員さんに\n押してもらう'),
        ('雨の日', 'surprise_big_pupils_cat', '会社を\n休む', 'sad_looking_away_tabby', '傘がぬれて\nさらに地獄'),
        ('降りる駅', 'dance_happy_banana_cat', 'ゆっくり\n降りる', 'dance_filmed_by_gray_cat', 'すみません\n降ります\n(戦い)'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}電車の混み具合", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_87_manin.mp4"), os.path.join(Wd.HERE, "out", "short_87_manin_preview"))
