"""Texas DOT (TxDOT) prestressed girders: Tx I-girders, wide-flange Tx
girders, legacy I-beams, U-beams and double-T beams.

Sources (inches; see ``data/txdot_beams.json`` for URLs, SHA-256 and page
locators):

* Tx28-Tx70: TxDOT standard IGD, sheet 1 of 2, (c) August 2017, revised
  March 2023 - typical sections and "Girder Dimensions and Section
  Properties" table. Current standard; all seven reproduce A, Yb, Ix, Iy.
* WF-Tx28-WF-Tx70: TxDOT standard WF-IGD, sheet 2 of 3, (c) August 2024.
  Exterior-girder curb and drip bead excluded, as in the printed properties.
  WF-Tx62's printed Ix is 20,000 in^4 low (misprint, pinned in tests).
* Legacy Type A, B, C, 54 and 72 I-beams, U40/U54 U-beams and the
  T/HT double-T family: PSTRS14 v6.1 user guide (TxDOT, February 2016),
  Appendix A Figures 1, 11 and 8. U-beam standards were retired by TxDOT
  in 2025; the double-T is not on the current index. Undimensioned details
  are handled as recorded per family in the JSON ``geometry_notes``.

Gross concrete only (no strands, deck, end blocks). Millimetres, origin at
the soffit centre, y upward.
"""

from __future__ import annotations

from dataclasses import dataclass

from shapely.geometry import Polygon, box
from shapely.ops import unary_union

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
class TxDotGirderDimensions:
    """Key dimensions (mm) plus the right-half or full outline (mm)."""

    size: str
    depth: float
    top_width: float
    bottom_width: float
    outline: tuple[tuple[float, float], ...]


class _TxDotBase:
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
        self._ring_in = self._ring_in_from(self.row, fam)
        pts = self._ring_in
        ytop = max(y for _, y in pts)
        top = [x for x, y in pts if abs(y - ytop) < 1e-9]
        bot = [x for x, y in pts if y < 1.0]  # includes soffit-chamfer tops
        self.dimensions = TxDotGirderDimensions(
            size=size,
            depth=ytop * INCH_TO_MM,
            top_width=(max(top) - min(top)) * INCH_TO_MM,
            bottom_width=(max(bot) - min(bot)) * INCH_TO_MM,
            outline=tuple(to_mm(pts)),
        )

    def _ring_in_from(self, row: dict, fam: dict):  # pragma: no cover - abstract
        raise NotImplementedError

    @property
    def polygon(self) -> Polygon:
        """Gross concrete outline (mm), anticlockwise."""
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        """``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


def tx_i_right_half_in(row: dict, t: dict) -> list[tuple[float, float]]:
    """Right half (inches) of a Tx / WF-Tx girder from the IGD template."""
    d = row["depth"]
    hb = t["bottom_width"] / 2
    c = t["soffit_chamfer"]
    he = row["bottom_edge"]
    hw = t["web_width"] / 2
    x_knee = hw + t["bottom_fillet"]
    y_knee = he + t["bottom_taper_rise"]
    y_top_edge = d - t["top_edge"]
    y_taper_end = y_top_edge - row["top_taper_rise"]
    return [
        (0.0, 0.0), (hb - c, 0.0), (hb, c), (hb, he),
        (x_knee, y_knee), (hw, y_knee + t["bottom_fillet"]),
        (hw, y_taper_end - t["top_fillet"]), (hw + t["top_fillet_run"], y_taper_end),
        (row["top_width"] / 2, y_top_edge), (row["top_width"] / 2, d), (0.0, d),
    ]


class TxDotIGirderSection(_TxDotBase):
    """TxDOT Tx28-Tx70 prestressed I-girders (IGD, rev. March 2023)."""

    FAMILY = "TX"
    SIZES = ("Tx28", "Tx34", "Tx40", "Tx46", "Tx54", "Tx62", "Tx70")

    def __init__(self, size: str = "Tx54"):
        super().__init__(size)

    def _ring_in_from(self, row, fam):
        return mirror_half(tx_i_right_half_in(row, fam["template_in"]))


class TxDotWideFlangeGirderSection(TxDotIGirderSection):
    """TxDOT WF-Tx28-WF-Tx70 wide-flange I-girders (WF-IGD, August 2024)."""

    FAMILY = "WF"
    SIZES = ("WF-Tx28", "WF-Tx34", "WF-Tx40", "WF-Tx46", "WF-Tx54", "WF-Tx62", "WF-Tx70")

    def __init__(self, size: str = "WF-Tx54"):
        _TxDotBase.__init__(self, size)


class TxDotLegacyIBeamSection(_TxDotBase):
    """Legacy TxDOT Type A, B, C, 54 and 72 I-beams (PSTRS14 Figure 1)."""

    FAMILY = "LEGACY_I"
    SIZES = ("A", "B", "C", "54", "72")

    def __init__(self, size: str = "C"):
        super().__init__(size)

    def _ring_in_from(self, r, fam):
        c = r["soffit_chamfer"]
        y1 = r["C"]
        y2 = y1 + r["E"]
        y3 = y2 + r["F"]
        y4 = y3 + r["G"]
        half = [
            (0.0, 0.0), (r["B"] / 2 - c, 0.0), (r["B"] / 2, c), (r["B"] / 2, y1),
            (r["W"] / 2, y2), (r["W"] / 2, y3), (r["A"] / 2, y4),
            (r["A"] / 2, r["D"]), (0.0, r["D"]),
        ]
        return mirror_half(half)


class TxDotUBeamSection(_TxDotBase):
    """TxDOT U40 and U54 open-top U-beams (PSTRS14 Figure 11; retired 2025)."""

    FAMILY = "U"
    SIZES = ("U40", "U54")

    def __init__(self, size: str = "U54"):
        super().__init__(size)

    def _ring_in_from(self, r, fam):
        t = fam["template_in"]
        hb = t["bottom_width"] / 2
        ts = t["bottom_slab"]
        outer = [
            (hb, 0.0), (hb + r["J"], r["E"]),
            (r["C"] / 2 - t["outer_edge_batter"], r["D"] - t["outer_edge_height"]),
            (r["C"] / 2, r["D"]),
        ]
        inner = [
            (r["F"] / 2, r["D"]), (r["G"], ts + r["H"]),
            (t["inner_chamfer_top_x"], t["inner_chamfer_top_y"]),
            (t["inner_chamfer_bottom_x"], ts),
        ]
        # outer right (up), inner right (down), inner left (up), outer left (down)
        return (outer + inner + [(-x, y) for x, y in reversed(inner)]
                + [(-x, y) for x, y in reversed(outer)])


class TxDotDoubleTSection(_TxDotBase):
    """TxDOT T22-T36 and wide-stem HT22-HT36 double-T beams (PSTRS14 Fig. 8).

    Provenance ``estimate``: stem-flange fillets and flange-edge keys are not
    dimensioned and are omitted (area +4 to +4.5 in^2, I +0.5-0.95%).
    """

    FAMILY = "DT"
    SIZES = (
        "6T22", "7T22", "8T22", "6T28", "7T28", "8T28", "6T36", "7T36", "8T36",
        "6HT22", "7HT22", "8HT22", "6HT28", "7HT28", "8HT28", "6HT36", "7HT36", "8HT36",
    )

    def __init__(self, size: str = "8T28"):
        super().__init__(size)

    def _ring_in_from(self, r, fam):
        a, c, d, tf = r["width"], r["stem_bottom"], r["depth"], r["flange"]
        h = d - tf
        top = c + 2 * h * r["batter"]
        parts = [box(-a / 2, d - tf, a / 2, d)]
        for xc in (-r["stem_spacing"] / 2, r["stem_spacing"] / 2):
            parts.append(Polygon([(xc - c / 2, 0), (xc + c / 2, 0),
                                  (xc + top / 2, d - tf), (xc - top / 2, d - tf)]))
        shell = unary_union(parts).simplify(0)
        return dedupe(list(shell.exterior.coords))


__all__ = [
    "TxDotGirderDimensions",
    "TxDotIGirderSection",
    "TxDotWideFlangeGirderSection",
    "TxDotLegacyIBeamSection",
    "TxDotUBeamSection",
    "TxDotDoubleTSection",
    "tx_i_right_half_in",
]
