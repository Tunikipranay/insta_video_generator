"""
Stage 4: mix YOUR recorded voiceover (+ optional background music) onto the
rendered video. Music is auto-ducked under the voice.

Record your voiceover reading narration_sheet.txt (phone voice memo is fine),
drop it in the project folder as voiceover.wav / .mp3 / .m4a, then run this.
Optional: put a music track at music/bg.mp3 (use royalty-free, e.g. the
YouTube Audio Library).
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def find_voiceover(workdir: Path):
    for ext in ("wav", "mp3", "m4a", "aac", "ogg"):
        p = workdir / f"voiceover.{ext}"
        if p.exists():
            return p
    return None


def run(cmd):
    print("$", " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], check=True)


def assemble(project_dir: str):
    workdir = Path(project_dir).resolve()
    vo = find_voiceover(workdir)
    if not vo:
        raise SystemExit(f"Put your recording at {workdir}/voiceover.wav "
                         "(or .mp3/.m4a) first. Read narration_sheet.txt as "
                         "your script.")
    music = ROOT / "music" / "bg.mp3"

    for src_name, out_name in [("video_16x9.mp4", "FINAL_youtube.mp4"),
                               ("video_9x16.mp4", "FINAL_instagram.mp4")]:
        src = workdir / "output" / src_name
        if not src.exists():
            print(f"[skip] {src} not rendered yet")
            continue
        out = workdir / "output" / out_name
        if music.exists():
            # sidechain-duck music under the voice, then mix
            fc = ("[2:a]aloop=loop=-1:size=2e9,volume=0.35[m];"
                  "[m][1:a]sidechaincompress=threshold=0.03:ratio=8:"
                  "attack=50:release=400[duck];"
                  "[1:a][duck]amix=inputs=2:duration=first:"
                  "dropout_transition=2[aout]")
            run(["ffmpeg", "-y", "-i", src, "-i", vo, "-i", music,
                 "-filter_complex", fc, "-map", "0:v", "-map", "[aout]",
                 "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                 "-shortest", out])
        else:
            run(["ffmpeg", "-y", "-i", src, "-i", vo,
                 "-map", "0:v", "-map", "1:a",
                 "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                 "-shortest", out])
        print(f"[ok] {out}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python pipeline/assemble.py projects/<slug>")
    assemble(sys.argv[1])
