from hooks.msp_hook import msp_inject
from hooks.ae_hook import ae_inject
from hooks.gms_hook import gms_inject
from observability.vfs_hooks import vfs_inject


# QUI agganci il tuo sistema reale

def apply_patches(MSP, AE, GMS, VFS):

    MSP = msp_inject(MSP)
    AE = ae_inject(AE)
    GMS = gms_inject(GMS)

    VFS.validate = vfs_inject(VFS.validate)

    return MSP, AE, GMS, VFS