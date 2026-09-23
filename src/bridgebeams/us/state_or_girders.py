"""Oregon DOT precast prestressed slabs, boxes and I-girders.

Sources (URLs, SHA-256 and page locators in data/state_or_girders.json):

* Oregon Standard Drawings 2024, BR400 series (effective 2026-06-01 to
  2026-11-30): BR400-BR422 12/15/18/21/26/30 in slabs, BR425-BR440
  33/39/42/48 in boxes, each with printed Area, c.g., I (and J).
* Oregon Standard Drawings 2024, BR300 series: BR325/330/335/340 Type
  II/III/IV/V I-girder midspan sections (no printed properties).

All units are 48 in wide with a continuous grout keyway (interior unit,
keyed both faces). Gross concrete only; millimetres, origin at soffit
centre, y upwards.
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

DATA_FILE = "state_or_girders.json"
WIDTH_IN = 48.0
VOID_SEGMENTS = 96


def _data() -> dict:
    return load_json(DATA_FILE)


def or_keyed_half_in(depth: float, top_band: float, key_band: float, k: dict):
    """Right half (inches) of a 48 in keyed slab/box outline, square corners."""
    h = WIDTH_IN / 2
    yk = depth - top_band - key_band
    return [
        (0.0, 0.0), (h, 0.0), (h, yk),
        (h - k["key_inset"], yk + k["lower_transition"]),
        (h - k["key_inset"], depth - top_band - k["upper_transition"]),
        (h - k["top_face_inset"], depth - top_band),
        (h - k["top_face_inset"], depth), (0.0, depth),
    ]


@dataclass(frozen=True)
class OrSlabDimensions:
    """ODOT slab dimensions in millimetres; voids as (x_centre, diameter)."""

    size: str
    depth: float
    width: float
    voids: tuple[tuple[float, float], ...]


class OrSlabSection:
    """ODOT 12/15/18/21/26/30 in precast prestressed slab (BR400-BR422)."""

    SIZES = ("12", "15", "18", "21", "26", "30")

    def __init__(self, size: str = "18"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _data()
        fam = data["slabs"]
        row = fam["sections"][size]
        self.size = size
        self.row = row
        self.provenance = "transcribed"
        self.source_status = fam["source_status"]
        self.published = row["published"]
        d = row["depth"]
        self._shell_in = mirror_half(or_keyed_half_in(d, 3.0, 4.0, data["key_template_in"]))
        self._voids_in = [circle(x, d / 2, dia / 2, VOID_SEGMENTS) for x, dia in row["voids"]]
        self.dimensions = OrSlabDimensions(
            size=size,
            depth=d * INCH_TO_MM,
            width=WIDTH_IN * INCH_TO_MM,
            voids=tuple((x * INCH_TO_MM, dia * INCH_TO_MM) for x, dia in row["voids"]),
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(self._shell_in), [to_mm(v) for v in self._voids_in])

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class OrBoxDimensions:
    """ODOT box dimensions in millimetres."""

    size: str
    depth: float
    width: float
    web: float
    slab: float
    void_width: float
    void_height: float
    void_chamfer: float


class OrBoxSection:
    """ODOT 33/39/42/48 in precast prestressed box (BR425-BR440)."""

    SIZES = ("33", "39", "42", "48")
    WEB, SLAB, VOID_CHAMFER = 5.0, 5.5, 3.0

    def __init__(self, size: str = "42"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _data()
        fam = data["boxes"]
        row = fam["sections"][size]
        self.size = size
        self.row = row
        self.provenance = "transcribed"
        self.source_status = fam["source_status"]
        self.published = row["published"]
        d = row["depth"]
        self._shell_in = mirror_half(or_keyed_half_in(d, 6.0, 6.0, data["key_template_in"]))
        x = WIDTH_IN / 2 - self.WEB
        c = self.VOID_CHAMFER
        y0, y1 = self.SLAB, d - self.SLAB
        self._void_in = [(x - c, y0), (x, y0 + c), (x, y1 - c), (x - c, y1),
                         (-x + c, y1), (-x, y1 - c), (-x, y0 + c), (-x + c, y0)]
        self.dimensions = OrBoxDimensions(
            size=size, depth=d * INCH_TO_MM, width=WIDTH_IN * INCH_TO_MM,
            web=self.WEB * INCH_TO_MM, slab=self.SLAB * INCH_TO_MM,
            void_width=2 * x * INCH_TO_MM, void_height=(y1 - y0) * INCH_TO_MM,
            void_chamfer=c * INCH_TO_MM,
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(self._shell_in), [to_mm(self._void_in)])

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class OrIGirderDimensions:
    """ODOT I-girder dimensions in millimetres."""

    size: str
    depth: float
    top_width: float
    bottom_width: float
    web_width: float
    soffit_chamfer: float
    right_half: tuple[tuple[float, float], ...]


class OrIGirderSection:
    """ODOT Type II/III/IV/V prestressed I-girder (BR325-BR340 midspan)."""

    SIZES = ("II", "III", "IV", "V")

    def __init__(self, size: str = "IV"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = _data()["i_girders"]
        r = fam["sections"][size]
        c = fam["soffit_chamfer"]
        self.size = size
        self.row = r
        self.provenance = fam["provenance"]
        self.source_status = fam["source_status"]
        self.published = None
        d = r["depth"]
        bb, tw, tt = r["bottom_width"] / 2, r["web_width"] / 2, r["top_width"] / 2
        half = [
            (0.0, 0.0), (bb - c, 0.0), (bb, c), (bb, r["bottom_edge"]),
            (tw, r["bottom_edge"] + r["bottom_taper"]),
            (tw, d - r["top_edge"] - r["top_taper"]),
            (tt, d - r["top_edge"]), (tt, d), (0.0, d),
        ]
        self._ring_in = mirror_half(half)
        self.dimensions = OrIGirderDimensions(
            size=size, depth=d * INCH_TO_MM,
            top_width=r["top_width"] * INCH_TO_MM,
            bottom_width=r["bottom_width"] * INCH_TO_MM,
            web_width=r["web_width"] * INCH_TO_MM,
            soffit_chamfer=c * INCH_TO_MM,
            right_half=tuple(to_mm(half)),
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "OrSlabDimensions", "OrSlabSection",
    "OrBoxDimensions", "OrBoxSection",
    "OrIGirderDimensions", "OrIGirderSection",
    "or_keyed_half_in",
]
