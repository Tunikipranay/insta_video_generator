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
    # weight must be the BOLD/NORMAL constant, not a string
    (r"weight\s*=\s*['\"](?i:bold)['\"]", "weight=BOLD"),
    (r"weight\s*=\s*['\"](?i:normal)['\"]", "weight=NORMAL"),
]

# kwargs the model invents that no Manim mobject accepts — delete them
DROP_KWARGS = ["text_align", "align", "curve", "text_color", "bg_color",
               "font_weight", "line_width", "border_radius"]

# scene classes the pipeline expects, by number prefix
REQUIRED_PREFIXES = ["S1_", "S2_", "S3_", "S4_", "S5_", "S6_",
                     "T1_", "T2_", "T3_"]


# Anything below this is unreadable on a phone screen. The model keeps
# writing font_size=12; raise it mechanically rather than hoping.
MIN_FONT_SIZE = 24


def _bump_font(m: re.Match) -> str:
    return (m.group(0) if int(m.group(1)) >= MIN_FONT_SIZE
            else f"font_size={MIN_FONT_SIZE}")


def sanitize(code: str) -> str:
    for pat, rep in ALIASES:
        code = re.sub(pat, rep, code)
    for kw in DROP_KWARGS:
        code = re.sub(rf"(?<=[(,\s]){kw}\s*=\s*[^,()]+,?\s*", "", code)
    code = re.sub(r"font_size\s*=\s*(\d+)", _bump_font, code)
    return code


def _literal(node, default=None):
    try:
        return ast.literal_eval(node)
    except Exception:
        return default


def _loop_count(node: ast.For) -> int:
    it = node.iter
    if isinstance(it, ast.Call) and getattr(it.func, "id", "") == "range":
        args = [_literal(a) for a in it.args]
        if all(isinstance(a, int) for a in args):
            return max(len(range(*args)), 1)
    if isinstance(it, (ast.List, ast.Tuple)):
        return max(len(it.elts), 1)
    return 1                                # unknown: count it once


def _body_seconds(body, mult=1) -> float:
    """Rough on-screen duration of a list of statements."""
    total = 0.0
    for node in body:
        if isinstance(node, ast.For):
            total += _body_seconds(node.body, _loop_count(node))
        elif isinstance(node, (ast.If, ast.With, ast.While)):
            total += _body_seconds(node.body)
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            name = getattr(call.func, "attr", "")
            if name not in ("play", "wait"):
                continue
            kw = {k.arg: _literal(k.value) for k in call.keywords}
            if name == "wait":
                secs = _literal(call.args[0], 1.0) if call.args else 1.0
            else:
                secs = kw.get("run_time", 1.0)
            total += float(secs if isinstance(secs, (int, float)) else 1.0)
    return total * mult


def estimate_scene_seconds(code: str) -> dict:
    """Static estimate of how long each scene will run, before rendering.

    Cheap insurance against the model writing a 15-second animation for a
    60-second narration — which the audio stage can only paper over with a
    long frozen frame.
    """
    out = {}
    for node in ast.walk(ast.parse(code)):
        if not isinstance(node, ast.ClassDef):
            continue
        for f in node.body:
            if isinstance(f, ast.FunctionDef) and f.name == "construct":
                out[node.name] = _body_seconds(f.body)
    return out


MAX_HOLD = 6.0          # longest a single held frame may become
PAD_GOAL = 0.9          # aim slightly under target; a mild stretch is free
                        # and overshooting leaves silence at the scene end


def pad_to_targets(code: str, targets: dict) -> str:
    """Lengthen existing holds so each scene covers its narration.

    The model reliably writes scenes shorter than their narration. Rather
    than freeze the last frame for half a minute at the end, spread the
    missing time over the pauses the scene already has, so the picture is
    always a deliberate hold on something relevant.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code
    lines = code.splitlines()
    edits = []
    for cls in tree.body:
        if not isinstance(cls, ast.ClassDef):
            continue
        secs = next((v for p, v in targets.items() if cls.name.startswith(p)),
                    None)
        if secs is None:
            continue
        construct = next((f for f in cls.body if isinstance(f, ast.FunctionDef)
                          and f.name == "construct"), None)
        if construct is None:
            continue
        deficit = secs * PAD_GOAL - _body_seconds(construct.body)
        waits = [n for n in construct.body
                 if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                 and getattr(n.value.func, "attr", "") == "wait"
                 and n.lineno == n.end_lineno]
        if deficit < 1 or not waits:
            continue
        share = deficit / len(waits)
        for w in waits:
            cur = (_literal(w.value.args[0], 1.0) if w.value.args else 1.0)
            if not isinstance(cur, (int, float)):
                continue
            new = round(min(cur + share, MAX_HOLD), 1)
            if new > cur:
                indent = " " * w.col_offset
                edits.append((w.lineno - 1, f"{indent}self.wait({new})"))
    for idx, text in sorted(edits, reverse=True):
        lines[idx] = text
    return "\n".join(lines) + "\n"


def validate(code: str, targets: dict | None = None) -> str | None:
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
    if targets:
        # targets are keyed by class-name prefix ("S3_") -> narration seconds
        est = estimate_scene_seconds(code)
        short = []
        for prefix, secs in targets.items():
            for name, e in est.items():
                if name.startswith(prefix) and e < 0.8 * secs:
                    short.append((name, e, secs))
        if short:
            detail = "; ".join(
                f"{n} runs ~{e:.0f}s but its narration is {t}s"
                for n, e, t in short)
            return ("These scenes are far too short for their narration, so "
                    f"the video would freeze on a still frame: {detail}. "
                    "Add more animated beats and longer self.wait() holds "
                    "until each scene fills its full time budget.")
    return None


REPAIR_PROMPT = """You are debugging Manim Community Edition v0.20 scene code
for an automated video pipeline. The file below crashed during rendering.

ERROR (from manim):
{error}

FULL FILE:
{code}

Fix the crash with the smallest possible change — AND scan the whole file
for every other occurrence of the same class of mistake and fix those too,
so the next render doesn't fail on the very next scene. Rules:
- Keep every scene class name and the overall structure identical.
- Only use the real Manim CE v0.20 API. Text accepts ONLY: text, font_size,
  color, weight (BOLD/NORMAL constants, not strings), font, slant,
  line_spacing, t2c, t2w. Anything else (size, text_align, align, curve,
  font_family, text_color...) does not exist. Code takes code_string and
  language. Rectangle/Circle take width/height/radius, stroke_color,
  stroke_width, fill_color, fill_opacity, color.
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
