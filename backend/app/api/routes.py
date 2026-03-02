"""Research API routes."""

import logging

from fastapi import APIRouter, HTTPException
from pydantic_ai import UsageLimitExceeded

from app.agent import ResearchAgent
from app.config import Settings
from app.models.schemas import ResearchRequest, ResearchResponse

logger = logging.getLogger(__name__)
_settings = Settings()
router = APIRouter()


@router.get(
    "/health",
    summary="Health check",
    description="Returns 200 if the API is up.",
)
async def health() -> dict[str, str]:
    """Health check for load balancers and monitoring."""
    return {"status": "ok"}


@router.post(
    "/research",
    response_model=ResearchResponse,
    summary="Run research",
    description=(
        "Run the research agent with the given prompt. Returns markdown and a list of sources "
        "(url, title, source_type, date) so the UI can show where information came from and how recent it is."
    ),
)
async def run_research(request: ResearchRequest) -> ResearchResponse:
    """
    Run the research agent and return markdown plus sources.

    Request body: prompt (required).
    Response: markdown (agent answer), sources (list of {url, title?, source_type?, date?}).
    Each source includes at least url; date is present or \"unknown\".
    """
    prompt_len = len(request.prompt) if request.prompt else 0
    logger.info(f"research request started: prompt_len={prompt_len}")
    try:
        research_agent = ResearchAgent(
            provider=_settings.default_llm_provider,
            model=_settings.default_llm_model,
        )
        markdown, sources = await research_agent.run_research(
            prompt=request.prompt
        )
        logger.info(f"research request completed: sources_count={len(sources)}, markdown_len={len(markdown or '')}")
        return ResearchResponse(markdown=markdown, sources=sources)
    except UsageLimitExceeded as e:
        logger.warning(f"research request hit step limit: {e}")
        raise HTTPException(
            status_code=429,
            detail=(
                "Research hit the maximum step limit. Try a more focused prompt, "
                "or increase MAX_AGENT_STEPS in backend/.env."
            ),
        ) from e
    except Exception as e:
        logger.exception(f"research request failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Research agent failed: {e!s}",
        ) from e
