"""Texas DOT (TxDOT) adjacent box beams, X-beams, slab beams and decked slab beams.

Sources (inches; URLs, SHA-256 and page locators in ``data/txdot_beams.json``):

* 4B20-5B40 box beams: TxDOT standards BB-B20/B28/B34/B40, sheet 1 of 3,
  (c) December 2006, revised January 2012. Typical sections plus "Beam
  Properties". B40 has an "over 100 feet" variant with 5x5 in void
  chamfers (note 8), encoded as ``"4B40-C"``/``"5B40-C"``. All 10 profiles
  reproduce the printed A, Ytop, Ybott and I exactly.
* 4XB20-5XB40 X-beams (spread box beams): XB-XB20..XB40, sheet 2 of 3,
  (c) August 2022. The 3/4 in soffit chamfer is adopted from the BB sheets
  (drawn, not called out); with it all eight match exactly.
* 4SB12-5SB15 slab beams: PSB-4SB12 etc., (c) January 2017. Solid
  rectangles; the printed properties exclude the 3/4 in exposed-corner
  chamfers, so the rectangle is returned.
* 6DS20-8DS23 decked slab beams: PSTRS14 v6.1 (TxDOT, Feb 2016) Figure 16.
  Void and deck-edge slope are undimensioned and are a least-squares
  reconstruction to the printed A/Yb/I (provenance ``fitted-reconstruction``).
  TxDOT retired the decked slab beam standards in January 2025.

Gross concrete only; voids are polygon interiors. Millimetres, origin at
the soffit centre, y upward. Transverse tendon/drain holes, shear-key grout,
end blocks and optional chamfer strips are excluded.
"""

from __future__ import annotations

from dataclasses import dataclass

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import (
    INCH_TO_MM,
    ccw_polygon,
    dedupe,
    load_json,
    mirror_half,
    to_mm,
)

DATA = "txdot_beams.json"


def _family(key: str) -> dict:
    return load_json(DATA)["families"][key]


@dataclass(frozen=True)
class TxDotSlabBoxDimensions:
    """Overall dimensions (mm) plus outline and void rings (mm)."""

    size: str
    depth: float
    width: float
    outline: tuple[tuple[float, float], ...]
    voids: tuple[tuple[tuple[float, float], ...], ...] = ()


def box_right_half_in(r: dict) -> list[tuple[float, float]]:
    """Right half (inches) of the TxDOT box / X-beam exterior outline."""
    hb = r["bottom_width"] / 2
    c = r["soffit_chamfer"]
    he, rec, d, tv = r["edge_height"], r["recess"], r["depth"], r["top_edge_height"]
    ht = hb - 2.0
    hr = hb - rec
    return [
        (0.0, 0.0), (hb - c, 0.0), (hb, c), (hb, he), (hr, he + rec),
        (hr, d - tv - (rec - 2.0)), (ht, d - tv), (ht, d), (0.0, d),
    ]


def box_void_in(r: dict) -> list[tuple[float, float]]:
    """Void ring (inches), clockwise, optional bottom corner chamfers."""
    vh = r["void_width"] / 2
    vb = r["void_bottom"]
    vt = r["depth"] - r["top_slab"]
    ch = r.get("void_chamfer", 0.0)
    ring = [(-vh, vb + ch), (-vh, vt), (vh, vt), (vh, vb + ch), (vh - ch, vb), (-vh + ch, vb)]
    return dedupe(ring)


class _SlabBoxBase:
    FAMILY = ""
    SIZES: tuple[str, ...] = ()

    def __init__(self, size: str):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = _family(self.FAMILY)
        self.size = size
        self.row = fam["sections"][size]
        self.provenance = self.row["provenance"]
        self.source_status = self.row["source_status"]
        self.published = self.row.get("published")
        self._shell_in, self._voids_in = self._rings_in(self.row, fam)
        xs = [p[0] for p in self._shell_in]
        ys = [p[1] for p in self._shell_in]
        self.dimensions = TxDotSlabBoxDimensions(
            size=size,
            depth=max(ys) * INCH_TO_MM,
            width=(max(xs) - min(xs)) * INCH_TO_MM,
            outline=tuple(to_mm(self._shell_in)),
            voids=tuple(tuple(to_mm(v)) for v in self._voids_in),
        )

    def _rings_in(self, row: dict, fam: dict):  # pragma: no cover - abstract
        raise NotImplementedError

    @property
    def polygon(self) -> Polygon:
        """Gross concrete section (mm): CCW shell, CW void interiors."""
        return ccw_polygon(to_mm(self._shell_in), [to_mm(v) for v in self._voids_in])

    @property
    def geometry(self):
        """``sectionproperties`` Geometry in millimetres (voids as holes)."""
        return geometry_from_polygon(self.polygon)


class TxDotBoxBeamSection(_SlabBoxBase):
    """TxDOT 4B/5B 20-40 in adjacent box beams (BB standards, rev. 2012)."""

    FAMILY = "BOX"
    SIZES = ("4B20", "5B20", "4B28", "5B28", "4B34", "5B34",
             "4B40", "4B40-C", "5B40", "5B40-C")

    def __init__(self, size: str = "4B28"):
        super().__init__(size)

    def _rings_in(self, r, fam):
        return mirror_half(box_right_half_in(r)), [box_void_in(r)]


class TxDotXBeamSection(TxDotBoxBeamSection):
    """TxDOT 4XB/5XB 20-40 in spread box (X) beams (XB standards, Aug 2022)."""

    FAMILY = "XB"
    SIZES = ("4XB20", "5XB20", "4XB28", "5XB28", "4XB34", "5XB34", "4XB40", "5XB40")

    def __init__(self, size: str = "4XB34"):
        _SlabBoxBase.__init__(self, size)


class TxDotSlabBeamSection(_SlabBoxBase):
    """TxDOT 4SB12, 4SB15, 5SB12, 5SB15 solid slab beams (PSB, Jan 2017)."""

    FAMILY = "SLAB"
    SIZES = ("4SB12", "4SB15", "5SB12", "5SB15")

    def __init__(self, size: str = "4SB15"):
        super().__init__(size)

    def _rings_in(self, r, fam):
        hw, d = r["width"] / 2, r["depth"]
        return [(-hw, 0.0), (hw, 0.0), (hw, d), (-hw, d)], []


class TxDotDeckedSlabBeamSection(_SlabBoxBase):
    """TxDOT 6/7/8 DS20 and DS23 decked slab beams (fitted reconstruction)."""

    FAMILY = "DS"
    SIZES = ("6DS20", "7DS20", "8DS20", "6DS23", "7DS23", "8DS23")

    def __init__(self, size: str = "7DS23"):
        super().__init__(size)

    def _rings_in(self, r, fam):
        fit = fam["fit"][self.size[-2:]]
        hs = r["stem_width"] / 2
        c = r["stem_height"]
        d = c + r["deck"]
        a = r["width"] / 2
        half = [(0.0, 0.0), (hs, 0.0), (hs, c), (a - fit["edge_undercut"], c), (a, d), (0.0, d)]
        vw, vh, vb = fit["void_width"] / 2, fit["void_height"], fit["void_bottom"]
        void = [(-vw, vb), (-vw, vb + vh), (vw, vb + vh), (vw, vb)]
        return mirror_half(half), [void]


__all__ = [
    "TxDotSlabBoxDimensions",
    "TxDotBoxBeamSection",
    "TxDotXBeamSection",
    "TxDotSlabBeamSection",
    "TxDotDeckedSlabBeamSection",
    "box_right_half_in",
    "box_void_in",
]
