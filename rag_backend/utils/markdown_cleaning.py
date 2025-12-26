import re
from typing import Dict, Any

def clean_markdown_content(content: str) -> str:
    """
    Clean markdown content by removing frontmatter, comments, and other non-content elements.
    """
    # Remove YAML frontmatter if present
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # Remove markdown comments (if any)
    content = re.sub(r'^\s*<!--.*?-->\s*$', '', content, flags=re.MULTILINE | re.DOTALL)

    # Remove excessive whitespace while preserving paragraph structure
    content = re.sub(r'\n\s*\n', '\n\n', content)  # Replace multiple newlines with double newline
    content = re.sub(r'^\s+', '', content, flags=re.MULTILINE)  # Remove leading whitespace
    content = re.sub(r'\s+$', '', content, flags=re.MULTILINE)  # Remove trailing whitespace

    return content.strip()

def extract_title_from_markdown(content: str) -> str:
    """
    Extract the title from markdown content (first H1 heading).
    """
    # Look for the first H1 heading
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    return ""

def extract_metadata_from_markdown(content: str) -> Dict[str, Any]:
    """
    Extract metadata from markdown content including title, headings, etc.
    """
    metadata = {
        "title": extract_title_from_markdown(content),
        "headings": []
    }

    # Extract all headings
    heading_pattern = r'^(#{1,6})\s+(.+)$'
    for match in re.finditer(heading_pattern, content, re.MULTILINE):
        level = len(match.group(1))
        heading = match.group(2).strip()
        metadata["headings"].append({
            "level": level,
            "text": heading
        })

    return metadata