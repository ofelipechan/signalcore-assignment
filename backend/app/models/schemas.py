"""Request/response and tool schemas."""

from pydantic import BaseModel, Field, HttpUrl


class ResearchRequest(BaseModel):
    """User research prompt."""

    prompt: str


class Source(BaseModel):
    """Provenance: where information came from."""

    url: str
    title: str | None = None
    source_type: str | None = None  # e.g. vendor_docs, github, comparison_site, community


class ResearchResponse(BaseModel):
    """Agent response with markdown and sources for transparency."""

    markdown: str
    sources: list[Source] = Field(default_factory=list)


class SearchToolArgs(BaseModel):
    """Input for the web search tool."""

    query: str = Field(..., description="Search query to find vendor docs, comparisons, etc.")


class FetchUrlToolArgs(BaseModel):
    """Input for the fetch_url tool."""

    url: HttpUrl = Field(..., description="URL of the page to fetch and extract main content from")


class ToolResult(BaseModel):
    """Internal return type for research tools: content for the LLM and sources for the API."""

    content: str
    sources: list[Source] = Field(default_factory=list)
