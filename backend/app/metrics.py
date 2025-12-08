import time
from collections import deque, defaultdict
from typing import Dict, List
import threading
import logging


class PerformanceMonitor:
    def __init__(self, max_samples: int = 1000):
        """
        Initialize performance monitor
        :param max_samples: Maximum number of samples to keep for metrics calculation
        """
        self.max_samples = max_samples
        self.latencies = deque(maxlen=max_samples)
        self.success_count = 0
        self.error_count = 0
        self.lock = threading.Lock()  # Thread-safe operations

    def record_request(self, latency_ms: float, success: bool = True):
        """
        Record a request for metrics tracking
        :param latency_ms: Request latency in milliseconds
        :param success: Whether the request was successful
        """
        with self.lock:
            self.latencies.append(latency_ms)
            if success:
                self.success_count += 1
            else:
                self.error_count += 1

    def get_metrics(self) -> Dict[str, float]:
        """
        Get current performance metrics
        """
        with self.lock:
            if not self.latencies:
                return {
                    "avg_latency_ms": 0.0,
                    "p50_latency_ms": 0.0,
                    "p95_latency_ms": 0.0,
                    "p99_latency_ms": 0.0,
                    "success_rate": 0.0,
                    "total_requests": 0,
                    "success_count": 0,
                    "error_count": 0
                }

            # Calculate average latency
            avg_latency = sum(self.latencies) / len(self.latencies)

            # Calculate percentiles (simplified approach)
            sorted_latencies = sorted(self.latencies)
            n = len(sorted_latencies)

            p50_idx = int(0.50 * n)
            p95_idx = int(0.95 * n)
            p99_idx = int(0.99 * n)

            total_requests = self.success_count + self.error_count
            success_rate = (self.success_count / total_requests) * 100 if total_requests > 0 else 0

            return {
                "avg_latency_ms": avg_latency,
                "p50_latency_ms": sorted_latencies[min(p50_idx, n-1)] if n > 0 else 0,
                "p95_latency_ms": sorted_latencies[min(p95_idx, n-1)] if n > 0 else 0,
                "p99_latency_ms": sorted_latencies[min(p99_idx, n-1)] if n > 0 else 0,
                "success_rate": success_rate,
                "total_requests": total_requests,
                "success_count": self.success_count,
                "error_count": self.error_count
            }


# Global performance monitor instance
perf_monitor = PerformanceMonitor()