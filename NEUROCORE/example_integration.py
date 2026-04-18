from observability.ali_engine import ALIEngine, ali_status
from core_patch import apply_patches


# MOCK SYSTEM
class VFS:
    def validate(self, data, confidence=0.0):
        return confidence > 0.5


def MSP(x):
    return x * 2


def AE(x):
    return x + 1


def GMS(task):
    return f"processed {task}"


# APPLY PATCHES
MSP, AE, GMS, VFS = apply_patches(MSP, AE, GMS, VFS)


# RUN FLOW
vfs = VFS()
ali_engine = ALIEngine()

valid = vfs.validate("data", confidence=0.7)

msp_out = MSP(10)
ae_out = AE(msp_out)
gms_out = GMS("task")

ali = ali_engine.compute(
    confidence=0.7,
    latency=120,
    divergence=0.1,
    vfs_score=0.8
)

print(valid, msp_out, ae_out, gms_out, ali_status(ali))