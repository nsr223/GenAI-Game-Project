# GenAI-Game-Project

Project ideas: https://docs.google.com/document/d/1YqFmUEwDxD2y9bsoIDNZqHgXfr6dqmoxmENA7_XG234/edit?usp=sharing

## Setup

We use [uv](https://docs.astral.sh/uv/) to manage Python and dependencies.

1. Install uv (Arch/CachyOS: `sudo pacman -S uv`; others: see the uv docs).
2. Install dependencies (uv fetches Python 3.12 if needed and creates `.venv/`):
   ```bash
   uv sync
   ```
3. Copy the env template and add your API key:
   ```bash
   cp .env.example .env
   ```
4. Run the tests:
   ```bash
   uv run pytest
   ```

Add a dependency with `uv add <pkg>` (or `uv add --dev <pkg>`), and commit `uv.lock`.
Without uv: `python -m venv .venv && .venv/bin/pip install -r requirements-dev.txt`.
