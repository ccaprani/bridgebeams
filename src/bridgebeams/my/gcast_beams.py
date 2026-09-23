"""G-CAST (Cast Concrete Sdn Bhd, Malaysia) prestressed beam catalogue.

Source: *Prestressed Concrete Beams*, June 2020 Rev.0, PDF pp 3-5
(U-beams U1-U12; TM beams 1040/1200/1360 x B 1350/1450/1550; I beam
1600 and T beam 1800). Each page has a dimensioned CAD section and a
property table (A, Yt, Yb, Ixx, Zt, Zb). Origin mid-soffit, y up, mm.

* :class:`GcastUBeamSection` (``fitted-reconstruction``): printed 970 base,
  35 chamfer, 7:1 outer batter, top block 325 = 40 + 235 + 50 with 30/15/19
  steps, 407 mm inner thickening, floor levels 150 (centre) / 200 (break) /
  355 (web toe). Not printed: web thickness and floor break half-width.
  Fitted to the nine A/Yb/Ixx rows: horizontal web width 157.4 mm (matches
  the 314 mm² per mm area increment) and break half-width 265 mm.
  Residuals <= 0.13 % A, 0.4 mm Yb, 0.24 % Ixx. For shallower marks the top
  block slides down the outer face (right-hand elevation), as drawn.
  This outline differs from Civilcon's U (za): different batter,
  top strip and areas; no geometry is shared.
* :class:`GcastTmBeamSection` (``estimate``): the drawn top flange carries a
  superelevation crossfall and stepped edges; it is replaced by a uniform
  87 mm flange (fitted to the nine areas). Bottom flange and web are the
  printed M-type details (970 base, 25 chamfer, 160 edge, 50 taper, 80
  splay, 160 web) with the 10 mm edge lean of the OKA M-beam drawing;
  upper splay 105 x 220 printed. Residuals <= 0.17 % A, 1.3 mm Yb, 0.43 % I.
* :class:`GcastIBeamSection` (``transcribed``): fully dimensioned 1600 mm
  I beam (1067 top with 80 x 50 shoulders, 203 web, 711 base).
  Residuals -0.06 % A, -0.2 mm Yb, -0.04 % I.
* :class:`GcastTBeamSection` (``fitted-reconstruction``): 1800 mm T beam,
  1750 top flange with crossfall drawn. Depth chain read as 250 (bottom
  flange including the 20 mm chamfer) + 205 + 1120 + 94 + 131 (flange at
  the root); the symmetric flange tip thickness (65 mm) is fitted to A,
  and then reproduces Yb and Ixx.
"""

from __future__ import annotations

from dataclasses import dataclass

from ._common import _SizedSection


@dataclass(frozen=True)
class GcastUBeamDimensions:
    depth: float
    bottom_width: float = 970.0
    chamfer: float = 35.0
    batter: float = 7.0
    web_horizontal: float = 157.4
    outer_step: float = 19.0
    ledge_level: float = 30.0
    outer_ledge: float = 50.0
    strip: float = 235.0
    inner_ledge: float = 40.0
    inner_step: float = 15.0
    thickening: float = 407.0
    valley_height: float = 150.0
    break_height: float = 200.0
    toe_height: float = 355.0
    break_half_width: float = 265.0

    def outer_x(self, y: float) -> float:
        return self.bottom_width / 2 + y / self.batter

    def inner_x(self, y: float) -> float:
        return self.outer_x(y) - self.web_horizontal

    def right_half(self) -> list[tuple[float, float]]:
        d = self.depth
        b = self.bottom_width / 2
        y_out = d - self.ledge_level - self.outer_step
        xot = self.outer_x(y_out)
        yl = d - self.ledge_level
        x_in_top = xot - self.outer_ledge - self.strip - self.inner_ledge
        y_kink = yl - self.inner_step - self.thickening
        y0 = yl - self.inner_step
        if y_kink <= self.toe_height:
            # U1: the thickening reaches the floor before the web face; the
            # sloping inner face runs straight to the toe level.
            xk = self.inner_x(y_kink)
            x_toe = x_in_top + (xk - x_in_top) * (y0 - self.toe_height) / (y0 - y_kink)
            inner = [(x_toe, self.toe_height)]
        else:
            inner = [(self.inner_x(y_kink), y_kink), (self.inner_x(self.toe_height), self.toe_height)]
        return [
            (b - self.chamfer, 0.0),
            (self.outer_x(self.chamfer), self.chamfer),
            (xot, y_out),
            (xot, yl),
            (xot - self.outer_ledge, yl),
            (xot - self.outer_ledge, d),
            (xot - self.outer_ledge - self.strip, d),
            (xot - self.outer_ledge - self.strip, yl),
            (x_in_top, yl),
            (x_in_top, y0),
            *inner,
            (self.break_half_width, self.break_height),
            (0.0, self.valley_height),
        ]


@dataclass(frozen=True)
class GcastTmBeamDimensions:
    depth: float
    flange_width: float
    flange_thickness: float = 87.0
    bottom_width: float = 970.0
    chamfer: float = 25.0
    flange_edge: float = 160.0
    edge_lean: float = 10.0
    taper_height: float = 50.0
    splay: float = 80.0
    web_width: float = 160.0
    top_splay_height: float = 105.0
    top_splay_width: float = 220.0

    def right_half(self) -> list[tuple[float, float]]:
        b, xw = self.bottom_width / 2, self.web_width / 2
        yt = self.flange_edge + self.taper_height
        yf = self.depth - self.flange_thickness
        return [
            (b - self.chamfer, 0.0),
            (b, self.chamfer),
            (b - self.edge_lean, self.flange_edge),
            (xw + self.splay, yt),
            (xw, yt + self.splay),
            (xw, yf - self.top_splay_height),
            (xw + self.top_splay_width, yf),
            (self.flange_width / 2, yf),
            (self.flange_width / 2, self.depth),
            (0.0, self.depth),
        ]


class GcastUBeamSection(_SizedSection):
    """G-CAST U-beam U1-U12 (800-1600 mm), fitted web and floor."""

    SIZES = ("U1", "U3", "U5", "U7", "U8", "U9", "U10", "U11", "U12")
    _DATA = "gcast_beams.json"

    def __init__(self, size: str = "U8"):
        super().__init__(size)
        self.dimensions = GcastUBeamDimensions(depth=float(self.published["depth"]))

    def right_half(self):
        return self.dimensions.right_half()


class GcastTmBeamSection(_SizedSection):
    """G-CAST TM beam, ``"TM<depth>-<flange width>"`` e.g. ``"TM1200-1450"``."""

    SIZES = tuple(f"TM{d}-{b}" for d in (1040, 1200, 1360) for b in (1350, 1450, 1550))
    _DATA = "gcast_beams.json"

    def __init__(self, size: str = "TM1200-1450"):
        super().__init__(size)
        p = self.published
        self.dimensions = GcastTmBeamDimensions(depth=float(p["depth"]), flange_width=float(p["flange_width"]))

    def right_half(self):
        return self.dimensions.right_half()


class GcastIBeamSection(_SizedSection):
    """G-CAST 1600 mm I beam (fully dimensioned)."""

    SIZES = ("I1600",)
    _DATA = "gcast_beams.json"

    def __init__(self, size: str = "I1600"):
        super().__init__(size)
        self.dimensions = {k: float(v) for k, v in self.published["dimensions_mm"].items()}

    def right_half(self):
        d = self.dimensions
        xb, xw, xt, xs = d["bottom_width"] / 2, d["web_width"] / 2, d["top_width"] / 2, d["strip_width"] / 2
        c = d["chamfer"]
        y1 = c + d["bottom_edge"]
        y2 = y1 + d["bottom_splay"]
        y3 = y2 + d["web"]
        y4 = y3 + d["top_splay_height"]
        y5 = y4 + d["top_taper"]
        y6 = y5 + d["flange_edge"]
        return [
            (xb - c, 0.0), (xb, c), (xb, y1), (xw, y2), (xw, y3),
            (xw + d["top_splay_width"], y4), (xt, y5), (xt, y6), (xs, y6),
            (xs, y6 + d["strip_height"]), (0.0, y6 + d["strip_height"]),
        ]


class GcastTBeamSection(_SizedSection):
    """G-CAST 1800 mm T beam; symmetric flange with fitted tip thickness."""

    SIZES = ("T1800",)
    _DATA = "gcast_beams.json"

    def __init__(self, size: str = "T1800"):
        super().__init__(size)
        self.dimensions = {k: float(v) for k, v in self.published["dimensions_mm"].items()}

    def right_half(self):
        d = self.dimensions
        xb, xw, xt = d["bottom_width"] / 2, d["web_width"] / 2, d["top_width"] / 2
        c = d["chamfer"]
        y1 = d["bottom_flange"]
        y2 = y1 + d["bottom_splay"]
        y3 = y2 + d["web"]
        y4 = y3 + d["top_splay_height"]
        depth = y4 + d["root_thickness"]
        return [
            (xb - c, 0.0), (xb, c), (xb, y1), (xw, y2), (xw, y3),
            (xw + d["top_splay_width"], y4), (xt, depth - d["tip_thickness"]),
            (xt, depth), (0.0, depth),
        ]


__all__ = [
    "GcastUBeamDimensions",
    "GcastTmBeamDimensions",
    "GcastUBeamSection",
    "GcastTmBeamSection",
    "GcastIBeamSection",
    "GcastTBeamSection",
]
