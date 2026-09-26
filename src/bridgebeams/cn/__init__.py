"""Chinese precast bridge sections."""

from .beijing_box import Beijing20bgql2BoxDimensions, Beijing20bgql2BoxSection

__all__ = ["Beijing20bgql2BoxDimensions", "Beijing20bgql2BoxSection"]

from .r2_shanghai_hollow_slab import (ShanghaiHingedHollowSlabDimensions, ShanghaiHingedHollowSlabSection, ShanghaiRigidHollowSlabDimensions, ShanghaiRigidHollowSlabSection)
__all__ += ['ShanghaiHingedHollowSlabDimensions', 'ShanghaiHingedHollowSlabSection', 'ShanghaiRigidHollowSlabDimensions', 'ShanghaiRigidHollowSlabSection']
