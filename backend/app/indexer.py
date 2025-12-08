import tiktoken
from typing import List, Dict, Any, Tuple
from pathlib import Path
import re
import logging
from .config import settings
from .db_meta import db_manager
from .retriever import qdrant_manager
from openai import OpenAI


class EmbedderAdapter:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.enc = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Using appropriate tokenizer

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text"""
        return len(self.enc.encode(text))

    def chunk_text(self, text: str, chunk_size: int = 600, overlap: int = 80) -> List[str]:
        """
        Split text into chunks of specified size with overlap
        """
        tokens = self.enc.encode(text)
        chunks = []

        start_idx = 0
        while start_idx < len(tokens):
            # Determine the end index for this chunk
            end_idx = start_idx + chunk_size

            # Extract the token slice
            chunk_tokens = tokens[start_idx:end_idx]

            # Decode back to text
            chunk_text = self.enc.decode(chunk_tokens)

            # Add to chunks list
            chunks.append(chunk_text)

            # Move start index forward by chunk_size - overlap
            start_idx = end_idx - overlap

            # Ensure we don't get stuck in an infinite loop
            if start_idx >= len(tokens):
                break

        return chunks

    def extract_headings(self, markdown_text: str) -> List[Tuple[str, str]]:
        """
        Extract headings and their content from markdown text
        Returns list of (heading, content) tuples
        """
        # Split text by headings
        heading_pattern = r'^(#{1,6})\s+(.+)$'
        lines = markdown_text.split('\n')

        sections = []
        current_heading = "Introduction"
        current_content = []

        for line in lines:
            match = re.match(heading_pattern, line.strip())
            if match:
                # Save previous section if it exists
                if current_content:
                    sections.append((current_heading, '\n'.join(current_content).strip()))

                # Start new section
                current_heading = match.group(2).strip()
                current_content = []
            else:
                current_content.append(line)

        # Add the last section
        if current_content:
            sections.append((current_heading, '\n'.join(current_content).strip()))

        return sections

    def clean_markdown(self, markdown_text: str) -> str:
        """
        Clean markdown text by removing special formatting that might interfere with embeddings
        """
        # Remove image references
        cleaned = re.sub(r'!\[.*?\]\(.*?\)', '', markdown_text)
        # Remove links but keep the text
        cleaned = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', cleaned)
        # Remove bold and italic formatting
        cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned)
        cleaned = re.sub(r'\*(.*?)\*', r'\1', cleaned)
        cleaned = re.sub(r'__(.*?)__', r'\1', cleaned)
        cleaned = re.sub(r'_(.*?)_', r'\1', cleaned)

        return cleaned.strip()

    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a text using OpenAI
        """
        try:
            response = self.client.embeddings.create(
                input=text,
                model="text-embedding-3-small"  # Using the model specified in research
            )
            return response.data[0].embedding
        except Exception as e:
            logging.error(f"Error generating embedding: {e}")
            raise

    async def process_document(self, doc_path: str, chunk_size: int = 600, overlap: int = 80) -> List[Dict[str, Any]]:
        """
        Process a document: read, extract headings, chunk, embed
        Returns list of processed chunks with embeddings and metadata
        """
        # Read the document
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Clean the markdown content
        cleaned_content = self.clean_markdown(content)

        # Extract headings and content
        heading_content_pairs = self.extract_headings(cleaned_content)

        all_chunks = []
        for heading, section_content in heading_content_pairs:
            if not section_content.strip():
                continue  # Skip empty sections

            # Chunk the section content
            chunks = self.chunk_text(section_content, chunk_size, overlap)

            for chunk in chunks:
                if not chunk.strip():
                    continue  # Skip empty chunks

                # Count tokens in the chunk
                token_count = self.count_tokens(chunk)

                # Validate token count is within required range
                if token_count < 500 or token_count > 800:
                    # For chunks outside the range, we can still process them but log a warning
                    logging.warning(f"Chunk token count ({token_count}) is outside the 500-800 range for {doc_path}")

                # Create chunk data
                chunk_data = {
                    "doc_path": str(doc_path),
                    "heading": heading,
                    "excerpt": chunk,
                    "token_count": token_count
                }
                all_chunks.append(chunk_data)

        # Generate embeddings for all chunks
        for chunk_data in all_chunks:
            embedding = await self.embed_text(chunk_data["excerpt"])
            chunk_data["embedding"] = embedding

        return all_chunks

    async def upsert_chunks_to_qdrant_and_db(self, chunks: List[Dict[str, Any]], job_id: Optional[str] = None):
        """
        Upsert chunks to Qdrant vector database and store metadata in Neon Postgres
        """
        if not chunks:
            return

        from typing import Optional  # Adding this import

        # Prepare data for Qdrant and Neon
        qdrant_vectors = []
        for idx, chunk in enumerate(chunks):
            # Create a unique ID for this chunk
            import uuid
            chunk_id = str(uuid.uuid4())

            # Prepare Qdrant point
            qdrant_point = {
                "id": chunk_id,
                "vector": chunk["embedding"],
                "payload": {
                    "doc_path": chunk["doc_path"],
                    "heading": chunk["heading"],
                    "excerpt": chunk["excerpt"],
                    "token_count": chunk["token_count"],
                    "created_at": __import__('datetime').datetime.utcnow().isoformat()
                }
            }
            qdrant_vectors.append(qdrant_point)

            # Store metadata in Neon
            await db_manager.insert_chunk(
                vector_id=chunk_id,
                doc_path=chunk["doc_path"],
                heading=chunk["heading"],
                excerpt=chunk["excerpt"],
                token_count=chunk["token_count"]
            )

            # Update indexing job progress if provided
            if job_id:
                # Update the job's processed chunks count
                await db_manager.update_indexing_job_status(job_id, "in_progress", idx + 1)
                logging.info(f"Processed chunk {idx + 1}/{len(chunks)} for job {job_id}")

        # Upsert vectors to Qdrant
        await qdrant_manager.upsert_vectors(qdrant_vectors)


# Global embedder adapter instance
embedder_adapter = EmbedderAdapter()