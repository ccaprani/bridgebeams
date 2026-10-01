# NZTA RR364 verified dimensions and nominal geometry

The existing NZ sections now retain a checked source record for the 1500 mm
I-beam and the 650/900 mm single hollow-core inner units. The 900 mm unit's
lower mold-release slope is corrected from 1:80 to the printed 1.5:140.
The earlier 1600 mm I-beam and 587 mm double hollow-core profiles are
preserved without a new source verification claim.

The original source is *NZ Transport Agency Research Report 364, Standard
precast concrete bridge beams* (2008), local filename `nzta-rr364.pdf`,
SHA256 `ea199fa1dfa3272c8c31bbe8ee200c616536fae4a25418ae084d51841b01fd6d`.
The dimensions were checked on 30 September 2026 by inspecting full PDF
pages first, then enlarged source crops and their dimension endpoints.

The packaged record is
`bridgebeams/nz/data/nzta_rr364_verified_dimensions.json`, read through
`importlib.resources`. Each constructed rechecked section exposes
`source_record` and `geometry_conventions`; these identify the drawing,
labels, source alternatives and remaining evidence gaps. No source
section-property table has been verified. All dimensions are millimetres.

| Profile | One-based PDF page | Printed drawing | Checked labels |
|---|---:|---|---|
| I-beam 1500 | 45 | S4.01 | Top/web/bottom widths 375/175/475; vertical chain 100+75+1005+150+170=1500 |
| Single hollow-core 650 | 29 | S2.01 | Inner top/max widths 1094/1138; void 830 wide, 380 high; top/bottom covers 140/130 |
| Single hollow-core 900 | 34 | S2.10 | Inner top/max widths 1094/1138; void 830 wide, 605 high; top/bottom covers 140/155 |

## I-beam convention

`NzIBeamSection(1500)` preserves its earlier outline and coordinate origin
at mid-soffit. It selects the source's 20 x 20 mm bottom chamfer option.
The alternative is a 20 mm radius. Small curves drawn at web-haunch
junctions have no labeled radii and are represented by sharp nominal
intersections. These are explicit geometry choices, rather than a claim
to reproduce every manufacturing fillet.

Independent integration of that nominal chamfer polygon gives area
363100 mm2, centroid 676.0391994859084 mm above soffit and centroidal Ixx
88784866625.39398 mm4. These are calculated properties of the stated
convention; no comparison to published properties is asserted.

## Single hollow-core convention

`NzHollowCoreSection(650)` and `NzHollowCoreSection(900)` preserve the
earlier coordinate convention: x=0 at the left lower key-ledge extent,
y=0 at soffit. The chosen nominal section fixes the 1138 mm maximum width
at the lower key ledge 110 mm above soffit, and the 1094 mm width at the
top. Combining those widths with the 12 mm joint diagonal gives a
calculated 34 mm recess. The upper key transition is at y=430 for both
depths, from their printed 220/320/110 and 470/320/110 side chains.

The enlarged lower-face details specify rise:run of 80:1 for 650 and
140:1.5 for 900. The geometry applies these slopes inward from the lower
ledge to the selected 20 mm bottom chamfer. Assigning those draft
endpoints is an explicit nominal interpretation; exact manufactured
draft/chamfer datums remain unresolved. Width at soffit is consequently
smaller than 1138 mm. The rechecked correction changes only the 900 mm
lower drafted faces.

Both octagonal inner voids use the printed 100 x 100 mm corner
transitions and 630 mm horizontal straight lengths. Their horizontal
chain is 154+100+630+100+154=1138. The vertical chains are
140+100+180+100+130=650 and 140+100+405+100+155=900. Local inspection,
drainage and connection holes are excluded from the continuous gross
section. The source expressly prohibits use of an inner unit singly in
isolation.

## Outer-unit records remain partial

The 650/900 outer-unit labels are retained in the same packaged JSON with
`status="partial_dimensions"` and `implemented=false`. Constructing
either still raises `ValueError`. Their top widths are 1122/1123 mm,
their lower overall widths are 1138 mm and their void widths are 630 mm.

The source lower horizontal labels are 324+100+430+100+124 for 650 and
334+100+430+100+124 for 900. The 334 glyph was checked again at higher
resolution. These chains have different endpoints from the overall-width
dimension and sum to 1078/1088 mm. Exact external offsets and draft
datums require reconciliation; no missing segments or substituted values
are inferred. The optional drip groove also has trapezoidal, semicircular
and triangular alternatives. A complete exterior outline remains held
until those geometry choices and datums are resolved.
