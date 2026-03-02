"""Research agent: Pydantic AI agent with search and fetch_url tools."""

import logging

from pydantic import HttpUrl
from pydantic_ai import Agent, RunContext, UsageLimits

from app.agent.prompts import load_system_prompt
from app.config import Settings
from app.models.schemas import Source
from app.tools import fetch_url_tool, search_tool
from app.tools import FetchUrlToolArgs, SearchToolArgs

logger = logging.getLogger(__name__)


class ResearchAgent:
    """
    Research agent: runs vendor comparison research using search and fetch_url tools.

    Constructor args define instance defaults; run_research(provider=..., model=...) overrides per call.
    Instantiate with the options you need (e.g. ResearchAgent(provider="openai", model="gpt-4o", max_steps=10)).
    """

    def __init__(
        self,
        *,
        provider: str | None = None,
        model: str | None = None,
        timeout: float = 120,
    ) -> None:
        """
        Args:
            provider: Default LLM provider (e.g. openai, anthropic, openrouter). Falls back to config/env.
            model: Default model id for the provider. Falls back to config/env.
            max_steps: Max agent steps (request limit) per run. Falls back to config max_agent_steps.
            timeout: HTTP timeout in seconds for tool calls. Falls back to config http_timeout_seconds.
        """
        self._provider = provider
        self._model = model
        self._timeout = timeout
        self._agent = self._create_agent()

    def _create_agent(self) -> Agent[list[Source], str]:
        """Build the Pydantic AI agent with system prompt and tools."""
        system_prompt = load_system_prompt()
        default_model = f"{self._provider}:{self._model}"

        agent: Agent[list[Source], str] = Agent(
            default_model,
            deps_type=list[Source],
            system_prompt=system_prompt,
            output_type=str
        )
        self._register_tools(agent)
        return agent

    def _register_tools(self, agent: Agent[list[Source], str]) -> None:
        """Register search and fetch_url as agent tools; collect sources into deps."""

        @agent.tool
        async def search(ctx: RunContext[list[Source]], query: str) -> str:
            """Search the web for vendor docs, comparisons, and discussions.
            Use at most 1–2 times total with broad queries (e.g. "X vs Y vs Z comparison").
            Use fetch_url only for the few most relevant URLs from results.
            """
            query_preview = query[:80] + "..." if len(query) > 80 else query
            logger.info(f"agent tool: search query={query_preview!r}")
            try:
                result = await search_tool(SearchToolArgs(query=query))
                ctx.deps.extend(result.sources)
                logger.info(f"agent tool: search done, sources={len(result.sources)}")
                return result.content
            except Exception as e:
                logger.exception(f"agent tool: search failed: {e}")
                return f"Error: Search failed ({e!s})."

        @agent.tool
        async def fetch_url(ctx: RunContext[list[Source]], url: str) -> str:
            """Fetch a URL and extract main content. Use at most 4 times total; pick the best URLs from search results."""
            logger.info(f"agent tool: fetch_url url={url}")
            try:
                parsed = HttpUrl(url)
            except Exception as e:
                logger.warning(f"agent tool: fetch_url invalid url {url!r}: {e}")
                return f"Error: Invalid URL {url!r}."
            try:
                result = await fetch_url_tool(FetchUrlToolArgs(url=parsed))
                ctx.deps.extend(result.sources)
                logger.info(f"agent tool: fetch_url done for {url}")
                return result.content
            except Exception as e:
                logger.exception(f"agent tool: fetch_url failed for {url}: {e}")
                return f"Error: Fetch failed ({e!s})."

    async def run_research(
        self,
        prompt: str,
    ) -> tuple[str, list[Source]]:
        """
        Run the research agent and return markdown plus sources from tool calls.

        provider/model/max_steps override instance defaults when provided. Returns the actual
        reference URLs collected by the tools.
        """
        sources: list[Source] = []
        resolved_max_steps = Settings().max_agent_steps
        usage_limits = UsageLimits(request_limit=resolved_max_steps)
        logger.info(f"run_research started: prompt_len={len(prompt or '')}, max_steps={resolved_max_steps}")
        try:
            result = await self._agent.run(
                prompt,
                deps=sources,
                usage_limits=usage_limits,
            )
            markdown = result.output if result.output is not None else ""
            logger.info(f"run_research completed: sources={len(sources)}, markdown_len={len(markdown)}")
            return markdown, sources
        except Exception as e:
            logger.exception(f"run_research failed: {e}")
            raise
