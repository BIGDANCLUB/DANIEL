"""新チャンネル「ダメ人間の猫ミーム」のショートのひな形（参考マネの作り = short_refstyle.py と同じ見た目・動き）。

使い方：このファイルをコピーして short_dame_<話>.py を作り、TITLE と cuts() の中身（台本）だけ書き換える。
python3 catmeme/short_dame_template.py → out/short_dame_template.mp4

台本の書き方（1行＝1カット）
  cut(背景, "セリフ（*赤くしたい所*、\\n で改行）", [(猫ミーム, 横位置, 高さ, 左右反転), ...],
      秒数, label="役名", speaker=しゃべる猫の番号, se="効果音", col=文字色, size=文字の大きさ, shake=揺らすか)
  - 横位置は L（左）・Rr（右）・C（真ん中）。高さは 950〜1150 くらい
  - 同じ猫ミームが続くと、登場し直さずに続きから動く（位置が変わればすっと移動）
  - 背景はゆっくり動き続ける。素材の一覧は assets/CATALOG.md、効果音は se/、BGM は bgm/
  - ショートは 45〜58秒（足りない・長すぎると書き出しが止まる）
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M

HERE = M.HERE
NAME = "short_dame_template"
TITLE = ("ダメ人間", "給料日3日後の財布がヤバすぎる")   # 上の黒い帯（1行目は赤い大きな文字、2行目は黄色）
L, Rr, C = M.L, M.Rr, M.C
LIME, WHITE = M.LIME, M.WHITE
NORA = os.path.join(S.BGM, "野良猫は宇宙を目指した.mp3")
HOME = "bg14_home_night"
DAME = "ダメ人間"   # 足元に黄緑で出す役名


def cuts():
    """台本の見本（ここを書き換える）。"""
    return [
        M.cut(HOME, "給料日！！\n今月こそ貯金するぞ！", [("dance_maxwell_cat", C, 1100, False)], 2.6, se="jan", bgm={"file": NORA, "gain": -6}),
        M.cut(HOME, "とりあえず\n*ご褒美*に焼肉！", [("joy_happy_happy_happy_cat", L, 1000, False), ("eat_chips_cat", Rr, 700, True)], 2.6,
              label=DAME, se="pikon"),
        M.cut(HOME, "3日後…", [("sleep_sleeping_cat", C, 1000, False)], 1.8, size=180, se="tv_dokkiri_tettere"),
        M.cut(HOME, "残高 *1,280円*", [("surprise_big_pupils_cat", C, 1150, False)], 2.4, size=150, shake=True, se="explosion_chudoon"),
        M.cut(HOME, "は？", [("huh_huh_cat", C, 1150, False)], 1.8, size=230, se="question_hatena_maou"),
        # …（45〜58秒になるまで続ける）
    ]


def main():
    cs = M.keep_going(cuts())
    title = M.title_band(*TITLE)
    for c in cs:
        c["draw"] = M.make_draw(c, title)
    total = sum(R.cut_dur(c) for c in cs)
    check = os.environ.get("CHECK", "1") == "1"   # CHECK=0 で長さチェックなし（試し書き出し用）
    print(f"{len(cs)} カット・{total:.1f}秒")
    S.run(cs, title, os.path.join(HERE, "out", NAME + ".mp4"), os.path.join(HERE, "out", NAME + "_preview"), check=check)


if __name__ == "__main__":
    main()
