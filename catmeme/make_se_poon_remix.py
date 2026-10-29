"""プロフェッショナルの「ポーン」を刻んで連打する「まね」SE を3種類つくる（10/28 ユーザー指定・コナンのまね音と同じ作り）。

python3 catmeme/make_se_poon_remix.py → se/tv_professional_poon_remix_a.mp3 / _b.mp3 / _c.mp3
- 元の音：se/tv_professional_poon.mp3。「ポ」は鳴り始めを短く切ったもの、最後の「ポーン」はのばして消えていく
- a：ポポポポーン
- b：ポポ、ポ、ポーン
- c：ポ、ポポポ、ポ、ポーン
"""
import os

import numpy as np

import render as R
from make_se_conan_remix import piece

SR = R.SR
SRC = os.path.join(R.SE_DIR, "tv_professional_poon.mp3")
ON = 0.68   # 「ポーン」の鳴り始め（秒）
PO, QUICK, PAUSE, LONG = 0.072, 0.028, 0.136, 5.7   # 「ポ」の長さ、続けて打つときのすき間、「、」の間、最後の「ポーン」（10/28 ユーザー指定：20%速く。10/29：最後のポーンは単発と同じ長さまで自然にのばす）


def build(src, rhythm):
    """rhythm：「ポポ、ポ、ポーン」のような文字。ポ＝短く1発、、＝間をあける、ー＝最後をのばす。"""
    out = []
    hits = rhythm.replace("ン", "")
    for k, ch in enumerate(hits):
        if ch == "、":
            out.append(np.zeros((int(PAUSE * SR), 2), np.float32))
        elif ch == "ポ":
            last = hits[k + 1:k + 2] == "ー"
            a = piece(src, LONG if last else PO, at=ON)
            if last:   # 元の音の終わりまでそのまま響かせる（単発のポーンと同じ）。最後だけ小さく消す
                fo = int(0.3 * SR)
                a[-fo:] *= np.linspace(1, 0, fo)[:, None]
            out.append(a)
            if not last and hits[k + 1:k + 2] == "ポ":
                out.append(np.zeros((int(QUICK * SR), 2), np.float32))
    a = np.concatenate(out)
    return a / np.abs(a).max() * 0.9


PATTERNS = {"a": "ポポポポーン", "b": "ポポ、ポ、ポーン"}   # 10/29：c（ポ、ポポポ、ポ、ポーン）はボツ


def build_full(src, rhythm):
    """10/29 ユーザー指定「途中で切らないVer」（コナン連打と同じ）：ポのたびに元のポーンを最後まで鳴らして重ねる。間隔は今までと同じ。"""
    starts, t = [], 0.0
    hits = rhythm.replace("ン", "").replace("ー", "")
    for k, ch in enumerate(hits):
        if ch == "、":
            t += PAUSE
        elif ch == "ポ":
            starts.append(t)
            t += PO + (QUICK if hits[k + 1:k + 2] == "ポ" else 0)
    one = src[int(ON * SR):].copy()
    out = np.zeros((int((starts[-1] + len(one) / SR) * SR) + 10, 2), np.float32)
    for st in starts:
        i = int(st * SR)
        out[i:i + len(one)] += one
    return out / np.abs(out).max() * 0.9


if __name__ == "__main__":
    src = R.load_audio(SRC).astype(np.float32)
    for k, rhythm in PATTERNS.items():
        a = build_full(src, rhythm)   # 10/29：途中で切らない形に
        out = os.path.join(R.SE_DIR, f"tv_professional_poon_remix_{k}.mp3")
        raw = out + ".f32"
        a.astype(np.float32).tofile(raw)
        os.system(f'ffmpeg -v error -y -f f32le -ar {SR} -ac 2 -i "{raw}" -b:a 192k "{out}"')
        os.remove(raw)
        print(out, rhythm, f"{len(a) / SR:.2f}秒")
