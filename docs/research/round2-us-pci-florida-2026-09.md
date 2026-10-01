# Round 2: US national PCI families and Florida DOT (September 2026)

Scope: the United States national PCI standard product families that are not
already implemented, plus Florida DOT precast girders. PCI AASHTO I–VI, the
WSDOT families and the MnDOT rectangular beams were already implemented and
are not duplicated here. Machine-readable record:
[round2-us-pci-florida-2026-09.json](data/round2-us-pci-florida-2026-09.json).

**Result: 130 profiles in 13 classes.** 24 are `transcribed` and 106 are
`transcribed-with-convention`. None is `fitted-reconstruction` or `estimate`.
Every class reproduces the property table it was checked against. The one
exception is the PCI heavy double tees, where the residuals are pinned (see
below). Per-size residuals are stored in each family's JSON under
`residuals_vs_published`.

## Sources retrieved (saved under `sources/expansion/round2/us/`, not committed)

| Local file | URL | Content used |
|---|---|---|
| `pci-bdm-2011-appendix-bc.pdf` (SHA-256 `e9e2d6a1…a52c`) | https://www.pci.org/PCI_Docs/GCPCI_Docs/Transportation_Resources/2011PCIBridgeManual-Appendix_BC.pdf | The full public Appendix B (B-1 to B-18) and Appendix C (C-1 to C-24) of *PCI Bridge Design Manual*, 3rd ed., November 2011 (MNL-133-11, ePub-compressed) |
| `pci-slab-shapes.pdf`, `pci-box-shapes.pdf`, `pci-aashto-pci-bulb-tees.pdf`, `pci-deck-bulb-tees.pdf`, `pci-next-beams.pdf` | pci.org `…/Transportation_Resources/{Slab Shapes, Box Shapes, AASHTO-PCI Bulb-Tees, Deck Bulb-Tees, NeXT Bridge Beams}.pdf` | Two-page extracts of the same appendix pages, recorded as duplicates |
| `pcine-nebt-us-customary.pdf` | https://www.pci.org/PCI_Docs/PCI_Northeast/Technical_Resources/Bridge/NEBT_US_Customary.pdf | Northeast bulb-tees: section p1, bulb layout p2 |
| `pcine-nedbt-2018.pdf` | https://www.pci.org/PCI_Docs/PCI_Northeast/Technical_Resources/Bridge/2018_03_06_NEDBT_plot.pdf | NEDBT sheet NEDBT-03 (PDF p3): details 1 and 7 |
| `pcij-2021-mj-brice-appendix.pdf` | https://www.pci.org/PCI_Docs/Publications/PCI%20Journal/2021/May-June/19-0034%20Brice_Appendix_MJ21.pdf | Independent property tables: AASHTO, FDOT and NEBT (plus other states, left to other agents) |
| `pcine-nebt-load-charts-2013-us.pdf`, `pcine-nebt-ptdg.pdf` | pci.org PCI Northeast | Context only |
| `fdot-2027-450-0{36,45,54,63,72,78,84,96}.pdf` | https://fdotwww.blob.core.windows.net/sitefinity/docs/default-source/design/standardplans/2027/idx/450-0NN.pdf | FIB end views, sheet 1 (last revised 11/01/19) |
| `fdot-2027-450-2{48,54,63,72}.pdf` | …/2027/idx/450-2NN.pdf | FUB typical sections, sheet 1 (last revised 11/01/16) |
| `fdot-2027-450-45{1,2,3}.pdf` | …/2027/idx/450-45N.pdf | Florida slab beam typical section and flange detail |
| `fdot-2027-spi-450-{010,210,450,120}.pdf` | https://fdotwww.blob.core.windows.net/sitefinity/docs/default-source/design/standardplans/2027/spi/spi-450-NNN.pdf | FY 2026-27 Standard Plans Instructions: section property tables (PDF p9, p10, pp32–34 and p7) |
| `fdot-2027-450-{010,120,210,450}.pdf`, `fdot-precast-beam-example.pdf` | as above; fdot.gov structures manual | Typical notes; AASHTO Type II; context |

The older FDOT IDS-20010 (2017) PDF is truncated on the server
(`fdot.gov/…/DS/17/IDS/IDS-20010.pdf`). It is superseded by the SPI files and
was not needed.

## Families implemented

The API is in mm, with the origin at mid-soffit and y upwards. Transcription
was done in source inches. Each drawing was read visually from 300–600 dpi
renders.

| Class (module) | Sizes | Provenance | Source locator | Validation |
|---|---|---|---|---|
| `PciSlabBeamSection` (`us.pci_standard_products`) | SI–SIV × 36/48 (8) | transcribed-with-convention | App. B-3/B-4, PDF p4–5 | area ≤0.12 %, yb exact, Ixx ≤0.02 % |
| `PciBoxBeamSection` | BI–BIV × 36/48 (8) | transcribed-with-convention | B-5/B-6, PDF p6–7 | area exact, yb ≤0.05 %, Ixx ≤0.09 % |
| `PciBulbTeeSection` | BT-54/63/72 | transcribed | B-9, PDF p10 | area exact, Ixx ≤0.03 % |
| `PciDeckBulbTeeSection` | DBT35/53/65 × 48/72/96 (9) | 6 transcribed, 3 (48 in) with convention | B-11, PDF p12 | area exact (72/96); +0.5 in² (48); Ixx ≤0.001 % |
| `PciDoubleTeeSection` | 5 light + 10 heavy (15) | transcribed | B-13, PDF p14 | light ≤0.07 % area; heavy pinned, see below |
| `PciNextBeamSection` (`us.pci_regional_products`) | NEXT 28–40 D × 96/120, NEXT 24–36 F × 95.5/143.5 (16) | transcribed-with-convention | App. C-3/C-4, PDF p22–23 | area −0.10 to +0.02 %, Ixx ≤0.1 %, yb ≤0.15 % |
| `PciNeBulbTeeSection` | NEBT39…87 (8) | transcribed-with-convention | PCINE NEBT sheet p1–2 | area ≤0.08 %, yb ≤0.07 %, Ixx ≤0.18 % |
| `PciNeDeckBulbTeeSection` | NEDBT40…80 (6) | transcribed-with-convention | NEDBT-03 (PDF p3) | area ≤0.13 %, Ixx ≤0.05 %, yb ≤0.02 % |
| `PciZone6UGirderSection` | U72/84/96 × 3/4 in ducts (6) | transcribed-with-convention | App. C-11 (sheet U-7), PDF p30 | area within 0.16 % of the weight-implied area |
| `FdotFloridaIBeamSection` (`us.fdot_girders`) | FIB-36/45/54/63/72/78/84/96 (8) | transcribed-with-convention | Index 450-0NN sheet 1; SPI 450-010 p9 | area +0.005 %, **perimeter exact**, Ixx ≤0.005 %, Iyy +0.003 % |
| `FdotFloridaUBeamSection` | FUB-48/54/63/72 (4) | transcribed-with-convention | Index 450-2NN sheet 1; SPI 450-210 p10 | area ≤0.07 %, Ixx ≤0.06 %, Iyy ≤0.14 % |
| `FdotFloridaSlabBeamSection` | 12/15/18 in × 48…60 in widths (39) | transcribed-with-convention | Index 450-451/2/3; SPI 450-450 pp32–34 | area/perimeter/Ixx/Iyy ≤0.01 % (one pinned Iyy) |

### Transcription tables (source inches)

- **Slab beams, B-3.** Each row gives L, H, L1, L2, voids, D1, D2:
  SI-36 36,12; SII-36 36,15,10.5,7.5,2,8;
  SIII-36 36,18,10.5,7.5,2,10; SIV-36 36,21,10,8,2,12; SI-48 48,12;
  SII-48 48,15,10,14,3,8,8; SIII-48 48,18,9.5,14.5,3,10,10;
  SIV-48 48,21,10,14,3,12,10.
- **Box beams, B-5.** W×H: 36/48 × 27, 33, 39, 42. Webs are 5 in, top and
  bottom flanges are 5.5 in, and the void chamfers are 3×3 in.
- **AASHTO-PCI bulb-tee.** The top flange is 3'-6", with a 3.5 in edge and a
  2 in drop over 1'-4". The 2×2 in fillet leads into a 6 in web. The bottom
  flange is 2'-2" wide, with a 6 in edge and a 4.5 in rise over 10 in.
  H = 54/63/72.
- **Deck bulb-tee.** The flange is 6 in. The taper is 3 in, then a 2×2 in
  fillet into a 6 in web. The taper run is 1'-7½", followed by a VAR flat.
  The bottom flange is 2'-1" wide, with a 6 in edge and a 3 in rise. H = 35/53/65,
  Hw = H − 20.
- **Double tees.** The values are W(ft)/H/T/A/C/E. The L and H tables are
  transcribed verbatim into the JSON.
- **NEXT beams.** Stems are 5'-0" c/c. Each stem is 1'-3" wide at the flange
  underside and battered 0.375:12 per face to the base width C. The table
  gives C = 13–13.75. R = 4 in fillets. ¾ in chamfers. The flange is 8 in (D)
  or 4 in (F).
- **NEBT.** Top 47.24 in, edge 3.35 in, 1.97 in taper. Web 7.09 in. Bottom
  31.89 in, edge 8.66 in, 3.94 in rise over 12.40 in. R7.87 fillets, R3.94
  bulb radius (p1 prints 3.9 in), 0.79 in chamfer and R0.79 at the top edge.
  Depths are 39.37…86.61 in (1000–2200 mm).
- **NEDBT.** Width 60 in. Flange 8 in minimum, 2¼ in drop. Web 7 1/16 in.
  R7 7/8 fillets. Bottom 31 7/8 in, 8 11/16 in edge, 3 15/16 in rise,
  ¾ in chamfer. H = 40…80 in.
- **Zone 6 U (U-7 table).** Each row gives D/duct/tw/W/T/tf/bf/weight:
  U72-3 72/3/9/121/81/20/70/2117;
  U84-3 84/3/9/127/87/20/70/2349; U96-3 96/3/9/133/93/20/70/2581;
  U72-4 72/4/10/123/81/21/72/2271; U84-4 84/4/10/129/87/21/72/2529;
  U96-4 96/4/10/135/93/21/72/2787. The bottom slab is 9 in and the flange edge
  9¼ in. Edge draft 2¼ in, 7½ in underside, 3:12 batter. Chamfers are 3 in
  inside and 1½ in at the soffit.
- **FIB.** The top is 4'-0", with a 3½ in edge and a 1½ in drop over 1'-5".
  A 3½ × 3½ in chamfer leads into a 7 in web. The bottom is 3'-2", with a 7 in
  edge and a 7½ in rise over 1'-3½" to the web face, plus a 1'-3" radius and
  ¾ in soffit chamfers. The straight web is H − 23 (1'-1" for FIB-36,
  6'-1" for FIB-96).
- **FUB.** The soffit is 4'-8" and the bottom slab 10 in. The inner 3 in
  chamfer sits at 4'-3⅛". The lower inner face is 1:4 and H − 34 high
  (1'-2"/1'-8"/3'-2" for 48/54/72). The upper inner face rises 21 in with a
  1 15/16 in run. Top flanges are 1'-4" wide, the edge 7 in, the underside drop
  1 in, the draft ½ in over the 8½ in underside. Chamfers are ¾ in and 1½ in.
  Top widths are 7'-10" (48), 8'-1" (54) and 8'-10" (72).
- **FSB.** W is measured at the soffit working point. The 4 in flange projects
  6 in. The upper body has 2 in chamfers. A ¾ in re-entrant fill, a ½ in edge
  draft, and ½ in / ¾ in edge chamfers. The body height is H − 4.

## Conventions and estimates (all recorded in the family JSON `geometry_notes`)

1. **Slab beams.** Keyways are omitted. PCI's published areas equal L·H minus
   the circular voids exactly, so PCI's own properties exclude the keyways.
2. **Box beams.** Every published area is 13.5 in² below the chamfered box.
   Keyway detail 2 (3/8 in × 6 in, then 3/4 in × 6 in) removes exactly
   6.75 in² per side and moves yb by the published amount, so detail 2 is used
   on both sides. The small sloped transitions are squared.
3. **Deck bulb-tee at 48 in.** The 19.5 in taper run overshoots the 24 in half
   width. The taper therefore keeps its 3 in drop and ends at the edge. This
   gives +0.5 in² in area; yb and Ixx match to 0.01 %.
4. **NEXT.** The D-beam edge key is undimensioned. It was scaled at 600 dpi as
   a 1 in recess (1 in land, 1 in taper, 4 in flat, 1 in taper, 1 in land).
   The F-beam edge is a ¼ in draft plus an R≈2 in rounded lower corner, also
   scaled. Neither was fitted; the areas still close within 0.1 %.
5. **NEDBT.** The bulb shoulder radius is not labelled, so the NEBT value
   (3.94 in) is used. The flange-edge V-key was scaled at 0.9 in. Callout
   rounding (12 3/8 in vs (31 7/8 − 7 1/16)/2) is 1/32 in. The flange is the
   8 in minimum; any variable build-up is excluded.
6. **Zone 6 U-girders.** The upper inner face slopes inward 2 in over 21 in,
   as dimensioned on the haunched-girder view of the same sheet. It meets the
   web inner face, which is offset tw perpendicular to the outer face. These
   two choices reproduce the weight-implied areas within 0.16 %, which is
   independent support for them. The source states the drawing is "for
   illustration purposes only", and `source_status` says so.
7. **FSB.** The re-entrant "¾ in fillet" is modelled as a 45° fill (chamfer).
   A circular fillet would be 0.32 in² low, whereas the fill reproduces all 39
   areas to 0.01 in².
8. **Polygonisation.** Arcs use 32 chords and circles use 128 chords.

## Pinned discrepancies (tests: `tests/test_us_pci_*`, `tests/test_us_fdot_*`)

- **PCI double tees, heavy table.** H6/7/8-35 are −0.78 to −0.89 % in area.
  H6/7/8-27 and H6/7/8-21 are −0.29 to −0.62 % in area and +1.53 to +1.70 %
  in Ixx, with yb −0.38 to −0.63 %. No single undimensioned detail explains
  all nine sections. The printed geometry is kept and each residual is
  pinned. Two smaller light-table offsets are also pinned: L5-27 yb −0.35 %
  and L6-27 yb −0.27 % / Ixx +0.14 %.
- **FDOT FSB 18 in × 5'-0" Iyy.** The table prints 195,689 in⁴; the polygon
  gives 196,689 (+0.51 %). The neighbouring increments imply about 196,700,
  so this is probably a one-digit typo in SPI 450-450.

## Not implemented / leads

- **FDOT AASHTO Type II (Index 450-120).** This is the PCI Type II outline
  plus ¾ in bottom chamfers. SPI 450-120 publishes the PCI properties (369 in²,
  50,979 in⁴) "neglecting the chamfers". Use `AashtoIBeamSection("II")`; the
  outline is not duplicated.
- **FIB-102.** It appears in PCI Journal 2021 Table A.4 (A = 1370.6 in²) but
  not in the FY 2026-27 Standard Plans index. It needs the retired Index 20102
  drawing.
- **PCI Zone 6 haunched pier girder (U84/132).** The depth is variable along
  the span. Not a prismatic profile.
- **AASHTO-PCI-ASBI segmental box segments (B-15 to B-18) and PCI Zone 6 U
  details beyond U-7.** These are out of scope (segmental/post-tensioned).
  They are recorded as leads.
- **PCEF / New England "NEBT" is the Northeast bulb-tee (implemented).** No
  separate PCEF table was found. The NEBT post-tensioned design guide
  (`pcine-nebt-ptdg.pdf`) uses the same section.
- **The PCI Journal 2021 appendix** also tabulates CA, CO, IL, MN, NE, NC,
  OH, OR, TX, VA and WA girders. Those are other agents' scope. It is a useful
  independent property check.
