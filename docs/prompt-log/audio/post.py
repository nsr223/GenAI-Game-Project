"""Post-process raw model output into game-ready OGG files.

Usage: python post.py IN.wav OUT.ogg loop|oneshot|music [target_rms_db]
loop:    trim 0.25 s at both ends (diffusion edge artefacts), crossfade the last 1.5 s into the start
         with an equal-power fade so the file loops without a click, RMS-normalise (default -26 dBFS).
oneshot: trim leading silence, 30 ms fade-in, 200 ms fade-out, peak-normalise to -4.5 dBFS (headroom for Vorbis overshoot).
music:   1 s fade-in, 3 s fade-out, RMS-normalise (default -20 dBFS); peaks limited to -1 dBFS.
Output is OGG Vorbis (ffmpeg, libvorbis q4), resampled to 44.1 kHz for the browser.
"""
import subprocess, sys, tempfile
import numpy as np
import soundfile as sf

src, dst, mode = sys.argv[1:4]
x, sr = sf.read(src)
x = x.mean(1) if x.ndim > 1 else x
db2a = lambda d: 10 ** (d / 20)


def rms_norm(y, target):
    r = np.sqrt(np.mean(y ** 2))
    y = y * db2a(target) / max(r, 1e-9)
    pk = np.abs(y).max()
    return y * (db2a(-1) / pk) if pk > db2a(-1) else y


if mode == "loop":
    t = int(0.25 * sr); x = x[t:-t]
    n = int(1.5 * sr)
    head, body, tail = x[:n], x[n:-n], x[-n:]
    ph = np.linspace(0, np.pi / 2, n)
    x = np.concatenate([tail * np.cos(ph) + head * np.sin(ph), body])
    x = rms_norm(x, float(sys.argv[4]) if len(sys.argv) > 4 else -26)
elif mode == "oneshot":
    thr = np.abs(x).max() * db2a(-40)
    start = max(0, np.argmax(np.abs(x) > thr) - int(0.01 * sr))
    x = x[start:]
    if len(sys.argv) > 4:  # optional max length in seconds
        x = x[:int(float(sys.argv[4]) * sr)]
    fi, fo = int(0.03 * sr), int(0.2 * sr)
    x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo)
    x = x * db2a(-4.5) / np.abs(x).max()
else:
    fi, fo = int(1 * sr), int(3 * sr)
    x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo)
    x = rms_norm(x, float(sys.argv[4]) if len(sys.argv) > 4 else -20)

with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
    sf.write(tmp.name, x.astype(np.float32), sr)
    import os
    af = ["-af", f"lowpass=f={os.environ['LOWPASS']}:poles=2"] if os.environ.get("LOWPASS") else []
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp.name, *af, "-ar", "44100", "-c:a", "libvorbis",
                    "-q:a", "4", dst], check=True)
print("wrote", dst)
