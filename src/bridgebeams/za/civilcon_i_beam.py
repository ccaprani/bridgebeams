"""South African standard I beams (Civilcon I1-I20, beam & slab construction).

Dimensions and section properties per the Civilcon PPBI datasheet (TMH7
NA+NB loading). The profile is decoded exactly from the PPBI vector
drawing:

- ``B1``: top flange width (at the top face; the flange sides taper
  slightly to ``B2`` at the flange base over depth ``D2``)
- ``B2``: top flange base width
- ``B3``: web width (constant)
- ``B4``: bottom flange width (constant, vertical sides)
- ``D2``/``D3``/``D4``/``D5``/``D6``: top flange / upper splay / web /
  lower splay (45 deg) / bottom flange depths; they sum exactly to the
  overall depth ``D1``.

The PPBI drawing shows the as-cast orientation (``B1`` face down, hence
the published "Yb over soffit" is measured from the ``B1`` face). This
module returns the section in the drawn orientation: origin at the middle
of the ``B4`` bottom-flange face, y positive towards the ``B1`` face,
millimetres. All 20 sizes reproduce the published area exactly (0.000%)
and the published second moment of area exactly.

No published geometric interpretation was available for ``B4`` beyond the
drawing itself; it is confirmed as the constant bottom-flange width by
exact area/centroid/inertia agreement for all 20 sizes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Optional

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "civilcon_i_beams.json"


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.za.data").joinpath(_DATA_FILE).read_text()
    )


@dataclass(frozen=True)
class CivilconIBeamDimensions:
    """Dimensions of one Civilcon I-beam size, millimetres.

    Attributes follow the manufacturer's labels: ``b1`` top flange width,
    ``b2`` top flange base width, ``b3`` web width, ``b4`` bottom flange
    width, ``d1`` overall depth, ``d2`` top flange depth, ``d3`` upper
    splay, ``d4`` web depth, ``d5`` lower splay (45 deg), ``d6`` bottom
    flange depth.
    """

    size: str
    b1: float
    b2: float
    b3: float
    b4: float
    d1: float
    d2: float
    d3: float
    d4: float
    d5: float
    d6: float

    @property
    def outline(self) -> list[tuple[float, float]]:
        r = [
            (self.b4 / 2.0, 0.0),
            (self.b4 / 2.0, self.d6),
            (self.b3 / 2.0, self.d6 + self.d5),
            (self.b3 / 2.0, self.d6 + self.d5 + self.d4),
            (self.b2 / 2.0, self.d6 + self.d5 + self.d4 + self.d3),
            (self.b1 / 2.0, self.d1),
        ]
        l = [(-x, y) for x, y in reversed(r)]
        return l + r


class CivilconIBeamSection:
    """South African Civilcon I beam (I1-I20) as a ``sectionproperties``
    Geometry.

    Examples
    --------
    >>> from bridgebeams.za import CivilconIBeamSection
    >>> i8 = CivilconIBeamSection("I8")
    >>> i8.dimensions.d1
    1220.0
    """

    SIZES = tuple(f"I{i}" for i in range(1, 21))

    def __init__(self, size: str = "I8"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = CivilconIBeamDimensions(
            size=size,
            b1=float(row["b1_top_flange_width"]),
            b2=float(row["b2_flange_base_width"]),
            b3=float(row["b3_web_width"]),
            b4=float(row["b4_bottom_flange_width"]),
            d1=float(row["d1_depth"]),
            d2=float(row["d2_top_flange_depth"]),
            d3=float(row["d3_upper_splay"]),
            d4=float(row["d4_web"]),
            d5=float(row["d5_lower_splay"]),
            d6=float(row["d6_bottom_flange_depth"]),
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the beam (millimetres)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["CivilconIBeamDimensions", "CivilconIBeamSection"]
