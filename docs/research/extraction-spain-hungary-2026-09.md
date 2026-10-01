# Extraction: Spain HP-1 (1977) and Hungary Ferrobeton (2026-09-23)

Machine-readable companion: `docs/research/data/extraction-spain-hungary-2026-09.json`.
Code: `src/bridgebeams/es/` (`Hp1BeamSection`) and `src/bridgebeams/hu/`
(`FerrobetonFpSection`, `FerrobetonFptSection`, `FerrobetonItgSection`,
`FerrobetonFi150Section`). Tests: `tests/test_es_hp1.py`, `tests/test_hu_ferrobeton.py`.

## Spain — «Colección de tramos con vigas pretensadas. Tipo HP 1»

- Orden de 9 de febrero de 1977, Ministerio de Obras Públicas; BOE núm. 118,
  18 mayo 1977, pp. 10886–10915. Sheets titled «Colección de vigas tipo HP-1»,
  Dirección General de Carreteras.
- URL: https://www.boe.es/boe/dias/1977/05/18/pdfs/A10886-10915.pdf
- Local: `sources/expansion/europe-americas/es_hp1.pdf`, SHA-256
  `79e5556d26a2c39db9d36989437e6e23e4ac8734d3bedc2ecc4a8fcaf68683a7`.
- **Status: historic 1977 standard.** The Order made its use optional (apartado 2.º).
  A reported 1985 annulment was not audited.

The 300 dpi JBIG2 images were extracted at native resolution with `pdfimages`.
SECCION I-I was cropped at ×2 and read on every sheet, and the SEMIALZADO chains
were checked against it. Dimensions are in metres, read top to soffit as: flange
edge / top splay / web / bottom splay / bottom edge.

| Tipo | PDF p | BOE p | Hoja | Canto | Top | Web | Bottom | Vertical chain | Hormigón m³/m | Molde m²/m |
|---|---|---|---|---|---|---|---|---|---|---|
| I | 6 | 10891 | 3 | 1,30 | 0,80 | 0,16 | 0,56 | 0,10 0,14 0,64 0,20 0,22 | 0,445 | 3,74 |
| II | 9 | 10894 | 6 | 1,50 | 0,80 | 0,16 | 0,60 | 0,10 0,13 0,80 0,22 0,25 | 0,504 | 4,21 |
| III | 13 | 10898 | 10 | 1,70 | 0,90 | 0,16 | 0,70 | 0,10 0,15 0,91 0,27 0,27 | 0,620 | 4,82 |
| IV | 17 | 10902 | 14 | 1,90 | 1,00 | 0,19 | 0,75 | 0,10 0,16 1,06 0,28 0,30 | 0,753 | 5,33 |
| V | 20 | 10905 | 17 | 2,10 | 1,10 | 0,19 | 0,80 | 0,10 0,17 1,23 0,30 0,30 | 0,842 | 5,89 |
| VI | 24 | 10909 | 21 | 2,30 | 1,20 | 0,19 | 0,80 | 0,10 0,18 1,37 0,30 0,35 | 0,934 | 6,37 |

**Validation.** The drawing has no fillets, so the model uses the straight-line
outline exactly as drawn.

- **Area.** Computed area agrees with the «Mediciones – sección central» concrete
  volume per metre within the table's 3-decimal rounding for every type. Residuals
  are −0.045 / 0.000 / +0.032 / +0.027 / −0.018 / −0.011 %.
- **Formwork.** This is a second, independent check: «Molde» m²/m equals the
  outline perimeter minus the top face within 2-decimal rounding, with residuals
  of +0.11 % or less.
- **Other properties.** No centroid or inertia is published.

Type IV's top-width callout "1,00" is faint, but both checks confirm it.

## Hungary — Ferrobeton Zrt. producer catalogue

The sheets are vector CAD (A4) drawn at exact scale. Callouts were read from
500–600 dpi renders. Superscript digits are decimals (3⁵ = 3.5 cm).

Arcs and chamfers without printed dimensions were measured from the vector paths
(`pdftocairo -svg`, circle fits, residual ≤0.001 cm). The implemented outlines
reproduce the vector vertices within 0.01 mm (FPT), 0.05 mm (FI-150) and 0.25 mm
(ITG, where the 16 cm web is drawn as 16.04).

| Family | Local file | SHA-256 |
|---|---|---|
| FP-20A/30A/37A jelű feszített hídgerenda (pp 1–3) | `hu_fp.pdf` | `612f6be52a2993cbf226e93bd29389a6f892eba7a6653870cb8733fad1d6f35a` |
| FPT jelű feszített hídgerenda család (p1) | `hu_fpt.pdf` | `d8454ca3481405e7e408f866cf56caf7dbbf69349a838322230e4cd0d0096c38` |
| ITG jelű feszített hídgerenda család (p1) | `hu_itg.pdf` | `1668284a851b7c45db7954a32d873565eb7ccab5d6cbe26655ac2cd19f7aeabb` |
| FI-150 jelű feszített hídgerendák (p1) | `hu_fi150.pdf` | `e661f3753aa5479364c765e651459b79f4b098acd3711e537b8d42ca96cb0240` |

(Local files under `sources/expansion/europe-americas/`; full ferrobeton.hu URLs are in the JSON. None of the sheets carries a printed page number.)

**FP (transcribed).** The outline is:

- 47 cm flat soffit, with 1.5 × 1.5 chamfers out to the 50 cm overall width;
- a 4.5 cm vertical edge;
- a 3.5 cm ledge that rises 0.5 cm to the 43 cm body.

The body is 13.5, 23.5 or 30.5 cm deep, giving overall depths of 20, 30 or 37 cm.
The projecting 13/15 cm stirrups are excluded. No property data is published.

**FPT.** Printed dimensions:

- top 6 + 58 + 6 = 70, web 30;
- flange chain 4 + 0.5 + 10.5 + 3.5;
- web length «változó» (variable);
- depths 45;70;80;90;100;130.

The remaining features are measured from the CAD vector, not printed:

- The top face slopes 1.0 cm outward over 4.0 cm down to the ledge root at a
  30.0 cm half-width.
- Radii: ledge root R1, ledge tip R1, flange outer corner R2.5, web fillet R2.5.
- Bottom arrises have 2 × 2 chamfers.

Validation used the tabulated Súly at an assumed 2500 kg/m³. Nothing was fitted.

- FPT-70/80/90/100/130 agree within 0.02 %, which is why these are
  `transcribed-with-convention` and not `fitted-reconstruction`.
- **Pinned:** FPT-45 on the same template gives 492.3 kg/m against 455 kg/m
  (+8.2 %). It is kept as `estimate`.
- **FPT-70/50** (the «EHGE 70» edge-girder replacement) is a separate, fully
  dimensioned sharp outline: 50 top, 16.75 + 1.75 + 51.5, web 30. **Pinned:** it
  gives 613.1 kg/m against 620 kg/m (−1.1 %).

**ITG (Tartóközép, midspan).** ITG-90 is fully chained and polygonal:

- top 0.6 + 5.7 + 1 + 46.6 + 1 + 5.7 + 0.6 = 61.2;
- vertical 4.5 + 9.8 + 2.8 + 11.1 + 35.2 + 8.6 + 18 = 90;
- web 16;
- bottom 35, widening to 36.4 at 18 cm.

ITG-70 and ITG-110 are `estimate`: only the 35.2 web segment changes (15.2 and
55.2). **ITG-45 is not implemented.** The fixed non-web chain totals 54.8 cm,
which exceeds 45 cm, and the 45 is bracketed in the source. The support
(Tartóvég) section is excluded.

**FI-150 (`estimate`).** Printed dimensions:

- top 80 (0.5 + 4 + 71 + 4 + 0.5), web 14.6, bottom 60 (1.5 + 57 + 1.5);
- vertical 4 + 12 + 23 + 93 + 8 + 7.5 + 0.5 + 2 = 150.

The fillet radii are not printed. The CAD-measured values used are:

- ledge root R1, ledge tip R1, flange lower tip R2.5;
- web/top flange R7.5, web/bulb R15, bulb corner R2.5.

The straight lines are transcribed; the radii are best estimates, so the whole
section is labelled `estimate`.

## Corrections to the prior assessment

- The FPT-70 mass residual is −0.02 %, not +1.8 %. The fillets
  and chamfers change the area by only about 0.2 cm², so the earlier figure must
  have come from a different sharp-outline reading. That reading was not traced.
- The Ferrobeton "undimensioned" fillets are present in the vector geometry, so
  they were measured rather than guessed.

## Remaining uncertainties

- HP-1 post-1977 legal status is unaudited.
- ITG-70/110 scaling is an assumption.
- The cause of the FPT-45 and FPT-70/50 mass discrepancies is unknown.
- The FPT check depends on the assumed density.
- The Ferrobeton sheets are undated. The ITG file name hints at 07/2015
  (unverified).
