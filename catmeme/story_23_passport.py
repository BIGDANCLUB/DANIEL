"""23_passport（世界2位の“最強パスポート”　なのに日本人の5人に4人が持っていない？）。原稿 scripts/sungeki_passport.md（v1）。
「寸劇」シリーズ（README・story_style.py）。役名の札に小さい国旗。

python3 catmeme/story_23_passport.py          → out/23_passport_full.mp4
python3 catmeme/story_23_passport.py --audio  → 音だけ作り直す

原稿のルール（必ず守る）：
- 冒頭で「再構成したお話」。国どうしの会話は作り話。他の国をバカにしない（出てくるのは上位の国だけ）
- 順位は「2026年1月版」「7月版」と版を書く。7月版の日本の渡航先の数は未確認なので出さない
- パスポートを取らない理由は「と言われている」。数字は確認メモどおり
- 背景は ChatGPT で作ってもらう（scripts/23_passport_bg_prompts.md）。届くまでは STANDIN の仮の背景
"""
import os
import sys

import story_style as T

T.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "23_passport"))
T.FLAGS = True
T.STANDIN.update({"ph01_passports": "bg44_world_map", "ph02_ranking_board": "bg43_award_stage",
                  "ph03_empty_passport_office": "bg78_agency_office", "ph04_yen_coins": "bg87_refund_money",
                  "ph05_passport_counter": "bg20_counter", "ph06_departure_gate": "bg45_airport_arrival",
                  "ph07_world_map": "bg44_world_map", "ph08_sunset_plane": "bg57_tokyo_skyline",
                  "bg01_award_stage": "bg43_award_stage", "bg02_jp_office": "bg25_office_desk",
                  "bg03_rainbow_meadow": "st05_rainbow_meadow"})
BGM_DIR = os.path.join(T.HERE, "bgm")
JAZZ = {"file": os.path.join(BGM_DIR, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3"), "gain": -3}
LOFI = {"file": os.path.join(BGM_DIR, "星降る夜のホットココア.mp3"), "gain": -2}
BRIGHT = {"file": os.path.join(BGM_DIR, "未来を創る君たちへ.mp3"), "gain": -2}
SG, KR, JP, WORKER = "シンガポール", "韓国", "日本", "日本の会社員"
OUT = os.path.join(T.HERE, "out", "23_passport_full.mp4")
NOTE = "※世界の“パスポートの強さ”ランキングをもとに再構成したお話です"


def ph(name, text, **kw):
    n = len(text.replace("\n", ""))
    return T.photo(name, text, dur=kw.pop("dur", max(3.4, 1.4 + 0.11 * n)), **kw)


def stage(cats):
    return T.Scene("bg01_award_stage", [(SG, "L", cats[0]), (KR, "C", cats[1]), (JP, "R", cats[2])])


def cuts():
    # ---- 0. 出だし（数字ドン・10/21：黒い画面で始めない） ----
    cs = [
        T.hook("ph02_ranking_board", "世界2位", sub="日本のパスポートの強さは", color="yellow", rays=True, dur=2.8,
               bgm=JAZZ),
        T.hook("ph03_empty_passport_office", "約17.8%", sub="なのに、持っている人は", color="red", dur=3.0,
               se="doon_heavy", cat=("surprise_big_pupils_cat", "R")),
        T.full("ph01_passports", "パスポートの強さは、\nビザなしで行ける国や地域の数で比べられます。", dur=4.2),
        T.full("ph01_passports", "毎年発表される世界ランキングで、\n日本はずっと上位の常連です。", dur=3.8),
    ]
    # ---- 1. ランキング発表 ----
    cs += [
        ph("ph02_ranking_board", "2026年1月版。\n1位はシンガポール、192か所。"),
        ph("ph02_ranking_board", "2位は日本と韓国、188か所。"),
    ]
    a = stage(["showoff_gojo_cosplay_cat", "dance_trending_cat", "sleepy_sleepy_cat"])
    a.say("L", "今年も1位、いただきました")
    a.say("C", "日本、2位タイだって！\nやったね！", dur=2.6)
    a.say("R", "……あ、うん", dur=1.8)
    a.zoom("C", "テンション低っ！！", color="yellow", cat="huh_huh_cat")
    a.say("R", "いや……うちの国民、\nあんまり持ってないから……", cat="blank_black_cat_zoning_out", dur=3.0)
    a.zoom("L", "は？", color="white", cat="glare_disgusted_cat", dur=1.6)
    cs += a.cuts
    a2 = stage(["glare_disgusted_cat", "think_bike_front_seat_cat", "blank_black_cat_zoning_out"])
    a2.say("C", "持ってないって、どういうこと？", dur=2.4)
    a2.say("R", "そもそも、作ってない人が多くて……", dur=2.6)
    a2.say("L", "ビザなしで188か所も\n行けるのに？", dur=2.6)
    a2.say("R", "……行ける“だけ”で", cat="sleepy_sleepy_cat")
    a2.zoom("C", "宝の持ちぐされ！！", color="red", cat="huh_huh_cat")
    cs += a2.cuts
    # ---- 2. 5人に4人が持っていない ----
    cs += [
        ph("ph03_empty_passport_office", "日本で有効なパスポートを持っている人は、\n2025年末で約17.8％。（外務省の旅券統計から計算）"),
        ph("ph03_empty_passport_office", "5人のうち4人は、\n“今すぐ海外に行ける状態”ではないことになります。"),
    ]
    b = stage(["slack_nail_filing_cat", "surprise_big_pupils_cat", "blank_black_cat_zoning_out"])
    b.zoom("C", "世界2位の最強パスポートなのに！？", color="red", rays=True, cat="surprise_big_pupils_cat")
    b.say("L", "伝説の剣を持ってるのに、\n家の押し入れにしまってる勇者……", dur=3.2)
    b.say("R", "……返す言葉もない", cat="sad_banana_cat_cry")
    cs += b.cuts
    # ---- 3. 日本の会社員に聞いてみた ----
    c = T.Scene("bg02_jp_office", [(KR, "L", "think_bike_front_seat_cat"), (WORKER, "R", "sulk_hungry_cat")], bgm=LOFI)
    c.say("L", "なんでパスポート取らないの？", dur=2.6)
    c.say("R", "まず、休みが取れない……")
    c.say("R", "円安で、海外が高い……", add=True)
    c.say("R", "英語も、ちょっと不安……", add=True)
    c.say("R", "あと、パスポート代も高かった……", add=True, dur=2.6)
    cs += c.cuts
    cs.append(ph("ph04_yen_coins", "休みの取りにくさ、円安、言葉の不安。\nパスポートを持たない理由として、\nよく挙げられると言われています。",
                 dur=5.2))
    d = T.Scene("bg02_jp_office", [(KR, "L", "realize_wet_cat_stare"), (WORKER, "R", "sulk_hungry_cat")])
    d.zoom("L", ["わかる…", "でも…", "もったいない…"], pos="mid", cat="realize_wet_cat_stare")
    cs += d.cuts
    d2 = T.Scene("bg02_jp_office", [(KR, "L", "think_bike_front_seat_cat"), (WORKER, "R", "sulk_hungry_cat")])
    d2.say("L", "連休に、ちょっとだけでも？", dur=2.4)
    d2.say("R", "連休は、どこも高くて……", dur=2.4)
    d2.say("R", "それに、パスポートって\n申請がめんどうそうで……", add=True, dur=2.8)
    d2.say("L", "いまはオンラインでも\n申請できるよ", cat="work_typing_cat", dur=2.6)
    d2.zoom("R", "えっ、そうなの！？", color="white", cat="surprise_big_pupils_cat")
    cs += d2.cuts
    # ---- 4. 2026年7月、パスポートが安くなった ----
    cs += [
        T.intro("そして2026年7月——", 2.6),
        ph("ph05_passport_counter", "パスポートの手数料が下がりました。", bgm=JAZZ),
        ph("ph05_passport_counter", "18歳以上は10年用に一本化され、\n窓口の申請で16,300円 → 9,300円に。\nオンライン申請なら8,900円。", dur=5.4),
    ]
    e = T.Scene("bg02_jp_office", [(KR, "L", "happy_girlfriend_dance_cat"), (WORKER, "R", "excited_hodomoe_city_cat")])
    e.zoom("R", "7,000円も安くなった！？", color="red", rays=True, cat="excited_hodomoe_city_cat")
    e.say("L", "よかったじゃん！")
    cs += e.cuts
    cs.append(ph("ph06_departure_gate", "ただし同じ7月から、\n日本を出るときにかかる“出国税”が\n1,000円 → 3,000円に上がりました。", dur=5.0))
    f = T.Scene("bg02_jp_office", [(KR, "L", "work_typing_cat"), (WORKER, "R", "rage_talking_cat")])
    f.zoom("R", "……上がってるやつもある！！", color="yellow", cat="rage_talking_cat")
    f.say("L", "10年に1回の手数料が7,000円下がって、\n出国税は1回2,000円アップ……", dur=3.6)
    f.say("L", "年に1回くらいの旅行なら、\nまあトントン？", add=True, dur=3.0)
    f.say("R", "計算させないで……", cat="blank_black_cat_zoning_out")
    cs += f.cuts
    f2 = T.Scene("bg02_jp_office", [(KR, "L", "work_typing_cat"), (WORKER, "R", "think_bike_front_seat_cat")])
    f2.say("R", "18歳未満の子どもは？", dur=2.2)
    f2.say("L", "5年用で、\n窓口4,800円・オンライン4,400円", dur=3.0)
    f2.say("R", "家族で作るなら、\nだいぶ違うな……", dur=2.6)
    f2.zoom("R", ["……まずは", "自分の分から"], pos="mid", cat="realize_wet_cat_stare")
    cs += f2.cuts
    # ---- 5. 実は、少しずつ“弱く”なっている？ ----
    cs += [
        ph("ph07_world_map", "実は日本のビザなし渡航先は、\n前の年の193から188に減りました。（1月版）"),
        ph("ph07_world_map", "2026年7月版では、日本は韓国・UAEと並んで\n2位を保っています。"),
    ]
    g = stage(["showoff_gojo_cosplay_cat", "dance_trending_cat", "stare_big_eyes_tabby_kitten"])
    g.say("L", "持ってるうちに、使わなきゃ")
    g.say("C", "次は一緒に旅行しよ！")
    g.zoom("R", ["……持つか", "……パスポート"], pos="mid", cat="stare_big_eyes_tabby_kitten")
    cs += g.cuts
    # ---- 6. 締め ----
    cs += [
        ph("ph08_sunset_plane", "世界でも指折りの“強いパスポート”。", bgm=BRIGHT),
        ph("ph08_sunset_plane", "その力を使うかどうかは、\n引き出しの中から取り出す、\nほんの少しの勇気なのかもしれません。", dur=4.8),
    ]
    h = T.Scene("bg03_rainbow_meadow", [(SG, "L", "wave_waving_cat"), (JP, "C", "dance_trending_cat"),
                                        (WORKER, "R", "excited_hodomoe_city_cat")])
    h.say("R", "オンラインで申請してきた！")
    h.say("C", "えらい！", dur=1.6)
    h.say("L", "ようこそ、世界へ")
    h.ending("happy_girlfriend_dance_cat")
    cs += h.cuts
    return cs


if __name__ == "__main__":
    if sys.argv[1:] == ["--audio"]:
        T.remux(cuts(), OUT)
        sys.exit()
    T.run(cuts(), OUT, OUT.replace("_full.mp4", "_preview"))
