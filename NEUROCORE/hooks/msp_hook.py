from observability.ol_core import ObservabilityLayer
import time

ol = ObservabilityLayer()


def msp_inject(fn):
    def wrapper(*args, **kwargs):
        trace_id = ol.emit("MSP", "stage_start", {"args": str(args)})

        start = time.time()
        result = fn(*args, **kwargs)
        latency = (time.time() - start) * 1000

        ol.emit(
            module="MSP",
            event="stage_end",
            payload={"result": str(result)},
            latency_ms=latency,
            trace_id=trace_id
        )

        return result
    return wrapper