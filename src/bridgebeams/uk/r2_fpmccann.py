"""FP McCann (UK) precast bridge beams, "Precast Bridge Beams" brochure v1.0 (2025).

Families (PDF pages 6-15): TY Type 1 (beam and slab), TY Type 2 (solid
infill), TYE, Y, YE, MY, MYE, SY, W and solid Box (SD1-SD6 in 495/750/970
widths). Every page prints the outline dimensions and a property table; the
outlines here are transcribed from the FP McCann pages (not from the Banagher
/ :mod:`bridgebeams.ie` classes, which are a separate source for the same
nominal range). Conventions, fitted details and pinned source discrepancies
are recorded in ``data/r2_fpmccann.json``.

Millimetres, origin at mid-soffit, y upwards. Edge beams keep the side of
their vertical face as drawn by FP McCann: TYE and MYE face at +x, YE at -x.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon

Point = tuple[float, float]


@lru_cache(maxsize=1)
def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.uk").joinpath("data/r2_fpmccann.json").read_text(encoding="utf-8")
    )


def _fillet(p0: Point, p1: Point, p2: Point, r: float, n: int = 12) -> list[Point]:
    """Tangent arc of radius ``r`` replacing corner ``p1`` of polyline p0-p1-p2."""
    ux, uy = p0[0] - p1[0], p0[1] - p1[1]
    vx, vy = p2[0] - p1[0], p2[1] - p1[1]
    lu, lv = math.hypot(ux, uy), math.hypot(vx, vy)
    ux, uy, vx, vy = ux / lu, uy / lu, vx / lv, vy / lv
    th = math.acos(max(-1.0, min(1.0, ux * vx + uy * vy)))
    t = r / math.tan(th / 2)
    bx, by = ux + vx, uy + vy
    lb = math.hypot(bx, by)
    h = r / math.sin(th / 2)
    cx, cy = p1[0] + bx / lb * h, p1[1] + by / lb * h
    a0 = math.atan2(p1[1] + uy * t - cy, p1[0] + ux * t - cx)
    a1 = math.atan2(p1[1] + vy * t - cy, p1[0] + vx * t - cx)
    d = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return [(cx + r * math.cos(a0 + d * k / n), cy + r * math.sin(a0 + d * k / n)) for k in range(n + 1)]


def _mirror_join(right: list[Point]) -> list[Point]:
    """Symmetric outline from a right half listed soffit -> top."""
    return [(-x, y) for x, y in reversed(right)] + right


class _FpMcCannBase:
    SIZES: tuple[str, ...] = ()
    _FAMILY = ""

    def _setup(self, size: str, family: str | None = None, key: str | None = None) -> dict:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = _load_data()["families"][family or self._FAMILY]
        self.size = size
        self.family = family or self._FAMILY
        self.published = dict(fam["published"][key or size])
        self.provenance = fam["provenance"]
        self.source_status = fam["source_status"]
        return fam

    def _outline(self) -> list[Point]:  # pragma: no cover - overridden
        raise NotImplementedError

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self._outline()), 1.0)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry (millimetres)."""
        return geometry_from_polygon(self.polygon)


# --------------------------------------------------------------------------- TY
_TY_LOWER: list[Point] = [(350.0, 0.0), (375.0, 25.0), (370.0, 135.0), (142.5, 240.0), (92.5, 320.0)]


def _ty_web(y: float) -> float:
    """TY web-line half width: 92.5 at y = 320, 200 at y = 850 (printed 400/530)."""
    return 92.5 + (y - 320.0) * (200.0 - 92.5) / 530.0


@dataclass(frozen=True)
class FpMcCannTyBeamDimensions:
    """``variant`` 'type1' (ledge + printed cap), 'type2' (web line to top) or 'edge' (TYE).

    ``cap`` is the printed cap width (type1) or face-to-cap distance (edge);
    unused for type2.
    """

    depth: float
    variant: str
    cap: float | None = None
    ledge_height: float = 50.0
    face_x: float = 375.0

    @property
    def outline(self) -> list[Point]:
        d = self.depth
        if self.variant == "type2":
            return _mirror_join(_TY_LOWER + [(_ty_web(d), d)])
        if self.variant == "type1":
            c = self.cap / 2
            return _mirror_join(_TY_LOWER + [(_ty_web(d - self.ledge_height), d - self.ledge_height),
                                             (c, d - self.ledge_height), (c, d)])
        # edge: web side on the left (mirrored TY), vertical face at +375
        xc = self.face_x - self.cap
        left = [(-x, y) for x, y in _TY_LOWER]  # soffit -> web
        left += [(-_ty_web(d - self.ledge_height), d - self.ledge_height), (xc, d - self.ledge_height), (xc, d)]
        return [(self.face_x, d), (self.face_x, 25.0), (self.face_x - 25.0, 0.0)] + left


class FpMcCannTyBeamSection(_FpMcCannBase):
    """FP McCann TY beams: Type 1 (beam and slab, TY4-TY10) and Type 2 (solid infill, TY1-TY10)."""

    SIZES = tuple(f"TY{i} (Type 1)" for i in range(4, 11)) + tuple(f"TY{i} (Type 2)" for i in range(1, 11))

    def __init__(self, size: str = "TY7 (Type 1)"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        des, typ = size.split(" (Type ")
        family = "ty_type1" if typ.startswith("1") else "ty_type2"
        fam = self._setup(size, family, des)
        self.designation = des
        cap = fam["transcribed_dims_mm"]["cap_width"][des] if family == "ty_type1" else None
        self.dimensions = FpMcCannTyBeamDimensions(
            depth=self.published["depth_mm"], variant="type1" if cap else "type2", cap=cap)

    def _outline(self):
        return self.dimensions.outline


class FpMcCannTyeBeamSection(_FpMcCannBase):
    """FP McCann TYE edge beams TYE4-TYE10 (vertical face at x = +375)."""

    SIZES = tuple(f"TYE{i}" for i in range(4, 11))
    _FAMILY = "tye"

    def __init__(self, size: str = "TYE7"):
        fam = self._setup(size)
        self.dimensions = FpMcCannTyBeamDimensions(
            depth=self.published["depth_mm"], variant="edge",
            cap=fam["transcribed_dims_mm"]["face_to_cap_edge"][size])

    def _outline(self):
        return self.dimensions.outline


# ---------------------------------------------------------------------------- Y
def _y_web_side(depth: float, cap_half: float, side_y: float, junction_y: float) -> list[Point]:
    """Right side from the flange-side top to the cap top (Y/YE/SY lower geometry)."""
    top = (cap_half + 40.0, depth - 55.0)
    side = (370.0, side_y)
    return ([(350.0, 0.0), (375.0, 25.0), side] + _fillet(side, (100.0, junction_y), top, 100.0)
            + [top, (cap_half + 35.0, depth - 50.0), (cap_half, depth - 50.0), (cap_half, depth)])


@dataclass(frozen=True)
class FpMcCannYBeamDimensions:
    """Y / YE beam. ``cap`` = printed cap width (Y) or rebate-to-cap distance (YE)."""

    depth: float
    cap: float
    edge: bool = False
    flange_side_height: float = 202.0
    junction_y: float = 379.0
    fillet_radius: float = 100.0
    rebate_width: float = 40.0
    rebate_height: float = 50.0

    @property
    def outline(self) -> list[Point]:
        d = self.depth
        if not self.edge:
            return _mirror_join(_y_web_side(d, self.cap / 2, self.flange_side_height, self.junction_y))
        face = -375.0
        xr = face + self.rebate_width
        xc = xr + self.cap
        right = _y_web_side(d, xc, self.flange_side_height, self.junction_y)
        return ([(face + 25.0, 0.0)] + right
                + [(xr, d), (xr, d - self.rebate_height), (face, d - self.rebate_height), (face, 25.0)])


class FpMcCannYBeamSection(_FpMcCannBase):
    """FP McCann Y beams Y1-Y8 (700-1400 deep)."""

    SIZES = tuple(f"Y{i}" for i in range(1, 9))
    _FAMILY = "y"

    def __init__(self, size: str = "Y4"):
        fam = self._setup(size)
        self.dimensions = FpMcCannYBeamDimensions(
            depth=self.published["depth_mm"], cap=fam["transcribed_dims_mm"]["cap_width"][size])

    def _outline(self):
        return self.dimensions.outline


class FpMcCannYeBeamSection(_FpMcCannBase):
    """FP McCann YE edge beams YE1-YE8 (vertical face at x = -375, 40 x 50 rebate)."""

    SIZES = tuple(f"YE{i}" for i in range(1, 9))
    _FAMILY = "ye"

    def __init__(self, size: str = "YE4"):
        fam = self._setup(size)
        self.dimensions = FpMcCannYBeamDimensions(
            depth=self.published["depth_mm"], cap=fam["transcribed_dims_mm"]["rebate_to_cap_edge"][size], edge=True)

    def _outline(self):
        return self.dimensions.outline


# --------------------------------------------------------------------------- MY
@dataclass(frozen=True)
class FpMcCannMyBeamDimensions:
    """MY / MYE beam. ``top_half`` (estimate) and ``bevel_x`` (fitted) per JSON."""

    depth: float
    edge: bool = False
    top_half: float = 220.0
    bevel_x: float = 165.0
    web_base_half: float = 150.0
    flare_top_y: float = 500.0

    def web(self, y: float) -> float:
        y = min(y, self.flare_top_y)
        return self.web_base_half + (self.top_half - self.web_base_half) * (y - 150.0) / (self.flare_top_y - 150.0)

    @property
    def outline(self) -> list[Point]:
        d = self.depth
        right = [(460.0, 0.0), (485.0, 25.0), (485.0, 100.0), (self.bevel_x, 125.0), (self.web_base_half, 150.0)]
        if d > self.flare_top_y:
            right += [(self.top_half, self.flare_top_y), (self.top_half, d)]
        else:
            right += [(self.web(d), d)]
        if not self.edge:
            return _mirror_join(right)
        left = [(-x, y) for x, y in right]  # soffit -> top on the web side
        return [(485.0, d), (485.0, 25.0), (460.0, 0.0)] + left


class FpMcCannMyBeamSection(_FpMcCannBase):
    """FP McCann MY beams MY1-MY7 (300-600 deep, 970 bottom flange)."""

    SIZES = tuple(f"MY{i}" for i in range(1, 8))
    _FAMILY = "my"

    def __init__(self, size: str = "MY4"):
        fam = self._setup(size)
        f = fam["fitted_or_estimated_mm"]
        self.dimensions = FpMcCannMyBeamDimensions(
            depth=self.published["depth_mm"], top_half=f["top_width_at_500"] / 2, bevel_x=150.0 + f["bevel_run"])

    def _outline(self):
        return self.dimensions.outline


class FpMcCannMyeBeamSection(_FpMcCannBase):
    """FP McCann MYE edge beams MYE1-MYE7 (vertical face at x = +485)."""

    SIZES = tuple(f"MYE{i}" for i in range(1, 8))
    _FAMILY = "mye"

    def __init__(self, size: str = "MYE4"):
        fam = self._setup(size)
        f = fam["fitted_or_estimated_mm"]
        self.dimensions = FpMcCannMyBeamDimensions(
            depth=self.published["depth_mm"], edge=True, top_half=f["top_width_at_500_half"],
            bevel_x=150.0 + f["bevel_run"])

    def _outline(self):
        return self.dimensions.outline


# --------------------------------------------------------------------------- SY
@dataclass(frozen=True)
class FpMcCannSyBeamDimensions:
    depth: float
    stem_half: float = 160.0
    stem_y: float = 1450.0
    cap_half: float = 120.0
    ledge_height: float = 50.0

    @property
    def outline(self) -> list[Point]:
        d = self.depth
        side, stem = (370.0, 252.0), (self.stem_half, self.stem_y)
        right = [(350.0, 0.0), (375.0, 25.0), side] + _fillet(side, (100.0, 429.0), stem, 100.0) + [stem]
        if d - self.ledge_height > self.stem_y:
            right.append((self.stem_half, d - self.ledge_height))
        right += [(self.cap_half, d - self.ledge_height), (self.cap_half, d)]
        return _mirror_join(right)


class FpMcCannSyBeamSection(_FpMcCannBase):
    """FP McCann SY beams SY1-SY6 (1500-2000 deep)."""

    SIZES = tuple(f"SY{i}" for i in range(1, 7))
    _FAMILY = "sy"

    def __init__(self, size: str = "SY4"):
        self._setup(size)
        self.dimensions = FpMcCannSyBeamDimensions(depth=self.published["depth_mm"])

    def _outline(self):
        return self.dimensions.outline


# ---------------------------------------------------------------------------- W
_W_TAN = 1.0 / math.tan(math.radians(82.0))


@dataclass(frozen=True)
class FpMcCannWBeamDimensions:
    """Open W trough. L1/L2 from the table, notch 60 wide x 50 high (see JSON)."""

    depth: float
    l1: float
    l2: float
    s: float
    f: float
    notch_width: float = 60.0
    notch_height: float = 50.0
    web_thickness: float = 170.0

    @property
    def l3(self) -> float:
        return self.l1 - 4 * self.notch_width - 2 * self.l2

    @property
    def outline(self) -> list[Point]:
        d, o = self.depth, self.l1 / 2
        yt = d - self.notch_height
        inner = self.l3 / 2
        slope = (o - 755.0) / (yt - 25.0)

        def outer(y: float) -> float:
            return 755.0 + (y - 25.0) * slope

        yk = yt - self.f - self.s
        right = [
            (730.0, 0.0), (755.0, 25.0), (o, yt), (o - self.notch_width, yt), (o - self.notch_width, d),
            (inner + self.notch_width, d), (inner + self.notch_width, yt), (inner, yt), (inner, yt - self.f),
            (outer(yk) - self.web_thickness, yk), (outer(360.0) - self.web_thickness, 360.0),
            (outer(210.0) - 275.0, 210.0), (0.0, 160.0),
        ]
        return [(0.0, 0.0)] + right + [(-x, y) for x, y in reversed(right[:-1])]


class FpMcCannWBeamSection(_FpMcCannBase):
    """FP McCann W beams W1, W3, W5, W7, W8, W9 (open trough, 800-1300 deep)."""

    SIZES = ("W1", "W3", "W5", "W7", "W8", "W9")
    _FAMILY = "w"

    def __init__(self, size: str = "W5"):
        fam = self._setup(size)
        t = fam["transcribed_dims_mm"]["top"][size]
        self.dimensions = FpMcCannWBeamDimensions(
            depth=self.published["depth_mm"], l1=t["L1"], l2=t["L2"], s=t["S"], f=t["F"])

    def _outline(self):
        return self.dimensions.outline


# -------------------------------------------------------------------------- Box
@dataclass(frozen=True)
class FpMcCannBoxBeamDimensions:
    depth: float
    bottom_width: float
    chamfer: float = 25.0
    side_vertical: float = 35.0
    shoulder_rise: float = 30.0
    shoulder_run: float = 65.0

    @property
    def top_width(self) -> float:
        return self.bottom_width - 2 * self.shoulder_run

    @property
    def outline(self) -> list[Point]:
        b, c = self.bottom_width / 2, self.chamfer
        y1 = c + self.side_vertical
        return _mirror_join([(b - c, 0.0), (b, c), (b, y1), (b - self.shoulder_run, y1 + self.shoulder_rise),
                             (b - self.shoulder_run, self.depth)])


class FpMcCannBoxBeamSection(_FpMcCannBase):
    """FP McCann solid Box beams SD1-SD6 (300-800 deep) in 495, 750 and 970 widths."""

    SIZES = tuple(f"SD{i} ({w})" for w in (495, 750, 970) for i in range(1, 7))
    _FAMILY = "box"

    def __init__(self, size: str = "SD4 (750)"):
        self._setup(size)
        self.dimensions = FpMcCannBoxBeamDimensions(
            depth=self.published["depth_mm"], bottom_width=float(size.split("(")[1].rstrip(")")))

    def _outline(self):
        return self.dimensions.outline


__all__ = [
    "FpMcCannTyBeamDimensions", "FpMcCannTyBeamSection", "FpMcCannTyeBeamSection",
    "FpMcCannYBeamDimensions", "FpMcCannYBeamSection", "FpMcCannYeBeamSection",
    "FpMcCannMyBeamDimensions", "FpMcCannMyBeamSection", "FpMcCannMyeBeamSection",
    "FpMcCannSyBeamDimensions", "FpMcCannSyBeamSection",
    "FpMcCannWBeamDimensions", "FpMcCannWBeamSection",
    "FpMcCannBoxBeamDimensions", "FpMcCannBoxBeamSection",
]
