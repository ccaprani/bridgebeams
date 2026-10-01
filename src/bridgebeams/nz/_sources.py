"""Packaged provenance for the rechecked NZTA RR364 sections."""

from copy import deepcopy
from functools import lru_cache
from importlib import resources
import json


@lru_cache(maxsize=1)
def _load_rr364() -> dict:
    return json.loads(
        resources.files("bridgebeams.nz")
        .joinpath("data/nzta_rr364_verified_dimensions.json")
        .read_text(encoding="utf-8")
    )


def rr364_record(profile: str) -> dict:
    """Return an independent record, including its original PDF locator.

    The registry also retains partial outer-unit dimensions, without making
    them constructible sections. Copies protect the cached source records
    from caller mutation.
    """
    data = _load_rr364()
    return deepcopy({"source": data["source"], **data["profiles"][profile]})
