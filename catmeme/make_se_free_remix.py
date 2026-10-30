"""ショート用：版権の心配がない効果音で「!?」と「え…」の連打をつくる（10/30 ユーザー指定：コナン・ポーンは使わない）。

python3 catmeme/make_se_free_remix.py → se/free_bang_remix_a.mp3 / _b.mp3、se/free_doubt_remix_a.mp3 / _b.mp3
- 「!?」：shock_piano（ショック・ピアノ）。「え…」：question_hatena_maou（ハテナ？・魔王魂）
- コナン連打・ポーン連打と同じ作り（make_se_poon_remix.build_full）：打つたびに元の音を最後まで鳴らして重ねる。途中で切らない
- a：連打（ジャジャジャジャーン）、b：間をあけて（ジャジャ、ジャ、ジャーン）
"""
import os

import numpy as np

import render as R

SR = R.SR
SRCS = {"bang": "shock_piano", "doubt": "question_hatena_maou"}
PATTERNS = {"a": "ポポポポーン", "b": "ポポ、ポ、ポーン"}
PO, QUICK, PAUSE = 0.072, 0.028, 0.136   # ポーン連打と同じ間隔


def onset(src):
    """鳴り始め（いちばん大きい所の 1/10 をこえた最初の所）。"""
    env = np.abs(src).max(1)
    return int(np.argmax(env > env.max() * 0.1))


def build_full(src, rhythm):
    starts, t = [], 0.0
    hits = rhythm.replace("ン", "").replace("ー", "")
    for k, ch in enumerate(hits):
        if ch == "、":
            t += PAUSE
        elif ch == "ポ":
            starts.append(t)
            t += PO + (QUICK if hits[k + 1:k + 2] == "ポ" else 0)
    one = src[onset(src):].copy()
    out = np.zeros((int((starts[-1] + len(one) / SR) * SR) + 10, 2), np.float32)
    for st in starts:
        i = int(st * SR)
        out[i:i + len(one)] += one
    return out / np.abs(out).max() * 0.9


if __name__ == "__main__":
    for kind, name in SRCS.items():
        src = R.load_audio(os.path.join(R.SE_DIR, name + ".mp3")).astype(np.float32)
        for k, rhythm in PATTERNS.items():
            a = build_full(src, rhythm)
            out = os.path.join(R.SE_DIR, f"free_{kind}_remix_{k}.mp3")
            raw = out + ".f32"
            a.astype(np.float32).tofile(raw)
            os.system(f'ffmpeg -v error -y -f f32le -ar {SR} -ac 2 -i "{raw}" -b:a 192k "{out}"')
            os.remove(raw)
            print(out, rhythm, f"{len(a) / SR:.2f}秒")
