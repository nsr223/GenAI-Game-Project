"""Write one versioned prompt file per generation from its settings JSON.

Usage: python logs.py RAW_DIR REPO_DIR RESULTS.json
RESULTS.json maps "<id>_v<n>" -> {"result": "...", "selected": true|false, "post": "..."}
Writes prompts/assets/{music|sfx}/<id>/v<n>.md with the exact prompt the model received.
"""
import json, pathlib, sys

raw, repo, results = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), json.load(open(sys.argv[3]))
for meta_file in sorted(raw.glob("*_v*.json")):
    m = json.load(open(meta_file))
    key = f"{m['id']}_v{m['version']}"
    r = results.get(key)
    if r is None:
        continue
    folder = repo / "prompts" / "assets" / ("music" if m["kind"] == "music" else "sfx") / m["id"]
    folder.mkdir(parents=True, exist_ok=True)
    settings = f"{m['seconds']} s, seed {m['seed']}"
    if m["kind"] == "music":
        settings += f", guidance {m.get('guidance', 3.0)}, sampling on"
    else:
        settings += f", {m.get('steps', 100)} steps, guidance {m.get('guidance', 2.5)}"
    lines = [
        f"# {m['id'].replace('_', ' ').capitalize()}: v{m['version']}",
        "",
        f"- **Tool:** `{m['tool']}`, run locally on CPU ({m['generation_seconds']:.0f} s)",
        f"- **Settings:** {settings}",
        f"- **Status:** {'selected' if r['selected'] else 'not selected'}",
        "",
        "## Prompt",
        "",
        "```",
        m["prompt"],
        "```",
    ]
    if m.get("negative"):
        lines += ["", f"**Negative prompt:** `{m['negative']}`"]
    lines += ["", "## Result", "", r["result"]]
    if r.get("post"):
        lines += ["", f"**Post-processing:** {r['post']}"]
    (folder / f"v{m['version']}.md").write_text("\n".join(lines) + "\n")
    print("wrote", folder / f"v{m['version']}.md")
