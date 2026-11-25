# Runtime art (placeholders)

The player UI loads rooms from `scenes.json` → `<room>.image` and portraits from
`/static/art/characters/<npc_id>.webp`. A missing file falls back to the drawn bulkhead or silhouette.

Everything here is **placeholder art** copied or cut from `prompts/assets/` (the versioned prompt log).
Looks are PROPOSED, not canon. Replace a file with the approved version when it exists, keeping the file name.

| File | Source | Notes |
|---|---|---|
| `rooms/bridge.webp` | `prompts/assets/rooms/bridge/v2.webp` | Production render; review says too dark, bridge too large |
| `rooms/mess_hall.webp` | `prompts/assets/rooms/mess_hall/v2.webp` | Production render; hotspots in `scenes.json` are placed on it |
| `rooms/wet_lab.webp`, `dry_lab`, `medical_bay`, `crew_quarters`, `editing_room`, `engineering_workshop` | Cells of `prompts/assets/concepts/rooms/v2.webp` | Square concept thumbnails (~385 px), cropped to 16:9 by CSS; hotspots auto-placed |
| `characters/sarah_morgan.webp`, `thomas_blake.webp` | `prompts/assets/characters/<id>/v1.webp` | Transparent production sprites; differ from the concept sheet looks |
| `characters/maya_chen.webp`, `daniel_reyes`, `olivia_hart`, `lucas_weber` | Figures of `prompts/assets/concepts/people/v2.webp` | Paper background removed automatically |

No art yet: `cabin_player` (start room), corridors and stairs, the other cabins.
