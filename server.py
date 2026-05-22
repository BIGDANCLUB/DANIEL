"""
Claude Coworks - Multi-Agent Research to PowerPoint Generator
3 agents collaborate:
  1. Research Agent  - gathers & summarizes information on a topic
  2. Structure Agent - organises the research into slide outlines
  3. PPTX Agent      - writes python-pptx code executed server-side
"""

import io
import json
import os
import textwrap

import anthropic
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
MODEL = "claude-opus-4-7"


# ---------------------------------------------------------------------------
# Agent helpers
# ---------------------------------------------------------------------------

def call_agent(system: str, user: str, max_tokens: int = 4096) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text


def research_agent(topic: str) -> str:
    system = textwrap.dedent("""
        あなたは優秀なリサーチャーです。
        与えられたトピックについて、わかりやすく正確な情報を日本語で提供してください。
        以下の形式で回答してください：
        - 概要（2〜3文）
        - 主要なポイント（5〜7項目、各項目に説明）
        - 重要な統計・事実（あれば）
        - 結論・まとめ
    """).strip()
    return call_agent(system, f"トピック: {topic}")


def structure_agent(topic: str, research: str) -> str:
    system = textwrap.dedent("""
        あなたはプレゼンテーション構成の専門家です。
        提供されたリサーチ内容を元に、パワーポイントのスライド構成をJSONで返してください。

        必ず以下のJSON形式のみを返してください（マークダウンコードブロック不要）:
        {
          "title": "プレゼンタイトル",
          "slides": [
            {
              "title": "スライドタイトル",
              "content": ["箇条書き1", "箇条書き2", "箇条書き3"]
            }
          ]
        }

        ルール:
        - タイトルスライド1枚 + コンテンツスライド5〜8枚 + まとめスライド1枚
        - 各スライドのcontentは3〜5項目
        - 日本語で記述
    """).strip()
    return call_agent(
        system,
        f"トピック: {topic}\n\nリサーチ内容:\n{research}",
        max_tokens=2048,
    )


# ---------------------------------------------------------------------------
# PPTX builder
# ---------------------------------------------------------------------------

THEME = {
    "bg": RGBColor(0x1A, 0x1A, 0x2E),
    "accent": RGBColor(0x4A, 0x9E, 0xFF),
    "text": RGBColor(0xEE, 0xEE, 0xEE),
    "sub": RGBColor(0xAA, 0xAA, 0xCC),
}


def _set_bg(slide, color: RGBColor):
    from pptx.oxml.ns import qn
    from lxml import etree

    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def build_pptx(structure: dict) -> io.BytesIO:
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]  # blank

    for i, slide_data in enumerate(structure["slides"]):
        slide = prs.slides.add_slide(blank_layout)
        _set_bg(slide, THEME["bg"])

        is_title_slide = i == 0

        if is_title_slide:
            # Big centered title
            tf = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11.33), Inches(1.5))
            p = tf.text_frame.paragraphs[0]
            p.text = slide_data["title"]
            p.font.size = Pt(40)
            p.font.bold = True
            p.font.color.rgb = THEME["accent"]
            p.alignment = 2  # center

            if slide_data.get("content"):
                sub = slide.shapes.add_textbox(Inches(1), Inches(4.2), Inches(11.33), Inches(1))
                sp = sub.text_frame.paragraphs[0]
                sp.text = slide_data["content"][0]
                sp.font.size = Pt(22)
                sp.font.color.rgb = THEME["sub"]
                sp.alignment = 2
        else:
            # Slide title bar
            title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.33), Inches(0.8))
            tp = title_box.text_frame.paragraphs[0]
            tp.text = slide_data["title"]
            tp.font.size = Pt(28)
            tp.font.bold = True
            tp.font.color.rgb = THEME["accent"]

            # Separator line (thin rectangle)
            from pptx.util import Emu
            line = slide.shapes.add_shape(
                1,  # MSO_SHAPE_TYPE.RECTANGLE
                Inches(0.5), Inches(1.15), Inches(12.33), Emu(40000),
            )
            line.fill.solid()
            line.fill.fore_color.rgb = THEME["accent"]
            line.line.fill.background()

            # Bullet points
            content_box = slide.shapes.add_textbox(
                Inches(0.7), Inches(1.4), Inches(11.93), Inches(5.5)
            )
            tf = content_box.text_frame
            tf.word_wrap = True

            for j, bullet in enumerate(slide_data.get("content", [])):
                if j == 0:
                    para = tf.paragraphs[0]
                else:
                    para = tf.add_paragraph()
                para.text = f"• {bullet}"
                para.font.size = Pt(20)
                para.font.color.rgb = THEME["text"]
                para.space_before = Pt(8)

    buf = io.BytesIO()
    prs.save(buf)
    buf.seek(0)
    return buf


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    topic = (data or {}).get("topic", "").strip()
    if not topic:
        return jsonify({"error": "topic is required"}), 400

    try:
        # Agent 1: Research
        research = research_agent(topic)

        # Agent 2: Structure
        raw_structure = structure_agent(topic, research)

        # Parse JSON (strip markdown fences if present)
        clean = raw_structure.strip()
        if clean.startswith("```"):
            clean = "\n".join(clean.split("\n")[1:])
            clean = clean.rsplit("```", 1)[0]
        structure = json.loads(clean)

        # Make title slide content list safe
        if not structure["slides"][0].get("content"):
            structure["slides"][0]["content"] = [topic]

        # Agent 3 / PPTX builder
        buf = build_pptx(structure)

        filename = f"{topic[:30].replace(' ', '_')}.pptx"
        return send_file(
            buf,
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            as_attachment=True,
            download_name=filename,
        )

    except json.JSONDecodeError as e:
        return jsonify({"error": f"構成JSONのパースに失敗しました: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/")
def index():
    return send_file("coworks.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
