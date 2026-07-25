"""
Stage 1+2: topic -> script JSON -> Manim scene code.

With ANTHROPIC_API_KEY set, this is fully automatic.
Without it, the prompts are written to disk so you can paste them into
claude.ai (free tier) and save the replies manually.
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config  # noqa: E402


def _slug(topic: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", topic.lower()).strip("_")[:48].rstrip("_")


def _call_claude(prompt: str, max_tokens: int = 24000) -> str:
    import anthropic  # pip install anthropic
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    msg = client.messages.create(
        model=config.AI_MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    if msg.stop_reason == "max_tokens":
        print(f"[warn] reply hit the {max_tokens}-token limit and was cut off")
    return msg.content[0].text


def _strip_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```[a-z]*\n?", "", text)
    text = re.sub(r"\n?```$", "", text)
    return text


def generate(topic: str) -> Path:
    slug = _slug(topic)
    workdir = ROOT / "projects" / slug
    workdir.mkdir(parents=True, exist_ok=True)

    script_prompt = (ROOT / "prompts" / "script_prompt.txt").read_text().format(
        topic=topic, target_seconds=config.TARGET_DURATION_SECONDS)

    have_key = bool(os.environ.get("ANTHROPIC_API_KEY"))

    # ---- Stage 1: script -------------------------------------------------
    script_path = workdir / "script.json"
    if script_path.exists():
        print(f"[skip] {script_path} already exists")
    elif have_key:
        print(f"[ai] writing script for: {topic}")
        raw = _strip_fences(_call_claude(script_prompt))
        script = json.loads(raw)
        total = sum(s["seconds"] for s in script["sections"])
        if total > config.MAX_DURATION_SECONDS:
            raise SystemExit(f"Deep script too long ({total}s) — regenerate.")
        t_total = sum(s["seconds"] for s in
                      script.get("teaser", {}).get("sections", []))
        if t_total > config.TEASER_MAX_SECONDS:
            raise SystemExit(f"Teaser too long ({t_total}s) — regenerate.")
        script_path.write_text(json.dumps(script, indent=2))
    else:
        p = workdir / "PASTE_ME_script_prompt.txt"
        p.write_text(script_prompt)
        print(f"No ANTHROPIC_API_KEY. Paste {p} into claude.ai, save the JSON "
              f"reply as {script_path}, then re-run.")
        return workdir

    # ---- Stage 2: scenes -------------------------------------------------
    scenes_path = workdir / "scenes.py"
    if scenes_path.exists():
        print(f"[skip] {scenes_path} already exists")
    elif have_key:
        print("[ai] writing Manim scenes")
        from pipeline.repair import sanitize, validate
        scene_prompt = (ROOT / "prompts" / "scene_prompt.txt").read_text().format(
            script_json=script_path.read_text())
        prompt, code = scene_prompt, None
        for attempt in range(3):
            code = sanitize(_strip_fences(_call_claude(prompt)))
            problem = validate(code)
            if problem is None:
                break
            print(f"[retry {attempt + 1}/3] scene code rejected: {problem}")
            prompt = (scene_prompt +
                      f"\n\nA previous attempt was rejected: {problem}\n"
                      "Write the complete file, all nine scene classes, "
                      "in full.")
        else:
            (workdir / "scenes_rejected.py").write_text(code)
            raise SystemExit(
                "The model could not produce a valid scenes.py in 3 tries. "
                f"Last attempt saved to {workdir / 'scenes_rejected.py'}.")
        scenes_path.write_text(code)
    else:
        scene_prompt = (ROOT / "prompts" / "scene_prompt.txt").read_text().format(
            script_json=script_path.read_text())
        p = workdir / "PASTE_ME_scene_prompt.txt"
        p.write_text(scene_prompt)
        print(f"Paste {p} into claude.ai, save the Python reply as "
              f"{scenes_path}, then re-run.")
        return workdir

    # ---- Narration sheet for your voiceover recording --------------------
    script = json.loads(script_path.read_text())
    lines = [f"NARRATION SHEET — {script['topic']}",
             "Record one take per section; keep each within its time box.", ""]
    for part, secs in [("DEEP VIDEO", script["sections"]),
                       ("TEASER", script.get("teaser", {}).get("sections", []))]:
        if not secs:
            continue
        lines += [f"== {part} ({sum(s['seconds'] for s in secs)}s) ==", ""]
        t = 0
        for s in secs:
            lines.append(f"[{t:>3}s – {t + s['seconds']:>3}s]  ({s['id']})")
            lines.append(f"  {s['narration']}")
            lines.append("")
            t += s["seconds"]
    (workdir / "narration_sheet.txt").write_text("\n".join(lines))
    print(f"[ok] project ready: {workdir}")
    return workdir


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python pipeline/generate.py "python decorators"')
    generate(" ".join(sys.argv[1:]))
