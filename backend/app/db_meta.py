import asyncpg
from typing import List, Optional, Dict, Any
from .config import settings
import logging
from datetime import datetime
import uuid


class DatabaseManager:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Establish connection to Neon Postgres database"""
        try:
            self.pool = await asyncpg.create_pool(
                settings.neon_db_url,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            logging.info("Connected to Neon Postgres database")
        except Exception as e:
            logging.error(f"Failed to connect to database: {e}")
            raise

    async def disconnect(self):
        """Close database connection"""
        if self.pool:
            await self.pool.close()

    async def create_tables(self):
        """Create required tables if they don't exist"""
        create_chunks_table = """
        CREATE TABLE IF NOT EXISTS chunks (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            vector_id TEXT NOT NULL,
            doc_path TEXT NOT NULL,
            heading TEXT,
            excerpt TEXT NOT NULL,
            token_count INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        create_indexing_jobs_table = """
        CREATE TABLE IF NOT EXISTS indexing_jobs (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'pending',
            docs_path TEXT NOT NULL,
            chunk_size INTEGER NOT NULL,
            overlap INTEGER NOT NULL,
            total_chunks INTEGER NOT NULL DEFAULT 0,
            processed_chunks INTEGER NOT NULL DEFAULT 0,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        );
        """

        async with self.pool.acquire() as conn:
            await conn.execute(create_chunks_table)
            await conn.execute(create_indexing_jobs_table)
            logging.info("Database tables created/verified")

    async def insert_chunk(self, vector_id: str, doc_path: str, heading: str, excerpt: str, token_count: int):
        """Insert a content chunk into the database"""
        query = """
        INSERT INTO chunks (vector_id, doc_path, heading, excerpt, token_count)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id
        """
        async with self.pool.acquire() as conn:
            result = await conn.fetchval(query, vector_id, doc_path, heading, excerpt, token_count)
            return result

    async def get_chunks_by_doc_path(self, doc_path: str) -> List[Dict[str, Any]]:
        """Retrieve all chunks for a specific document path"""
        query = """
        SELECT id, vector_id, doc_path, heading, excerpt, token_count, created_at
        FROM chunks
        WHERE doc_path = $1
        ORDER BY created_at
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, doc_path)
            return [dict(row) for row in rows]

    async def get_chunks_by_vector_ids(self, vector_ids: List[str]) -> List[Dict[str, Any]]:
        """Retrieve chunks by their vector IDs"""
        query = """
        SELECT id, vector_id, doc_path, heading, excerpt, token_count, created_at
        FROM chunks
        WHERE vector_id = ANY($1::text[])
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, vector_ids)
            return [dict(row) for row in rows]

    async def create_indexing_job(self, docs_path: str, chunk_size: int, overlap: int, total_chunks: int) -> str:
        """Create a new indexing job record"""
        query = """
        INSERT INTO indexing_jobs (docs_path, chunk_size, overlap, total_chunks)
        VALUES ($1, $2, $3, $4)
        RETURNING id
        """
        async with self.pool.acquire() as conn:
            job_id = await conn.fetchval(query, docs_path, chunk_size, overlap, total_chunks)
            return str(job_id)

    async def update_indexing_job_status(self, job_id: str, status: str, processed_chunks: Optional[int] = None):
        """Update indexing job status and progress"""
        query = """
        UPDATE indexing_jobs
        SET status = $1, processed_chunks = COALESCE($2, processed_chunks), completed_at = CASE WHEN $1 = 'completed' THEN CURRENT_TIMESTAMP ELSE completed_at END
        WHERE id = $3
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, status, processed_chunks, job_id)

    async def create_indexing_job(self, docs_path: str, chunk_size: int, overlap: int, total_chunks: int) -> str:
        """Create a new indexing job record"""
        query = """
        INSERT INTO indexing_jobs (docs_path, chunk_size, overlap, total_chunks)
        VALUES ($1, $2, $3, $4)
        RETURNING id
        """
        async with self.pool.acquire() as conn:
            job_id = await conn.fetchval(query, docs_path, chunk_size, overlap, total_chunks)
            return str(job_id)

    async def update_indexing_job_status(self, job_id: str, status: str, processed_chunks: Optional[int] = None):
        """Update indexing job status and progress"""
        query = """
        UPDATE indexing_jobs
        SET status = $1, processed_chunks = COALESCE($2, processed_chunks), completed_at = CASE WHEN $1 = 'completed' THEN CURRENT_TIMESTAMP ELSE completed_at END
        WHERE id = $3
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, status, processed_chunks, job_id)

    async def get_indexing_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get indexing job details"""
        query = """
        SELECT id, status, docs_path, chunk_size, overlap, total_chunks, processed_chunks, started_at, completed_at
        FROM indexing_jobs
        WHERE id = $1
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, job_id)
            return dict(row) if row else None


# Global database manager instance
db_manager = DatabaseManager()