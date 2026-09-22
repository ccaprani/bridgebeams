# Beam families

The Irish sections below are recovered from (or validated against) manufacturers'
published property tables, with the Banagher Precast Concrete *Bridge Beam
Manual* (3rd edition) as the principal Irish producer source. Where manufacturers
publish section properties and key widths but not internal profile
dimensions, the profile is a documented least-squares reconstruction, and
the tests enforce the deviation limits quoted below. Sources and URLs are
available in {doc}`research` and the local working registry `sources/SOURCES.md`.
See {doc}`global` for other implemented jurisdictions and their evidence limits.

## Ireland

### T beams (T1–T10) — solid slab construction

380–815 mm deep, 495 mm flange, 205 mm top. The published vertical stack
(chamfer 25 + flange side 75 + splay 40 + taper 50 + web H + taper 50 +
flange F) is exact, and the internal widths reproduce the published
properties to **< 0.02%**.

### TY / TYE beams — beam & slab (TY3–TY11) and solid slab (TY1–TY11)

400–900 mm deep, 750 mm bottom flange, published top width `Wf` per size
(nibbed top for beam & slab decks; full top flange for solid slab decks);
TYE edge beams have a full-height vertical face at `x = -375` and a
published centroid offset `Xc`. **Exact** (< 0.02%).

### Y beams (Y1–Y8) — beam & slab construction

700–1400 mm deep, 750 mm bottom flange, published top width `Wf`. The
manufacturers publish properties, `Wf` and strand layouts but not internal
dimensions, so the profile is a documented least-squares reconstruction:
**area 3.5%, centroid 2.1%, Ixx 4.8%** maximum deviation across all eight
sizes. `strand_locations()` provides the "all possible strand locations"
map.

### YE edge beams (YE1–YE8)

Asymmetric edge-beam companion to the Y: full-height vertical face on one
side; validated against published properties **including the centroid
offset `Xc`** to 0.8% rms.

### U beams (U600–U12) and SU edge beams (SU11–SU12)

600–1600 mm deep, 970 mm bottom flange; published `W1`/`W2`/`W3` per size.
Profile recovered exactly from the manual drawing: **≤ 0.3%** across all
thirteen sizes.

### M beams (M1–M10) and UMB edge beams (UMB1–UMB10)

640–1360 mm deep, 970 mm bottom flange, published web height `H`
(200/440/680 per size group); UMB is the U-shaped edge variant with edge
upstands. Validated to **≤ 0.7%**.

### SY / SYE beams (SY1–SY6, SYE1–SYE6) — long span

1500–2000 mm deep, 750 mm bottom flange. Validated to **< 0.6% rms**.

### Solid Box beams (SD1–SD8, width classes 1–4)

`IeSolidBoxBeamSection("SD4 (2)")` selects a 600 mm deep, 750 mm overall
width solid box. The 32 profiles span depths 300–1000 mm and widths
495/750/970/1500 mm. Classes (1)–(3) reproduce published properties within
documented rounding allowances. Class (4) uses the dimensioned nominal
outline: its published areas exceed geometry by 225/275 mm². Those source
discrepancies are recorded and tested separately; the shape is not fitted.

### W beams

`IeWBeamSection("W19")` selects the current 2300 mm profile. Sixteen
published sizes use the current manual's upper dimensions and the straight
lower contour recovered from a producer W19 DWG. The older project's upper
F/V dimensions are not substituted into the current range. Published areas
match within 4 mm² and Ixx within 0.0025%; W11's centroid rounding exception
is individually recorded. See {doc}`banagher-cad-followup`.

## United Kingdom

UK sources and profile coverage are separate from Irish producer families.
`bridgebeams.uk` currently exports no sections. Shared beam names and use
in UK projects do not transfer the source jurisdiction or establish
identical geometry. See the UK entry in {doc}`coverage`.

## Australia

### Super-T girders (T1–T5)

To AS5100.5 Appendix D Fig. D1(B), with pre-2001 and contemporary
subtypes and selectable web/flange thicknesses (VIC/NSW).

### I-girders (types 1–4)

To AS5100.5 Appendix D Fig. D1(A).

## Accuracy summary

### New Zealand and Qatar additions

`NzSuperTSection(1025)` and `NzSuperTSection(1225)` use the open-top
twin-web sections of NZTA RR364 S1.01/S1.11. The 1225 mm section has its
own lower geometry. `NzSuperTSection(1225, top_width=1990)` selects the
narrower S1.21 arrangement. The small formwork ledge is omitted from this
gross-profile approximation. This corrects earlier library geometry that
filled the open centre and misread upper haunches as bottom chamfers.

`NzIBeamSection(1500)` and `NzIBeamSection(1600)` transcribe RR364 S4.01
and S4.10, selecting the drawing's 20 mm chamfer option. Independent
analytic area checks validate the implementation; no published section
property table was located for these New Zealand profiles.

`QaQBeamSection("T1")` through `QaQBeamSection("T5")` implement Ashghal
SD 5-1-101 Rev 1 at the published 2150 mm top width. All five lower
profiles were read directly. Rounded and overdetermined source dimensions
do not close exactly; the documented reconstruction differs from the
published tables by at most **0.88% area, 0.85% centroid height and 1.26%
centroidal Ixx**. The nominal 125 mm web becomes approximately 122–123 mm
in this reconstruction. See {doc}`research-pdf-transcription` for the
source audit and explicit approximation choices.

### South Africa orientation correction

Civilcon PPBI places B1 at the soffit and B4 at the top. The previous
implementation reflected the section vertically and then compared the
complement of its centroid against the source. The corrected geometry uses
the drawn orientation: I1's centroid is about 318.221 mm above its 410 mm
wide soffit, with a 360 mm top flange. Area and centroidal inertia are
unchanged by reflection, but centroid height and top/bottom section moduli
are corrected. The source I18 top-modulus inconsistency is preserved and
tested separately. The full source audit is in {doc}`research-asia-africa`.

### Irish families

| Family | Area | Centroid | Ixx | Source of profile |
|---|---|---|---|---|
| IE T (T1–T10) | <0.01% | <0.02% | <0.02% | published drawing (exact) |
| IE TY/TYE | <0.01% | <0.02% | <0.02% | published drawing (exact) |
| IE U/SU | ≤0.05% | ≤0.05% | ≤0.3% | published drawing (exact) |
| IE SY | <0.05% | <0.05% | <0.05% | published drawing (fitted widths) |
| IE SYE | ≤1.2% | ≤1.2% | ≤1.2% | fitted (incl. published Xc) |
| IE MY | ≤2.2% | ≤2.2% | ≤2.2% | documented reconstruction |
| IE MYE | ≤0.6% | ≤0.6% | ≤0.6% | documented reconstruction (incl. Xc) |
| IE M | ≤0.7% | ≤0.7% | ≤0.7% | fitted web/block |
| IE UMB | ≤0.6% | ≤0.1% | ≤0.1% | published drawing (exact at UMB10) |
| IE Y | 3.5% | 2.1% | 4.8% | documented reconstruction |
| IE YE | 0.8% | 1.1% | 1.5% | documented reconstruction |

Suitable for preliminary design and assessment workflows; for detailed
design, confirm against the manufacturer's drawings/BIM.

### Sections added after visual review

`NoNtbKtbSection` supplies five NTB and five KTB profiles from Norway's V426.
The 15 mm bottom chamfers are a recorded reviewer inference. NTB uses a
mid-soffit origin; asymmetric KTB uses the nominal left soffit corner.

`NzHollowCoreSection(650)` and `(900)` supply inner units;
`NzHollowCoreSection(587, unit="inner"/"outer")` selects the two-void inner
or one-void outer unit. The 587 outer profile omits the optional drip groove.
The 650/900 outer void-location endpoints remain unresolved and are not
implemented. See {doc}`visual-followup-norway-nz`.

`CivilconYBeamSection("Y1"…"Y8")` includes the confirmed 40 × 50 mm ledges
and R100 web junction for the in-situ slab arrangement. Area differences
are below 0.037% and centroid differences below 0.476 mm. Y1's source
modulus discrepancy is retained separately; Y2–Y8 moduli agree within 0.1%.
See {doc}`visual-followup-za-ro-nepal`.
