# Pakistan follow-up: AASHTO practice and actual beam sections

Checked 22 September 2026. Pakistan **does use AASHTO bridge design provisions**, but the evidence found here points to a separately named **NHA Type A–H prestressed I-girder family**, not to an adopted, dimensionally identical US AASHTO Type I–VI catalogue. This is an evidence limit, not proof that no US section has ever been used on a Pakistani project. The three new source records are in [structured form](data/deep-search-pakistan-2026-09.json).

## Strongest section lead: NHA Types A–H

The NHA-authored July 2006 *Designing of Bridges on National Highways* is [text-indexed in a third-party copy](https://www.scribd.com/document/456777971/DESIGNING-OF-BRIDGES-ON-NATIONAL-HIGHWAYS-NHA-2006-pdf). Its contents items 7–8 include the girder schedule and March 2005 drawings **STANDARD/04** (Types A–C), **STANDARD/05** (D–F) and **STANDARD/06** (G–H). The title blocks attribute the drawings to NHA's Central Design Cell and name Lt Col (R) Muhammad Iqbal as designer. A [2025 UET Lahore research paper](https://irispublishers.com/ctcse/pdf/CTCSE.MS.ID.000766.pdf), PDF/printed p.2 **Table 1**, reproduces the dimensional schedule and identifies all eight as NHA standard I-girder sections. I downloaded and visually checked that page.

| NHA type | Span range (m) | H (mm) | B1 top (mm) | B2 web (mm) | B3 bottom (mm) | D1 / D2 / D3 / D4 / D5 (mm) |
|---|---:|---:|---:|---:|---:|---|
| A | 12–20 | 1200 | 550 | 180 | 550 | 250 / 90 / 475 / 185 / 200 |
| B | 14–23 | 1400 | 550 | 180 | 550 | 250 / 90 / 675 / 185 / 200 |
| C | 16–26 | 1600 | 600 | 180 | 600 | 250 / 100 / 750 / 210 / 290 |
| D | 20–28 | 1800 | 700 | 180 | 600 | 230 / 130 / 940 / 210 / 290 |
| E | 24–31 | 2000 | 700 | 180 | 600 | 230 / 130 / 1140 / 210 / 290 |
| F | 27–34 | 2200 | 900 | 190 | 620 | 200 / 175 / 1310 / 215 / 300 |
| G | 29–37 | 2400 | 1000 | 190 | 650 | 185 / 200 / 1485 / 230 / 300 |
| H | 32–40 | 2600 | 1100 | 190 | 750 | 170 / 225 / 1625 / 280 / 300 |

The paper's first span cell reads **“20-Dec”**, an apparent spreadsheet date-conversion error; the indexed NHA original reads **12–20 m**. The paper's p.3 **Figure 1** is a schematic whose dimension labels do not agree cleanly with Table 1 (it shows “B4” and “D6”). The original NHA STANDARD/04–06 sheets must therefore govern polygon transcription. The third-party copy was not visually inspected here, and an NHA-hosted copy/current revision remains to be obtained. These eight are leads, **not yet eight implemented profiles**.

This distinction has independent support: the [JICA West Bank Bypass design report](https://openjicareport.jica.go.jp/pdf/11879053_02.pdf), PDF p.17, says its minor-bridge PC-I shape was referenced to NHA's January 2005 *Standardization of Bridge Superstructures* and calls the type widely applied in Pakistan. [JICA Chapter 5](https://openjicareport.jica.go.jp/pdf/11879053_04.pdf), printed p.5-1 and p.5-84, lists **NHA DBNH**, **NHA SBS**, and **AASHTO 2004** separately, and says the three 29.9 m minor-bridge girders were designed with reference to the NHA documents. The JICA figures are bridge deck arrangements rather than complete proof of an A–H girder outline or constructed status.

## Direct NHA project drawing to transcribe

The [NHA-hosted Lahore–Sialkot Motorway link drawing pack](https://nha.gov.pk/wp-content/uploads/2018/01/Drawing-24-1-2018.pdf) is 190 PDF pages. On **PDF p.139, drawing LSM-EBP-BR-ST-012**, titled *Flyover at Station 0+337, 30M Girder Pre-Stressing Details*, sections **25-25, 26-26 and 27-27** show an I-shaped PSC girder with exterior/interior variants. I downloaded and visually inspected the original sheet. Section 25-25 gives **2000 mm** gross depth and **600 mm** bottom flange; section 26-26 gives a **900 mm** top flange as **350 + 200 + 350 mm**. This is project-specific design evidence. It is not labelled “AASHTO Type IV” or another US type on the sheet, and its relationship to the NHA A–H family remains to be checked against the complete contour. PDF p.72 **Structural Notes**, clause 2.1, cites **AASHTO LRFD 2010**; clause 2.2 cites the **West Pakistan Code of Practice for Highway Bridges 1967**. Clauses 6.1–6.4 give handling/installation requirements for prestressed girders. Those code citations cannot establish beam geometry.

## Search result and next evidence request

Searches for `site:nha.gov.pk "AASHTO TYPE" girder`, `site:gov.pk "AASHTO Type IV" bridge girder`, `Pakistan bridge drawing "AASHTO Type IV" "NHA"`, university repositories and producer terms did **not** yield a Pakistan authority drawing that explicitly calls out a US AASHTO Type I–VI girder, let alone a matching full contour. A Pakistani author's paper cites US Type IV performance literature, which is **not** a Pakistani Type IV deployment. Many NHA tender hits containing `AASHTO M-31` concern reinforcement material, and `AASHTO M 170 Class IV` concerns **concrete pipes**, not beams. One individual résumé mentions a Type VI **Illinois academic project**; it is not evidence for Pakistan.

Highest-value request to NHA Central Design Cell or the UET Lahore authors: an NHA-issued copy of *Standardization of Bridge Superstructures* (January/March 2005), especially **STANDARD/04–06**, and its current revision/status. Then compare complete A–H polygons to US standard drawings before reusing any US profile ID. The NHA project drawing's full contour can be separately transcribed without resolving that identity question.
