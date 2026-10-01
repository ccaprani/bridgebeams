"""Nepal Department of Roads standard precast RC I beams, 1300 and 1700.

Source: Government of Nepal, Ministry of Physical Infrastructure and
Transport, Department of Roads (Bridge Branch), *Standard Superstructure
Drawing for Road Bridges*, "RC Deck with Precast RC Beams", 20.0 m and
25.0 m simply supported spans, Drg. No. 5/10 "General Arrangement Drawing
and Dimensions" (PDF p7), with Drg. No. 7/10 Detail 'Y' (PDF p9)
confirming the 325 web and 187.5 splay. Dated July 14, 2015.

The beams are reinforced concrete, not prestressed. The midspan outline is
fully dimensioned: 700 top and bottom flanges, 325 web, 150 top flange +
65 top splay, 685/1085 clear web, 150 bottom splay + 250 bottom flange.

Chamfer convention (best estimate): sheet Note 4 says "Chamfer 12mm x 12mm
shall be provided at all junctions of the formwork unless otherwise
specified", but no chamfer is drawn. Here a 12 x 12 mm chamfer (12 mm
along each adjoining face) is cut at the six salient corners formed by two
formwork faces: the two soffit corners, the two bottom-flange shoulders and
the two top-flange underside corners. The two top edges (free, roughened
casting surface, Note 8) and the four re-entrant web/splay junctions are
left sharp. The chamfers remove 392.5 mm2, about 0.06% of the gross area.
Pass ``chamfer=False`` for the sharp nominal outline.

Millimetres, origin at mid-soffit, y upwards. Gross concrete only;
intermediate stiffeners and 700-wide rectangular end blocks are excluded.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.np")
        .joinpath("data/dor_precast_rc_i.json")
        .read_text(encoding="utf-8")
    )


def _chamfer(prev: tuple[float, float], corner: tuple[float, float],
             nxt: tuple[float, float], leg: float) -> list[tuple[float, float]]:
    """Replace ``corner`` with two points ``leg`` along each adjoining edge."""
    out = []
    for other in (prev, nxt):
        dx, dy = other[0] - corner[0], other[1] - corner[1]
        length = math.hypot(dx, dy)
        out.append((corner[0] + leg * dx / length, corner[1] + leg * dy / length))
    return out


@dataclass(frozen=True)
class DorPrecastRcIDimensions:
    """Midspan outline dimensions in millimetres."""

    depth: float
    web_height: float
    top_width: float = 700.0
    bottom_width: float = 700.0
    web_width: float = 325.0
    top_vertical: float = 150.0
    upper_splay_height: float = 65.0
    lower_splay_height: float = 150.0
    bottom_vertical: float = 250.0
    chamfer: float = 12.0

    def __post_init__(self) -> None:
        chain = (self.top_vertical + self.upper_splay_height + self.web_height
                 + self.lower_splay_height + self.bottom_vertical)
        if abs(chain - self.depth) > 1e-9:
            raise ValueError(f"vertical dimension chain {chain} does not close to depth {self.depth}")

    @property
    def sharp_half_profile(self) -> list[tuple[float, float]]:
        """Right half from the soffit centreline to the top centreline, no chamfers."""
        b, w, t = self.bottom_width / 2, self.web_width / 2, self.top_width / 2
        y1 = self.bottom_vertical
        y2 = y1 + self.lower_splay_height
        y3 = y2 + self.web_height
        y4 = y3 + self.upper_splay_height
        return [(0.0, 0.0), (b, 0.0), (b, y1), (w, y2), (w, y3), (t, y4), (t, self.depth),
                (0.0, self.depth)]

    @property
    def half_profile(self) -> list[tuple[float, float]]:
        """Right half with 12 x 12 chamfers at the three salient formed corners.

        Chamfered vertices (indices in :attr:`sharp_half_profile`): 1 soffit
        corner, 2 bottom-flange shoulder, 5 top-flange underside corner.
        """
        pts = self.sharp_half_profile
        if self.chamfer <= 0:
            return pts
        out: list[tuple[float, float]] = []
        for i, p in enumerate(pts):
            if i in (1, 2, 5):
                out.extend(_chamfer(pts[i - 1], p, pts[i + 1], self.chamfer))
            else:
                out.append(p)
        return out


class DorPrecastRcISection:
    """Nepal DoR precast RC I beam: ``1300`` (20 m span) or ``1700`` (25 m span)."""

    SIZES = ("1300", "1700")

    def __init__(self, size: str = "1300", chamfer: bool = True) -> None:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["sizes"] if r["size"] == size)
        self.size = size
        self.record = row
        self.span_m = row["span_m"]
        self.construction = "RC"
        self.prestressed = False
        self.provenance = row["provenance"] if chamfer else "transcribed"
        self.source_status = data["source_status"]
        d = row["dimensions_mm"]
        self.dimensions = DorPrecastRcIDimensions(
            depth=float(d["depth"]), web_height=float(d["web_height"]),
            chamfer=12.0 if chamfer else 0.0)

    @property
    def polygon(self) -> Polygon:
        # Drop the two centreline points; polygon_from_half_profile mirrors about x = 0.
        half = [p for p in self.dimensions.half_profile if p[0] != 0.0]
        return polygon_from_half_profile(half)

    @property
    def geometry(self):
        """Return the gross concrete ``sectionproperties`` geometry."""
        return geometry_from_polygon(self.polygon)


__all__ = ["DorPrecastRcIDimensions", "DorPrecastRcISection"]
