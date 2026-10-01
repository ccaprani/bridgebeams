"""Ferrobeton (Hungary) precast prestressed bridge beams: FP, FPT, ITG, FI-150.

Producer catalogue sheets (ferrobeton.hu), each one A4 page of vector CAD.
Source units are centimetres; superscript digits are decimals (3⁵ = 3.5).
Sections here are millimetres, origin at mid-soffit, y upwards, gross
concrete only (projecting stirrups excluded).

Undimensioned arcs/chamfers were measured from the vector CAD paths (the
sheets are drawn to exact scale); see ``data/ferrobeton.json`` for every
convention, estimate and per-size provenance. Only FPT has a published
property check (Súly kg/m at an assumed 2500 kg/m³).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile

from ._fillet import fillet_polyline

_CM = 10.0


def _family(name: str) -> dict:
    data = json.loads(
        resources.files("bridgebeams.hu")
        .joinpath("data/ferrobeton.json")
        .read_text(encoding="utf-8")
    )
    return data["families"][name]


class _Base:
    SIZES: tuple[str, ...] = ()
    source_status = "producer catalogue"

    def _check(self, size: str) -> None:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.outline)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


# --------------------------------------------------------------------- FP
@dataclass(frozen=True)
class FerrobetonFpDimensions:
    """FP plank, millimetres. ``body_height`` is the 43 cm upper body."""

    depth: float
    body_height: float
    overall_width: float = 500.0
    soffit_width: float = 470.0
    chamfer: float = 15.0
    edge_height: float = 45.0
    ledge_rise: float = 5.0
    body_width: float = 430.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        y_edge = self.chamfer + self.edge_height
        return [
            (self.soffit_width / 2, 0.0),
            (self.overall_width / 2, self.chamfer),
            (self.overall_width / 2, y_edge),
            (self.body_width / 2, y_edge + self.ledge_rise),
            (self.body_width / 2, self.depth),
        ]


class FerrobetonFpSection(_Base):
    """Ferrobeton FP-20A / FP-30A / FP-37A feszített hídgerenda (slab plank)."""

    SIZES = ("FP-20A", "FP-30A", "FP-37A")

    def __init__(self, size: str = "FP-30A"):
        self._check(size)
        fam = _family("FP")
        row = fam["sections"][size]
        c = fam["common_dimensions_cm"]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.dimensions = FerrobetonFpDimensions(
            depth=row["dimensions_cm"]["depth"] * _CM,
            body_height=row["dimensions_cm"]["body_height"] * _CM,
            overall_width=c["overall_width"] * _CM,
            soffit_width=c["soffit_width"] * _CM,
            chamfer=c["chamfer"] * _CM,
            edge_height=c["edge_height"] * _CM,
            ledge_rise=c["ledge_rise"] * _CM,
            body_width=c["body_width"] * _CM,
        )
        d = self.dimensions
        if abs(d.chamfer + d.edge_height + d.ledge_rise + d.body_height - d.depth) > 1e-6:
            raise ValueError(f"{size}: vertical chain does not close")


# -------------------------------------------------------------------- FPT
@dataclass(frozen=True)
class FerrobetonFptDimensions:
    """FPT T girder template, millimetres; flange levels measured down
    from the top. Undimensioned radii/chamfers are CAD-measured."""

    depth: float
    overall_width: float = 700.0
    top_face_width: float = 580.0
    web_width: float = 300.0
    ledge_root_half_width: float = 300.0
    ledge_root_below_top: float = 40.0
    ledge_tip_below_top: float = 45.0
    flange_edge_bottom_below_top: float = 150.0
    flange_root_below_top: float = 185.0
    bottom_chamfer: float = 20.0
    r_ledge_root: float = 10.0
    r_ledge_tip: float = 10.0
    r_flange_corner: float = 25.0
    r_web_fillet: float = 25.0
    arc_segments: int = 16

    @property
    def outline(self) -> list[tuple[float, float]]:
        h = self.depth
        xw, xo = self.web_width / 2, self.overall_width / 2
        verts = [
            (xw - self.bottom_chamfer, 0.0, 0.0),
            (xw, self.bottom_chamfer, 0.0),
            (xw, h - self.flange_root_below_top, self.r_web_fillet),
            (xo, h - self.flange_edge_bottom_below_top, self.r_flange_corner),
            (xo, h - self.ledge_tip_below_top, self.r_ledge_tip),
            (self.ledge_root_half_width, h - self.ledge_root_below_top, self.r_ledge_root),
            (self.top_face_width / 2, h, 0.0),
        ]
        return fillet_polyline(verts, self.arc_segments)


@dataclass(frozen=True)
class FerrobetonFpt7050Dimensions:
    """FPT-70/50 edge-girder outline, millimetres (sharp, fully dimensioned)."""

    depth: float = 700.0
    top_width: float = 500.0
    flange_edge_height: float = 167.5
    splay_height: float = 17.5
    web_width: float = 300.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        y = self.depth - self.flange_edge_height - self.splay_height
        return [
            (self.web_width / 2, 0.0),
            (self.web_width / 2, y),
            (self.top_width / 2, y + self.splay_height),
            (self.top_width / 2, self.depth),
        ]


class FerrobetonFptSection(_Base):
    """Ferrobeton FPT jelű feszített hídgerenda (T girder) family.

    FPT-70…130 share the drawn FPT-70 template with a variable web
    ('változó'); FPT-45 uses the same template as an estimate and its
    tabulated mass disagrees (+8.2%, pinned). FPT-70/50 is a separate
    50 cm-top outline for replacing EHGE 70 edge girders.
    """

    SIZES = ("FPT-45", "FPT-70", "FPT-70/50", "FPT-80", "FPT-90", "FPT-100", "FPT-130")

    def __init__(self, size: str = "FPT-90"):
        self._check(size)
        fam = _family("FPT")
        row = fam["sections"][size]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.mass_per_length = float(row["mass_kg_m"])
        if size == "FPT-70/50":
            d = row["dimensions_cm"]
            self.dimensions = FerrobetonFpt7050Dimensions(
                depth=row["depth_cm"] * _CM,
                top_width=d["top_width"] * _CM,
                flange_edge_height=d["flange_edge_height"] * _CM,
                splay_height=d["splay_height"] * _CM,
                web_width=d["web_width"] * _CM,
            )
        else:
            t = fam["template_cm"]
            self.dimensions = FerrobetonFptDimensions(
                depth=row["depth_cm"] * _CM,
                overall_width=t["overall_width"] * _CM,
                top_face_width=t["top_face_width"] * _CM,
                web_width=t["web_width"] * _CM,
                ledge_root_half_width=t["ledge_root_half_width"] * _CM,
                ledge_root_below_top=t["ledge_root_below_top"] * _CM,
                ledge_tip_below_top=t["ledge_tip_below_top"] * _CM,
                flange_edge_bottom_below_top=t["flange_edge_bottom_below_top"] * _CM,
                flange_root_below_top=t["flange_root_below_top"] * _CM,
                bottom_chamfer=t["bottom_chamfer"] * _CM,
                r_ledge_root=t["r_ledge_root"] * _CM,
                r_ledge_tip=t["r_ledge_tip"] * _CM,
                r_flange_corner=t["r_flange_corner"] * _CM,
                r_web_fillet=t["r_web_fillet"] * _CM,
            )


# -------------------------------------------------------------------- ITG
@dataclass(frozen=True)
class FerrobetonItgDimensions:
    """ITG midspan (Tartóközép) I girder, millimetres."""

    depth: float
    web_segment: float
    top_face_width: float = 466.0
    top_slope_offset: float = 10.0
    ledge_width: float = 57.0
    side_batter: float = 6.0
    web_width: float = 160.0
    bottom_width: float = 350.0
    bottom_batter: float = 7.0
    ledge_depth: float = 45.0
    side_height: float = 98.0
    underside_fall: float = 28.0
    top_haunch_height: float = 111.0
    bottom_splay_height: float = 86.0
    bottom_flange_height: float = 180.0

    @property
    def overall_width(self) -> float:
        return self.top_face_width + 2 * (self.top_slope_offset + self.ledge_width + self.side_batter)

    @property
    def outline(self) -> list[tuple[float, float]]:
        xb = self.bottom_width / 2
        xbw = xb + self.bottom_batter
        xw = self.web_width / 2
        x_ledge_in = self.top_face_width / 2 + self.top_slope_offset
        x_ledge_out = x_ledge_in + self.ledge_width
        xo = x_ledge_out + self.side_batter
        y1 = self.bottom_flange_height
        y2 = y1 + self.bottom_splay_height
        y3 = y2 + self.web_segment
        y4 = y3 + self.top_haunch_height
        y5 = y4 + self.underside_fall
        y6 = y5 + self.side_height
        return [
            (xb, 0.0), (xbw, y1), (xw, y2), (xw, y3), (xbw, y4), (xo, y5),
            (x_ledge_out, y6), (x_ledge_in, y6), (self.top_face_width / 2, self.depth),
        ]


class FerrobetonItgSection(_Base):
    """Ferrobeton ITG jelű feszített hídgerenda, midspan section.

    ITG-90 is fully dimensioned; ITG-70/110 are estimates that vary only
    the 35.2 cm web segment. ITG-45 is not implemented (template cannot
    fit 45 cm).
    """

    SIZES = ("ITG-70", "ITG-90", "ITG-110")

    def __init__(self, size: str = "ITG-90"):
        self._check(size)
        fam = _family("ITG")
        row = fam["sections"][size]
        t = fam["template_cm"]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.dimensions = FerrobetonItgDimensions(
            depth=row["depth_cm"] * _CM,
            web_segment=row["web_segment_cm"] * _CM,
            top_face_width=t["top_face_width"] * _CM,
            top_slope_offset=t["top_slope_offset"] * _CM,
            ledge_width=t["ledge_width"] * _CM,
            side_batter=t["side_batter"] * _CM,
            web_width=t["web_width"] * _CM,
            bottom_width=t["bottom_width"] * _CM,
            bottom_batter=t["bottom_batter"] * _CM,
            ledge_depth=t["ledge_depth"] * _CM,
            side_height=t["side_height"] * _CM,
            underside_fall=t["underside_fall"] * _CM,
            top_haunch_height=t["top_haunch_height"] * _CM,
            bottom_splay_height=t["bottom_splay_height"] * _CM,
            bottom_flange_height=t["bottom_flange_height"] * _CM,
        )
        d = self.dimensions
        chain = (d.ledge_depth + d.side_height + d.underside_fall + d.top_haunch_height
                 + d.web_segment + d.bottom_splay_height + d.bottom_flange_height)
        if abs(chain - d.depth) > 1e-6:
            raise ValueError(f"{size}: vertical chain {chain} != depth {d.depth}")


# ------------------------------------------------------------------ FI-150
@dataclass(frozen=True)
class FerrobetonFi150Dimensions:
    """FI-150 I girder, millimetres; radii are CAD-measured estimates."""

    depth: float = 1500.0
    top_face_width: float = 710.0
    top_width: float = 800.0
    web_width: float = 146.0
    bottom_width: float = 600.0
    soffit_width: float = 570.0
    chamfer_height: float = 40.0
    bulb_edge_height: float = 120.0
    bulb_splay_height: float = 230.0
    web_height: float = 930.0
    flange_haunch_height: float = 80.0
    flange_edge_height: float = 75.0
    ledge_fall: float = 5.0
    top_slope_height: float = 20.0
    top_slope_offset: float = 5.0
    r_ledge_root: float = 10.0
    r_ledge_tip: float = 10.0
    r_flange_tip: float = 25.0
    r_top_web: float = 75.0
    r_bottom_web: float = 150.0
    r_bulb_corner: float = 25.0
    arc_segments: int = 16

    @property
    def outline(self) -> list[tuple[float, float]]:
        y1 = self.chamfer_height
        y2 = y1 + self.bulb_edge_height
        y3 = y2 + self.bulb_splay_height
        y4 = y3 + self.web_height
        y5 = y4 + self.flange_haunch_height
        y6 = y5 + self.flange_edge_height
        y7 = y6 + self.ledge_fall
        xr = self.top_face_width / 2 + self.top_slope_offset
        verts = [
            (self.soffit_width / 2, 0.0, 0.0),
            (self.bottom_width / 2, y1, 0.0),
            (self.bottom_width / 2, y2, self.r_bulb_corner),
            (self.web_width / 2, y3, self.r_bottom_web),
            (self.web_width / 2, y4, self.r_top_web),
            (self.top_width / 2, y5, self.r_flange_tip),
            (self.top_width / 2, y6, self.r_ledge_tip),
            (xr, y7, self.r_ledge_root),
            (self.top_face_width / 2, self.depth, 0.0),
        ]
        return fillet_polyline(verts, self.arc_segments)


class FerrobetonFi150Section(_Base):
    """Ferrobeton FI-150 jelű feszített hídgerenda (150 cm I girder)."""

    SIZES = ("FI-150",)

    def __init__(self, size: str = "FI-150"):
        self._check(size)
        fam = _family("FI-150")
        d = fam["dimensions_cm"]
        r = fam["radii_cm"]
        self.size = size
        self.published = fam
        self.provenance = fam["provenance"]
        # ledge_width (printed 4) is implied by top/top-face widths and the 0.5 offset
        if abs(d["top_width"] / 2 - d["top_face_width"] / 2 - d["top_slope_offset"] - d["ledge_width"]) > 1e-9:
            raise ValueError("FI-150: top width chain does not close")
        self.dimensions = FerrobetonFi150Dimensions(
            **{k: v * _CM for k, v in d.items() if k != "ledge_width"},
            r_ledge_root=r["ledge_root"] * _CM,
            r_ledge_tip=r["ledge_tip"] * _CM,
            r_flange_tip=r["flange_tip"] * _CM,
            r_top_web=r["top_web_fillet"] * _CM,
            r_bottom_web=r["bottom_web_fillet"] * _CM,
            r_bulb_corner=r["bulb_corner"] * _CM,
        )
        dd = self.dimensions
        chain = (dd.chamfer_height + dd.bulb_edge_height + dd.bulb_splay_height + dd.web_height
                 + dd.flange_haunch_height + dd.flange_edge_height + dd.ledge_fall + dd.top_slope_height)
        if abs(chain - dd.depth) > 1e-6:
            raise ValueError(f"FI-150: vertical chain {chain} != depth {dd.depth}")


__all__ = [
    "FerrobetonFpDimensions", "FerrobetonFpSection",
    "FerrobetonFptDimensions", "FerrobetonFpt7050Dimensions", "FerrobetonFptSection",
    "FerrobetonItgDimensions", "FerrobetonItgSection",
    "FerrobetonFi150Dimensions", "FerrobetonFi150Section",
]
