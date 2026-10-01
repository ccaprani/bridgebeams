# Round 2, Africa and the Middle East: sources, extractions and leads

Recorded on 23 September 2026. The structured record is
[data/round2-africa-middle-east-2026-09.json](data/round2-africa-middle-east-2026-09.json).
Downloads are saved under `sources/expansion/round2/<cc>/`. That directory is
gitignored and nothing in it was committed.

This round implemented **24 profiles**:

| Package / class | Profiles | Provenance | Source status |
|---|---:|---|---|
| `qa.r2_ty_beams.QaTyBeamSection` | TY1–TY10 | transcribed | Current Ashghal standard detail SD 5-1-111 Rev 1 (October 2013) |
| `qa.r2_ty_beams.QaTyeBeamSection` | TYE1–TYE10 | transcribed | Current Ashghal standard detail SD 5-1-112 Rev 1 (October 2013) |
| `ma.SadetIBeamSection` (new `ma` package) | I40, I45, I50, I55 | estimate | Producer brochure with a schematic graphic |

## Qatar: Ashghal TY and TYE

Round 1 recorded that the TY and TYE sheets redirected to an Ashghal sign-in page.
On 23 September 2026 both sheets were public again and downloaded directly:

- [SD 5-1-111 Rev 1 TY - Beams](https://www.ashghal.gov.qa/en/SDDDocumentsLibrary/SD%205-1-111%20Rev%201%20TY%20-%20Beams.pdf).
  Local file `round2/qa/sd-5-1-111.pdf`, SHA-256
  `2ffa5e85015932561188f207e23920ddd3159960da878ee83d94a8992d3d662a`.
- [SD 5-1-112 Rev 1 TYE - Beams](https://www.ashghal.gov.qa/en/SDDDocumentsLibrary/SD%205-1-112%20Rev%201%20TYE%20-%20Beams.pdf).
  Local file `round2/qa/sd-5-1-112.pdf`, SHA-256
  `12ee6ccfa2a0b9cd65ed42c740a343703ef83ee96f633f11e0af31432de16c5c`.

Each is a one-page AutoCAD sheet (PDF page 1, sheet 1 of 1) in QCS Section 5, Part 1.
Both are dated October 2013 and carry Rev 1 of 23/10/2013. The dimension text uses
stroke fonts, so it is absent from the text layer. It was read visually from 400 dpi
renders. The property tables are present in the text layer and were cross-checked
against the renders.

### TY section (SD 5-1-111, "TY BEAM SECTION", scale 1:10)

All dimensions are in mm, measured upwards from the soffit.

| Item | Value |
|---|---|
| Base width | 750 |
| Bottom chamfers | 25 × 25 |
| Flange edge | 110 high; the face is inset 5 over its height |
| Sloping flange top | 105 high, with a 227.5 horizontal run from the edge |
| Splay | 80 high over a 50 horizontal run, meeting the web at y = 320 |
| Web width at y = 320 | 185 |
| Web taper | Linear, up to 400 wide at 850 (TY10) |
| Depth ladder | TY1…TY10 = 400…850 in 50 mm steps |
| Printed web widths at the ladder levels | 217, 238, 258, 278, 299, 319, 339, 359, 380, 400 |

### Implementation and checks

One mould outline is used. Shallower members are truncations of the TY10 outline,
as the section drawing shows, and the exact linear taper is used. The printed widths
agree with the taper within 0.5 mm.

The table header prints I as "×10¹⁰ mm⁴", but the values are actually **×10⁸ mm⁴**.
This was checked in two ways: I/yb and I/(D−yb) reproduce the printed Zb and Zt.

Against the published values, the implemented TY1–TY10 sections give:

- area within +0.013% to +0.065%
- yb within 0.5 mm
- Ixx within 0.05%
- Zt and Zb within 0.35%, because the printed yb is rounded to the nearest mm

### TYE section (SD 5-1-112)

TYE is the TY right half joined to a vertical outer face at x = −375:

- Only the soffit corner of that face carries the 25 mm chamfer.
- The top corner of that face is square as drawn.
- The top width is 575 at TYE10.
- The printed widths from the vertical face are 484…575.

**Pinned discrepancy.** The implemented areas are 0.127–0.157% below the table, and
Ixx is 0.13–0.15% below. The shortfall runs from −310 mm² at TYE1 to −756 mm² at
TYE10. The constant part is close to the 312.5 mm² left chamfer, so the table may
omit that chamfer. The depth-proportional part (≈1 mm²/mm) is unexplained. This is
not fitted. The TY rows on the companion sheet close within 0.07%, so the geometry
reading is not in doubt. The table's extra column, "Xc from vertical face", agrees
within 1 mm.

### Relation to the UK/Irish TY family

The outline is the same form as the UK/Irish TY family, but it was implemented from
the Ashghal sheet's own dimensions and tables. The Ashghal areas differ slightly from
Banagher's. For example, TY1 is 188 663 mm² here against Banagher's 188 790 mm².
No alias to the `ukie` classes is created.

### Other Ashghal sheets (research agent, same day)

SD 5-1-100 Rev 2 (general notes) assigns the drawing numbers:

- SD 5-1-101…110 are the Q-beam sheets.
- SD 5-1-111…115 are the TY/TYE sheets.

No other Ashghal precast beam family therefore exists in this series. SD 5-1-102 and
SD 5-1-103 (Q-girder reinforcement and prestressing) print a 185 mm bottom-slab
thickness and strand-grid widths. These could tighten the existing round-1
`qa.QaQBeamSection` reconstruction. That module is not modified here; this is a lead
for its owner.

Local copies of those sheets and their SHA-256 hashes:

| Sheet | Local file | SHA-256 |
|---|---|---|
| SD 5-1-100 | `round2/qa/sd-5-1-100.pdf` | `c090940f…` |
| SD 5-1-102 | `round2/qa/sd-5-1-102.pdf` | `31c3a2c5…` |
| SD 5-1-103 | `round2/qa/sd-5-1-103.pdf` | `8eaa983f…` |

## Morocco: SADET I40–I55 (estimates)

**Source.** The source is [SADET "Poutres industrielles"](https://sadet.ma/wp-content/uploads/2023/09/poutres-industrrielles.pdf),
PDF page 2. The local file is `sources/expansion/asia-africa/sadet-morocco.pdf`, SHA-256
`8f60ff2b42d0266c48ed6ef9a32759ad79732dbfe77cc476547fca0ed9a5bffd`.

The table gives three columns:

- Base (cm): 40, 45, 50 and 55.
- Portées limites (limiting spans, m): 25, 26, 28 and 29.
- Poids (kg/ml, mass per metre): 282, 888, 995 and 1150.

The embedded graphic is a 240 × 143 px raster showing four symmetric I outlines. It
has web callouts of 10, 15, 20 and 25 cm.

**Scaling.** The graphic uses one consistent scale. Pixel base ÷ printed base gives
10.98–11.11 mm/px for all four beams. The measured webs are 111/165/211/253 mm, which
is one stroke width (≈11 mm) above the callouts. All four are drawn at the same depth.

**Estimated outline.** Everything except the base and web widths is scaled from the
graphic. The estimates are:

| Feature | Value (mm) |
|---|---|
| Depth | 1220 |
| Top-flange vertical edge | 210 |
| Top taper | 100 |
| Bottom taper | 100 |
| Bottom flange | 150 |

The top width equals the base width, and corners are sharp. Scaled values carry about
±11 mm uncertainty.

**Mass check.** The density is not stated. At an assumed 2500 kg/m³, the implemented
outline's mass is below the printed mass by:

- I45: −9.6%
- I50: −4.0%
- I55: −3.7%

This is pinned in the tests and not fitted, because the printed masses may include
reinforcement. The printed I40 mass (282 kg/m, which implies 0.113 m²) conflicts with
its outline (0.26 m²) and with the family progression. It is preserved verbatim.

**Other Moroccan producers** (research agent): SADET's documentation page lists only
the same PDF. INTERSIG Maroc's page is descriptive only. No catalogue was found for
Préfa Maroc, Bonna Sabla or Tecnoprefa.

## South Africa: Bedrock Group sheets corroborate Civilcon (no new profiles)

[Bedrock Group's bridge-beam page](https://bedrockgroup.co.za/bridge-beams/) (accessed
2026-09-23) serves four 945 × 733 px catalogue images. These were saved to
`round2/za/bedrock-{M,T,U,Y}.png`. The SHA-256 hashes are in the JSON. The images
reproduce the Civilcon PPBM/PPBT/PPBU/PPBY sheets with the **same property tables**.
They are therefore not new profiles, and no `za/r2_*` module was written. They do add
evidence for the round-1 owner of `za.civilcon_*`:

- **M sheet.**
  - It prints the dimensions the Civilcon sheet omits: web 160; top 50 + 300 + 50
    (400 wide) with a 50 × 50 notch; upper flare 120 horizontal × **60** vertical;
    edge inset 10; chain 35/125/50/80.
  - The printed 60 mm flare confirms the round-1 *fitted* flare of 60.
  - The printed 10 mm inset conflicts with the fitted 15.
  - With all printed values (inset 10), every M2–M10 area is a constant +875 mm² above
    the table.
  - The sheet prints M4 = 378 600 mm² and M10 = 1360 mm, confirming the round-1
    typo corrections.
- **T sheet.** It labels T10 as **815**, which resolves the Civilcon 850/815 label
  conflict in favour of 815.
- **U and Y sheets.** They are identical in content to Civilcon's.

## Ethiopia, Kenya, Tanzania, Uganda, Nigeria and other sub-Saharan countries (bounded search, no geometry)

- **Ethiopia.** [Berhane (2002), AAU thesis](https://etd.aau.edu.et/items/cc61a905-fcb6-4cc0-8e04-e1d9e4bdeb9f)
  was downloaded as `round2/et/aau-berhane-2002.pdf` (SHA-256 `7ccfa3f0…`). Its "standard
  sections" are **US PCI sections**, for example "standard PCI IV-section with modified
  height". It is not an Ethiopian family and nothing is transferred. The ERA Bridge
  Design Manual 2002/2013 and the 2013 Standard Detailed Drawings were found only on
  reseller sites (Scribd, pdfcoffee, Course Hero), so they were not used.
- **Kenya.** The KeNHA "ROAD DESIGN MANUAL – Part IV – Bridge_Design.pdf" URL now
  returns an HTML page. KeNHA's design-manual listing has no bridge manual. The
  Mombasa AASHTO-mould lead from round 1 remains adoption evidence only.
- **Uganda.** The MoWT Volume 4 Bridge Design Manual (UACE-hosted, 169 pp) contains no
  precast beam sections. The local copy was discarded.
- **Tanzania and Malawi (JICA).** Kigoma port and the Tanzania outline design drawings
  (roads and drainage) contain no girder sections. The Malawi M5 basic design (2005)
  shows only undimensioned alternatives-comparison sketches. The Mozambique Zambezia/Tete
  basic design (2006) mentions PC T-girders without sections.
- **Nigeria.** The FMW "Structural Design" link (fmhud.gov.ng) now returns an HTML page.
- **Ghana, Botswana and Namibia.** Only specifications, reseller copies or maintenance
  manuals were found. No beam geometry.
- **Other South African producers** (Corestruc, Concor, SANRAL standard drawings). No
  public dimension sheet was found. Corestruc's bridge page names M, I and F types
  without dimensions.

## Algeria, Tunisia, Egypt and francophone West/Central Africa (research agent, no geometry)

- **Algeria.** The ENP 2016 master's thesis by GASMI & KACIMI is saved as
  `round2/dz/enp-gasmi-kacimi-pont-poutre.pdf` (SHA-256 `04523d05…`). Its PDF page 34
  shows a student SETRA pre-dimensioning of a VIPP beam for the Oued Illoula viaduct
  (Béjaïa–Ahnif autoroute link, proposed by the Agence Nationale des Autoroutes).
  **Not implemented**, for two reasons:
  - It is a student design, not a standard or produced beam.
  - Its chains do not close: 10 + 5 + 10 + 115 + 20 + 20 = 180 cm is labelled as both
    the beam depth and the beam + 20 cm slab height.
  Algerian producers (SAPTA, ENGOA, Cosider) publish no beam catalogue.
- **Tunisia.** SOMEF's *Catalogue_Somef_bpt_2017_technique.pdf* exists, but the server
  returns HTTP 403 to automated fetches. This is a strong lead for a manual browser
  download. Prefabind's page is descriptive only.
- **Egypt.** No public GARBLT standard was found. The ResearchGate paper that cites a
  GARBLT "General and Technical Conditions of Prestressed Concrete Bridges over the Nile"
  is behind a login. ECPC's line is prestressed pipes.
- **Cameroon.** Two 2iE master's theses were identified, but their PDFs could not be
  resolved: Sodiko interchange, Douala (PRAD variant), and PK 49 Ekekam–Evodoula (PSC
  beams).
- **Libya, Mauritania, Senegal and Côte d'Ivoire.** Clean negatives within the budget.
- **France (out of scope, flagged for the owner of `fr`).** AFGC "Recalculs des VIPP"
  (`round2/fr/afgc-recalculs-vipp.pdf`), Fig. 3 on PDF page 7, gives two fully
  dimensioned VIPP beams.

## Gulf, Levant and Iran

- **UAE**: Abu Dhabi DMT Standard Drawings Part 1/Part 2 (`round2/ae/dmt-standard-drawings-part{1,2}.pdf`, SHA-256 `9e46980d…`/`c5497b8a…`) are public, but Part 2 ST-19/ST-20 (PDF p73–74) draw the PC girder only as an undimensioned silhouette (deck splay/haunch/panel dimensions only). Dubai RTA publishes no bridge standard drawings found; Dubai Precast (round 1) remains a family-name list only; Abu Dhabi Road Structures Design Manual TR-516 (jawdah.qcc.abudhabi.ae) timed out.
- **Saudi Arabia**: RGA Saudi Highway Code SHC 302/304 (shc.rga.gov.sa) and MOMRA MA-100-D bridge specifications were network-unreachable (TCP timeout, not a login) — highest-value retry. Al Rashid Abetong makes building precast only. A PMU student design (`round2/sa/pmu-thesis-candidate.pdf`) uses generic AASHTO girders.
- **Oman, Kuwait, Bahrain, Jordan, Lebanon, Iraq, Iran, Israel**: effectively unresearched in this round — the shared WebSearch budget ran out; MTCIT Oman library lists no manuals, mpw.gov.kw refused connection, gov.il Netivei Israel returned 403, and Iran (Publication 139 standard precast girders) was not attempted. These are open gaps, not evidence of absence.

## Remaining uncertainties

- **TYE area offset (0.13–0.16%).** The source of the offset is unresolved.
- **SADET estimates.** Depth and flange heights are scaled from a 240 × 143 px graphic.
  A SADET technical sheet would replace every estimate. The printed I40 mass remains
  anomalous.
- **WebSearch budget.** The shared session WebSearch budget (200 calls) was exhausted
  during this round. The later Gulf, Levant and Iran sweeps therefore relied on direct
  fetches, and their negatives are weaker than the Qatar, UAE and Saudi Arabia results.
