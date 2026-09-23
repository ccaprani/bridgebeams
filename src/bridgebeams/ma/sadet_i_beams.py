"""SADET (Morocco) I40/I45/I50/I55 prestressed I-beams — ESTIMATES.

Source: SADET brochure "Poutres industrielles", PDF page 2 (raster graphic
240 x 143 px plus a table). The table prints only the base width (40/45/50/
55 cm), limiting span and mass per metre; the graphic shows four symmetric
I outlines with web callouts 10/15/20/25 cm.

The graphic is drawn to one consistent scale: each outline's pixel base
width divided by its printed base gives 10.98-11.11 mm/px for all four,
and the web callouts measure 111/165/211/253 mm (one stroke width above the
printed 100/150/200/250). Everything except base width and web width is
therefore SCALED from that graphic (about +/-11 mm per pixel) and is an
estimate: overall depth 1220 mm (all four drawn at the same depth), top
flange 210 mm vertical edge then a 100 mm taper to the web, bottom taper
100 mm and bottom flange 150 mm; top flange width equals the base width.

The printed masses imply areas 4-10 % above these outlines for I45-I55 at an
assumed 2500 kg/m3 (density not stated). The printed I40 mass (282 kg/m)
is inconsistent with the rest of the family and is preserved, not used.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile

_DATA = json.loads((Path(__file__).parent / "data" / "sadet_i_beams.json").read_text())


@dataclass(frozen=True)
class SadetIBeamDimensions:
    """Millimetres; origin at soffit centre, y up.

    ``base_width`` and ``web_width`` are printed; all heights are scaled
    estimates from the brochure graphic.
    """

    base_width: float
    web_width: float
    depth: float = 1220.0
    bottom_flange: float = 150.0
    bottom_taper: float = 100.0
    top_taper: float = 100.0
    top_flange: float = 210.0

    @property
    def top_width(self) -> float:
        return self.base_width

    @property
    def outline(self) -> list[tuple[float, float]]:
        b, w, t = self.base_width / 2, self.web_width / 2, self.top_width / 2
        y1 = self.bottom_flange
        y2 = y1 + self.bottom_taper
        y4 = self.depth - self.top_flange
        y3 = y4 - self.top_taper
        return [(b, 0.0), (b, y1), (w, y2), (w, y3), (t, y4), (t, self.depth)]


class SadetIBeamSection:
    """SADET I40-I55 gross section (producer brochure; estimate)."""

    SIZES = ("I40", "I45", "I50", "I55")

    def __init__(self, size: str = "I50"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = next(r for r in _DATA["sections"] if r["section"] == size)
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.source_status = _DATA["source_status"]
        est = _DATA["estimated_dimensions"]
        self.dimensions = SadetIBeamDimensions(
            base_width=float(row["base_width"]),
            web_width=float(row["web_width_callout"]),
            depth=est["depth"],
            bottom_flange=est["bottom_flange"],
            bottom_taper=est["bottom_taper"],
            top_taper=est["top_taper"],
            top_flange=est["top_flange"],
        )

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.outline)

    @property
    def geometry(self):
        """Return the gross concrete ``sectionproperties`` geometry."""
        return geometry_from_polygon(self.polygon)


__all__ = ["SadetIBeamDimensions", "SadetIBeamSection"]
