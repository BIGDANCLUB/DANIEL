"""コナンのひらめき音を細かく切って連打する「まね」SE を3種類つくる（10/28 ユーザー指定・参考 5-17／5-18／5-19）。

python3 catmeme/make_se_conan_remix.py → se/anime_conan_hirameki_remix_a.mp3 / _b.mp3 / _c.mp3 / _d.mp3
- 10/29：1発ずつ切らず、元のコナンの音を最後まで鳴らして重ねる（build_full）。d は5連打
- 元の音：se/anime_conan_hirameki_idea_realize_truth.mp3 の「キーン」の部分を切って使う
- a（5-17 まね）：刻む → 同じ高さで「キッキッキッ」と連打
- b（5-18 まね）：長短バラバラに刻む・ため → 速い連打 → 最後だけ低い音で落とす
- c（5-19 まね）：のばす → 機関銃のような超高速連打 → 低いところからもとの高さへしゃくって止める
- 低いゴーという音は参考どおり削る（350Hz より下を切る・10/29 ユーザー指摘で150→350）。音量は元のコナン音とそろえる
- 10/28 ユーザー指摘「連打のときに変な高音」：連打は「キ」のあとの部分を使い、高い音（2000Hz より上・1000Hz あたり）をおさえる。
  元より高くする刻みはやめ、連打を速くした（2回目の指摘）。4回目：速さは2回目に戻し、連打の数を減らした。
  10/29：連打の速さを参考動画の間隔（約0.12秒・速いところ約0.065秒）にそろえた
"""
import os

import numpy as np

import render as R

SR = R.SR
SRC = os.path.join(R.SE_DIR, "anime_conan_hirameki_idea_realize_truth.mp3")
HIT = 0.205   # 「キーン」の始まり（秒）
BODY = 0.30   # 「キーン」のあとの、のびている部分。連打はここを使う（始まりの「キ」をくり返すと耳につく高音になる・10/28）


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
    fi, fo = min(int(0.008 * SR), len(a) // 3), min(int(0.02 * SR), len(a) // 2)   # 切れ目のプチッという音を消す
    a[:fi] *= np.linspace(0, 1, fi)[:, None]
    a[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return a


def build(src, steps):
    """steps：(長さ, 半音 or (始め,終わり), 次までのすき間)。最後は少しのばしてフェード。"""
    out = []
    for k, (ln, st, gap) in enumerate(steps):
        g = st if isinstance(st, tuple) else None
        a = piece(src, ln, 0 if g else st, glide=g, at=HIT if k == 0 else BODY)   # 最初の1発だけ「キ」から
        out += [a, np.zeros((int(gap * SR), 2), np.float32)]
    a = np.concatenate(out)
    return a / np.abs(a).max() * 0.9


PATTERNS = {
    # 10/28 ユーザー指摘「まだ高い音がある」：元より高くする刻みはやめる。
    # 10/29 ユーザー指定「連打の速度は参考動画の速さ」：参考の音の間隔を測った値にそろえる
    #   5-17・5-18：1発ごとの間隔 約0.12秒（1秒に約8発）／5-19：速いところ 約0.065秒（1秒に約15発）
    # 10/29 ユーザー指摘「何か低い音が入っている」：低くした刻み・しゃくりをやめ、全部もとの高さにする
    # 5-17：2発 → ひと呼吸 → 同じ高さで連打
    "a": [(0.12, 0, 0.04), (0.10, 0, 0.40)]
         + [(0.095, 0, 0.03)] * 5 + [(0.26, 0, 0.0)],
    # 5-18：長短バラバラ → 連打 → 最後は長め
    "b": [(0.10, 0, 0.04), (0.06, 0, 0.02), (0.10, 0, 0.36)]
         + [(0.09, 0, 0.03)] * 4 + [(0.16, 0, 0.07), (0.22, 0, 0.0)],
    # 5-19：のばす → 速い連打 → のばして止める
    "c": [(0.12, 0, 0.02), (0.22, 0, 0.06)] + [(0.045, 0, 0.02)] * 6
         + [(0.30, 0, 0.13), (0.16, 0, 0.03), (0.22, 0, 0.0)],
    # d（10/29 試し）：少しだけ間隔を短く（約0.10秒）8連打（ユーザー指定）
    "d": [(0.075, 0, 0.025)] * 8,
}


def build_full(src, steps):
    """10/29 ユーザー指定「途中で切らず流しきる」：刻むかわりに、同じ間隔で元のコナンの音を最後まで鳴らして重ねる。"""
    starts, t = [], 0.0
    for ln, _st, gap in steps:
        starts.append(t)
        t += ln + gap
    one = src[int(HIT * SR):].copy()
    out = np.zeros((int((starts[-1] + len(one) / SR) * SR) + 10, 2), np.float32)
    for st in starts:
        i = int(st * SR)
        out[i:i + len(one)] += one
    return out / np.abs(out).max() * 0.9


if __name__ == "__main__":
    src = R.load_audio(SRC).astype(np.float32)
    # 10/29 ユーザー指定「流しきるほうがいい」：a・b・c とも、刻まずに元の音を最後まで鳴らして重ねる形にする。d は試しの5連打
    jobs = [(k, build_full(src, steps)) for k, steps in PATTERNS.items()]
    for k, a in jobs:
        a[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))[:, None]
        out = os.path.join(R.SE_DIR, f"anime_conan_hirameki_remix_{k}.mp3")
        raw = out + ".f32"
        a.astype(np.float32).tofile(raw)
        os.system(f'ffmpeg -v error -y -f f32le -ar {SR} -ac 2 -i "{raw}" -af "highpass=f=350,highpass=f=350,lowpass=f=2000,lowpass=f=2000,equalizer=f=1000:t=q:w=1:g=-7,loudnorm=I=-14:TP=-1" -ar {SR} -b:a 192k "{out}"')
        os.remove(raw)
        print(out, f"{len(a) / SR:.2f}秒")
