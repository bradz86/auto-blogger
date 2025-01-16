import os
    from pydantic import BaseSettings

    class Settings(BaseSettings):
        supabase_url: str
        supabase_key: str
        openai_api_key: str

        class Config:
            env_file = ".env"

    settings = Settings()
