#!/usr/bin/env python3
"""Gemini TTS で台本の各行を読み上げ、行ごとの WAV を作る。

- APIキーは環境変数 GEMINI_API_KEY から読む
- 生成した音声は voice_dir/NN.wav に保存し、文・声・指示が同じなら再生成しない
- キーが無くても、AI Studio などで作った音声を voice_dir/NN.wav に置けばそれを使う

- 台本の tts に "batch": 7 のように書くと、足りない行を数行ずつまとめて1回で読ませ、無音で切り分ける
  （1日の回数上限がある TTS モデルでも、長い台本を少ない回数で作れる）
  - 切り分けは「文字数から予想した位置」「照合モデルが答えた各行の読み始め」「無音の長さ」から決める
  - 切り分けた1行ずつを照合し、ずれた境目は隣の無音に付け替える。それでも合わない行だけ1行ずつ作り直す
- "check": true で、生成した音声が台本どおりか（アドリブ・読み飛ばしがないか）を gemini-3.8-flash で照合し、
  ずれていれば作り直す（batch のときは既定で有効。照合モデルは "check_model" で変更可）

usage:
  python3 tts_gemini.py story.json            # 足りない行だけ生成
  python3 tts_gemini.py story.json --force    # 全行作り直し
  python3 tts_gemini.py --list-models         # 使える TTS モデル名を確認
"""
import base64
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import wave

API = "https://generativelanguage.googleapis.com/v1beta"
DEFAULTS = {
    "model": "gemini-3.8-flash-tts",
    "voice": "Sulafat",
    # 人物像・場面・演技指示。行ごとの "tone"（その一文の気持ち）が後ろに付く
    "style": ("# AUDIO PROFILE\n72歳の日本人女性。穏やかで温かい声。\n"
              "## THE SCENE\n自分の身に起きた出来事を、目の前の人に打ち明けるように語っている。\n"
              "### DIRECTOR'S NOTES\n棒読みにせず、感情をこめて抑揚をはっきりつける。数字は少し強調する。"),
    "voice_dir": "voice",
}


def spoken(line):
    """読み上げる文。say があればそれ、無ければ字幕から強調記号と改行を除いたもの。"""
    if line.get("say"):
        return line["say"]
    return re.sub(r"[{}<>\[\]\n]", "", line["text"])


def tts_config(cfg):
    return {**DEFAULTS, **cfg.get("tts", {})}


def wav_path(cfg, base, i):
    return os.path.join(base, tts_config(cfg)["voice_dir"], f"{i + 1:02d}.wav")


def _key(tc, text, tone=None):
    return hashlib.sha1(json.dumps([tc["model"], tc["voice"], tc["style"], text, tone]).encode()).hexdigest()


def build_prompt(tc, text, tone=None):
    """指示（人物像・気持ち）と読み上げ文を分けて渡す。区切らないと指示まで読み上げてしまう。"""
    if not tc["style"]:
        return text
    head = "# RULES\nこれは決まった台本の朗読。TRANSCRIPT の文字どおりに読む。最初に発する言葉は TRANSCRIPT の最初の言葉。あいさつ・前置き・「昔々」などの語り出し・補足・感想は一切言わない。\n" + tc["style"] + (f"この一文の気持ち：{tone}" if tone else "")
    return f"{head}\n指示文は読まず、TRANSCRIPT の日本語だけを読み上げること。TRANSCRIPT に無い言葉を足さない。前置き・言い換え・繰り返しをしない。\n#### TRANSCRIPT\n{text}"


def _request(path, body=None, retry_400=False, timeout=120):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY が設定されていません（環境変数に登録してください）")
    req = urllib.request.Request(f"{API}/{path}", data=json.dumps(body).encode() if body else None,
                                 headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            if e.code == 429 and "per_day" in msg:   # 1日の上限：待っても戻らないので、再試行せずに止める
                sys.exit(f"Gemini API の1日の上限に達しました: {msg[:400]}")
            # TTS はまれに同じ指示でも 400 を返す（音声ではなく文章を返そうとしたとき）。数回までやり直す
            if (e.code in (429, 500, 503) or (retry_400 and e.code == 400 and attempt < 3)) and attempt < 5:
                wait = 2 ** attempt * 5
                print(f"  {e.code} → {wait}s 待って再試行", flush=True)
                time.sleep(wait)
                continue
            sys.exit(f"Gemini API エラー {e.code}: {msg[:500]}")


def synthesize(tc, text, out, tone=None, tries=3):
    """1行を読ませて保存。check が有効なら台本どおりか判定し、ずれていれば作り直す。"""
    for t in range(tries):
        audio = request_audio(tc, build_prompt(tc, text, tone))
        ok, why, _ = check_reading(tc, audio, [text])
        if ok or t == tries - 1:
            if not ok:
                print(f"  ※ 台本とずれたまま保存（{why}）", flush=True)
            save_wav(out, *audio)
            return
        print(f"  台本とずれている（{why}）→ 作り直し", flush=True)


def check_reading(tc, audio, texts):
    """音声が台本どおりに読まれているかを Gemini に判定させる（tts の "check": false で無効）。"""
    if not tc.get("check", int(tc.get("batch", 1) or 1) > 1):   # 既定はまとめ読みのときだけ照合
        return True, "", None
    pcm, ch, width, rate = audio
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(width)
        w.setframerate(rate)
        w.writeframes(pcm)
    script = "\n".join(texts)
    try:
        res = _request(f"models/{tc.get('check_model', 'gemini-3.8-flash')}:generateContent", {
            "contents": [{"parts": [
                {"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(buf.getvalue()).decode()}},
                {"text": "この音声が、次の台本どおりに読まれているか判定してください。台本に無い言葉の追加・前置き、"
                         "読み飛ばし、言い間違い、繰り返しがあれば NG。漢字とかなの表記ゆれ、句読点、間の長さは無視する。\n"
                         'JSON で {"ok": true/false, "reason": "NG の理由（短く）", "starts": [各行を読み始めた秒数（小数）]} だけを返す。'
                         "starts は台本の行と同じ数・同じ順にする。\n#### 台本\n" + script}]}],
            "generationConfig": {"responseMimeType": "application/json"},
        })
    except SystemExit as e:
        print(f"  ※ 照合できず（{str(e)[:60]}）→ 照合なしで進める", flush=True)
        return True, "", None
    try:
        r = json.loads(res["candidates"][0]["content"]["parts"][0]["text"])
        starts = r.get("starts")
        if not (isinstance(starts, list) and len(starts) == len(texts)):
            starts = None
        return bool(r.get("ok")), r.get("reason", ""), starts
    except (KeyError, ValueError):
        return True, "", None


def request_audio(tc, prompt):
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": tc["voice"]}}},
        },
    }
    # 長いまとめ読みは生成に数分かかる（1文字あたり約0.2秒の音声。余裕をみて最大15分待つ）
    wait = min(900, 120 + len(prompt) * 0.3)
    res = _request(f"models/{tc['model']}:generateContent", body, retry_400=True, timeout=wait)
    part = res["candidates"][0]["content"]["parts"][0]["inlineData"]
    return decode_audio(base64.b64decode(part["data"]), part.get("mimeType", ""))


def save_wav(out, pcm, ch, width, rate):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with wave.open(out, "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(width)
        w.setframerate(rate)
        w.writeframes(pcm)


def decode_audio(data, mime=""):
    """API の音声を (PCM, ch, 幅, rate) に。2.5 系は生PCM（audio/L16）、3.x 系は WAV ファイル丸ごと。
    WAV を生PCMとして扱うと、ヘッダが頭の「プチッ」、末尾のメタデータが「ザッ」というノイズになる。"""
    if data[:4] == b"RIFF":
        with wave.open(io.BytesIO(data)) as src:
            return src.readframes(src.getnframes()), src.getnchannels(), src.getsampwidth(), src.getframerate()
    m = re.search(r"rate=(\d+)", mime)
    return data, 1, 2, int(m.group(1)) if m else 24000


# --- まとめ読み（batch） ---
BATCH_MAX_CHARS = 220      # 1回に読ませる文字数の上限の既定（tts の "batch_chars" で変更。長すぎると読み飛ばしや声の揺れが出やすい）


def build_batch_prompt(tc, texts, tones):
    # 行ごとの気持ちを一覧で渡すと、モデルが語り手として話を作り始めることがある（gemini-3.8-flash-tts で確認）。
    # 既定では渡さず、人物設定と全体の演技指示だけで読ませる（"batch_tones": true で渡す）
    if not tc.get("batch_tones"):
        tones = [None] * len(texts)
    notes = "\n".join(f"{n + 1}行目：{t}" for n, t in enumerate(tones) if t)
    head = "# RULES\nこれは決まった台本の朗読。TRANSCRIPT の文字どおりに読む。最初に発する言葉は TRANSCRIPT の最初の言葉。あいさつ・前置き・「昔々」などの語り出し・補足・感想は一切言わない。\n" + tc["style"] + ("\n### 行ごとの気持ち\n" + notes if notes else "")
    return (f"{head}\n### 読み方\nTRANSCRIPT の各行を上から順に1行ずつ読む。行と行のあいだは、必ず1秒ほどはっきり間をあける。"
            "行の途中では長い間をあけない。\n指示文は読まず、TRANSCRIPT の日本語だけを読み上げること。TRANSCRIPT に無い言葉を足さない。前置き・言い換え・繰り返しをしない。\n#### TRANSCRIPT\n"
            + "\n".join(texts))


def _gaps(a, rate, db=-38, min_len=0.18):
    """無音区間 [(開始秒, 終了秒)]（先頭と末尾の無音は除く）"""
    import numpy as np
    win = int(0.01 * rate)
    n = len(a) // win
    lv = 20 * np.log10(np.sqrt((a[:n * win].reshape(n, win) ** 2).mean(1)) + 1e-9)
    quiet = lv < lv.max() + db
    loud = np.where(~quiet)[0]
    if len(loud) == 0:
        return [], 0, 0
    first, last = loud[0], loud[-1]
    out, i = [], first
    while i <= last:
        if quiet[i]:
            j = i
            while j <= last and quiet[j]:
                j += 1
            if (j - i) * 0.01 >= min_len:
                out.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    return out, first * 0.01, (last + 1) * 0.01


def split_batch(a, rate, lengths, starts=None):
    """まとめて読んだ音声 a を、文字数 lengths の各行に切り分ける位置（秒）を返す。うまくいかなければ None。
    行の区切りは「文字数から予想した位置に近い」かつ「長い無音」を動的計画法で選ぶ。"""
    n = len(lengths)
    if n == 1:
        return [], [], []
    gaps, start, end = _gaps(a, rate)
    if len(gaps) < n - 1:
        return None
    total = sum(lengths)
    speech = end - start
    exp = [start + speech * sum(lengths[:k + 1]) / total for k in range(n - 1)]
    try:   # 判定モデルが答えた「次の行の読み始め」を優先（文の途中の長い間と行の区切りを見分けるため）
        if starts and all(float(starts[k + 1]) > float(starts[k]) for k in range(n - 1)):
            exp = [float(starts[k + 1]) for k in range(n - 1)]
            sharp = True
        else:
            sharp = False
    except (TypeError, ValueError):
        sharp = False
    G = len(gaps)
    INF = float("inf")

    def cost(k, j):
        g0, g1 = gaps[j]
        mid = (g0 + g1) / 2
        if sharp:   # 読み始めの直前の無音を選ぶ（秒単位の誤差を見込む）
            return ((mid - exp[k]) / 0.6) ** 2 - 0.5 * min(g1 - g0, 1.5)
        return ((mid - exp[k]) / speech) ** 2 * 40 - min(g1 - g0, 1.5)

    best = [[INF] * G for _ in range(n - 1)]
    prev = [[-1] * G for _ in range(n - 1)]
    for j in range(G):
        best[0][j] = cost(0, j)
    for k in range(1, n - 1):
        run, arg = INF, -1
        for j in range(G):
            if j > 0 and best[k - 1][j - 1] < run:
                run, arg = best[k - 1][j - 1], j - 1
            if arg >= 0:
                best[k][j] = run + cost(k, j)
                prev[k][j] = arg
    j = min(range(G), key=lambda x: best[n - 2][x])
    if best[n - 2][j] == INF:
        return None
    picks = [j]
    for k in range(n - 2, 0, -1):
        j = prev[k][j]
        picks.append(j)
    picks.reverse()
    cuts = [(gaps[j][0] + gaps[j][1]) / 2 for j in picks]
    # 確認：各行の長さが文字数に見合っているか。区切りの無音が行の途中の間より短すぎないか
    bounds = [start] + cuts + [end]
    rate_all = speech / total
    for k in range(n):
        dur = bounds[k + 1] - bounds[k]
        r = dur / lengths[k] / rate_all
        if not 0.3 <= r <= 3.0:
            return None
    if sharp and any(abs(c - e) > 2.5 for c, e in zip(cuts, exp)):
        return None
    return cuts, gaps, picks


def synthesize_batch(tc, texts, tones, outs):
    """数行をまとめて読ませ、行ごとの WAV に切り分けて保存する。
    切り分けた1行ずつを照合し、ずれた境目は隣の無音に付け替えて照合し直す。
    保存できた行は True、作り直しが必要な行は False のリストを返す（全体が使えなければ全部 False）。"""
    import numpy as np
    return split_and_check(tc, request_audio(tc, build_batch_prompt(tc, texts, tones)), texts, outs)


def split_and_check(tc, audio, texts, outs):
    import numpy as np
    n = len(texts)
    pcm, ch, width, rate = audio
    if width != 2 or ch != 1:
        return [False] * n
    ok, why, starts = check_reading(tc, audio, texts)
    if not ok:
        # 長くまとめるほど、どこか1か所はずれやすい。組ごと捨てずに切り分けて、1行ずつの照合で合格した行は使う
        print(f"  一部が台本とずれている（{why}）→ 1行ずつ照合して使える行は残す", flush=True)
    a = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768
    lengths = [max(1, len(re.sub(r"[、。？！・…「」\s〜]", "", t))) for t in texts]
    split = split_batch(a, rate, lengths, starts)
    if split is None:
        print("  切り分けに失敗", flush=True)
        return [False] * n
    _, gaps, picks = split

    def seg(k, pk):
        cut = [(gaps[j][0] + gaps[j][1]) / 2 for j in pk]
        e = [0] + [int(c * rate) for c in cut] + [len(a)]
        return (np.clip(a[e[k]:e[k + 1]], -1, 1) * 32767).astype("<i2").tobytes()

    def good(k, pk):
        return check_reading(tc, (seg(k, pk), 1, 2, rate), [texts[k]])[0]

    oks = [good(k, picks) for k in range(n)]
    # ずれた境目（両隣の行が NG）を、隣の無音に付け替えてみる
    for b in range(n - 1):
        if oks[b] or oks[b + 1]:
            continue
        for d in (-1, 1, -2, 2):
            j = picks[b] + d
            lo = picks[b - 1] if b > 0 else -1
            hi = picks[b + 1] if b + 1 < n - 1 else len(gaps)
            if not lo < j < hi:
                continue
            trial = picks[:b] + [j] + picks[b + 1:]
            if good(b, trial) and good(b + 1, trial):
                picks, oks[b], oks[b + 1] = trial, True, True
                print(f"  {b + 1}行目と{b + 2}行目の境目を付け替え", flush=True)
                break
    for k in range(n):
        if oks[k]:
            save_wav(outs[k], seg(k, picks), 1, 2, rate)
    bad = [k + 1 for k in range(n) if not oks[k]]
    if bad:
        print(f"  照合で NG の行（1行ずつ作り直し）: {bad}", flush=True)
    return oks


def ensure_voice(story_path, force=False):
    cfg = json.load(open(story_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(story_path))
    tc = tts_config(cfg)
    manifest_path = os.path.join(base, tc["voice_dir"], "manifest.json")
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}

    def save_manifest():
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        json.dump(manifest, open(manifest_path, "w"), ensure_ascii=False, indent=1)

    todo = []   # (行番号, 出力先, 文, 気持ち, キー)
    for i, line in enumerate(cfg["lines"]):
        if "audio" in line:
            continue
        out = wav_path(cfg, base, i)
        text = spoken(line)
        k = _key(tc, text, line.get("tone"))
        # 手で置いたファイル（manifest に無い）はそのまま使う
        if os.path.exists(out) and not force and manifest.get(os.path.basename(out), k) == k:
            continue
        todo.append((i, out, text, line.get("tone"), k))

    def one(i, out, text, tone, k):
        print(f"[{i + 1:02d}] {text}", flush=True)
        synthesize(tc, text, out, tone)
        manifest[os.path.basename(out)] = k
        save_manifest()

    size = int(tc.get("batch", 1) or 1)
    if size <= 1:
        for job in todo:
            one(*job)
        return
    # 連続する行を、size 行・BATCH_MAX_CHARS 字までの組にまとめる
    groups, cur = [], []
    for job in todo:
        if cur and (len(cur) >= size or job[0] != cur[-1][0] + 1
                    or sum(len(j[2]) for j in cur) + len(job[2]) > int(tc.get("batch_chars", BATCH_MAX_CHARS))):
            groups.append(cur)
            cur = []
        cur.append(job)
    if cur:
        groups.append(cur)
    print(f"まとめ読み: {len(todo)} 行を {len(groups)} 回で生成", flush=True)

    def run(g):
        """組をまとめて読ませる。だめだった部分は半分に分けてまとめ直し、3行未満になったら1行ずつ。"""
        if len(g) < 3:
            for job in g:
                one(*job)
            return
        nums = f"{g[0][0] + 1:02d}〜{g[-1][0] + 1:02d}"
        print(f"[{nums}] {len(g)}行まとめて", flush=True)
        try:
            oks = synthesize_batch(tc, [j[2] for j in g], [j[3] for j in g], [j[1] for j in g])
        except (TimeoutError, OSError, KeyError) as e:   # 長すぎて時間切れ・応答が途切れた → 半分に分ける
            print(f"  まとめ読みに失敗（{type(e).__name__}）→ 半分に分けて読み直す", flush=True)
            oks = [False] * len(g)
        for job, ok in zip(g, oks):
            if ok:
                manifest[os.path.basename(job[1])] = job[4]
        save_manifest()
        if all(oks):
            return
        if not any(oks):          # 組ごと使えなかった → 半分に分けてまとめ直す
            half = len(g) // 2
            run(g[:half])
            run(g[half:])
            return
        k = 0                     # 一部だけ NG → NG の続いている部分ごとにまとめ直す
        while k < len(g):
            if oks[k]:
                k += 1
                continue
            e = k
            while e < len(g) and not oks[e]:
                e += 1
            run(g[k:e])
            k = e

    for g in groups:
        run(g)


def list_models():
    res = _request("models?pageSize=1000")
    for m in res.get("models", []):
        if "tts" in m["name"].lower():
            print(m["name"].split("/", 1)[1], "-", m.get("displayName", ""))


if __name__ == "__main__":
    if "--list-models" in sys.argv:
        list_models()
    else:
        ensure_voice(sys.argv[1], force="--force" in sys.argv)
