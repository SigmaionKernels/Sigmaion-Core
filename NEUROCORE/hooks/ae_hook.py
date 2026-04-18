from observability.ol_core import ObservabilityLayer
import time

ol = ObservabilityLayer()


def ae_inject(fn):
    def wrapper(*args, **kwargs):
        trace_id = ol.emit("AE", "finalize_start")

        start = time.time()
        result = fn(*args, **kwargs)
        latency = (time.time() - start) * 1000

        ol.emit(
            module="AE",
            event="finalize_end",
            payload={"output": str(result)},
            latency_ms=latency,
            trace_id=trace_id
        )

        return result
    return wrapper