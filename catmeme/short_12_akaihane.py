"""12本目（赤い羽根募金、2.5億円の行方が分からない）のショート。作りは最新の参考マネ（short_11_fukiso.py と同じ）。

python3 catmeme/short_12_akaihane.py → out/short_12_akaihane.mp4

本編（cuts_12_akaihane.py・原稿 scripts/12_akaihane.md）のルールをそのまま守る
- 元事務局長は「着服の疑い」。名前・顔は出さない・猫で演じない
- 募金した人・福祉の現場は被害者側。「募金するな」とは言わない
- 役名（足元の黄緑の文字）は生き物だけ：募金した人・福祉の現場の人
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M

HERE = M.HERE
NAME = "short_12_akaihane"
TITLE = ("国税が来て発覚！", "赤い羽根2.5億円", M.RED, M.YELLOW, M.WHITE)   # 上の帯はサムネA案と同じ文言（10/13）
C, L, Rr = M.C, M.L, M.Rr
LIME = M.LIME
PURPLE = os.path.join(S.BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")
LETTER = os.path.join(S.BGM, "手紙のさよなら.mp3")
CONV, PRESS, OFFICE, MEET, ROOM = "bg15_convenience", "bg07_press", "bg25_office_desk", "bg05_meeting", "bg02_room"
M.BGS += [os.path.join(HERE, "backgrounds", "01_todai")]
DON, GEN = "募金した人", "福祉の現場の人"


def one(bg, say, a, dur, h=1100, **kw):
    return M.cut(bg, say, [(a, C, h, kw.pop("flip", False))], dur, **kw)


def vic(bg, say, a, dur, role, **kw):
    return M.cut(bg, say, [(a, C, 1100, False)], dur, label=role, label_x=540, col=LIME, **kw)


def cuts():
    return [
        one(PRESS, "今年　大臣たちの胸に\n*赤い羽根がない*", "surprise_big_pupils_cat", 2.8, shake=True,
            se=["jan", "explosion_chudoon"], bgm={"file": PURPLE, "gain": -6}),
        one(PRESS, "政府ごと\n着用を控えた", "huh_huh_cat", 2.2, size=130, se="question_mark_pop_confused_huh"),
        one(OFFICE, "北海道で\n集めた募金など\n*約2億5,000万円*の行方が\n分からなくなっている", "realize_wet_cat_stare", 3.4, size=86,
            shake=True, se=["explosion_dokaan"]),
        vic(CONV, "毎年　コンビニの\nお釣りを\n入れてたのに……", "sad_banana_cat_cry", 2.8, DON, se="tear_drop"),
        one(OFFICE, "会計は\n事務局長が\n*1人で管理*", "glare_disgusted_cat", 2.6, se="pc_warning"),
        one(OFFICE, "*通帳も印鑑も*\n1人", "glare_disgusted_cat", 2.0, size=130, se="buzzer_wrong"),
        one(OFFICE, "足りない分は\n年度末に借金して\n*穴埋め*していたとみられる", "think_bike_front_seat_cat", 3.0, size=90, se="page_turn_01"),
        one(OFFICE, "監査は\n*決算の日の残高*しか\n見ていなかった", "think_bike_front_seat_cat", 2.8, se="kon"),
        one(PRESS, "発覚のきっかけは\n*国税の査察*", "surprise_big_pupils_cat", 2.6, shake=True, se="game_pokemon_super_effective_hit_big_damage"),
        one(PRESS, "内部じゃ\n誰も気づいて\nないの！？", "rage_talking_cat", 2.4, size=130, se="game_aceattorney_desk_slam"),
        one(PRESS, "元事務局長は懲戒解雇\n「着服の疑い」で\n刑事告訴を検討", "calm_black_face_sheep", 3.0, size=88, se="page_turn_02"),
        vic(OFFICE, "お年寄りに配る\nお弁当の予算が\n*半分*……", "sad_black_dog", 2.8, GEN, se="tear_drop",
            bgm={"file": LETTER, "gain": -6, "fade": 0.6}),
        one(OFFICE, "今年度の助成金は\n予定の*約5割*", "despair_dramatic_kitten", 2.6, se="chin_bell_failure_sad_ending"),
        one(CONV, "街頭ボランティアは\n例年の*8割減*", "sulk_hungry_cat", 2.6, se="deflate_hyororo"),
        vic(CONV, "募金したくても\nどこに入れたら\nいいのか……", "sad_banana_cat_cry", 2.6, DON, se="tear_drop"),
        one(ROOM, "“いい人だから任せる”が\n*いちばん危ない*", "eat_pop_cat", 2.8, size=90, se="tv_hissatsu_slash_finishing_blow_kill"),
        one(ROOM, "募金する？しない？\n大事なのは\n*どこに・どう使われるか*", "eat_pop_cat", 3.2, size=86, se="idea_newtype_01"),
        one(ROOM, "決算を公開してる？\nお金を扱う人は\n*1人じゃない？*", "calm_black_face_sheep", 3.0, size=90, se="pinpoon_correct"),
        one(CONV, "あなたは今年\n*する？しない？*", "happy_girlfriend_dance_cat", 2.6, size=130, se="chirin"),
        one(ROOM, "※元事務局長は「着服の疑い」の段階で\n刑事手続きで確定したものではありません\n※金額は北海道共同募金会の発表・報道より", "eat_pop_cat",
            3.0, size=50, se="pinpon_notice"),
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
