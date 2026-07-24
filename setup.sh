#!/usr/bin/env bash
# One-time setup — uses uv (https://docs.astral.sh/uv/) for the Python side.
# Linux (Ubuntu/Debian) and macOS.
set -e
cd "$(dirname "$0")"

echo "==> System dependencies"
if command -v apt-get >/dev/null; then
    sudo apt-get update -q
    sudo apt-get install -y -q ffmpeg libcairo2-dev libpango1.0-dev pkg-config
elif command -v brew >/dev/null; then
    brew install ffmpeg cairo pango pkg-config
else
    echo "!! Install ffmpeg, cairo and pango with your package manager, then re-run."
    exit 1
fi

echo "==> uv"
if ! command -v uv >/dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "==> Python environment (uv sync)"
uv sync

echo "==> Narrator voice (Piper, ~65MB, one time)"
mkdir -p tts
if [ ! -f tts/vits-piper-en_US-hfc_female-medium/en_US-hfc_female-medium.onnx ]; then
    curl -L -o tts/voice.tar.bz2 \
      https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-hfc_female-medium.tar.bz2
    tar xjf tts/voice.tar.bz2 -C tts/
    rm tts/voice.tar.bz2
fi

echo "==> Music bed + transition SFX (royalty-free by construction)"
uv run pipeline/gen_audio_assets.py

echo
echo "Setup complete. Next:"
echo "  1. Put your handles in config.py"
echo "  2. echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env    # never commit this file"
echo "  3. uv run make.py \"python decorators\" --draft"
