"""
    Content Brief Manager Agent - Creates structured content briefs
    """
    from typing import List, Dict
    from pydantic import BaseModel, Field
    from pydantic_ai import Agent

    class ContentBriefRequest(BaseModel):
        """Input for creating content briefs"""
        research_data: Dict[str, Any] = Field(description="Research findings")
        content_type: str = Field(description="Type of content to create")
        target_audience: str = Field(description="Intended audience")
        tone: str = Field("professional", description="Desired tone of voice")

    class ContentBrief(BaseModel):
        """Structured content brief"""
        title: str = Field(description="Proposed title")
        sections: List[Dict[str, str]] = Field(description="Content sections")
        keywords: List[str] = Field(description="Target keywords")
        references: List[str] = Field(description="Reference materials")
        style_guide: Dict[str, str] = Field(description="Style guidelines")

    brief_manager = Agent(
        "openai:gpt-4",
        system_prompt="""
        You are the Content Brief Manager. Your responsibilities include:
        1. Analyzing research data
        2. Creating detailed content outlines
        3. Specifying tone and style guidelines
        4. Ensuring alignment with content strategy
        """,
        result_type=ContentBrief
    )

    async def create_brief(request: ContentBriefRequest) -> ContentBrief:
        """Create a content brief from research data"""
        return await brief_manager.run(
            f"Create content brief for {request.content_type}",
            params=request.dict()
        )
