"""19_inawashiro（「見えたはず」か「見えなかった」か　猪苗代湖ボート事故、6年目の逆転有罪）のカット割り。
原稿 scripts/draft_inawashiro.md（v1）。作りは 10〜13本目と同じ。人が亡くなっている事故なので笑いは入れない。

python3 catmeme/cuts_19_inawashiro.py          → out/19_inawashiro_full.mp4
python3 catmeme/cuts_19_inawashiro.py --audio  → 音だけ作り直す

原稿のルール（必ず守る）：
- 亡くなった男の子・ご家族を笑いにしない。名前は出さない（「8歳の男の子」「ご両親」）。ご家族の言葉は報道の要旨だけ
- ボートを操縦していた人の名前・顔は出さない。「操縦していた男性（49）」まで。猫で演じない
- 事故を再現で演じない（図・地図・時系列のカードで説明する）
- 裁判官・検察・弁護側の言葉は報道の要旨だけ。ネットの声は架空の要約。「にゃ」禁止
- 落ち着いた猫・静かな効果音だけ（驚き・爆発・揺れ・集中線の演出はしない）
- 全動画共通：今日の一言・単語の途中で改行しない・最後はチャンネル登録の画面・過去の動画にはふれない
  （原稿の「11本目・13本目」の言及と「→ 〇本目もどうぞ」は、このルールに合わせて入れていない）
"""
import os
import sys

import cuts_04_leak as L
import render as R

HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("19_inawashiro", "17_imamori", "13_yard", "04_leak", "02_october", "01_todai")]
L.PT = os.path.join(HERE, "parts", "19_inawashiro")
R.PAN_DIRS = tuple(R.PAN_DIRS) + ("19_inawashiro",)
pt, cat, duo, dia, expl, chap, net = L.pt, L.cat, L.duo, L.dia, L.expl, L.chap, L.net
bg = L.bg
MIRAI, COCOA = L.MIRAI, L.COCOA
AM223 = os.path.join(L.BGM, "2_23_AM.mp3")
LETTER = os.path.join(L.BGM, "手紙のさよなら.mp3")

# 落ち着いた猫だけ（ふざけた動き・叫ぶ猫は入れない）
L.POOLS["quietN"] = ["sulk_hungry_cat", "sad_black_dog", "realize_wet_cat_stare", "blank_black_cat_zoning_out",
                     "sleepy_old_memories_cat", "think_bike_front_seat_cat", "stare_big_eyes_tabby_kitten", "sad_banana_cat_cry",
                     "despair_dramatic_kitten"]
L.POOLS["quietS"] = ["calm_black_face_sheep", "stare_interviewer_cat", "work_typing_cat", "talk_orange_white_sitting_cat",
                     "stand_real_sheep", "meow_gray_white_kitten", "calm_black_face_sheep"]
L.FALLBACK["quietN"] = ["quietS"]
L.FALLBACK["quietS"] = ["quietN"]
QN, QS = ("@quietN", "ニュース猫"), ("@quietS", "博識な猫")

COURT, COURTROOM, LAKE, SHORE, JACKET, CAL, SUNSET, FLOWERS, SWIM = (
    "bg104_supreme_court", "bg105_courtroom", "bg106_lake_calm", "bg107_lake_shore", "bg108_lifejacket", "bg109_calendar",
    "bg110_lake_sunset", "bg111_white_flowers", "bg112_swim_area")
QUIET, BOARD, SNS = "bg102_quiet_room", "bg03_blackboard", "bg09_sns"


def qn(say, b=QUIET, **kw):
    """ニュース猫（落ち着いた猫）がしゃべる。"""
    return duo(b, QN, QS, say, who="L", se=kw.pop("se", "pi"), **kw)


def qs(say, b=QUIET, **kw):
    """博識な猫（落ち着いた猫）がしゃべる。"""
    return duo(b, QN, QS, say, who="R", se=kw.pop("se", "kon"), **kw)


def sub(b, text, **kw):
    """【字幕】説明の字幕。猫は小さく1匹（落ち着いた猫）。"""
    return dict(bg=bg(b), sub=text, cats=[cat("@quietS", "博識な猫", 470, h=640)], se=kw.pop("se", "pi"), **kw)


def card(c, text, b=BOARD, **kw):
    return dia(c, text, b, right=QS, dur=kw.pop("dur", 5.0), se=kw.pop("se", "card_flip"), **kw)


def ex(b, text, **kw):
    """〔説明〕説明モード。"""
    return expl(b, [cat("@quietN", "ニュース猫", 500), cat("@quietS", "博識な猫", 1430)], "", text, dur=kw.pop("dur", 4.0),
                se=kw.pop("se", "pinpon_notice"), **kw)


def sep(text, **kw):
    """〔区切り〕黒い画面。"""
    return chap(text, se=kw.pop("se", "whoosh_shu"), dur=kw.pop("dur", 2.0), **kw)


def voice(say, **kw):
    return net("@quietN", say, se=kw.pop("se", "pi"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=5.2, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- 1. つかみ ----
        sub(COURT, "2026年10月16日\n最高裁判所", se="page_turn_01", bgm={"file": LETTER, "gain": -8}),
        sub(COURT, "「二審の無罪判決を\n破棄する」", dur=3.2),
        qn("……破棄？", COURT),
        sub(COURTROOM, "有罪 → 無罪 → そして　有罪", dur=3.2),
        sub(LAKE, "6年前の夏　湖で\n8歳の男の子が　亡くなった\n事故の裁判", dur=3.8),
        qn("6年……", LAKE),
        qs("“見えたはずだ”と\n“見えなかった”\nこの1点で", LAKE),
        qs("判決が2回\nひっくり返った", LAKE),
        dict(bg=bg(LAKE), card=pt("e01_title"), dur=4.0, se="kon"),
        # ---- 2. 何があったのか ----
        sep("2020年9月6日\n猪苗代湖", dur=2.4),
        card("e02_map", "福島県・猪苗代湖　会津若松市の中田浜の沖", LAKE),
        sub(SHORE, "午前11時ごろ"),
        sub(SHORE, "ライフジャケットを着て\n湖に浮かんでいた　4人", dur=3.4),
        sub(SHORE, "そこへ\nプレジャーボートが\n突っ込んだ", dur=3.2),
        sub(JACKET, "8歳の男の子が亡くなり\nお母さんは両足を切断\nほかにも1人が大けが", dur=4.4),
        qn("ライフジャケット\nちゃんと着てたのに……", JACKET),
        qs("浮いて遊んでたところに\n後ろから", JACKET),
        sub(COURTROOM, "ボートを操縦していたのは\n当時の会社役員の男性\n（いま49歳）", dur=3.8),
        sub(COURTROOM, "罪名は\n業務上過失致死傷", dur=3.0),
        qn("“前を見てなかった”\nってこと？", COURTROOM),
        qs("そこが\n6年争われたポイント", COURTROOM),
        # ---- 3. 裁判は2回ひっくり返った ----
        sep("有罪 → 無罪 → 有罪", bgm={"file": AM223, "gain": -6, "fade": 0.8}),
        card("e03_trial", "一審・福島地裁（2023年）は有罪\n禁錮2年の実刑", dur=4.6),
        card("e03_trial", "同乗者が撮った写真・動画に写る浮いているものは被害者\n約223メートル手前で見つけられたはず", dur=5.4),
        card("e03_trial", "二審・仙台高裁（2024年）は無罪", dur=4.0),
        card("e03_trial", "現場の再現は被告に不利な条件だった\n注意して見ていても　確実に見つけられたとは認めがたい", dur=5.6),
        card("e03_trial", "最高裁（2026年10月16日）は有罪\n一審の禁錮2年が確定へ", dur=4.6),
        card("e03_trial", "二審は一審の判断の組み立てを正しく読んでいない\n一審が不合理だと　具体的に示していない", dur=5.4),
        qn("223メートル手前で\n見えたはず　と\n確実には見えなかった　か……", COURTROOM),
        qs("同じ写真と\n同じ証拠を見て\n裁判所の答えが変わった", COURTROOM),
        ex(COURT, "「著しく正義に反する」\n＝最高裁が二審の判決を取り消すときに使う\n強い言葉", dur=4.6),
        qn("最高裁が\n“それはおかしい”って\nハッキリ言ったんだ", COURT),
        # ---- 4. 最高裁が動くまで ----
        sep("最高裁が動くまで"),
        sub(CAL, "2024年　二審の逆転無罪のあと\n検察が上告", dur=3.4),
        sub(CAL, "2026年9月18日\n最高裁が「弁論」を開く", dur=3.4),
        ex(COURT, "最高裁はふだん書類だけで判断する\nわざわざ「弁論」を開くのは\n二審の判決を見直すときが多い、と言われている", dur=5.0),
        qn("じゃあ　9月の時点で\n“もしかして”って……", COURT),
        qs("そう\nそして1か月後に\n逆転有罪", COURT),
        sub(COURT, "一審の禁錮2年の実刑が\n確定する", dur=3.2),
        # ---- 5. ご家族の6年 ----
        sep("ご家族の6年", bgm={"file": LETTER, "gain": -6, "fade": 0.8}),
        sub(FLOWERS, "判決のあと\nご両親が報道陣の取材に応じた", dur=3.4),
        sub(FLOWERS, "お父さん（報道の要旨）\n「逆転無罪があったので\n期待できないと思っていた」", dur=4.6),
        sub(FLOWERS, "「ようやく分かってくれる人が\n出てきてくれたことが\nありがたい」", dur=4.6),
        sub(FLOWERS, "「早く息子に\n会いに行きたい」", dur=4.0),
        dict(qn("……", FLOWERS, se=None), dur=3.0, no_pop=True),   # 無音で3秒（効果音なし）
        qs("一審で有罪　二審で無罪\n“どん底に落とされた”とも\n話していた", FLOWERS),
        qn("6年間　ずっと裁判で\n“見えたかどうか”を\n言い合ってたんだよね……", FLOWERS),
        sub(QUIET, "お母さんは\n両足を失った体で\n6年を過ごしてきた", dur=4.2),
        # ---- 6. 水の上の“見えない”危険 ----
        sep("水の上の“見えない”危険", bgm={"file": COCOA, "gain": -6, "fade": 0.8}),
        qs("車と違って\n水の上には\n信号も白線もない", LAKE),
        qs("ボートは前が持ち上がって\n前の低いところが\n見えにくくなる時がある", LAKE),
        qs("……と言われている", LAKE),
        card("e06_safety", "水辺で気をつけたいこと（一般的な注意）", SWIM, dur=5.6),
        qn("でも今回\nライフジャケットも\n着てたんだよ……", SWIM),
        qs("だから“守る側”だけじゃなく\n“操縦する側”の責任が\n問われた", SWIM),
        # ---- 7. ネットの声 ----
        sep("ネットの声", bgm={"file": MIRAI, "gain": -8, "fade": 0.8}),
        voice("最高裁\nよくひっくり返して\nくれた"),
        voice("二審の“見えなかった”で無罪は\nずっと納得できなかった"),
        voice("6年もかかったのが\n本当に苦しい"),
        voice("8歳の命で禁錮2年……\n重いのか軽いのか\n分からなくなる"),
        voice("子どもを持つ親として\n他人事じゃない"),
        voice("水の上のルール\nもっと厳しくしてほしい"),
        voice("ご両親が少しでも\n前に進めますように"),
        # ---- 8. まとめ ----
        dict(bg=bg(SUNSET), inset={"card": pt("e08_points"), "box": (200, 60, 1720, 860)}, dur=6.0,
             cats=[cat("@quietS", "博識な猫", 1750, h=380, bottom=1060, float=True)], se="kon"),
        qs("最後に司法が\n“著しく正義に反する”と\n言った", SUNSET),
        qn("6年は長すぎるけど……\nちゃんと届いた\nってことだよね", SUNSET),
        sub(SUNSET, "亡くなった男の子のご冥福を\n心よりお祈りします", dur=4.4, se=None),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "meow_gray_white_kitten", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


def cuts_full():
    cs = L.apply_fx(L.allocate(cuts_all(), max_use=6))   # 落ち着いた猫は数が少ないので6回まで
    for c in cs:   # 静かな動画：場所が変わる時のシュッという音は小さく
        se = c.get("se")
        if isinstance(se, list):
            c["se"] = [dict(s, gain=-16) if isinstance(s, dict) and s.get("f") == "whoosh_shu" else s for s in se]
    return cs


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "19_inawashiro_full.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cuts = cuts_full()
    if sys.argv[1:] == ["--audio"]:
        R.remux_audio(cuts, out, out.replace(".mp4", "_a.mp4"))
        os.replace(out.replace(".mp4", "_a.mp4"), out)
        sys.exit()
    if len(sys.argv) > 1:
        a, b = (int(x) if x else None for x in sys.argv[1].split(":"))
        cuts = cuts[a:b]
    R.render(cuts, out, preview_dir=out.replace(".mp4", "_preview"))
