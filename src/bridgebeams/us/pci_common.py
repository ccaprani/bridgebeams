"""Shared helpers for the PCI and FDOT section modules (round 2, 2026-09).

All source outlines are transcribed in inches and converted to millimetres
only when the Shapely polygon is built. Outlines are described as a right
half (x >= 0) with optional per-vertex corner treatments:

* ``("r", R)`` - circular fillet of radius ``R`` tangent to both edges,
  polygonised with ``arc_segments`` chords (convex or re-entrant corner);
* ``("c", c)`` - straight chamfer cutting ``c`` along both edges.

The helpers are private to the ``us`` PCI/FDOT modules; public classes
expose ``.polygon`` and ``.geometry`` exactly like the rest of the package.
"""

from __future__ import annotations

import json
import math
from importlib import resources
from typing import Iterable, Sequence

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

INCH_MM = 25.4

Vertex = tuple  # (x, y) or (x, y, (kind, size))


def load_json(name: str) -> dict:
    """Load one of this package's data tables."""
    return json.loads(
        resources.files("bridgebeams.us").joinpath(f"data/{name}").read_text(encoding="utf-8")
    )


def mirror_right_half(right: Sequence[Vertex]) -> list[Vertex]:
    """Close a right-half outline into a full symmetric ring.

    ``right`` runs anticlockwise (up the right-hand side). Points lying on
    the centreline (x == 0) are not duplicated by the mirror.
    """
    left = []
    for v in reversed(right):
        if abs(v[0]) < 1e-12:
            continue
        left.append((-v[0], v[1], *v[2:]))
    return list(right) + left


def _unit(dx: float, dy: float) -> tuple[float, float]:
    n = math.hypot(dx, dy)
    return dx / n, dy / n


def apply_corners(ring: Sequence[Vertex], arc_segments: int = 32) -> list[tuple[float, float]]:
    """Replace flagged vertices of a closed ring by fillets or chamfers."""
    pts = [(float(v[0]), float(v[1])) for v in ring]
    mods = [v[2] if len(v) > 2 else None for v in ring]
    n = len(pts)
    out: list[tuple[float, float]] = []
    for i, (p, mod) in enumerate(zip(pts, mods)):
        if mod is None:
            out.append(p)
            continue
        kind, size = mod
        a, b = pts[i - 1], pts[(i + 1) % n]
        u = _unit(a[0] - p[0], a[1] - p[1])
        v = _unit(b[0] - p[0], b[1] - p[1])
        if kind == "c":
            out.append((p[0] + u[0] * size, p[1] + u[1] * size))
            out.append((p[0] + v[0] * size, p[1] + v[1] * size))
            continue
        if kind != "r":
            raise ValueError(f"unknown corner treatment {kind!r}")
        theta = math.acos(max(-1.0, min(1.0, u[0] * v[0] + u[1] * v[1])))
        t = size / math.tan(theta / 2)
        t1 = (p[0] + u[0] * t, p[1] + u[1] * t)
        t2 = (p[0] + v[0] * t, p[1] + v[1] * t)
        bis = _unit(u[0] + v[0], u[1] + v[1])
        d = size / math.sin(theta / 2)
        c = (p[0] + bis[0] * d, p[1] + bis[1] * d)
        s = math.atan2(t1[1] - c[1], t1[0] - c[0])
        e = math.atan2(t2[1] - c[1], t2[0] - c[0])
        sweep = (e - s + math.pi) % (2 * math.pi) - math.pi
        for k in range(arc_segments + 1):
            ang = s + sweep * k / arc_segments
            out.append((c[0] + size * math.cos(ang), c[1] + size * math.sin(ang)))
    return out


def circle(cx: float, cy: float, r: float, n: int = 128) -> list[tuple[float, float]]:
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n))
            for k in range(n)]


def to_mm_polygon(exterior: Iterable, holes: Iterable[Iterable] = ()) -> Polygon:
    """Scale inch coordinates to mm and orient (CCW shell, CW holes)."""
    ext = [(x * INCH_MM, y * INCH_MM) for x, y in exterior]
    ints = [[(x * INCH_MM, y * INCH_MM) for x, y in h] for h in holes]
    return orient(Polygon(ext, ints), sign=1.0)


def _ring_terms(coords):
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    a = cx = cy = ixx0 = iyy0 = 0.0
    for i in range(len(xs) - 1):
        x0, y0, x1, y1 = xs[i], ys[i], xs[i + 1], ys[i + 1]
        cr = x0 * y1 - x1 * y0
        a += cr / 2
        cx += (x0 + x1) * cr / 6
        cy += (y0 + y1) * cr / 6
        ixx0 += (y0 * y0 + y0 * y1 + y1 * y1) * cr / 12
        iyy0 += (x0 * x0 + x0 * x1 + x1 * x1) * cr / 12
    return a, cx, cy, ixx0, iyy0


def gross_properties(poly: Polygon) -> dict[str, float]:
    """Area, centroid, centroidal Ixx/Iyy and perimeter including voids.

    Uses signed shoelace terms so correctly oriented interiors subtract.
    """
    poly = orient(poly, sign=1.0)
    tot = [0.0] * 5
    for ring in [poly.exterior, *poly.interiors]:
        for k, t in enumerate(_ring_terms(list(ring.coords))):
            tot[k] += t
    a, sx, sy, i0x, i0y = tot
    cx, cy = sx / a, sy / a
    return {
        "area": a, "cx": cx, "cy": cy,
        "ixx": i0x - a * cy * cy, "iyy": i0y - a * cx * cx,
        "perimeter": poly.exterior.length,
    }


def gross_properties_in(poly: Polygon) -> dict[str, float]:
    """``gross_properties`` expressed in inch units."""
    p = gross_properties(poly)
    return {"area": p["area"] / INCH_MM**2, "cx": p["cx"] / INCH_MM, "cy": p["cy"] / INCH_MM,
            "ixx": p["ixx"] / INCH_MM**4, "iyy": p["iyy"] / INCH_MM**4,
            "perimeter": p["perimeter"] / INCH_MM}


__all__ = ["INCH_MM", "gross_properties", "gross_properties_in"]
