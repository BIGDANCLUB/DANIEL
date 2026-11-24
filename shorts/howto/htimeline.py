"""作り方シリーズ共通の時間割（忍者屋敷・核シェルター〜）。台本の scene 名とナレーションの時刻（voice/timing.json）から場面を切る。
場面の頭は、その場面の最初の句の 0.08秒前（最初の場面は 0秒）。59.9秒 × 30コマ = 1797コマ。"""
import json
import os

FPS = 30
TOTAL = 59.9
LEAD_CUT = 0.08


class Timeline:
    def __init__(self, folder):
        self.folder = folder
        self.lines = json.load(open(os.path.join(folder, "voice", "timing.json")))["lines"]
        cuts = []
        for L in self.lines:
            if not cuts or cuts[-1][0] != L["scene"]:
                cuts.append((L["scene"], 0.0 if not cuts else round(L["start"] - LEAD_CUT, 3)))
        self.CUTS = cuts
        self.FPS, self.TOTAL = FPS, TOTAL

    def frames(self):
        total = int(round(TOTAL * FPS))
        starts = [int(round(t * FPS)) for _, t in self.CUTS] + [total]
        return {n: (starts[i], starts[i + 1] - starts[i]) for i, (n, _) in enumerate(self.CUTS)}

    def LT(self, i):
        """i 行目のはじまり（全体の秒）。"""
        return self.lines[i]["start"]

    def LE(self, i):
        """i 行目のおわり（全体の秒）。"""
        return self.lines[i]["start"] + self.lines[i]["dur"]

    def scene(self, name):
        f0, nf = self.frames()[name]
        t0 = f0 / FPS
        lines = [dict(L, t=L["start"] - t0, t_end=L["start"] - t0 + L["dur"]) for L in self.lines]
        return dict(name=name, f0=f0, nf=nf, t0=t0, dur=nf / FPS, lines=lines)
