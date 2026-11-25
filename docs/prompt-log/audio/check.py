"""Measure generated audio and draw spectrograms.

Usage: python check.py OUT_PNG file1.wav [file2.wav ...]
Prints per file: duration, peak/RMS dBFS, energy share per band, loudness spread over time,
spectral flatness (noise-like ~1, tonal ~0), and an estimate of dominant pitch stability.
"""
import sys
import numpy as np
import soundfile as sf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out_png, files = sys.argv[1], sys.argv[2:]
fig, axes = plt.subplots(len(files), 1, figsize=(10, 1.6 * len(files)), squeeze=False)
for ax, f in zip(axes[:, 0], files):
    x, sr = sf.read(f)
    if x.ndim > 1:
        x = x.mean(1)
    db = lambda v: 20 * np.log10(max(v, 1e-9))
    win = int(0.5 * sr)
    rms_t = np.array([np.sqrt(np.mean(x[i:i + win] ** 2)) for i in range(0, len(x) - win, win)])
    X = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    fr = np.fft.rfftfreq(len(x), 1 / sr)
    E = X ** 2
    bands = [(0, 200), (200, 1000), (1000, 4000), (4000, sr / 2)]
    share = [E[(fr >= a) & (fr < b)].sum() / E.sum() for a, b in bands]
    flat = np.exp(np.mean(np.log(X[1:] + 1e-12))) / np.mean(X[1:])
    print(f"{f.split('/')[-1]:32s} {len(x)/sr:5.1f}s peak {db(np.abs(x).max()):6.1f} rms {db(np.sqrt(np.mean(x**2))):6.1f} "
          f"spread {db(rms_t.max())-db(np.median(rms_t)):4.1f}dB  bands<200/1k/4k/+ {' '.join(f'{s:.2f}' for s in share)}  "
          f"flat {flat:.3f}")
    ax.specgram(x, Fs=sr, NFFT=1024, noverlap=512, cmap="magma", vmin=-120)
    ax.set_ylim(0, min(8000, sr / 2)); ax.set_ylabel(f.split("/")[-1][:18], fontsize=7); ax.tick_params(labelsize=6)
plt.tight_layout(); plt.savefig(out_png, dpi=80)
