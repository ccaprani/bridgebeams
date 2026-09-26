"""WSDOT trapezoidal tub girders U54/U66/U78 and UF60/UF72/UF84 (G4/G5/G6).

Geometry: WSDOT Bridge Design Manual M 23-50.01 (June 2006), Appendix A,
drawings 5.6-A1-5 (open tubs, PDF p. 444) and 5.6-A1-6 (tubs with top
flanges, PDF p. 445). G4/G5/G6 = 4'-0"/5'-0"/6'-0" bottom width. Webs
slope 1 horizontal : 7 vertical and are 7 in thick measured square to the
sloping face (7*sqrt(50)/7 = 7.0711 in horizontally). Bottom slab 6 in;
web-to-slab fillets rise to 1'-0" above the soffit with a horizontal run of
1'-0" (G4/G5) or 1'-6" (G6), as drawn.

UF flange block: 3 in inner and 5 in outer overhang beyond the web faces
at 6 in below the top, 4 1/2 in square edges and 1 1/2 in tapers down to
the web faces. The printed block width 1'-3 1/16" is the 1/16 in rounding
of 3 + 7.0711 + 5 = 15.0711 in (convention recorded in the JSON).

Validation: G4/G5 match WSDOT BDM M 23-50.24 (June 2025) Table 5.6.1-1
and the 2006 table exactly (A, Yb, Ix; Iy vs 2025). G6 (2006 table only)
are short by 36.0 in^2 with the drawn 1'-6" fillet run; a 2'-0" run
reproduces the 2006 G6 A, Yb and Ix exactly for all six G6 sizes, so the
2006 table and drawing disagree. The drawn geometry is implemented and the
discrepancy pinned in tests. UF84 and all G6 sizes were dropped by 2025.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us._wsdot_common import (
    INCH_TO_MM,
    ccw_polygon,
    dedupe,
    load_data,
    to_mm,
)


def tub_ring_in(depth: float, bottom_width: float, fillet_run: float, t: dict,
                flange: dict | None = None) -> list[tuple[float, float]]:
    """Closed outline in inches (open-top U, optionally with UF flange blocks)."""
    slope = t["web_slope_h_per_v"]
    th = t["web_thickness_normal_in"] * math.sqrt(1 + slope**2)
    b = bottom_width / 2
    rise = t["fillet_top_height_in"]
    slab = t["bottom_slab_in"]

    def xo(y):
        return b + slope * y

    def xi(y):
        return b + slope * y - th

    right = [(b, 0.0)]
    if flange is None:
        right += [(xo(depth), depth), (xi(depth), depth)]
    else:
        y1 = depth - flange["web_junction_below_top_in"]
        ye = depth - flange["edge_height_in"]
        xout = xo(y1) + flange["outer_overhang_in"]
        xin = xi(y1) - flange["inner_overhang_in"]
        right += [(xo(y1), y1), (xout, ye), (xout, depth), (xin, depth), (xin, ye), (xi(y1), y1)]
    right += [(xi(rise), rise), (xi(rise) - fillet_run, slab)]
    left = [(-x, y) for x, y in reversed(right)]
    return dedupe(right + left)


@dataclass(frozen=True)
class WsdotTubDimensions:
    """Tub dimensions in millimetres (source values are inches)."""

    size: str
    depth: float
    bottom_width: float
    web_thickness_normal: float
    bottom_slab: float
    fillet_run: float
    has_top_flange: bool


class WsdotTubGirderSection:
    """WSDOT U- and UF-series tub girders in G4/G5/G6 bottom widths."""

    SIZES = tuple(
        f"{d}G{g}" for d in ("U54", "U66", "U78", "UF60", "UF72", "UF84") for g in (4, 5, 6)
    )

    def __init__(self, size: str = "U54G4"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = load_data()["families"]["TUB"]
        row = fam["sections"][size]
        t = fam["template_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row.get("published_2025") or row.get("published_2006")
        flange = fam["uf_flange_in"] if size.startswith("UF") else None
        self._ring_in = tub_ring_in(row["depth_in"], row["bottom_width_in"], row["fillet_run_in"], t, flange)
        self.dimensions = WsdotTubDimensions(
            size=size,
            depth=row["depth_in"] * INCH_TO_MM,
            bottom_width=row["bottom_width_in"] * INCH_TO_MM,
            web_thickness_normal=t["web_thickness_normal_in"] * INCH_TO_MM,
            bottom_slab=t["bottom_slab_in"] * INCH_TO_MM,
            fillet_run=row["fillet_run_in"] * INCH_TO_MM,
            has_top_flange=flange is not None,
        )

    @property
    def polygon(self):
        """Gross concrete outline (mm), anticlockwise, open top."""
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["WsdotTubDimensions", "WsdotTubGirderSection", "tub_ring_in"]
