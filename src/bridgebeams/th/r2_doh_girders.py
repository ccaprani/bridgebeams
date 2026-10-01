"""Thai DOH 2015 standard precast plank girders, box beams and I-girders.

Source: Kingdom of Thailand, Department of Highways, *Standard Drawings for
Highway Design and Construction, 2015 Revision* (2018 edition), scanned PDF:

- PG-101 (sheet 208/R1, PDF p225): PC plank girders, spans 5-12 m,
  interior and exterior planks (12 m planks have three 150 mm voids).
- BB-101 (sheet 212/R1, PDF p229): PC box beams, 15 m and 20 m spans,
  interior and exterior beams with one octagonal void.
- IG-103 (sheet 217/R1, PDF p234) and IG-205 (sheet 223/R1, PDF p240):
  15 m and 20 m I-girders.

Drawing units are metres; this module works in millimetres, origin at the
middle of the soffit, y upwards. Exterior units carry the shear-key profile
on the left and the exposed vertical face on the right (+x). Conventions
and estimates are listed in ``data/r2_doh_girders.json``.

``ThDohIGirderR2Section("IG20")`` is the same physical girder as the
pre-existing :class:`bridgebeams.th.ThDOHIGirderSection` but resolves its
625 mm web + 200 mm bottom splay; do not count both profiles.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon

SOURCE_STATUS = "current national standard drawing (DOH 2015 revision, 2018 edition)"


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.th")
        .joinpath("data/r2_doh_girders.json")
        .read_text(encoding="utf-8")
    )


def _mm(v: float) -> float:
    return round(v * 1000.0, 6)


def _key_side(h: float, y_face: float, y_key: float, half: float, key: float,
              top_inset: float, chamfer: float) -> list[tuple[float, float]]:
    """Right-hand keyed side from the soffit corner up to the top corner."""
    pts = []
    if chamfer:
        pts += [(half - chamfer, 0.0), (half, chamfer)]
    else:
        pts.append((half, 0.0))
    pts += [(half, y_face), (half - key, y_key), (half - top_inset, h)]
    return pts


def _plain_side(h: float, half: float, chamfer: float) -> list[tuple[float, float]]:
    if chamfer:
        return [(half - chamfer, 0.0), (half, chamfer), (half, h)]
    return [(half, 0.0), (half, h)]


def _outline(h, y_face, y_key, half, key, top_inset, chamfer, exterior):
    right_keyed = _key_side(h, y_face, y_key, half, key, top_inset, chamfer)
    if exterior:
        right = _plain_side(h, half, chamfer)
    else:
        right = right_keyed
    left = [(-x, y) for x, y in reversed(right_keyed)]
    return right + left


# ---------------------------------------------------------------- planks


@dataclass(frozen=True)
class ThDohPlankDimensions:
    """PG-101 plank dimensions (mm). ``h1``: vertical outer face height;
    ``h2``: height of the 70 mm key point."""

    span_m: int
    h: float
    h1: float
    h2: float
    width: float = 990.0
    key_inset: float = 70.0
    top_inset: float = 45.0
    chamfer: float = 20.0
    void_diameter: float = 0.0
    void_centre: float = 0.0


class ThDohPlankGirderSection:
    """DOH PG-101 prestressed plank girder, interior (``-INT``) or exterior
    (``-EXT``) unit, e.g. ``"PG12-INT"``.

    Examples
    --------
    >>> ThDohPlankGirderSection("PG8-INT").dimensions.h
    280.0
    """

    SPANS = (5, 6, 7, 8, 9, 10, 12)
    SIZES = tuple(f"PG{s}-{u}" for s in SPANS for u in ("INT", "EXT"))
    source_status = SOURCE_STATUS

    def __init__(self, size: str = "PG10-INT", circle_points: int = 64):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        if circle_points < 16:
            raise ValueError("circle_points must be >= 16")
        data = _load_data()["plank"]
        span = size[2:].split("-")[0]
        row = data["table_m"][span]
        c = data["common_m"]
        voided = span == "12"
        self.size = size
        self.unit = "exterior" if size.endswith("EXT") else "interior"
        self.circle_points = circle_points
        self.provenance = "transcribed-with-convention"
        self.published = {"source_m": row}
        self.dimensions = ThDohPlankDimensions(
            span_m=int(span), h=_mm(row["h"]), h1=_mm(row["h1"]), h2=_mm(row["h2"]),
            void_diameter=_mm(c["void_diameter_12m"]) if voided else 0.0,
            void_centre=_mm(c["void_centre_12m"]) if voided else 0.0,
        )

    def _void_x(self) -> list[float]:
        if not self.dimensions.void_diameter:
            return []
        if self.unit == "interior":
            return [-250.0, 0.0, 250.0]
        x0 = -self.dimensions.width / 2
        return [x0 + 240.0, x0 + 540.0, x0 + 810.0]

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        ring = _outline(d.h, d.h1, d.h2, d.width / 2, d.key_inset, d.top_inset,
                        d.chamfer, self.unit == "exterior")
        r = d.void_diameter / 2
        n = self.circle_points
        holes = [[(x + r * math.cos(2 * math.pi * i / n), d.void_centre + r * math.sin(2 * math.pi * i / n))
                  for i in range(n)] for x in self._void_x()]
        return orient(Polygon(ring, holes), sign=1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


# ---------------------------------------------------------------- boxes


@dataclass(frozen=True)
class ThDohBoxBeamDimensions:
    """BB-101 box-beam dimensions (mm), labels as on the drawing table."""

    span_m: int
    h: float
    h1: float
    h3: float
    h4: float
    h5: float
    h7: float
    b1: float
    b2: float
    b3: float
    width: float = 990.0
    key_inset: float = 70.0
    key_rise: float = 70.0
    top_inset: float = 45.0


class ThDohBoxBeamSection:
    """DOH BB-101 prestressed box beam, e.g. ``"BB15-INT"`` or ``"BB20-EXT"``.

    Examples
    --------
    >>> ThDohBoxBeamSection("BB20-INT").dimensions.h
    700.0
    """

    SIZES = ("BB15-INT", "BB15-EXT", "BB20-INT", "BB20-EXT")
    source_status = SOURCE_STATUS

    def __init__(self, size: str = "BB15-INT"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()["box"]
        span = size[2:4]
        row = data["table_m"][span]
        self.size = size
        self.unit = "exterior" if size.endswith("EXT") else "interior"
        self.provenance = "transcribed-with-convention"
        self.published = {"source_m": row}
        b3 = row["b3_exterior"] if self.unit == "exterior" else row["b3_interior"]
        self.dimensions = ThDohBoxBeamDimensions(
            span_m=int(span), h=_mm(row["h"]), h1=_mm(row["h1"]), h3=_mm(row["h3"]),
            h4=_mm(row["h4"]), h5=_mm(row["h5"]), h7=_mm(row["h7"]),
            b1=_mm(row["b1"]), b2=_mm(row["b2"]), b3=_mm(b3),
        )

    def void(self) -> list[tuple[float, float]]:
        d = self.dimensions
        x0 = -d.width / 2 + d.key_inset + d.b1
        x1 = x0 + 2 * d.b2 + d.b3
        y0, y1 = d.h3, d.h - d.h1
        return [(x0 + d.b2, y0), (x1 - d.b2, y0), (x1, y0 + d.h4), (x1, y1 - d.h4),
                (x1 - d.b2, y1), (x0 + d.b2, y1), (x0, y1 - d.h4), (x0, y0 + d.h4)]

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        ring = _outline(d.h, d.h7, d.h7 + d.key_rise, d.width / 2, d.key_inset,
                        d.top_inset, 0.0, self.unit == "exterior")
        return orient(Polygon(ring, [self.void()]), sign=1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


# ---------------------------------------------------------------- I-girders


@dataclass(frozen=True)
class ThDohIGirderR2Dimensions:
    depth: float
    top_width: float
    top_edge: float
    top_haunch: float
    web: float
    web_height: float
    bottom_splay: float
    bottom_edge: float
    bottom_width: float
    chamfer: float = 20.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        b, w, t, c = self.bottom_width / 2, self.web / 2, self.top_width / 2, self.chamfer
        y1 = self.bottom_edge
        y2 = y1 + self.bottom_splay
        y3 = y2 + self.web_height
        y4 = y3 + self.top_haunch
        right = [(b - c, 0.0), (b, c), (b, y1), (w, y2), (w, y3), (t, y4), (t, self.depth)]
        return right + [(-x, y) for x, y in reversed(right)]


class ThDohIGirderR2Section:
    """DOH IG-103 (15 m) / IG-205 (20 m) I-girder midspan section.

    Examples
    --------
    >>> ThDohIGirderR2Section("IG15").dimensions.web
    150.0
    """

    SIZES = ("IG15", "IG20")
    source_status = SOURCE_STATUS

    def __init__(self, size: str = "IG15"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load_data()["igirder"]["table_m"][size]
        self.size = size
        self.provenance = "transcribed-with-convention"
        self.published = {"source_m": row}
        self.dimensions = ThDohIGirderR2Dimensions(**{k: _mm(v) for k, v in row.items()})

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline), sign=1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "ThDohBoxBeamDimensions",
    "ThDohBoxBeamSection",
    "ThDohIGirderR2Dimensions",
    "ThDohIGirderR2Section",
    "ThDohPlankDimensions",
    "ThDohPlankGirderSection",
]
