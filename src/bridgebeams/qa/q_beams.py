"""Qatar Ashghal Q-girders, SD 5-1-101 Rev 1 (October 2013).

Five open-top precast sections reconstructed from visually read dimensions.
Dimensions are millimetres, origin at the soffit centre. These are gross
concrete sections without deck, reinforcement, formwork or diaphragms.

The source's rounded base widths, 1069 mm reference, 125 mm nominal web,
840 mm clear opening and 1:10.55 slope do not close perfectly as one exact
polygon. This reconstruction fixes the explicit per-type base/valley
values and the 840 mm opening at the 25 mm ledge; both webs follow the
1:10.55 slope. The nominal 125 mm normal web is approximately 122-123 mm
in this reconstruction and is NOT represented as exact. The optional
10 mm corner radii are replaced by the source's 13 x 13 chamfer option.

At the published 2150 mm top width, discrepancies from the source table
are at most 0.88% in area, 0.85% in centroid height and 1.26% in Ixx.
These residuals are recorded, not fitted away. This is a documented
reconstruction rather than an exact manufacturing profile.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA = json.loads((Path(__file__).parent / "data" / "q_beams.json").read_text())


@dataclass(frozen=True)
class QaQBeamDimensions:
    """Read dimensions and explicit gross-profile reconstruction."""

    depth: float
    base_width: float
    valley_height: float
    valley_rise: float
    top_width: float = 2150.0
    top_flange_thickness: float = 117.0
    clear_opening: float = 840.0
    haunch_reference_width: float = 1069.0
    haunch_width: float = 200.0
    haunch_height: float = 75.0
    ledge_width: float = 25.0
    ledge_depth: float = 25.0
    slope: float = 10.55
    chamfer: float = 13.0
    nominal_web_thickness: float = 125.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        d, c = self.depth, self.chamfer
        bf, tip = self.base_width / 2, self.top_width / 2
        yf = d - self.top_flange_thickness
        yh = yf - self.haunch_height
        xh = bf + yh / self.slope
        yi = self.valley_height + self.valley_rise
        xt = self.clear_opening / 2
        xi = xt - (d - self.ledge_depth - yi) / self.slope
        r = [
            (0.0, 0.0), (bf - c, 0.0), (bf + c / self.slope, c),
            (xh, yh), (self.haunch_reference_width / 2 + self.haunch_width, yf),
            (tip - c, yf), (tip, yf + c), (tip, d - c), (tip - c, d),
            (xt + self.ledge_width, d),
            (xt + self.ledge_width, d - self.ledge_depth),
            (xt, d - self.ledge_depth), (xi, yi), (0.0, self.valley_height),
        ]
        return r + [(-x, y) for x, y in reversed(r[1:-1])]


class QaQBeamSection:
    """Ashghal type T1-T5 with the published 2150 mm flange width.

    ``section_type`` is a source designation, e.g. ``"T3"``. Span ranges
    in the source data are indicative only and do not establish capacity.
    """

    TYPES = tuple(_DATA["sections"])

    # Documented reconstruction; dimensions do not close, residuals <=1.26% recorded.
    provenance = "fitted-reconstruction"
    source_status = "Ashghal SD 5-1-101 Rev 1 (Oct 2013)"

    def __init__(self, section_type: str = "T1"):
        if section_type not in self.TYPES:
            raise ValueError(f"section_type must be one of {self.TYPES}, got {section_type!r}")
        self.section_type = section_type
        row = _DATA["sections"][section_type]
        self.dimensions = QaQBeamDimensions(**row["dimensions_mm"])

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["QaQBeamDimensions", "QaQBeamSection"]
