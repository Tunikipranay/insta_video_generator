"""Central configuration for the video factory."""
import os
from pathlib import Path

# Load .env (KEY=value lines) so the API key never has to live in shell
# config or, worse, in git. Real environment variables take precedence.
_env = Path(__file__).parent / ".env"
if _env.exists():
    for _line in _env.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip())

# ---- Branding ----------------------------------------------------------
CHANNEL_NAME = "2min AI"             # shown on the end card
INSTA_HANDLE = "@2min_ai"            # CTA on every video
YOUTUBE_HANDLE = "@2min_ai"

# ---- Video specs -------------------------------------------------------
# Deep explainer (YouTube): Khan-Academy pacing — slow, motivated, why-first
TARGET_DURATION_SECONDS = 210        # ~3.5 minutes
MAX_DURATION_SECONDS = 260           # hard cap for the deep version
# Teaser (Instagram Reels / Shorts): hooks viewers toward the full video
TEASER_MAX_SECONDS = 60
FPS = 30
QUALITY = "-qh"                      # -ql 480p (drafts) / -qm 720p / -qh 1080p

# ---- Narrator delivery -------------------------------------------------
SPEECH_LENGTH_SCALE = 1.08           # >1 = slower, calmer teacher pace
SPEECH_SENTENCE_SILENCE = 0.4        # seconds of pause between sentences

# ---- Visual house style (3blue1brown-inspired, but your own) -----------
BG_COLOR = "#0e1116"                 # near-black blue, cinematic
ACCENT = "#58C4DD"                   # 3b1b-ish blue
ACCENT_2 = "#FFD866"                 # warm yellow for highlights
ACCENT_3 = "#FC6255"                 # red for "slow / wrong"
ACCENT_4 = "#83C167"                 # green for "fast / right"
TEXT_COLOR = "#ECECEC"
CODE_FONT = "DejaVu Sans Mono"
FONT_NAME = "DejaVu Sans"            # body text font

# ---- Compatibility shims ------------------------------------------------
# Scene files do `from manim import *` and then `import config`, so this
# module shadows Manim's own global `config`. AI-written scenes reach for
# frame geometry through that name; mirror Manim's 16:9 defaults here so
# those references resolve instead of crashing the render.
frame_width = 14.222222222222221
frame_height = 8.0
frame_x_radius = frame_width / 2
frame_y_radius = frame_height / 2
FRAME_WIDTH = frame_width
FRAME_HEIGHT = frame_height
pixel_width = 1920
pixel_height = 1080

# ---- AI script generation ---------------------------------------------
# Set the env var ANTHROPIC_API_KEY to enable automatic generation.
# Without a key, the pipeline prints the prompt so you can paste it into
# claude.ai (free) and save the JSON reply yourself.
AI_MODEL = "claude-haiku-4-5"        # cheap + good enough for scripts
