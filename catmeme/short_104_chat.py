"""ショート104：日本vs世界　社内チャットの返信（world_short.py・段階でくらべる型・11/15 ユーザー指定：候補7番）。59.9秒。

python3 catmeme/short_104_chat.py → out/short_104_chat.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/15 一覧で確認）
- 概要欄の注意：※目安です（よくあるイメージで、実際の統計ではありません）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg25_office_desk'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1分', 'dance_cute_dog', '👍', 'work_typing_cat', '承知いたしました'),
        ('5分', 'cocky_dj_cat', 'OK', 'think_chin_paw_orange_cat', '文面を\n3回書き直す'),
        ('10分', 'happy_hamster_open_arms', 'ランチ中', 'stare_lying_tabby_cat', '既読だけ\nつける'),
        ('30分', 'listen_dancing_dog', '気にしない', 'sad_looking_away_tabby', '返信が遅れ\n申し訳ございません'),
        ('1時間', 'rizz_cat_rizz', '会議中', 'scream_phone_orange_cat', '上司に\nCCされる'),
        ('夜', 'smug_squint_bicolor_cat', '通知オフ', 'stare_tabby_wide_eyes_cat', '寝る前に\n確認'),
        ('休日', 'stare_aloha_gray_cat', '見ない', 'despair_dramatic_kitten', '休日なのに\n未読0を守る'),
        ('翌日', 'happy_chipi_chapa_cat', 'Hi!', 'calm_black_face_sheep', 'お疲れさまです\n昨日の件ですが'),
        ('1週間', 'dance_filmed_by_gray_cat', '忘れた', 'blank_black_cat_zoning_out', 'まだ\n既読スルーが\n気になる'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}社内チャットの返信", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_104_chat.mp4"), os.path.join(Wd.HERE, "out", "short_104_chat_preview"))
