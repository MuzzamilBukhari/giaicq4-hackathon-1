import time
from collections import defaultdict, deque
from typing import Dict
import logging


class RateLimiter:
    def __init__(self, max_requests: int = 10, window_size: int = 60):
        """
        Initialize rate limiter
        :param max_requests: Maximum number of requests allowed per window
        :param window_size: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests: Dict[str, deque] = defaultdict(deque)

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from the given identifier is allowed
        :param identifier: Unique identifier for the client (e.g., IP address)
        :return: True if request is allowed, False otherwise
        """
        current_time = time.time()

        # Remove old requests outside the window
        while (self.requests[identifier] and
               current_time - self.requests[identifier][0] > self.window_size):
            self.requests[identifier].popleft()

        # Check if we're under the limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(current_time)
            return True

        # Rate limit exceeded
        logging.warning(f"Rate limit exceeded for {identifier}")
        return False

    def get_reset_time(self, identifier: str) -> float:
        """
        Get the time when the rate limit will reset for this identifier
        """
        if not self.requests[identifier]:
            return 0

        # The reset time is the oldest request time + window_size
        oldest_request = self.requests[identifier][0]
        return oldest_request + self.window_size


# Global rate limiter instance
# Default: 10 requests per minute per IP
rate_limiter = RateLimiter(max_requests=10, window_size=60)