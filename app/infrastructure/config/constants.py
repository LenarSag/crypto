from datetime import timedelta

CIRCUIT_BREAKER_FAIL_MAX = 5
CIRCUIT_BREAKER_RESET_TIMEOUT = timedelta(seconds=60)  # in seconds
