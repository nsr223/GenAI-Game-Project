"""Generate music (MusicGen) and sound effects (AudioLDM) from a JSON spec.

Usage: python gen.py SPEC.json OUT_WAV_DIR [only_id ...]
Each spec item: {id, kind: music|sfx, version, prompt, negative?, seconds, seed, guidance?, steps?}
Writes OUT_WAV_DIR/<id>_v<version>.wav (raw model output) and a .json with settings + timing.
"""
import json, sys, time, pathlib
import numpy as np
import soundfile as sf
import torch

torch.set_num_threads(2)
spec = json.load(open(sys.argv[1]))
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
only = set(sys.argv[3:])
items = [s for s in spec if not only or s["id"] in only]

_mg = None
_ldm = None


def musicgen():
    global _mg
    if _mg is None:
        from transformers import AutoProcessor, MusicgenForConditionalGeneration
        name = "facebook/musicgen-small"
        _mg = (AutoProcessor.from_pretrained(name), MusicgenForConditionalGeneration.from_pretrained(name))
    return _mg


def audioldm():
    global _ldm
    if _ldm is None:
        from diffusers import AudioLDMPipeline
        _ldm = AudioLDMPipeline.from_pretrained("cvssp/audioldm-s-full-v2", torch_dtype=torch.float32)
    return _ldm


for s in items:
    t0 = time.time()
    torch.manual_seed(s["seed"])
    if s["kind"] == "music":
        proc, model = musicgen()
        inp = proc(text=[s["prompt"]], padding=True, return_tensors="pt")
        with torch.no_grad():
            a = model.generate(**inp, do_sample=True, guidance_scale=s.get("guidance", 3.0),
                               max_new_tokens=int(s["seconds"] * 50))
        audio = a[0, 0].numpy(); sr = model.config.audio_encoder.sampling_rate
        tool = "facebook/musicgen-small (transformers)"
    else:
        pipe = audioldm()
        g = torch.Generator().manual_seed(s["seed"])
        audio = pipe(s["prompt"], negative_prompt=s.get("negative"), num_inference_steps=s.get("steps", 100),
                     audio_length_in_s=s["seconds"], guidance_scale=s.get("guidance", 2.5), generator=g).audios[0]
        sr = 16000
        tool = "cvssp/audioldm-s-full-v2 (diffusers)"
    base = out / f"{s['id']}_v{s['version']}"
    sf.write(str(base) + ".wav", audio.astype(np.float32), sr)
    meta = dict(s, tool=tool, sample_rate=sr, generation_seconds=round(time.time() - t0, 1))
    json.dump(meta, open(str(base) + ".json", "w"), indent=1)
    print(f"done {s['id']} v{s['version']} in {meta['generation_seconds']}s", flush=True)
