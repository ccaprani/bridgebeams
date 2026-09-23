# Round 2, Europe: new precast bridge-beam sources and implementations (23 September 2026)

Machine-readable companion: `docs/research/data/round2-europe-2026-09.json`. Each
family's full transcription is in its own data file. These files record the
source URL, local path, SHA-256, PDF page, dimensions in source units,
published values, geometry notes and residuals. This record gives the overview
and the judgement calls. **Status: useful, not authoritative.** Every
`estimate` and `fitted-reconstruction` profile needs owner review before any
structural use.

**Result: 381 profiles in 42 classes.** By provenance: transcribed 70,
transcribed-with-convention 160, fitted-reconstruction 45, estimate 106. The
round adds seven new country packages (`it`, `fr`, `dk`, `ua`, `bg`, `lt`, `hr`).
It extends nine existing packages (`pl`, `ro`, `es`, `nl`, `gr`, `uk`, `hu`,
`tr`, `ru`) through new modules; files in existing packages use the `r2_`
prefix. The new tests pass: 1224 tests across 19 files.

## Method

Four retrieval agents covered west-central, Romance, east and UK/Nordic
Europe. Their tables are `scratchpad/r2eu/{west-central,romance,east,uk-nordic}.md`
and the key rows are reproduced below. They searched in native languages and
downloaded to `sources/expansion/round2/<cc>/`. The shared WebSearch quota of
200 calls ran out partway through the round. After that, retrieval used direct
fetches of known domains, so "dry" verdicts for SI, ME, MK, LV, LU, CH, SE and
IS are weak evidence. Implementation agents and the main thread then read
every coded dimension from rendered pages. Vector PDFs were measured with
PyMuPDF path extraction. Raster sketches were traced with masks and scaled by
the printed dimensions. Where a source publishes properties (area, centroid,
I, mass per metre or volume), the model was checked against them. Individual
discrepancies are pinned in tests; tolerances were not widened to hide them.
No file under `sources/` was deleted.

## Families implemented

| Class | Profiles | Provenance | Source (page) | Validation |
|---|---:|---|---|---|
| `pl.r2_pekabex_mg_t.PekabexMgtSection` | 10 (MG-T18…46) | estimate | Pekabex/Mosty Gdańsk MG-T catalogue 2023, PDF p3 section C–C, p6 table | Only 2390 top, 220 web and H are printed; other dimensions scaled from the to-scale vector outline. V/Lc ÷ span area = 0.95–1.08 (includes the 450-web support zones) |
| `ro.r2_somaco.SomacoGirderSection` | 5 (GP 52E, 95E, 105E, 93, 220-40) | estimate | Somaco 2025 catalogue pp3–4 vector schematics | Schematics shown to be to scale: IPTANA GP42/72 reproduce the dimensioned ASA sections. V/L residuals: 52E +0.1 %, 105E 0.0 %, 93 −3.3 %, 95E −8.9 % (pinned), GP220 −17 % (end blocks included in V) |
| `ro.r2_prebet.PrebetGirderSection` | 21 | 11 transcribed, 10 with-convention | Prebet Aiud website CAD drawings (7 JPGs) | Chains close; T103 chain 102.4 cm vs 103 and the T95-EC 51/50 width conflict are pinned; relationship to ASA IPTANA recorded |
| `es.r2_tierra.TierraBeamSection` | 16 (IL, IP, IP-A, TPP, TA..A) | estimate | Tierra Armada "Precast & Prestressed Beam Bridges" (2012) pp3, 4, 5, 11 | Sketches to scale within 1 %; no properties published |
| `es.r2_prethor.Prethor{Vi,Va,Vu,Vc,Vaa}Section` | 77 | estimate / fitted-reconstruction | Dossier Prethor 2020 pp59–70 | P (t/m) at 2.5 t/m³: unfitted VI/VA within 0.7 %; one slab thickness fitted per family (≤ 1.4 cm change); VUP-120, VCP80/220-95 and VAA-A pinned |
| `it.paver.PaverBeamSection` | 28 (VHP, UHP, HP100, HTP, IHP, THP) | estimate | Paver Via 2021 brochure pp3–7 plus UHP/HTP/HP125 sheets | Model vs traced sketch area within 1–2 %; no properties published |
| `nl.r2_haitsma.HaitsmaHkpSection` | 10 (HKP-600…1400) | transcribed-with-convention | HKP folder p4 (table + sketch) | A −0.05 %, v ≤ 0.7 mm, I −0.05…−0.09 % for all ten |
| `nl.r2_haitsma.HaitsmaHbmSection`, `HaitsmaHgrSection` | 2 + 1 | transcribed | April 2009 1:10 vector drawings | Printed chains reproduced; the HBM folder table conflict is pinned |
| `nl.r2_spanbeton.*` (SKK, PIQ, SJP, SJP-flex, SRP, ZIP, ZIPXL) | 67 | transcribed-with-convention | Spanbeton project sheets (Wayback 2016, byte-identical) | Full Ab/Zb/Ib tables; discrepancy bands pinned (PIQ, SRP I, ZIPXL 1000–1700); self-weight agrees within 0.4–1.5 % |
| `fr.afgc_vipp.AfgcVippBeamSection` | 2 (support, mid-span) | transcribed | AFGC F-04 "Recalculs des VIPP" (2010) p7 Fig. 3 | One surveyed beam, asymmetric as measured; chain-vs-total conflicts pinned |
| `gr.r2_projects.GrProjectGirderSection` | 2 | 1 transcribed, 1 with-convention | Dervenakia G3 tender description p35; NTUA Eleftheriou 2020 p19 Σχήμα 9 | Chains close; project-specific, not national families |
| `dk.crh_ot.CrhOtBeamSection` | 10 (OT 118/500…1400) | transcribed-with-convention | CRH OT-bjælker product page image | Outline fully dimensioned; **100 mm depth steps are a convention**, since the source gives a 500–1400 range |
| `uk.r2_fpmccann.*` (TY, TYE, Y, YE, MY, MYE, SY, W, Box) | 84 | transcribed / with-convention / fitted (MY, MYE) | FP McCann Precast Bridge Beams v1.0 (2025) pp6–15 | Area, Yb, Zt and Zb per size; W family −0.8 % area pinned; comparison with Banagher (ie) recorded per family |
| `ua.i_beams.{UaB40,ThreeBet,UaBm}BeamSection` | 17 | transcribed / with-convention | NIDI rebuilding recommendations 2022; 3 Бетони leaflet; Kovalska 2020; Oberbeton | 3Bet-90 area within 0.18 % of V/L; 3Bet-120 +1.4 % pinned |
| `bg.rila_gt.RilaGtSection`, `bg.zbe_mg.ZbeMgSection` | 5 + 1 | transcribed / with-convention | Rila and ZBE product drawings | Chains close; ГТ185 mean edge height 185.5 pinned |
| `lt.tilsta.TilstaSijaSection` | 4 | transcribed / with-convention | Tilsta 2025 catalogue pp4–7 (vector 1:50) | S-850 matches 0.29 m³/m; the S-1000 note mismatch (+22 %) is pinned |
| `hr.viadukt_san.ViaduktSanSection` | 3 | with-convention / estimate (210/75) | TVZ teaching notes p4 reproducing Viadukt SAN girders | Walls printed; voids of 210/75 scaled |
| `hu.r2_sw_shp.SwShpSection` | 3 | transcribed-with-convention | SW Umwelttechnik SHP catalogue pp2–4 | Solid, not voided (the loops are stirrups); t/m slope within 1 % |
| `tr.r2_itu_tip.ItuTipBeamSection` | 9 (TİP I–III × A–C) | transcribed / with-convention | ITU M.Sc. thesis (Sarsık 2008) pp20–23 | Published A, yb and I (alone and composite) match; TİP III 13.5→13.0 chain fix is pinned; issuing authority not stated |
| `ru.r2_su3503_b12.Su3503B12Section` | 4 | transcribed / with-convention | Series 3.503.1-81 Vyp. 5-1 (1988) pp9–25 | Midspan area × 12 m is 3.0–3.5 % below published V (the ends), pinned |

## Judgement calls to review

- **Haitsma HKP edition conflict.** The folder table and its sketch (230 mm top
  slab, 155 mm bottom slab, 10 mm side step) reproduce the published A/v/I
  within 0.1 %. The April 2009 1:20 drawings (250/160 slabs, solid HKP-600)
  would not. The folder edition is implemented; the drawing edition is recorded
  only. The 10 mm side step is modelled as a recess over the top 300 mm. This
  closes a constant 6000 mm² gap at every depth.
- **Haitsma HGKO** duplicates the implemented HKO digit for digit, so it is not
  re-implemented.
- **Somaco IPTANA GP42/52/72/80** are the ASA IPTANA sections already
  implemented. Somaco's V/L confirms them: 0.130–0.133, 0.150, 0.386 and 0.407
  m² against ASA's 0.132, 0.154, 0.389 and 0.411 m². No duplicate class was
  added.
- **Pekabex MG-T.** All sizes share the flanges; only the web height changes.
  V/Lc steps between MG-T24 and MG-T27, which may mean thicker parts on the
  longer beams. This is unresolved.
- **Paver.** Intermediate depths extend the straight web lines common to the
  H170 and H80 sketches. HTP is implemented at C = 150 cm, although the sketch
  is drawn with about 120 cm. IHP120–140 are skipped because of a
  designation/depth conflict.
- **Tierra.** IP-200's label is illegible and was read from context. IP-255-A
  is IP-235-A with a web 200 mm longer (convention). TPP is modelled with the
  drawn 1.80 m lower wing, where the source gives a 1.20–1.80 range.
- **FP McCann vs Banagher.** Box SD and TY Type 2 are identical to Banagher.
  Y/YE/MY/MYE/SY/W differ; the existing ie Y/MY are fitted reconstructions.
  FP's own W drawing disagrees with FP's W table, which equals Banagher's.
- **CRH OT 118.** The depth enumeration is a convention (see table).
- **Greek and French sections** are single project or survey sections, not
  standard families.

## Leads not implemented

See `leads_not_implemented` in the JSON: 26 entries, one line each, with the
reason. The main ones:

- PL: GDDKiA type-object catalogue (T18–T27 deck assemblies; overlaps
  Mosty-Łódź T).
- CZ: KŠ PREFA and PREFA NB (envelope only).
- SK: Doprastav I/10 (no datasheet).
- BG: Stomanobeton (parametric).
- BY, MD, EE: envelope only.
- RU: 3.503.1-73 Klyazma (non-prestressed).
- PT: ISEP thesis (host unreachable).
- ES: Rubiera, PRECÓN, Hormipresa (host unreachable or gated).
- DE: DDR BT 70 type catalogue (Bundesarchiv, not digitised) and the BASt BT
  70/700 reports (bot-blocked).
- FI: Parma käyttöseloste p12 (not assessed).
- GB: Tarmac, Moore and Shay Murtagh, plus the legacy C&CA/MoT standards (not
  reached).

Held files with odd status, kept rather than deleted:

- `fr/kp1_katalog_gamme_poutres.pdf` is an HTML redirect page saved under a
  PDF name.
- `es/andece_artesas.pdf` is a 210-byte empty response.

## Downloads (key)

The retrieval tables list every download with its URL, local path, SHA-256 and
pages. The JSON `sources_downloaded_round2.key` lists the 26 files behind the
implemented families. The Spanbeton URLs are Wayback snapshots located through
the CDX API; the `id_` downloads are byte-identical to the local files.
