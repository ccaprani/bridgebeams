"""South African Civilcon I1-I20 gross sections, in source drawing orientation.

PPBI.pdf page 1 shows B1 at the soffit and B4 at the top. B2 is the
bottom flange width at its upper edge; B3 is the web. From the soffit,
D2/D3/D4/D5/D6 are bottom edge / bottom splay / clear web / top splay /
top edge heights. Origin is the B1 soffit centre, y positive upwards.

Published Yb is therefore the centroid height above y=0. Earlier versions
returned a vertically reflected profile; its area and centroidal inertia
were unchanged, but centroid and top/bottom section moduli were reversed.
The source I18 top modulus is inconsistent with its dimensions; preserve
that printed value and flag it rather than relaxing every section check.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

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

    Attributes retain the source labels: b1 soffit width, b2 upper
    bottom-flange width, b3 web width, b4 top width; d1 overall depth,
    d2 bottom-edge height, d3 bottom splay, d4 clear web height,
    d5 top splay and d6 top-edge height.
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
            (self.b1 / 2.0, 0.0),
            (self.b2 / 2.0, self.d2),
            (self.b3 / 2.0, self.d2 + self.d3),
            (self.b3 / 2.0, self.d2 + self.d3 + self.d4),
            (self.b4 / 2.0, self.d1 - self.d6),
            (self.b4 / 2.0, self.d1),
        ]
        return r + [(-x, y) for x, y in reversed(r)]


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
            b1=float(row["b1_soffit_width"]),
            b2=float(row["b2_bottom_flange_upper_width"]),
            b3=float(row["b3_web_width"]),
            b4=float(row["b4_top_flange_width"]),
            d1=float(row["d1_depth"]),
            d2=float(row["d2_bottom_flange_depth"]),
            d3=float(row["d3_bottom_splay"]),
            d4=float(row["d4_web"]),
            d5=float(row["d5_top_splay"]),
            d6=float(row["d6_top_flange_depth"]),
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the beam (millimetres)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["CivilconIBeamDimensions", "CivilconIBeamSection"]
