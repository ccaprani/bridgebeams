# Round 3 — Chile (MOP Manual de Carreteras Vol. 4) and Brazil (IFES São Domingos), 2026-09

Sources were downloaded manually by the owner (no web retrieval in this round).
Machine-readable record: `docs/research/data/round3-chile-brazil-2026-09.json`.

## Sources

| Local file | Origin | SHA-256 | Pages |
|---|---|---|---|
| `sources/expansion/round2/manual/cl/volumen-4-planos-obras-tipo-ondac.pdf` | MOP – DGOP – Dirección de Vialidad, *Manual de Carreteras, Volumen Nº 4 — Planos de Obras Tipo*, **Edición 2018** (© 2018). MOP Manual de Carreteras site (mc.mop.gob.cl); exact file URL not recorded (unverified) | `c3878fc531a6e252b32dbc75049c66c73311c85b6c45b1377f8e1ec33e68648f` | 411 (encrypted, print allowed; sheets are raster/vector images, text only on index pages) |
| `sources/expansion/round2/manual/br/ifes-sao-domingos-atena.pdf` | Atena Editora 2023, *Engenharias: pesquisa, desenvolvimento e inovação 2* (CIP; page footers say "3"), ISBN 978-65-258-0935-9, DOI 10.22533/at.ed.359231801; Cap. 2 DOI 10.22533/at.ed.3592318012. Original IFES repository item (repositorio.ifes.edu.br handle 123456789/2795) was anti-bot blocked in round 2 | `fbd41d70a651fcb808c3d57242ccd1c74bfa968f97e5638a85dbfce94d300567` | 242 |

## Chile — MOP MC Vol. 4, Sección 4.604 "Tableros de un Tramo, 11 m ≤ L ≤ 15 m"

Chapter 4.600 index (PDF p27, Índice Láminas dated Marzo 2015) lists three deck
types for 11–15 m single spans: losa nervada (vigas prefabricadas de hormigón
armado), tablero mixto hormigón-acero (steel girders — out of scope) and
tablero con viga de hormigón postensado. Sheets are PDF pp361–374.

### Viga postensada — lámina 4.604.203 (Noviembre 2000, PDF p372); 4.604.201 (Marzo 2015, PDF p370)

"Geometría y Cables Viga Postensada", Corte C-C (midspan). Common: depth 80 cm
("80 al eje"), top flange 15, 5 × 5 fillet flange-to-web, 10 cm bottom taper,
2,5 cm soffit chamfers ("tip. 2,5", Corte D-D). Table "VIGA POSTENSADA —
GEOMETRIA (cm)":

| Calzada | L (cm) | h4 | e | a1 | a2 | Ducto 1 | Ducto 2 | Size |
|---|---|---|---|---|---|---|---|---|
| 8,0 m con pasillo | 1100 | 15 | 15 | 40 | 55 | 13 | — | C8-L11 |
| | 1200 | 15 | 15 | 40 | 65 | 16 | — | C8-L12 |
| | 1300 | 15 | 15 | 40 | 75 | 10 | 9 | C8-L13 |
| | 1400 | 20 | 20 | 50 | 85 | 11 | 11 | C8-L14 |
| | 1500 | 20 | 20 | 65 | 95 | 13 | 12 | C8-L15 |
| 10,0 m sin pasillo | 1100 | 15 | 15 | 40 | 45 | 12 | — | C10-L11 |
| | 1200 | 15 | 15 | 40 | 55 | 14 | — | alias of C8-L11 |
| | 1300 | 15 | 15 | 40 | 65 | 17 | — | alias of C8-L12 |
| | 1400 | 20 | 20 | 40 | 75 | 10 | 10 | C10-L14 |
| | 1500 | 20 | 20 | 40 | 85 | 12 | 11 | C10-L15 |

(a1 = top width, a2 = bulb width, e = web, h4 = bulb vertical side.)

- 8 distinct outlines implemented as `MopVigaPostensadaSection` (`transcribed-with-convention`);
  the two duplicate rows are accepted as aliases, not counted.
- Convention: the top face carries the deck crossfall p% (depth given "al eje");
  modelled horizontal at 80 cm. Flat flange underside (a1 − e)/2 − 5 derived from the chain.
- Deck: 23 cm H-30 slab on 3 beams at 390 cm (1180 cm deck) or 340 cm (1080 cm); beam H-40.
  Note on 4.604.201: "Vigas postensadas se pueden reemplazar por diseño con vigas pretensadas (de fábrica)".
- No published section properties or concrete volumes (4.604.205 is steel only): no property check.
  End blocks (Cortes A-A/B-B, 200 cm + 60 cm transition) not modelled.

### Losa nervada viga prefabricada — lámina 4.604.001 (Marzo 2015, PDF p363); 4.604.003 (Nov. 2000, PDF p365)

"SECCIÓN VIGA": trapezoidal RC rib 25 (top) / 20 (soffit) × 70 cm, "Viga
prefabricada: Hormigón H-30"; Nota 14 allows prefabrication (planta o pie de
obra). 16 ribs at 75 cm (1160 cm deck) or 15 at 74 cm (1060 cm), 17 cm slab.
Implemented as `MopLosaNervadaVigaSection("V25/20x70")`, `transcribed`.
Check: "Cubicación 1 viga" H-30 = 1,73 / 1,89 / 2,05 / 2,21 / 2,36 m³ for
L = 11–15 m; A × L with A = 0.1575 m² reproduces all five (max 0.23%, rounding).

### Not implemented from Vol. 4
4.604.10x steel "Viga acero" (composite steel); 4.110 cajones prefabricados
(box culverts); 4.602 cast-in-place slabs. No other precast beam sheets found.

## Brazil — São Domingos bridge longarina (Atena 2023, Cap. 2)

Nóbrega & Ferreira (IFES), Cap. 2 pp5–29. Figura 7 "Seção transversal da viga
principal (longarina)", Fonte: PROJETO DE ENGENHARIA (2016), PDF p33 / printed p21.
Bridge: ES-010 over Córrego São Domingos, Conceição da Barra-ES; 20,10 m span,
6 precast prestressed I girders at 240 cm, 18 cm slab, 1480 cm deck (Figura 8).

| Dimension (cm) | Value |
|---|---|
| depth | 130 |
| top width / flange / taper | 60 / 10 / 7,5 |
| web width / height | 20 / 85 |
| bottom taper / flange / width | 7,5 / 20 / 45 |

- Implemented as `SaoDomingosLongarinaSection("SD-130")`, `transcribed`, source_status project-specific.
- The 30 cm block above the flange ("ALÇA DE IÇAMENTO", lifting loop) is excluded;
  hviga+laje = 1,48 m = 1,30 + 0,18 confirms.
- A = 0.374375 m² → 9.36 kN/m at 25 kN/m³ vs Tabela 5 q3 = 9,4 kN/m (−0.4%, rounding).
- Pinned: Tabela 8 yGc = 0,921 m is not reproduced (girder centroid 0.651 m;
  gross composite with b = 2,2 m, 18 cm slab 1.031 m). Definition unclear; recorded only.

### Other content in the book
No other Brazilian precast bridge sections: the remaining chapters cover steel
frames, materials, robotics, etc. No leads.

## Remaining uncertainties
- Chile: exact download URL; real top-face slope per project; whether a
  pretensioned factory substitute would keep this outline (the note implies a
  new design).
- Brazil: yGc definition; the figure is a raster reproduction of project drawings.
