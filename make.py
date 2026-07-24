"""
2min_ai video factory — one command from topic to published-ready video.

  python make.py "python decorators"                 # full auto, AI voice
  python make.py "python decorators" --draft         # fast 480p preview
  python make.py "python decorators" --voice none    # silent masters only
                                                     # (record your own VO)
  python make.py "python decorators" --voice path/to/other-voice.onnx

Requires ANTHROPIC_API_KEY for automatic script/scene writing.
Without it, the prompts are saved to files — paste them into claude.ai
(free), save the replies where instructed, and re-run the same command.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from pipeline.generate import generate            # noqa: E402
from pipeline.render import render                # noqa: E402
from pipeline import voiceover_ai                 # noqa: E402
from pipeline.repair import repair, sanitize      # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="topic -> finished short video")
    ap.add_argument("topic", nargs="+", help="video topic, in quotes")
    ap.add_argument("--draft", action="store_true",
                    help="render fast 480p preview instead of 720p")
    ap.add_argument("--hq", action="store_true",
                    help="render 1080p60 (slow; for publishing)")
    ap.add_argument("--voice", default="ai",
                    help="'ai' (default), 'none' (silent, record your own), "
                         "or a path to a Piper .onnx voice")
    args = ap.parse_args()
    topic = " ".join(args.topic)
    quality = "-ql" if args.draft else ("-qh" if args.hq else "-qm")

    # 1. script + scenes (AI, or manual paste flow)
    workdir = generate(topic)
    if not (workdir / "scenes.py").exists():
        return  # manual mode: instructions were printed; re-run when saved

    # 2. render animation + build silent masters — with self-repair:
    # if AI-written scene code crashes, static-sanitize first, then ask
    # the model to fix its own bug and retry (twice at most).
    scenes_path = workdir / "scenes.py"
    for attempt in range(3):
        try:
            render(workdir, quality)
            break
        except subprocess.CalledProcessError as e:
            err = ((e.output or "") + "\n" + (e.stderr or "")).strip()
            if attempt == 0:
                cleaned = sanitize(scenes_path.read_text())
                if cleaned != scenes_path.read_text():
                    print("[repair] applied static API fixes, retrying...")
                    scenes_path.write_text(cleaned)
                    continue
            if attempt == 2 or not os.environ.get("ANTHROPIC_API_KEY"):
                raise SystemExit(
                    "Scene render failed. Fix the error above in "
                    f"{scenes_path} and re-run.")
            print("[repair] scene code crashed — asking the AI to fix it...")
            if not repair(scenes_path, err):
                raise SystemExit(f"Auto-repair failed; fix {scenes_path} manually.")

    # 3. audio
    if args.voice == "none":
        print("\nSilent masters ready. Record narration_sheet.txt as "
              f"{workdir}/voiceover.wav then run:\n"
              f"  python pipeline/assemble.py {workdir}")
        return
    voice = None if args.voice == "ai" else args.voice
    voiceover_ai.main(workdir, voice)
    print(f"\nDone. Publish these:\n"
          f"  {workdir}/output/FINAL_youtube_ai_voice.mp4   (deep explainer)\n"
          f"  {workdir}/output/FINAL_instagram_teaser.mp4   (reel -> YouTube)\n"
          f"Tip: watch it once before posting — if a scene needs a tweak, "
          f"edit {workdir}/scenes.py and re-run this command.")


if __name__ == "__main__":
    main()
