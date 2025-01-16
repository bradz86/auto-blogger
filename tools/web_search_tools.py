"""
    Web Search Tools - Demonstrates API integration with fallback
    """
    from typing import Optional, Dict
    from pydantic import BaseModel
    from pydantic_ai import RunContext, tool
    import httpx

    class WebSearchDeps(BaseModel):
        api_key: Optional[str]

    @tool
    async def search_web(ctx: RunContext[WebSearchDeps], query: str) -> Dict[str, Any]:
        """
        Search the web using Brave Search API with fallback to dummy data.

        Args:
            ctx: RunContext containing API key
            query: Search query string

        Returns:
            Dictionary containing search results
        """
        if ctx.deps.api_key:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(
                        "https://api.search.brave.com/res/v1/web/search",
                        params={"q": query},
                        headers={"X-Subscription-Token": ctx.deps.api_key}
                    )
                    response.raise_for_status()
                    return response.json()
                except Exception as e:
                    return {
                        "status": "error",
                        "error": str(e)
                    }
        else:
            # Fallback to dummy data
            return {
                "status": "success",
                "results": [
                    {
                        "title": f"Dummy result for {query}",
                        "url": "https://example.com",
                        "description": "This is a dummy result because no API key was provided"
                    }
                ]
            }
