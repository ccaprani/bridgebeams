# bridgebeams documentation

```{toctree}
:maxdepth: 2
:caption: Contents:

installation
families
tutorials
global
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

## Families

| Jurisdiction | Family | Sizes | Validation vs published tables |
|---|---|---|---|
| Australia | Super-T (T1–T5) | 675–1725 mm deep | ported from v0.1; AS5100.5 App. D |
| Australia | I-girders (1–4) | 750–965 mm deep | ported from v0.1 |
| Ireland/UK | T (T1–T10) | 380–815 mm | **exact** (<0.02%) |
| Ireland/UK | TY / TYE | 400–900 mm | **exact** (<0.02%) |
| Ireland/UK | Y / YE | 700–1400 mm | 2.6% / 0.8% rms |
| Ireland/UK | U / SU | 600–1600 mm | **exact** (≤0.3%) |
| Ireland/UK | M / UMB | 640–1360 mm | 0.7% / ≤0.6% |
| Ireland/UK | SY / SYE | 1500–2000 mm | <0.05% / 0.56% rms |
| Ireland/UK | MY / MYE | 300–600 mm | 0.8% / 0.3% rms |
| Türkiye | KGM I-girders | 900–1700 mm | analytic (no tables published) |
| South Africa | Civilcon I-beams | 710–1675 mm | exact vs published Ixx |
| Korea | KHC PSC I-girders | 1650–2500 mm | +2–3% vs literature |
| Russia | Soyuzdorproekt 3.503 33 m I-beams | Б3300 marks | 0.3% rms |
| Thailand | DOH IG-205 (20 m) | 1200 mm | drawn dims |
| Russia/CIS | 3.503.1-81 33 m I-beams | 1530/1730 mm | 0.3% vs volumes |

See {doc}`global` for the clickable world map of jurisdictions and
{doc}`families` for profiles, accuracy statements and sources.

## Indices

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
