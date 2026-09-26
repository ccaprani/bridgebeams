"""Missouri DOT (MoDOT) prestressed I girders and NU girders.

Source: MoDOT Engineering Policy Guide 751.22 "Prestressed Concrete I
Girders", 751.22.1.2 Geometric Properties (figures dated 2022),
https://epg.modot.org/index.php/751.22_Prestressed_Concrete_I_Girders

* ``MoDotIGirderSection``: Type 2, 3, 4 and 6 with their modified-web
  variants, and bulb-tee Types 7 and 8 (14 profiles).
* ``MoDotNuGirderSection``: MoDOT's NU 35, 43, 53, 63, 70 and 78
  drawings (6 profiles). These are MoDOT's inch-rounded NU outlines
  (1 3/8 in top taper); they are not asserted equal to NDOT drawings.

Every dimension is printed on the figures and every profile reproduces the
printed A, yb, Ixx and Iyy to print precision. Gross concrete only.
Millimetres, origin at soffit centre, y upward.
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

DATA_FILE = "state_mo_girders.json"
ARC_SEGMENTS = 64


def tapered_i_half_in(d: dict) -> list[tuple[float, float]]:
    """Right half (inches) of a straight-tapered I girder with soffit bevels.

    ``d`` holds top/web/bottom widths, bottom edge, list of bottom tapers
    (rise, run) from the flange edge inwards, straight web height, list of
    top tapers (rise, run) from the web outwards and top edge thickness.
    """
    bev = d.get("soffit_bevel", 0.0)
    x = d["bottom_width"] / 2
    pts = [(0.0, 0.0)]
    pts += [(x - bev, 0.0), (x, bev)] if bev else [(x, 0.0)]
    y = d["bottom_edge"]
    pts.append((x, y))
    for rise, run in d["bottom_tapers_rise_run"]:
        x -= run
        y += rise
        pts.append((x, y))
    if abs(x - d["web_width"] / 2) > 1e-9:
        raise ValueError("bottom tapers do not close on the web face")
    y += d["web_height"]
    pts.append((x, y))
    for rise, run in d["top_tapers_rise_run"]:
        x += run
        y += rise
        pts.append((x, y))
    if abs(x - d["top_width"] / 2) > 1e-9:
        raise ValueError("top tapers do not close on the flange edge")
    y += d["top_edge"]
    pts += [(x, y), (0.0, y)]
    return pts


def nu_half_in(depth: float, t: dict, n: int = ARC_SEGMENTS) -> list[tuple[float, float]]:
    """Right half of an NU-type girder: tapers to web faces, tangent fillets."""
    bw, ch = t["bottom_width"] / 2, t.get("soffit_chamfer", 0.0)
    w, tw = t["web_width"] / 2, t["top_width"] / 2
    yb1 = t["bottom_edge"]
    yb2 = yb1 + t["bottom_taper"]
    yt2 = depth - t["top_edge"]
    yt1 = yt2 - t["top_taper"]
    pts = [(0.0, 0.0)]
    pts += [(bw - ch, 0.0), (bw, ch)] if ch else [(bw, 0.0)]
    pts += [(bw, yb1), (w, yb2), (w, yt1), (tw, yt2), (tw, depth), (0.0, depth)]
    k = len(pts)
    rc, rw = t["flange_corner_radius"], t["web_fillet_radius"]
    return filleted_path(pts, {k - 6: rc, k - 5: rw, k - 4: rw, k - 3: rc}, n)


@dataclass(frozen=True)
class MoDotIGirderDimensions:
    """Principal dimensions in millimetres (source inches in ``source_in``)."""

    size: str
    depth: float
    top_width: float
    web_width: float
    bottom_width: float
    source_in: dict


class MoDotIGirderSection:
    """MoDOT Type 2/3/4/6 (with modified webs) and bulb-tee Type 7/8."""

    SIZES = (
        "Type2", "Type2-7", "Type2-8",
        "Type3", "Type3-7", "Type3-8",
        "Type4", "Type4-7", "Type4-8",
        "Type6", "Type6-7.5", "Type6-8.5",
        "Type7", "Type8",
    )

    def __init__(self, size: str = "Type6"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = load_json(DATA_FILE)["i_girders"][size]
        d = row["dimensions_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row["published_in"]
        self._half_in = tapered_i_half_in(d)
        self.dimensions = MoDotIGirderDimensions(
            size=size,
            depth=self._half_in[-1][1] * INCH_TO_MM,
            top_width=d["top_width"] * INCH_TO_MM,
            web_width=d["web_width"] * INCH_TO_MM,
            bottom_width=d["bottom_width"] * INCH_TO_MM,
            source_in=dict(d),
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(mirror_half(self._half_in)))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class MoDotNuDimensions:
    """NU dimensions in millimetres; ``template_in`` holds the source inches."""

    size: str
    depth: float
    top_width: float
    web_width: float
    bottom_width: float
    template_in: dict


class MoDotNuGirderSection:
    """MoDOT NU 35/43/53/63/70/78 girders (MoDOT drawings, inches)."""

    SIZES = ("NU35", "NU43", "NU53", "NU63", "NU70", "NU78")

    def __init__(self, size: str = "NU53"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = load_json(DATA_FILE)
        row = data["nu_girders"][size]
        t = data["nu_template_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row["published_in"]
        self._half_in = nu_half_in(row["depth_in"], t)
        self.dimensions = MoDotNuDimensions(
            size=size,
            depth=row["depth_in"] * INCH_TO_MM,
            top_width=t["top_width"] * INCH_TO_MM,
            web_width=t["web_width"] * INCH_TO_MM,
            bottom_width=t["bottom_width"] * INCH_TO_MM,
            template_in=dict(t),
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(mirror_half(self._half_in)))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "MoDotIGirderDimensions", "MoDotIGirderSection",
    "MoDotNuDimensions", "MoDotNuGirderSection",
    "tapered_i_half_in", "nu_half_in",
]
