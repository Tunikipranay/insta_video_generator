"""
Stage 3: render all scenes in a project's scenes.py, concatenate in order,
and export 16:9 (YouTube) + 9:16 (Instagram Reels / Shorts) versions.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config  # noqa: E402

QUALITY_DIRS = {"-ql": "480p15", "-qm": "720p30", "-qh": "1080p60"}


def scene_classes(scenes_py: Path):
    """(deep, teaser) scene class names, each sorted by their number prefix."""
    names = re.findall(r"^class\s+(\w+)\s*\(", scenes_py.read_text(), re.M)
    deep = sorted(n for n in names if re.match(r"S\d+_", n))
    teaser = sorted(n for n in names if re.match(r"T\d+_", n))
    return deep, teaser


def run(cmd, **kw):
    print("$", " ".join(str(c) for c in cmd))
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    p = subprocess.run([str(c) for c in cmd], env=env,
                       capture_output=True, text=True, **kw)
    if p.returncode != 0:
        tail = "\n".join(((p.stdout or "") + "\n" + (p.stderr or ""))
                         .strip().splitlines()[-40:])
        print(tail)
        raise subprocess.CalledProcessError(p.returncode, p.args,
                                            output=p.stdout, stderr=p.stderr)


VERTICAL_VF = ("split[a][b];"
               "[a]scale=1080:1920:force_original_aspect_ratio=increase,"
               "crop=1080:1920,gblur=sigma=30,eq=brightness=-0.08[bg];"
               "[b]scale=1080:-2[fg];"
               "[bg][fg]overlay=(W-w)/2:(H-h)/2")


def concat(clips, out_path):
    lst = out_path.with_suffix(".txt")
    lst.write_text("".join(f"file '{c}'\n" for c in clips))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", out_path])


def verticalize(src, dst):
    run(["ffmpeg", "-y", "-i", src, "-filter_complex", VERTICAL_VF,
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p", dst])


def render(project_dir: str, quality: str = None):
    quality = quality or config.QUALITY
    workdir = Path(project_dir).resolve()
    scenes_py = workdir / "scenes.py"
    deep, teaser = scene_classes(scenes_py)
    if not deep:
        raise SystemExit("No S<number>_ scene classes found in scenes.py")
    print(f"Rendering {len(deep)} deep scenes: {deep}")
    if teaser:
        print(f"Rendering {len(teaser)} teaser scenes: {teaser}")

    media = workdir / "media"
    for s in deep + teaser:
        run(["manim", quality, "--disable_caching", "--media_dir", media,
             scenes_py, s], cwd=ROOT)  # cwd=ROOT so house_style/config import

    qdir = QUALITY_DIRS[quality]
    clip = lambda s: media / "videos" / "scenes" / qdir / f"{s}.mp4"
    missing = [s for s in deep + teaser if not clip(s).exists()]
    if missing:
        raise SystemExit(f"Missing rendered clips: {missing}")

    out = workdir / "output"
    out.mkdir(exist_ok=True)

    # deep explainer: 16:9 master (YouTube)
    horizontal = out / "video_16x9.mp4"
    concat([clip(s) for s in deep], horizontal)

    # teaser: 9:16 master (Reels/Shorts) — only if teaser scenes exist
    teaser_v = None
    if teaser:
        t16 = out / "teaser_16x9.mp4"
        concat([clip(s) for s in teaser], t16)
        teaser_v = out / "teaser_9x16.mp4"
        verticalize(t16, teaser_v)
    else:
        # legacy single-format projects: keep the vertical of the main video
        teaser_v = out / "video_9x16.mp4"
        verticalize(horizontal, teaser_v)

    print(f"\n[ok] {horizontal}\n[ok] {teaser_v}")
    return horizontal, teaser_v


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python pipeline/render.py projects/<slug> [-ql|-qm|-qh]")
    render(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
