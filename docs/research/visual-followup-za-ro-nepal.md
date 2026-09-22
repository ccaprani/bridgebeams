# Visual review follow-up: South Africa, Romania and Nepal

Recorded 2026-09-22 from Colin Caprani's **BRIDGEBEAMS VISUAL REVIEW v3**, exported at `2026-09-22T11:24:10.339Z`. These are identified human readings, followed by checks against the retained source PDFs. They do not silently replace producer values. Structured results are in [the companion JSON](data/visual-followup-za-ro-nepal.json).

## Civilcon Y: eight outlines implemented

The confirmed notches are **40 mm wide and 50 mm deep on each side**. The raised central top face between them is:

| Mark | Depth (mm) | Width between notches (mm) | Width across both ledges (mm) |
|---|---:|---:|---:|
| Y1 | 700 | 198 | 278 |
| Y2 | 800 | 227 | 307 |
| Y3 | 900 | 256 | 336 |
| Y4 | 1000 | 285 | 365 |
| Y5 | 1100 | 313 | 393 |
| Y6 | 1200 | 342 | 422 |
| Y7 | 1300 | 371 | 451 |
| Y8 | 1400 | 400 | 480 |

The [producer PPBY sheet](https://civilcon-za.co.za/wp-content/uploads/2017/05/PPBY.pdf), page 1, establishes the remaining outline: maximum base width 750 mm; 25 × 25 mm bottom chamfers; a 5 mm inset over the next 177 mm of height; a 177 mm lower splay; theoretical web junction width 200 mm; and a tangent radius of 100 mm. The theoretical right-side junction is therefore `(100, 379)` relative to the soffit centre, where `379 = 25 + 177 + 177`. This junction is replaced by the circular fillet; it is not a vertex on the concrete boundary.

`CivilconYBeamSection` implements this **40 mm in-situ slab arrangement**, with a 64-segment approximation of the radius. It does not model the separate 70 mm topdeck detail. The earlier broad question about decoding every top width is closed.

Using the rounded, dimensioned widths without fitting any parameters, all eight calculated areas agree with the published values within **0.037%**, and centroids within **0.476 mm**. Y2–Y8 top and bottom section moduli agree within **0.1%**. **Y1 retains a source-property discrepancy:** calculated top modulus is 0.33978% above the table, and bottom modulus 0.16862% above. This is recorded separately, not attributed automatically to rounding or removed by fitting the geometry. Targeted tests cover the dimensioned boundaries, all eight property comparisons, and invalid names: **9 passed**.

## Civilcon M: remove the visual task; retain the hypothesis

Colin's reading is that these are probably standard UK M beams and that the notch is approximately 40 × 50 mm. The [PPBM source](https://civilcon-za.co.za/wp-content/uploads/2017/05/PPBM.pdf) does not dimension that notch, so neither the size nor equivalence to a particular UK manufacturer is promoted to a verified source fact. No Civilcon-to-UK alias has been added.

The existing M4 printed area `37860 mm²` and M10 printed depth `360 mm` remain verbatim; the drawing explicitly labels M10 as 1360 mm. The appropriate next step is a dimensioned manufacturer/CAD comparison of the whole profile. Re-reading the same sheet cannot establish the missing notch dimension, so the old visual task is closed as **insufficient source detail**.

## Romania ASA: both lower-width readings resolved

In the [ASA CONS catalogue](https://asacons.ro/wp-content/uploads/2025/09/ASA-CONSOLIS-catalog.pdf), printed/PDF page 97, the 42 and 52 cm families share the lower horizontal chain:

`10 + 25 + 530 + 25 + 10 = 600 mm`.

The 530 mm is the flat soffit between the chamfers. Moving outward from the centreline on either side gives horizontal coordinates **265 mm at the soffit chamfer endpoint, 290 mm at the other chamfer endpoint, and 300 mm at the maximum outer flange face**. The final 10 mm is the side-face offset, not a second 10 mm bottom chamfer. Thus “600 mm bottom flange width” means maximum flange width; it does not mean a 600 mm flat soffit.

For the 72 and 80 cm families on printed/PDF page 99, the corresponding chain is:

`10 + 25 + 850 + 25 + 10 = 920 mm`.

The corresponding half-width coordinates are **425, 450 and 460 mm**, and the flat soffit is 850 mm. The dimensioned section gives 920 mm maximum flange width. The adjacent strand-position drawing for the 72 cm family prints **90 cm**, which conflicts with the 92 cm dimensioned section and the confirmed chain. Both printed values are retained; geometry should follow the dimensioned section, while the inconsistency remains visible. No new visual reading is requested for the already resolved `1` and `2.5` numerals.

The remaining readable dimensions have now also been transcribed:

| Mark | Depth | Top width | Web/waist width | Vertical dimension chain, from soffit (mm) | Radius callout |
|---|---:|---:|---|---|---|
| 42 | 420 | 220 | 140 callout | 25 + 75 + 70 + 200 + 50 | `5`, leader to curve; interpreted as 50 mm |
| 52 | 520 | 220 | Not separately printed | 25 + 75 + 70 + 200 + 150 | `5`, leader to curve; interpreted as 50 mm |
| 72 | 720 | 1020 | 270 | 25 + 85 + 80 + 50 + 270 + 48 + 82 + 80 | R = 50 mm |
| 80 | 800 | 1020 | 270 | 25 + 85 + 80 + 50 + 350 + 48 + 82 + 80 | R = 50 mm |

Both deeper profiles give the top horizontal chain `335 + 40 + 270 + 40 + 335 = 1020 mm`. The source notation `8` with superscript `5` is **8.5 cm**, while `8` with superscript `2` is **8.2 cm**; treating these as 8 cm leaves a false depth discrepancy. All four vertical chains close to their stated depths.

**The remaining limitation is exact arc construction, not unreadable text.** For the upper fillets of 72/80, treating the 40 mm horizontal and 48 mm vertical transition leaders as exact tangent endpoints gives `R = (40² + 48²)/(2 × 40) = 48.8 mm`, whereas the source prints R50. Conversely, R50 and a 40 mm horizontal transition require a 48.990 mm vertical rise. The adjacent sloping-flange tangent introduces another consistency condition. These rounded nominal dimensions cannot all be imposed as exact circular geometry. The PDF's outline uses illustrative cubic Bézier curves and does not supply a production CAD arc.

For 42, the 140 mm throat callout does not clearly separate minimum/tangent width from the theoretical intersection of the adjoining straight faces; for 52 that width is not separately printed. Copying it from 42 or selecting a nominal circular construction is an additional modelling convention. No ASA constructor has been added by silently choosing those conventions. The complete readable transcriptions are preserved in the companion JSON. A dimensioned CAD outline or an explicitly documented nominal reconstruction would resolve this; asking for the small numerals again would not.

## Nepal: correct the presentation and withdraw the chamfer question

The old question did not make its evidence easy to identify. Re-inspection of both retained **PDF page 7, drawing 5/10** sheets finds the labelled **SECTION OF PRECAST BEAM AT MID SPAN (TYP.)**: right centre on the 20 m sheet, and near the bottom left on the 25 m sheet. Focused renders have been saved locally as:

- `sources/expansion/asia-africa/nepal-precast20-p7-midspan.png`
- `sources/expansion/asia-africa/nepal-precast25-p7-midspan.png`

The 20 m depth stack is `150 + 65 + 685 + 150 + 250 = 1300 mm`; the 25 m stack substitutes 1085 mm for the clear web, giving 1700 mm overall. Both sections dimension 700 mm flange width and 325 mm web width. The rectangular intermediate-stiffener overlay complicates the small full-page view. The source index is the [Nepal Department of Roads standard superstructures library](https://dor.gov.np/index.php/home/publication/standard-superstructures-for-road-bridges).

Note 4 specifies 12 × 12 mm chamfers at formwork junctions, but these small section views do not individually resolve the corner applications. The earlier request to determine that scope from the supplied sheets is **withdrawn**. The retained section dimensions are supported; an exact chamfered outline remains unimplemented. Resolving that requires an explicit detail or an explicitly labelled modelling assumption, rather than another broad visual-review request.
