"""Web search tool using Tavily API."""

import logging

from tavily import AsyncTavilyClient

from app.config import Settings
from app.models.schemas import SearchToolArgs, Source, ToolResult

logger = logging.getLogger(__name__)


async def search_tool(args: SearchToolArgs) -> ToolResult:
    """
    Search the web via Tavily API; return a summary for the LLM and sources with provenance.

    Each result includes url and title. If the API key is not configured
    or the request fails, returns a ToolResult with an error message and empty sources.
    """
    query = args.query or ""
    logger.info(f"search_tool: query={(query[:100] + '...' if len(query) > 100 else query)!r}")
    settings = Settings()
    max_results = settings.search_max_results
    description_max_len = settings.search_description_max_len
    if not settings.tavily_api_key or not settings.tavily_api_key.strip():
        logger.warning("search_tool: Tavily API key not configured")
        return ToolResult(content="Error: Tavily API key not configured.", sources=[])

    try:
        client = AsyncTavilyClient(api_key=settings.tavily_api_key.strip())
        response = await client.search(
            query=args.query,
            search_depth="basic",
            max_results=max_results,
        )
    except Exception as e:
        logger.exception(f"search_tool: Tavily search failed: {e}")
        return ToolResult(content=f"Error: Tavily search failed ({e!s}).", sources=[])

    results = response.get("results") if isinstance(response, dict) else []
    if not isinstance(results, list):
        results = []

    sources: list[Source] = []
    parts: list[str] = []

    for i, item in enumerate(results[:max_results]):
        if not isinstance(item, dict):
            continue
        url_str = item.get("url") or ""
        title = item.get("title") or ""
        content_snippet = item.get("content") or ""
        if isinstance(content_snippet, str) and len(content_snippet) > description_max_len:
            content_snippet = content_snippet[:description_max_len] + "..."

        sources.append(
            Source(url=url_str, title=title or None)
        )
        parts.append(f"[{i + 1}] Title: {title}\nURL: {url_str}\nContent: {content_snippet}")

    content = "\n\n".join(parts) if parts else "No search results found."
    logger.info(f"search_tool: done, results={len(sources)}")
    return ToolResult(content=content, sources=sources)
