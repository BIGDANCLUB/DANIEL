"""ショート91：日本vs世界 敬語の段階（world_short.py・段階でくらべる型・11/12 ユーザー指定：候補4番）。59.9秒。

python3 catmeme/short_91_keigo.py → out/short_91_keigo.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg25_office_desk"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('友だち', 'wave_waving_cat', 'Hi!', 'happy_hamster_open_arms', 'おつー'),
        ('先輩', 'talk_orange_white_sitting_cat', 'Hi!', 'meow_ragdoll_chubby_cat', 'おつかれさまです'),
        ('上司', 'stare_interviewer_cat', 'Hi!', 'work_typing_cat', 'おつかれさまでございます'),
        ('部長', 'smug_squint_bicolor_cat', 'Hi John!', 'sad_looking_away_tabby', 'お手すきの際に\nご確認いただけますと\n幸いです'),
        ('社長', 'rizz_cat_rizz', 'Hey!', 'surprise_big_pupils_cat', '誠に恐縮ですが\n何卒お願い\n申し上げます'),
        ('取引先', 'cocky_dj_cat', 'Nice to\nmeet you', 'despair_dramatic_kitten', '平素より格別の\nお引き立てを\n賜り'),
        ('お詫び', 'calm_black_face_sheep', 'Sorry', 'scream_phone_orange_cat', '誠に申し訳\nございません\nでした'),
        ('メールの最後', 'stare_aloha_gray_cat', 'Thanks', 'blank_black_cat_zoning_out', '引き続き\nよろしく\nお願いいたします'),
        ('家で', 'dance_cute_dog', 'Hi!', 'sleep_sleeping_cat', 'うん'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}敬語の段階", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_91_keigo.mp4"), os.path.join(Wd.HERE, "out", "short_91_keigo_preview"))
