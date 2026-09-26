"""Haitsma Beton HKP box girders, HBM plank girders and HGR-500 edge beam.

Sources (see data/r2_haitsma.json): HKP-ligger folder (property table and
dimensioned sketch) with the april 2009 1:20 HKP profile drawings; HBM-450/550
and HGR-500 april 2009 1:10 profile drawings (vector CAD). Millimetres, origin
at mid-soffit, y upwards. HKP voids are polygon interiors.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(resources.files("bridgebeams.nl").joinpath("data/r2_haitsma.json").read_text(encoding="utf-8"))


@dataclass(frozen=True)
class HaitsmaHkpDimensions:
    """HKP folder profile (mm). ``depth`` = profile height H."""

    depth: float
    width: float = 1480.0
    top_slab: float = 230.0
    bottom_slab: float = 155.0
    void_width: float = 1200.0
    void_chamfer: float = 100.0
    side_band_height: float = 300.0
    side_recess: float = 10.0
    bottom_chamfer: float = 15.0

    @property
    def exterior(self) -> list[tuple[float, float]]:
        h, b, r, c = self.depth, self.width / 2, self.side_recess, self.bottom_chamfer
        yb = h - self.side_band_height
        right = [(b - c, 0.0), (b, c), (b, yb - r), (b - r, yb), (b - r, h)]
        return right + [(-x, y) for x, y in reversed(right)]

    @property
    def void(self) -> list[tuple[float, float]]:
        w, c = self.void_width / 2, self.void_chamfer
        y0, y1 = self.bottom_slab, self.depth - self.top_slab
        return [(w - c, y0), (w, y0 + c), (w, y1 - c), (w - c, y1),
                (-(w - c), y1), (-w, y1 - c), (-w, y0 + c), (-(w - c), y0)]


class HaitsmaHkpSection:
    """HKP-600 … HKP-1400 box/slab girder (1480 wide), folder-table edition."""

    SIZES = ("HKP-600", "HKP-650", "HKP-700", "HKP-800", "HKP-900", "HKP-1000",
             "HKP-1100", "HKP-1200", "HKP-1300", "HKP-1400")

    def __init__(self, size: str = "HKP-1000"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()["hkp"]
        h = size.split("-")[1]
        self.size = size
        self.published = dict(zip(("A_1e5mm2", "v_mm", "I_1e9mm4", "Qeg_kNm"), data["published"][h]))
        self.provenance = data["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = HaitsmaHkpDimensions(depth=float(h))

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        return orient(Polygon(d.exterior, [d.void]), 1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class HaitsmaHbmDimensions:
    depth: float
    half_profile: tuple[tuple[float, float], ...]


class HaitsmaHbmSection:
    """HBM-450 / HBM-550 solid plank girder (april 2009 drawings)."""

    SIZES = ("HBM-450", "HBM-550")

    def __init__(self, size: str = "HBM-450"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()["hbm"]
        self.size = size
        self.provenance = data["provenance"]
        self.source_status = data["source_status"]
        self.published = data["folder_table"][size.split("-")[1]]
        half = tuple(tuple(p) for p in data["half_profiles_mm"][size])
        self.dimensions = HaitsmaHbmDimensions(depth=half[-1][1], half_profile=half)

    @property
    def polygon(self) -> Polygon:
        right = list(self.dimensions.half_profile)
        return Polygon(right + [(-x, y) for x, y in reversed(right)])

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class HaitsmaHgrDimensions:
    depth: float
    outline: tuple[tuple[float, float], ...]


class HaitsmaHgrSection:
    """HGR-500 asymmetric edge beam (x = 0 at the middle of the 485 mm soffit)."""

    SIZES = ("HGR-500",)

    def __init__(self, size: str = "HGR-500"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()["hgr"]
        self.size = size
        self.provenance = data["provenance"]
        self.source_status = data["source_status"]
        pts = tuple((x - 242.5, y) for x, y in data["outline_mm_from_soffit_left"])
        self.dimensions = HaitsmaHgrDimensions(depth=max(y for _, y in pts), outline=pts)

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline), 1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["HaitsmaHkpDimensions", "HaitsmaHkpSection", "HaitsmaHbmDimensions",
           "HaitsmaHbmSection", "HaitsmaHgrDimensions", "HaitsmaHgrSection"]
