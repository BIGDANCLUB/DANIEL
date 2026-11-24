"""「忍者屋敷の作り方」の合成（共通の hcompose を使う）。左上の NINJA KIT、右上の ENEMY RADAR、白い輪、効果音。
usage: python3 compose.py frames_root out.mp4   → 59.9秒ちょうど"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import hcompose as HC  # noqa: E402
from htimeline import Timeline  # noqa: E402

T = Timeline(HERE)
LT, LE = T.LT, T.LE

BGM = os.path.join(HERE, "..", "..", "bgm", "howto_ninja.wav")
KIT_TITLE = "NINJA KIT"
KIT = [(LT(9), "どんでん返し"), (LT(13) + 0.5, "隠し梯子"), (LT(16), "隠し部屋"), (LT(23), "落とし穴"), (LT(28), "刀隠し"),
       (LT(32), "からくり窓"), (LT(34) + 0.9, "縄ばしご")]
SCOPE = "radar"
SCOPE_TITLE = "ENEMY RADAR"
ST_COL = {"侵入": (235, 40, 40), "苦戦": (255, 150, 20), "防衛": (40, 200, 90)}
ST_LEVEL = {"侵入": 2, "苦戦": 1, "防衛": 0}
STATUS = [(0.0, "防衛"), (LT(2), "侵入"), (LT(9), "防衛"), (LT(10), "苦戦"), (LT(15), "防衛"), (LT(19), "侵入"), (LT(23), "防衛"),
          (LT(24), "侵入"), (LT(28), "防衛"), (LT(29), "侵入"), (LT(32), "防衛"), (LT(33), "苦戦"), (LT(35) + 0.8, "防衛"), (LT(36), None)]
# 白い輪：(場面, 印, はじまり, おわり)（全体の秒）
RINGS = [("n02_donden", "hero", LT(8), LE(8) + 0.05), ("n03_ladder", "hero", LT(16), LE(16) + 0.1), ("n05_pit", "enemy", LT(22) + 0.1, LE(22) + 0.3),
         ("n06_katana", "katana", LT(27), LE(27)), ("n07_window", "pin", LT(30) + 0.6, LE(31)), ("n08_rope", "hero", LT(35), LE(35))]
OVER = [(l["start"], (T.lines[i + 1]["start"] if i + 1 < len(T.lines) else T.TOTAL), l["over"]) for i, l in enumerate(T.lines) if l.get("over")]
OVER += [(LT(18) + 0.45, LT(19) - 0.05, "3階建て")]


def sfx(put, TL):
    st = {n: t for n, t in TL.CUTS}
    # 1) 家がドドドッと建つ、屋根がドン、敵がドロンと現れて屋根へ
    put(HC.whoosh(0.9, 1), 0.1, 0.9)
    for k, ts in enumerate([0.12, 0.18, 0.2, 0.36, 0.55]):
        put(HC.thud(k, 60 + 8 * k), ts + 0.15, 0.8)
    put(HC.thud(9, 50, 0.9), 1.2, 1.0)
    put(HC.rumble(1.0, 10), 1.2, 0.5)
    for k in range(4):
        put(HC.whoosh(0.4, 20 + k), LT(2) - 0.55 + 0.12 * k, 0.5)
        put(HC.fwip(30 + k), LT(2) + 0.5 + 0.12 * k, 0.6)
    # 2) どんでん返し：軸の線がシュー、板がギーッと回る、ドンッ
    put(HC.swish(0.8, 40), st["n02_donden"] + 0.08 + 0.9, 0.5)
    put(HC.creak(41, 0.8), LT(6) + 0.1, 0.7)
    put(HC.creak(42, 0.4), LT(7) + 1.0, 0.9)
    put(HC.thud(43, 110, 0.3), LT(7) + 1.35, 0.6)
    for k in range(6):
        put(HC.clack(44 + k), LT(7) - 0.2 + 0.11 * k, 0.25)
    put(HC.ding(), LT(9), 0.8)
    # 3) 敵が回ってくる、天井の板がズズッ、梯子がガタン、登る、引き上げる、板が閉まる
    put(HC.creak(50, 0.4), LT(10) + 0.25, 0.8)
    for k in range(8):
        put(HC.clack(51 + k), LT(11) - 0.2 + 0.11 * k, 0.25)
    put(HC.swish(0.5, 60), LT(12) + 0.55, 0.6)
    put(HC.thud(61, 120, 0.3), LT(13) + 0.55, 0.8)
    put(HC.ding(), LT(13) + 0.5, 0.5)
    for k in range(5):
        put(HC.clack(62 + k), LT(14) + 0.1 + 0.16 * k, 0.4)
    put(HC.swish(0.4, 68), LT(14) + 1.1, 0.6)
    put(HC.thud(69, 140, 0.25), LT(15) + 0.45, 0.7)
    put(HC.ding(), LT(16), 0.8)
    # 4) 前の壁が沈み、屋根が飛ぶ、階ごとにピン
    put(HC.rumble(0.8, 70), LT(18) + 0.1, 0.8)
    put(HC.whoosh(0.7, 71), LT(18) + 0.15, 0.8)
    for k in range(3):
        put(HC.ding() * 0.6, LT(18) + 0.55 + 0.28 * k, 0.6)
    # 5) 忍び足、床板がバタン、ヒューッ、ドスン
    for k in range(10):
        put(HC.clack(80 + k) * 0.5, st["n05_pit"] + 0.2 + 0.32 * k, 0.25)
    put(HC.thud(91, 130, 0.3), LT(21) + 0.1, 0.9)
    put(HC.whoosh(0.7, 92), LT(21) + 0.15, 0.7)
    put(HC.thud(93, 55, 0.7), LT(22) + 0.1, 1.0)
    put(HC.ding(), LT(23), 0.8)
    # 6) 刀：床板がパカッ、ふとんがバサッ、刀がシャキン
    put(HC.clack(100), LT(27) + 0.1, 0.8)
    put(HC.whoosh(0.5, 101), LT(27) + 0.2, 0.7)
    put(HC.swish(0.4, 102), LT(27) + 0.45, 0.8)
    put(HC.ding() * 0.8, LT(27) + 0.5, 0.7)
    put(HC.thud(103, 60, 0.5), LT(28) - 0.1, 0.6)
    put(HC.ding(), LT(28), 0.8)
    # 7) 窓がガタガタ → かんぬきを抜くと、スーッと開いて、敵がドテッ
    for k in range(int((LT(32) + 0.2 - LT(29) - 0.7) / 0.14)):
        put(HC.clack(110 + k) * 0.6, LT(29) + 0.7 + 0.14 * k, 0.35)
    put(HC.swish(0.4, 150), LT(32) + 0.0, 0.6)
    put(HC.swish(0.5, 151), LT(32) + 0.25, 0.8)
    put(HC.thud(152, 60, 0.5), LT(32) + 0.6, 0.8)
    put(HC.ding(), LT(32), 0.8)
    # 8) 敵がどっと押し寄せる、縄ばしごがバサッ、スルスルッ
    put(HC.roar(2.0, 160), st["n08_rope"] + 0.1, 0.35)
    put(HC.whoosh(0.6, 161), LT(34) + 0.35, 0.8)
    put(HC.swish(0.6, 162), LT(35) + 0.05, 0.9)
    put(HC.thud(163, 80, 0.4), LT(35) + 0.6, 0.6)
    put(HC.ding(), LT(34) + 0.9, 0.8)
    # 9) 完成：歓声、ピン
    put(HC.whoosh(1.2, 170), st["n09_final"], 0.5)
    put(HC.cheer(3.0, 171), LT(38) - 0.1, 0.6)
    put(HC.ding(), LT(39) - 0.09, 0.9)


if __name__ == "__main__":
    HC.main(sys.modules[__name__], HERE)
