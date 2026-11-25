# Audio generation: scripts and evidence

Everything needed to reproduce the game's music and sound. Results and reasons per version are in `prompts/assets/CHANGELOG.md` → "Music and sound".

| File | Purpose |
|---|---|
| `spec_v1.json`, `spec_v2.json` | Exact prompts, negative prompts, durations and seeds of every generation |
| `gen.py` | Runs MusicGen (`facebook/musicgen-small`) for music and AudioLDM (`cvssp/audioldm-s-full-v2`) for sound; writes WAV + settings JSON |
| `check.py` | Measures each clip (RMS, peak, loudness spread, band energy, spectral flatness) and draws spectrograms |
| `post.py` | Turns a raw clip into a game file: seamless loop crossfade, fades, level matching, OGG Vorbis |
| `logs.py` | Writes `prompts/assets/{music,sfx}/<id>/vN.md` from the settings JSON, so saved prompts match the model input word for word |
| `img/` | Spectrograms of all v1 clips and of the v2 retries |

```bash
pip install torch transformers diffusers accelerate soundfile scipy matplotlib   # ffmpeg with libvorbis needed for post.py
python gen.py spec_v1.json raw/                     # ~4 min per 30 s track, ~2 min per 10 s effect on 2 CPU cores
python check.py raw/sheet.png raw/*.wav
python post.py raw/ship_hum_v1.wav frontend/static/audio/ambience/ship_hum.ogg loop -28
```

Same seed and settings give the same output only on the same library versions; small differences across machines are expected.
