# HANDOFF — bridgebeams agent briefing (v2)

Read this fully before starting work.

## Repository

- Local: `~/projects/bridgebeams`, branch **`ukie-beams`**
- Remote: `github.com/ccaprani/bridgebeams` (private)
- PRs #1 (`aus-sections`) and #2 (`ukie-beams`) are open, stacked, NOT merged
- Environment: `source ~/anaconda3/etc/profile.d/conda.sh && conda activate pybridge`
- Test: `python -m pytest tests/ -q` — 180 tests, all passing
- Docs: `cd docs && python -m sphinx -b html source _build/html` (zero warnings)

## Current state (as of this handoff)

**22 families, 15 subpackages, ~10 jurisdictions implemented:**

| Package | Family | Validation |
|---|---|---|
| `ie` | T, TY/TYE, Y/YE, U/SU, M/UMB, SY/SYE, MY/MYE (11 families) | exact to 2.6% |
| `aus` | Super-T (T1–T5), I-girders (1–4) | ported from v0.1 |
| `jp` | JIS A 5373 T-girders AG18–24, BG18–24 | structural checks |
| `kr` | KHC PSC I-girders (25/30/35 m) | +2–3% vs literature |
| `tr` | KGM I90–I170 | analytic |
| `za` | Civilcon I1–I20 | exact |
| `ru` | Soyuzdorproekt Б3300 | 0.3% rms |
| `th` | DOH IG-205 (20 m) | drawn dims |
| `gr` | Egnatia extended-I (45 sections) | depth law + widths |
| `be` | FEBE I-beams (900–2050) | evidence-flagged |
| `pl` | Mosty-Łódź T12–T27 | two-producer attested |
| `nz` | Super-T 1025/1225 | Colin-confirmed drawing read |
| `uk` | STUB (planned CBDG families) | — |

Plus: `adapters.py` (concreteproperties + ospgrillage), clickable world map
in docs, executed tutorial notebook, `HANDOFF.md` (this file).

## Reference PDFs (local, gitignored)

All stored in `sources/pdfs/` — do NOT commit:

| File | Content |
|---|---|
| `nzta-rr364.pdf` (6.6 MB, 57 pp) | NZ standard beam designs: Super-T, hollow-core, I-beams |
| `nzta-rr252.pdf` (700 KB, 70 pp) | Stage 1 survey (NZ/AU/UK/US/CA beam practice) |
| `nzta-highway-structures-design-guide.pdf` | NZ context doc |
| `japan-thr-pccen.pdf` (9.2 MB, 44 pp) | JIS A 5373 AG/BG girder design/construction |
| `japan-mlit-chubu-cb005.pdf` (3 MB, 66 pp) | MLIT Chubu guideline (AG/BG dims on p28) |
| `norway-v426.pdf` (12.3 MB) | NTB/KTB form drawings (raster, no text layer) |
| `qatar-sd-5-1-101.pdf` | Q-beam sections (5 types, 1:10 vector) |
| `qatar-sd-5-1-111.pdf` | TY-beams (property table extracted) |
| `05316-precast-beam-properties.xls` | Original spreadsheet (19 IE/UK families + 50 DWGs) |

Also: `~/Downloads/bridgebeams-manual/` — Colin's 15-country source library
(ae au br cl ee fi ir kh nz ph sa tn us/mi us/oh us/or) with round-5 manifest.

## What needs doing — priority order

### 1. NZ I-beam 1500 (RR 364 page 45)

Colin confirmed: **"The 1500mm deep TI girder dims are all on p45 of the PDF."**
Render page 45 at high zoom, find the cross-section drawing, read ALL dims
(top flange width/thickness, web, bottom flange width/thickness, haunches).
Then implement `bridgebeams.nz` I-beam family.

The previous agent struggled to read the dimension callouts from the scanned
drawing — the text is CAD stroke-font (graphics, not text layer). Use the
`dims_review.html` tool (below) for Colin to read dims visually.

RR 252 also gives historic NZ I-beam types by flange width × depth:
200×750, 350×900, 450×1150, 500×1400 (flange width confirmed by Colin).

### 2. NZ hollow-core (RR 364 S2.x sheets)

Colin confirmed: **"the hollow core beam info is all there"** in the RR 364 PDF.
The S2.x sheets (pages ~29–50) have the 650-deep and 900-deep hollow-core
deck unit sections with dimensions. Render + read + implement.

### 3. Qatar Q-beams (SD 5-1-101)

Type 1 (800 deep) fully read (see `sources/research/research-qatar-ashghal.md`
Appendix B). Type 5 (1900) read (Appendix C). Types 2–4 need vision reads.
Base-width law verified linear: `base = 1091 − 2·depth/10.55`.
Colin noted: **"These are all standard Aussie super T"** — same topology family.

### 4. Norway NTB/KTB (V426 form drawings)

V426 PDF is raster drawings-only. Colin checked pages 11–14, 20–21: no
dimensioned cross-sections found. NTB designation format decoded:
`NTB [bottom-flange width]−[web]×[height]` (e.g. NTB 1200-220×1000).
Needs form-drawing pages K201/K202 (may need NZTA/SVV request).

### 5. Belgium FEBE flange thicknesses

FEBE PDF at `https://www.febe.be/wp-content/uploads/2017/07/FEBE_Standardisation-Poutres-Prefabriquees-pour-Ouvrages-dart_4e-editon-2017_sec.pdf`
returns 403 to automated fetchers. Opens in a normal browser. Colin (or
anyone with a browser) can download it, then read the per-height m-values
and flange thicknesses.

### 6. Michigan/Oregon/other manual collection

`~/Downloads/bridgebeams-manual/us/mi/` has MDOT I-beam and bulb-tee
detail sheets with TEXT LAYERS (2275 words on PC-1N). `us/or/` has BR360/375
girder drawings. These may be directly implementable without vision reads.

### 7. Japan full detail

AG/BG section drawing found on p28 of the MLIT Chubu guideline
(`japan-mlit-chubu-cb005.pdf`). Current implementation uses the simplified
profile (800×160 top flange, 300 web). The full drawing may have more detail.

## The dims_review.html tool

**How it works:** render PDF pages to PNG at high zoom → base64-embed in a
self-contained HTML page → labelled input boxes per dimension → Colin reads
and types values → "Show Results" → copy-paste back to the agent → implement.

**Location:** `dims_review.html` at repo root (gitignored, 12 MB with images).

**Key lesson:** the previous agent's own vision reads of dimension callouts
were unreliable — it kept showing Colin crops that weren't the right areas.
The tool works best when you:
1. Render the FULL page first (no cropping)
2. Let Colin identify which area has the section drawing
3. THEN zoom into that specific area
4. Ask targeted questions ("what is the top flange width?")

**Clipboard API doesn't work on file:// origin** — use a "Show Results"
textarea that Colin selects and copies manually.

## Coding conventions (READ THE EXISTING CODE)

Every family module follows this pattern (see `src/bridgebeams/ie/ie_t_beam.py`
for the reference implementation):

```python
@dataclass(frozen=True)
class XxxDimensions:
    depth: float
    # ... other dims
    @property
    def outline(self) -> list[tuple[float, float]]:
        # anti-clockwise, origin at mid-soffit, y up, mm
        ...

class XxxSection:
    SIZES = ("X1", "X2", ...)
    def __init__(self, size: str): ...
    @property
    def polygon(self) -> Polygon: ...
    @property
    def geometry(self): ...  # sectionproperties Geometry
```

Data JSONs in `<pkg>/data/` carry published tables (test fixtures),
fitted parameters, residuals, source citations.

## Critical gotchas (each one has caused a bug)

1. **Mirror bug**: when mirroring a right-half profile, include the soffit
   corner. Omitting it silently halves the area.
2. **Ixx reference**: published Ixx is about the CENTROID. Shoelace gives
   I₀ about the soffit. Convert: `Ic = I0 − A·cy²`.
3. **Winding**: compute `cy` using the SIGNED area denominator so the
   centroid is correct regardless of winding direction.
4. **y-references**: top flange underside from the TOP (`d − ttf`);
   bottom flange top from the SOFFIT (`bft`). Mixing these causes
   self-intersection.
5. **Fitted tolerances**: don't tighten without refitting; don't loosen
   without justification.
6. **Stroke-font labels**: dimension annotations in CAD drawings are
   vector graphics — invisible to text extraction AND to OCR. Only
   vision reading works.

## Source registry

All URLs, access dates, licensing: `sources/SOURCES.md`.
Research briefs: `sources/research/*.md` (16+ files).
`sources/` is **gitignored** — do not commit.

## Commit protocol

Push to `ukie-beams` branch. PR #2 tracks. Do NOT merge. Do NOT push to
main. Commit with descriptive messages. Test before committing.
