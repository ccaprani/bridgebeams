# Installation

`bridgebeams` is installable from the source repository:

```bash
git clone https://github.com/ccaprani/bridgebeams.git
cd bridgebeams
python -m pip install .
```

Dependencies: `numpy`, `shapely`, `sectionproperties` (>= 3.0).

For development (tests and documentation):

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

To use the adapters, install the target packages as well, e.g.
`concreteproperties` and/or `ospgrillage`.

## Units

All geometry is in **millimetres** and results are reported in mm², mm³ and
mm⁴ — matching the manufacturers' published tables. Convert externally for
other unit systems.
