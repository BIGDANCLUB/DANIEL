"""13本目（盗難ハイエース300台・ヤード）のショート1本目「300台なのに容疑は1台」。作りは short_12_akaihane.py と同じ。

python3 catmeme/short_13_yard.py → out/short_13_yard.mp4

本編（cuts_13_yard.py・原稿 scripts/13_yard.md）のルールをそのまま守る
- 逮捕された4人は容疑の段階。名前・顔は出さない・猫で演じない
- 国籍でひとくくりにしない。「ヤード＝悪」と言わない。手口のやり方は説明しない
- 主語になる団体（県警など）は団体名の札つきの猫で出す。過去の動画にはふれない
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M

HERE = M.HERE
NAME = "short_13_yard"
TITLE = ("盗難ハイエース300台", "容疑はたった1台!?", M.RED, M.YELLOW, M.WHITE)
C = M.C
LIME = M.LIME
PURPLE = os.path.join(S.BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")
M.BGS[:0] = [os.path.join(HERE, "backgrounds", "13_yard")]
# 背景：ユーザー提供の写真（ハイエース・ヤード）と縦の動く背景
SCRAP, RAID, GARAGE, RUN, CITY = ("bg41_yard_scrap", "bg42_yard_raid_ai", "bg39_hiace_black_garage", "bg38_hiace_white_run",
                                  "bg40_hiace_white_city")
POLICE_CAR, POLICE = "t04_police_car_night", "t05_police_officer_night"
VIC = "車を盗まれた人"


def one(bg, say, a, dur, h=1100, **kw):
    return M.cut(bg, say, [(a, C, h, kw.pop("flip", False))], dur, **kw)


def vic(bg, say, a, dur, **kw):
    return M.cut(bg, say, [(a, C, 1100, False)], dur, label=VIC, label_x=540, col=LIME, **kw)


def org(bg, who, say, a, dur, **kw):
    """主語になる団体を猫で出す（10/14 ユーザー指定）。"""
    return M.cut(bg, say, [(a, C, 1100, False)], dur, label=who, label_x=540, **kw)


def cuts():
    return [
        one(GARAGE, "朝起きたら\n*ハイエースがない*", "surprise_big_pupils_cat", 2.6, shake=True,
            se=["jan", "explosion_chudoon"], bgm={"file": PURPLE, "gain": -6}),
        vic(GARAGE, "工具も全部\n積んだままだったのに……", "sad_banana_cat_cry", 2.8, se="tear_drop"),
        org(POLICE_CAR, "4県警", "2026年6月\n*4人を逮捕*", "stare_standing_marmot", 2.4, se="siren_police"),
        one(SCRAP, "このヤードだけで\n盗難車*300台以上*を\n受け取ったとみられる", "realize_wet_cat_stare", 3.2, size=86,
            se="doon_movie"),
        one(RAID, "塀の中で解体して\n*海外へ*", "glare_disgusted_cat", 2.4, se="pc_warning"),
        one(POLICE, "でも逮捕の容疑は\n*ハイエース1台*", "surprise_big_pupils_cat", 2.6, shake=True,
            se="game_pokemon_super_effective_hit_big_damage"),
        one(POLICE, "300台なのに\n*1台*！？", "rage_talking_cat", 2.2, size=130, se="game_aceattorney_desk_slam"),
        one(RAID, "“盗難車だと*知らなかった*”\nと言われると\n罪に問うのが難しい", "think_bike_front_seat_cat", 3.2, size=84, se="kon"),
        one(SCRAP, "ヤードを取り締まる\n*国の法律*は\nまだない", "calm_black_face_sheep", 2.8, se="pi"),
        one(SCRAP, "ルールは県の条例だけ\n違反しても\n*30万円以下の罰金*など", "glare_disgusted_cat", 3.0, size=84, se="buzzer_wrong"),
        one(RAID, "単純計算で\n*9億円近く*の\n被害かもしれないのに……", "despair_dramatic_kitten", 2.8, size=90,
            se="chin_bell_failure_sad_ending"),
        vic(GARAGE, "警察に届けたら\n“見つかったら\n連絡します”……", "sad_black_dog", 2.8, se="tear_drop"),
        one(RUN, "盗まれた人が\n*自分で探す*ことも多い\nと言われている", "sulk_hungry_cat", 2.8, size=90, se="deflate_hyororo"),
        one(RAID, "窃盗団に\n“大した罪にならない”と\n思われている　と言われている", "huh_huh_cat", 3.0, size=84,
            se="question_mark_pop_confused_huh"),
        one(GARAGE, "これ\n*ナメられすぎ*\nじゃない？", "rage_talking_cat", 2.4, size=120, se="tv_hissatsu_slash_finishing_blow_kill"),
        one(CITY, "あなたの車は\n*大丈夫？*", "eat_pop_cat", 2.4, size=130, se="chirin"),
        one(CITY, "※逮捕された4人は容疑の段階です\n※300台は警察の見立て（報道より）\n※9億円は保険金の平均からの単純計算です", "eat_pop_cat",
            3.0, size=48, se="pinpon_notice"),
    ]


def main():
    cs = M.keep_going(cuts())
    title = M.title_band(*TITLE)
    for c in cs:
        c["draw"] = M.make_draw(c, title)
    print(f"{len(cs)} カット・{sum(R.cut_dur(c) for c in cs):.1f}秒")
    S.run(cs, title, os.path.join(HERE, "out", NAME + ".mp4"), os.path.join(HERE, "out", NAME + "_preview"))


if __name__ == "__main__":
    main()
