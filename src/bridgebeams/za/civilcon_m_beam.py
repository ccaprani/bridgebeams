"""Civilcon M2–M10 I-beams ("M beam"): fitted reconstruction.

PPBM page 1 prints only part of the outline: the 970 mm base, 35 mm chamfer,
125 mm flange edge, 50 mm flange taper, 80 mm lower splay, and the lower
web heights 200 (M2–M4), 440 (M5–M7) and 680 (M8–M10) above the splay.
The web width, top flange width, top notch, flare and flange-edge inset
are not printed. This class uses a reconstruction:

* Web width is 160 mm and top flange width is 400 mm. These are derived exactly from the
  published area steps: +32000 mm² per 80 mm within a group and -25600 mm²
  across groups. They are confirmed by scaling (160.0/400.8 mm).
* The top notch is 50 × 50 mm each side, leaving a 300 mm raised strip. This is scaled
  from the drawing: line centres at x = 150.4 and y = D - 50.0. A free fit gives
  49.5 mm. Colin Caprani's 40 × 50 mm reading is not supported by the
  scaled drawing or the properties.
* The flange-taper break half-width is 160 mm, giving a 45° 80 × 80 splay to the web. This is
  scaled from the drawing.
* The upper flare is 120 mm horizontal × 60 mm vertical, and the flange edge is inset 15 mm
  over the 125 mm edge. These are fitted: with them all eight usable
  published areas close exactly, centroids agree within 0.4 mm and moduli
  within 0.12% (except M8 Zt, see below). **The drawing is different.** It scales to
  an 80 mm flare rise and a 10 mm inset. That drawn outline is 1525 mm² (0.3–0.5%) short on every
  area and up to 1.6% low on Zt. The fitted values are the best estimate
  of the geometry behind the published properties, not a transcription.

Source discrepancies are preserved: the M4 area is printed as 37860, and
378600 closes exactly. The M10 table depth is 360, while the drawing label is 1360 and
Zt is consistent with 1360. The M8 Zt is internally inconsistent with its
Zb and Yb (1.16%). Colin Caprani suggested these are UK M beams, but that
equivalence is unverified and no alias is provided.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.za.data").joinpath("civilcon_m_beams.json").read_text()
    )


@dataclass(frozen=True)
class CivilconMBeamDimensions:
    """Millimetres; origin at the soffit centre, y positive upwards.

    ``lower_web_height`` is the printed 200/440/680 above the 290 mm web
    start. ``flare_height`` and ``edge_inset`` are fitted to the published
    properties (drawing scales 80 and 10); web/top widths are derived and
    the notch and taper break are scaled.
    """

    depth: float
    lower_web_height: float
    flare_height: float = 60.0
    edge_inset: float = 15.0
    notch_width: float = 50.0
    notch_depth: float = 50.0
    base_width: float = 970.0
    chamfer: float = 35.0
    flange_edge: float = 125.0
    taper_height: float = 50.0
    taper_break_half_width: float = 160.0
    splay_height: float = 80.0
    web_width: float = 160.0
    top_width: float = 400.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Right half from the soffit up to the top centre."""
        b = self.base_width / 2
        y1 = self.chamfer + self.flange_edge
        y2 = y1 + self.taper_height
        y3 = y2 + self.splay_height
        y4 = y3 + self.lower_web_height
        w, t = self.web_width / 2, self.top_width / 2
        return [
            (b - self.chamfer, 0.0),
            (b, self.chamfer),
            (b - self.edge_inset, y1),
            (self.taper_break_half_width, y2),
            (w, y3),
            (w, y4),
            (t, y4 + self.flare_height),
            (t, self.depth - self.notch_depth),
            (t - self.notch_width, self.depth - self.notch_depth),
            (t - self.notch_width, self.depth),
        ]


class CivilconMBeamSection:
    """Civilcon M2–M10 gross concrete section (PPBM), fitted reconstruction."""

    SIZES = tuple(f"M{i}" for i in range(2, 11))

    def __init__(self, size: str = "M6"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["sections"] if r["section"] == size)
        fit = data["fitted_parameters"]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = CivilconMBeamDimensions(
            depth=row["depth_used"],
            lower_web_height=row["lower_web_height"],
            flare_height=fit["flare_height"],
            edge_inset=fit["edge_inset"],
        )

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.outline)

    @property
    def geometry(self):
        """Return the gross concrete ``sectionproperties`` geometry."""
        return geometry_from_polygon(self.polygon)


__all__ = ["CivilconMBeamDimensions", "CivilconMBeamSection"]
