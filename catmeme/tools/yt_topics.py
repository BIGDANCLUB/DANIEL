"""yt_trends.py の結果をネタごとにまとめてランキングにする。

python catmeme/tools/yt_topics.py 20261004
  入力: research/yt_trends_<日付>.json と research/yt_topics_<日付>.json（タイトルを読んで手で付けたラベル）
  出力: research/yt_topics_<日付>.md

ネタは「ニュース」（同じ出来事）と「話題」（お金・会社員あるある など）を一緒に並べる。並び順は合計再生数。
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(HERE), "research")
TOP = 15         # ランキングに載せるネタの数
SHOW = 5         # 各ネタの内訳に載せる動画の数


def vid_of(url):
    return url.rsplit("=", 1)[1]


def title(v):
    return re.sub(r"\|", "／", v["title"])


def main():
    day = sys.argv[1]
    with open(os.path.join(RES, f"yt_trends_{day}.json"), encoding="utf-8") as f:
        data = json.load(f)
    with open(os.path.join(RES, f"yt_topics_{day}.json"), encoding="utf-8") as f:
        labels = json.load(f)
    by_id = {vid_of(v["url"]): v for v in data["videos_7d"]}

    rows = []
    for g in labels["topics"]:
        vs = sorted((by_id[i] for i in g["ids"] if i in by_id), key=lambda v: v["views"], reverse=True)
        if vs:
            rows.append((g, vs))
    rows.sort(key=lambda r: sum(v["views"] for v in r[1]), reverse=True)
    rows = rows[:TOP]

    lines = [f"# 猫ミーム×時事：ネタ別ランキング TOP{TOP}（{day[:4]}-{day[4:6]}-{day[6:]}）", "",
             f"元データ: `yt_trends_{day}.md`（上位30チャンネルが直近7日に投稿した {len(by_id)} 本）。"
             f"ネタの分け方はタイトルを読んで手で付けたもの（`yt_topics_{day}.json`）。"
             "「ニュース」は同じ出来事、「話題」はお金・会社員あるあるのような同じテーマ。", "",
             "| # | ネタ | 種類 | 合計再生数 | 本数 | チャンネル数 | いちばん見られた動画 |",
             "|---|---|---|---|---|---|---|"]
    for i, (g, vs) in enumerate(rows, 1):
        top = vs[0]
        lines.append(f"| {i} | {g['name']} | {g['kind']} | {sum(v['views'] for v in vs):,} | {len(vs)} | "
                     f"{len({v['channel'] for v in vs})} | [{title(top)}]({top['url']})（{top['views']:,}） |")
    lines += ["", "## 内訳（2本以上のネタ・再生数の多い順に最大5本）", ""]
    for i, (g, vs) in enumerate(rows, 1):
        if len(vs) < 2:
            continue
        lines += [f"### {i}. {g['name']}", ""]
        for v in vs[:SHOW]:
            lines.append(f"- {v['views']:,} — [{title(v)}]({v['url']})（{v['channel']}・{v['published']}）")
        if len(vs) > SHOW:
            lines.append(f"- ほか {len(vs) - SHOW} 本")
        lines.append("")

    # どのネタにも入らない動画はチャンネルのジャンルで集計
    used = {i for g in labels["topics"] for i in g["ids"]}
    genre_of = {c: g for g, cs in labels["channel_genres"].items() for c in cs}
    agg = {}
    for i, v in by_id.items():
        if i in used:
            continue
        a = agg.setdefault(genre_of.get(v["channel"], "その他（素材集・日常もの など）"), [0, 0])
        a[0] += v["views"]
        a[1] += 1
    lines += ["## ランキングの対象外（ネタに分けられない動画）", "",
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
