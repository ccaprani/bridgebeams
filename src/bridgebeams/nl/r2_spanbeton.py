"""Spanbeton (Consolis Spanbeton, now VBI) precast bridge beams.

Sources: Spanbeton "projectbladen" (archived from spanbeton.nl; bridge-beam
production ended 2020), see ``data/r2_spanbeton.json`` for local files,
SHA-256, pages and every convention:

* ``SpanbetonSkkSection`` - SKK 700-1900 box girders (kokerbalk), p3.
* ``SpanbetonPiqSection`` - PIQ 1200-1450 wide box girders (b = 2790), p4.
* ``SpanbetonSjpSection`` - SJP 300-700 inverted-T slab beams (990 module).
* ``SpanbetonSjpFlexSection`` - SJP-flex 300-800 (1180 module).
* ``SpanbetonSrpSection`` - SRP 550-900 L-shaped edge beam.
* ``SpanbetonZipSection`` - ZIP 500-900 rail beams (inverted T).
* ``SpanbetonZipxlSection`` - ZIPXL 1000-2400 rail beams (I / bulb-T).

All outlines are dimensioned on the sheets; undimensioned details (void
haunches, edge keys, chamfers, the ZIPXL 1800-2400 flange curve) were
measured from the vector drawings, hence ``transcribed-with-convention``.
Millimetres, origin at mid-soffit, y upwards. Box voids are polygon
interiors. Intermittent transverse openings are excluded from the gross
section (the published SJP/SJP-flex properties smear them; see tests).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon

SOURCE_STATUS = "producer project sheets (archived, production ended 2020)"


@lru_cache(maxsize=None)
def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.nl").joinpath("data/r2_spanbeton.json").read_text(encoding="utf-8")
    )


def _mirror(right: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Right half (soffit to top) -> closed full ring (right then mirrored left)."""
    return list(right) + [(-x, y) for x, y in reversed(right)]


class _SpanbetonBase:
    _key = ""
    SIZES: tuple[str, ...] = ()
    source_status = SOURCE_STATUS

    def __init__(self, size: str):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        block = _load_data()[self._key]
        self.size = size
        self.published = block["sizes"][size]
        self.provenance = self.published.get("provenance", block["provenance"])
        self.residuals = self.published.get("residuals")

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


# --------------------------------------------------------------------------- SKK
@dataclass(frozen=True)
class SpanbetonSkkDimensions:
    """SKK box girder (mm). Printed: depth, width, slabs, web, rebate; rest measured."""

    depth: float
    width: float
    top_slab: float
    bottom_slab: float
    ledge_half_width: float
    web: float = 155.0
    rebate_depth: float = 30.0
    rebate_level: float = 315.0  # below top, outer corner
    rebate_fall: float = 5.0
    soffit_chamfer: float = 15.0
    top_haunch: tuple[float, float] = (75.0, 200.0)
    bottom_chamfer: tuple[float, float] = (75.0, 75.0)
    ledge_depth: float = 20.0


class SpanbetonSkkSection(_SpanbetonBase):
    """Spanbeton SKK 700-1900 box girder (b = 1480 up to 1600, 1180 above)."""

    _key = "skk"
    SIZES = tuple(f"SKK-{h}" for h in range(700, 1901, 100))

    def __init__(self, size: str = "SKK-1200"):
        super().__init__(size)
        h = float(self.published["ht_mm"])
        narrow = h > 1600
        self.dimensions = SpanbetonSkkDimensions(
            depth=h,
            width=1180.0 if narrow else 1480.0,
            top_slab=225.0 if narrow else 170.0,
            bottom_slab=175.0 if narrow else 140.0,
            ledge_half_width=355.0 if narrow else 415.0,
        )

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        b, h, c = d.width / 2, d.depth, d.soffit_chamfer
        right = [(b - c, 0.0), (b, c), (b, h - d.rebate_level),
                 (b - d.rebate_depth, h - d.rebate_level + d.rebate_fall), (b - d.rebate_depth, h)]
        vi = b - d.web
        yt = h - d.top_slab
        hx, hy = d.top_haunch
        bx, by = d.bottom_chamfer
        void = [(vi - bx, d.bottom_slab), (vi, d.bottom_slab + by), (vi, yt - d.ledge_depth - hy),
                (vi - hx, yt - d.ledge_depth), (d.ledge_half_width, yt - d.ledge_depth),
                (d.ledge_half_width, yt)]
        return orient(Polygon(_mirror(right), [_mirror(void)]), sign=1.0)


# --------------------------------------------------------------------------- PIQ
@dataclass(frozen=True)
class SpanbetonPiqDimensions:
    """PIQ wide box girder (mm), bottom flange b = 2790 (the tabulated width)."""

    depth: float
    bottom_width: float = 2790.0
    top_width: float = 1820.0
    shoulder_width: float = 1900.0
    rebate_level: float = 350.0  # below top, inner corner
    rebate_fall: float = 6.0
    shoulder_height: float = 150.0
    shoulder_chamfer: float = 38.0
    web_outer_bottom: float = 878.0  # half-width at the flange fillet (1750/2 printed)
    web_root_level: float = 237.0
    flange_root: tuple[float, float] = (900.0, 176.0)
    flange_tip: float = 114.0
    soffit_edge_chamfer: float = 35.0
    web_at_soffit: float = 183.0
    top_slab: float = 175.0
    bottom_slab: float = 140.0
    web_inner_top: float = 736.0
    top_haunch: tuple[float, float] = (76.0, 200.0)
    bottom_chamfer: tuple[float, float] = (85.0, 75.0)
    ledge_depth: float = 20.0
    ledge_half_width: float = 612.0


class SpanbetonPiqSection(_SpanbetonBase):
    """Spanbeton PIQ 1200-1450 wide box girder (bottom flange 2790)."""

    _key = "piq"
    SIZES = tuple(f"PIQ-{h}" for h in range(1200, 1451, 50))

    def __init__(self, size: str = "PIQ-1300"):
        super().__init__(size)
        self.dimensions = SpanbetonPiqDimensions(depth=float(self.published["ht_mm"]))

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        h, b, c = d.depth, d.bottom_width / 2, d.soffit_edge_chamfer
        sw, tw = d.shoulder_width / 2, d.top_width / 2
        shoulder_bottom = h - d.rebate_level - d.rebate_fall - d.shoulder_height
        right = [(b - c, 0.0), (b, c), (b, d.flange_tip), d.flange_root,
                 (d.web_outer_bottom, d.web_root_level),
                 (sw - d.shoulder_chamfer, shoulder_bottom - d.shoulder_chamfer),
                 (sw, shoulder_bottom), (sw, h - d.rebate_level - d.rebate_fall),
                 (tw, h - d.rebate_level), (tw, h)]
        vi = d.web_outer_bottom - d.web_at_soffit + 0.0  # inner face at the bottom chamfer
        yt = h - d.top_slab
        hx, hy = d.top_haunch
        bx, by = d.bottom_chamfer
        void = [(vi - bx, d.bottom_slab), (vi, d.bottom_slab + by),
                (d.web_inner_top, yt - d.ledge_depth - hy),
                (d.web_inner_top - hx, yt - d.ledge_depth),
                (d.ledge_half_width, yt - d.ledge_depth), (d.ledge_half_width, yt)]
        return orient(Polygon(_mirror(right), [_mirror(void)]), sign=1.0)


# --------------------------------------------------------------------------- SJP
@dataclass(frozen=True)
class SpanbetonSjpDimensions:
    """SJP inverted-T slab beam (mm). ``top_width`` is table column b."""

    h1: float
    h2: float
    top_width: float
    width: float = 990.0
    edge: float = 85.0
    root_level: float = 105.0
    root_width: float = 260.0


class SpanbetonSjpSection(_SpanbetonBase):
    """Spanbeton SJP 300-700 volstortligger (990 mm module)."""

    _key = "sjp"
    SIZES = tuple(f"SJP-{h}" for h in range(300, 701, 50))

    def __init__(self, size: str = "SJP-500"):
        super().__init__(size)
        r = self.published
        self.dimensions = SpanbetonSjpDimensions(float(r["h1_mm"]), float(r["h2_mm"]), float(r["b_mm"]))

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        w, t = d.width / 2, d.top_width / 2
        right = [(w, 0.0), (w, d.edge), (d.root_width / 2, d.root_level), (t, d.h1 - d.h2)]
        if d.h2 > 0:
            right.append((t, d.h1))
        return orient(Polygon(_mirror(right)), sign=1.0)


# ---------------------------------------------------------------------- SJP-flex
@dataclass(frozen=True)
class SpanbetonSjpFlexDimensions:
    """SJP-flex inverted-T slab beam (mm). ``top_width`` is table column b."""

    h1: float
    h2: float
    top_width: float
    width: float = 1180.0
    edge: float = 110.0
    stem_width: float = 350.0
    stem_vertical_top: float = 286.0
    flange_step: tuple[float, float, float] = (447.0, 420.0, 20.0)  # x from, x to, rise
    flange_root: tuple[float, float] = (190.0, 140.0)
    root_chamfer: float = 15.0
    soffit_corner: tuple[float, float] = (20.0, 20.0)


class SpanbetonSjpFlexSection(_SpanbetonBase):
    """Spanbeton SJP-flex 300-800 volstortligger (1180 mm module)."""

    _key = "sjp_flex"
    SIZES = tuple(f"SJP-flex-{h}" for h in range(300, 801, 50))

    def __init__(self, size: str = "SJP-flex-500"):
        super().__init__(size)
        r = self.published
        self.dimensions = SpanbetonSjpFlexDimensions(float(r["h1_mm"]), float(r["h2_mm"]), float(r["b_mm"]))

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        w, s, t = d.width / 2, d.stem_width / 2, d.top_width / 2
        x0, x1, rise = d.flange_step
        rx, ry = d.flange_root
        cx, cy = d.soffit_corner
        right = [(w - cx, 0.0), (w, cy), (w, d.edge), (x0, d.edge), (x1, d.edge + rise), (rx, ry),
                 (s, ry + d.root_chamfer), (s, d.stem_vertical_top), (t, d.h1 - d.h2)]
        if d.h2 > 0:
            right.append((t, d.h1))
        return orient(Polygon(_mirror(right)), sign=1.0)


# --------------------------------------------------------------------------- SRP
@dataclass(frozen=True)
class SpanbetonSrpDimensions:
    """SRP L-shaped edge beam (mm), outer (cantilever) face on the left."""

    h1: float
    width: float = 490.0
    soffit_width: float = 300.0
    cantilever: float = 225.0
    slope_height: float = 250.0
    lip: float = 100.0
    top_flat: float = 275.0
    top_slope: float = 50.0
    step: float = 190.0

    @property
    def h2(self) -> float:
        return self.h1 - self.step

    @property
    def h3(self) -> float:
        return self.h1 - self.cantilever - self.slope_height


class SpanbetonSrpSection(_SpanbetonBase):
    """Spanbeton SRP 550-900 edge beam (randbalk) for SJP decks."""

    _key = "srp"
    SIZES = tuple(f"SRP-{h}" for h in range(550, 901, 50))

    def __init__(self, size: str = "SRP-700"):
        super().__init__(size)
        self.dimensions = SpanbetonSrpDimensions(float(self.published["h1_mm"]))

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        x_in = d.width - d.soffit_width  # 190: inner edge of the soffit from the outer face
        x0 = x_in + d.soffit_width / 2
        pts = [(x_in, 0.0), (d.width, 0.0), (d.width, d.h2), (d.top_flat + d.top_slope, d.h2),
               (d.top_flat, d.h1), (0.0, d.h1), (0.0, d.h1 - d.cantilever),
               (d.lip, d.h1 - d.cantilever), (x_in, d.h3)]
        return orient(Polygon([(x - x0, y) for x, y in pts]), sign=1.0)


# --------------------------------------------------------------------- ZIP/ZIPXL
_EDGE_KEY = ((24.0, 0.0), (7.0, 19.0), (0.0, 60.0), (32.0, 92.0), (15.0, 140.0))


def _bezier(p0, p1, p2, p3, n):
    out = []
    for k in range(1, n):
        t = k / n
        a, b, c, e = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + e * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + e * p3[1]))
    return out


@dataclass(frozen=True)
class SpanbetonZipDimensions:
    """ZIP / ZIPXL rail beam (mm). ``h`` and ``h1`` as tabulated (see JSON notes)."""

    series: str  # "ZIP", "ZIPXL-1" (1000-1700) or "ZIPXL-2" (1800-2400)
    h: float
    h1: float
    width: float
    stem: float
    flange_rise: tuple[float, float]  # (x from centre, y) of the flange-top knee
    haunch_top: float
    head_chamfer: float = 120.0
    edge_key: tuple[tuple[float, float], ...] = _EDGE_KEY

    @property
    def total_depth(self) -> float:
        return self.h if self.series == "ZIPXL-2" else self.h + 35.0


class _ZipBase(_SpanbetonBase):
    _key = "zip"
    bezier_segments = 12

    def _dims(self, series: str) -> SpanbetonZipDimensions:
        r = self.published
        h, h1 = float(r["h_mm"]), float(r["h1_mm"])
        if series == "ZIP":
            return SpanbetonZipDimensions(series, h, h1, 1180.0, 300.0, (375.0, 175.0), 275.0)
        return SpanbetonZipDimensions(series, h, h1, 1480.0, 250.0, (365.0, 208.0), 395.0,
                                      head_chamfer=105.0 if h == 990 else 120.0)

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        w, s, h = d.width / 2, d.stem / 2, d.h
        right = [(w - dx, y) for dx, y in d.edge_key] + [d.flange_rise, (s, d.haunch_top)]
        if d.series == "ZIP":
            right += [(s, h), (115.0, h), (115.0, h + 35.0)]
        elif d.series == "ZIPXL-1":
            right += [(s, h - d.h1 - d.head_chamfer), (250.0, h - d.h1), (250.0, h), (215.0, h),
                      (215.0, h + 35.0)]
        else:
            p3, p0 = (s, h - 275.0), (720.0, h - 85.0)
            right += [p3] + _bezier(p3, p3, (500.0, h - 90.0), p0, self.bezier_segments)
            right += [p0, (720.0, h - 45.0), (685.0, h - 45.0), (685.0, h)]
        return orient(Polygon(_mirror(right)), sign=1.0)


class SpanbetonZipSection(_ZipBase):
    """Spanbeton ZIP 500-900 rail beam (1180 bottom flange)."""

    SIZES = tuple(f"ZIP-{h}" for h in range(500, 901, 100))

    def __init__(self, size: str = "ZIP-700"):
        super().__init__(size)
        self.dimensions = self._dims("ZIP")


class SpanbetonZipxlSection(_ZipBase):
    """Spanbeton ZIPXL 1000-1700 (bulb head) and 1800-2400 (wide top flange) rail beams."""

    SIZES = tuple(f"ZIPXL-{h}" for h in range(1000, 2401, 100))

    def __init__(self, size: str = "ZIPXL-1500"):
        super().__init__(size)
        self.dimensions = self._dims("ZIPXL-2" if int(size.split("-")[1]) >= 1800 else "ZIPXL-1")


__all__ = [
    "SpanbetonPiqDimensions",
    "SpanbetonPiqSection",
    "SpanbetonSjpDimensions",
    "SpanbetonSjpFlexDimensions",
    "SpanbetonSjpFlexSection",
    "SpanbetonSjpSection",
    "SpanbetonSkkDimensions",
    "SpanbetonSkkSection",
    "SpanbetonSrpDimensions",
    "SpanbetonSrpSection",
    "SpanbetonZipDimensions",
    "SpanbetonZipSection",
    "SpanbetonZipxlSection",
]
