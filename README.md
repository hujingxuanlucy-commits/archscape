# ArchScape

Interactive prototype for **ArchScape** — an app for architects, photographers and urban
explorers to capture buildings, build a visual path through the city, and share it.

Eleven screens in a phone shell, navigable the way the real app would be: tab bar, back
buttons, card taps. No page list, no shortcuts.

## Run it

```bash
python3 build/serve.py
```

Then open <http://localhost:4318/archscape.html>. Or just open `archscape.html` directly —
it is a single self-contained file with every photo inlined.

## What to try

| Screen | Worth trying |
| --- | --- |
| Onboarding | Four steps — pick a role, pick themes, start exploring |
| Discover | Nearby / Trending / Following / Saved swap the spot list |
| Capture | Wait ~2.5s for a passive scan, **or** hit the shutter to shoot first |
| Capture | "Not this building? Scan again" re-reads the same frame for another match |
| Check-in | Editable building details; Publish drops the post into Community |
| Journey Map | Toggle the Architecture / Art Spaces / Photography route layers |
| Profile | Captures / Saved / Journeys tabs pin to the top on scroll |
| Search | Browse by style, or search across name, city and style |

## Design system

Taken from the brand board in `reference/`:

| Token | Value | Use |
| --- | --- | --- |
| Signal red | `#952324` | Accent, primary actions, Architecture route |
| Ink | `#0F0F0F` | Dark ground |
| Paper | `#FAF8F5` | Light ground |
| Steel | `#3E6B9A` | Art Spaces route |
| Graphite | `#666666` | Photography route |
| Bone | `#E5E0D8` | Rules and borders |

Cormorant Garamond for display, Inter for UI. The organising idea is the transit map:
every journey is a coloured line through the city, and the lines cross, diverge and
reconnect like the people who walk them.

## Build

`archscape.html` is **generated** — edit `build/app.template.html`, not the output.

```bash
pip install pillow
python3 build/crop.py     # cut photo assets out of reference/ -> build/assets.json
python3 build/maps.py     # cut the two map textures, paint out baked-in markers
python3 build/build.py    # template + assets -> archscape.html
```

`build.py` alone is enough for markup, CSS or JS changes; the crop steps only need
re-running if the imagery changes. The build emits pure ASCII — every non-ASCII character
becomes an HTML entity or `\u` escape — so the page renders correctly regardless of what
charset a server sends.

## Layout

```
archscape.html          the built app, self-contained
build/
  app.template.html     source of truth: markup, CSS, JS
  assets.json           photos as base64 data URIs
  crop.py  maps.py      asset extraction from reference/
  build.py  serve.py    build and local preview
reference/              original design mockups and brand board
```
