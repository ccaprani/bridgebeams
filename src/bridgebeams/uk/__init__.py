"""United Kingdom standard precast bridge beam sections.

The historic UK families (CBDG standard beams: inverted-T, M, I and box,
from the Prestressed Concrete Bridge Development Group tradition) are the
ancestors of the Irish ranges implemented in :mod:`bridgebeams.ie` and
are planned here, with sources collected in the repository's
``sources/`` registry.

Shared geometry backends for UK and Irish sections live in
:mod:`bridgebeams._geometry` (and, where a shape serves both markets,
the Irish module's builder is reused by the UK wrapper).
"""

__all__: list[str] = []
