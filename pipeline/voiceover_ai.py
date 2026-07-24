"""
AI voiceover stage (free, local, natural female voice via Piper).

Per section of script.json:
  1. synthesize narration
  2. auto-sync: if narration runs longer than the scene, the scene is
     slowed slightly to fit (never sped up — animations stay smooth);
     if shorter, the narration is padded with silence
  3. rebuild the full video, mix voice + soft whoosh transitions +
     auto-ducked ambient music, master to -16 LUFS (social media standard)

Usage:
  python pipeline/voiceover_ai.py projects/<slug> [voice_onnx_path]

Outputs in projects/<slug>/output/:
  FINAL_youtube_ai_voice.mp4    (16:9)
  FINAL_instagram_ai_voice.mp4  (9:16)
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VOICE = ROOT / "tts" / "vits-piper-en_US-hfc_female-medium" / "en_US-hfc_female-medium.onnx"
QUALITY_DIRS = ["1080p60", "720p30", "480p15"]
LEAD_IN = 0.35          # silence before each section's speech
MAX_STRETCH = 1.6       # never slow a scene more than this


def sh(cmd, **kw):
    subprocess.run([str(c) for c in cmd], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kw)


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(out.stdout.strip())


def scene_clips(workdir):
    scenes_py = workdir / "scenes.py"
    names = sorted(n for n in re.findall(r"^class\s+(\w+)\s*\(",
                                         scenes_py.read_text(), re.M)
                   if re.match(r"S\d+_", n))
    for q in QUALITY_DIRS:
        d = workdir / "media" / "videos" / "scenes" / q
        clips = [d / f"{n}.mp4" for n in names]
        if all(c.exists() for c in clips):
            return clips
    raise SystemExit("Rendered scene clips not found — run render.py first.")


def synthesize(text, voice, out_wav):
    p = subprocess.run([sys.executable, "-m", "piper", "-m", str(voice),
                        "-f", str(out_wav)], input=text.encode(),
                       capture_output=True)
    if p.returncode != 0 or not out_wav.exists():
        raise SystemExit(f"piper failed: {p.stderr.decode()[:400]}")


def main(project_dir, voice=None):
    voice = Path(voice) if voice else DEFAULT_VOICE
    workdir = Path(project_dir).resolve()
    script = json.loads((workdir / "script.json").read_text())
    sections = script["sections"]
    clips = scene_clips(workdir)
    if len(clips) != len(sections):
        raise SystemExit(f"{len(clips)} scenes vs {len(sections)} sections")

    tmp = workdir / "output" / "vo_build"
    tmp.mkdir(parents=True, exist_ok=True)

    seg_videos, seg_audios, starts, t = [], [], [], 0.0
    for i, (sec, clip) in enumerate(zip(sections, clips)):
        wav = tmp / f"sec{i}.wav"
        if not wav.exists():
            synthesize(sec["narration"], voice, wav)
        a_dur = duration(wav) + LEAD_IN + 0.3
        v_dur = duration(clip)
        target = max(v_dur, a_dur)
        factor = min(target / v_dur, MAX_STRETCH)
        target = v_dur * factor

        seg_v = tmp / f"vid{i}.mp4"
        if factor > 1.01:
            sh(["ffmpeg", "-y", "-i", clip, "-vf", f"setpts={factor:.4f}*PTS",
                "-r", "30", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-an", seg_v])
        else:
            sh(["ffmpeg", "-y", "-i", clip, "-c:v", "libx264", "-preset",
                "fast", "-crf", "18", "-r", "30", "-pix_fmt", "yuv420p",
                "-an", seg_v])
        target = duration(seg_v)

        seg_a = tmp / f"aud{i}.wav"
        delay_ms = int(LEAD_IN * 1000)
        sh(["ffmpeg", "-y", "-i", wav, "-af",
            f"adelay={delay_ms}|{delay_ms},apad", "-ar", "44100", "-ac", "2",
            "-t", f"{target:.3f}", seg_a])

        seg_videos.append(seg_v)
        seg_audios.append(seg_a)
        starts.append(t)
        t += target
        print(f"  {clip.stem}: video {v_dur:.1f}s -> {target:.1f}s "
              f"(voice {a_dur - LEAD_IN - 0.3:.1f}s, stretch x{factor:.2f})")

    total = t
    print(f"total: {total:.1f}s")

    # concat video
    cat_v = tmp / "concat_v.txt"
    cat_v.write_text("".join(f"file '{v}'\n" for v in seg_videos))
    full_v = tmp / "full_video.mp4"
    sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", cat_v,
        "-c", "copy", full_v])

    # concat voice track + loudness-normalize
    cat_a = tmp / "concat_a.txt"
    cat_a.write_text("".join(f"file '{a}'\n" for a in seg_audios))
    vo_raw = tmp / "vo_raw.wav"
    sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", cat_a, vo_raw])
    vo = tmp / "vo.wav"
    sh(["ffmpeg", "-y", "-i", vo_raw, "-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", vo])

    # final mix: voice + whooshes at section starts + ducked music
    music = ROOT / "music" / "bg_generated.wav"
    whoosh = ROOT / "music" / "whoosh.wav"
    inputs = ["-i", full_v, "-i", vo, "-stream_loop", "-1", "-i", music]
    w_starts = [s for s in starts[1:]]          # whoosh at each transition
    fc, mix_ins = [], ["[1:a]"]
    fc.append("[2:a]volume=0.16[m0];[m0][1:a]sidechaincompress="
              "threshold=0.02:ratio=6:attack=80:release=500[duck]")
    mix_ins.append("[duck]")
    for j, s in enumerate(w_starts):
        inputs += ["-i", str(whoosh)]
        idx = 3 + j
        ms = int(s * 1000)
        fc.append(f"[{idx}:a]volume=0.22,adelay={ms}|{ms}[w{j}]")
        mix_ins.append(f"[w{j}]")
    fc.append("".join(mix_ins) +
              f"amix=inputs={len(mix_ins)}:duration=first:normalize=0[aout]")

    out169 = workdir / "output" / "FINAL_youtube_ai_voice.mp4"
    sh(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fc),
        "-map", "0:v", "-map", "[aout]", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", out169])

    # vertical
    out916 = workdir / "output" / "FINAL_instagram_ai_voice.mp4"
    vf = ("split[a][b];"
          "[a]scale=1080:1920:force_original_aspect_ratio=increase,"
          "crop=1080:1920,gblur=sigma=30,eq=brightness=-0.08[bg];"
          "[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
    sh(["ffmpeg", "-y", "-i", out169, "-filter_complex", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-c:a", "copy", out916])

    print(f"[ok] {out169}\n[ok] {out916}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python pipeline/voiceover_ai.py projects/<slug> [voice.onnx]")
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
