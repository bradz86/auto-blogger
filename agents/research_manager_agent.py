"""
    Research Manager Agent - Handles all research-related tasks
    """
    from typing import List, Optional, Dict
    from pydantic import BaseModel, Field
    from pydantic_ai import Agent, RunContext
    from tools.web_search_tools import search_web

    class ResearchRequest(BaseModel):
        """Structured input for research tasks"""
        topic: str = Field(description="Main research topic")
        keywords: List[str] = Field(description="Keywords to focus on")
        max_results: Optional[int] = Field(5, description="Maximum results to return")

    class ResearchResult(BaseModel):
        """Structured output for research tasks"""
        topic: str = Field(description="Research topic")
        sources: List[str] = Field(description="List of sources used")
        key_points: List[str] = Field(description="Key findings from research")
        competitor_analysis: Optional[Dict[str, Any]] = Field(description="Competitor analysis data")
        keyword_analysis: Optional[Dict[str, Any]] = Field(description="Keyword research data")

    class ResearchDependencies(BaseModel):
        """Shared resources for research"""
        web_search_api_key: Optional[str]
        supabase_url: str
        supabase_key: str

    research_manager = Agent(
        "openai:gpt-4",
        system_prompt="""
        You are the Research Manager Agent. Your responsibilities include:
        1. Conducting comprehensive research on given topics
        2. Analyzing and synthesizing information from multiple sources
        3. Coordinating with sub-agents for specialized research
        4. Presenting findings in a structured format
        """,
        deps_type=ResearchDependencies,
        result_type=ResearchResult
    )

    @research_manager.tool
    async def conduct_web_search(ctx: RunContext[ResearchDependencies], query: str) -> Dict[str, Any]:
        """Conduct web search using available tools"""
        return await search_web(ctx, query)

    async def keyword_analysis(ctx: RunContext[ResearchDependencies], keywords: List[str]) -> Dict[str, Any]:
        """Stub for KeywordAgent integration"""
        # TODO: Implement actual KeywordAgent integration
        return {
            "primary_keyword": keywords[0] if keywords else "N/A",
            "secondary_keywords": keywords[1:] if len(keywords) > 1 else [],
            "search_volume": "N/A",
            "competition": "N/A"
        }

    async def competitor_analysis(ctx: RunContext[ResearchDependencies], topic: str) -> Dict[str, Any]:
        """Stub for CompetitorResearchAgent integration"""
        # TODO: Implement actual CompetitorResearchAgent integration
        return {
            "top_competitors": [],
            "content_gaps": [],
            "opportunities": []
        }

    async def conduct_research(request: ResearchRequest, deps: ResearchDependencies) -> ResearchResult:
        """Orchestrate the research workflow"""
        # Step 1: Conduct web search
        search_results = await research_manager.run(
            f"Search for information about: {request.topic}",
            deps=deps,
            tools=[conduct_web_search],
            params={"query": f"{request.topic} {', '.join(request.keywords)}"}
        )

        # Step 2: Perform keyword analysis
        keyword_data = await keyword_analysis(deps, request.keywords)

        # Step 3: Perform competitor analysis
        competitor_data = await competitor_analysis(deps, request.topic)

        # Step 4: Aggregate results
        return ResearchResult(
            topic=request.topic,
            sources=search_results.data.get("results", [])[:request.max_results],
            key_points=[
                "Key point 1 based on research",
                "Key point 2 based on research",
                "Key point 3 based on research"
            ],
            competitor_analysis=competitor_data,
            keyword_analysis=keyword_data
        )

    if __name__ == "__main__":
        import asyncio
        from config import settings

        # Example usage
        deps = ResearchDependencies(
            web_search_api_key=settings.BRAVE_API_KEY,
            supabase_url=settings.SUPABASE_URL,
            supabase_key=settings.SUPABASE_KEY
        )

        request = ResearchRequest(
            topic="AI in Healthcare",
            keywords=["AI", "healthcare", "machine learning"],
            max_results=3
        )

        result = asyncio.run(conduct_research(request, deps))
        print(result)
