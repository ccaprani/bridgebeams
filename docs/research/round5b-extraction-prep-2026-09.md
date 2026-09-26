# Round 5b: extraction prep for the four implementable leads (2026-09-26)

Sources for the four highest-value leads from the round-5 sweep were
downloaded and catalogued this session. **Geometry extraction did not
start**: every section drawing is raster (or viewer-walled) and this
session's model has no image support (the Michigan round's sheets were
read visually). The page maps and text-layer data below make a
vision-capable session turnkey. Machine record:
`docs/research/data/round5b-extraction-prep-2026-09.json`.

## Finland — TIEL 2160004-2000 "Jännitetty elementtisilta" (highest value)

`sources/expansion/round5-extraction/fi/TIEL-2160004-2000-jbe00.pdf`
(84 pp, SHA-256 8a9b1788…, from tieh.fi/sillat/julkaisut/jbe00.pdf).
PageMaker PDF; all figures are embedded rasters; body text extracts fine.

| What | Where |
|---|---|
| **Figure 1 — the three section types, dimensioned** (rect / trapezoid / I) | PDF p11 (embedded image 1697×903; extracted to `fi/img/fig-000.png`) |
| Second figure (typical deck section, spacings) | PDF p12 (`fi/img/fig-001.png`; OCR: Hl=6500, 200/1175 overhangs, 1650 spacings) |
| LIITE 1 model drawings (7 sheets incl. 1.4 jännepalkki) | PDF pp25-31 (CCITT scans, extracted to `fi/img2/m-00*.png`) |
| LIITE 3.1 material quantities per size | PDF pp38-40 (text tables) |
| LIITE 4 calculations / design example | PDF pp41-84 (text) |

Text-layer facts already extracted (prose, p10-11): spans L 16-40 m; beam
spacings k 1.8/2.1/2.4/2.7 m (1.5 for L/H=24); slenderness L/H 15/20/24;
three section types (suorakaide / puolisuunnikas / I); beam widths 500 and
600 nominal (RunkoBES alternatives 480/580); I-beam top-flange height
200-500 mm; web formwork heights 300/600/900/1200 → total heights (with
slab) 1200/1500/1800/2100 mm; strand 93 mm² (St 1570/1770) or 100 mm²
(St 1630/1860). Figure-1 OCR fragments: 100/300/100, 300, 180, 450/500/600.
**To do in a vision session: read Figure 1 + LIITE 1.4 dims, build the
size matrix from LIITE 3.1, validate against LIITE 4 if properties appear.**

## Estonia — E-Betoonelement ViaPlus

`sources/expansion/round5-extraction/ee/ViaPlus.pdf` (20 pp, SHA-256
8cc3bcd7…) + `karptala_scr_2012.pdf` (1 p, 28992495…) + saved web page.

Text-layer facts: ZIP beam (inverted T) — section drawing on **ViaPlus.pdf
p9** with text dims **1200 (flange) / 240 / 1180 / 240 / h1 (variable) /
max 500 (fascia)**, beam centres n×1200; structure-height series **755,
855, 955, 1055, 1155, 1255, 1355, 1455, 1555, 1655, 1755, 1855, 1955 mm**
(INCLUDES the CIP slab; span nomogram p10 with mass labels 15.0-44.0 t →
printed areas available). Box beam (karptala): width 950, height
800-1000, length ≤27 m, mass ≤42 t, fascia trapezoidal, central void with
stiffness ribs ~5 m, solid near supports (brochure text; section drawing
in brochure is raster). **To do: view p9 drawing to assign the 240s
(flange depth vs stem width) and the 1180; then build ZIP series (13
heights, slab-dependent) + box 950×800..1000 as far as the void geometry
is printed.**

## Iran — RMTO Publication 102 (typical bridge deck drawings ≤ 20 m)

`sources/expansion/round5-extraction/ir/RMTO-102.pdf` (56 pp, 10.8 MB,
SHA-256 981cc9d2…; obtained through the picofile generateDownloadLink
endpoint from the civil20.blogfa.com mirror — the official RMTO copy
needs an archive request). Fully scanned (no text layer).
**To do in a vision session: page-by-page survey (Persian), find the
پیش‌تنیده (prestressed) prestressed girder/slab sheets, transcribe.**

## Cambodia — MPWT standard drawings (downgraded)

The sweep's IMPLEMENTABLE status was **downgraded to LEAD-NO-DIMS** in the
round-5 record: the cited JICA report (12112595, kept at
`kh/jica-2011-bridge-standard-drawings.pdf`, SHA-256 d13addf6…) is the
Final Report Vol III **bridge inspection survey**, not the drawings; the
actual Prakas 511/2012 standard drawings sit on the viewer-walled MPWT
page (mpwt.gov.kh/en/documents/declaration/39). **To do: browser fetch
(Colin's signed-in browser or a browser agent) of the MPWT documents
page; then vision transcription of the hollow-slab 15-25 m and PCDG
18-30 m sheets.**

## Blocker note

Extraction needs an image-capable model session (the Michigan round
sheets were read at 110-600 dpi renders). This session's model and its
subagents return NO-VISION. All raster renders are pre-generated in
`sources/expansion/round5-extraction/` (`fi/img`, `fi/img2`, renders for
Iran/Cambodia to be made at 300 dpi when vision returns).
