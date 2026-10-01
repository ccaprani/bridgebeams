# Round 2: Latin America and the Caribbean precast bridge beams

Date: 23 September 2026. The structured record is in [round2-latin-america-2026-09.json](data/round2-latin-america-2026-09.json). This round added **23 profiles** from **five documents** in four jurisdictions:

| Class | Sizes | Provenance |
|---|---|---|
| `mx.r2_producer_aashto.DragonAashtoSection` | I–VI | I–IV `transcribed`; V–VI `transcribed-with-convention` |
| `mx.r2_producer_aashto.TubecoAashtoSection` | III–VI | all `transcribed-with-convention` |
| `br.DnitPcpLongarinaSection` | PCP-10, PCP-15, PCP-20 | `transcribed` |
| `ar.PretensaViSection` | VI-90, VI-100, VI-120, VI-130, VI-154, VI-160, VPI-45 | all `estimate` |
| `cr.PuentePrefaBeamSection` | CALIFORNIA-137, CALIFORNIA-167, SIMPLE-TE-97 | California `estimate`; T `transcribed-with-convention` |

By provenance: 7 transcribed, 7 transcribed-with-convention and 9 estimates. All outlines are in millimetres, with the origin at mid-soffit and y pointing up. No geometry was transferred between jurisdictions. The Mexican Tipo I–VI profiles come only from the Mexican producer sheets and are not aliases of `us.AashtoIBeamSection`. Dragón's V and VI webs are printed and drawn at 0.26 m, compared with 20 cm for Tubeco.

## Brazil: DNIT IPR-751 (federal standard)

The source is *Publicação IPR-751 — Álbum de projetos-tipo de pontes semipermanentes*. The profiles use Volume 1 — Desenhos, 2ª edição (2023), "PCP-xx – Longarina pré-moldada L01 = L02", Corte D-D, esc. 1:25. The sheets are folhas 46, 55 and 66, at PDF pages 56, 65 and 76. The 1st edition (2022) has the same dimensions on the same PDF pages, which was checked visually. The properties come from Volume 2 — Memória de cálculo, 2ª ed. 2023, Tabela 2-5, folhas 140–142. These are the "1ª Etapa" values, for the precast beam alone.

| cm | depth | flange width (top = bottom) | top flange / taper | web | bottom taper / flange |
|---|---|---|---|---|---|
| PCP-10 | 70 | 50 | 15 / 10 | 20 | 10 / 15 |
| PCP-15 | 100 | 50 | 15 / 10 | 20 | 15 / 15 |
| PCP-20 | 130 | 60 | 15 / 10 | 20 | 15 / 15 |

Residuals against Tabela 2-5:

* **PCP-15:** A 0.3275 vs 0.328 m², yi 0.4939 vs 0.494 m and I 0.03665 vs 0.037 m⁴. All are within the printed rounding.
* **PCP-20:** A 0.4300 vs 0.430 m², yi 0.6403 vs 0.640 m and I 0.08696 vs 0.0870 m⁴. This is exact.
* **PCP-10:** A is **0.2600 vs 0.267 m² (pinned, −2.6%)**. yi = 0.35 m matches exactly, and I = 0.01354 m⁴ is consistent with the printed 0.014 m⁴.

Two further notes:

* Tabela 2-1 in Volume 2 calls PCP-10 and PCP-15 "concreto armado pré-moldado", but Volume 1 has an armadura ativa sheet for every module. This inconsistency is recorded, not resolved.
* The solid end blocks are excluded.

## Mexico: new producer sheets (SEPSA not duplicated)

**Prefabricados Dragón, *Ficha técnica — Trabes tipo AASHTO*** is a single page with dimensions in metres. It was read from a 400-dpi render. Each vertical chain sums to its printed depth. The dimensions are:

* **I:** 0.70 deep, top 0.30, web 0.13, bottom 0.406, chain 0.10/0.08/…/0.13/0.13.
* **II:** 0.91 deep; 0.30/0.15/0.45.
* **III:** 1.15 deep; 0.40/0.18/0.56.
* **IV:** 1.35 deep; 0.50/0.20/0.66.
* **V:** 1.60 deep; top 1.06, web 0.26, bottom 0.71; chain 0.13/0.08/0.10/0.91/0.20/0.18.
* **VI:** 1.85 deep; the same widths as V; chain 0.13/0.08/0.10/1.09/0.25/0.20.

For V and VI, the break point between the outer and inner top tapers is not printed. At the sheet scale it measures a half-width of 0.231 m for V and 0.229 m for VI. That is a 45° inner bevel of 0.10 × 0.10 m, so a knee width of 0.46 m is used.

**Tubeco, *Elementos presforzados*** is a brochure with dimensions in centimetres, on PDF p7 (printed p6). It includes a 2 cm soffit chamfer, with the 2 cm vertical leg assumed. The dimensions are:

* **III:** 115 deep, web 18, bottom 56. The printed chain is 18/9/50/20/18.
* **IV:** 135 deep, top 50 = 15 + 20 + 15, bottom 66.
* **V:** 160 deep, top 107 = 34 + 9.5 + 20 + 9.5 + 34, bottom 71, chain 13/7/10/85/25/20.
* **VI:** 183 deep, with the same widths as V and a 108 cm web.

The sheet has two source typos, both pinned in the tests:

* **Tipo III top width:** printed "30", but 11 + 18 + 11 = 40 and the drawing scales to 38.8 cm. 40 cm is used.
* **Tipo IV chain:** 20 + 9 + 57 + 23 + 20 = 129 against the printed depth of 135. The drawn taper scales to 15.2 cm, so 15 is used.

PDF p8 shows a Nebraska girder with the same callouts as SEPSA's. It gives only an H range of 135–240 cm, so it corroborates `mx.SepsaNebraskaSection` and is not implemented separately.

Neither sheet publishes section properties. The tests are analytic: the chain closes, and widths and areas check.

## Argentina: Pretensa (estimates)

The *Puentes* brochure (`sources/expansion/europe-americas/ar_pretensa.pdf`) prints only depth, kg/m and spans. The VI schematic on p1 and the VPI-45 schematic on p2 were rendered at 500–600 dpi and measured by pixel run-lengths.

* **VI:** the schematic is assumed to be drawn at the maximum depth of 1.60 m. It measures flange widths of 585, a 110 mm top flange, a 45 mm top taper, a 140 mm web, a 120 mm bottom taper and a 230 mm bottom flange. Unfitted, this outline gives 1030 kg/m against the published 948 kg/m (+8.6%), which supports the scale assumption.
* **Each VI type:** the four flange heights are scaled by depth/1600. The web is then solved so that the area equals kg/m ÷ 2500 kg/m³. This gives webs of 116, 145, 124, 129, 95 and 112 mm.
* **Templates rejected:** a fixed-flange template and a uniformly scaled one were both tried and rejected. The published masses are not linear in depth, so they fit neither template.
* **VPI-45:** scaled from the printed 0.45 m depth. It measures 415 wide with flange heights of 70/50/100/95 and a web of about 95 mm. The web is fitted to 296 kg/m, which gives 89.5 mm. The unfitted outline is 1% heavy.

Treat every Pretensa dimension as uncertain by ±20%.

## Costa Rica: PuentePrefa

The profiles come from the diagrams `elem_prefa_diag2/3.jpg` on the producer's *Elementos prefabricados* page, which states spans of 4–40 m.

* **Viga California 137/167:** the printed dimensions are the depth, bottom 48, bottom flange 15, bottom overhang 15, web 18 and top flange edge 8. The top width, which is drawn equal to 48, and both tapers are scaled from the 600-px image at about 1.1 cm/px. That gives a top taper of 13 (137) and 17 (167) and a bottom taper of 15. These two profiles are estimates.
* **Simple te:** fully printed as 93 top, 10 flange, 97 deep and a stem tapering from 20 to 11. The flange soffit is modelled flat.
* **Doble te:** skipped. It is drawn flange-down and its stem positions are not printed.

## Searched, blocked or rejected

| Country | Lead | Outcome |
|---|---|---|
| BR | UFC thesis (Filgueira 2016) | Blocked: connection refused (curl and WebFetch) |
| BR | IFES São Domingos 1.30 m I girders | Blocked: Anubis anti-bot challenge |
| BR | SciELO/IBRACON U-beam paper | Rejected: the geometry is cited from Caprani, Mayer & Siamphukdee (Australia) |
| BR | Protensul, Cassol, T&A, Leonardi, Rotesma | Project lists or prose only |
| MX | ANIPPAC catalogue and `02.pdf` | Blocked: sgcaptcha |
| MX | COMPRE, MEXPRESA, ITISA | No dimensions |
| CL | MOP Manual de Carreteras Vol. 4, §4.604 "Tableros de un tramo 11–15 m" (losa con viga pretensada) | Blocked: reCAPTCHA on the official site and on silo.tips. This is the best Chilean lead |
| CO | INVIAS, Preansa | No standard; sections are project-specific |
| PE | MTC Manual de Puentes, Supermix | No outlines |
| PE | Continental thesis | Academic, not implemented |
| EC | Mavisa "Viga tipo I California" | No dimensioned image found |
| NI | Yahoska shop drawing (UCC thesis, PDF p115) | Labels are detached from their dimension lines; would need a fitted reconstruction |
| SV | MOPT UNI07E | AASHTO Tipo IV postensada, H = 1.40 m, L = 31.30 m; no drawing |
| GT | SEGEPLAN Benque Viejo | HTTP 403 |
| GT | USAC T6054 | Teaching reproduction of the US types |
| PR | ACT Planos Modelo | No girder sheets found; the PR bulb-tee standard is unverified |
| UY, PY, BO, VE, HN, PA, DO, JM, CU, HT | — | No dimensioned public source found within the bounded effort. The session web-search budget ran out part-way through |

## Remaining uncertainties

* Dragón V/VI knee width is taken from the drawing scale.
* Tubeco's soffit-chamfer vertical leg and its top-corner rounding are not dimensioned.
* The DNIT PCP-10 table area differs from the drawing.
* All Pretensa and PuentePrefa California dimensions beyond depth are estimates.
* None of these producers publishes I or yb, apart from DNIT.
