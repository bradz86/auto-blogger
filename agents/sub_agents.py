from pydantic_ai import Agent
    from pydantic import BaseModel
    from config import settings

    class DraftContent(BaseModel):
        introduction: str
        body: str
        conclusion: str

    drafting_agent = Agent(
        "openai:gpt-4",
        system_prompt="You are a content writer. Create well-structured blog content.",
        result_type=DraftContent
    )
