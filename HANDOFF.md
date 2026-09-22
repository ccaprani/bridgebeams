# HANDOFF — bridgebeams agent briefing

Read this fully before touching anything. It covers state, conventions,
blockers, and the exact next actions.

## Repository

- Local: `~/projects/bridgebeams`, branch **`ukie-beams`** (all work is on
  this branch; PR #1 `aus-sections` and PR #2 `ukie-beams` are open,
  stacked, NOT merged).
- Remote: `github.com/ccaprani/bridgebeams` (private until merged).
- Environment: `source ~/anaconda3/etc/profile.d/conda.sh && conda activate pybridge`
  then `python -m pytest tests/ -q` — 180 tests, all passing.
- Install: `python -m pip install -e .`

## What this package is

Standard precast/prestressed concrete bridge beam sections as
`sectionproperties` `Geometry` objects (millimetres), for use with
`sectionproperties`, `concreteproperties`, `PyBridge`, and `ospgrillage`.
**22 families across 15 subpackages, 10 jurisdictions.**

## Package layout

```
src/bridgebeams/
├── _geometry.py        # shared: mirror-symmetric polygon builder, shoelace props
├── adapters.py         # to_concreteproperties(), osp_grillage_properties()
├── aus/                # Super-T (T1-T5), I-girders (1-4) — AS5100.5 App D
├── ie/                 # Ireland: T, TY/TYE, Y/YE, U/SU, M/UMB, SY/SYE, MY/MYE
│   └── data/*.json     # published tables + reconstruction params + sources
├── jp/                 # Japan: JIS A 5373 T-girders (AG18-24, BG18-24)
├── kr/                 # Korea: KHC PSC I-girders (25/30/35 m)
├── tr/                 # Türkiye: KGM I-girders (I90-I170)
├── za/                 # South Africa: Civilcon I-beams (I1-I20)
├── ru/                 # Russia: Soyuzdorproekt 3.503.1-81 33 m I-beams
├── th/                 # Thailand: DOH IG-205 (20 m)
├── gr/                 # Greece: Egnatia extended-I (45 parametric sections)
├── be/                 # Belgium: FEBE standardised I-beams (900-2050)
├── pl/                 # Poland: Mosty-Łódź T12-T27
└── uk/                 # UK: STUB — planned CBDG families (inverted-T, M, I, box)
```

Each family module follows the same pattern: a frozen `Dimensions`
dataclass with an `.outline` property (list of (x, y) points, anti-clockwise,
origin at mid-soffit, y up), and a `Section` class exposing `.polygon`
(shapely) and `.geometry` (sectionproperties). Data JSONs carry the
published tables (test fixtures), fitted parameters, residual summaries,
and source citations.

## Conventions and gotchas (READ BEFORE CODING)

1. **The mirror bug.** When building a mirror-symmetric polygon from a
   right-half profile, you MUST include the soffit corner point in the
   mirrored list. Omitting it silently produces a self-intersecting
   polygon whose shoelace area is wrong (typically halves it). This bug
   has bitten three times. Always hand-verify: compute the area of one
   known size analytically and compare.
2. **y-reference bug.** Published `Ixx` is about the horizontal
   *centroidal* axis. Polygon shoelace gives I₀ about y=0 (soffit).
   Convert: `Ic = I0 − A·cy²`. Forgetting this produces Ixx errors of
   ±50–300%. Also: when computing `cy` from the shoelace formula, use the
   *signed* area denominator (`signed = cr.sum()/2`) so the centroid is
   correct regardless of winding direction.
3. **Mixed y-references in outlines.** Top flange underside: measured from
   the TOP of the section (`y = d − ttf`). Bottom flange top: measured
   from the SOFFIT (`y = bft`). Mixing these causes self-intersection at
   the flange edges. Always construct half-outlines bottom-up with
   monotonic y.
4. **Fitted-family tolerances.** Where the profile is a documented
   reconstruction (not exact published dims), the test tolerances are
   set to the documented residual + margin. Do not tighten without
   refitting. Do not loosen without justification in the data JSON.
5. **Stroke-font labels.** Dimension annotations in manufacturer CAD
   drawings are stroke-font vector paths — invisible to text extraction
   AND to OCR (they are graphics, not text). The only way to read them is
   a human or a vision model looking at a rendered image.
6. **Skip-file patterns.** Some package `__init__.py` files use lazy
   imports; the top-level `bridgebeams/__init__.py` re-exports
   everything. When adding a new family, update BOTH the subpackage
   `__init__` and the top-level `__init__`, plus create a test file.

## Validation philosophy

Where the manufacturer publishes section properties (A, yc, Ixx), the
tests validate computed geometry against those tables. Tolerances:

| Family | Area | Centroid | Ixx | Why not exact |
|---|---|---|---|---|
| IE T | <0.01% | <0.02% | <0.02% | exact published profile |
| IE TY/TYE | <0.01% | <0.02% | <0.02% | exact |
| IE U/SU | ≤0.05% | ≤0.05% | ≤0.3% | exact |
| IE Y | 3.5% | 2.1% | 4.8% | fitted reconstruction |
| IE YE | 0.8% | 1.1% | 1.5% | fitted |
| IE M | ≤0.7% | ≤0.7% | ≤0.7% | fitted web/block |
| IE SY/SYE | <0.05% | <0.05% | <0.05% | near-exact |
| JP AG/BG | N/A | N/A | N/A | no published tables; structural checks only |
| TR KGM | N/A | N/A | N/A | analytic validation |
| ZA Civilcon | exact | exact | exact | exact published profile |
| KR KHC | +2% | +2% | +3% | tabulated haunches heavier than as-built |
| RU Б3300 | 0.3% rms | 0.3% | 0.3% | fitted |
| GR Egnatia | N/A | N/A | N/A | thicknesses are user parameters |

## Remaining work — by blocker

### 1. Vision-digitisation tasks (documents in hand, dims visible to a
human/vision reader but not machine-extractable)

These require rendering PDF pages to PNG and reading them visually
(e.g. the `read` tool on a saved image). All PDFs are already downloaded.

| Family | Document | Location | What to read |
|---|---|---|---|
| Japan AG/BG web+flange | THR/PCCEN Tohoku PDF (44 pp) | `/tmp/dims_review/thr_pccen.pdf` | pp. 27–31 may have the standard-section drawing; Table 6 of the source paper has full dims for the Korean KHC equivalents |
| NZ Super-T 1225 confirmation | RR 364 S1.25 | `/tmp/dim_extract/nz/rr364.pdf` p. 26 (index 25) | same section, +200 mm deeper; confirm web taper dims |
| Norway NTB/KTB flange thicknesses | V426 form drawings K201/K202 | `/tmp/dims_review/v426.pdf` (12 MB, drawings-only) | locate form drawing pages by rendering; read flange/web dims per height (600–1400) |
| Qatar Q-beams T2–T5 | Ashghal SD 5-1-101 | `/tmp/qatar_sdd/SD-5-1-101_Rev1_Q-Girder-Sections.pdf` | render regions T2 (330,45,655,360), T3 (645,45,970,400), T4 (15,505,340,740), T5 (335,505,665,790) pt; read per-type: base width, tent low level, tent rise |
| Greece flange thicknesses | Frontiers 2020 Fig. 2–5 | `/tmp/dim_extract/gr/g002.jpg` etc. | the paper's figures are charts, NOT dimensioned sections; the cross-section detail is left to the designer by intent |

### 2. Purchase-gated (no free source exists)

| Family | Source | Cost |
|---|---|---|
| Japan full per-part dims | PCCEN handbook 2020 | ¥3,080 https://www.pcken.or.jp/publications/list/ |
| Norway V426 printed copy | Statens vegvesen | free but raster-only |

### 3. No national catalogue exists (documented, not blocked)

Mexico, Argentina, Chile, Colombia, Sweden, Saudi Arabia, UAE, Vietnam,
Philippines — these countries adopt AASHTO/BS/EN standards or use
producer catalogues. Producer leads are in
`sources/research/research-global-catalogue.md`.

### 4. Implementation candidates (data in hand, not yet coded)

| Family | Status | Blocker |
|---|---|---|
| Qatar Q-beams (5 types) | Type 1 + Type 5 dims fully read; T2–T4 interpolation scripted | one careful topology pass (see gotcha #1); all dims in `sources/research/research-qatar-ashghal.md` Appendices B–C |
| Greece flange thicknesses | published as design choices, not dims | encode as required constructor args (already done in `gr` module) |
| South Africa M/Y/T/U | same British families as IE; Civilcon publishes full tables | needs its own module + decoding (the Civilcon tables use a different notation from Banagher) |
| Russia other series | Б1200–Б3300 range, several widths | data recovery from Russian-language mirrors |
| NZ hollow-core (587/650/900) + I-beams (1500/1600) | RR 364 drawings available | same vision-digitisation task |

## Source registry

All URLs, access dates, licensing notes, and research briefs are in
`sources/SOURCES.md` and `sources/research/*.md` (14 briefs). The
`sources/` directory is **gitignored** (working materials, not
committed). If you need the source PDFs, re-download them — the URLs are
in the registry.

## The dims_review.html tool

`dims_review.html` at the repo root (gitignored) is a self-contained
HTML page for human vision-reading of drawing images. It embeds
rendered drawing sheets as base64 images with labelled input boxes per
dimension, zoom sliders, localStorage persistence, and a "Copy results"
button that outputs all entries as `key: value` lines.

To rebuild it with different images, see `sources/SOURCES.md` for the
render commands (PyMuPDF `get_pixmap` at 3–5× zoom on the target PDF
page). The pattern: render → base64 → embed in HTML → human reads →
copy results → parse → implement.

## Commit and push protocol

The user (Colin Caprani) reviews all work before merge. Push to the
`ukie-beams` branch (or a new branch for new jurisdictions). PR #2
tracks this branch. Do NOT merge. Do NOT push to main. Commit with
descriptive messages. `sources/` is gitignored — do not force-add it.
