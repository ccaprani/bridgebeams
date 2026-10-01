"""Norwegian V426 NTB/KTB gross precast profiles, millimetres.

The 15 x 15 mm bottom chamfers are Colin Caprani's 2026-09-22 visual
interpretation of projected drawing leaders, not printed dimensions.
All other profile dimensions are read from Figure 3.3.2(a-j), pp37-46.
Recesses remain unfilled; reinforcement, deck and end details are omitted.
NTB origin is the soffit centre; KTB origin is the nominal left soffit
corner before chamfering. KTB1400 has its top left corner at x=-30.
"""
from dataclasses import dataclass
import json
from pathlib import Path

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon

_DATA = json.loads((Path(__file__).parent / 'data' / 'ntb_ktb.json').read_text())


@dataclass(frozen=True)
class NoNtbKtbDimensions:
    depth: float
    bottom_width: float
    top_width: float
    web_width: float
    bottom_web_height: float
    shoulder_height: float
    top_flange_height: float
    top_haunch_height: float
    left_top_offset: float = 0
    bottom_chamfer: float = 15
    top_rebate: float = 30
    bottom_rebate_height: float = 40
    bottom_rebate_top_width: float = 15
    bottom_rebate_bottom_width: float = 20

    def outline(self, family: str) -> list[tuple[float, float]]:
        symmetric = family == 'NTB'
        b = self.bottom_width / 2 if symmetric else self.bottom_width
        w = self.web_width / 2 if symmetric else self.web_width
        t = self.top_width / 2 if symmetric else self.top_width + self.left_top_offset
        d, c, s = self.depth, self.bottom_chamfer, self.shoulder_height
        r = [(b-c, 0), (b, c), (b, s-self.bottom_rebate_height),
             (b-self.bottom_rebate_bottom_width, s-self.bottom_rebate_height),
             (b-self.bottom_rebate_top_width, s), (w, self.bottom_web_height)]
        if self.top_flange_height:
            r += [(w, d-self.top_flange_height-self.top_haunch_height),
                  (t, d-self.top_flange_height)]
        r += [(t, d-self.top_rebate), (t-self.top_rebate, d-self.top_rebate),
              (t-self.top_rebate, d)]
        if symmetric:
            return r + [(-x, y) for x, y in reversed(r)]
        return r + [(self.left_top_offset, d),
                    (self.left_top_offset*c/d, c), (c, 0)]


class NoNtbKtbSection:
    """Five NTB and five KTB reconstructed gross profiles from V426.

    Bottom chamfers use the explicitly recorded user interpretation.
    This is not a certified production/formwork geometry.
    """
    TYPES = tuple(_DATA['sections'])

    # 15 x 15 mm bottom chamfers are a reviewer inference, not printed.
    provenance = "transcribed-with-convention"
    source_status = "Statens vegvesen V426 handbook figures"

    def __init__(self, section_type: str = 'NTB800-400x1400'):
        if section_type not in self.TYPES:
            raise ValueError(f'section_type must be one of {self.TYPES}, got {section_type!r}')
        self.section_type = section_type
        row = _DATA['sections'][section_type]
        self.family = row['family']
        self.dimensions = NoNtbKtbDimensions(**row['dimensions_mm'])

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline(self.family)), sign=1)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ['NoNtbKtbDimensions', 'NoNtbKtbSection']
