import time
import uuid
import json
from collections import deque


class ObservabilityLayer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ObservabilityLayer, cls).__new__(cls)
            cls._instance.buffer = deque(maxlen=1000)
            cls._instance.log_file = "ol_stream.ndjson"
        return cls._instance

    def emit(self, module, event, payload=None, status="ok", latency_ms=0.0, trace_id=None):
        trace_id = trace_id or str(uuid.uuid4())

        record = {
            "ts": time.time(),
            "module": module,
            "event": event,
            "payload": payload or {},
            "status": status,
            "latency_ms": latency_ms,
            "trace_id": trace_id
        }

        self.buffer.append(record)

        with open(self.log_file, "a") as f:
            f.write(json.dumps(record) + "\n")

        return trace_id