# Round 2: East and Southeast Asia and Oceania precast beam extraction (23 September 2026)

This round implements **163 profiles** in 22 section classes across 9 jurisdictions. They are grouped below by the provenance label on each profile. **This is research-grade data, not an authoritative standard.** Each profile carries a `provenance` and a `source_status` label, and corrections are invited. The [machine-readable register](data/round2-east-asia-oceania-2026-09.json) gives the source URL, local file, SHA-256 and page locators for every source retrieved.

| Provenance | Profiles |
|---|---:|
| transcribed | 79 |
| transcribed-with-convention | 58 |
| fitted-reconstruction | 11 |
| estimate | 15 |

| Jurisdiction | Module / class | Profiles |
|---|---|---:|
| China (Shanghai) | `cn.r2_shanghai_hollow_slab` ShanghaiHingedHollowSlabSection / ShanghaiRigidHollowSlabSection | 8 + 8 |
| Japan | `jp.r2_jis_slab_girders` JisSlabGirderSection | 40 |
| Japan | `jp.r2_bipre_girders` BipreIGirderSection / BipreHollowGirderSection | 6 + 3 |
| Taiwan | `tw.r2_thb_pci_girders` ThbPciGirderSection | 7 |
| Thailand | `th.r2_doh_girders` ThDohPlankGirderSection / ThDohBoxBeamSection / ThDohIGirderR2Section | 14 + 4 + 2 (IG20 duplicates the existing DOH girder) |
| Vietnam | `vn.c620_girders` Vn620GirderSection | 5 |
| Cambodia | `kh.vong_scc_girder` KhVongGirderSection | 1 |
| Malaysia | `my` JkrPrtBeamSection / OkaMBeamSection / Gcast{U,TM,I,T}BeamSection | 10 + 9 + 9 + 9 + 1 + 1 |
| Indonesia | `id.r2_wika_voided_slab` WikaVoidedSlabSection; `id.r2_waskita` WaskitaPcIGirderSection / WaskitaVoidedSlabSection | 4; 8 + 5 |
| Australia (QLD, NSW) | `aus.r2_tmr_deck_units` TmrDeckUnitSection; `aus.r2_tfnsw_cbs_modules` TfnswCbsModuleSection | 5; 4 |

**No profile was implemented** for Hong Kong, Macau, Singapore, Mongolia, Laos, Myanmar, New Zealand (beyond the existing RR364 families), Fiji or Papua New Guinea. The regional sections below record bounded searches and leads for each. These are search outcomes, not proof that no source exists. Web searching was cut short when the session search budget ran out during the Chinese provincial-atlas pass.

Downloaded source files are stored under `sources/expansion/round2/<cc>/`, which is gitignored.

## China, Hong Kong, Macau

### Implemented: Shanghai 先张法预应力混凝土空心板（桥梁）, 16 profiles

Source: 上海市建筑标准设计《先张法预应力混凝土空心板（桥梁）》（征求意见稿）
DBJT08-101-20xx, 图集号 2021沪G1005, 159 pp, vector CAD.
URL https://zjw.sh.gov.cn/cmsres/4c/4c7fa68a2357415c983c9b8a30a514b3/ccbaf741f888cd24cdf8ee666074c47e.pdf,
local `sources/expansion/round2/cn/sh-dbjt08-101.pdf`,
SHA-256 `2ee81a5d2426f95a179a949564b6b87d89afd359aeaef3800d4630f3c7eec142`.
Status: consultation draft (PDF created 2021-10-19). The issued atlas is
DBJT 08-101-2024, which is not held. Draft values may differ.

Module `bridgebeams.cn.r2_shanghai_hollow_slab`, data `cn/data/r2_shanghai_hollow_slabs.json`.

#### Vol. 1 刚接空心板 (rigid-jointed): `ShanghaiRigidHollowSlabSection`, 8 profiles, transcribed-with-convention

Locators: printed page = PDF page − 3. Table 1 is on PDF p6 and Table 2 (void formers) on PDF p7.
The midspan B-B sections are on PDF pp 37/40 (10 m), 45/48 (13 m), 53/56 and 61/64 (16/18 m),
and 69/72 and 77/80 (20/22 m). In each pair the middle slab comes first, then the edge slab. The 16 m and 18 m
sheets have identical sections, as do the 20 m and 22 m sheets. So there are 4 depths × {middle, edge}.

| Size | D | Void | Void bottom | Printed side heights |
|---|---:|---|---:|---|
| 10m | 550 | Ø360 | 90 | 357 / 383; edge 283+50+200 |
| 13m | 650 | Ø360 | 140 | 457 / 483; edge 383+50+200 |
| 16-18m | 850 | 360×650 round-ended (R180) | 100 | 657 / 683; edge 583+50+200 |
| 20-22m | 950 | 360×650 round-ended | 150 | 757 / 783; edge 683+50+200 |

Common dimensions:
- Base 1100.
- Middle slab: 50+1200+50 = 1300 at the ledge corners, with a 180 overhang.
- Edge slab: 300+1150+50 = 1500 overall. The cantilever tip is 200 thick, and its soffit rises 50 over 300.
- R30 reentrant fillets.
- Void centres at ±225 (145+360+90+360+145).
- 2% top crossfall.

Conventions:
- The top line is y = D + 0.02x. This reproduces every printed side height.
- The fillets are exact tangent arcs.
- Voids are placed by the printed bottom cover. The printed top cover is measured at x = −225 and is 4.5 mm short on the crossfall.
- The drip groove (R10) is omitted.
- No property table exists, so the tests use an independent hand-area formula.

#### Vol. 2 铰接空心板 (hinge-jointed): `ShanghaiHingedHollowSlabSection`, 8 profiles, transcribed

Locators: printed page = PDF page − 125. The parameter table is on PDF p127. The property table
(**表1 空心板毛截面特性**) is on PDF p130. The sections are on PDF pp 140–149.

| Size | D | Key (20 / k / k, deepest inset) | Void | Bottom / top cover | Published A (m²) mid / edge | Published I (m⁴) mid / edge |
|---|---:|---|---|---|---|---|
| 10m | 520 | 70, 50 | Ø360 | 80 / 80 | 0.30093 / 0.39868 | 0.00956 / 0.01178 |
| 13m | 620 | 70, 50 | Ø360 | 80 / 180 | 0.39993 / 0.49818 | 0.01675 / 0.01976 |
| 16-18m | 820 | 70, 50 | 360×650 | 90 / 80 | 0.38912 / 0.48837 | 0.03230 / 0.04046 |
| 20-22m | 900 | 80, 60 | 360×650 | 130 / 120 | 0.46542 / 0.56652 | 0.04632 / 0.05706 |

Widths and voids:
- Middle slab: 990 wide, with a 930 top surface (30 inset each side). The void chain is 100+360+70+360+100.
- Edge slab: 995 base, with the key on one side and a 400 cantilever on the other. The chain is 30+965+400.
  The cantilever tip is 200 thick and its root is at D−250.

Validation against the published values:
- Residuals are ≤0.004% for A, ≤0.002% for Yx and ≤0.036% for I (the 10 m I is printed to 3 significant figures).
- The published area matches only without the drip groove, so the published areas exclude it.
- The "50/60" callout is the horizontal inset of the deepest point of the key. This reading is confirmed by all eight area matches.
- The "80 mm topping" column is composite and is not used.

Tests: `tests/test_cn_r2_shanghai_hollow_slab.py`, 51 passed.

### Searched, not implemented

- **MOT 2008/2017 通用图 (T梁, 小箱梁, 空心板):** the only distribution found is through resellers (login or paywall). No open official PDF was located.
  The qlgc textbook tables give depth, rib and bottom-flange widths only, with no complete outline, so they were not implemented.
- **Chongqing T梁 standardisation Ver1.0 (12 volumes, March 2022 consultation):** jtj.cq.gov.cn times out (curl and WebFetch). Access is blocked.
- **Shanghai 预制拼装桥梁结构设计通用图 Part 4:** a steel-concrete composite box, so it is out of scope. Parts 1–3 were not located.
- **Shenzhen SJG 217-2026 装配式桥梁技术规程:** issued, but contains rules only. It points to the Guangdong highway
  standardisation 装配式预应力混凝土箱梁通用图, which is recorded as a lead.
- **Hong Kong:**
  - The HyD Structures Standard Drawings index lists no precast beams.
  - SDM 2013 has no standard sections.
  - GN040 is about thrie-beam barriers and is irrelevant (downloaded, then deleted).
  - The EPD IECL U-beam remains a project-only lead.
  - No `hk` package was created.
- **Macau:** a bounded DSSCU search found no bridge beam standards. No `mo` package was created.
- The session web-search budget ran out (200/200) during the China provincial-atlas search. Further provincial
  atlases (Zhejiang 2024 T梁, Guangdong 箱梁通用图, Chongqing DJBT50-186 小箱梁) remain leads.

## Japan, Taiwan

### Implemented (56 profiles)

| Module / class | Profiles | Provenance | Source status |
|---|---:|---|---|
| `jp.r2_jis_slab_girders.JisSlabGirderSection` | 40 (AS05–AS24, BS05–BS24; 18 distinct outlines) | 39 transcribed, AS19 transcribed-with-convention | JIS A 5373 スラブ橋げた; MLIT Chubu 道路設計要領 v2014.03 (superseded) + producer catalogues |
| `jp.r2_bipre_girders.BipreIGirderSection` | 6 (I25–I50) | 5 transcribed-with-convention, I45 estimate | Bi-Prestressing association trial designs (試設計), web (c)2009 |
| `jp.r2_bipre_girders.BipreHollowGirderSection` | 3 (H25–H35) | transcribed | same |
| `tw.r2_thb_pci_girders.ThbPciGirderSection` | 7 (Types I–VII) | transcribed | historic Dec 1991 公路總局 PCI standard drawings (withdrawn), via 2012 DGH journal |

#### JIS A 5373 slab girders (スラブ橋げた)
- Dimensions: Chubu v2014.03 PDF p28 / printed 5-25, 表-5-Ⅲ-9 (H, H1, H2, H3, mm) and 図-5-Ⅲ-40.
  Solid (充実断面): 700 soffit, 70 edge, 30×30 splay, 640 body to top. Hollow (中空断面): void 400 wide
  (120 walls), 300 top with 50×50 chamfers, H1 vertical sides, 110-high V bottom to apex at H3; H = H2+50+H1+110+H3.
- Published gross properties: Nihon Koatsu 2024 諸元表 PDF pp3–4 (Ac cm², yuc/ylc cm, Ic cm⁴, Wuc/Wlc cm³).
  **All 40 areas exact; Ic max |Δ| 0.0074 %; yb max |Δ| 0.48 mm** (x.x5 cm rounding ties).
- Pinned: Chubu prints AS19 H2 = 106; chain closure, Asahi Danke (JIS A 5373-2010) table and published A = 3096 cm²
  all give 160. Used 160.
- The 2025.09 Chubu edition removed the table (defers to PCCEN JIS A 5373-2016 handbook, 2020). Whether 2016 changed
  dimensions is unverified; the 2024 producer sheet still uses these values.
- Support-side H2 is 140 for all hollow types (Asahi Danke note); only midspan modelled.

#### Bi-pre trial girders
- GIFs img3/img11 at 475 px; read after 4× upscale. I: 25/30/35 m = 800 wide flanges, 200 web, tapers 60(run 200)+90(run 100);
  40/45/50 m = 1000 wide, 210 web, tapers 90(run 300)+120(run 95). Flange edge 210/230/250/250/270/270; 30 mm top set-back
  and 30 mm lip (horizontal-step convention). Printed clear webs 130/190/300/330/590 all close; I45 only prints 1400 total,
  chain 270/90/120/440/120/90/270 scaled (estimate).
- Hollow: 750 body, 850 ledge (100 edge + 50×50 splay), void 370 wide, top slab 200, sides 375/475/625, 75 V, apex 200.

#### Taiwan DGH PCI Types I–VII
- 臺灣公路工程 38(4-5) May 2012 pp.152–155, PDF pp11–12: 圖2 and 表4 (cm). GTF/GBF/GHT/TFT/BFT/GWB/H1/H3/F2;
  H2 = F1 = 0 for all; F2 = (GBF−GWB)/2 checked for all 7. GBL/GBH are end-block lengths (excluded).
- Type I: figure prints bottom taper 18 cm, table H3 = 19 cm → table used, conflict pinned (≈20 cm² area).
- Types VI and VII are both 45 m; article recommends dropping VII. Standard declared no longer applicable → historic.

### Leads / not implemented
- SMC Preconcrete PC橋げた PDF: connection timeout (blocked).
- Taipei DORTS 捷運 Wenhu Neihu precast U-girder: only overall dims (4.3/4.088/1.3/0.24 m) and A = 1.58 m², Yc = 0.39 m,
  Iz = 0.25 m⁴; outline undimensioned → lead.
- Nihon Koatsu 軽荷重スラブ橋げた (JIS 100 kN) / NKL slab: no public spec sheet.
- PCCEN 2020 handbook (JIS A 5373-2016) purchase-only.
- MLIT 2018 precast guideline: forms only (PCコンポ, Uコンポ, バルブT), no dimensions.

## Vietnam, Cambodia, Laos, Myanmar, Thailand

This pass added **27 profiles**: 20 Thai DOH, 5 Vietnamese (from producer drawings) and 1 Cambodian (from a thesis). The count of 27 includes IG20, which is a resolved duplicate of the existing Thai 20 m girder. Laos and Myanmar have no implemented profile, so their packages were not created. Every dimension below was read visually from rendered pages or crops.

### Thailand: DOH Standard Drawings, 2015 Revision (2018 Edition)

- **Source.** The PDF is `sources/expansion/round2/th/doh-std-2015.pdf`, SHA-256 `7ac8bea1…73bd2`. It was retrieved from the Wayback snapshot (20240806) of the doh.go.th URL. It is a scanned raster, and around the bridge sheets the PDF page is the sheet number + 17. The index is on PDF p5–6.
- **PG-101, PC plank girder (sheet 208/R1, PDF p225).** The table gives h/h1/h2 in m:

  | Span | h | h1 | h2 |
  |---|---|---|---|
  | 5 m | 0.18 | 0.05 | 0.09 |
  | 6 m | 0.21 | 0.05 | 0.09 |
  | 7 m | 0.24 | 0.05 | 0.09 |
  | 8 m | 0.28 | 0.05 | 0.10 |
  | 9 m | 0.31 | 0.08 | 0.14 |
  | 10 m | 0.35 | 0.08 | 0.14 |
  | 12 m | 0.45 | 0.08 | 0.14 |

  - Common dimensions: soffit 0.99, key inset 0.07 at h2, top inset 0.045 (top 0.90).
  - Only the 12 m plank has voids: three Ø0.15 at mid-depth. Interior holes are at ±0.25 and 0. Exterior holes follow the chain 0.24/0.30/0.27/0.18 from the keyed edge.
  - Exterior planks have one keyed side (0.51 + 0.48 about the CG line).
  - Convention: 20 mm soffit chamfers, from the sheet's "CHAMFER 0.02 (TYP.)" note and the rounded soffit corners that are drawn.
  - 14 profiles: `PG{5,6,7,8,9,10,12}-{INT,EXT}`.
- **BB-101, PC box beam, 15/20 m (sheet 212/R1, PDF p229).**
  - Table (m):

    | Span | b1 | b2 | b3 (int/ext) | h1 | h2 | h3 | h4 | h5 | h6 | h7 | h |
    |---|---|---|---|---|---|---|---|---|---|---|---|
    | 15 m | 0.18 | 0.10 | 0.29 / 0.36 | 0.18 | 0.28 | 0.14 | 0.09 | 0.10 | 0.25 | 0.35 | 0.60 |
    | 20 m | 0.18 | 0.10 | 0.29 / 0.36 | 0.18 | 0.36 | 0.16 | 0.08 | 0.20 | 0.30 | 0.40 | 0.70 |

  - The chains close in both directions: vertically h3+2h4+h5+h1 = h, and h2 = 2h4+h5. Horizontally the bottom chain gives 0.99 for interior beams (two keys) and for exterior beams (one key).
  - The key has the same shape as on the plank, with a 45° diagonal 70 mm across and 70 mm up.
  - There is a "0.02" callout at every top corner that I could not place. I ignored it; the area effect is below 0.1%.
  - 4 profiles.
- **IG-103, 15 m I-girder (sheet 217/R1, PDF p234, section D-D).**
  - Dimensions: 750 deep, 450 top, 150 web (top chain 0.15/0.15/0.15), 500 bottom.
  - Vertical chain: 100/75/225/150/200.
  - This corrects the old JSON remark that the web is about 175 mm.
- **IG-205, 20 m I-girder (sheet 223/R1, PDF p240).**
  - Vertical chain: 100/75/**625/200**/200; top chain 0.1375/0.175/0.1375.
  - The existing `ThDOHIGirderSection` models the lower 825 mm as a plain web. The new `ThDohIGirderR2Section("IG20")` is the same girder with the splay resolved, so the integrator should count only one of the two.
  - I-girder soffit chamfers are drawn but not dimensioned. I used 20 mm as an estimate.
- **Checks.** DOH publishes no section properties. The tests reproduce the analytic areas exactly, and the voided sections include their holes.

### Vietnam: Bê tông 620 Châu Thới producer drawings

The drawings are published as JPEG sheets on 620chauthoi.com, under the product pages *Dầm I* and *Dầm T*. They are held in `sources/expansion/round2/vn/c620/`, with SHA-256 values in the JSON. All dimensions are in mm, and the chains close in every case.

| Size | Source section | Transcription (mm) | Provenance |
|---|---|---|---|
| I33 (22TCN 272-05) | MẶT CẮT 4-4 | 1400 = 160 + 120 + 770 + 170 + 180; top 500, web 160, bottom 610; VÁT CẠNH 25×25 | transcribed |
| I24.54 | D-D | 1143 = 178 + 114 + 483 + 190 + 178; 410/178/558; 25 mm chamfer adopted from the I33 sheet | transcribed-with-convention |
| I18.6 | D-D | 700 = 50 + 85 + 75 + 220 + 100 + 145 + 25; top 390, 20×50 top rebates to a 430 flange; web 160; bottom 560; 25×25 chamfers | transcribed |
| T18.6 cải tiến | C-C (midspan) | 950 deep; 400-wide block 313 deep with a 30×30 rebate (top 340); web tapers 1:12 per face to a 200 soffit; R130 fillet | transcribed-with-convention |
| TN20 (T ngược) | giữa dầm | 750 = 30 + 160 + 70 + 250 + 70 + 70 + 100; base 980, web 160, flange 440, top 360; R70 fillet; vát góc 20×20 | transcribed-with-convention |

- **T18.6 check.** B-B (770 deep, 230 soffit) implies the same 306 mm web width under the block, which confirms the 1:12 reading.
- **T18.6 convention.** The ledge is only 47 mm wide, so the R130 arc is modelled as tangent to the web and ending at the block's bottom corner.
- **TN20 convention.** The sloping flange top meets the theoretical web intersection at 170 mm, and the R70 fillet is a true tangent arc at that point. Its tangent point is about 11 mm lower than the 240 implied by the 70 mm fillet-zone callout.
- **I24.54 note.** Its inch-derived values resemble AASHTO Type III. The 410 top and 116 haunch offsets are this producer's own values, and no identity with the US section is claimed.

### Cambodia: Kochi University of Technology thesis

- **Source.** VONG Seng (2006), hdl 10173/210, Fig. 3.3.2 on PDF p30 / printed p28. It shows girder TB_12_f60: 850 deep, top 580 with a 160 mm edge and a 200 mm flange zone, web 150 × 450, bottom 350 with a 120 mm edge and a 200 mm zone.
- **Status.** This is a research design for a 12 t self-weight limit. A real-scale girder was produced and monitored in Cambodia. It is not an MPWT standard.
- **Implementation.** Transcribed with sharp corners. Area 236 900 mm².

### Bounded negatives and leads

- **Vietnam, national standards.** Bộ GTVT/TEDI standard (định hình) drawings are only on paywalled libraries.
- **Vietnam, TNEC.** The typical sheet is partial: Super-T 2400/1750/700 with trough widths 590/432, a 990/920 hollow box, girder 12.5 at 700/400/163, and an inverted-T with a 980 base.
- **Vietnam, Super-T book.** The Lê Văn Lạc Super-T book scan (Cần Thơ) is illegible at 500 dpi.
- **Vietnam, older I33.** The UTC lecture gives an older post-tensioned I33: 1650 deep, 850 top, 650 bottom, 200 web. That is partial and is a different girder from 620's 1400 mm I33.
- **Thailand.** Pound Concrete multibeam gives w/W/D/T only, and T is undefined. The DRR rural-road drawings and CPAC were not searched.
- **Laos and Myanmar.** The JICA preparatory surveys (NR9, New Thaketa, Mekong connectivity) contain only steel or cast-in-situ alternatives. No precast standard sections were found.
- **Cambodia.** The Bridge Design Standard (AUSTROADS 1996 base) is available only as a Scribd copy and contains no girder drawings.

## Malaysia, Singapore, Indonesia, Mongolia

Retrieved and checked on 23 September 2026. Every dimension was read from rendered or upscaled page images. The WIKA voided-slab dimensions were measured from the vector paths of the brochure drawing.

### Implemented: 57 profiles

| Module / class | Sizes | Provenance | Source (PDF p / printed p) | Check against published properties |
|---|---|---|---|---|
| `my.jkr_prt.JkrPrtBeamSection` | PRT1, PRT2, PRT3 | transcribed | G-CAST 2020 p2; OKA 2018 p1 | A exact; Yb within 0.4 mm; I within 0.05 % |
| same | PRT-M1450…1800 (7) | transcribed-with-convention | OKA 2018 p1 | hw list matches; both area-range endpoints exact |
| `my.oka_m_beam.OkaMBeamSection` | M2–M10 (9) | transcribed | OKA 2018 p2 | A is −500 mm² (−0.12 to −0.16 %) for every row; Yb within 1.2 mm; I −0.27 to −0.50 %; the M10 area typo (−300 mm²) is pinned |
| `my.gcast_beams.GcastUBeamSection` | U1, U3, U5, U7–U12 (9) | fitted-reconstruction | G-CAST p3 | A within 0.1 %; Yb within 0.4 mm; I within 0.25 % |
| `my.gcast_beams.GcastTmBeamSection` | TM1040/1200/1360 × B1350/1450/1550 (9) | estimate | G-CAST p4 | A within 0.16 %; Yb within 1.9 mm; I within 0.45 % |
| `my.gcast_beams.GcastIBeamSection` | I1600 | transcribed | G-CAST p5 | A −0.06 %; Yb −0.2 mm; I −0.04 % |
| `my.gcast_beams.GcastTBeamSection` | T1800 | fitted-reconstruction | G-CAST p5 | A 0.00 %; Yb +0.2 mm; I +0.02 % |
| `id.r2_wika_voided_slab.WikaVoidedSlabSection` | VS57, VS62, VS66 | transcribed-with-convention | WIKA 2022 p19 | A −0.02 %; I −0.10 % or better |
| same | VS74 | fitted-reconstruction | WIKA 2022 p19 | A −0.02 %; I −0.07 % |
| `id.r2_waskita.WaskitaPcIGirderSection` | H90, H125, H140, H160, H170, H185, H210, H230 | transcribed-with-convention | Waskita 2026 p14 (printed 13) notation; p15 (printed 14) table | Analytic check only; no published properties |
| `id.r2_waskita.WaskitaVoidedSlabSection` | H57, H62, H66 (970); H52.5, H62.5 (1200) | estimate | Waskita 2026 p44–45 (printed 43–44) | Analytic check only |

Totals: 57 profiles. By provenance: transcribed 13, transcribed-with-convention 18, fitted-reconstruction 11, estimate 14.

### Transcriptions (source units = mm unless stated)

- **JKR PRT (G-CAST p2 = OKA p1).**
  - Top flange: 800 wide = 90 + 620 + 90, with a raised strip 30 high.
  - Flange edge 130; taper 35 high over 250 each side to a 300 web; the web runs to the soffit.
  - hw = 1055/1155/1205 for PRT1/2/3.
  - Printed properties: A = 458350/488350/503350; Yb = 722/774/800; I = 68.3/85.1/94.4 × 10⁹.
  - PRT-M: H = 1450, 1500, 1550, 1600, 1650, 1700, 1800; hw = H − 195; area range 518350–623350.
- **OKA M (p2).** The chain was read from the scan:
  - Base 970 with 20×20 chamfers; flange edge 160 with a 10 mm lean (10 + 315 + 80 = 405).
  - 50 taper; 80×80 splay; web 160; lower web 200/440/680 by group.
  - Top splay 60 high × 120 wide to a 400 top; 50×50 shoulders; 300 strip.
  - Within each group the top flange edge is 120/200/280 mm; each step adds 80 mm.
  - This resolves the Civilcon M unknowns (web, top flange and notch) for the OKA product. It does not prove that Civilcon uses the same geometry.
- **G-CAST U (p3).**
  - Base 970; 35 chamfer; outer batter 7:1.
  - Top block 325 = 40 + 235 + 50, with steps of 30, 15 and 19.
  - Inner thickening 407.
  - Floor: 150 at the centre, +50 to the break, +155 to the web toe (355).
  - Not printed, so fitted: web width 157.4 horizontal (the area increment gives 157.1) and break half-width 265.
- **G-CAST TM (p4).**
  - Bottom as the M-type (25 chamfer). Top splay 105 × 220.
  - The drawn flange has a crossfall (S.E.) and stepped edges. It is replaced by a uniform symmetric 87 mm flange, fitted to the areas.
- **G-CAST I1600 (p5).**
  - Top 1067 = 80 + 907 + 80. Stack 50/77/76/102; web 838 × 203.
  - Splays 102 × 102 (top) and 254 × 254 (bottom). Bottom edge 183 + 20 chamfer. Base 711.
  - The mm values are the AASHTO Type V inch values, but the top has shoulders. It is kept as a G-CAST profile, not as an alias of Type V.
- **G-CAST T1800 (p5).**
  - Base 660, 20 chamfer; bottom flange 250 including the chamfer; 205 splay; web 1120 × 250; 94 × 100 top splay; flange 131 at the root.
  - The tip thickness of 65 is fitted to A, and it then reproduces Yb and I.
  - The literal reading 250 + 20 gives Yb 928 against the published 944, so it was rejected.
- **WIKA VS (p19, cm).**
  - Printed: width 97; depth 57/62/66/74; void Ø25/30/30 (VS74 oval 30 wide); void-centre labels 28.5/31/33/39.
  - Printed A = 4397/4420/4784/5032 cm²; I = 1411372/1785520/2170299/2977551 cm⁴.
  - Measured from the vector drawing (0.618 pt/cm):
    - void centres at x = ±22.95 cm;
    - side key: half-width 48.5 below y = 30.13 cm and 45.5 above y = 34.05 cm;
    - soffit chamfer 1.50 × 1.06 cm.
  - VS74: the oval is drawn 36.6 cm high, which gives A +1.8 %. Its height is fitted to 38.0 cm, centred at the printed 39.
- **Waskita PC-I (p15).** Printed values (mm):

  | H (cm) | A | B | Tw1 | h1 | h2 | h3 | h4 |
  |---|---|---|---|---|---|---|---|
  | 90 | 550 | 650 | 170 | 130 | 75 | 100 | 125 |
  | 125 | 550 | 650 | 170 | 130 | 75 | 100 | 125 |
  | 140 | 700 | 650 | 180 | 130 | 75 | 100 | 225 |
  | 160 | 700 | 650 | 180 | 130 | 75 | 100 | 225 |
  | 170 | 800 | 700 | 200 | 130 | 120 | 250 | 250 |
  | 185 | 800 | 700 | 200 | 130 | 120 | 250 | 250 |
  | 210 | 800 | 700 | 200 | 130 | 120 | 250 | 250 |
  | 230 | 850 | 750 | 250 | 130 | 120 | 250 | 250 |

  - Top shoulders are 80 × 70 (p14 sketch). h1 is read as starting below the 70 mm shoulder level.
  - Tw2 and h5–h8 describe the end section and are not used.
  - Semi-T is not implemented because the table gives no depth H.
- **Waskita VS (p45).**
  - Type 1 (B 970): H 570/620/660; D 250/300/350.
  - Type 2 (B 1200): H 525/625; D 250/300.
  - All sizes: h = H/2, h1 25, b 50; h2 = 75/100/120 (Type 1) and 75/100 (Type 2).
  - Estimated: void positions (±240 for Type 1; 0 and ±320 for Type 2) and 25×25 chamfers.

### Remaining uncertainties

- The OKA and G-CAST drawings are raster images, read at 2–4× upscale. The G-CAST TM flange crossfall is not represented.
- For Waskita there are no properties to validate against. The h1 reading rests on the notation sketch.
- The WIKA VS lateral dimensions depend on the brochure's vector drawing being to scale. The four depths agree within 1.2 %, which supports this.

### Leads not implemented (one line each)

- **Hume Concrete (Malaysia):** catalogue at https://chuanhuat.com.my/w3/wp-content/uploads/2014/09/concreteBeams.pdf, 72 ppi raster. It has M2–M10, inverted T-beams (535–890 mm, 8 property rows) and I-beams I-5..I-7 and I-12..I-14 with properties. A UK-style inverted-T reconstruction leaves a constant +1055 mm² area and +1–2 % I residual, and the resolution is too low to resolve it. Needs a higher-resolution copy.
- **G-CAST TM end section** (320 mm web): not implemented, because it is not a midspan section.
- **Geoquest PRECAST-BEAMS-EN** (https://www.geoquest-group.com/wp-content/uploads/2019/12/PRECAST-BEAMS-EN_V01_BD.pdf): this is the Tierra Armada (Spain) catalogue (IL series etc.). It is a Europe-scope source, not Indonesian geometry. It was downloaded but not implemented.
- **Bina Marga Panduan Praktis Perencanaan Teknis Jembatan 02/M/BM/2021** (1536 pp, downloaded): worked design examples only. The bounded search found no standard girder table.
- **Bina Marga standard-drawing sets:** SE DJBM 15/2021 Gambar Standar and Suplemen 02/S/Pd/BM/2022 (binamarga.pu.go.id NSPK) are leads. Indexed text lists PTI voided slabs for 5–16 m, class A depths 310–740 and class B 280–710. Not retrieved.
- **Waskita 2026 remaining products:**
  - PC-U (p20): only A and B are given.
  - PC-T (p23): the drawing is unlabelled.
  - Semi-T: no depth given.
  - Segmental box Types 1/2 (p10–11): a segmental box, not a beam.
- **WIKA December 2017 bridge sheet** (wika-beton.co.id 03-5-BRIDGE.pdf): repeats the 2022 PC-I/U/VS data. It could refine the existing WIKA PC-U estimates (it has 4 U sizes with A/I). Not in my scope.
- **Singapore:** the LTA Civil Design Criteria has no standard beam sections, and no bridge-beam producer catalogue with dimensions was found (Coninco etc.). Bounded search; no profile.
- **Mongolia:** no new source beyond gap-mongolia.pdf (not extractable). Bounded search.
- **Not searched this pass:** Prestasi Concrete, Eastern Pretech and Adhi Persada Beton product sheets.

## Australia, New Zealand, Fiji, Papua New Guinea

### Implemented (9 profiles, all `aus`, new frozen-dataclass interface)

#### Queensland TMR transversely stressed PSC deck units — `aus/r2_tmr_deck_units.py` (`TmrDeckUnitSection`, 5 profiles, all `transcribed`)

Source: TMR Standard Drawings (CC BY 4.0), drawing 3 of 6 of each span set, SECTION C "Typical section inner units" (PDF p3), read visually at 250 dpi. Common rules: SD2042 drawing 2 of 2 (PDF p2) §8(a) "The chamfer for the void shall be 75mm x 75mm"; §11 "596mm wide deck units".

| SIZE | Depth | Void (bottom / height / top, side cover) | Drawings (span) | Rev/date |
|---|---:|---|---|---|
| 500 | 500 | solid | SD2050 (10 m), SD2051 (11 m) | D 07/25 |
| 540 | 540 | solid | SD2052 (12 m), SD2053 (13 m) | E/D 07/25 |
| 650 | 650 | 240 / 220 / 190, 120 | SD2055 (15 m) | C 07/25 |
| 760 | 760 | 240 / 330 / 190, 120 | SD2059 (19 m) | C 7/25 |
| 1100 | 1100 | 240 / 670 / 190, 120 | SD2065 (25 m) | B 7/18 |

All: width 596, 25x25 soffit chamfers (top corners square), void 356 wide with 75x75 chamfers. Excluded: end recesses/hold-down holes, 90 dia transverse stressing holes. Outer units share the precast section (kerb/parapet is cast in situ). Identical-outline span pairs (10/11, 12/13 m) counted once. No published properties; analytic area checks only. Not retrieved: 14, 16–18, 20–24 m sets (drawing numbers 2054/2056–2058/2060–2064 inferred, unverified) — TMR index and those URLs return a Cloudflare challenge.

#### TfNSW Country Bridge Solutions 600 mm double-T deck modules — `aus/r2_tfnsw_cbs_modules.py` (`TfnswCbsModuleSection`, 4 profiles)

Source: TfNSW/RMS "Country Bridge Solutions – Modular Bridge Drawings", approved 07.10.2016, published 2022: Type 1 sets 8/10/12 m (PRECAST MODULE CONCRETE – SHEET C, MBxxDL54, PDF p28, Sections 1 and 3 — identical across spans), Type 2 10 m (SHEET B, PDF p25), Type 3 10 m (SHEET B, PDF p27). Read at 300 dpi.

| SIZE | Provenance | Overall width | Notes |
|---|---|---:|---|
| T1-internal | transcribed | 2470 | 1650 body + 2 × 410×75 stubs |
| T1-external | transcribed-with-convention | 2060 | 755 kerb flush with body edge + 1 stub |
| T2-external | transcribed-with-convention | 2410 | 325 kerb overhang (450 at soffit) + 1675 body + 1 stub |
| T3-external | transcribed-with-convention | 2420 | kerb + full 180 deck flange, no closure pour |

Printed common: depth 600, webs 320 at soffit, 810 gap, 17.6:1 batter (both faces lean outward upward; 100→79 and 810→760 chains close within 0.3 mm), top slab 160 over 760 void, stub 410×75 whose top is 160 below deck top, 20×20 soffit chamfers, 20×20 void-top fillets, 40×40 flange fillets, 15×15 flange-tip chamfers. Conventions: chamfer legs horizontal/vertical; kerb outer corners 15×15; kerb 5 mm top detail and 10 mm drainage recess ignored; origin at centre of 810 gap (not centroid for external modules). Pinned: Type 2 top chain 325+107 = 432 vs 429.3 implied by soffit chain 450 and batter (2.7 mm); soffit chain used. Mass check: Type 1 internal 13.1/16.4/19.7 t for 8/10/12 m sets at 2550 kg/m³ → 0.647 m² per metre from the increment (±3% rounding); implemented area 0.6414 m² (−0.9%).

### Searched, not implementable (bounded effort)

- **NZTA red-folder standard drawings** (e.g. D87-0-111-10-7004-4R6 U-beams; D00 Red Folder 3 index; RR252): nzta.govt.nz assets now sit behind an Incapsula bot challenge for curl/WebFetch. Not bypassed. RR364 (already held) is fully used by existing nz classes except the 650/900 outer units.
- **Stahlton double-tee rural bridge sheet** (NZ): section not dimensioned beyond abutment; unit width 1.8–2.1 m, 1000 dimension ambiguous. Lead only.
- **Humes NZ Double T bridge brochure**: 800 mm deep × 2 m wide, 8–18 m; no flange/web dimensions. Lead only.
- **Tasmania DSG Standardised Plank Design guide Rev05** (rectangular transversely post-tensioned planks): Cloudflare challenge; lead.
- **Main Roads WA Structures Engineering Design Manual**: plank bridges (6/9/12 m standard planks), modified NAASRA Type 2 I-beam 915 deep, Teeroff 750–2250; figures are GA drawings without beam dimensions. Lead.
- **TfNSW B0201 Super-T standard sizes**: downloaded (1 p), not transcribed — Super-T already in legacy `aus`; NSW flange variant supported there.
- **Fiji**: FRA Structures Design Guide Supplement v3.0 — no beam sections. **PNG**: ADB 43200-012 TA report blocked (Cloudflare). No fj/pg package created.
