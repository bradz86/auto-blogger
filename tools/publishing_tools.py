"""
    Publishing Tools - Demonstrates WordPress integration with error handling
    """
    from typing import Dict
    from pydantic import BaseModel
    from pydantic_ai import RunContext, tool
    import httpx

    class WordPressDeps(BaseModel):
        url: str
        username: str
        password: str

    class PublishResult(BaseModel):
        status: str
        url: Optional[str]
        error: Optional[str]

    @tool
    async def publish_to_wordpress(ctx: RunContext[WordPressDeps], content: Dict[str, Any]) -> PublishResult:
        """
        Publish content to WordPress.

        Args:
            ctx: RunContext containing WordPress credentials
            content: Content to publish

        Returns:
            PublishResult containing operation status
        """
        try:
            async with httpx.AsyncClient() as client:
                # First authenticate
                auth_response = await client.post(
                    f"{ctx.deps.url}/wp-json/jwt-auth/v1/token",
                    data={
                        "username": ctx.deps.username,
                        "password": ctx.deps.password
                    }
                )
                auth_response.raise_for_status()
                token = auth_response.json()["token"]

                # Then publish
                publish_response = await client.post(
                    f"{ctx.deps.url}/wp-json/wp/v2/posts",
                    json=content,
                    headers={"Authorization": f"Bearer {token}"}
                )
                publish_response.raise_for_status()

                return PublishResult(
                    status="success",
                    url=publish_response.json()["link"]
                )
        except Exception as e:
            return PublishResult(
                status="error",
                error=str(e)
            )
