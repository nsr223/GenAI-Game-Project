"""Cut a seamless loop from the steady part of a hum take.

Usage: python humloop.py IN.wav OUT.ogg START END [target_rms_db]
Takes START..END seconds, crossfades the last 0.3 s into the first 0.3 s (equal power) so the hum can repeat
for as long as the model is thinking, RMS-normalises (default -20 dBFS), encodes OGG Vorbis at 44.1 kHz.
"""
import subprocess, sys, tempfile
import numpy as np, soundfile as sf

src, dst, a, b = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
target = float(sys.argv[5]) if len(sys.argv) > 5 else -20
x, sr = sf.read(src)
x = x[int(a * sr):int(b * sr)]
n = int(0.3 * sr)
ph = np.linspace(0, np.pi / 2, n)
loop = np.concatenate([x[-n:] * np.cos(ph) + x[:n] * np.sin(ph), x[n:-n]])
loop *= 10 ** (target / 20) / np.sqrt(np.mean(loop ** 2))
loop *= min(1, 10 ** (-3 / 20) / np.abs(loop).max())
with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
    sf.write(tmp.name, loop.astype(np.float32), sr)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp.name, "-ar", "44100", "-c:a", "libvorbis",
                    "-q:a", "5", dst], check=True)
print("wrote", dst, f"{len(loop) / sr:.2f} s loop")
