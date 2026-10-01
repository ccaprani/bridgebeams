"""PCI Bridge Design Manual (Nov 2011) Appendix B standard products.

AASHTO solid/voided slab beams SI-SIV (36/48 in), AASHTO box beams BI-BIV
(36/48 in), AASHTO-PCI bulb-tees BT-54/63/72, PCI deck bulb-tees (35/53/65 in
deep, 48/72/96 in wide) and the Appendix B-13 double tees. Dimensions are
transcribed in inches from PCI MNL-133-11 Appendix B (PDF pp4-14 of the
public ``2011PCIBridgeManual-Appendix_BC.pdf``) and converted to mm; origin
at mid-soffit, y up. Strands, keys the published properties ignore, end
blocks and decks are excluded. Every convention is listed in
``data/pci_standard_products.json``. The classic AASHTO I-beams I-VI are in
:mod:`bridgebeams.us.aashto_i_beams` and are not duplicated here.
"""

from __future__ import annotations

from dataclasses import dataclass

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.pci_common import (
    circle, load_json, mirror_right_half, to_mm_polygon,
)

_DATA = "pci_standard_products.json"


class _PciBase:
    FAMILY = ""
    SIZES: tuple[str, ...] = ()
    source_status = "PCI Bridge Design Manual 3rd ed. (Nov 2011) reference section"

    def __init__(self, size: str) -> None:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = load_json(_DATA)[self.FAMILY]
        self.size = size
        self.row = dict(zip(fam["columns"], fam["rows"][size]))
        self.published = dict(zip(fam["published_columns"], fam["published"][size]))
        prov = fam["provenance"]
        self.provenance = (prov.get(size, fam.get("provenance_default")) if isinstance(prov, dict) else prov)
        self.dimensions = self._dimensions()

    def _dimensions(self):  # pragma: no cover - overridden
        raise NotImplementedError

    @property
    def polygon(self) -> Polygon:
        return self.dimensions.polygon()

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


# --------------------------------------------------------------- slab beams
@dataclass(frozen=True)
class PciSlabBeamDimensions:
    """Inches. ``void_x`` are void centres; voids sit at mid-depth."""

    width: float
    depth: float
    void_x: tuple[float, ...] = ()
    void_d: tuple[float, ...] = ()

    def polygon(self, circle_points: int = 128) -> Polygon:
        w, h = self.width / 2, self.depth
        ext = [(-w, 0), (w, 0), (w, h), (-w, h)]
        holes = [circle(x, h / 2, d / 2, circle_points)[::-1] for x, d in zip(self.void_x, self.void_d)]
        return to_mm_polygon(ext, holes)


class PciSlabBeamSection(_PciBase):
    """AASHTO/PCI solid (SI) and voided (SII-SIV) slab beams, 36 or 48 in wide."""

    FAMILY = "slab"
    SIZES = ("SI-36", "SII-36", "SIII-36", "SIV-36", "SI-48", "SII-48", "SIII-48", "SIV-48")

    def _dimensions(self) -> PciSlabBeamDimensions:
        r = self.row
        if r["voids"] == 0:
            return PciSlabBeamDimensions(r["L"], r["H"])
        if r["voids"] == 2:
            return PciSlabBeamDimensions(r["L"], r["H"], (-r["L2"], r["L2"]), (r["D1"], r["D1"]))
        return PciSlabBeamDimensions(r["L"], r["H"], (-r["L2"], 0.0, r["L2"]), (r["D1"], r["D2"], r["D1"]))


# ---------------------------------------------------------------- box beams
@dataclass(frozen=True)
class PciBoxBeamDimensions:
    """Inches. Stepped keyway (detail 2) on both sides, chamfered void."""

    width: float
    depth: float
    web: float = 5.0
    top_flange: float = 5.5
    bottom_flange: float = 5.5
    void_chamfer: float = 3.0
    key_upper_inset: float = 0.375
    key_upper_depth: float = 6.0
    key_lower_inset: float = 0.75
    key_lower_depth: float = 6.0

    def polygon(self) -> Polygon:
        w, h = self.width / 2, self.depth
        y1 = h - self.key_upper_depth
        y2 = y1 - self.key_lower_depth
        right = [(w, 0), (w, y2), (w - self.key_lower_inset, y2), (w - self.key_lower_inset, y1),
                 (w - self.key_upper_inset, y1), (w - self.key_upper_inset, h)]
        ext = right + [(-x, y) for x, y in reversed(right)]
        vx, c = w - self.web, self.void_chamfer
        yb, yt = self.bottom_flange, h - self.top_flange
        void = [(-vx + c, yb), (vx - c, yb), (vx, yb + c), (vx, yt - c),
                (vx - c, yt), (-vx + c, yt), (-vx, yt - c), (-vx, yb + c)]
        return to_mm_polygon(ext, [void[::-1]])


class PciBoxBeamSection(_PciBase):
    """AASHTO/PCI adjacent box beams BI-BIV, 36 or 48 in wide."""

    FAMILY = "box"
    SIZES = ("BI-36", "BI-48", "BII-36", "BII-48", "BIII-36", "BIII-48", "BIV-36", "BIV-48")

    def _dimensions(self) -> PciBoxBeamDimensions:
        return PciBoxBeamDimensions(self.row["W"], self.row["H"])


# --------------------------------------------------------------- bulb tees
@dataclass(frozen=True)
class PciBulbTeeDimensions:
    """Inches; AASHTO-PCI bulb-tee (Appendix B-9)."""

    depth: float
    top_width: float = 42.0
    top_edge: float = 3.5
    top_taper_drop: float = 2.0
    top_taper_run: float = 16.0
    fillet: float = 2.0
    web: float = 6.0
    bottom_width: float = 26.0
    bottom_edge: float = 6.0
    bottom_taper_rise: float = 4.5

    def polygon(self) -> Polygon:
        h, tw = self.depth, self.web / 2
        yf = h - self.top_edge - self.top_taper_drop
        right = [(self.bottom_width / 2, 0), (self.bottom_width / 2, self.bottom_edge),
                 (tw, self.bottom_edge + self.bottom_taper_rise), (tw, yf - self.fillet),
                 (tw + self.fillet, yf), (tw + self.fillet + self.top_taper_run, h - self.top_edge),
                 (self.top_width / 2, h)]
        return to_mm_polygon(mirror_right_half(right))


class PciBulbTeeSection(_PciBase):
    """AASHTO-PCI bulb-tee BT-54, BT-63 or BT-72."""

    FAMILY = "bulb_tee"
    SIZES = ("BT-54", "BT-63", "BT-72")

    def _dimensions(self) -> PciBulbTeeDimensions:
        return PciBulbTeeDimensions(self.row["H"])


@dataclass(frozen=True)
class PciDeckBulbTeeDimensions:
    """Inches; PCI deck bulb-tee (Appendix B-11)."""

    depth: float
    width: float
    flange: float = 6.0
    flange_taper: float = 3.0
    fillet: float = 2.0
    web: float = 6.0
    taper_run: float = 19.5
    bottom_width: float = 25.0
    bottom_taper: float = 3.0
    bottom_edge: float = 6.0

    def polygon(self) -> Polygon:
        h, tw, w = self.depth, self.web / 2, self.width / 2
        yu = h - self.flange
        yf = yu - self.flange_taper
        x_end = min(tw + self.fillet + self.taper_run, w)
        right = [(self.bottom_width / 2, 0), (self.bottom_width / 2, self.bottom_edge),
                 (tw, self.bottom_edge + self.bottom_taper), (tw, yf - self.fillet),
                 (tw + self.fillet, yf), (x_end, yu)]
        if x_end < w:
            right.append((w, yu))
        right.append((w, h))
        return to_mm_polygon(mirror_right_half(right))


class PciDeckBulbTeeSection(_PciBase):
    """PCI deck bulb-tee; sizes ``DBT<H>-<W>`` for H 35/53/65 in, W 48/72/96 in."""

    FAMILY = "deck_bulb_tee"
    SIZES = tuple(f"DBT{h}-{w}" for h in (35, 53, 65) for w in (48, 72, 96))

    def _dimensions(self) -> PciDeckBulbTeeDimensions:
        return PciDeckBulbTeeDimensions(self.row["H"], self.row["W"])


# -------------------------------------------------------------- double tees
@dataclass(frozen=True)
class PciDoubleTeeDimensions:
    """Inches. ``stem_bottom`` = A, ``stem_top`` = C, ``stem_spacing`` = E."""

    width: float
    depth: float
    flange: float
    stem_bottom: float
    stem_top: float
    stem_spacing: float

    def polygon(self) -> Polygon:
        h, w, e = self.depth, self.width / 2, self.stem_spacing / 2
        yu = h - self.flange
        right = [(0, yu), (e - self.stem_top / 2, yu), (e - self.stem_bottom / 2, 0),
                 (e + self.stem_bottom / 2, 0), (e + self.stem_top / 2, yu), (w, yu), (w, h)]
        return to_mm_polygon(mirror_right_half(right))


class PciDoubleTeeSection(_PciBase):
    """PCI Appendix B-13 double tee; ``L``/``H`` = light/heavy table, then W(ft)-H(in)."""

    FAMILY = "double_tee"
    SIZES = ("L5-27", "L6-23", "L6-27", "L8-27", "L8-35", "H5-36", "H6-35", "H7-35", "H8-35",
             "H6-27", "H7-27", "H8-27", "H6-21", "H7-21", "H8-21")

    def _dimensions(self) -> PciDoubleTeeDimensions:
        r = self.row
        return PciDoubleTeeDimensions(12 * r["W_ft"], r["H"], r["T"], r["A"], r["C"], r["E"])


__all__ = [
    "PciSlabBeamDimensions", "PciSlabBeamSection",
    "PciBoxBeamDimensions", "PciBoxBeamSection",
    "PciBulbTeeDimensions", "PciBulbTeeSection",
    "PciDeckBulbTeeDimensions", "PciDeckBulbTeeSection",
    "PciDoubleTeeDimensions", "PciDoubleTeeSection",
]
