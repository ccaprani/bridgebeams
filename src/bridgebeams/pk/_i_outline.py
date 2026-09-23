"""Five-segment symmetric I outline helper (private to ``bridgebeams.pk``)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FiveSegmentIDimensions:
    """Symmetric I outline with straight splays, in millimetres.

    Vertical chain from the soffit: ``bottom_edge`` (vertical bottom-flange
    side), ``bottom_splay`` (straight taper to the web), ``web_height``
    (clear web), ``top_splay`` (straight taper to the flange underside) and
    ``top_edge`` (vertical top-flange side). The chain must close to
    ``depth``.
    """

    depth: float
    top_width: float
    web_width: float
    bottom_width: float
    top_edge: float
    top_splay: float
    web_height: float
    bottom_splay: float
    bottom_edge: float

    def __post_init__(self) -> None:
        chain = (self.top_edge + self.top_splay + self.web_height
                 + self.bottom_splay + self.bottom_edge)
        if abs(chain - self.depth) > 1e-6:
            raise ValueError(
                f"vertical chain {chain} does not close to depth {self.depth}")

    @property
    def right_half(self) -> list[tuple[float, float]]:
        """Right-half vertices from the soffit corner to the top corner."""
        b, w, t = self.bottom_width / 2, self.web_width / 2, self.top_width / 2
        y1 = self.bottom_edge
        y2 = y1 + self.bottom_splay
        y3 = y2 + self.web_height
        y4 = y3 + self.top_splay
        return [(b, 0.0), (b, y1), (w, y2), (w, y3), (t, y4), (t, self.depth)]
