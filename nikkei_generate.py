"""
日経新聞スタイル テクノロジーニュース PPTX生成スクリプト
収集済みニュースをClaudeで日経調に整形してPPTXを生成
"""

import io
import json
import os
import textwrap

import anthropic
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-opus-4-7"

# ── 収集済みニュース（調査済み）────────────────────────────────────────────
RAW_NEWS = {
    "SMR（小型モジュール炉）": [
        "米エネルギー省（DOE）、軽水炉SMR近接展開向けに8社へ計9400万ドルを拠出。ライセンス取得・サプライチェーン・サイト整備の空白を埋める",
        "スウェーデンのBlykalla社、東部ノーシュンデットに6基のSEALERリアクター建設申請。鉛冷却型SMRとして初の実建設申請",
        "ルワンダ原子力委員会とHoltec社がSMR-300の開発協定締結。アフリカ初の商業SMR展開に向け始動",
        "Deep Fission（カリフォルニア）がIPO計画を公表。評価額約16.6億ドル。地中深部埋設型SMRの商用化を目指す",
        "世界SMR市場は「原子力黄金期」に突入との業界評価。2025〜26年が政策・資金調達・商業契約の転換点",
    ],
    "ロボット": [
        "JAL（日本航空）が羽田空港でヒューマノイドロボットの実証実験開始（5月）。手荷物積み込み・機内清掃を3年間試験運用",
        "GMO AIロボティクス、2026年を「ヒューマノイド元年」と宣言。航空業界初の本格的長期導入契約",
        "経産省、2040年までに国内物理AIセクターを確立し世界市場シェア30%獲得を目標とする方針を3月公表",
        "「ヒューマノイドサミット東京2026」が5月28〜29日に高輪ゲートウェイで開催。石黒浩教授がジェミノイドで基調講演",
        "日本の労働力不足が加速：インバウンド急増と生産年齢人口減少が空港・物流現場での導入を後押し",
    ],
    "半導体": [
        "SIA発表：2026年Q1の世界半導体売上は2985億ドル、前四半期比25%増。年間1兆ドル突破の歴史的節目が視野に",
        "インドTata電子がASMLと協定締結。グジャラート州ドーレラに110億ドル投資でインド初の前工程ファブ建設",
        "米先端製造投資クレジット（CHIPS法）が2026年末失効見通し。民間投資数千億ドルを呼び込んだ制度の存続が焦点",
        "研究者が2D材料の落とし穴を発見：絶縁層との界面に原子スケールのギャップが形成され、次世代チップの微細化を阻害",
        "AI学習・推論需要がコンピューティングインフラを根本的に刷新。ヘテロジニアス統合が主流手法として台頭",
    ],
    "AI（人工知能）": [
        "Google I/O 2026でGemini Omni・Antigravityを発表。動画生成・リミックスを会話型UIで操作可能に",
        "Apple、iOS 27でGoogle・Anthropicなど外部AIプロバイダーをApple Intelligence基盤として選択可能にする方針",
        "OpenAI、企業向け「OpenAI Deployment Company」を40億ドル以上の初期出資で設立。AI導入加速を狙う",
        "Meta、AI開発にピボットしながら8000人削減・6000人採用凍結。LLM研究への集中投資を継続",
        "英ロイズ・バンキング・グループ、英FTSE100企業初となるAIの取締役会議室導入を実施",
    ],
    "宇宙": [
        "NASA、5月26日に月面基地（Moon Base）計画の進捗発表会を予定。月面持続的プレゼンスへの具体工程を提示",
        "NASAのPsyche探査機が火星を高度2800マイルでフライバイ実施。金属小惑星「プシュケ」への軌道修正に重力を活用",
        "NASAのNancy Grace Roman宇宙望遠鏡、打ち上げ時期を2026年9月に前倒し。天文学コミュニティに期待感",
        "ブルーオリジンの無人着陸機MK1「エンデュランス」が極限環境試験を完了。将来の有人月面着陸技術の実証機",
        "ボイジャー1号が約50年稼働の観測機器を停止。エネルギー枯渇が迫る中、最後の電力温存措置を実施",
    ],
    "量子コンピューティング": [
        "米商務省、CHIPS法に基づき量子ハードウェア9社へ計20.13億ドル投資を提案。GlobalFoundriesとIBMが量子ファウンドリー構築で多額受領",
        "日本の研究チーム、量子「Wステート」の瞬時検出手法を開発。量子通信・テレポーテーション・演算の新地平",
        "欧州初のエクサスケール機「JUPITER」が50量子ビットの完全シミュレーションに成功。量子優位性の検証が加速",
        "Googleが警告：量子コンピュータが一部暗号を2029年までに解読可能になるリスク。サイバーセキュリティ対応の猶予は3年",
        "Quantinuum×BMWグループ、マルチイヤーの量子コンピューティング協業を拡大。製造工程の量子最適化を本格推進",
    ],
}

DATE_STR = "2026年5月22日（木）"


# ── Claude で日経調テキストに整形 ─────────────────────────────────────────
def rewrite_nikkei(section: str, bullets: list[str]) -> list[str]:
    system = textwrap.dedent("""
        あなたは日本経済新聞の記者です。
        与えられた箇条書きを、日経新聞の記事見出し・本文スタイルで書き直してください。

        ルール:
        - 各項目を「見出し＋補足1行」の形式にする
        - 見出しは20〜30字、補足は30〜40字
        - ビジネスインパクトを重視した簡潔・客観的な表現
        - 専門用語はそのまま使用
        - JSON配列のみを返す（各要素は "【見出し】補足" 形式の文字列）
        - 例: ["【DOEがSMR8社に94億円拠出】米政府、商業展開向け供給網整備を加速","..."]
    """).strip()

    raw = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system,
        messages=[{
            "role": "user",
            "content": f"セクション: {section}\n\n箇条書き:\n" + "\n".join(f"- {b}" for b in bullets)
        }],
    ).content[0].text.strip()

    # Strip markdown fences
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:]).rsplit("```", 1)[0]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return bullets  # fallback: use originals


# ── 日経カラーテーマ ──────────────────────────────────────────────────────
NIKKEI = {
    "bg":        RGBColor(0xFF, 0xFF, 0xFF),   # 白
    "header":    RGBColor(0xCC, 0x22, 0x33),   # 日経赤
    "title_fg":  RGBColor(0xFF, 0xFF, 0xFF),   # 白（ヘッダー上）
    "headline":  RGBColor(0x11, 0x11, 0x11),   # 見出し黒
    "body":      RGBColor(0x33, 0x33, 0x33),   # 本文グレー
    "accent":    RGBColor(0xCC, 0x22, 0x33),   # アクセント線
    "category":  RGBColor(0xF5, 0xF5, 0xF5),  # カテゴリ背景
    "date":      RGBColor(0x88, 0x88, 0x88),   # 日付グレー
    "logo_bg":   RGBColor(0xCC, 0x22, 0x33),
}

SECTION_COLORS = {
    "SMR（小型モジュール炉）":   RGBColor(0x1A, 0x6B, 0xAA),
    "ロボット":                  RGBColor(0x22, 0x99, 0x55),
    "半導体":                    RGBColor(0xDD, 0x77, 0x00),
    "AI（人工知能）":            RGBColor(0x99, 0x22, 0xCC),
    "宇宙":                      RGBColor(0x11, 0x44, 0xAA),
    "量子コンピューティング":    RGBColor(0xBB, 0x22, 0x44),
}


def _set_bg(slide, color: RGBColor):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def _add_text(slide, text, x, y, w, h, size, bold=False, color=None, align=PP_ALIGN.LEFT, wrap=True):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color or NIKKEI["body"]
    p.alignment = align
    return tb


def _add_rect(slide, x, y, w, h, color: RGBColor):
    shape = slide.shapes.add_shape(1, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


# ── スライド構築 ──────────────────────────────────────────────────────────
def build_nikkei_pptx(news: dict[str, list[str]]) -> io.BytesIO:
    prs = Presentation()
    prs.slide_width  = Inches(13.33)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # ── タイトルスライド ──────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    _set_bg(s, NIKKEI["bg"])

    # 赤ヘッダーバー
    _add_rect(s, Inches(0), Inches(0), Inches(13.33), Inches(1.8), NIKKEI["header"])
    # 日経ロゴ風テキスト
    _add_text(s, "日本経済新聞", Inches(0.4), Inches(0.15), Inches(5), Inches(0.8),
              28, bold=True, color=NIKKEI["title_fg"], align=PP_ALIGN.LEFT)
    _add_text(s, "NIKKEI", Inches(0.4), Inches(0.8), Inches(3), Inches(0.6),
              14, bold=False, color=RGBColor(0xFF, 0xCC, 0xCC), align=PP_ALIGN.LEFT)
    # 日付
    _add_text(s, DATE_STR, Inches(9.5), Inches(0.55), Inches(3.5), Inches(0.6),
              13, color=RGBColor(0xFF, 0xDD, 0xDD), align=PP_ALIGN.RIGHT)

    # メインタイトル
    _add_text(s, "テクノロジー最前線", Inches(1), Inches(2.1), Inches(11.33), Inches(1.2),
              44, bold=True, color=NIKKEI["headline"], align=PP_ALIGN.CENTER)
    # サブタイトル
    _add_text(s, "SMR ／ ロボット ／ 半導体 ／ AI ／ 宇宙 ／ 量子コンピューティング",
              Inches(1), Inches(3.5), Inches(11.33), Inches(0.7),
              18, color=NIKKEI["body"], align=PP_ALIGN.CENTER)
    # アクセント下線
    _add_rect(s, Inches(3.5), Inches(4.35), Inches(6.33), Emu(30000), NIKKEI["accent"])
    # 号数
    _add_text(s, "直近24時間 速報版", Inches(1), Inches(4.7), Inches(11.33), Inches(0.5),
              14, color=NIKKEI["date"], align=PP_ALIGN.CENTER)

    # ── ニュース各セクション ──────────────────────────────────────
    for section, bullets in news.items():
        s = prs.slides.add_slide(blank)
        _set_bg(s, NIKKEI["bg"])
        cat_color = SECTION_COLORS.get(section, NIKKEI["accent"])

        # 上部ヘッダーバー（細め）
        _add_rect(s, Inches(0), Inches(0), Inches(13.33), Inches(0.9), NIKKEI["header"])
        _add_text(s, "日本経済新聞  テクノロジー面",
                  Inches(0.3), Inches(0.1), Inches(8), Inches(0.6),
                  13, color=NIKKEI["title_fg"])
        _add_text(s, DATE_STR, Inches(9.5), Inches(0.18), Inches(3.5), Inches(0.5),
                  12, color=RGBColor(0xFF, 0xDD, 0xDD), align=PP_ALIGN.RIGHT)

        # カテゴリタグ
        tag_w = Inches(3.2)
        _add_rect(s, Inches(0.4), Inches(1.05), tag_w, Inches(0.45), cat_color)
        _add_text(s, f"  {section}", Inches(0.4), Inches(1.05), tag_w, Inches(0.45),
                  14, bold=True, color=NIKKEI["title_fg"])

        # セクション見出し下線
        _add_rect(s, Inches(0.4), Inches(1.55), Inches(12.5), Emu(25000), cat_color)

        # 記事バレット
        y = Inches(1.75)
        line_h = Inches(0.78)
        for i, bullet in enumerate(bullets[:5]):
            # 丸番号
            _add_rect(s, Inches(0.4), y + Emu(30000), Inches(0.32), Inches(0.32), cat_color)
            _add_text(s, str(i + 1), Inches(0.4), y + Emu(28000), Inches(0.32), Inches(0.32),
                      10, bold=True, color=NIKKEI["title_fg"], align=PP_ALIGN.CENTER)

            # バレット本文
            tb = slide.shapes if False else s.shapes
            bullet_box = s.shapes.add_textbox(Inches(0.82), y, Inches(12.1), Inches(0.68))
            tf = bullet_box.text_frame
            tf.word_wrap = True

            # 見出し部分と本文を分ける（【...】を太字に）
            p = tf.paragraphs[0]
            text = bullet
            if "】" in text and text.startswith("【"):
                head, _, rest = text.partition("】")
                head = head.lstrip("【")
                run1 = p.add_run()
                run1.text = f"【{head}】"
                run1.font.bold = True
                run1.font.size = Pt(16)
                run1.font.color.rgb = NIKKEI["headline"]
                run2 = p.add_run()
                run2.text = f"　{rest}"
                run2.font.size = Pt(14)
                run2.font.color.rgb = NIKKEI["body"]
            else:
                p.text = text
                p.font.size = Pt(14)
                p.font.color.rgb = NIKKEI["body"]

            y += line_h

        # フッター
        _add_rect(s, Inches(0), Inches(7.15), Inches(13.33), Emu(35000), NIKKEI["header"])
        _add_text(s, "© 日本経済新聞社  本資料はClaude Coworks（多エージェント）が生成",
                  Inches(0.3), Inches(7.18), Inches(10), Inches(0.28),
                  9, color=RGBColor(0xFF, 0xDD, 0xDD))

    # ── まとめスライド ─────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    _set_bg(s, NIKKEI["bg"])
    _add_rect(s, Inches(0), Inches(0), Inches(13.33), Inches(0.9), NIKKEI["header"])
    _add_text(s, "日本経済新聞  テクノロジー面",
              Inches(0.3), Inches(0.1), Inches(8), Inches(0.6), 13, color=NIKKEI["title_fg"])

    _add_text(s, "【編集後記】  本日のテクノロジー主要6分野まとめ",
              Inches(0.4), Inches(1.1), Inches(12.5), Inches(0.7),
              22, bold=True, color=NIKKEI["headline"])
    _add_rect(s, Inches(0.4), Inches(1.85), Inches(12.5), Emu(25000), NIKKEI["accent"])

    summaries = [
        ("SMR",   "米欧で政策・民間投資が加速。原子力の小型化が商業化フェーズへ移行"),
        ("ロボット", "羽田空港でJALがヒューマノイド実証。日本が物理AI産業の世界覇権を狙う"),
        ("半導体", "Q1売上25%増の2985億ドル。年間1兆ドルが現実圏内。印度ファブ建設も始動"),
        ("AI",    "Google I/O・Apple・OpenAIが相次ぎ新戦略を発表。規制と競争が同時激化"),
        ("宇宙",   "NASA月面基地計画・ローマン望遠鏡前倒し。民間宇宙技術の成熟が加速"),
        ("量子",   "米20億ドル投資・Google「2029年暗号解読リスク」警告。量子安保が緊急課題に"),
    ]

    y = Inches(2.1)
    for label, text in summaries:
        col = SECTION_COLORS.get(
            next((k for k in SECTION_COLORS if label in k), ""), NIKKEI["accent"])
        _add_rect(s, Inches(0.4), y + Emu(20000), Inches(1.1), Inches(0.3), col)
        _add_text(s, label, Inches(0.4), y + Emu(18000), Inches(1.1), Inches(0.3),
                  11, bold=True, color=NIKKEI["title_fg"], align=PP_ALIGN.CENTER)
        _add_text(s, text, Inches(1.65), y, Inches(11.2), Inches(0.42),
                  13, color=NIKKEI["body"])
        y += Inches(0.73)

    _add_rect(s, Inches(0), Inches(7.15), Inches(13.33), Emu(35000), NIKKEI["header"])
    _add_text(s, "© 日本経済新聞社  本資料はClaude Coworks（多エージェント）が生成",
              Inches(0.3), Inches(7.18), Inches(10), Inches(0.28),
              9, color=RGBColor(0xFF, 0xDD, 0xDD))

    buf = io.BytesIO()
    prs.save(buf)
    buf.seek(0)
    return buf


# ── メイン ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("日経スタイル整形中（Claudeエージェント）...")
    nikkei_news = {}
    for section, bullets in RAW_NEWS.items():
        print(f"  [{section}] 日経調に整形...")
        nikkei_news[section] = rewrite_nikkei(section, bullets)

    print("PPTX構築中...")
    buf = build_nikkei_pptx(nikkei_news)

    outpath = "/home/user/DANIEL/nikkei_tech_news.pptx"
    with open(outpath, "wb") as f:
        f.write(buf.read())
    print(f"完成: {outpath}")
