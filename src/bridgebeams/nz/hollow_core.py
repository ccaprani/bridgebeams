"""NZTA RR364 hollow-core gross units, drawings S2.01, S2.10 and S3.01.

Source PDF pages 29/34/40. Single-core 650/900 inner units use octagonal
voids and 20 mm bottom chamfers; 587 uses the circular void and 15 mm
chamfer options. Single-core lower mould-release faces use the printed
1:80 (650) or 1.5:140 (900) slopes. The nominal geometry convention fixes
1138 mm maximum width at the 110 mm high key ledge and 1094 mm top width;
the drafted face runs from that ledge to the selected chamfer. Those
datums are an explicit interpretation, not a source-exact mold outline.
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
from ._sources import rr364_record


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

    # Chamfer option selected, recess derived, circular voids polygonised.
    provenance = "transcribed-with-convention"
    source_status = "NZTA RR364 standard drawings"

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
        if depth == 587:
            self.dimensions = NzHollowCoreDimensions()
        else:
            labels = self.source_record["dimensions"]
            draft = labels["mould_draft"]
            # Nominal key depth reconciles both printed overall widths and
            # the 12 mm upper joint chamfer; it is a calculated convention.
            key_depth = (labels["lower_width"] - labels["top_width"]) / 2 + 12
            self.dimensions = NzHollowCoreDimensions(
                depth=depth, width=labels["lower_width"], key_depth=key_depth,
                key_top_height=depth-labels["side_vertical_chain"][0],
                corner_chamfer=20, void_diameter=0, void_centre_height=0,
                lower_face_slope=draft["run"] / draft["rise"],
            )

    @property
    def source_record(self) -> dict | None:
        """Independent source evidence; the earlier 587 mm units were not rechecked."""
        if self.depth == 587:
            return None
        # Numeric SIZES validation also accepts integral floats; canonicalize
        # only the record key while retaining the public depth value.
        return rr364_record(f"hollow_core_{int(self.depth)}_{self.unit}")

    @property
    def geometry_conventions(self) -> tuple[str, ...]:
        record = self.source_record
        if record is not None:
            return tuple(record["geometry_conventions"])
        return ("Earlier 587 mm transcription retained without rechecking.",
                "Circular voids polygonised; 15 mm chamfers selected.",
                "Local holes and optional outer-unit drip groove omitted.")

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        if self.depth != 587:
            void = self.source_record["dimensions"]["void"]
            bottom = void["bottom_cover"]
            top = self.depth - void["top_cover"]
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
