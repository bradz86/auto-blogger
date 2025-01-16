from pydantic_ai import Agent, RunContext
    from pydantic import BaseModel
    from typing import List
    from config import settings

    class ResearchData(BaseModel):
        sources: List[str]
        key_points: List[str]

    research_agent = Agent(
        "openai:gpt-4",
        system_prompt="You are a research manager. Gather and summarize information.",
        result_type=ResearchData
    )

    @research_agent.tool
    async def search_web(ctx: RunContext, query: str) -> str:
        # Implement web search functionality
        return f"Search results for {query}"
