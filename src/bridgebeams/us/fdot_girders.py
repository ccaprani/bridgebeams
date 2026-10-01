"""Florida DOT FY 2026-27 Standard Plans precast girders.

* Florida-I Beams FIB-36/45/54/63/72/78/84/96 (Index 450-036 ... 450-096);
* Florida-U Beams FUB-48/54/63/72 (Index 450-248 ... 450-272);
* Florida Slab Beams, 12/15/18 in deep, 4'-0" to 5'-0" wide in 1 in steps
  (Index 450-451/452/453; 39 tabulated widths).

Outlines are transcribed in inches from the sheet-1 end views/typical
sections (visually read at 300-400 dpi) and validated against the section
property tables in the matching Standard Plans Instructions (SPI 450-010,
450-210, 450-450), including perimeter and Iyy where printed. Units of the
API are mm, origin at mid-soffit, y up. Strands, end blocks and the FDOT
AASHTO Type II (identical to :class:`bridgebeams.us.AashtoIBeamSection`
``"II"``) are not included. See ``data/fdot_girders.json``.
"""

from __future__ import annotations

from dataclasses import dataclass

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.pci_common import apply_corners, load_json, mirror_right_half, to_mm_polygon

_DATA = "fdot_girders.json"


class _FdotBase:
    FAMILY = ""
    SIZES: tuple[str, ...] = ()
    source_status = "current standard (FDOT FY 2026-27 Standard Plans)"

    def __init__(self, size: str) -> None:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = load_json(_DATA)[self.FAMILY]
        self.size = size
        self.row = dict(zip(fam["columns"], fam["rows"][size]))
        self.published = dict(zip(fam["published_columns"], fam["published"][size]))
        self.provenance = fam["provenance"]
        self.dimensions = self._dimensions()

    def _dimensions(self):  # pragma: no cover - overridden
        raise NotImplementedError

    @property
    def polygon(self) -> Polygon:
        return self.dimensions.polygon()

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class FdotFloridaIBeamDimensions:
    """Inches; Florida-I beam end view (common to all depths)."""

    depth: float
    top_width: float = 48.0
    top_edge: float = 3.5
    top_taper_drop: float = 1.5
    top_taper_run: float = 17.0
    top_chamfer: float = 3.5
    web: float = 7.0
    bottom_width: float = 38.0
    bottom_edge: float = 7.0
    bottom_taper_rise: float = 7.5
    web_fillet: float = 15.0
    soffit_chamfer: float = 0.75

    def polygon(self, arc_segments: int = 32) -> Polygon:
        h, tw = self.depth, self.web / 2
        yc = h - self.top_edge - self.top_taper_drop
        right = [(self.bottom_width / 2, 0.0, ("c", self.soffit_chamfer)),
                 (self.bottom_width / 2, self.bottom_edge),
                 (tw, self.bottom_edge + self.bottom_taper_rise, ("r", self.web_fillet)),
                 (tw, yc - self.top_chamfer), (tw + self.top_chamfer, yc),
                 (tw + self.top_chamfer + self.top_taper_run, h - self.top_edge),
                 (self.top_width / 2, h)]
        return to_mm_polygon(apply_corners(mirror_right_half(right), arc_segments))


class FdotFloridaIBeamSection(_FdotBase):
    """FDOT Florida-I beam FIB-36 ... FIB-96."""

    FAMILY = "fib"
    SIZES = ("FIB-36", "FIB-45", "FIB-54", "FIB-63", "FIB-72", "FIB-78", "FIB-84", "FIB-96")

    def _dimensions(self) -> FdotFloridaIBeamDimensions:
        return FdotFloridaIBeamDimensions(self.row["H"])


@dataclass(frozen=True)
class FdotFloridaUBeamDimensions:
    """Inches; Florida-U beam typical section."""

    depth: float
    bottom_width: float = 56.0
    batter: float = 0.25
    bottom_slab: float = 10.0
    inner_chamfer: float = 3.0
    inner_half_width: float = 25.5625   # half of 4'-3 1/8" at the chamfer top
    upper_inner_rise: float = 21.0
    upper_inner_run: float = 1.9375
    flange_width: float = 16.0
    flange_edge: float = 7.0
    underside_drop: float = 1.0
    edge_draft: float = 0.5
    underside_run: float = 8.5
    top_chamfer: float = 0.75
    soffit_chamfer: float = 1.5

    @property
    def top_width(self) -> float:
        yo = self.depth - self.flange_edge - self.underside_drop
        return 2 * (self.bottom_width / 2 + self.batter * yo + self.underside_run + self.edge_draft)

    def polygon(self, arc_segments: int = 32) -> Polygon:
        h = self.depth
        yo = h - self.flange_edge - self.underside_drop
        xo = self.bottom_width / 2 + self.batter * yo
        w = self.top_width / 2
        xi = w - self.flange_width
        yc = self.bottom_slab + self.inner_chamfer
        right = [(self.bottom_width / 2, 0.0, ("c", self.soffit_chamfer)), (xo, yo),
                 (xo + self.underside_run, h - self.flange_edge, ("c", self.top_chamfer)), (w, h),
                 (xi, h), (xi - self.upper_inner_run, h - self.upper_inner_rise),
                 (self.inner_half_width, yc), (self.inner_half_width - self.inner_chamfer, self.bottom_slab),
                 (0.0, self.bottom_slab)]
        return to_mm_polygon(apply_corners(mirror_right_half(right), arc_segments))


class FdotFloridaUBeamSection(_FdotBase):
    """FDOT Florida-U beam FUB-48, FUB-54, FUB-63 or FUB-72."""

    FAMILY = "fub"
    SIZES = ("FUB-48", "FUB-54", "FUB-63", "FUB-72")

    def _dimensions(self) -> FdotFloridaUBeamDimensions:
        return FdotFloridaUBeamDimensions(self.row["H"])


@dataclass(frozen=True)
class FdotFloridaSlabBeamDimensions:
    """Inches; ``width`` W at the soffit working point."""

    depth: float
    width: float
    flange: float = 4.0
    flange_projection: float = 6.0
    top_chamfer: float = 2.0
    reentrant_chamfer: float = 0.75
    edge_draft: float = 0.5
    edge_top_chamfer: float = 0.5
    edge_bottom_chamfer: float = 0.75

    def polygon(self) -> Polygon:
        w, h, f = self.width / 2, self.depth, self.flange
        xb = w - self.flange_projection
        right = [(w, 0.0, ("c", self.edge_bottom_chamfer)), (w - self.edge_draft, f, ("c", self.edge_top_chamfer)),
                 (xb, f, ("c", self.reentrant_chamfer)), (xb, h, ("c", self.top_chamfer))]
        return to_mm_polygon(apply_corners(mirror_right_half(right)))


class FdotFloridaSlabBeamSection(_FdotBase):
    """FDOT Florida slab beam ``FSB<depth>-<width in>``, e.g. ``FSB12-48`` (4'-0")."""

    FAMILY = "fsb"
    SIZES = tuple(f"FSB{h}-{w}" for h in (12, 15, 18) for w in range(48, 61))

    def _dimensions(self) -> FdotFloridaSlabBeamDimensions:
        return FdotFloridaSlabBeamDimensions(self.row["H"], self.row["W"])


__all__ = [
    "FdotFloridaIBeamDimensions", "FdotFloridaIBeamSection",
    "FdotFloridaUBeamDimensions", "FdotFloridaUBeamSection",
    "FdotFloridaSlabBeamDimensions", "FdotFloridaSlabBeamSection",
]
