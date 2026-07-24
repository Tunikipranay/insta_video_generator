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
    """Scene classes in file order (S1_..., S2_... naming keeps them sorted)."""
    names = re.findall(r"^class\s+(\w+)\s*\(", scenes_py.read_text(), re.M)
    return sorted(n for n in names if re.match(r"S\d+_", n))


def run(cmd, **kw):
    print("$", " ".join(str(c) for c in cmd))
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    subprocess.run([str(c) for c in cmd], check=True, env=env, **kw)


def render(project_dir: str, quality: str = None):
    quality = quality or config.QUALITY
    workdir = Path(project_dir).resolve()
    scenes_py = workdir / "scenes.py"
    scenes = scene_classes(scenes_py)
    if not scenes:
        raise SystemExit("No S<number>_ scene classes found in scenes.py")
    print(f"Rendering {len(scenes)} scenes: {scenes}")

    media = workdir / "media"
    for s in scenes:
        run(["manim", quality, "--disable_caching", "--media_dir", media,
             scenes_py, s], cwd=ROOT)  # cwd=ROOT so house_style/config import

    qdir = QUALITY_DIRS[quality]
    clips = [media / "videos" / "scenes" / qdir / f"{s}.mp4" for s in scenes]
    missing = [c for c in clips if not c.exists()]
    if missing:
        raise SystemExit(f"Missing rendered clips: {missing}")

    out = workdir / "output"
    out.mkdir(exist_ok=True)
    concat_list = out / "concat.txt"
    concat_list.write_text("".join(f"file '{c}'\n" for c in clips))

    horizontal = out / "video_16x9.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
         "-c", "copy", horizontal])

    # 9:16 for Instagram: center the 16:9 frame over a blurred, scaled copy.
    vertical = out / "video_9x16.mp4"
    vf = ("split[a][b];"
          "[a]scale=1080:1920:force_original_aspect_ratio=increase,"
          "crop=1080:1920,gblur=sigma=30,eq=brightness=-0.08[bg];"
          "[b]scale=1080:-2[fg];"
          "[bg][fg]overlay=(W-w)/2:(H-h)/2")
    run(["ffmpeg", "-y", "-i", horizontal, "-filter_complex", vf,
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p", vertical])

    print(f"\n[ok] {horizontal}\n[ok] {vertical}")
    return horizontal, vertical


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python pipeline/render.py projects/<slug> [-ql|-qm|-qh]")
    render(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
