import re
from typing import List, Dict, Any

def chunk_text(text: str, max_tokens: int = 512, overlap: int = 100) -> List[str]:
    """
    Split text into chunks of approximately max_tokens with overlap.
    This function tries to respect sentence boundaries when possible.
    """
    # Simple token estimation (1 token ~ 4 characters for English text)
    avg_chars_per_token = 4
    max_chars = max_tokens * avg_chars_per_token
    overlap_chars = overlap * avg_chars_per_token

    sentences = re.split(r'[.!?]+\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If adding this sentence would exceed the limit
        if len(current_chunk) + len(sentence) > max_chars:
            if current_chunk:
                chunks.append(current_chunk.strip())

            # Start a new chunk, potentially with overlap from the previous chunk
            if len(sentence) > max_chars:
                # If the sentence itself is too long, split it by length
                for i in range(0, len(sentence), max_chars - overlap_chars):
                    chunk_portion = sentence[i:i + max_chars - overlap_chars]
                    if chunk_portion.strip():
                        chunks.append(chunk_portion.strip())
                # Continue with the last part as the current chunk
                current_chunk = sentence[-(max_chars - overlap_chars):] if len(sentence) > (max_chars - overlap_chars) else ""
            else:
                current_chunk = sentence
        else:
            current_chunk += " " + sentence

    # Add the last chunk if it exists
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Ensure overlap between chunks
    if len(chunks) > 1 and overlap_chars > 0:
        final_chunks = [chunks[0]]
        for i in range(1, len(chunks)):
            prev_chunk_end = final_chunks[-1][-overlap_chars:]
            new_chunk = prev_chunk_end + " " + chunks[i]
            final_chunks.append(new_chunk)
        chunks = final_chunks

    return chunks

def extract_metadata_from_path(file_path: str) -> Dict[str, str]:
    """
    Extract metadata from file path.
    Example: docs/module1/chapter2/section.md -> module="module1", section="section"
    """
    import os
    path_parts = file_path.split(os.sep)

    metadata = {
        "module": "",
        "chapter": "",
        "section": "",
        "url": ""
    }

    # Extract module (second-to-last directory if docs is first)
    if len(path_parts) >= 3 and path_parts[0] == "docs":
        metadata["module"] = path_parts[1] if len(path_parts) > 1 else ""
        metadata["chapter"] = path_parts[2] if len(path_parts) > 2 else ""
        metadata["section"] = os.path.splitext(path_parts[-1])[0] if path_parts else ""
    elif len(path_parts) >= 2:
        metadata["module"] = path_parts[0] if len(path_parts) > 0 else ""
        metadata["section"] = os.path.splitext(path_parts[-1])[0] if path_parts else ""

    # Create URL from path
    metadata["url"] = "/" + "/".join(path_parts).replace(".md", "")

    return metadata