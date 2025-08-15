import os
from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/musical_instruments")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    # API Settings
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Musical Instruments Platform")
    
    # Environment
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Production domain configuration
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    DOMAIN: str = os.getenv("DOMAIN", "getyourmusicgear.com")
    
    # CORS - Updated for production
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        if self.ENVIRONMENT == "production":
            return [
                f"https://{self.DOMAIN}",
                f"https://www.{self.DOMAIN}",
                "https://getyourmusicgear.onrender.com",
                "http://127.0.0.1:3000",  # For internal nginx proxy
                "http://localhost:3000"   # For internal nginx proxy
            ]
        else:
            return ["http://localhost:3000", "http://localhost:3001"]
    
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Affiliate Programs
    AMAZON_ASSOCIATE_TAG: str = os.getenv("AMAZON_ASSOCIATE_TAG", "")
    THOMANN_AFFILIATE_ID: str = os.getenv("THOMANN_AFFILIATE_ID", "")
    
    # Render.com specific settings
    PORT: int = int(os.getenv("PORT", "8000"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
