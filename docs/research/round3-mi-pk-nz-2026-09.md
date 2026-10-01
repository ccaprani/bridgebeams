# Round 3: Michigan, Punjab (Pakistan) and NZ manual sources (2026-09)

The owner downloaded these sources manually; no web search was done. Status: 20
Michigan profiles implemented in `us/state_r3_mi_beams.py`. They are 7 spread boxes
(`transcribed`), 10 side-by-side boxes (`transcribed-with-convention`: the key offsets
are estimates) and 3 bulb tees (`transcribed`, checked against printed weights). Nothing
could be implemented from the Pakistan or NZ files. The disclaimer applies: this data is
useful, not authoritative. Machine-readable record:
`docs/research/data/round3-mi-pk-nz-2026-09.json`.

## Sources

| Source | Local path | SHA-256 | Outcome |
|---|---|---|---|
| MDOT Bridge Week 2026, "Michigan Bridge Design Standards and Guides" (60 slides), URL not recorded | sources/expansion/round2/manual/us/mi/02.01_Cavalieri_DesignStandards.pdf | 762dc9ba2ce523968d6a9ab6a84e3d71472e13ce186796c3fb7643e2d21191c1 | No sections. Slide 8: BDG 8.43.01 sole-plate lengths only (MI 1800 2'-11 3/8", Bulb Tee 3'-4") |
| MDOT Final Report OR15-182 (2018), App. K Recommended Bridge Design Guide (52 pp), URL not recorded | sources/expansion/round2/manual/us/mi/dot_36033_DS2.pdf | 880dbc34ce940bdd0357f12c9bbb7410edd6015bc27f7888dd691021db67c533 | **20 profiles implemented** |
| Punjab C&W Dept, Standard Specifications for Road & Bridge Construction 2022 (512 pp) | sources/expansion/round2/manual/pk/Specification of Road & Bridge 2022 C&W.pdf | 30f556d7b39c28b56e6ea0791e3b0322610a38165192c2670587b4f72b453e62 | Text-only spec; no girder sections |
| MoW X261/0/112/17/6004 sheet 1, standard steel truss deck systems | sources/expansion/round2/manual/nz/X261-0-112-17-6004-1R0.pdf | d7c5c72941fad9efe567b2b5a0c4e42b9115285b5fe93d729e6de4bab2eb11e8 | Stahlton plank not dimensioned |
| MoW X275/0/112/18/7004 sheet 19, launching anchor beam | sources/expansion/round2/manual/nz/X275-0-112-18-7004-19R0.pdf | 05ea24c501ecf6176c3aff9816d629c71a42d9c86913312fefcc4c406e34aa5a | Steel erection gear; not relevant |
| Reynolds et al., "NZ Transport Agency Highway Structures Design Guide" (paper, 10 pp) | sources/expansion/round2/manual/nz/NZ-Transport-Agency-Highway-Structures-Design-Guide.pdf | 0f8290bc759d7100d49354209e23417b12e2e80ca71feb17a382c68fbb324b51 | No beam references |

## Michigan: OR15-182 Appendix K (`us/state_r3_mi_beams.py`)

The report says: "These plans are not meant to prescribe MDOT standards or
requirements, but represent recommendations for design" (PDF p2). For that reason,
`source_status` does not claim these are MDOT standard beams. The sheets are dated
05/09/18 and marked NO SCALE. Every dimension was read from 400 dpi renders.

### Spread box, SBB 003 (PDF p35): 7 profiles, `transcribed`

| Size (in) | Top slab | Bottom slab | Web | Void chamfer | Calc. A (in²) |
|---|---|---|---|---|---|
| 17x36 | 5 | 5 | 5 | 1 1/2 | 434.25 |
| 21x36 | 5 | 5 | 5 | 1 1/2 | 474.25 |
| 21x48 | 6 | 6 | 4 | 1 1/2 | 652.25 |
| 27x48 | 6 | 6 | 4 | 3 | 713.75 |
| 33x48 | 6 | 6 | 4 | 3 | 761.75 |
| 39x48 | 6 | 6 | 4 | 3 | 809.75 |
| 48x48 | 6 | 6 | 4 | 3 | 881.75 |

All sizes have a 1/2" BEVEL (TYP) at the soffit corners and square top corners.

### Side-by-side box, SSBB 003 (PDF p39) and SSBB 004 (PDF p40): 10 profiles

- Sizes are 17x36, 21x48, 27x48, 33x48 and 39x48. There is no 48x48 side-by-side
  section. Each size has an interior version (`-INT`) and a fascia version (`-FAS`).
- Slabs, webs and void chamfers are the same as the spread box of the same size.
- Fascia beams have a 9" top slab, because the void is lowered for the barrier EL04
  bars. They have a key on one side only ("OMIT SHEAR KEY" on the exterior face). In
  the module the key is on the -x side, as drawn.
- The **17x36 fascia is drawn with no void.** A pixel scan confirmed that the section
  has only its top and bottom outline lines. It is implemented as a solid section.
- **Shear key:** only two values are printed: the 3" top zone and the 4" key height.
  The horizontal offsets are not dimensioned, and the sheet is not drawn to scale (the
  36" overall width is drawn about 1.6 times too wide against the 5" web callout).
  The offsets were measured against the local callouts on the 17x36 and 27x48
  interior sections:
  - top setback: 0.38–0.39 in
  - recess: 0.78–0.81 in
  - transitions: about 45°

  **Estimate used:** 3/8 in setback and 3/4 in recess, with a 3/8 × 3/8 upper
  transition and a 3/4 × 3/4 lower slope. Provenance is therefore
  `transcribed-with-convention`. The estimated key removes about 4.3 in² per keyed side, which is 1–2% of the gross area.
  For comparison, MoDOT's printed key is 5/8 in / 1 1/4 in with the same proportions.

### Bulb tee, BTB 002 (PDF p43): 3 profiles, `transcribed`

**Top flange:**
- 4'-1" wide.
- The right-hand chain is a 5" edge. The left-hand chain is 5" + 3" + 3", giving an
  11" top zone.
- Horizontally: 1'-5 1/2" from the edge to the fillet start, plus a 3" fillet run.
- The half-width closes exactly onto the 8" web: 24.5 − 17.5 − 3 = 4.

**Bottom flange:**
- 3'-4" wide, with a 3/4" BEVEL (TYP).
- Vertical chain: 5 1/2" + 7" + 2" = 1'-2 1/2".
- Horizontally: a 1'-2" taper run plus a 2" fillet run, closing onto the web:
  20 − 14 − 2 = 4.

**Depths:** 3'-0", 3'-6" and 4'-0" (BT36/42/48).

**Validation.** The BEAM DIMENSIONS row "APPROX WEIGHT (TONS)" equals gross area × T ×
150 pcf, where T is the 70'-0" to 110'-0" row:

| Span | Depth | Printed (tons) | Calc. (tons) | Residual |
|---|---|---|---|---|
| 70 | 36 | 32 | 32.008 | +0.03% |
| 80 | 36 | 36.6 | 36.581 | −0.05% |
| 90 | 42 | 43.4 | 43.403 | +0.01% |
| 100 | 48 | 50.8 | 50.726 | −0.15% |
| 110 | 48 | 55.8 | 55.799 | −0.00% |

This independently confirms the full outline, including the web height for each
depth. The calculated areas are 877.94, 925.94 and 973.94 in². The Michigan bulb tee is
distinct from the WSDOT WF (6 1/8" web, 38 3/8" bottom flange), PCI BT and PCI NEBT.
The Brice et al. (2021) appendix has no Michigan table.

### Existing classes checked

There were no Michigan classes before this round. The MoDOT boxes
(`state_mo_slabs_boxes`) use the same nominal 17–42 in depth series but have a
different key and are a different agency's product. They were not reused.

## Pakistan: Punjab C&W 2022 specification

This is a text-only construction specification. A pdftotext grep found:

- "girder": 52 hits, covering placement, curing, formwork and erection clauses
- "precast": 48 hits, covering members, piles, posts and paving blocks
- "prestressed": 14 hits
- "AASHTO": 350 hits, all test or material standards
- "Type I/II/III": cement types only
- "I-girder", "box beam", "Type IV": 0 hits

There are only two large raster images: the cover (p3) and a bituminous paving form
(p245). No section is specified or dimensioned, so nothing was implemented. The existing
`pk` NHA Types A–H are unaffected.

## New Zealand

- **X261 (1-bit scan, 299 dpi), alternative 2 "Stahlton longspan deck, transoms 4 m
  crs":**
  - The drawing gives pairs of 230 mm deep Stahlton planks at 963 mm centres, 25 mm
    timber permanent formwork, a 125 mm deck, 762×267×173 UB transoms and a
    150×90×12 L seating.
  - The plank is drawn only as a schematic trapezoid, with no width, web or flange
    dimensions.
  - It was not implemented. The known values (230 mm depth, 963 mm pair spacing) are
    recorded in the JSON.
- **X275:** a steel launching anchor beam. Not relevant.
- **HSDG conference paper:** no standard beam content.

## Leads (not implemented)

- MDOT MI 1800 girder (BDG 6.60.03 / PC-4 special detail). The deck gives only a
  2'-11 3/8" sole plate.
- MDOT standard box beams (BDG 6.65 / PC-5 series). These may differ from the
  OR15-182 local-agency sheets.
- Stahlton Longspan plank product data (NZ).
