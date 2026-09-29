# ArchScape

ArchScape is an architecture, city, and community experience with two self-contained HTML pages:

- `archscape-showcase.html` — the product case-study website.
- `archscape.html` — the interactive app prototype.

Both pages can be opened directly in a browser. The showcase's visual media is embedded into its HTML so it can also be shared as a single file.

## Repository structure

- `archscape-showcase.html` — shareable showcase page.
- `archscape.html` — generated interactive prototype.
- `showcase-assets/` — current source media for future showcase updates.
- `build/` — scripts and template used to rebuild `archscape.html`.
- `archive/` — earlier showcase exports, retired automation, and original source imagery retained for reference and prototype rebuilds.

## Preview locally

```bash
python3 -m http.server 4173
```

Open `http://127.0.0.1:4173/archscape-showcase.html`.

## Rebuild the prototype

`archscape.html` is generated from `build/app.template.html` and `build/assets.json`.

```bash
python3 build/build.py
```

The crop utilities use their source imagery from `archive/prototype-source/`.
