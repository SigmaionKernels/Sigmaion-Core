from observability.ol_core import ObservabilityLayer
import time

ol = ObservabilityLayer()


def vfs_inject(fn):
    def wrapper(*args, **kwargs):
        confidence = kwargs.get("confidence", 0.0)

        start = time.time()
        result = fn(*args, **kwargs)
        latency = (time.time() - start) * 1000

        ol.emit(
            module="VFS",
            event="validation",
            payload={"result": result, "confidence": confidence},
            status="ok" if result else "fail",
            latency_ms=latency
        )

        return result
    return wrapper