"""Qatar Ashghal TY and TYE pretensioned beams (QCS 2014 standard details).

Sources: Ashghal SD 5-1-111 Rev 1 "TY - Beams" and SD 5-1-112 Rev 1
"TYE - Beams" (October 2013; revised logo/drawing number 23/10/2013).
Both one-sheet AutoCAD drawings were read visually at 400 dpi.

TY (symmetric inverted-tee): 750 mm base, 25 x 25 mm bottom chamfers,
110 mm near-vertical flange edge inset 5 mm, 105 mm sloping flange top to
the 227.5 mm offset, an 80 mm splay 50 mm wide to a 185 mm web that tapers
linearly to 400 mm at 850 mm (TY10). Shallower TYn are truncations of the
same outline at depth 400 + 50(n-1) mm; the drawing's printed rounded
widths (217 ... 380) are the tapered-web widths at those levels.

TYE (edge beam): the TY right half joined to a vertical outer face at
x = -375 mm; only the soffit corner of that face carries the 25 mm chamfer.
Top width 575 mm at TYE10.

All ten TY rows reproduce the published area within 0.07 %, centroid within
0.5 mm and inertia within 0.05 %. TYE areas are 0.13-0.16 % BELOW the
published values (pinned, not fitted). The table header labels I as
"x10^10 mm^4" but the values are x10^8 mm^4 (checked against Zt/Zb and yb).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile

_DATA = json.loads((Path(__file__).parent / "data" / "r2_ty_beams.json").read_text())


@dataclass(frozen=True)
class QaTyBeamDimensions:
    """Millimetres; origin at soffit centre, y up (SD 5-1-111 / 112)."""

    depth: float
    base_width: float = 750.0
    chamfer: float = 25.0
    flange_edge_height: float = 110.0
    flange_edge_inset: float = 5.0
    flange_slope_height: float = 105.0
    flange_slope_run: float = 227.5
    splay_height: float = 80.0
    splay_run: float = 50.0
    web_bottom_width: float = 185.0
    top_width_at_850: float = 400.0

    @property
    def web_bottom_level(self) -> float:
        return self.chamfer + self.flange_edge_height + self.flange_slope_height + self.splay_height

    def web_width_at(self, y: float) -> float:
        """Full TY web width at height ``y`` (linear taper 185 -> 400 over 320 -> 850)."""
        y0 = self.web_bottom_level
        return self.web_bottom_width + (y - y0) * (self.top_width_at_850 - self.web_bottom_width) / (850.0 - y0)

    @property
    def right_half(self) -> list[tuple[float, float]]:
        """TY right half from the soffit (chamfer end) to the top corner."""
        b = self.base_width / 2
        y1 = self.chamfer
        y2 = y1 + self.flange_edge_height
        y3 = y2 + self.flange_slope_height
        x2 = b - self.flange_edge_inset
        x3 = x2 - self.flange_slope_run
        return [
            (b - self.chamfer, 0.0),
            (b, y1),
            (x2, y2),
            (x3, y3),
            (x3 - self.splay_run, self.web_bottom_level),
            (self.web_width_at(self.depth) / 2, self.depth),
        ]


class _AshghalBase:
    SIZES: tuple[str, ...] = ()
    _KEY = ""

    def __init__(self, size: str):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = _DATA["families"][self._KEY]
        row = next(r for r in fam["sections"] if r["section"] == size)
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.source_status = _DATA["source_status"]
        self.dimensions = QaTyBeamDimensions(depth=float(row["depth"]))

    @property
    def geometry(self):
        """Return the gross concrete ``sectionproperties`` geometry."""
        return geometry_from_polygon(self.polygon)


class QaTyBeamSection(_AshghalBase):
    """Ashghal TY1-TY10 (SD 5-1-111 Rev 1), symmetric gross section."""

    SIZES = tuple(f"TY{i}" for i in range(1, 11))
    _KEY = "TY"

    def __init__(self, size: str = "TY5"):
        super().__init__(size)

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.right_half)


class QaTyeBeamSection(_AshghalBase):
    """Ashghal TYE1-TYE10 edge beams (SD 5-1-112 Rev 1).

    The vertical outer (edge) face is on the left, at x = -375 mm.
    """

    SIZES = tuple(f"TYE{i}" for i in range(1, 11))
    _KEY = "TYE"

    def __init__(self, size: str = "TYE5"):
        super().__init__(size)

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        b = d.base_width / 2
        pts = [(-(b - d.chamfer), 0.0), *d.right_half, (-b, d.depth), (-b, d.chamfer)]
        return orient(Polygon(pts), 1.0)


__all__ = ["QaTyBeamDimensions", "QaTyBeamSection", "QaTyeBeamSection"]
