"""Small circular-fillet helper shared by the Netherlands modules."""

from __future__ import annotations

import math


def fillet(corner, toward_a, toward_b, radius, segments=24):
    """Points of a circular fillet inscribed in the corner ``a-corner-b``.

    ``toward_a``/``toward_b`` are points on the two straight edges. The
    returned points run from the tangent point on edge ``a`` to the one on
    edge ``b``, both included.
    """
    cx, cy = corner
    ua = (toward_a[0] - cx, toward_a[1] - cy)
    ub = (toward_b[0] - cx, toward_b[1] - cy)
    la, lb = math.hypot(*ua), math.hypot(*ub)
    ua = (ua[0] / la, ua[1] / la)
    ub = (ub[0] / lb, ub[1] / lb)
    angle = math.acos(max(-1.0, min(1.0, ua[0] * ub[0] + ua[1] * ub[1])))
    t = radius / math.tan(angle / 2)
    bis = (ua[0] + ub[0], ua[1] + ub[1])
    lbis = math.hypot(*bis)
    d = radius / math.sin(angle / 2)
    centre = (cx + bis[0] / lbis * d, cy + bis[1] / lbis * d)
    pa = (cx + ua[0] * t, cy + ua[1] * t)
    pb = (cx + ub[0] * t, cy + ub[1] * t)
    a0 = math.atan2(pa[1] - centre[1], pa[0] - centre[0])
    a1 = math.atan2(pb[1] - centre[1], pb[0] - centre[0])
    sweep = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return [
        (centre[0] + radius * math.cos(a0 + sweep * i / segments),
         centre[1] + radius * math.sin(a0 + sweep * i / segments))
        for i in range(segments + 1)
    ]
