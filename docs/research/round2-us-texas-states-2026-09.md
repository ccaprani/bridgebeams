# Round 2: US state DOT standard beams (Texas and other states), September 2026

Topic `us-texas-states`. Retrieved and implemented 2026-09-23. This record covers
**433 profiles** in 39 section classes under `bridgebeams.us` (modules `txdot_*` and `state_*`).
They come from DOT standard sheets, design manuals and TxDOT's PSTRS14 program library.
It supplements [us-states-followup.md](us-states-followup.md). The machine-readable record is
[round2-us-texas-states-2026-09.json](data/round2-us-texas-states-2026-09.json).
Each module also has its own data JSON under `src/bridgebeams/us/data/`, holding source URL, SHA-256,
page locators, inch transcriptions, published properties and per-size residuals.

**Disclaimer.** These are useful reconstructions for crowd-sourced correction, not
authoritative agency geometry. `provenance` on every section states how far to trust it.

| State | Classes (profiles) | Provenance | Source status |
|---|---|---|---|
| TX | Tx I (7), WF-Tx (7), box 4B/5B (10), X-beam (8), slab (4) | transcribed / -with-convention | current TxDOT standards (2012-2024) |
| TX | legacy I A/B/C/54/72 (5), U40/U54 (2), decked slab (6), double-T T/HT (18) | with-convention / fitted / estimate | PSTRS14 v6.1 library (Feb 2016); U and DS standards retired 2025 |
| CO | CBT37.5-CBT90 (7) | transcribed | B-618-CBT2, rev. to 9/24 |
| VA | PCBT-29..93 (9), voided slab (6), box (8) | transcribed / -with-convention | VDOT Manual Part 2 Ch 12, Part 4 |
| CA | I (6), BT (7), WF + WF-PT (26), bath tub (6), voided slab (8) | transcribed / -with-convention / estimate | Caltrans BDM 5.3 (Sept 2023) |
| MO | I Types 2-8 (14), NU (6), box (18), voided slab (9), solid slab (2) | transcribed | MoDOT EPG 751.21/751.22 |
| IA | A-D (4), BTB-BTE (4) | transcribed / -with-convention | Iowa LRFD BDM 5.4.1 (Jan 2025) |
| NE | NU900-NU2000 (6) | fitted-reconstruction | NDOR Design Aids of NU I-Girder Bridges (2010); 2026 BDM not retrievable |
| WI | 28, 36W-82W (6), box (12) | transcribed / estimate | WisDOT Bridge Manual Ch 19 standards |
| IL | deck beams 11x48-42x48 (12) | transcribed | IDOT CAD cell library 2025 |
| OR | slab (6), box (4), I Types II-V (4) | transcribed / -with-convention | ODOT BR300/BR400 series (2026) |
| PA | I (21), 28/63-28/96 (7), bulb tee (54), box/plank (58) | transcribed-with-convention | PennDOT BD-652M (2016), BC-775M (2022) |
| NY | box (22), slab unit (8), PCEF bulb tee (6) | transcribed / -with-convention | NYSDOT BD-PC set 01-26 (effective May 2026) |

Not implemented: Georgia (the bulb tee is AASHTO-PCI BT-63, and the manuals are behind a WAF);
Michigan (Cloudflare 403); Ohio (the ODOT standards moved and the new pages 404; Brice 2021 gives WF36-49..WF72-49
and Modified Type IV properties, but not dimensions). NYSDOT NEBT/NEXT sheets were transcribed but are not exposed.
They duplicate the PCI Northeast family in `pci_regional_products`; the outlines agree within about 0.2% of area.

## Independent cross-check: Brice et al., PCI Journal May-June 2021 appendix

The source is `sources/expansion/round2/us/pcij-2021-mj-brice-appendix.pdf`
(<https://www.pci.org/PCI_Docs/Publications/PCI%20Journal/2021/May-June/19-0034%20Brice_Appendix_MJ21.pdf>,
SHA-256 `59570b50e78c1cafdd1feebc820abb22bf88ece9be603f917a22b279ffc4c5f9`), Tables A.2-A.13.
Its values were computed by the authors from agency drawings, so they are independent of the tables transcribed here.
Per-size residuals are in the JSON (`brice_crosscheck`).

- **TX Tx28-Tx70, CO CBT45-CBT90, CA I36-I66, CA BT49-BT85, VA PCBT-29..93**: all agree
  within 0.01% A, 0.005 in yb and 0.01% Ix/Iy. The exception is CA BT67, whose Ix is 0.09% low against Brice.
  Brice gives BT49 A = 876.1 in^2, which confirms that Caltrans' printed 856 is a misprint.
- **NE NU900-NU2000**: A +0.03 to +0.08%, yb +0.01 to +0.04 in, Ix -0.10 to +0.24%, Iy -0.07%.
  This is consistent with the fitted metric reconstruction.
- **CA WF48-WF120**: A -0.2 to -0.34%, yb -0.23 to -0.30 in, Iy +4.0% against Brice (the 2016 Design Aid).
  The implemented outline follows BDM 5.3 (2023) and agrees with that memo within 0.03% A.
  The systematic Iy and yb offsets suggest the 2016 WF bottom flange differs from 2023. That is an edition difference, not a transcription error (unverified).
- **CA Tub55-85**: A +0.10 to +0.20%, Ix -0.44 to +0.09% (Tub73 is the outlier), consistent with the 2023 memo residuals.
- Brice's IL IL27-IL72, OR BI/BT, OH WF and MN M/MH/MW tables have no dimensioned drawing in hand. They are recorded as leads only.



### Texas (TxDOT) — 67 profiles

Module `bridgebeams.us.txdot_girders` and `bridgebeams.us.txdot_slabs_boxes`;
data `src/bridgebeams/us/data/txdot_beams.json` (source URLs, SHA-256, page
locators, transcription in inches, published properties, per-size residuals).
Standards index: <https://www.dot.state.tx.us/insdtdot/orgchart/cmd/cserve/standard/bridge-e.htm>
(retrieved 2026-09-23). The TxDOT FTP server's TLS chain is incomplete;
files were fetched with certificate verification disabled (public documents,
integrity recorded by SHA-256).

#### Sources

| Local file (`sources/expansion/round2/us/txdot/`) | URL | SHA-256 (first 16) | Locator | Status |
|---|---|---|---|---|
| IG-IGD-23.pdf | ftp.dot.state.tx.us/…/bridge/IG-IGD-23.pdf | 35af35f82d321fbf | PDF p1, IGD sheet 1 of 2 | current; (c) Aug 2017, rev 10-19, 3-23 |
| IG-WF-IGD-24.pdf | …/IG-WF-IGD-24.pdf | 363dc8c44dbdaee4 | PDF p2, WF-IGD sheet 2 of 3 | current; (c) Aug 2024 |
| BB-B20/B28/B34/B40-12.pdf | …/BB-B20-12.pdf etc. | fdeee98c…, 284b509b…, 0343643e…, 05148523… | PDF p1, sheet 1 of 3 | current; (c) Dec 2006, rev 01-12 |
| XB-XB20/28/34/40-22.pdf | …/XB-XB20-22.pdf etc. | b065562e…, 79b8e475…, 9fa57210…, c337ecd6… | PDF p2, sheet 2 of 3 | current; (c) Aug 2022 |
| PSB-4SB12/4SB15/5SB12/5SB15-17.pdf | …/PSB-4SB12-17.pdf etc. | 17003d4f…, c99eff6d…, 3b475742…, b7b920a8… | PDF p1 | current; (c) Jan 2017 |
| pstrs14_user_guide.pdf | ftp.dot.state.tx.us/pub/txdot-info/isd/txdotapps/support/user_guide_pstrs14.pdf | 9d805d2c6c4a34f1 | App. A Fig 1 (p92), Fig 8 (p99), Fig 11 (p102), Fig 16 (p107) | PSTRS14 v6.1, Feb 2016 |
| pci2006_txdot_products.pdf | pci.org/PCI_Docs/Papers/2006/Txdot-Standard-Prestressed-Bridge-Products.pdf | e293ec418a0dcf59 | p7 Fig 9 | Eskridge & Holt, PCI NBC 2006 (supporting only) |
| u_beam_guide_2007.pdf | texashistory.unt.edu/ark:/67531/metapth637454/m2/1/high_res_d/u_beam_guide.pdf | 8ff1cac7e958c0eb | — | TxDOT draft U-beam design guide 2007 (no geometry) |

All dimension readings were made from 300–400 dpi renders (BB sheets are
stroke-font vector text with no text layer).

#### Transcription (inches)

**Tx girders (IGD).** Bottom 32, soffit chamfer 3/4, bottom-flange edge
6 3/4 (Tx28–40) / 8 3/4 (Tx46–70), taper 9 1/2 run × 4 3/4 rise, 3×3 web
fillet, web 7, 2×2 top fillet, top taper rise 2 (2 1/2 for Tx62/70) over
run top/2 − 5 1/2, top edge 3 1/2, top 36 (42 for Tx62/70). Clear web B =
6/12/18/22/30/37 1/2/45 1/2 closes exactly. Residuals: A ≤ 0.31 in² (print
rounding), Yb ≤ 0.005, Ix/Iy ≤ 0.5 in⁴ — exact.

**WF-Tx girders (WF-IGD).** Same bottom/web template; top 72 (84 for
WF-Tx62/70), taper rise 4 7/8 (5 7/8) over 30 1/2 (36 1/2). Curb and drip
bead (exterior girders only, note 14) excluded; published properties
exclude them. Exact, except **WF-Tx62 printed Ix 660,613 vs 680,613
computed** (A, Yb, Iy, weight all match) — digit misprint, pinned.

**Box beams (BB).** Bottom width 47 3/4 (4B) / 59 3/4 (5B), top width 4 in
less. Right-side stack from soffit: 3/4 chamfer; full-width edge he; 45°
recess r; vertical; 45° return (r−2); top vertical tv. B20: he 5, r 4, tv 5;
B28: 5, 5, 4; B34: 11, 5, 4; B40: 17, 5, 4. Void width 29 3/4 / 41 3/4
(B20), 27 3/4 / 39 3/4 (B28–40); bottom slab 5, top slab 5 1/2. B40 "over
100 ft" variant: 5×5 void bottom chamfers (note 8) → sizes `4B40-C`,
`5B40-C`. All 10 exact (A, Ytop, Ybott, I).

**X-beams (XB).** Same exterior as BB per depth; bottom slab 7, top slab
5 1/2, void 24 3/4 / 36 3/4. The soffit chamfer is drawn but not called out
on XB sheets: 3/4 in adopted from the BB note (provenance
`transcribed-with-convention`); with it all 8 exact, without it I is
0.1–0.2% high.

**Slab beams (PSB).** Rectangles 47 3/4 or 59 3/4 × 12 or 15. Printed
properties are those of the unchamfered rectangle (e.g. 573.0 = 47.75×12)
although the general notes chamfer exposed corners 3/4 in; rectangle used.
4SB15 printed I 13,429 = truncation of 13,429.7.

**Legacy I-beams (PSTRS14 Fig. 1).** Type A/B/C/54/72 table A–W. Soffit
chamfer undimensioned; 3/4 in reproduces A, Yb, I exactly. **Type 54:
printed F = 30 does not close D = 54 (sum 52); F = 32 reproduces
A 493.44 / Yb 25.531 / I 164,023 exactly** → used, pinned
(provenance `fitted-reconstruction`). Type IV in the same figure is the
AASHTO Type IV outline and is not duplicated (PCI/AASHTO module owns it).

**U40/U54 (PSTRS14 Fig. 11).** Table C/D/E/F/G/H/J/K plus common callouts:
bottom 4'-7", slab 8 1/4, top flange 1'-3 3/4, outer edge 5 7/8 high with
3/8 batter, flange soffit falls 7/8 to the web, web 5 normal, inner kink
at (G, 8 1/4+H), inner chamfer (2'-1 1/4, 11 1/4)→(1'-9 1/2, 8 1/4). Outer
web slope J/E = 1:3.97. Residuals: U40 A +2.8 in² (+0.28%), Yb −0.01,
I +0.23%; U54 A +1.7 (+0.15%), Yb −0.02, I +0.23%. Not fitted away.
Standards retired by TxDOT (index memo 06/11/2025); UBD sheet now 404.

**Decked slab beams (PSTRS14 Fig. 16).** Printed: A (6'-5 3/4, 7'-5 3/4,
7'-11 3/4), B, stem 4'-11 3/4, C = 12/15, deck 8. Void and deck-edge
slope undimensioned → least-squares fit of (void width, height, bottom,
edge undercut) per depth to the 9 printed A/Yb/I values: DS20 35.480 ×
6.608 at 6.224, undercut 2.194; DS23 44.321 × 8.432 at 6.696, undercut
2.693. Residuals ≤ 0.001% A, ≤ 0.004 in Yb, ≤ 2.1 in⁴ I. Provenance
`fitted-reconstruction`; standard retired Jan 2025.

**Double-T T/HT 22/28/36 (PSTRS14 Fig. 8).** Flange 6, width A, stem
bottom C, batter 3/4:12 per face, stems 48 in apart (4'-0"). HT's printed
B (1'-1 7/8) does not close with A and 48; 48 in spacing adopted for both
(identical area excess in T and HT supports it). Fillets and edge keys
omitted → A +4.0 to +4.5 in² (≤ 0.64%), Yb +0.03..0.06, I +0.54..0.95%.
Provenance `estimate`.

#### Leads not implemented (Texas)
- TxDOT "UX" U-beam variant: not found on the index or in PSTRS14.
- Current UBD / DSBD standard sheets: retired and removed (404); a Scribd
  copy of UB-UBD-23 exists but requires login (not used).
- PSTRS14 Fig. 3 "Type VI" (42/28/72, 1 1/4 chamfer): AASHTO Type VI outline — PCI/AASHTO module.
- PSTRS14 Figs 4/5 and 17/18 duplicate the current BB/XB sheets (confirmed identical tables for B20/B28).
- TxDOT Bridge Design Guide (Jan 2023) PDF returned an HTML interstitial; not used.


## VA / CO / GA / CA round-2 notes (fork), 2026-09-23

### Sources downloaded (all to sources/expansion/round2/us/, retrieved 2026-09-23)
| URL | local | SHA-256 |
|---|---|---|
| https://www.codot.gov/programs/bridge/bridge-manuals/design-standards/structural-worksheets-pdfs/b-600/sheet_b-618-cbt2.pdf | co_b-618-cbt2.pdf | 76c3495a789abd4e93d655f589d5de36977f8090e75dab5ce0717bf2d8d2e16b |
| https://www.codot.gov/programs/bridge/bridge-manuals/design-standards/structural-worksheets-pdfs/b-600/sheet_b-618-u.pdf | co_b-618-u.pdf | 32b7df65759c602abee131adb46088049a8d2d52bea9513ff9f5ce866a153147 |
| (also sheet_b-618-cbt1, -cbt3, -1..-7: elevations/PT box details, no new sections) | co_b-618-*.pdf | not recorded |
| https://www.vdot.virginia.gov/x/vdotvirginiagov/doing-business/technical-guidance-and-support/technical-guidance-documents/structure-and-bridge/manuals-of-structure-and-bridge-acc/part2/Chapter12.pdf | va_part2_ch12.pdf | 54d681c62ed1a8bc5f57e3100ee565ede2bbfaec9387a6f1163e859820659223 |
| .../part4/PCBT-53S.pdf (same base URL, /x/ path) | va_PCBT-53S.pdf | d293c77419065cdc871a0d26c782bd795d84057c734c60ec719aa3f83541b4be |
| https://www.vdot.virginia.gov/media/vdotvirginiagov/.../part4/Part4.pdf | va_part4.pdf | d8966b6555097ae28627909cc66332d47dbda146d4b53d1b05f1b519c166e57b |
| .../part4/PCBT-MISC1.pdf | va_PCBT-MISC1.pdf | 35c96f160dbf87e965eeaa41a86c6292ae2702d8da34d8dcd375469bf894ceb7 |
| https://dot.ca.gov/-/media/dot-media/programs/engineering/documents/bridgedesignmemos/09/092023bdm-53--precast-prestressed-girders-a11y.pdf | ca_bdm5-3.pdf | 748701c73a5a0765ef3f49a3f247df95f7d5242c44ca545429d57a267b244bb1 |
| https://dot.ca.gov/-/media/dot-media/programs/engineering/documents/bridgestandarddetails/chap-1/202007-xs1-121-1-a11y/xs1-121-1-a11y.pdf | ca_xs1-121-1.pdf | 4c23e66d92983887b22bc2839eaabe198dff8a28b9e1b4af06a46bc62d57dc34 |
| https://dot.ca.gov/-/media/dot-media/programs/engineering/documents/bridgestandarddetails/chap-1/202007-xs1-121-3-ug-a11y.pdf | ca_xs1-121-3-ug.pdf | 15435a8262b1d234ffac5ce4e9dad2649296c5efbbe2572efb91e1b391348cd6 |
| https://www.dot.ga.gov/PartnerSmart/DesignSoftware/Bridge/PDF/bulb63.pdf | ga_bulb63.pdf | 6c8e004bd1878f36b8fae2393ea3aa51fceb95c14531ad9f4613b8d2afbdda92 |

### Colorado — CoCbtGirderSection (7, transcribed)
Locator: B-618-CBT2 single sheet, revs 6/19..9/24; CBT 90 DETAIL fully dimensioned, table on sheet.
Template (in): top 50 (4'-2"), top edge 3.75, taper 3, bevel 3x3, web 7, bottom 39.5 (3'-3 1/2"),
bottom edge 5.875 (derived: D - 9.75 - clear web - 7.5, same for all), lower taper rise 4.5, lower bevel 3x3,
3/4 chamfer at soffit corners only. Clear web Ref = D - 23.125 on every detail.
Published (A, Ix, Iy, yb): 37.5: 792/151579/88998/18.50; 45: 845/240424/89212/22.08; 54: 908/378473/89469/26.40;
63: 971/553233/89727/30.74; 72: 1034/767268/89984/35.10; 81: 1097/1023130/90241/39.48; 90: 1160/1323390/90498/43.87.
Residuals: all four properties exact to print precision; CBT81 Ix computed 1,023,134 vs 1,023,130 (pinned).

### Virginia — state_va_girders.py
PCBT-29..93 (9, transcribed-with-convention). PCBT-53S sheet 1 (28Apr2023) + File 12.03-5 (PDF p31, 31Oct2018):
top 47, 4 edge, 1.5 taper, 2x2 bevel, 18 run, web 7, bottom 32, 7 edge, 3 taper rise over 9 run, 3.5x3.5 bevel,
clear web D-21. Soffit chamfer drawn undimensioned -> 3/4 in adopted; reproduces A (0.1), yb (0.01), I (0.1e3) exactly for all 9.
Voided slabs 36/48 x 15/18/21 (6, transcribed): File 12.05-5 (PDF p50, 26Apr2026) table W,D,D1,D2,A,B,C;
key File 12.05-10 (PDF p55): 3/8 recess over top 4", 3/8 transition, 3/4 recess to 8" below top, 3/4 bottom chamfer.
Published excludes keys; shear_keys=False reproduces A/I exactly; default keyed outline is 8.3 in^2 lower.
Box 36/48 x 27/33/39/42 (8, transcribed-with-convention): File 12.06-6 (PDF p64, 30Apr2026): 6" top/bottom slabs,
5" webs, 3x3 void chamfers; key File 12.06-11 (PDF p69): same key with 6"/12". Key-less = published + 20.0 in^2 exactly
(PCI-4th-ed key deducted in table, shape not given). VDOT key removes 12.8 -> pinned residual A +7.2 in^2 (1.0-1.2%),
yb +0.03..0.07, I +1.0..1.4%. Drip V-notches and tendon holes omitted.
Published box (A, yb, I): 36x27 580/13.31/51070; 36x33 640/16.25/86820; 36x39 700/19.20/134100; 36x42 730/20.68/162400;
48x27 724/13.35/67380; 48x33 784/16.30/113500; 48x39 844/19.25/173700; 48x42 874/20.73/209500.

### California — state_ca_girders.py (Caltrans BDM 5.3, Sept 2023, PDF pp3-8)
- CA I36..I66 (6, transcribed), Fig/Table 5.3.4.1-1 p3: 19 top/bottom, web 7, top 3+6, bottom 6+6. A exact; yb within 0.05 (printed 0.1); I within 0.14%.
- CA BT49..BT85 (7, transcribed-with-convention), p4: 47.25 top, 7.875 web, 3.9375 edge + 3.9375 taper, 29.5 bottom, 7.875 edge, 5.875 taper, R 7.875 tangent fillets; D from ft-in column (metric-converted). A within 0.11%, yb 0.045, I within 0.41%. **BT49 printed A 856 vs 876 computed (+2.35%) - misprint, pinned.**
- CA WF48..WF120 + WF48PT..WF120PT (26, transcribed-with-convention), pp5-6: top 48/49.5, web 6.5/8, bottom 45/46.5; 3" tip, 1.75 taper to web face (20.75 run), r=10 web fillets, r=2.5 tip/edge radii, 6.125 bottom edge, 6.375 taper (19.25 run), 3/4 soffit chamfer. Even rows A +0.02%, yb <=0.024, I -0.12..-0.30%. **Odd rows 78/90/102/114 (both variants): A ~2.2 in^2 below the uniform progression, I +0.1%: pinned.**
- CA TUB55..TUB85 (6, transcribed-with-convention), p7: 59 soffit, 4:1 webs, 7.875 normal web, 6.875 bottom slab, 16.75 flange to inner face, 2.875x2 ledge, inner vertical to 6.875 below top, incline to 11.75 below top, 3x3 inner chamfers. **Table column "D (in)" is actually h (D-475 mm).** A within 0.1%, yb 0.032, I within 0.25%.
- SI..SIV x 36/48 voided slabs (8, estimate), p8: printed widths/depths/voids; shear key undimensioned: estimated from 400-dpi render (top inset 1", recess 2", 1" chamfer, key zone middle third). No property table.
- xs1-121-1 bulb-tee detail sheet: depth D is a project variable -> no named sizes from it (Memo BT sizes used instead).

### Georgia — not implemented
GDOT bulb63.pdf (Bulb Tee 63 in PSC beam end spans, 2022) shows 3'-6" top flange = AASHTO-PCI BT-63 family (PCI-national, owned by another agent). GDOT Bridge & Structures Policy Manual (rev 3.8, 12/29/2025), BridgeNotes and Box Beam guide URLs return an F5 "Request Rejected" page to scripted fetches (WAF) - not bypassed.

### Leads not implemented
- CDOT B-618-U "Prestressed Concrete U" (32b7df...): parametric U (Fw, Tw 5/7.5/10, Tb 6.35/8.1, depths 48/60/72/84/96 "preferably"); flange width project-variable and no property table.
- VDOT PCB-2..6 (AASHTO Type II-VI, Part 4) - PCI-national geometry, not duplicated. VDOT exterior box (File 12.06-7), inverted T-beams (12.07) not examined in detail.
- GDOT policy manual Appendix 3D beam charts / Type I Mod / box beams: blocked by WAF.
- Caltrans voided slab key: dimension via Caltrans standard plan (B-series slab sheets) if a sheet is found.


## NE / MO / IA sub-slice notes (fork, 2026-09-23)

63 profiles implemented. Per-size residuals are in `ne-mo-ia-residuals.json`
(also embedded in `ne-mo-ia.json`). Transcriptions in source units are in the
package JSON files.

### Sources (URL -> local path, SHA-256)

| Source | Local | SHA-256 | Locator |
|---|---|---|---|
| NDOR "Design Aids of NU I-Girder Bridges" https://dot.nebraska.gov/media/cf4norno/design-aids-nu-i-girder-bridges.pdf (via Wayback 20250515024112) | sources/expansion/round2/us/ne_design-aids-nu-i-girder-bridges.pdf | 676284ea…a7b47dda | Fig 1 p13, Table 1 p14 (PDF = printed). PDF dated 2010-08-01 |
| MoDOT EPG 751.22 https://epg.modot.org/index.php/751.22_Prestressed_Concrete_I_Girders | sources/expansion/round2/us/mo_epg_751_22.html + modot/751.22.1.2_*_2022.jpg (7 figures) | html bedf92b1…; per-image hashes in state_mo_girders.json | 751.22.1.2 Geometric Properties |
| MoDOT EPG 751.21 https://epg.modot.org/index.php/751.21_Prestressed_Concrete_Slab_and_Box_Beams | mo_epg_751_21.html + modot/751.21.1.3_*.jpg (8 figures) | html 2f75e851…; per-image hashes in state_mo_slabs_boxes.json | 751.21.1.3 Geometric Properties + shear key detail |
| Iowa DOT LRFD BDM 5.4.1 (January 2025) https://iowadot.gov/media/4637/download?inline (via Wayback 20250522092537) | ia_bdm_5-4-2_ppcb.pdf | 970097a5…a5e707 | Figs 5.4.1.1.1-1/-2, PDF p3, printed 5.4.1: 3 |

### Transcription (inches)

**MoDOT I girders** (top/web/bottom; bottom edge; bottom taper rise×run; straight web; top taper(s) rise×run; top edge; 3/4 soffit bevel; top corners square):
Type 2: 13/6/17; 5; 6×5.5; 16; 1×3.5; 4 (D 32). Modified 7"/8" web: top 14/15, bottom 18/19.
Type 3: same widths; 7; 6×5.5; 20; 1×3.5; 5 (D 39). Type 4: 8; 6×5.5; 25; 1×3.5; 5 (D 45).
Type 6: 24/6.5/24; 6; 7×8.75; 31.5; 4.5×8.75; 5 (D 54). Modified 7½/8½ web: 25/25, 26/26.
Type 7: 42/6/26; 6; 4.5×10; 54; 2×2 then 2×16; 4 (D 72.5). Type 8: web 45 (D 63.5).

**MoDOT NU**: top 48 1/4, edge 2 9/16, taper 1 3/8 (to web face), web 5 7/8, R 7 7/8 web fillets, R 2 flange corners, bottom 38 3/8, edge 5 5/16, taper 5 1/2, 3/4 soffit chamfer. Depth / straight web: NU35 35 7/16 / 20 11/16; NU43 43 5/16 / 28 9/16; NU53 53 5/32 / 38 13/32; NU63 63 / 48 1/4; NU70 70 7/8 / 56 1/8; NU78 78 3/4 / 64. Stack closes exactly for every size.

**MoDOT boxes**: width 36 or 48; top slab 5, bottom slab 6; void width 22/24 (36 in) or 32/36 (48 in) for D<27 / D>=27; void height 6/10/16/22/28/31 for D 17/21/27/33/39/42; 2×2 void chamfers at four corners; 1 1/2 soffit bevels. Adjacent key: top 4 zone set back 5/8; 5/8×3/8 chamfer into recess 1 1/4 inside soffit face; recess over D−10; 3/4 rise × 1 1/4 run back out at y=6. Spread: plain rectangle.
**MoDOT voided slabs**: circular voids; 36 in: x=±8, 48 in: x=0,±14. Dia 8.5/11.5/12.5 (48-in 21-in centre void 10.5); centre height 8/9.5/10.5 for D 15/18/21. Same key for adjacent.
**MoDOT solid**: 48/52 × 11; key with 3 top zone, 4 recess, 4 bottom zone.

**Iowa A–D**: A 13/6/17; 5; 6×5.5; 16; 1×3.5; 4 (=MoDOT Type 2). B 13/6/17; 7; 6×5.5; 20; 1×3.5; 5. C 16/9/20; 8; 6×5.5; 25; 1×3.5; 5. D 20/7/22; 8; 7.5×7.5; 31.5; 1×6.5; 6. 3/4×3/4 soffit bevels.
**Iowa BTB–BTE**: top 34, tip 3 13/16, taper 1 11/16 to web face, web 6 1/2, R 8 web fillets, bottom 30, edge 7 1/2, taper 5 1/2 to web face, R 2 shoulder, 3/4 "FILLET" at soffit corners; straight web 17 1/2 / 26 1/2 / 35 1/2 / 44 1/2 (D 36/45/54/63). Secondary callouts (4 5/8, 7 1/16, 7 15/16, 6 3/16) check the fillet tangent points to 1/32 in.

**NDOR NU (metric)**: 1225 top, 65 edge, 45 taper, 150 web, R200, R50, 975 bottom, 135 edge, 140 taper; heights 900/1100/1350/1600/1800/2000. Figure 1 inch callouts (48.2, 2.56, 1.75, 5.9, 7.9, 2, 38.4, 5.3, 5.5) are these values rounded.

### Conventions and estimates

1. NE NU: **estimate** 20 mm soffit chamfer (not drawn). Without it, area is +527 mm² (+0.08%) and I is +0.09% for every size. With it: area ≤0.01%, I ≤0.06%, yb ≤0.05 in (print 0.1). Hence `fitted-reconstruction`.
2. NE NU: Table 1 NU1350 metric I is 126,841e6 mm⁴, but its inch value 302,334 in⁴ = 125,840e6 mm⁴. **Pinned** as a source typo (test_us_state_ne_nu.py::test_nu1350_metric_inertia_typo_pinned).
3. MoDOT NU uses a 1 3/8 in top taper, not NDOR's 1.75 in (45 mm). These are kept as separate state drawings. No geometry is transferred between them.
4. Iowa A–D: the printed A/yb/I exclude the drawn 3/4 in soffit bevels (exact to print). The polygon keeps the bevels, so the as-drawn area is 0.5625 in² below print. **Pinned** in test_us_state_ia_beams.py::test_ad_published_excludes_bevels.
5. Iowa BT: the "3/4 in FILLET" at the soffit is taken as a 3/4 in radius, so provenance is `transcribed-with-convention`. The top-flange tip corners are square, as drawn. The printed properties are not self-consistent between depths. Per-size residuals are **pinned**: area −0.13/−1.73/−0.23/−0.33 in², I −0.10/−0.16/−0.27/−0.29%. The BTB printed yb (17.14) is 0.515 in above the computed 16.62. This is pinned as a probable source error.
6. Arcs use 64 segments (MoDOT NU/Iowa BT/NE NU). Circular voids are 128-gons, which leaves the void area 0.04% low (≤0.17 in² gross-area excess).

### Residual summary

- MoDOT I (14) and NU (6): A ≤0.06 in², yb ≤0.005 in, Ixx ≤0.002%, Iyy ≤0.01%. These are exact to print.
- MoDOT boxes (18) and solid slabs (2): A ≤0.05 in², Ixx/Iyy ≤0.01%. The void areas are exact.
- MoDOT voided slabs (9): A ≤0.17 in² (polygonal voids), I ≤0.02%.
- Iowa A–D: exact to print once the bevels are added back. BT: see item 5.
- NE NU: see item 1.

### Leads not implemented

- The NDOT BDM 2026-02-23 (Figure 5.4 / Table 5.7, NU35–NU78) cannot be fetched: dot.nebraska.gov refuses connections from this host and has no Wayback copy. This is the current NE source. Its imperial NU35..NU78 set likely matches the MoDOT naming.
- The Iowa BSB standard sheets 4600–4790 and the standards index return HTTP 403.
- The MoDOT bridge standard drawing PDFs (modot.org) sit behind a 202 bot challenge. The EPG figures are sufficient.
- MoDOT EPG 751.22 also shows 7-ksi/8-ksi strand design charts. These are not geometry.


## Round 2 notes: Wisconsin, Illinois, Michigan, Oregon (fork report, 2026-09-23)

All downloads under `sources/expansion/round2/us/` (gitignored), retrieved 2026-09-23.

### Sources (URL -> local path, SHA-256)
| Source | Local | SHA-256 |
|---|---|---|
| https://wisconsindot.gov/dtsdManuals/strct/manuals/bridge/std-ch19.pdf (WisDOT BM Ch19 standard details, 27 pp) | wi_std-ch19.pdf | 7690db40f29143fcc135c5352022606f1fbd7e834b5d8d7ce9acbba8b00c613f |
| https://wisconsindot.gov/dtsdManuals/strct/manuals/bridge/ch19.pdf (WisDOT BM Ch19, Jan 2023) | wi_bm_ch19.pdf | cd99e94862a5189c5d7e9bf631c0e64600cd3fc3110c9adc4776e03bef8736d1 |
| https://idot.illinois.gov/content/dam/soi/en/web/idot/documents/doing-business/specialty-lists/highways/bridges/cell-libraries/bridge/beams-prestressed-deck-beams.pdf (IDOT cell library, PD cells 4/4/2025) | il_cell_beams-prestressed-deck-beams.pdf | 178fadf3285a73336f4c690cd1b4b68f0ad146d9bc6cc5bacfaac46ba6c5d822 |
| https://idot.illinois.gov/.../bm-design-guides/bm-3.5-lrfd-ppc-deck-beam-design.pdf (DG 3.5, May 2019) | il_dg35.pdf | 9f3c20e171774d5599402450079f4565f8f640a889b72ed69f22bc877654d013 |
| https://idot.illinois.gov/.../bm-design-guides/bm-3.4-lrfd-ppc-i-design.pdf (DG 3.4, Sept 2021) | il_dg34.pdf | f7882451865dd66a482ffd165059e61bc43790b002a80bca0fa310c4f17f14a3 |
| https://www.oregon.gov/odot/engineering/202601/br400s_all.pdf (ODOT BR400 series, eff. 2026-06-01..11-30) | or_br400s_all_202601.pdf | 5dc35c69833a40ed8e13b866535f7781f91e3bf68912bbdf53aa2fea5cd702a2 |
| https://www.oregon.gov/odot/engineering/202607/br400s_all.pdf (next edition, eff. 2026-12-01; identical properties) | or_br400s_all_202607.pdf | 6113d0f93fd595d8b4c1f84964607f574ad1f35a668c176922bbe190b3e9d2cf |
| https://www.oregon.gov/odot/engineering/202601/br300s_all.pdf (ODOT BR300 girders) | or_br300s_all_202601.pdf | 6476990177f23054db2b51610d895cb05187b76088fbbf69f0de696aa92f3314 |
| https://idot.illinois.gov/.../il-beams-ppcprestressing.xls (IDOT, 2016; not used - strand tables) | il_beams_ppcprestressing.xls | (not hashed; unused) |
| IDOT all_abd_memos.zip (current ABDs only; ABD 15.2 not included) | il_abd/ | (unused) |

### Wisconsin (implemented: 6 I-girders + 12 boxes)
Page locators (std-ch19.pdf): Std 19.01 28" details PDF p1 (props Std 19.02 p2); 36W 19.11 p3 / 19.12 p4;
45W 19.13 p5 / 19.14 p6; 54W 19.15 p7 / 19.16 p8; 72W 19.17 p9 / 19.18 p10; 82W 19.19 p11 / 19.20 p12;
boxes Std 19.50 (3'-0") p21, 19.51 (4'-0", shear key recess detail) p22. Box properties: BM Table 19.3-3, printed 19-46, PDF p46.

I-girder transcription (inches):
| Size | D | top W | top edge | top taper | web | bottom W | bottom edge | bottom taper | fillet | soffit bevel |
|---|---|---|---|---|---|---|---|---|---|---|
| 28 | 28 | 18 | 3 | 4 | 6 | 18 | 4 | 6 | none | 3/4 |
| 36W | 36 | 34 | 3 7/8 | 1 5/8 | 6 1/2 | 30 | 7 1/2 | 5 1/2 | R8 both | 3/4 |
| 45W | 45 | 34 | 3 7/8 | 1 5/8 | 6 1/2 | 30 | 7 1/2 | 5 1/2 | R8 | 3/4 |
| 54W/72W/82W | 54/72/82 | 48 | 3 | 2 1/2 | 6 1/2 | 30 | 7 1/2 | 5 1/2 | R8 | 3/4 |
Printed web heights (between taper/web intersections) 17 1/2, 26 1/2, 35 1/2, 53 1/2, 63 1/2 = D - 18 1/2. Fillet tangent callouts (4 5/8, 7 15/16, 7 1/16, 7 1/4, 10 13/16, 4 5/8) agree with the exact tangent construction to <=0.05 in.

Residuals (model - published): 36W A +1.07 in2, yb +0.02, I +0.10%; 45W A -0.43, yb **-0.121 (pinned)**, I +0.07%; 54W A -0.58, I -0.37%; 72W -0.58, -0.27%; 82W -0.58, -0.23%; 28" A -0.56 (bevel; bevel-free = 312 exactly), yb +0.02, **I -2.26% (pinned; printed 28,687 vs 28,040 drawn / 28,138 bevel-free)**. 36W vs 45W printed areas are mutually inconsistent by ~1.5 in2.

Boxes: 36/48 wide x 12/17/21/27/33/42 deep; 5 in webs, 5 1/2 slabs, void chamfers 1 1/2 (<=21 in) / 3 in (>=27 in), 3/4 soffit chamfers. **Estimate:** shear-key recess modelled 3/4 in deep from 4 in below top to 3 in above soffit, 45-degree transitions, 5 in web measured from the recessed face. Pinned systematic residual: A +3.1..+3.6 in2 (+0.42..0.73%), I +0.59..+1.04%, yb (from I/Sb) model 0.02..0.09 in higher. Alternatives tried (3/8 recess; web from full face) are worse / depth-dependent.

### Illinois (implemented: 12 deck beams)
IDOT cell library pages (PDF): 11x48 p4, 11x52 p7, 17x36 p10, 17x48 p13, 21x36 p16, 21x48 p19, 27x36 p22, 27x48 p25, 33x36 p28, 33x48 p31, 42x36 p34, 42x48 p37 ('SECTION B-B Showing dimensions').
Template: full width W; top band inset 5/8 each side; key inset 1 1/4 with 3/8 (upper) and 3/4 (lower) transitions; 1 1/2 soffit chamfers; void 2x2 chamfers; 5 1/2 slabs.
| Size | bands top/key/bottom | web | void WxH |
|---|---|---|---|
| 11x48, 11x52 | 3/4/4 | solid | - |
| 17x36 | 3/4.5/9.5 | 7 | 22x6 |
| 17x48 | 3/4.5/9.5 | 8 | 32x6 |
| 21x36 | 3/4.5/13.5 | 7 | 22x10 |
| 21x48 | 3/4.5/13.5 | 8 | 32x10 |
| 27x36 / 27x48 | 6/7/14 | 6 | 24x16 / 36x16 |
| 33x36 / 33x48 | 6/7/20 | 6 | 24x22 / 36x22 |
| 42x36 / 42x48 | 6/7/29 | 6 | 24x31 / 36x31 |
Validation: DG 3.5 example (27x36): A 569.9, I 49,697, Cb 13.30, Ct 13.71 -> model 569.92, 49,696.9, 13.295. Other rows unvalidated (BM Table 3.5.4-1 lives in the IDOT Bridge Manual on PowerDMS, JS-only).

### Oregon (implemented: 6 slabs + 4 boxes + 4 I-girders)
BR400 series (202601 edition): BR400 12" p1, BR405 15" p2, BR410 18" p3, BR415 21" p4, BR420 26" p5, BR422 30" p6, BR425 33" box p7, BR430 39" p8, BR435 42" p9, BR440 48" p10 (BR445 general notes p11). BR300: BR325 Type II p4, BR330 III p5, BR335 IV p6, BR340 V p7.
Slabs 48 wide: key = 3 in top band inset 3/8, 4 in key band (3/8 and 3/4 transitions) at 3/4 recess, square corners. Voids at mid-depth: 15": 3x8 @15; 18": 3x10 @14.5; 21": 12/10/12 @14; 26": 2x15 3/4 @ +-11; 30": 2x17 3/4 @ +-11. Boxes: 5 webs, 38 void, 5 1/2 slabs, 3x3 void chamfers, 6 in top band + 6 in key band. Residuals: slabs <=0.45 in2, <=0.002 in yb, <=0.022% I; boxes +0.20 in2, <=0.01 in, -0.055..+0.023% I.
I-girders (in): II 36: 12/18/6, stack 6,3,15,6,6; III 45: 16/22/7, 7,4.5,19,7.5,7; IV 54: 20/26/8, 8,6,23,9,8; V 63: 20/26/8, 8,6,32,9,8. Soffit chamfer "1 in max" modelled at 1 in (convention). No printed properties; analytic only (II A=368 = 369 - chamfers).

### Michigan - NOT implemented (blocked)
MDOT Bridge Design Guides / Michigan Design Manual on mdotjboss.state.mi.us return a Cloudflare challenge (curl) and HTTP 403 (WebFetch). Not bypassed. Leads: Bridge Design Guide 6.60.03 (MI 1800 girder), PC-4G "Prestressed concrete 1800 beam details", Michigan Design Manual Ch 7 (docGuid 3083d916-...), MSU theses d.lib.msu.edu/etd/49388 and 49214 mention the 70.9 in MI 1800 girder (secondary).

### Leads not implemented
- IDOT IL-beams IL27-IL90 (ABD 15.2/21.2 Fig. 1 dims; only IL72-2438 A=980, I=624,180, Cb=29.39 found in DG 3.4 p3.4-67). ABD 15.2 not in the current ABD zip; Bridge Manual on PowerDMS (JS-only); Scribd copy not used.
- IDOT deck beam properties for 11 other sizes (BM Table 3.5.4-1).
- ODOT BR360/365/375 BT36/BT45/BT60 deck bulb-tees: top flange width W is a project variable (60-102 in) and flange-edge details need more work.
- ODOT 202607 edition (effective 2026-12-01) - identical properties; switch source when it becomes current.
- WisDOT box: exact shear-key recess depth (would remove the systematic +0.5% A / +0.8% I).
- WisDOT 28" I: printed I = 28,687 vs 28,040 drawn - ask WisDOT which is correct.


## PA / NY / OH sub-slice notes (fork, 2026-09-23)

### Sources (all retrieved 2026-09-23; saved under sources/expansion/round2/us/)
| Source | URL | Local | SHA-256 |
|---|---|---|---|
| PennDOT BD-652M "Standard Prestressed Beam Sizes and Section Properties", sheets 1-3, recommended APR.29, 2016 (PDF mod 2025-01-28) — PRIMARY | https://docs.penndot.pa.gov/Public/Bureaus/Bridge/BD-Stds/BD652M.pdf | penndot_cur_BD652M.pdf | 65e8961429f0d08c8e71a526ad4d84e8cd166e7a3938bdf678875634a5d52e95 |
| PennDOT BC-775M adjacent box beam details, sheet 2 "Shear Key Detail", recommended NOV.23, 2022 | https://docs.penndot.pa.gov/Public/Bureaus/Bridge/BC-Stds/BC775M.pdf | penndot_BC775M.pdf | d9eeb34e8a4425997a0d0eb8afea98bd3488475c2b992bfef12ba3e53682d1fd |
| PennDOT BD-652M 2003 Ed. Change 6, DEC.29, 2008 (superseded; comparison only) | https://docs.penndot.pa.gov/Public/Bureaus/Bridge/BD-Stds/2003Ed/Change6/BD652M.pdf | penndot_BD652M.pdf | 73217534214998652e06eb4126f6f64b8d866d5233b4c62d0967c13fb7024551 |
| PennDOT BD-660M / BD-661M (deck/barrier over adjacent boxes; no outline data, used only to locate the key reference) | https://docs.penndot.pa.gov/Public/Bureaus/Bridge/BD-Stds/BD660M.pdf , .../BD661M.pdf | penndot_cur_BD660M.pdf, penndot_cur_BD661M.pdf | not used for geometry |
| NYSDOT BD-PC (USC) 2026 set, approved 2026-01-13, EB 26-004, lettings from 2026-05-01 | https://www.dot.ny.gov/main/business-center/engineering/cadd-info/bridge-details-sheets-repostitory-usc/BD-PC_01-26.pdf | nysdot_BD-PC_01-26.pdf | 3ea2cf78993dc01ae0993fc90042e84fad3551c64054d5f7829398bb28e864d5 |

(Stray 404 HTML bodies from failed guesses were deleted.)

### Page locators
- BD-652M (2016): PDF p1 = sheet 1 (adjacent box, plank, spread box sketches + tables, notes); p2 = sheet 2 (PA I-beams, AASHTO I-beams); p3 = sheet 3 (PA bulb-tee, 54 rows).
- BC-775M: PDF p2, "SHEAR KEY DETAIL" (lower right).
- NYSDOT BD-PC: p1 BD-PC1 (36 in units), p2 BD-PC2 (48 in units), p14 BD-PC14 (PCEF + AASHTO I), p15 BD-PC15 (NEBT), p31 BD-PC31 (NEXT D), p36 BD-PC36 (NEXT F).

### Implemented (140 PA + 36 NY = 176 profiles exposed)

After the coordinator instruction of 2026-09-23, NyNebtSection (6) and NyNextBeamSection (16) were removed from the module as duplicates of the PCI Northeast family. Their transcriptions and residuals remain in `state_ny_bd_pc.json` and are kept below for reference.

| Class (module) | SIZES | Provenance | Residuals vs published |
|---|---|---|---|
| PaIBeamSection (state_pa_beams) | 21 (18/30 ... 26/63) | transcribed-with-convention | A exact, yb <=0.008 in, I <=0.004% |
| PaAashtoIBeamSection | 7 (28/63 ... 28/96) | transcribed-with-convention | exact to print |
| PaBulbTeeSection | 54 (33/29 ... 33/95.5; 36/42/48 in flanges x T1 7/9 in) | transcribed-with-convention | A <=0.04%, yb <=0.005, I <=0.001% |
| PaBoxBeamSection | 58 (adjacent 48/36 x 17-66 = 28; spread 28; plank 48/36 x 12 = 2) | transcribed-with-convention | spread exact; adjacent >=33 in: A <=0.03%, I <=0.1%; adjacent 17-30: A -0.76..-1.11% (pinned); planks A 0.1%, I 0.03% |
| NyBoxBeamSection (state_ny_beams) | 22 (B36/B48 x 24-54) | transcribed | B36 A exact (0.01%); B48 A +0.44..+0.88% (pinned); I -0.40..+0.92% (pinned, source column not smooth) |
| NySlabUnitSection | 8 (S36/S48 x 12/15/18/21) | transcribed | 12/18 in exact; S36x21 -0.27% A; S*x15 pinned; S48x21 +5.4% (pinned) |
| NyPcefBulbTeeSection | 6 (PCEF-39 ... 79) | transcribed-with-convention | exact (A +0.25 in2 rounding); PCEF-63 I pinned (digit transposition) |
| NyNebtSection | 6 (NEBT-39 ... 79) | fitted-reconstruction | A +0.14..0.26%, yb +0.05..0.09 in, I +0.07..0.18% |
| NyNextBeamSection | 16 (NEXT 28-40 D at 96/120 in; NEXT 24-36 F at 95.5/143.5 in) | transcribed-with-convention | D: A -0.04%, I <=0.003%; F: A +0.11..0.17%, I +0.10..0.15% |

### Transcription (inches)
PennDOT PA I-beam: columns W2 W1 D T2 B3 C B1 T1 B4 B2 W3; outline (W1/2,0)-(W1/2,T1)-(W3/2,T1+B1)-(W3/2,T1+B1+C)-(W2/2,D-T2)-(W2/2,D). Full rows in src/bridgebeams/us/data/state_pa_bd652m.json (pa_i_beam).
PennDOT AASHTO I: W2 42, W1 28, T2 5, D1 3, B3 4, B1 10, T1 8, X1 13, B4 4, B2 10, W3 8; C = D-30 (33,36,42,48,54,60,66).
PA bulb-tee: W1 33, W3 8, T2 4.5, B3 2, D2 3.5, B1 3, B4 2, B2 9, X2 3.5; (W2, D1, X1) = (36,1,12), (42,1.25,15), (48,1.5,18); T1 = 9 or 7; C = 8..72 step 8; D = T2+D1+B3+C+D2+B1+T1.
PA boxes: webs 5, top slab 3, bottom slab 5.5, void corner 45-deg fillets 1.5x1.5 (D<=21) / 3x3 (D>21); ¾ chamfers (note 5) omitted.
BC-775M key (per face, from top): 3/8 recess to 3 in (12 in beams) or 6 in (others); 3/8-rise taper to 3/4 recess; 3/4-rise taper back to full face at 7 in (12 in) or 12 in (others) below top. Label "FOR 12\" BEAM DEPTHS" attached to the 3"/4" pair. Top joint 1¼ in, lower joint ½ in (consistent with 3/8 upper recess).
NYSDOT box/slab key (BD-PC1 "shear key recess detail"): bottom 4 in full width + ¾ soffit chamfer; ¾x¾ taper to ¾ recess; 3/8x3/8 taper to top 4 in band inset 3/8. Box: webs 5 from recessed face, slabs 5½/5½, void chamfer 3. Slab voids: 36 in ±7½ centres, dia 8/10/12; 48 in at 0, ±14 (1'-2"), dia 8/10/(12,10,12).
PCEF: top 47, bottom 32, web 7; top tip 4, 1½ drop over 18 in, 2x2 chamfer; bottom edge 9, 3 in rise over 9 in, 3½x3½ chamfer; web = D-23 (16 in for PCEF-39, 4'-8" for PCEF-79).
NEBT: top 47¼, bottom 31⅞, web 7⅛; R 7⅞ web fillets, R 4 bulb corner, R ⅞ flange tip, ¾ chamfer; 20⅛ / 12⅜ runs; used tip 3⅜ + 2 in drop (see below), bottom edge 8⅝, taper rise 3⅞.
NEXT: stems 5'-0" c/c, 1'-3" wide at flange soffit, slope 0.375:12, C = 13/13.25/13.5/13.75, R=4, ¾ stem chamfers; D flange 9 (key-way 1 full + ¾ chamfers + 5½ recess ¾ deep); F flange 4 with ¼ draft.

### Conventions / estimates
1. PA: ¾ chamfers omitted everywhere (PennDOT tables reproduced exactly only without them).
2. PA adjacent boxes/planks: interior unit (keys on both faces), key per BC-775M.
3. NY PCEF: ¾ soffit chamfers omitted (table exact without them); NY boxes/slabs/NEXT keep drawn chamfers (tables match with them).
4. NEBT (fitted-reconstruction): labels read as tip 3⅜ in + 2 in drop to the web intersection (5⅜ total). The drawn arrow placement suggests tip 2 in + 1⅜ drop, but that closes neither the overall depth (stack 3⅜ + web + 3⅞ + 8⅝ is 2 in short) nor the area (-29 in2); the chosen reading closes the depth and fits all six tables.
5. NEXT: minimum flange (no grinding allowance), fascia drip groove omitted.

### Pinned discrepancies
- PA BD-652M adjacent 17-30 in: properties computed with the 3/4 (plank) key; BC-775M says 6/6 for non-12 in beams; implementation follows BC-775M (area -0.76..-1.11%). tests: test_pinned_adjacent_17_to_30_table_uses_plank_key.
- PA 2008 edition 24/63 row: properties correspond to T2=6/C=32, not the printed T2=9/C=29; 2016 edition corrected (920 in2, 30.90) — 2016 used.
- NY yb column = D/2 for every box/slab (not true centroid).
- NY box I column non-smooth (third differences swing -4400..+2500 in4 vs constant 135 in model); B48 areas 0.4-0.9% below drawn webs.
- NY S48x21: table = three 12 in voids, drawing labels middle 10 in (drawing followed).
- NY S36x15 / S48x15 table areas 0.9 / 2.9 in2 above drawn 8 in voids.
- NY PCEF-63 I printed 500945 = transposition of 500495.

### Leads not implemented
- NYSDOT BD-PC14 AASHTO Type I-VI table (PCI national family; already in AashtoIBeamSection) — skipped.
- NYSDOT NEXT D/F intermediate flange widths (range allowed; only tabulated widths implemented).
- NYSDOT BD-PC22-27 (other girder/segment sheets) not reviewed in detail.
- Ohio ODOT: www.dot.state.oh.us Standard Bridge Drawings page says MOVED to transportation.ohio.gov/working/engineering/structural/design/02-active-drawings, which returns 404; guessed PSBD PDF paths 404; ftp.dot.state.oh.us/pub/Structures lists nothing. WebSearch budget exhausted (session limit 200). Blocked; record as lead.
- PennDOT BD-652M has no drawn outline for dapped ends (note 4); not relevant to gross section.
