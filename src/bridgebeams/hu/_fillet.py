"""Tangent circular fillets on a polyline (private helper)."""

from __future__ import annotations

import math

Point = tuple[float, float]


def fillet_polyline(
    vertices: list[tuple[float, float, float]], segments: int = 16
) -> list[Point]:
    """Return a polyline with circular fillets at interior vertices.

    ``vertices`` are ``(x, y, radius)``; a radius of 0 keeps a sharp
    corner. End vertices are never filleted. Each arc is tangent to both
    adjacent straight segments and is tessellated into ``segments``
    chords. Works for convex and re-entrant corners alike.
    """
    out: list[Point] = [(vertices[0][0], vertices[0][1])]
    for i in range(1, len(vertices) - 1):
        bx, by, r = vertices[i]
        if r <= 0:
            out.append((bx, by))
            continue
        ax, ay = out[-1]
        cx_, cy_ = vertices[i + 1][0], vertices[i + 1][1]
        u = (ax - bx, ay - by)
        v = (cx_ - bx, cy_ - by)
        lu, lv = math.hypot(*u), math.hypot(*v)
        u = (u[0] / lu, u[1] / lu)
        v = (v[0] / lv, v[1] / lv)
        theta = math.acos(max(-1.0, min(1.0, u[0] * v[0] + u[1] * v[1])))
        t = r / math.tan(theta / 2)
        if t > lu + 1e-9 or t > lv + 1e-9:
            raise ValueError(f"fillet radius {r} too large at vertex {i}")
        bis = (u[0] + v[0], u[1] + v[1])
        lb = math.hypot(*bis)
        d = r / math.sin(theta / 2)
        centre = (bx + bis[0] / lb * d, by + bis[1] / lb * d)
        p = (bx + u[0] * t, by + u[1] * t)
        q = (bx + v[0] * t, by + v[1] * t)
        a0 = math.atan2(p[1] - centre[1], p[0] - centre[0])
        a1 = math.atan2(q[1] - centre[1], q[0] - centre[0])
        sweep = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        for k in range(segments + 1):
            a = a0 + sweep * k / segments
            out.append((centre[0] + r * math.cos(a), centre[1] + r * math.sin(a)))
    out.append((vertices[-1][0], vertices[-1][1]))
    return out
