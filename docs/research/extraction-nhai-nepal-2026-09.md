# Extraction record: NHAI I girders (India) and DoR precast RC I beams (Nepal)

Checked 2026-09-23. Structured record: [extraction-nhai-nepal-2026-09.json](data/extraction-nhai-nepal-2026-09.json).
Code: `bridgebeams.india.nhai_i_girders` (`Nh45aIGirderSection`, `DelhiVadodaraPscISection`) and
`bridgebeams.np.precast_rc_i` (`DorPrecastRcISection`). Package data:
`src/bridgebeams/india/data/nhai_i_girders.json` and `src/bridgebeams/np/data/dor_precast_rc_i.json`.

All dimensions below were read from rendered pages that were inspected visually. The NHAI
Package II sheets are CAD vector drawings. The Nepal and Delhi–Vadodara sheets are raster
scans.

## 1. NHAI NH 45-A Package II: seven midspan outlines

**Source:** [PKG II Modified Structural Drawings](https://nhai.gov.in/nhai/sites/default/files/2020/PKG_II_Modified_Structural_drawings.pdf),
prepared by Feedback Infra Pvt. Ltd. for NHAI. Local copy:
`sources/expansion/asia-africa/nhai-pkg-ii-modified-structural-drawings.pdf`, 68 pp, SHA-256
`7f21b6abd44f339680aa5f7d1d91cfad75edb3055f09d0f6cbd635765fa09227`.

**Status:** every drawing sheet is stamped **FINAL FEASIBILITY REPORT** and is at revision R0.
These are project proposal drawings for named structures. They are not a national standard, and
nothing in them shows that the girders were approved or built. `source_status` is
`"Final Feasibility Report"`.

**Coverage:** I surveyed all 68 pages through the text layer, and viewed the text-less pages
(20, 41, 51, 54, 56 and 59), which are divider sheets. Every "SECTION AT MID" girder view is
listed below. PDF p50 is already implemented as `Nh45aPscISection`.

Every outline has the same five-segment vertical chain, measured from the top: flange edge 150,
splay 100, clear web, splay 150, flange 250. Units are mm. "Label" is the construction label
printed on the drawing.

| SIZES key | Label | Depth | Top / web / base | Clear web | Splay horizontals (printed) | PDF pages; drawing no. (FIPL-HD-TPT-117-V-N-45A-…) | Gross A (mm²) | cy (mm) | Ixx (mm⁴) |
|---|---|---|---|---|---|---|---|---|---|
| PSC-1500 | PSC-I girder | 1500 | 900/300/750 | 850 | 300 / 225 | p61 FLY-CH-51+475-GA-01; p66 FLY-TYP-GA-01; p68 FLY-TYP-GA-02 (all three identical) | 716 250 | 739.18 | 1.8652e11 |
| PSC-2000 | PSC-I girder | 2000 | 900/300/750 | 1350 | 300 / 225 | p52 MNB CUM VUP-CH-43+835-GA-01; p63 FLY-CH-61+015-GA-01 (1st detail) | 866 250 | 983.48 | 4.0026e11 |
| RCC-1300 | RCC-I girder | 1300 | 800/300/600 | 650 | 250 / 150 | p63 FLY-CH-61+015-GA-01 (2nd detail) | 587 500 | 662.84 | 1.0907e11 |
| RCC-1400 | precast RCC I girder | 1400 | 800/300/600 | 750 † | 250 / 150 | p22 MNB-CH-33+284-GA-01 (2×16 m) | 617 500 | 712.42 | 1.3345e11 |
| RCC-1500 | precast RCC I girder | 1500 | 800/300/600 | 850 † | 250 / 150 | p28 MNB-CH-40+484; p30 MNB-CH-41+043 (1×21 m); p47 MJB-CH-47+471 (13×20 m) | 647 500 | 762.03 | 1.6091e11 |
| RCC-2000 | precast RCC I girder | 2000 | 900/300/750 | 1350 | 300 / 225 | p26 MNB-CH-40+161-GA-01 (1×30 m) | 866 250 | 983.48 | 4.0026e11 |
| RCC-2250 | precast RCC I girder | 2250 | 900 ‡/300/750 | 1600 | 300 / 225 | p44 MJB-CH-38+514-GA-01 (2×36 m) | 941 250 | 1106.31 | 5.4655e11 |

† The clear web height is not printed separately. It is derived by closing the printed chain to
the overall depth.

‡ In the p44 render, the overall 900 callout falls above the view. The chain 300 | 300 | 300 is
printed.

**Identities:** each identical outline is still exposed as its own SIZES entry, and the identity
is recorded in `identical_to`.
- PSC-2000 and RCC-2000 have the same outline.
- RCC-2250 has the same outline as `Nh45aPscISection` CH50+473-MID (p50, PSC).
- PSC-1500 and RCC-1500 are **different** outlines: the flange widths are 900/750 and 800/600.

**Construction:** PSC means prestressed. RCC means precast reinforced concrete and is **not
prestressed**. Each instance carries `construction` and `prestressed`.

**Excluded:** end sections (rectangular webs with 75/100/40/25 mm offsets), the deck slab,
strands and reinforcement.

**Validation:** there are no published properties. The tests check that the polygon areas match
independent rectangle-plus-trapezoid sums, that the chains close, and that the splay widths
equal (flange − web)/2.

## 2. Delhi–Vadodara Expressway package II, Volume III: 30 m PSC I at km 37+744

**Source:** [pkg2-VOL-III.pdf](https://nhai.gov.in/nhai/sites/default/files/Agreements_document/pkg2-VOL-III.pdf).
Local copy: `sources/expansion/india-followup/nhai-project.pdf`, SHA-256
`828db4e970519efa152ae40f8326f235d7fccfea775869d8e81ce68fb2a9cc0f`.

**Pages checked:**
- p39: divider sheet, "PSC I-BEAM (SIZE 1x30.0M) AT KM 37+744".
- p40: general arrangement plan only. Note 9 says all dimensions are tentative and may change
  after detailed design.
- p41 (hand-stamped page 40): "CROSS SECTION OF PRECAST PSC GIRDER", at support and at mid span,
  scale 1:50.
- p42: divider for a different structure, an RCC T-beam (1×18 m) at km 38+860. It is not in
  scope.

The title-block date reads "AUGUST 201x". The last digit and the drawing number are illegible.

**Midspan readings:**

| Item | Reading |
|---|---|
| Top width | 1100 |
| Base width | 750 |
| Overall depth | 2000 |
| Vertical chain | 150 / 100 / 1350 / 150 / 250. It closes to 2000. |
| Elevation label "2225" | Girder plus the 225 mm deck slab (Detail A). |
| Web width | Illegible. The only embedded image is a 1189×840 1-bit JBIG2 scan. |

**Web width estimate:** I scaled it from line centres on the native pixels. At 1:50 one native
pixel is about 26 mm.
- The 1100 top width spans 42 px, which gives 26.2 mm/px.
- The web spans 11 px, which gives **288 ± 26 mm**.
- As a scale check, the half-base measures 760 mm (printed 750) and the depth measures about
  2000 mm.

I adopted **300 mm**. It is the nearest round value inside the measurement band, and it matches
the 300 mm web of every NH 45-A girder. The whole profile has `provenance = "estimate"`.

**Result:** A = 906 250 mm², cy = 1023.84 mm, Ixx = 4.3238e11 mm⁴. Each ±26 mm of web width
changes A by ±37 050 mm² (±4 %). The support section (1100 top over a rectangular 750 stem) is
not implemented.

## 3. Nepal DoR precast RC I beams 1300 / 1700 (`np`)

**Sources:** Department of Roads (Bridge Branch), *Standard Superstructure Drawing for Road
Bridges*, "RC Deck with Precast RC Beams", dated 14 July 2015. Drawing 5/10 (PDF p7) is the
general arrangement. Drawing 7/10 (PDF p9) is the outer-beam reinforcement sheet containing
Detail 'Y'. I also viewed drawing 6/10 (PDF p8), the deck and cross-girder reinforcement. It
adds no beam-outline dimensions.

| Size | Span | Local file | SHA-256 |
|---|---|---|---|
| 1300 | 20 m | `nepal-precast20.pdf` | `16fb2632…376f` |
| 1700 | 25 m | `nepal-precast25.pdf` | `d7b9eeed…5ba4` |

The URLs are in the JSON; they are taken from `asia-africa-sources.json`. The beams are
**reinforced, not prestressed**.

**Midspan outline (mm):**

| Item | 1300 | 1700 |
|---|---|---|
| Top / bottom width | 700 | 700 |
| Web | 325 | 325 |
| Chain (flange edge / splay / clear web / splay / flange) | 150 / 65 / 685 / 150 / 250 | 150 / 65 / 1085 / 150 / 250 |
| Splay horizontal | 187.5 | 187.5 |

The 187.5 splay horizontal is printed as "187⁵" in Detail 'Y' on p9 of both volumes. The
midspan view on p7 is cut through an intermediate stiffener. Its 700-wide rectangle is the
stiffener, and the I inside it is the beam.

**Chamfer convention (best estimate):** Note 4 reads "Chamfer 12mm×12mm shall be provided at
all junctions of the formwork unless otherwise specified in the drawings." No chamfer is drawn
on any section.
- **Adopted:** 12 mm legs along both faces at the **six salient corners formed by two formwork
  faces**: 2 soffit corners, 2 bottom-flange shoulders and 2 top-flange underside corners.
- **Left sharp:** the top edges, because the top is a free casting surface that is wire-brushed
  per Note 8, and the four re-entrant web/splay junctions.
- **Area removed:** 2 × (72.0 + 56.2 + 68.0) = **392.5 mm²**. This is 0.064 % of the 1300
  section and 0.053 % of the 1700 section. cy moves by 0.1 mm and Ixx by −0.1 %.
- **Alternatives:** also chamfering the top edges would remove 536.5 mm² in total. Filling the
  re-entrant junctions would add 248.5 mm². Every alternative is under 600 mm², or under 0.1 %.
- `chamfer=False` returns the sharp nominal outline with `provenance = "transcribed"`.
  Otherwise provenance is `"transcribed-with-convention"`.

**Results:**

| Size | Chamfered A (mm²) | cy (mm) | Ixx (mm⁴) | Sharp A (mm²) |
|---|---|---|---|---|
| 1300 | 612 420.0 | 616.00 | 1.0999e11 | 612 812.5 |
| 1700 | 742 420.0 | 807.59 | 2.2932e11 | 742 812.5 |

**Consistency only (not a section check):** the sheets give a beam mass of 37 t (20 m) and 55 t
(25 m), and 44 / 66 m³ of M35 concrete per span in the precast beams. Assuming three beams per
span, that implies about 2.5 t/m³. The beam length, end blocks and stiffeners are not
separately quantified, so this cannot validate the midspan area.

## Remaining uncertainties

- The Delhi–Vadodara web width stays an estimate until a clearer copy of the drawing is found.
  The printed label is a 2–3 character blob.
- Nepal chamfer scope is a convention. Its effect on the properties is negligible.
- None of these sources publishes section properties. All checks are analytic.
- NHAI Package II girders are feasibility proposals. There is no evidence that they were built.
