#!/usr/bin/env bash
# One-time setup for the 2min_ai video factory.
# Tested on Ubuntu/Debian. macOS: brew install cairo pango ffmpeg, then rerun.
set -e
cd "$(dirname "$0")"

echo "==> System dependencies (needs sudo on Linux)"
if command -v apt-get >/dev/null; then
    sudo apt-get update -q
    sudo apt-get install -y -q ffmpeg libcairo2-dev libpango1.0-dev pkg-config python3-venv
fi

echo "==> Python virtual environment"
python3 -m venv venv
./venv/bin/pip install --upgrade pip setuptools wheel
./venv/bin/pip install -r requirements.txt

echo "==> Downloading the narrator voice (Piper, ~65MB, one time)"
mkdir -p tts
if [ ! -f tts/vits-piper-en_US-hfc_female-medium/en_US-hfc_female-medium.onnx ]; then
    curl -L -o tts/voice.tar.bz2 \
      https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-hfc_female-medium.tar.bz2
    tar xjf tts/voice.tar.bz2 -C tts/
    rm tts/voice.tar.bz2
fi

echo "==> Generating music bed + transition SFX (royalty-free by construction)"
./venv/bin/python pipeline/gen_audio_assets.py

echo
echo "Setup complete. Next steps:"
echo "  1. Put your handles in config.py"
echo "  2. export ANTHROPIC_API_KEY=sk-...   (or use the free claude.ai paste flow)"
echo "  3. source venv/bin/activate"
echo "  4. python make.py \"python decorators\" --draft"
