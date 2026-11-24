"""「核シェルターの作り方」の合成（共通の hcompose を使う）。左上の SHELTER KIT、右上の放射線の計器、白い輪、効果音。
usage: python3 compose.py frames_root out.mp4   → 59.9秒ちょうど"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import hcompose as HC  # noqa: E402
from htimeline import Timeline  # noqa: E402

T = Timeline(HERE)
LT, LE = T.LT, T.LE

BGM = os.path.join(HERE, "..", "..", "bgm", "howto_shelter.wav")
KIT_TITLE = "SHELTER KIT"
KIT = [(LT(6) + 1.6, "鉄筋コンクリート"), (LT(8), "防爆扉"), (LT(13), "1mの土"), (LT(17), "曲がった入口"), (LT(23), "換気フィルター"),
       (LT(28) + 0.6, "水と食料"), (LT(29) + 0.8, "ベッドとトイレ")]
SCOPE = "gauge"
SCOPE_TITLE = "RADIATION"
ST_COL = {"危険": (235, 40, 40), "注意": (255, 170, 20), "安全": (40, 200, 90)}
ST_LEVEL = {"危険": 2, "注意": 1, "安全": 0}
STATUS = [(0.0, "安全"), (LT(4), "危険"), (LT(6) + 1.4, "注意"), (LT(8), "安全"), (LT(10), "注意"), (LT(11), "危険"), (LT(13), "安全"),
          (LT(15), "危険"), (LT(17), "安全"), (LT(19), "注意"), (LT(22), "安全"), (LT(24), "危険"), (LT(25) + 1.0, "注意"), (LT(27) + 0.8, "安全"),
          (LT(29), None)]
RINGS = [("s02_blast", "door", LT(8), LE(8) + 0.2), ("s03_soil", "hero", LT(11) + 0.2, LE(11)), ("s05_air", "filter", LT(21) + 0.2, LE(21) + 0.1),
         ("s05_air", "hero", LT(18) + 0.2, LE(18))]
OVER = [(l["start"], (T.lines[i + 1]["start"] if i + 1 < len(T.lines) else T.TOTAL), l["over"]) for i, l in enumerate(T.lines) if l.get("over")]


def sfx(put, TL):
    st = {n: t for n, t in TL.CUTS}
    # 1) 土をドバッと掘る、部屋がドスン、走る足音、ミサイルがゴーッ
    put(HC.whoosh(0.9, 1), 0.1, 0.9)
    put(HC.thud(2, 55, 0.8), LT(0) + 0.15, 1.0)
    put(HC.rumble(0.8, 3), LT(0) + 0.15, 0.7)
    put(HC.whoosh(0.6, 4), LT(1), 0.6)
    put(HC.thud(5, 45, 1.0), LT(1) + 0.42, 1.0)
    for k in range(10):
        put(HC.clack(10 + k) * 0.6, LT(1) + 0.4 + 0.12 * k, 0.3)
    put(HC.roar(2.2, 20), LT(3) + 0.2, 0.6)
    # 2) 閃光、ドーン、爆風、コンクリート、扉がガシャン、ドン
    put(HC.boom(30, 4.0), st["s02_blast"] + 0.1, 1.0)
    put(HC.roar(2.5, 31), LT(5) - 0.3, 0.9)
    put(HC.rumble(2.0, 32), LT(5) - 0.2, 0.9)
    put(HC.swish(0.8, 33), LT(6) + 0.5, 0.5)
    put(HC.thud(34, 70, 0.6), LT(6) + 1.3, 0.9)
    put(HC.ding(), LT(6) + 1.6, 0.6)
    put(HC.creak(35, 0.5), LT(7) + 0.6, 0.6)
    put(HC.thud(36, 90, 0.5), LT(7) + 1.1, 1.0)
    put(HC.clack(37), LT(7) + 1.1, 0.9)
    put(HC.boom(38, 1.2) * 0.6, LT(8) + 0.35, 0.8)
    put(HC.ding(), LT(8), 0.8)
    # 3) 灰が降る（シャラシャラ）、ガイガーカウンター、土がドスン
    put(HC.swish(2.2, 40), LT(9), 0.4)
    put(HC.ticks(LT(12) + 1.5 - LT(10), 18, 41), LT(10), 0.5)
    put(HC.whoosh(0.6, 42), LT(12) + 0.9, 0.7)
    put(HC.thud(43, 45, 1.0), LT(12) + 1.5, 1.0)
    put(HC.ticks(LE(13) - LT(12) - 1.6, 2, 44), LT(12) + 1.6, 0.4)
    put(HC.ding(), LT(13), 0.8)
    # 4) 放射線がまっすぐ（カリカリ）→ 通路を作りかえる ゴゴゴ → 静かに
    put(HC.ticks(LT(16) + 0.6 - LT(15), 22, 50), LT(15), 0.5)
    put(HC.rumble(0.9, 51), LT(16) + 0.6, 0.9)
    put(HC.ticks(LE(17) - LT(16) - 1.0, 2, 52), LT(16) + 1.0, 0.4)
    put(HC.ding(), LT(17), 0.8)
    # 5) ファンがブーン、空気がシュー
    put(HC.hum(LE(23) - LT(20) + 0.5, 110, 60), LT(20), 0.45)
    put(HC.swish(1.0, 61), LT(20) + 0.3, 0.5)
    put(HC.swish(1.0, 62), LT(22), 0.5)
    put(HC.ding(), LT(23), 0.8)
    # 6) 時計がチクタク、カレンダーがパラパラ、棚にポンポン
    for k in range(int((LT(28) - LT(25)) / 0.25)):
        put(HC.clack(70 + k) * 0.35, LT(25) + 0.25 * k, 0.3)
    for k in range(14):
        put(HC.fwip(90 + k), LT(26) + (LT(28) - LT(26)) * k / 14, 0.4)
    for k in range(20):
        put(HC.clack(110 + k), LT(28) + 0.1 + 0.04 * k, 0.35)
    put(HC.ding(), LT(28) + 0.6, 0.8)
    # 7) ベッドとトイレがポン、歓声、ピン
    put(HC.thud(130, 120, 0.3), LT(29) + 0.3, 0.6)
    put(HC.thud(131, 140, 0.3), LT(29) + 0.6, 0.6)
    put(HC.ding(), LT(29) + 0.8, 0.6)
    put(HC.cheer(2.8, 132), LT(30) - 0.1, 0.6)
    put(HC.ding(), LT(30) - 0.09, 0.9)


if __name__ == "__main__":
    HC.main(sys.modules[__name__], HERE)
