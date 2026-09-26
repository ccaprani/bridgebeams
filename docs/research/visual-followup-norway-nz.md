# Norway and New Zealand: visual review follow-up

The review exported on 22 September 2026 closes the Norwegian outline blockers and the NZ shear-key readings. Fourteen additional gross profiles are implemented: all five NTB and five KTB sections, NZ650/900 inner units, and NZ587 inner/outer units. The original review answers are preserved in [the response record](data/visual-review-responses-2026-09-22.json); [the coordinate record](data/visual-followup-norway-nz.json) stores every implemented exterior and the precise remaining tasks.

## Norway: ten reconstructed gross profiles

`NoNtbKtbSection` implements V426 Figure 3.3.2(a–j), PDF/printed pages 37–46. NTB coordinates use the soffit centre as origin; KTB uses the nominal left soffit corner before chamfering.

- The bottom 15×15 mm chamfer is **Colin's inference by projecting dimension leaders**, not an explicitly printed dimension. It is the documented default in the reconstruction.
- The top recess is 30×30 mm. The bottom-flange recess is 40 mm high, 15 mm inward at its top and 20 mm inward at its bottom. The recess remains unfilled in the precast section.
- KTB1400's left edge goes from nominal (0, 0) to (-30, 1400). Its total top width 400 puts the right edge at 370; the right stem edge is 280. This distinction prevents an extra 30 mm being added to the top width.
- KTB1200/1000 have vertical left faces, as Colin observed. Direct inspection also confirms vertical left faces on KTB800/600, pages 44/46; their upper and lower widths are 280/770. No universal slope was imposed across the family.
- Reinforcement-cover dimensions are not concrete-outline coordinates. No deck, reinforcement or end-block detail is included.

These are gross reconstructed profiles with explicit inference provenance, not certified formwork drawings. The implementation's independent strip-integration tests check area, top widths, unfilled recesses, symmetry and the KTB1400 slope.

## NZ: explicit inner and outer units

The drawings were read directly; no further prose comparison is requested from Colin.

| Drawing / PDF page | Implemented | Key detail | Void detail |
|---|---|---|---|
| S2.01 / 29 | 650 inner | Upper transition starts 220 below top, at y430; 12×12 chamfer; key bottom y110. Derived 34 mm recess. | One centred octagon, 830 maximum/630 flat width, 380 height; top 140/bottom 130 cover. |
| S2.10 / 34 | 900 inner | Upper transition starts 470 below top, at y430; 12×12 chamfer; key bottom y110. Derived 34 mm recess. | One centred octagon, 830 maximum/630 flat width, 605 height; top 140/bottom 155 cover. |
| S3.01 / 40 | 587 inner | Upper transition starts 157 below top, at y430; 12×12 chamfer; key bottom y110. Printed 38 mm recess. | Two 368 mm circular voids, at x308/836,y294. |
| S3.01 / 40 | 587 outer | Same key on right only; exposed left side, 15×15 top corner. | One 368 mm circular void at x836,y294. |

For 650/900, the printed widths 1138/1094 give a 22 mm upper inset on each side. Adding the 12 mm upper key chamfer gives the 34 mm main recess. The enlarged lower-corner detail explicitly marks the mould-release face as **1:80**; this is a slope symbol, not an 80 mm vertical dimension. The gross implementation anchors the maximum 1138 mm width at the 110 mm ledge, follows the slope to the 20 mm chamfer elevation, and selects the 20×20 chamfer option. The void chain 154+100+630+100+154 closes exactly to 1138 mm.

For 587, the main recess is **38 mm, not 12 mm**. The 12 mm dimension is the transition chamfer. The resulting upper inner-unit width is 1092 mm:1144−2×(38−12). The 587 outline selects 15 mm corner chamfers; the circles use 256 vertices by default, with configurable resolution and an analytic area-error bound tested against exact circles. The allowed alternative hexagonal void is not silently substituted.

`NzHollowCoreSection(650)` and `(900)` return inner units. `NzHollowCoreSection(587, unit="outer")` returns the edge unit with the exposed edge on the left. The outer 587 gross profile excludes the optional drip groove explicitly. Local inspection/drain/connection holes are excluded throughout. RR364 says inner units must not be used singly in isolation.

## Remaining agent-side task: single-core outer-unit coordinate endpoints

The 650/900 outer drawings have been compared. Their flat void width is 430 mm rather than 630, giving 630 mm maximum void width; each void is eccentric toward the keyed face. Their overall upper widths are 1122 and 1123 mm respectively, while both lower widths are 1138 mm. The outer face and drip-groove geometry are shown.

The remaining issue is a precise dimension-reference reconciliation, not a missing description of inner versus outer:

- 650 outer: the chain 324+100+430+100+124 totals 1078 mm, 60 mm short of 1138.
- 900 outer: the chain 334+100+430+100+124 totals 1088 mm, 50 mm short of 1138.

The first chain endpoint is near the drip-groove side and the last is near the key face; these are not both overall-width endpoints. A PDF vector trace was attempted, but its drawn endpoint spacing is not precise enough to turn the partial chain into an exact coordinate placement. These two outer variants remain excluded from the API until the references are reconciled from CAD or source notes. Neither the supplied 12 mm readings nor the inner/outer distinction remains on the human visual-review queue.

## Verification

The targeted Norway/NZ test files pass 21 tests. They compare independent source-literal strip integrals, key-face locations, circular-hole analytic limits, hole counts, eccentricity and supported input combinations. Source SHA-256 values and the implemented coordinate chains are retained in the JSON record. No independent published section-property table was identified for these profiles.
