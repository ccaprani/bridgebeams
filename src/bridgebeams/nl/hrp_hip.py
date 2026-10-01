"""Haitsma Beton HRP rail girders and HIP I-girders (brugliggers).

Source: Haitsma Beton "HRP- en HIP-brugliggers" folder, PDF pages 2 (HRP)
and 3 (HIP natte knoop and HIP druklaag). See ``data/haitsma_hrp_hip.json``.

The main outlines are dimensioned. Side shear-key recesses, edge rebates,
chamfers and the HRP plank rebate at the top of the stem are drawn but
**not dimensioned**; they are scaled from the vector drawing (HIP) or
fitted to the published Ab/V/I (HRP recess depth). Provenance is therefore
``fitted-reconstruction`` for every size.

The two HIP variants have different precast outlines and are separate
SIZES entries: ``HIP<H>-natte-knoop`` (wet joint / transverse
post-tensioning) and ``HIP<H>-druklaag`` (with 200 mm in-situ topping).
The PDF tables cover H = 1200-2000 mm; the Haitsma web page describes
1600-2400 mm (edition conflict, recorded in the JSON).

Millimetres, origin at mid-soffit, y upwards.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile


@lru_cache(maxsize=None)
def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.nl").joinpath("data/haitsma_hrp_hip.json").read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class HaitsmaHrpDimensions:
    """HRP dimensions (mm). Printed: 220/215/300/215/220 and 66/84/20/130."""

    depth: float
    half_width: float = 585.0
    stem_width: float = 300.0
    knee_x: float = 365.0
    edge_level: float = 150.0
    knee_level: float = 170.0
    stem_root_level: float = 300.0
    key_bottom: float = 66.0
    # ESTIMATES (undimensioned on the drawing)
    bottom_chamfer: float = 20.0
    key_depth: float = 30.0  # fitted to published Ab/V/I (drawing scales ~20)
    key_top: float = 135.0
    top_chamfer: float = 15.0
    plank_rebate_width: float = 35.0
    plank_rebate_depth: float = 15.0

    def flange_top_y(self, x: float) -> float:
        return self.edge_level + (self.knee_level - self.edge_level) * (self.half_width - x) / (
            self.half_width - self.knee_x
        )

    @property
    def outline(self) -> list[tuple[float, float]]:
        w, k = self.half_width, self.key_depth
        xs = self.stem_width / 2
        xt = w - k - self.top_chamfer
        return [
            (w - self.bottom_chamfer, 0.0),
            (w, self.bottom_chamfer),
            (w, self.key_bottom),
            (w - k, self.key_bottom + k),
            (w - k, self.key_top),
            (xt, self.flange_top_y(xt)),
            (self.knee_x, self.knee_level),
            (xs, self.stem_root_level),
            (xs, self.depth - self.plank_rebate_depth),
            (xs - self.plank_rebate_width, self.depth - self.plank_rebate_depth),
            (xs - self.plank_rebate_width, self.depth),
        ]


@dataclass(frozen=True)
class HaitsmaHipDimensions:
    """HIP dimensions (mm); ``variant`` is 'natte-knoop' or 'druklaag'."""

    depth: float
    variant: str
    bottom_half_width: float = 740.0
    web_width: float = 250.0
    bottom_edge: float = 162.0  # 59 + 103
    bottom_knee: tuple[float, float] = (250.0, 283.0)  # 125+125, 162+121
    web_root: float = 383.0  # + 100
    # natte knoop top: 300 + 880 + 300, chain 300 / 69 / 22
    nk_block_half_width: float = 440.0
    nk_block_depth: float = 300.0
    nk_wing_edge: float = 69.0
    nk_wing_slope: float = 22.0
    # druklaag top: 1440 overall, chain 90 / 185
    dl_half_width: float = 720.0
    dl_edge: float = 90.0
    dl_haunch: float = 185.0
    # ESTIMATES scaled from the drawing (undimensioned)
    rebate_level: float = 59.0
    rebate_depth: float = 25.0
    rebate_rise: float = 15.0
    side_draft: float = 5.0
    dl_haunch_break: tuple[float, float] = (625.0, 100.0)  # (x, depth below top)
    dl_ledge_width: float = 25.0
    dl_ledge_depth: float = 57.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        w, H = self.bottom_half_width, self.depth
        xw = self.web_width / 2
        pts = [
            (w, 0.0),
            (w, self.rebate_level),
            (w - self.rebate_depth, self.rebate_level + self.rebate_rise),
            (w - self.rebate_depth + self.side_draft, self.bottom_edge),
            self.bottom_knee,
            (xw, self.web_root),
        ]
        if self.variant == "natte-knoop":
            y_edge = H - self.nk_block_depth - self.nk_wing_edge
            wing = self.nk_block_half_width + 300.0
            pts += [
                (xw, y_edge - self.nk_wing_slope),
                (wing, y_edge),
                (wing, H - self.nk_block_depth),
                (self.nk_block_half_width, H - self.nk_block_depth),
                (self.nk_block_half_width, H),
            ]
        elif self.variant == "druklaag":
            bx, bd = self.dl_haunch_break
            x_top = self.dl_half_width - self.dl_ledge_width
            pts += [
                (xw, H - self.dl_edge - self.dl_haunch),
                (bx, H - bd),
                (self.dl_half_width, H - self.dl_edge),
                (self.dl_half_width, H - self.dl_ledge_depth),
                (x_top, H - self.dl_ledge_depth),
                (x_top, H),
            ]
        else:
            raise ValueError(f"unknown HIP variant {self.variant!r}")
        return pts


class HaitsmaHrpSection:
    """Haitsma HRP500-HRP1600 inverted-T rail girder (railligger)."""

    SIZES = tuple(f"HRP{h}" for h in range(500, 1601, 100))
    provenance = "fitted-reconstruction"
    source_status = "producer catalogue (Haitsma Beton HRP/HIP folder, PDF 2018)"

    def __init__(self, size: str = "HRP1000"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = next(r for r in _load_data()["hrp"]["published_properties"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = HaitsmaHrpDimensions(float(row["H"]))

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


class HaitsmaHipSection:
    """Haitsma HIP I-girder, natte knoop and druklaag variants, H 1200-2000."""

    VARIANTS = ("natte-knoop", "druklaag")
    SIZES = tuple(f"HIP{h}-{v}" for v in VARIANTS for h in range(1200, 2001, 100))
    provenance = "fitted-reconstruction"
    source_status = "producer catalogue (Haitsma Beton HRP/HIP folder, PDF 2018; web page lists 1600-2400)"

    def __init__(self, size: str = "HIP1600-druklaag"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        depth_part, variant = size[3:].split("-", 1)
        rows = _load_data()["hip"][variant.replace("-", "_")]["published_properties"]
        row = next(r for r in rows if r["H"] == int(depth_part))
        self.size = size
        self.variant = variant
        self.published = row
        self.dimensions = HaitsmaHipDimensions(float(row["H"]), variant)

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "HaitsmaHipDimensions",
    "HaitsmaHipSection",
    "HaitsmaHrpDimensions",
    "HaitsmaHrpSection",
]
