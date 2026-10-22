"""24本目のショート2本目「なぜ1人で受け取れる？」政党交付金のしくみ。60秒ちょうど。作りは short_24_chudo.py と同じ。

python3 catmeme/short_24b_chudo.py → out/short_24b_chudo.mp4
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M
from short_24_chudo import AGENCY, HALL, MEETING, MONEY, OFFICE, PAPERS, TL, one, org

HERE = M.HERE
NAME = "short_24b_chudo"
TITLE = ("党は解体、議員は1人", "なぜ税金が入る？", M.WHITE, M.YELLOW, M.RED)
NORA = os.path.join(S.BGM, "野良猫は宇宙を目指した.mp3")


def cuts():
    return [
        org(AGENCY, "総務省", "10月20日\n11の党に\n*政党交付金*", "work_typing_cat", 3.4, se=["jan", "explosion_chudoon"],
            bgm={"file": NORA, "gain": -3}),
        one(OFFICE, "議員*1人*の\n中道改革連合にも\n約5億8470万円", "stare_interviewer_cat", 3.0, se="kon"),
        one(OFFICE, "*なんで！？*", "huh_huh_cat", 2.4, who="N", size=130),
        one(TL, "そもそも\n政党交付金は\n*税金*", "talk_orange_white_sitting_cat", 2.6, se="pikon"),
        one(TL, "*国民1人あたり250円*\nぶんが\n政党に配られる", "talk_orange_white_sitting_cat", 3.0, se="pi"),
        one(MONEY, "毎年\n*約315億円*\n（2025年分）", "calm_black_face_sheep", 2.6, se="price_display"),
        one(MONEY, "*毎年300億円以上！？*", "surprise_big_pupils_cat", 2.4, who="N", size=100),
        one(TL, "ルール①\n*1月1日*の時点で\n1年分が決まる", "calm_black_face_sheep", 3.0, se="pi"),
        one(TL, "ルール②\n4・7・10・12月の\n*年4回*に分けて交付", "calm_black_face_sheep", 3.0, se="pi"),
        one(TL, "ルール③\n離党した議員は\n*持っていけない*", "calm_black_face_sheep", 3.0, se="pi"),
        one(OFFICE, "1月1日の中道は\n*まだ大きな党*\n→1年分 約23億円", "work_typing_cat", 3.2, se="kon"),
        one(OFFICE, "党を*1人で残せば*\n残りも入る\n（報道の解説）", "work_typing_cat", 3.0, se="pi"),
        one(OFFICE, "それ\n*アリなの！？*", "huh_huh_cat", 2.0, who="N", size=120),
        one(PAPERS, "今のルールでは\n*違法ではない*", "talk_orange_white_sitting_cat", 2.6, se="kon"),
        one(PAPERS, "党は\n*衆院選の支払い*に\n使うと説明", "talk_orange_white_sitting_cat", 3.0, se="pi"),
        org(MEETING, "日本維新の会", "“1人しか残っていないのに\n*受け取るべきではない*”\n（要旨）", "angry_aiming_cat", 3.4,
            se="page_turn_01"),
        one(HALL, "制度の\n*見直し*を求める声も", "realize_wet_cat_stare", 2.6, who="N", se="kon"),
        one(PAPERS, "使い道は\n毎年*報告書で公開*される", "talk_orange_white_sitting_cat", 2.8, se="pinpoon_note"),
        one(PAPERS, "*ちゃんと見届けよう*", "eat_pop_cat", 2.2, who="N", size=110, se="chirin"),
        one(PAPERS, "※発言・数字は報道・総務省の資料によるものです\n※特定の政党を応援・批判する意図はありません",
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
