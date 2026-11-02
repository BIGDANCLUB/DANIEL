"""「AとBで、かかるお金をくらべる」長尺の共通部品（11/1：タワマンvs一戸建て・東京vs地方・ひとり暮らしvs実家・ガソリンvsハイブリッド）。
作りは 26本目（車ありvs車なし）・34本目（車vs125cc）と同じ：いつもの2匹の掛け合い＋グラフ（重りが落ちて棒がのびる）＋演出。
約8分ぶんの原稿をテンポよく3分ほどに圧縮する（ユーザー指定）。

使い方（各台本で）:
    import compare_long as C
    C.setup("35_tower", STANDIN)
    C.charts({...})
    C.main("35_tower", cuts_all, ["c0", ...])
"""
import glob
import os
import sys

import cuts_04_leak as L
import cuts_26_kuruma as K
import render as R
import wide_bars as B

HERE = L.HERE
pt, cat, chap, fx, CONAN, POON = L.pt, L.cat, L.chap, K.fx, K.CONAN, K.POON
PURPLE, COCOA, MIRAI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.NORA
bg, nn, ss, boom, qq, g = K.bg, K.nn, K.ss, K.boom, K.qq, K.g
MONEY, BOARD = K.MONEY, K.BOARD
_bbg = B._bg


def _chart_bg(n):
    try:
        return _bbg(n)
    except FileNotFoundError:
        return _chart_bg(K.STANDIN[n])


def setup(name, standin, tempo=1.0):
    """背景フォルダ（届いた絵は backgrounds/<name> に置く）・代わりの背景・解説画面のフォルダ。"""
    R.TEMPO = getattr(R, "TEMPO", 1.0) * tempo
    L.BGS[:0] = [os.path.join(HERE, "backgrounds", name)]
    L.BGS += sorted(d for d in glob.glob(os.path.join(HERE, "backgrounds", "*")) if os.path.isdir(d) and d not in L.BGS)
    L.PT = os.path.join(HERE, "parts", name)
    K.STANDIN.update(standin)
    B._bg = _chart_bg


def charts(d, drop_b="pafu"):
    """グラフを登録。右の列（B）が落ちる音は気の抜けた軽い音、左の列はゲーム風の音（車の動画と同じ）。"""
    K.CHARTS.update(d)
    for k in d:
        K.DROP_SE[k] = {1: drop_b}
        K.STEP_SE.setdefault(k, K.GAME_STEP[:6] + ["game_mario_1up"])


def card(c, sub, **kw):
    return L.dia(c, sub, BOARD, right=("@calm", "博識な猫"), dur=kw.pop("dur", 4.4), se=kw.pop("se", "card_flip"), **kw)


def notice(b, cats):
    return dict(bg=bg(b), cats=[{"a": a_, "x": x_, "h": h_, "bottom": 1070, "mute": True} for a_, x_, h_ in cats],
                fx=["dim"], layers_top=[pt("e00_notice")], dur=6.0, no_pop=True, notice=True,
                se={"f": "chime_announce", "len": 3.0, "gain": -2})


def title(b, a1, a2):
    return dict(bg=bg(b), card=pt("e01_title"), dur=4.0, se="jan",
                cats=[{"a": a1, "x": 300, "h": 440, "bottom": 1050, "float": True},
                      {"a": a2, "x": 1640, "h": 400, "bottom": 1050, "float": True, "mute": True}])


def ending(b):
    return [dict(bg=bg(b), card=pt("e10_ending"), dur=3.6, se="chirin",
                 cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
            dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
                 cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}])]


def slot(b, pre, v, post):
    """金額がスロットのように回って止まる（博識な猫のアップ）。"""
    return fx(boom(None, b, who="S", se=["explosion_dokaan", {"f": "kaan", "at": 0.9}]), slot=(pre, v, post))


def hatena(b):
    """直前の画面が止まって白黒になり、左に傾いて大きな「？」が降りてくる（驚きの間・約1.55秒）。BGMは止めて専用の曲だけ。"""
    return dict(bg=bg(b), hatena=True, dur=1.55, dip=False, duck_bgm=-60, no_pop=True,
                se={"f": "hatena_mono_tilt", "gain": 4, "len": 1.6})


def main(name, cuts_all, chart_names):
    out = os.path.join(HERE, "out", name + "_full.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if sys.argv[1:] == ["--charts"]:
        for k in chart_names:
            print(B.make(k, K.CHARTS[k], force=True))
        return
    cuts = K.hype(L.apply_fx(L.allocate(cuts_all(), max_use=7, gap=1)))
    if sys.argv[1:] == ["--len"]:
        print(len(cuts), round(sum(R.cut_dur(c) for c in cuts), 1))
        return
    if len(sys.argv) > 1:
        a, b = (int(x) if x else None for x in sys.argv[1].split(":"))
        cuts = cuts[a:b]
    R.render(cuts, out, preview_dir=out.replace(".mp4", "_preview"))
