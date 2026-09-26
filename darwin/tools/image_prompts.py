"""Codex（imagegen）に渡す画像プロンプトを【】ごとに書き出す。

  python tools/image_prompts.py 01-keiba   # → episodes/01-keiba/out/image_prompts.md

source が opus（図解）・reuse（既存クリップの使い回し）のショットと、start_from で続きから作るショットは画像不要。
"""
import argparse

from common import load_episode, out_dir

DEFAULT_HINT = "顔の一貫性のため、まず 02_hakken を作り、気に入った1枚を他カットの参照画像にしてください。"


def speed_note(s):
    if not s.get("speed"):
        return ""
    slow = [g for g in s["speed"] if g["rate"] != 1]
    parts = ", ".join(f"{g['from']:g}〜{g['to']:g}秒 {g['rate']:g}倍" for g in slow)
    return f"（生成 {s['gen_seconds']:g}秒 → {parts} → 再生 {s['duration']:g}秒）"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    args = ap.parse_args()
    ep_dir, ep = load_episode(args.episode)
    blocks = ep["image_blocks"]
    aspect = ep.get("format", {}).get("aspect", "9:16")
    orient = "横" if aspect == "16:9" else "縦"
    md = [f"# {ep['title']} 画像プロンプト（Codex / imagegen 用）\n",
          f"生成した画像は `images/<ファイル名>.png` として保存してください（{orient} {aspect}）。\n",
          f"{ep.get('image_hint', DEFAULT_HINT)}\n"]
    need = 0
    for s in ep["sections"]:
        head = f"\n## {s['part']} {s['label']}" if s.get("part") else f"\n## {s['label']}"
        src = s.get("source", "h3")
        if s.get("start_from"):
            md += [f"{head} → 画像不要（{s['start_from']} のクリップの続きから作る）\n"]
            continue
        if src == "opus":
            md += [f"{head} → 画像不要（図解・画面を Claude が作る）\n"]
            continue
        if src == "reuse":
            md += [f"{head} → 画像不要（{', '.join(r['clip'] for r in s['reuse'])} のクリップを使い回す）\n"]
            continue
        need += 1
        prompt = " ".join([*(blocks[b] for b in s["image_uses"]), s["image_prompt"]])
        md += [f"{head} → `images/{s['id']}.png` {speed_note(s)}\n",
               "\n".join(f"> （{l['emotion']}）{l['text']}" for l in s["lines"]) + "\n",
               f"```\n{prompt}\n```\n", f"Negative:\n```\n{blocks['NEGATIVE']}\n```\n"]
    md.insert(3, f"作る画像は {need} 枚です。\n")
    dest = out_dir(ep_dir) / "image_prompts.md"
    dest.write_text("".join(md), encoding="utf-8")
    print(f"{dest}（画像 {need} 枚）")


if __name__ == "__main__":
    main()
