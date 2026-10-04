"""yt_trends.py の結果を「同じニュース」ごとにまとめてランキングにする。

python catmeme/tools/yt_topics.py 20261004
  入力: research/yt_trends_<日付>.json と research/yt_topics_<日付>.json（タイトルを読んで手で付けたラベル）
  出力: research/yt_topics_<日付>.md

並び順は「合計再生数」。同じネタを何チャンネルが扱ったかも出す（多いほど話題になっているネタ）。
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(HERE), "research")
TOP = 15


def vid_of(url):
    return url.rsplit("=", 1)[1]


def title(v):
    return re.sub(r"\|", "／", v["title"])


def groups_table(groups, by_id, heading, lines):
    rows = []
    for g in groups:
        vs = sorted((by_id[i] for i in g["ids"] if i in by_id), key=lambda v: v["views"], reverse=True)
        if vs:
            rows.append((g["name"], vs))
    rows.sort(key=lambda r: sum(v["views"] for v in r[1]), reverse=True)
    rows = rows[:TOP]
    lines += [heading, "", "| # | ネタ | 合計再生数 | 本数 | チャンネル数 | いちばん見られた動画 |", "|---|---|---|---|---|---|"]
    for i, (name, vs) in enumerate(rows, 1):
        chans = {v["channel"] for v in vs}
        top = vs[0]
        lines.append(f"| {i} | {name} | {sum(v['views'] for v in vs):,} | {len(vs)} | {len(chans)} | "
                     f"[{title(top)}]({top['url']})（{top['views']:,}） |")
    lines.append("")
    for name, vs in rows:
        if len(vs) < 2:
            continue
        lines += [f"### {name}", ""]
        for v in vs:
            lines.append(f"- {v['views']:,} — [{title(v)}]({v['url']})（{v['channel']}・{v['published']}）")
        lines.append("")


def main():
    day = sys.argv[1]
    with open(os.path.join(RES, f"yt_trends_{day}.json"), encoding="utf-8") as f:
        data = json.load(f)
    with open(os.path.join(RES, f"yt_topics_{day}.json"), encoding="utf-8") as f:
        labels = json.load(f)
    by_id = {vid_of(v["url"]): v for v in data["videos_7d"]}

    lines = [f"# 猫ミーム×時事：ネタ別ランキング（{day[:4]}-{day[4:6]}-{day[6:]}）", "",
             f"元データ: `yt_trends_{day}.md`（上位30チャンネルが直近7日に投稿した {len(by_id)} 本）。"
             "ネタの分け方はタイトルを読んで手で付けたもの（`yt_topics_" + day + ".json`）。", ""]
    groups_table(labels["news"], by_id, "## 同じニュースを扱った動画（合計再生数順）", lines)
    groups_table(labels["themes"], by_id, "## 特定のニュースではないが同じ話題（合計再生数順）", lines)

    # 残りはチャンネルのジャンルで集計
    used = {i for g in labels["news"] + labels["themes"] for i in g["ids"]}
    genre_of = {c: g for g, cs in labels["channel_genres"].items() for c in cs}
    agg = {}
    for i, v in by_id.items():
        if i in used:
            continue
        g = genre_of.get(v["channel"], "その他")
        a = agg.setdefault(g, [0, 0])
        a[0] += v["views"]
        a[1] += 1
    lines += ["## 時事ではない動画（チャンネルのジャンル別）", "",
              "| ジャンル | 合計再生数 | 本数 |", "|---|---|---|"]
    for g, (views, n) in sorted(agg.items(), key=lambda kv: kv[1][0], reverse=True):
        lines.append(f"| {g} | {views:,} | {n} |")

    out = os.path.join(RES, f"yt_topics_{day}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    missing = used - set(by_id)
    print(f"-> {out}" + (f"（見つからないID: {sorted(missing)}）" if missing else ""))


if __name__ == "__main__":
    main()
