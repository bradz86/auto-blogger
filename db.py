from supabase import create_client
    from config import settings

    supabase = create_client(settings.supabase_url, settings.supabase_key)

    def save_blog_post(content: dict):
        return supabase.table("blog_posts").insert(content).execute()
