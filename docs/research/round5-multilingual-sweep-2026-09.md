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
`docs/research/data/round5-multilingual-sweep-2026-09.json`; URLs are only
those the agents found in search results (no fabrication). Status lines
below are generated from that file.

## Wave 1 results (26 September 2026)

122 jurisdictions classified across the five clusters. Machine record:
`docs/research/data/deep-search-multilingual-sweep-2026-09.json` (also
feeds the coverage map's research layer). Raw agent tables preserved in
`sources/expansion/round5-multilingual-sweep/`.

| Status | Count | Meaning |
|---|---|---|
| LEAD-NO-DIMS | 73 | PSC beams used, no public dimensions |
| AASHTO-ADOPTION | 24 | credible AASHTO/PCI-shape adoption evidence |
| NONE-FOUND | 11 | no PSC beam evidence found |
| IMPLEMENTABLE | 4 | dimensioned sections publicly downloadable |
| RUSSIAN-ADOPTION | 4 | Soviet типовые series (Kazakhstan, Uzbekistan, Kyrgyzstan, Tajikistan) |
| IMPORTED-OTHER | 4 | foreign systems (Namibia NAASRA, Mongolia JTG, Fiji/Vanuatu AS 5100) |
| LOCAL-STANDARD | 2 | Germany Typenentwürfe, Belarus series |

### The four IMPLEMENTABLE hits (next extraction targets)
1. **Finland** — TIEL 2160004-2000 *Jännitetty elementtisilta*: 84-pp
   standard with dimensioned rect/trapezoid/I beams, L 16–40 m,
   H 1.2–2.1 m (tieh.fi/sillat/julkaisut/jbe00.pdf — verified fetched).
2. **Estonia** — E-Betoonelement ViaPlus inverted-T/ZIP beams and
   950×1000 box beams ≤27 m, dimensions on the public catalogue page
   (betoonelement.ee).
3. **Cambodia** — MPWT/JICA standard drawings: pre-tensioned hollow
   slab 15–25 m and post-tensioned deck girders 18–30 m (Prakas
   511/2012, KH/EN + JICA-hosted 2011 draft).
4. **Iran** — RMTO Publication 102 typical bridge deck drawings
   (precast/prestressed, ≤20 m spans) via civil20.blogfa mirror; the
   official RMTO copy needs an archive request.

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
- Europe outside Finland: nothing public (Germany ARS 24/1999
  Typenentwürfe and the Russian series both exist but are not freely
  downloadable); Greece re-check confirmed local pretensioned I-girders
  (PROKEL/ARMOS), not imported W-shapes.
- Strong follow-up fetches flagged by agents: Uruguay per-bridge design
  dataset ZIP (gub.uy), Mozambique ANE *Desenhos-tipo* (2023, content
  unverified), Kenya KeNHA 2025 manuals ZIP, Paraguay MOPC *Atlas de
  Planos* behind procurement login.

Wave 2 (unassigned remainder): Caribbean micro-states, Pacific islands,
Cape Verde, Djibouti, small Gulf/Central Asian states — most are
NOT-COVERED territory above plus the never-researched leftovers.
