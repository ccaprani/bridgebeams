# Banagher Solid Box and W families: existing-PDF transcription

Read on 22 September 2026 from the existing 62-page **Bridge Beam Manual, 3rd Edition**, Banagher Precast Concrete. [Original registry source](https://files.brintex.com/Occurrence/291/Brochure/7518/brochure.pdf). This pass re-opened the local PDF; it did not re-fetch that inherited external URL.

Local source: `sources/banagher-bridge-beam-manual-3ed.pdf`. SHA-256: `5432e2db0b2f95045320f91254c52ce3f7b1f6d62279c6f05ae6aef4e46bb7bf`. Machine-readable transcription: `data/banagher-pending-families.json`.

The two tables provide **48 sections: 32 Solid Box and 16 W beams**. All published values below were extracted and checked against rendered pages. Drawing dimensions are in millimetres. PDF page numbers are one-based; printed page numbers are separately retained. The 24 verified Solid Box variants are now implemented in `src/bridgebeams/ie/ie_solid_box.py`; width class (4) and W remain research-only.

## Solid Box: PDF page 14, printed page 12

Eight depths, 300–1000 mm in 100 mm steps, each have four width classes. Upper widths are 365/620/840/1370 mm; overall lower widths are 495/750/970/1500 mm. The source prefers the 750 and 970 mm sizes. Each side projects 65 mm at the bottom shoulder. The shoulder rises 30 mm, the outer vertical face is 35 mm high, and the lower corner has a 25 × 25 mm chamfer. Thus the straight upper side starts 90 mm above the soffit, consistent with the drawing’s 910 mm straight side at 1000 mm overall depth.

Published section moduli use 10^6 mm³. No Ixx column is published for this family. Calculated inertia in the JSON is explicitly marked as independent polygon integration, not a transcription.

| Section | Depth mm | Area mm² | Centroid above soffit mm | Top Z, 10⁶ mm³ | Bottom Z, 10⁶ mm³ | Self-weight kN/m |
|---|---:|---:|---:|---:|---:|---:|
| SD1 (1) | 300.0 | 118630.0 | 141.5 | 5.85 | 6.55 | 2.97 |
| SD2 (1) | 400.0 | 155130.0 | 190.6 | 10.37 | 11.39 | 3.88 |
| SD3 (1) | 500.0 | 191630.0 | 240.0 | 16.11 | 17.46 | 4.79 |
| SD4 (1) | 600.0 | 228130.0 | 289.6 | 23.09 | 24.75 | 5.7 |
| SD5 (1) | 700.0 | 264630.0 | 339.3 | 31.28 | 33.26 | 6.62 |
| SD6 (1) | 800.0 | 301130.0 | 389.1 | 40.7 | 42.98 | 7.53 |
| SD7 (1) | 900.0 | 337630.0 | 438.9 | 51.34 | 53.93 | 8.44 |
| SD8 (1) | 1000.0 | 374130.0 | 488.8 | 63.19 | 66.09 | 9.35 |
| SD1 (2) | 300.0 | 195125.0 | 144.9 | 9.7 | 10.39 | 4.88 |
| SD2 (2) | 400.0 | 257125.0 | 194.3 | 17.19 | 18.2 | 6.43 |
| SD3 (2) | 500.0 | 319125.0 | 244.0 | 26.77 | 28.09 | 7.98 |
| SD4 (2) | 600.0 | 381125.0 | 293.8 | 38.42 | 40.05 | 9.53 |
| SD5 (2) | 700.0 | 443125.0 | 343.6 | 52.15 | 54.09 | 11.08 |
| SD6 (2) | 800.0 | 505125.0 | 393.5 | 67.94 | 70.19 | 12.63 |
| SD7 (2) | 900.0 | 567125.0 | 443.4 | 85.81 | 88.36 | 14.18 |
| SD8 (2) | 1000.0 | 629125.0 | 493.3 | 105.74 | 108.6 | 15.73 |
| SD1 (3) | 300.0 | 261125.0 | 146.2 | 13.01 | 13.69 | 6.53 |
| SD2 (3) | 400.0 | 345125.0 | 195.8 | 23.07 | 24.07 | 8.63 |
| SD3 (3) | 500.0 | 429125.0 | 245.5 | 35.95 | 37.26 | 10.73 |
| SD4 (3) | 600.0 | 513125.0 | 295.4 | 51.64 | 53.25 | 12.83 |
| SD5 (3) | 700.0 | 597125.0 | 345.3 | 70.13 | 72.05 | 14.93 |
| SD6 (3) | 800.0 | 681125.0 | 395.2 | 91.43 | 93.66 | 17.03 |
| SD7 (3) | 900.0 | 765125.0 | 445.1 | 115.52 | 118.06 | 19.13 |
| SD8 (3) | 1000.0 | 849125.0 | 495.1 | 142.42 | 145.26 | 21.23 |
| SD1 (4) | 300.0 | 420350.0 | 147.5 | 20.98 | 21.68 | 10.51 |
| SD2 (4) | 400.0 | 557350.0 | 197.3 | 37.24 | 38.26 | 13.93 |
| SD3 (4) | 500.0 | 694350.0 | 247.2 | 58.08 | 59.41 | 17.36 |
| SD4 (4) | 600.0 | 831350.0 | 297.1 | 83.49 | 85.14 | 20.78 |
| SD5 (4) | 700.0 | 968350.0 | 347.0 | 113.48 | 115.44 | 24.21 |
| SD6 (4) | 800.0 | 1105400.0 | 397.0 | 148.03 | 150.31 | 27.64 |
| SD7 (4) | 900.0 | 1242400.0 | 446.9 | 187.15 | 189.74 | 31.06 |
| SD8 (4) | 1000.0 | 1379400.0 | 496.9 | 230.84 | 233.74 | 34.49 |

### Independent drawing/property check

Nominal polygon integration reproduces every published area for width classes (2) and (3) exactly. Class (1) differs by +5 mm², consistent with its area column rounded to tens. Across those 24 variants, centroid differences are below 0.043 mm and section-modulus differences below 0.0052 × 10^6 mm³. The small modulus differences can cross a last-digit half-rounding boundary, so a future test should document its rounding allowance. These 24 sections are implemented with the exact nominal dimensions. The targeted test file `tests/test_ie_solid_box.py` passes 27 tests, including all published property comparisons and a sectionproperties mesh check.

**Width class (4) needs resolution:** published areas exceed the same dimensioned polygon by 225 mm² for SD1–SD5 and 275 mm² for SD6–SD8. Centroid differs by up to 0.112 mm and bottom modulus by up to 0.141 × 10^6 mm³. This discrepancy is larger than ordinary last-digit rounding. Preserve the source values and seek a producer drawing or correction; do not tune the outline to fit the table.

## W: PDF page 30, printed page 28

The source provides two profile regimes, W1–W15 and W16–W19. The column names W1/W2/W3 are drawing dimensions and must not be confused with section designations. `Web` denotes a vertical extent of the sloping inner web segment, not web thickness. A dash in V is preserved as null in JSON.

| Section | Depth mm | Area mm² | Centroid mm | Top Z, 10⁶ mm³ | Bottom Z, 10⁶ mm³ | Ixx, 10⁹ mm⁴ | Self-weight kN/m |
|---|---:|---:|---:|---:|---:|---:|---:|
| W1 | 800.0 | 572360.0 | 305.3 | 71.88 | 116.46 | 35.556 | 14.31 |
| W3 | 900.0 | 606880.0 | 345.9 | 89.54 | 143.43 | 49.614 | 15.17 |
| W5 | 1000.0 | 641400.0 | 387.5 | 108.76 | 171.88 | 66.61 | 16.04 |
| W7 | 1100.0 | 692030.0 | 440.2 | 136.21 | 204.15 | 89.871 | 17.3 |
| W8 | 1200.0 | 726550.0 | 484.2 | 159.46 | 235.73 | 114.14 | 18.16 |
| W9 | 1300.0 | 761070.0 | 528.7 | 184.11 | 268.56 | 142.0 | 19.03 |
| W10 | 1400.0 | 812400.0 | 585.2 | 219.51 | 305.62 | 178.85 | 20.31 |
| W11 | 1500.0 | 846920.0 | 631.3 | 248.01 | 341.33 | 215.46 | 21.17 |
| W12 | 1600.0 | 881440.0 | 677.6 | 277.84 | 378.23 | 256.28 | 22.04 |
| W13 | 1700.0 | 933470.0 | 736.7 | 321.13 | 419.9 | 309.34 | 23.34 |
| W14 | 1800.0 | 975150.0 | 790.6 | 362.63 | 462.97 | 366.03 | 24.38 |
| W15 | 1900.0 | 1016060.0 | 844.3 | 405.7 | 507.3 | 428.3 | 25.4 |
| W16 | 2000.0 | 1057970.0 | 898.6 | 451.09 | 552.89 | 496.83 | 26.45 |
| W17 | 2100.0 | 1102680.0 | 954.5 | 499.74 | 599.75 | 572.45 | 27.57 |
| W18 | 2200.0 | 1150190.0 | 1011.8 | 551.68 | 647.82 | 655.49 | 28.75 |
| W19 | 2300.0 | 1213750.0 | 1081.1 | 622.31 | 701.68 | 758.56 | 30.34 |

| Section | Overall width W1 mm | W2 mm | W3 mm | Web mm | S mm | F mm | V mm |
|---|---:|---:|---:|---:|---:|---:|---:|
| W1 | 1704.4 | 243.2 | 1058.0 | 100.0 | 220.0 | 70.0 | — |
| W3 | 1732.4 | 243.2 | 1086.0 | 200.0 | 220.0 | 70.0 | — |
| W5 | 1760.4 | 243.2 | 1114.0 | 300.0 | 220.0 | 70.0 | — |
| W7 | 1788.4 | 250.2 | 1128.0 | 350.0 | 220.0 | 120.0 | — |
| W8 | 1816.4 | 250.2 | 1156.0 | 450.0 | 220.0 | 120.0 | — |
| W9 | 1844.4 | 250.2 | 1184.0 | 550.0 | 220.0 | 120.0 | — |
| W10 | 1872.4 | 257.2 | 1198.0 | 600.0 | 220.0 | 170.0 | — |
| W11 | 1900.4 | 257.2 | 1226.0 | 700.0 | 220.0 | 170.0 | — |
| W12 | 1928.4 | 257.2 | 1254.0 | 800.0 | 220.0 | 170.0 | — |
| W13 | 1956.4 | 264.2 | 1268.0 | 850.0 | 220.0 | 220.0 | — |
| W14 | 1984.4 | 278.2 | 1268.0 | 950.0 | 248.0 | 192.0 | — |
| W15 | 2012.4 | 292.2 | 1268.0 | 1050.0 | 276.0 | 164.0 | — |
| W16 | 2040.4 | 306.2 | 1268.0 | 1050.0 | 276.0 | 136.0 | 128 |
| W17 | 2068.4 | 320.2 | 1268.0 | 1050.0 | 276.0 | 108.0 | 256 |
| W18 | 2096.4 | 334.2 | 1268.0 | 1050.0 | 276.0 | 80.0 | 384 |
| W19 | 2124.4 | 348.2 | 1268.0 | 1050.0 | 276.0 | 100.0 | 464 |

The drawing also prints 1500 mm nominal lower width, 1460 mm bottom flat, 20 mm horizontal lower-corner projection per side, 50 mm top step height and 40 mm inner top-step projection. The W16–W19 profile adds a 171 mm horizontal web dimension at its kink. These are recorded separately from the property table.

**Geometry remains incomplete:** the concrete profile’s inner bottom-slab vertices, corner radii and lower-corner vertical extent are not all explicitly dimensioned. Appendix C on PDF pp 51–58 gives reinforcement and strand arrangements, which confirm the outlines but do not replace the missing concrete dimensions. Strand cover, pitch and elevation must not be mislabelled as mould geometry. Obtain the producer CAD/mould section before implementation.

## Verification and interpretation

The JSON retains original table scales and units alongside each row’s source page. Polygon checks use the shoelace area, first-moment and second-moment formulas, independently of the package geometry code. This check exposed the wide Solid Box discrepancy; it does not validate structural design capacity. “Soffit” means the beam underside; “section modulus” means the elastic geometric modulus; “self-weight” here is the published approximate force per unit length. No modulus or inertia has been inferred for the incomplete W profile.
