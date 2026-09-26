# Ontario MTO NU and box girders: extraction record (September 2026)

Scope: Ontario Ministry of Transportation (MTO) prestressed NU girders and box
girders. These are Ontario provincial standards, not a national Canadian
catalogue. Machine-readable companion:
[extraction-ontario-2026-09.json](data/extraction-ontario-2026-09.json).

## Sources

The June 2025 standard drawings are obtained from the
[MTO Structural Standard Drawings portal](https://www.library.mto.gov.on.ca/SydneyPLUS/TechPubs/Portal/tp/ssdViews.aspx)
on 23 September 2026. The portal has no per-drawing URLs. Each drawing is
downloaded by posting its row's ASP.NET download control. The hashes of the
retrieved SS107-16 and SS107-25 match the copies retrieved on 22 September,
which confirms the retrieval mapping. Local copies are in
`sources/expansion/europe-americas/` (gitignored, reference only).

| Drawing | Title (original) | Date | Local file | SHA-256 (first 16) |
|---|---|---|---|---|
| SS107-13 | Prestressed Box Girders and Bearings (B700, B800, B900) | June 2025 | ca_mto_ss107_13.pdf | f09855653c1fb35e |
| SS107-14 | Prestressed Box Girders and Bearings (B1000) | June 2025 | ca_mto_ss107_14.pdf | c603460caf713ce2 |
| SS107-15 | Prestressed Box Girder Details | June 2025 | ca_mto_ss107_15.pdf | f6492f2ec97940b5 |
| SS107-16 | Prestressed NU Girders and Bearings (NU 900) | June 2025 | ca_mto_ss107_16.pdf | cc45346cf2251d70 |
| SS107-17 … -23 | … (NU 1200, 1400, 1600, 1800, 1900, 2000, 2400) | June 2025 | ca_mto_ss107_17 … _23.pdf | see JSON |
| SS107-24 | Prestressed NU Girders - Details | June 2025 | ca_mto_ss107_24.pdf | 993c6e51c7fd9beb |
| (DRAFT) | Prestressed NU Girders and Bearings, 25 July 2023, pp1–8 | 2023 | ca_mto_nu.pdf | 190e5f3bff7c1e7d |
| (DRAFT) | Prestressed Concrete Girder Guidelines BRO-00X, August 2023 | 2023 | ca_mto_guide.pdf | 4cf5ad75d1b99f4d |

Each drawing is a single-page PDF, so every locator is PDF page 1. Guide
locators: Table 2 (NU) is on PDF p15, printed p7. Table 3 (boxes) is on
PDF p16, printed p8. The box text on p15 says the standard sizes run from
B700 to B1000 in 100 mm steps and gives two widths, 915 and 1220 mm.

## NU girders: transcription (mm)

Each sheet's TYPICAL SECTION was viewed at 400–500 dpi. All eight 2025
sheets and all eight 2023 DRAFT sheets carry the same callouts. Only the
web height differs.

| Callout | Value |
|---|---|
| Top width | 1235 |
| Top flange tip vertical edge | 65 |
| Top taper, to theoretical web-face intersection | 45 |
| Web width | 160 |
| Web height (printed) | 515 / 815 / 1015 / 1215 / 1415 / 1515 / 1615 / 2015 = D − 385 |
| Bottom taper, from web face | 140 |
| Bottom flange vertical edge | 135 |
| Bottom width | 985 |
| Web–flange fillets | R200 (TYP) |
| Flange-tip fillets | R50 (TYP) |
| Soffit corners | 20mm CHAMFER (TYP) |

Depths: NU900, NU1200, NU1400, NU1600, NU1800, NU1900, NU2000 and NU2400,
on SS107-16 to SS107-23 respectively. The SS107-24 Table 2 lists the same
eight depths.

### Conventions

- Each fillet is the unique circular arc tangent to the two dimensioned
  lines at the printed theoretical corner. The tangent lengths fit within
  every straight segment. For example, the 515 mm NU900 web holds
  143.3 + 184.0 mm of tangent length. The arcs are tessellated with 32
  chords by default. This gives an area error below 0.008% and an Ixx
  error below 0.007% against exact arcs.
- The 20 mm chamfer is taken as 20 × 20 mm at 45°.
- The top-flange upper corners are square, as drawn.
- The guide mentions a 185 mm web for post-tensioned use. It is not on a
  standard sheet and is not implemented.

Provenance: `transcribed-with-convention`. Status: `current SS107-xx (June 2025)`.
The 2023 DRAFT sheets are superseded. They were visually confirmed to have
identical callouts.

### Analytic properties (exact arcs; no published table exists)

| Size | A (mm²) | yb (mm) | Ixx (mm⁴) |
|---|---|---|---|
| NU900 | 427 110.5 | 410.441 | 4.6489e10 |
| NU1200 | 475 110.5 | 542.791 | 9.5586e10 |
| NU1400 | 507 110.5 | 632.880 | 1.3992e11 |
| NU1600 | 539 110.5 | 724.146 | 1.9432e11 |
| NU1800 | 571 110.5 | 816.391 | 2.5942e11 |
| NU1900 | 587 110.5 | 862.830 | 2.9619e11 |
| NU2000 | 603 110.5 | 909.459 | 3.3588e11 |
| NU2400 | 667 110.5 | 1097.589 | 5.2548e11 |

The area was checked two ways: by tessellation, and in closed form as the
straight-line polygon plus r²(cot(θ/2) − (π−θ)/2) per fillet. The two
agree to within 0.1 mm². No local source (Ontario, CPCI or other) gives
properties for this Ontario outline, so these are implementation checks
only. The US Nebraska NU metric property tables do not apply because the
outline is different.

## Box girders: transcription (mm)

Source: SS107-13/14, STRAND GRID ARRANGEMENT section 2 (midspan voided
section). Section 1 shows the solid end block and is excluded.

| Callout | Value |
|---|---|
| Width | 1220 (only width on the 2025 sheets) |
| H | 700 / 800 / 900 (SS107-13), 1000 (SS107-14) |
| Top and bottom slabs | 140 |
| Webs | 125 (TYP) |
| Void chamfers | 75 × 75 (TYP) |
| Outer corners | 20 CHAMFER (TYP), with the top pair optional per note 15. The bottom pair is "20mm CHAMFER (TYP)". |

The sides are plain and vertical, with no shear key. SS107-15 shows the
transverse connection: welded L102/L51 steel ties across a nominal 10 mm
gap. The void is filled with solid Styrofoam (note 16) and is modelled as
a hole.

### Conventions and estimates

- All four 20 mm outer chamfers are included because they are drawn.
  Omitting the optional top pair adds 400 mm².
- **915 mm width (estimate):** this width appears only in the DRAFT 2023
  guide, where Table 3 is labelled "915 / 1220". No held current drawing
  shows it. The best estimate reuses the 140/125/75/20 details of the 1220
  template, which gives a 665 mm void. Provenance: `estimate`.
- 1220 units: provenance `transcribed-with-convention` (45° chamfers).

SIZES are `B{700,800,900,1000}-{1220,915}`, eight profiles in total.

| Size | A (mm²) | yb (mm) | Ixx (mm⁴) |
|---|---|---|---|
| B700-1220 | 457 050 | 350 | 2.9177e10 |
| B800-1220 | 482 050 | 400 | 4.1189e10 |
| B900-1220 | 507 050 | 450 | 5.5610e10 |
| B1000-1220 | 532 050 | 500 | 7.2567e10 |
| B700-915 | 371 650 | 350 | 2.2342e10 |
| B800-915 | 396 650 | 400 | 3.1749e10 |
| B900-915 | 421 650 | 450 | 4.3139e10 |
| B1000-915 | 446 650 | 500 | 5.6637e10 |

## Remaining uncertainties

- None of the held sources publishes properties, so nothing is validated
  independently.
- 915 mm boxes: it is not known whether a current 915 drawing exists, or
  whether its web and slab details match the 1220 unit.
- Chamfer angle (45°) and fillet tangency are drafting conventions. The
  shapes drawn on the sheets are consistent with them.
- `docs/research/canada-followup.md` still says SS107-17 to SS107-23 are
  not downloaded and NU is not implemented. The integrator should update
  that note.
