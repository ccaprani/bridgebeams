"""Validation of U/SU, TY/TYE and SY/SYE families against published tables,
plus M/UMB."""

import json
from importlib import resources

import pytest

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.ukie import (
    IeMBeamSection,
    IeSYBeamSection,
    IeSYEBeamSection,
    IeTYBeamSection,
    IeUMBBeamSection,
    IeUBeamSection,
)

U_DATA = json.loads(
    resources.files("bridgebeams.ukie.data").joinpath("ie_u_beam.json").read_text()
)
TY_DATA = json.loads(
    resources.files("bridgebeams.ukie.data").joinpath("ie_ty_beam.json").read_text()
)
SY_DATA = json.loads(
    resources.files("bridgebeams.ukie.data").joinpath("ie_sy_beam.json").read_text()
)
M_DATA = json.loads(
    resources.files("bridgebeams.ukie.data").joinpath("ie_m_beam.json").read_text()
)

TOL_EXACT = {"area": 0.005, "yc": 0.005, "ixx": 0.005}
TOL_M = {"area": 0.01, "yc": 0.01, "ixx": 0.01}


def test_u_family_all_sizes():
    for row in U_DATA["published_properties"]:
        beam = IeUBeamSection(row["section"])
        props = section_properties(as_polygon(beam.geometry))
        assert props["area"] == pytest.approx(row["area"], rel=0.004), row["section"]
        assert props["cy"] == pytest.approx(row["yc"], rel=0.004), row["section"]
        assert props["ixx"] == pytest.approx(row["ixx_e9"] * 1e9, rel=0.004), row["section"]


def test_u_invalid_size_raises():
    with pytest.raises(ValueError):
        IeUBeamSection("U2")


@pytest.mark.parametrize("variant,edge,key", [
    ("bs", False, "ty_bs"),
    ("ss", False, "ty_ss"),
    ("bs", True, "tye_bs"),
    ("ss", True, "tye_ss"),
])
def test_ty_family_all_sizes(variant, edge, key):
    for row in TY_DATA["published_properties"][key]:
        size = row["section"]
        beam = IeTYBeamSection(size, variant=variant)
        props = section_properties(as_polygon(beam.geometry))
        assert props["area"] == pytest.approx(row["area"], rel=0.001), size
        assert props["cy"] == pytest.approx(row["yc"], rel=0.001), size
        assert props["ixx"] == pytest.approx(row["ixx_e9"] * 1e9, rel=0.001), size
        if edge:
            xc = props["cx"] + 375.0
            assert xc == pytest.approx(row["xc"], rel=0.01), size


def test_ty_invalid_size_raises():
    with pytest.raises(ValueError):
        IeTYBeamSection("TY1", variant="bs")  # bs starts at TY3
    with pytest.raises(ValueError):
        IeTYBeamSection("TY12", variant="ss")


def test_sy_family_all_sizes():
    for row in SY_DATA["published_properties"]["sy"]:
        beam = IeSYBeamSection(row["section"])
        props = section_properties(as_polygon(beam.geometry))
        assert props["area"] == pytest.approx(row["area"], rel=0.001), row["section"]
        assert props["cy"] == pytest.approx(row["yc"], rel=0.001), row["section"]
        assert props["ixx"] == pytest.approx(row["ixx_e9"] * 1e9, rel=0.001), row["section"]


def test_sye_family_all_sizes():
    # fitted family: max deviation 1.2%
    for row in SY_DATA["published_properties"]["sye"]:
        beam = IeSYEBeamSection(row["section"])
        poly = as_polygon(beam.geometry)
        assert poly.is_valid, row["section"]
        props = section_properties(poly)
        assert props["area"] == pytest.approx(row["area"], rel=0.015), row["section"]
        assert props["cy"] == pytest.approx(row["yc"], rel=0.015), row["section"]
        assert props["ixx"] == pytest.approx(row["ixx_e9"] * 1e9, rel=0.015), row["section"]
        xc = props["cx"] + 375.0
        assert xc == pytest.approx(row["xc"], rel=0.02), row["section"]


def test_m_family_all_sizes():
    for row in M_DATA["published_properties"]["m"]:
        beam = IeMBeamSection(row["section"])
        props = section_properties(as_polygon(beam.geometry))
        assert props["area"] == pytest.approx(row["area"], rel=TOL_M["area"]), row["section"]
        assert props["cy"] == pytest.approx(row["yc"], rel=TOL_M["yc"]), row["section"]
        assert props["ixx"] == pytest.approx(row["ixx_e9"] * 1e9, rel=TOL_M["ixx"]), row["section"]


def test_umb_family_all_sizes():
    for row in M_DATA["published_properties"]["umb"]:
        beam = IeUMBBeamSection(row["section"])
        props = section_properties(as_polygon(beam.geometry))
        assert props["area"] == pytest.approx(row["area"], rel=0.007), row["section"]
        assert props["cy"] == pytest.approx(row["yc"], rel=0.007), row["section"]
        assert props["ixx"] == pytest.approx(row["ixx_e9"] * 1e9, rel=0.007), row["section"]


def test_m_umb_invalid_size_raises():
    with pytest.raises(ValueError):
        IeMBeamSection("M11")
    with pytest.raises(ValueError):
        IeUMBBeamSection("UMB11")


def test_sy_invalid_size_raises():
    with pytest.raises(ValueError):
        IeSYBeamSection("SY7")
