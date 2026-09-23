"""Shared helpers for the round-2 US state DOT modules (``txdot_*``, ``state_*``).

Source dimensions are kept in inches in each module's JSON file; public
geometry is millimetres (1 in = 25.4 mm exactly), origin at the soffit
centre, y upwards. Polygons are returned anticlockwise with clockwise
interiors (voids).
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

INCH_TO_MM = 25.4
ARC_SEGMENTS = 16


@lru_cache(maxsize=None)
def load_json(name: str) -> dict:
    """Load ``bridgebeams/us/data/<name>`` (cached)."""
    return json.loads(
        resources.files("bridgebeams.us").joinpath("data", name).read_text(encoding="utf-8")
    )


def dedupe(points, tol: float = 1e-9):
    """Drop consecutive duplicate vertices (also across the closing edge)."""
    out: list[tuple[float, float]] = []
    for p in points:
        if not out or abs(p[0] - out[-1][0]) > tol or abs(p[1] - out[-1][1]) > tol:
            out.append((float(p[0]), float(p[1])))
    while len(out) > 1 and abs(out[0][0] - out[-1][0]) <= tol and abs(out[0][1] - out[-1][1]) <= tol:
        out.pop()
    return out


def mirror_half(right_half):
    """Full ring from a right-half path running from (0, 0) up to (0, depth).

    The path must start and end on x = 0; the left half is its mirror image.
    """
    ring = list(right_half) + [(-x, y) for x, y in reversed(right_half)]
    return dedupe(ring)


def to_mm(points_in):
    return [(x * INCH_TO_MM, y * INCH_TO_MM) for x, y in points_in]


def ccw_polygon(shell, holes=()):
    """Valid-orientation polygon: CCW shell, CW interiors."""
    return orient(Polygon(shell, [list(h) for h in holes]), sign=1.0)


def fillet(p_prev, corner, p_next, radius: float, n: int = ARC_SEGMENTS):
    """Replace ``corner`` by a tangent circular arc of ``radius``.

    ``p_prev`` and ``p_next`` are points on the two straight lines through
    ``corner``. Returns the arc as ``n + 1`` points from the tangent point on
    the incoming line to the tangent point on the outgoing line. A zero
    radius returns ``[corner]``.
    """
    if radius <= 0:
        return [corner]
    ux, uy = p_prev[0] - corner[0], p_prev[1] - corner[1]
    vx, vy = p_next[0] - corner[0], p_next[1] - corner[1]
    lu, lv = math.hypot(ux, uy), math.hypot(vx, vy)
    ux, uy, vx, vy = ux / lu, uy / lu, vx / lv, vy / lv
    cosang = max(-1.0, min(1.0, ux * vx + uy * vy))
    ang = math.acos(cosang)
    if abs(math.pi - ang) < 1e-12:
        return [corner]
    t = radius / math.tan(ang / 2)
    p = (corner[0] + ux * t, corner[1] + uy * t)
    q = (corner[0] + vx * t, corner[1] + vy * t)
    bx, by = ux + vx, uy + vy
    lb = math.hypot(bx, by)
    d = radius / math.sin(ang / 2)
    c = (corner[0] + bx / lb * d, corner[1] + by / lb * d)
    a0 = math.atan2(p[1] - c[1], p[0] - c[0])
    a1 = math.atan2(q[1] - c[1], q[0] - c[0])
    sweep = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return [(c[0] + radius * math.cos(a0 + sweep * i / n),
             c[1] + radius * math.sin(a0 + sweep * i / n)) for i in range(n + 1)]


def filleted_path(points, radii, n: int = ARC_SEGMENTS):
    """Polyline with vertex ``i`` rounded by ``radii.get(i, 0)``.

    ``points`` is an open path; the first and last vertices are never rounded.
    """
    out = [points[0]]
    for i in range(1, len(points) - 1):
        r = radii.get(i, 0.0)
        out.extend(fillet(points[i - 1], points[i], points[i + 1], r, n) if r else [points[i]])
    out.append(points[-1])
    return dedupe(out)


def circle(cx: float, cy: float, r: float, n: int = 64):
    """Clockwise circle ring (for use as a void)."""
    return [(cx + r * math.cos(-2 * math.pi * i / n), cy + r * math.sin(-2 * math.pi * i / n))
            for i in range(n)]


def _ring_terms(coords):
    pts = list(coords)
    if pts[0] == pts[-1]:
        pts = pts[:-1]
    a = sy = ixx = iyy = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        c = x0 * y1 - x1 * y0
        a += c
        sy += (y0 + y1) * c
        ixx += (y0 * y0 + y0 * y1 + y1 * y1) * c
        iyy += (x0 * x0 + x0 * x1 + x1 * x1) * c
    return a / 2, sy / 6, ixx / 12, iyy / 12


def gross_properties(poly: Polygon, unit: float = 1.0) -> dict[str, float]:
    """Area, yb (centroid above y=0), centroidal Ix and Iy about x=0, holes included.

    ``unit`` divides lengths (use 25.4 for inches from a mm polygon).
    """
    a, s, i, j = _ring_terms(poly.exterior.coords)
    sign = 1.0 if a > 0 else -1.0
    a, s, i, j = a * sign, s * sign, i * sign, j * sign
    for h in poly.interiors:
        da, ds, di, dj = _ring_terms(h.coords)
        k = 1.0 if da > 0 else -1.0  # normalise hole to positive area, then subtract
        a, s, i, j = a - k * da, s - k * ds, i - k * di, j - k * dj
    cy = s / a
    return {
        "area": a / unit**2,
        "yb": cy / unit,
        "ix": (i - a * cy * cy) / unit**4,
        "iy": j / unit**4,
    }


__all__ = [
    "INCH_TO_MM", "load_json", "dedupe", "mirror_half", "to_mm", "ccw_polygon",
    "fillet", "filleted_path", "circle", "gross_properties",
]
