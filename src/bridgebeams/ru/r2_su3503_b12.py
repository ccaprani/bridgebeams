"""Russian Soyuzdorproekt series 3.503.1-81 (Vypusk 5-1): 12 m precast
pretensioned I-beams B1200.174.90 / B1200.194.90 (edge beams) and
B1200.140.90 / B1200.180.90 (intermediate beams).

Marking: ``B<length cm>.<top slab width by concrete, cm>.<height cm>``
(sheet 3.503.1-81.5-1-T, PDF p9). Midspan section Б-Б from the formwork
drawings 3.503.1-81.5-1-1ФЧ (PDF p10) and -11ФЧ (PDF p23): 900 high, 150 thick
top slab, 160 web, R300 haunches tangent to the slab and web, R200 fillets
tangent to the web and to a 1:1 splay (141/172/100 vertical chain), bottom
flange 620 wide at 100 mm tapering to 600 at the soffit.

The top slab of the edge beams is asymmetric: 1040 mm from the beam axis on
the outer (cantilever) side, ``e`` = 700/900 mm on the inner side; the
intermediate beams have ``e`` on both sides. The outer cantilever is placed
on the -x side. Protruding joint loops (264 mm, drawn thin) are not concrete.

Geometry convention: millimetres, origin at mid-soffit on the web axis,
y upwards.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "r2_su3503_b12.json"

_HEIGHT = 900.0
_T_SLAB = 150.0
_WEB = 160.0
_R_HAUNCH = 300.0
_R_FILLET = 200.0
_H_BOT = 100.0  # bottom flange edge height (620 wide)
_H_SPLAY = 172.0  # 1:1 splay height (printed)
_W_BOT = 620.0
_W_SOFFIT = 600.0


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ru.data").joinpath(_DATA_FILE).read_text(encoding="utf-8")
    )


def _arc(cx, cy, r, a0, a1, n=12):
    return [
        (cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n))
        for i in range(n + 1)
    ]


def _web_right() -> list[tuple[float, float]]:
    """Right web face from the slab underside down to the soffit."""
    aw = _WEB / 2.0
    y_slab = _HEIGHT - _T_SLAB
    pts = _arc(aw + _R_HAUNCH, y_slab - _R_HAUNCH, _R_HAUNCH, math.pi / 2, math.pi)
    # R200 fillet: tangent to the web, ending tangent to the 1:1 splay
    y_fillet = _H_BOT + _H_SPLAY + _R_FILLET * math.sin(math.pi / 4)  # 141 printed
    pts += _arc(aw + _R_FILLET, y_fillet, _R_FILLET, math.pi, 1.25 * math.pi, 8)
    x_end, y_end = pts[-1]
    pts += [(x_end + (y_end - _H_BOT), _H_BOT), (_W_SOFFIT / 2.0, 0.0)]
    return pts


@dataclass(frozen=True)
class Su3503B12Dimensions:
    """Dimensions of one 12 m beam mark, millimetres."""

    length_mm: float
    top_width: float
    slab_left: float  # from beam axis, -x side (1040 cantilever on edge beams)
    slab_right: float  # e, +x side
    height: float = _HEIGHT
    slab_thickness: float = _T_SLAB
    web_thickness: float = _WEB
    bottom_flange_width: float = _W_BOT
    soffit_width: float = _W_SOFFIT

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Full outline, anti-clockwise from the soffit."""
        web = _web_right()  # top -> bottom
        y_slab = self.height - self.slab_thickness
        right = list(reversed(web)) + [
            (self.slab_right, y_slab),
            (self.slab_right, self.height),
            (-self.slab_left, self.height),
            (-self.slab_left, y_slab),
        ]
        left = [(-x, y) for x, y in web]
        return right + left


class Su3503B12Section:
    """Soyuzdorproekt 3.503.1-81 Vypusk 5-1 12 m I-beam (midspan section) as a
    ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.ru.r2_su3503_b12 import Su3503B12Section
    >>> Su3503B12Section("B1200.174.90").dimensions.top_width
    1740.0
    """

    SIZES = ("B1200.174.90", "B1200.194.90", "B1200.140.90", "B1200.180.90")

    source_status = "historic standard (series 3.503.1-81, Vypusk 5-1, 1988)"

    def __init__(self, size: str = "B1200.174.90"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sizes"][size]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.dimensions = Su3503B12Dimensions(
            length_mm=float(row["length_mm"]),
            top_width=float(row["top_width_mm"]),
            slab_left=float(row["slab_left_mm"]),
            slab_right=float(row["e_mm"]),
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the beam (millimetres)."""
        return geometry_from_polygon(self.polygon)

    @property
    def volume_area(self) -> float:
        """Average area implied by the published concrete volume / length."""
        return self.published["volume_m3"] * 1e9 / self.published["length_mm"]


__all__ = ["Su3503B12Dimensions", "Su3503B12Section"]
