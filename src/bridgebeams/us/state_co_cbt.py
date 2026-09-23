"""Colorado DOT CBT37.5-CBT90 Colorado Bulb Tee girders.

Source: CDOT Staff Bridge worksheet B-618-CBT2 "Prestressed Concrete CBT"
(revisions through 9/24), single sheet. The CBT 90 detail is fully
dimensioned (50 in top flange, 7 in web, 39 1/2 in bottom flange, 3/4 in
soffit chamfers); the other depths are "similar except as shown" and differ
only in the clear web ("Ref") height. The sheet's property table (A, Ix, Iy,
yb) is reproduced to print precision by this outline.

Gross concrete only. Millimetres, origin at the soffit centre, y upward.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import INCH_TO_MM, ccw_polygon, load_json, mirror_half, to_mm

DATA_FILE = "state_co_cbt.json"


def cbt_right_half_in(depth: float, t: dict) -> list[tuple[float, float]]:
    """Right-half outline (inches) from soffit centre to top centre."""
    tw = t["web_width"] / 2
    bb = t["bottom_flange_width"] / 2
    tt = t["top_flange_width"] / 2
    c = t["soffit_chamfer"]
    ye = t["bottom_edge_height"]
    yt = ye + t["bottom_taper_rise"]
    y_top_edge = depth - t["top_edge_thickness"]
    y_bevel = y_top_edge - t["top_taper_rise"]
    return [
        (0.0, 0.0),
        (bb - c, 0.0),
        (bb, c),
        (bb, ye),
        (tw + t["bottom_bevel_run"], yt),
        (tw, yt + t["bottom_bevel_rise"]),
        (tw, y_bevel - t["top_bevel_rise"]),
        (tw + t["top_bevel_run"], y_bevel),
        (tt, y_top_edge),
        (tt, depth),
        (0.0, depth),
    ]


@dataclass(frozen=True)
class CoCbtDimensions:
    """CBT girder dimensions in millimetres (source values are inches)."""

    size: str
    depth: float
    top_flange_width: float
    bottom_flange_width: float
    web_width: float
    right_half: tuple[tuple[float, float], ...]


class CoCbtGirderSection:
    """CDOT Colorado Bulb Tee girder, e.g. ``CoCbtGirderSection("CBT63")``."""

    SIZES = ("CBT37.5", "CBT45", "CBT54", "CBT63", "CBT72", "CBT81", "CBT90")

    def __init__(self, size: str = "CBT63"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = load_json(DATA_FILE)
        row = data["sections"][size]
        t = data["template_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.published = row["published"]
        half = cbt_right_half_in(row["depth_in"], t)
        self._ring_in = mirror_half(half)
        self.dimensions = CoCbtDimensions(
            size=size,
            depth=row["depth_in"] * INCH_TO_MM,
            top_flange_width=t["top_flange_width"] * INCH_TO_MM,
            bottom_flange_width=t["bottom_flange_width"] * INCH_TO_MM,
            web_width=t["web_width"] * INCH_TO_MM,
            right_half=tuple(to_mm(half)),
        )

    @property
    def polygon(self):
        """Gross concrete outline (mm), anticlockwise."""
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["CoCbtDimensions", "CoCbtGirderSection", "cbt_right_half_in"]
