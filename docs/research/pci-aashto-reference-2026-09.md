# PCI reference for classic AASHTO I-beams

The [PCI Bridge Design Manual Appendix B-7/B-8 PDF](https://ems-www.pci.org/PCI_Docs/Design_Resources/Transportation_Resources/AASHTO%20I%20Beams.pdf), dated November 2011, gives a dimensioned sketch, a full `D1–D6`/`B1–B6` table and section properties for Types I–VI. It is the baseline for `bridgebeams.us.AashtoIBeamSection("IV")` and the other five type choices. Local PDF: `sources/expansion/europe-americas/pci-aashto-i-beams-2011.pdf`; SHA-256 `b8b5d6955224e0cf3e7f5ad2287378be8ca668aa948b6a0351002489abfe9bec`. The [structured source record](data/deep-search-us-aashto-2026-09.json) is searchable on the map.

The source dimensions are in inches; the library converts each ordinate by exactly 25.4 mm/in and uses the soffit as `y=0`. Types I–IV use one upper splay; Types V–VI have the extra `D3`/`B5` transition. The gross polygons omit strands, deck and end details. Independent polygon properties reproduce PCI's rounded area, soffit-to-centroid distance and centroidal `Ixx` for all six; the largest area difference is 0.5 in² (Type III), largest centroid difference is less than 0.005 in, and largest Ixx difference is less than 25 in⁴.

| Type | Depth (in) | Top / bottom widths (in) | Published A (in²) | Published yb (in) | Published Ixx (in⁴) |
|---|---:|---:|---:|---:|---:|
| I | 28 | 12 / 16 | 276 | 12.59 | 22,750 |
| II | 36 | 12 / 18 | 369 | 15.83 | 50,980 |
| III | 45 | 16 / 22 | 560 | 20.27 | 125,390 |
| IV | 54 | 20 / 26 | 789 | 24.73 | 260,730 |
| V | 63 | 42 / 28 | 1,013 | 31.96 | 521,180 |
| VI | 72 | 42 / 28 | 1,085 | 36.38 | 733,320 |

These are dated standard-product reference geometries. The [FHWA history of prestressed bridge girders](https://www.fhwa.dot.gov/publications/research/infrastructure/structures/05058/01.cfm) explains that AASHTO/PCI I-beams were standardized in the late 1950s/1960s and states subsequently developed their own sections. A matching type name on a Pakistani, Philippine or Latin-American drawing is a **lead**, not proof of an unmodified profile. Compare all twelve dimension entries and the area/centroid/inertia after unit conversion; assign the same profile ID to another jurisdiction only when the drawing supports that equivalence. Otherwise preserve a separate local variant.
