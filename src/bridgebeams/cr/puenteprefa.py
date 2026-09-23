"""PuentePrefa (Costa Rica) "Viga California" I-beams and "Simple te" T-beam.

Source: PuentePrefa Ltda, web page *Elementos prefabricados*
(https://www.puenteprefa.cr/elementos_prefabricados.html), product
diagrams ``elem_prefa_diag2.jpg`` (two "Viga california", 137 and 167 cm)
and ``elem_prefa_diag3.jpg`` ("Doble te", "Simple te"). The page states
the precast beams serve 4–40 m bridge spans. Dimensions in centimetres.

Viga California (I): printed depth 137/167, bottom width 48, bottom flange
edge 15, web 18 (the "15" callout is the bottom-flange overhang, 48 = 15
+ 18 + 15) and top-flange edge 8. The top width and both tapers are **not**
printed; they are scaled from the 600-px diagrams (drawn to a uniform
scale, 0.89–0.90 px/cm), so these two are ``"estimate"``.

Simple te (T): printed top width 93, flange 10, depth 97, stem 20 at the
flange and 11 at the soffit; modelled with a flat flange soffit and square
corners (``"transcribed-with-convention"``). The "Doble te" diagram (drawn
flange-down) is not implemented: its stem positions are not printed and
its bridge orientation is ambiguous.

Millimetres, origin at mid-soffit, y up. No section properties published.
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
        resources.files("bridgebeams.cr")
        .joinpath("data/puenteprefa_beams.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class PuentePrefaBeamDimensions:
    """Polygonal I or T outline in millimetres.

    For a T-beam set ``bottom_flange = bottom_taper = 0``; the web then
    tapers linearly from ``web_width`` (under the top flange) to
    ``web_bottom_width`` at the soffit.
    """

    depth: float
    top_width: float
    web_width: float
    top_flange: float
    top_taper: float = 0.0
    bottom_width: float = 0.0
    bottom_flange: float = 0.0
    bottom_taper: float = 0.0
    web_bottom_width: float = 0.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        D, xt, xw = self.depth, self.top_width / 2, self.web_width / 2
        if self.bottom_flange:
            xb = self.bottom_width / 2
            right = [
                (xb, 0.0),
                (xb, self.bottom_flange),
                (xw, self.bottom_flange + self.bottom_taper),
                (xw, D - self.top_flange - self.top_taper),
            ]
        else:
            right = [(self.web_bottom_width / 2, 0.0), (xw, D - self.top_flange - self.top_taper)]
        right += [(xt, D - self.top_flange), (xt, D)]
        return right + [(-x, y) for x, y in reversed(right)]


class PuentePrefaBeamSection:
    """PuentePrefa ``"CALIFORNIA-137"``, ``"CALIFORNIA-167"`` or ``"SIMPLE-TE-97"``.

    >>> PuentePrefaBeamSection("CALIFORNIA-167").dimensions.depth
    1670.0
    """

    SIZES = ("CALIFORNIA-137", "CALIFORNIA-167", "SIMPLE-TE-97")

    def __init__(self, size: str = "CALIFORNIA-167"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["types"][size]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = PuentePrefaBeamDimensions(
            **{k: 10.0 * float(v) for k, v in row["dimensions_cm"].items()}
        )

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline), sign=1.0)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["PuentePrefaBeamDimensions", "PuentePrefaBeamSection"]
