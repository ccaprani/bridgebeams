"""NZTA RR364 hollow-core gross units, drawings S2.01, S2.10 and S3.01.

Source PDF pages 29/34/40. Single-core 650/900 inner units use octagonal
voids and 20 mm bottom chamfers; 587 uses the circular void and 15 mm
chamfer options. Single-core lower mould-release faces use the printed 1:80
slope, with 1138 mm maximum width at the 110 mm high key ledge.
The outer unit is oriented with the exposed edge on the left. Its optional
soffit drip groove is omitted from this gross section, as are local drain,
inspection and connection holes. The source prohibits isolated use of an
inner unit. The 650/900 outer units remain research transcriptions.
"""
from dataclasses import dataclass
from math import cos, sin, pi

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


@dataclass(frozen=True)
class NzHollowCoreDimensions:
    depth: float = 587
    width: float = 1144
    key_depth: float = 38
    key_top_chamfer: float = 12
    key_top_height: float = 430
    key_bottom_height: float = 110
    corner_chamfer: float = 15
    void_diameter: float = 368
    void_centre_height: float = 294
    lower_face_slope: float = 0

    def outline(self, unit: str) -> list[tuple[float, float]]:
        w, d, c = self.width, self.depth, self.corner_chamfer
        k, a = self.key_depth, self.key_top_chamfer
        # The lower face leans inward towards the soffit; width is fixed
        # at the key ledge. Corner offsets are measured from that face.
        dx = (self.key_bottom_height-c)*self.lower_face_slope
        r = [(w-dx-c, 0), (w-dx, c), (w, self.key_bottom_height),
             (w-k, self.key_bottom_height), (w-k, self.key_top_height-a),
             (w-k+a, self.key_top_height), (w-k+a, d)]
        if unit == 'inner':
            return r + [(w-x, y) for x, y in reversed(r)]
        return r + [(c, d), (0, d-c), (0, c), (c, 0)]


class NzHollowCoreSection:
    """Single 650/900 inner or double 587 inner/outer gross unit.

    Circular voids use ``circle_points`` equally spaced vertices, default
    256 per circle. Set a multiple of four >=32. Their analytic nominal
    diameter is 368 mm; the polygon approximation slightly overstates
    concrete area. Outer-unit drip groove is excluded explicitly.
    """
    UNITS = ('inner', 'outer')
    SIZES = (587, 650, 900)

    def __init__(self, depth: int = 587, unit: str = 'inner', circle_points: int = 256):
        if depth not in self.SIZES:
            raise ValueError(f'depth must be one of {self.SIZES}')
        if unit not in self.UNITS:
            raise ValueError(f'unit must be one of {self.UNITS}, got {unit!r}')
        if depth != 587 and unit != 'inner':
            raise ValueError('650/900 outer unit dimension endpoints remain unresolved')
        if isinstance(circle_points, bool) or not isinstance(circle_points, int) or circle_points < 32 or circle_points % 4:
            raise ValueError('circle_points must be a multiple of four, >=32')
        self.depth, self.unit, self.circle_points = depth, unit, circle_points
        self.dimensions = (NzHollowCoreDimensions() if depth == 587 else
                           NzHollowCoreDimensions(depth=depth, width=1138,
                               key_depth=34, key_top_height=430,
                               corner_chamfer=20, void_diameter=0,
                               void_centre_height=0, lower_face_slope=1/80))

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        if self.depth != 587:
            bottom = 130 if self.depth == 650 else 155
            top = self.depth - 140
            # 154 + 100 + 630 + 100 + 154 = 1138 mm, directly from source.
            hole = [(254, bottom), (884, bottom), (984, bottom+100),
                    (984, top-100), (884, top), (254, top),
                    (154, top-100), (154, bottom+100)]
            return orient(Polygon(d.outline(self.unit), [hole]), sign=1)
        centres = (308, 836) if self.unit == 'inner' else (836,)
        holes = [[(x+d.void_diameter/2*cos(2*pi*i/self.circle_points),
                   d.void_centre_height+d.void_diameter/2*sin(2*pi*i/self.circle_points))
                  for i in range(self.circle_points)] for x in centres]
        return orient(Polygon(d.outline(self.unit), holes), sign=1)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ['NzHollowCoreDimensions', 'NzHollowCoreSection']
