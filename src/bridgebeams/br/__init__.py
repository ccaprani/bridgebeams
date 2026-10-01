"""Brazilian precast bridge beams (DNIT federal standard album)."""

from .dnit_pcp import DnitPcpLongarinaDimensions, DnitPcpLongarinaSection

__all__ = ["DnitPcpLongarinaDimensions", "DnitPcpLongarinaSection"]

from .r3_ifes_sao_domingos import (SaoDomingosLongarinaDimensions, SaoDomingosLongarinaSection)
__all__ += ['SaoDomingosLongarinaDimensions', 'SaoDomingosLongarinaSection']
