"""17_imamori（元戦隊ヒロイン・今森茉耶の経歴と、2026年10月のSNS騒動・発信休止）の解説画面。原稿 scripts/17_imamori.md。

python3 catmeme/make_parts_17_imamori.py → catmeme/parts/17_imamori/*.png（＋ preview/）
公式発表・週刊誌報道・本人のSNS投稿を分けて書く。妊娠の経緯や LINE の関係者は推測しない。
"""
import os

from PIL import Image

import parts as P
from make_parts_04_leak import table3

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "17_imamori")
PREV = os.path.join(OUT, "preview")

ITEMS = {
    "e00_notice": P.message(["※週刊誌の報道は「疑惑」で、確定した事実ではありません", "※本人や関係者への誹謗中傷・詮索はやめてください",
                             "※背景イラストはAIで作っています　※猫は演出です",
                             "※学芸会では効果音を口で鳴らす役でした"], opaque=True, size=56),   # 最後の行は今日の一言
    "e01_title": P.message(["元戦隊ヒロイン　今森茉耶", "再出発からわずか6日で発信休止"], sub="2026年10月8日 YouTube初投稿 → 10月14日 すべての発信を休止と表明", size=84),
    "e02_profile": table3("今森茉耶ってだれ？", ("", "内容", ""), [
        ("生まれ", "2006年3月26日　宮崎県出身", ""),
        ("中学生", "TikTokで活動", ""),
        ("2022年", "芸能事務所 seju と契約", ""),
        ("2023年", "グラビアデビュー", ("ミスマガジン2023 グランプリ", True)),
    ], widths=(220, 640), size=46),
    "e03_sentai": P.bullets("ナンバーワン戦隊ゴジュウジャー（2025年2月〜）", [
        "一河角乃／ゴジュウユニコーン役",
        "シリーズ初の　女性のブラック戦士",
        "放送開始時は18歳",
        "戦隊シリーズは　若手俳優の登竜門と言われる",
    ], size=52),
    "e04_bunshun": table3("2025年9月の週刊誌報道（疑惑）", ("", "内容", ""), [
        ("9月10日", "共演していたスーツアクターとの不倫疑惑", ("週刊文春", True)),
        ("9月18日", "プロサッカー選手との交際疑惑も報道", ("週刊文春", True)),
        ("東映", "プライバシーを理由に回答せず", ""),
        ("注意", "どちらも確定した事実ではない", ""),
    ], widths=(220, 700), size=44),
    "e05_cancel": table3("2025年11月8日（公式の発表）", ("だれ", "発表", ""), [
        ("事務所 seju", "20歳未満の飲酒を確認　契約を解除", ""),
        ("テレビ朝日", "降板の申し入れに同意", "番組サイト"),
        ("本人", "Instagramで謝罪", "「非常に恥ずべき行為」"),
        ("理由", "20歳未満の飲酒", ("不倫疑惑ではない", True)),
    ], widths=(260, 700), size=44),
    "e05_age": P.bullets("18歳と20歳のちがい", [
        "成人（大人）になる年齢　18歳（2022年から）",
        "お酒・たばこが許される年齢　20歳のまま",
        "→ 19歳は「成人」でも　お酒は法律違反",
    ], size=54),
    "e06_swap": P.bullets("番組の対応", [
        "降板直後の放送は　出演シーンをカット・編集",
        "11月15日　志田こはくさんの起用を発表",
        "11月30日の第40話から　同じ役で出演",
        "テレビ朝日社長「子供向け番組で申し訳ない」（11月25日）",
    ], size=50),
    "e07_youtube": P.bullets("2026年10月　YouTubeで再出発（本人の動画・報道）", [
        "10月8日　YouTubeに初投稿",
        "契約終了後は　約4か月ラウンジで働いたと説明",
        "パパ活の疑いは否定",
        "芸能界には戻らない考えを示した",
    ], size=50),
    "e10_timeline": table3("2026年10月の6日間", ("日付", "できごと", ""), [
        ("10月8日", "YouTubeに初投稿", ""),
        ("10月12日", "YouTuberとの対談動画が公開", ""),
        ("", "過去の妊娠経験にふれた発言が拡散", ""),
        ("10月14日未明", "LINEの画像をXに投稿→削除", ""),
        ("10月14日", "謝罪し　すべての発信を休止と表明", ""),
    ], widths=(280, 720), size=44),
    "e10_apology": P.bullets("10月14日の本人の文書（報道より）", [
        "妊娠の発言について説明・謝罪　その後のことは話せない",
        "LINEの画像の投稿についても謝罪",
        "「心がもたず」と　追い詰められていた心境",
        "しばらく　すべての発信をやめると表明",
    ], size=48),
    "e11_summary": table3("ここまでの流れ", ("いつ", "できごと", ""), [
        ("2023年", "ミスマガジン2023 グランプリ", ""),
        ("2025年2月", "ゴジュウジャーで戦隊ヒロインに", ""),
        ("2025年9月", "週刊誌の不倫・交際疑惑", "疑惑"),
        ("2025年11月", "20歳未満の飲酒で契約解除・降板", "公式"),
        ("2026年10月", "YouTube再出発→騒動→発信休止", "本人"),
    ], widths=(260, 720), size=44),
    "e11_note": P.bullets("分けて考えたいこと", [
        "20歳未満の飲酒は　本人の責任",
        "週刊誌の疑惑は　確定した事実ではない",
        "プライベートな話を広める・詮索する",
        "誹謗中傷する　→ 別の問題",
    ], size=56),
    "e12_ending": P.message(["ネットの言葉は", "相手に届いている"], sub="※誹謗中傷・詮索はやめましょう", size=96),
}


def main():
    os.makedirs(PREV, exist_ok=True)
    for name, img in ITEMS.items():
        img.save(os.path.join(OUT, name + ".png"))
        bg = P.placeholder_bg("背景")
        bg.alpha_composite(img)
        bg.convert("RGB").save(os.path.join(PREV, name + ".jpg"), quality=85)
    files = sorted(f for f in os.listdir(PREV) if f.endswith(".jpg") and f != "_contact.jpg")
    cols, tw, th = 4, 480, 270
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), "white")
    for i, fn in enumerate(files):
        sheet.paste(Image.open(os.path.join(PREV, fn)).resize((tw - 8, th - 8)), ((i % cols) * tw + 4, (i // cols) * th + 4))
    sheet.save(os.path.join(PREV, "_contact.jpg"), quality=85)
    print(f"{len(ITEMS)} parts -> {OUT}")


if __name__ == "__main__":
    main()
