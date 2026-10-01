# Round 2: South Asia, Korea and the Philippines

Extraction date: 23 September 2026. The structured record is in
[data/round2-south-asia-korea-philippines-2026-09.json](data/round2-south-asia-korea-philippines-2026-09.json).
Downloads are under `sources/expansion/round2/{pk,kr,lk,bd,ph}/`, which is gitignored.

**Twenty profiles** were implemented in six classes. Pakistan has 11, Bangladesh 4, Korea 3, Sri Lanka 1 and India 1.
The Philippines, Bhutan, Afghanistan and the Maldives have **no implemented profile**: the
DPWH and MoIT hosts block automated retrieval, and no dimensioned source was located for the others.

| Class | Sizes | Provenance | Source (PDF page) |
|---|---|---|---|
| `pk.NhaStandardIGirderSection` | A–H | transcribed-with-convention | Mustafa & Javed 2025, Table 1 (p2), reproducing NHA STANDARD/04–06 (2005) |
| `pk.LsmPscIGirderSection` | 20m, 30m, 45m | transcribed | NHA Lahore–Sialkot link drawings, Dec 2017: ST-008 (p177), ST-012 (p139), ST-015 (p142) |
| `kr.r2_improved_psc_beam.ImprovedPscBeamSection` | H1400, H1700, H2000 | H2000 transcribed; others with convention | 국토해양부 대전지방국토관리청, 개량형 PSC BEAM 표준도, 2008 (pp 5, 12, 19, 27, 34, 41) |
| `lk.RdaTB505BeamSection` | TB505 | transcribed | RDA/NWP/T/497-9 (June 2024) p10; confirmed by the Pallanoya 3/2 km tender pack p10 |
| `bd.JicaPcIGirderSection` | 25m, 30m, 35m, 40m | fitted-reconstruction | JICA Western Bangladesh Bridges Improvement FR, Table 7.4.1, printed p7-27 (PDF p27) |
| `india.r2_delhi_vadodara_psc_i.DelhiVadodaraPscISection` | 30m | estimate | NHAI Delhi–Vadodara Pkg II Vol III, PDF p41 / printed p40 |

## Pakistan

### NHA standard Types A–H

Source: Table 1 of the 2025 paper, visually checked. The values are in mm. D1–D5 close to H exactly for all eight types.

| Type | Span (m) | H | B1 top | B2 web | B3 bottom | D1 | D2 | D3 | D4 | D5 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 12–20 | 1200 | 550 | 180 | 550 | 250 | 90 | 475 | 185 | 200 |
| B | 14–23 | 1400 | 550 | 180 | 550 | 250 | 90 | 675 | 185 | 200 |
| C | 16–26 | 1600 | 600 | 180 | 600 | 250 | 100 | 750 | 210 | 290 |
| D | 20–28 | 1800 | 700 | 180 | 600 | 230 | 130 | 940 | 210 | 290 |
| E | 24–31 | 2000 | 700 | 180 | 600 | 230 | 130 | 1140 | 210 | 290 |
| F | 27–34 | 2200 | 900 | 190 | 620 | 200 | 175 | 1310 | 215 | 300 |
| G | 29–37 | 2400 | 1000 | 190 | 650 | 185 | 200 | 1485 | 230 | 300 |
| H | 32–40 | 2600 | 1100 | 190 | 750 | 170 | 225 | 1625 | 280 | 300 |

**Convention:** the table is read as a five-segment I. D1 is the top-flange side, D2 a straight top splay, D3 the clear web, D4 a straight
bottom splay and D5 the bottom-flange side. There are no chamfers. The paper's own Figure 1 (p3) shows a
two-slope top underside with B4 and D6 labels that Table 1 does not have. That conflict is recorded rather than
resolved. The NHA STANDARD/04–06 sheets are still the governing retrieval target. The first span cell prints
"20-Dec", a spreadsheet date artefact, and is recorded as 12–20.

### Lahore–Sialkot Motorway link: 20, 30 and 45 m girders

All values are printed on the sheets. Every width chain and depth chain closes.

| Size | Drawing | H | Top | Web | Bottom | Chain from top (mm) |
|---|---|---:|---:|---:|---:|---|
| 20m | LSM-EBP-BR-ST-008 | 1600 | 800 (300+200+300) | 200 | 600 | 150/150/860/200/240 |
| 30m | LSM-EBP-BR-ST-012 | 2000 | 900 (350+200+350) | 200 | 600 | 170/170/1170/200/290 |
| 45m | LSM-EBP-BR-ST-015 | 2750 | 1100 (445+210+445) | 210 | 750 (270+210+270) | 220/200/1650/280/400 |

This is one project design. The structural notes cite AASHTO LRFD 2010 and the WPCPHB 1967, and no US type is named. None of these outlines equals an NHA A–H type.

## Korea: 개량형 PSC BEAM (2008)

Midspan (중앙부) sections are drawn for L = 25/30/35 m in the 표준형 series and 25/25/30 m in the 확장형 series. They reduce to
**three** distinct outlines. All share a 1200 top (500+200+500), a 200 web and a 1000 bottom (400+200+400). The top chain is 150 + 60,
the bottom splay is 150 and the bottom side is 175. The clear web is 865, 1165 or 1465. Radii are R50 at the top-flange underside
corner, R150 at the web fillets and R100 at the bottom shoulders. They are implemented as tangent arcs.

**Correction:** the H=1.4/1.7 sheets and the extended H=2.0 sheets print the bottom side as "75". Their chains then fall
100 mm short of H. The standard H=2.0 sheet (p19) prints **175**, which closes, and the scans measure about 160–175 mm.
175 is adopted, and a test pins the non-closure of "75". The undimensioned rounding at the top outer corners and soffit
corners is kept sharp.

## Sri Lanka: RDA T/B/505

The 13.5 m inverted-T beam has a 500 base with 25×25 soffit chamfers. Its vertical chain is 75 side + 80 taper, then a 100 web
over 100 mm, then a 45° 50 splay to a 200 × 195 top bulb, for 525 overall. The 2024 vector sheet omits the web and chamfer-leg
values, but the Pallanoya scan prints 100 and 25. The beams sit side by side with 225 mm polythene void displacers
in a filled deck. The standalone T/B/505 sheet was not obtained.

## Bangladesh: JICA / RHD PC-I, 25–40 m

The sketches print the depth, the full vertical chain, an 80 + 540/640 + 80 top rebate chain and the bottom width. The web is
**fitted** to the published area. It gives 200.0 mm (30, 40 m), 199.96 (35 m, where the published 0.6960 m² sits on the rounding
boundary: 696,050 mm²) and 179.5 (25 m, adopted 180, residual +550 mm² or +0.10%). This is a preliminary cost-estimate design, not an
issued RHD standard.

## India: Delhi–Vadodara Pkg II, 30 m

Printed values are 2000 deep, 1100 top, 750 base, and chain 150/100/1350/150/250. The web label is illegible on the 1-bit scan and
scales to about 288 mm, so 300 is adopted as an **estimate** (±20 mm).

## Analytic gross properties (no published tables except the Bangladesh areas)

| Profile | A (mm²) | yb (mm) | Ixx (mm⁴) |
|---|---:|---:|---:|
| NHA A / E / H | 433 375 / 679 300 / 997 475 | 601.6 / 997.1 / 1331.8 | 7.17e10 / 3.40e11 / 9.08e11 |
| LSM 20m / 30m / 45m | 591 000 / 734 500 / 1 153 900 | 812.2 / 1040.8 / 1395.9 | 1.87e11 / 3.70e11 / 1.14e12 |
| KR H1400 / H1700 / H2000 | 668 689 / 728 689 / 788 689 | 696.8 / 843.8 / 991.3 | 1.81e11 / 2.94e11 / 4.40e11 |
| LK TB505 | 129 875 | 207.3 | 3.51e9 |
| BD 25m / 30m / 35m / 40m | 529 550 / 672 300 / 696 050 / 752 300 | 781.1 / 820.1 / 896.2 / 1012.0 | 1.70e11 / 2.38e11 / 2.96e11 / 4.14e11 |
| IN Delhi–Vadodara 30m | 906 250 | 1023.8 | 4.32e11 |

## Leads not implemented

- **Philippines:** the DPWH Odiongan Type VI and POW 17J00028 "Type IV-B" files are on dpwh.gov.ph, which is behind an Incapsula bot challenge (not bypassed). The Laguna EIS figures (p120) are undimensioned. The JICA Davao bypass report names "AASHTO girder type V" with no dimensions. No Philippine profile can be implemented without DPWH plans.
- **Pakistan:** the original NHA STANDARD/04–06 sheets exist only as a login-gated Scribd mirror. The JICA West Bank Bypass report confirms NHA SBS (Jan 2005) usage but gives no dimensions.
- **Korea:** the MOCT 2002 load-rating manual, Tables 2.4–2.7, lists historic 1963/1978 and ADB/IBRD standard PSC-I by H/BU/BB only. The KEC 2017 standard-drawing set has no girders. The 2005 KEC standardisation report was not pursued, because the existing KHC class covers it.
- **Sri Lanka:** the ICC/ELS producer ranges are unreachable (404/403/refused). Other T/B/5xx sheets were not found.
- **Bangladesh:** the LGED manuals return HTTP 500. The Cross-Border report gives H and b6 only.
- **India:** the MoRTH 32 m sheets are blocked (TLS error or homepage redirect). RDSO refuses connections.
- **Bhutan:** Dopshari DSZ-SUP-08 returns HTTP 403.
- **Afghanistan, Maldives:** no source was found. The web-search budget was exhausted before targeted searches.

> **Integration note (23 September 2026):** the round-2 Delhi–Vadodara class
> duplicated `bridgebeams.india.DelhiVadodaraPscISection("KM37+744-MID")`
> from the round-1 extraction. Both use the same PDF (SHA-256 `828db4e9…`, p41)
> and give identical geometry (symmetric difference 0 mm²). The round-2 module
> was removed; the independent 300 ± 20 mm web reading agrees with the
> round-1 300 ± 26 mm estimate.

> **Update, 25 September 2026: Pakistan NHA Types A–H confirmed.** The owner
> supplied the NHA page "Summary of proposed standard cross-section of
> girders" (`sources/expansion/round2/manual/pk/owner-supplied-nha-summary-standard-girders.png`,
> SHA-256 `0a67013e…`). All 72 tabulated values equal the journal Table 1
> implemented in `pk.NhaStandardIGirderSection`. Its schematic is the
> five-segment I with straight splays, which resolves the Figure 1 conflict in
> favour of the implemented reading. Provenance is raised to `transcribed`.
> The page is headed "proposed"; the STANDARD/04–06 sheets themselves remain
> unseen.

> **Update, 25 September 2026: NHA STANDARD/04–06 sheets seen.** The owner
> supplied the three "Detail of standard cross-section of girders" drawings from
> the Central Design Cell, NHA Islamabad (STANDARD/04: Types A–C, March 2005;
> /05: D–F, March 2005; /06: G–H, title block March 2006). Images are in
> `sources/expansion/round2/manual/pk/nha-STANDARD-0{4,5,6}-owner-supplied.png`.
> Every printed dimension, flange split, depth chain and 1:1 / about 1:2 splay
> slope agrees with `pk.NhaStandardIGirderSection`. The drawings now govern.
