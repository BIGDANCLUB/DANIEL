"""桃太郎版の合成。新幹線版（../mach/compose_all.py）の仕組みを使い、文字と効果音だけ差し替える。
usage: python3 compose.py frames_root out.mp4 [bgm.mp3]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(HERE, "..", "mach"))
import timeline as TL  # noqa: E402  （桃太郎の時間割。compose_all もこれを使う）
import compose_all as C  # noqa: E402
import overlay as O  # noqa: E402
from grade import grade  # noqa: E402
from PIL import Image  # noqa: E402

WHITE, OR = (255, 255, 255), O.ORANGE
C.REWIND_PREFIX = "m03"


def fmt_t(t, tag):
    lab = tag[0]
    if "億" in lab:
        return f"{t:.10f}"
    if "1000" in lab:
        return f"{t:.6f}"
    if "/" in lab:
        return f"{t:.3f}"
    return f"{t:.2f}"


def draw_shot(s, i, base, sun):
    g = grade(base, sun=tuple(sun)) if sun else grade(base, sun=(base.width / 2, -base.height * 0.4), glow=0.4, haze=0.15)
    g = g.resize((O.W, O.H), Image.LANCZOS).convert("RGBA")
    sec = i / TL.FPS
    O.watermark(g)
    if s.get("kind") == "open":
        count = 5 - int(sec)
        O.opening(g, [("もしも", WHITE), ("桃太郎", OR), ("が", WHITE)], [("光の速さ", OR), ("で鬼ヶ島に向かったら？", WHITE)],
                  count if count >= 1 else None, ["「桃太郎は、", "鬼ヶ島へ鬼退治に出かけました」"], "昔話『桃太郎』より")
        return g
    t, tag = TL.t_of(s, i)
    td = min(t, s["freeze"]) if s.get("freeze") else t
    O.timer(g, "出発から", (fmt_t(td, tag), "秒"), tag[0], O.TAG_GREEN if tag[1] == "green" else O.TAG_ORANGE,
            max_w=440 if s.get("info") else 850)     # 右上の箱と重ならないように
    O.speed(g, "鬼ヶ島まで", "", C.fmt_km(TL.remain_km(td)), "km")
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

    for k in range(5):
        put(C.sfx_tick(), k + 0.05, 0.6)
    put(C.sfx_whoosh(0.6, True, 1), st["m02_foot"] + 0.9, 0.7)
    put(C.sfx_boom(2.5, 2), st["m03a_vanish"] + 5 / 30, 1.0)
    put(C.sfx_whoosh(1.0, False, 3), st["m03a_vanish"] + 0.3, 0.5)
    put(C.sfx_whoosh(0.7, False, 4), st["m05_rewind"], 0.8)
    put(C.sfx_whoosh(4.0, True, 5), st["m06_run"], 0.5)
    put(C.sfx_crackle(4.4, 6), st["m07_fire"], 0.6)
    put(C.sfx_crackle(4.4, 7), st["m08_safe"], 0.35)
    put(C.sfx_whoosh(4.0, True, 8), st["m09_light"], 0.4)
    put(C.sfx_boom(3.0, 9), st["m10_sound"] + 0.2, 0.8)
    put(C.sfx_splash(3.5, 10), st["m11_sea"] + 0.3, 0.8)
    put(C.sfx_whoosh(3.0, False, 11), st["m12_clock"] + 0.5, 0.4)
    put(C.sfx_boom(2.0, 12), st["m13_oni"] + 1.5, 0.9)
    put(C.sfx_boom(2.5, 13), st["m14_club"] + 0.3, 0.8)
    a = a / max(1e-6, abs(a).max()) * 0.8
    return a


C.draw_shot = draw_shot
C.build_audio = build_audio

if __name__ == "__main__":
    C.main()
