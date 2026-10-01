# Round 3 — Philippines: Standard AASHTO I-girders (owner-supplied slide), 2026-09

Machine-readable record: [`data/round3-philippines-2026-09.json`](data/round3-philippines-2026-09.json).
Implemented as `bridgebeams.ph.PhDpwhAashtoSection` (data: `src/bridgebeams/ph/data/dpwh_aashto.json`).

## Source

| Local file | Origin | SHA-256 |
|---|---|---|
| `sources/expansion/round2/manual/ph/owner-supplied-types-of-bridges-philippines-aashto.png` (2000 × 1500 px) | Single presentation slide titled *Types of Bridges (Philippines) — Deck Girder Bridges — Prestressed Concrete Girders (PSCG) — Standard AASHTO I-Girders*. Found and supplied by the owner; author, presentation, date and URL unrecorded (unverified). | `c5e9056f77e5a10e77e47a30f5b5dff4d44988f2d81609912448ea17e734274d` |

Status: **secondary presentation slide (origin unrecorded); DPWH practice**. It is not a
DPWH standard drawing. It is, however, the first dimensioned Philippine source in the
repository: round 2 ([round2-south-asia-korea-philippines-2026-09.md](round2-south-asia-korea-philippines-2026-09.md))
recorded "no Philippine profile can be implemented without DPWH plans", because
dpwh.gov.ph sits behind an Incapsula challenge. The other local file,
`odiongan-spillway-fy-2023-compressed-45-88.html`, is only that challenge page, not the drawing.

## Transcription (mm, read visually from 2× crops)

Vertical chains are listed top to soffit, exactly as printed.

| Slide label | Size key | Depth | Top | Web | Bottom | Chain as printed | Chain sum | Provenance |
|---|---|---|---|---|---|---|---|---|
| TYPE I | `I` | 711 | 305 | 152 | 406 | 102 / 76 / 279 / 127 / 127 | 711 | transcribed |
| TYPE II | `II` | 914 | 305 | 152 | 457 | 152 / 76 / 381 / 152 / 152 | 913 | transcribed-with-convention |
| TYPE III | `III` | 1143 | 406 | 178 | 559 | 178 / 114 / 483 / 191 / 178 | 1144 | transcribed-with-convention |
| TYPE IV | `IV` | 1372 | 508 | 203 | 660 | 203 / 152 / 584 / 229 / 203 | 1371 | transcribed-with-convention |
| TYPE V | `V-as-drawn` | 1829 | 1067 | 203 | 660 | 127 / 76 / 102 / 1067 / 254 / 203; horizontal fillet callout 102 | 1829 | transcribed |

Conventions:

- Types I–IV: 45° tapers are drawn. Their horizontal extents come from the width
  differences, which the slide does not dimension separately: for example,
  (305 − 152)/2 = 76.5 against a 76 rise for Type I.
- Types II–IV: the printed chains miss the overall depth by 1 mm because each inch
  value was rounded on its own. The overall depth and the flange/taper callouts govern,
  and the web segment absorbs the residual (web used: II 382, III 482, IV 585).
- `V-as-drawn`: the top transition has two stages. A 127 edge leads to a 76-high outer
  taper and then a 102 × 102 fillet into the web. The outer taper's horizontal extent,
  (1067 − 203)/2 − 102 = 330, is derived. For Type I, one "127" label is printed below the
  soffit line; it belongs to the lowest chain interval.
- The slide publishes no section properties, so no property residuals can be computed.

## Comparison with PCI 2011 (`bridgebeams.us.AashtoIBeamSection`)

| PH size | vs US | Max vertex diff (mm) | Hausdorff (mm) | Area PH/US | Ixx PH/US |
|---|---|---|---|---|---|
| I | I | 0.61 | 0.49 | 0.99896 | 0.99916 |
| II | II | 0.82 | 0.71 | 0.99779 | 0.99805 |
| III | III | 0.71 | 0.57 | 1.00075 | 1.00000 |
| IV | IV | 1.00 | 0.78 | 0.99937 | 1.00019 |
| V-as-drawn | **VI** | 25.6 (0.5 excluding the soffit corners) | 25.6 | 0.97545 | 0.96744 |
| V-as-drawn | V | — | 228.8 | — | — |

Types I–IV are soft conversions of PCI Types I–IV, so the differences come only from inch→mm
rounding plus the 1 mm chain residual.

**Label conflict:** the outline labelled "TYPE V" is 1829 mm deep with a 1067 mm top flange,
127/76/102 top chain, 102 fillet, 203 web and 254/203 bottom chain. That is AASHTO/PCI
**Type VI** (72 in), not Type V (63 in = 1600 mm). The slide's label is kept as the size key
`V-as-drawn`.

**Bottom-flange conflict (pinned):** the slide prints a 660 mm bottom flange (26 in, the Type IV
value) for this outline. PCI Types V and VI both have B2 = 28 in = 711.2 mm. The width is
implemented as printed, so the bottom taper is 228.5 wide × 254 high rather than 45°. This makes
the area 2.5 % and Ixx 3.3 % lower than Type VI. The artwork is schematic, with unequal x/y
pixel scales, so it cannot settle the question. Its soffit/top pixel ratio (0.56) favours the
narrower flange over 711 (0.67). The slide may have copied Type IV's value, or DPWH may use a
narrower-bottom Type VI variant.

## Cross-references and remaining work

- [aashto-cross-jurisdiction-followup-2026-09.md](aashto-cross-jurisdiction-followup-2026-09.md),
  priority 1: the DPWH Odiongan Bridge 2 drawing (PDS 26/43) labels a 40 m **AASHTO Type VI**
  with indexed callouts 1829 and 1067 mm. This agrees with the geometry of this slide's
  "TYPE V". That sheet is the decisive check on the 660 vs 711 bottom flange. Local retrieval
  still returns only the bot-challenge page.
- Same file, priority 2: DPWH POW 17J00028 "PSC Girder AASHTO Type IV-B" is still undefined.
  The slide's Type IV is plain PCI Type IV, so it says nothing about `IV-B`.
- [round2-south-asia-korea-philippines-2026-09.md](round2-south-asia-korea-philippines-2026-09.md):
  the JICA Davao bypass report names "AASHTO girder type V" without dimensions. Given this
  slide's mislabelling, any Philippine "Type V" reference needs its depth checked before
  anyone assumes 1600 mm.
- [deep-search-korea-argentina-philippines-2026-09.md](deep-search-korea-argentina-philippines-2026-09.md):
  the Laguna Lakeshore EIS describes a 40 m Type VI option and NU 2000. This is consistent
  with Type VI being in Philippine use.
- The slide's origin should be recorded if the owner can recall it.
