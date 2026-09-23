"""PCI regional products: NEXT D/F beams, Northeast bulb-tees (NEBT),
Northeast deck bulb tees (NEDBT) and PCI Zone 6 spliced U-girders.

Sources (inches, converted to mm; origin at mid-soffit, y up):

* NEXT D / NEXT F: PCI Bridge Design Manual (Nov 2011) Appendix C-3/C-4.
  Stem geometry, R4 fillets and 3/4 in chamfers are dimensioned; the flange
  edge shear key (D) and edge rounding (F) are not, and are scaled from the
  drawing (``transcribed-with-convention``; not fitted, area within 0.1 %).
* NEBT 39-87: PCI Northeast Appendix C sheet (metric-origin 1000-2200 mm
  girders) - ``transcribed-with-convention``.
* NEDBT 40-80: PCI Northeast sheet NEDBT-03 (2018) -
  ``transcribed-with-convention`` (bulb radius borrowed from NEBT, edge key
  scaled from the drawing).
* Zone 6 U-girders: PCI BDM Appendix C-11 sheet U-7, an illustrative
  concept - ``transcribed-with-convention`` (areas within 0.16 % of the
  weight-implied areas).

Data, conventions and residuals: ``data/pci_regional_products.json``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.pci_common import apply_corners, load_json, mirror_right_half, to_mm_polygon

_DATA = "pci_regional_products.json"


class _RegionalBase:
    FAMILY = ""
    SIZES: tuple[str, ...] = ()
    source_status = "PCI Bridge Design Manual (Nov 2011) Appendix C regional product"

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


# ------------------------------------------------------------------- NEXT
@dataclass(frozen=True)
class PciNextBeamDimensions:
    """Inches. ``kind`` is ``"D"`` (8 in deck flange) or ``"F"`` (4 in form flange).

    ``edge_key_depth`` (D) and ``edge_radius`` (F) are scaled from the drawing.
    """

    kind: str
    width: float
    depth: float
    stem_base: float
    stem_spacing: float = 60.0
    stem_top: float = 15.0
    fillet: float = 4.0
    chamfer: float = 0.75
    edge_key_depth: float = 1.0
    edge_draft: float = 0.25
    edge_radius: float = 2.0

    @property
    def flange(self) -> float:
        return 8.0 if self.kind == "D" else 4.0

    def polygon(self, arc_segments: int = 32) -> Polygon:
        w, b, yu = self.width / 2, self.depth, self.depth - self.flange
        e, st, sb = self.stem_spacing / 2, self.stem_top / 2, self.stem_base / 2
        right = [(0.0, yu), (e - st, yu, ("r", self.fillet)), (e - sb, 0.0, ("c", self.chamfer)),
                 (e + sb, 0.0, ("c", self.chamfer)), (e + st, yu, ("r", self.fillet))]
        if self.kind == "D":
            k = self.edge_key_depth
            right += [(w, yu), (w, yu + 1), (w - k, yu + 2), (w - k, yu + 6), (w, yu + 7), (w, b)]
        else:
            right += [(w - self.edge_draft, yu, ("r", self.edge_radius)), (w, b)]
        return to_mm_polygon(apply_corners(mirror_right_half(right), arc_segments))


class PciNextBeamSection(_RegionalBase):
    """NEXT D (28-40 in) and NEXT F (24-36 in) at the tabulated min/max widths.

    Sizes are ``NEXT<depth><D|F>-<width in>``, e.g. ``NEXT36D-96``.
    """

    FAMILY = "next"
    SIZES = tuple(
        [f"NEXT{b}D-{w}" for b in (40, 36, 32, 28) for w in (96, 120)]
        + [f"NEXT{b}F-{w}" for b in (36, 32, 28, 24) for w in ("95.5", "143.5")]
    )
    # Scaled from the C-3/C-4 drawings (see JSON geometry_notes).
    KEY_DEPTH_D = 1.0
    EDGE_RADIUS_F = 2.0

    def _dimensions(self) -> PciNextBeamDimensions:
        r = self.row
        return PciNextBeamDimensions(r["type"], r["A"], r["B"], r["C"],
                                     edge_key_depth=self.KEY_DEPTH_D, edge_radius=self.EDGE_RADIUS_F)


# ------------------------------------------------------------------- NEBT
@dataclass(frozen=True)
class PciNeBulbTeeDimensions:
    """Inches; Northeast bulb-tee (PCI Northeast)."""

    depth: float
    top_width: float = 47.24
    top_edge: float = 3.35
    top_taper_drop: float = 1.97
    web: float = 7.09
    bottom_width: float = 31.89
    bottom_edge: float = 8.66
    bottom_taper_rise: float = 3.94
    web_fillet: float = 7.87
    bulb_radius: float = 3.94
    soffit_chamfer: float = 0.79
    top_edge_radius: float = 0.79

    def polygon(self, arc_segments: int = 32) -> Polygon:
        h, tw, bw = self.depth, self.web / 2, self.bottom_width / 2
        right = [(bw, 0.0, ("c", self.soffit_chamfer)), (bw, self.bottom_edge, ("r", self.bulb_radius)),
                 (tw, self.bottom_edge + self.bottom_taper_rise, ("r", self.web_fillet)),
                 (tw, h - self.top_edge - self.top_taper_drop, ("r", self.web_fillet)),
                 (self.top_width / 2, h - self.top_edge, ("r", self.top_edge_radius)),
                 (self.top_width / 2, h)]
        return to_mm_polygon(apply_corners(mirror_right_half(right), arc_segments))


class PciNeBulbTeeSection(_RegionalBase):
    """Northeast bulb-tee NEBT39-NEBT87 (1000-2200 mm deep)."""

    FAMILY = "nebt"
    SIZES = ("NEBT39", "NEBT47", "NEBT55", "NEBT63", "NEBT71", "NEBT79", "NEBT83", "NEBT87")
    source_status = "PCI Northeast regional standard (PCI BDM Appendix C sheet)"

    def _dimensions(self) -> PciNeBulbTeeDimensions:
        return PciNeBulbTeeDimensions(self.row["H"])


# ------------------------------------------------------------------ NEDBT
@dataclass(frozen=True)
class PciNeDeckBulbTeeDimensions:
    """Inches; Northeast deck bulb tee at its 8 in minimum flange."""

    depth: float
    width: float = 60.0
    flange: float = 8.0
    flange_taper_drop: float = 2.25
    web: float = 7.0625
    bottom_width: float = 31.875
    bottom_edge: float = 8.6875
    bottom_taper_rise: float = 3.9375
    web_fillet: float = 7.875
    bulb_radius: float = 3.9375  # convention: NEBT value
    soffit_chamfer: float = 0.75
    edge_key_depth: float = 0.9  # convention: scaled from drawing

    def polygon(self, arc_segments: int = 32) -> Polygon:
        h, tw, bw, w = self.depth, self.web / 2, self.bottom_width / 2, self.width / 2
        yu = h - self.flange
        right = [(bw, 0.0, ("c", self.soffit_chamfer)), (bw, self.bottom_edge, ("r", self.bulb_radius)),
                 (tw, self.bottom_edge + self.bottom_taper_rise, ("r", self.web_fillet)),
                 (tw, yu - self.flange_taper_drop, ("r", self.web_fillet)),
                 (w, yu), (w - self.edge_key_depth, yu + self.flange / 2), (w, h)]
        return to_mm_polygon(apply_corners(mirror_right_half(right), arc_segments))


class PciNeDeckBulbTeeSection(_RegionalBase):
    """Northeast deck bulb tee NEDBT40-NEDBT80 (60 in wide)."""

    FAMILY = "nedbt"
    SIZES = ("NEDBT40", "NEDBT48", "NEDBT56", "NEDBT64", "NEDBT72", "NEDBT80")
    source_status = "PCI Northeast regional standard details (issue 2018-03-06)"

    def _dimensions(self) -> PciNeDeckBulbTeeDimensions:
        return PciNeDeckBulbTeeDimensions(self.row["H"])


# -------------------------------------------------------- Zone 6 U-girders
@dataclass(frozen=True)
class PciZone6UGirderDimensions:
    """Inches; PCI Zone 6 spliced U-girder typical (non-haunched) section."""

    depth: float
    web: float
    width: float
    top_opening: float
    bottom_width: float
    batter: float = 0.25
    bottom_slab: float = 9.0
    flange_edge: float = 9.25
    edge_draft: float = 2.25
    upper_inner_slope: float = 2.0 / 21.0
    inner_chamfer: float = 3.0
    soffit_chamfer: float = 1.5

    def polygon(self) -> Polygon:
        d, k = self.depth, self.batter
        w, t, bw = self.width / 2, self.top_opening / 2, self.bottom_width / 2
        yu = d - self.flange_edge
        off = self.web * math.hypot(1.0, k)          # horizontal web thickness
        x_in0 = bw - off                              # inner face at y = 0
        # upper inner face: x = t - s (d - y); web inner face: x = x_in0 + k y
        s = self.upper_inner_slope
        yk = (t - s * d - x_in0) / (k - s)
        ys = self.bottom_slab
        yc = ys + self.inner_chamfer
        right = [(bw, 0.0, ("c", self.soffit_chamfer)), (bw + k * yu, yu), (w - self.edge_draft, yu),
                 (w, d), (t, d), (x_in0 + k * yk, yk), (x_in0 + k * yc, yc),
                 (x_in0 + k * yc - self.inner_chamfer, ys), (0.0, ys)]
        return to_mm_polygon(apply_corners(mirror_right_half(right)))


class PciZone6UGirderSection(_RegionalBase):
    """PCI Zone 6 (SE region) spliced U-girders U72/U84/U96 with 3 in or 4 in ducts."""

    FAMILY = "zone6_u"
    SIZES = ("U72-3", "U84-3", "U96-3", "U72-4", "U84-4", "U96-4")
    source_status = "PCI BDM 2011 Appendix C illustrative concept (not a standard)"

    def _dimensions(self) -> PciZone6UGirderDimensions:
        r = self.row
        return PciZone6UGirderDimensions(r["D"], r["tw"], r["W"], r["T"], r["bf"])


__all__ = [
    "PciNextBeamDimensions", "PciNextBeamSection",
    "PciNeBulbTeeDimensions", "PciNeBulbTeeSection",
    "PciNeDeckBulbTeeDimensions", "PciNeDeckBulbTeeSection",
    "PciZone6UGirderDimensions", "PciZone6UGirderSection",
]
