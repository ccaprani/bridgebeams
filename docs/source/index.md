# bridgebeams documentation

```{toctree}
:maxdepth: 2
:caption: Contents:

installation
families
tutorials
global
coverage
research
api
sources
```

## Overview

`bridgebeams` provides standard precast/prestressed **concrete bridge beam
sections** for use with the
[sectionproperties](https://sectionproperties.readthedocs.io) package — a
shared section library for `sectionproperties`, `concreteproperties`,
[PyBridge](https://github.com/ccaprani/PyBridge) and grillage tools such as
`ospgrillage`.

All geometry is in **millimetres** and returned as `sectionproperties`
`Geometry` objects, so sections can be meshed and analysed directly, or
wrapped with materials for concrete section design checks.

The complete coverage view currently counts **284 fixed profiles across
14 countries**, separately from **114 jurisdictions with research records**.
Belgian and Greek parametric templates are listed separately because their
flange thicknesses must be supplied.

## Implemented families

This table lists implemented families, not every researched country.
See {doc}`coverage` for the clickable map and complete country table, with
separate counts for source records, fixed profiles and parametric templates.
The UK and Ireland are separate jurisdictions; UK sources are catalogued
but the UK namespace currently exports no profiles.

| Jurisdiction | Family | Sizes | Validation vs published tables |
|---|---|---|---|
| Australia | Super-T (T1–T5) | 675–1725 mm deep | ported from v0.1; AS5100.5 App. D |
| Australia | I-girders (1–4) | 750–965 mm deep | ported from v0.1 |
| Ireland | T (T1–T10) | 380–815 mm | **exact** (<0.02%) |
| Ireland | TY / TYE | 400–900 mm | **exact** (<0.02%) |
| Ireland | Y / YE | 700–1400 mm | 2.6% / 0.8% rms |
| Ireland | U / SU | 600–1600 mm | **exact** (≤0.3%) |
| Ireland | M / UMB | 640–1360 mm | 0.7% / ≤0.6% |
| Ireland | SY / SYE | 1500–2000 mm | <0.05% / 0.56% rms |
| Ireland | MY / MYE | 300–600 mm | 0.8% / 0.3% rms |
| Türkiye | KGM I-girders | 900–1700 mm | analytic (no tables published) |
| South Africa | Civilcon I-beams | 710–1980 mm | corrected source orientation; published A/Yb/Z checks |
| Korea | KHC PSC I-girders | 1650–2500 mm | +2–3% vs literature |
| Russia | Soyuzdorproekt 3.503 33 m I-beams | Б3300 marks | 0.3% rms |
| Thailand | DOH IG-205 (20 m) | 1200 mm | drawn dims |
| Greece | Egnatia extended-I (45) | 1250–2150 mm | depth law + widths published |
| Ireland | Solid Box SD, width classes 1–4 | 32 variants, 300–1000 mm | nominal dimensions; class 4 source discrepancies recorded |
| Ireland | W | 16 variants, 800–2300 mm | current manual and producer CAD; Ixx residual <0.0025% |
| Norway | NTB/KTB | 10 profiles, 600–1400 mm | reconstructed gross sections; reviewer-inferred 15 mm chamfers |
| South Africa | Civilcon Y | Y1–Y8, 700–1400 mm | source and reviewed ledges; Y1 modulus discrepancy retained |
| New Zealand | Super-T; I-beams; hollow-core | 1025/1225; 1500/1600; 587/650/900 mm | hollow-core inner variants and 587 outer; drawing/analytic checks |
| Qatar | Q-girders T1–T5 | 800–1900 mm | reconstruction, maximum Ixx residual 1.26% |
| Mexico | SEPSA I profiles | 7 variants, 540–1830 mm | published area within 50 mm² rounding |
| Taiwan | Freeway Bureau IV–VIII | 1350–2100 mm | dimensioned gross profiles, analytic checks |
| Belgium | FEBE I-beams | 900–2050 mm | designer-supplied flange thicknesses |
| Japan | JIS AG/BG T-girders | 900–1300 mm | source drawing metadata; no A/I table |
| Poland | Mosty-Łódź T12–T27 | standard family | source metadata and geometric checks |

See {doc}`global` for jurisdiction coverage and representative profiles, and
{doc}`families` for profiles, accuracy statements and sources.

## Indices

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
