# WSDOT girder extraction: WF, U/UF tubs, bulb tees, deck bulb tees, slabs (2026-09)

This round adds **44 WSDOT gross-section profiles** to `bridgebeams.us`. The existing W42G/W50G/W58G/W74G module (`wsdot_w_girders.py`) is unchanged. All source dimensions are stored in inches in `src/bridgebeams/us/data/wsdot_extended_girders.json`. The code converts to millimetres with 1 in = 25.4 mm exactly. The origin is at mid-soffit and y points up. Only gross concrete is modelled: no strands, deck slab, end blocks, recesses or sawteeth.

## Sources

| Id | Document | Status | Local file / SHA-256 |
|---|---|---|---|
| wsdot_2006 | WSDOT *Bridge Design Manual* M 23-50.01 (Complete). Appendix 5.6-A sheets are dated June 2006; the manual pages are dated August 2006. <https://wsdot.wa.gov/publications/manuals/fulltext/M23-50/M23-50.01Complete.pdf> | Archived. Used as the geometry source. | `sources/expansion/europe-americas/us_wsdot_2006_complete.pdf`, `db8e991a…f3676af` |
| wsdot_2025 | WSDOT BDM M 23-50.24, ch. 5, Table 5.6.1-1, June 2025. <https://www.wsdot.wa.gov/publications/manuals/fulltext/m23-50/chapter5.pdf> | Current. Used as the property source. | `sources/expansion/europe-americas/us_wsdot_chapter5_2025.pdf`, `6af4c603…84205da0` |
| wsdot_2026_deck | Sheet 5.6-A1-11, *Prestressed Concrete Deck Girders*, revised 2026-07-30. <https://wsdot.wa.gov/publications/fulltext/Bridge/Web_BSD/5.6_A1_11.PDF> | **PRELIMINARY PLAN – NOT FOR CONSTRUCTION** | `sources/expansion/europe-americas/us_wsdot_deck.pdf`, `033bcab1…25fb46b` |

Page locators in the 2006 PDF (every page was rendered and viewed at 200–600 dpi):

| Item | PDF page | Printed page/sheet |
|---|---|---|
| 2006 properties table | 306 | p5-96, Table 5.6.1-1 |
| Wide-flange girders (WF) | 441 | sheet 5.6-A1-2 |
| Bulb tees | 442 | sheet 5.6-A1-3 |
| Wide-flange bulb tees | 443 | sheet 5.6-A1-4 |
| U tubs | 444 | sheet 5.6-A1-5 |
| UF tubs | 445 | sheet 5.6-A1-6 |
| Deck bulb tees (DG) | 446 | sheet 5.6-A1-7 |
| Slabs | 447 | sheet 5.6-A1-8 |
| W32BTG Section C | 534 | detail sheet 5.6-A13-1 |
| Tub typical section | 546 | detail sheet 5.6-A16-1 |
| W35DG section | 580 | detail sheet 5.6-A24-1 |
| W35DG keyway, Section A | 581 | detail sheet 5.6-A24-2 |
| W35DG worked example | 737 | Appendix 5-B8 |

Detail sheets 5.6-A3 to 5.6-A27 occupy about PDF pp460–595. The key labels were read from their title blocks.

## Implemented classes

| Class (module) | SIZES | Provenance | Source status |
|---|---|---|---|
| `WsdotWfGirderSection` (`wsdot_wf_girders.py`) | WF36G, WF42G, WF50G, WF58G, WF66G, WF74G, WF83G, WF95G, WF100G, WF100G-61 | WF42/50/58/74/83/95: transcribed. WF36/66/100: transcribed-with-convention. WF100G-61: fitted-reconstruction. | Current (2025 properties) |
| `WsdotTubGirderSection` (`wsdot_tub_girders.py`) | U54/U66/U78 and UF60/UF72/UF84, each in G4/G5/G6 (18 sizes) | U G4/G5: transcribed. UF G4/G5: transcribed-with-convention. All G6: transcribed-with-convention. | U/UF60/UF72 G4/G5 are current. UF84 and all G6 are historic 2006 only. |
| `WsdotBulbTeeSection` (`wsdot_legacy_girders.py`) | W32BTG, W38BTG, W62BTG, WF32BTG, WF38BTG, WF50BTG, WF62BTG | W*BTG: transcribed. WF*BTG: estimate. | Historic 2006 |
| `WsdotDeckBulbTeeSection` (same module) | W35DG, W41DG, W53DG, W65DG (`spacing_in` 48–72, default 48) | transcribed-with-convention | Historic 2006. The 2026 replacement sheet is PRELIMINARY. |
| `WsdotSlabGirderSection` (same module) | SLAB12x48, SLAB18x48, SLAB24x48, SLAB26x48, SLAB30x52 | 12/18/26: transcribed-with-convention. 24/30: estimate. | Current (2025 properties) |

## Transcriptions (inches)

- **WF template (5.6-A1-2):**
  - Top flange: 4'-1" (49 in) wide, with a 3" edge, a 3" taper and a 3"×3" bevel into the web.
  - Web: 6⅛".
  - Bottom flange: 3'-2⅜" wide, with a 1" chamfer, a 5⅛" edge, a 4½" taper and a 3"×3" bevel.
  - The 1'-4⅛" callout is measured from the web face to the bottom-flange edge (19.1875 − 3.0625 = 16.125 in).
  - Depths: 42, 50 and 58 in; 74 in; W83G = 6'-10⅝" (82.625 in); W95G = 7'-10½" (94.5 in).
  - WF36G, WF66G and WF100G are not drawn. They use the same template at the 2025 depths.
- **U tubs (5.6-A1-5):**
  - Bottom width 4'-0", 5'-0" or 6'-0". Depth 4'-6", 5'-6" or 6'-6".
  - Webs slope 7:1. The 7" (TYP.) thickness is measured square to the web, which is 7.0711 in horizontally.
  - Bottom slab 6". The fillet top is 1'-0" above the soffit.
  - Fillet horizontal run: 1'-0" for G4 and G5, 1'-6" for G6.
- **UF tubs (5.6-A1-6):**
  - Depth 5'-0", 6'-0" or 7'-0".
  - The flange block overhangs 3" inboard and 5" outboard, at the web junction 6 in below the top.
  - The block has a 4½" edge and a 1½" taper. Its printed width is 1'-3 1/16".
- **Bulb tees (5.6-A1-3; W32BTG Section C):**
  - Top flange: 49 in wide, with a 3"/3"/2" stack, a 1'-6½" taper run and a 3" bevel run.
  - Web: 6". Bottom flange: 2'-1", with a 6" edge, a 3" taper over 9½" and a 1" chamfer (TYP.).
  - WF*BTG (5.6-A1-4) uses the same stack. Its flange width is 4'-0" MIN to 8'-0" MAX, and its horizontal runs are not dimensioned.
- **Deck bulb tees (5.6-A1-7; 5.6-A24-1/-2):**
  - Top stack: 6" flange, 3" taper and a 2"×2" bevel. Taper run 1'-7½".
  - Web 6". Bottom flange as for the bulb tees.
  - Flange width is 4'-0" MIN to 6'-0" MAX to the joint centreline. The concrete edge sits ½" (TYP.) from the joint at the top and 3/16" (TYP.) at the lower lip.
  - Keyway: a 1" vertical face at the top, then a V recess 2" deep with its apex 3" below the top. The recess returns to the lip 5" below the top.
- **Slabs (5.6-A1-8):**
  - 12" solid. 18" with three 9" voids at 0 and ±12½". 26" with two 15.7" voids at ±9".
  - The module is 4'-0", with a 1" (TYP.) top joint and a 3/16" bottom joint. The V key is undimensioned.

## Conventions, estimates and findings

1. **The 2006 Table 5.6.1-1 omits the 1 in bottom chamfers.** With the chamfers removed, the table is reproduced exactly for W50G (526.5/22.77/165462), WF42G (728.5/20.33/184042.9), WF50G and WF58G. The 2025 table includes the chamfers and matches the drawn outlines exactly. The 2025 table is therefore the validation target wherever it exists. The 2006 WF74G/W83G/W95G rows differ slightly again; they use older depths (82.62 and 94.49 in).
2. **WF:** all nine sizes reproduce the 2025 A, Yb, Ix and Iy to print precision.
3. **WF100G-61** (2025 row "WF100G with 5'-1" Top Flange"): no drawing is held. A 3 in thick flat extension from x = 24.5 in to x = 30.5 in reproduces A, Yb, Ix and Iy exactly (1118.78/49.890/1612834/99849), so it is recorded as a fitted reconstruction.
4. **UF flange width:** the overhang callouts give a block width of 15.0711 in. The printed width, 15 1/16 in, is that value rounded to 1/16 in. The overhang reading reproduces all properties exactly; the printed width would not.
5. **G6 tub discrepancy (re-diagnosed):** the drawn 1'-6" fillet run gives areas 36.0 in² below the 2006 table for all six G6 sizes. A **2'-0" run reproduces the 2006 G6 A, Yb and Ix exactly** for all six sizes; for example, U54G6 gives 1254.82/18.164/341728 against a published 1254.8/18.16/341728. The fillet scales to about 18 in on the drawing, so the 2006 drawing and the 2006 table disagree. Detail sheet 5.6-A16-1 breaks the fillet in its typical section and cannot settle the question. The drawn geometry is implemented. The −36 in² residual is pinned in `test_g6_drawn_outline_is_36in2_short_of_2006_table`. The 24 in value is recorded in the JSON (`fillet_run_that_reproduces_2006_table_in`).
6. **BTG:** the drawn outline, including the chamfer, is exactly +4.0 in² over the 2006 table at all three depths. Yb is +0.11 to +0.20 in and Iz is +0.07 to +0.37%. Without chamfers the excess is 5.0 in². First-moment balance places that excess about 6 in below the top, i.e. at the taper/bevel junction. The following readings were tested and none closes it: a 2.5 or 2.75 in edge, a narrower flange, no bevel, and top chamfers. The residual is unexplained and is pinned.
7. **WF*BTG** (estimate): the taper run and bevel are assumed equal to the W*BTG values (18.5 + 3 in), which matches the scaled drawing (~19–20 in). A constant 3 in flat extends to the variable flange width, with a default of 72 in. No published properties exist.
8. **DG:**
   - Concrete top width is spacing − 1 in, and the lower lip is at spacing/2 − 3/16 in.
   - At 48 in spacing the 19.5 in taper would pass the tip, so it is clipped there (the "VARIES" flat length is 0).
   - The drip notch is omitted.
   - W35DG compared with the worked example (A 669, yb 20.9, I 100096, Ip 169341, giving Iy 69245): A −0.57%, yb +0.05 in, I −0.52%, Iy −3.4%. Without the keyway the residuals are +0.43%, +0.17 in, +0.34% and +1.6%. The keyway is kept because it is drawn and dimensioned. The worked example does not give its own outline.
   - The 2026 PRELIMINARY sheet raises the DG minimum width to 4'-1".
9. **Slabs:** WSDOT's 2025 properties equal a rectangle of module width minus 1 in, less circular voids at mid-depth, with the keys ignored. This holds exactly for all five slabs: 12" 564/6768; 18" 655.1/21876; 24" 740.8/48178; 26" 834.8/62875; 30"×4'-4" 1021.1/104444. The implementation follows that convention.
   - The 24" and 30" slabs are not in the 2006 manual. Their H, W, void count and diameter come from the 2026 PRELIMINARY table.
   - Their void x-positions are estimates: ±9 in for the 24" slab and ±10 in for the 30" slab. These positions affect Iy only.
   - Voids are 256-gon interiors, which changes A by less than 0.02%.

## Residual summary (calculated − published)

The full per-size values are in the JSON under `residuals`.

| Family | Reference | Area | Yb | Ix | Iy |
|---|---|---|---|---|---|
| WF (10) | 2025 | ≤ 0.04 in² | ≤ 0.005 in | ≤ 0.5 in⁴ | ≤ 0.5 in⁴ |
| U/UF G4/G5 (10) | 2025 | ≤ 0.035 in² | ≤ 0.005 in | ≤ 0.5 in⁴ | ≤ 0.5 in⁴ |
| UF84 G4/G5 | 2006 | 0.013 in² | ≤ 0.0004 in | ≤ 0.2 in⁴ | — |
| G6 (6) | 2006 | −36.0 in² (pinned) | +0.30 to +0.53 in | −1.1 to −1.7% | — |
| W*BTG (3) | 2006 | +4.0 in² (pinned) | +0.11 to +0.20 in | +0.07 to +0.37% | — |
| W35DG | worked example | −3.8 in² (−0.57%) | +0.05 in | −0.52% | −3.4% |
| Slabs (5) | 2025 | ≤ 0.17 in² | 0 | ≤ 2 in⁴ | — |

## Remaining uncertainties

- The origin of the G6 fillet-run conflict (1'-6" on the drawing, 2'-0" implied by the table) is unresolved. No G6 row survives in the 2025 table.
- The BTG 4–5 in² table excess is unexplained.
- The WF*BTG taper and bevel runs are assumed.
- For the DG keyway, the exact end point of the lower slope, the drip notch and the worked example's own outline are unknown.
- The 24" and 30" slab void spacings are assumed.
- The WF100G 5'-1" flange extension form is inferred. The current WSDOT 5.6-A1-10 sheet was not inspected for it.
- Not in scope and not implemented: double tees and ribbed decks (5.6-A1-9), PT spliced girders (5.6-A1-10/-11), and the 2026 WF*DG/WF*TDG deck girders (PRELIMINARY; not dimensioned).
