"""
    Content Writer Agent - Finalizes and polishes content
    """
    from typing import List, Dict
    from pydantic import BaseModel, Field
    from pydantic_ai import Agent

    class FinalContentRequest(BaseModel):
        """Input for finalizing content"""
        draft: Dict[str, Any] = Field(description="Content draft")
        seo_requirements: Dict[str, Any] = Field(description="SEO specifications")
        style_guide: Dict[str, str] = Field(description="Style guidelines")

    class FinalContent(BaseModel):
        """Structured final content"""
        title: str = Field(description="Final title")
        content: str = Field(description="Final content")
        meta_description: str = Field(description="SEO meta description")
        headings: List[str] = Field(description="Content headings")
        word_count: int = Field(description="Final word count")
        seo_score: float = Field(description="SEO optimization score")

    writer = Agent(
        "openai:gpt-4",
        system_prompt="""
        You are the Content Writer. Your responsibilities include:
        1. Polishing and finalizing content
        2. Ensuring SEO best practices
        3. Verifying style guide compliance
        4. Adding necessary references and citations
        """,
        result_type=FinalContent
    )

    async def finalize_content(request: FinalContentRequest) -> FinalContent:
        """Finalize and polish content"""
        # Example of streaming response handling (commented out)
        # async for chunk in writer.run_streaming(
        #     f"Finalize content based on provided draft",
        #     params=request.dict()
        # ):
        #     # Process chunks incrementally
        #     print(f"Received chunk: {chunk}")
        
        return await writer.run(
            f"Finalize content based on provided draft",
            params=request.dict()
        )
