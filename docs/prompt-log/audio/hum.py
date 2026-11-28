"""Generate "Hmmm" thinking hums with Bark and cut a seamless loop from the steadiest part.

Usage: python hum.py OUT_DIR
For each take: raw WAV + JSON with the voiced-hum measurement:
  steady = longest run of 50 ms frames that are loud (> -45 dBFS), strongly voiced (autocorrelation > 0.8)
           and in the hum pitch range (70-350 Hz). Longer steady runs make a more natural loop.
"""
import json, sys, time, pathlib
import numpy as np, soundfile as sf, torch
from transformers import AutoProcessor, BarkModel

torch.set_num_threads(2)
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
TAKES = [  # (take id, voice preset, text, seed)
    ("hum_male_a", "v2/en_speaker_6", "Hmmmmmmmm...", 1),
    ("hum_male_b", "v2/en_speaker_6", "Hmmmmmmmm...", 2),
    ("hum_male_c", "v2/en_speaker_3", "Hmmmmmmmm...", 1),
    ("hum_female_a", "v2/en_speaker_9", "Hmmmmmmmm...", 1),
    ("hum_female_b", "v2/en_speaker_9", "Hmmmmmmmm...", 2),
    ("hum_female_c", "v2/en_speaker_4", "Hmmmmmmmm...", 1),
]


def steady_run(x, sr):
    w = int(0.05 * sr); frames = []
    for i in range(0, len(x) - w, w):
        seg = x[i:i + w]
        rms = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)
        ac = np.correlate(seg, seg, "full")[w - 1:]
        lo, hi = int(sr / 350), int(sr / 70)
        lag = lo + int(np.argmax(ac[lo:hi]))
        frames.append(rms > -45 and ac[0] > 0 and ac[lag] / ac[0] > 0.8)
    best, cur, best_end = 0, 0, 0
    for k, ok in enumerate(frames):
        cur = cur + 1 if ok else 0
        if cur > best:
            best, best_end = cur, k + 1
    return best * w / sr, (best_end - best) * w / sr, best_end * w / sr


p = AutoProcessor.from_pretrained("suno/bark-small")
m = BarkModel.from_pretrained("suno/bark-small")
sr = m.generation_config.sample_rate
for take, preset, text, seed in TAKES:
    torch.manual_seed(seed); t0 = time.time()
    with torch.no_grad():
        a = m.generate(**p(text, voice_preset=preset), do_sample=True).cpu().numpy().squeeze()
    sf.write(out / f"{take}.wav", a, sr)
    length, start, end = steady_run(a, sr)
    meta = dict(take=take, tool="suno/bark-small (transformers)", voice_preset=preset, prompt=text, seed=seed,
                sample_rate=sr, seconds=round(len(a) / sr, 2), steady_seconds=round(length, 2),
                steady_from=round(start, 2), steady_to=round(end, 2), generation_seconds=round(time.time() - t0))
    json.dump(meta, open(out / f"{take}.json", "w"), indent=1)
    print("done", take, f"steady {length:.2f}s ({start:.2f}-{end:.2f})", flush=True)
