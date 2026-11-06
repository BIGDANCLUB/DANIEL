"""大谷版の合成。新幹線版（../mach/compose_all.py）の仕組みを使い、文字と効果音だけ差し替える。
usage: python3 compose.py frames_root out.mp4 [bgm.mp3]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(HERE, "..", "mach"))
import timeline as TL  # noqa: E402
import compose_all as C  # noqa: E402
import overlay as O  # noqa: E402
from grade import grade  # noqa: E402
from PIL import Image  # noqa: E402

WHITE, OR = (255, 255, 255), O.ORANGE
C.REWIND_PREFIX = "o03"


def draw_shot(s, i, base, sun):
    g = grade(base, sun=tuple(sun)) if sun else grade(base, sun=(base.width / 2, -base.height * 0.4), glow=0.4, haze=0.15)
    g = g.resize((O.W, O.H), Image.LANCZOS).convert("RGBA")
    sec = i / TL.FPS
    O.watermark(g)
    if s.get("kind") == "open":
        count = 5 - int(sec)
        O.opening(g, [("もしも", WHITE), ("大谷翔平", OR), ("が", WHITE)], [("ホームランを年250本", OR), ("打ったら？", WHITE)],
                  count if count >= 1 else None, ["2025年は158試合で55本塁打。", "ナ・リーグMVP"], "MLBの公式記録より")
        return g
    gm, tag = TL.t_of(s, i)
    O.timer(g, "開幕から", (f"{max(1, int(gm)) if gm > 0 else 1}", "試合目"), tag[0],
            O.TAG_GREEN if tag[1] == "green" else O.TAG_ORANGE)
    O.speed(g, "ホームラン", "", f"{TL.hr(gm)}", "本")
    if s.get("note") and s["note"][0] <= sec < s["note"][1]:
        O.note(g, s["note"][2])
    for a, b, lines in s.get("captions", []):
        if a <= sec < b:
            O.caption(g, lines)
    if s.get("info"):
        title, rows = s["info"]
        O.info_box(g, title, [(ic, tx, col) for (at, ic, tx, col) in rows if sec >= at])
    return g


def build_audio(total, st):
    import numpy as np
    a = np.zeros(int(total * C.SR) + C.SR)

    def put(x, at, gain=1.0):
        i = int(at * C.SR)
        j = min(len(a), i + len(x))
        a[i:j] += gain * x[: j - i]

    def crack():   # バットの「カキーン」
        n = int(0.25 * C.SR)
        return (C.tone(0.25, 2200) * 0.5 + C.noise(0.25, 1) * 0.5) * C.env(n, 0.001, 0.04)

    for k in range(5):
        put(C.sfx_tick(), k + 0.05, 0.6)
    put(crack(), st["o02_swing"] + 0.4, 1.0)
    r = np.random.default_rng(3)
    for name in ("o03a_fly", "o03b_stands", "o03c_board", "o03d_last"):
        n = TL.shot(name)["frames"] / TL.FPS
        for _ in range(int(n * 8)):
            put(crack(), st[name] + r.uniform(0, n), 0.35)
        put(C.sfx_whoosh(n, True, 4), st[name], 0.5)       # 歓声の代わりのざわめき
    put(C.sfx_whoosh(0.7, False, 5), st["o05_rewind"], 0.8)
    put(crack(), st["o06_pergame"] + 0.2, 0.8)
    put(C.sfx_whoosh(4.0, True, 6), st["o08_rain"], 0.5)
    put(C.sfx_whoosh(4.0, True, 7), st["o12_fans"], 0.5)
    a = a / max(1e-6, abs(a).max()) * 0.8
    return a


C.draw_shot = draw_shot
C.build_audio = build_audio

if __name__ == "__main__":
    C.main()
