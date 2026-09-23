"""Haitsma Beton HKO and HKO-XL inverted-T slab girders (volstortliggers).

Source: Haitsma Beton "HKO HKO-XL" folder, PDF page 2 (see
``data/haitsma_hko.json`` for URL, SHA-256 and every convention).

* ``HaitsmaHkoSection`` (HKO300-HKO700): outline transcribed from the
  dimensioned HKO drawing; the undimensioned stem-root fillet is an
  r = 15 mm estimate. The printed inertia column omits its multiplier;
  the geometry shows it is x10^9 mm^4.
* ``HaitsmaHkoXlSection`` (HKO-XL300-800): only the 1180 mm width chain
  and depth range are printed. The outline is scaled from the drawing and
  two offsets are fitted to the published A/Z/I: an **estimate**.

Millimetres, origin at mid-soffit, y upwards. Intermittent transverse
holes are excluded from the gross section.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources

from shapely.geometry import Polygon, box
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile

from ._arc import fillet


@lru_cache(maxsize=None)
def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.nl").joinpath("data/haitsma_hko.json").read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class HaitsmaHkoDimensions:
    """HKO dimensions in mm. ``top_width`` is table column B."""

    depth: float
    top_width: float
    width: float = 990.0
    stem_root_width: float = 270.0
    root_level: float = 105.0
    edge_height: float = 75.0
    chamfer_level: float = 88.0
    chamfer_flat: float = 30.0
    chamfer_width: float = 30.0
    side_draft: float = 5.0
    soffit_radius: float = 15.0
    root_radius: float = 15.0  # ESTIMATE: undimensioned in source

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Right half from the soffit corner region to the top corner."""
        w = self.width / 2
        edge_top = (w, self.edge_height)
        soffit_corner = (w - self.side_draft, 0.0)
        c1 = (w - self.chamfer_flat, self.edge_height)
        c2 = (w - self.chamfer_flat - self.chamfer_width, self.chamfer_level)
        root = (self.stem_root_width / 2, self.root_level)
        top = (self.top_width / 2, self.depth)
        pts = fillet(soffit_corner, (0.0, 0.0), edge_top, self.soffit_radius, 8)
        pts += [edge_top, c1, c2]
        pts += fillet(root, c2, top, self.root_radius, 12)
        pts.append(top)
        return pts


class HaitsmaHkoSection:
    """Haitsma HKO300-HKO700 gross precast section."""

    SIZES = tuple(f"HKO{h}" for h in range(300, 701, 50))
    provenance = "transcribed-with-convention"
    source_status = "producer catalogue (Haitsma Beton HKO folder, PDF 2021)"

    def __init__(self, size: str = "HKO500"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()["hko"]
        row = next(r for r in data["published_properties"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = HaitsmaHkoDimensions(float(row["H"]), float(row["B"]))

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class HaitsmaHkoXlDimensions:
    """HKO-XL estimated outline (mm): the H=800 profile truncated at ``depth``."""

    depth: float
    soffit_half_width: float = 585.0
    soffit_radius: float = 10.0
    edge_top: tuple[float, float] = (590.0, 82.0)
    lip_x: float = 583.0
    lip_top: float = 99.0
    flange_top: tuple[tuple[float, float], ...] = ((505.0, 99.0), (490.0, 118.0), (200.0, 131.0), (175.0, 137.0))
    stem_half_width: float = 175.0
    splay_start_y: float = 303.0
    splay_end: tuple[float, float] = (308.0, 602.0)
    top_step: tuple[float, float] = (300.0, 620.0)
    full_depth: float = 800.0

    @property
    def full_outline(self) -> list[tuple[float, float]]:
        """Right half of the H = 800 outline."""
        pts = fillet((self.soffit_half_width, 0.0), (0.0, 0.0), self.edge_top, self.soffit_radius, 8)
        pts += [self.edge_top, (self.lip_x, self.edge_top[1]), (self.lip_x, self.lip_top)]
        pts += list(self.flange_top)
        pts += [(self.stem_half_width, self.splay_start_y), self.splay_end, self.top_step,
                (self.top_step[0], self.full_depth)]
        return pts


class HaitsmaHkoXlSection:
    """Haitsma HKO-XL300-800 (ESTIMATE: scaled and fitted outline)."""

    SIZES = tuple(f"HKO-XL{h}" for h in range(300, 801, 50))
    provenance = "estimate"
    source_status = "producer catalogue (Haitsma Beton HKO folder, PDF 2021); outline undimensioned"

    def __init__(self, size: str = "HKO-XL500"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()["hko_xl"]
        row = next(r for r in data["published_properties"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = HaitsmaHkoXlDimensions(float(row["H"]))

    @property
    def polygon(self) -> Polygon:
        full = polygon_from_half_profile(self.dimensions.full_outline)
        cut = full.intersection(box(-1e4, -1.0, 1e4, self.dimensions.depth))
        return orient(Polygon(cut.exterior.coords), 1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "HaitsmaHkoDimensions",
    "HaitsmaHkoSection",
    "HaitsmaHkoXlDimensions",
    "HaitsmaHkoXlSection",
]
