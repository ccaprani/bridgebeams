"""Wisconsin DOT prestressed I-girders (28 in, 36W-82W) and box girders.

Sources (data/state_wi_girders.json has URLs, SHA-256 and page locators):

* WisDOT Bridge Manual Chapter 19 Standard Details (std-ch19.pdf):
  Std 19.01/19.11/19.13/19.15/19.17/19.19 'SECTION THRU GIRDER' (PDF pp1-11,
  odd) with published A, yB, I on the paired design-data sheets
  19.02-19.20 (PDF pp2-12, even); Std 19.50/19.51 3'-0" and 4'-0" box girder
  sections (PDF pp21-22).
* WisDOT Bridge Manual Chapter 19 (January 2023) Table 19.3-3 (printed
  p19-46, PDF p46): box girder A, I, St, Sb, J.

36W-82W use one template: 30 in bottom flange, 6 1/2 in web, 7 1/2 in edge
+ 5 1/2 in taper, R = 8 in tangent fillets at both web junctions, 3/4 in
soffit bevels. The 28 in girder has straight tapers. The box shear-key
recess depth is an interpreted estimate (see ``geometry_notes``).

Gross concrete only; millimetres, origin at soffit centre, y upwards.
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

DATA_FILE = "state_wi_girders.json"


def _data() -> dict:
    return load_json(DATA_FILE)


def wi_girder_half_in(row: dict, template: dict) -> list[tuple[float, float]]:
    """Right-half outline (inches) from the soffit centre to the top centre."""
    d = row["depth"]
    if row["type"] == "straight":
        bb, tw, tt = row["bottom_width"] / 2, row["web_width"] / 2, row["top_width"] / 2
        bev = row["soffit_bevel"]
        ye = row["bottom_edge"]
        return [
            (0.0, 0.0), (bb - bev, 0.0), (bb, bev), (bb, ye),
            (tw, ye + row["bottom_taper"]),
            (tw, d - row["top_edge"] - row["top_taper"]),
            (tt, d - row["top_edge"]), (tt, d), (0.0, d),
        ]
    t = template
    bb, tw, tt = t["bottom_width"] / 2, t["web_width"] / 2, row["top_width"] / 2
    bev = t["soffit_bevel"]
    ye = t["bottom_edge"]
    pts = [
        (0.0, 0.0), (bb - bev, 0.0), (bb, bev), (bb, ye),
        (tw, ye + t["bottom_taper_rise"]),                 # 4: lower fillet corner
        (tw, d - row["top_edge"] - row["top_taper"]),     # 5: upper fillet corner
        (tt, d - row["top_edge"]), (tt, d), (0.0, d),
    ]
    r = t["fillet_radius"]
    return filleted_path(pts, {4: r, 5: r})


@dataclass(frozen=True)
class WiGirderDimensions:
    """WisDOT I-girder dimensions in millimetres."""

    size: str
    depth: float
    top_width: float
    bottom_width: float
    web_width: float
    right_half: tuple[tuple[float, float], ...]


class WiGirderSection:
    """WisDOT 28 in and 36W/45W/54W/72W/82W prestressed I-girders."""

    SIZES = ("28", "36W", "45W", "54W", "72W", "82W")

    def __init__(self, size: str = "54W"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = _data()["i_girders"]
        row = fam["sections"][size]
        t = fam["template_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row["published"]
        half = wi_girder_half_in(row, t)
        self._ring_in = mirror_half(half)
        straight = row["type"] == "straight"
        self.dimensions = WiGirderDimensions(
            size=size,
            depth=row["depth"] * INCH_TO_MM,
            top_width=row["top_width"] * INCH_TO_MM,
            bottom_width=(row["bottom_width"] if straight else t["bottom_width"]) * INCH_TO_MM,
            web_width=(row["web_width"] if straight else t["web_width"]) * INCH_TO_MM,
            right_half=tuple(to_mm(half)),
        )

    @property
    def polygon(self):
        """Gross concrete outline (mm), anticlockwise."""
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


def wi_box_rings_in(width: float, depth: float, t: dict):
    """(shell, void-or-None) rings in inches for a WisDOT box girder."""
    h = width / 2
    r = t["key_recess"]
    ch = t["soffit_chamfer"]
    ybot, ytop = t["key_bottom_band"], depth - t["key_top_band"]
    half = [
        (0.0, 0.0), (h - ch, 0.0), (h, ch), (h, ybot),
        (h - r, ybot + r), (h - r, ytop - r), (h, ytop),
        (h, depth), (0.0, depth),
    ]
    shell = mirror_half(half)
    if depth <= 12:
        return shell, None
    c = t["void_chamfer_deep"] if depth >= t["void_chamfer_switch_depth"] else t["void_chamfer_shallow"]
    x = h - r - t["web"]
    y0, y1 = t["bottom_slab"], depth - t["top_slab"]
    void = [(x - c, y0), (x, y0 + c), (x, y1 - c), (x - c, y1),
            (-x + c, y1), (-x, y1 - c), (-x, y0 + c), (-x + c, y0)]
    return shell, void


@dataclass(frozen=True)
class WiBoxGirderDimensions:
    """WisDOT box girder dimensions in millimetres."""

    size: str
    width: float
    depth: float
    section_no: int
    web: float
    key_recess: float


class WiBoxGirderSection:
    """WisDOT 3'-0" and 4'-0" prestressed box girders, sections 1-6.

    Sizes are ``"<width>x<depth>"`` in inches, e.g. ``"48x21"``.
    Interior unit with a shear-key recess on both faces (estimate).
    """

    SIZES = tuple(f"{w}x{d}" for w in (36, 48) for d in (12, 17, 21, 27, 33, 42))

    def __init__(self, size: str = "48x21"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = _data()["box_girders"]
        t = fam["template_in"]
        w, d = (float(v) for v in size.split("x"))
        self.size = size
        self.provenance = fam["provenance"]
        self.source_status = fam["source_status"]
        self.published = fam["published"][size]
        self._shell_in, self._void_in = wi_box_rings_in(w, d, t)
        self.dimensions = WiBoxGirderDimensions(
            size=size,
            width=w * INCH_TO_MM,
            depth=d * INCH_TO_MM,
            section_no=self.published["section_no"],
            web=t["web"] * INCH_TO_MM,
            key_recess=t["key_recess"] * INCH_TO_MM,
        )

    @property
    def polygon(self):
        holes = [to_mm(self._void_in)] if self._void_in else []
        return ccw_polygon(to_mm(self._shell_in), holes)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "WiGirderDimensions", "WiGirderSection",
    "WiBoxGirderDimensions", "WiBoxGirderSection",
    "wi_girder_half_in", "wi_box_rings_in",
]
