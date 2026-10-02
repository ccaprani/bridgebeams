"""GPRM Prestress (Hawaii) Keehi IV and VI prestressed bridge girders.

Source: GPRM *Keehi Girders*, four undated sheets K-VI W, K-VI,
K-IV W and K-IV. PDF metadata records creation/modification in 2010;
the sheets' issued/revised fields are blank. All dimensions are printed
in inches. Public geometry is millimetres, origin at the soffit centre.

Wide flanges use the printed maximum width (57 or 56.5 in) and 3 in
edge thickness. Project-specific narrower flanges are not additional
profiles. IV MOD adds the printed 4 in to the top flange of IV.

The polygons retain the printed 3/4 in soffit chamfers and 3/4 in
lower-web radii, represented by 64 straight segments per arc. Unlabelled
upper corners remain sharp. Published properties largely describe the
sharp outline without those corner details; discrepancies are retained
in the source data and independent checks rather than fitted away.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import (
    INCH_TO_MM,
    ccw_polygon,
    filleted_path,
    load_json,
    mirror_half,
    to_mm,
)

ARC_SEGMENTS = 64


@dataclass(frozen=True)
class GprmKeehiDimensions:
    """Principal dimensions in mm, with the original inch dimensions."""

    size: str
    depth: float
    top_width: float
    web_width: float
    bottom_width: float
    source_in: dict


class GprmKeehiGirderSection:
    """Five explicitly dimensioned Keehi profiles; wide variants at maximum width."""

    SIZES = ("K-VI W", "K-VI", "K-IV W", "K-IV", "K-IV MOD")

    def __init__(self, size: str = "K-VI"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        self.size = size
        self.row = load_json("gprm_keehi_girders.json")["sections"][size]
        self.published = self.row["published_in"]
        self.provenance = self.row["provenance"]
        self.source_status = self.row["source_status"]
        d = self.row["dimensions_in"]
        self.dimensions = GprmKeehiDimensions(
            size=size,
            depth=d["depth"] * INCH_TO_MM,
            top_width=d["top_width"] * INCH_TO_MM,
            web_width=d["web_width"] * INCH_TO_MM,
            bottom_width=d["bottom_width"] * INCH_TO_MM,
            source_in=dict(d),
        )

    def _right_half_in(self):
        d = self.dimensions.source_in
        xb, xw, xt = d["bottom_width"] / 2, d["web_width"] / 2, d["top_width"] / 2
        c = d["soffit_chamfer"]
        y_web_bottom = d["bottom_edge"] + d["bottom_splay"]
        y_web_top = y_web_bottom + d["web_height"]
        points = [
            (0.0, 0.0), (xb - c, 0.0), (xb, c),
            (xb, d["bottom_edge"]), (xw, y_web_bottom), (xw, y_web_top),
        ]
        if d["top_splay_height"]:
            points.append((xw + d["top_splay_run"], y_web_top + d["top_splay_height"]))
        points.extend([(xt, d["depth"] - d["top_edge"]), (xt, d["depth"]), (0.0, d["depth"])])
        return filleted_path(points, {4: d["lower_web_radius"]}, ARC_SEGMENTS)

    @property
    def polygon(self):
        """Gross concrete polygon in mm, excluding steel and local project details."""
        return ccw_polygon(to_mm(mirror_half(self._right_half_in())))

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["GprmKeehiDimensions", "GprmKeehiGirderSection"]
