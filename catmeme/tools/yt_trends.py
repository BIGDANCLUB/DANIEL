"""猫ミームで時事ネタを扱うYouTubeチャンネルを集め、直近1週間に投稿された動画を再生数順に並べる。

必要: 環境変数 YOUTUBE_API_KEY（YouTube Data API v3 のキー。値は表示しない）
python3 catmeme/tools/yt_trends.py → catmeme/research/yt_trends_<日付>.md / .json

しくみ
1. 検索ワードで「猫ミーム × ニュース・時事」の動画とチャンネルを集める（直近30日）
2. チャンネルごとに登録者数と直近30日の動画の再生数を取り、上位30チャンネルを選ぶ
3. その30チャンネルが直近7日に投稿した動画を、再生数の多い順に並べる
   ※APIで取れるのは「投稿からの合計再生数」。直近7日に投稿された動画に絞ることで「直近1週間の再生数」に近い値にする
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.parse
import urllib.request

API = "https://www.googleapis.com/youtube/v3/"
KEY = os.environ.get("YOUTUBE_API_KEY")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "research")

QUERIES = ["猫ミーム ニュース", "猫ミーム 時事", "猫ミーム 解説", "猫ミーム 事件", "猫ミーム 炎上",
           "猫ミーム 政治", "猫ミーム 経済", "猫ミームで解説", "猫ミーム 速報", "猫マニ ニュース"]
CAT_WORDS = ("猫ミーム", "猫マニ", "#猫ミーム", "猫meme", "ねこミーム")
N_CHANNELS = 30


def get(path, **params):
    params["key"] = KEY
    url = API + path + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def chunks(xs, n=50):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def is_catmeme(title, desc=""):
    s = title + " " + desc
    return any(w in s for w in CAT_WORDS)


def video_stats(ids):
    out = {}
    for ch in chunks(list(ids)):
        for it in get("videos", part="snippet,statistics", id=",".join(ch)).get("items", []):
            out[it["id"]] = it
    return out


def main():
    if not KEY:
        sys.exit("YOUTUBE_API_KEY が設定されていません")
    now = dt.datetime.now(dt.timezone.utc)
    month_ago, week_ago = now - dt.timedelta(days=30), now - dt.timedelta(days=7)

    # 1. 候補の動画・チャンネルを集める
    vids = set()
    for q in QUERIES:
        token = None
        for _ in range(2):   # 1ワードにつき最大100件
            res = get("search", part="snippet", q=q, type="video", regionCode="JP", relevanceLanguage="ja",
                      publishedAfter=iso(month_ago), maxResults=50, order="viewCount",
                      **({"pageToken": token} if token else {}))
            for it in res.get("items", []):
                vids.add(it["id"]["videoId"])
            token = res.get("nextPageToken")
            if not token:
                break
    stats = video_stats(vids)

    # 2. チャンネルごとに、猫ミーム動画の直近30日の再生数を合計
    ch_views = {}
    for v in stats.values():
        sn = v["snippet"]
        if not is_catmeme(sn["title"], sn.get("description", "")):
            continue
        ch_views.setdefault(sn["channelId"], 0)
        ch_views[sn["channelId"]] += int(v["statistics"].get("viewCount", 0))
    chans = {}
    for ch in chunks(list(ch_views)):
        for it in get("channels", part="snippet,statistics,contentDetails", id=",".join(ch)).get("items", []):
            chans[it["id"]] = it
    def score(cid):
        subs = int(chans[cid]["statistics"].get("subscriberCount", 0) or 0)
        return ch_views[cid] + subs * 2
    top = sorted((c for c in ch_views if c in chans), key=score, reverse=True)[:N_CHANNELS]

    # 3. 上位チャンネルの直近7日の投稿
    recent = []
    for cid in top:
        uploads = chans[cid]["contentDetails"]["relatedPlaylists"]["uploads"]
        items = get("playlistItems", part="contentDetails", playlistId=uploads, maxResults=50).get("items", [])
        ids = [i["contentDetails"]["videoId"] for i in items
               if i["contentDetails"].get("videoPublishedAt", "") >= iso(week_ago)]
        for vid, v in video_stats(ids).items():
            recent.append({
                "title": v["snippet"]["title"],
                "channel": chans[cid]["snippet"]["title"],
                "published": v["snippet"]["publishedAt"][:10],
                "views": int(v["statistics"].get("viewCount", 0)),
                "url": "https://www.youtube.com/watch?v=" + vid,
            })
    recent.sort(key=lambda r: r["views"], reverse=True)

    # 書き出し
    os.makedirs(OUT, exist_ok=True)
    day = now.strftime("%Y%m%d")
    data = {"channels": [{"name": chans[c]["snippet"]["title"],
                          "subscribers": int(chans[c]["statistics"].get("subscriberCount", 0) or 0),
                          "catmeme_views_30d": ch_views[c],
                          "url": "https://www.youtube.com/channel/" + c} for c in top],
            "videos_7d": recent}
    with open(os.path.join(OUT, f"yt_trends_{day}.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    lines = [f"# 猫ミーム×時事チャンネル調査（{now:%Y-%m-%d}）", "", f"## 上位{len(top)}チャンネル", "",
             "| # | チャンネル | 登録者 | 猫ミーム動画の再生数（直近30日） |", "|---|---|---|---|"]
    for i, c in enumerate(data["channels"], 1):
        lines.append(f"| {i} | [{c['name']}]({c['url']}) | {c['subscribers']:,} | {c['catmeme_views_30d']:,} |")
    lines += ["", "## 直近7日に投稿された動画（再生数順）", "",
              "| # | 再生数 | タイトル | チャンネル | 投稿日 |", "|---|---|---|---|---|"]
    for i, r in enumerate(recent, 1):
        t = re.sub(r"\|", "／", r["title"])
        lines.append(f"| {i} | {r['views']:,} | [{t}]({r['url']}) | {r['channel']} | {r['published']} |")
    with open(os.path.join(OUT, f"yt_trends_{day}.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{len(top)} channels, {len(recent)} videos -> {OUT}")


if __name__ == "__main__":
    main()
