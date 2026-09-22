# Visual review: implementation and source follow-up

Colin Caprani supplied 12 drawing readings on 22 September 2026. The
[verbatim response record](data/visual-review-responses-2026-09-22.json)
preserves the export and subsequent clarification that DWGs were embedded
in the workbook. Printed dimensions, reviewer inferences and approximate
suggestions remain distinct evidence.

## Forty-six additional profiles

| Country | Implementation | Added profiles | Evidence and qualifications |
|---|---|---:|---|
| Ireland | Banagher W | 16 | Current manual dimensions plus the straight lower contour in recovered producer W19 CAD; older upper F/V dimensions kept separate. |
| Ireland | Solid Box width class (4) | 8 | Fully dimensioned nominal manual outline; source area excess of 225/275 mm² retained explicitly. No matching SD CAD was identified. |
| Norway | NTB/KTB | 10 | Source outline dimensions plus Colin's inferred 15 mm bottom chamfers. KTB1400 has a 30 mm outer-face offset; the other KTB faces are vertical. |
| New Zealand | Hollow-core | 4 | 650/900 inner units and 587 inner/outer units. Key depths are 34/38 mm; 12 mm is the key-transition chamfer. |
| South Africa | Civilcon Y | 8 | Confirmed 40 × 50 mm notches and per-size upper widths; R100 junction. Y1 modulus discrepancy retained separately. |

The full repository suite passes **314 tests** (14 existing dependency
warnings). Geometry tests include source property comparisons, independent
strip integration, void topology, actual soffit/upper boundaries and
asymmetric-face orientation. The common-scale figure in the global overview
shows representative new profiles, including open W and NZ hollow-core
voids.

Detailed evidence:

- [Norway and New Zealand](visual-followup-norway-nz.md).
- [Recovered workbook and Banagher project CAD](banagher-cad-followup.md).
- [Civilcon, Romania and Nepal](visual-followup-za-ro-nepal.md).

## CAD recovery

The recovered `05316 Precast Beam Properties.xls` contains **50 embedded
DWGs**. Their bytes and the existing DXF conversions were verified and
copied into persistent, ignored local source storage. The workbook contains
many useful families, but no sheet explicitly identifying modern W or SD.
Its U drawing must not be mistaken for W: the base widths differ.

The W lower contour was instead resolved from the separate locally held
Banagher W19 project DWG. All sixteen current polygons match published areas
within 4 mm² and Ixx within 0.0025%. Their dimensions and the CAD entity
handles are retained in the audit. Original CAD/workbook publications remain
private; numeric facts, source identities and hashes are versioned.

## Closed questions and remaining work

The twelve original review cards are archived with the received answers and
individual outcomes. No broad request to narrate inner-versus-edge drawings
is repeated. Remaining tasks are specific source or modelling issues:

- **NZ650/900 outer units:** partial void chains have endpoints inside the
  overall outline; the exact eccentric placement still needs reconciliation.
  The source drawings have already been compared and both discrepancies
  are documented.
- **Civilcon M:** 40 × 50 mm is an approximate suggested notch, and UK
  equivalence is a hypothesis. Neither is silently treated as a producer
  dimension or implemented jurisdiction alias.
- **Romanian ASA42/52/72/80:** the 600/920 mm lower-width chains are resolved.
  Remaining dimension chains are transcribed, but throat references and
  upper radius/tangent constraints do not all close. These are concrete
  source questions, not a request to reread the resolved small numerals.
- **Nepal:** the old review prompt used an unhelpful full-sheet image.
  Focused midspan-section crops now identify the source evidence; the
  unsupported request to infer every corner's chamfer scope is withdrawn.

## Coverage presentation

Ireland and the United Kingdom are separate jurisdictions throughout the family tables and coverage data. Banagher's shared producer catalogue is assigned to both; UK aliases retain the same profile IDs and do not create new distinct geometry. Use the complete country table and clickable map in
the Sphinx coverage page; the short family table is not the research-country
list. Fixed profile counts, parametric templates and source records are
separate measures. India is included as research evidence even while it has
no implemented constructor.

The current coverage build counts **294 distinct fixed profiles across 17 countries**,
**114 researched jurisdictions**, **176 source records**, and **469 country-profile assignments** across the
regional, PDF, Banagher, India, US, Canada and producer-availability records. These 176 records are not 176
unique publications. The default country table also includes Belgium,
Greece and Poland from legacy implementation/template coverage. The
[India follow-up](india-followup.md) has five primary records: four additions
and one updated RDSO record, deduplicated by identifier.

The isolated wheel at the visual-review checkpoint contained 24 family JSON files and constructed all 46 new
profiles outside the checkout. The source manifests and review answers are
versioned; local original PDFs, workbook and CAD remain ignored.

The final local Sphinx build passed with warnings treated as errors. Twelve
served pages and 82 unique local source/asset links returned HTTP 200. The
map's click, keyboard selection, country search and filters were checked;
India's five records are unique by identifier. The served review archive
matches all 12 received responses verbatim and uses separate storage for new
optional clarifications.
