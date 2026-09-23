"""TfNSW Country Bridge Solutions 600 mm precast prestressed double-T deck modules.

Source: Transport for NSW (Roads and Maritime Services) *Country Bridge
Solutions — Modular Bridge Drawings*, 07.10.2016 (published 2022),
sheet "PRECAST MODULE CONCRETE - SHEET C" (Type 1, drawings MB08/10/12DL54,
PDF p28, Sections 1 and 3) and "... SHEET B" (Type 2 PDF p25, Type 3 PDF
p27, Section 1). The 8, 10 and 12 m sets print identical sections.

Profiles (origin at the centre of the 810 mm soffit gap between the two
webs, y up, mm):

- ``T1-internal`` Type A internal module: 1650 body plus two 410 x 75
  flange stubs (overall 2470) for the in-situ closure pours.
- ``T1-external`` Type B external module: 1650 body with a 755 high kerb
  upstand on the outer side and one 410 stub (overall 2060).
- ``T2-external`` Type 2 (single lane, closure pour) module: 325 kerb,
  1675 body and one stub (overall 2410).
- ``T3-external`` Type 3 (single lane, no closure pour) module: kerb plus
  full 180 mm deck flange, overall 2420.

Common printed geometry: depth 600 to deck top; two webs 320 wide at the
soffit, 810 apart, faces battered 17.6:1 (both faces lean outward going
up); top slab 160 over the 760 wide void; 20 x 20 soffit chamfers,
20 x 20 fillets at the void-top corners, 40 x 40 fillets under the
flanges, 15 x 15 chamfers at flange tips. Conventions (stated): chamfer
and fillet legs are taken horizontal/vertical; the kerb's outer corners
use the 15 x 15 "typ" chamfer; the kerb's 5 mm top detail and 10 mm
drainage recess are ignored (kerb face runs straight from the 300 mm top
flat to deck level 25 mm further in). Local bearing recesses, vent holes,
drainage pipes, anchor bolts and the solid 450 mm end blocks are excluded.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.aus")
        .joinpath("data/r2_tfnsw_cbs_modules.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class TfnswCbsModuleDimensions:
    """Dimensions (mm). ``left``/``right`` edge kinds: ``stub``, ``kerb``, ``deck``."""

    left: str
    right: str
    left_overhang: float  # soffit web outer face to left extreme (printed bottom chain)
    right_overhang: float
    depth: float = 600.0
    web_soffit_width: float = 320.0
    web_gap: float = 810.0
    batter: float = 17.6
    top_slab: float = 160.0
    stub_width: float = 410.0
    stub_thickness: float = 75.0
    deck_flange: float = 180.0
    kerb_height: float = 755.0
    kerb_top: float = 300.0
    kerb_bottom: float = 365.0
    kerb_face_run: float = 25.0
    soffit_chamfer: float = 20.0
    void_fillet: float = 20.0
    flange_fillet: float = 40.0
    tip_chamfer: float = 15.0

    # -- derived levels -------------------------------------------------
    @property
    def stub_bottom(self) -> float:
        return self.depth - self.top_slab - self.stub_thickness  # 365

    @property
    def void_top(self) -> float:
        return self.depth - self.top_slab  # 440

    def _flange_bottom(self, kind: str) -> float:
        if kind == "deck":
            return self.depth - self.deck_flange
        return self.kerb_bottom if kind == "kerb" else self.stub_bottom

    def _outer(self, y: float) -> float:
        """|x| of a web outer face at height y."""
        return self.web_gap / 2 + self.web_soffit_width + y / self.batter

    def _inner(self, y: float) -> float:
        return self.web_gap / 2 - y / self.batter

    def _side(self, kind: str, overhang: float) -> list[tuple[float, float]]:
        """Right-hand side profile (x >= 0) from soffit web outer corner up to
        the top corner at the web-body edge, returned bottom to top."""
        c, ff, t = self.soffit_chamfer, self.flange_fillet, self.tip_chamfer
        xs = self.web_gap / 2 + self.web_soffit_width  # 725
        edge = xs + overhang
        yb = self._flange_bottom(kind)
        pts = [(xs - c, 0.0), (self._outer(c), c), (self._outer(yb - ff), yb - ff),
               (self._outer(yb) + ff, yb)]
        if kind == "stub":
            body = edge  # vertical construction-joint face of the body
            tip = body + self.stub_width
            yt = self.void_top
            pts += [(tip - t, yb), (tip, yb + t), (tip, yt - t), (tip - t, yt),
                    (body, yt), (body, self.depth)]
        elif kind == "deck":
            pts += [(edge - t, yb), (edge, yb + t), (edge, self.depth - t),
                    (edge - t, self.depth)]
        elif kind == "kerb":
            k = self.kerb_height
            pts += [(edge - t, yb), (edge, yb + t), (edge, k - t), (edge - t, k),
                    (edge - self.kerb_top, k),
                    (edge - self.kerb_top - self.kerb_face_run, self.depth)]
        else:
            raise ValueError(kind)
        return pts

    def outline(self) -> list[tuple[float, float]]:
        """CCW ring: soffit left to right (through the open void between the
        webs), up the right side, across the top, down the left side."""
        right = self._side(self.right, self.right_overhang)
        left = [(-x, y) for x, y in self._side(self.left, self.left_overhang)]
        c, f = self.soffit_chamfer, self.void_fillet
        xi, yv = self.web_gap / 2, self.void_top
        xv = self._inner(yv) - f
        middle = [(-(xi + c), 0.0), (-self._inner(c), c),
                  (-self._inner(yv - f), yv - f), (-xv, yv),
                  (xv, yv), (self._inner(yv - f), yv - f),
                  (self._inner(c), c), (xi + c, 0.0)]
        return middle + right + list(reversed(left))


class TfnswCbsModuleSection:
    """TfNSW CBS 600 mm double-T deck module gross section.

    Examples
    --------
    >>> from bridgebeams.aus.r2_tfnsw_cbs_modules import TfnswCbsModuleSection
    >>> round(TfnswCbsModuleSection("T1-internal").polygon.bounds[2])
    1235
    """

    SIZES = ("T1-internal", "T1-external", "T2-external", "T3-external")
    source_status = "current TfNSW standard drawings (Country Bridge Solutions, 2016 issue)"

    def __init__(self, size: str = "T1-internal"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load_data()["sections"][size]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.dimensions = TfnswCbsModuleDimensions(**row["dimensions_mm"])

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline()), sign=1)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["TfnswCbsModuleDimensions", "TfnswCbsModuleSection"]
