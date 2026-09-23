"""Virginia DOT PCBT bulb-tees, voided slabs and box beams.

Sources: VDOT Manual of the Structure and Bridge Division, Part 2,
Chapter 12 (File Nos. 12.03-5, 12.05-5, 12.05-10, 12.06-6, 12.06-11) and
Part 4 standard PCBT-53S (28 Apr 2023). See ``data/state_va_girders.json``
for URLs, SHA-256, page locators and every convention.

* ``VaPcbtSection``: PCBT-29 ... PCBT-93. Fully dimensioned outline; the
  undimensioned soffit chamfer is taken as 3/4 in, which reproduces the
  published A, yb and I to print precision.
* ``VaVoidedSlabSection``: 3 ft / 4 ft wide, 15/18/21 in deep, circular
  voids, VDOT shear key. ``shear_keys=False`` gives the published
  (key-less) property convention exactly.
* ``VaBoxBeamSection``: 3 ft / 4 ft wide, 27/33/39/42 in deep, 6 in slabs,
  5 in webs, 3 in void chamfers, VDOT shear key. The published net
  properties deduct a different (PCI) key; residuals are recorded.

Gross concrete only. Millimetres, origin at the soffit centre, y upward.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import (
    INCH_TO_MM,
    ccw_polygon,
    circle,
    load_json,
    mirror_half,
    to_mm,
)

DATA_FILE = "state_va_girders.json"


def _family(name: str) -> dict:
    return load_json(DATA_FILE)["families"][name]


def pcbt_right_half_in(depth: float, t: dict) -> list[tuple[float, float]]:
    """PCBT right-half outline (inches), soffit centre to top centre."""
    tw = t["web_width"] / 2
    bb = t["bottom_flange_width"] / 2
    tt = t["top_flange_width"] / 2
    c = t["soffit_chamfer"]
    ye = t["bottom_edge_height"]
    yt = ye + t["bottom_taper_rise"]
    y_edge = depth - t["top_edge_thickness"]
    y_bev = y_edge - t["top_taper_rise"]
    pts = [(0.0, 0.0)]
    if c:
        pts += [(bb - c, 0.0), (bb, c)]
    else:
        pts += [(bb, 0.0)]
    pts += [
        (bb, ye),
        (tw + t["bottom_bevel_run"], yt),
        (tw, yt + t["bottom_bevel_rise"]),
        (tw, y_bev - t["top_bevel_rise"]),
        (tw + t["top_bevel_run"], y_bev),
        (tt, y_edge),
        (tt, depth),
        (0.0, depth),
    ]
    return pts


def keyed_side_in(half_width: float, depth: float, key: dict | None) -> list[tuple[float, float]]:
    """Right side face from soffit corner to top corner with an optional VDOT key."""
    b = half_width
    if not key:
        return [(b, 0.0), (b, depth)]
    lo = key["lower_recess"]
    up = key["upper_recess"]
    y_bot = depth - key["total_depth"]
    y_up = depth - key["upper_depth"]
    return [
        (b, 0.0),
        (b, y_bot),
        (b - lo, y_bot + key["bottom_chamfer"]),
        (b - lo, y_up - key["transition"]),
        (b - up, y_up),
        (b - up, depth),
    ]


@dataclass(frozen=True)
class VaPcbtDimensions:
    """PCBT dimensions in millimetres (source values are inches)."""

    size: str
    depth: float
    top_flange_width: float
    bottom_flange_width: float
    web_width: float
    right_half: tuple[tuple[float, float], ...]


class VaPcbtSection:
    """VDOT PCBT bulb-tee, e.g. ``VaPcbtSection("PCBT-53")``."""

    SIZES = tuple(f"PCBT-{d}" for d in (29, 37, 45, 53, 61, 69, 77, 85, 93))

    def __init__(self, size: str = "PCBT-53"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = _family("PCBT")
        row = fam["sections"][size]
        t = fam["template_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = fam["source_status"]
        self.published = row["published"]
        half = pcbt_right_half_in(row["depth_in"], t)
        self._ring_in = mirror_half(half)
        self.dimensions = VaPcbtDimensions(
            size=size,
            depth=row["depth_in"] * INCH_TO_MM,
            top_flange_width=t["top_flange_width"] * INCH_TO_MM,
            bottom_flange_width=t["bottom_flange_width"] * INCH_TO_MM,
            web_width=t["web_width"] * INCH_TO_MM,
            right_half=tuple(to_mm(half)),
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class VaVoidedSlabDimensions:
    """Voided slab dimensions in millimetres."""

    size: str
    width: float
    depth: float
    voids: tuple[tuple[float, float, float], ...]  # (x centre, y centre, diameter)
    shear_keys: bool


class VaVoidedSlabSection:
    """VDOT voided slab ``"<width in>x<depth in>"``, e.g. ``"36x18"``."""

    SIZES = ("36x15", "36x18", "36x21", "48x15", "48x18", "48x21")

    def __init__(self, size: str = "36x18", shear_keys: bool = True):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = _family("VOIDED_SLAB")
        row = fam["sections"][size]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = fam["source_status"]
        self.published = row["published"]
        w, d = row["width_in"], row["depth_in"]
        yc = d - row["C_in"]
        if row["void_d2_in"] is None:
            xs = [(-row["B_in"] / 2, row["void_d1_in"]), (row["B_in"] / 2, row["void_d1_in"])]
        else:
            xs = [(-row["B_in"], row["void_d1_in"]), (0.0, row["void_d2_in"]),
                  (row["B_in"], row["void_d1_in"])]
        self._voids_in = [(x, yc, dia) for x, dia in xs]
        side = keyed_side_in(w / 2, d, fam["shear_key_in"] if shear_keys else None)
        self._ring_in = mirror_half([(0.0, 0.0)] + side + [(0.0, d)])
        self.dimensions = VaVoidedSlabDimensions(
            size=size,
            width=w * INCH_TO_MM,
            depth=d * INCH_TO_MM,
            voids=tuple((x * INCH_TO_MM, y * INCH_TO_MM, dia * INCH_TO_MM)
                        for x, y, dia in self._voids_in),
            shear_keys=shear_keys,
        )

    @property
    def polygon(self):
        holes = [circle(x, y, dia / 2, 96) for x, y, dia in self.dimensions.voids]
        return ccw_polygon(to_mm(self._ring_in), holes)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class VaBoxBeamDimensions:
    """Box beam dimensions in millimetres."""

    size: str
    width: float
    depth: float
    top_slab: float
    bottom_slab: float
    web: float
    void_chamfer: float
    shear_keys: bool


class VaBoxBeamSection:
    """VDOT interior box beam ``"<width in>x<depth in>"``, e.g. ``"48x33"``."""

    SIZES = ("36x27", "36x33", "36x39", "36x42", "48x27", "48x33", "48x39", "48x42")

    def __init__(self, size: str = "48x33", shear_keys: bool = True):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = _family("BOX")
        row = fam["sections"][size]
        v = fam["void_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = fam["source_status"]
        self.published = row["published"]
        w, d = row["width_in"], row["depth_in"]
        side = keyed_side_in(w / 2, d, fam["shear_key_in"] if shear_keys else None)
        self._ring_in = mirror_half([(0.0, 0.0)] + side + [(0.0, d)])
        bx = w / 2 - v["web"]
        y0, y1, c = v["bottom_slab"], d - v["top_slab"], v["chamfer"]
        self._void_in = [(bx - c, y0), (bx, y0 + c), (bx, y1 - c), (bx - c, y1),
                         (-bx + c, y1), (-bx, y1 - c), (-bx, y0 + c), (-bx + c, y0)]
        self.dimensions = VaBoxBeamDimensions(
            size=size,
            width=w * INCH_TO_MM,
            depth=d * INCH_TO_MM,
            top_slab=v["top_slab"] * INCH_TO_MM,
            bottom_slab=v["bottom_slab"] * INCH_TO_MM,
            web=v["web"] * INCH_TO_MM,
            void_chamfer=c * INCH_TO_MM,
            shear_keys=shear_keys,
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(self._ring_in), [to_mm(self._void_in)])

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "VaPcbtDimensions", "VaPcbtSection",
    "VaVoidedSlabDimensions", "VaVoidedSlabSection",
    "VaBoxBeamDimensions", "VaBoxBeamSection",
    "pcbt_right_half_in", "keyed_side_in",
]
