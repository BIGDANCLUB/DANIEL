"""長尺（ナレーションと登場する猫だけの形）に、まわりで反応する猫をふやす（10/30 ユーザー指定「素材もっと使って」）。

- ナレーションの場面：まん中の猫に加えて、左右に反応する猫を1匹ずつ（字幕の上・声なし）
- 1匹がしゃべる場面：左右どちらかの下に、反応する猫を1匹（声なし）
- 注意書き・タイトル・章・解説画面・グラフ・画面分割の場面にはつけない
素材は場面ごとに順番に変えて、となりの場面と同じにならないようにする。
"""

POOL = ["stare_big_eyes_tabby_kitten", "surprise_big_pupils_cat", "huh_huh_cat", "glare_disgusted_cat", "stare_tabby_wide_eyes_cat",
        "peek_what_happen_cat", "realize_wet_cat_stare", "think_bike_front_seat_cat", "meow_gray_white_kitten", "eat_chips_cat",
        "happy_hamster_open_arms", "sulk_hungry_cat", "blank_black_cat_zoning_out", "spit_not_my_taste_cat", "yell_orange_fat_cat",
        "excited_hodomoe_city_cat", "confused_i_dont_know_cat", "sleepy_old_memories_cat", "calm_black_face_sheep",
        "happy_chipi_chapa_cat", "dance_happy_banana_cat", "meow_ragdoll_chubby_cat", "stand_real_sheep", "walk_white_duck"]


def add(cs, nar_box, skip=()):
    k, prev = 0, set()
    for c in cs:
        if (len(c.get("cats", [])) != 1 or c.get("notice") or c.get("card") or c.get("chapter") or c.get("inset") or c.get("chart") or c.get("split")
                or c.get("qmarks") or not c.get("cats")):
            prev = set()
            continue
        here = {q["a"] for q in c["cats"]}
        pick = []
        while len(pick) < (2 if c.get("sub_box") == nar_box else 1):
            a = POOL[k % len(POOL)]
            k += 1
            if a not in here and a not in prev and a not in skip and a not in pick:
                pick.append(a)
        if c.get("sub_box") == nar_box:   # ナレーション：左右に1匹ずつ
            extra = [dict(a=pick[0], x=230, h=430, bottom=820, mute=True, float=True, full=False),
                     dict(a=pick[1], x=1690, h=430, bottom=820, mute=True, float=True, full=False, flip=True)]
        else:   # しゃべる場面：下の左右どちらかに1匹
            right = k % 2 == 0
            extra = [dict(a=pick[0], x=1700 if right else 220, h=420, bottom=1075, mute=True, float=True, full=False, flip=right)]
        c["cats"] = list(c["cats"]) + extra
        prev = {q["a"] for q in c["cats"]}
    return cs
