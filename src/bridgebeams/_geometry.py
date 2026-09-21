"""Shared geometry helpers for bridge beam section libraries."""

from __future__ import annotations

import numpy as np
import sectionproperties.pre.geometry as sp_geom
from shapely.geometry import Polygon


def polygon_from_half_profile(right_half: list[tuple[float, float]]) -> Polygon:
    """Build a closed, mirror-symmetric polygon from a right-half profile.

    ``right_half`` runs from the soffit centreline **up the right side** to the
    top. The returned polygon mirrors the profile about x = 0 and closes
    through the top edge, giving an anti-clockwise simple polygon.

    Parameters
    ----------
    right_half:
        Points (x, y), x >= 0, first point on the soffit (y = 0).
    """
    right = [(x, y) for x, y in right_half]
    # mirror ALL points including the soffit corner so the bottom edge closes
    left = [(-x, y) for x, y in reversed(right)]
    return Polygon(left + right)


def geometry_from_polygon(poly: Polygon) -> sp_geom.Geometry:
    """Wrap a shapely polygon as a ``sectionproperties`` Geometry."""
    return sp_geom.Geometry(poly)


def as_polygon(geometry: sp_geom.Geometry) -> Polygon:
    """Return the shapely polygon of a Geometry across v3.x versions."""
    poly = getattr(geometry, "polygon", None)
    if poly is None:
        poly = geometry.geom
    return poly


def section_properties(poly: Polygon) -> dict[str, float]:
    """Exact geometric properties of a polygon (shoelace integration).

    Returns area, centroid height ``cy`` above y = 0, and second moment of
    area ``ixx`` about the horizontal centroidal axis, all in the polygon's
    own units.
    """
    pts = list(poly.exterior.coords)
    xs = np.asarray([p[0] for p in pts], float)
    ys = np.asarray([p[1] for p in pts], float)
    x2, y2 = np.roll(xs, -1), np.roll(ys, -1)
    cr = xs * y2 - x2 * ys
    area = abs(cr.sum()) / 2.0
    cy = ((ys + y2) * cr).sum() / (6.0 * area)
    i0 = abs(((ys * ys + ys * y2 + y2 * y2) * cr).sum() / 12.0)
    return {"area": area, "cy": cy, "ixx": i0 - area * cy * cy}
