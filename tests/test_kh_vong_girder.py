"""Cambodian thesis PC I-girder (Vong Seng 2006)."""

import pytest

from bridgebeams.kh.vong_scc_girder import KhVongGirderSection


def test_geometry():
    s = KhVongGirderSection()
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == (-290, 0, 290, 850)
    assert p.area == pytest.approx(580 * 160 + (580 + 150) / 2 * 40 + 150 * 450 + (150 + 350) / 2 * 80 + 350 * 120)
    assert s.provenance == "transcribed"
    assert "thesis" in s.source_status
    assert s.geometry is not None


def test_invalid_size():
    with pytest.raises(ValueError):
        KhVongGirderSection("TB_14_f60")
