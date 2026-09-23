# HANDOFF — bridgebeams global collection

Updated 23 September 2026 (extraction round). Read before changing geometry or using old research
notes. This briefing supersedes the previous handoff: several source locators,
width interpretations and blocker claims in it were wrong.

## Repository and verification

- Repository: `~/projects/bridgebeams`; working branch `ukie-beams`.
- Remote: `github.com/ccaprani/bridgebeams`. Preserve the review-before-merge
  workflow. Do not merge or push to main. Keep changes on this branch or a
  new jurisdiction branch, with descriptive commits.
- Python: `/home/ccaprani/anaconda3/envs/pybridge/bin/python`.
- Full test suite (consolidated 23 September 2026; data-driven, same checks as the former 3369): **185 passed**,
  14 existing Matplotlib/Pyparsing deprecation warnings. Command:
  `timeout 180 /home/ccaprani/anaconda3/envs/pybridge/bin/python -m pytest tests/ -q`.
- Wheel checked outside the checkout: **all family JSON tables included**;
  Ontario, Minnesota and Washington classes construct from the installed wheel,
  and UK aliases resolve to the same Irish geometry classes. Earlier isolated
  wheel checks covered all 46 visual-review and 43 preceding expansion profiles.
  The new India and US AASHTO modules also built and constructed from isolated
  wheel installs; the India gross midspan area is 941250 mm².
  The old `bridgebeams.ukie.data` package-data rule silently omitted BE/JP/PL
  tables; the new wildcard includes each family's `data/*.json`.
- Sphinx command:
  `/home/ccaprani/anaconda3/envs/pybridge/bin/python tools/build_local_docs.py`.
  Strict (`-E -W`) build passed after the India, AASHTO, Brazil and multilingual research additions.
  Obsolete generated `gen/bridgebeams.ukie*` pages are excluded. Research
  includes use `:relative-docs: data/` so JSON links resolve as downloads.
- Pages site: `https://ccaprani.github.io/bridgebeams/coverage.html` contains
  the live interactive map. `.github/workflows/pages.yml` builds Sphinx from
  `ukie-beams`, installs Pandoc for the tutorial notebook, and publishes the
  static artifact. The `github-pages` deployment environment permits exactly
  `main` and `ukie-beams`; the repository homepage points to the site.

Latest commits on `ukie-beams` are `728a14b` (PCI AASHTO I–VI and Pakistan
follow-up), `cb1a82b` (Korea/Argentina/Philippines leads), `4717e74` (Brazilian
papers and DNIT guidance), and `d22bc38` (IFES São Domingos retrieval lead).
The latest Pages deployment for `d22bc38` passed. Live coverage data reads 301
profiles, 476 country-profile assignments, 122 researched jurisdictions and
233 source records. Brazil, Pakistan, the Philippines and Argentina remain
researched countries with zero implemented profiles; Korea has three existing
implemented profiles but its new PSC-I records are not yet implemented.

## Round 2 web retrieval and publication stance, 23 September 2026 (read first)

Owner's stance (Colin): keep pushing and do our best. The catalogue is
explicitly *not authoritative*, only useful, and this dev work is **not yet
released** (no corrections workflow). There is a prominent disclaimer in the
README, docs index, coverage map, package docstring and
`bridgebeams.DISCLAIMER`. `docs/source/disclaimer.md` explains the provenance
levels. **Never delete downloaded
reference material**, even irrelevant files or HTML block pages; record their
status instead.

Tests are data-driven. `tests/test_catalogue.py` walks every counted profile
(validity, orientation, voids, provenance, invalid sizes); each family file has one
aggregated `*_catalogue_checks` test that lists failing family/size cases; pinned source
discrepancies remain individually named tests. 30 legacy profiles (AU IGirder/Super-T,
13 IeU, 4 SU3503 I33) are stored clockwise and pinned as such in `KNOWN_CW`; consider
normalising them.

Owner review queue (round 3, 15 cards: source conflicts, scan readings, estimate
gallery, counting policy, manual downloads) is in the local `dims_review.html`
(build with `--with-review`); images and generator in `sources/review-2026-09-23/`.

Totals now: **1728 distinct profiles, 1903 country-profile assignments, 44
countries**. Every profile has `provenance`: 543 transcribed, 760
with-convention, 190 fitted, 235 estimate. The 301 pre-September profiles
were backfilled (`tests/test_provenance_legacy.py`). The coverage map shows the
provenance split and the per-family estimate counts.

Round 2 records are in `docs/research/round2-*-2026-09.md` and JSON (sources,
hashes, leads not implemented). Downloads are in `sources/expansion/round2/<cc>/`.
The whole session scratchpad (retrieval tables, extra PDFs, page renders) is
preserved at `sources/expansion/round2/session-scratch-20260923/`.

| Area | Added | Highlights / caveats |
|---|---:|---|
| US PCI national + Florida (`us/pci_*`, `us/fdot_*`) | 130 | Full PCI BDM 2011 App. B/C; FIB within 0.005%; PCI heavy double-T residuals pinned |
| US Texas + 11 states (`us/txdot_*`, `us/state_*`) | 433 | Independently checked against Brice et al. 2021 PCI Journal tables; PA contributes 140 (width × depth matrix) |
| Europe (new it, fr, dk, ua, bg, lt, hr; `r2_*` in pl, ro, es, nl, gr, uk, hu, tr, ru) | 381 | UK FP McCann (84) is GB-only; Spanbeton ZIPXL/PIQ/SRP table conflicts pinned; Paver, MG-T, Tierra, Somaco are estimates |
| Latin America (br, ar, cr; `mx/r2_*`) | 23 | DNIT IPR-751 PCP-15/20 exact; Pretensa all estimates |
| South Asia + Korea (pk, lk, bd; `kr/r2_*`) | 19 | NHA A–H come from a 2025 journal table; the original NHA sheets are only on Scribd |
| East/SE Asia + Oceania (vn, kh, my; `r2_*` in cn, jp, tw, th, id, aus) | 162 | JIS slab girders exact; Shanghai atlas is a 2021 draft; old Thai IG-205 class superseded for counting by `ThDohIGirderR2Section("IG20")` |
| Africa + Middle East (ma; `qa/r2_*`) | 24 | Ashghal TY/TYE now public; SADET estimates |

Integration decisions: a round-2 Delhi–Vadodara duplicate was removed (same
PDF and geometry as round 1). The GB coverage count = Banagher aliases + UK-only
modules. UA 3Bet/Б count 17 SIZES but only 7 distinct sections. FP McCann box
SD and TY Type 2 are identical to Banagher geometry but counted as a separate
producer. **Open for review:**
- A Bedrock (ZA) reprint of Civilcon M prints a 10 mm edge inset against the fitted 15 mm, with a constant +875 mm² area offset. Consider refitting `CivilconMBeamSection`.
- OKA (MY) M-beam dimensions could inform Civilcon M, but they were not transferred.
- The shared web-search budget ran out in round 2. The Gulf states, Iran, parts of North Africa, the other UK producers and legacy UK standards, and several Nordic and Balkan countries got little or no coverage. Blocked leads (Cloudflare, Incapsula, CAPTCHA, Scribd) are listed per record.

## Extraction round 1, 23 September 2026

Every downloaded but unimplemented source was assessed by visual page
inspection, then 255 further profiles were implemented from it. Coverage is now
**556 distinct profiles, 731 country-profile assignments, 26 countries**.
Every new class exposes `provenance` (`transcribed` 70,
`transcribed-with-convention` 77, `fitted-reconstruction` 55, `estimate` 53)
and `source_status`. Owner instruction: hedge what needs hedging, but put a
best estimate in the data. Estimates are therefore implemented and labelled,
not omitted. Per-family evidence, conventions and pinned discrepancies are in
`docs/research/extraction-*-2026-09.md` and matching `data/*.json`.

| Package / classes | Profiles | Notes |
|---|---:|---|
| `us` WsdotWf/Tub/BulbTee/DeckBulbTee/SlabGirder | 44 | WF36–100 and U/UF G4/G5 reproduce 2025 WSDOT tables exactly; G6 −36 in² (table implies 2'-0" fillet run vs drawn 1'-6") and W*BTG +4 in² pinned; WF*BTG and 24/30 in slabs (2026 PRELIMINARY) estimates |
| `ca` CaMtoNuGirder/CaMtoBoxGirder | 16 | SS107-13…24 (June 2025) now downloaded; NU900–2400 (8 depths) current; 915 mm boxes DRAFT-2023 estimates |
| `sk` VphGirder/VphSlabBeam | 12 | 20 catalogue rows share 12 drawings; 2.1 m girder table conflict (yc 986 vs 1016, I −4.8%) pinned |
| `es` Hp1Beam | 6 | Historic 1977; area and formwork perimeter both check |
| `hu` Ferrobeton FP/FPT/ITG/FI-150 | 14 | Radii measured from vector PDF paths; FPT-45 +8.2% mass pinned; ITG-45 skipped |
| `nl` Haitsma HKO/HKO-XL/HRP/HIP | 50 | HKO I multiplier ×10⁹ mm⁴; HKO-XL all estimates; HIP web-page 1600–2400 range unresolved |
| `ro` AsaGrindaPod 42/52/72/80/95/105 | 6 | New p101 girders 95/105; 52 and 105 estimates; no published properties |
| `za` Civilcon T/U/SpecialU/M | 30 | T10 = 815 (not 850 label); U/SU/M fitted to properties; M notch scales 50×50, not 40×50; table typos preserved |
| `india` Nh45aIGirder/DelhiVadodaraPscI | 8 | Feasibility drawings; RCC ≠ prestressed; Delhi–Vadodara web 300 ± 26 mm estimate |
| `np` DorPrecastRcI | 2 | 12 mm chamfer convention (≤600 mm² effect) |
| `cn` Beijing20bgql2Box | 2 | a = 0/300; urban-rail atlas; no properties |
| `id` Wika channel/PC-I/PC-U/bulb tee | 16 | Channel girders fitted ≤0.1%; I/U/bulb-tee are estimates from schematic drawings |
| `mx` SepsaBox/DoubleTee/Nebraska | 49 | Box table contradictions (CA-180 −5%, CA-135, B-400) pinned; Nebraska estimates |

Not extractable from held files: Pretensa, Tierra, Paver, Somaco, WIKA
voided slabs, Bangladesh, SADET, Mongolia, Senegal, Botswana, Dubai, Betonel,
Guinea, Haiti, cz_zpsv, fr_prad, fi_parma, md_asd, hr_gpkrk, al_apm and the
HTML snapshots (see `docs/research/extraction-*` and the assessment notes
summarised there). Brazil's `sources/expansion/brazil/` is empty; still
retrieval-blocked. Priority for owner review: every `estimate` profile, the
pinned table conflicts above, and whether estimates should count toward the
coverage headline or be flagged separately on the map.

## Jurisdictions and coverage

UK and Ireland are separate country entries. Banagher explicitly markets the
same bridge-beam catalogue in both and documents UK projects. `bridgebeams.uk`
exports aliases for the 13 `bridgebeams.ie` Banagher geometry families. The map
assigns those 175 profiles to each jurisdiction, while stable profile IDs keep
the global distinct-profile total deduplicated. These aliases are not a
separate UK national standard. The 122-jurisdiction research footprint includes access-blocked
and incomplete sources; it is not implemented-profile coverage. The full
clickable map/table is `docs/source/coverage.md`, generated by
`tools/build_coverage.py`. Current totals (pre-extraction figures superseded above): 556 distinct fixed profiles in 26 countries,
122 research jurisdictions, 233 source records, and 731 country-profile assignments;
the default table of 123 includes one legacy-only template country (BE).
India now has one project feasibility profile; Greece and Poland have both
geometry/templates and new research records. The helper
`tools/build_local_docs.py` regenerates coverage before Sphinx. India
source evidence is refreshed in `docs/research/india-followup.md`.
The US follow-ups are `docs/research/us-states-followup.md` and
`docs/research/us-washington-followup.md`; Ontario is
`docs/research/canada-followup.md`. US: four 2006 WSDOT W outlines checked
against 2025 properties and three 2019 MnDOT rectangular sections. Canada:
three 2025 Ontario MTO solid slabs. These are state/provincial sources, not
national standard sets. The current Ontario NU drawings still need exact
curved-transition reconstruction; WSDOT's inspected 2026 WF sheets are stamped
preliminary. The inherited W74G depth entry was corrected to 73.5 inches.

## Durable source collection

Start at **`docs/research/README.md`**, not the ignored historical registry.
It links the current country index, translated titles/terminology, original
source URLs, source-status distinctions, tables, and outstanding blockers.

- `docs/research/europe-americas-2026-09.md` and
  `data/europe-americas-sources.json`.
- `docs/research/asia-africa-2026-09.md` and
  `data/asia-africa-sources.json`.
- `docs/research/pdf-transcription-2026-09.md` and
  `data/pdf-transcriptions.json`: 28 drawing records, 17 Norwegian/Japanese
  translated terms, four source PDF manifests.
- `docs/research/banagher-pending-families-2026-09.md` and
  `data/banagher-pending-families.json`: 32 Solid Box and 16 W table rows.
- `docs/research/deep-search-*-2026-09.md` and matching `data/*.json`:
  57 current discovery records across 10 queues, covering manufacturers,
  academic papers, project drawings, technical guides and standard leads.
  One NHAI feasibility midspan
  contour is implemented; the others remain source or contact leads.
  Pekabex MG-T and Haitsma HKP/HGKO are strong producer-drawing targets.
  Ashghal TY/TYE sheets have indexed tables but direct access redirected to
  sign-in; Beijing 20BGQL2 is a verified parametric urban-rail box atlas with
  0–300 mm width variable. Geoquest/COMPRE and Sri Lanka RDA T/B/505 are useful
  manufacturer or authority contact targets. Portuguese ISEP PDF retrieval
  timed out; Waskita's catalogue returned HTTP 403, so its indexed H-series
  terms remain unverified.
  Brazil now has five new discovery records (six map records including the
  earlier registry): UFC I-beam thesis, IBRACON/SciELO U-beam
  paper, DNIT IPR guidance, and the IFES São Domingos completed-bridge drawing
  lead. Brazil remains research-only until the transition dimensions are read
  from the original figures.
  The most recent focused reports are `deep-search-brazil-2026-09.md`,
  `deep-search-korea-argentina-philippines-2026-09.md`,
  `pakistan-us-section-followup-2026-09.md`,
  `aashto-cross-jurisdiction-followup-2026-09.md` and
  `pci-aashto-reference-2026-09.md`.

Counts for the evolving regional registries are generated, not hardcoded here:

```
python3 tools/check_source_catalogue.py
python3 tools/check_source_catalogue.py --verify-downloads --write-index
python3 tools/check_discovery_sources.py
```

The second command requires the ignored local downloads and `pdfinfo`.
It verifies PDF/HTML hashes and PDF page counts, then refreshes the country
index. Regional counts exclude the separate PDF and Banagher audit records.
Citation-only inherited standards may have a null URL rather than a guessed
link. Access-blocked, rejected, draft and preliminary sources are explicitly
labelled; they must not be counted as verified implementation-ready profiles.

PDFs, HTML snapshots, extracts and visual evidence are retained under
`sources/expansion/{europe-americas,asia-africa,pdf-backlog}/`; these are
ignored private working materials. Original Banagher/Concast PDFs remain
under `sources/`. Do not force-add original publications or snapshots.
All numeric conversions preserve source units or identify derived SI values.

## New implementations and corrected geometry

The new and audited families below use millimetres, origin at mid-soffit,
y upwards, a frozen Dimensions dataclass and a Section exposing Shapely
`.polygon` and sectionproperties `.geometry`. New classes are exported from
their country package and the top-level `bridgebeams` package. Legacy
Australian classes retain their earlier dictionary dimensions, interface and
negative-y convention; do not assume the new interface applies to them.

| Module / public class | Coverage | Evidence and limitations |
|---|---|---|
| `india.Nh45aPscISection` | One NH 45-A Ch 50+473 midspan PSC I profile | NHAI drawing FIPL-HD-TPT-117-V-N-45A-MJB-CH-50+473-GA-01, sheet 03/03, PDF p50; 2250 mm depth and 900/300/750 mm top/web/bottom widths; gross area 941250 mm². Title block says Final Feasibility Report, so no built/approved claim; end block excluded. PDF SHA-256 `7f21b6abd44f339680aa5f7d1d91cfad75edb3055f09d0f6cbd635765fa09227`. |
| `us.AashtoIBeamSection` | Classic Types I–VI, six dated US reference profiles | PCI Bridge Design Manual Appendix B-7/B-8, November 2011; all D1–D6/B1–B6 dimensions transcribed and gross A/yb/Ixx checked against published rounded values. No implied adoption in Pakistan or other countries. |
| `ie.ie_solid_box.IeSolidBoxBeamSection` | 32 SD variants: classes (1)–(4) | Nominal dimensions; class4 table discrepancies preserved |
| `mx.SepsaIGirderSection` | 7: I-MODIFIED, II, III, IV, IV-MODIFIED, V, VI | Producer-specific metric profiles, not aliases for US AASHTO; published area within 50 mm² rounding |
| `tw.TaiwanISection` | IV–VIII | Freeway Bureau Fig.10/Table 14, PDF p34/printed p30; post-tensioned gross midspan, ducts/end blocks omitted; analytic A/cy/I validation |
| `qa.QaQBeamSection` | T1–T5 | Ashghal SD 5-1-101 Rev1; directly read lower dimensions; documented reconstruction, not an exact manufacturing profile |
| `nz.NzIBeamSection` | 1500/1600 | RR364 S4.01/S4.10, PDF pp 45/51; source's 20 mm chamfer option, analytic area checks |
| `nz.NzSuperTSection` | 1025/1225; 1225 also with `top_width=1990` | Corrected open-top twin-web gross profile; formwork ledge omitted explicitly |
| `za.CivilconIBeamSection` | I1–I20 | Corrected vertical orientation: B1 at soffit, B4 at top; direct published centroid and actual top/bottom moduli checked |

The initial expansion added **43 profiles**, plus the newly supported narrower NZ
Super-T arrangement. Existing AU/IE/BE/GR/JP/KR/PL/RU/TH/TR/ZA families remain.
The UK namespace now exports aliases for Banagher's shared Ireland/UK producer range.

### Corrections that affect existing analyses

1. **NZ Super-T:** the old polygon filled the open centre. It also mistook
   the upper 100×75 haunch for bottom chamfers and gave 1225 the 1025 lower
   profile. Current drawings: S1.01/PDF8 = base852, valley240, rise67,
   bottom clear709; S1.11/PDF15 = base814, valley260, rise64, clear674.
   S1.21/PDF22 uses the 1990 top width. S1.25/PDF26 is unit data, not the
   section drawing. The small 15 mm ledge has a 45 MAX depth, not an exact
   depth, so the gross-profile approximation omits it and states this.
2. **Civilcon I:** no evidence supported the old invented as-cast inversion.
   The drawing is B1 at y=0, B4 at y=depth. I1 centroid is about 318.221 mm
   above the 410 mm soffit, with 360 mm top. Area/inertia are invariant under
   reflection and could not detect the old error. Centroid and Zt/Zb do
   change. Internal data keys have been renamed to match the source labels;
   the dimensions dataclass retains its b1…d6 attribute names. Source I18
   Zt is inconsistent by about 0.417%; only that discrepancy is separately
   pinned in tests, not hidden by widening every family's tolerances.
3. **Qatar:** 200+1069+200 brackets the haunch, not overall flange width.
   Nominal overall width is 2150. Lower concrete has a central valley, not
   a peak. T2–T4 values were read directly, replacing interpolation. Rounded
   source callouts do not close perfectly: nominal 125 mm webs become about
   122–123 mm in the chosen reconstruction. Maximum source residuals are
   0.88% area, 0.85% centroid and1.26% Ixx; full per-type residuals are in JSON.
4. **Japan:** 240 and151/152 in the Tohoku source are stirrup dimensions,
   not concrete web/flange dimensions. Existing JP code already uses the
   correct 300 mm web; the stale research brief was wrong. Relevant PDF
   pages are 9–10, printed 5–6. BG reinforcement changes do not define a new
   universal concrete profile.

Representative new/corrected profiles are rendered in
`docs/source/_static/images/global-additions.svg`. Regenerate with
`/home/ccaprani/anaconda3/envs/pybridge/bin/python examples/plot_global_additions.py`.

## Remaining blockers and productive next work

The received human readings and closed queue are documented in
`docs/source/research-visual-review.md`; its illustrated local companion is
the ignored `dims_review.html`. All 12 answered cards are archived with
verbatim answers; additional optional comments use separate v4 storage. Build with
`/home/ccaprani/anaconda3/envs/pybridge/bin/python tools/build_local_docs.py --with-review`
and serve `docs/_build/html` on loopback port 8766. The helper attaches local
source materials, so use this output locally. A build without `--with-review`
removes those attachments. Read the review guide for the precise workflow.

- **Implemented after visual review:** all 10 Norway NTB/KTB,16 current
  Banagher W,8 nominal SD class4,8 Civilcon Y, and 4 NZ hollow-core units
  (650/900 inner;587 inner/outer). These 46 profiles pass 314 full-suite tests.
  Their code, source traces and qualifications are documented in
  `docs/research/visual-review-followup-2026-09.md` and its linked reports.
- **Norway:** 15 mm bottom chamfers are Colin's visual inference, not printed
  callouts. KTB1400 has30 mm outer-face offset; other KTB faces are vertical.
- **NZ650/900 outer:** only the exact eccentric void-chain endpoints remain
  unresolved. Do not ask for another prose comparison of the drawings;
  the inner/outer differences and partial-chain discrepancies are recorded.
- **Banagher CAD:**50 embedded DWGs were recovered from
  `/mnt/data/sync/consulting/Roughan O'Donovan/Structure B01/05316 Beam Design/05316 Precast Beam Properties.xls`.
  Persistent hash-verified originals/conversions are ignored under
  `sources/expansion/banagher-cad/`. No W/SD sheet was identified there.
  A separate W19 project DWG resolves W's straight lower contour; use current
  manual F/V values rather than the older project's values. SD class4 uses
  fully dimensioned nominal manual geometry with 225/275 mm² source-area
  discrepancies explicitly pinned. Do not call that SD CAD verification.
- **Civilcon M:** approximate 40 × 50 mm notch and UK equivalence are hypotheses.
  M4/M10/T10/U5/U10/I18 and Y1 property discrepancies remain recorded; do not
  silently replace literal tables. Y1–Y8 geometry is now implemented.
- **Romanian ASA:** lower chains 600/920 mm resolved and all remaining callouts
  transcribed. Throat references and R50 tangent chains still conflict; exact
  issues are in `visual-followup-za-ro-nepal.md`. Nepal's vague chamfer-scope
  question is withdrawn; focused section crops exist and exact scope is not
  inferred from them.
- **Other countries:** the versioned regional reports identify many further
  primary drawing/property sources and exact current blockers. Slovakia,
  Netherlands, Romania, Indonesia and the expanded Mexican box/U tables
  have useful numeric data. Published properties alone are not enough to
  define missing profile coordinates. Ontario draft and WSDOT preliminary
  overview sheets retain those statuses. The inherited German BT link was
  a miscited materials-production catalogue and is rejected as beam data.
- **Pakistan and AASHTO adoption:** NHA Types A–H are a promising, separately
  named PSC I-girder family (1200–2600 mm deep). An NHA-hosted 30 m project
  sheet has section views for transcription. AASHTO LRFD citation does not
  establish that these match US Types I–VI. Obtain/visually inspect NHA
  STANDARD/04–06 before implementation. See
  `docs/research/pakistan-us-section-followup-2026-09.md`.
- **Other AASHTO-named leads:** Philippine DPWH Type VI has an indexed
  dimensioned drawing; Honduras Type IV has reported completed use;
  Nicaragua Type IV has fabrication evidence. Guatemala, El Salvador and
  Peru have producer, tender or academic leads. No foreign outline is yet
  proven identical to the PCI reference. See
  `docs/research/aashto-cross-jurisdiction-followup-2026-09.md`.
- **New retrieval leads:** Korea's CODIL archive has a 2005 PSC-I
  standardisation report and a 30 m project drawing with partial dimensions;
  Argentina's TRID record describes a 1972 draft standard with four
  premoulded beam types; a Philippine DPWH/EMB EIS records common AASHTO use
  and a 45 m NU 2000 alternative. None is yet complete geometry.
- **Brazil:** a UFC thesis provides a study-specific prestressed I section,
  an IBRACON/SciELO paper gives area and inertia for five U beams on a 33.5 m
  bridge, and DNIT IPR 751/2022 confirms federal use of precast prestressed I/T
  longarinas. The thesis/paper figures and the cited DNIT bridge album need
  retrieval before any Brazilian profile is implemented.
- Do not repeat old blanket claims that countries have no national
  catalogue. Unsuccessful searches are bounded search outcomes, not proof
  of absence. Producer and regional highway-agency catalogues are useful.

## Geometry and provenance rules

- Include the soffit corner when mirroring half-profiles. Check polygon
  validity, winding, analytical area and actual void topology.
- Convert shoelace inertia about y=0 to centroidal inertia:
  `Ic = I0 - A*cy**2`; use signed area for centroid calculations.
- Measure upper flange depths down from the TOP and lower features up from
  the SOFFIT. Confirm physical top/bottom widths from source leaders.
- Preserve original dimensions, revisions, page numbers and units alongside
  translations. Distinguish exact transcription, derived values, fitted
  reconstruction and designer-supplied dimensions.
- Stroke-font CAD labels require rendered visual inspection. OCR or a
  nearby reinforcement label is not adequate evidence.
- Validate against independent published properties where possible. Analytic
  checks without a property table prove implementation consistency, not
  manufacturer approval or structural capacity.
- Do not loosen tolerances to hide source contradictions. Record individual
  exceptions with evidence; do not transfer national/producer geometry
  solely because two sources share an AASHTO or British family name.
- Back up pre-existing docs/configs to adjacent `backups/` directories.
  Source-tree test passes do not replace an isolated wheel/data-file check.
