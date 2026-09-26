# United States state standards follow-up

Reviewed 22 September 2026. This inventory records **ten states** with primary
DOT source collections in addition to the Washington State sheets already in
the regional catalogue. One Ohio lead currently returns 404 and is separately
marked blocked. US state rows do **not** increase the number of countries on the
global map. Named AASHTO types in different states are not assumed to share an
identical outline.

The machine-readable [source inventory](data/us-states-followup.json) records
the document identifier, revision evidence, section family, transcription
readiness and missing geometry for each state.

| State | Primary source and edition | Geometry available | Result |
| --- | --- | --- | --- |
| California | [Caltrans xs1-121-1 bulb-tee](https://dot.ca.gov/-/media/dot-media/programs/engineering/documents/bridgestandarddetails/chap-1/202007-xs1-121-1-a11y/xs1-121-1-a11y.pdf), approved October 2025 | Typical bulb-tee dimensions; project chooses depth `D` | Source verified; profile pending companion details and chosen depth. |
| Florida | [FDOT 450-036](https://fdotwww.blob.core.windows.net/sitefinity/docs/default-source/design/standardplans/2027/idx/450-036.pdf?sfvrsn=797b8c54_1), FY 2026-27; sheet 1 revised 2019 | FIB36 full width/depth and radius leader | Rounded transition needs reconstruction and property validation. [Current index](https://www.fdot.gov/design/standardplans/current) lists FIB36 through FIB96 plus U beams. |
| Iowa | [Iowa DOT beam standards](https://iowadot.gov/consultants-contractors/bridges-structures/bridge-culvert-standards/bridge-standards), index updated 9 September 2026 | A/B/C/D and bulb-tee C/D/E sheets; 4700 revised April 2026 | Index verified; its current PDF download endpoint was blocked by the fetcher. |
| Minnesota | [MnDOT Section 5 Figure 5.4.6.1](https://www.dot.state.mn.us/bridge/pdf/lrfdmanual/section05.pdf), February 2019, printed 5-37 / PDF page 37 | 14RB, 18RB, 22RB: 26 in wide, 14/18/22 in deep, with gross properties | **Three profiles implemented** in `bridgebeams.us`, source snapshot 2019. |
| Missouri | [MoDOT EPG 751.22](https://epg.modot.org/index.php/751.22_Prestressed_Concrete_I_Girders), live guide | Type 2/3/4/6 I, Type 7/8 bulb-tee and six NU designations; [PDF drawing index](https://www.modot.org/bridge-standard-drawings) | Family confirmed; no outline transcribed. |
| Nebraska | [NDOT Bridge Design Manual](https://dot.nebraska.gov/media/4dapkdwu/2026-02-23_ndot-bdm-ch-1-3-5-6-7-8-9-10-13-app-c.pdf), 23 February 2026, printed 5-16 | Figure 5.4 NU shape and Table 5.7 properties for NU35/43/53/63/70/78 | Strong next implementation target; trace curved transitions. The designation is not the exact height in inches. |
| New York | [NYSDOT BD-PC1/2 2026 set](https://www.dot.ny.gov/main/business-center/engineering/cadd-info/bridge-details-sheets-repostitory-usc/BD-PC_01-26.pdf), effective 1 May 2026 | 36/48 in slab and box sections, keys, voids and property tables | Source verified; detailed void/key polygons pending. The old BD-PS1E individual PDF currently redirects to 404. |
| Pennsylvania | [PennDOT BD-652M](https://docs.penndot.pa.gov/Public/Bureaus/Bridge/BD-Stds/2003Ed/Change6/BD652M.pdf), December 2008, sheet 3 | PA bulb-tee dimensions and 36 published property rows | Historical snapshot; resolve lower corner and anomalous row before implementation. |
| Texas | [TxDOT IGD-23](https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/IG-IGD-23.pdf), revised March 2023 | Tx28/34/40/46/54/62/70 dimensions and property table | Source verified; perimeter tracing pending. [Current drawing index](https://www.dot.state.tx.us/insdtdot/orgchart/cmd/cserve/standard/bridge-e.htm) also lists slab/box/X beams. |
| Wisconsin | [WisDOT Chapter 19 standards](https://wisconsindot.gov/Pages/doing-bus/eng-consultants/cnslt-rsrces/strct/bridge-manual-standards.aspx), sheet revisions through July 2026 | 28 and 36W/45W/54W/72W/82W dimension and design-data sheets | Family confirmed; pair each drawing and property sheet. |

The Minnesota implementation uses source dimensions directly:
`x = ±13 × 25.4 mm`; `y = 0` at the soffit and `y = 14/18/22 × 25.4 mm` at
the top. Its four vertices make a solid rectangular gross section. The tests
check the independent printed areas (364, 468, 572 in²), centroid heights
(7, 9, 11 in), inertias (5945, 12640, 23070 in⁴) and bottom moduli (849,
1404, 2097 in³). The 18RB inertia is 12,636 in⁴ by exact rectangle
integration but printed 12,640; that difference is source rounding, not
extra concrete. The 22RB calculation is 23,070.67 in⁴. No strands, deck,
stool, reinforcement or end blocks are part of these profiles.

[MnDOT's manual index](https://www.dot.state.mn.us/bridge/lrfd.html) lists an
October 2025 revision of Section 5. Its document server rejected automated
access here, so these three implemented profiles remain explicitly tied to the
accessible February 2019 edition until the 2025 Figure 5.4.6.1 is checked.
The [Ohio PBSD-1-25 lead](https://ftp.dot.state.oh.us/pub/construction/ODOT%20JAN%202026%20SPEC%20UPDATE/Standard%20Drawings%20and%20Plan%20Insert%20Sheets/Bridge%20Standard%20SCDs/SBD%20%26%20DDS%20Revised%20Drawings_01-16-26.pdf)
was search-indexed but returns 404 and has not been counted.
