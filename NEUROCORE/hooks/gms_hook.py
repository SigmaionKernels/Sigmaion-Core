from observability.ol_core import ObservabilityLayer

ol = ObservabilityLayer()


def gms_inject(fn):
    def wrapper(task, *args, **kwargs):
        trace_id = ol.emit("GMS", "dispatch", {"task": str(task)})

        result = fn(task, *args, **kwargs)

        ol.emit(
            module="GMS",
            event="dispatch_end",
            payload={"result": str(result)},
            trace_id=trace_id
        )

        return result
    return wrapper