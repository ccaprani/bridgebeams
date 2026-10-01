"""Spanish MOPU 1977 "Colección de vigas tipo HP-1" doble T girders, Types I–VI.

Source: Orden de 9 de febrero de 1977, «Obras de Paso de Carreteras.
Colección de tramos con vigas pretensadas. Tipo HP 1», BOE núm. 118,
18 mayo 1977, pp. 10886–10915. SECCION I-I on each formwork sheet
("VIGA TIPO n – ENCOFRADOS Y ARMADURAS PASIVAS"), PDF pp 6/9/13/17/20/24.

This is a historic 1977 standard (use declared non-obligatory; later
annulment reported but not audited). Only the midspan ("sección central")
gross concrete section is modelled: straight-line outline, no fillets,
end blocks and riostras excluded. Source dimensions are metres; the
section is in millimetres, origin at mid-soffit, y upwards.

Validated against the "Mediciones – sección central" concrete m³/m and
formwork (molde) m²/m printed on each sheet; no centroid or inertia is
published.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.es")
        .joinpath("data/hp1_beams.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class Hp1BeamDimensions:
    """SECCION I-I dimensions in millimetres (source metres × 1000)."""

    depth: float
    top_width: float
    web_width: float
    bottom_width: float
    top_edge_height: float
    top_splay_height: float
    web_height: float
    bottom_splay_height: float
    bottom_edge_height: float

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Right half from the soffit corner to the top corner."""
        y1 = self.bottom_edge_height
        y2 = y1 + self.bottom_splay_height
        y3 = y2 + self.web_height
        y4 = y3 + self.top_splay_height
        return [
            (self.bottom_width / 2, 0.0),
            (self.bottom_width / 2, y1),
            (self.web_width / 2, y2),
            (self.web_width / 2, y3),
            (self.top_width / 2, y4),
            (self.top_width / 2, self.depth),
        ]


class Hp1BeamSection:
    """HP-1 "viga tipo" I–VI midspan gross concrete section (historic, 1977).

    Examples
    --------
    >>> from bridgebeams.es import Hp1BeamSection
    >>> Hp1BeamSection("III").dimensions.depth
    1700.0
    """

    SIZES = ("I", "II", "III", "IV", "V", "VI")
    source_status = "historic 1977 standard"

    def __init__(self, size: str = "III"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sections"][size]
        self.size = size
        self.name_original = f"Viga tipo {size} (HP-1)"
        self.published = row
        self.provenance = row.get("provenance", data["provenance"])
        self.dimensions = Hp1BeamDimensions(
            **{k: round(float(v) * 1000.0, 6) for k, v in row["dimensions_m"].items()}
        )
        d = self.dimensions
        chain = (d.top_edge_height + d.top_splay_height + d.web_height
                 + d.bottom_splay_height + d.bottom_edge_height)
        if abs(chain - d.depth) > 1e-6:
            raise ValueError(f"HP-1 {size}: vertical chain {chain} != depth {d.depth}")

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.outline)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["Hp1BeamDimensions", "Hp1BeamSection"]
