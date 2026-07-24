# 2min_ai video factory 🎬

Turn a topic into a 1–2 minute, 3blue1brown-style animated explainer —
script, cinematic Manim animation, natural female voiceover, ambient music,
YouTube (16:9) and Instagram Reels (9:16) exports — with **one command**:

```bash
python make.py "python decorators"
```

Built for the [@2min_ai](https://instagram.com/2min_ai) channel; MIT-licensed
so you can fork it for yours.

## What's AI and what's plain code

Only **one** step uses a generative AI API, and it's optional:

| Stage                     | What runs                        | AI? |
|---------------------------|----------------------------------|-----|
| Script writing            | Claude API (or you, or claude.ai free paste flow) | ✅ optional |
| Animation code writing    | Claude API (same options)        | ✅ optional |
| Rendering animations      | Manim + FFmpeg, deterministic    | ❌ |
| Voiceover                 | Piper TTS — a local neural voice, no API, no cost | offline model |
| Music + whoosh SFX        | Synthesized with numpy/scipy — royalty-free by construction | ❌ |
| Timing sync, mixing, mastering, 9:16 crop | FFmpeg | ❌ |

So the "AI budget" is a few cents per video (Claude Haiku writes ~2k tokens),
or zero if you paste the prompts into claude.ai yourself. Everything else is
local, free, and reproducible.

## Setup (one time, ~5 minutes)

Python deps are managed with [uv](https://docs.astral.sh/uv/) via
`pyproject.toml` (a `uv.lock` is committed for reproducible installs).

```bash
git clone https://github.com/Tunikipranay/insta_video_generator.git
cd insta_video_generator
bash setup.sh          # system deps + uv sync + voice model + music assets
echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env   # optional; enables full automation
```

`.env` is git-ignored — your key never leaves your machine. Prefer doing it
manually? `uv sync` creates the environment from the lockfile; the rest of
setup.sh just downloads the voice model and generates the music assets.

Then edit `config.py` — handles, colors, target duration all live there.

## Daily workflow

```bash
# 1. pick a topic (see topics.txt for the backlog) and draft it
uv run make.py "python generators" --draft

# 2. watch projects/python_generators/output/FINAL_youtube_ai_voice.mp4
#    tweak scenes.py or script.json if needed, re-run

# 3. final quality and post
uv run make.py "python generators" --hq
```

(No uv? `pip install -r requirements.txt` in a venv still works.)

Flags: `--draft` (fast 480p), `--hq` (1080p60), `--voice none` (silent
masters + a timed narration sheet so you can record your own voice —
`pipeline/assemble.py` mixes it in), `--voice path/to/voice.onnx` (any
[Piper voice](https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models)).

### No API key? Free manual mode

Run `make.py` once — it writes `PASTE_ME_script_prompt.txt` into the project
folder. Paste it into claude.ai, save the JSON reply as `script.json`, run
again, do the same for the scene prompt, run once more. Same result, $0.

## How a video is structured

Every script follows a retention formula enforced by the prompts
(`prompts/`): a ≤5s hook, one idea built visually, one **real use case
with runnable code**, a one-line payoff, and the same end card on every
video. Videos never exceed 110 seconds.

## How the pieces fit

```
make.py
 ├─ pipeline/generate.py       topic → script.json → scenes.py → narration_sheet.txt
 ├─ pipeline/render.py         scenes.py → per-scene mp4 → 16:9 + 9:16 silent masters
 └─ pipeline/voiceover_ai.py   per-section TTS → auto-sync (slow scenes that run
                               short, never speed up) → whoosh transitions →
                               music ducked under voice → -16 LUFS master
house_style.py                 shared theme: colors, glow dots, code windows,
                               kv boxes, end card — the channel's visual identity
config.py                      handles, palette, durations, model choice
```

Each video lives in `projects/<slug>/` with everything editable: the script
JSON, the Manim code, and the narration sheet. The two `projects/` in the
repo (`python_dicts`, `how_chatgpt_works`) are working examples.

## Reviewing AI-written scenes

The scene prompt encodes the house rules, but generated layout can still
overlap or crowd. The 30-second check that catches 95% of it: render
`--draft`, then skim frames:

```bash
ffmpeg -i projects/<slug>/output/video_16x9.mp4 -vf fps=1/5 frames_%02d.png
```

Fix anything off in `scenes.py` (it's ordinary Python) and re-run.

## Contributing

Issues and PRs welcome — especially new `house_style.py` components,
better prompts, and non-English voice presets.

## License

MIT — see [LICENSE](LICENSE).
