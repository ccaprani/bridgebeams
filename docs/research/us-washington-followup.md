# Washington State W-series prestressed concrete I-girders

Four gross WSDOT W-series section profiles are now represented: **W42G, W50G, W58G and W74G**. The coordinates are from WSDOT's archived *Bridge Design Manual M 23-50.01*, Appendix A, drawing 5.6-A1-1 (June 2006, PDF page 440). WSDOT's *Bridge Design Manual M 23-50.24*, Table 5.6.1-1 (June 2025, printed page 5-85; PDF page 95), provides an independent check of all four gross section properties. These are source-dated geometric outlines, not approval for a present-day bridge design.

The [archived outline PDF](https://wsdot.wa.gov/publications/manuals/fulltext/M23-50/M23-50.01Complete.pdf) is locally retained as `sources/expansion/europe-americas/us_wsdot_2006_complete.pdf` (SHA-256 `db8e991abdbaf8eb6ffe68e58c7a0110dabf0be08e0dd848728344f02f3676af`). The [2025 property-table PDF](https://www.wsdot.wa.gov/publications/manuals/fulltext/m23-50/chapter5.pdf) is locally retained as `sources/expansion/europe-americas/us_wsdot_chapter5_2025.pdf` (SHA-256 `6af4c603fd17fa738361ad3764d6ddcb2035457e0ed002e4da68c9ab84205da0`). Both local PDFs are reference copies ignored by Git. The exact source coordinates and printed properties are in `src/bridgebeams/us/data/wsdot_w_girders.json`.

All source dimensions are inches. The API multiplies outline coordinates by exactly 25.4 mm/in, with the origin at the middle of the soffit and positive `y` upward. Only gross concrete is modelled: no strands, deck, bearing recess, shear key, or end variation.

| Section | Depth / top / bottom width (in) | Published A / Yb / Ix / Iy | Calculated A / Yb / Ix / Iy | Evidence |
|---|---|---|---|---|
| W42G | 42 / 15 / 20 | 373.25 / 18.94 / 76,092 / 5,408 | 373.25 / 18.9427 / 76,091.58 / 5,407.82 | Drawing 5.6-A1-1; Table 5.6.1-1 |
| W50G | 50 / 20 / 25 | 525.5 / 22.81 / 164,958 / 13,363 | 525.5 / 22.8103 / 164,957.51 / 13,362.77 | Same |
| W58G | 58 / 25 / 25 | 603.5 / 28.00 / 264,609 / 17,065 | 603.5 / 28.0033 / 264,609.24 / 17,065.31 | Same |
| W74G | 73.5 / 43 / 25 | 746.7 / 38.08 / 546,110 / 34,759 | 746.6875 / 38.0771 / 546,110.45 / 34,759.38 | Same |

Areas are square inches, centroid heights are inches above soffit, and second moments are inches to the fourth power. Discrepancies fit the WSDOT table's printed precision; no dimensions were adjusted to match the table. The W42G lower flange has a 1 × 1 in chamfer, 5 in straight side and 2 in upward taper, while its upper flange has a 3½ in straight edge and 1½ in downward taper. W50G/W58G have 1 × 1 in lower chamfers, 6 in straight lower edges, 3 in lower tapers, 5 in straight upper edges and 2 in upper tapers. W74G's upper wing has an additional 2 × 2 in bevel between its web and long taper. These drawing leaders define the right-half vertices in the JSON; mirroring completes each polygon.

The inherited `us_wsdot_iwf` registry row previously listed W74G depth as **73.625 in**. Both the archived drawing and the 2025 table say **73.5 in**; the registry row has been corrected.

The current [WSDOT superstructure drawing portal](https://wsdot.wa.gov/engineering-standards/design-topics/superstructure-design-bridges-structures) also links the nine WF designations, deck girders and tub girders. Their outlines need separate geometry closure. The downloaded 2026 detail/overview sheets inspected here display **“PRELIMINARY PLAN NOT FOR CONSTRUCTION”**; a live portal link does not remove that status. Their available top-level widths and depths do not suffice to create exact polygon sections.

Verification: `python -m pytest tests/test_us_wsdot_w_girders.py -q` passed all six tests. They check the source-dimension vertices, WSDOT published A/Yb/Ix/Iy within printed rounding, polygon symmetry and validity, and a `sectionproperties` mesh build.
