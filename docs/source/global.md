# Global bridge beams

Standard precast/prestressed bridge beam families by jurisdiction. Click a
pin on the map to jump to that jurisdiction. Green = implemented in
`bridgebeams`; blue = researched with dimension sources collected; grey =
surveyed, planned.

```{raw} html
<div style="max-width: 900px; margin: 0 auto;">
<object data="_static/images/world_bridge_beams.svg" type="image/svg+xml"
        style="width:100%; height:auto;" aria-label="World map of bridge beam families"></object>
</div>
```

The per-region research briefs (dimension tables, standard-drawing URLs,
licensing notes) live in `sources/research/` of the repository working
tree; the registry with URLs is `sources/SOURCES.md`.

## Implemented

(ireland-uk)=

### Ireland / UK

The Irish standard precast ranges (Banagher / Concast / Shay Murtagh —
common industry families to I.S. EN 15050): **T, TY/TYE, Y/YE, U/SU,
M/UMB, SY/SYE, MY/MYE**. Implemented with published-table validation from
**exact** (T, TY, U) to documented reconstructions (Y: 2.6% rms; MY: 2.2%).
The 2007 "05316 Precast Beam Properties" spreadsheet — the origin of this
effort — carries the same tables plus 50 embedded CAD drawings.

(australia)=

### Australia

**Super-T girders (T1–T5, pre- and post-2001)** and **I-girders (types
1–4)** to AS5100.5 Appendix D — ported from the original 0.1 release to the
current `sectionproperties` API.

## Researched — dimension sources collected

(united-states)=

### United States

AASHTO Types I–VI; PCI/CIOS bulb-tees (BT-54/63/72); PCI box beams; deck
bulb-tees; NEXT beams; spliced U-girders. Dimension sources: PCI Bridge
Design Manual appendices plus state DOT standard drawings (TxDOT, WSDOT,
PennDOT, FDOT, NCDOT) — freely downloadable. Colorado DOT alone
standardised 56 I-beam sizes (brief:
`sources/research/research-us-aashto-pci.md`).

(canada)=

### Canada

CPCI standard sections (Design Manual, 5th ed.); Ontario MTO **NU series**
(NU900–NU2400, standardised 2014); Alberta SL/SLW-510 + NU1200–NU2800;
BC MoT D202 standard prestressed I-beams. CSA S6 context.

(china)=

### China

JTG 通用图 standard ranges: 装配式预应力混凝土 T梁 (20–40 m spans),
先张/后张空心板 (10–20 m), 装配式小箱梁 (20–40 m). Dimension tables
reproduced in the open qlgc textbook; JTG D60/D62/3362 context free from
MOT.

(india)=

### India

IRC standard precast girders and MoRTH standard drawings (brief in
`sources/research/research-india-europe-aunz.md`).

(japan)=

### Japan

**JIS A 5373:2016 Annex B** is the only codified source: pretensioned
I-girders AG18–AG24 (spans 18–24 m; depths 900–1200 mm; base width
800 mm) plus slab girders. Full web/flange/strand detail lives in the
PCCEN design-manufacturing handbook (purchase); MLIT regional guidelines
give free span tables.

(korea)=

### Korea

No national catalogue (KDS 24 14 21 gives minimum thicknesses only). The
de-facto standard is the **KHC (Korea Expressway Corp.) PSC I-girder**:
25 m → 1750 deep (640/200/600 flanges/web), 30 m → 2000 (700/200/660),
35 m → 2200 (760/220/720); Ix = 4.64×10¹² mm⁴ for the 35 m section.
Full brief with CODIL sources:
`sources/research/research-japan-korea-sea.md`.

## Surveyed — planned

(brazil)=

### Brazil

Standard I-beams (vigas I pré-moldadas), DNIT/DNER patterns, manufacturer
standard sections (brief in `sources/research/research-canada-brazil.md`).

(mexico)=

### Mexico

SCT/CAPA standard drawings (survey brief).

(argentina-chile-colombia)=

### Argentina / Chile / Colombia

National practice survey (same brief).

(united-kingdom)=

### United Kingdom

Historic CBDG standard beams (inverted-T, M, I, box) — the ancestors of the
Irish ranges already implemented; historic dimension sources identified.

(nordics)=

### Nordics

Sweden (Bro), Norway, Finland standard beam families surveyed.

(turkey)=

### Turkey

KGM standard precast sections surveyed.

(russia-cis)=

### Russia / CIS

GOST / Союздорпроект typical series surveyed.

(middle-east)=

### Middle East

Gulf practice (adopted AASHTO/BS/EN + national drawings) surveyed.

(south-africa)=

### South Africa

No SANRAL national catalogue, but the SA families are the **British-tradition
M (M2–M10), I (I1–I20), Y (Y1–Y8), T (T1–T10), U (U1–U12)** ranges —
precaster Civilcon publishes **complete dimension tables** (free PDFs,
TMH7 loading span charts). Our existing Y/T/U implementations already
cover much of this practice; the I-beam table is a strong candidate for
implementation (brief: `sources/research/research-africa-mideast-cis.md`).

### Qatar

**Ashghal Standard Detail Drawings SD 5-1-100…115** (free, official):
**Q-girder** family (5 depths: 800/1050/1250/1550/1900 mm) and a TY-beam
family (10 sizes, 400–850 mm) with full section-property tables — a
standout primary source in the Gulf (brief:
`sources/research/research-africa-mideast-cis.md`).

(southeast-asia)=

### Southeast Asia

Malaysia (JKR), Thailand (DOH), Indonesia (Bina Marga), Vietnam,
Philippines — adopted foreign standards plus local families surveyed.

(new-zealand)=

### New Zealand

**NZTA RR 364 (2008)** publishes complete standard designs — hollow-core
deck units, I-beams, and **Super-T at 1025/1225 mm** (default below 35 m)
— free PDF with dimensions and strand patterns; RR 252 reviews AU/UK/US/CA
practice. Historic MoW families (1970s) documented too.

(norway)=

### Norway

**Handbok V426 "Prefabrikkerte brubjelker"** (free, Statens vegvesen):
pre-approved pretensioned **NTB / KTB** T-beams, spans 12–40 m, with form
and reinforcement drawings. Historic NIB series (302 predimensioned
I-beams) in the archived Bruhåndbok.

(continental-europe)=

### Continental Europe

**Belgium**: FEBE standardisation catalogue — I-beams h = 900–2050 mm in
50 mm steps (free). **Spain**: BOE official collections — HP-1 (1977) and
vigas pretensadas I/II/IC/IIC with drawings. **Poland**: Mosty-Łódź
T12–T27 system + GDDKiA recommended catalogue (free). **Germany**: East-
German typified BT 50/70 → BT 500/700 series (public Bauarchiv-DDR).
**Greece**: 45 standard extended-I sections published (Frontiers in Built
Environment 2020, open access, from 2,284 as-built Egnatia beams).
**Finland**: historic Jbe I–V type drawings (open Doria records).
Switzerland, Austria, Portugal: producer catalogues only.
