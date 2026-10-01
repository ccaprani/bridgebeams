# Civilcon T, U, Special U and M beams: extraction record (September 2026)

Scope: the four remaining one-page Civilcon (South Africa) producer sheets,
PPBT, PPBU, PPBUS and PPBM. Machine-readable companion:
[extraction-civilcon-tum-2026-09.json](data/extraction-civilcon-tum-2026-09.json).
Per-size data and residuals are in `src/bridgebeams/za/data/civilcon_{t,u,special_u,m}_beams.json`.

Status: producer catalogue sheets (no date or revision printed). Each is a
single-page PDF, so every locator is PDF page 1; there is no printed page number.
Each page was rendered at 300 dpi and read visually. Unprinted features were
scaled from line centres. The scale was calibrated on the printed overall width
(and, for U/M/SU, cross-checked against the printed depth or strand-row levels).

| Sheet | Title (original) | URL | Local file | SHA-256 (first 16) |
|---|---|---|---|---|
| PPBT | T BEAM | https://civilcon-za.co.za/wp-content/uploads/2017/05/PPBT.pdf | sources/expansion/asia-africa/civilcon-T.pdf | 76748c16a8296cb2 |
| PPBU | U BEAM | https://civilcon-za.co.za/wp-content/uploads/2017/05/PPBU.pdf | sources/expansion/asia-africa/civilcon-U.pdf | 6033d5d21b764f77 |
| PPBUS | SPECIAL U BEAM | https://civilcon-za.co.za/wp-content/uploads/2017/05/PPBUS.pdf | sources/expansion/asia-africa/civilcon-US.pdf | d7a4d8e53c8c2bf3 |
| PPBM | M BEAM | https://civilcon-za.co.za/wp-content/uploads/2017/05/PPBM.pdf | sources/expansion/asia-africa/civilcon-M.pdf | 0c6d2b0234fc3e7f |

## Summary

| Class | Sizes | Provenance | Max residual vs published (excluding pinned) |
|---|---|---|---|
| `za.CivilconTBeamSection` | T1–T10 | transcribed-with-convention | A exact; Yb 0.42 mm; Z 0.43% |
| `za.CivilconUBeamSection` | U1, U3, U5, U7–U12 | fitted-reconstruction | A 0.11%; Yb 0.22 mm; Zt 0.06%; Zb 0.04% |
| `za.CivilconSpecialUBeamSection` | SU1, SU2 | fitted-reconstruction | A 0.010%; Yb 0.39 mm; Z 0.018% |
| `za.CivilconMBeamSection` | M2–M10 | fitted-reconstruction | A exact (1 mm²); Yb 0.40 mm; Zt 0.08%; Zb 0.12% |

Pinned source discrepancies: T10 Zb (+0.732%); U10 Zb (printed 255.65e6, outline 225.73e6); M8 Zt (−1.188%; the table is internally inconsistent by 1.16%). Also recorded: M4 area printed 37860 (378600 closes exactly), M10 table depth 360 (drawing and Zt give 1360), and T10 drawing label 850 (815 used).

## T beam (PPBT): transcription

Printed: base 495; bottom chamfers 25 × 25; 6 mm side inset over the 75 mm flange edge; 40 mm flange-top taper; 50 mm splay to the 105 mm web; clear web 240 (T3–T10); 50 mm splay to the 205 mm bulb; bulb `335 max`. Right chain: 25 / 75 / 40 / 50 / 240 / 50 / 335 max. Depth labels: T1 380, T2 420, T3 535 … T9 775 (40 mm pitch), and **T10 850**.

T1/T2 are dashed. The web ends 90 mm above the lower splay (y = 280), a 50 mm splay rises to the 205 bulb (the `50` callout is the horizontal offset from the web face to the dashed bulb face), and the `90` above it reaches the T2 top (420).

Half profile from the soffit: (222.5,0) (247.5,25) (241.5,100) (102.5,140) (52.5,190) (52.5,w) (102.5,w+50) (102.5,D), with w = 430 (T3–T10) or 280 (T1/T2).

- **Derived:** the 205 mm width at the taper/splay junction is not printed. It closes all ten published areas exactly and matches the drawing, where the break aligns with the dashed T1/T2 bulb face.
- **T10 depth:** 815 is used. The table, `335 max` + 480, the 40 mm label pitch and exact area closure all support it. At 850 the area would be 178735 mm² (+4.2%).
- **T10 Zb:** the outline that reproduces A exactly and Yb within 0.34 mm gives Zb 34.73e6 against the printed 34.48e6 (+0.732%). This is pinned in the tests.

## U beam (PPBU): fitted reconstruction

The section drawn is U12 (1600). The right-hand elevation shows the shallower marks. There, the entire top block (shoulders, raised strip, lip and 380 mm inner thickening) moves down the 6.75:1 outer face. Each mark is therefore U12 with the top block translated along the outer face.

Printed and used: base 970; 35 × 35 chamfers (elevation detail); outer batter 6,75:1; web 165 normal to the parallel faces; top 50 (outer shoulder, 30 below top) + 250 (raised strip) + 40 (inner shoulder, 33 below top) with a 15 mm vertical inner lip; thickening 380 from the inner shoulder to the web-face break; floor half-widths 240 + 129. The left top chain 100/90/45 locates strands (4*), not concrete.

Checked by scaling (0.66804 px/mm): the outer faces pass through ±485 at y = 0, so 970 is the theoretical soffit intersection. The top face is at 1601 mm, and the strip, shoulders, lip and 380 break all agree with the model within 1 mm.

**Not printed:** the floor valley and break heights. The web toe is placed at the printed 369 mm half-width on the inner web face, which gives y = 342.9. The valley and break heights are fitted by least squares to all nine A, Yb and Ixx values: **valley 129.4, break 218.3**. The drawing scales to about 153 and 204, and the toe to about (371.2, 357.8); the printed `129` scales to about 131. With the drawing's floor the areas run from +0.18% to −0.06%. With the fitted floor the largest area residual is 0.11%. Treat the floor as a reconstruction.

Web-width note: published area steps are exactly 33523 mm² per 100 mm, which implies a 167.6 mm horizontal web width. The printed 165 normal at 6.75:1 gives 166.80. The printed values are kept, which produces the +0.10% (U1) to −0.11% (U12) area trend. Freeing the web width does not produce round-number geometry.

Pinned: the printed U10 Zb 255.65e6 is inconsistent with its own Zt/Yb. The outline gives 225.73e6, which suggests a transposed digit in 225.65. Recorded only: U5 self weight 13.76 kN/m against 13.60 from A × 25 kN/m³. The table has no U2/U4/U6.

## Special U (PPBUS): fitted reconstruction

The catalogue index says US1/US2; the sheet and table say SU1/SU2, and the sheet names are used. SU2 (1200) is drawn solid. SU1 (900) is drawn as a dashed lobe 300 mm lower on the same webs.

Printed: base 2000 (no soffit chamfer drawn); lobe 175 + 175, inner edge 850 from the centreline; lobe stack 50 + 150 + 100; 75 outer splay offset; 125 inner splay length (the 75/100/125 triangle); 75 mm shoulder; web horizontal chain 60 + 80 + 60 = 200; SU1 lobe inner edge 810. Density is 25.5 kN/m³, and the self-weight header's kN/m³ is really kN/m.

Derived: the neck spans x = 925…1125 at y = D − 300, so the parallel web faces have a 1 : 7.2 batter from 800/1000 at the soffit (scaled 1 : 7.23). The published area step of exactly 120000 = 2 × 200 × 300 confirms the 200 mm web.

**Not printed; scaled then confirmed:** the floor top is at 200 (scaled 199.7). The floor splay is 45° from x = 700 (scaled line x = y + 499.5) to the web, meeting it at (848.4, 348.4). Both rows agree within 0.010% on A, 0.39 mm on Yb and 0.018% on Z. A ±1 mm floor change moves A by about 0.2%, so the floor thickness is well constrained, but the splay size is weakly constrained. The provenance is fitted-reconstruction rather than estimate because the two property rows independently confirm these values.

Discrepancy: sliding the lobe 300 mm down the 1:7.2 web puts the SU1 inner edge at 808.3, against the printed 810. The 1.7 mm difference is recorded and not forced.

## M beam (PPBM): fitted reconstruction

Printed: base 970; 35 chamfer; 125 flange edge; 50 taper; 80 splay; lower web heights 200 (M2–M4), 440 (M5–M7) and 680 (M8–M10) above the 290 mm web start. The depth labels run to M10 1360. The table prints M10 as 360 and the M4 area as 37860.

Derived exactly from the published areas: **web 160**, from the group change 240·(w − 400) + 32000 = −25600. **Top flange 400**, from +32000 per 80 mm within a group. Scaling agrees (160.0 and 400.8).

Scaled (1.05052 px/mm): top notch **50 × 50** each side (300 raised strip); taper break half-width 160, giving a 45° 80 × 80 splay; drawn flare 120 × 80; drawn edge inset 10 over 125.

**Conflict:** the drawn outline is 1525 mm² short on every row (0.34–0.49%), and its Zt is up to 1.6% low. A least-squares fit of flare height and edge inset gives 59.93 and 15.10. The round values **flare 120 × 60 and inset 15** reproduce all eight usable published areas exactly. They also give Yb within 0.40 mm and Z within 0.12% (except M8 Zt). A free four-parameter fit returns notch 49.45, flare 60.8, break 162.3 and inset 16.4. These fitted values are implemented as the best estimate of the geometry behind the published properties, and the drawn values are recorded in JSON. Colin Caprani's 2026-09-22 reading of a notch of about 40 × 50 is not supported by the scaled drawing or by the properties. The UK M-beam equivalence remains unverified; no alias is provided.

Pinned: the M8 published Zt is internally inconsistent: Zt·(D − Yb) exceeds Zb·Yb by 1.16%. The calculated Zt is 1.188% below the printed value.

## Remaining uncertainties

- U floor levels and the M flare/inset are property-fitted and conflict with the drawing by 10–24 mm and 20/5 mm respectively. Producer CAD would resolve both.
- The U web width (167.6 implied versus 166.8 printed) is unresolved.
- None of the sheets carries a date or revision, so current production status is unverified.
- Strand patterns, diaphragms (SU) and the T strand note are not modelled.
