"""「もしも恋のドキドキが周りに聞こえるようになったら？」の時間割（30fps、約53秒）。台本は SCRIPT.md。
e は「聞こえだしてから」の経過秒。segs = [(コマ数, e0, e1)]。"""

FPS = 30
DAY = 86400
YEAR = 365 * DAY
T_VANISH = 5.6          # 聞こえだす瞬間（ほかの作品と同じ名前で使う）
H = 3600


def segs(*parts):
    return list(parts)


def at(e0, frames, dur):
    return segs((frames, e0, e0 + dur))


SHOTS = [
    dict(name="d00_open", frames=210, kind="open", t0=0.0, loc="東京・駅前の交差点（朝8時）"),
    dict(name="d01_burst", frames=120, segs=at(0.0, 120, 4.0), loc="同じ瞬間 ― 東京・駅前の交差点",
         captions=[(0.4, 4.0, "その朝、心臓の[音]が聞こえだした", ["世界中で、いっせいに", "※見えるように音の波をかいています"])]),
    dict(name="d02_train", frames=150, segs=at(30 * 60, 150, 5.0), card="30分後", loc="東京・満員電車",
         captions=[(1.0, 5.0, "好きになると[バレる]", ["1分に70回が120回へ", "となりの人に聞こえる"])]),
    dict(name="d03_distance", frames=135, segs=at(31 * 60, 135, 4.5), loc="東京・駅のホーム",
         captions=[(0.3, 4.5, "音は[はなれる]と小さくなる", ["きょりが2倍で", "音の強さは4分の1"])]),
    dict(name="d04_meeting", frames=150, segs=at(2 * H, 150, 300), card="2時間後", loc="東京・会社の会議室",
         captions=[(1.0, 5.0, "課長のポーカーフェイスが[通じない]", ["きんちょうも", "音でわかる"])]),
    dict(name="d05_bridge", frames=150, segs=at(2 * H + 600, 150, 300), loc="【実話】1974年 ― カナダ・キャピラノ渓谷", sepia=True,
         captions=[(0.4, 5.0, "ゆれる橋では[恋]と勘ちがい", ["女性に電話した男性は", "ゆれる橋で18人中9人、かたい橋で16人中2人"])]),
    dict(name="d06_coaster", frames=150, segs=at(14 * DAY + 3 * H, 150, 600), card="2週間後", loc="東京・遊園地",
         captions=[(1.0, 5.0, "デートは[ジェットコースター]が大人気", ["こわいドキドキを", "恋のドキドキと勘ちがいする"])]),
    dict(name="d07_library", frames=120, segs=at(30 * DAY + 5 * H, 120, 600), card="1か月後", loc="東京・図書館",
         captions=[(0.9, 4.0, "静かな場所が[うるさく]なった", ["100人の心臓の音が", "重なる"])]),
    dict(name="d08_home", frames=240, segs=at(YEAR + 21 * H, 240, 8.0), card="1年後", loc="東京・課長の家（夜9時）",
         captions=[(1.0, 4.4, "夫婦の心臓は[そろって]打つ", ["恋人どうしは心拍と呼吸がそろう、", "という研究がある（2012年 アメリカ）"]),
                   (4.4, 8.0, "ドキドキしなくても[となり]にいる", ["30年分の", "トクン、トクン"])]),
    dict(name="s99_end", frames=90, kind="end"),
]


def shot(name):
    return next(s for s in SHOTS if s["name"] == name)


def e_of(s, i):
    k = 0
    for n, a, b in s["segs"]:
        if i < k + n:
            return a + (b - a) * (i - k) / n, (b - a) / (n / FPS)
        k += n
    n, a, b = s["segs"][-1]
    return b, (b - a) / (n / FPS)


def total_frames():
    return sum(s["frames"] for s in SHOTS)


def start_of(name):
    k = 0
    for s in SHOTS:
        if s["name"] == name:
            return k / FPS
        k += s["frames"]
    raise KeyError(name)
