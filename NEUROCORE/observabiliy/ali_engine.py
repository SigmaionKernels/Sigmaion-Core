class ALIEngine:
    def compute(self, confidence, latency, divergence, vfs_score):
        return (
            confidence * 3 +
            (1 - min(latency / 1000, 1)) * 2 +
            (1 - divergence) * 3 +
            vfs_score * 2
        )


def ali_status(ali):
    if ali >= 10:
        return "EMERGENCY_HALT"
    elif ali >= 5:
        return "UNSTABLE"
    elif ali >= 2:
        return "WARNING"
    return "STABLE"