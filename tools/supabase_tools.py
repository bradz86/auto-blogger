"""
    Supabase Tools - Demonstrates PydanticAI's Function Tools with Supabase integration
    """
    from typing import Optional, Dict, Any
    from pydantic import BaseModel
    from pydantic_ai import RunContext, tool
    from supabase import create_client

    class SupabaseDeps(BaseModel):
        url: str
        key: str

    class BlogPost(BaseModel):
        """Represents a blog post structure"""
        title: str
        content: str
        author: str
        tags: list[str]

    @tool
    async def save_blog_post(ctx: RunContext[SupabaseDeps], post: BlogPost) -> Dict[str, Any]:
        """
        Save a blog post to Supabase.

        Args:
            ctx: RunContext containing Supabase credentials
            post: BlogPost to save

        Returns:
            Dictionary containing operation status and post ID
        """
        supabase = create_client(ctx.deps.url, ctx.deps.key)
        try:
            result = supabase.table("blog_posts").insert(post.dict()).execute()
            return {
                "status": "success",
                "id": result.data[0]["id"],
                "created_at": result.data[0]["created_at"]
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    @tool
    async def get_user_settings(ctx: RunContext[SupabaseDeps], user_id: str) -> Dict[str, Any]:
        """
        Retrieve user settings from Supabase.

        Args:
            ctx: RunContext containing Supabase credentials
            user_id: ID of the user to retrieve settings for

        Returns:
            Dictionary containing user settings
        """
        supabase = create_client(ctx.deps.url, ctx.deps.key)
        try:
            result = supabase.table("user_settings").select("*").eq("user_id", user_id).execute()
            return result.data[0] if result.data else {}
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
