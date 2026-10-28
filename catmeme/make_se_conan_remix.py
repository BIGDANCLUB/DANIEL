"""コナンのひらめき音を細かく切って連打する「まね」SE を3種類つくる（10/28 ユーザー指定・参考 5-17／5-18／5-19）。

python3 catmeme/make_se_conan_remix.py → se/anime_conan_hirameki_remix_a.mp3 / _b.mp3 / _c.mp3
- 元の音：se/anime_conan_hirameki_idea_realize_truth.mp3 の「キーン」の部分を切って使う
- a（5-17 まね）：音の高さを少しずつ上げながら刻む → 同じ高さで「キッキッキッ」と連打
- b（5-18 まね）：長短バラバラに刻む・ため → 速い連打 → 最後だけ低い音で落とす
- c（5-19 まね）：のばす → 機関銃のような超高速連打 → 上にしゃくり上げてブツッと止める
- 低いゴーという音は参考どおり削る（150Hz より下を切る）。音量は元のコナン音とそろえる
"""
import os

import numpy as np

import render as R

SR = R.SR
SRC = os.path.join(R.SE_DIR, "anime_conan_hirameki_idea_realize_truth.mp3")
HIT = 0.205   # 「キーン」の始まり（秒）


def piece(src, ln, st=0.0, glide=None, at=HIT):
    """元の音の at 秒から ln 秒ぶん。st 半音だけ高さを変える（glide=(始め, 終わり) なら途中でしゃくる）。"""
    if glide:
        r = 2 ** (np.linspace(glide[0], glide[1], int(ln * SR)) / 12)
    else:
        r = np.full(int(ln * SR), 2 ** (st / 12))
    pos = at * SR + np.cumsum(r)
    pos = pos[pos < len(src) - 2]
    i = pos.astype(int)
    f = (pos - i)[:, None]
    a = src[i] * (1 - f) + src[i + 1] * f
    fi, fo = min(int(0.004 * SR), len(a) // 2), min(int(0.012 * SR), len(a) // 2)
    a[:fi] *= np.linspace(0, 1, fi)[:, None]
    a[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return a


def build(src, steps):
    """steps：(長さ, 半音 or (始め,終わり), 次までのすき間)。最後は少しのばしてフェード。"""
    out = []
    for k, (ln, st, gap) in enumerate(steps):
        g = st if isinstance(st, tuple) else None
        a = piece(src, ln, 0 if g else st, glide=g)
        out += [a, np.zeros((int(gap * SR), 2), np.float32)]
    a = np.concatenate(out)
    return a / np.abs(a).max() * 0.9


PATTERNS = {
    # 5-17：上がっていくメロディ → 同じ高さで連打
    "a": [(0.13, 0, 0.03), (0.09, 2, 0.02), (0.13, 3, 0.03), (0.16, 2, 0.02), (0.16, 5, 0.03), (0.12, 3, 0.05),
          (0.11, 0, 0.04), (0.11, 0, 0.04), (0.11, 0, 0.08), (0.12, 0, 0.04), (0.08, 0, 0.03), (0.12, 0, 0.04),
          (0.30, 0, 0.0)],
    # 5-18：長短バラバラ → 速い連打 → 最後だけ低く落とす
    "b": [(0.12, 3, 0.05), (0.14, 3, 0.02), (0.24, 3, 0.04), (0.10, 2, 0.06), (0.24, 0, 0.03), (0.08, 3, 0.03),
          (0.08, 3, 0.03), (0.06, 0, 0.02), (0.06, 0, 0.02), (0.22, 0, 0.03), (0.16, -4, 0.04), (0.25, 0, 0.0)],
    # 5-19：のばす → 超高速連打 → しゃくり上げてブツッと止める
    "c": [(0.24, 0, 0.04), (0.12, 3, 0.03)] + [(0.035, s, 0.015) for s in (0, 5, 0, 5, 0, 5, 0, 5, 0)]
         + [(0.40, 0, 0.02), ((0.13), (0, 5), 0.03), (0.07, 7, 0.03), (0.26, 4, 0.0)],
}


if __name__ == "__main__":
    src = R.load_audio(SRC).astype(np.float32)
    for k, steps in PATTERNS.items():
        a = build(src, steps)
        a[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))[:, None]
        out = os.path.join(R.SE_DIR, f"anime_conan_hirameki_remix_{k}.mp3")
        raw = out + ".f32"
        a.astype(np.float32).tofile(raw)
        os.system(f'ffmpeg -v error -y -f f32le -ar {SR} -ac 2 -i "{raw}" -af "highpass=f=150,highpass=f=150,loudnorm=I=-14:TP=-1" -ar {SR} -b:a 192k "{out}"')
        os.remove(raw)
        print(out, f"{len(a) / SR:.2f}秒")
