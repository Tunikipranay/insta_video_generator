"""
Scene-code self-repair.

Two layers of defense against AI-generated Manim code that crashes:

1. sanitize(code): static fixes for the most common invented kwargs,
   applied before the code is ever written to disk. Costs nothing.
2. repair(scenes_path, error_text): when a render still crashes, send the
   error + the full file back to the model and write the corrected file.
   make.py calls this automatically and retries the render.
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# common AI mistakes -> real Manim CE v0.20 API
ALIASES = [
    (r"\bfont_family\s*=", "font="),
    (r"(?<=[(,\s])lang\s*=", "language="),
    (r"(?<=[(,\s])size\s*=", "font_size="),
    (r"(?<=[(,\s])text_size\s*=", "font_size="),
    (r"\bScene\.play\b", "self.play"),
]

# scene classes the pipeline expects, by number prefix
REQUIRED_PREFIXES = ["S1_", "S2_", "S3_", "S4_", "S5_", "S6_",
                     "T1_", "T2_", "T3_"]


def sanitize(code: str) -> str:
    for pat, rep in ALIASES:
        code = re.sub(pat, rep, code)
    return code


def validate(code: str) -> str | None:
    """Return a human-readable problem with the scene file, or None if OK.

    Catches the two failure modes that used to reach the renderer: a reply
    truncated by the token limit (unparseable, and usually missing the last
    scenes) and a reply that silently dropped scene classes.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return (f"The file does not parse: {e.msg} at line {e.lineno}. "
                "It looks truncated or malformed — return the COMPLETE file.")
    names = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    missing = [p for p in REQUIRED_PREFIXES
               if not any(n.startswith(p) for n in names)]
    if missing:
        return (f"Missing scene classes starting with: {', '.join(missing)}. "
                f"Found only: {', '.join(names) or '(none)'}. "
                "Every scene class is required — return the COMPLETE file.")
    for n in ast.walk(tree):
        if isinstance(n, ast.ClassDef) and any(
                n.name.startswith(p) for p in REQUIRED_PREFIXES):
            if not any(isinstance(f, ast.FunctionDef) and f.name == "construct"
                       for f in n.body):
                return f"Class {n.name} has no construct(self) method."
    return None


REPAIR_PROMPT = """You are debugging Manim Community Edition v0.20 scene code
for an automated video pipeline. The file below crashed during rendering.

ERROR (from manim):
{error}

FULL FILE:
{code}

Fix the crash — and any other invalid Manim API usage you notice — with the
smallest possible change. Rules:
- Keep every scene class name and the overall structure identical.
- Only use the real Manim CE v0.20 API (e.g. Text takes font_size= and
  font=; Code takes code_string/language; there is no 'size' kwarg).
- Keep the house-style imports and helpers exactly as they are.
- `config` is THIS PROJECT's config.py, not Manim's global config. Use it
  only for colours (config.ACCENT, ACCENT_2, ACCENT_3, ACCENT_4, BG_COLOR,
  TEXT_COLOR) and handles. For frame geometry use the Manim constants
  ORIGIN/UP/DOWN/LEFT/RIGHT or self.camera.frame_width — and never draw a
  full-frame black rectangle; the screen must never go blank.
- Output the ENTIRE file, every scene class, from the first import to the
  last line. Never abbreviate, never write "... rest unchanged".
Reply with ONLY the corrected full Python file, no markdown fences,
no commentary."""


def repair(scenes_path, error_text: str) -> bool:
    """Ask the model to fix scenes.py. Returns True if a new file was written."""
    from pipeline.generate import _call_claude, _strip_fences
    scenes_path = Path(scenes_path)
    code = scenes_path.read_text()
    # keep only the useful tail of a long rich traceback
    error_tail = "\n".join(error_text.strip().splitlines()[-40:])
    prompt = REPAIR_PROMPT.format(error=error_tail, code=code)
    for attempt in range(2):
        fixed = sanitize(_strip_fences(_call_claude(prompt)))
        problem = validate(fixed)
        if problem is None:
            scenes_path.write_text(fixed)
            return True
        print(f"[repair] rejected the fix: {problem}")
        prompt += (f"\n\nYour previous reply was rejected: {problem}\n"
                   "Return the complete, valid file this time.")
    return False                          # refuse a broken or partial reply
