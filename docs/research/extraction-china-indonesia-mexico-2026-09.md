# Extraction: China (Beijing 20BGQL2), Indonesia (WIKA Beton), Mexico (SEPSA) — 2026-09

This round adds 67 gross-section profiles:

- **`cn`** (new package): 2 profiles, Beijing 20BGQL2 midspan box at a = 0 and a = 300 mm. Any `a` in 0–300 mm is also accepted.
- **`id`** (new package): 16 WIKA Beton profiles:
  - 4 CG channel girders, `fitted-reconstruction`;
  - 5 PC-I, 6 PC-U and 1 bulb tee, all `estimate`.
- **`mx`** (existing package): 49 new SEPSA profiles:
  - 10 box / Type U, `transcribed-with-convention`;
  - 26 double tees, `transcribed`;
  - 13 Nebraska girders, `estimate`.

  The existing `sepsa_i_girder.py` is unchanged.

All outputs are in mm, with the origin at mid-soffit and y pointing up. Voids are Shapely interiors. Structured data: `docs/research/data/extraction-china-indonesia-mexico-2026-09.json`.

## Sources

| Id | Document (original title) | Status | Local file / SHA-256 | Pages used |
|---|---|---|---|---|
| CN-BEIJING-20BGQL2 | 北京市工程建设标准设计文件 · 轨道交通通用图集 **20BGQL2** 《时速100公里及以下城市轨道交通后张法预应力混凝土单线预制箱梁》, 北京市规划和自然资源委员会 / 北京市城乡规划标准化办公室. <https://ghzrzyw.beijing.gov.cn/biaozhunguanli/bzgj/tytj/202105/P020210527325354365083.pdf> | Issued atlas for urban rail, not highway. Issue date not verified; the cover carries no date. | `sources/expansion/asia-africa/beijing-20bgql2.pdf`, `5aecbbfc…cffa6` | PDF p23 = printed p15 (预制箱梁构造图（二）, I–I 截面, A详图, 附注) and PDF p22 = printed p14 (构造图（一）). |
| ID-WIKA-2022 | WIKA Beton, *Brosur WTON 2022*. <https://crm.wika-beton.co.id/wika-crm-storage/brochure/1660206289_Brosur%20WTON%202022.pdf> | Producer brochure, July 2022 | `sources/expansion/asia-africa/wika-2022.pdf`, `7ec2716d…bffa23` | PDF p17 (PC-U), p18 (PC-I), p20 (bulb tee), p22 (channel girders). The brochure pages are unnumbered. |
| mx_sepsa | Grupo Constructor SEPSA, *Catálogo de piezas SEPSA V-05 27-21*. <https://sepsacv.com.mx/wp-content/uploads/2022/02/CATALOGO-DE-PIEZAS-SEPSA-V-05-27-21.pdf> | Producer catalogue | `sources/expansion/europe-americas/mx_sepsa.pdf`, `4bf8d28b…33feb` | PDF p5 (Trabe Nebraska), pp6–9 (Trabe Cajón CA-85…CA-180, B-400, Sección tipo U), p19 (Muro/Losa TT). The catalogue pages are unnumbered. |

I re-read every dimension from renders: Beijing at 400 dpi, WIKA p22 at 600 dpi, WIKA pp17/18/20 at 400 dpi, SEPSA pp5–9 at 400 dpi and SEPSA p19 at 500 dpi.

**Method note.** The WIKA and SEPSA pages are vector drawings. I extracted their paths with PyMuPDF (`page.get_drawings()`), which gave two results:

- **SEPSA drawings are uniformly scaled.** x/y scale factors agree within 0.2% on CA-85, CA-150, the three CA Type U sections, B-400 and all the Nebraska drawings. I used them only for *undimensioned* details: radii, chamfer lines and flange break points.
- **WIKA drawings are schematic.** The PC-I x/y factor ratio is 1.05–1.07. The bulb tee is strongly distorted: its x scale varies from 23.6 to 35.8 mm/pt across the section, while y is 33.4 mm/pt.

## 1. Beijing 20BGQL2 — `cn.Beijing20bgql2BoxSection`

Section I–I (midspan), all dimensions printed in mm:

| Item | Value |
|---|---|
| Depth | 200 + 150 + 1450 = **1800**. PDF p22 shows the midspan chain 200/150/1080/150/220. |
| Width | 2 × (2600 + a), with a = 0–300 (附注1: 图中桥面宽度参数a值取为0~300mm) |
| Soffit | 2 × 950 |
| Outer web | 250 horizontal over 1450 (58:10 slope marker); R=50 at the web–soffit and web–wing corners |
| Wing | 200 thick over the flat width a; tapers to 350 at the web top over 1400 |
| Void | 220 bottom slab, 1380 high, 200 top slab; 450×150 top haunches; 300×150 bottom haunches; half-widths 916 / 730 at the haunch ends; 280 web (normal) |
| A详图 | 滴水檐 (drip groove) R=20, 150 from the wing tip |
| Span table | L = 25/30/32 m, L1 = 3.45/2.95/3.95 m, n = 3/4/4. The midspan section is the same for all three spans. |

**Consistency.** A 280 normal web on the 250:1450 slope gives half-widths of 915.9 and 729.7 at the haunch ends, against 916 and 730 printed.

**Conventions:**

- The R50 corners are exact tangent arcs.
- The drip groove is an R20 circle centred on the wing soffit 150 mm from the tip. It lies on the tapered soffit when a < 170. Pass `drip_groove=False` to drop it.
- The following are excluded: vent, access and drain holes, the II–II/III–III end thickening (400 bottom slab), and the 20×20 end chamfers.

**Analytic results (no published properties):**

| Case | Area | yb | Ixx |
|---|---|---|---|
| a = 0 | 2 567 095 mm² | 1156.3 mm | 1.0251e12 mm⁴ |
| a = 300 | 2 687 095 mm² | 1180.6 mm | 1.0594e12 mm⁴ |

The fillet-free closed form is 2 568 520 + 400a mm².

**Registry correction.** `deep-search-asia-africa-2026-09.json` stated an outer depth of "150 + 1450 = 1600 at II–II". The drawing gives 1800 at every section.

## 2. WIKA Beton — `id`

### Channel girders CG60/70/80/100 × 1200 (p22) — `fitted-reconstruction`

Printed dimensions:

- Width chains: 240+20+50+580+50+20+240 (CG60), 235+25+50+580+50+25+235 (CG70) and 230+30+50+580+50+30+230 (CG80). All sum to 1200.
- Top: 15 + 1170 + 15.
- Depth chains: 50 / 150 / 400, 500, 600 or 800.

Published values (the brochure uses "." as the thousands separator):

| Section | A (cm²) | I (cm⁴) |
|---|---|---|
| CG60 | 4 329 | 1 293 103 |
| CG70 | 4 806 | 2 023 171 |
| CG80 | 5 274 | 2 968 087 |
| CG100 | 6 334 | 5 717 699 |

**Pinned: the CG100 chain does not close.** It is printed as 230+40+50+**580**+50+40+230 = 1220. The vector drawing shows a 560 void top, which gives a 50×50 haunch and closes to 1200. I used 560.

**Undimensioned details:** the side shear key, the inner-haunch rise and the corner chamfers.

- Scaled from the drawing (chamfers ≈20, haunch 50×50, key 25), the outline gives A +0.14…+0.29% and I −0.28…−0.71%.
- A least-squares fit of values common to all four sizes gives c = 4.1, h = 40.1, key = 31.7 mm. The worst residual is 0.04%.
- **Implemented rounding:** 5×5 bottom chamfers, a 50×50 haunch and a 35 mm key recess with 25 mm rises. Residuals are ≤0.05% in A and ≤0.10% in I.

### PC-I H90–H210 (p18), PC-U H120–H230 (p17), Bulb Tee H220 (p20) — `estimate`

Only H, the widths and the web are printed. PC-I uses "," as the thousands separator: `2,572 cm²` = 2 572.

**PC-I**

- I rescaled the vector outline so the printed widths are exact.
- Two factors were then solved per size to reproduce A and I exactly: one for the top-flange depths and one for the bottom-flange heights.
- The factors are 0.90–1.015 and 0.996–1.016, so the drawing proportions are close to real.

**Bulb tee**

- The drawn area is 22% too large, because of the distortion noted above.
- The fitted factors are 0.88 (top) and 0.61 (bulb heights). This gives a 288 mm edge and a 206 mm taper.

**PC-U**

- There is one drawing for six sizes. Scaled as U-185/190, its 300 mm bottom slab matches the printed "300" label.
- Kept as printed: the 300 slab and the 300 web (horizontal thickness in the upper vertical part).
- How sizes vary: the webs translate with the top width A, and the mid-web region stretches with H.
- One common fit over all 12 A/I values gives a top-zone depth scale of 0.86 and a soffit half-width shift of −85 mm. Residuals are −1.26…+1.08% in A and −0.77…+0.53% in I; the worst is H210.
- I rejected exact per-size fits. They need a top-flange scale of 0.2–0.35 for H165–H230, which is implausible.

None of these outlines should be read as manufacturer geometry.

Out of scope and not implemented: voided slabs VS57–74 and segmental boxes. Both are PARTIAL in the assessment.

## 3. SEPSA — `mx`

### Muro/Losa TT (p19) — `transcribed`, 26 profiles

Uses (original): "Trabes para puentes vehiculares y puentes peatonales, sistemas de piso para edificios, naves industriales…". The unit is multi-purpose.

| Variant | Stem axes | Width chain | Flange | Haunch | Stem top | Rows |
|---|---|---|---|---|---|---|
| Ligera | 150 | 59.5 / 31 / 119 / 31 / 59.5 | 5 | 7.5×7.5 | 16 | h 85–45 |
| Pesada | 150 | 54.8 / 40.4 / 109.6 / 40.4 / 54.8 | 5 | 8×8 | 24.4 | h 85–45 |
| Americana | 122 | 68.5 / 41 / 81 / 41 / 68.5 | 5 | 8×8 | 25 | h **81**–45 |

- **Stem bottom b:** taken from the table for each h.
- **Flange width a:** trimmed symmetrically. The tabulated area changes by exactly 50 cm² per 10 cm of a.
- **Area check:** every one of the 328 h × a cells is checked. Residuals are within b-rounding (±0.05 × stem height + 0.5 cm²).
- **Pinned:** Ligera h=75 (−5.0 cm²) and h=60 (−3.5 cm²).
- **Pesada at a = 190:** the haunch foot at 95.2 cm overhangs the 95 cm flange edge. I trimmed it, which removes a 2 mm sliver.

### Trabe Cajón CA-85…CA-180, B-400 and Sección tipo U (pp6–9) — `transcribed-with-convention`, 10 profiles

The wing width `a` is a parameter. Table rows were reused from `europe-americas-sources.json` and visually re-checked.

**Printed dimensions (cm):**

| Family | H | Void (top / bottom / height) | Chamfers | Web | Bottom slab | Straight web | Wing |
|---|---|---|---|---|---|---|---|
| CA-85 | 85 | 54.7 / 39.6 / 58 | 10, 15 | 9 | 15 | 52 | 5 + 7.8 + 20.2 |
| CA-115 | 115 | 59.4 / 39.6 / 88 | 10, 15 | 9 | 15 | 82 | 5 + 7.8 + 20.2 |
| CA-135 | 135 | 62.5 / 39.6 / 108 | 10, 15 | 9 | 15 | 102 | 5 + 7.8 + 20.2 |
| CA-150 | 150 | 65.2 / 39.6 / 123 | 10, 15 | 9 | 15 | 117 | 5 + 7.8 + 20.2 |
| CA-180 | 180 | 69.4 / 39.6 / 153 | 10, 15 | 9 | 15 | 147.2 (Type U drawing: 147) | 5 + 7.8 + 20.2 |
| B-400 | 160 | 124 / 83.8 / 125 | 15, 25 | 17 | 20 | 95 + 35.3 | 5 + 7.1 + 17.6 |

- All CA families share an 83.8 base with R5 corners (36.9 + 5 each side) and an R22 web–wing fillet.
- B-400 has a 165.7 base, an 86.3 flat, an R20 web–wing fillet and a large unlabelled soffit radius.

**Type U drawings:**

| Section | Width chain | Web | Bottom slab |
|---|---|---|---|
| CA-135-U | 118.7 / 7 / 58.5 / 7 / 118.7 | 11 | 20 |
| CA-150-U | 117.5 / 7 / 60.8 / 7 / 117.5 (sums to 309.8) | 11 | 20 |
| CA-180-U | 115.4 / 7 / 65.2 / 7 / 115.4 | 11 | 25 |
| B-400-U | 119 / 12 / 138 / 12 / 119 | 15 | 20 (bottom chain 39.7 / 86.3 / 39.7) |

**Conventions and measured values:**

- **Void chamfers** are at 45°.
- **Web thickness** is measured normal to the web. On CA-150, CA-180, B-400 and the Type U sections the dimension lines are drawn perpendicular to the web; on CA-85 and CA-115 they look horizontal. The difference is under 0.1 cm.
- **B-400 soffit radius:** R40, measured. A circle through the drawn tangent points gives R = 39.97. It reproduces the 86.3 flat and 165.7 base to 0.02 cm.
- **Type U inner bottom radius:** R27, measured on all three CA Type U drawings.
- **B-400 Type U top chamfer:** the line x + y = 206.1 cm, measured.
- **Wing soffit line:** it passes through the tip at a_max with b = 5. Its slope is solved so that the fillet tangent lies b1 below the tip soffit.
- **Check on that solution:** the resulting straight-web heights are 51.99 / 82.00 / 102.00 / 117.04 / 147.00 / 130.33, against 52 / 82 / 102 / 117 / 147.2 (147 on the Type U drawing) / 130.3 printed. The soffit flats come out at 36.87–36.88, against 36.9 printed.
- **Tip thickness b:** matches every table row within 0.03 cm, except CA-115. Its b column is a copy of CA-85's, so the deviation reaches 0.21 cm at a = 140.

**Area residuals (calculated − table) over all 103 rows:**

| Family | Closed (cm²) | Closed (%) | Type U (cm²) |
|---|---|---|---|
| CA-85 | −15…−10 | −0.26…−0.18 | — |
| CA-115 | −31…−12 | −0.47…−0.23 | — |
| CA-135 | **+43…+108 (pinned)** | **+0.6…+2.0** | +14…+34 (≤0.50%) |
| CA-150 | +14…+17 | +0.19…+0.25 | −4…−3 |
| CA-180 | **−368…−350 (pinned)** | **−5.3…−4.5** | −34…−15; the a=190 duplicate is −122 |
| B-400 | **+89…+104 (pinned)** | **+0.7…+0.9** | −6…−4 |

Source discrepancies I preserved rather than fitted away:

1. **CA-180 closed.** The table is about 360 cm² above the drawn geometry at every width. The closed-table area is even *below* the Type U area (8108 vs 8133 at a = 310), while the Type U geometry matches to ≤0.4%. This is probably a table or drawing error; it is unresolved.
2. **CA-135 closed.** Area decrements are about 4 cm² per 10 cm of a larger than the table's own b column implies. Also, the closed drawing prints a = 300 while the table uses 310, and the Type U value at a = 310 (6807) equals the closed value at a = 300.
3. **B-400 closed.** +0.8%, while the Type U matches within 0.06%. The mismatch is therefore in the top-slab or void region; the cause is unresolved.
4. **TC180 Type U a = 190.** The row repeats 7280 from a = 200.

### Trabe Nebraska (p5) — `estimate`, 13 profiles

Types: 135, 180, 200 alero especial, 210, 220, 240 and 240 base especial. Each has an 18 cm web; all except 135 also have a 20 cm web. The 20 cm variant adds 1 cm to every half-width. The published area difference is exactly 2 cm × depth for every type, which confirms this.

**Printed:**

- Vertical chain: 10 / 22 / web / 27 / 15.
  - Alero especial: 2 / 8.5 / 2.5 / 20 at the top.
  - Base especial: 25 bottom edge.
- Widths: 41/18/41 and 27.5/45/27.5; 125 or 184 top.
- Radii: R20 fillets and R5 at the bottom-flange corner.

**Estimated from the vector drawing:**

- flange-tip quarter-circle R10 (alero especial: R8.5 below a 2 cm vertical edge);
- the top-flange soffit break point, taken as a line tangent to R20 (the catalogue polyline is not tangent);
- 2×2 soffit chamfers on the base especial type;
- the 45 cm width taken as the chord at the lower R20 tangent points.

Area residuals are −0.23…−0.16% against the published m² values.

## Remaining uncertainties

- The WIKA PC-I, PC-U and bulb-tee outlines are fitted shapes, not drawings.
- The Beijing atlas issue date is not verified.
- The SEPSA CA-180, CA-135 and B-400 closed-table discrepancies need producer confirmation.
- There are no published inertia values for any SEPSA or Beijing profile.
