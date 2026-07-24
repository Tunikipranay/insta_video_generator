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
MAX_DURATION_SECONDS = 110           # hard cap: under 2 minutes always
TARGET_DURATION_SECONDS = 75         # sweet spot for retention
FPS = 30
QUALITY = "-qh"                      # -ql 480p (drafts) / -qm 720p / -qh 1080p

# ---- Visual house style (3blue1brown-inspired, but your own) -----------
BG_COLOR = "#0e1116"                 # near-black blue, cinematic
ACCENT = "#58C4DD"                   # 3b1b-ish blue
ACCENT_2 = "#FFD866"                 # warm yellow for highlights
ACCENT_3 = "#FC6255"                 # red for "slow / wrong"
ACCENT_4 = "#83C167"                 # green for "fast / right"
TEXT_COLOR = "#ECECEC"
CODE_FONT = "DejaVu Sans Mono"

# ---- AI script generation ---------------------------------------------
# Set the env var ANTHROPIC_API_KEY to enable automatic generation.
# Without a key, the pipeline prints the prompt so you can paste it into
# claude.ai (free) and save the JSON reply yourself.
AI_MODEL = "claude-haiku-4-5"        # cheap + good enough for scripts
