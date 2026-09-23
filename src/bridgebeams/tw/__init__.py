"""Taiwan Freeway Bureau precast post-tensioned concrete I girders."""

from .i_section import TaiwanIDimensions, TaiwanISection

__all__ = ["TaiwanIDimensions", "TaiwanISection"]

from .r2_thb_pci_girders import (ThbPciGirderDimensions, ThbPciGirderSection)
__all__ += ['ThbPciGirderDimensions', 'ThbPciGirderSection']
