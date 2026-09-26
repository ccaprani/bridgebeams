# Round 5: Multilingual per-country sweep (2026-09-26)

Systematic local-language web sweep for prestressed-concrete (PSC) bridge
beam sections across the countries not yet implemented in the catalogue.
Motivation: earlier rounds searched mostly in English; most of the
remaining world either (a) uses AASHTO/PCI shapes imported through
design-and-build or aid programmes — which the catalogue should *record as
adoption evidence* rather than re-implement — or (b) has national standard
beam families documented only in the local language.

## Method

Five parallel researcher agents, one per continental/language cluster
(Latin America · Europe · MENA + Central Asia · Sub-Saharan Africa ·
Asia-Pacific + Caribbean). Per country, 2-4 searches using local-language
terms for "prestressed concrete bridge beam" plus authority names, and an
explicit English "AASHTO girder/beam + country" adoption check. Every
country is classified with exactly one status:

| Status | Meaning | Catalogue treatment |
|---|---|---|
| `IMPLEMENTABLE` | Publicly downloadable dimensioned PSC beam sections | queue for extraction round |
| `AASHTO-ADOPTION` | Credible evidence AASHTO/PCI shapes are the standard practice | record as adoption source (no new geometry) |
| `IMPORTED-OTHER` | Another foreign system (Spanish, Russian типовые, Chinese, Australian...) | record; geometry only if the parent system is in the catalogue |
| `LOCAL-STANDARD` | National standard family, dimensions in paywalled/printed code | record code + lead |
| `LEAD-NO-DIMS` | PSC beams used, no public dimensions | record best lead |
| `NONE-FOUND` / `NOT-COVERED` | no evidence / agent budget exhausted | retry in a later wave |

Agent outputs are consolidated into
`docs/research/data/deep-search-multilingual-sweep-2026-09.json`; URLs are only
those the agents found in search results (no fabrication). Status lines
below describe the original wave; the current machine record incorporates the
subsequent visual-audit corrections noted below.

## Wave 1 results (26 September 2026)

122 jurisdictions classified across the five clusters. Machine record:
`docs/research/data/deep-search-multilingual-sweep-2026-09.json` (also
feeds the coverage map's research layer). Raw agent tables preserved in
`sources/expansion/round5-multilingual-sweep/`.

| Status | Count | Meaning |
|---|---|---|
| LEAD-NO-DIMS | 73 | initial survey: PSC beams used, no public dimensions |
| AASHTO-ADOPTION | 24 | credible AASHTO/PCI-shape adoption evidence |
| NONE-FOUND | 11 | no PSC beam evidence found |
| IMPLEMENTABLE | 4 | initial survey claims, two subsequently downgraded |
| RUSSIAN-ADOPTION | 4 | Soviet типовые series (Kazakhstan, Uzbekistan, Kyrgyzstan, Tajikistan) |
| IMPORTED-OTHER | 4 | foreign systems (Namibia NAASRA, Mongolia JTG, Fiji/Vanuatu AS 5100) |
| LOCAL-STANDARD | 2 | Germany Typenentwürfe, Belarus series |

### Follow-up of the four initial IMPLEMENTABLE claims

The initial-wave table above is historical. After text-only prep and the
Class C visual audit on26 September, the current122-row machine record has
**75 LEAD-NO-DIMS and2 IMPLEMENTABLE**, with all other counts unchanged.
IMPLEMENTABLE remains a source-readiness survey label; it is not a profile
count. The [round5b follow-up](round5b-extraction-prep-2026-09.md) records
**five implemented profiles** and the residual work. No vision blocker remains.

1. **Finland — one model implemented:** TIEL2160004-2000, PDF p28,
   LIITE1.4 A–A h1270. This is a nominal model example, not a national SKU.
   Rectangle/trapezoid and I mould options do not establish a fixed matrix;
   H1.2–2.1 m includes slab. LIITE3.1 quantities are curves. Rounded
   LIITE4 properties corroborate but do not exactly equal the haunched model.
2. **Estonia — LEAD-NO-DIMS:** ViaPlus ZIP bare bottom1180 mm,1200
   spacing/slab strip,240 CIP slab. Chart labels are spans in metres, not
   masses. ZIP web/haunch/tip geometry and box void/walls/taper remain
   incomplete; width950/height800–1000 is not a discrete box catalogue.
3. **Cambodia — LEAD-NO-DIMS:** the retained JICA file is a March2013
   inspection-survey appendix, not standard drawings. Actual MPWT/Prakas
   sheets were not acquired; old titles/span ranges remain unverified leads.
   Only a45-second curl timeout is newly verified, not a viewer wall.
4. **Iran — four profiles implemented:** RMTO102 PDF p52/sheet8-4 h370,
   p51/8-5 h470, p54/8-7 h770 and p56/8-8 part A h1000; nominal PSC
   inverted-T outlines below the separate slab. The document mixes RC and
   PSC. h620 (p53/8-6) remains withheld for missing width corroboration;
   other PSC families remain untranscribed. No bare property table identified;
   mirror provenance/current applicability caveat retained.

### AASHTO-adoption cluster (24)
Latin America is nearly uniform (Colombia, Peru, Ecuador, Panama,
Guatemala, Honduras, El Salvador, Nicaragua, Dominican Republic, Costa
Rica) joined by Saudi Arabia, Jordan, Egypt, Afghanistan, South Sudan,
Trinidad & Tobago (Type III/IV named), Bahamas, Guam, USVI, Belize.
Notable nuance: Abu Dhabi (DMT TR-516) explicitly *rejects* standard
AASHTO/PCI precast I-girders; Kuwait's manual is the only Gulf one that
names families. Recorded as adoption evidence, not new geometry — the
catalogue's existing `us.AashtoIBeamSection` profiles cover the shapes.

### Other patterns
- Soviet legacy in Central Asia (серия 3.503.1-81; Kazakhstan СТ РК
  3368-2019 procurement evidence); Mongolia imports Chinese JTG 3362.
- JICA/Japanese practice drives Myanmar, Laos, Cambodia, Timor-Leste,
  Samoa; Fiji and Vanuatu formally adopt Australian AS 5100.
- Within this sweep's remaining-country targets, Finland yielded one model;
  Estonia's public brochures remain dimension-incomplete. Germany ARS24/1999
  Typenentwürfe and the cited Russian series remain access leads. This is not
  a claim that other European countries lack public sections; Greece's re-check
  confirmed local pretensioned I-girders (PROKEL/ARMOS), not imported W-shapes.
- Strong follow-up fetches flagged by agents: Uruguay per-bridge design
  dataset ZIP (gub.uy), Mozambique ANE *Desenhos-tipo* (2023, content
  unverified), Kenya KeNHA 2025 manuals ZIP, Paraguay MOPC *Atlas de
  Planos* behind procurement login.

Wave 2 (unassigned remainder): Caribbean micro-states, Pacific islands,
Cape Verde, Djibouti, small Gulf/Central Asian states — most are
NOT-COVERED territory above plus the never-researched leftovers.
