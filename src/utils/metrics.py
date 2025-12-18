from typing import Dict, Any
from datetime import datetime
from src.utils.logging import get_logger
from dataclasses import dataclass
from enum import Enum
import time


class QueryType(Enum):
    INFORMATIONAL = "informational"
    PROCEDURAL = "procedural"
    COMPARATIVE = "comparative"
    EXPLANATORY = "explanatory"


@dataclass
class QueryMetrics:
    query_id: str
    query_text: str
    query_type: QueryType
    response_time_ms: float
    tokens_used: int
    context_chunks_used: int
    sources_cited: int
    timestamp: datetime
    success: bool
    error_message: str = None


class MetricsCollector:
    """
    Service for collecting and monitoring query performance metrics
    """
    def __init__(self):
        self.logger = get_logger(__name__)
        self.metrics: list[QueryMetrics] = []

    def record_query(
        self,
        query_id: str,
        query_text: str,
        query_type: QueryType,
        start_time: float,
        tokens_used: int,
        context_chunks_used: int,
        sources_cited: int,
        success: bool,
        error_message: str = None
    ):
        """
        Record metrics for a processed query
        """
        response_time_ms = (time.time() - start_time) * 1000

        metric = QueryMetrics(
            query_id=query_id,
            query_text=query_text,
            query_type=query_type,
            response_time_ms=response_time_ms,
            tokens_used=tokens_used,
            context_chunks_used=context_chunks_used,
            sources_cited=sources_cited,
            timestamp=datetime.now(),
            success=success,
            error_message=error_message
        )

        self.metrics.append(metric)

        # Log performance metrics
        self.logger.info(
            f"Query {query_id} completed: "
            f"response_time={response_time_ms:.2f}ms, "
            f"tokens={tokens_used}, "
            f"context_chunks={context_chunks_used}, "
            f"sources_cited={sources_cited}, "
            f"success={success}"
        )

    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get a summary of performance metrics
        """
        if not self.metrics:
            return {"message": "No metrics collected yet"}

        successful_queries = [m for m in self.metrics if m.success]
        if not successful_queries:
            return {"message": "No successful queries yet"}

        avg_response_time = sum(m.response_time_ms for m in successful_queries) / len(successful_queries)
        avg_tokens = sum(m.tokens_used for m in successful_queries) / len(successful_queries)
        avg_context_chunks = sum(m.context_chunks_used for m in successful_queries) / len(successful_queries)

        success_rate = len(successful_queries) / len(self.metrics) * 100

        return {
            "total_queries": len(self.metrics),
            "successful_queries": len(successful_queries),
            "success_rate_percent": success_rate,
            "average_response_time_ms": avg_response_time,
            "average_tokens_used": avg_tokens,
            "average_context_chunks": avg_context_chunks,
            "recent_queries_count": len(self.metrics[-10:])  # Last 10 queries
        }

    def get_slow_queries(self, threshold_ms: float = 2000) -> list[QueryMetrics]:
        """
        Get queries that took longer than the threshold
        """
        return [m for m in self.metrics if m.response_time_ms > threshold_ms]

    def get_error_queries(self) -> list[QueryMetrics]:
        """
        Get queries that resulted in errors
        """
        return [m for m in self.metrics if not m.success]


# Global instance
metrics_collector = MetricsCollector()