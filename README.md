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

### Ireland / UK (`bridgebeams.ukie`)

- **Y beams (Y1–Y8)**, 700–1400 mm deep, 750 mm soffit — the Irish standard
  beam-and-slab range (Banagher/Concast/Shay Murtagh publish identical
  tables). Reconstructed profile validated to 2.6% rms against published
  properties, plus the "all possible strand locations" map.
- **YE edge beams (YE1–YE8)** — asymmetric edge beam with full-height
  vertical face; validated to 0.8% rms against published properties
  (including the published centroid offset Xc).
- **T beams (T1–T10)** — solid slab construction; exact published profile,
  validated to <0.02% against published properties.
- TY/TYE, M/UMB, U and box families are planned on the same pipeline
  (dimensioned sources already collected under `sources/`).

### Australia (`bridgebeams.aus`)

- **Super-T girders (T1–T5)** to AS5100.5 App. D, pre- and post-2001 variants.
- **I-girders (types 1–4)** to AS5100.5 App. D.

## Quick start

```bash
python -m pip install -e .
```

```python
from bridgebeams.ukie import IeYBeamSection, strand_locations
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
sizes (`src/bridgebeams/ukie/data/ie_y_beam.json`):

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

All dimension sources are registered with URLs in
[`sources/SOURCES.md`](sources/SOURCES.md). Regional research briefs for
future families (US AASHTO/PCI, China JTG, Canada CPCI/NU, Brazil, India,
Europe) live in `sources/research/`. Source documents are working
references and are not committed.

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## License

MIT — see [LICENSE](LICENSE).
