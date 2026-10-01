"""Precast prestressed I longarina of the São Domingos Creek bridge (ES-010, Brazil).

Source: R. J. C. Nóbrega and E. G. Ferreira (IFES), "Análise comparativa das
normas NBR 6118/2014, NBR 7188/2013 e AASHTO LRFD 2012, baseada na teoria
da confiabilidade – estudo de caso de uma viga I da ponte sobre Córrego São
Domingos na rodovia estadual ES-010, trecho Itaúnas - ES-421", Capítulo 2
of *Engenharias: pesquisa, desenvolvimento e inovação* (Atena Editora,
2023, doi:10.22533/at.ed.3592318012), Figura 7 "Seção transversal da viga
principal (longarina)" reproduced from the 2016 project drawings (PDF p33).

Project-specific (not a standard): 20.10 m span, six girders at 2.40 m
under an 18 cm slab. Drawing units are centimetres; this module returns
millimetres, origin mid-soffit, y up. The lifting-loop block drawn above
the top flange is excluded.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.br")
        .joinpath("data/r3_ifes_sao_domingos.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class SaoDomingosLongarinaDimensions:
    """Figura 7 dimensions in millimetres."""

    depth: float
    top_width: float
    top_flange: float
    top_taper: float
    web_width: float
    web_height: float
    bottom_taper: float
    bottom_flange: float
    bottom_width: float

    @property
    def outline(self) -> list[tuple[float, float]]:
        xt, xw, xb, D = self.top_width / 2, self.web_width / 2, self.bottom_width / 2, self.depth
        right = [
            (xb, 0.0),
            (xb, self.bottom_flange),
            (xw, self.bottom_flange + self.bottom_taper),
            (xw, D - self.top_flange - self.top_taper),
            (xt, D - self.top_flange),
            (xt, D),
        ]
        return right + [(-x, y) for x, y in reversed(right)]


class SaoDomingosLongarinaSection:
    """São Domingos bridge (ES-010) 1.30 m precast prestressed I girder.

    >>> SaoDomingosLongarinaSection().polygon.bounds
    (-300.0, 0.0, 300.0, 1300.0)
    """

    SIZES = ("SD-130",)

    def __init__(self, size: str = "SD-130"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        self.size = size
        self.published = data["published"]
        self.provenance = data["sizes"][size]["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = SaoDomingosLongarinaDimensions(
            **{k: 10.0 * float(v) for k, v in data["dimensions_cm"].items()}
        )

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline), sign=1.0)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["SaoDomingosLongarinaDimensions", "SaoDomingosLongarinaSection"]
