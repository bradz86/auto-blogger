"""
    Keyword Agent - Handles keyword research and optimization
    """
    from pydantic_ai import Agent
    from pydantic import BaseModel

    class KeywordAnalysis(BaseModel):
        primary_keyword: str
        secondary_keywords: list[str]
        search_volume: int
        competition: str

    keyword_agent = Agent(
        "openai:gpt-4",
        system_prompt="""
        You are the Keyword Research Agent. Your role is to:
        1. Identify relevant keywords
        2. Analyze search volume and competition
        3. Suggest keyword variations
        """,
        result_type=KeywordAnalysis
    )
