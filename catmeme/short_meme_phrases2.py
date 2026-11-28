"""ショート「ニュースから生まれたネット名フレーズ 第2弾」（縦 1080x1920・45〜58秒の1本）。最初の5秒は A＋D のつかみ。

python3 catmeme/short_meme_phrases2.py → out/short_meme_phrases2.mp4

① 並べない万博（大阪・関西万博・2025）… 「並ばない万博」のはずが長い行列、予約も取れず「並べない」と皮肉られた
② 暫定とは？（ガソリンの暫定税率・1974〜2025）… 「暫定」のまま約51年続いた
③ ステルス値上げ … 値段はそのまま、中身をこっそり減らす“実質値上げ”
ルール：笑うのは言葉と出来事のおかしさまで。個人名・特定の商品名は出さない。
"""
import os

import short_03_kodomo_nisa as S
import short_04_leak as Q
import short_hooks as H
import short_meme_phrases as M

HERE = S.HERE
PURPLE, COCOA, MIRAI = M.PURPLE, M.COCOA, M.MIRAI
NEWS = S.NEWS
YELLOW, RED, NAVY = S.YELLOW, S.RED, S.NAVY
GREEN, ORANGE = H.GREEN, H.ORANGE
card, react = M.card, M.react
OUT = os.path.join(HERE, "out", "short_meme_phrases2.mp4")
PHRASES = [("並べない万博", RED), ("暫定とは？", ORANGE), ("ステルス値上げ", NAVY)]


def cuts():
    return [
        H.hook_cut_AD(PHRASES, big="名フレーズ", count="第2弾!!", beat_total=2.4, bgm={"file": PURPLE, "gain": -4}),
        # ① 並べない万博
        Q.panel(card(1, "大阪・関西万博（2025年）", "並べない万博", ["目標は「並ばない万博」", "実際は大行列　予約も取れず「並べない」"]),
                "並ばない\n→並べない！？", dur=5.0, se="card_flip"),
        react("bg09_sns", "huh_huh_cat", "“並ばない”って\nそういう意味！？", dur=2.6, se="boing_01"),
        Q.two("bg09_sns", "weird_meowing_cat", "eat_pop_cat", "並ばない→長く並ぶ\n→並べない\nと言い換えが進化", who="R", dur=3.6,
              se="page_turn_01"),
        # ② 暫定とは？
        Q.panel(card(2, "ガソリンの暫定税率（1974〜2025年）", "暫定とは？", ["「暫定」として1974年にスタート", "そのまま約51年続いて　2025年末に廃止"],
                     col=ORANGE), "51年も\n“暫定”！？", cap_col=RED, dur=5.0, se="card_flip", bgm={"file": COCOA, "gain": -6}),
        react("bg20_counter", "surprise_big_pupils_cat", "暫定の意味を\n辞書で引きたい", dur=2.6, se="kon"),
        Q.two("bg02_room", "spin_spinning_cat", "think_bike_front_seat_cat", "1リットルあたり25.1円\n2025年12月31日に\nようやく廃止された", who="R", dur=3.6,
              se="pinpoon_correct"),
        # ③ ステルス値上げ
        Q.panel(card(3, "物価高のなかで", "ステルス\n値上げ", ["値段はそのまま　中身をこっそり減らす", "“ステルス”＝こっそり、気づかれないように"],
                     col=NAVY), "こっそり\n値上げ！？", dur=5.0, se="card_flip"),
        react("bg16_food_aisle", "glare_disgusted_cat", "お菓子が\n1枚減ってる…", dur=2.6, se="tear_drop"),
        Q.two("bg16_food_aisle", "huh_huh_cat", "eat_pop_cat", "値段より\n「内容量」の数字を\n見るのが大事な", who="R", dur=3.4, se="tv_professional_poon"),
        Q.two("bg02_room", "sleepy_sleepy_cat", "eat_pop_cat", "言葉にすると\nモヤモヤが\n伝わりやすいんだな", who="R", dur=3.2, se="hyoshigi_01",
              bgm={"file": MIRAI, "gain": -8, "fade": 0.8}),
        Q.one("bg03_blackboard", "wave_waving_cat", "ニュース猫", NEWS, "第1弾の6選も見てね\nほかに知ってたら\nコメントで！", cap_col=YELLOW, h=760,
              dur=3.4, se="chirin"),
    ]


def main():
    S.run(cuts(), Q.title_band("ニュースから生まれた", "ネット名フレーズ第2弾", label="ネットで生まれた名フレーズ"), OUT,
          os.path.join(HERE, "out", "short_meme_phrases2_preview"))


if __name__ == "__main__":
    main()
