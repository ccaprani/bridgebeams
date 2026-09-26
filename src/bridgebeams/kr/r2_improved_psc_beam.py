"""Korean 개량형 PSC BEAM (improved PSC beam) standard sections, H = 1.4/1.7/2.0 m.

Source: 국토해양부 대전지방국토관리청, 개량형 PSC BEAM 표준도 (appendix to the
research report 개량형 PSC BEAM 적용방안), October 2008, CODIL OTMCRK110390.
The 중앙부 (midspan) views are on PDF pp 5, 12, 19, 27, 34 and 41.

Printed midspan outline: top flange 1200 wide (500+200+500) with a 150
vertical side, then a 60 mm underside taper to the 200 web. The bottom
flange is 1000 wide (400+200+400), with a 175 vertical side and a 150 taper.
Radii: R50 at the top-flange underside corner, R150 at the web fillets and
R100 at the bottom-flange shoulders. The H=1.4/1.7 sheets print the
bottom-flange side as "75". That does not close the vertical chain; 175
(printed on the H=2.0 sheet, PDF p19) is adopted, as documented in the JSON.

Millimetres, origin at mid-soffit, y upwards. Gross midspan concrete only.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "r2_improved_psc_beam.json"


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.kr").joinpath(f"data/{_DATA_FILE}").read_text(encoding="utf-8")
    )


def _fillet(vertices: list[tuple[float, float, float]], segments: int = 16) -> list[tuple[float, float]]:
    """Polyline with tangent circular fillets at interior vertices ``(x, y, r)``."""
    out = [(vertices[0][0], vertices[0][1])]
    for i in range(1, len(vertices) - 1):
        bx, by, r = vertices[i]
        if r <= 0:
            out.append((bx, by))
            continue
        ax, ay = vertices[i - 1][0], vertices[i - 1][1]
        cx, cy = vertices[i + 1][0], vertices[i + 1][1]
        u = (ax - bx, ay - by)
        v = (cx - bx, cy - by)
        lu, lv = math.hypot(*u), math.hypot(*v)
        u = (u[0] / lu, u[1] / lu)
        v = (v[0] / lv, v[1] / lv)
        theta = math.acos(max(-1.0, min(1.0, u[0] * v[0] + u[1] * v[1])))
        t = r / math.tan(theta / 2)
        if t > lu or t > lv:
            raise ValueError(f"radius {r} too large at vertex {i}")
        bis = (u[0] + v[0], u[1] + v[1])
        lb = math.hypot(*bis)
        d = r / math.sin(theta / 2)
        centre = (bx + bis[0] / lb * d, by + bis[1] / lb * d)
        p = (bx + u[0] * t, by + u[1] * t)
        q = (bx + v[0] * t, by + v[1] * t)
        a0 = math.atan2(p[1] - centre[1], p[0] - centre[0])
        a1 = math.atan2(q[1] - centre[1], q[0] - centre[0])
        sweep = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        for k in range(segments + 1):
            a = a0 + sweep * k / segments
            out.append((centre[0] + r * math.cos(a), centre[1] + r * math.sin(a)))
    out.append((vertices[-1][0], vertices[-1][1]))
    return out


@dataclass(frozen=True)
class ImprovedPscBeamDimensions:
    """Midspan dimensions (mm). Heights measured from the soffit/top as named."""

    depth: float
    web_height: float
    top_width: float = 1200.0
    web_width: float = 200.0
    bottom_width: float = 1000.0
    top_edge: float = 150.0
    top_splay: float = 60.0
    bottom_splay: float = 150.0
    bottom_edge: float = 175.0
    r_top_corner: float = 50.0
    r_web: float = 150.0
    r_bottom_shoulder: float = 100.0

    def __post_init__(self) -> None:
        chain = (self.top_edge + self.top_splay + self.web_height
                 + self.bottom_splay + self.bottom_edge)
        if abs(chain - self.depth) > 1e-6:
            raise ValueError(f"vertical chain {chain} does not close to depth {self.depth}")

    @property
    def sharp_right_half(self) -> list[tuple[float, float, float]]:
        """Right-half vertices ``(x, y, radius)`` from soffit centre to top centre."""
        b, w, t = self.bottom_width / 2, self.web_width / 2, self.top_width / 2
        y1 = self.bottom_edge
        y2 = y1 + self.bottom_splay
        y3 = y2 + self.web_height
        y4 = y3 + self.top_splay
        return [
            (0.0, 0.0, 0.0),
            (b, 0.0, 0.0),
            (b, y1, self.r_bottom_shoulder),
            (w, y2, self.r_web),
            (w, y3, self.r_web),
            (t, y4, self.r_top_corner),
            (t, self.depth, 0.0),
            (0.0, self.depth, 0.0),
        ]

    @property
    def right_half(self) -> list[tuple[float, float]]:
        """Filleted right half, excluding the two centreline points."""
        pts = _fillet(self.sharp_right_half)
        return pts[1:-1]


class ImprovedPscBeamSection:
    """Korean 개량형 PSC BEAM midspan section: ``"H1400"``, ``"H1700"`` or ``"H2000"``.

    Examples
    --------
    >>> from bridgebeams.kr.r2_improved_psc_beam import ImprovedPscBeamSection
    >>> ImprovedPscBeamSection("H1700").dimensions.web_height
    1165.0
    """

    SIZES = ("H1400", "H1700", "H2000")

    def __init__(self, size: str = "H1700") -> None:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sizes"][size]
        self.size = size
        self.record = row
        self.span_m = tuple(row["span_m"])
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        d = row["dimensions_mm"]
        self.dimensions = ImprovedPscBeamDimensions(
            depth=float(d["depth"]), web_height=float(d["web_height"])
        )

    @property
    def polygon(self) -> Polygon:
        right = self.dimensions.right_half
        left = [(-x, y) for x, y in reversed(right)]
        return Polygon(left + right)

    @property
    def geometry(self):
        """Gross concrete ``sectionproperties`` geometry (mm)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["ImprovedPscBeamDimensions", "ImprovedPscBeamSection"]
