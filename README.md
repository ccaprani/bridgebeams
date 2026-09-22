# bridgebeams

Standard precast/prestressed concrete bridge beam sections for use with the
[`sectionproperties`](https://sectionproperties.readthedocs.io) package — a
shared section library for `sectionproperties`, `concreteproperties`,
[PyBridge](https://github.com/ccaprani/PyBridge) and grillage tools such as
`ospgrillage`.

All geometry is in **millimetres** and returned as `sectionproperties`
`Geometry` objects, so sections can be meshed and analysed directly, or
wrapped with materials in `concreteproperties`/`PyBridge`. For
`ospgrillage`, run a `sectionproperties` analysis on the geometry and feed
the computed properties (`A`, `I`, `J`, `Ay`, `Az`) into `og.create_section`.

## Families

### Ireland (`bridgebeams.ie`)

- **T beams (T1–T10)** — solid slab construction; exact published profile,
  validated to <0.02% against published properties.
- **TY / TYE beams** — beam & slab (TY3–TY11, nibbed top) and solid slab
  (TY1–TY11, full flange) variants with edge beams; exact, <0.02%.
- **Y beams (Y1–Y8)** — beam & slab; reconstructed profile validated to
  2.6% rms, with the "all possible strand locations" map.
- **YE edge beams (YE1–YE8)** — asymmetric; validated to 0.8% rms
  (including the published centroid offset Xc).
- **U beams (U600–U12) / SU (SU11–SU12)** — exact, ≤0.3%.
- **M beams (M1–M10) / UMB edge beams** — validated to ≤0.7%.
- **SY / SYE beams (SY1–SY6)** — long span; validated to <0.6% rms.
- **MY / MYE beams (MY1–MY7)** — solid slab; validated to ≤2.2%.
- **Solid Box (SD1–SD8, width classes 1–4)** — 32 nominal profiles;
  class 4 retains explicit source-property discrepancies.
- **W beams** — 16 current profiles, verified against published properties
  using current manual dimensions and recovered producer CAD.

### United Kingdom (`bridgebeams.uk`)

The UK namespace exports aliases for Banagher's 13 shared Ireland/UK families (175 named profiles). Each alias refers to the Irish producer geometry; a profile has one stable ID and can be assigned to both countries. Other UK producers and standards still require separate source-backed profiles.

## Australia (`bridgebeams.aus`)

- **Super-T girders (T1–T5)** to AS5100.5 App. D, pre- and post-2001 variants.
- **I-girders (types 1–4)** to AS5100.5 App. D.

## Global collection

The library also includes families for Belgium, Greece, India, Japan, Korea,
Mexico, New Zealand, Norway, Poland, Qatar, Russia, South Africa, Taiwan, Thailand and
Türkiye. Evidence
quality varies by family: some profiles are exact transcriptions, some are
documented reconstructions, and others require designer-supplied dimensions.
India's first constructor is one NHAI NH 45-A project midspan PSC I-girder
from a dimensioned **Final Feasibility Report**, not a national standard or
evidence of construction.

The [global source collection](docs/research/README.md) contains country-by-country
research, original titles with English translations, structured source records,
and page-based PDF transcriptions. A source appearing in the catalogue does not
mean that its beam family is implemented or that every profile dimension is known.
The [multilingual discovery queue](docs/source/research.md) adds 38
manufacturer, university, standards-library and technical-publication leads
across 25 countries, with exact designations and drawing locators where found.

The [visual-review record](docs/source/research-visual-review.md) preserves
the received answers and their implementation outcomes. With the local source
materials present, run `python tools/build_local_docs.py --with-review`, then
`python -m http.server 8766 --bind 127.0.0.1 --directory docs/_build/html`.
Open <http://localhost:8766/research-visual-review.html> for the guide and
illustrated review link.

The [live coverage map and complete country table](https://ccaprani.github.io/bridgebeams/coverage.html)
separate researched sources from implemented profiles. UK and Ireland are
separate entries. The research footprint spans 121 jurisdictions; many
currently have source evidence only.

The United States now includes four WSDOT W-series girders and three
edition-specific Minnesota rectangular beams; ten further state DOT records
are in the [US follow-up](docs/research/us-states-followup.md). Canada's
Ontario MTO S300/S400/S500 solid slabs are in the
[Ontario follow-up](docs/research/canada-followup.md).

The visual-review follow-up adds 46 profiles: 16 Irish W, eight wide Solid
Box, ten Norwegian NTB/KTB, four NZ hollow-core and eight Civilcon Y.

Earlier additions include seven SEPSA I-girders for Mexico, five Taiwanese
Freeway Bureau I-girders, five Ashghal Q-girder reconstructions for Qatar,
and two NZTA I-beams. The NZ Super-T
geometry now preserves the open centre and each size's distinct lower profile.
Civilcon I-beams now use the source's B1 soffit as `y=0`; the previous
vertical inversion is corrected, so centroid heights and top/bottom section
moduli change. Existing analyses using these two families should be recomputed.

## Quick start

```bash
python -m pip install -e .
```

```python
from bridgebeams.ie import IeYBeamSection, strand_locations
from sectionproperties.analysis import Section

beam = IeYBeamSection("Y4")            # 1000 mm deep Y4
geom = beam.geometry                    # sectionproperties Geometry (mm)
geom.create_mesh(mesh_sizes=[5000])

# all possible prestress strand locations (mm), filtered to this depth
strands = strand_locations("Y4")

# feed concreteproperties / PyBridge:
#   from concreteproperties.concrete_section import ConcreteSection
#   cs = ConcreteSection(geom.compound(material=concrete))  # etc.
```

## Accuracy statement (Y family)

Manufacturers publish `Wf`, section properties and strand layouts but not
the internal profile dimensions, so the Y-beam internals are a documented
least-squares reconstruction fitted to the published properties of all eight
sizes (`src/bridgebeams/ie/data/ie_y_beam.json`):

| Quantity | Max deviation from published (Y1–Y8) |
|---|---|
| Area | 3.5% |
| Centroid height | 2.1% |
| Second moment of area | 4.8% |

The pytest suite checks every size against the published table. Suitable for
preliminary and assessment workflows; for detailed design, confirm against
the manufacturer's drawings/BIM (see `sources/SOURCES.md`).

## Note on units

Millimetres in, properties out in mm²/mm³/mm⁴ — matching the hard-coded
dimension tables. Convert externally for other unit systems.

## Sources & provenance

The versioned [source collection](docs/research/README.md) records source
URLs, translations, dimensions and remaining blockers. Earlier working notes
are retained locally in `sources/SOURCES.md` and `sources/research/`.
Source PDFs and rendered drawings are private working references and are not
committed; published factual dimensions and provenance are retained in the
research records and family data files.

## Documentation

Sphinx docs (pydata theme), including an executed tutorial notebook:

```bash
python -m pip install -e ".[docs]"
python -m sphinx -b html docs/source docs/_build/html
```

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## License

MIT — see [LICENSE](LICENSE).
