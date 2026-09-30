# Michigan MDOT dimensions verified from original drawings

Verified 2026-09-30. Governing geometry is MDOT PC-1Q, PC-2L, PC-4J and PC-5D, printed revision **12-22-2025**, PDF page **1**. Full pages were inspected before enlarging sections. Positioned text and dimension-arrow connectivity supported the visual reads; no physical dimensions were measured from drawing scale.

The four existing public families cover thirteen gross midspan profiles. I28 now uses the current 4-inch top edge / 3-inch haunch chain. I70 now includes its dimensioned 2-inch horizontal short-haunch run. API names and sizes are preserved.

## Source identity

| Sheet | SHA256 | Original local source |
|---|---|---|
| PC-1Q | `12bdae9fbfa3f654ed4bb169f15b4f3a7990e2fc68363d77fe23a8d53a083a52` | `/home/ccaprani/Downloads/bridgebeams-manual/us/mi/mdot_PC-1Q_I-beam-details_2025-12-22.pdf` |
| PC-2L | `bd50afeae3a4cda8be83688dece21cc8d489f83553fb63e502d4c389dc4058a7` | `/home/ccaprani/Downloads/bridgebeams-manual/us/mi/mdot_PC-2L_70in-I-beam-details_2025-12-22.pdf` |
| PC-4J | `315a625b55dae7acb3a12ad61a5469f73810633c78106d27fcc018098b65ad56` | `/home/ccaprani/Downloads/bridgebeams-manual/us/mi/mdot_PC-4J_1800-beam-details_2025-12-22.pdf` |
| PC-5D | `6b8064ebbf2741035c8f820715870f8582028e53e0bb7466d2ee72e380e06f04` | `/home/ccaprani/Downloads/bridgebeams-manual/us/mi/mdot_PC-5D_bulb-tee-details_2025-12-22.pdf` |

Independent property reference: `sources/expansion/round3/mi-wayback/redownloaded/live-2026/BDG-complete-set.pdf`; SHA256 `41a5a153fbef6d7fba65ee08301c240b54c21ddae34aecfb547e620290d8c028`. Full original pages were inspected at PDF p125 (printed 6.60.01, issued 02/14/11), p126 (6.60.02, 02/14/11) and p127 (6.60.03, 05/22/23).

## Source dimensions and conversions

Each cell is **published inches → millimetres**, using exactly 25.4 mm/in. Nominal 1800 has a drawn depth 1800.225 mm.

| Profile | Depth | Top flange width | Web | Bottom flange width |
|---|---:|---:|---:|---:|
| I28 | 28 → 711.2 | 12 → 304.8 | 6 → 152.4 | 16 → 406.4 |
| I36 | 36 → 914.4 | 12 → 304.8 | 6 → 152.4 | 18 → 457.2 |
| I45 | 45 → 1143 | 16 → 406.4 | 7 → 177.8 | 22 → 558.8 |
| I54 | 54 → 1371.6 | 20 → 508 | 8 → 203.2 | 26 → 660.4 |
| I70 | 70 → 1778 | 30 → 762 | 6 → 152.4 | 26 → 660.4 |
| 1800 | 70.875 → 1800.225 | 47.25 → 1200.15 | 5.875 → 149.225 | 35.5 → 901.7 |
| BT36 | 36 → 914.4 | 49 → 1244.6 | 8 → 203.2 | 40 → 1016 |
| BT42 | 42 → 1066.8 | 49 → 1244.6 | 8 → 203.2 | 40 → 1016 |
| BT48 | 48 → 1219.2 | 49 → 1244.6 | 8 → 203.2 | 40 → 1016 |
| BT54 | 54 → 1371.6 | 49 → 1244.6 | 8 → 203.2 | 40 → 1016 |
| BT60 | 60 → 1524 | 49 → 1244.6 | 8 → 203.2 | 40 → 1016 |
| BT66 | 66 → 1676.4 | 49 → 1244.6 | 8 → 203.2 | 40 → 1016 |
| BT72 | 72 → 1828.8 | 49 → 1244.6 | 8 → 203.2 | 40 → 1016 |


All thirteen profiles retain **3/4-inch → 19.05 mm** straight bevels at their outside soffit corners. They are concrete dimensions even when the leaders appear in reinforcement drawings.

## Current PC-1Q I-beams

Page 1 lower SECTION B-B reads top-to-soffit:

| Profile | Top edge | Upper haunch | Clear web | Lower haunch | Bottom edge | Sum (in) |
|---|---:|---:|---:|---:|---:|---:|
| I28 | 4 | 3 | 11 | 5 | 5 | 28 |
| I36 | 6 | 3 | 15 | 6 | 6 | 36 |
| I45 | 7 | 4.5 | 19 | 7.5 | 7 | 45 |
| I54 | 8 | 6 | 23 | 9 | 8 | 54 |

Horizontal haunch runs derive from half the flange-minus-web width. No unprinted junction fillets are introduced. Historical BDG 6.60.01, p125 explicitly shows Type I top edge 3.75 in and haunch 3.25 in; current PC-1Q shows 4 and 3 in. Its property table remains an independent historical cross-check and does not override the current dimensions.

## PC-2L 70-inch I-beam

Page 1 lower SECTION B-B chain: **6+2+1.5+49.5+3.5+7.5=70 in**. Upper short haunch rises 1.5 in over the printed **2 in horizontal run**. Its right station is (5,62) in, followed by the main slope to (15,64), replacing the old connection to (15,62).

Independent full-width stations (height, width), in: **(0,24.5),(0.75,26),(7.5,26),(11,6),(60.5,6),(62,10),(64,30),(70,30)**. Integrating these linear widths gives area **779.4375 in²**, centroid **34.85700826 in** above soffit, and centroidal Ix **514616.4583 in⁴**.

SECTION A-A prints a **16 in end web**; the elevation prints a **7 ft 6 in longitudinal web transition**. Exact end flange/haunch intersection elevations and the transition contour remain unresolved. They are stored under `partial_sections.end_face`, `implemented:false`. I70 still means the 6 in midspan web. No independent I70 property table was located in the reviewed BDG pages.

## PC-4J 1800 beam

Page 1 chain: **3+2+54.5+5.5+5.875=70.875 in**. The 3 in arrows run top-to-outer-edge underside; the 2 in arrows give the additional drop to the theoretical upper web-haunch datum. Reference intersections, in inches:

| Right-half reference | x | y above soffit |
|---|---:|---:|
| Bottom outside slope intersection | 17.75 | 5.875 |
| Lower web-haunch intersection | 2.9375 | 11.375 |
| Upper web-haunch intersection | 2.9375 | 65.875 |
| Top outside slope intersection | 23.625 | 67.875 |

Printed radii: **R7.875 in → 200.025 mm** at both web junctions; **R2 in → 50.8 mm** at the two outside slope corners. Actual tangencies differ from those theoretical intersections. The upper reinforcement SECTION A-A expressly leaders **3/4 in BEVEL(TYP)** to the bottom-soffit concrete corner; it must not become an R2 corner.

The implemented circular tangent arcs use **16 chords per arc**. Source radii and tangent construction are distinct from chord discretization, which is a numerical convention. The duplicate lower-web station was removed before assigning source-corner arc indices. The shared helper was unchanged.

## PC-5D bulb tees

Page 1 lower SECTION A-A/B-B lists 36, 42, 48, 54, 60, 66, 72 in depths. With two 6 in form blockouts, top flange is **49 in**, web **8 in**, bottom flange **40 in**. Upper vertical chain **5+3+3=11 in** has horizontal runs 17.5+3 in. Lower chain **5.5+7+2=14.5 in** has horizontal runs 14+2 in. Hence 2×(17.5+3)+8=49 and 2×(14+2)+8=40. The short haunches are straight bevels, not circular fillets.

Calculated clear web heights are **10.5,16.5,22.5,28.5,34.5,40.5,46.5 in**. All seven 49 in contours are fully source-dimensioned; each vertical chain closes to its depth.

Blockout removal gives the separately printed **61 in top flange**. The starred note below upper SECTION A-A references Bridge Design Guide 6.60.03B for reinforcement with blockout removal. The 5 in thickness arrows end at the 49 in boundary; no 61 in outside-edge thickness is directly labelled. Conditional continuation of the printed 3/17.5 slope gives 5−6×3/17.5=**139/35=3.971428571 in**; this is extrapolated rather than a published 4 in value. `partial_sections.61_in_flange` remains `implemented:false`.

## Independent verification and remaining limits

Tests integrate the twelve straight profiles as independent linear width functions, rather than reproducing their polygon construction. The 1800 test independently solves offset line equations and verifies source tangent stations, radii, 17 points on each circle and soffit bevels. All thirteen polygons must be valid, CCW, symmetric and have the right soffit/depth.

Published BDG values remain unchanged. The missing BT42 row was read directly on p127: **965 lb/ft, area 926.3 in², Ybot 21.1 in, Ixx 217461 in⁴**. Existing published-property tolerances were preserved. Residuals are stored separately from dimensions in package JSON:

| Family | Maximum absolute residual against reviewed BDG table |
|---|---|
| I28-I54 | 0.6216% across area, St, Sb, Ix |
| 1800 | area 0.9107%; St 0.7167%; Sb 0.0682%; Ix 0.3309% |
| BT36-BT72 | area 0.0413%; Ix 0.0404%; rounded Ybot within 0.0434 in |

Residuals are reported without changing source dimensions or loosening thresholds. Exact end I70, full 61 in bulb-tee, strand/deck-haunch/end-diaphragm geometry remains outside the implemented contour.

Target validation: `/home/ccaprani/anaconda3/envs/pybridge/bin/python -m pytest tests/test_us_state_r4_mi_mdot_standard.py tests/test_michigan_verified_dimensions.py -q`. Root owns later integration-wide validation.
