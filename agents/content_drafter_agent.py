"""
    Content Drafter Agent - Creates initial content drafts
    """
    from typing import List, Dict
    from pydantic import BaseModel, Field
    from pydantic_ai import Agent, RunContext

    class DraftRequest(BaseModel):
        """Input for creating content drafts"""
        brief: Dict[str, Any] = Field(description="Content brief")
        word_count: int = Field(1000, description="Target word count")
        placeholder_format: str = Field("[PLACEHOLDER]", description="Format for placeholders")

    class ContentDraft(BaseModel):
        """Structured content draft"""
        title: str = Field(description="Draft title")
        content: str = Field(description="Draft content")
        placeholders: List[str] = Field(description="List of placeholders needing completion")
        word_count: int = Field(description="Actual word count")

    drafter = Agent(
        "openai:gpt-4",
        system_prompt="""
        You are the Content Drafter. Your responsibilities include:
        1. Creating initial content drafts
        2. Identifying areas needing additional information
        3. Following provided style guidelines
        4. Maintaining consistent tone and voice
        """,
        result_type=ContentDraft
    )

    @drafter.tool
    async def format_placeholder(ctx: RunContext, text: str) -> str:
        """Format text as a placeholder"""
        return f"{ctx.deps.placeholder_format}{text}{ctx.deps.placeholder_format}"

    async def create_draft(request: DraftRequest) -> ContentDraft:
        """Create initial content draft"""
        return await drafter.run(
            f"Create content draft based on provided brief",
            params=request.dict(),
            tools=[format_placeholder]
        )
