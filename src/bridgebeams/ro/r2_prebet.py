"""Prebet Aiud (Romania) precast prestressed road-bridge girders.

Source: Prebet Aiud S.A., product page "Grinzi pentru viaducte / Viaduct
girders" (https://www.prebet.ro/en/viaduct-girders/), seven CAD section
images (JPEG, 1600 x 900 px). Dimensions are centimetres; superscripts are
decimals (8^2 = 8.2 cm). Every size drawn is implemented:

* ``INVT42-EC``/``INVT52-EC``/``INVT42-TIP``/``INVT52-TIP`` - small
  pretensioned inverted-T (page: H = 0.42 / 0.52 m); the dashed line 10 cm
  below the top is the 42 cm variant.
* ``I72-TIP``/``I80-TIP`` - pretensioned I (H = 0.72 / 0.80 m).
* ``T93-TIP``/``T95-EC`` - pretensioned T (H = 0.93 m).
* ``T103-TIP``/``T105-EC`` - pretensioned or post-tensioned T (H = 1.03-1.05 m).
* ``T140``..``T200`` - pretensioned "tip T" bulb girders (H = 1.40-2.00 m).
* ``I130``..``I180`` - pretensioned "tip I" (H = 1.30-1.80 m, top block max).
* ``TS160-TIP``/``TS184-EC``/``TS210-EC`` - segmental ("tronsonate") T.

Straight-sided outlines are fully dimensioned (``transcribed``); sections
with fillets use the printed radius constructed tangent to the printed
faces, plus small undimensioned soffit chamfers where drawn
(``transcribed-with-convention``). See ``data/r2_prebet.json``.
Millimetres, origin at mid-soffit, y upwards; no end blocks, ducts or
strands.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile

from ._arc import fillet


@lru_cache(maxsize=None)
def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ro").joinpath("data/r2_prebet.json").read_text(encoding="utf-8")
    )


def _arc(centre, radius, start, end, segments=24):
    """Shortest circular arc from ``start`` to ``end`` (both on the circle)."""
    a0 = math.atan2(start[1] - centre[1], start[0] - centre[0])
    a1 = math.atan2(end[1] - centre[1], end[0] - centre[0])
    sweep = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return [
        (centre[0] + radius * math.cos(a0 + sweep * i / segments),
         centre[1] + radius * math.sin(a0 + sweep * i / segments))
        for i in range(segments + 1)
    ]


def _tangent_point(p, centre, radius):
    """Tangent point on the circle, seen from external point ``p``, nearer the web (smaller x)."""
    dx, dy = p[0] - centre[0], p[1] - centre[1]
    d = math.hypot(dx, dy)
    a = math.acos(radius / d)
    b = math.atan2(dy, dx)
    pts = [(centre[0] + radius * math.cos(b + s * a), centre[1] + radius * math.sin(b + s * a)) for s in (1, -1)]
    return min(pts, key=lambda q: q[0])


def _web_fillet(web_point, web_dir, radius, edge):
    """Fillet tangent to a web line at ``web_point`` and to the line through ``edge``.

    ``web_dir`` is a unit vector along the web face; the fillet centre is on
    the outer (void) side. Returns (tangent point on flange line, arc points
    from that tangent point to ``web_point``).
    """
    n = (web_dir[1], -web_dir[0])
    if n[0] < 0:
        n = (-n[0], -n[1])
    centre = (web_point[0] + radius * n[0], web_point[1] + radius * n[1])
    t = _tangent_point(edge, centre, radius)
    return t, _arc(centre, radius, t, web_point)


def half_profile_cm(kind: str, depth: float, p: dict) -> list[tuple[float, float]]:
    """Right-half outline in cm (soffit centreline side first, running up to the top)."""
    H = depth
    if kind == "inverted-T-EC":
        a = (p["web_width_at_tangent"] / 2, p["web_tangent_level"])
        b = (p["top_width_ref"] / 2, p["top_ref_level"])
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        d = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        edge = (p["edge_width"] / 2, p["edge_level"])
        _, arc = _web_fillet(a, d, p["radius"], edge)
        x_top = a[0] + (b[0] - a[0]) * (H - a[1]) / (b[1] - a[1])
        return [(p["soffit_width"] / 2, 0.0), edge, *arc, (x_top, H)]
    if kind == "inverted-T-TIP":
        c = p["soffit_chamfer"]
        xb = p["bottom_width"] / 2
        edge = (xb, p["edge_level"])
        corner = (p["throat_width"] / 2, p["throat_level"])
        stem = (p["stem_width"] / 2, p["stem_level"])
        return [(xb - c, 0.0), (xb, c), edge, *fillet(corner, edge, stem, p["radius"]), stem, (stem[0], H)]
    if kind == "I-fillet":
        c = p["soffit_chamfer"]
        xb, xw, xt = p["bottom_width"] / 2, p["web_width"] / 2, p["top_width"] / 2
        edge = (xb, p["edge_level"])
        _, low = _web_fillet((xw, p["lower_tangent_level"]), (0.0, 1.0), p["radius"], edge)
        top_edge = (xt, H - p["top_edge"])
        _, up = _web_fillet((xw, H - p["upper_tangent_below_top"]), (0.0, -1.0), p["radius"], top_edge)
        return [(xb - c, 0.0), (xb, c), edge, *low, *reversed(up), top_edge, (xt, H)]
    if kind == "T-bulb":
        xw, xt = p["web_width"] / 2, p["top_width"] / 2
        edge = (p["edge_width"] / 2, p["edge_level"])
        _, low = _web_fillet((xw, p["lower_tangent_level"]), (0.0, 1.0), p["lower_radius"], edge)
        top_edge = (xt, H - p["top_edge"])
        knee = (xw + p["knee_run"], H - p["top_edge"] - p["underside_drop"])
        slope = (top_edge[1] - knee[1]) / (top_edge[0] - knee[0])
        corner = (xw, knee[1] - slope * p["knee_run"])
        up = fillet(corner, (xw, 0.0), top_edge, p["upper_radius"])
        return [(p["soffit_width"] / 2, 0.0), edge, *low, *up, top_edge, (xt, H)]
    if kind == "polyline":
        x, y = p["bottom_width"] / 2, p["edge_level"]
        pts = [(x, 0.0), (x, y)]
        for run, rise in p["lower_segments"]:
            x, y = x - run, y + rise
            pts.append((x, y))
        up = p["upper_segments"]
        y = H - p["top_edge"] - sum(r for _, r in up)
        pts.append((x, y))
        for run, rise in up:
            x, y = x + run, y + rise
            pts.append((x, y))
        pts.append((x, H))
        return pts
    raise ValueError(f"unknown kind {kind!r}")


@dataclass(frozen=True)
class PrebetGirderDimensions:
    """Model parameters of one Prebet girder (mm; converted from printed cm)."""

    mark: str
    kind: str
    depth: float
    top_width: float
    bottom_width: float
    params: tuple  # sorted (name, value) pairs in cm, as in the JSON

    def __getitem__(self, key):
        return dict(self.params)[key]


class PrebetGirderSection:
    """Prebet Aiud precast road/viaduct girders (21 drawn sizes)."""

    SIZES = (
        "INVT42-EC", "INVT52-EC", "INVT42-TIP", "INVT52-TIP",
        "I72-TIP", "I80-TIP",
        "T93-TIP", "T95-EC", "T103-TIP", "T105-EC",
        "T140", "T160", "T180", "T200",
        "I130", "I150", "I160", "I180",
        "TS160-TIP", "TS184-EC", "TS210-EC",
    )
    source_status = "producer web page drawings (Prebet Aiud, images dated 2016-05)"

    def __init__(self, size: str = "T95-EC"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load_data()["sizes"][size]
        self.size = size
        self.record = row
        self.name = row["name_original"]
        self.provenance = row["provenance"]
        p = row["model_parameters_cm"]
        half = half_profile_cm(row["kind"], row["depth_cm"], p)
        self._half_mm = [(x * 10.0, y * 10.0) for x, y in half]
        self.dimensions = PrebetGirderDimensions(
            mark=size,
            kind=row["kind"],
            depth=row["depth_cm"] * 10.0,
            top_width=2 * self._half_mm[-1][0],
            bottom_width=2 * max(x for x, y in self._half_mm if y < row["depth_cm"] * 5.0),
            params=tuple(sorted((k, json.dumps(v) if isinstance(v, list) else v) for k, v in p.items())),
        )

    @property
    def half_profile(self) -> list[tuple[float, float]]:
        return list(self._half_mm)

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self._half_mm)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["PrebetGirderDimensions", "PrebetGirderSection", "half_profile_cm"]
