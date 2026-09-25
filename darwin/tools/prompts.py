"""Codex（imagegen）に渡す画像プロンプトを【】ごとに書き出す。

  python tools/prompts.py 01-keiba   # → episodes/01-keiba/out/image_prompts.md
"""
import argparse
from pathlib import Path

from common import load_episode, out_dir


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    args = ap.parse_args()
    ep_dir, ep = load_episode(args.episode)
    blocks = ep["image_blocks"]
    md = [f"# {ep['title']} 画像プロンプト（Codex / imagegen 用）\n",
          "生成した画像は `images/<ファイル名>.png` として保存してください（縦 9:16）。\n",
          "顔の一貫性のため、まず 02_hakken を作り、気に入った1枚を他カットの参照画像にしてください。\n"]
    for s in ep["sections"]:
        prompt = " ".join([*(blocks[b] for b in s["image_uses"]), s["image_prompt"]])
        md += [f"\n## {s['label']} → `images/{s['id']}.png`\n",
               "\n".join(f"> （{l['emotion']}）{l['text']}" for l in s["lines"]) + "\n",
               f"```\n{prompt}\n```\n", f"Negative:\n```\n{blocks['NEGATIVE']}\n```\n"]
    dest = out_dir(ep_dir) / "image_prompts.md"
    dest.write_text("".join(md), encoding="utf-8")
    print(dest)


if __name__ == "__main__":
    main()
