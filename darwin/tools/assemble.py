"""③ 結合：クリップ＋ナレーション＋環境音＋SE＋オチのBGM を 9:16 の mp4 にまとめる。

  python tools/assemble.py 01-keiba      # → episodes/01-keiba/out/final.mp4（＋字幕 subtitles.srt）

素材（任意。無ければスキップして警告のみ）
  assets/ambience/<名前>.wav   … episode.json の section.ambience（無ければ H3 が生成した音を薄く敷く）
  assets/sfx/<名前>.wav        … line.cues の sfx
  assets/bgm/<名前>.wav        … line.cues の bgm（そこから最後まで流れる）
"""
import argparse
import sys
from pathlib import Path

from common import find_asset, load_config, load_episode, load_json, out_dir, probe, run_ffmpeg

AR = ["-ar", "48000", "-ac", "2"]


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    args = ap.parse_args()

    r = load_config()["render"]
    ep_dir, ep = load_episode(args.episode)
    out = Path(ep_dir, "out")
    tl = load_json(out / "timeline.json")
    work = out_dir(ep_dir, "work")
    total = tl["total"]
    W, H, FPS = r["width"], r["height"], r["fps"]
    amb_by_sec = {s["id"]: s.get("ambience") for s in ep["sections"]}

    v_list, a_list = [], []
    for s in tl["sections"]:
        sid, L = s["id"], s["duration"]
        clip = out / "clips" / f"{sid}.mp4"
        if not clip.exists():
            sys.exit(f"クリップがありません: {clip}（tools/comfy_h3.py を実行してください）")
        info = probe(clip)
        slow = max(1.0, L / info["duration"])
        if slow > 1.0:
            print(f"  {sid}: 映像 {info['duration']:.2f}秒 < ナレ {L:.2f}秒 → {slow:.2f}倍スロー")

        seg = work / f"v_{sid}.mp4"
        vf = (f"setpts=PTS*{slow:.5f},scale={W}:{H}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H},fps={FPS},setsar=1")
        run_ffmpeg(["-i", clip, "-an", "-vf", vf, "-t", f"{L:.3f}", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "18", "-pix_fmt", "yuv420p", seg])
        v_list.append(seg)

        amb = work / f"a_{sid}.wav"
        asset = find_asset("ambience", amb_by_sec.get(sid) or "")
        if asset:
            run_ffmpeg(["-stream_loop", "-1", "-i", asset, "-t", f"{L:.3f}", *AR, amb])
        elif r["use_clip_audio_as_ambience"] and info["has_audio"]:
            run_ffmpeg(["-i", clip, "-vn", "-af", f"atempo={1 / slow:.5f},apad", "-t", f"{L:.3f}", *AR, amb])
        else:
            run_ffmpeg(["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{L:.3f}", amb])
        a_list.append(amb)

    def concat(files, dest, copy):
        lst = work / f"{dest.stem}.txt"
        lst.write_text("".join(f"file '{f.as_posix()}'\n" for f in files), encoding="utf-8")
        run_ffmpeg(["-f", "concat", "-safe", "0", "-i", lst, *(["-c", "copy"] if copy else AR), dest])

    video = work / "video.mp4"
    concat(v_list, video, copy=True)
    ambience = work / "ambience.wav"
    concat(a_list, ambience, copy=False)
    narration = work / "narration.wav"
    concat([out / "narration" / f"{s['id']}.wav" for s in tl["sections"]], narration, copy=False)

    # SE / BGM の配置
    inputs = [video, narration, ambience]
    filters = ["[1:a]aresample=48000,volume=1.0[narr]", f"[2:a]volume={r['ambience_volume']}[amb]"]
    mix = ["[narr]", "[amb]"]
    for s in tl["sections"]:
        for line in s["lines"]:
            for cue in line.get("cues", []):
                t = line["start"] + cue.get("offset", 0.0)
                kind, folder = ("bgm", "bgm") if "bgm" in cue else ("sfx", "sfx")
                asset = find_asset(folder, cue[kind])
                if not asset:
                    print(f"  ※ 素材なし（スキップ）: assets/{folder}/{cue[kind]}.wav  @{t:.2f}秒")
                    continue
                idx = len(inputs)
                inputs.append(asset)
                ms = int(t * 1000)
                label = f"c{idx}"
                if kind == "bgm":
                    filters.append(f"[{idx}:a]aresample=48000,atrim=0:{total - t:.3f},"
                                   f"afade=t=in:d={r['bgm_fade_in']},volume={r['bgm_volume']},"
                                   f"adelay={ms}|{ms}[{label}]")
                else:
                    filters.append(f"[{idx}:a]aresample=48000,volume={r['sfx_volume']},adelay={ms}|{ms}[{label}]")
                mix.append(f"[{label}]")
                print(f"  {kind.upper()} {asset.name} @{t:.2f}秒")
    fo = r["fade_out"]
    filters.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,"
                   f"afade=t=out:st={total - fo:.3f}:d={fo},loudnorm=I={r['loudness_lufs']}:TP=-1.5:LRA=11[aout]")
    filters.append(f"[0:v]fade=t=out:st={total - fo:.3f}:d={fo}[vout]")

    cmd = []
    for f in inputs:
        cmd += ["-i", f]
    final = out / "final.mp4"
    run_ffmpeg([*cmd, "-filter_complex", ";".join(filters), "-map", "[vout]", "-map", "[aout]",
                "-t", f"{total:.3f}", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", *AR, "-movflags", "+faststart", final])

    srt = []
    n = 1
    for s in tl["sections"]:
        for line in s["lines"]:
            srt.append(f"{n}\n{srt_time(line['start'])} --> {srt_time(line['start'] + line['duration'])}\n{line['text']}\n")
            n += 1
    (out / "subtitles.srt").write_text("\n".join(srt), encoding="utf-8")

    print(f"\n完成: {final}（{probe(final)['duration']:.2f}秒）")
    print(f"字幕: {out / 'subtitles.srt'}")


if __name__ == "__main__":
    main()
