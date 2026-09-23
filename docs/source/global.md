# Global bridge beams

`bridgebeams` has two related collections: implemented section geometry and
sources for additional families. They have different evidence requirements.
The [research catalogue](research.md) records original titles, English
translations, dimensions, source URLs and remaining blockers from the
September 2026 international search.

The **research footprint** includes source records for many more jurisdictions
than have implemented beam geometry; the live count is on {doc}`coverage`.
See {doc}`coverage` for the complete country list and clickable heat map.
Its counts distinguish fixed profiles, parametric templates and researched
sources. The table below is only the implemented-family summary.

![Representative new and corrected beam profiles at a common scale](_static/images/global-additions.svg)

## Implemented families

| Jurisdiction | Module | Families | Evidence limits |
|---|---|---|---|
| Australia | `bridgebeams.aus` | Super-T T1–T5; I-girders 1–4 | AS5100.5 Appendix D; historical variants retained |
| Canada (Ontario) | `bridgebeams.ca` | MTO S300/S400/S500 solid slabs; NU900–NU2400 (8); box girders B700–B1000 (8) | June 2025 SS107 drawings; NU fillets are exact tangent arcs; 915 mm boxes are DRAFT 2023 estimates |
| Ireland | `bridgebeams.ie` | T, TY/TYE, Y/YE, U/SU, M/UMB, SY/SYE, MY/MYE, Solid Box, W | Source-specific exact and reconstructed profiles; SD class 4 discrepancies retained |
| United Kingdom | `bridgebeams.uk` | Banagher producer range, shared with Ireland | Availability aliases retain the same profile IDs and geometry; not a separate national standard |
| United States | `bridgebeams.us` | PCI AASHTO I-beams I–VI; MnDOT 14RB/18RB/22RB; WSDOT W42G–W74G, WF36G–WF100G, U/UF tubs G4–G6, bulb tees, deck bulb tees, slabs | WF and U/UF G4/G5 reproduce 2025 WSDOT properties; G6, W*BTG and deck-tee residuals pinned; WF*BTG and 24/30 in slabs are estimates |
| Belgium | `bridgebeams.be` | FEBE standardised I-beams | Flange thicknesses must be supplied by the designer |
| Greece | `bridgebeams.gr` | Egnatia extended-I families | Published depth law/widths; flange thicknesses are design inputs |
| India (NHAI projects) | `bridgebeams.india` | NH 45-A Ch 50+473 PSC I; NH 45-A Package II PSC/RCC 1300–2250 (7); Delhi–Vadodara PSC I | Final Feasibility Report drawings; RCC girders are reinforced, not prestressed; Delhi–Vadodara web width is a scan-measured estimate |
| Japan | `bridgebeams.jp` | JIS/PCCEN AG/BG T-girders | Chubu drawing metadata; additional drawing audit is in the PDF report |
| Korea | `bridgebeams.kr` | KHC PSC I-girders | Published 25/30/35 m data; 20/40 m sizes are extrapolated |
| Mexico | `bridgebeams.mx` | SEPSA I-girders (7); box and Type U (10); double tees (26); Nebraska (13) | Producer-specific; box table contradictions (CA-180, CA-135, B-400) pinned; Nebraska flange details estimated |
| New Zealand | `bridgebeams.nz` | RR364 Super-T; I-beams; 587/650/900 hollow-core | Gross profiles; 650/900 outer units remain excluded |
| Norway | `bridgebeams.no` | Five NTB and five KTB profiles | 15 mm bottom chamfers are reviewer-inferred |
| Poland | `bridgebeams.pl` | Mosty-Łódź T12–T27 | Family-specific dimension/provenance metadata |
| Qatar | `bridgebeams.qa` | Ashghal Q-girders T1–T5 | Documented reconstruction; maximum A/centroid/Ixx deviations 0.88%/0.85%/1.26% |
| Russia | `bridgebeams.ru` | 3.503.1-81, 33 m I-beams | Fitted flange profile validated against producer volumes |
| South Africa | `bridgebeams.za` | Civilcon I1–I20, Y1–Y8, T1–T10, U (9), Special U (2), M2–M10 | T is transcribed; U, Special U and M are reconstructions fitted to published properties; individual table discrepancies preserved |
| China (Beijing) | `bridgebeams.cn` | 20BGQL2 1800 mm urban-rail box, a = 0 and 300 mm | Dimensioned atlas section I–I; no published properties |
| Hungary | `bridgebeams.hu` | Ferrobeton FP, FPT, ITG, FI-150 (14) | Producer catalogue; radii measured from vector drawings; FPT-45, ITG-70/110 and FI-150 are estimates |
| Indonesia | `bridgebeams.id` | WIKA channel girders CG60–CG100; PC-I, PC-U, bulb tee | Channel girders fitted within 0.1%; I/U/bulb-tee outlines are estimates fitted to published A and I |
| Nepal | `bridgebeams.np` | DoR precast RC I 1300/1700 | 2015 standard drawing; stated 12 mm chamfer convention |
| Netherlands | `bridgebeams.nl` | Haitsma HKO, HKO-XL, HRP, HIP (50) | Producer tables; HRP/HIP keys fitted; HKO-XL outlines are estimates |
| Romania | `bridgebeams.ro` | ASA Grindă pod 42/52/72/80/95/105 | Transcribed with R-fillet conventions; 52 and 105 estimated; no published properties |
| Slovakia | `bridgebeams.sk` | VPH-PTMN girders and slab beams (12) | Published A/centroid/I; 2.1 m girder table conflict pinned |
| Spain | `bridgebeams.es` | HP-1 Tipo I–VI | Historic 1977 standard; areas match published volumes within 0.05% |
| Taiwan | `bridgebeams.tw` | Freeway Bureau Types IV–VIII | Dimensioned post-tensioned gross midspan profiles; analytically checked |
| Thailand | `bridgebeams.th` | DOH IG-205 | Published 20 m standard drawing |
| Türkiye | `bridgebeams.tr` | KGM-lineage I90/I120/I140/I170 | Worked-example profile assumptions; project drawing confirmation needed |

Banagher's documented Ireland/UK catalogue is available through both `bridgebeams.ie` and `bridgebeams.uk`; the UK exports alias the same producer geometry. Other UK designs require their own evidence and implementations.

Pakistan's NHA Type A–H PSC I-girders are [documented research leads](pakistan-us-section-followup-2026-09.md), with an NHA project drawing available for transcription. AASHTO design-code use does not show that their profiles equal US Types I–VI. The [cross-jurisdiction queue](aashto-cross-jurisdiction-followup-2026-09.md) likewise keeps AASHTO-named foreign beams separate pending full outline comparison.

![Examples implemented after visual review](_static/images/review-additions.svg)

## India and research-only countries

India has project-specific constructors from NHAI drawings:
`bridgebeams.india.Nh45aPscISection("CH50+473-MID")`, the seven NH 45-A
Package II outlines in `Nh45aIGirderSection`, and the Delhi–Vadodara
`DelhiVadodaraPscISection`. Every source title block says **Final
Feasibility Report**. They do not establish a national standard, a built
girder or an approved final design. The separate {doc}`india-followup`
records RDSO railway, MoRTH RCC and IRICEN leads.

Every family added in the September 2026 extraction round exposes
`provenance` (`transcribed`, `transcribed-with-convention`,
`fitted-reconstruction` or `estimate`) and `source_status`. Check both
before relying on a profile. The extraction records in {doc}`research`
list each convention, estimate and pinned discrepancy.

## Expanded source collection

See {doc}`research` for the complete regional reports and downloadable JSON:

- {doc}`research-europe-americas`: highway-agency standards, national
  catalogues and producer families across Europe and the Americas.
- {doc}`research-asia-africa`: Asia, Middle East and African sources, with
  English translations and explicit access limits.
- {doc}`research-pdf-transcription`: direct checks of the Qatar, New Zealand,
  Norway and Japan drawing backlog, including corrections to older notes.

The source records distinguish inspected documents from search leads and
unavailable downloads. Overall depths and widths alone do not define an
exact section. Some publications give independently tabulated area, centroid
and inertia; others still need internal haunch/flange dimensions.

## How to use the collection

Select a family by the original designation and source revision. Read its
accuracy statement before calculating section properties. For a researched
family that is not implemented, use the page-specific transcription and
original source to establish all necessary dimensions, then validate the
resulting polygon against independent published properties where available.

The new and audited families use millimetres and a soffit-based vertical
coordinate. Legacy Australian classes retain their existing negative-y
coordinate convention and older interface; check the family API. Research
records retain source units; centroid direction and inertia units must be
converted explicitly. Source publications remain copyrighted and are kept
as ignored local working materials. Their factual dimensions and provenance
are retained in versioned records.
