"""③ 結合：クリップ＋ナレーション＋環境音＋SE＋オチのBGM を mp4 にまとめる。

  python tools/assemble.py 01-keiba      # → episodes/01-keiba/out/final.mp4（＋字幕 subtitles.srt）

素材（任意。無ければスキップして警告のみ）
  assets/ambience/<名前>.wav   … episode.json の section.ambience（無ければ H3 が生成した音を薄く敷く）
  assets/sfx/<名前>.wav        … line.cues の sfx
  assets/bgm/<名前>.wav        … line.cues の bgm（そこから最後まで流れる）

尺を決め打ちするシリーズ（section に source がある episode）
  source h3    … out/clips/<id>.mp4 に speed（区間ごとの再生速度）を当てる
  source opus  … out/clips/<id>.mp4（tools/opus_render.py が作る図解・画面）
  source reuse … reuse に書いた既存クリップの区間をつなぐ
  overlay      … out/overlays/<id>.mov（透過付き。opus_render.py が作る）があれば重ねる
  audio        … ambient（H3 の音を薄く）/ animal（H3 の鳴き声を大きめに）/ mute
  スローのコマ補間は config の render.interp（blend＝速い / minterpolate＝きれいだが遅い / none）。
  out/clips/<id>_rife.mp4（外部で補間済み・スロー適用済み）があればそれを優先する。
  解像度は episode.json の format.render が config より優先。format.bgm が false なら BGM を入れない。
"""
import argparse
import sys
from pathlib import Path

from common import find_asset, load_config, load_episode, load_json, out_dir, probe, run_ffmpeg

AR = ["-ar", "48000", "-ac", "2"]
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p"]


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def atempo_chain(rate):
    """atempo は 1 段 0.5〜100 倍なので、0.5 未満は分けて掛ける。"""
    parts = []
    while rate < 0.5:
        parts.append("atempo=0.5")
        rate /= 0.5
    parts.append(f"atempo={rate:.5f}")
    return ",".join(parts)


def interp_filter(rate, FPS, mode):
    if rate >= 1 or mode == "none":
        return f"fps={FPS}"
    if mode == "minterpolate":
        return f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
    return f"framerate=fps={FPS}"


def segments_of(s, clips):
    """(入力ファイル, 開始, 終了, 速度) のリスト。"""
    if s["source"] == "reuse":
        return [(clips / f"{r['clip']}.mp4", r["from"], r["to"], r.get("rate", 1)) for r in s["reuse"]]
    clip = clips / f"{s['id']}.mp4"
    rife = clips / f"{s['id']}_rife.mp4"
    if rife.exists():
        return [(rife, 0, None, 1)]
    if s.get("speed"):
        return [(clip, g["from"], g["to"], g["rate"]) for g in s["speed"]]
    return [(clip, 0, None, 1)]


def build_shot(s, L, clips, overlays, work, r, W, H, FPS):
    """1ショット分の映像（無音）と音声 wav を作る。"""
    segs = segments_of(s, clips)
    files = []
    for f, *_ in segs:
        if not f.exists():
            hint = "tools/opus_render.py" if s["source"] == "opus" else "tools/comfy_h3.py"
            sys.exit(f"クリップがありません: {f}（{hint} を実行してください）")
        if f not in files:
            files.append(f)
    idx = {f: i for i, f in enumerate(files)}
    mode = r.get("interp", "blend")

    fl, labels = [], []
    for k, (f, a, b, rate) in enumerate(segs):
        tr = f"trim=start={a}" + (f":end={b}" if b is not None else "")
        fl.append(f"[{idx[f]}:v]{tr},setpts=(PTS-STARTPTS)/{rate},{interp_filter(rate, FPS, mode)},"
                  f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1[s{k}]")
        labels.append(f"[s{k}]")
    fl.append(f"{''.join(labels)}concat=n={len(labels)}:v=1:a=0,tpad=stop_mode=clone:stop_duration={L:.3f}[cat]")
    inputs = [x for f in files for x in ("-i", f)]
    ov = overlays / f"{s['id']}.mov"
    if ov.exists():
        inputs += ["-i", ov]
        fl.append(f"[{len(files)}:v]scale={W}:{H},format=rgba[ov];[cat][ov]overlay=0:0:eof_action=pass[v]")
    else:
        if s.get("overlay"):
            print(f"  ※ 重ねる素材なし（スキップ）: {ov.name}  … {s['overlay']}")
        fl.append("[cat]null[v]")
    seg = work / f"v_{s['id']}.mp4"
    run_ffmpeg([*inputs, "-filter_complex", ";".join(fl), "-map", "[v]", "-t", f"{L:.3f}", "-r", str(FPS), *ENC, seg])

    amb = work / f"a_{s['id']}.wav"
    audio = s.get("audio", "mute")
    src_info = probe(segs[0][0]) if s["source"] == "h3" else {"has_audio": False}
    if audio in ("ambient", "animal") and src_info["has_audio"]:
        vol = r["ambience_volume"] if audio == "ambient" else r.get("animal_volume", 1.0)
        af, al = [], []
        for k, (f, a, b, rate) in enumerate(segs):
            tr = f"atrim=start={a}" + (f":end={b}" if b is not None else "")
            af.append(f"[0:a]{tr},asetpts=PTS-STARTPTS" + (f",{atempo_chain(rate)}" if rate != 1 else "") + f"[a{k}]")
            al.append(f"[a{k}]")
        af.append(f"{''.join(al)}concat=n={len(al)}:v=0:a=1,volume={vol},apad[aout]")
        run_ffmpeg(["-i", segs[0][0], "-filter_complex", ";".join(af), "-map", "[aout]", "-t", f"{L:.3f}", *AR, amb])
    else:
        run_ffmpeg(["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{L:.3f}", amb])
    return seg, amb


def build_legacy(sid, L, clip, amb_name, work, r, W, H, FPS):
    """ナレーションの長さに合わせる従来の作り方（ダーウィン風ショート）。"""
    if not clip.exists():
        sys.exit(f"クリップがありません: {clip}（tools/comfy_h3.py を実行してください）")
    info = probe(clip)
    slow = max(1.0, L / info["duration"])
    if slow > 1.0:
        print(f"  {sid}: 映像 {info['duration']:.2f}秒 < ナレ {L:.2f}秒 → {slow:.2f}倍スロー")

    seg = work / f"v_{sid}.mp4"
    vf = (f"setpts=PTS*{slow:.5f},scale={W}:{H}:force_original_aspect_ratio=increase,"
          f"crop={W}:{H},fps={FPS},setsar=1")
    run_ffmpeg(["-i", clip, "-an", "-vf", vf, "-t", f"{L:.3f}", *ENC, seg])

    amb = work / f"a_{sid}.wav"
    asset = find_asset("ambience", amb_name or "")
    if asset:
        run_ffmpeg(["-stream_loop", "-1", "-i", asset, "-t", f"{L:.3f}", *AR, amb])
    elif r["use_clip_audio_as_ambience"] and info["has_audio"]:
        run_ffmpeg(["-i", clip, "-vn", "-af", f"atempo={1 / slow:.5f},apad", "-t", f"{L:.3f}", *AR, amb])
    else:
        run_ffmpeg(["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{L:.3f}", amb])
    return seg, amb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--only", nargs="*", default=[], help="このショットだけ作り直して確認用に out/work に残す（最終結合はしない）")
    args = ap.parse_args()

    r = load_config()["render"]
    ep_dir, ep = load_episode(args.episode)
    fmt = ep.get("format", {})
    r = {**r, **fmt.get("render", {})}
    out = Path(ep_dir, "out")
    tl = load_json(out / "timeline.json")
    work = out_dir(ep_dir, "work")
    clips, overlays = out / "clips", out / "overlays"
    total = tl["total"]
    W, H, FPS = r["width"], r["height"], r["fps"]
    by_id = {s["id"]: s for s in ep["sections"]}
    use_bgm = fmt.get("bgm", True)

    v_list, a_list = [], []
    for s in tl["sections"]:
        sid, L = s["id"], s["duration"]
        sec = by_id[sid]
        if args.only and sid not in args.only:
            continue
        if "source" in sec:
            seg, amb = build_shot(sec, L, clips, overlays, work, r, W, H, FPS)
            print(f"  ✓ {sid:<6} {sec['source']:<5} {L:5.2f}秒  {sec['label']}")
        else:
            seg, amb = build_legacy(sid, L, clips / f"{sid}.mp4", sec.get("ambience"), work, r, W, H, FPS)
        v_list.append(seg)
        a_list.append(amb)
    if args.only:
        print(f"\n確認用: {work}（v_<ID>.mp4）")
        return

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
    filters = ["[1:a]aresample=48000,volume=1.0[narr]", "[2:a]aresample=48000[amb]"
               if any("source" in s for s in ep["sections"]) else f"[2:a]volume={r['ambience_volume']}[amb]"]
    mix = ["[narr]", "[amb]"]
    for s in tl["sections"]:
        for line in s["lines"]:
            for cue in line.get("cues", []):
                t = line["start"] + cue.get("offset", 0.0)
                kind, folder = ("bgm", "bgm") if "bgm" in cue else ("sfx", "sfx")
                if kind == "bgm" and not use_bgm:
                    continue
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
