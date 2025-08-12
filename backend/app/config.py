from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/musical_instruments"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Musical Instruments API"
    
    # Environment
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # CORS
    ALLOWED_HOSTS: list = ["*"]
    
    # Affiliate Programs
    AMAZON_ASSOCIATE_TAG: str = ""
    THOMANN_AFFILIATE_ID: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
