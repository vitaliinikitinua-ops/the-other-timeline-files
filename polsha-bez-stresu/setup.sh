#!/usr/bin/env bash
# One-time setup for rendering "Польща без стресу" videos in a fresh session.
set -e
cd "$(dirname "$0")"
pip install -q piper-tts faster-whisper
mkdir -p voice/model
B=https://huggingface.co/rhasspy/piper-voices/resolve/main/uk/uk_UA/ukrainian_tts/medium
for f in uk_UA-ukrainian_tts-medium.onnx uk_UA-ukrainian_tts-medium.onnx.json; do
  [ -f voice/model/$f ] || curl -sL -o voice/model/$f $B/$f
done
echo "setup ok"
