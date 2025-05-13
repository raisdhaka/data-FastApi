from pydantic_settings import BaseSettings  # Changed import

class settings(BaseSettings):
    DATABASE_URL: str
    # ... other settings ...

    class Config:
        env_file = ".env"