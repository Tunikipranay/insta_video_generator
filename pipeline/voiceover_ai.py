"""
AI voiceover stage (free, local, natural female voice via Piper).

For each part of script.json (deep video sections + teaser sections):
  1. synthesize narration at a calm teacher pace (config.SPEECH_*)
  2. auto-sync: a scene whose narration runs long is slowed slightly
     (never sped up); shorter narration gets silence padding
  3. rebuild the video, mix voice + soft whoosh transitions + auto-ducked
     ambient music, master to -16 LUFS (social media standard)

Usage:
  python pipeline/voiceover_ai.py projects/<slug> [voice_onnx_path]

Outputs in projects/<slug>/output/:
  FINAL_youtube_ai_voice.mp4     deep explainer, 16:9
  FINAL_instagram_teaser.mp4     teaser, 9:16 (when the script has one)
  FINAL_instagram_ai_voice.mp4   legacy: vertical of the main video when
                                 the script has no teaser
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config  # noqa: E402

DEFAULT_VOICE = ROOT / "tts" / "vits-piper-en_US-hfc_female-medium" / "en_US-hfc_female-medium.onnx"
QUALITY_DIRS = ["1080p60", "720p30", "480p15"]
LEAD_IN = 0.35          # silence before each section's speech
MAX_STRETCH = 1.6       # never slow a scene more than this

VERTICAL_VF = ("split[a][b];"
               "[a]scale=1080:1920:force_original_aspect_ratio=increase,"
               "crop=1080:1920,gblur=sigma=30,eq=brightness=-0.08[bg];"
               "[b]scale=1080:-2[fg];"
               "[bg][fg]overlay=(W-w)/2:(H-h)/2")


def sh(cmd, **kw):
    subprocess.run([str(c) for c in cmd], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kw)


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(out.stdout.strip())


def scene_clips(workdir):
    """(deep_clips, teaser_clips) from the newest rendered quality dir."""
    scenes_py = workdir / "scenes.py"
    names = re.findall(r"^class\s+(\w+)\s*\(", scenes_py.read_text(), re.M)
    deep = sorted(n for n in names if re.match(r"S\d+_", n))
    teaser = sorted(n for n in names if re.match(r"T\d+_", n))
    for q in QUALITY_DIRS:
        d = workdir / "media" / "videos" / "scenes" / q
        dc = [d / f"{n}.mp4" for n in deep]
        tc = [d / f"{n}.mp4" for n in teaser]
        if all(c.exists() for c in dc + tc) and dc:
            return dc, tc
    raise SystemExit("Rendered scene clips not found — run render.py first.")


def synthesize(text, voice, out_wav):
    base = [sys.executable, "-m", "piper", "-m", str(voice), "-f", str(out_wav)]
    pacing = ["--length-scale", str(config.SPEECH_LENGTH_SCALE),
              "--sentence-silence", str(config.SPEECH_SENTENCE_SILENCE)]
    for cmd in (base + pacing, base):        # old piper: retry without pacing
        p = subprocess.run(cmd, input=text.encode(), capture_output=True)
        if p.returncode == 0 and out_wav.exists():
            return
    raise SystemExit(f"piper failed: {p.stderr.decode()[:400]}")


def build(tag, sections, clips, voice, tmp, out_path, vertical=False):
    """Voice one part (deep or teaser) and write the final mixed video."""
    seg_videos, seg_audios, starts, t = [], [], [], 0.0
    for i, (sec, clip) in enumerate(zip(sections, clips)):
        wav = tmp / f"{tag}_sec{i}.wav"
        if not wav.exists():
            synthesize(sec["narration"], voice, wav)
        a_dur = duration(wav) + LEAD_IN + 0.3
        v_dur = duration(clip)
        factor = min(max(a_dur / v_dur, 1.0), MAX_STRETCH)
        # if even max slow-down can't cover the narration, freeze the last
        # frame for the remainder so the voice is never cut off
        extra = max(0.0, a_dur - v_dur * factor)

        seg_v = tmp / f"{tag}_vid{i}.mp4"
        vf = f"setpts={factor:.4f}*PTS" if factor > 1.01 else "null"
        if extra > 0.05:
            vf += f",tpad=stop_mode=clone:stop_duration={extra:.3f}"
        sh(["ffmpeg", "-y", "-i", clip, "-vf", vf, "-r", "30",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-an", seg_v])
        target = duration(seg_v)

        seg_a = tmp / f"{tag}_aud{i}.wav"
        ms = int(LEAD_IN * 1000)
        sh(["ffmpeg", "-y", "-i", wav, "-af", f"adelay={ms}|{ms},apad",
            "-ar", "44100", "-ac", "2", "-t", f"{target:.3f}", seg_a])

        seg_videos.append(seg_v); seg_audios.append(seg_a); starts.append(t)
        t += target
        print(f"  [{tag}] {clip.stem}: video {v_dur:.1f}s -> {target:.1f}s "
              f"(voice {a_dur - LEAD_IN - 0.3:.1f}s, stretch x{factor:.2f})")
    total = t
    print(f"  [{tag}] total: {total:.1f}s")

    for name, items in [("v", seg_videos), ("a", seg_audios)]:
        (tmp / f"{tag}_concat_{name}.txt").write_text(
            "".join(f"file '{x}'\n" for x in items))
    full_v = tmp / f"{tag}_full.mp4"
    sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", tmp / f"{tag}_concat_v.txt", "-c", "copy", full_v])
    vo_raw = tmp / f"{tag}_vo_raw.wav"
    sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", tmp / f"{tag}_concat_a.txt", vo_raw])
    vo = tmp / f"{tag}_vo.wav"
    sh(["ffmpeg", "-y", "-i", vo_raw, "-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", vo])

    music = ROOT / "music" / "bg_generated.wav"
    whoosh = ROOT / "music" / "whoosh.wav"
    inputs = ["-i", full_v, "-i", vo, "-stream_loop", "-1", "-i", music]
    fc = ["[2:a]volume=0.16[m0];[m0][1:a]sidechaincompress="
          "threshold=0.02:ratio=6:attack=80:release=500[duck]"]
    mix_ins = ["[1:a]", "[duck]"]
    for j, s in enumerate(starts[1:]):
        inputs += ["-i", str(whoosh)]
        ms = int(s * 1000)
        fc.append(f"[{3 + j}:a]volume=0.22,adelay={ms}|{ms}[w{j}]")
        mix_ins.append(f"[w{j}]")
    fc.append("".join(mix_ins) +
              f"amix=inputs={len(mix_ins)}:duration=first:normalize=0[aout]")

    mixed = tmp / f"{tag}_mixed.mp4"
    sh(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fc),
        "-map", "0:v", "-map", "[aout]", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", mixed])

    if vertical:
        sh(["ffmpeg", "-y", "-i", mixed, "-filter_complex", VERTICAL_VF,
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-c:a", "copy", out_path])
    else:
        sh(["ffmpeg", "-y", "-i", mixed, "-c", "copy", out_path])
    print(f"[ok] {out_path}")


def main(project_dir, voice=None):
    voice = Path(voice) if voice else DEFAULT_VOICE
    workdir = Path(project_dir).resolve()
    script = json.loads((workdir / "script.json").read_text())
    deep_clips, teaser_clips = scene_clips(workdir)
    deep_secs = script["sections"]
    teaser_secs = script.get("teaser", {}).get("sections", [])
    if len(deep_clips) != len(deep_secs):
        raise SystemExit(f"{len(deep_clips)} deep scenes vs "
                         f"{len(deep_secs)} sections")

    tmp = workdir / "output" / "vo_build"
    tmp.mkdir(parents=True, exist_ok=True)

    build("deep", deep_secs, deep_clips, voice, tmp,
          workdir / "output" / "FINAL_youtube_ai_voice.mp4")

    if teaser_secs and len(teaser_clips) == len(teaser_secs):
        build("teaser", teaser_secs, teaser_clips, voice, tmp,
              workdir / "output" / "FINAL_instagram_teaser.mp4", vertical=True)
    elif not teaser_secs:
        # legacy project: vertical of the main video
        src = workdir / "output" / "FINAL_youtube_ai_voice.mp4"
        dst = workdir / "output" / "FINAL_instagram_ai_voice.mp4"
        sh(["ffmpeg", "-y", "-i", src, "-filter_complex", VERTICAL_VF,
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-c:a", "copy", dst])
        print(f"[ok] {dst}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python pipeline/voiceover_ai.py projects/<slug> [voice.onnx]")
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
