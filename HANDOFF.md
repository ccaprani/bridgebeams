# HANDOFF — bridgebeams global collection

Updated 22 September 2026. Read before changing geometry or using old research
notes. This briefing supersedes the previous handoff: several source locators,
width interpretations and blocker claims in it were wrong.

## Repository and verification

- Repository: `~/projects/bridgebeams`; working branch `ukie-beams`.
- Remote: `github.com/ccaprani/bridgebeams`. Preserve the review-before-merge
  workflow. Do not merge or push to main. Keep changes on this branch or a
  new jurisdiction branch, with descriptive commits.
- Python: `/home/ccaprani/anaconda3/envs/pybridge/bin/python`.
- Full test suite after the geometry changes: **266 passed**, 14 existing
  Matplotlib/Pyparsing deprecation warnings. Command:
  `timeout 180 /home/ccaprani/anaconda3/envs/pybridge/bin/python -m pytest tests/ -q`.
- Wheel checked outside the checkout: **all 21 family JSON tables included**;
  all 43 newly implemented profiles construct from the extracted wheel.
  The old `bridgebeams.ukie.data` package-data rule silently omitted BE/JP/PL
  tables; the new wildcard includes each family's `data/*.json`.
- Sphinx command:
  `/home/ccaprani/anaconda3/envs/pybridge/bin/python -m sphinx -b html docs/source docs/_build/html`.
  Obsolete generated `gen/bridgebeams.ukie*` pages are excluded. Research
  includes use `:relative-docs: data/` so JSON links resolve as downloads.

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

Counts for the evolving regional registries are generated, not hardcoded here:

```
python3 tools/check_source_catalogue.py
python3 tools/check_source_catalogue.py --verify-downloads --write-index
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
| `ie.ie_solid_box.IeSolidBoxBeamSection` | 24 SD variants: SD1–SD8, width classes (1)–(3) | 495/750/970 mm overall widths, depths 300–1000; nominal drawing checked against A/Yb/Zt/Zb |
| `mx.SepsaIGirderSection` | 7: I-MODIFIED, II, III, IV, IV-MODIFIED, V, VI | Producer-specific metric profiles, not aliases for US AASHTO; published area within 50 mm² rounding |
| `tw.TaiwanISection` | IV–VIII | Freeway Bureau Fig.10/Table 14, PDF p34/printed p30; post-tensioned gross midspan, ducts/end blocks omitted; analytic A/cy/I validation |
| `qa.QaQBeamSection` | T1–T5 | Ashghal SD 5-1-101 Rev1; directly read lower dimensions; documented reconstruction, not an exact manufacturing profile |
| `nz.NzIBeamSection` | 1500/1600 | RR364 S4.01/S4.10, PDF pp 45/51; source's 20 mm chamfer option, analytic area checks |
| `nz.NzSuperTSection` | 1025/1225; 1225 also with `top_width=1990` | Corrected open-top twin-web gross profile; formwork ledge omitted explicitly |
| `za.CivilconIBeamSection` | I1–I20 | Corrected vertical orientation: B1 at soffit, B4 at top; direct published centroid and actual top/bottom moduli checked |

The new families add **43 profiles**, plus the newly supported narrower NZ
Super-T arrangement. Existing AU/IE/BE/GR/JP/KR/PL/RU/TH/TR/ZA families remain.
The UK namespace is still a separate historic-family stub.

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

- **Norway NTB/KTB:** the free V426 PDF is 96 pages with useful text, not
  drawings-only or purchase-gated. Ten profiles are transcribed from
  pp 37–46. NTB800-400x1400 means400 TOP width; actual stem is 220. Small
  rebates/top recesses are partly resolved, but the controlling bottom
  chamfer size and KTB asymmetric coordinates still need form drawings or
  an explicit source note. Do not treat nearby reinforcement dimensions
  as concrete dimensions. See the exact unresolved callouts in JSON.
- **NZ hollow-core650/900/587:** overall dimensions and voids are transcribed.
  Side keys, edge/inner variants and optional drip details need a deliberate
  outline. The double hollow-core depth is 587, not576. Do not silently
  substitute an inner unit for an edge unit.
- **Banagher Solid Box width class (4):** nominal profile differs from source
  area by 225/275 mm², beyond its printed rounding. Keep it research-only.
  **W:** all 16 published rows transcribed; internal concrete vertices/radii
  remain unresolved. Appendix strand coordinates are not profile vertices.
- **Civilcon M/Y/T/U:** all 58 rows across the six producer PDFs are retained,
  with notation decoded. M4 area, M10 tabulated depth, T10 depth, U5/U10
  values and I18 top modulus have explicit source discrepancies. Do not
  overwrite literal source tables with plausible repairs.
- **Other countries:** the versioned regional reports identify many further
  primary drawing/property sources and exact current blockers. Slovakia,
  Netherlands, Romania, Indonesia and the expanded Mexican box/U tables
  have useful numeric data. Published properties alone are not enough to
  define missing profile coordinates. Ontario draft and WSDOT preliminary
  overview sheets retain those statuses. The inherited German BT link was
  a miscited materials-production catalogue and is rejected as beam data.
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
