"""VÁHOSTAV-SK-PREFA VPH-PTMN precast prestressed bridge beams (Slovakia).

Sources: *PREDPÄTÉ NOSNÍKY VPH-PTMN* (Slovak original, "Katalóg mostných
nosníkov") and its English edition *PRESTRESSED BEAMS VPH PTMN*, PDF pages
6, 8, 10 (2016-PM slab units K/M), 12 (2016-T), 14 (2010 I 1.2 m),
16 (2016-I), 18/19 (2010 I 1.4 m), 21 (2010-R2 1.9 m) and 23 (2010-R2
2.1 m). Printed page numbers equal PDF page numbers. Dimensions are mm.

Every outline is a gross midspan section: prestressing, ducts, optional
PE-pipe lightening voids ("možné vyľahčenie"), transverse holes (DET. A)
and end blocks are excluded. The top roughening ("zdrsnenie povrchu") is
treated as a flat surface. All R=50 junctions are true circular arcs tangent
to both straight faces; the printed tangent extents (26/44 on the lower
splay, 42/49 on the upper) are reproduced by that construction.

Known source issues (see ``data/vph_ptmn.json``): the 1.9 m flange chain
33+49+36+49 = 167 is labelled 168 and the depth only closes with 168, so
the flange edge is taken as 34; the 2.1 m drawing is internally consistent
but its published centroid/inertia are not (pinned in tests); the p18/p19
shared image prints 100 for the 200 web and 249 for 247.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon

ARC_SEGMENTS = 32


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.sk")
        .joinpath("data/vph_ptmn.json")
        .read_text(encoding="utf-8")
    )


def _rounded(corners: list[tuple[float, float]], radii: dict[int, float],
             segments: int = ARC_SEGMENTS) -> list[tuple[float, float]]:
    """Replace ``corners[i]`` by a tangent circular arc of radius ``radii[i]``."""
    out: list[tuple[float, float]] = []
    n = len(corners)
    for i, p in enumerate(corners):
        r = radii.get(i, 0.0)
        if not r:
            out.append(p)
            continue
        a, b = corners[i - 1], corners[(i + 1) % n]
        u = (a[0] - p[0], a[1] - p[1])
        v = (b[0] - p[0], b[1] - p[1])
        lu, lv = math.hypot(*u), math.hypot(*v)
        u, v = (u[0] / lu, u[1] / lu), (v[0] / lv, v[1] / lv)
        angle = math.acos(max(-1.0, min(1.0, u[0] * v[0] + u[1] * v[1])))
        t = r / math.tan(angle / 2)
        bis = (u[0] + v[0], u[1] + v[1])
        lb = math.hypot(*bis)
        d = r / math.sin(angle / 2)
        c = (p[0] + bis[0] / lb * d, p[1] + bis[1] / lb * d)
        s = math.atan2(p[1] + u[1] * t - c[1], p[0] + u[0] * t - c[0])
        e = math.atan2(p[1] + v[1] * t - c[1], p[0] + v[0] * t - c[0])
        sweep = (e - s + math.pi) % (2 * math.pi) - math.pi
        out.extend((c[0] + r * math.cos(s + sweep * k / segments),
                    c[1] + r * math.sin(s + sweep * k / segments))
                   for k in range(segments + 1))
    return out


def _tangent_length(radius: float, slope_angle: float) -> float:
    """Tangent length of a fillet between a vertical face and a line at
    ``slope_angle`` (radians) to the horizontal: interior angle 90° + θ."""
    return radius / math.tan((math.pi / 2 + slope_angle) / 2)


def _splay_sharp_heights(edge_tangent: float, rise: float, run: float,
                         radius: float) -> tuple[float, float]:
    """Lower splay: fillet tangent points on both vertical faces are printed
    (``edge_tangent`` and ``edge_tangent + rise``); return the theoretical
    sharp-corner heights at the flange edge and at the web face."""
    t = 0.0
    for _ in range(200):
        theta = math.atan((rise - 2 * t) / run)
        t = _tangent_length(radius, theta)
    return edge_tangent + t, edge_tangent + rise - t


@dataclass(frozen=True)
class VphSlabBeamDimensions:
    """VPH-PTMN 2016-PM slab-bridge units (millimetres).

    ``unit`` is ``"M"`` (intermediate, symmetric inverted T) or ``"K"``
    (outer/edge unit, rectangular block on the left and one splayed ledge
    on the right). ``edge_height`` (55) is the vertical outer face up to the
    lower fillet tangent point; ``splay_rise`` (220) runs from that tangent
    point to the tangent point on the stem face; ``splay_run`` (300) is the
    horizontal ledge projection. Origin at mid-soffit of the unit.
    """

    depth: float
    unit: str
    bottom_width: float
    stem_width: float
    edge_height: float = 55.0
    splay_rise: float = 220.0
    splay_run: float = 300.0
    fillet_radius: float = 50.0

    def corners(self) -> tuple[list[tuple[float, float]], dict[int, float]]:
        y_edge, y_root = _splay_sharp_heights(self.edge_height, self.splay_rise,
                                              self.splay_run, self.fillet_radius)
        b, h, r = self.bottom_width / 2, self.depth, self.fillet_radius
        if self.unit == "M":
            s = self.stem_width / 2
            pts = [(-b, 0), (b, 0), (b, y_edge), (s, y_root), (s, h),
                   (-s, h), (-s, y_root), (-b, y_edge)]
            return pts, {2: r, 3: r, 6: r, 7: r}
        if self.unit == "K":
            x_stem = b - self.splay_run
            pts = [(-b, 0), (b, 0), (b, y_edge), (x_stem, y_root), (x_stem, h), (-b, h)]
            return pts, {2: r, 3: r}
        raise ValueError(f"unit must be 'K' or 'M', got {self.unit!r}")

    @property
    def outline(self) -> list[tuple[float, float]]:
        pts, radii = self.corners()
        return _rounded(pts, radii)


@dataclass(frozen=True)
class VphGirderDimensions:
    """VPH-PTMN I / inverted-T girders (millimetres, origin mid-soffit).

    Lower flange: ``bottom_edge_height`` is the fillet tangent point on the
    vertical flange face (140 above soffit), ``bottom_splay_rise`` (220) runs
    to the tangent point on the web; the horizontal splay run is
    (bottom_width - web_width)/2. ``bottom_chamfer`` is the 15/15 soffit
    chamfer (SKOSENIE 15/15).

    Upper flange (absent when ``top_width`` is None): ``top_edge_depth`` is
    the theoretical sharp corner of the flange edge measured down from the
    top; ``top_web_tangent_depth`` is the fillet tangent point on the web
    measured down from the top. ``top_edge_radius`` is 50 except on the
    2.1 m girder (sharp edge). The edge rebate is ``rebate_width`` ×
    ``rebate_depth``. A raised top strip (2016-T only) is
    ``strip_width`` × ``strip_height``, included in ``depth``.
    """

    depth: float
    bottom_width: float
    web_width: float
    top_width: float | None
    top_edge_depth: float = 75.0
    top_web_tangent_depth: float = 167.0
    top_edge_radius: float = 50.0
    rebate_width: float = 30.0
    rebate_depth: float = 20.0
    strip_width: float = 0.0
    strip_height: float = 0.0
    bottom_chamfer: float = 15.0
    bottom_edge_height: float = 140.0
    bottom_splay_rise: float = 220.0
    fillet_radius: float = 50.0

    def _top_root_sharp_depth(self) -> float:
        run = (self.top_width - self.web_width) / 2
        root = self.top_web_tangent_depth
        for _ in range(200):
            theta = math.atan((root - self.top_edge_depth) / run)
            root = self.top_web_tangent_depth - _tangent_length(self.fillet_radius, theta)
        return root

    def corners(self) -> tuple[list[tuple[float, float]], dict[int, float]]:
        b, w, h, c = self.bottom_width / 2, self.web_width / 2, self.depth, self.bottom_chamfer
        r = self.fillet_radius
        y_edge, y_root = _splay_sharp_heights(self.bottom_edge_height, self.bottom_splay_rise,
                                              b - w, r)
        right: list[tuple[float, float]] = []
        radii_right: dict[int, float] = {}
        if c:
            right += [(b - c, 0.0), (b, c)]
        else:
            right += [(b, 0.0)]
        radii_right[len(right)] = r
        right.append((b, y_edge))
        radii_right[len(right)] = r
        right.append((w, y_root))
        if self.top_width is None:
            top_body = h - self.strip_height
            right.append((w, top_body))
            if self.strip_height:
                s = self.strip_width / 2
                right += [(s, top_body), (s, h)]
        else:
            t = self.top_width / 2
            radii_right[len(right)] = r
            right.append((w, h - self._top_root_sharp_depth()))
            if self.top_edge_radius:
                radii_right[len(right)] = self.top_edge_radius
            right.append((t, h - self.top_edge_depth))
            right += [(t, h - self.rebate_depth), (t - self.rebate_width, h - self.rebate_depth),
                      (t - self.rebate_width, h)]
        left = [(-x, y) for x, y in reversed(right)]
        pts = right + left
        n = len(pts)
        radii = dict(radii_right)
        radii.update({n - 1 - i: rad for i, rad in radii_right.items()})
        return pts, radii

    @property
    def outline(self) -> list[tuple[float, float]]:
        pts, radii = self.corners()
        return _rounded(pts, radii)


class _VphSection:
    _KIND = ""

    def __init__(self, size: str):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(s for s in data["sections"] if s["size"] == size)
        self.size = size
        self.row = row
        self.published = row["published"]
        self.designations = tuple(d["designation"] for d in row["catalogue_rows"])
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = self._dimensions(row["model"])

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline), sign=1.0)

    @property
    def geometry(self):
        """Gross concrete ``sectionproperties`` geometry."""
        return geometry_from_polygon(self.polygon)


class VphSlabBeamSection(_VphSection):
    """VPH-PTMN 2016-PM inverted-T slab-bridge units, 11/13/15 m (K and M)."""

    SIZES = ("2016-PM11-K", "2016-PM11-M", "2016-PM13-K", "2016-PM13-M",
             "2016-PM15-K", "2016-PM15-M")

    def __init__(self, size: str = "2016-PM13-M"):
        super().__init__(size)

    @staticmethod
    def _dimensions(model: dict) -> VphSlabBeamDimensions:
        return VphSlabBeamDimensions(**model)


class VphGirderSection(_VphSection):
    """VPH-PTMN 2016-T, 2010 I (1.2/1.4 m), 2016-I and 2010-R2 (1.9/2.1 m)."""

    SIZES = ("2016-T", "2010-I-1.2", "2016-I", "2010-I-1.4", "2010-R2-1.9", "2010-R2-2.1")

    def __init__(self, size: str = "2010-I-1.2"):
        super().__init__(size)

    @staticmethod
    def _dimensions(model: dict) -> VphGirderDimensions:
        return VphGirderDimensions(**model)


__all__ = ["VphSlabBeamDimensions", "VphSlabBeamSection",
           "VphGirderDimensions", "VphGirderSection"]
