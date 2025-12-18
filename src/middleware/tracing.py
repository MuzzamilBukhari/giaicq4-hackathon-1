from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from src.utils.logging import get_logger
from src.utils.metrics import metrics_collector, QueryType
from typing import Optional, Dict, Any
from uuid import uuid4
from datetime import datetime
import time
import json


class TracingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for request tracing and performance monitoring
    """
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = get_logger(__name__)

    async def dispatch(self, request: Request, call_next):
        # Generate a unique request ID
        request_id = str(uuid4())

        # Add request ID to request state for use in handlers
        request.state.request_id = request_id

        # Log the incoming request
        start_time = time.time()
        self.logger.info(
            f"[{request_id}] {request.method} {request.url.path} - "
            f"IP: {self._get_client_ip(request)}, "
            f"User-Agent: {request.headers.get('user-agent', 'unknown')}"
        )

        try:
            # Process the request
            response = await call_next(request)

            # Calculate response time
            response_time = time.time() - start_time

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{response_time:.2f}ms"

            # Log the completed request
            self.logger.info(
                f"[{request_id}] Completed {request.method} {request.url.path} - "
                f"Status: {response.status_code}, "
                f"Response Time: {response_time:.2f}ms"
            )

            return response

        except Exception as e:
            # Calculate response time for error case
            response_time = time.time() - start_time

            # Log the error
            self.logger.error(
                f"[{request_id}] Error processing {request.method} {request.url.path} - "
                f"Error: {str(e)}, "
                f"Response Time: {response_time:.2f}ms"
            )

            # Re-raise the exception
            raise

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


def add_tracing_to_app(app):
    """
    Add tracing middleware to the FastAPI application
    """
    app.add_middleware(TracingMiddleware)


# Additional tracing utilities
class RequestTracer:
    """
    Utility class for more detailed request tracing within handlers
    """
    def __init__(self):
        self.logger = get_logger(__name__)

    def trace_step(self, request: Request, step_name: str, details: Optional[Dict[str, Any]] = None):
        """
        Trace a specific step in request processing
        """
        request_id = getattr(request.state, 'request_id', 'unknown')
        log_msg = f"[{request_id}] STEP: {step_name}"
        if details:
            log_msg += f" - Details: {details}"

        self.logger.debug(log_msg)

    def trace_event(self, request: Request, event_name: str, data: Optional[Dict[str, Any]] = None):
        """
        Trace a specific event during request processing
        """
        request_id = getattr(request.state, 'request_id', 'unknown')
        log_msg = f"[{request_id}] EVENT: {event_name}"
        if data:
            log_msg += f" - Data: {data}"

        self.logger.info(log_msg)


# Global tracer instance
request_tracer = RequestTracer()