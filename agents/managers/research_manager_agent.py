"""
    Research Manager Agent - Handles all research-related tasks
    """
    from pydantic_ai import Agent, RunContext
    from pydantic import BaseModel
    from typing import List

    class ResearchData(BaseModel):
        sources: List[str]
        key_points: List[str]
        citations: List[str]

    research_manager = Agent(
        "openai:gpt-4",
        system_prompt="""
        You are the Research Manager. Your role is to:
        1. Gather relevant information
        2. Validate sources
        3. Summarize key points
        """,
        result_type=ResearchData
    )

    @research_manager.tool
    async def search_web(ctx: RunContext, query: str) -> str:
        """Search the web for relevant information"""
        # Implementation would use a web search API
        return f"Search results for {query}"
