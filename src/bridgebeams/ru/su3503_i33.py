"""Russian Soyuzdorproekt series 3.503.1-81 (Vypusk 7-1): 33 m precast
prestressed I-beams (B3300.174/194.153/173).

Marking per GOST 23009: ``B<length mm>.<top width dm>.<height dm>`` - e.g.
B3300.174.173 is 33 m long with a 1740 mm top slab and 1730 mm high. The
cross-section (top slab 1040+e wide x 180 with 30x30 edge notches, R300
haunches into a 200 web, 620-wide bottom flange with R200 fillets) was
recovered from the scanned release drawings (sheet 100/2-13); the bottom
flange thickness is least-squares fitted to the producer volume-derived
areas of all four marks (**rms 0.30%, max 0.32%** - see
``data/su3503_i33.json``). Design code context: SP 35.13330.

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres. Symmetric about x = 0.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "su3503_i33.json"

_T_SLAB = 180.0
_EDGE_NOTCH = 30.0
_R_HAUNCH = 283.8  # fitted; drawing R300
_R_FILLET = 223.9  # fitted; drawing R200
_BOTTOM_FLANGE_WIDTH = 620.0
_T_BOT = 196.9  # fitted bottom flange thickness


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ru.data").joinpath(_DATA_FILE).read_text()
    )


def _arc(cx: float, cy: float, r: float, a0: float, a1: float, n: int = 10):
    return [
        (cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n))
        for i in range(n + 1)
    ]


@dataclass(frozen=True)
class Su3503I33Dimensions:
    """Dimensions of one 33 m I-beam mark, millimetres."""

    length_mm: float
    height: float
    top_width: float
    e: float
    web_thickness: float = 200.0
    b2: float = 580.0
    c: float = 20.0
    volume_m3: float = 0.0
    mass_t: float = 0.0
    concrete: str = "B35"

    @property
    def bottom_flange_width(self) -> float:
        return _BOTTOM_FLANGE_WIDTH

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Full outline, anti-clockwise. Right half top->bottom with the
        R300 haunch fillet (centre below the slab) and the R200 bottom
        fillet (centre above the flange)."""
        h = self.height
        b = self.top_width
        aw = self.web_thickness / 2.0
        fl = self.bottom_flange_width / 2.0
        y_slab = h - _T_SLAB

        right = [
            (b / 2.0, h),
            (b / 2.0, y_slab),
            (aw + _R_HAUNCH, y_slab),
        ]
        # R300 haunch fillet: centre (aw+R, y_slab-R), 90 deg -> 180 deg
        right += _arc(aw + _R_HAUNCH, y_slab - _R_HAUNCH, _R_HAUNCH, math.pi / 2, math.pi, 10)
        y_web_bot = _T_BOT + _R_FILLET
        right += [(aw, y_web_bot)]
        # R200 bottom fillet: centre (aw+R, t_bot+R), 180 deg -> 270 deg
        right += _arc(aw + _R_FILLET, _T_BOT + _R_FILLET, _R_FILLET, math.pi, 1.5 * math.pi, 8)
        right += [(fl, _T_BOT), (fl, 0.0)]
        left = [(-x, y) for x, y in reversed(right)]
        return left + right


class Su3503I33Section:
    """Soyuzdorproekt 3.503.1-81 33 m I-beam as a ``sectionproperties``
    Geometry.

    Examples
    --------
    >>> from bridgebeams.ru import Su3503I33Section
    >>> beam = Su3503I33Section("B3300.174.173")
    >>> beam.dimensions.height
    1730.0
    """

    SIZES = (
        "B3300.174.153",
        "B3300.194.153",
        "B3300.174.173",
        "B3300.194.173",
    )

    def __init__(self, size: str = "B3300.174.173"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = Su3503I33Dimensions(
            length_mm=float(row["length_mm"]),
            height=float(row["height"]),
            top_width=float(row["top_width"]),
            e=float(row["e"]),
            volume_m3=float(row["volume_m3"]),
            mass_t=float(row["mass_t"]),
            concrete=row["concrete"],
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the beam (millimetres)."""
        return geometry_from_polygon(self.polygon)

    @property
    def target_area(self) -> float:
        """Section area implied by the published volume / length."""
        return self.published["volume_m3"] * 1e9 / self.published["length_mm"]


__all__ = ["Su3503I33Dimensions", "Su3503I33Section"]
