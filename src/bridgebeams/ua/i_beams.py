"""Ukrainian precast prestressed bridge I-beams.

Three families, all millimetres, origin at mid-soffit, y upwards:

* :class:`UaB40BeamSection` -- "Б L.H.40" beams (ТОВ «Мост Строй Комплект»,
  after the ДерждорНДІ 2012 album) as reproduced in the NIDI 2022
  rebuilding recommendations, section 3.3.5 (pp45-61). Fully dimensioned
  incl. R40/R50 fillets.
* :class:`ThreeBetBeamSection` -- 3Bet-90 / 3Bet-120 («3 Бетони», Kalush):
  NIDI section 3.3.6 drawings, validated against the producer's published
  concrete volumes.
* :class:`UaBmBeamSection` -- БМ-24 / БМ-33 (Kovalska / Darnytsia ZBK),
  detailed from the identical Oberbeton parametric section (R100 fillets).

All source locators, transcriptions and conventions are in
``data/ua_beams.json``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile
from bridgebeams.hu._fillet import fillet_polyline


@lru_cache(maxsize=1)
def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ua").joinpath("data/ua_beams.json").read_text(encoding="utf-8")
    )


def _polygon(half: tuple[tuple[float, float, float], ...]) -> Polygon:
    return polygon_from_half_profile(fillet_polyline(list(half), segments=16))


@dataclass(frozen=True)
class UaBeamDimensions:
    """Key printed dimensions (mm) plus the right-half vertex list.

    ``half_profile`` runs from the soffit corner to the top-centre edge as
    ``(x, y, fillet_radius)``; radius 0 is a sharp corner.
    """

    depth: float
    top_width: float
    bottom_width: float
    web_width_min: float
    half_profile: tuple[tuple[float, float, float], ...]


class _UaBeamBase:
    SIZES: tuple[str, ...] = ()
    _family = ""

    def _check(self, size: str) -> dict:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        self.size = size
        return _load_data()["families"][self._family]

    @property
    def polygon(self) -> Polygon:
        return _polygon(self.dimensions.half_profile)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


class UaB40BeamSection(_UaBeamBase):
    """"Б L.H.40" I-beam (NIDI 2022 §3.3.5, ДерждорНДІ 2012 album).

    Sizes are the source designations (length cm . depth cm . top width cm).
    12/15 m share the 1000 mm section and 18/21/24 m the 1100 mm section.

    >>> UaB40BeamSection("B3300.120.40").dimensions.depth
    1200.0
    """

    SIZES = ("B1200.100.40", "B1500.100.40", "B1800.110.40",
             "B2100.110.40", "B2400.110.40", "B3300.120.40")
    _family = "B40"
    provenance = "transcribed"
    source_status = "national rebuilding recommendations 2022 (reproduces ДерждорНДІ 2012 album)"

    def __init__(self, size: str = "B1800.110.40"):
        fam = self._check(size)
        row = fam["sizes"][size]
        self.published = row
        self.length = row["length_m"] * 1000.0
        h = float(row["depth"])
        # bottom-flange/haunch vertex from the facade chain (75/175/275); the
        # section chain 20 + f + R40 tangent length (19.0) agrees within 0.1 mm
        yb = h - 925.0
        half = (
            (230.0, 0.0, 0.0),
            (250.0, 20.0, 0.0),
            (250.0, yb, 40.0),
            (90.0, yb + 130.0, 40.0),
            (90.0, h - 240.0, 50.0),
            (200.0, h - 150.0, 40.0),
            (200.0, h, 0.0),
        )
        self.dimensions = UaBeamDimensions(h, 400.0, 500.0, 180.0, half)


class ThreeBetBeamSection(_UaBeamBase):
    """3Bet-90 (H 900) / 3Bet-120 (H 1200) I-beam, one entry per catalogued length.

    ``published_volume`` is the producer's concrete volume (m3) for the size.

    >>> ThreeBetBeamSection("3Bet-120-33").type
    '3Bet-120'
    """

    SIZES = ("3Bet-90-12", "3Bet-90-15", "3Bet-90-18", "3Bet-90-21", "3Bet-90-24",
             "3Bet-120-24", "3Bet-120-27", "3Bet-120-30", "3Bet-120-33")
    _family = "3Bet"
    source_status = "producer leaflet (Ukravtodor-approved 2008) + national rebuilding recommendations 2022"

    def __init__(self, size: str = "3Bet-90-18"):
        fam = self._check(size)
        row = fam["sizes"][size]
        typ = fam["types"][row["type"]]
        self.type = row["type"]
        self.published = row
        self.provenance = typ["provenance"]
        self.length = row["length_m"] * 1000.0
        self.published_volume = row["volume_m3"]
        half = tuple(tuple(float(v) for v in p) for p in typ["half_profile_mm"])
        xs = [p[0] for p in half]
        web_min = 2 * min(p[0] for p in half if 0 < p[1] < typ["depth"] - 200)
        self.dimensions = UaBeamDimensions(
            float(typ["depth"]), 2 * max(xs), 2 * half[0][0], web_min, half
        )


class UaBmBeamSection(_UaBeamBase):
    """БМ-24 (H 1100) / БМ-33 (H 1500) I-beam (Kovalska; = Oberbeton section).

    >>> UaBmBeamSection("BM-33").dimensions.depth
    1500.0
    """

    SIZES = ("BM-24", "BM-33")
    _family = "BM"
    provenance = "transcribed-with-convention"
    source_status = "producer catalogues (Kovalska 2020; Oberbeton 2017)"

    def __init__(self, size: str = "BM-24"):
        fam = self._check(size)
        row = fam["sizes"][size]
        self.published = row
        h = float(row["depth"])
        half = (
            (220.0, 0.0, 0.0),
            (240.0, 20.0, 0.0),
            (240.0, 153.0, 0.0),
            (80.0, 313.0, 100.0),
            (80.0, h - 320.0, 100.0),
            (300.0, h - 100.0, 0.0),
            (300.0, h - 45.0, 0.0),
            (240.0, h - 40.0, 0.0),
            (240.0, h, 0.0),
        )
        self.dimensions = UaBeamDimensions(h, 600.0, 480.0, 160.0, half)


__all__ = ["UaBeamDimensions", "UaB40BeamSection", "ThreeBetBeamSection", "UaBmBeamSection"]
