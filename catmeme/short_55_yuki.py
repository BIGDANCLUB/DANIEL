"""ショート55：日本vs世界 雪が降ったときの反応の差（world_short.py・地震の反応と同じ作り・10/31 ユーザー指定）。59.9秒。

python3 catmeme/short_55_yuki.py → out/short_55_yuki.mp4
- 積雪ごとに「だれもいない → 世界の猫 → 日本（東京）の猫」の3段。雪国の国は平然、東京は数センチで大さわぎ、のずれで笑わせる
- けがや事故のことは書かない。最後は「みんなも雪の日は気をつけよう」。BGM なし
"""
import os

import world_short as Wd

ST = "bg61_snow_onsen"
K = 59.9 / 58.5


def cuts():
    out = []
    rows = [
        ("積雪1cm", "slack_nail_filing_cat", "気づかない", "stare_big_eyes_tabby_kitten", "SNSに\n雪の写真があふれる"),
        ("積雪3cm", "eat_chips_cat", "ふつうに\n出勤", "scream_phone_orange_cat", "ニュースが\n雪一色に"),
        ("積雪5cm", "walk_white_duck", "雪の上を\nお散歩", "despair_dramatic_kitten", "電車が\n止まる"),
        ("積雪10cm", "calm_black_face_sheep", "まだ\n冬のはじめ", "sad_looking_away_tabby", "駅に\n大行列"),
        ("積雪20cm", "ride_kitten_bike", "タイヤを\nかえるだけ", "stare_tabby_wide_eyes_cat", "スーパーから\nパンが消える"),
        ("積雪30cm", "cocky_dj_cat", "学校も\nふつうにある", "confused_i_dont_know_cat", "長ぐつが\n売り切れ"),
        ("積雪50cm", "happy_chipi_chapa_cat", "雪かきは\nいい運動", "sulk_hungry_cat", "家から\n出られない"),
        ("積雪1m", "dance_three_kittens", "スキーで\n出勤", "blank_black_cat_zoning_out", "東京では\n見たことがない"),
        ("積雪2m", "happy_hamster_open_arms", "冬が\n来たね", "realize_wet_cat_stare", "みんなも\n雪の日は\n気をつけよう"),
    ]
    for lv, wcat, wcap, jcat, jcap in rows:
        big = lv in ("積雪20cm", "積雪30cm", "積雪50cm", "積雪1m", "積雪2m")
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}雪が降ったときの反応", 96, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_55_yuki.mp4"), os.path.join(Wd.HERE, "out", "short_55_yuki_preview"))
