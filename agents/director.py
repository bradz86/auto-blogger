from pydantic_ai import Agent
    from pydantic import BaseModel
    from config import settings

    class BlogOutline(BaseModel):
        title: str
        sections: list[str]

    director_agent = Agent(
        "openai:gpt-4",
        system_prompt="You are a content director. Create blog outlines based on topics.",
        result_type=BlogOutline
    )
