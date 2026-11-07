"""24本目（中道改革連合の政党交付金）のショート1本目「議員1人の党に5.8億円」。作りは short_17_imamori.py と同じ。60秒ちょうど。

python3 catmeme/short_24_chudo.py → out/short_24_chudo.mp4
- 実在の政治家は猫で演じない（写真は報道写真・発言は要旨）。党・役所は名札つきの猫
- 党の説明と批判の両方を出す。悪口・あだ名は使わない。笑顔の写真を批判の言葉と並べない
- 画面の下と右端には猫・役名・写真を置かない
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M

HERE = M.HERE
NAME = "short_24_chudo"
TITLE = ("議員1人の党に", "交付金5.8億円", M.WHITE, M.YELLOW, M.RED)
C = M.C
PURPLE = os.path.join(S.BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")
COCOA = os.path.join(S.BGM, "星降る夜のホットココア.mp3")
M.BGS[:0] = [os.path.join(HERE, "backgrounds", d) for d in ("24_chudo/photos", "16_tenchim", "15_vambi", "17_imamori", "14_japan",
                                                            "04_leak", "01_todai")]
MONEY, PAPERS, AGENCY, OFFICE, MEETING, VOTE, PRESS, TL, HALL = (
    "bg87_refund_money", "bg88_contract_papers", "bg78_agency_office", "bg25_office_desk", "bg05_meeting", "bg04_voting",
    "bg07_press", "bg103_timeline2", "bg75_seminar_hall")
NEWS, SAGE = "ニュース猫", "博識な猫"


def one(bg, say, a, dur, who="S", **kw):
    return M.cut(bg, say, [(a, C, 1100, False)], dur, label={"N": NEWS, "S": SAGE}[who], label_x=540, **kw)


def org(bg, who, say, a, dur, **kw):
    c = M.cut(bg, say, [(a, C, 1100, False)], dur, label=who, label_x=540, **kw)
    c["label_size"] = 96
    return c


def photo_img(name, box=(900, 560)):
    from PIL import Image, ImageOps
    im = Image.open(M.bg_path(name)).convert("RGB")
    k = min(box[0] / im.width, box[1] / im.height)
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    return ImageOps.expand(im, border=10, fill=(255, 255, 255)).convert("RGBA")


def pic(name, say, dur, **kw):
    """報道写真をセリフの下に枠つきで（猫なし）。顔に字幕をかけない。"""
    c = M.cut(TL, say, [], dur, size=kw.pop("size", 70), se=kw.pop("se", "page_turn_01"), **kw)
    img = photo_img(name)
    c["img"], c["img_y"] = img, M.SAFE_BOTTOM - 10 - img.height / 2
    return c


def cuts():
    return [
        org(MONEY, "中道改革連合", "議員*1人*の党に\n政党交付金\n*約5億8470万円*", "meow_gray_white_kitten", 3.2,
            se=["jan", "explosion_chudoon"], bgm={"file": PURPLE, "gain": -4}),
        one(MONEY, "1人で\n*5億8000万円！？*", "surprise_big_pupils_cat", 2.4, who="N", size=110),
        one(MONEY, "議員の給料じゃなく\n*党に入るお金*", "talk_orange_white_sitting_cat", 2.6, se="pi"),
        pic("p1_party_handshake", "2026年1月\n立憲民主党と公明党が\n*合流してできた新党*", 3.2),
        one(VOTE, "2月の衆院選で\n*49議席*に", "calm_black_face_sheep", 2.6, se="kon"),
        one(MEETING, "9月　合流が決裂\n*事実上解体*", "work_typing_cat", 2.6, se="pi"),
        one(OFFICE, "49人のうち\n*48人が離党*\n残ったのは1人", "stare_interviewer_cat", 3.0, se="kon"),
        one(OFFICE, "なのに\n*お金は入る*の！？", "huh_huh_cat", 2.4, who="N", size=110),
        one(TL, "交付金は\n*1月1日*の時点で\n1年分が決まる", "talk_orange_white_sitting_cat", 3.0, se="pikon"),
        one(TL, "今年分は\n*約23億3881万円*", "talk_orange_white_sitting_cat", 2.6, se="price_display"),
        one(TL, "離党した議員は\n*新しい党に\n持っていけない*", "calm_black_face_sheep", 3.0, se="pi"),
        one(OFFICE, "だから党を\n*1人で残した*\n（報道の解説）", "calm_black_face_sheep", 3.0, se="kon"),
        one(PAPERS, "党の説明\n衆院選の経費\n*約20億円*を支払い中", "work_typing_cat", 3.2, se="page_turn_02",
            bgm={"file": COCOA, "gain": -4, "fade": 0.5}),
        pic("p3_hashina_pose", "中道で幹事長を務めた\n*階猛氏*", 2.6),
        pic("p2_hashina_talk", "“*負い目を感じなくては*\nいけないものではない”\n（要旨）", 3.2),
        org(MEETING, "公明党", "“国民の血税\n*使い道をしっかり示して*”\n（要旨）", "stare_interviewer_cat", 3.2, se="page_turn_01"),
        one(HALL, "世論調査では\n*74.0%*が\n“納得できない”", "realize_wet_cat_stare", 3.0, who="N", se="doon_heavy"),
        one(MONEY, "12月分も\n*交付される見込み*", "talk_orange_white_sitting_cat", 2.6, se="pi"),
        one(MONEY, "あなたは\n*納得できる？*", "eat_pop_cat", 2.2, size=120, se="chirin"),
        one(MONEY, "※発言・数字は報道によるものです\n※特定の政党を応援・批判する意図はありません\n※写真は報道写真です",
            "eat_pop_cat", 3.0, size=44, se="pinpon_notice"),
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
