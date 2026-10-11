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
TITLE = ("ダメ人間", "家賃で馬券買っちゃった")
C = M.C
RED = M.RED
NORA = os.path.join(S.BGM, "野良猫は宇宙を目指した.mp3")
VADER = os.path.join(S.BGM, "～やる気のないダースベイダーのテーマ～ (320  kbps).mp3")
LETTER = os.path.join(S.BGM, "手紙のさよなら.mp3")
HOME, PHONE, SPOT = "bg14_home_night", "bg26_phone_alert", "bg06_spotlight"


def one(bg, say, a, dur, h=1100, **kw):
    """1匹だけの独り言カット（主人公のダメ人間）。"""
    return M.cut(bg, say, [(a, C, h, kw.pop("flip", False))], dur, **kw)


def cuts():
    return [
        # 冒頭：まとめで目を引く
        one(SPOT, "家賃払うために\n*家賃で馬券*\n買っちゃった。", "sad_banana_cat_cry", 3.2, size=120, shake=True, label="ダメ人間", label_x=540,
            se=["jan", "explosion_chudoon"], bgm={"file": NORA, "gain": -6}),
        one(HOME, "……いや、最初から\nそのつもりじゃ\nなかったんだけど。", "sad_black_dog", 2.8, se="whoosh_shu"),
        one(HOME, "家賃 *7万2千円*", "think_bike_front_seat_cat", 2.0, size=130, se="page_turn_01"),
        one(HOME, "口座に *7万6千円*", "think_bike_front_seat_cat", 2.0, size=130, se="pi"),
        one(HOME, "今月こそ\n払わんとな。", "think_bike_front_seat_cat", 2.0, se="kon"),
        one(HOME, "……でも4千円で\n給料日まで2週間か。", "sulk_hungry_cat", 2.6, se="tear_drop"),
        one(HOME, "あー、きっつ。", "sulk_hungry_cat", 1.8, size=140),
        one(PHONE, "……あ、今日\n*競馬*あるじゃん。", "realize_wet_cat_stare", 2.2, se="pikon"),
        one(PHONE, "いやいや、\n*千円だけ*。", "happy_girlfriend_dance_cat", 2.0, se="shine_kira_01"),
        one(PHONE, "生活費の方からだし。", "happy_girlfriend_dance_cat", 2.0),
        one(PHONE, "……。", "stare_standing_marmot", 1.8, size=200, se="drumroll"),
        one(PHONE, "は？外れた。", "huh_huh_cat", 1.8, size=150, se="buzzer_wrong"),
        one(HOME, "クッソ、あの馬\nなんで来ねえんだよ。", "angry_cat_hits_cat", 2.4, shake=True, se="tsukkomi_bishi"),
        one(PHONE, "……次のレース\n*3倍*か。", "work_dog_staring_computer", 2.2, se="cursor_move_01"),
        one(PHONE, "5千円入れたら\n*1万5千円*……。", "work_dog_staring_computer", 2.2, se="price_display"),
        one(HOME, "家賃払っても\n飯食えるな。", "eat_crunchy_cat_luna", 2.2, se="eat_paku"),
        one(HOME, "……よし。", "flip_emo_cat_hair", 1.6, size=200, se="sword_shakiin"),
        one(PHONE, "……。", "blank_black_cat_zoning_out", 1.8, size=200, se="drumroll"),
        one(SPOT, "はあ！？\n*最下位*！？", "surprise_big_pupils_cat", 1.9, size=160, shake=True, se=["explosion_dokaan"],
            bgm={"file": VADER, "gain": -6, "fade": 0.3}),
        one(SPOT, "ふざけんなよ！！", "rage_talking_cat", 1.9, size=150, shake=True, se="game_aceattorney_desk_slam"),
        one(HOME, "……。", "stand_real_sheep", 1.4, size=200),
        one(HOME, "あ、*家賃まで*\n使っちゃった。", "realize_wet_cat_stare", 2.2, se="shock_piano"),
        one(HOME, "……やべえ。", "despair_dramatic_kitten", 1.8, size=170, se="deflate_hyororo"),
        one(HOME, "大家さん、ずっと\n待ってくれてんのに。", "sad_black_dog", 2.4, se="tear_drop",
            bgm={"file": LETTER, "gain": -6, "fade": 0.6}),
        one(HOME, "……。", "sleepy_old_memories_cat", 1.4, size=200),
        one(HOME, "いや、だからこそ\n半端な金額じゃ\n*失礼*だよな。", "showoff_gojo_cosplay_cat", 2.6, se="idea_newtype_01",
            bgm={"file": NORA, "gain": -6, "fade": 0.3}),
        one(HOME, "……明日もう一回増やして\n*ちゃんと払お*。", "cocky_dj_cat", 3.0, label="ダメ人間", label_x=540, se="tv_dokkiri_tettere"),
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
