"""39_raden（VTuberの音声ガイド 154万円の費用と経済効果）（11/2 ユーザー指定・くらべる長尺と同じ作り）。2〜3分。

python3 catmeme/cuts_39_raden.py [--charts|--len]
題材：オタク総研の記事（11/2）「ホロライブVTuberの“案件価格”が自治体文書から判明」ほか
  静岡県立美術館の音声ガイド（2026年1月20日〜3月15日・ロダン館／ナイトミュージアム／中村宏展／2000年代の絵画の4つ）を
  ホロライブの儒烏風亭らでんさんが担当。県の公開資料（令和7年度 事務事業及び予算の執行実績）に委託料154万円（受託はカバー株式会社）。
  本人が配信で見つけて驚いた。本人の報酬がそのまま154万円ではない。ファンからは「破格」の声
  地域での直接消費は推計 約3600万円（報道）。来館者の約34％がらでんさんの発信をきっかけに来館（報道）
  → 費用の約23倍（3600÷154＝23.4）
原稿のルール：実在の人をけなさない・からかわない（ほめる方向）。推計は推計と言う。今日の一言・単語の途中で改行しない・最後はチャンネル登録
"""
import compare_long as C
import cuts_26_kuruma as K
import wide_bars as B

MUSEUM, STREAM, DOCS, CITY, FOOD, HOTEL, PHONE = ("bg39_museum", "bg72_live_stream", "bg97_tabloid_desk", "bg31_city_meeting",
                                                  "bg47_ramen_shop", "bg66_hotel_price", "bg73_shorts_phone")
C.setup("39_raden", {MUSEUM: "bg75_seminar_hall"}, tempo=1.0)
bg, nn, ss, boom, qq, g, fx, chap = C.bg, C.nn, C.ss, C.boom, C.qq, C.g, C.fx, C.chap
CONAN, POON, MONEY = C.CONAN, C.POON, C.MONEY

VS = [("費用（委託料）", "red"), ("経済効果（推計）", "teal")]
N = 23   # 3600 ÷ 154 ＝ 23.4

C.charts({
    "r0_vs": B.Chart(VS, [(0.5, 0, "委託料", 154, "red"), (1.8, 1, "地域での消費", 3600, "teal")], 3900, bg=MUSEUM,
                     head="費用と経済効果（目安）", total_fmt="{v}万円", result_at=3.0, highlight=1),
    "r1_stack": B.Chart([("154万円", "red"), ("154万円が何個分？", "teal")],
                        [(-1, 0, "", 154, "red")] + [(0.6 + 0.16 * k, 1, "", 154, ("teal", "gold")[k % 2]) for k in range(N)]
                        + [(0.6 + 0.16 * N + 0.3, 1, "", 3600 - 154 * N, "teal")], 3900, bg=MONEY,
                        head="154万円を積み上げると……", total_fmt="{v}万円", result_at=0.6 + 0.16 * N + 1.0, highlight=1),
    "r2_visit": B.Chart([("発信がきっかけ", "pink"), ("それ以外", "navy")],
                        [(0.4, 0, "", 34, "pink"), (1.3, 1, "", 66, "navy")], 80, bg=MUSEUM,
                        head="来館したきっかけ（報道より）", total_fmt="約{v}％", highlight=0),
})
K.DROP_SE["r1_stack"] = {1: "game_coin_get_money_gain_happy"}
K.STEP_SE.pop("r1_stack", None)


def cuts_all():
    return [
        C.notice(MUSEUM, (("read_book_orange_kitten", 220, 560), ("dance_three_kittens", 640, 520), ("calm_black_face_sheep", 1000, 560),
                          ("money_counting_orange_cat", 1360, 560), ("dance_happy_banana_cat", 1720, 600))),
        # ---- つかみ ----
        nn("VTuberに\n県のお仕事を頼むと\nいくらかかるの？", STREAM, se="question_hatena_maou", bgm={"file": C.PURPLE, "gain": -4}),
        ss("それが\n県の公開資料に\n書いてあった", DOCS, se="pi"),
        # 11/2 ユーザー指定：154万円はそんなに高くないので白黒「？」はなし・音はお金のチャリーン
        fx(boom(None, MUSEUM, who="S", se=[{"f": "coin_chariin", "at": 0.9, "gain": -2}]), slot=("美術館の音声ガイド 委託料", 154, "万円")),
        boom("154万円!?", MUSEUM, se=[CONAN]),
        ss("しかも\nその効果は\nもっとすごかった", MONEY, se="pikon"),
        C.title(MUSEUM, "read_book_orange_kitten", "talk_orange_white_sitting_cat"),
        C.card("e02_premise", "静岡県立美術館の音声ガイドの話", dur=5.2),
        # ---- 何があった ----
        chap("① 何があった？", se="quiz_question_01", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        ss("静岡県立美術館の\n音声ガイドを\nVTuberが担当", MUSEUM, se="pi"),
        ss("ホロライブの\n儒烏風亭らでんさん", MUSEUM, se="pikon"),
        ss("美術や博物館が大好きで\n博物館とのコラボも\nしてきたVTuber", MUSEUM, se="kon"),
        ss("ロダン館や\n夜のナイトミュージアム\n4つの展示を案内", MUSEUM, se="kon"),
        ss("スマホで聞ける\n無料の音声ガイド", PHONE, se="pikon"),
        nn("推しの声で\n美術館をめぐれるの？", PHONE, se="question_hatena_maou"),
        nn("それは行く", PHONE, red=True, se=["explosion_dokaan"]),
        # ---- 154万円 ----
        chap("② 154万円の中身", se="doon_heavy"),
        ss("県が毎年出している\nお金の使いみちの資料に", DOCS, se="pi"),
        ss("音声ガイドの委託料\n154万円と\n書いてあった", DOCS, se="kon"),
        ss("本人も配信で\nこの資料を見つけて\n驚いていた", STREAM, se="pikon"),
        fx(nn("自分の案件の値段を\n県の資料で知る……", STREAM, se=POON), "swirl"),
        ss("154万円は\n会社への委託料\n収録や制作もぜんぶ込み", DOCS, se="kon"),
        ss("本人の報酬が\nそのまま154万円\nではない", DOCS, se="pi"),
        ss("ファンからは\n破格という声も", PHONE, se="kon"),
        nn("たしかに\n県のお仕事にしては\n安く感じる", PHONE, se="pikon"),
        # ---- 経済効果 ----
        chap("③ 経済効果は？", se="quiz_question_01", bgm={"file": C.MIRAI, "gain": -4, "fade": 0.6}),
        ss("報道によると\n美術館のまわりで\n使われたお金は", CITY, se="pi"),
        ss("推計で\n約3600万円", MONEY, se="kon"),
        g("r0_vs", "費用と経済効果を\nくらべると……", dur=5.0),
        qq(MONEY, "anime_conan_hirameki_remix_b"),
        fx(boom("約23倍!!", MONEY, se=["explosion_chudoon"]), "money"),
        fx(nn("154万円が\n3600万円に\n化けた!?", MONEY, se="tv_professional_poon_remix_a"), "swirl"),
        g("r1_stack", "154万円を\n何個積めば\n届く？", dur=6.4),
        boom("154万円\n23個分!!", MONEY, se=["explosion_dokaan"]),
        ss("さらに\n来館者の約34％が\nらでんさんの発信が\nきっかけ", MUSEUM, se="pi"),
        g("r2_visit", "3人に1人は\nらでんさんきっかけ", dur=3.8),
        fx(boom("3人に1人!?", MUSEUM, se=["explosion_chudoon", {"f": "glass_break_01", "gain": -4}]), "crack"),
        nn("3600万円を\n動かした声……", MONEY, se="shine_kiraan_maou"),
        # ---- なぜ ----
        chap("④ なぜそんなに効果が？", se="whoosh_shu", bgm={"file": C.COCOA, "gain": -4, "fade": 0.6}),
        ss("ふだん美術館に\n行かない人が\n来るきっかけになった", MUSEUM, se="kon"),
        ss("遠くから\n来るファンもいる", MUSEUM, se="kon"),
        ss("来たら\nごはんを食べる", FOOD, se="pikon"),
        ss("お土産も買う\n泊まる人もいる", HOTEL, se="pikon"),
        nn("聖地めぐりって\nやつだね", HOTEL, se="kon"),
        ss("お金は\n美術館だけじゃなく\n町じゅうで使われる", CITY, se="kon"),
        nn("推しの力って\nすごい……", CITY, red=True, se=["explosion_dokaan"]),
        # ---- 注意 ----
        chap("⑤ 気をつけたいこと", se="doon_heavy"),
        ss("3600万円は推計\n計算のしかたで\n数字は変わる", DOCS, se="pi"),
        ss("それでも\n費用の何倍ものお金が\n地域で使われた", MONEY, se="kon"),
        nn("税金の使い方として\nかなり上手なのでは", CITY, se="pikon"),
        ss("文化とVTuber\n相性がいいのかも\nしれない", MUSEUM, se="sparkle_kirakira_01"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy", bgm={"file": C.NORA, "gain": -4, "fade": 0.6}),
        C.card("e07_points", "154万円で 約3600万円の消費", dur=5.6),
        nn("次は\nどこの美術館と\nコラボするんだろう", MUSEUM, se="kon"),
        ss("推しに会いに\n美術館へ\n行ってみよう", MUSEUM, se="kon"),
    ] + C.ending(MUSEUM)


if __name__ == "__main__":
    C.main("39_raden", cuts_all, ["r0_vs", "r1_stack", "r2_visit"])
