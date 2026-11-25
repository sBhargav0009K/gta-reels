"""Synth beat bed (v2: faster, punchier) + whooshes at cuts + hit at t=0.
Usage: music.py out.wav total_seconds cut1,cut2,...   env BPM (default 100), MOOD=chill|drive"""
import os, sys, wave
import numpy as np

SR = 44100
out, total = sys.argv[1], float(sys.argv[2])
cuts = [float(c) for c in sys.argv[3].split(",")] if len(sys.argv) > 3 and sys.argv[3] else []
bpm = float(os.environ.get("BPM", 100)); mood = os.environ.get("MOOD", "drive")
n = int(SR * total); t = np.arange(n) / SR; mix = np.zeros(n)
beat = 60 / bpm; bar = beat * 4
rng = np.random.default_rng(5)
note = lambda m: 440 * 2 ** ((m - 69) / 12)
chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]] if mood == "chill" else \
         [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]]
for i in range(int(total / bar) + 1):
    ch = chords[i % 4]; s0 = i * bar
    idx = (t >= s0) & (t < s0 + bar); tt = t[idx] - s0
    env = np.minimum(1, tt / 0.05) * np.exp(-tt * 0.9)
    for m in ch:
        f = note(m)
        mix[idx] += 0.045 * env * (np.sin(2 * np.pi * f * tt) + 0.35 * np.sign(np.sin(2 * np.pi * f * tt)) * 0.3)
    # pulsing bass on 8ths
    fb = note(ch[0] - 24)
    ph = (tt % (beat / 2)) / (beat / 2)
    mix[idx] += 0.16 * np.exp(-ph * 4) * np.sin(2 * np.pi * fb * tt)
k = 0.0; step = 0
while k < total:
    i0 = int(k * SR)
    if step % 2 == 0:
        L = int(0.22 * SR); tt = np.arange(L) / SR
        kick = np.sin(2 * np.pi * (45 + 110 * np.exp(-tt * 35)) * tt) * np.exp(-tt * 14)
        seg = mix[i0:i0 + L]; seg += 0.45 * kick[:len(seg)]
    if step % 4 == 2:
        L = int(0.16 * SR); tt = np.arange(L) / SR
        sn = rng.normal(0, 1, L) * np.exp(-tt * 20) + 0.4 * np.sin(2 * np.pi * 190 * tt) * np.exp(-tt * 25)
        seg = mix[i0:i0 + L]; seg += 0.13 * sn[:len(seg)]
    L = int(0.04 * SR); tt = np.arange(L) / SR
    hat = np.diff(rng.normal(0, 1, L + 1)) * np.exp(-tt * 80)
    seg = mix[i0:i0 + L]; seg += (0.035 if step % 2 else 0.02) * hat[:len(seg)]
    k += beat / 2; step += 1
for c in cuts:
    L = int(0.4 * SR); i0 = max(0, int((c - 0.25) * SR)); tt = np.arange(L) / SR
    nz = np.convolve(rng.normal(0, 1, L), np.ones(10) / 10, mode="same")
    env = np.sin(np.pi * tt / tt[-1]) ** 2
    seg = mix[i0:i0 + L]; seg += 0.22 * (nz * env)[:len(seg)]
# impact at 0
L = int(0.6 * SR); tt = np.arange(L) / SR
hit = (np.sin(2 * np.pi * (40 + 80 * np.exp(-tt * 20)) * tt) * np.exp(-tt * 6) + 0.3 * rng.normal(0, 1, L) * np.exp(-tt * 18))
mix[:L] += 0.6 * hit
mix = np.tanh(mix * 1.5) / 1.5
fade = np.minimum(1, (total - t) / 0.8)
mix *= fade
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.85
st = np.stack([mix, mix], 1)
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
