"""
    Director Agent - Central orchestrator for the auto-blogging platform
    """
    from typing import Optional, Dict, Any
    from pydantic import BaseModel, Field
    from pydantic_ai import Agent, RunContext
    from tools.supabase_tools import save_blog_post, get_user_settings
    from tools.web_search_tools import search_web
    from tools.publishing_tools import publish_to_wordpress

    class BlogRequest(BaseModel):
        """Structured input for blog creation"""
        user_id: str = Field(description="ID of the requesting user")
        topic: str = Field(description="Main topic of the blog post")
        keywords: list[str] = Field(description="SEO keywords to target")
        content_type: str = Field(description="Type of content to create")
        publish: bool = Field(description="Whether to publish the content")

    class BlogResult(BaseModel):
        """Structured output for blog creation"""
        status: str = Field(description="Operation status")
        message: str = Field(description="Result message")
        content_url: Optional[str] = Field(description="URL of published content")
        content_id: Optional[str] = Field(description="ID of stored content")

    class DirectorDependencies(BaseModel):
        """Shared resources for the Director Agent"""
        supabase_url: str
        supabase_key: str
        wordpress_url: Optional[str]
        wordpress_creds: Optional[Dict[str, str]]

    director_agent = Agent(
        "openai:gpt-4",
        system_prompt="""
        You are an expert SEO Director AI agent. Your responsibilities include:
        1. Analyzing user requests and creating detailed content plans
        2. Coordinating research, writing, and editing processes
        3. Ensuring content meets SEO best practices
        4. Managing the publishing workflow
        """,
        deps_type=DirectorDependencies,
        result_type=BlogResult
    )

    @director_agent.tool
    async def get_user_preferences(ctx: RunContext[DirectorDependencies], user_id: str) -> Dict[str, Any]:
        """Retrieve user preferences from Supabase"""
        return await get_user_settings(ctx, user_id)

    @director_agent.tool
    async def store_content(ctx: RunContext[DirectorDependencies], content: Dict[str, Any]) -> Dict[str, Any]:
        """Store content in Supabase"""
        return await save_blog_post(ctx, content)

    @director_agent.tool
    async def publish_content(ctx: RunContext[DirectorDependencies], content: Dict[str, Any]) -> Dict[str, Any]:
        """Publish content to WordPress"""
        if ctx.deps.wordpress_url and ctx.deps.wordpress_creds:
            return await publish_to_wordpress(ctx, content)
        return {"status": "skipped", "message": "WordPress credentials not configured"}

    async def create_blog_post(request: BlogRequest, deps: DirectorDependencies) -> BlogResult:
        """Orchestrate the blog creation workflow"""
        # Step 1: Get user preferences
        user_prefs = await director_agent.run(
            "Get user preferences for content creation",
            deps=deps,
            tools=[get_user_preferences],
            params={"user_id": request.user_id}
        )

        # Step 2: Conduct research
        research_results = await director_agent.run(
            f"Research topic: {request.topic} with keywords: {', '.join(request.keywords)}",
            deps=deps,
            tools=[search_web],
            params={"query": f"{request.topic} {', '.join(request.keywords)}"}
        )

        # Step 3: Generate content outline
        outline = await director_agent.run(
            f"Create content outline for: {request.topic}",
            deps=deps,
            params={
                "topic": request.topic,
                "keywords": request.keywords,
                "content_type": request.content_type
            }
        )

        # Step 4: Store content
        storage_result = await director_agent.run(
            "Store generated content",
            deps=deps,
            tools=[store_content],
            params={"content": outline.data}
        )

        # Step 5: Publish if requested
        publish_result = {"status": "skipped"}
        if request.publish:
            publish_result = await director_agent.run(
                "Publish content",
                deps=deps,
                tools=[publish_content],
                params={"content": outline.data}
            )

        return BlogResult(
            status="success",
            message="Blog post created successfully",
            content_url=publish_result.get("url"),
            content_id=storage_result.get("id")
        )

    if __name__ == "__main__":
        import asyncio
        from config import settings

        # Example usage
        deps = DirectorDependencies(
            supabase_url=settings.SUPABASE_URL,
            supabase_key=settings.SUPABASE_KEY,
            wordpress_url=settings.WORDPRESS_URL,
            wordpress_creds={
                "username": settings.WORDPRESS_USERNAME,
                "password": settings.WORDPRESS_PASSWORD
            }
        )

        request = BlogRequest(
            user_id="123",
            topic="AI in Healthcare",
            keywords=["AI", "healthcare", "machine learning"],
            content_type="blog post",
            publish=True
        )

        result = asyncio.run(create_blog_post(request, deps))
        print(result)
