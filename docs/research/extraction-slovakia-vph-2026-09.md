# Slovakia: VÁHOSTAV VPH-PTMN bridge beams, extraction record (September 2026)

Scope: the precast prestressed bridge beams in the VÁHOSTAV-SK-PREFA, s.r.o.
(Horný Hričov) producer catalogue. The machine-readable companion is
[extraction-slovakia-vph-2026-09.json](data/extraction-slovakia-vph-2026-09.json).
The implementation is in `src/bridgebeams/sk/vph_ptmn.py`, with data in
`src/bridgebeams/sk/data/vph_ptmn.json` and tests in `tests/test_sk_vph_ptmn.py`.

## Sources

| Role | Title (original) | URL | Local file | SHA-256 (first 16) |
|---|---|---|---|---|
| Primary, English | PRESTRESSED BEAMS VPH-PTMN for the road bridges and the bridge accessories: PRODUCT ASSORTMENT OUTLINE | https://vph.sk/assets/Uploads/ProduktPage/14/PRESTRESSED-BEAMS-VPH-PTMN.pdf | sources/expansion/europe-americas/sk_vph_en.pdf | da0a17b02464df4d |
| Slovak original | PREDPÄTÉ NOSNÍKY VPH-PTMN (Katalóg mostných nosníkov) | https://vph.sk/assets/Uploads/ProduktPage/14/Katalog-mostnych-nosnikov.pdf | sources/expansion/europe-americas/sk_vph.pdf | 2e2f81545b4a161a |

The English PDF metadata gives a creation date of 2017-03-17, so the status
is recorded as "producer catalogue". The printed sheet numbers equal the PDF
page numbers. All 36 section-constant values in the Slovak text layer (decimal
commas) are identical to the English ones. The English p14 heading "2016-T" is
a copy error: the Slovak heading reads "NOSNÍK VPH-PTMN 2010".

The drawings are raster images at 200–270 ppi. On pp 6–21 I extracted them
at native resolution with `pdfimages` and read them zoomed 2–5×. For p23 I
also used the separately drawn centre-of-beam prestressing view.

## Profiles implemented (12 distinct cross-sections, 20 catalogue rows)

| Size (SIZES) | Original title / designation | PDF p. | Depth | Provenance |
|---|---|---|---|---|
| 2016-PM11-K / -M | Nosníky tvaru obráteného „T“ … VPH-PTMN 2016 – PM, 11m (krajný „K“ / stredný „M“) | 6 | 400 | transcribed |
| 2016-PM13-K / -M | … 2016 – PM, 13m | 8 | 500 | transcribed |
| 2016-PM15-K / -M | … 2016 – PM, 15m | 10 | 575 | transcribed |
| 2016-T | … so zníženou výškou 1,0m „VPH-PTMN 2016-T“ (18/21/24 m) | 12 | 1000 | transcribed |
| 2010-I-1.2 | Nosníky tvaru „I“ … s výškou 1,2m „VPH-PTMN 2010“ (18/21/24 m) | 14 | 1200 | transcribed |
| 2016-I | … so zníženou výškou 1,2m „VPH-PTMN 2016-I“ (27/30/32 m) | 16 | 1200 | transcribed |
| 2010-I-1.4 | … s výškou 1,4m „VPH-PTMN 2010 I“ (27/30/32 m) | 18, 19 | 1400 | transcribed |
| 2010-R2-1.9 | … dĺžky 38m s výškou 1,9m „VPH-PTMN 2010-R2“ | 21 | 1900 | transcribed-with-convention |
| 2010-R2-2.1 | … dĺžky 42m s výškou 2,1m „VPH-PTMN 2010-R2“ | 23 | 2100 | transcribed (property discrepancy pinned) |

The brief's figure of "18" does not match the source. The catalogue has 20
rows. Rows that differ only in production length share one drawing and one
set of section constants, so they are exposed as `designations` of a single
size rather than counted twice.

## Transcription (mm, as printed)

- **2016-PM (all).** The vertical edge is 55. The splay chain is fillet 44 + slope 132 + fillet 44 = 220 (right-hand side: 220). The horizontal chain is 26 + 247 + 26 under a 300 projection. All corners are R=50.
  - M units: 820 = 300 + 220 + 300, with a 220 stem.
  - K units: 780 wide, with a 480 block and a 300 ledge.
  - The "170 from top" dimension on p6 M runs to the upper splay tangent line (400 − 170 = 230 ≈ 55 + 44 + 132 = 231), not to the stem corner.
- **Lower flange (all girders).** SKOSENIE 15/15, edge 140, then 44 + 132 + 44 (right-hand side 220), and 26 + 247 + 26 / 300. On the R2 girders the chain is written 15 + 125 + 44 + 132 + 44 = 360 and 184 + 176.
- **2016-T.** Body 980, raised roughened strip 140 × 20 (40 + 140 + 40 = 220) to 1000. Stem 220, bottom 410 + 410.
- **2010 I 1.2 / 1.4.** Top 30 + 270 + 200 + 270 + 30 = 800, rebate 30 × 20. The left chain is 33 + 49 + 36 + 49 = 167 and the right chain 75 + 92 = 167. The horizontal chain is 42 + 216 + 42. The straight web is 673 or 873 and the web is 200.
- **2016-I.** Top and bottom are both 820, web 220, rebate 40 × 20. The chain is as for 2010 I except that the right chain prints 33 + 135 (a slip for 134).
- **2010-R2 1.9.** Top 40 + 720 + 40 = 800, left chain 33 + 49 + 36 + 49, right chain 82 + 85 labelled 168, straight web 1372, bottom 15 + 770 + 15.
- **2010-R2 2.1.** Top 40 + 1020 + 40 = 1100, rebate 40 × 20. The chain is 20 + 55 + 59 + 49 = 183, with 183 on the right. There is no radius at the flange edge (it is sharp); R50 appears at the web only. Straight web 1557, web 200, bottom as for 1.9. The centre-of-beam view reads 20 + 53 + 61 + 49 = 183, and scaling it gives the same outline.

## Conventions

- The R=50 fillets are true tangent arcs. The printed tangent points are used, and the theoretical sharp corners are solved from them. The resulting extents are 26.5/44.1 on the lower splay and 42.3/49.3 on the 1:6 upper splay, which matches the printed values.
- The top roughening is modelled as flat.
- Excluded from the outline: the optional PE-pipe voids ("možné vyľahčenie", R50), the PE rúra Ø50, the DET. A transverse holes, prestressing, ducts and end blocks.
- Soffit chamfers are included on the girders. None are drawn on the PM units.

## Decisions on drawing slips

1. **p18/p19 web "100", splay "249".** Both pages embed the same image (PDF object 312), so the slips appear on both. I used web 200 and splay 247, based on the upper 200 label, the 800 total and the right-hand side. With these values the residuals are A −0.03 %, yt −0.1 mm and I −0.05 %.
2. **1.9 m, 167 vs 168.** I adopted 168 by making the flange edge 34 instead of 33. This closes the chain: 168 + 1372 + 360 = 1900. The residuals are −0.03 % / 0.0 mm / −0.07 %. Keeping 167 with a 1373 web gives −0.11 % / −0.8 mm / −0.25 %.
3. **2016-I "135".** I used 134 (a total of 167), because the depth closes with it.

## Residuals (computed − published)

| Size | A | yt (mm) | Iy |
|---|---|---|---|
| 2016-PM11-K | +0.21 % | +0.3 | +0.40 % |
| 2016-PM11-M | 0.00 % | +0.5 | +0.39 % |
| 2016-PM13-K | +0.17 % | +0.6 | +0.31 % |
| 2016-PM13-M | **+0.48 %** | +1.0 | +0.31 % |
| 2016-PM15-K | +0.15 % | +0.4 | +0.27 % |
| 2016-PM15-M | +0.22 % | +0.6 | +0.27 % |
| 2016-T | −0.11 % | −0.7 | −0.53 % |
| 2010-I-1.2 | −0.03 % | −0.4 | −0.05 % |
| 2016-I | −0.11 % | −0.7 | −0.25 % |
| 2010-I-1.4 | −0.03 % | −0.1 | −0.05 % |
| 2010-R2-1.9 | −0.03 % | 0.0 | −0.07 % |
| 2010-R2-2.1 | −0.13 % | **−30.2** | **−4.80 %** |

The PM areas are printed to 3 s.f., so a residual of ±500 mm² is rounding.

## Remaining uncertainties

- **2010-R2 2.1 m.** The drawing is closed and self-consistent, but the table is not. No single plausible misreading reproduces the published yt of 1.016 m and I of 0.39284 m⁴. A 3-parameter least-squares fit needs a 137 mm flange edge and a 186 mm web, and both views contradict that. The profile is implemented as drawn and the residuals are pinned in the tests. The published constants may belong to a different (earlier or heavier-flanged) design; this is unverified.
- **2016-PM13-M area.** The model gives 0.209 m² against the printed 0.208 m². The centroid and inertia agree.
- **2016-PM inertia.** Every unit, K and M alike, is +0.27 to +0.40 % above the published inertia. The cause is unknown, and the tests pin this band.
- **2016-T and 2016-I.** Both are 395 mm² below their 5-s.f. published areas. The same deficit on both 2016 designs suggests a shared detail that is not drawn.
- **Superseded assessment note.** The earlier assessment reported a "PM M units ~3 mm high" centroid. That came from the misreading of the 170 dimension described above; with the correct chain the M centroids agree to within 1 mm.
