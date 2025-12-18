from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from collections import defaultdict
from datetime import datetime, timedelta
from src.utils.logging import get_logger
from typing import Dict
import time

logger = get_logger(__name__)


class RateLimiter:
    """
    Simple in-memory rate limiter middleware
    Tracks requests by IP address and enforces rate limits
    """
    def __init__(self, requests_per_minute: int = 100):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)

    def is_allowed(self, request: Request) -> bool:
        """
        Check if a request is allowed based on rate limits
        """
        # Get client IP address
        client_ip = self._get_client_ip(request)

        # Get current time
        now = datetime.now()

        # Clean old requests (older than 1 minute)
        self._clean_old_requests(client_ip, now)

        # Check if limit is exceeded
        current_requests = len(self.requests[client_ip])
        is_allowed = current_requests < self.requests_per_minute

        # Log the request
        logger.debug(f"Rate limit check for {client_ip}: {current_requests}/{self.requests_per_minute} requests - {'ALLOWED' if is_allowed else 'BLOCKED'}")

        # Record this request if allowed
        if is_allowed:
            self.requests[client_ip].append(now)

        return is_allowed

    def _get_client_ip(self, request: Request) -> str:
        """
        Get the client IP address from the request
        """
        # Try to get IP from various headers first (in case of proxies)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip.strip()

        # Fall back to client host
        if request.client and request.client.host:
            return request.client.host

        # Default to localhost if no IP found
        return "127.0.0.1"

    def _clean_old_requests(self, client_ip: str, now: datetime):
        """
        Remove requests older than 1 minute
        """
        cutoff_time = now - timedelta(minutes=1)
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > cutoff_time
        ]

    def get_rate_limit_headers(self, request: Request) -> dict:
        """
        Get rate limit headers for response
        """
        client_ip = self._get_client_ip(request)
        current_requests = len(self.requests[client_ip])

        headers = {
            "X-RateLimit-Limit": str(self.requests_per_minute),
            "X-RateLimit-Remaining": str(max(0, self.requests_per_minute - current_requests)),
            "X-RateLimit-Reset": str(int((datetime.now() + timedelta(minutes=1)).timestamp()))
        }

        return headers


# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=100)