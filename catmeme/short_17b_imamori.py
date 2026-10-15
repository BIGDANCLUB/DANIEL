"""17本目（今森茉耶）のショート2本目「放送中にヒロインが交代」。60秒ちょうど。
番組（テレビ朝日・東映）がどう対応したかが中心。週刊誌は疑惑、降板の公式理由は20歳未満の飲酒。"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M
from short_17_imamori import HERO, IZAKAYA, MAG, QUIET, STUDIO, TL, TVSTA, one, org, side

HERE = M.HERE
NAME = "short_17b_imamori"
TITLE = ("放送中にヒロイン交代", "戦隊シリーズ異例の対応", M.WHITE, M.YELLOW, M.RED)
PURPLE = os.path.join(S.BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")


def cuts():
    return [
        side("p7_cast_announcement", "戦隊ヒロインが\n*放送の途中で*\n交代！？", "surprise_big_pupils_cat", 3.0, shake=True,
             se=["jan", "explosion_chudoon"], bgm={"file": PURPLE, "gain": -6}),
        side("p1_cast_and_hero", "ゴジュウユニコーン役\n*今森茉耶*さん", "huh_huh_cat", 2.4, se="pi"),
        side("p8_cast_items", "スーパー戦隊\n*50周年*の記念作品", "excited_hodomoe_city_cat", 2.4, se="pikon"),
        one(HERO, "シリーズ初の\n*女性ブラック*", "stare_big_eyes_tabby_kitten", 2.4, size=120, se="jan"),
        one(HERO, "2025年9月\n週刊誌の*不倫疑惑*\n（あくまで疑惑）", "peek_what_happen_cat", 2.8, size=96, se="page_turn_02"),
        org(TVSTA, "事務所", "11月8日\n*20歳未満の飲酒*を確認\n契約を解除", "work_typing_cat", 3.0, size=96, shake=True,
            se=["explosion_dokaan"]),
        org(TVSTA, "テレビ朝日", "番組も\n*降板*を発表", "call_customer_service_cat", 2.4, size=120, se="page_turn_01"),
        one(IZAKAYA, "19歳は成人でも\n*お酒は20歳から*", "think_bike_front_seat_cat", 2.6, size=100, se="pi"),
        one(IZAKAYA, "2022年に成人は*18歳*に\nでもお酒とたばこは\n*20歳のまま*", "stare_interviewer_cat", 2.8, size=96, se="kon"),
        one(QUIET, "本人もInstagramで\n“*非常に恥ずべき行為*”と\n謝罪", "realize_wet_cat_stare", 2.6, size=96, se="kon"),
        one(HERO, "でも番組は\n*放送中*……\nどうする？", "confused_i_dont_know_cat", 2.6, size=100, se="question_mark_pop_confused_huh"),
        one(HERO, "出演シーンを\n*カット・編集*して放送", "work_dog_staring_computer", 2.6, size=100, se="pc_warning"),
        one(HERO, "変身したあとの\nヒーローは\n*そのまま登場*", "stare_interviewer_cat", 2.6, se="pi"),
        org(TVSTA, "番組", "代わりの起用発表は\n降板から*1週間後*\n11月15日", "work_typing_cat", 2.6, size=96, se="pikon"),
        side("p4_shida_kohaku", "11月30日から\n*志田こはく*さんが\n同じ役に", "yell_orange_fat_cat", 3.0, size=96,
             se=["explosion_chudoon"]),
        one(HERO, "志田さんは\n『ドンブラザーズ』で\n*ヒロイン経験*あり", "excited_hodomoe_city_cat", 2.8, size=96, se="pi"),
        one(HERO, "物語では\n“*顔と声が変わった*”\n設定と紹介された", "stare_big_eyes_tabby_kitten", 2.8, size=96, se="kon"),
        one(HERO, "むちゃだけど\n*番組を止めない*工夫", "talk_orange_white_sitting_cat", 2.6, size=100, se="idea_newtype_01"),
        org(TVSTA, "テレビ朝日", "社長は\n“*子供向け番組で\n申し訳ない*”と謝罪", "call_customer_service_cat", 2.8, size=96,
            se="page_turn_02"),
        one(TL, "1人の行動が\n*番組全体*に影響", "realize_wet_cat_stare", 2.6, size=110, se="kon"),
        one(TL, "あなたは\n*覚えてる？*", "eat_pop_cat", 2.2, size=130, se="chirin"),
        one(TL, "※週刊誌の報道は疑惑で、降板の公式の理由は20歳未満の飲酒です\n※本人・関係者への誹謗中傷はやめてください\n"
                "※背景イラストの一部はAIで作っています", "eat_pop_cat", 3.0, size=42, se="pinpon_notice"),
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
