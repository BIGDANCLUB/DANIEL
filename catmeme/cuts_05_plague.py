"""05_plague（ロシアのペスト研究所）のカット割り。原稿 scripts/05_plague.md。作りは 04 と同じ（部品は cuts_04_leak を使い回す）。

python3 catmeme/cuts_05_plague.py          → out/05_plague_full.mp4
python3 catmeme/cuts_05_plague.py --audio  → 音だけ作り直す
python3 catmeme/cuts_05_plague.py 0:10     → 先頭10カットだけ

注意（指示書より）：亡くなった方は笑いにしない・名前を出さない・猫で演じない。「ペストは確認されていない（当局）」を必ず入れる。
"""
import os
import sys

import cuts_04_leak as L
import render as R

HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("05_plague", "04_leak", "03_kodomo_nisa", "02_october", "01_todai")]
L.PT = os.path.join(HERE, "parts", "05_plague")
# 新しい背景がないときは、これまでの背景で代用する（ユーザー判断 10/8：既存のイラストで作る）
STANDIN = {"bg27_lab": "bg18_backyard", "bg28_siberia_town": "bg11_tsukuba", "bg29_medieval": "bg10_kyoto",
           "bg30_airport": "bg20_counter"}
_bg = L.bg


def bg(n):
    try:
        return _bg(n)
    except FileNotFoundError:
        return _bg(STANDIN[n])


L.bg = bg
pt, cat, duo, solo, close, dia, expl, chap, net, nn, ss = L.pt, L.cat, L.duo, L.solo, L.close, L.dia, L.expl, L.chap, L.net, L.nn, L.ss
N, S = L.N, L.S
PURPLE, COCOA, MIRAI, KAMI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.KAMI, L.NORA


def two(b, sub, **kw):
    """2匹を並べて、上に説明の字幕（出来事の説明）。"""
    return dict(bg=bg(b), cats=[cat("@react", "ニュース猫", 500, h=700), cat("@calm", "博識な猫", 1430, h=700)], say=sub,
                text_top=True, **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=4.2, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- 1. つかみ ----
        dict(bg=bg("bg27_lab"), card=pt("e01_title"), dur=2.6, bgm={"file": PURPLE, "gain": -4}, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        chap("10月　シベリアで…"),
        dict(bg=bg("bg28_siberia_town"), sub="シベリアの「ペスト研究所」で\n28歳の職員が亡くなった",
             cats=[cat("@calm", "博識な猫", 470, h=640)], se="doon_movie"),
        dict(bg=bg("bg28_siberia_town"), sub="接触した約200人が\n隔離・観察に", cats=[cat("@calm", "博識な猫", 470, h=640)],
             se="pc_warning"),
        close("bg28_siberia_town", "@react", "ニュース猫", "ペストって……\nあの歴史の教科書の！？", se=["explosion_chudoon"]),
        ss("そう、あの", "bg28_siberia_town", se="kon"),
        nn("ちょっと待って\nパンデミック再び！？", "bg28_siberia_town", se="spring_byoin"),
        ss("落ち着け\n今わかってることを\n順番に見ていこう", "bg28_siberia_town", se="pikon"),
        expl("bg28_siberia_town", [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "",
             "先に結論：ロシア当局は\n「ペストは確認されていない」と発表", dur=3.4, se="pinpon_notice"),
        # ---- 2. 何が起きたか ----
        chap("何が起きたのか…", se="doon_heavy"),
        dia("e02_map", "ロシア・シベリアのイルクーツク州", right=S, dur=5.5, se="xylophone_transition"),
        ss("ペストの診断や対策のために\n菌を研究してる所な", "bg27_lab", se="page_turn_01"),
        dia("e03_timeline", "9月末に体調をくずし　10月2日に重い肺炎で亡くなった", right=S, se="card_flip"),
        dia("e03_timeline", "接触した人は　約90人→約200人に（現地の報道）", right=S, se="card_place"),
        two("bg28_siberia_town", "病院の一部を封鎖\n近くの工場はマスク着用を指示\n（現地の報道）", se="pi"),
        two("bg28_siberia_town", "現地メディアは\n「肺ペストに感染した可能性」と報道", se="doon_movie"),
        two("bg27_lab", "「菌の入った試験管を割った」\nと話していた、という報道も\n（確認されていない）", se="glass_break_01"),
        close("bg27_lab", "@react", "ニュース猫", "試験管割った！？\nそれ一番やばいやつ", se=["game_mgs_alert"]),
        ss("ただ　これは\n確認されてない話な", "bg27_lab", se="tsukkomi_bishi"),
        expl("bg27_lab", [cat("@react", "ニュース猫", 500), cat("@calm", "博識な猫", 1430)], "",
             "ロシアの衛生当局は\n「仕事に関係する菌は見つからなかった」\n死因は「原因不明の肺炎」と説明", dur=3.8,
             se="pinpon_notice"),
        two("bg05_meeting", "WHO（世界保健機関）にも\n「ペストの症例はない」と報告", se="page_turn_02"),
        two("bg05_meeting", "接触者からは\nコロナとかぜのウイルスが\n各2人だけ", se="pikon"),
        two("bg05_meeting", "約5,000件の検査でも\n危険な病原体は出ず\n隔離された人の約9割が解除", se="pinpoon_correct"),
        two("bg05_meeting", "当局は「職員はワクチンを\n接種していた」とも説明", se="page_turn_01"),
        nn("え、じゃあ結局\nペストじゃなかったの？", "bg02_room", se="question_hatena_maou"),
        ss("当局の発表ではそう\nただ本当の死因は\nまだはっきりしてない", se="hyoshigi_01"),
        dia("e04_vs", "報道と当局の発表が　食い違っている", right=S, dur=6.0, se="xylophone_transition"),
        nn("情報が二転三転しすぎて\nもうわからん", se="spring_byoin"),
        two("bg05_meeting", "ロシア大統領府の報道官\n「噂ではなく公式の情報を」\n（報道の要旨）", se="pi"),
        two("bg05_meeting", "アメリカ大統領「できる限り支援する」\n国務長官「注視しているが\n警戒すべき事態とは見ていない」", se="pi"),
        two("bg05_meeting", "WHOは　死因や病原体について\nさらに情報を求めている", se="page_turn_02"),
        two("bg05_meeting", "アメリカの感染症の専門家\n「今は“原因不明の肺炎”と\n呼ぶべき」（報道の要旨）", se="pi"),
        two("bg27_lab", "イギリスの専門家\n「本来の安全手順なら\n感染は防げたはず」（報道の要旨）", se="pi"),
        two("bg05_meeting", "「注意は必要だけど\nパニックになる段階ではない」\nという専門家の声も", se="pinpoon_note"),
        nn("専門家は\nわりと落ち着いてるのね", se="kon"),
        # ---- 3. そもそもペストって？ ----
        chap("そもそも「ペスト」って？", se="quiz_question_01", bgm={"file": NORA, "gain": -2}),
        dia("e05_plague", "細菌がおこす感染症　ネズミ→ノミ→人とうつる", right=S, se="page_turn_01"),
        nn("ネズミとノミ……", "bg02_room", se="boing_01"),
        dia("e06_types", "種類は3つ　人から人へうつるのは肺ペスト", right=S, se="card_flip"),
        dia("e05_plague", "早めに抗生物質で治療すれば　治る病気", right=S, se="pinpoon_correct"),
        nn("治るのか！\nちょっと安心した", se="pikon"),
        ss("だから\n“早く見つけて早く治療”\nが大事なんだ", se="idea_newtype_01"),
        chap("歴史の教科書の「黒死病」", se="bell_tower_goon"),
        dict(bg=bg("bg29_medieval"), sub="14世紀　ヨーロッパで\n大流行した「黒死病」", cats=[cat("@calm", "博識な猫", 470, h=640)],
             se="doon_movie"),
        dict(bg=bg("bg29_medieval"), sub="ヨーロッパの人口の\n3分の1〜半分が\n亡くなったとされる", cats=[cat("@calm", "博識な猫", 470, h=640)],
             se="doon_heavy"),
        close("bg29_medieval", "@react", "ニュース猫", "半分！？\nスケールがバグってる", se=["explosion_dokaan"],
              sting={"file": KAMI, "len": 4.0, "gain": -16}),
        ss("当時は\n抗生物質も\nなかったからな", "bg29_medieval", se="kon"),
        dia("e07_history", "実は今も　世界では毎年患者が出ている", right=S, se="page_turn_02"),
        dia("e07_history", "日本では　1926年を最後に　国内での発生はない", right=S, se="pinpoon_note"),
        nn("100年出てないのか", se="pikon"),
        two("bg28_siberia_town", "シベリアの草原には\nペスト菌を持つ野生動物がいる\n→ だから研究所がある", se="page_turn_01"),
        ss("つまり“ペスト研究所”は\nペストから人を守るための所な", "bg27_lab", se="tv_professional_poon"),
        # ---- 4. なぜ騒がれたか ----
        chap("なんでこんなに　騒がれた？", se="quiz_question_02", bgm={"file": COCOA, "gain": -2}),
        dia("e08_why", "「研究所」「隔離」「食い違う発表」がそろった", right=S, se="xylophone_transition"),
        nn("なんか……\nコロナの最初っぽい", se="question_hatena_maou"),
        ss("そう\nそれが一番の理由\nだと思う", se="kon"),
        two("bg02_room", "コロナのときも　最初は\n「原因不明の肺炎」と報じられた", se="page_turn_01"),
        two("bg09_sns", "噂が先に広まり\n公式発表があとから否定する形に", se="pi"),
        nn("噂のほうが\n足が速い", "bg09_sns", se="dash_super_fast"),
        chap("ネットでは　こんな声も…\n（どれも確認されていません）", se="whoosh_shu", dur=2.2),
        net("@react", "研究所から\n漏れたんじゃ", se="kon"),
        net("@react", "生物兵器では？", se="pi"),
        net("@react", "ロシアは\n隠してる", se="boing_01"),
        net("@react", "変異した\nペストかも", se="question_hatena_maou"),
        ss("どれも\n“という声”な\n根拠は出てない", se="hyoshigi_02"),
        # ---- 5. 日本への影響 ----
        chap("日本は大丈夫？", se="quiz_den"),
        nn("北海道から\n近くない？", "bg30_airport", se="question_hatena_maou"),
        dia("e02_map", "イルクーツクから札幌まで　直線で約2,900km", "bg30_airport", right=S, dur=5.0, se="card_flip"),
        two("bg30_airport", "今のところ\n日本への影響が出ている\nという報道はない", se="pinpoon_correct"),
        two("bg30_airport", "当局の発表では\nペストは検出されず\n接触者にも感染者なし", se="page_turn_01"),
        two("bg30_airport", "仮にペストでも\n抗生物質で治療できる", dur=4.0, se="pikon"),
        two("bg30_airport", "ペストは日本の「検疫感染症」\n空港や港の検疫所で\n入ってこないよう見張っている", se="page_turn_01"),
        ss("怖がりすぎず\n続報は公式の発表で\n確認な", "bg30_airport", se="tv_professional_poon"),
        nn("“まとめ”より\n“一次情報”ね", "bg30_airport", se="idea_newtype_01"),
        # ---- 6. ネットの声 ----
        chap("ネットの声", se="whoosh_shu", bgm={"file": MIRAI, "gain": -2, "fade": 0.8}),
        net("@react", "コロナの時も\n最初は\n“原因不明の肺炎”\nだったんよ", se="kon"),
        net("@react", "“公式情報を”\nって言われるほど\n噂を\n信じたくなる", se="silly"),
        net("@react", "抗生物質で\n治るって聞いて\n少し安心した", se="pikon"),
        net("@react", "教科書でしか\n見たことない単語が\nニュースに\n出てくるの怖い", se="boing_01"),
        net("@react", "シベリアから\n北海道まで\n何キロあると\n思ってんの", se="tsukkomi_bishi"),
        net("sleepy_old_memories_cat", "亡くなった\n職員さんが\n一番気の毒", se="chiin_01"),
        # ---- 7. まとめ ----
        dict(bg=bg("bg03_blackboard"), inset={"card": pt("e09_matome"), "box": (200, 60, 1720, 860)}, dur=5.0,
             cats=[cat("@react", "ニュース猫", 1750, h=380, bottom=1060, float=True)], se="chiin_01"),
        ss("わかってないことは\nわかってないって\n言うのが大事", dur=3.0, se="tv_professional_poon"),
        nn("続報が出たら\nまたやります", se="pikoon_retro"),
        dict(bg=bg("bg03_blackboard"), card=pt("e10_ending"), dur=3.0, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
    ]


def cuts_full():
    return L.apply_fx(L.allocate(cuts_all()))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "05_plague_full.mp4")
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
