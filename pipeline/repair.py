"""
Scene-code self-repair.

Two layers of defense against AI-generated Manim code that crashes:

1. sanitize(code): static fixes for the most common invented kwargs,
   applied before the code is ever written to disk. Costs nothing.
2. repair(scenes_path, error_text): when a render still crashes, send the
   error + the full file back to the model and write the corrected file.
   make.py calls this automatically and retries the render.
"""
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


def sanitize(code: str) -> str:
    for pat, rep in ALIASES:
        code = re.sub(pat, rep, code)
    return code


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
Reply with ONLY the corrected full Python file, no markdown fences,
no commentary."""


def repair(scenes_path, error_text: str) -> bool:
    """Ask the model to fix scenes.py. Returns True if a new file was written."""
    from pipeline.generate import _call_claude, _strip_fences
    scenes_path = Path(scenes_path)
    code = scenes_path.read_text()
    # keep only the useful tail of a long rich traceback
    error_tail = "\n".join(error_text.strip().splitlines()[-40:])
    fixed = _strip_fences(_call_claude(
        REPAIR_PROMPT.format(error=error_tail, code=code)))
    if "class S1_" not in fixed:
        return False                      # refuse a reply that lost the scenes
    scenes_path.write_text(sanitize(fixed))
    return True
