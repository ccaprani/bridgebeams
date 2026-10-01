# PDF backlog: visual transcription and implementation, 22 September 2026

> **Follow-up after visual review:** Norway and four NZ hollow-core variants are now implemented; see [the visual follow-up](visual-followup-norway-nz.md). The original transcription below is retained as source history.

Four existing source PDFs were recovered from `/tmp` into persistent ignored working materials under `sources/expansion/pdf-backlog/`. The published text and drawings were inspected as rendered images. This pass supplies 28 section records and 17 translated drawing terms in [the machine-readable transcription](data/pdf-transcriptions.json), fixes the NZ Super-T topology, adds two NZ I-beams, and implements five Qatar Q-beam reconstructions.

These results supersede conflicting statements in older research briefs and HANDOFF.md. A numerical dimension is reported as read only when its leader/feature was identified visually. Derived numbers and approximation choices are identified separately. No values were interpolated between beam types. Existing local PDFs were reused; the links below identify the publisher but their current HTTP availability was not checked in this PDF task.

## Source identity and page conventions

Page numbers below are one-based PDF pages. Zero-based indices and printed sheet labels are also stored in JSON. Original PDFs, full-page renders and selected detailed crops are retained under the ignored directory, not embedded into the package or repository documentation. Publication does not establish an open redistribution licence for the original drawings.

| Key | Publisher and document | PDF pages | Local PDF | SHA-256 |
|---|---|---:|---|---|
| QA | [Ashghal SD 5-1-101 Rev 1, October 2013](https://www.ashghal.gov.qa/en/SDDDocumentsLibrary/SD%205-1-101%20Rev%201%20Q-Girder%20Sections.pdf) | 1 | `qatar-q-girders.pdf` | `8b2e22c2af37186dde1211a839823fa1e54e2706335e39ed61303ed7756eebc5` |
| NZ | [NZTA Research Report 364, December 2008](https://www.nzta.govt.nz/resources/research/reports/364/) | 57 | `nz-rr364.pdf` | `ea199fa1dfa3272c8c31bbe8ee200c616536fae4a25418ae084d51841b01fd6d` |
| NO | [Statens vegvesen V426, Prefabrikkerte brubjelker](https://www.vegvesen.no/globalassets/fag/handboker/hb-v426-prefabrikkerte-brubjelker.pdf) | 96 | `norway-v426.pdf` | `8e759c194e284791736e3a717f7f340f5ea85bdd5c77d67c6ba1fe559c2ca77e` |
| JP | [PCCEN Tohoku/MLIT, pretensioned beam-bridge girder design and construction in deicing-salt regions, 2017-03-23](https://www.thr.mlit.go.jp/road/sesaku/manual/20170323point2.pdf) | 44 | `japan-thr-pccen.pdf` | `f6be892e0d876ce6c895688d693602ed24a338fb16fd46d3bec9aba35dc3db6a` |

## Qatar Q-girders: all five lower zones and property table read

The section is an **open-top U**, with outward wings and a valley in the top surface of the bottom concrete. The valley is lowest at the centre and rises toward the webs. The earlier "tent peak at centre" interpretation is reversed. The repeated dimension chain **200 + 1069 + 200 does not specify overall flange width**: it defines the haunch references. Note 3 and the property-table sketch specify **2150 mm** nominal overall flange width, maximum 2300 mm and minimum spacing 1800 mm. The last number is a spacing requirement, not an instruction to set a 1800 mm flange.

| Type | Depth | Base width callout | Valley above soffit | Rise to web junction | Indicative span, m |
|---|---:|---:|---:|---:|---|
| T1 | 800 | 939 | 290 | 71 | 12–17 |
| T2 | 1050 | 892 | 290 | 67 | 14–21 |
| T3 | 1250 | 854 | 310 | 64 | 16–24 |
| T4 | 1550 | 797 | 310 | 58 | 20–28 |
| T5 | 1900 | 731 | 375 | 53 | 25–34 |

All dimensions above are mm except the final column. T2–T4 are direct visual readings, replacing the previous interpolation proposal. Common callouts: precast flange thickness **117**, top clear opening at ledge **840**, ledge **25 × 25**, slope triangle **10.55 vertical : 1 horizontal**, nominal web dimension **125**, haunch **200 × 75**, corner chamfer **13 × 13**. Bottom corners permit nominal **10 radius OR 13 × 13 chamfer**. Note 7's typical **200 mm slab** is the in-situ deck, not the precast flange thickness.

The source table is headed “OPEN FLANGE – SECTION PROPERTIES BASED ON TOP FLANGE WIDTH OF 2150 mm.” Its units are **I ×10¹⁰ mm⁴** and **Z ×10⁷ mm³**; these must not be confused with the separate TY drawing's disputed units.

| Type | A, mm² | Yb, mm | I, ×10¹⁰ mm⁴ | Zt, ×10⁷ mm³ | Zb, ×10⁷ mm³ |
|---|---:|---:|---:|---:|---:|
| T1 | 565861 | 381 | 4.043 | 9.650 | 10.613 |
| T2 | 611622 | 496 | 8.182 | 14.770 | 16.497 |
| T3 | 661823 | 588 | 12.761 | 19.276 | 21.702 |
| T4 | 716068 | 740 | 21.633 | 26.707 | 29.234 |
| T5 | 815801 | 903 | 36.251 | 36.360 | 40.145 |

`QaQBeamSection("T1"…"T5")` implements a **documented reconstruction** at 2150 mm width. It preserves each type's independent base and valley dimensions, the 840 mm opening at the 25 mm ledge, and parallel web faces at 1:10.55. The rounded dimensions do not close exactly: the resulting normal web is approximately 122–123 mm, rather than the nominal 125 mm callout. This limitation is stated in both code and source data. The reconstruction uses the permitted chamfer alternative; no dimensions were fitted to the property table.

| Type | Area residual, % | Centroid residual, % | Ixx residual, % |
|---|---:|---:|---:|
| T1 | +0.876142 | +0.810067 | +1.161617 |
| T2 | +0.686861 | +0.822894 | +1.257488 |
| T3 | +0.502217 | +0.848838 | +1.238156 |
| T4 | +0.207972 | +0.819743 | +1.111543 |
| T5 | +0.085155 | +0.640268 | +1.068144 |

Exact calculated residuals are stored in `src/bridgebeams/qa/data/q_beams.json`; rounded display above is informational. Tests use 1% area, 1% centroid and 1.5% inertia tolerances, plus an independent integrated-area check and open-void topology checks. Source span ranges do not establish capacity.

Evidence renders: `qatar-sheet.png`, `qatar-T1.png` through `qatar-T5.png`, `qatar-table.png`, `qatar-notes.png`, `qatar-detail.png`. Some type crops include a neighbouring section's depth dimension at the far left; the type's own caption identifies its depth.

## New Zealand: corrected Super-T geometry and two I-beams

The handoff's page 26, S1.25, is **unit data**, not the 1225 mm profile. The geometry is on:

| PDF page / index | Drawing | Type | Flange width | Base | Valley level | Valley rise | Lower clear opening |
|---|---|---|---:|---:|---:|---:|---:|
| 8 / 7 | S1.01 | 1025, 20/22.5 m arrangement | 2490 | 852 | 240 | 67 | 709 |
| 15 / 14 | S1.11 | 1225, 25/27.5 m arrangement | 2490 | 814 | 260 | 64 | 674 |
| 22 / 21 | S1.21 | 1225, 30 m arrangement | 1990 | 814 | 260 | 64 | 674 |

Common callouts: 840 mm top opening at ledge, 100 mm nominal webs, 100 mm precast flange, **100 horizontal × 75 vertical upper haunch**, slope **10.56:1**, and **20 mm chamfer or radius** at lower corners and flange tips. The former code treated 100×75 as bottom chamfers, kept the 1025 base for the 1225, and filled the central void with solid concrete. All three errors are corrected in `nz/super_t.py`. The prior comments attributing this interpretation to a user reading are superseded by the source images; this does not imply the user supplied the erroneous polygon interpretation.

Detail A specifies a **15 mm ledge** and **45 MAX** depth. It does not give an exact ledge depth. The current geometry therefore remains an explicit gross-profile approximation: ledge omitted, 840 mm aperture placed at the top surface, slightly adjusted inner-web taper. The lower valley, outer taper and top haunch are retained. No source property table was located. Tests verify actual absence of concrete through the open top and centre valley, two separate webs on a horizontal cut, and independent area integration. Use `NzSuperTSection(1225, top_width=1990)` for S1.21.

The I-beams are fully dimensioned on pages 45 and 51:

| PDF page / drawing | Depth | Top width | Top thickness | Upper haunch height | Web width | Clear web height | Bottom width | Bottom thickness | Lower haunch height |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 45 / S4.01 | 1500 | 375 | 100 | 75 | 175 | 1005 | 475 | 170 | 150 |
| 51 / S4.10 | 1600 | 470 | 110 | 145 | 180 | 975 | 620 | 150 | 220 |

`NzIBeamSection(1500/1600)` implements these external profiles, choosing the source's 20×20 bottom-chamfer alternative. Height stacks close exactly. Analytic area fixtures sum rectangles and trapezoids and subtract the two chamfer triangles; horizontal-cut tests verify top, web and bottom widths. Local holes, ducts, reinforcement and deck are omitted. No independent published A/I table was found.

### NZ hollow-core profiles transcribed, not implemented

| Page / drawing | Inner unit | Overall dimensions | Void |
|---|---|---|---|
| 29 / S2.01 | Single hollow-core 650 | depth 650, top 1094, bottom 1138 | top cover 140, bottom cover 130, height 380, vertical side 180, four 100×100 splays, flat width 630, maximum width 830 (derived 100+630+100) |
| 34 / S2.10 | Single hollow-core 900 | depth 900, top 1094, bottom 1138 | top cover 140, bottom cover 155, height 605, vertical side 405, four 100×100 splays, flat width 630, maximum width 830 |
| 40 / S3.01 | Double hollow-core **587** | depth 587, width 1144 | two 368 diameter voids, centres 308 and 836 from left, 294 above soffit, 528 apart |

The double hollow-core depth is **587**, not 576 as in the older brief. The 650/900 outer edge units are asymmetric and differ from their inner units; the 587 edge unit has one void. Side keys, the sloping mould-release faces and drip-groove options still require a chosen explicit profile. The source allows a hexagonal alternative to the 587 circular void if specified area, cover, web thickness, location and weight are preserved. Source notes prohibit using the inner hollow-core units in isolation. These are genuine multiple variants, not missing national standards.

Evidence: `nz-rr364-p5.png` index; pages 8, 15, 22, 29, 34, 40, 45 and 51 rendered with matching filenames. All dimensions above were read from these sheets.

## Norway: the free handbook already contains ten section drawings

The retained V426 file has **96 pages with a useful text layer**, rather than being a drawings-only package. Printed/PDF pages **37–46**, Figure 3.3.2(a–j), provide the typical formwork and reinforcement cross-sections. The free copy therefore removes the handoff's supposed printed-copy/purchase dependency.

| Printed/PDF page | Original type label | Depth | Bottom width | Top width | NTB web width | Bottom flange height at web | Outer shoulder height |
|---|---|---:|---:|---:|---:|---:|---:|
| 37 | NTB800-400x1400 | 1400 | 800 | 400 | 220 | 265 | 197 |
| 38 | KTB570-400x1400 | 1400 | 570 | 400 | — | 265 | 197 |
| 39 | NTB1000-300x1200 | 1200 | 1000 | 300 | 220 | 265 | 173 |
| 40 | KTB1200 | 1200 | 670 | **320** | — | 265 | 173 |
| 41 | NTB1200-220x1000 | 1000 | 1200 | 220 | 220 | 265 | 150 |
| 42 | KTB1000 | 1000 | 770 | 280 | — | 265 | 150 |
| 43 | NTB1200-220x800 | 800 | 1200 | 220 | 220 | 265 | 150 |
| 44 | KTB800 | 800 | 770 | 280 | — | 265 | 150 |
| 45 | NTB1200-220x600 | 600 | 1200 | 220 | 220 | 265 | 150 |
| 46 | KTB600 | 600 | 770 | 280 | — | 265 | 150 |

The middle number in `NTB800-400x1400` is **top width 400**, not web thickness: the drawing explicitly gives the central stem as **220**. This invalidates the older brief's blanket designation interpretation. KTB sections are asymmetric, with a sloping exterior, so no constant web width is inferred in the table. “Outer shoulder height” includes the 40 mm step: outside vertical face heights are 157, 133 and 110 respectively. These terms are defined for transcription and are not a complete geometric construction.

For NTB/KTB1400, the top-zone vertical chain is **125 + 75**; for the 1200 sections it is **125 + 37**. The sections include small top recesses, bottom joint/rebate features (15/5/40 callouts), bottom chamfers, and reinforcement-cover leaders. Their exact line-to-line relationships must be resolved into coordinates before implementation; reading a number beside a bar does not make it a concrete dimension. In particular, the repeated 55/60/65 figures mostly locate reinforcement and must not be used as concrete flange thicknesses. No Norway module is added until those relationships are explicitly resolved. The page renders `norway-v426-p37.png` through `-p46.png` remove the former document-location blocker.

A further bounded high-resolution check of representative NTB1400 page 37 confirms the top recess as 30×30 and the lower rebate with 15+5 horizontal offsets over a 40 mm vertical drop. The bottom outer chamfer is drawn but its size is not specified by an identified concrete-outline leader on that page. The nearby 12 belongs to the stirrup/bottom reinforcement detail and is not a chamfer dimension. A handbook text search for chamfers/corners and K201/K202 did not recover a controlling size. Exact implementation therefore still needs the applicable form drawing or general chamfer note. Additional evidence is retained in `norway-p37-top.png` and `norway-p37-bottom.png`.

Selected translations (all 17 entries across Norway and Japan are stored in JSON):

| Original | English |
|---|---|
| Tverrsnitt og armering | Cross-section and reinforcement |
| Typisk form- og armeringstverrsnitt | Typical formwork and reinforcement cross-section |
| Horisontal stegarmering iht. N400 | Horizontal web reinforcement in accordance with N400 |
| Utsparing forutsettes utstøpt | Recess assumed to be filled with concrete/grout |
| Ekstra samv.bøyler ved ender | Additional composite-action stirrups at the ends |
| Spenntau | Prestressing strand |
| Alternativ bøyleutforming | Alternative stirrup configuration |

## Japan: separate stirrup dimensions from concrete dimensions

Relevant pages are **PDF 9–10 / printed 5–6**, not PDF 27–31. On PDF page 9 the separate right-hand sketches are reinforcement shapes: **240** is the central stirrup dimension, and **152/151** are horizontal returns of that stirrup. They are **not** a 240 mm concrete web and 152 mm flange thickness. The concrete web/bottom width is **300**, and overall top width is **800 = 20 + 760 + 20**.

PDF page 10/printed 6 shows standard concrete sections for BG19 (1000 deep), BG20/21 (1100), BG22/23 (1200). The concrete top-flange and haunch stack is 160 + 35. Existing `jp/data/jis_t_girders.json` already records web300/top800/top-thickness160/haunch35 from the Chubu source; no Japanese implementation change is required. This correction targets the stale research brief.

The page-9 text says using coated prestressing steel and epoxy-coated reinforcement increases their outside diameters, potentially causing interference and end cracking. It specifies moving the middle prestressing-steel row **7 mm horizontally toward the girder centre**, and modifying stirrups to secure **25 and 30 mm clear cover**. The page-10 note says the left half of each illustrated section represents the girder end region. BG19–BG23 need added debonded strands; BG24 requires individual treatment including reconsideration of strand arrangement. These reinforcement changes must not be turned into a new universal concrete section.

| Original | English |
|---|---|
| 設計上の留意点 | Points to note in design |
| ＰＣ鋼材位置および鉄筋形状 | Position of prestressing steel and shape of reinforcing bars |
| 標準桁仕様での配置確認（BG19の例） | Arrangement check for standard girder specification (BG19 example) |
| 被覆ＰＣ鋼材を使用したＰＣ桁への変更仕様（BG19の例） | Modified specification for a PC girder using coated prestressing steel (BG19 example) |
| 支間中央部断面図 | Cross-section at midspan |
| 鉄筋間隔 / PC鋼材間隔 | Reinforcing-bar spacing / prestressing-steel spacing |
| ボンドレス鋼材の追加 | Addition of debonded prestressing steel |
| 横締孔 | Transverse prestressing hole |
| ベントアップ | Bent-up prestressing strands |

Evidence: `japan-thr-pccen-p9.png`, `japan-thr-pccen-p10.png`, `japan-bg19-detail.png`. This pass does not assert that AG reinforcement arrangements are identical to BG or establish an edition-to-edition identity from these figures alone.

## Verification performed and remaining work

Targeted execution with `/home/ccaprani/anaconda3/envs/pybridge/bin/python` passed **10 NZ Super-T tests**, **10 Qatar Q-beam tests**, and **3 NZ I-beam tests**. Qatar tests compare against independently transcribed published area, centroid and Ixx; both NZ families use analytic area and actual-topology checks because no source property table was found. Root integration is responsible for the full suite and public exports. No commits were made by this PDF worker.

Remaining bounded tasks are concrete: fully resolve Norway rebates/chamfers and asymmetric KTB slopes before coding; select and trace NZ hollow-core inner/outer unit variants; decide whether the NZ Super-T formwork ledge needs a user-defined depth rather than the explicitly omitted gross-profile detail. Qatar's nominal125-versus-reconstructed122–123 web discrepancy remains documented instead of being silently calibrated away. Purchase is not needed to read the Norwegian standard section drawings already recovered here.
