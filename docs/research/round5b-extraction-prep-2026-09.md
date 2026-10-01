# Round 5b: extraction prep and visual-audit implementation (2026-09-26)

**Current outcome: five nominal profiles implemented — one Finnish model
and four Iranian source-sheet sections. Estonia and the Cambodian standard
drawing lead remain blocked by missing geometry/source acquisition. There
is no remaining image-capability blocker.** Machine record:
`docs/research/data/round5b-extraction-prep-2026-09.json`.

Chronology: the initial text-only prep stopped before geometry extraction
and reported no image support. A subsequent Class C visual audit, with
parent confirmation of Finnish A–A and Iranian p52, superseded its tentative
interpretations. This implementation uses that approved audit, not OCR guesses.
The detailed local evidence is in
`sources/expansion/round5-extraction/vision-audit/findings.md`.
PDF pages below are 1-based. All profiles are bare concrete; CIP slab,
reinforcement, permanent formwork and end blocks are excluded.

## Finland — TIEL 2160004-2000 "Jännitetty elementtisilta" (highest value)

`sources/expansion/round5-extraction/fi/TIEL-2160004-2000-jbe00.pdf`
(84 pp, SHA-256 8a9b1788…, from tieh.fi/sillat/julkaisut/jbe00.pdf).
PageMaker PDF; all figures are embedded rasters; body text extracts fine.

| What | Where |
|---|---|
| **Figure 1 — the three section types, dimensioned** (rect / trapezoid / I) | PDF p11 (embedded image 1697×903; extracted to `fi/img/fig-000.png`) |
| Second figure (typical deck section, spacings) | PDF p12 (`fi/img/fig-001.png`; OCR: Hl=6500, 200/1175 overhangs, 1650 spacings) |
| LIITE 1 model drawings (7 sheets incl. 1.4 jännepalkki) | PDF pp25-31 (CCITT scans, extracted to `fi/img2/m-00*.png`) |
| LIITE 3.1 material consumption curves (not a size matrix) | PDF p39; p38 contents, p40 slab quantities |
| LIITE 4 calculations / design example | PDF pp41-84 (text) |

Figure 1: rectangle width450; trapezoid bottom500/top300; I-profile
bottom600/web180/top300, slab230 (all mm). PDF pp10–12 describe nominal,
customizable design/mould choices, not a fixed national size matrix. Combined
heights1200/1500/1800/2100 include the slab and are not bare girder SKUs.
LIITE 3.1 plots material quantities against span, not tabulated sizes.

Implemented `bridgebeams.fi.TielModelISection("TIEL-model-AA-h1270")`:
PDF p28, printed **LIITE 1.4 A–A**, one 30 m-span model example, not a
national SKU. Its 12-vertex outline has bottom600/web180/top300 and vertical
stack210+210+600+50+200=1270 mm. No rectangular/trapezoid families or
combinations of mould choices are extrapolated.

PDF p51 (LIITE 4 printed p11) gives rounded A=0.39 m², cy=0.51 m,
Ixx=0.063 m⁴, using the three-rectangle idealization specified on p49
(LIITE 4 printed p9): widths600/180/300, layer heights315/730/225 mm.
The exact nominal polygon instead has A387900 mm², cy510.466615107 mm,
Ixx62,950,060,542.666 mm⁴ (audit-derived, **not printed**). The rectangle
approximation has the same area but cy508.509280742 mm and
Ixx63,263,640,491.589 mm⁴. Both round to the source values; those values
are corroboration only, not tight analytical validation targets.

## Estonia — E-Betoonelement ViaPlus

`sources/expansion/round5-extraction/ee/ViaPlus.pdf` (20 pp, SHA-256
8cc3bcd7…) + `karptala_scr_2012.pdf` (1 p, 28992495…) + saved web page.

**Visual correction:** ViaPlus p9 dimensions bare ZIP bottom width1180 mm,
not1200. The1200 is slab-strip width/beam centre spacing; both240 labels
are CIP slab thicknesses, not web/flange dimensions. `max500` is a
horizontal edge overhang. The stem, haunch heights and flange-tip details
remain incompletely dimensioned.

On p10, heights755–1955 mm include beam plus slab. Bar-end labels15.0–44.0
and their green counterparts are **spans in metres, not masses**; no bare
area is available from this chart. Subtracting240 cannot complete the
missing outlines or establish a13-size catalogue.

The box brochure gives width950, height800–1000, length≤27 m and maximum
mass42 t, with a hollow middle and solid support regions. It lacks wall,
void, haunch and taper dimensions and a discrete height catalogue; photographs
are not dimensioned sections. **ZIP, edge and box implementations remain
blocked pending dimensioned manufacturer drawings.**

## Iran — RMTO Publication 102 (typical bridge deck drawings ≤ 20 m)

`sources/expansion/round5-extraction/ir/RMTO-102.pdf` (56 pp, 10.8 MB,
SHA-256 981cc9d2…; obtained through the picofile generateDownloadLink
endpoint from the civil20.blogfa.com mirror — the official RMTO copy
needs an archive request). Fully scanned (no text layer).
The visual audit positively established PSC (p6 PRETENSIONING/STRAND and
selected-sheet strand captions); ordinary RC sheets also occur. Implemented
`bridgebeams.ir.Rmto102InvertedTSection` entries:

| Catalogue locator | PDF page | Printed sheet | Bare h mm |
|---|---:|---|---:|
| RMTO102-8-4-h370 | 52 | 8-4 | 370 |
| RMTO102-8-5-h470 | 51 | 8-5 | 470 |
| RMTO102-8-7-h770 | 54 | 8-7 | 770 |
| RMTO102-8-8A-h1000 | 56 | 8-8, part A | 1000 |

Each nominal 8-vertex inverted-T has bottom500/web200, bottom vertical80
and haunch rise150 mm, ending below the separate180 mm CIP slab. Sheet
names are locators, not manufacturer SKUs; p51/p52 are not in ascending
span order. No bare A/cy/I property table was identified; tests independently
derive properties from rectangles and triangles.

**Withheld:** p53 sheet8-6 h620 omits its upper width chain, so the200 mm
web cannot be silently inherited. Other PSC slab, spaced-girder and small
culvert/joist families remain untranscribed. Geometry is source-visible,
but official version/current applicability of the mirror is unverified.

## Cambodia — MPWT standard drawings (downgraded)

The sweep's IMPLEMENTABLE claim was **downgraded to LEAD-NO-DIMS**.
The retained `kh/jica-2011-bridge-standard-drawings.pdf` (SHA-256 d13addf6…)
is actually the **March2013** Final Report Volume III Appendix of *The
Project for Study on the Improvement of Existing Bridges in the Kingdom
of Cambodia*: p5 lists the bridge inspection survey, not standard drawings.
The filename is misleading. The Prakas/MPWT drawing title and span ranges
remain unverified leads; actual drawing sheets were not acquired.

The audit's public curl request to
`https://www.mpwt.gov.kh/en/documents/declaration/39` timed out after45 s
(exit28). **Only timeout is established**, not a viewer wall or browser
access restriction. A lawful public/browser acquisition remains follow-up;
no implementation can be made from this inspection report. Existing Cambodian
catalogue profiles from other sources are unaffected.

## Evidence retention and remaining work

All five acquired PDFs (FI, IR, two EE brochures, KH inspection report) are
copied under country subfolders in `~/Downloads/bridgebeams-manual/`, with
`round5-source-manifest.json` and `round5-SHA256SUMS` at that store's root.
Hashes are also recorded in the machine record and new package data. No
source was deleted. The old no-vision blocker is historical only; remaining
blocks are missing EE geometry, missing KH drawings, IR h620 width
corroboration and residual families, plus source-version limitations.
