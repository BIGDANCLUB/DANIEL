"""19本目（猪苗代湖ボート事故、6年目の逆転有罪）のショート。作りは short_17_imamori.py と同じ。60秒ちょうど。

python3 catmeme/short_19_inawashiro.py → out/short_19_inawashiro.mp4
- 人が亡くなった事故なので笑いは入れない：落ち着いた猫・静かな効果音だけ（驚き・揺れの演出はしない）
- 亡くなった男の子・ボートを操縦していた人の名前は出さない。事故は再現しない。ご家族の言葉は報道の要旨だけ
- 画面の下と右端には猫・役名を置かない（short_refstyle の SAFE_BOTTOM）
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M

HERE = M.HERE
NAME = "short_19_inawashiro"
TITLE = ("猪苗代湖ボート事故", "最高裁で逆転有罪", M.WHITE, M.YELLOW, M.RED)
C = M.C
LETTER = os.path.join(S.BGM, "手紙のさよなら.mp3")
M.BGS[:0] = [os.path.join(HERE, "backgrounds", d) for d in ("19_inawashiro", "17_imamori")]
COURT, COURTROOM, LAKE, SHORE, JACKET, FLOWERS, SWIM, SUNSET = (
    "bg104_supreme_court", "bg105_courtroom", "bg106_lake_calm", "bg107_lake_shore", "bg108_lifejacket", "bg111_white_flowers",
    "bg112_swim_area", "bg110_lake_sunset")
NEWS, SAGE = "ニュース猫", "博識な猫"


def one(bg, say, a, dur, who="S", size=96, se="pi", **kw):
    """しゃべる猫だけを真ん中に（名前つき）。"""
    return M.cut(bg, say, [(a, C, 1100, False)], dur, label={"N": NEWS, "S": SAGE}[who], label_x=540, size=size, se=se, **kw)


def cuts():
    return [
        one(COURT, "6年前　湖で\n8歳の男の子が\n亡くなった事故", "stare_interviewer_cat", 3.2, bgm={"file": LETTER, "gain": -6}),
        one(COURT, "2026年10月16日\n最高裁が\n*逆転有罪*", "calm_black_face_sheep", 3.0, se="kon"),
        one(LAKE, "2020年9月\n福島県の\n*猪苗代湖*", "talk_orange_white_sitting_cat", 2.6),
        one(SHORE, "ライフジャケットを着て\n湖に浮かんでいた\n*4人*", "talk_orange_white_sitting_cat", 3.0),
        one(SHORE, "そこへ\n*プレジャーボート*が\n突っ込んだ", "stand_real_sheep", 2.8),
        one(JACKET, "8歳の男の子が亡くなり\nお母さんは\n*両足を切断*", "stand_real_sheep", 3.2, size=90),
        one(JACKET, "着てたのに……", "sad_black_dog", 2.2, who="N", size=110),
        one(COURTROOM, "争点は\n衝突の前に\n*見つけられたか*", "stare_interviewer_cat", 3.0),
        one(COURTROOM, "一審（2023年）\n*有罪*\n禁錮2年の実刑", "calm_black_face_sheep", 3.0, se="kon"),
        one(COURTROOM, "約223メートル手前で\n*見つけられたはず*", "calm_black_face_sheep", 3.0),
        one(COURTROOM, "二審（2024年）\n*無罪*", "work_typing_cat", 2.6, se="kon"),
        one(COURTROOM, "確実に見つけられたとは\n*認めがたい*", "work_typing_cat", 3.0),
        one(COURTROOM, "同じ証拠で\n答えが*変わった*……", "realize_wet_cat_stare", 2.6, who="N"),
        one(COURT, "そして最高裁は\n二審の無罪を\n*破棄*", "stare_interviewer_cat", 3.0, se="kon"),
        one(COURT, "“破棄しなければ\n*著しく正義に反する*”", "stare_interviewer_cat", 3.0),
        one(FLOWERS, "お父さん（報道の要旨）\n“ようやく\n*分かってくれる人*が”", "meow_gray_white_kitten", 3.4, size=88),
        one(FLOWERS, "“早く息子に\n*会いに行きたい*”", "meow_gray_white_kitten", 3.0, se=None),
        one(SWIM, "水の上には\n信号も*白線*もない", "talk_orange_white_sitting_cat", 2.8),
        one(SUNSET, "亡くなった男の子の\n*ご冥福*を\nお祈りします", "sleepy_old_memories_cat", 3.2, se=None),
        one(SUNSET, "※裁判の内容・ご家族の言葉は報道の要旨です\n※猫は演出です\n※背景イラストはAIで作っています",
            "sleepy_old_memories_cat", 3.0, size=44, se="pinpon_notice"),
    ]


def main():
    cs = M.keep_going(cuts())
    cs[0]["se"] = "pi"   # 人が亡くなった事故なので、最初の「チリン」は入れない（静かに始める）
    title = M.title_band(*TITLE)
    for c in cs:
        c["draw"] = M.make_draw(c, title)
    print(f"{len(cs)} カット・{sum(R.cut_dur(c) for c in cs):.1f}秒")
    S.run(cs, title, os.path.join(HERE, "out", NAME + ".mp4"), os.path.join(HERE, "out", NAME + "_preview"))


if __name__ == "__main__":
    main()
