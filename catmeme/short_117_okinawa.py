"""ショート117：首都圏vs沖縄　寒さへの反応（world_short.py・段階でくらべる型・11/16 ユーザー指定：候補29番）。59.9秒。

python3 catmeme/short_117_okinawa.py → out/short_117_okinawa.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・地域・人もけなさない
- 自分のチャンネルで伸びた「日本vs世界・地域どうしの比べ合い」の傾向に合わせた（11/16）
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/16 一覧で確認）
- 概要欄の注意：※目安です（よくあるイメージで、地域や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg62_okinawa_beach'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('25℃', 'work_typing_cat', 'ちょっと\n涼しい', 'dance_cute_dog', 'ちょうどいい'),
        ('22℃', 'think_chin_paw_orange_cat', '長そでを\n出す', 'happy_hamster_open_arms', '半そで'),
        ('20℃', 'stare_tabby_wide_eyes_cat', '上着を\n着る', 'cocky_dj_cat', '快適'),
        ('18℃', 'sad_looking_away_tabby', 'ダウンを\n着る', 'listen_dancing_dog', '気持ちいい'),
        ('16℃', 'scream_phone_orange_cat', '暖房を\nつける', 'rizz_cat_rizz', '秋だな'),
        ('15℃', 'despair_dramatic_kitten', '外に出ない', 'smug_squint_bicolor_cat', 'まだ半そで'),
        ('13℃', 'sleep_sleeping_cat', 'こたつから\n出られない', 'stare_aloha_gray_cat', 'ちょっと寒い'),
        ('10℃', 'blank_black_cat_zoning_out', 'ニュースで\n大寒波', 'happy_chipi_chapa_cat', 'まだまだ'),
        ('5℃', 'sad_banana_cat_cry', '沖縄では\n伝説の寒さ', 'dance_filmed_by_gray_cat', 'ふつうの冬'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('首都圏', '沖縄'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}首都圏vs沖縄", 96, Wd.BLACK, 95), ("{y}寒さへの反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_117_okinawa.mp4"), os.path.join(Wd.HERE, "out", "short_117_okinawa_preview"))
