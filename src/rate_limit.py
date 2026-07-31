"""Simple in-memory rate limiter for API abuse protection."""

from __future__ import annotations

import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self, max_calls: int, window_seconds: float) -> None:
        self.max_calls = max_calls
        self.window = window_seconds
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        bucket = self._hits[key]
        while bucket and now - bucket[0] > self.window:
            bucket.popleft()
        if len(bucket) >= self.max_calls:
            return False
        bucket.append(now)
        return True


# Per-IP style keys; callers pass user_id or IP.
assistant_limiter = RateLimiter(max_calls=30, window_seconds=60)
billing_limiter = RateLimiter(max_calls=10, window_seconds=60)
upload_limiter = RateLimiter(max_calls=15, window_seconds=60)
