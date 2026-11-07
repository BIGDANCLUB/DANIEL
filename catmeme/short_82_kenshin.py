"""ショート82：日本vs世界 健康診断の結果（world_short.py・段階でくらべる型・11/7 ユーザー指定：候補14番）。59.9秒。

python3 catmeme/short_82_kenshin.py → out/short_82_kenshin.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg28_jp_clinic"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('A判定', 'happy_chipi_chapa_cat', 'ふつう', 'showoff_gojo_cosplay_cat', '職場で\n自慢する'),
        ('B判定', 'stare_interviewer_cat', '問題なし', 'think_chin_paw_orange_cat', 'ちょっと\n気にする'),
        ('C判定', 'calm_black_face_sheep', '少し\n気をつける', 'eat_chips_cat', 'とりあえず\nポテチ'),
        ('D判定', 'call_customer_service_cat', 'すぐ病院へ', 'sleepy_old_memories_cat', '忙しいから\nまた今度'),
        ('E判定', 'surprise_big_pupils_cat', '仕事を\n休む', 'dance_filmed_by_gray_cat', 'その日も\n飲み会'),
        ('再検査', 'glare_disgusted_cat', 'すぐ予約', 'sad_looking_away_tabby', '封筒を\nあけない'),
        ('腹囲', 'read_book_orange_kitten', '気にしない', 'despair_dramatic_kitten', '前日だけ\nお腹をへこませる'),
        ('前日の夜', 'sleep_sleeping_cat', 'いつも通り', 'stare_lying_tabby_cat', '急に\nサラダだけ'),
        ('1年後', 'dance_happy_banana_cat', '健康', 'blank_black_cat_zoning_out', '去年と\n同じ結果'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}健康診断の結果", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_82_kenshin.mp4"), os.path.join(Wd.HERE, "out", "short_82_kenshin_preview"))
