# -*- coding: utf-8 -*-
"""ブリーフ(日本語) → 実プロンプト の合成層

日本語 → booru タグへの翻訳は Claude 側が担当し、その結果を prompt.json に落とす。
このモジュールは「画質層 / 安全層 / ユーザー層」を決まった順で積むだけ。
安全層は常時強制で、prompt.json からは外せない。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import config as C


def _clean(s: str) -> str:
    """重複タグを消して整形する (先勝ち)。"""
    seen, out = set(), []
    for tag in (t.strip() for t in s.replace("\n", ",").split(",")):
        if not tag:
            continue
        k = re.sub(r"\s+", " ", tag.lower())
        if k in seen:
            continue
        seen.add(k)
        out.append(re.sub(r"\s+", " ", tag))
    return ", ".join(out)


def compose(user_pos: str, user_neg: str = "") -> tuple[str, str]:
    """最終的な positive / negative を組み立てる。

    positive = 画質 + 安全(成人・rating:sensitive) + ユーザー
    negative = ユーザー + 汎用ネガ + ハードブロック(露骨表現・年齢)
    """
    positive = _clean(f"{C.QUALITY_POS}, {C.SAFETY_POS}, {user_pos}")
    negative = _clean(f"{user_neg}, {C.BASE_NEG}, {C.HARD_NEG}")
    return positive, negative


def load(work_dir: Path) -> dict:
    """works/NNN/prompt.json を読み、安全層を適用して返す。"""
    data = json.loads((work_dir / "prompt.json").read_text(encoding="utf-8"))
    pos, neg = compose(data.get("positive", ""), data.get("negative", ""))
    data["_positive"] = pos
    data["_negative"] = neg
    return data


def save(work_dir: Path, *, positive: str, negative: str = "",
         model: str = C.DEFAULT_MODEL, motion: str = C.DEFAULT_MOTION,
         seed: int | None = None, **extra) -> Path:
    work_dir.mkdir(parents=True, exist_ok=True)
    payload = {"positive": positive, "negative": negative,
               "model": model, "motion": motion, "seed": seed, **extra}
    p = work_dir / "prompt.json"
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


if __name__ == "__main__":
    p, n = compose("1girl, solo, silver hair, sailor uniform, classroom, sunset")
    print("POSITIVE:\n ", p, "\n\nNEGATIVE:\n ", n)
