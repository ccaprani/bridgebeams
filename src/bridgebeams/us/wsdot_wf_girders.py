"""WSDOT wide-flange prestressed I-girders WF36G-WF100G.

Geometry: WSDOT Bridge Design Manual M 23-50.01 (June 2006), Appendix A,
drawing 5.6-A1-2 "Precast Prestressed Wide Flange Girders", PDF p. 441.
One depth-parametric template (49 in top flange, 6 1/8 in web, 38 3/8 in
bottom flange) is drawn for WF42G/WF50G/WF58G/WF74G/W83G/W95G; WF36G,
WF66G and WF100G are the same template at their current depths.
Validation: WSDOT BDM M 23-50.24 (June 2025) Table 5.6.1-1, PDF p. 95;
all nine sizes reproduce the published A, Yb, Ix and Iy to print
precision. The 2006 sheet's W83G/W95G are the current WF83G/WF95G.

``WF100G-61`` is the 2025 "WF100G with 5'-1" Top Flange" row. It is not
drawn in the 2006 manual; the outline adds a 3 in thick, 6 in flat
extension to each flange tip, a reconstruction that reproduces all four
published properties exactly (provenance ``fitted-reconstruction``).

Gross concrete only: no strands, deck, end blocks or recesses.
Millimetres, origin at soffit centre, y upward.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us._wsdot_common import (
    INCH_TO_MM,
    ccw_polygon,
    load_data,
    mirrored_ring_in,
    to_mm,
)


def wf_right_half_in(depth: float, top_width: float, t: dict) -> list[tuple[float, float]]:
    """Right-half outline in inches from the 5.6-A1-2 template ``t``."""
    tw = t["web_width_in"] / 2
    bb = t["bottom_flange_width_in"] / 2
    c = t["bottom_chamfer_in"]
    ye = t["bottom_edge_height_in"]
    yt = ye + t["bottom_taper_rise_in"]
    bev_b = t["bottom_bevel_in"]
    top_edge = t["top_edge_in"]
    top_taper = t["top_taper_in"]
    bev_t = t["top_bevel_in"]
    std_half = t["standard_top_width_in"] / 2
    pts = [
        (0.0, 0.0),
        (bb - c, 0.0),
        (bb, c),
        (bb, ye),
        (tw + bev_b, yt),
        (tw, yt + bev_b),
        (tw, depth - top_edge - top_taper - bev_t),
        (tw + bev_t, depth - top_edge - top_taper),
        (std_half, depth - top_edge),
    ]
    if top_width / 2 > std_half:
        # WF100G 5'-1" flange: constant-thickness flat extension (fitted).
        pts.append((top_width / 2, depth - top_edge))
    pts += [(top_width / 2, depth), (0.0, depth)]
    return pts


@dataclass(frozen=True)
class WsdotWfDimensions:
    """WF girder dimensions in millimetres (source values are inches)."""

    size: str
    depth: float
    top_flange_width: float
    bottom_flange_width: float
    web_width: float
    right_half: tuple[tuple[float, float], ...]


class WsdotWfGirderSection:
    """WSDOT WF36G-WF100G wide-flange girders (plus the WF100G 5'-1" flange)."""

    SIZES = (
        "WF36G", "WF42G", "WF50G", "WF58G", "WF66G",
        "WF74G", "WF83G", "WF95G", "WF100G", "WF100G-61",
    )

    def __init__(self, size: str = "WF74G"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = load_data()["families"]["WF"]
        row = fam["sections"][size]
        t = fam["template_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row.get("published_2025")
        half_in = wf_right_half_in(row["depth_in"], row["top_flange_width_in"], t)
        self._ring_in = mirrored_ring_in(half_in)
        self.dimensions = WsdotWfDimensions(
            size=size,
            depth=row["depth_in"] * INCH_TO_MM,
            top_flange_width=row["top_flange_width_in"] * INCH_TO_MM,
            bottom_flange_width=t["bottom_flange_width_in"] * INCH_TO_MM,
            web_width=t["web_width_in"] * INCH_TO_MM,
            right_half=tuple(to_mm(half_in)),
        )

    @property
    def polygon(self):
        """Gross concrete outline (mm), anticlockwise."""
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["WsdotWfDimensions", "WsdotWfGirderSection", "wf_right_half_in"]
