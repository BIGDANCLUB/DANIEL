"""サラリーマンあるあるショートの部品（10/28）。作りは「定時で帰る日」「給料日の前と後」（world_short.py）と同じ。
赤い札に時刻や日付、白い字幕、白いふち取りの猫、役名の札。長さは 59.9 秒にそろえる。BGM なし。"""
import os

import world_short as Wd

OFF, OFF2, ROOM, NIGHT, MEET, CONBINI, TRAIN, IZAKAYA, PARK, CAFE = (
    "bg25_office_desk", "bg78_agency_office", "bg02_room", "bg14_home_night", "bg05_meeting", "bg15_convenience",
    "bg53_shinkansen", "bg13_izakaya", "bg59_sakura_park", "bg100_lounge_night")


def s(bg, tag, say, cat, d=2.5, **kw):
    kw.setdefault("tag_style", "time")
    return Wd.solo(bg, tag, say, cat, dur=d, **kw)


def t(bg, tag, say, left, right, who="R", ll=None, rl=None, d=2.5, **kw):
    kw.setdefault("tag_style", "time")
    return Wd.talk(bg, tag, say, left, right, who=who, llabel=ll, rlabel=rl, dur=d, **kw)


def run(name, top, sub, cs, band=None):
    cs = [c for c in cs if c]
    for c in cs:
        c["cats"] = [q for q in c["cats"] if q.get("a")]
    fixed = [c for c in cs if any(q["a"].startswith("scream_standing_marmot") for q in c["cats"])]   # マーモットは1回叫んだら次へ
    for c in fixed:
        c["dur"] = 1.3
    k = (59.9 - sum(c["dur"] for c in fixed)) / sum(c["dur"] for c in cs if c not in fixed)
    for c in cs:
        if c not in fixed:
            c["dur"] *= k
    band = band or Wd.rich_band([("{y}" + top, 130, Wd.BLACK, 300), ("{r}" + sub, 110, Wd.WHITE, 440)], *Wd.I.BAND)
    Wd.run(cs, band, os.path.join(Wd.HERE, "out", name + ".mp4"), os.path.join(Wd.HERE, "out", name + "_preview"))
