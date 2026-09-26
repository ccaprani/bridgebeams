# Round 3: Oregon deck bulb-tees and Ohio I-beams (2026-09)

Owner-supplied sources (manual downloads) plus previously retrieved Oregon
BR300 set and Brice et al. (2021) appendix. Status: 12 Oregon DKBT profiles
(`transcribed-with-convention`) and 13 Ohio I-beam profiles (`transcribed`)
implemented. Disclaimer applies: useful, not authoritative.

## Sources

| Source | Local path | SHA-256 | Locator |
|---|---|---|---|
| Oregon Standard Drawings 2024, BR300 series (eff. 2026-06-01), https://www.oregon.gov/odot/engineering/202601/br300s_all.pdf | sources/expansion/round2/us/or_br300s_all_202601.pdf | 6476990177f23054db2b51610d895cb05187b76088fbbf69f0de696aa92f3314 | BR360 p9, BR365 p10, BR375 p11 |
| Oregon Standard Drawings 2021, BR360 36" Deck Bulb-T (eff. 2023-06-01..11-30), URL not recorded (unverified) | sources/expansion/round2/manual/us/or/BR360.pdf | a001514fc6b973200a4b3cee59900768a432c3686b8903ca172bcc8cf9fd1323 | p1 |
| Oregon Standard Drawings 2021, BR375 60" Deck Bulb-T (eff. 2023-06-01..11-30), URL not recorded (unverified) | sources/expansion/round2/manual/us/or/BR375.pdf | e59f96cf34f05764d01dee0d44c235c65361e68c9fe67446f16336a7c9dec4bf | p1 |
| ODOT (Ohio) Bridge Design Manual, 2020 Ed., Jan 2026, URL not recorded (unverified) | sources/expansion/round2/manual/us/oh/ODOT-BDM-2026-01.pdf | b49c470018b14eda432649532b2a9335cf736dfe2c22c2def52bf138fd85f074 | §308.2.3.4 PDF p235 (printed 3-173); Fig. 308-6 p236; §308.2.3.3 box beams p227-228 |
| ODOT (Ohio) Standard Bridge Drawing PSID-1-13 "Prestressed Concrete I-Beam Bridge Details", 10 sheets, dated 01-18-2013 rev. 07-20-2018, MicroStation V8 DGN; index cited by Brice 2021: http://www.dot.state.oh.us/Divisions/Engineering/Structures/standard/Bridges/Pages/StandardBridgeDrawings.aspx (file URL unverified) | sources/expansion/round2/manual/us/oh/PSID-1-13_2018-07-20.dgn | 358ee65f7159c078e7bffcb8df31404dbfe85f374f98fd597e1693d715fd1603 | sheet 1 (Types II-IV, Mod IV + property table), sheets 2-3 (WF + property table) |
| Brice et al. (2021) PCI Journal appendix | sources/expansion/round2/us/pcij-2021-mj-brice-appendix.pdf | (registry) | Table A.10 Ohio, Table A.11 Oregon |

The 2021 BR360/BR375 sheets and the 2024 BR360/BR365/BR375 sheets show
identical section dimensions (checked visually on 300 dpi renders).

## Oregon DKBT36/45/60 (`us/state_r3_or_deck_bulb_tee.py`)

END VIEW right-hand dimension chain (inches, bottom up) and MIDSPAN SECTION:

| Item | DKBT36 | DKBT45 | DKBT60 |
|---|---|---|---|
| Bulb edge (2'-0" wide) | 6 | 6 | 6 |
| Bulb taper (9 in run to web) | 3 | 3 | 3 |
| Web straight (6 in web) | 1'-3" | 2'-0" | 3'-3" |
| Fillet (3 in run) | 2 | 2 | 2 |
| Flange taper (1'-6" run) | 4 | 4 | 4 |
| Flange edge (min.) | 6 | 6 | 6 |
| Total | 3'-0" | 3'-9" | 5'-0" |

Top flange width W is project-specific; the sheets' deck-reinforcement table
spans W = 60-72, 72-84, 84-102 in. SIZES `DKBT{36,45,60}-W{60,72,84,102}`
(min, breakpoints, max); `flange_width=` accepts any W in [60, 102].
Pixel measurement on BR360 (12.47 px/in) confirms the chain heights to 0.1 in
and the flange underside slope position (e.g. x = 13.9 in at y = 27.75 in).

Conventions: 1 in soffit chamfer ("1 in max."); flat top (0.02 slope/tilt
ignored); square flange tips (interior-flange edge connection/key and the
3/4 in exterior drip groove omitted, undimensioned). No properties are
printed; Brice Table A.11 Oregon BT48-BT96/BI51-75 rows are the non-deck
BT/BI girders, not the DKBT (not applicable). Tests: dimensions and a
hand-summed area (e.g. DKBT36-W60 A = 776.0 in2).

## Ohio PSID-1-13 I-beams (`us/state_r3_oh_i_beams.py`)

The BDM prints no geometry; §308.2.3.4 permits AASHTO Types II-IV, modified
Type IV and WF36-49..WF72-49 "as shown in PSID-1-13". The DGN is V8 (OLE
compound, MicroStation 08.11). No V8 reader was available (no GDAL/ogr2ogr,
ODA, dgnlib); GDAL's DGN driver reads V7 only. Decoded with a small parser
(`docs/research/data/round3-oregon-ohio-dgn-extract.py`): zlib-inflated
`Dgn^G` streams; record length 4 + 2 x words-to-follow (u32 at +8); level at
+0x10; line/line-string vertices as doubles at +0x6C / +0x74. Concrete
outlines are the weight-2 lines (sheet 1) and level-7 lines (WF sheets);
polygonised with shapely. Scale 1250 UOR/in, fixed by all depths/widths.
All vertices land on 1/16 in (residual < 0.0005 in); all symmetric.

Right-half vertices (in), after (0,0):

| Size | vertices |
|---|---|
| II | (8.25,0) (9,0.75) (9,6) (3,12) (3,27) (6,30) (6,36) |
| III | (10.25,0) (11,0.75) (11,7) (3.5,14.5) (3.5,33.5) (8,38) (8,45) |
| IV | (12.25,0) (13,0.75) (13,8) (4,17) (4,40) (10,46) (10,54) |
| MOD-IV-60/66/72 | (12.25,0) (13,0.75) (13,8) (4,17) (4,D-9) (7,D-6) (b,D-4) (b,D); b = 18/18/24 |
| WF36-49..WF72-49 | (19.25,0) (20,0.75) (20,5.5) (6,12.5) (4,14.5) (4,D-11) (7,D-8) (24.5,D-5) (24.5,D) |

Validation: Brice 2021 Table A.10 (WF36-49..WF72-49, Mod IV 60/66/72) is
reproduced to every printed digit for A, yb, Ix and Iy. PSID-1-13 printed
tables:

- Types II, III, IV and Mod IV 60/66: printed A/yb/I are those of the section
  **without** the 3/4 in soffit chamfers (squared-off: dA <= 0.5 in2 rounding,
  dyb <= 0.004 in, dI <= 0.001 %). With chamfers the model is 0.56 in2 and
  0.11-0.27 % I below print. Pinned in tests.
- Mod IV 72: printed values match the chamfered outline exactly (I 684,726).
- WF: printed A is 0.4 in2 above the outline for every depth, I 0.036-0.040 %
  above, yb within 0.05 in (printed to 0.1). Brice agrees with the outline.
  Pinned in tests; cause unknown (perhaps a different chamfer treatment).

Not modelled: top-flange clipping (max 6 in), shipping holes, end blocks,
the "HYBRID I-BEAM (36"-72")" end-diaphragm dimension table (DIM. A-E).

## Leads not implemented

- Ohio box beams: BDM §308.2.3.3 defers geometry to PSBD-1-25 (48 in wide)
  and PSBDD-3 (36 in wide design data); neither in hand.
- Oregon non-deck BT48-BT96 / BI51-BI75 (Brice Table A.11, source ODOT
  "Details-Bridge" 2019): properties known, no dimensioned drawing in hand.
