# Extraction record: Netherlands (Haitsma) and Romania (ASA CONS), September 2026

New packages: `bridgebeams.nl` (46 profiles) and `bridgebeams.ro` (6 profiles).
Units are mm, the origin is at mid-soffit and y points upwards. The companion data is in
`docs/research/data/extraction-netherlands-romania-2026-09.json`. The per-size transcriptions,
conventions and residuals are in the package JSON files:

- `src/bridgebeams/nl/data/haitsma_hko.json`
- `src/bridgebeams/nl/data/haitsma_hrp_hip.json`
- `src/bridgebeams/ro/data/asa_grinda_pod.json`

Every dimension coded below was read from a rendered page that I looked at: 150–2400 dpi PNG crops, plus the vector paths extracted with `pdftocairo -svg` for ASA.

## Sources

| Source | Local file | SHA-256 | Pages |
|---|---|---|---|
| Haitsma Beton, *HKO HKO-XL* folder ([PDF](https://www.haitsma.nl/media/kbqasilf/hko-hko-xl-folder.pdf)), PDF created 2021-04-14 | `sources/expansion/europe-americas/nl_hko.pdf` | `85d30809…4c4513` | PDF p2 |
| Haitsma Beton, *HRP- en HIP-brugliggers* ([PDF](https://www.haitsma.nl/media/241925/folder-hrp-hip.pdf)), PDF created 2018-02-22 | `sources/expansion/europe-americas/nl_hip.pdf` | `37a0eb77…7b71` | PDF p2 (HRP-ligger), p3 (HIP-ligger) |
| Haitsma HIP web page (snapshot; URL not in registry) | `sources/expansion/europe-americas/nl_haitsma.html` | — | — |
| ASA CONS România (Consolis) catalogue ([PDF](https://asacons.ro/wp-content/uploads/2025/09/ASA-CONSOLIS-catalog.pdf)) | `sources/expansion/europe-americas/ro_asa.pdf` | `443d7d9a…12bd` | PDF/printed p97 (Grindă pod 42, 52), p99 (72, 80), p101 (95, 105) |

## Netherlands: Haitsma

### HKO-ligger (`HaitsmaHkoSection`, HKO300–HKO700, 9 profiles, transcribed-with-convention)

- **Transcribed (mm):** 990 = 360 + 270 + 360. The flange edge is 75 high, followed by a 30 flat and a 30 × 13 chamfer up to y = 88. The flange top then rises 17 to the theoretical root at (±135, 105). The dimensioned values are r = 15 at the soffit corner and a 5 mm side-face draft. The stem is straight from the root to the table top width B at y = H. The drawn HKO600 has 495 = 600 − 105 and B = 484, which confirms this reading.
- **Estimate:** the stem-root fillet is undimensioned. I took r = 15, matching the dimensioned soffit radius; the drawing scales to about 13 mm. The intermittent Ø75/105 transverse holes ("Sparingen") are excluded.
- **Finding:** the inertia multiplier is **×10⁹ mm⁴**. The printed column (header "mm4") gives 1.20 and 10.57. The model gives 1.196e9 and 10.53e9, and the sharp outline gives 1.200e9 and 10.56e9.
- **Residuals:** area −0.16 to −0.67% (the table has 3 significant figures), centroid ≤ 0.9 mm, I −0.08 to −0.41%.
- **Pinned:** HKO650 printed I = 13.27 is a source outlier. The model gives +1.54%, and the value breaks the 10.57 / 16.95 progression.

### HKO-XL-ligger (`HaitsmaHkoXlSection`, HKO-XL300–800, 11 profiles, **estimate**)

- **Printed:** only 415 + 350 + 415 = 1180 and "min 300 max 800". The table gives Z, A, I (10e6 mm4), Wo and Wb.
- **Estimate:** I scaled the H = 800 outline from a 2400 dpi render. The horizontal and vertical scales agree against 1180. The profile is a flange with a 5 mm draft and a 6 mm lip, a 350 mm stem, a splay, and a 600 mm vertical top. I fitted two offsets to all 11 rows: the splay moved 9 mm inward and the flange-top band lowered 9 mm. Each size is the H = 800 outline truncated at y = H. The published area increments support this: they are linear in H up to about 620 and 600 mm²/mm above that.
- **Residuals:** area −0.12 to +0.59%, Z ≤ 1.2 mm, I ≤ 0.49%. The +0.5% area from HKO-XL700 upwards follows from a 27 500 mm² step in the source (650→700) where 30 000 is expected.
- An invisible text layer on p2 contains another table ("400 390 2,39E+05 147 3,28 …"). It does not render and was not used.

### HRP-ligger (`HaitsmaHrpSection`, HRP500–1600, 12 profiles, fitted-reconstruction)

- **Transcribed:** 220 + 215 + 300 + 215 + 220 = 1170 and the vertical chain 66 / 84 / 20 / 130 from the soffit. The stem is B = 300; the published area steps are exactly 30 000 per 100 mm.
- **Estimates:** the drawing shows several undimensioned features. I scaled the 20 × 20 bottom chamfers, the 15 mm top-edge chamfer and a plank rebate at the stem top (drawn about 36 × 13; adopted 35 × 15). I fitted the side shear-key recess depth to Ab/V/I: least squares gave 30.9, the drawing scales about 20, and I adopted 30. The recess has a 45° lower bevel from y = 66 and a top at 135.
- **Residuals:** area +0.08 to +0.16%, V ≤ 0.9 mm, I ≤ 0.27%. The sharp outline without keys would give +1.0 to +2.1% area and +1.5 to +2.7% I.

### HIP-ligger (`HaitsmaHipSection`, 2 × 9 profiles, fitted-reconstruction)

- **Natte knoop** (wet joint / dwarsnaspanning): the top is 300 + 880 + 300 with the chain 300 / 69 / 22 from the top. The bottom is 490 + 125 + 250 + 125 + 490 = 1480 with the chain 59 / 103 / 121 / 100 from the soffit.
- **Druklaag** (+200 mm topping): the top is 1440 overall with 90 / 185 from the top. The bottom is the same as natte knoop.
- **Estimates scaled from the vector drawing:**
  - Bottom edge rebate: 25 in, 15 up at y = 59, then a 5 mm draft to y = 162.
  - Druklaag top ledges: 25 wide × 57 deep, so the top face is 1390.
  - Druklaag underside: breaks from the 90 edge to (625, H − 100).
  - The druklaag drawing is asymmetric (joint profile). I mirrored the dimensioned right side.
- **Residuals:** natte knoop area ≤ 0.30%, V ≤ 0.5 mm, I ≤ 0.11%. Druklaag area +0.03%, V ≤ 0.5 mm, I ≤ 0.20%.
- **Pinned:**
  - HIP1200 natte knoop area is −0.68%. The 888 000 → 907 000 step (19 000) contradicts the 250 mm web; every other step is 25 000.
  - HIP1700 natte knoop I = 3.70E+11 is +1.74%; it breaks the progression.
- **Edition conflict:** the PDF tables are 1200–2000 mm. The web page states "tussen de 1600 en 2400mm" for both the druklaag and dwarsnaspanning variants. I implemented the PDF tables. The heights above 2000 mm are unverified, and the web page may describe a later edition.

## Romania: ASA CONS "Grindă pod"

The source units are cm, and superscript digits are decimals (8² = 8.2, 2⁵ = 2.5). No area or inertia values are published, so validation is analytic: chain closure plus tangent residuals. The earlier transcriptions in `visual-followup-za-ro-nepal` were re-read and confirmed. That report's 48.8 mm radius argument is superseded by the construction below.

| Mark | Depth | Top | Bottom (max / soffit) | Vertical chain | Provenance |
|---|---|---|---|---|---|
| 42 | 42 | 22 (19+22+19 chain) | 60 / 53 (1, 2.5, 53, 2.5, 1) | 2.5 + 7.5 + 7 + 20 + 5 | transcribed-with-convention |
| 52 | 52 | 22 | 60 / 53 | 2.5 + 7.5 + 7 + 20 + 15 | **estimate** (stem width 14 assumed) |
| 72 | 72 | 102 (33.5+4+27+4+33.5) | 92 / 85 | 2.5+8.5+8+5+27+4.8+8.2+8 | transcribed-with-convention |
| 80 | 80 | 102 | 92 / 85 | 2.5+8.5+8+5+35+4.8+8.2+8 | transcribed-with-convention |
| 95 | 95 | 120 (42+10+16+10+42) | 47 / 45 (1+45+1) | 12+21.5+39.5+10+2+10 | transcribed-with-convention |
| 105 | 105 | 118 (40+10+18+10+40) | 50 / 50 | 12+24.5+44.5+10+2+12 | **estimate** (lower slope 45°) |

### Conventions

- **42:** the 14 callout is the theoretical sharp intersection, at the "7" level (y = 17), of the tapered stem (22 at y = 37) and the lower-flange slope from (30, 10). The printed "5" leader (no R prefix) is read as R = 50 mm, inscribed tangent to both faces. The tangent points lie 45.3 mm from the corner.
- **52:** the stem width is not printed. I copied 14 from 42. The vector outline extrapolates to about 12.6 cm, and its flange slope differs from 42's (0.37 vs 0.29), so this is an estimate.
- **72/80:** the straight chains are kept as printed and R = 50 is kept exact.
  - Upper fillet, tangent to the web and to the 8.2/33.5 slope (13.75°): horizontal extent 38.1 (printed 40), vertical extent 48.5 (printed 48), web tangent at 509 / 589 (printed 510 / 590).
  - Lower fillet: the circle is tangent to the web at the printed 240 level. The flange face is the tangent from the edge (460, 110) and meets the circle at y = 191.9 (printed 190).
  - All residuals are ≤ 2 mm.
  - The 72 strand view prints 90 cm where the section prints 92. The geometry follows the dimensioned section.
- **95/105 reading:** the first vertical label (10 on 95, 12 on 105) is taken as the flange-edge thickness, followed by the "2" underside drop and the 10 fillet zone. Only this reading closes to 95 and 105. The vector drawings are drawn at 93 and 103 cm, which corresponds to the other reading. The stated depth governs.
- **95/105 fillets:**
  - Top R100: the web tangent is within 0.1 mm of the printed level. The horizontal extent is 95.2 / 95.0 against the printed 10 cm, because that 10 cm is measured to the theoretical knee.
  - 95 lower R200 on the 6 : 8.7 slope: the web tangent is at 331.9 (printed 335).
  - 105 lower slope: undimensioned. I used 45°, close to the drawn ~46°. The web tangent is at 362.8 (printed 365).
- **Excluded:** end blocks, strands and ducts. The Somaco GP series, a separate producer, is not used.

## Remaining uncertainties

- None of the HRP/HIP key, rebate or ledge sizes is dimensioned in the source. The HRP recess depth is fitted and deviates from its scaled value (30 vs about 20).
- HKO-XL is an estimate from an undimensioned drawing. The HKO root fillet is estimated.
- The HIP range differs between the PDF (1200–2000) and the web page (1600–2400).
- The ASA 52 stem width and the 105 lower slope are assumptions. The ASA drawings are not to scale.
