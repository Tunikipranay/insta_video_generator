"""
Generate royalty-free-by-construction audio assets:
  music/bg_generated.wav — soft ambient synth pad (Am F C G loop)
  music/whoosh.wav       — gentle transition swell
Run once: python pipeline/gen_audio_assets.py
"""
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

ROOT = Path(__file__).resolve().parent.parent
SR = 44100


def lowpass(x, hz, order=4):
    sos = butter(order, hz, btype="low", fs=SR, output="sos")
    return sosfilt(sos, x)


def bandpass(x, lo, hi, order=4):
    sos = butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    return sosfilt(sos, x)


def pad_note(freq, dur, detune=0.0):
    t = np.arange(int(dur * SR)) / SR
    f = freq * (1 + detune)
    x = (0.50 * np.sin(2 * np.pi * f * t)
         + 0.22 * np.sin(2 * np.pi * 2 * f * t)
         + 0.10 * np.sin(2 * np.pi * 3 * f * t)
         + 0.18 * np.sin(2 * np.pi * 0.5 * f * t))       # sub octave
    # slow shimmer
    x *= 1 + 0.08 * np.sin(2 * np.pi * 0.35 * t + freq)
    return x


def chord(freqs, dur, detune):
    x = sum(pad_note(f, dur, detune) for f in freqs) / len(freqs)
    n = len(x)
    fade = int(1.2 * SR)
    env = np.ones(n)
    env[:fade] = np.linspace(0, 1, fade) ** 2
    env[-fade:] = np.linspace(1, 0, fade) ** 2
    return x * env


def make_music(total=100.0):
    A2, C3, E3 = 110.0, 130.81, 164.81
    F2, G2, B2, D3, G3 = 87.31, 98.0, 123.47, 146.83, 196.0
    prog = [(A2, C3, E3), (F2, A2, C3), (C3, E3, G3), (G2, B2, D3)]
    chord_dur, overlap = 5.0, 1.2

    def channel(detune):
        step = int((chord_dur - overlap) * SR)
        n = int(total * SR) + int(chord_dur * SR)
        out = np.zeros(n)
        pos, i = 0, 0
        while pos < int(total * SR):
            c = chord(prog[i % 4], chord_dur, detune)
            out[pos:pos + len(c)] += c
            pos += step
            i += 1
        return out[:int(total * SR)]

    left = lowpass(channel(-0.0012), 1800)
    right = lowpass(channel(+0.0012), 1800)
    stereo = np.stack([left, right], axis=1)
    stereo *= 0.30 / (np.abs(stereo).max() + 1e-9)
    return stereo


def make_whoosh(dur=0.7):
    rng = np.random.default_rng(7)
    x = rng.standard_normal(int(dur * SR))
    x = bandpass(x, 250, 1400)
    t = np.linspace(0, 1, len(x))
    env = np.sin(np.pi * t) ** 2.5          # swell up then down
    x *= env
    x *= 0.5 / (np.abs(x).max() + 1e-9)
    return np.stack([x, x], axis=1)


if __name__ == "__main__":
    out = ROOT / "music"
    out.mkdir(exist_ok=True)
    wavfile.write(out / "bg_generated.wav", SR,
                  (make_music() * 32767).astype(np.int16))
    wavfile.write(out / "whoosh.wav", SR,
                  (make_whoosh() * 32767).astype(np.int16))
    print(f"[ok] {out}/bg_generated.wav, {out}/whoosh.wav")
