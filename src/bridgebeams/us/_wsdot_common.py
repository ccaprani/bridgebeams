"""Shared loader and polygon helpers for the extended WSDOT girder modules.

Source dimensions are stored in inches in
``data/wsdot_extended_girders.json``; public geometry is millimetres
(1 in = 25.4 mm exactly), origin at the soffit centre, y upwards.
"""

from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

INCH_TO_MM = 25.4
DATA_FILE = "data/wsdot_extended_girders.json"


@lru_cache(maxsize=1)
def load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.us").joinpath(DATA_FILE).read_text(encoding="utf-8")
    )


def dedupe(points):
    """Drop consecutive duplicate vertices (also across the closing edge)."""
    out = []
    for p in points:
        if not out or (abs(p[0] - out[-1][0]) > 1e-12 or abs(p[1] - out[-1][1]) > 1e-12):
            out.append(p)
    if len(out) > 1 and abs(out[0][0] - out[-1][0]) < 1e-12 and abs(out[0][1] - out[-1][1]) < 1e-12:
        out.pop()
    return out


def mirrored_ring_in(right_half_in):
    """Full ring (inches) from a right-half path starting and ending on x = 0."""
    ring = list(right_half_in) + [(-x, y) for x, y in reversed(right_half_in)]
    return dedupe(ring)


def to_mm(points_in):
    return [(x * INCH_TO_MM, y * INCH_TO_MM) for x, y in points_in]


def ccw_polygon(shell_mm, holes_mm=()):
    return orient(Polygon(shell_mm, list(holes_mm)), sign=1.0)
