"""
    Main entry point for the application
    """
    from agents.director_agent import director_agent
    from agents.managers.research_manager_agent import research_manager
    from tools.supabase_tools import save_blog_post

    async def generate_blog(topic: str):
        # Step 1: Create outline
        outline = await director_agent.run(f"Create outline for: {topic}")
        
        # Step 2: Conduct research
        research = await research_manager.run(f"Research: {topic}")
        
        # Step 3: Save to database
        await save_blog_post({
            "topic": topic,
            "outline": outline.data.dict(),
            "research": research.data.dict()
        })

        return {"status": "success", "outline": outline, "research": research}

    if __name__ == "__main__":
        import asyncio
        result = asyncio.run(generate_blog("AI in Healthcare"))
        print(result)
