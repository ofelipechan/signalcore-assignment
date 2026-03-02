"""Fetch URL tool: fetch page and extract main content with provenance."""

import logging
import re
from html import unescape

import httpx
from readability import Document

from app.config import Settings
from app.models.schemas import FetchUrlToolArgs, Source, ToolResult

logger = logging.getLogger(__name__)


def _extract_date_from_headers(response: httpx.Response) -> str | None:
    """Try to get date from Last-Modified, Date, or other response headers."""
    last_modified = response.headers.get("last-modified")
    if last_modified:
        return last_modified
    date_header = response.headers.get("date")
    if date_header:
        return date_header
    return None


def _extract_date_from_html(html: str) -> str | None:
    """Try to get date from common meta tags in HTML (double and single quotes)."""
    meta_patterns = [
        r'<meta[^>]+property="article:modified_time"[^>]+content="([^"]+)"',
        r'<meta[^>]+content="([^"]+)"[^>]+property="article:modified_time"',
        r'<meta[^>]+property="article:published_time"[^>]+content="([^"]+)"',
        r'<meta[^>]+content="([^"]+)"[^>]+property="article:published_time"',
        r'<meta[^>]+name="date"[^>]+content="([^"]+)"',
        r'<meta[^>]+content="([^"]+)"[^>]+name="date"',
        r'<meta[^>]+property="og:updated_time"[^>]+content="([^"]+)"',
        r'<meta[^>]+content="([^"]+)"[^>]+property="og:updated_time"',
        r"<meta[^>]+content='([^']+)'[^>]+property=['\"]article:published_time['\"]",
        r"<meta[^>]+property=['\"]article:published_time['\"][^>]+content='([^']+)'",
    ]
    for pattern in meta_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _strip_script_style(html: str) -> str:
    """Remove <script>...</script> and <style>...</style> blocks and their content."""
    html = re.sub(r"<script[^>]*>[\s\S]*?</script>", " ", html, flags=re.IGNORECASE)
    html = re.sub(r"<style[^>]*>[\s\S]*?</style>", " ", html, flags=re.IGNORECASE)
    return html


def _html_to_plain_text(html: str) -> str:
    """Strip HTML tags and return plain text."""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    return unescape(text).strip()


async def fetch_url_tool(args: FetchUrlToolArgs) -> ToolResult:
    """
    Fetch a URL and extract main content; return content and provenance (url, title, date).

    Uses httpx for fetch and readability-lxml for main content. On failure returns
    a ToolResult with an error message and empty sources so the agent can retry or report.
    """
    settings = Settings()
    timeout = settings.http_timeout_seconds
    url_str = str(args.url)
    logger.info(f"fetch_url_tool: url={url_str}")

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url_str)
            response.raise_for_status()
    except httpx.TimeoutException:
        logger.warning(f"fetch_url_tool: timeout after {timeout}s for {url_str}")
        return ToolResult(content=f"Error: Request timed out after {timeout}s.", sources=[])
    except httpx.HTTPStatusError as e:
        logger.warning(f"fetch_url_tool: HTTP {e.response.status_code} for {url_str}")
        return ToolResult(content=f"Error: HTTP {e.response.status_code} for {url_str}.", sources=[])
    except httpx.RequestError as e:
        logger.exception(f"fetch_url_tool: request failed for {url_str}: {e}")
        return ToolResult(content=f"Error: Request failed ({e!s}).", sources=[])

    try:
        doc = Document(response.text)
        title = doc.title() or None
        raw_html = getattr(doc, "input", response.text)
        raw_html = _strip_script_style(raw_html)
        content = _html_to_plain_text(raw_html)
        if not content.strip():
            content = "(No main content extracted)"
        content = content[:5000] if len(content) > 5000 else content
    except Exception as e:
        logger.warning(f"fetch_url_tool: readability parse failed for {url_str}: {e}")
        raw_fallback = _strip_script_style(response.text)
        content = _html_to_plain_text(raw_fallback)[:5000] or "(Failed to parse content)"

    source = Source(url=url_str, title=title)
    logger.info(f"fetch_url_tool: done for {url_str}, title={title!r}")
    return ToolResult(content=content, sources=[source])
