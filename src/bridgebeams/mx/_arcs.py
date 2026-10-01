"""Small plane-geometry helpers for tangent fillets (private to ``mx``).

All functions work in the caller's units. Points are ``(x, y)`` tuples and
directions need not be normalised.
"""

from __future__ import annotations

import math

Point = tuple[float, float]


def unit(v: Point) -> Point:
    n = math.hypot(v[0], v[1])
    return (v[0] / n, v[1] / n)


def intersect(p: Point, u: Point, q: Point, v: Point) -> Point:
    """Intersection of the lines p + s*u and q + t*v."""
    det = u[0] * (-v[1]) - u[1] * (-v[0])
    if abs(det) < 1e-14:
        raise ValueError("parallel lines")
    rx, ry = q[0] - p[0], q[1] - p[1]
    s = (rx * (-v[1]) - ry * (-v[0])) / det
    return (p[0] + s * u[0], p[1] + s * u[1])


def arc(centre: Point, radius: float, start: Point, end: Point, n: int) -> list[Point]:
    """Points on the shorter circular arc from ``start`` to ``end`` (inclusive)."""
    a0 = math.atan2(start[1] - centre[1], start[0] - centre[0])
    a1 = math.atan2(end[1] - centre[1], end[0] - centre[0])
    sweep = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return [
        (
            centre[0] + radius * math.cos(a0 + sweep * i / n),
            centre[1] + radius * math.sin(a0 + sweep * i / n),
        )
        for i in range(n + 1)
    ]


def fillet(corner: Point, d_in: Point, d_out: Point, radius: float, n: int) -> list[Point]:
    """Tangent fillet at the corner of two straight edges.

    ``d_in`` points from the corner back along the incoming edge and
    ``d_out`` from the corner along the outgoing edge. Returns the arc from
    the incoming tangent point to the outgoing tangent point.
    """
    u, v = unit(d_in), unit(d_out)
    cos_t = max(-1.0, min(1.0, u[0] * v[0] + u[1] * v[1]))
    theta = math.acos(cos_t)
    tangent = radius / math.tan(theta / 2)
    p = (corner[0] + u[0] * tangent, corner[1] + u[1] * tangent)
    q = (corner[0] + v[0] * tangent, corner[1] + v[1] * tangent)
    b = unit((u[0] + v[0], u[1] + v[1]))
    dist = radius / math.sin(theta / 2)
    centre = (corner[0] + b[0] * dist, corner[1] + b[1] * dist)
    return arc(centre, radius, p, q, n)


def line_x_at(p: Point, q: Point, y: float) -> float:
    """x on the line through p and q at height y."""
    return p[0] + (q[0] - p[0]) * (y - p[1]) / (q[1] - p[1])


def offset_line(p: Point, q: Point, distance: float) -> tuple[Point, Point]:
    """Offset the line p->q by ``distance`` to its right-hand side."""
    d = unit((q[0] - p[0], q[1] - p[1]))
    nrm = (d[1], -d[0])
    return (
        (p[0] + nrm[0] * distance, p[1] + nrm[1] * distance),
        (q[0] + nrm[0] * distance, q[1] + nrm[1] * distance),
    )


def ring_properties(rings: list[list[Point]]) -> dict[str, float]:
    """Area, centroid height and centroidal Ixx of an exterior minus holes.

    ``rings[0]`` is the exterior and the remainder are holes; winding is
    handled internally (absolute areas of each ring are used).
    """
    total_a = total_ay = total_i0 = 0.0
    for k, ring in enumerate(rings):
        pts = list(ring)
        if pts[0] != pts[-1]:
            pts.append(pts[0])
        a = ay = i0 = 0.0
        for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
            c = x1 * y2 - x2 * y1
            a += c / 2
            ay += (y1 + y2) * c / 6
            i0 += (y1 * y1 + y1 * y2 + y2 * y2) * c / 12
        sign = 1.0 if a > 0 else -1.0
        a, ay, i0 = a * sign, ay * sign, i0 * sign
        if k:
            a, ay, i0 = -a, -ay, -i0
        total_a += a
        total_ay += ay
        total_i0 += i0
    cy = total_ay / total_a
    return {"area": total_a, "cy": cy, "ixx": total_i0 - total_a * cy * cy}
