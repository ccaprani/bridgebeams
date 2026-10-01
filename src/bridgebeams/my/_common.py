"""Shared helpers for the Malaysian precast beam families (internal)."""

from __future__ import annotations

import json
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def load_data(name: str) -> dict:
    return json.loads(
        resources.files("bridgebeams.my").joinpath(f"data/{name}").read_text(encoding="utf-8")
    )


def mirror(right: list[tuple[float, float]]) -> Polygon:
    """Mirror a right-half chain (soffit -> top, or soffit -> centreline).

    ``right`` starts at the right soffit corner and runs up the right side.
    The mirrored left side is appended in reverse, giving an anticlockwise
    ring. Points on x = 0 are not duplicated.
    """
    left = [(-x, y) for x, y in reversed(right)]
    ring: list[tuple[float, float]] = []
    for p in list(right) + left:
        if not ring or abs(p[0] - ring[-1][0]) > 1e-9 or abs(p[1] - ring[-1][1]) > 1e-9:
            ring.append((float(p[0]), float(p[1])))
    if abs(ring[0][0] - ring[-1][0]) < 1e-9 and abs(ring[0][1] - ring[-1][1]) < 1e-9:
        ring.pop()
    return orient(Polygon(ring), sign=1)


class _SizedSection:
    """Base: size lookup in a JSON table, provenance, polygon/geometry."""

    SIZES: tuple[str, ...] = ()
    _DATA = ""
    source_status = ""

    def __init__(self, size: str):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = load_data(self._DATA)
        self.size = size
        self.published = data["sections"][size]
        self.provenance = self.published["provenance"]
        self.source_status = data["source_status"]

    def right_half(self) -> list[tuple[float, float]]:  # pragma: no cover - abstract
        raise NotImplementedError

    @property
    def polygon(self) -> Polygon:
        return mirror(self.right_half())

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)
