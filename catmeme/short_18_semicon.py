"""18本目（日本の素材と半導体・寸劇シリーズ）のショート。作りは short_17_imamori.py と同じ。60秒ちょうど。

python3 catmeme/short_18_semicon.py → out/short_18_semicon.mp4
- 役は国（アメリカ・台湾・日本の“架空の素材メーカーの人”）。役名の左に小さい国旗。会話は作り話
- 会社名・数字は語り（写真の場面）の中だけ。「日本で9割」は「と言われることも」まで
- 他の国をバカにしない。「寸劇」とは書かない（10/20）
- 画面の下と右端には猫・役名・写真を置かない（short_refstyle の SAFE_BOTTOM）
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M

HERE = M.HERE
NAME = "short_18_semicon"
TITLE = ("実はAIブームの陰の主役", "日本の“素材”", M.WHITE, M.YELLOW, M.RED)
C = M.C
LIGHT = os.path.join(S.BGM, "nc102462_Cat_life.mp3")
M.BGS[:0] = [os.path.join(HERE, "backgrounds", d) for d in ("18_semicon", "18_story")]
OFFICE, CLEAN, PLANT, FIELD, MEADOW = ("bg01_us_ai_office", "bg02_cleanroom", "bg03_jp_material_plant", "bg04_kumamoto_factory",
                                       "st05_rainbow_meadow")
WHO = {"US": ("アメリカ", "us"), "TW": ("台湾", "tw"), "JP": ("日本", "jp")}


def say(bg, who, text, a, dur, size=96, se="pi", **kw):
    """しゃべる国の猫だけを真ん中に（役名＋国旗）。"""
    c = M.cut(bg, text, [(a, C, 1100, False)], dur, label=WHO[who][0], label_x=540, size=size, se=se, **kw)
    c["label_flag"] = WHO[who][1]
    return c


def photo_img(name, box=(900, 600)):
    from PIL import Image, ImageOps
    im = Image.open(M.bg_path(name)).convert("RGB")
    k = min(box[0] / im.width, box[1] / im.height)
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    return ImageOps.expand(im, border=10, fill=(255, 255, 255)).convert("RGBA")


def tell(name, text, dur, **kw):
    """語り：写真をセリフの下に枠つきで（猫なし）。画面の下の隠れるところには置かない。"""
    c = M.cut(MEADOW, text, [], dur, size=kw.pop("size", 86), se=kw.pop("se", "kon"), **kw)
    img = photo_img(name)
    c["img"], c["img_y"] = img, M.SAFE_BOTTOM - 10 - img.height / 2
    return c


def cuts():
    return [
        say(OFFICE, "US", "AIチップ\nあと*10万個*！！\n今すぐ！！", "dance_edm_cat", 2.6, bgm={"file": LIGHT, "gain": -2}),
        say(OFFICE, "TW", "作れるよ\n*材料さえ届けばね*", "work_typing_cat", 2.8),
        say(OFFICE, "US", "材料？\nそんなの\n*どこでも買える*でしょ", "cocky_dj_cat", 2.8),
        say(OFFICE, "TW", "……それが\n*そうでもない*んだよね", "slack_nail_filing_cat", 2.8),
        say(CLEAN, "JP", "今月の\n*“いつものやつ”*\nお届けにあがりました", "talk_orange_white_sitting_cat", 3.2),
        say(CLEAN, "TW", "*助かる〜〜！！*", "happy_chipi_chapa_cat", 2.2, size=110),
        say(CLEAN, "US", "……誰？\nその*地味な人*", "glare_disgusted_cat", 2.6),
        say(CLEAN, "TW", "この人がいないと\n*世界のチップが*\n*作れない*", "stare_interviewer_cat", 3.0),
        say(CLEAN, "US", "*え！？*", "surprise_big_pupils_cat", 1.8, size=130),
        tell("ph02_wafer_closeup", "シリコンウエハーは\n日本の2社で\n*世界の過半*（報道）", 3.4),
        tell("ph04_japan_factory_town", "回路を描く\n“フォトレジスト”も\n日本の会社が*上位*に", 3.2),
        tell("ph03_chemical_plant", "“日本で世界の9割”と\n*言われることも*", 3.0),
        say(PLANT, "JP", "昔から同じものを\n*ちょっとずつ*\n良くしてきただけで……", "sleepy_old_memories_cat", 3.2, size=90),
        say(PLANT, "US", "地味なのに……\n*世界の首根っこを*……", "realize_wet_cat_stare", 3.0),
        say(PLANT, "TW", "AIの主役はチップ\nでも\n*チップの主役は材料*", "stare_interviewer_cat", 3.2, size=90),
        tell("ph06_kumamoto_fields", "台湾のTSMCは\n熊本の第2工場で\n*最先端の3ナノ*を作る方針", 3.4),
        say(FIELD, "US", "*ずるい！！*\nうちにも工場ちょうだい！！", "sad_banana_cat_cry", 2.8, size=90),
        say(MEADOW, "JP", "……はい\n*いつも通り*\nお届けします", "meow_gray_white_kitten", 2.8),
        say(MEADOW, "JP", "※国どうしの会話は作り話です\n※会社名・数字は報道によるものです\n※背景・写真はAIで作っています",
            "meow_gray_white_kitten", 3.0, size=44, se="pinpon_notice"),
    ]


def main():
    cs = M.keep_going(cuts())
    title = M.title_band(*TITLE)
    for c in cs:
        c["draw"] = M.make_draw(c, title)
    print(f"{len(cs)} カット・{sum(R.cut_dur(c) for c in cs):.1f}秒")
    S.run(cs, title, os.path.join(HERE, "out", NAME + ".mp4"), os.path.join(HERE, "out", NAME + "_preview"))


if __name__ == "__main__":
    main()
