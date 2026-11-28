"""11本目（2,000万円の車を盗んだ疑いでも不起訴）のショート。作りは最新の参考マネ（short_10_idcf.py と同じ）。

python3 catmeme/short_11_fukiso.py → out/short_11_fukiso.mp4

本編（cuts_11_fukiso.py・原稿 scripts/11_fukiso.md）のルールをそのまま守る
- 不起訴の人は罪に問われていない：「犯人」と呼ばない・猫で演じない
- 国籍は報道どおり「ブラジル国籍の男性」「アメリカ国籍の男性」まで出す（10/12 ユーザー指定）。国籍への怒りは煽らない。怒りの矛先は事件・置き去りの被害者・理由を説明しない仕組み
- 役名（足元の黄緑の文字）は生き物だけ：車の持ち主・警備員
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M

HERE = M.HERE
NAME = "short_11_fukiso"
TITLE = ("まさかの不起訴", "2,000万円の車を盗んだ疑いでも")
C, L, Rr = M.C, M.L, M.Rr
LIME = M.LIME
PURPLE = os.path.join(S.BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")
LETTER = os.path.join(S.BGM, "手紙のさよなら.mp3")
HOME, FEST, PRESS, ROOM = "bg18_backyard", "bg13_izakaya", "bg07_press", "bg02_room"
M.BGS += [os.path.join(HERE, "backgrounds", "01_todai")]
OWNER, GUARD = "車の持ち主", "警備員"


def one(bg, say, a, dur, h=1100, **kw):
    return M.cut(bg, say, [(a, C, h, kw.pop("flip", False))], dur, **kw)


def vic(bg, say, a, dur, role, **kw):
    """被害者（架空）のひとこと。足元に役名。"""
    return M.cut(bg, say, [(a, C, 1100, False)], dur, label=role, label_x=540, col=LIME, **kw)


def cuts():
    return [
        one(HOME, "時価*2,000万円*の\n高級車が\n盗まれた", "surprise_big_pupils_cat", 2.8, shake=True,
            se=["jan", "explosion_chudoon"], bgm={"file": PURPLE, "gain": -6}),
        vic(HOME, "朝起きたら……\n車が……\nない……", "sad_banana_cat_cry", 2.6, OWNER, se="tear_drop"),
        one(PRESS, "盗んだ疑いで\n*ブラジル国籍*の男性を逮捕\nほかとあわせ*3件*で送検", "realize_wet_cat_stare", 3.0, se="siren_police"),
        one(PRESS, "さすがに\n起訴でしょ", "think_bike_front_seat_cat", 2.2, size=130, se="kon"),
        one(PRESS, "結果\n→　*不起訴*", "blank_black_cat_zoning_out", 2.4, size=160, shake=True, se=["explosion_dokaan"]),
        one(PRESS, "はあああ！？", "huh_huh_cat", 1.8, size=170, se="game_pokemon_super_effective_hit_big_damage"),
        one(PRESS, "地検「公訴を維持するに足りる\n証拠を収集するに\n至らなかった」", "calm_black_face_sheep", 3.2, size=72, se="pinpon_notice"),
        one(PRESS, "つまり\n*証拠が集まらなかった*\nってこと", "calm_black_face_sheep", 2.6, se="pikon"),
        vic(HOME, "じゃあ……\n私の車は……？", "sad_banana_cat_cry", 2.4, OWNER, se="chin_bell_failure_sad_ending"),
        one(FEST, "その2日後\nお祭りで警備員が\n*顔を殴られた*", "surprise_big_pupils_cat", 2.8, se="punch"),
        vic(FEST, "仕事してた\nだけなのに……", "sad_black_dog", 2.4, GUARD, se="tear_drop"),
        one(PRESS, "殴った疑いで逮捕された\n*アメリカ国籍*の男性も\n→　*不起訴*", "glare_disgusted_cat", 2.8, shake=True, se=["explosion_dokaan"]),
        one(PRESS, "理由は\n「犯行後の状況も含めた\n証拠を踏まえ」*だけ*", "rage_talking_cat", 3.0, size=86, se="pc_warning"),
        one(PRESS, "説明\nそれだけ！？", "rage_talking_cat", 2.0, size=160, shake=True, se="game_aceattorney_desk_slam"),
        M.cut(HOME, "被害者は\n*置き去り*……", [("sad_banana_cat_cry", L, 950, False), ("sad_black_dog", Rr, 950, True)], 2.6,
              label=GUARD, label_x=860, se="shock_piano", bgm={"file": LETTER, "gain": -6, "fade": 0.6}),
        one(ROOM, "納得できないときは\n*検察審査会*に\n申し立てる道もある", "eat_pop_cat", 3.0, se="idea_newtype_01"),
        one(ROOM, "でも被害者が\nそこまでやらなきゃ\nいけないの？", "sulk_hungry_cat", 2.6, se="question_hatena_maou"),
        one(ROOM, "必要なのは\nちゃんと裁くこと\n*なぜ不起訴かを説明すること*", "eat_pop_cat", 3.0, size=86, se="tv_professional_poon"),
        one(PRESS, "これ\n*納得できますか？*", "angry_cat_hits_cat", 2.6, size=140, shake=True, se="doon_heavy"),
        one(ROOM, "※不起訴の人は法律上\n罪に問われていません\n※国籍で人をひとくくりにする\n意図はありません", "eat_pop_cat", 2.8, size=58,
            se="pinpon_notice"),
    ]


def main():
    cs = M.keep_going(cuts())
    cs[14]["labels"] = [(OWNER, 230)]
    title = M.title_band(*TITLE)
    for c in cs:
        c["draw"] = M.make_draw(c, title)
    print(f"{len(cs)} カット・{sum(R.cut_dur(c) for c in cs):.1f}秒")
    S.run(cs, title, os.path.join(HERE, "out", NAME + ".mp4"), os.path.join(HERE, "out", NAME + "_preview"))


if __name__ == "__main__":
    main()
