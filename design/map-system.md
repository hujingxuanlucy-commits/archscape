# ArchScape Map System

One cartographic language, three grammars. The basemap, type, and control furniture are
identical everywhere; what changes per screen is the single question the map answers and,
critically, **what its color encodes**. Today all three maps reuse the Journey map's
content-category routes (Architecture / Art / Photography), which is why they read as one
map pasted three times. This spec separates them.

**The one rule that fixes the mixing:** on any given map, hue carries exactly one meaning.

| Dimension          | A · Explore → Nearby            | B · My Journey Map               | C · Path Crossings                  |
|--------------------|---------------------------------|----------------------------------|-------------------------------------|
| Subject            | Places near you                 | One day's walk                   | Paths in relation                   |
| Question answered  | "What's worth walking to?"      | "Where has today taken me?"      | "Who is near my path?"              |
| **Color encodes**  | **POI category**                | **Stop status**                  | **Person**                          |
| Lines              | None                            | One chronological route          | My line + ≤3 dotted friend lines    |
| Markers            | Category discs with state       | Numbered sequence discs          | Avatar discs + plain dots           |
| Legend             | Category filters (tappable)     | Status key (static)              | People toggles (tappable, avatars)  |
| Label density      | Basemap only                    | Basemap + selected stop          | Basemap, minimal                    |

---

## A. Explore → Nearby — POI-first, discovery-oriented

**Shows.** The district around the user's position and the places worth walking to:
a *you-are-here* marker plus POI discs. Nothing else. Orientation, not narration.

**Points, not clusters, not paths.**
- Individual points at today's data density (~9 POIs). Dormant cluster rule for future
  density: ≥3 markers within 18 screen px collapse to a cluster disc (r 9, paper fill,
  1.6px ink stroke, ink count numeral); splits apart on zoom.
- **No route lines, ever, on this map.** The two route fragments currently drawn
  (arch + art) are removed. A route is a story; this screen is a shelf.

**Marker color = category.** This is the only screen where category hue paints the map:
Architecture `#AF2B34` · Art Spaces `#3B6E9D` · Photography `#7B7C79`.

**Marker states** (all at POI radius, see tokens):
- **Recommended** (default): solid category disc, 2px paper keyline.
- **Saved**: category disc with an inner paper ring at 0.45r (donut) — "marked by me."
- **Visited**: paper-filled disc with 2px category stroke (hollow) — "already mine."
- **Selected**: 1.4×, white core dot, name label above. The only labelled POI.
- **You are here**: 7px ink `#2B2B2B` disc, 2px paper ring, 14px halo at 12% ink. Not a
  category color, not gold — a fixed, quiet anchor.

**Labels.** Basemap registers only (districts, water, park). POIs stay unnamed until
selected; the Nearby Spots cards below the map do the naming.

**Legend.** None by default (the map is subordinate here). If filtering is ever needed,
the category chips above the feed are the filter — the map obeys them; no on-map card.

---

## B. My Journey Map — one journey, in time

**Primary route logic.** The main line is **today's walk**: one continuous polyline
through the day's check-ins in chronological order (MoMA 09:41 → Seagram 10:26 →
Chrysler 11:12 → …), drawn in journey red `#AF2B34`, stepping along the street grid.
The three parallel category routes are retired from this screen. The line means one
thing: *the path my feet actually took, in order.*

- **Walked** segments: solid, full weight, paper halo.
- **Up next** segment (from the last check-in to the next planned stop, e.g.
  Guggenheim 11:58 in the timeline): same red, dashed 2 : 1.4, 65% opacity, no halo.

**Stops = sequence, not category.**
- Discs at POI radius carrying their **sequence numeral** (8px, 700, paper).
- **Completed**: solid red disc, paper numeral.
- **Current** (latest check-in): 1.3×, white core, soft red halo — the focal mark.
- **Upcoming**: paper fill, 2px red stroke, red numeral.
- Category is *demoted to the timeline*: the Stops Today rows keep their category dot;
  the map does not repeat it.

**Map ↔ timeline coupling.** Same sequence numbers in both. Tap a map stop → its
timeline row highlights (and scrolls into view); tap a row → map flies to that stop and
selects it. Selection is one shared state, not two.

**Legend = status, not content.** Three static rows, not toggles:
`— Walked · - - Up next · ◉ Current stop`. (Category toggles move out of this screen's
life entirely; "All journeys" remains a separate page, no ghost lines on the default view.)

**Search stays inside the map** (per reference map1), stats bar and Stops Today below
are untouched.

---

## C. Path Crossings — social, overlap-oriented

**My path = one line.** The *same* single chronological journey line as screen B (one
source of truth, literally the same polyline data), solid red, full weight. Never the
three category routes. My stop discs are demoted to plain 3.5px red dots — on this
screen my itinerary is context, not subject.

**Friends.**
- Each friend = **one dotted line in their personal hue** (0.7× my weight, round dots,
  85% opacity, no halo) + an **avatar marker at the head of their path**: 26px circle
  containing their avatar art from the shared registry, 2px paper ring + 1.5px
  personal-hue outer ring. Tap → their profile card.
- Earlier waypoints on a friend's path get no markers (dots on the line suffice) —
  multiple fully-marked itineraries is exactly the noise to avoid.
- **At most 3 friend paths at once.** Others collapse into the "+N nearby" count in the
  header badge and the list below; toggling in the legend swaps who is drawn.

**Crossings / proximity.**
- Where a friend's path passes within ~150m of mine: one **soft halo** — red `#AF2B34`
  at 18%, r = clamp(10 + scale·110, 12, 19)px, no stroke — centered on my path's nearest
  vertex. One halo per crossing; tap target 28px; tap → that friend's card / meet CTA.
- Halos mark *crossings only*, never ambient radii around every friend.

**Legend = people.** Two sections: **My route** (one row: solid red swatch, "You") and
**Other explorers** (one row per drawn friend: 16px avatar + handle + dotted swatch in
their hue). Friend rows toggle their path. No category vocabulary anywhere on this screen.

---

## Shared design tokens

### Basemap (already shipped — unchanged)
| Token | Value |
|---|---|
| Ground (land) | `#EAE3D4` |
| Streets | `#FAF7EF` minor · `#FDFBF4` avenues · `#FFFEF9` major |
| Water | `#C7D7E1` |
| Parks | `#CBD8B9` |
| Blocks (scale > 0.3 only) | `#E1D7C2` @ .9 |
| Bridges / borough fabric | `#F2EDE1` / `#F4EFE4` |

### Label registers
| Register | Spec |
|---|---|
| Districts | caps, 8.5px 600, tracking .17em, `#8C8272`, ground-tint halo |
| Boroughs (wide zoom) | caps, 11px 600, tracking .22em, `#6F6758` |
| Water / park names | display italic 13.5px, `#6F8CA1` / `#6D875E`, two-line stack |
| Selected name | 10px 600 ink `#2B2B2B`, paper halo 3.4px |

### Color roles — a hue never means two things on one screen
| Role | Values | Lives on |
|---|---|---|
| Category | arch `#AF2B34` · art `#3B6E9D` · photo `#7B7C79` | Explore markers only |
| Status | walked/current red `#AF2B34` solid · up-next red dashed @65% · visited = outline · saved = donut | Journey |
| People | you `#AF2B34` · rose `#C2748C` · sky `#6E93B8` · moss `#6F8F63` | Crossings |
| Meet / anchor accents | gold `#C9922E` (meet point) · ink `#2B2B2B` (you-are-here) | any |

Red is deliberately both "Architecture" (Explore) and "me/my path" (Journey, Crossings) —
legal because the meanings never co-occur on a screen.

### Lines (scale-adaptive; `sc` = px per mercator metre)
| Style | Spec |
|---|---|
| My route / walked | w = clamp(3.4 + sc·30, 3.4, 5.2); paper `#FBF8F1` halo w+2.2 @ .6; round joins |
| Up next | same w, dash w·1.6 / w·1.3, 65% opacity, no halo |
| Friend path | 0.7w, dot dash `0.1 / w·1.75`, round caps, 85% opacity, no halo |

### Markers
| Marker | Spec |
|---|---|
| POI / stop disc | r = clamp(5.8 + sc·40, 6.4, 8.4); keyline `#FBF8F1` 2px |
| Selected | r×1.4, white core r·0.34, +name label, keyline 2.6px |
| Sequence numeral | 8px 700 paper, centered |
| Small dot (demoted stop) | r ≈ 0.55× POI radius, no numeral |
| Avatar marker | 26px circle, avatar SVG from the people registry, paper ring 2px + person-hue ring 1.5px |
| You-are-here | ink 7px + paper ring 2px + 12%-ink halo 14px |
| Cluster (dormant) | r 9 paper disc, ink stroke 1.6px, ink count |

### Map furniture
| Piece | Spec |
|---|---|
| Legend card | `rgba(250,248,243,.93)`, 1px `rgba(0,0,0,.07)` border, r6, 10/13px padding; h4 8.5px caps .18em; rows 11.5px; solid swatch 21×3px, dotted swatch = 2.5px dotted border in person hue |
| Zoom / FIT | existing white card column, unchanged |
| Search field | Journey map only, bottom inset, unchanged |
| Interaction | lazy pointer capture at 4px; zoom clamp 0.0045–2.6; **FIT frames the screen's subject**: Explore = POIs + you; Journey = today's line; Crossings = my line + drawn friends |

### Default frames (measured off the reference sheets)
| Map | lat, lng, scale | Frame height |
|---|---|---|
| Explore | 40.7601, −73.9820, 0.0423 | 272px |
| Journey | 40.7584, −73.9820, 0.0401 | 364px |
| Crossings | 40.7584, −73.9820, 0.0401 | 330px |

---

## Delta vs. today (implementation checklist, in order)

1. **Explore**: delete the two route fragments; add marker state styling
   (recommended / saved / visited) + you-are-here; keep POIs unlabelled until selected.
2. **Journey**: build one chronological polyline from the Stops Today data (replacing
   the three category ROUTES on this screen); sequence-numbered stop discs with
   completed / current / upcoming states; dashed up-next leg to the next planned stop;
   legend → static status key; two-way map↔timeline selection.
3. **Crossings**: my line becomes that same single journey polyline; friend paths gain
   avatar head-markers; my stops demote to plain dots; legend rows gain 16px avatars
   (structure already people-based); halo token unchanged.
4. **Shared**: no renderer rewrite needed — `makeLiveMap` already parameterises places /
   routes / layers / cross; the work is data shape (status + sequence on stops, person
   on routes) plus marker-state rendering.

**Open questions** (small, non-blocking):
- Up-next leg needs one "planned" stop in the journey data — the timeline already shows
  Guggenheim 11:58, so the data exists; confirm it should render as planned rather than
  completed.
- Cluster rule stays dormant until POI density grows — agreed?
