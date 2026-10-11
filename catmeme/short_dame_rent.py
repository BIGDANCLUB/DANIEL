"""ダメ人間の猫ミーム #1「家賃で馬券買っちゃった」（台本：ユーザー指示 10/11）。作りは short_dame_template.py と同じ。

python3 catmeme/short_dame_rent.py → out/short_dame_rent.mp4
最初の1文は、ショートの頭で目を引くための“まとめ”（集中線＋揺れ＋ドカン）。
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M

HERE = M.HERE
NAME = "short_dame_rent"
TITLE = ("とあるダメ人間", "家賃で馬券買っちゃった")
C, L, Rr = M.C, M.L, M.Rr
RED = M.RED
NORA = os.path.join(S.BGM, "野良猫は宇宙を目指した.mp3")
LOFI = os.path.join(S.BGM, "2_23_AM.mp3")   # 最下位からの落ち込み（ダースベイダーのテーマは市販曲で使用不可）
LETTER = os.path.join(S.BGM, "手紙のさよなら.mp3")
HOME, PHONE, SPOT = "bg14_home_night", "bg26_phone_alert", "bg06_spotlight"


def one(bg, say, a, dur, h=1100, **kw):
    """1匹だけの独り言カット（主人公のダメ人間）。"""
    return M.cut(bg, say, [(a, C, h, kw.pop("flip", False))], dur, **kw)


def two(bg, say, me, other, dur, label, speaker=0, **kw):
    """主人公（左）と相手役（右・足元に役名）の掛け合い。me / other = (素材, 高さ)。"""
    return M.cut(bg, say, [(me[0], L, me[1], False), (other[0], Rr, other[1], True)], dur, label=label, speaker=speaker, **kw)


def race(say, runners, dur, **kw):
    """競馬：馬役の猫ミームが右から左へ走り抜ける。runners=[(素材, 高さ, 速さ, 下からの位置, 役名)]。"""
    c = M.cut(PHONE if kw.pop("phone", False) else SPOT, say, [(a, 540, h, False) for a, h, _, _, _ in runners], dur, **kw)
    for k, (a, h, speed, lift, tag) in zip(c["cats"], runners):
        k.update(move=(1500, 1500 - 2200 * speed), bob=40, phase=lift / 100, drop=-lift, pop=False, mute=True)
        if tag:
            k.update(tag=tag, tag_up=h * 0.15)
    return c


# 登場人物（主人公以外。生き物だけ）
OYA = ("sleepy_old_memories_cat", 1000)      # 大家さん（ずっと待ってくれている）
UMA = ("stand_real_sheep", 850)             # 次のレースの3倍の馬（→ 最下位の「あの馬」）
RUN1 = [("ride_kitten_bike", 520, 1.05, 0, "あの馬"), ("drive_monkey_golf_cart", 560, 1.25, 260, None),
        ("dance_cute_dog", 600, 1.4, 520, None)]
RUN2 = [("dance_white_dog", 560, 1.35, 0, None), ("drive_monkey_golf_cart", 560, 1.2, 280, None),
        ("stand_real_sheep", 520, 0.55, 540, "あの馬")]


def cuts():
    return [
        # 冒頭：まとめで目を引く
        one(SPOT, "家賃払うために\n*家賃で馬券*\n買っちゃった。", "sad_banana_cat_cry", 3.2, size=120, shake=True,
            se=["jan", "explosion_chudoon"], bgm={"file": NORA, "gain": -6}),
        one(HOME, "……いや、最初から\nそのつもりじゃ\nなかったんだけど。", "sad_black_dog", 2.8, se="whoosh_shu"),
        two(HOME, "家賃 *7万2千円*", ("think_bike_front_seat_cat", 1000), OYA, 2.0, "大家さん", size=130, se="page_turn_01"),
        two(HOME, "口座に *7万6千円*", ("think_bike_front_seat_cat", 1000), OYA, 2.0, "大家さん", size=130, se="pi"),
        two(HOME, "今月こそ\n払わんとな。", ("think_bike_front_seat_cat", 1000), OYA, 2.0, "大家さん", se="kon"),
        one(HOME, "……でも4千円で\n給料日まで2週間か。", "sulk_hungry_cat", 2.6, se="tear_drop"),
        one(HOME, "あー、きっつ。", "sulk_hungry_cat", 1.8, size=140),
        one(PHONE, "……あ、今日\n*競馬*あるじゃん。", "realize_wet_cat_stare", 2.2, se="pikon"),
        one(PHONE, "いやいや、\n*千円だけ*。", "happy_girlfriend_dance_cat", 2.0, se="shine_kira_01"),
        one(PHONE, "生活費の方からだし。", "happy_girlfriend_dance_cat", 2.0),
        race("……。", RUN1, 2.3, se=["drumroll", "dash_super_fast"]),
        two(PHONE, "は？外れた。", ("huh_huh_cat", 1050), ("snore_snoring_dog", 900), 1.8, "あの馬", size=150, se="buzzer_wrong"),
        two(HOME, "クッソ、あの馬\nなんで来ねえんだよ。", ("angry_cat_hits_cat", 1050), ("snore_snoring_dog", 900), 2.4, "あの馬",
            shake=True, se="tsukkomi_bishi"),
        two(PHONE, "……次のレース\n*3倍*か。", ("work_dog_staring_computer", 1000), UMA, 2.2, "3倍の馬", se="cursor_move_01"),
        two(PHONE, "5千円入れたら\n*1万5千円*……。", ("work_dog_staring_computer", 1000), UMA, 2.2, "3倍の馬", se="price_display"),
        one(HOME, "家賃払っても\n飯食えるな。", "eat_crunchy_cat_luna", 2.2, se="eat_paku"),
        one(HOME, "……よし。", "flip_emo_cat_hair", 1.6, size=200, se="sword_shakiin"),
        race("……。", RUN2, 2.4, se=["drumroll", "dash_super_fast"]),
        two(SPOT, "はあ！？\n*最下位*！？", ("surprise_big_pupils_cat", 1100), UMA, 1.9, "あの馬", size=160, shake=True,
            se=["explosion_dokaan"], bgm={"file": LOFI, "gain": -6, "fade": 0.3}),
        one(SPOT, "ふざけんなよ！！", "rage_talking_cat", 1.9, size=150, shake=True, se="game_aceattorney_desk_slam"),
        one(HOME, "……。", "blank_black_cat_zoning_out", 1.2, size=200),
        one(HOME, "あ、*家賃まで*\n使っちゃった。", "realize_wet_cat_stare", 2.2, se="shock_piano"),
        one(HOME, "……やべえ。", "despair_dramatic_kitten", 1.8, size=170, se="deflate_hyororo"),
        two(HOME, "大家さん、ずっと\n待ってくれてんのに。", ("sad_black_dog", 950), OYA, 2.4, "大家さん", se="tear_drop",
            bgm={"file": LETTER, "gain": -6, "fade": 0.6}),
        two(HOME, "……。", ("sad_black_dog", 950), OYA, 1.2, "大家さん", size=200),
        two(HOME, "いや、だからこそ\n半端な金額じゃ\n*失礼*だよな。", ("showoff_gojo_cosplay_cat", 1000), OYA, 2.6, "大家さん",
            se="idea_newtype_01", bgm={"file": NORA, "gain": -6, "fade": 0.3}),
        two(HOME, "……明日もう一回増やして\n*ちゃんと払お*。", ("cocky_dj_cat", 1000), OYA, 2.8, "大家さん", se="tv_dokkiri_tettere"),
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
