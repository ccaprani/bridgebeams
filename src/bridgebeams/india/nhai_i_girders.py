"""NHAI project precast I-girder midspan outlines (PSC and RCC).

Two NHAI project drawing sources are covered:

``Nh45aIGirderSection``
    NH 45-A Package II, *PKG II Modified Structural Drawings*
    (Feedback Infra for NHAI, March/November 2017, R0). Every sheet is
    stamped FINAL FEASIBILITY REPORT. These are proposal drawings for named
    structures, not an Indian national standard, and nothing here claims
    the girders were approved or built. Seven midspan outlines are exposed.
    ``PSC-*`` sizes are drawn as "PSC-I girder" (prestressed); ``RCC-*``
    sizes are drawn as "precast RCC I girder" (reinforced, not prestressed).
    Where two sizes share an identical outline, both remain separate SIZES
    entries and the identity is recorded in ``identical_to``.

``DelhiVadodaraPscISection``
    Delhi–Vadodara Expressway package II (Sohna–Firozpur Jhirka), Volume III,
    1 x 30 m PSC I-beam at km 37+744, PDF p41. The 1-bit scan makes the
    midspan web width illegible; 300 mm is a best estimate from scale
    measurement (288 +/- 26 mm). The whole profile is labelled ``estimate``.

All outlines use the same five-segment symmetric I: top flange edge,
straight top splay, vertical web, straight bottom splay, bottom flange edge.
Millimetres, origin at mid-soffit, y upwards. Gross concrete only: strands,
reinforcement, deck slab and the thickened end blocks are excluded.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.india")
        .joinpath("data/nhai_i_girders.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class NhaiIGirderDimensions:
    """Five-segment symmetric I outline, in millimetres.

    Vertical chain from the top: ``top_vertical`` flange edge,
    ``upper_splay_height``, ``web_height``, ``lower_splay_height`` and
    ``bottom_vertical``. These must add up to ``depth``.
    """

    depth: float
    top_width: float
    web_width: float
    bottom_width: float
    top_vertical: float
    upper_splay_height: float
    web_height: float
    lower_splay_height: float
    bottom_vertical: float

    def __post_init__(self) -> None:
        chain = (self.top_vertical + self.upper_splay_height + self.web_height
                 + self.lower_splay_height + self.bottom_vertical)
        if abs(chain - self.depth) > 1e-9:
            raise ValueError(f"vertical dimension chain {chain} does not close to depth {self.depth}")
        if not (self.web_width < self.top_width and self.web_width < self.bottom_width):
            raise ValueError("web must be narrower than both flanges")

    @property
    def upper_splay_width(self) -> float:
        """Horizontal extent of each top splay (flange edge to web face)."""
        return (self.top_width - self.web_width) / 2

    @property
    def lower_splay_width(self) -> float:
        """Horizontal extent of each bottom splay (flange edge to web face)."""
        return (self.bottom_width - self.web_width) / 2

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Anti-clockwise vertices of the gross section, starting at the left soffit corner."""
        b, w, t = self.bottom_width / 2, self.web_width / 2, self.top_width / 2
        y_lower = self.bottom_vertical + self.lower_splay_height
        y_upper = y_lower + self.web_height
        y_top_splay = y_upper + self.upper_splay_height
        return [(-b, 0.0), (b, 0.0), (b, self.bottom_vertical),
                (w, y_lower), (w, y_upper), (t, y_top_splay),
                (t, self.depth), (-t, self.depth), (-t, y_top_splay),
                (-w, y_upper), (-w, y_lower), (-b, self.bottom_vertical)]


_DIM_KEYS = ("depth", "top_width", "web_width", "bottom_width", "top_vertical",
             "upper_splay_height", "web_height", "lower_splay_height", "bottom_vertical")


class _NhaiIGirderBase:
    SIZES: tuple[str, ...] = ()
    _DATA_KEY = ""
    _DEFAULT = ""

    def __init__(self, size: str | None = None) -> None:
        size = self._DEFAULT if size is None else size
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()[self._DATA_KEY]
        row = next(r for r in data["sizes"] if r["size"] == size)
        self.size = size
        self.record = row
        self.dimensions = NhaiIGirderDimensions(**{k: float(row["dimensions_mm"][k]) for k in _DIM_KEYS})
        self.construction = row["construction"]
        self.prestressed = row["construction"] == "PSC"
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.identical_to = tuple(row.get("identical_to", ()))
        self.pdf_pages = tuple(loc["pdf_page"] for loc in row["locators"])

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """Return the gross concrete ``sectionproperties`` geometry."""
        return geometry_from_polygon(self.polygon)


class Nh45aIGirderSection(_NhaiIGirderBase):
    """NH 45-A Package II midspan I girders, PSC and precast RCC.

    ``PSC-1500``/``PSC-2000`` and ``RCC-2000``/``RCC-2250`` use the
    900/300/750 family; ``RCC-1300``/``1400``/``1500`` use 800/300/600.
    ``RCC-2000`` is outline-identical to ``PSC-2000`` and ``RCC-2250`` to
    :class:`~bridgebeams.india.Nh45aPscISection` (PDF p50).
    """

    SIZES = ("PSC-1500", "PSC-2000", "RCC-1300", "RCC-1400", "RCC-1500", "RCC-2000", "RCC-2250")
    _DATA_KEY = "nh45a_package_ii"
    _DEFAULT = "PSC-2000"


class DelhiVadodaraPscISection(_NhaiIGirderBase):
    """Delhi–Vadodara pkg II 30 m precast PSC I girder at km 37+744 (midspan).

    Best estimate: the web width (300 mm) is scaled from a 1-bit scan
    because the printed value is illegible. ``provenance == "estimate"``.
    """

    SIZES = ("KM37+744-MID",)
    _DATA_KEY = "delhi_vadodara_pkg_ii"
    _DEFAULT = "KM37+744-MID"


__all__ = ["NhaiIGirderDimensions", "Nh45aIGirderSection", "DelhiVadodaraPscISection"]
