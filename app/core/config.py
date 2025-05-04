from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    # ... other settings ...

    class Config:
        env_file = ".env"