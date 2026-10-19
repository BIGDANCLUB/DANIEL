"""18_semicon【寸劇】AIブームの陰の主役「日本の素材がないと、半導体が作れない？」。原稿 scripts/sungeki_semicon.md（v1）。

python3 catmeme/story_18_semicon.py → out/18_semicon_full.mp4
「寸劇」シリーズ（README・story_style.py）。役名の札に小さい国旗。背景・写真は AI（backgrounds/18_semicon）。

原稿のルール（必ず守る）：
- 冒頭で「再構成したお話」。国どうし・会社どうしの会話は作り話
- 実在の人・実在の会社の人を猫で演じない。役は国（アメリカ・台湾・日本）と“架空の素材メーカーの人”。
  会社名は語り（photo）の事実の説明の中だけ
- 他の国をバカにしない。アメリカ・台湾は頼りにしてくれる仲間、日本は地味で謙虚な職人
- 「日本で9割」は「と言われることも」まで。「にゃ」禁止・単語の途中で改行しない
"""
import os

import story_style as T

T.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "18_semicon"))
T.FLAGS = True
BGM_DIR = os.path.join(T.HERE, "bgm")
LIGHT = {"file": os.path.join(BGM_DIR, "nc102462_Cat_life.mp3"), "gain": -1}
BRIGHT = {"file": os.path.join(BGM_DIR, "未来を創る君たちへ.mp3"), "gain": -2}
US, TW, JP = "アメリカ", "台湾", "日本"


def ph(name, text, **kw):
    """語り（黒い画面＋写真＋字幕）。長さは字幕の文字数から。"""
    n = len(text.replace("\n", ""))
    return T.photo(name, text, dur=kw.pop("dur", max(3.4, 1.4 + 0.11 * n)), **kw)


def cuts():
    cs = [
        # ---- 0. 冒頭 ----
        T.intro("これは、半導体をめぐる国と企業の関係を", 3.2),
        T.intro("もとに再構成したお話です。", 3.0),
        ph("ph01_smartphone_ai", "スマホにも、AIにも欠かせない“半導体”。"),
        ph("ph01_smartphone_ai", "その“材料”の多くが日本から届いていることは、\nあまり知られていません。"),
    ]
    # ---- 1. アメリカ「AIチップ、今すぐ！」 ----
    a = T.Scene("bg01_us_ai_office", [(US, "L", "dance_edm_cat"), (TW, "R", "work_typing_cat")], bgm=LIGHT)
    a.say("L", "AIチップ、あと10万個！！")
    a.say("L", "いや20万個！！", add=True)
    a.say("L", "今すぐ！！", add=True)
    a.say("R", "作れるよ。材料さえ届けばね")
    a.zoom("L", "材料？そんなのどこでも買えるでしょ", color="white", cat="cocky_dj_cat")
    a.say("R", "……それが、そうでもないんだよね", cat="slack_nail_filing_cat")
    a.say("L", "え？", cat="huh_huh_cat")
    cs += a.cuts
    # ---- 2. 半導体って、何でできてる？ ----
    cs += [
        ph("ph02_wafer_closeup", "半導体は、薄い“シリコンの板”に\n細かい回路を焼きつけて作ります。"),
        ph("ph02_wafer_closeup", "その板＝シリコンウエハーや、\n回路を描くための“感光材（フォトレジスト）”。"),
        ph("ph03_chemical_plant", "こうした材料の多くを、\n日本のメーカーが作っています。"),
    ]
    # ---- 3. 台湾の工場に、いつもの人が来る ----
    b = T.Scene("bg02_cleanroom", [(TW, "L", "work_typing_cat"), (JP, "R", "talk_orange_white_sitting_cat")])
    b.say("R", "おつかれさまです。\n今月の“いつものやつ”、お届けにあがりました", dur=3.6)
    b.zoom("L", "助かる〜〜！！", color="yellow", cat="happy_chipi_chapa_cat")
    b.say("L", "これがないと、\nうちのライン全部止まるからね", cat="work_typing_cat")
    b.say("R", "いえいえ、ただの化学メーカーですので", cat="sleepy_old_memories_cat")
    b.enter(US, "C", "glare_disgusted_cat")   # アメリカが入ってくる → 役名が3つになる
    b.say("C", "台湾、チップまだ？\n……って、誰その地味な人", dur=3.2)
    b.say("L", "この人がいないと、\n世界のチップが作れない人", cat="stare_interviewer_cat", dur=3.0)
    b.zoom("C", "え！？", color="yellow", cat="surprise_big_pupils_cat", dur=1.6)
    b.say("R", "いえいえ、とんでもない……", cat="meow_gray_white_kitten")
    cs += b.cuts
    # ---- 4. 日本の“地味な”正体 ----
    cs += [
        T.intro("その日本の会社とは——", 2.8),
        ph("ph04_japan_factory_town", "半導体の土台になる“シリコンウエハー”は、\n日本の信越化学工業とSUMCOの2社で、\n"
                                      "世界の過半を作っていると報じられています。", bgm=dict(LIGHT, **{"from": 40})),
        ph("ph04_japan_factory_town", "回路を描く“フォトレジスト”でも、\n東京応化工業やJSRなど日本の会社が上位に並びます。"),
        ph("ph04_japan_factory_town", "“日本の会社で世界の9割”と言われることも。"),
    ]
    c = T.Scene("bg03_jp_material_plant", [(US, "L", "glare_disgusted_cat"), (TW, "C", "stare_interviewer_cat"),
                                           (JP, "R", "talk_orange_white_sitting_cat")])
    c.say("R", "うちは、昔から同じものを、\nちょっとずつ良くしてきただけで……", dur=3.4)
    c.zoom("L", ["な、なんだと…", "地味なのに…", "世界の首根っこを…"], pos="mid", cat="realize_wet_cat_stare")
    c.say("C", "AIの主役はチップ。\nでも、チップの主役は材料なのよ", dur=3.2)
    c.zoom("L", "最先端って、そういうことなの！？", color="yellow", cat="huh_goat_talks_to_huh_cat")
    c.say("R", "よく言われます。“地味ですね”って", cat="sleepy_old_memories_cat")
    c.zoom("C", "それがいちばん強いのよ！！", color="red", rays=True, cat="angry_cat_hits_cat")
    cs += c.cuts
    # ---- 5. なぜ日本は強い？ ----
    cs += [
        ph("ph05_cleanroom_workers", "材料に求められるのは、\nとてつもない“純度”と“同じ品質”。"),
        ph("ph05_cleanroom_workers", "何十年も、同じものを、少しずつ良くし続けてきたこと。\n"
                                     "それが、簡単にはまねできない強みになっている、と言われています。", dur=5.6),
    ]
    d = T.Scene("bg03_jp_material_plant", [(US, "L", "cocky_dj_cat"), (TW, "C", "slack_nail_filing_cat"),
                                           (JP, "R", "talk_orange_white_sitting_cat")])
    d.say("L", "じゃあ、レシピ教えてよ")
    d.say("R", "……それはちょっと", cat="blank_black_cat_zoning_out")
    d.say("L", "ケチ！！", cat="rage_talking_cat")
    d.say("C", "何十年分の“ちょっとずつ”は、\nレシピだけじゃまねできないのよ", dur=3.4)
    d.zoom("R", "……（にっこり）", pos="mid", cat="joy_happy_happy_happy_cat", dur=2.4)
    cs += d.cuts
    # ---- 6. 工場ごと、日本へ ----
    cs += [
        T.intro("そして2026年——", 2.6),
        ph("ph06_kumamoto_fields", "台湾の半導体大手TSMCは、熊本の第2工場で\n最先端の“3ナノ”の半導体を作る方針を発表しました。",
           bgm=BRIGHT),
        ph("ph06_kumamoto_fields", "政府は「世界最先端の工場が日本にあることは、\n経済安全保障の面で大きな意義がある」としています。",
           dur=5.2),
    ]
    e = T.Scene("bg04_kumamoto_factory", [(TW, "L", "dance_trending_cat"), (JP, "C", "talk_orange_white_sitting_cat"),
                                          (US, "R", "glare_disgusted_cat")])
    e.say("L", "材料が近くにあるなら、\n工場ごと来ちゃえばいいじゃない", dur=3.2)
    e.zoom("C", "え、来るんですか！？", color="white", cat="surprise_big_pupils_cat")
    e.say("L", "来た", cat="cocky_dj_cat", dur=1.6)
    e.say("R", "ずるい！！　うちにも工場ちょうだい！！", cat="sad_banana_cat_cry", dur=2.8)
    e.say("C", "みなさん、仲良く使ってくださいね……", cat="talk_orange_white_sitting_cat")
    cs += e.cuts
    # ---- 7. 締め ----
    cs += [
        ph("ph07_sunset_factory", "派手なAIの陰で、\n地味な材料を作り続けてきた日本の会社。"),
        ph("ph07_sunset_factory", "世界の最先端は、案外“いつものやつ”に\n支えられているのかもしれません。", dur=4.6),
    ]
    f = T.Scene("st05_rainbow_meadow", [(US, "L", "wave_waving_cat"), (TW, "C", "calmdown_dancing_cat"),
                                        (JP, "R", "meow_gray_white_kitten")])
    f.say("L", "来月も“いつものやつ”、よろしく！！", dur=2.8)
    f.say("R", "……はい。いつも通り、お届けします", dur=2.8)
    f.say("C", "それが一番ありがたいのよ", dur=2.6)
    f.ending("happy_girlfriend_dance_cat")
    cs += f.cuts
    return cs


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["--audio"]:
        T.remux(cuts(), os.path.join(T.HERE, "out", "18_semicon_full.mp4"))
        sys.exit()
    T.run(cuts(), os.path.join(T.HERE, "out", "18_semicon_full.mp4"), os.path.join(T.HERE, "out", "18_semicon_preview"))
