"""VOICEVOX（ずんだもん）で台本を1行ずつ wav にする（11/22 ユーザー指定・ユーザーが VOICEVOX の取得と実行を許可）。

python3 catmeme/tools/zunda_tts.py <台本.txt> <出力フォルダ> [話速]
- 台本：「番号<TAB>文」の行（# で始まる行は飛ばす）→ 出力フォルダ/<番号>.wav
- VOICEVOX 一式は /home/user/vv（公式配布：voicevox_core 0.16.0・voicevox_onnxruntime 1.17.3・0.vvm・open_jtalk 辞書）
- 使うときは概要欄に「VOICEVOX:ずんだもん」と書く
"""
import os
import sys

from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile

VV = "/home/user/vv"
ZUNDA = 3   # ずんだもん（ノーマル）


def main():
    src, out = sys.argv[1], sys.argv[2]
    speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.25
    os.makedirs(out, exist_ok=True)
    ort = Onnxruntime.load_once(filename=os.path.join(VV, "voicevox_onnxruntime-linux-x64-1.17.3", "lib", "libvoicevox_onnxruntime.so.1.17.3"))
    syn = Synthesizer(ort, OpenJtalk(os.path.join(VV, "open_jtalk_dic_utf_8-1.11")))
    with VoiceModelFile.open(os.path.join(VV, "0.vvm")) as m:
        syn.load_voice_model(m)
    for ln in open(src, encoding="utf-8"):
        if not ln.strip() or ln.startswith("#"):
            continue
        num, text = ln.rstrip("\n").split("\t", 1)
        q = syn.create_audio_query(text, ZUNDA)
        q.speed_scale = speed
        q.pre_phoneme_length = 0.05
        q.post_phoneme_length = 0.05
        open(os.path.join(out, num + ".wav"), "wb").write(syn.synthesis(q, ZUNDA))
        print(num, text, flush=True)


if __name__ == "__main__":
    main()
